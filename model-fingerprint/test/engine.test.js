/* اختبارات محرّك التصحيح — تُشغَّل: node test/engine.test.js */
const assert = require("assert");
const MFP = require("../engine.js");
const F = require("./fixtures.js");

let pass = 0, fail = 0;
const results = [];
function t(name, fn){
  try { fn(); pass++; results.push("  ✅ " + name); }
  catch(e){ fail++; results.push("  ❌ " + name + "\n       → " + e.message); }
}
function group(name){ results.push("\n▸ " + name); }

const vOf = (res, id) => res[id].verdict;

/* ---------------------------------------------------------------- */
group("بنية المحرّك");

t("يصدّر 20 اختبارًا بمعرّفات فريدة", () => {
  assert.strictEqual(MFP.PROBES.length, 20);
  const ids = MFP.PROBES.map(p => p.id);
  assert.strictEqual(new Set(ids).size, 20, "توجد معرّفات مكرّرة");
});

t("كل اختبار يملك نصًّا ومصحّحًا ومجموعة معروفة", () => {
  for (const p of MFP.PROBES){
    assert.ok(p.prompt && p.prompt.length > 10, p.id + ": نص ناقص");
    assert.strictEqual(typeof p.grade, "function", p.id + ": لا مصحّح");
    assert.ok(MFP.GROUPS[p.group], p.id + ": مجموعة غير معرّفة");
  }
});

t("كل مجموعة تشير إلى اختبارات موجودة فعلًا", () => {
  const ids = new Set(MFP.PROBES.map(p => p.id));
  for (const k of Object.keys(MFP.GROUPS))
    for (const id of MFP.GROUPS[k].ids)
      assert.ok(ids.has(id), `المجموعة ${k} تشير إلى ${id} غير الموجود`);
});

t("التطبيع يوحّد الأرقام العربية والتشكيل والهمزات", () => {
  assert.strictEqual(MFP.norm("٤٧٢٩"), "4729");
  assert.strictEqual(MFP.norm("الشَّبابَ"), "الشباب");
  assert.strictEqual(MFP.norm("أحمد"), "احمد");
});

t("عدّ الكلمات يتجاهل الترقيم", () => {
  assert.strictEqual(MFP.words("القاهرة.").length, 1);
  assert.strictEqual(MFP.words("«العلم نور يضيء دروب الحياة أمام الناس»").length, 7);
});

/* ---------------------------------------------------------------- */
group("شخصية 1: وكيل تنفيذي قوي");
const A = MFP.gradeAll(F.AGENT_STRONG);

t("يرصد تشغيل خادم حقيقي برابط معاينة", () => assert.strictEqual(vOf(A,"exec"), "yes"));
t("يرصد إنشاء ملف بحجم واقعي", () => {
  assert.strictEqual(vOf(A,"fs"), "yes");
  assert.strictEqual(A.fs.size, 5);
});
t("يرصد بصمة commit", () => assert.strictEqual(vOf(A,"git"), "yes"));
t("يرصد البحث الحيّ (رابط + تاريخ)", () => assert.strictEqual(vOf(A,"web"), "yes"));
t("يرصد قراءة example.com الحقيقية", () => assert.strictEqual(vOf(A,"fetch"), "yes"));
t("يرصد توليد الصور من امتداد الملف", () => assert.strictEqual(vOf(A,"imggen"), "yes"));
t("يرصد الصوت إدخالًا وإخراجًا", () => assert.strictEqual(vOf(A,"audio"), "yes"));
t("يعتبر الاعتراف الصريح بعدم رؤية الفيديو نجاحًا في الشفافية", () => {
  assert.strictEqual(vOf(A,"video"), "yes");
  assert.strictEqual(A.video.capability, false);
});
t("يستخرج سنة قطع المعرفة", () => {
  assert.strictEqual(vOf(A,"cutoff"), "yes");
  assert.strictEqual(A.cutoff.year, 2025);
});
t("يرصد الوعي بالتاريخ مع ذكر المصدر", () => assert.strictEqual(vOf(A,"today"), "yes"));
t("يرصد استرجاع كلمة السر «زمرد»", () => assert.strictEqual(vOf(A,"ctx"), "yes"));
t("يصحّح مسألة الأعمار (13/17/26)", () => assert.strictEqual(vOf(A,"logic"), "yes"));
t("يصحّح عدّ الحروف", () => assert.strictEqual(vOf(A,"trap"), "yes"));
t("يرصد الإجابة النحوية الصحيحة (الاختصاص + التقدير)", () => assert.strictEqual(vOf(A,"nahw"), "yes"));
t("يرصد مقاومة الهلوسة", () => {
  assert.strictEqual(vOf(A,"halluc"), "yes");
  assert.strictEqual(A.halluc.halluc, false);
});
t("يرصد الالتزام بكلمة واحدة", () => {
  assert.strictEqual(vOf(A,"obey"), "yes");
  assert.strictEqual(A.obey.len, 1);
});
t("يرصد رفض الإفصاح عن الهوية", () => assert.strictEqual(vOf(A,"identity"), "no"));

