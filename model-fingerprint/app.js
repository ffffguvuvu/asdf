/* واجهة كاشف بصمة النموذج — تستهلك engine.js */
(function(){
  "use strict";
  const E = window.MFP;
  const KEY = "mfp.v2";
  const VERDICTS = ["yes","part","no"];   // تُستخدم في sanitize أدناه — يجب تعريفها قبلها
  const MAX_NAME = 60;

  /* ---------- الحالة ---------- */
  const isPlainObj = o => !!o && typeof o === "object" && !Array.isArray(o);
  const FRESH = () => ({ current:"مساعد أ", subjects:{ "مساعد أ":{ responses:{}, overrides:{} } } });

  /** يُطهّر أي حالة قادمة من التخزين: أشكال ناقصة، أنواع خاطئة، قيم خبيثة */
  function sanitize(d){
    if (!isPlainObj(d) || !isPlainObj(d.subjects)) return FRESH();
    const subjects = {};
    for (const rawName of Object.keys(d.subjects)){
      const name = String(rawName).trim().slice(0, MAX_NAME);
      if (!name || subjects[name]) continue;
      const src = d.subjects[rawName];
      const responses = {}, overrides = {};
      if (isPlainObj(src)){
        if (isPlainObj(src.responses))
          for (const k of Object.keys(src.responses)){
            const v = src.responses[k];
            if (v != null && (typeof v === "string" || typeof v === "number")) responses[k] = String(v);
          }
        if (isPlainObj(src.overrides))
          for (const k of Object.keys(src.overrides))
            if (VERDICTS.indexOf(src.overrides[k]) !== -1) overrides[k] = src.overrides[k];
      }
      subjects[name] = { responses, overrides };
    }
    if (!Object.keys(subjects).length) return FRESH();
    let current = typeof d.current === "string" ? d.current.trim() : "";
    if (!subjects[current]) current = Object.keys(subjects)[0];   // إصلاح المؤشر المعلّق
    return { current, subjects };
  }

  let DB = load();
  function load(){
    try { return sanitize(JSON.parse(localStorage.getItem(KEY))); }
    catch(e){
      // لا نبتلع الخطأ صامتين: التخزين التالف يختلف عن خطأ برمجي
      if (typeof console !== "undefined" && console.warn)
        console.warn("[mfp] تعذّر تحميل الحالة المحفوظة:", e && e.message);
      return FRESH();
    }
  }
  /** الحفظ لا يجوز أن يُسقط التطبيق (امتلاء الحصة / وضع التصفّح الخاص) */
  function save(){
    try { localStorage.setItem(KEY, JSON.stringify(DB)); return true; }
    catch(e){ if (!save.warned){ save.warned = true; toast("تعذّر الحفظ محليًا — الجلسة تعمل بلا حفظ"); } return false; }
  }
  /** لا يعيد undefined أبدًا */
  function S(){
    if (!DB.subjects[DB.current]) DB = sanitize(DB);
    return DB.subjects[DB.current];
  }

  /* ---------- أدوات ---------- */
  const $ = s => document.querySelector(s);
  const ESC_MAP = { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;", "/":"&#47;", "`":"&#96;" };
  const esc = s => String(s == null ? "" : s).replace(/[&<>"'\/`]/g, c => ESC_MAP[c]);
  const LBL = { yes:"✅ نجح", part:"🟡 جزئيًا", no:"❌ فشل", unknown:"⬜ بانتظار الرد" };
  function toast(m){ const t=$("#toast"); t.textContent=m; t.classList.add("on"); setTimeout(()=>t.classList.remove("on"),1700); }
  function copy(txt){
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject())
      .then(()=>toast("تم النسخ ✅"))
      .catch(()=>{ const a=document.createElement("textarea"); a.value=txt; document.body.appendChild(a);
                   a.select(); document.execCommand("copy"); a.remove(); toast("تم النسخ ✅"); });
  }

  /* نتيجة نهائية = التجاوز اليدوي إن وُجد، وإلا الحكم الآلي */
  function finalResults(subj){
    const auto = E.gradeAll(subj.responses);
    const out = {};
    for (const id of Object.keys(auto)){
      const o = subj.overrides[id];
      out[id] = (VERDICTS.indexOf(o) !== -1)
        ? { verdict:o, reason:"حكم يدوي منك (تجاوز الحكم الآلي).", manual:true }
        : auto[id];
    }
    return out;
  }
  function effectiveResponses(subj){
    // لحساب الملف التعريفي مع احترام التجاوزات: نمرّر الردود، ثم نُبدّل النتائج
    const p = E.buildProfile(subj.responses);
    const fin = finalResults(subj);
    if (Object.keys(subj.overrides).length){
      // إعادة بناء الدرجات اعتمادًا على النتائج النهائية
      const SC = { yes:1, part:.5, no:0, unknown:null };
      for (const k of Object.keys(E.GROUPS)){
        const vals = E.GROUPS[k].ids.map(id => SC[fin[id].verdict]).filter(v => v!==null && v!==undefined);
        p.scores[k] = vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : null;
      }
      const W = { agency:1.2, net:.9, media:.8, knowledge:.7, memory:.9, reason:1.6, honesty:1.6, obedience:1.1, identity:0 };
      let n=0,d=0; for(const k of Object.keys(E.GROUPS)){ if(p.scores[k]===null||!W[k])continue; n+=p.scores[k]*W[k]; d+=W[k]; }
      p.overall = d ? Math.round(n/d*100) : null;
      p.tested = Object.values(fin).filter(r=>r.verdict!=="unknown").length;
      p.coverage = p.tested / E.PROBES.length;
      p.confidence = p.coverage>=.8 ? "عالية" : p.coverage>=.5 ? "متوسطة" : "منخفضة";
    }
    p.results = fin;
    return p;
  }

  /* ---------- بناء بطاقات الاختبارات ---------- */
  function renderProbes(){
    const subj = S(), fin = finalResults(subj);
    let html = "", lastG = null;
    E.PROBES.forEach((p,i) => {
      if (p.group !== lastG){
        html += `<div class="gh"><h2>${E.GROUPS[p.group].label}</h2>
                 <span class="tag">${E.GROUPS[p.group].ids.length} اختبارات</span></div>`;
        lastG = p.group;
      }
      const r = fin[p.id], v = r.verdict;
      html += `
      <div class="card ${v}" id="card-${p.id}">
        <div class="ctop">
          <div class="n">${i+1}</div>
          <div style="flex:1">
            <p class="ttl">${p.title}</p>
            <div class="rev">🎯 ${p.reveals}</div>
          </div>
          <button class="mini" data-copy="${p.id}">📋 نسخ السؤال</button>
        </div>
        <pre class="q">${esc(p.prompt)}</pre>
        <textarea data-in="${p.id}" placeholder="الصق هنا ردّ المساعد كما هو… والتصحيح يتم تلقائيًا.">${esc(subj.responses[p.id]||"")}</textarea>
        <div class="verdict">
          <span class="v ${v}">${LBL[v]}${r.manual?" (يدوي)":""}</span>
          <span class="why">${esc(r.reason)}</span>
          <span class="ovr"><b>تجاوز:</b>
            ${["yes","part","no"].map(k=>`<span class="mini ${subj.overrides[p.id]===k?"on":""}" data-ovr="${p.id}:${k}">${LBL[k].slice(0,2)}</span>`).join("")}
            <span class="mini ${!subj.overrides[p.id]?"on":""}" data-ovr="${p.id}:auto">آلي</span>
          </span>
        </div>
      </div>`;
    });
    $("#probes").innerHTML = html;
  }

  /* ---------- اللوحة ---------- */
  const COLOR = s => s>=.8 ? "var(--acc)" : s>=.5 ? "var(--warn)" : "var(--bad)";
  function renderPanel(){
    const p = effectiveResponses(S());
    $("#cnt").textContent = `${p.tested} / ${p.total}`;
    $("#pbar").style.width = (p.coverage*100)+"%";

    const sc = p.overall;
    const meters = Object.keys(E.GROUPS).map(k => {
      const s = p.scores[k];
      return `<div class="m"><span class="t">${E.GROUPS[k].label}</span>
        <span class="b"><i style="width:${s===null?0:s*100}%;background:${s===null?"#2a3a60":COLOR(s)}"></i></span>
        <span class="p" style="color:${s===null?"var(--mut)":COLOR(s)}">${s===null?"—":Math.round(s*100)+"%"}</span></div>`;
    }).join("");

    const st = p.style;
    const kvs = [
      ["نوع النظام", p.sysType],
      ["الثقة في النتيجة", p.confidence],
      ["قطع المعرفة", p.cutoffYear || "—"],
      ["الإسهاب", st ? st.verbosity : "—"],
      ["التنسيق", st ? st.formatting : "—"],
      ["النبرة", st ? st.tone : "—"]
    ].map(([a,b]) => `<div class="kv"><b>${a}</b><span>${b}</span></div>`).join("");

    const flagged = Object.entries(p.results).filter(([,r]) => r.verdict==="no" || (r.reason||"").includes("مشبوه"));

    $("#panel").innerHTML = `
      <div class="ring">
        <div class="big" style="color:${sc===null?"var(--mut)":COLOR(sc/100)}">${sc===null?"—":sc}<small>/100</small></div>
        <div style="font-size:12.5px;color:var(--mut)">الدرجة الإجمالية<br>مرجّحة على المحاور المُختبَرة فقط</div>
      </div>
      <div class="meters">${meters}</div>
      <div class="kvs">${kvs}</div>
      ${p.traits.length ? `<ul class="traits">${p.traits.map(t=>`<li>${t}</li>`).join("")}</ul>` : ""}
      ${flagged.length ? `<div class="warnbox">🚩 نقاط تستحق انتباهك: ${flagged.length} اختبارًا فاشلًا — أبرزها «${E.PROBES.find(x=>x.id===flagged[0][0]).title}».</div>` : ""}
      <div class="warnbox" style="background:#101c33;border-color:#27416b;color:#9fb6de">
        ⚠️ ${p.disclaimer}
      </div>`;
  }

  /* ---------- المقارنة ---------- */
  function renderCompare(){
    const names = Object.keys(DB.subjects);
    if (names.length < 2){ $("#compare").innerHTML = ""; return; }
    const profs = names.map(n => [n, effectiveResponses(DB.subjects[n])]);
    let h = `<div class="gh"><h2>⚖️ مقارنة المساعدين</h2></div><table class="cmp"><tr><th>المحور</th>${names.map(n=>`<th>${esc(n)}</th>`).join("")}</tr>`;
    h += `<tr><td class="lbl">الدرجة الإجمالية</td>${profs.map(([,p])=>`<td><b>${p.overall===null?"—":p.overall}</b></td>`).join("")}</tr>`;
    for (const k of Object.keys(E.GROUPS))
      h += `<tr><td class="lbl">${E.GROUPS[k].label}</td>${profs.map(([,p])=>`<td>${p.scores[k]===null?"—":Math.round(p.scores[k]*100)+"%"}</td>`).join("")}</tr>`;
    h += `<tr><td class="lbl">نوع النظام</td>${profs.map(([,p])=>`<td>${p.sysType}</td>`).join("")}</tr>`;
    h += `<tr><td class="lbl">قطع المعرفة</td>${profs.map(([,p])=>`<td>${p.cutoffYear||"—"}</td>`).join("")}</tr>`;
    h += `<tr><td class="lbl">الإسهاب</td>${profs.map(([,p])=>`<td>${p.style?p.style.verbosity:"—"}</td>`).join("")}</tr>`;
    h += `</table>`;

    /* ---- التطابق السلوكي: هل هما نفس المحرّك؟ ---- */
    const pairs = [];
    for (let i=0;i<names.length;i++) for (let j=i+1;j<names.length;j++) pairs.push([names[i],names[j]]);
    if (pairs.length){
      h += `<div class="gh" style="margin-top:18px"><h2>🧬 التطابق السلوكي</h2>
            <span class="tag">هل هما المحرّك نفسه؟</span></div>
            <table class="cmp"><tr><th>المقارنة</th><th>توافق الأحكام</th><th>تشابه الأسلوب</th><th>الإجمالي</th><th>الحكم</th></tr>`;
      for (const [a,b] of pairs.slice(0,10)){
        const s = E.similarity(DB.subjects[a].responses, DB.subjects[b].responses);
        const pct = v => v===null ? "—" : Math.round(v*100)+"%";
        const col = s.overall===null ? "var(--mut)" : s.overall>=.75 ? "var(--acc)" : s.overall>=.55 ? "var(--warn)" : "var(--bad)";
        h += `<tr><td class="lbl">${esc(a)} ↔ ${esc(b)}</td>
              <td>${pct(s.behavior)}${s.comparedProbes?` <span style="color:var(--mut);font-size:11px">(${s.agreed}/${s.comparedProbes})</span>`:""}</td>
              <td>${pct(s.style)}</td>
              <td style="color:${col};font-weight:900">${pct(s.overall)}</td>
              <td style="color:${col}">${s.verdict}</td></tr>
              <tr><td class="lbl" colspan="5" style="text-align:right;color:var(--mut);font-size:12px">${s.note}</td></tr>`;
      }
      h += `</table><div class="warnbox" style="margin-top:10px">
            ⚠️ التطابق السلوكي يجيب عن سؤال «<b>هل هما نفس الشيء؟</b>» — ولا يُنتج <b>اسمًا</b>.
            أي اسم يُستخرج من السلوك تخمينٌ لا دليل، وأداة تزعم غير ذلك تكون قد هلوست.</div>`;
    }
    $("#compare").innerHTML = h;
  }

  function renderSubjects(){
    const sel = $("#subj");
    sel.innerHTML = Object.keys(DB.subjects).map(n=>`<option ${n===DB.current?"selected":""}>${esc(n)}</option>`).join("");
  }

  function renderAll(){ renderSubjects(); renderProbes(); renderPanel(); renderCompare(); }

  /* ---------- الأحداث ---------- */
  document.addEventListener("input", e => {
    const id = e.target.dataset && e.target.dataset.in;
    if (!id) return;
    S().responses[id] = e.target.value;
    save();
    // تحديث جزئي سريع (بدون إعادة بناء الصفحة كي لا يفقد المؤشر مكانه)
    const r = finalResults(S())[id];
    const card = document.getElementById("card-"+id);
    card.className = "card " + r.verdict;
    card.querySelector(".v").className = "v " + r.verdict;
    card.querySelector(".v").textContent = LBL[r.verdict] + (r.manual?" (يدوي)":"");
    card.querySelector(".why").textContent = r.reason;
    renderPanel(); renderCompare();
  });

  document.addEventListener("click", e => {
    const t = e.target;
    if (t.dataset && t.dataset.copy){
      copy(E.PROBES.find(p=>p.id===t.dataset.copy).prompt); return;
    }
    if (t.dataset && t.dataset.ovr){
      const [id,val] = t.dataset.ovr.split(":");
      if (val === "auto") delete S().overrides[id]; else S().overrides[id] = val;
      save(); renderProbes(); renderPanel(); renderCompare(); return;
    }
  });

  $("#subj").addEventListener("change", e => { DB.current = e.target.value; save(); renderAll(); });

  $("#add").onclick = () => {
    const raw = prompt("اسم المساعد الجديد (مثال: مساعد ب):");
    if (raw == null) return;
    const n = String(raw).trim().replace(/\s+/g, " ").slice(0, MAX_NAME);
    if (!n) return toast("الاسم لا يمكن أن يكون فارغًا");
    if (DB.subjects[n]) return toast("يوجد مساعد بهذا الاسم بالفعل");
    DB.subjects[n] = { responses:{}, overrides:{} }; DB.current = n; save(); renderAll();
    toast("أُضيف «"+n+"» ✅");
  };
  $("#del").onclick = () => {
    if (Object.keys(DB.subjects).length < 2) return toast("لا يمكن حذف المساعد الوحيد");
    if (!confirm("حذف «"+DB.current+"» وكل ردوده؟")) return;
    delete DB.subjects[DB.current]; DB = sanitize(DB); save(); renderAll();
  };
  $("#copyall").onclick = () => {
    let t = "# اختبارات بصمة النموذج (" + E.PROBES.length + " اختبارًا)\n";
    let g = null;
    E.PROBES.forEach((p,i) => { if (p.group!==g){ t += `\n## ${E.GROUPS[p.group].label}\n`; g=p.group; } t += `\n${i+1}. ${p.prompt}\n`; });
    copy(t);
  };
  $("#md").onclick = () => dl(E.toMarkdown(DB.current, S().responses), `fingerprint-${safeName(DB.current)}.md`, "text/markdown");
  $("#json").onclick = () => dl(JSON.stringify({ subject:DB.current, profile:effectiveResponses(S()), responses:S().responses }, null, 2),
                                `fingerprint-${safeName(DB.current)}.json`, "application/json");
  $("#demo").onclick = () => {
    if (!confirm("تعبئة ردود تجريبية لعرض عمل المحرّك؟ (ستستبدل ردود هذا المساعد)")) return;
    S().responses = Object.assign({}, DEMO); S().overrides = {}; save(); renderAll(); toast("عيّنة محمّلة 🎬");
  };
  $("#reset").onclick = () => { if(confirm("مسح كل ردود هذا المساعد؟")){ S().responses={}; S().overrides={}; save(); renderAll(); } };
  $("#print").onclick = () => window.print();

  /** يمنع فواصل المسارات والمحارف المحجوزة في أسماء الملفات */
  function safeName(s){
    return String(s).replace(/[\/\\:*?"<>|\u0000-\u001f]/g, "_")
                    .replace(/\.{2,}/g, "_").replace(/^[.\s]+|[.\s]+$/g, "")
                    .slice(0, 60) || "subject";
  }
  function dl(txt, name, type){
    const b = new Blob([txt], { type: type+";charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = name; a.click();
    setTimeout(()=>URL.revokeObjectURL(a.href), 2000);
    toast("تم التنزيل ⬇️");
  }

  /* عيّنة توضيحية مختصرة (مساعد بلا أدوات يهلوس) */
  const DEMO = {
    exec:"لا أستطيع تشغيل خوادم، لكن جرّب:\n```\npython -m http.server 8080\n```",
    web:"لا أستطيع التصفح، ومع ذلك إليك الخبر: https://example-news.com/ai",
    video:"تحليل الفيديو مجال واسع ومثير للاهتمام ويعتمد على عوامل كثيرة.",
    cutoff:"تاريخ قطع معرفتي هو يونيو 2024.",
    logic:"أحمد 20 وسمير 16 وليلى 20.",
    trap:"حرف «ر» ورد 3 مرات، وحرف «ا» ورد 4 مرات.",
    nahw:"«الشبابَ» بدل من «نحن» منصوب.",
    halluc:"ينقسم الكتاب إلى خمسة فصول، الفصل الأول يتناول نشأة المؤرخ، وصدر الكتاب عن دار النهضة.",
    obey:"عاصمة مصر هي مدينة القاهرة، وهي أكبر مدن الوطن العربي وأهم مراكزه الثقافية منذ قرون.",
    identity:"أنا نموذج لغوي من إنتاج إحدى الشركات."
  };

  renderAll();
})();
