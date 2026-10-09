/* اختبارات أمنية — تُثبت الثغرة أولًا ثم تمنع عودتها. node test/security.test.js */
const assert = require("assert");
const fs = require("fs"), path = require("path");
let JSDOM;
try { ({ JSDOM } = require("jsdom")); }
catch(e){ console.log("⚠️  jsdom غير مثبّت — تخطّي الاختبارات الأمنية."); process.exit(0); }

const DIR = path.join(__dirname, "..");
const read = f => fs.readFileSync(path.join(DIR, f), "utf8");

let pass=0, fail=0; const log=[];
function t(n, fn){ try{ fn(); pass++; log.push("  ✅ "+n); } catch(e){ fail++; log.push("  ❌ "+n+"\n       → "+(e&&e.message)); } }
const group = n => log.push("\n▸ "+n);

/** يقلع التطبيق على حالة تخزين مُعطاة (قد تكون خبيثة/تالفة) */
function bootWith(stored, opts={}){
  const html = read("index.html").replace(/<script src="[^"]+"><\/script>/g, "");
  const dom = new JSDOM(html, { runScripts:"dangerously", url:"http://localhost/" });
  const w = dom.window;
  w.confirm = () => true;
  w.prompt  = () => w.__nextPrompt ?? "مساعد ب";
  w.document.execCommand = () => true;
  w.URL.createObjectURL = () => "blob:stub";
  w.URL.revokeObjectURL = () => {};
  w.__downloads = [];
  const oc = w.document.createElement.bind(w.document);
  w.document.createElement = tag => { const el = oc(tag);
    if (String(tag).toLowerCase()==="a") el.click = function(){ w.__downloads.push(this.download); };
    return el; };
  if (opts.fullStorage){                       // محاكاة امتلاء التخزين
    w.localStorage.setItem = () => { const e = new Error("QuotaExceededError"); e.name="QuotaExceededError"; throw e; };
  } else if (stored !== undefined){
    w.localStorage.setItem("mfp.v2", typeof stored === "string" ? stored : JSON.stringify(stored));
  }
  w.eval(read("engine.js"));
  w.eval(read("app.js"));
  return w;
}
const type=(w,id,v)=>{ const ta=w.document.querySelector(`[data-in="${id}"]`); ta.value=v;
                       ta.dispatchEvent(new w.Event("input",{bubbles:true})); };

/* ---------------------------------------------------------------- */
group("SEC-1 · حقن HTML/JS عبر محتوى المستخدم");

t("لصق وسم script في الرد لا يُنفَّذ", () => {
  const w = bootWith();
  type(w, "web", '<img src=x onerror="window.__xss=1"><script>window.__xss=1<\/script>');
  assert.ok(!w.__xss, "تم تنفيذ كود من رد المستخدم");
  assert.strictEqual(w.document.querySelectorAll("img[src=x]").length, 0, "حُقن عنصر img");
});

t("اسم مساعد خبيث لا يُنفَّذ في القائمة ولا جدول المقارنة", () => {
  const w = bootWith();
  w.__nextPrompt = '<img src=x onerror="window.__xss2=1">"onmouseover="window.__xss2=1';
  w.document.querySelector("#add").click();
  type(w, "obey", "القاهرة");
  assert.ok(!w.__xss2, "تم تنفيذ كود من اسم المساعد");
  assert.strictEqual(w.document.querySelectorAll("#compare img").length, 0);
  assert.strictEqual(w.document.querySelectorAll("#subj img").length, 0);
});

t("الاقتباسات في اسم المساعد لا تكسر السمات (attribute injection)", () => {
  const w = bootWith();
  w.__nextPrompt = 'a" onfocus="window.__xss3=1" x="';
  w.document.querySelector("#add").click();
  const opts = [...w.document.querySelectorAll("#subj option")];
  assert.ok(!opts.some(o => o.hasAttribute("onfocus")), "حُقنت سمة onfocus");
  assert.ok(!w.__xss3);
});

/* ---------------------------------------------------------------- */
group("SEC-2 · تلف/تلاعب التخزين المحلي");

t("حالة تالفة: current يشير إلى مساعد محذوف", () => {
  const w = bootWith({ current:"شبح", subjects:{ "مساعد أ":{ responses:{}, overrides:{} } } });
  assert.strictEqual(w.document.querySelectorAll("[id^=card-]").length, 30, "لم تُرسم الصفحة");
  assert.ok(Object.keys(w.localStorage).length >= 0);
});

t("حالة ناقصة: مساعد بلا حقلي responses/overrides", () => {
  const w = bootWith({ current:"أ", subjects:{ "أ":{} } });
  assert.strictEqual(w.document.querySelectorAll("[id^=card-]").length, 30);
  type(w, "obey", "القاهرة");
  assert.strictEqual(w.document.getElementById("card-obey").className, "card yes");
});

