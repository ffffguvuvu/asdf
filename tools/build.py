# -*- coding: utf-8 -*-
"""يولّد ملف HTML ملون شامل لأسئلة IQ مع الرسوم والشروح."""
import os
import sys
import html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_a
import content_b
import content_c
import content_d
import content_e

CHAPTERS = content_a.CH + content_b.CH + content_c.CH + content_d.CH + content_e.CH

SOURCES = [
    ('بسهولة شرح أسئلة IQ (نسبة الذكاء) - الجزء الأول', 'V_zkkehBvbQ', 'مصفوفات وأشكال'),
    ('بسهولة شرح أسئلة IQ - الشكل المكمل - الجزء الثاني', 'wtUI5X2ppjs', 'الشكل المكمل'),
    ('بسهولة شرح أسئلة IQ - الجزء الثاني', 'bjytZM1dJOw', 'أشكال متنوعة'),
    ('بسهولة شرح أسئلة IQ (المكعبات) - الجزء الرابع', '4Qk4AJJp7Yo', 'المكعبات'),
    ('بسهولة شرح أسئلة IQ (المصفوفات) - الجزء الخامس', 'hfRxRoU8OFY', 'المصفوفات'),
    ('بسهولة شرح أسئلة IQ (المرايا وثني الورق) - الجزء السادس', 'MDt1D3NzB24', 'المرايا وثني الورق'),
    ('بسهولة شرح أسئلة IQ (تعبيرات الوجه) - الجزء السابع', 'Ouyv9RTYXHQ', 'تعبيرات الوجه'),
    ('شرح أسئلة IQ (الأسئلة المقالية) - الجزء الثامن', '5t8OAwQMEFk', 'الأسئلة المقالية'),
    ('حل IQ اختبار تدوير الأشكال - اختبار بيردو للتصور المكاني', 'D9kUXTcia4A', 'التصور المكاني'),
    ('أحدث أسئلة IQ - المتسلسلة - المتتاليات - المتواليات', '-x_B02vr9QY', 'المتتاليات'),
    ('شرح أحدث أسئلة IQ - حل أشكال X, Y, Z بسهولة', '2Ihx_bTZzTU', 'تركيب الأشكال'),
    ('شرح متتاليات بالكسور العشرية', '3uY8YdcW0ic', 'الكسور العشرية'),
    ('متتاليات الحروف - أحدث أسئلة IQ', 'cAIyFyMa7VY', 'متتاليات الحروف'),
    ('IQ - شرح أسئلة تركيب الأشكال بمعلومية X , Y , Z', '5jx2zlqbyC8', 'تركيب الأشكال'),
    ('شرح أحدث أشكال IQ - وردت بالفعل في الاختبارات', 'YoEJZqi61CM', 'أشكال حديثة'),
    ('حل أشكال IQ الحديثة التي وردت بالفعل خلال الفترة السابقة', '2oSouwEyWZE', 'أشكال حديثة'),
    ('شرح أحدث أسئلة IQ بسهولة - تخصص لغة عربية 2024', 'H7oXyOwewpM', 'مراجعة مطولة'),
    ('أحدث أسئلة IQ (طي الورق) وردت بالفعل في الاختبارات', 'i6nL9sjz-Dw', 'طي الورق'),
    ('شرح أحدث أسئلة IQ - المتتابعات والمتسلسلة', 'RIMlB-lU3Zs', 'المتتابعات'),
    ('أحدث أشكال نسبة الذكاء IQ وردت بالفعل - 2025', 'fE9INmOeuGs', 'أشكال 2025'),
    ('شرح أحدث أسئلة IQ - ورقة سمكة يد (ألغاز الأشكال)', 'pZWlqSyV5qA', 'ألغاز الأشكال'),
    ('شرح أسئلة ونماذج الميزان من محور IQ', 'x7G9D552NRc', 'الميزان'),
    ('أحدث أسئلة IQ - العلاقة بين الأشياء (الشوكة والملعقة...)', 'lpjD8DxhEKk', 'العلاقة بين الأشياء'),
    ('شرح أسئلة IQ - الأمثال الشعبية ولماذا نستخدم؟', 'YtyenRbHXkA', 'الأمثال الشعبية'),
    ('أسهل طريقة لحل طي المكعبات - المكعبات المفرودة', 'VhTX7E_XJNA', 'طي المكعبات'),
    ('أسهل طريقة لحل IQ - استخرج الشكل الخاطئ للمكعبات', 'tR_-va2vlmA', 'استراتيجية عقارب الساعة'),
    ('بأسهل طرق الحل - دليلك الشامل لحل طي المكعبات', 'nq1hV7tput0', 'طي المكعبات'),
    ('شرح أحدث أسئلة المتتاليات (المتتابعات) من محور IQ', 'PUF2tQlIJFk', 'المتتاليات'),
    ('مراجعة ما قبل الامتحان - العلاقة بين الأشياء - الأمثال', 'NFJ627OHhfQ', 'التفكير المجرد'),
    ('أحدث أسئلة IQ العلاقات اللفظية - وردت بالفعل', 'dz-sE6m2qfg', 'العلاقات اللفظية'),
    ('بسهولة حل أسئلة IQ - المكعبات والعلاقة بين الأشياء', 'CR5hlBRX6Go', 'مراجعة'),
    ('أحدث أسئلة في IQ - طريقة حل أسئلة نسبة الذكاء 2026', 'XbokmztXcuw', 'مراجعة 2026'),
    ('أحدث أسئلة في IQ - مراجعة ما قبل الامتحان', 'SoeGN11cUAQ', 'مراجعة'),
    ('حل أحدث مسألة من أشكال IQ بطريقة سهلة وبسيطة', 'oIpba1Dz4OY', 'مصفوفة أشكال'),
    ('أحدث أسئلة في IQ - لجميع الوظائف 2025', 'kK_LDGJVMwU', 'مراجعة 2025'),
    ('أحدث أشكال IQ وردت بالفعل - مسابقة الأزهر الشريف', 'zapEEiuKolw', 'الأزهر'),
    ('شرح ومراجعة IQ - الأشكال المماثلة - العلاقات - تدوير المكعب', 'h_d5Q6PTVPk', 'مراجعة'),
    ('التناظر اللفظي في IQ - العلاقة بين الكلمات', 'rdee9dRkE7g', 'التناظر اللفظي'),
    ('أحدث أسئلة وردت بالفعل في IQ - المماثل + المرايا + المتتاليات', '3zT0e7wN5Jw', 'مراجعة'),
    ('حل أحدث أسئلة IQ والتفكير المنطقي - 2026', 'Nm4w4T-SQ4U', 'تفكير منطقي'),
    ('أحدث أشكال IQ - مسابقة الطب البيطري', 'BVUNf8AFYHU', 'الطب البيطري'),
    ('أحدث أشكال IQ - تركيب الأشكال XYZ - المتماثلة 2026', '68GlrljDVXk', 'مراجعة 2026'),
    ('شرح أحدث أشكال IQ - تخصص الدراسات بمسابقة الحصة', 'rXsi_P42sBA', 'تخصص الدراسات'),
    ('شكل IQ من (منسا) حيّر الجميع - أحدث أشكال IQ', '0bz1oMT6zq0', 'شكل منسا'),
    ('حل أكثر من 10 أشكال IQ من أصعب الأشكال', 'OmU6XDh_peI', 'أشكال صعبة'),
    ('أحدث أنماط IQ - تخصص اللغة الإنجليزية 2026', 'qm-HIrolrQI', 'أنماط 2026'),
    ('أحدث 10 أشكال IQ - الأزهر والأحساء 2026', 'Cz-tTLKItEc', 'مراجعة 2026'),
    ('أهم 20 شكل IQ وردت بالفعل في اختبارات التوظيف', 'LYWSbDP100o', '20 شكلًا'),
    ('مسابقة الخبراء - أهم أنماط IQ وردت بالفعل', 'yOJd0tAVxIk', 'مسابقة الخبراء'),
    ('بأسهل طرق الحل - المتطابقة والمماثلة وتدوير الأشكال', 'pmDaEsMNvkI', 'المتطابقة والمماثلة'),
]

