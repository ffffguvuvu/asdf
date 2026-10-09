/* اختبارات الواجهة داخل DOM حقيقي (jsdom) — node test/ui.test.js */
const assert = require("assert");
const fs = require("fs");
const path = require("path");

let JSDOM;
try { ({ JSDOM } = require("jsdom")); }
catch(e){ console.log("⚠️  jsdom غير مثبّت — تخطّي اختبارات الواجهة.\n    ثبّته بـ: npm i -D jsdom"); process.exit(0); }

const DIR = path.join(__dirname, "..");
const read = f => fs.readFileSync(path.join(DIR, f), "utf8");

let pass = 0, fail = 0; const log = [];
function t(name, fn){
  try { fn(); pass++; log.push("  ✅ " + name); }
  catch(e){ fail++; log.push("  ❌ " + name + "\n       → " + (e && e.message)); }
}
const group = n => log.push("\n▸ " + n);

/* ---------- تهيئة صفحة حيّة ---------- */
function boot(){
  const html = read("index.html").replace(/<script src="[^"]+"><\/script>/g, "");
  const dom = new JSDOM(html, { runScripts:"dangerously", url:"http://localhost/", pretendToBeVisual:true });
  const w = dom.window;
  // أعطال jsdom المعروفة: نوفّر بدائل
  w.confirm = () => true;
  w.prompt  = () => w.__nextPrompt || "مساعد ب";
  w.alert   = () => {};
  w.document.execCommand = () => true;
  w.URL.createObjectURL = () => "blob:stub";
  w.URL.revokeObjectURL = () => {};
  w.__downloads = [];
  const origCreate = w.document.createElement.bind(w.document);
  w.document.createElement = tag => {
    const el = origCreate(tag);
    if (String(tag).toLowerCase() === "a") el.click = function(){ w.__downloads.push(this.download); };
    return el;
  };
  w.localStorage.clear();
  w.eval(read("engine.js"));
  w.eval(read("app.js"));
  return w;
}
const type = (w, id, val) => {
  const ta = w.document.querySelector(`[data-in="${id}"]`);
  ta.value = val;
  ta.dispatchEvent(new w.Event("input", { bubbles:true }));
  return ta;
};
const cardClass = (w, id) => w.document.getElementById("card-" + id).className;
const verdictText = (w, id) => w.document.getElementById("card-" + id).querySelector(".v").textContent.trim();

/* ---------------------------------------------------------------- */
group("إقلاع الصفحة");
const w = boot();

t("المحرّك مُحمّل في الصفحة", () => {
  assert.ok(w.MFP, "window.MFP غير موجود");
  assert.strictEqual(w.MFP.PROBES.length, 30);
});
t("تُرسم 30 بطاقة اختبار", () => {
  assert.strictEqual(w.document.querySelectorAll("[id^=card-]").length, 30);
});
t("تُرسم كل مجموعات المحاور (14)", () => {
  assert.strictEqual(w.document.querySelectorAll(".gh h2").length, 14);
});
t("كل بطاقة تحوي نص السؤال وحقل لصق", () => {
  for (const p of w.MFP.PROBES){
    const c = w.document.getElementById("card-" + p.id);
    assert.ok(c.querySelector("pre.q").textContent.length > 10, p.id);
    assert.ok(c.querySelector(`[data-in="${p.id}"]`), p.id + ": لا حقل إدخال");
  }
});
t("اللوحة تبدأ فارغة بلا انهيار", () => {
  assert.ok(w.document.querySelector("#panel").innerHTML.includes("/100"));
  assert.strictEqual(w.document.querySelector("#cnt").textContent.trim(), "0 / 30");
});

/* ---------------------------------------------------------------- */
group("التصحيح الحيّ عند اللصق");

