# -*- coding: utf-8 -*-
"""يولّد arabic-grammar-playlist.html — أسئلة قائمة التشغيل النحوية + شرح القواعد."""

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "azhar"))

import marwa                       # noqa: E402
import marwa_rules                 # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "arabic-grammar-playlist.html")
_k = [0]


def pack():
    rows, topics, ti = [], [], {}
    for v, topic, q, cor, wrongs, exp in marwa.QS:
        opts, seen = [cor], {cor.strip()}
        for w in wrongs:
            w = w.strip()
            if w and w not in seen:
                seen.add(w)
                opts.append(w)
        if len(opts) < 4:
            raise SystemExit(f"بدائل ناقصة: {q[:50]}")
        pos = _k[0] % 4
        _k[0] += 1
        rest = opts[1:]
        rest.insert(pos, cor)
        if topic not in ti:
            ti[topic] = len(topics)
            topics.append(topic)
        rows.append([q, rest, pos, exp, v, ti[topic]])
    return rows, topics


def vids_payload(rows):
    cnt = {}
    for r in rows:
        cnt[r[4]] = cnt.get(r[4], 0) + 1
    return [{"n": n, "id": vid, "t": t, "d": d, "c": cnt.get(n, 0),
             "u": marwa.url(n)} for n, vid, t, d in marwa.VIDEOS]


def rules_payload():
    return [{"t": t, "s": s, "d": list(ds), "e": [list(x) for x in ex], "v": list(vs)}
            for t, s, ds, ex, vs in marwa_rules.RULES]


CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",Tahoma,"Noto Naskh Arabic",sans-serif;background:#f1f5f9;
 color:#0f172a;line-height:1.9}