PLAN = [
    ("اليوم 1", "المتتاليات والمتواليات + المصفوفات الرقمية", "احفظ أنماط الفروق والمربعات والمكعبات، وحُل 30 مسألة متتالية."),
    ("اليوم 2", "متتاليات الحروف + الشكل المكمل", "اكتب ترتيب الحروف على ورقة، وتدرّب على حل السلسلتين بخطوتين."),
    ("اليوم 3", "المكعبات", "تدريب مكثّف على: الاستبعاد - المثلثات - عقارب الساعة (بمكعب ورقي حقيقي)."),
    ("اليوم 4", "التصور المكاني + التدوير (بيردو)", "استخدم علبة ثقاب أو مكعبًا حقيقيًا ودوّره بيدك."),
    ("اليوم 5", "الأشكال المتطابقة + تركيب X/Y/Z", "ركز على الفرق بين التدوير والانعكاس."),
    ("اليوم 6", "المرايا وثني الورق + تعبيرات الوجه", "جرب ثني الورق بيدك، واحفظ علامات المشاعر السبعة."),
    ("اليوم 7", "مراجعة شاملة + اختبار زمني", "حُل نموذج كامل بـ 30 سؤالًا في 25 دقيقة."),
]

EXAM_TIPS = [
    "اقرأ <b>رأس السؤال</b> أولًا: هل المطلوب الصحيح أم «الخاطئ» أم «المختلف»؟ نصف الأخطاء سببه عدم قراءة المطلوب.",
    "لا تتوقف أكثر من 45 ثانية على السؤال الواحد — علّمه وارجع إليه في النهاية.",
    "استخدم <b>الاستبعاد</b> قبل التخيّل: حذف اختيارين يرفع احتمال إصابتك من 25% إلى 50%.",
    "في أسئلة الأشكال: سمِّ الأشكال بصوت منخفض (مثلث، دائرة، مربع) فهذا ينشّط الانتباه.",
    "اكتب الفروق بين الأرقام فوق السلسلة مباشرة على ورقة الأسئلة.",
    "راجع إجاباتك في آخر 5 دقائق: تأكد أنك لم تختر «الصحيح» في سؤال يطلب «الخاطئ».",
    "التدريب أهم من الحفظ: نفس الأسئلة تتكرر بأشكال قريبة جدًا.",
]


