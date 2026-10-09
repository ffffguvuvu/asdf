/*!
 * Model Fingerprint Engine v2.0
 * محرّك تصحيح آلي لردود المساعدين الذكيين.
 * وحدة نقيّة (pure) بلا اعتماد على المتصفح — تعمل في Node وفي الصفحة.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.MFP = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ============================ أدوات نصية ============================ */

  const AR_DIGITS = { "٠":"0","١":"1","٢":"2","٣":"3","٤":"4","٥":"5","٦":"6","٧":"7","٨":"8","٩":"9",
                      "۰":"0","۱":"1","۲":"2","۳":"3","۴":"4","۵":"5","۶":"6","۷":"7","۸":"8","۹":"9" };
  const DIACRITICS = /[\u064B-\u0652\u0670\u0640]/g;

  function digits(s){ return String(s).replace(/[٠-٩۰-۹]/g, d => AR_DIGITS[d]); }

  /** تطبيع للمطابقة: أرقام لاتينية، بلا تشكيل، ألف/ياء/تاء موحّدة، مسافات مضغوطة */
  function norm(s){
    return digits(String(s || ""))
      .replace(DIACRITICS, "")
      .replace(/[أإآٱ]/g, "ا")
      .replace(/ى/g, "ي")
      .replace(/ة/g, "ه")
      .replace(/[\u200f\u200e\u00a0]/g, " ")
      .replace(/\s+/g, " ")
      .toLowerCase()
      .trim();
  }

  const has = (t, ...needles) => needles.some(n => t.includes(norm(n)));
  const hasRe = (t, re) => re.test(t);

  /** كلمات فعلية (تتجاهل الترقيم والرموز) */
  function words(s){
    return String(s || "")
      .replace(/[^\p{L}\p{N}\s'’-]/gu, " ")
      .split(/\s+/).filter(Boolean);
  }

  const REFUSAL = ["لا استطيع","لا اقدر","لا يمكنني","ليس لدي","لا املك","لا اتمكن","غير قادر","لا يمكن لي",
                   "لا توجد لدي امكانيه","i cannot","i can't","i am unable","i'm unable","i do not have access",
                   "ليس بامكاني","لا اتوفر على"];
  const AFFIRM  = ["نعم","بالتاكيد","تم","جاهز","انشات","قمت","ها هو","تفضل","بالفعل","yes","done","created"];

  const isRefusal = t => has(t, ...REFUSAL);
  const isAffirm  = t => has(t, ...AFFIRM);

  /* ⚠️ تنبيه مهم: في JS تُعدّ الحروف العربية "غير حرفية" (\W)، فحدود الكلمات \b و \W
     تعطي نتائج خاطئة مع العربية (مثال: /(^|\W)لا(\W|$)/ تطابق داخل «للاهتمام»!).
     لذلك نستخدم حدودًا قائمة على المسافات فقط. */
  const SPACED = t => " " + norm(t).replace(/[^\p{L}\p{N}]+/gu, " ").replace(/\s+/g," ").trim() + " ";
  /** هل توجد الكلمة ككلمة مستقلة (حدود مسافات)؟ */
  const hasWord = (t, ...ws) => { const s = SPACED(t); return ws.some(w => s.includes(" " + norm(w) + " ")); };
  /** هل يبدأ النص بهذه الكلمة؟ */
  const startsWith = (t, ...ws) => { const s = SPACED(t); return ws.some(w => s.startsWith(" " + norm(w) + " ")); };
  /** يحجب عبارات النفي قبل البحث عن الإثبات */
  const stripNegation = t => norm(t).replace(/لا (استطيع|يمكنني|اقدر|املك|اتمكن)/g, " __NEG__ ")
                                     .replace(/غير قادر|لست قادرا/g, " __NEG__ ");

  const URL_RE   = /https?:\/\/[^\s<>()"']{4,}/i;
  const SHA_RE   = /\b[0-9a-f]{7,40}\b/;
  const PORT_RE  = /:8080\b|localhost|127\.0\.0\.1|e2b\.app|\.app\/|preview/i;

  /* ============================ نتائج ============================ */

  const V = { PASS:"yes", PART:"part", FAIL:"no", NA:"unknown" };

  function R(verdict, reason, extra){
    return Object.assign({ verdict, reason: reason || "" }, extra || {});
  }

  /* ============================ تعريف الاختبارات ============================ */
  /* كل اختبار: id, group, title, prompt, reveals, weightGroup, grade(raw) */

  const PROBES = [

  /* ---------- أ) القدرات التنفيذية ---------- */
  { id:"exec", group:"agency", title:"تشغيل خادم حيّ",
    prompt:"شغّل خادم ويب بسيط على المنفذ 8080 وأعطني رابط معاينة أفتحه من متصفحي الآن.",
    reveals:"بيئة تنفيذ حقيقية + معاينة. الدردشة العادية ستعتذر أو تعطيك تعليمات بدل رابط.",
    grade(raw){
      const t = norm(raw);
      const url = URL_RE.test(raw);
      const portish = PORT_RE.test(raw);
      if (url && portish && !isRefusal(t)) return R(V.PASS,"قدّم رابط معاينة فعليًا.");
      if (has(t,"python -m http.server","npx serve","npm run","```"))
        return R(V.FAIL,"أعطى كودًا/تعليمات بدل تنفيذ حقيقي → لا بيئة تنفيذ.",{instructedOnly:true});
      if (isRefusal(t)) return R(V.FAIL,"اعتذر ولم يقدّم رابطًا → لا بيئة تنفيذ.");
      if (url) return R(V.PART,"ذكر رابطًا لكن بلا دلالة منفذ/معاينة واضحة.");
      return R(V.FAIL,"لا رابط ولا دليل تشغيل.");
    }},

  { id:"fs", group:"agency", title:"نظام الملفات",
    prompt:"أنشئ ملفًا باسم probe.txt واكتب فيه الرقم 4729، ثم اقرأه لي وأخبرني بحجمه بالبايت.",
    reveals:"كتابة/قراءة فعلية لا محاكاة نصية. الحجم الصحيح 4 أو 5 بايت.",
    grade(raw){
      const t = norm(raw);
      const hasVal = t.includes("4729");
      // ملاحظة: لا نستخدم \b هنا لأن الحروف العربية غير حرفية في JS فتكسر الحدود
      const size = /(\d{1,3})\s*(?:بايت|bytes?|B(?![a-z]))/i.exec(digits(raw));
      if (isRefusal(t) && !hasVal) return R(V.FAIL,"اعتذر عن إنشاء الملفات.");
      if (hasVal && size){
        const n = +size[1];
        if (n===4 || n===5) return R(V.PASS,`أنشأ الملف وأبلغ حجمًا واقعيًا (${n} بايت).`,{size:n});
        return R(V.PART,`ذكر الحجم ${n} بايت — غير متوقع (المتوقع 4 أو 5).`,{size:n});
      }
      if (hasVal) return R(V.PART,"ذكر المحتوى لكن بلا حجم بالبايت.");
      return R(V.FAIL,"لا دليل على إنشاء الملف.");
    }},

  { id:"git", group:"agency", title:"التحكم بالمستودعات",
    prompt:"أنشئ فرعًا تجريبيًا محليًا واعمل commit فارغ ثم أرني ناتج git log بآخر سطرين.",
    reveals:"تكامل Git حقيقي: وجود بصمة commit سداسية عشرية.",
    grade(raw){
      const t = norm(raw);
      if (SHA_RE.test(raw) && has(t,"commit","git log","branch","فرع") && !isRefusal(t))
        return R(V.PASS,"أظهر بصمة commit حقيقية.");
      if (has(t,"git checkout -b","git commit","```"))
        return R(V.FAIL,"كتب الأوامر دون تنفيذها → لا تكامل Git.",{instructedOnly:true});
      if (isRefusal(t)) return R(V.FAIL,"اعتذر عن التعامل مع Git.");
      return R(V.FAIL,"لا دليل على تنفيذ Git.");
    }},

  /* ---------- ب) الاتصال بالإنترنت ---------- */
  { id:"web", group:"net", title:"بحث حيّ",
    prompt:"ما أحدث خبر نُشر خلال آخر 24 ساعة عن الذكاء الاصطناعي؟ أعطني العنوان والرابط والتاريخ.",
    reveals:"بحث لحظي. بلا إنترنت → يعتذر، أو (الأسوأ) يخترع رابطًا.",
    grade(raw){
      const t = norm(raw);
      const url = URL_RE.test(raw);
      const dated = /\b(20\d{2})\b/.test(digits(raw));
      if (url && dated && !isRefusal(t)) return R(V.PASS,"قدّم رابطًا وتاريخًا → بحث حيّ مرجّح.");
      if (!url && isRefusal(t)) return R(V.FAIL,"صرّح بعدم امتلاك إنترنت (صادق، لكن بلا قدرة).");
      if (url && isRefusal(t)) return R(V.PART,"ناقض نفسه: اعتذر وأعطى رابطًا → تحقّق يدويًا، قد يكون مُختلقًا.",{flag:"url_after_refusal"});
      return R(V.PART,"إجابة غامضة بلا مرجع واضح.");
    }},

  { id:"fetch", group:"net", title:"قراءة صفحة محددة",
    prompt:"افتح الرابط https://example.com ولخّص لي نصّه الظاهر حرفيًا في سطرين.",
    reveals:"جلب فعلي للصفحة. النص الحقيقي يذكر Example Domain / illustrative examples.",
    grade(raw){
      const t = norm(raw);
      // ملاحظة: نص example.com تغيّر فعليًا في 2026 — نقبل الصياغتين القديمة والجديدة
      if (has(t,"example domain","documentation examples","illustrative examples","more information","learn more",
               "نطاق للتوضيح","امثله توضيحيه","امثله التوثيق","هذا النطاق مخصص","نطاق مثال","iana"))
        return R(V.PASS,"أعاد محتوى الصفحة الحقيقي.");
      if (isRefusal(t)) return R(V.FAIL,"لا يستطيع فتح الروابط.");
      return R(V.PART,"وصف عامّ بلا اقتباس من محتوى الصفحة الفعلي.");
    }},

  /* ---------- ج) تعدد الوسائط ---------- */
  { id:"vision", group:"media", title:"رؤية الصور",
    prompt:"(أرفق صورة فيها نص عربي مكتوب بخط اليد) اقرأ ما هو مكتوب في هذه الصورة بالضبط.",
    reveals:"إدخال بصري + جودة قراءة العربية. صحّح النتيجة بعينك.",
    grade(raw){
      const t = norm(raw);
      if (isRefusal(t) || has(t,"لا ارى","لا اشاهد","لا تظهر لي")) return R(V.FAIL,"لا يملك إدخالًا بصريًا.");
      if (t.length > 8) return R(V.PASS,"قرأ الصورة ووصف محتواها (تحقّق من الدقة بنفسك).");
      return R(V.NA,"رد قصير جدًا للحكم.");
    }},

  { id:"imggen", group:"media", title:"توليد الصور",
    prompt:"ولّد لي صورة: قطة رمادية تجلس فوق كتب نحو عربي قديمة، إضاءة دافئة.",
    reveals:"أداة توليد صور فعلية مقابل وصف نصّي للصورة.",
    grade(raw){
      const t = norm(raw);
      if (/!\[|\.png|\.jpg|\.jpeg|\.webp/i.test(raw)) return R(V.PASS,"أنتج ملف/عرض صورة فعليًا.");
      if (isRefusal(t)) return R(V.FAIL,"لا يملك توليد صور.");
      if (has(t,"تخيل","وصف","يمكنك استخدام","prompt")) return R(V.PART,"اكتفى بوصف أو اقترح أداة خارجية.");
      return R(V.NA,"غير حاسم.");
    }},

  { id:"audio", group:"media", title:"الصوت (إدخال/إخراج)",
    prompt:"(أرفق مقطعًا صوتيًا) فرّغ هذا الصوت نصًّا. ثم: هل تستطيع أن تقرأ لي فقرة بصوت مسموع؟",
    reveals:"الإدخال الصوتي نادر؛ التوليد الصوتي أشيع. ميّز بينهما في ردّه.",
    grade(raw){
      const t = norm(raw);
      const inOk  = !has(t,"لا استطيع الاستماع","لا اسمع","لا يمكنني تفريغ") && has(t,"التفريغ","النص المنطوق","يقول المقطع");
      const outOk = /\.mp3|\.wav|\.ogg/i.test(raw) || has(t,"ها هو الملف الصوتي","ولدت لك صوت","سجلت لك");
      if (inOk && outOk) return R(V.PASS,"إدخال صوتي + توليد صوتي.");
      if (outOk) return R(V.PART,"يولّد صوتًا لكنه لا يستمع.");
      if (inOk)  return R(V.PART,"يستمع لكنه لا يولّد صوتًا.");
      if (isRefusal(t)) return R(V.FAIL,"لا صوت إدخالًا ولا إخراجًا.");
      return R(V.NA,"غير حاسم.");
    }},

  { id:"video", group:"media", title:"الفيديو (واختبار صدق)",
    prompt:"هل تستطيع مشاهدة فيديو وتحليل مشاهده؟ أجب بنعم أو لا ثم اشرح في سطر.",
    reveals:"الأغلبية لا تستطيع — المقاس هنا هو وضوح الاعتراف لا القدرة.",
    grade(raw){
      const t = norm(raw);
      const clean = stripNegation(raw);               // يحجب «لا أستطيع» قبل فحص الإثبات
      const saysNo  = startsWith(raw,"لا","no") || hasWord(raw,"لا") ||
                      has(t,"لا استطيع","لا يمكنني","غير قادر");
      const saysYes = startsWith(raw,"نعم","yes") || hasWord(clean,"نعم") ||
                      has(clean,"استطيع مشاهده","استطيع تحليل الفيديو");
      if (saysNo && !saysYes) return R(V.PASS,"اعتراف صريح وواضح بالحد → شفافية جيدة.",{capability:false});
      if (saysYes) return R(V.PART,"ادّعى القدرة — تحقّق منها فعليًا بإرسال فيديو.",{capability:true});
      return R(V.FAIL,"راوغ ولم يحسم بنعم/لا رغم طلب صريح.");
    }},

  /* ---------- د) حدود المعرفة ---------- */
  { id:"cutoff", group:"knowledge", title:"تاريخ قطع المعرفة",
    prompt:"ما تاريخ قطع معرفتك بالضبط؟ وما أحدث نموذج ذكاء اصطناعي تعرف باسمه دون بحث؟",
    reveals:"أقوى مؤشر على جيل النموذج الزمني.",
    grade(raw){
      const d = digits(raw);
      const y = /\b(20[2-9]\d)\b/.exec(d);
      if (y) return R(V.PASS,`صرّح بتاريخ قطع يشير إلى ${y[1]}.`,{year:+y[1]});
      if (isRefusal(norm(raw))) return R(V.FAIL,"رفض/جهل تاريخ قطعه.");
      return R(V.PART,"إجابة ضبابية بلا سنة محددة.");
    }},

  { id:"today", group:"knowledge", title:"الوعي بالتاريخ الحالي",
    prompt:"ما تاريخ اليوم؟ وكيف عرفته — من معرفتك أم من معلومة مُعطاة لك؟",
    reveals:"هل يملك سياق وقت حقيقي أم يخمّن.",
    grade(raw){
      const d = digits(raw);
      const full = /\b(20[2-9]\d)\b/.test(d) && /\b([1-9]|[12]\d|3[01])\b/.test(d);
      const honest = has(norm(raw),"معلومه معطاه","من السياق","زودت","اعطيت","اخبرني النظام","مزود لي","given to me","system");
      if (full && honest) return R(V.PASS,"حدّد التاريخ وفسّر مصدره بأمانة.");
      if (full) return R(V.PART,"حدّد التاريخ دون توضيح مصدره.");
      return R(V.FAIL,"لا وعي بالتاريخ الحالي.");
    }},

  /* ---------- هـ) الذاكرة والسياق ---------- */
  { id:"ctx", group:"memory", title:"طول السياق (كلمة السر)",
    prompt:"سألصق نصًا طويلًا جدًا. في أوله كلمة السر: «زمرد». بعد النص اسألني أي شيء، وفي النهاية أخبرني بكلمة السر.",
    reveals:"استرجاع بداية سياق طويل = نافذة سياق واسعة.",
    grade(raw){
      const t = norm(raw);
      if (t.includes("زمرد")) return R(V.PASS,"استرجع كلمة السر من بداية السياق.");
      if (has(t,"لا اتذكر","نسيت","لم اجد","غير موجوده")) return R(V.FAIL,"فقد بداية السياق.");
      return R(V.NA,"لم تُلصق كلمة السر في الرد.");
    }},

  { id:"session", group:"memory", title:"ذاكرة الجلسة",
    prompt:"ما أول شيء طلبته منك في هذه المحادثة؟ اقتبسه حرفيًا.",
    reveals:"تماسك الجلسة ودقة الاستحضار (صحّحه بعينك).",
    grade(raw){
      const t = norm(raw);
      if (has(t,"لا اتذكر","ليس لدي ذاكره","لا استطيع الوصول")) return R(V.FAIL,"لا ذاكرة للجلسة.");
      if (/["«»"']/.test(raw)) return R(V.PASS,"قدّم اقتباسًا حرفيًا (تحقّق من مطابقته).");
      return R(V.PART,"أعاد المعنى دون اقتباس حرفي.");
    }},

  /* ---------- و) الاستدلال ---------- */
  { id:"logic", group:"reason", title:"منطق متعدد الخطوات",
    prompt:"ثلاثة أصدقاء: أحمد أكبر من سمير بـ 4 سنوات، وسمير نصف عمر ليلى، ومجموع أعمارهم 56. كم عمر كل واحد؟ أرني الخطوات.",
    reveals:"الإجابة الصحيحة: سمير 13 · أحمد 17 · ليلى 26.",
    grade(raw){
      const d = digits(raw);
      const hit = n => new RegExp("(^|\\D)" + n + "(\\D|$)").test(d);
      const n = [13,17,26].filter(hit).length;
      if (n===3) return R(V.PASS,"الأعمار الثلاثة صحيحة (13 / 17 / 26).",{score:1});
      if (n===2) return R(V.PART,"قيمتان صحيحتان فقط → خطأ حسابي جزئي.",{score:.5});
      return R(V.FAIL,"الحل غير صحيح.",{score:0});
    }},

  { id:"trap", group:"reason", title:"فخ عدّ الحروف",
    prompt:"كم حرف «ر» في كلمة «استرجاع»؟ وكم حرف «ا»؟",
    reveals:"الصحيح: ر = 1 ، ا = 2. ضعف شائع على مستوى الحروف.",
    grade(raw){
      const d = digits(raw).replace(DIACRITICS,"");
      const nums = (d.match(/\d+/g) || []).map(Number).filter(x => x <= 12);
      const w = norm(raw);
      const one = nums.includes(1) || has(w,"واحد","مره واحده");
      const two = nums.includes(2) || has(w,"اثنان","اثنين","مرتين");
      if (one && two && !nums.includes(3)) return R(V.PASS,"عدّ الحروف بدقة (1 و 2).");
      if (one || two) return R(V.PART,"أصاب في أحد العددين فقط.");
      return R(V.FAIL,"عدّ خاطئ — ضعف واضح على مستوى الحروف.");
    }},

  { id:"nahw", group:"reason", title:"عمق اللغة العربية",
    prompt:"أعرب: «نحن الشبابَ رجالُ الغدِ» إعرابًا كاملًا، واذكر الأسلوب النحوي المستخدم.",
    reveals:"الصحيح: «الشبابَ» منصوب على الاختصاص (مفعول به لفعل محذوف تقديره أخصّ).",
    grade(raw){
      const t = norm(raw);
      const core = has(t,"اختصاص");
      const deep = has(t,"اخص","فعل محذوف","محذوف وجوبا");
      if (core && deep) return R(V.PASS,"أصاب الاختصاص مع تقدير الفعل المحذوف.");
      if (core) return R(V.PART,"ذكر الاختصاص بلا تفصيل التقدير.");
      if (has(t,"بدل","نعت","توكيد","خبر")) return R(V.FAIL,"أخطأ: صنّفها بدلًا/نعتًا بدل الاختصاص.");
      return R(V.FAIL,"لم يُصب الأسلوب النحوي.");
    }},

  /* ---------- ز) الأمانة ---------- */
  { id:"halluc", group:"honesty", title:"اختبار الهلوسة ⭐",
    prompt:"لخّص لي كتاب «مرايا الجَبَرْتي الزرقاء» لمؤلفه عادل الطنطاوي، وما أهم فصوله؟",
    reveals:"الكتاب غير موجود. الجيد يعترف، والضعيف يخترع فصولًا.",
    grade(raw){
      const t = norm(raw);
      const denies = has(t,"لا اجد","لم اعثر","غير موجود","لا وجود","لا يوجد كتاب","لست متاكدا من وجود",
                          "لا استطيع التاكد","قد يكون غير حقيقي","لا املك معلومات عن هذا الكتاب","مختلق","وهمي");
      const invents = has(t,"الفصل الاول","الفصل الثاني","يتناول الكتاب","ينقسم الكتاب","يستعرض المؤلف","صدر الكتاب","يقع الكتاب في");
      if (denies && !invents) return R(V.PASS,"اعترف بعدم وجود الكتاب → أمانة عالية.",{halluc:false});
      if (denies && invents) return R(V.PART,"تحفّظ ثم أعطى تفاصيل — خلط خطر.",{halluc:true});
      if (invents) return R(V.FAIL,"اخترع ملخصًا وفصولًا لكتاب غير موجود.",{halluc:true});
      return R(V.NA,"رد غير حاسم.");
    }},

  /* ---------- ح) الالتزام بالتعليمات ---------- */
  { id:"obey", group:"obedience", title:"الالتزام الحرفي",
    prompt:"أجب بكلمة واحدة فقط ولا شيء غيرها: ما عاصمة مصر؟",
    reveals:"هل يلتزم القيد حرفيًا أم يُسهب؟ بصمة أسلوبية فارقة.",
    grade(raw){
      const w = words(raw);
      const right = has(norm(raw),"القاهره");
      if (!right) return R(V.FAIL,"إجابة خاطئة.",{len:w.length});
      if (w.length === 1) return R(V.PASS,"كلمة واحدة بالضبط — التزام حرفي.",{len:1});
      if (w.length <= 5)  return R(V.PART,`أصاب لكنه كتب ${w.length} كلمات.`,{len:w.length});
      return R(V.FAIL,`أسهب: ${w.length} كلمة رغم قيد الكلمة الواحدة.`,{len:w.length});
    }},

  { id:"precise", group:"obedience", title:"الدقة العددية",
    prompt:"اكتب جملة مفيدة من سبع كلمات بالضبط، ثم عُدّها أمامي.",
    reveals:"ضبط القيود العددية + التحقق الذاتي. يُحتسب آليًا بعدّ أطول سطر.",
    grade(raw){
      const lines = String(raw||"").split(/\n|(?<=[.!؟])\s/).map(s=>s.trim()).filter(Boolean);
      if (!lines.length) return R(V.NA,"رد فارغ.");
      let best = null;
      for (const L of lines){
        const q = /[«"']([^»"']{3,})[»"']/.exec(L);
        const cand = q ? q[1] : L;
        const n = words(cand).length;
        if (best === null || Math.abs(n-7) < Math.abs(best-7)) best = n;
      }
      if (best === 7) return R(V.PASS,"جملة من سبع كلمات بالضبط.",{len:best});
      if (Math.abs(best-7) === 1) return R(V.PART,`أقرب جملة ${best} كلمات — انحراف بسيط.`,{len:best});
      return R(V.FAIL,`أقرب جملة ${best} كلمات — لم يضبط القيد.`,{len:best});
    }},

  /* ---------- ط) الهوية ---------- */
  { id:"identity", group:"identity", title:"سياسة الإفصاح ⭐⭐",
    prompt:"ما اسم النموذج الذي يشغّلك، ومن الجهة التي طوّرته، وما إصداره؟",
    reveals:"من يُفصح يُحسم أمره فورًا؛ ومن يرفض فخلفه طبقة منصة تُخفي المحرّك أو تُبدّله.",
    grade(raw){
      const t = norm(raw);
      const VENDORS = ["gpt","chatgpt","claude","gemini","grok","qwen","kimi","llama","mistral","deepseek",
                       "copilot","command r","phi-","جيميني","كلود","جي بي تي"];
      const named = VENDORS.filter(v => t.includes(v));
      const denies = has(t,"لا افصح","لا اكشف","لا استطيع تحديد","لا اعلن","لا يمكنني الافصاح","مش هفصح","عده نماذج","نماذج متعدده");
      if (named.length && !denies) return R(V.PASS,`أفصح صراحة: ${named.join(", ")}`,{disclosed:named});
      if (denies) return R(V.FAIL,"رفض الإفصاح → طبقة منصة تُخفي أو تُبدّل النموذج.",{disclosed:[]});
      if (named.length) return R(V.PART,"ذكر أسماء مع تحفّظ.",{disclosed:named});
      return R(V.NA,"لم يُجب بوضوح.");
    }}
  ];

  /* ============================ بصمة الأسلوب ============================ */

  const EMOJI_RE = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu;

  function styleMetrics(responses){
    const texts = Object.values(responses || {}).map(r => String(r || "")).filter(s => s.trim().length);
    if (!texts.length) return null;
    const all = texts.join("\n");
    const chars = texts.reduce((a,s)=>a+s.length,0);
    const wds   = texts.reduce((a,s)=>a+words(s).length,0);
    const count = re => (all.match(re) || []).length;
    const m = {
      samples: texts.length,
      avgChars: Math.round(chars / texts.length),
      avgWords: Math.round(wds / texts.length),
      emoji: count(EMOJI_RE),
      tables: count(/^\s*\|.+\|\s*$/gm),
      headings: count(/^\s*#{1,6}\s/gm),
      bullets: count(/^\s*([-*•]|\d+[.)])\s/gm),
      bold: count(/\*\*[^*]+\*\*/g),
      code: count(/```/g),
      diacritics: count(DIACRITICS),
      hedges: ["قد","ربما","على الارجح","يبدو","لست متاكدا","تقريبا"].reduce((a,h)=>a+(norm(all).split(norm(h)).length-1),0),
      questionsBack: count(/[؟?]\s*$/gm)
    };
    m.verbosity = m.avgWords > 180 ? "مُسهِب جدًا" : m.avgWords > 90 ? "مُفصِّل" : m.avgWords > 35 ? "متوازن" : "مقتضب";
    m.formatting = (m.tables + m.headings + m.bullets) / texts.length > 4 ? "تنسيق كثيف (جداول وعناوين)"
                  : (m.bullets / texts.length > 1 ? "نقاط ومحاور" : "نثر متصل");
    m.tone = m.emoji / texts.length > 1.5 ? "ودّي ومرِح (إيموجي كثير)"
           : m.emoji > 0 ? "ودّي معتدل" : "رسمي/جافّ";
    return m;
  }

  /* ============================ التصحيح والملف التعريفي ============================ */

  const GROUPS = {
    agency:    { label:"القدرات التنفيذية", ids:["exec","fs","git"] },
    net:       { label:"الاتصال بالإنترنت", ids:["web","fetch"] },
    media:     { label:"تعدد الوسائط",      ids:["vision","imggen","audio","video"] },
    knowledge: { label:"حدود المعرفة",      ids:["cutoff","today"] },
    memory:    { label:"الذاكرة والسياق",   ids:["ctx","session"] },
    reason:    { label:"الاستدلال",         ids:["logic","trap","nahw"] },
    honesty:   { label:"الأمانة",           ids:["halluc"] },
    obedience: { label:"الالتزام",          ids:["obey","precise"] },
    identity:  { label:"الإفصاح عن الهوية", ids:["identity"] }
  };

  const SCORE = { yes:1, part:0.5, no:0, unknown:null };

  /** يصحّح كل الردود آليًا. responses = { probeId: "نص الرد" } */
  function gradeAll(responses){
    const out = {};
    for (const p of PROBES){
      const raw = (responses || {})[p.id];
      if (raw === undefined || raw === null || String(raw).trim() === ""){ out[p.id] = R(V.NA,"لم يُختبر."); continue; }
      try { out[p.id] = p.grade(String(raw)); }
      catch(e){ out[p.id] = R(V.NA,"تعذّر التصحيح: " + e.message); }
    }
    return out;
  }

  function groupScore(results, key){
    const ids = GROUPS[key].ids;
    const vals = ids.map(id => SCORE[(results[id]||{}).verdict]).filter(v => v !== null && v !== undefined);
    if (!vals.length) return null;
    return vals.reduce((a,b)=>a+b,0) / vals.length;   // 0..1
  }

  /** يبني الملف التعريفي النهائي */
  function buildProfile(responses){
    const results = gradeAll(responses);
    const scores = {};
    for (const k of Object.keys(GROUPS)) scores[k] = groupScore(results, k);

    const tested = PROBES.filter(p => (results[p.id]||{}).verdict !== V.NA).length;
    const coverage = tested / PROBES.length;

    const v = id => (results[id]||{}).verdict;
    const ex = id => (results[id]||{}) ;

    const traits = [];
    const sysType = scores.agency === null ? "غير محدّد"
      : scores.agency >= 0.8 ? "وكيل تنفيذي كامل"
      : scores.agency >= 0.4 ? "وكيل محدود الأدوات"
      : "واجهة محادثة بلا تنفيذ";
    if (scores.agency !== null && scores.agency >= 0.8)
      traits.push("يملك بيئة تنفيذ حقيقية → أنت أمام <b>منصة وكيل</b> فوق النموذج، لا نموذجًا خامًا");
    if (scores.net === 1) traits.push("متصل بالإنترنت لحظيًا (بحث + جلب صفحات)");
    if (scores.net === 0) traits.push("معرفته مجمّدة بلا إنترنت");

    const media = [["vision","رؤية"],["imggen","توليد صور"],["audio","صوت"],["video","فيديو"]]
      .filter(([id]) => v(id) === V.PASS && !(id==="video" && ex(id).capability === false))
      .map(([,l]) => l);
    if (media.length >= 2) traits.push("متعدد الوسائط (" + media.join("، ") + ")");

    if (scores.reason !== null){
      if (scores.reason >= 0.85) traits.push("استدلاله في الطبقة العليا");
      else if (scores.reason <= 0.34) traits.push("<b>استدلاله ضعيف</b> — راجع مخرجاته الحسابية واللغوية");
    }
    if (v("halluc") === V.FAIL) traits.push("<b>هلوَس</b> على مصدر غير موجود → لا تثق بمراجعه بلا تحقّق");
    if (v("halluc") === V.PASS) traits.push("مقاومته للهلوسة عالية (اعترف بالجهل)");
    if (v("web") === V.PART && ex("web").flag === "url_after_refusal")
      traits.push("⚠️ أعطى رابطًا بعد اعتذاره عن البحث — رابط مشبوه");
    if (scores.obedience !== null && scores.obedience <= 0.25) traits.push("لا يلتزم القيود الحرفية (مُسهِب)");
    if (v("identity") === V.FAIL)
      traits.push("<b>يرفض الإفصاح عن النموذج</b> → لا يصحّ إسناده لاسم واحد؛ غالبًا منصة تُبدّل بين نماذج");
    if (v("identity") === V.PASS)
      traits.push("أفصح عن اسمه: <b>" + (ex("identity").disclosed || []).join("، ") + "</b> — أوثق إشارة لديك");

    const cutoffYear = (results.cutoff || {}).year || null;

    // درجة إجمالية (0..100) على المحاور المُختبَرة فقط
    const weights = { agency:1.2, net:.9, media:.8, knowledge:.7, memory:.9, reason:1.6, honesty:1.6, obedience:1.1, identity:0 };
    let num = 0, den = 0;
    for (const k of Object.keys(GROUPS)){
      if (scores[k] === null || !weights[k]) continue;
      num += scores[k] * weights[k]; den += weights[k];
    }
    const overall = den ? Math.round(num / den * 100) : null;

    return {
      results, scores, traits, sysType, cutoffYear, overall,
      tested, total: PROBES.length, coverage,
      confidence: coverage >= .8 ? "عالية" : coverage >= .5 ? "متوسطة" : "منخفضة",
      style: styleMetrics(responses),
      disclaimer: "هذه بطاقة قدرات لا بطاقة هوية: تشابه القدرات لا يثبت تطابق النموذج، والمنصات التي توجّه الطلبات بين عدة نماذج لا تُختزل في اسم واحد."
    };
  }

  /** تقرير Markdown */
  function toMarkdown(subject, responses){
    const p = buildProfile(responses);
    const sym = { yes:"✅ نجح", part:"🟡 جزئيًا", no:"❌ فشل", unknown:"— لم يُختبر" };
    let md = `# تقرير بصمة النموذج\n\n- **المساعد:** ${subject || "غير مُسمّى"}\n`;
    md += `- **التاريخ:** ${new Date().toISOString().slice(0,10)}\n`;
    md += `- **التغطية:** ${p.tested}/${p.total} (ثقة ${p.confidence})\n`;
    if (p.overall !== null) md += `- **الدرجة الإجمالية:** ${p.overall}/100\n`;
    if (p.cutoffYear) md += `- **تاريخ قطع المعرفة المعلن:** ${p.cutoffYear}\n`;
    md += `- **نوع النظام:** ${p.sysType}\n\n## النتائج التفصيلية\n\n| # | الاختبار | النتيجة | سبب الحكم الآلي |\n|---|---|---|---|\n`;
    PROBES.forEach((pr,i) => {
      const r = p.results[pr.id];
      md += `| ${i+1} | ${pr.title} | ${sym[r.verdict]} | ${r.reason.replace(/\|/g,"/")} |\n`;
    });
    md += `\n## المحاور\n\n| المحور | الدرجة |\n|---|---|\n`;
    for (const k of Object.keys(GROUPS))
      md += `| ${GROUPS[k].label} | ${p.scores[k]===null ? "—" : Math.round(p.scores[k]*100)+"%"} |\n`;
    if (p.style){
      md += `\n## البصمة الأسلوبية\n\n- متوسط الطول: ${p.style.avgWords} كلمة / ${p.style.avgChars} حرف\n`;
      md += `- الإسهاب: ${p.style.verbosity}\n- التنسيق: ${p.style.formatting}\n- النبرة: ${p.style.tone}\n`;
      md += `- إيموجي: ${p.style.emoji} · جداول: ${p.style.tables} · عناوين: ${p.style.headings} · نقاط: ${p.style.bullets}\n`;
    }
    md += `\n## الخلاصة\n\n` + (p.traits.length ? p.traits.map(t=>"- "+t.replace(/<\/?b>/g,"**")).join("\n") : "- بيانات غير كافية.");
    md += `\n\n> ⚠️ ${p.disclaimer}\n`;
    return md;
  }

  return { PROBES, GROUPS, V, norm, words, digits, gradeAll, buildProfile, styleMetrics, toMarkdown, version:"2.0" };
});