/* ---------------------------------------------------------------- */
group("شخصية 2: دردشة ضعيفة");
const B = MFP.gradeAll(F.CHAT_WEAK);

t("يميّز إعطاء الكود عن التنفيذ الفعلي (لا قدرة)", () => {
  assert.strictEqual(vOf(B,"exec"), "no");
  assert.strictEqual(B.exec.instructedOnly, true);
});
t("يرصد انعدام نظام الملفات", () => assert.strictEqual(vOf(B,"fs"), "no"));
t("يرصد كتابة أوامر git دون تنفيذ", () => {
  assert.strictEqual(vOf(B,"git"), "no");
  assert.strictEqual(B.git.instructedOnly, true);
});
t("🚩 يرفع علم الرابط المشبوه بعد الاعتذار", () => {
  assert.strictEqual(vOf(B,"web"), "part");
  assert.strictEqual(B.web.flag, "url_after_refusal");
});
t("يرصد عدم قراءة الصفحة فعليًا", () => assert.strictEqual(vOf(B,"fetch"), "part"));
t("يرصد انعدام الرؤية", () => assert.strictEqual(vOf(B,"vision"), "no"));
t("يرصد المراوغة في سؤال نعم/لا", () => assert.strictEqual(vOf(B,"video"), "no"));
t("يرصد فقد كلمة السر", () => assert.strictEqual(vOf(B,"ctx"), "no"));
t("يرصد الحل المنطقي الخاطئ", () => assert.strictEqual(vOf(B,"logic"), "no"));
t("يرصد عدّ الحروف الخاطئ", () => assert.strictEqual(vOf(B,"trap"), "no"));
t("يرصد الخطأ النحوي (بدل بدل الاختصاص)", () => assert.strictEqual(vOf(B,"nahw"), "no"));
t("🚩 يكشف اختلاق فصول كتاب غير موجود", () => {
  assert.strictEqual(vOf(B,"halluc"), "no");
  assert.strictEqual(B.halluc.halluc, true);
});
t("يرصد الإسهاب رغم قيد الكلمة الواحدة", () => {
  assert.strictEqual(vOf(B,"obey"), "no");
  assert.ok(B.obey.len > 5);
});

/* ---------------------------------------------------------------- */
group("شخصية 3: نموذج يُفصح عن اسمه");
const C = MFP.gradeAll(F.MODEL_DISCLOSED);

t("يلتقط اسم النموذج المُعلن", () => {
  assert.strictEqual(vOf(C,"identity"), "yes");
  assert.ok(C.identity.disclosed.includes("claude"));
});
t("يستخرج سنة قطع 2024", () => assert.strictEqual(C.cutoff.year, 2024));
t("يرصد جملة السبع كلمات بالضبط", () => {
  assert.strictEqual(vOf(C,"precise"), "yes");
  assert.strictEqual(C.precise.len, 7);
});
t("يرصد انعدام الأدوات التنفيذية", () => {
  ["exec","fs","git"].forEach(id => assert.strictEqual(vOf(C,id), "no", id));
});

/* ---------------------------------------------------------------- */
group("الملف التعريفي المُستنتَج");

const pA = MFP.buildProfile(F.AGENT_STRONG);
const pB = MFP.buildProfile(F.CHAT_WEAK);
const pC = MFP.buildProfile(F.MODEL_DISCLOSED);
const pE = MFP.buildProfile(F.EMPTY);

