/* يولّد PROBES.md من engine.js — مصدر واحد للحقيقة. node tools/gen-probes.js */
const fs=require("fs"), path=require("path"), M=require("../engine.js");

let md = `# 🔍 اختبارات بصمة النموذج — نسخة جاهزة للإرسال

> **مُولَّد آليًا من \`engine.js\` — لا تحرّره يدويًا.** أعد توليده بـ \`node tools/gen-probes.js\`.
>
> الصقها كاملة لأي مساعد ذكي، أو أرسل كل قسم على حدة، ثم الصق ردوده في الصفحة التفاعلية ليصحّحها المحرّك تلقائيًا.
>
> ⚠️ هذه الاختبارات تكشف **الصفات والقدرات**، ولا تُثبت **اسم النموذج**: المنصات التي توجّه الطلبات
> بين عدة نماذج لا تُختزل في اسم واحد.

`;
let n = 0, lastG = null;
for (const p of M.PROBES){
  if (p.group !== lastG){ md += `\n---\n\n## ${M.GROUPS[p.group].label}\n`; lastG = p.group; }
  n++;
  const prompt = p.prompt.replace(/\s*\n\s*/g," ").trim();
  md += `\n### ${n}. ${p.title}\n\n> ${prompt}\n\n- 🎯 **يكشف:** ${p.reveals}\n`;
}

md += `\n---\n\n## 📋 جدول التسجيل\n\n| # | الاختبار | ✅/🟡/❌ | الملاحظة |\n|---|---|---|---|\n`;
M.PROBES.forEach((p,i)=> md += `| ${i+1} | ${p.title} | | |\n`);

md += `\n---\n\n## 🧬 كيف تقرأ النتيجة؟\n\n| النمط | الاستنتاج |\n|---|---|\n`;
md += `| نجح في 1‑3 | **وكيل تنفيذي** فوق نموذج — أنت أمام منصة لا نموذجًا خامًا |\n`;
md += `| نجح في 4‑5 | متصل بالإنترنت لحظيًا |\n`;
md += `| نجح في 6‑9 | متعدد الوسائط |\n`;
md += `| فشل في 17 | ميل للهلوسة ← لا تثق بمراجعه بلا تحقّق |\n`;
md += `| فشل في 18 | لا يلتزم القيود الحرفية (مُسهِب) |\n`;
md += `| رفض 20 | لا يصحّ إسناده لاسم نموذج واحد |\n`;
md += `\n> 🎯 **القاعدة الذهبية:** قيمة المساعد لا تُقاس باسمه ولا بترتيبه في جدول، بل بأدائه على **مهامك أنت**.\n`;

const out = path.join(__dirname,"..","PROBES.md");
if (process.argv.includes("--check")){
  const cur = fs.existsSync(out) ? fs.readFileSync(out,"utf8") : "";
  if (cur !== md){ console.error("❌ PROBES.md غير متزامن مع المحرّك — شغّل: node tools/gen-probes.js"); process.exit(1); }
  console.log("✅ PROBES.md متزامن"); process.exit(0);
}
fs.writeFileSync(out, md, "utf8");
console.log("✓ أُنشئ PROBES.md — " + M.PROBES.length + " اختبارًا");
