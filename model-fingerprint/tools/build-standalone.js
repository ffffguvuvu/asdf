/* يدمج CSS+JS داخل HTML واحد يعمل بالنقر المزدوج — node tools/build-standalone.js [--check] */
const fs=require("fs"), path=require("path");
const D=path.join(__dirname,".."), rd=f=>fs.readFileSync(path.join(D,f),"utf8");

const html = rd("index.html")
  .replace('<link rel="stylesheet" href="styles.css" />', "<style>\n"+rd("styles.css")+"\n</style>")
  .replace('<script src="engine.js"></script>', "<script>\n"+rd("engine.js")+"\n</script>")
  .replace('<script src="app.js"></script>',    "<script>\n"+rd("app.js")+"\n</script>")
  .replace("<title>كاشف بصمة النموذج v2 | تصحيح آلي</title>",
           "<title>كاشف بصمة النموذج v2 — ملف واحد مستقل</title>");

if (html.includes("<script src=") || html.includes('href="styles.css"'))
  throw new Error("فشل الدمج: بقيت مراجع خارجية");

const out = path.join(D, "كاشف-بصمة-النموذج.html");
if (process.argv.includes("--check")){
  const cur = fs.existsSync(out) ? fs.readFileSync(out,"utf8") : "";
  if (cur !== html){ console.error("❌ الملف المستقل غير متزامن — شغّل: node tools/build-standalone.js"); process.exit(1); }
  console.log("✅ الملف المستقل متزامن"); process.exit(0);
}
fs.writeFileSync(out, html, "utf8");
console.log(`✓ كاشف-بصمة-النموذج.html — ${(html.length/1024).toFixed(1)} KB · بلا أي اعتماد خارجي`);