def esc(s):
    return s


def qcard(q, color, idx):
    steps = "".join(f"<li>{esc(s)}</li>" for s in q["steps"])
    tip = (f'<div class="tip"><span class="tip-i">💡</span><div>{esc(q["tip"])}</div></div>'
           if q.get("tip") else "")
    return f"""
    <article class="qcard" id="{q['id']}">
      <div class="qhead" style="--c:{color}">
        <span class="qnum">{idx}</span>
        <h3>{esc(q['title'])}</h3>
      </div>
      <div class="qbody">
        <figure class="qfig">{q['fig']}</figure>
        <div class="qsol">
          <p class="ask"><span class="ask-l">المطلوب</span>{esc(q['ask'])}</p>
          <div class="steps-t">خطوات الحل</div>
          <ol class="steps">{steps}</ol>
          <div class="ans"><span class="ans-k">الإجابة</span><span class="ans-v">{esc(q['answer'])}</span></div>
          {tip}
        </div>
      </div>
    </article>"""


def chapter_html(ch):
    rules = "".join(f"<li>{esc(r)}</li>" for r in ch["rules"])
    cards = "".join(qcard(q, ch["color"], i + 1) for i, q in enumerate(ch["qs"]))
    return f"""
  <section class="chapter" id="ch-{ch['key']}" style="--c:{ch['color']}">
    <div class="ch-head">
      <div class="ch-icon">{ch['icon']}</div>
      <div>
        <h2>{esc(ch['title'])}</h2>
        <div class="ch-meta">{len(ch['qs'])} سؤالًا مشروحًا بالرسم</div>
      </div>
    </div>
    <p class="ch-intro">{ch['intro']}</p>
    <div class="rules">
      <div class="rules-t">⚙️ قواعد الحل السريع</div>
      <ol>{rules}</ol>
    </div>
    <div class="cards">{cards}</div>
    <a class="totop" href="#top">↑ العودة للفهرس</a>
  </section>"""