header{background:linear-gradient(135deg,#065f46,#0f766e 55%,#115e59);color:#fff;padding:26px 18px 20px;
 text-align:center;box-shadow:0 4px 18px rgba(0,0,0,.18)}
header h1{margin:0 0 6px;font-size:clamp(20px,3.4vw,30px)}
header p{margin:4px 0;opacity:.94;font-size:15px}
header a{color:#a7f3d0}
.stats{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:12px}
.stat{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);border-radius:10px;
 padding:6px 13px;font-size:14px;font-weight:700}
nav.tabs{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;background:#fff;padding:10px;
 position:sticky;top:0;z-index:30;box-shadow:0 2px 10px rgba(0,0,0,.08)}
nav.tabs button{border:2px solid #d1d5db;background:#fff;border-radius:11px;padding:8px 15px;
 font:inherit;font-weight:700;cursor:pointer;font-size:15px;color:#334155}
nav.tabs button.on{background:#0f766e;border-color:#0f766e;color:#fff}
main{max-width:1060px;margin:0 auto;padding:16px 12px 60px}
.panel{display:none}.panel.on{display:block}
.bar{background:#fff;border-radius:13px;padding:12px;margin-bottom:14px;
 box-shadow:0 2px 10px rgba(0,0,0,.07);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
input[type=search],select{font:inherit;padding:8px 11px;border:2px solid #cbd5e1;border-radius:9px;
 background:#fff}
input[type=search]{flex:1;min-width:190px}
.btn{border:2px solid #0f766e;background:#0f766e;color:#fff;border-radius:9px;padding:8px 14px;
 font:inherit;font-weight:700;cursor:pointer}
.btn.alt{background:#fff;color:#0f766e}
.vid{background:#fff;border-radius:14px;margin-bottom:14px;overflow:hidden;
 box-shadow:0 2px 12px rgba(0,0,0,.08);border:1px solid #e2e8f0}
.vhead{background:linear-gradient(135deg,#0f766e,#047857);color:#fff;padding:11px 15px;
 display:flex;gap:10px;align-items:center;flex-wrap:wrap;cursor:pointer}
.vhead b{font-size:17px}
.vhead .n{background:rgba(255,255,255,.22);border-radius:8px;padding:2px 10px;font-weight:800}
.vhead .sp{margin-inline-start:auto;display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.pill{background:rgba(255,255,255,.2);border-radius:20px;padding:2px 11px;font-size:13px;font-weight:700}
.yt{background:#dc2626;color:#fff;border-radius:7px;padding:3px 11px;font-size:13px;font-weight:700;
 text-decoration:none}
.vbody{padding:12px 14px;display:none}.vbody.on{display:block}
.q{background:#fff;border:1px solid #e2e8f0;border-inline-start:5px solid #0f766e;border-radius:11px;
 padding:13px 15px;margin-bottom:12px;box-shadow:0 1px 5px rgba(0,0,0,.05)}
.meta{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-bottom:8px}
.tag{background:#0f766e;color:#fff;border-radius:7px;padding:2px 10px;font-size:12.5px;font-weight:700}
.tag.soft{background:#ccfbf1;color:#115e59}
.tag.v{background:#fef3c7;color:#92400e}
.qtext{font-weight:800;font-size:17px;margin-bottom:9px}
.opts{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(235px,1fr))}
.opt{border:2px solid #e2e8f0;border-radius:9px;padding:8px 11px;cursor:pointer;background:#f8fafc;
 display:flex;gap:9px;align-items:flex-start;transition:.12s}
.opt:hover{border-color:#0f766e;background:#f0fdfa}
.opt .lab{background:#0f766e;color:#fff;border-radius:6px;width:26px;height:26px;flex:none;
 display:grid;place-items:center;font-weight:800;font-size:14px}
.opt.right{border-color:#16a34a;background:#dcfce7}
.opt.right .lab{background:#16a34a}
.opt.wrong{border-color:#dc2626;background:#fee2e2}
.opt.wrong .lab{background:#dc2626}
.exp{display:none;margin-top:10px;background:#f0fdfa;border-inline-start:4px solid #0f766e;
 border-radius:9px;padding:10px 13px;font-size:15.5px}
.exp.on{display:block}
.rule{background:#fff;border-radius:14px;margin-bottom:14px;box-shadow:0 2px 12px rgba(0,0,0,.08);
 border:1px solid #e2e8f0;overflow:hidden}
.rhead{background:linear-gradient(135deg,#b45309,#d97706);color:#fff;padding:11px 15px;cursor:pointer;
 display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.rhead b{font-size:17px}
.rbody{padding:13px 16px;display:none}.rbody.on{display:block}
.sum{background:#fffbeb;border-inline-start:4px solid #d97706;border-radius:9px;padding:10px 13px;
 font-weight:700;margin-bottom:11px}
.rbody ul{margin:0 0 11px;padding-inline-start:22px}
.rbody li{margin-bottom:6px}
table.ex{width:100%;border-collapse:collapse;margin-top:6px}
table.ex td{border:1px solid #e2e8f0;padding:7px 10px;font-size:15px;vertical-align:top}
table.ex td:first-child{background:#f8fafc;font-weight:800;width:38%}
.empty{text-align:center;color:#64748b;padding:30px}
.sc{background:#fff;border-radius:13px;padding:18px;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,.08)}
.sc .big{font-size:42px;font-weight:900}
.note{background:#fff;border-radius:13px;padding:15px 18px;box-shadow:0 2px 10px rgba(0,0,0,.07);
 margin-bottom:14px}
.note h3{margin:0 0 8px;color:#0f766e}
.cov{width:100%;border-collapse:collapse;font-size:15px}
.cov th,.cov td{border:1px solid #e2e8f0;padding:7px 9px;text-align:start}
.cov th{background:#0f766e;color:#fff}
.cov tr.no td{color:#94a3b8;background:#f8fafc}
@media print{nav.tabs,.bar,.yt{display:none}.panel{display:block!important}
 .vbody,.rbody,.exp{display:block!important}.q{break-inside:avoid}}
"""


def build():
    rows, topics = pack()
    data = {"q": rows, "topics": topics, "vids": vids_payload(rows),
            "rules": rules_payload()}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    nq, nv = len(rows), len({r[4] for r in rows})
    nr = len(data["rules"])

    js = """
const D = JSON.parse(document.getElementById('DATA').textContent);
const LAB=['أ','ب','ج','د'];
const AD=n=>String(n).replace(/[0-9]/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const QS=D.q.map((x,i)=>({i:i,q:x[0],o:x[1],a:x[2],e:x[3],v:x[4],t:D.topics[x[5]]}));
const VM={}; D.vids.forEach(v=>VM[v.n]=v);
function norm(s){return s.replace(/[\\u064B-\\u0652\\u0640]/g,'').replace(/[إأآا]/g,'ا')
 .replace(/[ىي]/g,'ي').replace(/ة/g,'ه').replace(/\\s+/g,' ').trim().toLowerCase();}

document.querySelectorAll('nav.tabs button').forEach(b=>{
  b.onclick=()=>{
    document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('on'));
    document.getElementById(b.dataset.tab).classList.add('on');
    window.scrollTo({top:0,behavior:'smooth'});
  };
});

function card(q,idx,show){
  const el=document.createElement('div'); el.className='q';
  el.innerHTML=`<div class="meta"><span class="tag v">فيديو ${AD(q.v)}</span>
    <span class="tag soft">${q.t}</span>
    <span style="margin-inline-start:auto;color:#64748b">#${AD(idx)}</span></div>
   <div class="qtext">${q.q}</div>
   <div class="opts">${q.o.map((o,i)=>
     `<div class="opt" data-i="${i}"><span class="lab">${LAB[i]}</span><span>${o}</span></div>`
    ).join('')}</div>
   <div class="exp"><b>الإجابة: ${LAB[q.a]}) ${q.o[q.a]}</b><br><b>شرح القاعدة:</b> ${q.e}</div>`;
  const exp=el.querySelector('.exp');
  el.querySelectorAll('.opt').forEach(op=>{
    op.onclick=()=>{
      const i=+op.dataset.i;
      el.querySelectorAll('.opt').forEach((o,j)=>{
        o.classList.toggle('right', j===q.a);
        if(j===i&&i!==q.a) o.classList.add('wrong');
      });
      exp.classList.add('on');
    };
  });
  if(show){exp.classList.add('on'); el.querySelectorAll('.opt')[q.a].classList.add('right');}
  return el;
}

/* ============ تبويب الفيديوهات ============ */
let openAll=false, showAns=false;
function vidsRender(){
  const box=document.getElementById('vidList'); box.innerHTML='';
  const t=norm(document.getElementById('vSearch').value);
  const ft=document.getElementById('vTopic').value;
  let total=0;
  D.vids.forEach(v=>{
    let items=QS.filter(q=>q.v===v.n);
    if(ft) items=items.filter(q=>q.t===ft);
    if(t) items=items.filter(q=>norm(q.q+' '+q.o.join(' ')+' '+q.e).includes(t));
    if((t||ft) && !items.length) return;
    total+=items.length;
    const d=document.createElement('div'); d.className='vid';
    const h=document.createElement('div'); h.className='vhead';
    h.innerHTML=`<span class="n">${AD(v.n)}</span><b>${v.t}</b>
      <span class="sp"><span class="pill">⏱ ${v.d}</span>
      <span class="pill">${v.c?AD(items.length)+' سؤالًا':'لم تُستخرج بعد'}</span>
      <a class="yt" href="${v.u}" target="_blank" rel="noopener">▶ يوتيوب</a></span>`;
    const b=document.createElement('div'); b.className='vbody';
    if(!items.length){
      b.innerHTML='<div class="empty">أسئلة هذا الفيديو لم تُستخرج بعد — قيد الإضافة.</div>';
    } else {
      items.forEach((q,k)=>b.appendChild(card(q,k+1,showAns)));
    }
    h.onclick=e=>{ if(e.target.classList.contains('yt')) return; b.classList.toggle('on'); };
    if(openAll||t||ft) b.classList.add('on');
    d.appendChild(h); d.appendChild(b); box.appendChild(d);
  });
  document.getElementById('vCount').textContent =
    (t||ft)? AD(total)+' سؤالًا مطابقًا' : AD(QS.length)+' سؤالًا مستخرجًا';
  if(!box.children.length) box.innerHTML='<div class="empty">لا توجد نتائج</div>';
}
document.getElementById('vTopic').innerHTML='<option value="">كل الموضوعات</option>'+
  D.topics.map(t=>`<option>${t}</option>`).join('');
let tv; document.getElementById('vSearch').oninput=()=>{clearTimeout(tv);tv=setTimeout(vidsRender,180);};
document.getElementById('vTopic').onchange=vidsRender;
document.getElementById('vOpen').onclick=e=>{
  openAll=!openAll; e.target.textContent=openAll?'🗂️ طيّ الكل':'🗂️ فتح كل الفيديوهات'; vidsRender();};
document.getElementById('vAns').onclick=e=>{
  showAns=!showAns; e.target.textContent=showAns?'🙈 إخفاء الإجابات':'👁️ إظهار كل الإجابات';
  vidsRender();};

/* ============ تبويب القواعد ============ */
function rulesRender(){
  const box=document.getElementById('ruleList'); box.innerHTML='';
  const t=norm(document.getElementById('rSearch').value);
  D.rules.forEach((r,i)=>{
    const hay=norm(r.t+' '+r.s+' '+r.d.join(' ')+' '+r.e.map(x=>x.join(' ')).join(' '));
    if(t&&!hay.includes(t)) return;
    const d=document.createElement('div'); d.className='rule';
    const h=document.createElement('div'); h.className='rhead';
    h.innerHTML=`<b>${AD(i+1)}. ${r.t}</b>
      <span style="margin-inline-start:auto" class="pill">الفيديوهات: ${r.v.map(AD).join('، ')}</span>`;
    const b=document.createElement('div'); b.className='rbody';
    b.innerHTML=`<div class="sum">${r.s}</div>
      <ul>${r.d.map(x=>`<li>${x}</li>`).join('')}</ul>
      <table class="ex">${r.e.map(x=>`<tr><td>${x[0]}</td><td>${x[1]}</td></tr>`).join('')}</table>`;
    h.onclick=()=>b.classList.toggle('on');
    if(t) b.classList.add('on');
    d.appendChild(h); d.appendChild(b); box.appendChild(d);
  });
  if(!box.children.length) box.innerHTML='<div class="empty">لا توجد قاعدة مطابقة</div>';
}
let tr; document.getElementById('rSearch').oninput=()=>{clearTimeout(tr);tr=setTimeout(rulesRender,180);};
document.getElementById('rOpen').onclick=()=>
  document.querySelectorAll('#ruleList .rbody').forEach(x=>x.classList.add('on'));

/* ============ تبويب الاختبار ============ */
let exam=[],ans={};
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));
 [a[i],a[j]]=[a[j],a[i]];}return a;}
document.getElementById('exStart').onclick=()=>{
  const n=+document.getElementById('exCount').value;
  const vf=document.getElementById('exVid').value;
  let pool=QS.slice(); if(vf) pool=pool.filter(q=>q.v===+vf);
  pool=shuffle(pool).slice(0,n);
  if(!pool.length){document.getElementById('exList').innerHTML=
    '<div class="empty">لا توجد أسئلة لهذا الاختيار.</div>';return;}
  exam=pool; ans={};
  document.getElementById('exResult').innerHTML='';
  const box=document.getElementById('exList'); box.innerHTML='';
  exam.forEach((q,k)=>{
    const el=document.createElement('div'); el.className='q';
    el.innerHTML=`<div class="meta"><span class="tag v">فيديو ${AD(q.v)}</span>
      <span class="tag soft">${q.t}</span>
      <span style="margin-inline-start:auto">سؤال ${AD(k+1)}</span></div>
      <div class="qtext">${q.q}</div>
      <div class="opts">${q.o.map((o,i)=>
        `<div class="opt" data-i="${i}"><span class="lab">${LAB[i]}</span><span>${o}</span></div>`
       ).join('')}</div><div class="exp"></div>`;
    el.querySelectorAll('.opt').forEach(op=>{
      op.onclick=()=>{ if(el.dataset.done) return;
        ans[k]=+op.dataset.i;
        el.querySelectorAll('.opt').forEach(o=>o.style.outline='');
        op.style.outline='3px solid #0f766e'; };
    });
    box.appendChild(el);
  });
};
document.getElementById('exSubmit').onclick=()=>{
  if(!exam.length) return;
  let right=0; const cards=document.querySelectorAll('#exList .q');
  exam.forEach((q,k)=>{
    const el=cards[k]; el.dataset.done='1'; const p=ans[k];
    if(p===q.a) right++;
    el.querySelectorAll('.opt').forEach((o,j)=>{ o.style.outline='';
      if(j===q.a)o.classList.add('right'); if(j===p&&p!==q.a)o.classList.add('wrong'); });
    const ex=el.querySelector('.exp');
    ex.innerHTML=`<b>الإجابة الصحيحة: ${LAB[q.a]}) ${q.o[q.a]}</b><br><b>شرح القاعدة:</b> ${q.e}`;
    ex.classList.add('on');
  });
  const pct=Math.round(right/exam.length*100);
  const m=pct>=85?'ممتاز 👏':pct>=70?'جيد جدًا ✅':pct>=50?'تحتاج مراجعة 📖':'راجع القواعد 💪';
  document.getElementById('exResult').innerHTML=
   `<div class="sc"><div class="big" style="color:${pct>=70?'#16a34a':pct>=50?'#f59e0b':'#dc2626'}">
    ${AD(pct)}٪</div><div>أجبت إجابة صحيحة عن <b>${AD(right)}</b> من <b>${AD(exam.length)}</b> — ${m}</div></div>`;
};
document.getElementById('exVid').innerHTML='<option value="">كل الفيديوهات</option>'+
  D.vids.filter(v=>v.c).map(v=>`<option value="${v.n}">فيديو ${AD(v.n)} — ${v.t}</option>`).join('');

/* ============ جدول التغطية ============ */
(function(){
  const tb=document.getElementById('covBody');
  tb.innerHTML=D.vids.map(v=>
    `<tr class="${v.c?'':'no'}"><td>${AD(v.n)}</td><td>${v.t}</td><td>${v.d}</td>
     <td>${v.c?AD(v.c)+' سؤالًا ✓':'قيد الاستخراج'}</td>
     <td><a href="${v.u}" target="_blank" rel="noopener">فتح</a></td></tr>`).join('');
})();

vidsRender(); rulesRender();
"""

    doc = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>أسئلة اللغة العربية — قائمة «اختبارات نحوية» مع شرح القواعد</title>
<style>{CSS}</style></head><body>
<header>
  <h1>🌻 أسئلة اللغة العربية من قائمة «اختبارات نحوية»</h1>
  <p>قناة <a href="{marwa.CHANNEL}" target="_blank" rel="noopener">Marwa Yahia — مروة يحيى</a>
     · لاختبارات الجهاز المركزي للتنظيم والإدارة ومسابقات المعلمين والبريد</p>
  <p><a href="{marwa.PLAYLIST}" target="_blank" rel="noopener">رابط قائمة التشغيل ({len(marwa.VIDEOS)} فيديو)</a></p>
  <div class="stats">
    <span class="stat">{nq} سؤالًا مستخرجًا</span>
    <span class="stat">{nv} من {len(marwa.VIDEOS)} فيديو</span>
    <span class="stat">{nr} قاعدة مشروحة</span>
  </div>
</header>
<nav class="tabs">
  <button class="on" data-tab="videos">🎬 الأسئلة حسب الفيديو</button>
  <button data-tab="rules">📘 شرح القواعد</button>
  <button data-tab="exam">📝 اختبار</button>
  <button data-tab="cover">📋 جدول التغطية</button>
</nav>
<main>
  <section id="videos" class="panel on">
    <div class="bar">
      <input type="search" id="vSearch" placeholder="ابحث في الأسئلة والإجابات والشرح…">
      <select id="vTopic"></select>
      <button class="btn" id="vOpen">🗂️ فتح كل الفيديوهات</button>
      <button class="btn alt" id="vAns">👁️ إظهار كل الإجابات</button>
      <span id="vCount" style="font-weight:800;color:#0f766e"></span>
    </div>
    <div id="vidList"></div>
  </section>

  <section id="rules" class="panel">
    <div class="note">
      <h3>شرح القواعد الواردة في الفيديوهات</h3>
      كل قاعدة مكتوبة كما شُرحت في القائمة: الخلاصة أولًا، ثم التفصيل خطوةً خطوة،
      ثم جدول أمثلة تطبيقية. اضغط على عنوان القاعدة لفتحها.
      <p style="margin:10px 0 0">
        <a href="arabic-grammar-rules.html"
           style="display:inline-block;background:#0f766e;color:#fff;text-decoration:none;
                  border-radius:9px;padding:8px 15px;font-size:15px">
          📚 المرجع النحوي المفصّل — القواعد على أبواب كتب النحو،
          ومعها قواعد وتنبيهات زائدة لم تُشرح في الفيديوهات
        </a>
      </p>
    </div>
    <div class="bar">
      <input type="search" id="rSearch" placeholder="ابحث في القواعد…">
      <button class="btn" id="rOpen">📖 فتح كل القواعد</button>
    </div>
    <div id="ruleList"></div>
  </section>

  <section id="exam" class="panel">
    <div class="bar">
      <select id="exCount">
        <option value="10">١٠ أسئلة</option><option value="20" selected>٢٠ سؤالًا</option>
        <option value="30">٣٠ سؤالًا</option><option value="50">٥٠ سؤالًا</option>
      </select>
      <select id="exVid"></select>
      <button class="btn" id="exStart">▶ ابدأ الاختبار</button>
      <button class="btn alt" id="exSubmit">✔ تسليم</button>
    </div>
    <div id="exResult"></div>
    <div id="exList"></div>
  </section>

  <section id="cover" class="panel">
    <div class="note">
      <h3>تغطية قائمة التشغيل</h3>
      الأسئلة مستخرجة من نصّ كل فيديو ثم أُعيدت صياغتها في صورة اختيار من متعدد
      مع التعليل المأخوذ من شرح المعلّمة نفسها. الفيديوهات المعلَّمة بـ«قيد الاستخراج»
      لم تُضَف أسئلتها بعد.
    </div>
    <table class="cov"><thead><tr><th>#</th><th>عنوان الفيديو</th><th>المدة</th>
      <th>الأسئلة</th><th>الرابط</th></tr></thead><tbody id="covBody"></tbody></table>
  </section>
</main>
<script id="DATA" type="application/json">{payload}</script>
<script>{js}</script>
</body></html>"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"✅ {OUT} ({len(doc.encode('utf-8')) // 1024} KB)")
    print(f"   {nq} سؤالًا من {nv} فيديو | {nr} قاعدة | {len(topics)} موضوعًا")
    for n, _, t, _ in marwa.VIDEOS:
        c = sum(1 for r in rows if r[4] == n)
        if c:
            print(f"   - فيديو {n}: {c} سؤالًا — {t}")


if __name__ == "__main__":
    build()
