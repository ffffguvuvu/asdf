# -*- coding: utf-8 -*-
"""
build.py — يبني ملف HTML ملوّنًا واحدًا يحتوي كل أسئلة الذكاء (IQ) مع الأشكال والشرح.
التشغيل:  python3 src/build.py
الناتج :  iq-guide.html  في جذر المستودع.
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from model import AR_LABELS, balance_answers     # noqa: E402
from content_a import CHAPTERS_A                 # noqa: E402
from content_b import CHAPTERS_B                 # noqa: E402
from content_c import CHAPTERS_C                 # noqa: E402
from extras import EXAM, TIPS, PLAN, QUICKTABLE, SOURCES  # noqa: E402

CHAPTERS = balance_answers(CHAPTERS_A + CHAPTERS_B + CHAPTERS_C)
FONT_DIR = os.path.join(ROOT, "assets", "fonts")


# ------------------------------------------------------------------ fonts
def font_face(file, weight, rng):
    path = os.path.join(FONT_DIR, file)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (
        "@font-face{font-family:'Cairo';font-style:normal;font-display:swap;"
        f"font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2');"
        f"unicode-range:{rng};}}"
    )


AR_RANGE = "U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0898-08E1,U+08E3-08FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FEFF"
LA_RANGE = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"


def fonts_css():
    css = ""
    for f, w in (("cairo-arabic-400-normal.woff2", 400),
                 ("cairo-arabic-700-normal.woff2", 700),
                 ("cairo-arabic-800-normal.woff2", 800)):
        css += font_face(f, w, AR_RANGE)
    for f, w in (("cairo-latin-400-normal.woff2", 400),
                 ("cairo-latin-700-normal.woff2", 700)):
        css += font_face(f, w, LA_RANGE)
    return css


# ------------------------------------------------------------------- html
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_cells(cells, cls="stem"):
    if not cells:
        return ""
    out = f'<div class="{cls}">'
    for c in cells:
        out += f'<div class="cell">{c}</div>'
    out += "</div>"
    return out


def render_options(q, qid):
    opts = q["options"]
    okind = q["okind"]
    out = '<div class="options' + (" text" if okind == "text" else "") + '">'
    for i, o in enumerate(opts):
        correct = " correct" if i == q["answer"] else ""
        label = AR_LABELS[i]
        if okind == "text":
            out += (f'<div class="opt{correct}"><span class="olabel">{label}</span>'
                    f'<span class="otext">{o}</span></div>')
        else:
            out += (f'<div class="opt{correct}"><span class="olabel">{label}</span>'
                    f'<div class="ofig">{o}</div></div>')
    out += "</div>"
    return out


def render_question(ch, q, n):
    qid = f'{ch["id"]}-{n}'
    stem = render_cells(q.get("stem"))
    note = f'<div class="note">{q["stem_note"]}</div>' if q.get("stem_note") else ""
    steps = "".join(f"<li>{s}</li>" for s in q["steps"])
    tip = f'<div class="tip"><b>⚠️ انتبه:</b> {q["tip"]}</div>' if q.get("tip") else ""
    ans_label = AR_LABELS[q["answer"]]
    ans_extra = f' — {q["answer_text"]}' if q.get("answer_text") else ""
    return f"""
<article class="qcard" id="{qid}">
  <header class="qhead">
    <span class="qnum">سؤال {n}</span>
    <h4>{q["prompt"]}</h4>
  </header>
  <div class="qbody">
    <div class="qfig">
      {stem}{note}
      <div class="optitle">الاختيارات</div>
      {render_options(q, qid)}
    </div>
    <div class="qsol">
      <div class="soltitle">طريقة الحل خطوة بخطوة</div>
      <ol class="steps">{steps}</ol>
      <div class="answer">✅ الإجابة الصحيحة: <b>{ans_label}</b>{ans_extra}</div>
      {tip}
    </div>
  </div>
</article>"""


def render_chapter(ch):
    qs = "".join(render_question(ch, q, i + 1) for i, q in enumerate(ch["questions"]))
    how = "".join(f"<li>{s}</li>" for s in ch["how"])
    traps = "".join(f"<li>{s}</li>" for s in ch["traps"])
    src = "".join(f'<span class="srcchip">▶ {s}</span>' for s in ch["source"])
    return f"""