CSS = """
:root{
  --ink:#1f2a44; --muted:#5b6b8a; --bg:#f4f7fd; --card:#ffffff; --line:#e3e9f5;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Cairo","Tajawal","Segoe UI",Tahoma,Arial,sans-serif;
  line-height:1.85; -webkit-font-smoothing:antialiased;
}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px 70px}
/* cover */
.cover{
  background:linear-gradient(135deg,#2a6fdb 0%,#7b4bd8 45%,#ef5da8 100%);
  color:#fff;padding:52px 20px 44px;text-align:center;position:relative;overflow:hidden;
}
.cover:after{content:"";position:absolute;inset:0;background:
 radial-gradient(circle at 12% 18%,rgba(255,255,255,.22),transparent 42%),
 radial-gradient(circle at 88% 12%,rgba(255,255,255,.18),transparent 40%);}
.cover .inner{position:relative;z-index:1;max-width:1000px;margin:0 auto}
.cover h1{font-size:40px;margin:0 0 10px;line-height:1.4;font-weight:900}
.cover p.sub{font-size:19px;margin:0 auto 22px;max-width:760px;opacity:.95}
.badges{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:18px}
.badge{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.4);
  padding:7px 14px;border-radius:999px;font-size:14px;font-weight:700}
.stats{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin-top:8px}
.stat{background:rgba(255,255,255,.16);border-radius:16px;padding:14px 22px;min-width:130px}
.stat b{display:block;font-size:28px;line-height:1.3}
.stat span{font-size:13px;opacity:.9}
/* note */
.note{background:#fff8e6;border:1px solid #ffe1a6;border-right:6px solid #f4a261;
  border-radius:14px;padding:16px 18px;margin:26px 0;font-size:15px}
.note b{color:#b26a12}
/* toc */
.toc{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px 22px;margin:26px 0}
.toc h2{margin:0 0 14px;font-size:22px}
.toc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.toc a{display:flex;gap:10px;align-items:center;text-decoration:none;padding:12px 14px;
  border-radius:12px;background:#f8fafd;border:1px solid var(--line);transition:.15s}
.toc a:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(31,42,68,.08)}
.toc .ic{font-size:22px}
.toc .tx{font-weight:800;font-size:15px}
.toc .ct{font-size:12px;color:var(--muted);font-weight:600}
/* chapter */
.chapter{margin:48px 0 0;scroll-margin-top:16px}
.ch-head{display:flex;gap:14px;align-items:center;background:var(--card);
  border:1px solid var(--line);border-right:7px solid var(--c);border-radius:16px;padding:16px 18px;
  box-shadow:0 6px 20px rgba(31,42,68,.05)}
.ch-icon{font-size:32px;background:color-mix(in srgb,var(--c) 14%,#fff);width:60px;height:60px;
  display:grid;place-items:center;border-radius:14px;flex:0 0 auto}
.ch-head h2{margin:0;font-size:25px;color:var(--c)}
.ch-meta{font-size:13px;color:var(--muted);font-weight:700}
.ch-intro{background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:16px 18px;margin:14px 0;font-size:16px}
.rules{background:linear-gradient(180deg,#f7f9ff,#eef3ff);border:1px dashed var(--c);
  border-radius:14px;padding:14px 18px;margin:0 0 18px}
.rules-t{font-weight:900;color:var(--c);margin-bottom:6px}
.rules ol{margin:0;padding-inline-start:22px}
.rules li{margin:4px 0;font-size:15px}
/* question card */
.cards{display:grid;gap:18px}
.qcard{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;
  box-shadow:0 4px 16px rgba(31,42,68,.05)}
.qhead{display:flex;gap:12px;align-items:center;padding:14px 18px;background:var(--c);color:#fff}
.qnum{background:rgba(255,255,255,.22);width:34px;height:34px;border-radius:50%;display:grid;
  place-items:center;font-weight:900;flex:0 0 auto}
.qhead h3{margin:0;font-size:18px;font-weight:900}
.qbody{display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:18px;padding:18px}
.qfig{margin:0;background:#fbfcff;border:1px solid var(--line);border-radius:14px;padding:14px;
  display:grid;place-items:center;overflow:auto}
.qfig svg{max-width:100%;height:auto}
.qsol{min-width:0}
.ask{margin:0 0 10px;font-size:16px;font-weight:700}
.ask-l{display:inline-block;background:#eef3ff;color:#2a6fdb;font-size:12px;font-weight:900;
  padding:3px 10px;border-radius:999px;margin-inline-end:8px}
.steps-t{font-weight:900;color:#2a9d8f;margin-bottom:4px}
.steps{margin:0 0 12px;padding-inline-start:22px}
.steps li{margin:5px 0;font-size:15px}
.ans{background:#eafaf3;border:1px solid #bfe9d8;border-radius:12px;padding:10px 14px;
  display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.ans-k{background:#2a9d8f;color:#fff;font-size:12px;font-weight:900;padding:4px 12px;border-radius:999px}
.ans-v{font-weight:900;color:#12705f;font-size:17px}
.tip{display:flex;gap:10px;background:#fff6fb;border:1px solid #ffd9ec;border-radius:12px;
  padding:10px 14px;margin-top:12px;font-size:14.5px}
.tip-i{font-size:18px}
.totop{display:inline-block;margin:16px 0 0;font-size:13px;color:var(--muted);text-decoration:none}
/* sources */
.src{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:26px 0}
.src h2{margin:0 0 12px;font-size:22px}
.src ol{margin:0;padding-inline-start:22px;columns:2;column-gap:30px}
.src li{margin:5px 0;font-size:14.5px;break-inside:avoid}
.src a{color:#2a6fdb;text-decoration:none;font-weight:700}
.src a:hover{text-decoration:underline}
.src .tg{font-size:12px;color:var(--muted);font-weight:700}
/* plan */
.plan{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.day{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;
  border-top:5px solid #7b4bd8}
.day b{display:block;color:#7b4bd8;margin-bottom:4px}
.day .t{font-weight:900;margin-bottom:4px}
.day .d{font-size:14px;color:var(--muted)}
.tips{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-top:22px}
.tips ol{padding-inline-start:22px;margin:0}
.tips li{margin:7px 0}
footer{text-align:center;color:var(--muted);font-size:13px;padding:30px 0 10px}
@media (max-width:820px){
  .qbody{grid-template-columns:1fr}
  .src ol{columns:1}
  .cover h1{font-size:29px}
}
@media print{
  body{background:#fff}
  .cover{background:#2a6fdb !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .qcard,.ch-head,.rules,.tip,.ans{break-inside:avoid}
  .chapter{break-before:page}
  .totop{display:none}
}
"""