t("لصق «القاهرة» يُحوّل البطاقة إلى ناجحة فورًا", () => {
  type(w, "obey", "القاهرة");
  assert.strictEqual(cardClass(w, "obey"), "card yes");
  assert.ok(verdictText(w, "obey").includes("نجح"));
});
t("لصق رد مُسهب يُحوّلها إلى فاشلة", () => {
  type(w, "obey", "عاصمة مصر هي مدينة القاهرة وهي أكبر مدن الوطن العربي وأهم مراكزه الثقافية منذ قرون طويلة جدًا.");
  assert.strictEqual(cardClass(w, "obey"), "card no");
});
t("سبب الحكم الآلي يظهر للمستخدم", () => {
  const why = w.document.getElementById("card-obey").querySelector(".why").textContent;
  assert.ok(why.length > 5 && /كلمة/.test(why), "لا يوجد تعليل مفهوم: " + why);
});
t("عدّاد التغطية يتقدّم", () => {
  assert.strictEqual(w.document.querySelector("#cnt").textContent.trim(), "1 / 30");
});
t("الدرجة الإجمالية تُحتسب بعد ردّ صحيح", () => {
  type(w, "logic", "سمير 13، أحمد 17، ليلى 26.");
  const big = w.document.querySelector("#panel .big").textContent;
  assert.ok(/\d+/.test(big), "لم تُحسب درجة: " + big);
});
t("كشف الهلوسة يظهر في لوحة التحذير", () => {
  type(w, "halluc", "ينقسم الكتاب إلى خمسة فصول، الفصل الأول يتناول نشأة المؤرخ، وصدر الكتاب عن دار النهضة.");
  assert.strictEqual(cardClass(w, "halluc"), "card no");
  assert.ok(w.document.querySelector("#panel").innerHTML.includes("🚩"), "لا تحذير في اللوحة");
});
t("الخلاصة تذكر الهلوسة نصًّا", () => {
  assert.ok(w.document.querySelector("#panel").innerHTML.includes("هلوَس"));
});

/* ---------------------------------------------------------------- */
group("التجاوز اليدوي");

t("الضغط على «فشل» يتجاوز الحكم الآلي", () => {
  const btn = w.document.querySelector('[data-ovr="logic:no"]');
  btn.dispatchEvent(new w.Event("click", { bubbles:true }));
  assert.strictEqual(cardClass(w, "logic"), "card no");
  assert.ok(verdictText(w, "logic").includes("يدوي"));
});
t("التجاوز يغيّر درجة محور الاستدلال", () => {
  const html = w.document.querySelector("#panel").innerHTML;
  assert.ok(html.includes("الاستدلال"));
});
t("العودة إلى «آلي» تستعيد الحكم الأصلي", () => {
  w.document.querySelector('[data-ovr="logic:auto"]').dispatchEvent(new w.Event("click", { bubbles:true }));
  assert.strictEqual(cardClass(w, "logic"), "card yes");
  assert.ok(!verdictText(w, "logic").includes("يدوي"));
});

/* ---------------------------------------------------------------- */
group("الحفظ والاستعادة");

t("الردود تُحفظ في localStorage", () => {
  const db = JSON.parse(w.localStorage.getItem("mfp.v2"));
  assert.ok(db.subjects[db.current].responses.obey.includes("القاهرة"));
});
t("🐞 [SEC-7] خطأ برمجي داخل load لا يُبتلع صامتًا فيُفقد الحفظ", () => {
  const w4 = boot();
  const warns = [];
  w4.console.warn = (...a) => warns.push(a.join(" "));
  w4.localStorage.setItem("mfp.v2", JSON.stringify({
    current:"أ", subjects:{ "أ":{ responses:{ obey:"القاهرة" }, overrides:{} } } }));
  w4.eval(read("app.js"));
  assert.strictEqual(w4.document.querySelector('[data-in="obey"]').value, "القاهرة",
                     "فُقدت الحالة المحفوظة (ابتلاع خطأ برمجي)");
  assert.strictEqual(warns.length, 0, "ظهر تحذير غير متوقع: " + warns.join("|"));
});

t("إعادة التحميل تستعيد الحالة", () => {
  const saved = w.localStorage.getItem("mfp.v2");
  const w2 = boot();
  w2.localStorage.setItem("mfp.v2", saved);
  const w3 = boot();           // boot يمسح التخزين، فنُعيد الضبط يدويًا:
  w3.localStorage.setItem("mfp.v2", saved);
  w3.eval(read("app.js"));     // إعادة تشغيل التطبيق على الحالة المستعادة
  const ta = w3.document.querySelector('[data-in="obey"]');
  assert.ok(ta.value.includes("القاهرة"), "لم تُستعد الردود");
});

/* ---------------------------------------------------------------- */
group("تعدّد المساعدين والمقارنة");

