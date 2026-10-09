/* يولّد تقارير عيّنة من الشخصيات الاختبارية — node tools/make-sample.js */
const fs = require("fs"), path = require("path");
const MFP = require("../engine.js");
const F = require("../test/fixtures.js");
const out = path.join(__dirname, "..", "samples");
const map = { "agent-strong":["وكيل تنفيذي قوي",F.AGENT_STRONG],
              "chat-weak":["دردشة ضعيفة",F.CHAT_WEAK],
              "model-disclosed":["نموذج يُفصح عن اسمه",F.MODEL_DISCLOSED] };
for (const [file,[name,resp]] of Object.entries(map)){
  const md = MFP.toMarkdown(name, resp);
  fs.writeFileSync(path.join(out, `report-${file}.md`), md, "utf8");
  const p = MFP.buildProfile(resp);
  console.log(`✓ ${file.padEnd(16)} درجة=${String(p.overall).padStart(3)}  نوع=${p.sysType}`);
}