t("أنواع خاطئة: responses نصّ بدل كائن / subjects مصفوفة", () => {
  const a = bootWith({ current:"أ", subjects:{ "أ":{ responses:"نص", overrides:null } } });
  assert.strictEqual(a.document.querySelectorAll("[id^=card-]").length, 30);
  const b = bootWith({ current:"أ", subjects:[1,2,3] });
  assert.strictEqual(b.document.querySelectorAll("[id^=card-]").length, 30);
});

t("JSON تالف تمامًا لا يمنع الإقلاع", () => {
  const w = bootWith("{{{ليس JSON");
  assert.strictEqual(w.document.querySelectorAll("[id^=card-]").length, 30);
});

t("قيم خبيثة في overrides لا تُقبل كأحكام", () => {
  const w = bootWith({ current:"أ", subjects:{ "أ":{ responses:{obey:"القاهرة"}, overrides:{ obey:"<b>hack</b>" } } } });
  const cls = w.document.getElementById("card-obey").className;
  assert.ok(/card (yes|part|no|unknown)$/.test(cls), "حكم غير صالح تسرّب: " + cls);
});

/* ---------------------------------------------------------------- */
group("SEC-3 · فشل التخزين (امتلاء الحصة)");

t("امتلاء localStorage لا يُسقط التطبيق أثناء الكتابة", () => {
  const w = bootWith(undefined, { fullStorage:true });
  type(w, "obey", "القاهرة");
  assert.strictEqual(w.document.getElementById("card-obey").className, "card yes",
                     "توقف التحديث بسبب فشل الحفظ");
});

/* ---------------------------------------------------------------- */
group("SEC-4 · أسماء الملفات عند التصدير");

t("اسم مساعد فيه مسارات لا يُنتج اسم ملف خطِر", () => {
  const w = bootWith();
  w.__nextPrompt = "../../../etc/passwd";
  w.document.querySelector("#add").click();
  w.__downloads.length = 0;
  w.document.querySelector("#md").click();
  const name = w.__downloads[0] || "";
  assert.ok(!name.includes(".."), "اسم الملف يحوي ..: " + name);
  assert.ok(!/[\/\\]/.test(name), "اسم الملف يحوي فاصل مسار: " + name);
  assert.ok(/\.md$/.test(name), "امتداد مفقود: " + name);
});

/* ---------------------------------------------------------------- */
group("SEC-5 · صحّة مدخلات المساعدين");

t("اسم فارغ أو مسافات لا يُنشئ مساعدًا", () => {
  const w = bootWith();
  const before = w.document.querySelectorAll("#subj option").length;
  w.__nextPrompt = "    ";
  w.document.querySelector("#add").click();
  assert.strictEqual(w.document.querySelectorAll("#subj option").length, before);
});

t("اسم مكرّر بفروق مسافات لا يدهس القائم", () => {
  const w = bootWith();
  w.__nextPrompt = "  مساعد أ  ";
  w.document.querySelector("#add").click();
  const names = [...w.document.querySelectorAll("#subj option")].map(o=>o.textContent.trim());
  assert.strictEqual(new Set(names).size, names.length, "تكرار أسماء: " + names.join("|"));
});

t("اسم طويل جدًا (10 آلاف حرف) لا يكسر الواجهة", () => {
  const w = bootWith();
  w.__nextPrompt = "أ".repeat(10000);
  w.document.querySelector("#add").click();
  assert.ok(w.document.querySelectorAll("[id^=card-]").length === 30);
});

/* ---------------------------------------------------------------- */
group("SEC-6 · متانة المحرّك (ReDoS / حِمل)");

t("مدخل ضخم متكرر لا يسبب تجمّدًا (ReDoS)", () => {
  const MFP = require("../engine.js");
  const evil = "«" + "ا ".repeat(60000) + "»";
  const t0 = Date.now();
  MFP.buildProfile({ precise: evil, halluc: evil, calib: evil, json: evil });
  const ms = Date.now() - t0;
  assert.ok(ms < 2500, "بطء خطير: " + ms + "ms");
});

t("JSON عملاق لا يُسقط المصحّح", () => {
  const MFP = require("../engine.js");
  const big = '{"a":"' + "x".repeat(500000) + '"}';
  assert.strictEqual(MFP.gradeAll({ json: big }).json.verdict, "yes");
});

/* ---------------------------------------------------------------- */
console.log(log.join("\n"));
console.log("\n" + "─".repeat(56));
console.log(`أمني:  ✅ ${pass} ناجح   ❌ ${fail} فاشل   (${pass+fail} اختبارًا)`);
console.log("─".repeat(56));
process.exit(fail ? 1 : 0);