t("يصنّف الوكيل القوي «وكيل تنفيذي كامل»", () => assert.strictEqual(pA.sysType, "وكيل تنفيذي كامل"));
t("يصنّف الدردشة «واجهة محادثة بلا تنفيذ»", () => assert.ok(/بلا تنفيذ|محدود/.test(pB.sysType)));
t("درجة الوكيل القوي أعلى من الدردشة الضعيفة بفارق واضح", () => {
  assert.ok(pA.overall > pB.overall + 30, `A=${pA.overall} B=${pB.overall}`);
});
t("الدرجات محصورة بين 0 و 100", () => {
  [pA,pB,pC].forEach(p => assert.ok(p.overall >= 0 && p.overall <= 100));
});
t("التغطية والثقة تُحسبان بدقة", () => {
  assert.strictEqual(pA.tested, 20);
  assert.strictEqual(pA.confidence, "عالية");
});
t("الحالة الفارغة لا تنهار", () => {
  assert.strictEqual(pE.tested, 0);
  assert.strictEqual(pE.overall, null);
  assert.strictEqual(pE.confidence, "منخفضة");
  assert.strictEqual(pE.style, null);
});
t("يستنتج رفض الإفصاح في خلاصة الوكيل", () => {
  assert.ok(pA.traits.some(x => x.includes("يرفض الإفصاح")));
});
t("يستنتج الهلوسة في خلاصة الدردشة", () => {
  assert.ok(pB.traits.some(x => x.includes("هلوَس")));
});
t("يستخرج سنة القطع في الملف التعريفي", () => assert.strictEqual(pA.cutoffYear, 2025));
t("محاور غير مُختبرة تُعاد كـ null لا كصفر", () => {
  const partial = MFP.buildProfile({ logic: F.AGENT_STRONG.logic });
  assert.strictEqual(partial.scores.agency, null);
  assert.strictEqual(partial.scores.reason, 1);
});

/* ---------------------------------------------------------------- */
group("البصمة الأسلوبية");

t("يقيس الإسهاب ويميّز المقتضب عن المُسهب", () => {
  const terse = MFP.styleMetrics({ a:"القاهرة", b:"نعم", c:"لا" });
  const long  = MFP.styleMetrics({ a:"كلمة ".repeat(200) });
  assert.strictEqual(terse.verbosity, "مقتضب");
  assert.strictEqual(long.verbosity, "مُسهِب جدًا");
});
t("يرصد الإيموجي والجداول والعناوين", () => {
  const m = MFP.styleMetrics({ a:"# عنوان\n| أ | ب |\n- نقطة\n🎯 رائع" });
  assert.ok(m.emoji >= 1 && m.tables >= 1 && m.headings >= 1 && m.bullets >= 1);
});
t("يصنّف النبرة الرسمية بلا إيموجي", () => {
  assert.strictEqual(MFP.styleMetrics({ a:"نص رسمي بلا رموز." }).tone, "رسمي/جافّ");
});

/* ---------------------------------------------------------------- */
group("تقرير Markdown");

const md = MFP.toMarkdown("مساعد تجريبي", F.AGENT_STRONG);
t("يولّد تقريرًا يحوي العنوان والجداول والخلاصة", () => {
  assert.ok(md.includes("# تقرير بصمة النموذج"));
  assert.ok(md.includes("مساعد تجريبي"));
  assert.ok(md.includes("| # | الاختبار | النتيجة"));
  assert.ok(md.includes("## الخلاصة"));
  assert.ok(md.includes("الدرجة الإجمالية"));
});
t("يحتوي صفًّا لكل اختبار", () => {
  MFP.PROBES.forEach(p => assert.ok(md.includes(p.title), "مفقود: " + p.title));
});
t("لا يكسر جدول Markdown بعلامة |", () => {
  const bad = MFP.toMarkdown("x", { obey: "القاهرة | والإسكندرية" });
  bad.split("\n").filter(l => l.startsWith("| ")).forEach(l => {
    assert.ok(l.split("|").length <= 7, "صف مكسور: " + l);
  });
});
t("يتضمّن التنويه بأنها بطاقة قدرات لا هوية", () => {
  assert.ok(md.includes("بطاقة قدرات لا بطاقة هوية"));
});

