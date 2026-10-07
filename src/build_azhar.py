# -*- coding: utf-8 -*-
"""يبني azhar-arabic-guide.html : بنك أسئلة مسابقة تعيين معلم لغة عربية بالأزهر (كل الأقسام)."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "azhar"))
sys.path.insert(0, os.path.join(HERE, "tarbawy"))

import qkit                     # noqa: E402
import arabic_kb                # noqa: E402,F401
import arabic_cur               # noqa: E402
import arabic_cur2              # noqa: E402
import arabic_cur3              # noqa: E402
import sections                 # noqa: E402
import english                  # noqa: E402
import iqbank                   # noqa: E402
import extras                   # noqa: E402

import gen as tgen              # noqa: E402  (مولّد التربوي)
import curated as tcur          # noqa: E402
from kb_core import G as TG     # noqa: E402  (مجموعات التربوي)

OUT = os.path.join(os.path.dirname(HERE), "azhar-arabic-guide.html")

SECS = [
    ("spec", "التخصص — لغة عربية", "#047857"),
    ("tarb", "التربوي", "#4f46e5"),
    ("behav", "الكفايات السلوكية", "#be123c"),
    ("comp", "الحاسب الآلي", "#0369a1"),
    ("gen", "المعلومات العامة", "#b45309"),
    ("eng", "اللغة الإنجليزية", "#7c3aed"),
    ("iq", "الذكاء IQ", "#0f766e"),
]
SEC_NAME = {s: n for s, n, _ in SECS}

# موضوعات التربوي الأكثر تكرارًا في المسابقات
TARB_HOT = {
    "تصنيف بلوم", "أنواع التقويم", "خصائص الاختبار الجيد", "أنواع الصدق", "نظريات التعلم",
    "طرق التدريس", "صياغة الأهداف", "عناصر المنهج", "مفهوم المنهج", "القياس والتقويم",
    "الدافعية والتعزيز", "الإدارة الصفية", "التعلم النشط", "أدوات التقويم", "جدول المواصفات",
    "مفهوم التعلم", "الذكاءات المتعددة", "النمو المعرفي", "أنواع الأسئلة", "التعلم التعاوني",
    "مستويات المجال المعرفي عند بلوم", "تصنيف بلوم المعدّل (أندرسون)", "مكوّنات الهدف السلوكي",
    "مراحل النمو المعرفي عند بياجيه", "هرم الحاجات عند ماسلو", "التعزيز والعقاب",
    "أنواع أسئلة الاختبارات", "مفاهيم القياس والتقويم", "استراتيجيات التعلم النشط",
}


def tarbawy_bank():
    out = []
    for q in tgen.kb_bank() + tgen.num_bank() + tcur.bank(tgen.mk):
        r = 0
        if q["s"] == tcur.SRC_EXAM:
            r = 2
        elif q["s"] == tcur.SRC_SJT:
            r = 1
        elif q["t"] in TARB_HOT:
            r = 1
        out.append({"q": q["q"], "o": q["o"], "a": q["a"], "e": q["e"],
                    "x": "tarb", "t": q["t"], "s": q["s"], "r": r})
    return out


def collect():
    qs = (qkit.kb_bank()
          + qkit.ordered_bank(["osool", "hamza"])
          + qkit.cur_bank()
          + arabic_cur.bank()
          + arabic_cur2.bank()
          + arabic_cur3.bank()
          + extras.bank()
          + sections.numeric_bank()
          + english.bank()
          + iqbank.bank()
          + tarbawy_bank())
    seen, out = set(), []
    for q in qs:
        key = (q["q"].strip(), tuple(sorted(q["o"])))
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
    # فكّ الاشتراك اللفظي: متنٌ واحد بإجابتين مختلفتين في موضوعين مختلفين
    import re as _re
    from collections import defaultdict as _dd

    def _n(t):
        t = _re.sub(r"[\u064B-\u0652\u0640]", "", t)
        for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه")):
            t = t.replace(a, b)
        return _re.sub(r"\s+", " ", t).strip()

    seen_t = _dd(set)
    for q in out:
        seen_t[_n(q["q"])].add((q["t"], _n(q["o"][q["a"]])))
    clash = {k for k, v in seen_t.items()
             if len({t for t, _ in v}) > 1 and len({a for _, a in v}) > 1}
    for q in out:
        if _n(q["q"]) in clash:
            q["q"] = f"(في {q['t']}) {q['q']}"

    order = {s: i for i, (s, _, _) in enumerate(SECS)}
    out.sort(key=lambda q: (order.get(q["x"], 9), -q["r"], q["t"]))
    return out


def validate(qs):
    errs = []
    for i, q in enumerate(qs):
        if len(q["o"]) != 4 or len(set(q["o"])) != 4:
            errs.append(f"{i}: بدائل غير سليمة — {q['q'][:45]}")
        if not 0 <= q["a"] < 4:
            errs.append(f"{i}: مفتاح خارج النطاق")
        if not q["e"].strip():
            errs.append(f"{i}: بلا شرح — {q['q'][:45]}")
        if q["x"] not in SEC_NAME:
            errs.append(f"{i}: قسم غير معروف {q['x']}")
    return errs


def pack(qs):
    topics, srcs, ti, si, rows = [], [], {}, {}, []
    for q in qs:
        if q["t"] not in ti:
            ti[q["t"]] = len(topics)
            topics.append(q["t"])
        if q["s"] not in si:
            si[q["s"]] = len(srcs)
            srcs.append(q["s"])
        rows.append([q["q"], q["o"], q["a"], q["e"], q["x"], ti[q["t"]], si[q["s"]], q["r"]])
    return rows, topics, srcs


def kb_payload():
    out = []
    for g in qkit.GA:
        out.append({"sec": g["sec"], "cat": g["cat"], "note": g.get("note") or "",
                    "hot": 1 if g["hot"] else 0,
                    "items": [[i["n"], i["d"], i.get("p", ""), i.get("ex", "")] for i in g["items"]]})
    for g in TG:
        out.append({"sec": "tarb", "cat": g["cat"], "note": g.get("note") or "", "hot": 0,
                    "items": [[i["n"], i["d"], i.get("p", ""), i.get("ex", "")] for i in g["items"]]})
    return out


def ar(n):
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


CSS = """
*{box-sizing:border-box}
:root{--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--ok:#16a34a;--no:#dc2626;--gold:#b45309}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI","Tahoma","Noto Naskh Arabic","Noto Sans Arabic","Arial",sans-serif;
  background:linear-gradient(180deg,#ecfdf5 0%,#f8fafc 340px,#f8fafc 100%);
  color:var(--ink);direction:rtl;line-height:1.85;font-size:17px}
header.hero{background:radial-gradient(1100px 380px at 85% -40%,#34d399 0%,transparent 60%),
  linear-gradient(135deg,#064e3b 0%,#065f46 40%,#1e3a8a 100%);
  color:#fff;padding:32px 18px 24px;text-align:center;box-shadow:0 10px 30px rgba(6,78,59,.25)}
header.hero h1{margin:0 0 6px;font-size:32px}
header.hero p{margin:0;opacity:.93}
.stats{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.stat{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.28);border-radius:14px;
  padding:9px 16px;min-width:112px}
.stat b{display:block;font-size:22px}.stat span{font-size:12.5px;opacity:.92}
nav.tabs{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;position:sticky;top:0;z-index:40;
  background:#fff;border-bottom:1px solid var(--line);padding:9px;box-shadow:0 2px 10px rgba(15,23,42,.06)}
nav.tabs button{border:1px solid var(--line);background:#f8fafc;border-radius:999px;padding:7px 16px;
  font-size:15.5px;font-family:inherit;cursor:pointer;font-weight:700;color:#334155}
nav.tabs button.on{background:linear-gradient(135deg,#047857,#1d4ed8);color:#fff;border-color:transparent}
main{max-width:1060px;margin:0 auto;padding:16px 12px 80px}
.panel{display:none}.panel.on{display:block}
.toolbar{background:#fff;border:1px solid var(--line);border-radius:16px;padding:13px;margin-bottom:14px;
  box-shadow:0 6px 18px rgba(15,23,42,.06)}
.row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:9px}.row:last-child{margin-bottom:0}
input[type=search],select{font-family:inherit;font-size:16px;padding:8px 11px;border:1px solid var(--line);
  border-radius:10px;background:#f8fafc;color:var(--ink)}
input[type=search]{flex:1;min-width:210px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 13px;cursor:pointer;
  font-size:14.5px;font-family:inherit;font-weight:700;color:#475569}
.chip.on{color:#fff;border-color:transparent}
.btn{font-family:inherit;font-weight:700;font-size:15.5px;padding:8px 16px;border-radius:10px;border:none;
  cursor:pointer;background:linear-gradient(135deg,#047857,#1d4ed8);color:#fff}
.btn.ghost{background:#fff;color:#334155;border:1px solid var(--line)}
.btn.gold{background:linear-gradient(135deg,#f59e0b,#dc2626)}
.btn.on{outline:3px solid #fbbf24}
.q{background:#fff;border:1px solid var(--line);border-right:6px solid #94a3b8;border-radius:14px;
  padding:13px 15px;margin-bottom:11px;box-shadow:0 4px 14px rgba(15,23,42,.05)}
.q.star{background:linear-gradient(180deg,#fffbeb 0%,#fff 60%);border-color:#fcd34d}
.q .meta{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-bottom:7px;font-size:12.5px;color:var(--muted)}
.tag{border-radius:999px;padding:2px 9px;color:#fff;font-weight:700;font-size:12px}
.tag.soft{background:#eef2ff;color:#4338ca}.tag.src{background:#f1f5f9;color:#475569}
.tag.hot{background:linear-gradient(135deg,#f59e0b,#dc2626)}
.tag.rep{background:#fef3c7;color:#92400e}
.qtext{font-weight:800;font-size:17px;margin-bottom:9px}
.opts{display:grid;gap:6px}
.opt{display:flex;gap:9px;align-items:flex-start;border:1px solid var(--line);border-radius:10px;
  padding:7px 10px;cursor:pointer;background:#f8fafc;transition:.15s}
.opt:hover{background:#ecfdf5}
.opt .lab{min-width:25px;height:25px;border-radius:50%;background:#e2e8f0;color:#334155;display:grid;
  place-items:center;font-weight:800;font-size:13.5px}
.opt.right{background:#dcfce7;border-color:#86efac}.opt.right .lab{background:var(--ok);color:#fff}
.opt.wrong{background:#fee2e2;border-color:#fca5a5}.opt.wrong .lab{background:var(--no);color:#fff}
.exp{margin-top:9px;background:#f0fdf4;border:1px dashed #86efac;border-radius:10px;padding:8px 11px;
  font-size:15.5px;color:#14532d;display:none}
.exp.on{display:block}
.ltr{direction:ltr;text-align:left;font-family:"Segoe UI",Arial,sans-serif}
.pager{display:flex;gap:7px;justify-content:center;align-items:center;flex-wrap:wrap;margin:16px 0}
.pager button{font-family:inherit;border:1px solid var(--line);background:#fff;border-radius:9px;
  padding:6px 13px;cursor:pointer;font-weight:700}
.pager button:disabled{opacity:.45;cursor:default}
.kbcard{background:#fff;border:1px solid var(--line);border-radius:14px;margin-bottom:12px;overflow:hidden}
.kbcard h3{margin:0;padding:11px 15px;font-size:17px;color:#fff;cursor:pointer;display:flex;
  justify-content:space-between;align-items:center;gap:8px}
.kbcard table{width:100%;border-collapse:collapse;font-size:15.5px;display:none}
.kbcard.open table{display:table}
.kbcard td{border-top:1px solid var(--line);padding:8px 13px;vertical-align:top}
.kbcard td.n{font-weight:800;width:33%;background:#f8fafc}
.kbcard .note{display:none;padding:9px 15px;background:#ecfeff;color:#155e75;font-size:14.5px;border-top:1px solid var(--line)}
.kbcard.open .note{display:block}
.ex{display:block;color:#7c3aed;font-size:14px;margin-top:3px}
.sc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;text-align:center;margin-bottom:14px}
.sc .big{font-size:44px;font-weight:900}
.secbar{display:flex;justify-content:space-between;align-items:center;gap:8px;background:#0f172a;color:#fff;
  border-radius:12px;padding:8px 14px;margin:18px 0 10px;font-weight:800}
.hide{display:none}
footer{text-align:center;color:var(--muted);font-size:13.5px;padding:24px 10px 40px}
@media print{nav.tabs,.toolbar,.pager,.btn{display:none!important}.q{break-inside:avoid;box-shadow:none}
  .exp{display:block!important}body{background:#fff}}
@media(max-width:600px){header.hero h1{font-size:23px}body{font-size:16px}main{padding:10px 7px 60px}}
"""


def build():
    qs = collect()
    errs = validate(qs)
    if errs:
        print("‼ ملاحظات:", len(errs))
        for e in errs[:15]:
            print("   ", e)
    rows, topics, srcs = pack(qs)
    data = json.dumps({"q": rows, "topics": topics, "srcs": srcs,
                       "secs": [{"id": s, "name": n, "color": c} for s, n, c in SECS],
                       "kb": kb_payload()}, ensure_ascii=False, separators=(",", ":"))

    n_star = sum(1 for q in qs if q["r"] == 2)
    n_rep = sum(1 for q in qs if q["r"] == 1)
    per_sec = {s: sum(1 for q in qs if q["x"] == s) for s, _, _ in SECS}
    sec_rows = "\n".join(
        f"<tr><td style='font-weight:800;color:{c}'>{n}</td><td>{ar(per_sec[s])}</td>"
        f"<td>{ar(sum(1 for q in qs if q['x'] == s and q['r'] == 2))}</td></tr>"
        for s, n, c in SECS)

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>بنك أسئلة مسابقة الأزهر — معلم لغة عربية (كل الأقسام بالإجابات)</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <h1>بنك أسئلة مسابقة الأزهر 🕌📖</h1>
  <p>معلم لغة عربية — كل أقسام الاختبار في ملف واحد: التخصص والتربوي والكفايات السلوكية
  والحاسب والمعلومات العامة والإنجليزي والذكاء</p>
  <div class="stats">
    <div class="stat"><b>{ar(len(qs))}</b><span>سؤالًا بالإجابة والشرح</span></div>
    <div class="stat"><b>⭐ {ar(n_star)}</b><span>الأكثر تكرارًا</span></div>
    <div class="stat"><b>🔁 {ar(n_rep)}</b><span>متكررة ومهمة</span></div>
    <div class="stat"><b>{ar(len(SECS))}</b><span>أقسام</span></div>
    <div class="stat"><b>{ar(len(topics))}</b><span>موضوعًا</span></div>
  </div>
</header>

<nav class="tabs">
  <button class="on" data-tab="hot">🔥 الأشهر والأكثر تكرارًا</button>
  <button data-tab="bank">🗂️ بنك الأسئلة</button>
  <button data-tab="exam">📝 امتحان محاكٍ</button>
  <button data-tab="review">⚡ المراجعة السريعة</button>
  <button data-tab="about">ℹ️ عن الملف</button>
</nav>

<main>
  <section class="panel on" id="hot">
    <div class="toolbar">
      <div class="row"><b>⭐ هذه أهم أسئلة المسابقة وأكثرها تكرارًا</b></div>
      <div class="row" style="color:var(--muted);font-size:15px">
        ركّز عليها أولًا؛ وهي مرتبة حسب القسم. الإجابات والشروح تظهر بالضغط على أي اختيار،
        أو اضغط «إظهار كل الإجابات».</div>
      <div class="row">
        <button class="btn ghost" id="hotToggle">👁️ إظهار كل الإجابات</button>
        <input type="search" id="hotSearch" placeholder="🔎 ابحث داخل الأسئلة الأكثر تكرارًا…">
      </div>
    </div>
    <div id="hotList"></div>
  </section>

  <section class="panel" id="bank">
    <div class="toolbar">
      <div class="row">
        <input type="search" id="search" placeholder="🔎 ابحث في كل الأسئلة… (إعراب، بلوم، Excel، tense، الأزهر)">
        <select id="topic"><option value="">كل الموضوعات</option></select>
      </div>
      <div class="row" id="secChips"></div>
      <div class="row">
        <button class="btn ghost" id="onlyStar">⭐ الأكثر تكرارًا فقط</button>
        <button class="btn ghost" id="toggleAll">👁️ إظهار كل الإجابات</button>
        <button class="btn ghost" id="shuffle">🔀 ترتيب عشوائي</button>
        <span id="count" style="color:var(--muted);font-weight:700"></span>
      </div>
    </div>
    <div id="list"></div>
    <div class="pager" id="pager"></div>
  </section>

  <section class="panel" id="exam">
    <div class="toolbar">
      <div class="row">
        <label>نوع الامتحان:</label>
        <select id="exMode">
          <option value="sim">محاكاة المسابقة (كل الأقسام)</option>
          <option value="star">الأكثر تكرارًا فقط</option>
          <option value="sec">قسم واحد</option>
        </select>
        <select id="exSec"></select>
        <label>عدد الأسئلة:</label>
        <select id="exCount"><option>20</option><option selected>30</option><option>50</option>
          <option>75</option><option>100</option></select>
        <button class="btn gold" id="exStart">ابدأ ▶</button>
      </div>
      <div class="row" style="color:var(--muted);font-size:15px">
        محاكاة المسابقة توزّع الأسئلة على الأقسام السبعة بنسب قريبة من الاختبار الفعلي.
      </div>
    </div>
    <div id="exResult"></div>
    <div id="exList"></div>
    <div class="pager hide" id="exBar">
      <button class="btn" id="exSubmit">✅ تصحيح الامتحان</button>
      <button class="btn ghost" id="exAgain">↻ امتحان جديد</button>
    </div>
  </section>

  <section class="panel" id="review">
    <div class="toolbar">
      <div class="row">
        <input type="search" id="kbSearch" placeholder="🔎 ابحث في المفاهيم والقواعد…">
        <button class="btn ghost" id="kbAll">فتح/طي الكل</button>
      </div>
      <div class="row" id="kbChips"></div>
    </div>
    <div id="kbList"></div>
  </section>

  <section class="panel" id="about">
    <div class="toolbar">
      <h2 style="margin-top:0">عن هذا الملف</h2>
      <p>ملف واحد مستقل (يعمل بدون إنترنت) يجمع <b>{ar(len(qs))}</b> سؤالًا بالإجابة النموذجية
      وشرح سببها، موزعة على أقسام اختبار مسابقة الأزهر لمعلم اللغة العربية:</p>
      <table style="width:100%;border-collapse:collapse;font-size:16px">
        <tr style="background:#f1f5f9"><td style="padding:6px 10px"><b>القسم</b></td>
        <td style="padding:6px 10px"><b>عدد الأسئلة</b></td><td style="padding:6px 10px"><b>منها ⭐ الأكثر تكرارًا</b></td></tr>
        {sec_rows}
      </table>
      <p style="margin-top:14px"><b>كيف مُيّزت الأسئلة؟</b></p>
      <ul>
        <li><span class="tag hot">⭐ الأكثر تكرارًا</span> أسئلة تتكرر في المسابقات فعليًا أو تدور حولها
        معظم الامتحانات (إعراب، ممنوع من الصرف، ميزان صرفي، صور بلاغية، إملاء، بلوم، الصدق والثبات،
        مواقف سلوكية، اختصارات الحاسب، معلومات الأزهر، قواعد الإنجليزي الأساسية، علاقات لفظية).</li>
        <li><span class="tag rep">🔁 متكرر</span> أسئلة في الموضوعات المهمة التي لا يخلو منها امتحان.</li>
        <li>الباقي أسئلة تدريب تغطي بقية التفاصيل حتى لا يفاجئك سؤال خارج المألوف.</li>
      </ul>
      <p><b>طريقة الاستخدام المقترحة:</b> ابدأ بتبويب «🔥 الأشهر والأكثر تكرارًا» كاملًا، ثم ذاكر
      «⚡ المراجعة السريعة» لكل قسم، ثم طبّق في «📝 امتحان محاكٍ» حتى تثبت درجتك فوق ٨٥٪،
      وأخيرًا امسح بقية البنك بالتصفية حسب الموضوع.</p>
      <p style="color:var(--muted)">تنبيه: المعلومات ذات الطابع الرسمي (قوانين، مسميات، أرقام قرارات)
      مذكورة في حدود الثابت والمستقر؛ راجع آخر القرارات الرسمية قبل الامتحان.</p>
    </div>
  </section>
</main>

<footer>بنك أسئلة مسابقة الأزهر — معلم لغة عربية · {ar(len(qs))} سؤالًا بالإجابات والشرح · ملف واحد بدون إنترنت</footer>

<script id="DATA" type="application/json">{data}</script>
<script>
const D = JSON.parse(document.getElementById('DATA').textContent);
const SC = {{}}; D.secs.forEach(s=>SC[s.id]=s);
const LAB = ['أ','ب','ج','د'];
const AD = n => String(n).replace(/[0-9]/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const QS = D.q.map((x,i)=>({{i:i,q:x[0],o:x[1],a:x[2],e:x[3],x:x[4],t:D.topics[x[5]],s:D.srcs[x[6]],r:x[7]}}));
const isEn = t => /[A-Za-z]/.test(t) && !/[\\u0600-\\u06FF]/.test(t);
let view = QS.slice(), page = 0, per = 25, showAll = false, starOnly = false;
let fSec='', fTopic='', fText='';

document.querySelectorAll('nav.tabs button').forEach(b=>{{
  b.onclick=()=>{{
    document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('on'));
    document.getElementById(b.dataset.tab).classList.add('on');
    window.scrollTo({{top:0,behavior:'smooth'}});
  }};
}});

function card(q, idx, forceShow){{
  const sc = SC[q.x];
  const el = document.createElement('div');
  el.className = 'q' + (q.r===2?' star':'');
  el.style.borderRightColor = sc.color;
  const badge = q.r===2 ? '<span class="tag hot">⭐ الأكثر تكرارًا</span>'
              : q.r===1 ? '<span class="tag rep">🔁 متكرر</span>' : '';
  el.innerHTML =
    `<div class="meta"><span class="tag" style="background:${{sc.color}}">${{sc.name}}</span>
      <span class="tag soft">${{q.t}}</span>${{badge}}
      <span class="tag src">${{q.s}}</span>
      <span style="margin-inline-start:auto">#${{AD(idx)}}</span></div>
     <div class="qtext${{isEn(q.q)?' ltr':''}}">${{q.q}}</div>
     <div class="opts">${{q.o.map((o,i)=>
        `<div class="opt${{isEn(o)?' ltr':''}}" data-i="${{i}}"><span class="lab">${{LAB[i]}}</span><span>${{o}}</span></div>`).join('')}}</div>
     <div class="exp"><b>الإجابة: ${{LAB[q.a]}}) ${{q.o[q.a]}}</b><br>${{q.e}}</div>`;
  const exp = el.querySelector('.exp');
  el.querySelectorAll('.opt').forEach(op=>{{
    op.onclick=()=>{{
      const i=+op.dataset.i;
      el.querySelectorAll('.opt').forEach((o,j)=>{{
        o.classList.toggle('right', j===q.a);
        if(j===i && i!==q.a) o.classList.add('wrong');
      }});
      exp.classList.add('on');
    }};
  }});
  if(forceShow){{ exp.classList.add('on'); el.querySelectorAll('.opt')[q.a].classList.add('right'); }}
  return el;
}}
function norm(s){{return s.replace(/[\\u064B-\\u0652\\u0640]/g,'').replace(/[إأآا]/g,'ا').replace(/[ىي]/g,'ي').replace(/ة/g,'ه').toLowerCase();}}

/* ---------- تبويب الأكثر تكرارًا ---------- */
let hotShow=false;
const HOT = QS.filter(q=>q.r===2);
function hotRender(){{
  const box=document.getElementById('hotList'); box.innerHTML='';
  const t=norm(document.getElementById('hotSearch').value.trim());
  D.secs.forEach(s=>{{
    const items=HOT.filter(q=>q.x===s.id && (!t || norm(q.q+' '+q.o.join(' ')+' '+q.e).includes(t)));
    if(!items.length) return;
    const bar=document.createElement('div'); bar.className='secbar';
    bar.style.background=s.color;
    bar.innerHTML=`<span>${{s.name}}</span><span>${{AD(items.length)}} سؤالًا</span>`;
    box.appendChild(bar);
    items.forEach((q,k)=>box.appendChild(card(q,k+1,hotShow)));
  }});
  if(!box.children.length) box.innerHTML='<p style="text-align:center;color:#64748b">لا توجد نتائج</p>';
}}
document.getElementById('hotToggle').onclick=e=>{{
  hotShow=!hotShow; e.target.textContent=hotShow?'🙈 إخفاء كل الإجابات':'👁️ إظهار كل الإجابات'; hotRender();
}};
let th; document.getElementById('hotSearch').oninput=()=>{{clearTimeout(th);th=setTimeout(hotRender,180);}};

/* ---------- بنك الأسئلة ---------- */
const chips=document.getElementById('secChips');
const allChip=document.createElement('button');
allChip.className='chip on'; allChip.textContent='كل الأقسام ('+AD(QS.length)+')';
allChip.dataset.v=''; allChip.style.background='#334155'; allChip.style.color='#fff';
chips.appendChild(allChip);
D.secs.forEach(s=>{{
  const n=QS.filter(q=>q.x===s.id).length;
  const b=document.createElement('button'); b.className='chip';
  b.textContent=s.name+' ('+AD(n)+')'; b.dataset.v=s.id; b.dataset.c=s.color; chips.appendChild(b);
}});
chips.onclick=e=>{{
  const b=e.target.closest('.chip'); if(!b) return;
  [...chips.children].forEach(c=>{{c.classList.remove('on');c.style.background='';c.style.color='';}});
  b.classList.add('on'); b.style.background=b.dataset.c||'#334155'; b.style.color='#fff';
  fSec=b.dataset.v; fTopic=''; fillTopics(); apply();
}};
const topicSel=document.getElementById('topic');
function fillTopics(){{
  const set=new Set(QS.filter(q=>!fSec||q.x===fSec).map(q=>q.t));
  topicSel.innerHTML='<option value="">كل الموضوعات</option>'+[...set].sort().map(t=>`<option>${{t}}</option>`).join('');
}}
fillTopics();
topicSel.onchange=()=>{{fTopic=topicSel.value;apply();}};
let tmr; document.getElementById('search').oninput=e=>{{clearTimeout(tmr);tmr=setTimeout(()=>{{fText=e.target.value.trim();apply();}},180);}};
document.getElementById('onlyStar').onclick=e=>{{
  starOnly=!starOnly; e.target.classList.toggle('on',starOnly);
  e.target.textContent = starOnly?'⭐ عرض الكل':'⭐ الأكثر تكرارًا فقط'; apply();
}};
document.getElementById('toggleAll').onclick=e=>{{
  showAll=!showAll; e.target.textContent=showAll?'🙈 إخفاء كل الإجابات':'👁️ إظهار كل الإجابات'; render();
}};
document.getElementById('shuffle').onclick=()=>{{
  for(let i=view.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[view[i],view[j]]=[view[j],view[i]];}}
  page=0;render();
}};
function apply(){{
  const t=norm(fText);
  view=QS.filter(q=>{{
    if(fSec&&q.x!==fSec) return false;
    if(fTopic&&q.t!==fTopic) return false;
    if(starOnly&&q.r!==2) return false;
    if(t&&!norm(q.q+' '+q.o.join(' ')+' '+q.e).includes(t)) return false;
    return true;
  }});
  page=0;render();
}}
function render(){{
  const list=document.getElementById('list'); list.innerHTML='';
  const total=view.length, pages=Math.max(1,Math.ceil(total/per));
  if(page>=pages) page=pages-1;
  const st=page*per;
  view.slice(st,st+per).forEach((q,k)=>list.appendChild(card(q,st+k+1,showAll)));
  document.getElementById('count').textContent= total?`${{AD(total)}} سؤالًا — صفحة ${{AD(page+1)}} من ${{AD(pages)}}`:'لا توجد نتائج';
  const pg=document.getElementById('pager'); pg.innerHTML='';
  const mkb=(txt,fn,dis)=>{{const b=document.createElement('button');b.textContent=txt;b.disabled=!!dis;b.onclick=fn;pg.appendChild(b);}};
  mkb('« الأولى',()=>{{page=0;render();top();}},page===0);
  mkb('السابق',()=>{{page--;render();top();}},page===0);
  const sel=document.createElement('select');
  for(let i=0;i<pages;i++){{const o=document.createElement('option');o.value=i;o.textContent='صفحة '+AD(i+1);if(i===page)o.selected=true;sel.appendChild(o);}}
  sel.onchange=()=>{{page=+sel.value;render();top();}}; pg.appendChild(sel);
  mkb('التالي',()=>{{page++;render();top();}},page>=pages-1);
  mkb('الأخيرة »',()=>{{page=pages-1;render();top();}},page>=pages-1);
  const ps=document.createElement('select');
  [10,25,50,100].forEach(v=>{{const o=document.createElement('option');o.value=v;o.textContent=AD(v)+' بالصفحة';if(v===per)o.selected=true;ps.appendChild(o);}});
  ps.onchange=()=>{{per=+ps.value;page=0;render();}}; pg.appendChild(ps);
}}
function top(){{document.getElementById('bank').scrollIntoView({{behavior:'smooth'}});}}

/* ---------- الامتحان ---------- */
const exSec=document.getElementById('exSec');
exSec.innerHTML=D.secs.map(s=>`<option value="${{s.id}}">${{s.name}}</option>`).join('');
exSec.classList.add('hide');
document.getElementById('exMode').onchange=e=>exSec.classList.toggle('hide', e.target.value!=='sec');
const SHARE={{spec:0.40,tarb:0.20,behav:0.10,comp:0.08,gen:0.08,eng:0.08,iq:0.06}};
let exam=[], answers={{}};
function shuffle(a){{for(let i=a.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}}return a;}}
document.getElementById('exStart').onclick=()=>{{
  const mode=document.getElementById('exMode').value, n=+document.getElementById('exCount').value;
  let pool=[];
  if(mode==='sim'){{
    D.secs.forEach(s=>{{
      const k=Math.max(1,Math.round(n*(SHARE[s.id]||0.1)));
      const cand=shuffle(QS.filter(q=>q.x===s.id).slice());
      cand.sort((p,q)=>q.r-p.r);
      pool=pool.concat(shuffle(cand.slice(0,Math.min(cand.length,k*3))).slice(0,k));
    }});
    pool=pool.slice(0,n);
  }} else if(mode==='star'){{
    pool=shuffle(QS.filter(q=>q.r===2).slice()).slice(0,n);
  }} else {{
    pool=shuffle(QS.filter(q=>q.x===exSec.value).slice()).slice(0,n);
  }}
  exam=pool; answers={{}};
  document.getElementById('exResult').innerHTML='';
  document.getElementById('exBar').classList.remove('hide');
  const box=document.getElementById('exList'); box.innerHTML='';
  exam.forEach((q,k)=>{{
    const sc=SC[q.x];
    const el=document.createElement('div'); el.className='q'; el.style.borderRightColor=sc.color;
    el.innerHTML=`<div class="meta"><span class="tag" style="background:${{sc.color}}">${{sc.name}}</span>
      <span class="tag soft">${{q.t}}</span><span style="margin-inline-start:auto">سؤال ${{AD(k+1)}}</span></div>
      <div class="qtext${{isEn(q.q)?' ltr':''}}">${{q.q}}</div>
      <div class="opts">${{q.o.map((o,i)=>`<div class="opt${{isEn(o)?' ltr':''}}" data-i="${{i}}"><span class="lab">${{LAB[i]}}</span><span>${{o}}</span></div>`).join('')}}</div>
      <div class="exp"></div>`;
    el.querySelectorAll('.opt').forEach(op=>{{
      op.onclick=()=>{{
        if(el.dataset.done) return;
        answers[k]=+op.dataset.i;
        el.querySelectorAll('.opt').forEach(o=>o.style.outline='');
        op.style.outline='3px solid #047857';
      }};
    }});
    box.appendChild(el);
  }});
  box.scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('exSubmit').onclick=()=>{{
  let right=0; const cards=document.querySelectorAll('#exList .q'); const bySec={{}};
  exam.forEach((q,k)=>{{
    const el=cards[k]; el.dataset.done='1'; const pick=answers[k];
    bySec[q.x]=bySec[q.x]||[0,0]; bySec[q.x][1]++;
    if(pick===q.a){{right++;bySec[q.x][0]++;}}
    el.querySelectorAll('.opt').forEach((o,j)=>{{
      o.style.outline='';
      if(j===q.a)o.classList.add('right');
      if(j===pick&&pick!==q.a)o.classList.add('wrong');
    }});
    const exp=el.querySelector('.exp');
    exp.innerHTML=`<b>الإجابة الصحيحة: ${{LAB[q.a]}}) ${{q.o[q.a]}}</b><br>${{q.e}}`;
    exp.classList.add('on');
  }});
  const pct=Math.round(right/exam.length*100);
  const msg=pct>=85?'ممتاز 👏':pct>=70?'جيد جدًا ✅':pct>=50?'تحتاج مراجعة 📖':'راجع الأقسام الضعيفة 💪';
  const det=Object.keys(bySec).map(s=>`${{SC[s].name}}: ${{AD(bySec[s][0])}}/${{AD(bySec[s][1])}}`).join(' · ');
  document.getElementById('exResult').innerHTML=
   `<div class="sc"><div class="big" style="color:${{pct>=70?'#16a34a':pct>=50?'#f59e0b':'#dc2626'}}">${{AD(pct)}}٪</div>
    <div>أجبت إجابة صحيحة عن <b>${{AD(right)}}</b> من <b>${{AD(exam.length)}}</b> — ${{msg}}</div>
    <div style="color:#64748b;font-size:15px;margin-top:6px">${{det}}</div></div>`;
  document.getElementById('exResult').scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('exAgain').onclick=()=>document.getElementById('exStart').click();

/* ---------- المراجعة السريعة ---------- */
const kbList=document.getElementById('kbList'), kbChips=document.getElementById('kbChips');
let kbSec='';
const kbAllChip=document.createElement('button');
kbAllChip.className='chip on'; kbAllChip.textContent='كل الأقسام'; kbAllChip.dataset.v='';
kbAllChip.style.background='#334155'; kbAllChip.style.color='#fff'; kbChips.appendChild(kbAllChip);
D.secs.forEach(s=>{{
  if(!D.kb.some(g=>g.sec===s.id)) return;
  const b=document.createElement('button'); b.className='chip'; b.textContent=s.name;
  b.dataset.v=s.id; b.dataset.c=s.color; kbChips.appendChild(b);
}});
kbChips.onclick=e=>{{
  const b=e.target.closest('.chip'); if(!b) return;
  [...kbChips.children].forEach(c=>{{c.classList.remove('on');c.style.background='';c.style.color='';}});
  b.classList.add('on'); b.style.background=b.dataset.c||'#334155'; b.style.color='#fff';
  kbSec=b.dataset.v; kbRender();
}};
document.getElementById('kbSearch').oninput=()=>kbRender();
document.getElementById('kbAll').onclick=()=>{{
  const any=kbList.querySelector('.kbcard:not(.open)');
  kbList.querySelectorAll('.kbcard').forEach(c=>c.classList.toggle('open',!!any));
}};
function kbRender(){{
  const t=norm(document.getElementById('kbSearch').value.trim());
  kbList.innerHTML='';
  D.kb.forEach(g=>{{
    if(kbSec&&g.sec!==kbSec) return;
    const items=t?g.items.filter(it=>norm(it[0]+' '+it[1]+' '+it[2]).includes(t)):g.items;
    if(!items.length) return;
    const sc=SC[g.sec]||{{color:'#334155',name:''}};
    const c=document.createElement('div'); c.className='kbcard'+(t?' open':'');
    c.innerHTML=`<h3 style="background:${{sc.color}}"><span>${{g.hot?'⭐ ':''}}${{g.cat}}</span>
      <span style="font-size:13.5px;opacity:.92">${{sc.name}} · ${{AD(items.length)}}</span></h3>
      <table>${{items.map(it=>`<tr><td class="n">${{it[0]}}${{it[2]?' <span style="background:#92400e;color:#fde68a;border-radius:6px;padding:1px 6px;font-size:12px">'+it[2]+'</span>':''}}</td>
      <td>${{it[1]}}${{it[3]?'<span class="ex">🧩 '+it[3]+'</span>':''}}</td></tr>`).join('')}}</table>
      ${{g.note?`<div class="note">📌 ${{g.note}}</div>`:''}}`;
    c.querySelector('h3').onclick=()=>c.classList.toggle('open');
    kbList.appendChild(c);
  }});
  if(!kbList.children.length) kbList.innerHTML='<p style="text-align:center;color:#64748b">لا توجد نتائج</p>';
}}
hotRender(); render(); kbRender();
</script>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {OUT} ({os.path.getsize(OUT)/1024:.0f} KB)")
    print(f"   المجموع: {len(qs)} سؤالًا | ⭐ {n_star} | 🔁 {n_rep} | موضوعات: {len(topics)}")
    for s, n, _ in SECS:
        print(f"   - {n}: {per_sec[s]}")
    return len(qs)


if __name__ == "__main__":
    build()