def main():
    total_q = sum(len(c["qs"]) for c in CHAPTERS)
    toc = "".join(
        f'<a href="#ch-{c["key"]}"><span class="ic">{c["icon"]}</span>'
        f'<span><span class="tx">{c["title"]}</span><br><span class="ct">{len(c["qs"])} سؤالًا</span></span></a>'
        for c in CHAPTERS)
    chapters = "".join(chapter_html(c) for c in CHAPTERS)
    srcs = "".join(
        f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">{esc(t)}</a>'
        f' <span class="tg">— {esc(tag)}</span></li>'
        for t, vid, tag in SOURCES)
    plan = "".join(
        f'<div class="day"><b>{esc(d)}</b><div class="t">{esc(t)}</div><div class="d">{esc(x)}</div></div>'
        for d, t, x in PLAN)
    tips = "".join(f"<li>{esc(t)}</li>" for t in EXAM_TIPS)

    doc = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>المرجع الشامل لأسئلة IQ - من قناة «هنتعلم أون لاين مع إيمان السيد»</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body id="top">
<div class="cover">
  <div class="inner">
    <h1>المرجع الشامل لأسئلة القدرات الذهنية IQ</h1>
    <p class="sub">جمع وتلخيص لكل أسئلة <b>IQ</b> (الصور والأشكال والأعداد والحروف) مع <b>طريقة الحل</b> خطوة بخطوة،
    مستخلص من فيديوهات قناة <b>«هنتعلم أون لاين مع إيمان السيد»</b>، ومع كل سؤال <b>رسم توضيحي</b> بجانبه الشرح.</p>
    <div class="badges">
      <span class="badge">🎯 لجميع المسابقات والوظائف</span>
      <span class="badge">🧩 التنظيم والإدارة</span>
      <span class="badge">👩‍🏫 معلم مساعد مادة</span>
      <span class="badge">📐 التربية والتعليم</span>
      <span class="badge">🏛️ الأوقاف والأزهر والبريد</span>
    </div>
    <div class="stats">
      <div class="stat"><b>{len(CHAPTERS)}</b><span>أبواب</span></div>
      <div class="stat"><b>{total_q}</b><span>سؤالًا مشروحًا</span></div>
      <div class="stat"><b>{len(SOURCES)}</b><span>فيديو مصدر</span></div>
      <div class="stat"><b>100+</b><span>رسم توضيحي</span></div>
    </div>
  </div>