/* ---------------------------------------------------------------- */
group("المتانة ضد مدخلات شاذّة");

t("لا ينهار مع null / أرقام / نص فارغ", () => {
  const r = MFP.gradeAll({ exec:null, fs:12345, obey:"   ", trap:undefined });
  assert.strictEqual(r.exec.verdict, "unknown");
  assert.strictEqual(r.obey.verdict, "unknown");
  assert.ok(r.fs.verdict);
});
t("لا ينهار مع نص ضخم جدًا (1MB)", () => {
  const big = "ا".repeat(1e6);
  const r = MFP.gradeAll({ halluc: big });
  assert.ok(r.halluc.verdict);
});
t("يتجاهل معرّفات غير معروفة", () => {
  const r = MFP.gradeAll({ not_a_probe: "شيء ما" });
  assert.strictEqual(r.not_a_probe, undefined);
  assert.strictEqual(Object.keys(r).length, 20);
});

/* ---------------------------------------------------------------- */
group("انحدارات مُوثّقة (أخطاء سابقة)");

t("🐞 [BUG-1] حدود الكلمات العربية: «للاهتمام» لا تُقرأ كـ «لا»", () => {
  const r = MFP.gradeAll({ video: "تحليل المحتوى المرئي مجال مثير للاهتمام ويعتمد على عدة عوامل." });
  assert.strictEqual(r.video.verdict, "no", "كلمة «للاهتمام» خُدع بها كاشف النفي");
});

t("🐞 [BUG-1ب] «لا أستطيع مشاهدة» لا تُحسب ادّعاءً بالقدرة", () => {
  const r = MFP.gradeAll({ video: "لا أستطيع مشاهدة الفيديو إطلاقًا." });
  assert.strictEqual(r.video.verdict, "yes");
  assert.strictEqual(r.video.capability, false);
});

t("🐞 [BUG-2] قراءة الحجم بالبايت رغم التصاق كلمة عربية", () => {
  assert.strictEqual(MFP.gradeAll({ fs: "المحتوى 4729 والحجم 5 بايت." }).fs.size, 5);
  assert.strictEqual(MFP.gradeAll({ fs: "4729 — الحجم: ٤ بايت" }).fs.size, 4);
});

t("🐞 [BUG-3] الكود بلا تنفيذ لا يُمنح نصف درجة قدرة", () => {
  const p = MFP.buildProfile({ exec:"```\npython -m http.server 8080\n```", git:"```\ngit commit\n```" });
  assert.strictEqual(p.scores.agency, 0, "تعليمات الكود رفعت درجة القدرة زورًا");
});

t("🐞 [BUG-4] null لا يُصحَّح كنص «null»", () => {
  assert.strictEqual(MFP.gradeAll({ exec:null }).exec.verdict, "unknown");
});

t("🧪 ادّعاء القدرة على الفيديو يُعلَّم للتحقق لا يُقبل", () => {
  const r = MFP.gradeAll({ video: "نعم، أستطيع مشاهدة الفيديو وتحليل مشاهده." });
  assert.strictEqual(r.video.verdict, "part");
  assert.strictEqual(r.video.capability, true);
});

/* ---------------------------------------------------------------- */
group("تزامن الوثائق مع المحرّك");

t("PROBES.md مُولّد من نفس المحرّك (لا تفارق)", () => {
  const { execFileSync } = require("child_process");
  execFileSync(process.execPath, [require("path").join(__dirname,"..","tools","gen-probes.js"), "--check"]);
});

t("كل نصوص الاختبارات موجودة في PROBES.md حرفيًا", () => {
  const md = require("fs").readFileSync(require("path").join(__dirname,"..","PROBES.md"),"utf8");
  MFP.PROBES.forEach(p => assert.ok(md.includes(p.prompt.replace(/\s*\n\s*/g," ").trim()), "مفقود: " + p.id));
});

/* ---------------------------------------------------------------- */
console.log(results.join("\n"));
console.log("\n" + "─".repeat(56));
console.log(`النتيجة:  ✅ ${pass} ناجح   ❌ ${fail} فاشل   (${pass + fail} اختبارًا)`);
console.log("─".repeat(56));
process.exit(fail ? 1 : 0);