<section class="chapter" id="{ch['id']}" style="--c1:{ch['color']};--c2:{ch['color2']}">
  <div class="chead">
    <div class="cicon">{ch['icon']}</div>
    <div>
      <div class="cnum">المحور {ch['num']}</div>
      <h2>{ch['title']}</h2>
      <p>{ch['subtitle']}</p>
    </div>
    <div class="ccount">{len(ch['questions'])}<small>سؤال</small></div>
  </div>
  <div class="cintro">
    <div class="box idea"><h3>💡 فكرة السؤال</h3><p>{ch['idea']}</p></div>
    <div class="box how"><h3>🧭 خطوات الحل</h3><ol>{how}</ol></div>
    <div class="box trap"><h3>🚩 أخطاء شائعة</h3><ul>{traps}</ul></div>
  </div>
  <div class="srcline">مصدر الشرح على القناة: {src}</div>
  {qs}
  <div class="backtop"><a href="#toc">↑ العودة إلى الفهرس</a></div>
</section>"""


def render_toc():
    items = ""
    for ch in CHAPTERS:
        items += (f'<a class="tocitem" href="#{ch["id"]}" style="--c1:{ch["color"]};--c2:{ch["color2"]}">'
                  f'<span class="ti">{ch["icon"]}</span>'
                  f'<span class="tt"><b>{ch["num"]}. {ch["title"]}</b><small>{ch["subtitle"]}</small></span>'
                  f'<span class="tc">{len(ch["questions"])}</span></a>')
    return items


def render_exam():
    rows = ""
    for i, (qst, opts, ans, why) in enumerate(EXAM, 1):
        o = " &nbsp;•&nbsp; ".join(f"<b>{AR_LABELS[j]}</b> {t}" for j, t in enumerate(opts))
        rows += (f'<tr><td class="n">{i}</td><td>{qst}<div class="exopts">{o}</div></td>'
                 f'<td class="ans"><b>{AR_LABELS[ans]}</b><div class="why">{why}</div></td></tr>')
    return rows


def build():
    total_q = sum(len(c["questions"]) for c in CHAPTERS)
    css = CSS.replace("/*FONTS*/", fonts_css())
    html = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>الدليل الشامل لأسئلة الذكاء IQ — الأشكال والأعداد وطرق الحل</title>
<meta name="description" content="ملف ملوّن شامل لكل أنماط أسئلة الذكاء IQ: الأشكال والمصفوفات والمكعبات والمرايا وطي الورق والمتتاليات العددية والحروف والعلاقات اللفظية، مع صورة كل شكل وبجانبها طريقة الحل خطوة بخطوة.">
<style>{css}</style>
</head>
<body>

<div class="toolbar no-print">
  <div class="tb-in">
    <span class="brand">🧠 دليل IQ الشامل</span>
    <select id="jump" aria-label="انتقال سريع">
      <option value="">— انتقال سريع إلى محور —</option>
      {''.join(f'<option value="{c["id"]}">{c["num"]}. {c["title"]}</option>' for c in CHAPTERS)}
      <option value="exam">نموذج اختبار سريع</option>
    </select>
    <button id="toggleAns" class="btn">🙈 إخفاء الإجابات</button>
    <button id="printBtn" class="btn alt">🖨️ طباعة / حفظ PDF</button>
  </div>
</div>

<header class="cover">
  <div class="cover-in">
    <div class="kicker">ملف مراجعة شامل · مسابقات التوظيف والجهاز المركزي للتنظيم والإدارة</div>
    <h1>الدليل الشامل لأسئلة الذكاء <span>IQ</span></h1>
    <p class="sub">كل أنماط أسئلة الذكاء: الأشكال والصور والأعداد والحروف — مع صورة كل شكل وبجانبها طريقة الحل خطوة بخطوة</p>
    <div class="stats">
      <div class="stat"><b>{len(CHAPTERS)}</b><span>محورًا</span></div>
      <div class="stat"><b>{total_q}</b><span>سؤالًا محلولًا</span></div>
      <div class="stat"><b>{total_q}</b><span>شكلًا ورسمًا</span></div>
      <div class="stat"><b>١٠</b><span>أسئلة اختبار ذاتي</span></div>
    </div>
    <div class="credit">مُستخلَص من سلسلة شرح الـ IQ على قناة
      <a href="https://youtube.com/@emanelsayed.online" target="_blank" rel="noopener">هنتعلم أون لاين مع إيمان السيد</a>
      (قائمة «IQ – نسبة الذكاء» وما يتبعها من فيديوهات)</div>
  </div>
</header>

<section class="usage">
  <div class="ubox"><h3>📘 كيف تستعمل هذا الملف؟</h3>
    <ol>
      <li>اقرأ «فكرة السؤال» و«خطوات الحل» في أول كل محور قبل حل أسئلته.</li>
      <li>غطِّ عمود الشرح وحاول الحل بنفسك، أو اضغط زر <b>إخفاء الإجابات</b> في الأعلى.</li>
      <li>بعد كل سؤال اقرأ «انتبه» فهي تلخّص الفخ الذي يسقط فيه أغلب المتقدمين.</li>
      <li>في آخر الملف: جدول سريع لكل الأنماط + نصائح الامتحان + خطة ٧ أيام + اختبار ذاتي.</li>
      <li>للطباعة أو حفظ نسخة PDF اضغط زر <b>طباعة / حفظ PDF</b> (الملف مُهيّأ للطباعة الملوّنة).</li>
    </ol>
  </div>
</section>

<section id="toc" class="toc">
  <h2>📑 فهرس المحاور</h2>
  <div class="tocgrid">{render_toc()}</div>
</section>

{''.join(render_chapter(ch) for ch in CHAPTERS)}

<section class="appendix" id="quick">
  <h2>⚡ جدول سريع: اعرف نوع السؤال وطريقته من أول نظرة</h2>
  <table class="qt">
    <thead><tr><th>لو رأيت هذا في الامتحان…</th><th>فهذا النمط</th><th>افعل هذا فورًا</th></tr></thead>
    <tbody>{''.join(f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>' for a, b, c in QUICKTABLE)}</tbody>
  </table>
</section>

<section class="appendix" id="tips">
  <h2>🎯 نصائح ذهبية داخل لجنة الامتحان</h2>
  <div class="tipgrid">{''.join(f'<div class="tcard"><b>{t}</b><p>{d}</p></div>' for t, d in TIPS)}</div>
</section>

<section class="appendix" id="plan">
  <h2>🗓️ خطة ٧ أيام لإتقان محور الذكاء</h2>
  <div class="plan">{''.join(f'<div class="day"><span>{d}</span><p>{t}</p></div>' for d, t in PLAN)}</div>
</section>

<section class="appendix" id="exam">
  <h2>📝 نموذج اختبار سريع (١٠ أسئلة) — اختبر نفسك</h2>
  <p class="examnote">غطِّ العمود الأخير، أجب في ٨ دقائق، ثم صحّح لنفسك. من ٨ فأكثر: مستواك ممتاز.</p>
  <table class="extable">
    <thead><tr><th>#</th><th>السؤال</th><th>الإجابة والسبب</th></tr></thead>
    <tbody>{render_exam()}</tbody>
  </table>
</section>

<section class="appendix" id="sources">
  <h2>🔗 مصادر الملف من القناة</h2>
  <p class="examnote">الملف مبني على محتوى سلسلة IQ في قناة «هنتعلم أون لاين مع إيمان السيد»، وأُعيد رسم كل الأشكال رسمًا جديدًا داخل هذا الملف للتوضيح.</p>
  <div class="srcgrid">
    {''.join(f'<a class="srccard" href="{u}" target="_blank" rel="noopener"><b>{t}</b><span>{u}</span></a>' for t, u in SOURCES)}
  </div>
</section>

<footer class="foot">
  <p>أُعدّ هذا الملف لأغراض المراجعة والتدريب الذاتي · كل الأشكال رُسمت داخل الملف بصيغة SVG فتظهر بوضوح عند الطباعة وعلى كل الشاشات.</p>
  <p class="small">بالتوفيق إن شاء الله 🤍</p>
</footer>

<script>
(function(){{
  var body = document.body;
  body.classList.add('answers-on');
  var btn = document.getElementById('toggleAns');
  btn.addEventListener('click', function(){{
    var on = body.classList.toggle('answers-on');
    btn.textContent = on ? '🙈 إخفاء الإجابات' : '👁️ إظهار الإجابات';
  }});
  document.getElementById('printBtn').addEventListener('click', function(){{ window.print(); }});
  document.getElementById('jump').addEventListener('change', function(e){{
    var id = e.target.value;
    if(id){{ document.getElementById(id).scrollIntoView({{behavior:'smooth'}}); }}
  }});
}})();
</script>
</body>
</html>"""
    out = os.path.join(ROOT, "iq-guide.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(out) / 1024
    print(f"✅ تم إنشاء {out}  ({size:.0f} KB) — {len(CHAPTERS)} محورًا و{total_q} سؤالًا")


CSS = """
/*FONTS*/
*{box-sizing:border-box}
:root{
  --ink:#0f172a; --muted:#475569; --line:#e2e8f0; --bg:#f6f8fc;
  --c1:#2563eb; --c2:#60a5fa;
}
html{scroll-behavior:smooth; scroll-padding-top:80px}
body{margin:0;font-family:'Cairo',system-ui,'Segoe UI',Tahoma,sans-serif;background:var(--bg);
  color:var(--ink);line-height:1.85;font-size:16px}
h1,h2,h3,h4{margin:0 0 .4em;line-height:1.5}
a{color:#1d4ed8}
ol,ul{margin:.3em 0;padding-inline-start:1.2em}
li{margin:.25em 0}

/* ---------- toolbar ---------- */
.toolbar{position:sticky;top:0;z-index:50;background:rgba(15,23,42,.96);backdrop-filter:blur(6px);
  box-shadow:0 2px 14px rgba(15,23,42,.25)}
.tb-in{max-width:1180px;margin:auto;display:flex;gap:10px;align-items:center;padding:9px 16px;flex-wrap:wrap}
.brand{color:#fff;font-weight:800;letter-spacing:.3px}
.tb-in select{margin-inline-start:auto;border-radius:10px;border:0;padding:8px 10px;font-family:inherit;
  font-size:14px;background:#1e293b;color:#e2e8f0;max-width:min(52vw,340px)}
.btn{border:0;border-radius:10px;padding:8px 14px;font-family:inherit;font-weight:700;font-size:14px;
  cursor:pointer;background:#38bdf8;color:#07263a}
.btn.alt{background:#fbbf24;color:#3b2a06}
.btn:hover{filter:brightness(1.08)}

/* ---------- cover ---------- */
.cover{background:
  radial-gradient(1200px 400px at 90% -10%,rgba(56,189,248,.45),transparent 60%),
  radial-gradient(900px 400px at 0% 0%,rgba(244,114,182,.35),transparent 60%),
  linear-gradient(135deg,#0f172a,#1e3a8a 55%,#4c1d95);
  color:#fff;padding:54px 18px 46px;text-align:center}
.cover-in{max-width:1000px;margin:auto}
.kicker{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);
  padding:5px 14px;border-radius:999px;font-size:13px;margin-bottom:14px}
.cover h1{font-size:clamp(28px,5vw,46px);font-weight:800;text-shadow:0 4px 18px rgba(0,0,0,.35)}
.cover h1 span{background:linear-gradient(90deg,#fde047,#fb923c);-webkit-background-clip:text;
  background-clip:text;color:transparent}
.cover .sub{max-width:760px;margin:6px auto 18px;opacity:.93;font-size:clamp(14px,2.2vw,18px)}
.stats{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:18px 0 10px}
.stat{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:14px;
  padding:10px 18px;min-width:108px}
.stat b{display:block;font-size:26px;line-height:1.2;color:#fde047}
.stat span{font-size:13px;opacity:.9}
.credit{font-size:13.5px;opacity:.9;margin-top:10px}
.credit a{color:#fde047;font-weight:700}

/* ---------- usage + toc ---------- */
.usage,.toc,.appendix{max-width:1180px;margin:26px auto;padding:0 16px}
.ubox{background:#fff;border:2px dashed #93c5fd;border-radius:16px;padding:16px 20px}
.ubox h3{color:#1d4ed8}
.toc h2,.appendix h2{font-size:clamp(20px,3vw,27px);margin-bottom:14px;
  background:linear-gradient(90deg,#1e293b,#2563eb);-webkit-background-clip:text;background-clip:text;color:transparent}
.tocgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
.tocitem{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--line);
  border-radius:14px;padding:11px 14px;text-decoration:none;color:var(--ink);
  border-inline-start:6px solid var(--c1);transition:.18s}
.tocitem:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(2,6,23,.1)}
.tocitem .ti{font-size:24px}
.tocitem .tt{display:flex;flex-direction:column;flex:1}
.tocitem .tt small{color:var(--muted);font-size:12.5px;line-height:1.5}
.tocitem .tc{background:var(--c1);color:#fff;border-radius:999px;min-width:30px;text-align:center;
  font-weight:800;font-size:13px;padding:2px 8px}

/* ---------- chapter ---------- */
.chapter{max-width:1180px;margin:34px auto;padding:0 16px}
.chead{display:flex;gap:16px;align-items:center;background:linear-gradient(120deg,var(--c1),var(--c2));
  color:#fff;border-radius:18px 18px 0 0;padding:16px 20px;box-shadow:0 10px 24px rgba(2,6,23,.12)}
.chead .cicon{font-size:34px;background:rgba(255,255,255,.2);border-radius:14px;padding:6px 12px}
.chead h2{font-size:clamp(18px,2.7vw,26px);margin:0}
.chead p{margin:2px 0 0;opacity:.92;font-size:14px}
.cnum{font-size:12.5px;opacity:.9;letter-spacing:.5px}
.ccount{margin-inline-start:auto;text-align:center;background:rgba(255,255,255,.18);border-radius:14px;
  padding:8px 14px;font-size:22px;font-weight:800}
.ccount small{display:block;font-size:11.5px;font-weight:400;opacity:.9}
.cintro{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px;background:#fff;
  padding:16px;border:1px solid var(--line);border-top:0}
.box{border-radius:14px;padding:12px 14px;font-size:14.6px}
.box h3{font-size:15.5px;margin-bottom:6px}
.box.idea{background:#eff6ff;border:1px solid #bfdbfe}
.box.how{background:#f0fdf4;border:1px solid #bbf7d0}
.box.trap{background:#fef2f2;border:1px solid #fecaca}
.srcline{background:#fff;border:1px solid var(--line);border-top:0;padding:8px 16px;font-size:13px;color:var(--muted)}
.srcchip{display:inline-block;background:#f1f5f9;border:1px solid var(--line);border-radius:999px;
  padding:3px 10px;margin:3px 4px;font-size:12.5px}

/* ---------- question card ---------- */
.qcard{background:#fff;border:1px solid var(--line);border-top:0;overflow:hidden}
.chapter .qcard:last-of-type{border-radius:0 0 18px 18px}
.qhead{display:flex;gap:12px;align-items:flex-start;padding:14px 16px 6px;background:
  linear-gradient(90deg,color-mix(in srgb,var(--c1) 10%,#fff),#fff)}
.qnum{background:var(--c1);color:#fff;border-radius:999px;padding:3px 12px;font-size:13px;font-weight:800;white-space:nowrap}
.qhead h4{font-size:16.5px;margin:0;font-weight:700}
.qbody{display:grid;grid-template-columns:minmax(300px,1.05fr) minmax(280px,1fr);gap:14px;padding:6px 16px 18px}
.qfig{background:#fbfdff;border:1px solid #e6eefc;border-radius:14px;padding:12px}
.stem{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center}
.cell{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:5px;min-width:76px;flex:0 0 auto}
.cell svg{width:84px;height:84px;display:block}
.cell svg.big{width:132px;height:132px}
.cell:has(.series){width:100%;border:0;background:transparent;padding:0}
.note{text-align:center;color:var(--muted);font-size:12.6px;margin-top:6px}
.optitle{margin:12px 0 6px;font-size:13px;color:var(--muted);text-align:center;
  border-top:1px dashed #cbd5e1;padding-top:8px}
.options{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.opt{position:relative;background:#fff;border:2px solid #e2e8f0;border-radius:12px;padding:6px 6px 4px;
  min-width:86px;text-align:center}
.opt svg{width:72px;height:72px;display:block;margin:auto}
.opt svg.big{width:112px;height:112px}
.olabel{position:absolute;inset-inline-start:6px;top:4px;background:#f1f5f9;border-radius:999px;
  width:22px;height:22px;line-height:22px;font-size:12.5px;font-weight:800;color:#475569}
.options.text .opt{min-width:112px;padding:10px 12px}
.otext{font-weight:700;font-size:15.5px}
body.answers-on .opt.correct{border-color:#16a34a;background:#f0fdf4;box-shadow:0 0 0 3px rgba(22,163,74,.15)}
body.answers-on .opt.correct .olabel{background:#16a34a;color:#fff}
body.answers-on .opt.correct::after{content:"✔";position:absolute;inset-inline-end:6px;top:3px;color:#16a34a;font-weight:800}

.qsol{background:#fffdf7;border:1px solid #fde68a;border-radius:14px;padding:12px 14px}
.soltitle{font-weight:800;color:#b45309;margin-bottom:6px;font-size:15px}
.steps{margin:0;padding-inline-start:1.3em;font-size:15px}
.steps li{margin:.3em 0}
.answer{margin-top:10px;background:#dcfce7;border:1px solid #86efac;color:#14532d;border-radius:10px;
  padding:8px 12px;font-weight:700;font-size:15px}
body:not(.answers-on) .answer{filter:blur(6px);user-select:none}
body:not(.answers-on) .steps{filter:blur(5px);user-select:none}
.tip{margin-top:9px;background:#fff1f2;border:1px solid #fecdd3;border-radius:10px;padding:8px 12px;
  font-size:14px;color:#9f1239}
.backtop{text-align:center;padding:10px;font-size:13px}

/* ---------- series chips ---------- */
.series{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;padding:6px 0}
.chip{min-width:52px;padding:8px 12px;border-radius:12px;background:#fff;
  border:2px solid var(--chip,#2563eb);color:var(--chip,#2563eb);font-weight:800;font-size:19px;text-align:center}
.chip.q{background:#fff7ed;border-color:#ef4444;color:#ef4444;border-style:dashed}

/* ---------- appendix ---------- */
.qt,.extable{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;
  box-shadow:0 6px 18px rgba(2,6,23,.06);font-size:14.6px}
.qt th,.extable th{background:linear-gradient(120deg,#1e293b,#334155);color:#fff;padding:10px;text-align:start}
.qt td,.extable td{padding:10px;border-top:1px solid var(--line);vertical-align:top}
.qt tr:nth-child(even) td,.extable tr:nth-child(even) td{background:#f8fafc}
.extable .n{font-weight:800;color:#2563eb;width:36px}
.extable .ans{width:34%;background:#f0fdf4 !important}
.extable .ans b{display:inline-block;background:#16a34a;color:#fff;border-radius:8px;padding:1px 10px}
.exopts{color:#475569;font-size:13.6px;margin-top:4px}
.why{font-size:13.4px;color:#166534;margin-top:4px}
body:not(.answers-on) .extable .ans{filter:blur(6px)}
.tipgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.tcard{background:#fff;border:1px solid var(--line);border-inline-start:6px solid #2563eb;border-radius:14px;padding:12px 14px}
.tcard b{color:#1d4ed8}
.tcard p{margin:4px 0 0;font-size:14.4px;color:#334155}
.plan{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.day{background:linear-gradient(135deg,#fff,#f1f5f9);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.day span{display:inline-block;background:#7c3aed;color:#fff;border-radius:999px;padding:2px 12px;font-size:13px;font-weight:800}
.day p{margin:7px 0 0;font-size:14.4px}
.examnote{color:var(--muted);font-size:14px;margin:0 0 10px}
.srcgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}
.srccard{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 12px;
  text-decoration:none;color:var(--ink)}
.srccard:hover{border-color:#93c5fd;background:#f8fbff}
.srccard span{display:block;font-size:11.5px;color:#64748b;direction:ltr;text-align:start;word-break:break-all}
.foot{background:#0f172a;color:#cbd5e1;text-align:center;padding:26px 16px;margin-top:34px}
.foot .small{opacity:.7;font-size:13px}

@media (max-width:820px){
  .qbody{grid-template-columns:1fr}
  .cell svg{width:72px;height:72px}
  .cell svg.big{width:112px;height:112px}
  .opt svg.big{width:96px;height:96px}
}

/* ---------- print ---------- */
@media print{
  @page{size:A4;margin:11mm}
  body{background:#fff;font-size:11.6pt}
  .no-print{display:none !important}
  body:not(.answers-on) .answer,body:not(.answers-on) .steps,
  body:not(.answers-on) .extable .ans{filter:none !important}
  .opt.correct{border-color:#16a34a !important;background:#f0fdf4 !important}
  .cover{padding:28px 10px}
  .chapter,.appendix,.toc,.usage{margin:10px auto;page-break-inside:auto}
  .qcard{page-break-inside:avoid;break-inside:avoid}
  .chead{page-break-after:avoid}
  .cintro{page-break-inside:avoid}
  a{text-decoration:none;color:inherit}
  .cell svg{width:66px;height:66px}
  .opt svg{width:58px;height:58px}
  .cell svg.big{width:96px;height:96px}
  .opt svg.big{width:84px;height:84px}
}
"""

if __name__ == "__main__":
    build()