</div>

<div class="wrap">

  <div class="note">
    <b>كيف تقرأ هذا الملف؟</b> كل سؤال موضوع في بطاقة مستقلة: على اليمين <b>صورة الشكل</b> (مرسومة بدقة
    بحسب وصف الشرح في الفيديو)، وبجانبها <b>المطلوب</b>، ثم <b>خطوات الحل</b> مرقّمة، ثم <b>الإجابة</b>،
    ثم <b>خدعة/تنبيه</b> إن وُجد. في أعلى كل باب تجد «قواعد الحل السريع» الخاصة بهذا النوع.
    <br><b>تنبيه مهم:</b> الرسوم في هذا الملف <b>إعادة رسم توضيحية</b> مبنية على الشرح الوارد في الفيديوهات
    (لا يمكن أخذ لقطات من الفيديو نفسه)، وهي مطابقة في الفكرة والخصائص — الغرض منها أن تتخيّل الشكل وتتمرّن عليه.
  </div>

  <nav class="toc">
    <h2>📚 فهرس الأبواب</h2>
    <div class="toc-grid">{toc}</div>
  </nav>

  {chapters}

  <section class="src" id="sources">
    <h2>🎬 مصادر المحتوى (فيديوهات القناة)</h2>
    <p style="margin:0 0 10px;color:#5b6b8a;font-size:14.5px">
      القناة: <a href="https://youtube.com/@emanelsayed.online" target="_blank" rel="noopener">هنتعلم أون لاين مع إيمان السيد</a>
      — قائمة تشغيل IQ:
      <a href="https://www.youtube.com/playlist?list=PLO9L9sHOfqhPGsDyK_JAvNnkP0Ua8o_6Q" target="_blank" rel="noopener">IQ - نسبة الذكاء</a>
    </p>
    <ol>{srcs}</ol>
  </section>

  <section class="src" id="plan">
    <h2>🗓️ خطة مذاكرة 7 أيام</h2>
    <div class="plan">{plan}</div>
    <div class="tips">
      <h3 style="margin:0 0 8px">نصائح يوم الامتحان</h3>
      <ol>{tips}</ol>
    </div>
  </section>

  <footer>
    أُعدّ هذا الملف لأغراض التدريب والمراجعة، والمحتوى <b>استرشادي</b> مبني على ما ورد في فيديوهات القناة،
    ولا يُعدّ ضمانًا لتكرار الأسئلة في الامتحان. بالتوفيق والنجاح 🌸
  </footer>
</div>
</body>
</html>
"""
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "IQ-guide.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote", out, len(doc), "chars,", total_q, "questions")


if __name__ == "__main__":
    main()