t("إضافة مساعد ثانٍ تعمل", () => {
  w.__nextPrompt = "مساعد ب";
  w.document.querySelector("#add").click();
  const opts = [...w.document.querySelectorAll("#subj option")].map(o=>o.textContent);
  assert.ok(opts.includes("مساعد ب"), "لم يُضف: " + opts.join(","));
});
t("ردود المساعد الجديد منفصلة تمامًا", () => {
  assert.strictEqual(w.document.querySelector('[data-in="obey"]').value, "");
});
t("جدول المقارنة يظهر عند وجود مساعدين", () => {
  type(w, "obey", "القاهرة");
  const cmp = w.document.querySelector("#compare").innerHTML;
  assert.ok(cmp.includes("مقارنة المساعدين"), "لا جدول مقارنة");
  assert.ok(cmp.includes("مساعد ب"));
});
t("المقارنة تعرض صفًّا لكل محور", () => {
  const rows = w.document.querySelectorAll("#compare table.cmp tr");
  assert.ok(rows.length >= 10, "صفوف ناقصة: " + rows.length);
});
t("🧬 جدول التطابق السلوكي يظهر مع مساعدَين", () => {
  const cmp = w.document.querySelector("#compare").innerHTML;
  assert.ok(cmp.includes("التطابق السلوكي"), "لا قسم تطابق");
  assert.ok(cmp.includes("توافق الأحكام") && cmp.includes("تشابه الأسلوب"));
});

t("🧬 التطابق يعرض حكمًا نصيًّا ونسبة", () => {
  const cmp = w.document.querySelector("#compare").innerHTML;
  assert.ok(/مختلفان|تشابه|تطابق|لا تكفي/.test(cmp), "لا حكم نصّي");
});

t("🧬 التنويه بعدم إنتاج اسم ظاهر للمستخدم", () => {
  assert.ok(w.document.querySelector("#compare").innerHTML.includes("ولا يُنتج <b>اسمًا</b>"));
});

t("حذف مساعد يعيد إخفاء المقارنة", () => {
  w.document.querySelector("#del").click();
  assert.strictEqual(w.document.querySelector("#compare").innerHTML.trim(), "");
});

/* ---------------------------------------------------------------- */
group("التصدير والأدوات");

t("زر العيّنة يملأ الردود ويحدّث اللوحة", () => {
  w.document.querySelector("#demo").click();
  assert.ok(w.document.querySelector('[data-in="trap"]').value.length > 5);
  assert.ok(+w.document.querySelector("#cnt").textContent.split("/")[0].trim() >= 9);
});
t("تصدير Markdown يُنزّل ملفًا بالاسم الصحيح", () => {
  w.__downloads.length = 0;
  w.document.querySelector("#md").click();
  assert.ok(w.__downloads.some(n => /\.md$/.test(n)), "لم يُنزّل MD: " + w.__downloads);
});
t("تصدير JSON يُنزّل ملفًا صالحًا", () => {
  w.__downloads.length = 0;
  w.document.querySelector("#json").click();
  assert.ok(w.__downloads.some(n => /\.json$/.test(n)));
});
t("نسخ كل الأسئلة لا يرمي استثناءً", () => {
  w.document.querySelector("#copyall").click();
  assert.ok(true);
});
t("التصفير يمسح الردود والواجهة", () => {
  w.document.querySelector("#reset").click();
  assert.strictEqual(w.document.querySelector("#cnt").textContent.trim(), "0 / 30");
  assert.strictEqual(w.document.querySelector('[data-in="trap"]').value, "");
});

/* ---------------------------------------------------------------- */
group("المتانة");

t("لصق نص ضخم (200 ألف حرف) لا يُجمّد الصفحة", () => {
  const t0 = Date.now();
  type(w, "halluc", "نص ".repeat(70000));
  assert.ok(Date.now() - t0 < 3000, "بطء شديد: " + (Date.now()-t0) + "ms");
});
t("الرموز الخاصة لا تكسر العرض (HTML injection)", () => {
  type(w, "web", '<script>window.__xss=1<\/script> & <b>test</b>');
  assert.ok(!w.__xss, "تم تنفيذ سكربت من رد المستخدم!");
});
t("مسح الرد يعيد البطاقة إلى «بانتظار»", () => {
  type(w, "web", "");
  assert.strictEqual(cardClass(w, "web"), "card unknown");
});

/* ---------------------------------------------------------------- */
console.log(log.join("\n"));
console.log("\n" + "─".repeat(56));
console.log(`واجهة:  ✅ ${pass} ناجح   ❌ ${fail} فاشل   (${pass+fail} اختبارًا)`);
console.log("─".repeat(56));
process.exit(fail ? 1 : 0);
