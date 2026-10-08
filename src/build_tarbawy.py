# -*- coding: utf-8 -*-
"""يبني ملف tarbawy-guide.html : بنك أسئلة التربوي لمسابقات التعيين (أسئلة + إجابات + شرح)."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tarbawy"))

import gen            # noqa: E402
import curated        # noqa: E402
from kb_core import G  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "tarbawy-guide.html")

AXES = [
    ("psych", "علم النفس التربوي", "#6366f1"),
    ("goals", "الأهداف التربوية", "#0ea5e9"),
    ("curric", "المناهج", "#10b981"),
    ("teach", "طرق التدريس", "#f59e0b"),
    ("eval", "القياس والتقويم", "#ef4444"),
    ("calc", "مسائل القياس والإحصاء", "#be123c"),
    ("tech", "تكنولوجيا التعليم", "#8b5cf6"),
    ("mgmt", "الإدارة الصفية", "#14b8a6"),
    ("law", "التشريعات والأخلاقيات", "#f43f5e"),
    ("research", "البحث والتنمية المهنية", "#84cc16"),
    ("special", "التربية الخاصة", "#06b6d4"),
]
AXIS_NAME = {a: n for a, n, _ in AXES}


def collect():
    qs = gen.kb_bank() + gen.num_bank() + curated.bank(gen.mk)
    seen, out = set(), []
    for q in qs:
        key = (q["q"].strip(), tuple(sorted(q["o"])))
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
    # الأسئلة المحصّلة من الامتحانات أولًا
    rank = {curated.SRC_EXAM: 0, curated.SRC_SJT: 1}
    out.sort(key=lambda q: (rank.get(q["s"], 2), q["x"], q["t"]))
    return out


def validate(qs):
    errs = []
    for i, q in enumerate(qs):
        if len(q["o"]) != 4:
            errs.append(f"{i}: عدد البدائل {len(q['o'])}")
        if len(set(q["o"])) != 4:
            errs.append(f"{i}: بدائل مكررة — {q['q'][:40]}")
        if not (0 <= q["a"] < 4):
            errs.append(f"{i}: مفتاح خارج النطاق")
        if not q["e"].strip():
            errs.append(f"{i}: بلا تفسير")
        if not q["q"].strip().endswith(("؟", ":", "؟:")):
            pass
        if q["x"] not in AXIS_NAME:
            errs.append(f"{i}: محور غير معروف {q['x']}")
    return errs


def pack(qs):
    topics, srcs = [], []
    ti, si = {}, {}
    rows = []
    for q in qs:
        t = q["t"]
        if t not in ti:
            ti[t] = len(topics)
            topics.append(t)
        s = q["s"]
        if s not in si:
            si[s] = len(srcs)
            srcs.append(s)
        rows.append([q["q"], q["o"], q["a"], q["e"], q["x"], ti[t], si[s]])
    return rows, topics, srcs


def kb_payload():
    out = []
    for g in G:
        out.append({
            "id": g["id"], "axis": g["axis"], "cat": g["cat"],
            "note": g.get("note") or "",
            "items": [[i["n"], i["d"], i.get("p", ""), i.get("ex", "")] for i in g["items"]],
        })
    return out


CSS = """
*{box-sizing:border-box}
:root{
  --bg:#0f172a;--bg2:#15213b;--card:#ffffff;--ink:#0f172a;--muted:#64748b;
  --line:#e2e8f0;--ok:#16a34a;--no:#dc2626;--gold:#f59e0b;
}
html,body{margin:0;padding:0}
body{
  font-family:"Segoe UI","Tahoma","Noto Naskh Arabic","Noto Sans Arabic","Arial",sans-serif;
  background:linear-gradient(180deg,#eef2ff 0%,#f8fafc 320px,#f8fafc 100%);
  color:var(--ink);direction:rtl;line-height:1.85;font-size:17px;
}
header.hero{
  background:radial-gradient(1200px 400px at 80% -40%,#38bdf8 0%,transparent 60%),
             linear-gradient(135deg,#1e1b4b 0%,#312e81 45%,#0f766e 100%);
  color:#fff;padding:34px 20px 26px;text-align:center;box-shadow:0 10px 30px rgba(15,23,42,.25);
}
header.hero h1{margin:0 0 6px;font-size:34px;letter-spacing:.5px}
header.hero p{margin:0;opacity:.92;font-size:17px}
.stats{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:18px}
.stat{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);
  border-radius:14px;padding:10px 18px;min-width:120px;backdrop-filter:blur(4px)}
.stat b{display:block;font-size:24px}
.stat span{font-size:13px;opacity:.9}
nav.tabs{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;
  position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line);
  padding:10px;box-shadow:0 2px 10px rgba(15,23,42,.06)}
nav.tabs button{border:1px solid var(--line);background:#f8fafc;border-radius:999px;
  padding:8px 18px;font-size:16px;font-family:inherit;cursor:pointer;font-weight:700;color:#334155}
nav.tabs button.on{background:linear-gradient(135deg,#4f46e5,#0ea5e9);color:#fff;border-color:transparent}
main{max-width:1060px;margin:0 auto;padding:18px 14px 80px}
.panel{display:none}.panel.on{display:block}
.toolbar{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px;
  margin-bottom:16px;box-shadow:0 6px 18px rgba(15,23,42,.06)}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.row:last-child{margin-bottom:0}
input[type=search],select{font-family:inherit;font-size:16px;padding:9px 12px;border:1px solid var(--line);
  border-radius:10px;background:#f8fafc;color:var(--ink)}
input[type=search]{flex:1;min-width:220px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;
  cursor:pointer;font-size:15px;font-family:inherit;font-weight:700;color:#475569}
.chip.on{color:#fff;border-color:transparent}
.btn{font-family:inherit;font-weight:700;font-size:16px;padding:9px 18px;border-radius:10px;
  border:none;cursor:pointer;background:linear-gradient(135deg,#4f46e5,#0ea5e9);color:#fff}
.btn.ghost{background:#fff;color:#334155;border:1px solid var(--line)}
.btn.gold{background:linear-gradient(135deg,#f59e0b,#ef4444)}
.q{background:var(--card);border:1px solid var(--line);border-right:6px solid #94a3b8;
  border-radius:14px;padding:14px 16px;margin-bottom:12px;box-shadow:0 4px 14px rgba(15,23,42,.05)}
.q .meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px;font-size:13px;color:var(--muted)}
.tag{border-radius:999px;padding:2px 10px;color:#fff;font-weight:700;font-size:12.5px}
.tag.soft{background:#eef2ff;color:#4338ca}
.tag.src{background:#f1f5f9;color:#475569}
.qtext{font-weight:800;font-size:17.5px;margin-bottom:10px}
.opts{display:grid;gap:7px}
.opt{display:flex;gap:9px;align-items:flex-start;border:1px solid var(--line);border-radius:10px;
  padding:8px 11px;cursor:pointer;background:#f8fafc;transition:.15s}
.opt:hover{background:#eef2ff}
.opt .lab{min-width:26px;height:26px;border-radius:50%;background:#e2e8f0;color:#334155;
  display:grid;place-items:center;font-weight:800;font-size:14px}
.opt.right{background:#dcfce7;border-color:#86efac}
.opt.right .lab{background:var(--ok);color:#fff}
.opt.wrong{background:#fee2e2;border-color:#fca5a5}
.opt.wrong .lab{background:var(--no);color:#fff}
.exp{margin-top:10px;background:#fffbeb;border:1px dashed #fcd34d;border-radius:10px;
  padding:9px 12px;font-size:15.5px;color:#78350f;display:none}
.exp.on{display:block}
.exp b{color:#92400e}
.pager{display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap;margin:18px 0}
.pager button{font-family:inherit;border:1px solid var(--line);background:#fff;border-radius:9px;
  padding:7px 14px;cursor:pointer;font-weight:700}
.pager button:disabled{opacity:.45;cursor:default}
.kbcard{background:#fff;border:1px solid var(--line);border-radius:14px;margin-bottom:14px;overflow:hidden}
.kbcard h3{margin:0;padding:12px 16px;font-size:18px;color:#fff;cursor:pointer;
  display:flex;justify-content:space-between;align-items:center}
.kbcard table{width:100%;border-collapse:collapse;font-size:16px;display:none}
.kbcard.open table{display:table}
.kbcard td{border-top:1px solid var(--line);padding:9px 14px;vertical-align:top}
.kbcard td.n{font-weight:800;width:32%;color:#1e293b;background:#f8fafc}
.kbcard .note{display:none;padding:10px 16px;background:#ecfeff;color:#155e75;font-size:15px;border-top:1px solid var(--line)}
.kbcard.open .note{display:block}
.ex{display:block;color:#7c3aed;font-size:14.5px;margin-top:3px}
.sc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;text-align:center;margin-bottom:16px}
.sc .big{font-size:46px;font-weight:900}
.hide{display:none}
footer{text-align:center;color:var(--muted);font-size:14px;padding:26px 10px 40px}
@media print{
  nav.tabs,.toolbar,.pager,.btn{display:none!important}
  .q{break-inside:avoid;box-shadow:none}
  .exp{display:block!important}
  body{background:#fff}
}
@media(max-width:600px){
  header.hero h1{font-size:25px}body{font-size:16px}
  main{padding:12px 8px 60px}
}
"""


def ar(n):
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def build():
    qs = collect()
    errs = validate(qs)
    if errs:
        print("‼ أخطاء:", len(errs))
        for e in errs[:20]:
            print("   ", e)
    rows, topics, srcs = pack(qs)
    payload = {
        "q": rows, "topics": topics, "srcs": srcs,
        "axes": [{"id": a, "name": n, "color": c} for a, n, c in AXES],
        "kb": kb_payload(),
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    n_exam = sum(1 for q in qs if q["s"] == curated.SRC_EXAM)
    n_sjt = sum(1 for q in qs if q["s"] == curated.SRC_SJT)
    n_kb = len(G)
    n_items = sum(len(g["items"]) for g in G)

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>بنك أسئلة التربوي — مسابقات التعيين (أسئلة بالإجابات والشرح)</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <h1>بنك أسئلة التربوي 📚</h1>
  <p>مسابقات تعيين المعلمين — أسئلة بالإجابات النموذجية والشرح، في كل محاور التربوي</p>
  <div class="stats">
    <div class="stat"><b id="sTotal">{ar(len(qs))}</b><span>سؤال بالإجابة</span></div>
    <div class="stat"><b>{ar(len(AXES))}</b><span>محاور تربوية</span></div>
    <div class="stat"><b>{ar(len(topics))}</b><span>موضوعًا فرعيًا</span></div>
    <div class="stat"><b>{ar(n_exam + n_sjt)}</b><span>سؤال امتحانات ومواقف</span></div>
    <div class="stat"><b>{ar(n_items)}</b><span>مفهومًا في المراجعة</span></div>
  </div>
</header>

<nav class="tabs">
  <button class="on" data-tab="bank">🗂️ بنك الأسئلة</button>
  <button data-tab="exam">📝 وضع الامتحان</button>
  <button data-tab="review">⚡ المراجعة السريعة</button>
  <button data-tab="about">ℹ️ عن الملف</button>
</nav>

<main>
  <section class="panel on" id="bank">
    <div class="toolbar">
      <div class="row">
        <input type="search" id="search" placeholder="🔎 ابحث في الأسئلة والإجابات… (مثال: بلوم، الصدق، معامل التمييز)">
        <select id="topic"><option value="">كل الموضوعات</option></select>
        <select id="src"><option value="">كل المصادر</option></select>
      </div>
      <div class="row" id="axisChips"></div>
      <div class="row">
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
        <label>المحور:</label>
        <select id="exAxis"><option value="">كل المحاور</option></select>
        <label>عدد الأسئلة:</label>
        <select id="exCount">
          <option>10</option><option selected>20</option><option>30</option>
          <option>50</option><option>100</option>
        </select>
        <button class="btn gold" id="exStart">ابدأ الامتحان ▶</button>
      </div>
      <div class="row" style="color:var(--muted);font-size:15px">
        اختر إجابتك لكل سؤال ثم اضغط «تصحيح الامتحان»؛ ستظهر درجتك وتصحيح كل سؤال مع الشرح.
      </div>
    </div>
    <div id="exResult"></div>
    <div id="exList"></div>
    <div class="pager hide" id="exSubmitBar">
      <button class="btn" id="exSubmit">✅ تصحيح الامتحان</button>
      <button class="btn ghost" id="exAgain">↻ امتحان جديد</button>
    </div>
  </section>

  <section class="panel" id="review">
    <div class="toolbar">
      <div class="row">
        <input type="search" id="kbSearch" placeholder="🔎 ابحث في المفاهيم والتعريفات…">
        <button class="btn ghost" id="kbAll">فتح/طي الكل</button>
      </div>
      <div class="row" id="kbChips"></div>
    </div>
    <div id="kbList"></div>
  </section>

  <section class="panel" id="about">
    <div class="toolbar">
      <h2 style="margin-top:0">عن هذا الملف</h2>
      <p>ملف واحد مستقل (لا يحتاج إنترنت) يجمع <b>{ar(len(qs))}</b> سؤالًا في التربوي بإجاباتها النموذجية
      وشرح سبب الإجابة، موزعة على {ar(len(AXES))} محاور و{ar(len(topics))} موضوعًا فرعيًا.</p>
      <p><b>مصادر المحتوى:</b></p>
      <ul>
        <li><b>{ar(n_exam)}</b> سؤالًا من الأسئلة المتداولة في امتحانات مسابقات التعيين (التربوي) بإجاباتها.</li>
        <li><b>{ar(n_sjt)}</b> موقفًا تدريسيًا وتربويًا (أسئلة المواقف) بالإجابة الأفضل مهنيًا وتعليلها.</li>
        <li>باقي الأسئلة مشتقة اشتقاقًا منهجيًا من قاعدة مفاهيم تضم <b>{ar(n_items)}</b> مفهومًا في
        <b>{ar(n_kb)}</b> مجموعة معرفية، على نمط الأسئلة التي تتكرر في المسابقات
        (تعريف ← مصطلح، مصطلح ← تعريف، «يُعد من» و«ليس من»، صاحب النظرية، الترتيب، المواقف التطبيقية)،
        بالإضافة إلى الأسئلة الحسابية في القياس والإحصاء بحلولها خطوة بخطوة.</li>
      </ul>
      <p><b>طريقة الاستخدام:</b> استعمل «بنك الأسئلة» للمذاكرة مع البحث والتصفية،
      و«وضع الامتحان» لاختبار نفسك بزمن مفتوح، و«المراجعة السريعة» لمراجعة المفاهيم قبل الامتحان مباشرة.
      ويمكنك طباعة الملف أو حفظه PDF من المتصفح (Ctrl+P) وستظهر الإجابات والشروح في النسخة المطبوعة.</p>
      <p style="color:var(--muted)">ملاحظة: الأسئلة الحسابية والمفاهيمية مُراجَعة آليًا ويدويًا،
      ومع ذلك يُنصح دائمًا بمراجعة الأسئلة ذات الطابع القانوني على آخر القرارات الوزارية السارية.</p>
    </div>
  </section>
</main>

<footer>بنك أسئلة التربوي — نسخة واحدة مستقلة تعمل دون إنترنت · {ar(len(qs))} سؤالًا بالإجابات والشرح</footer>

<script id="DATA" type="application/json">{data}</script>
<script>
const D = JSON.parse(document.getElementById('DATA').textContent);
const AX = {{}}; D.axes.forEach(a=>AX[a.id]=a);
const LAB = ['أ','ب','ج','د'];
const AD = n => String(n).replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[d]);
const QS = D.q.map((r,i)=>({{i:i,q:r[0],o:r[1],a:r[2],e:r[3],x:r[4],t:D.topics[r[5]],s:D.srcs[r[6]]}}));
let view = QS.slice(), page = 0, per = 25, showAll = false;
let fAxis = '', fTopic = '', fSrc = '', fText = '';

/* ---------- tabs ---------- */
document.querySelectorAll('nav.tabs button').forEach(b=>{{
  b.onclick = ()=>{{
    document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('on'));
    document.getElementById(b.dataset.tab).classList.add('on');
    window.scrollTo({{top:0,behavior:'smooth'}});
  }};
}});

/* ---------- filters ---------- */
const chips = document.getElementById('axisChips');
function chip(label,val,color,cls){{
  const b=document.createElement('button'); b.className='chip'; b.textContent=label;
  b.dataset.v=val; if(color) b.dataset.c=color; return b;
}}
const allChip = chip('كل المحاور','',''); allChip.classList.add('on');
allChip.style.background='#334155'; allChip.style.color='#fff'; allChip.style.borderColor='transparent';
chips.appendChild(allChip);
D.axes.forEach(a=>{{
  const n = QS.filter(q=>q.x===a.id).length;
  const b = chip(a.name+' ('+AD(n)+')', a.id, a.color);
  chips.appendChild(b);
}});
chips.onclick = e=>{{
  const b = e.target.closest('.chip'); if(!b) return;
  [...chips.children].forEach(c=>{{c.classList.remove('on');c.style.background='';c.style.color='';c.style.borderColor='';}});
  b.classList.add('on');
  b.style.background = b.dataset.c || '#334155'; b.style.color='#fff'; b.style.borderColor='transparent';
  fAxis = b.dataset.v; fTopic=''; fillTopics(); apply();
}};

const topicSel = document.getElementById('topic'), srcSel = document.getElementById('src');
function fillTopics(){{
  const set = new Set(QS.filter(q=>!fAxis||q.x===fAxis).map(q=>q.t));
  topicSel.innerHTML = '<option value="">كل الموضوعات</option>' +
    [...set].sort().map(t=>`<option>${{t}}</option>`).join('');
}}
srcSel.innerHTML = '<option value="">كل المصادر</option>' +
  D.srcs.map(s=>`<option>${{s}}</option>`).join('');
fillTopics();
topicSel.onchange = ()=>{{fTopic=topicSel.value; apply();}};
srcSel.onchange = ()=>{{fSrc=srcSel.value; apply();}};
let tmr; document.getElementById('search').oninput = e=>{{
  clearTimeout(tmr); tmr=setTimeout(()=>{{fText=e.target.value.trim(); apply();}},180);
}};
document.getElementById('toggleAll').onclick = e=>{{
  showAll = !showAll;
  e.target.textContent = showAll ? '🙈 إخفاء كل الإجابات' : '👁️ إظهار كل الإجابات';
  render();
}};
document.getElementById('shuffle').onclick = ()=>{{
  for(let i=view.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[view[i],view[j]]=[view[j],view[i]];}}
  page=0; render();
}};

function norm(s){{return s.replace(/[\\u064B-\\u0652\\u0640]/g,'').replace(/[إأآا]/g,'ا').replace(/[ىي]/g,'ي').replace(/ة/g,'ه');}}
function apply(){{
  const t = norm(fText);
  view = QS.filter(q=>{{
    if(fAxis && q.x!==fAxis) return false;
    if(fTopic && q.t!==fTopic) return false;
    if(fSrc && q.s!==fSrc) return false;
    if(t && !norm(q.q+' '+q.o.join(' ')+' '+q.e).includes(t)) return false;
    return true;
  }});
  page = 0; render();
}}

/* ---------- render bank ---------- */
function card(q, idx){{
  const ax = AX[q.x];
  const el = document.createElement('div');
  el.className='q'; el.style.borderRightColor = ax.color;
  el.innerHTML =
   `<div class="meta">
      <span class="tag" style="background:${{ax.color}}">${{ax.name}}</span>
      <span class="tag soft">${{q.t}}</span>
      <span class="tag src">${{q.s}}</span>
      <span style="margin-inline-start:auto">#${{AD(idx)}}</span>
    </div>
    <div class="qtext">${{q.q}}</div>
    <div class="opts">${{q.o.map((o,i)=>
      `<div class="opt" data-i="${{i}}"><span class="lab">${{LAB[i]}}</span><span>${{o}}</span></div>`).join('')}}</div>
    <div class="exp"><b>الإجابة: ${{LAB[q.a]}}) ${{q.o[q.a]}}</b><br>${{q.e}}</div>`;
  const exp = el.querySelector('.exp');
  el.querySelectorAll('.opt').forEach(op=>{{
    op.onclick = ()=>{{
      const i = +op.dataset.i;
      el.querySelectorAll('.opt').forEach((o,j)=>{{
        o.classList.toggle('right', j===q.a);
        if(j===i && i!==q.a) o.classList.add('wrong');
      }});
      exp.classList.add('on');
    }};
  }});
  if(showAll){{
    exp.classList.add('on');
    el.querySelectorAll('.opt')[q.a].classList.add('right');
  }}
  return el;
}}
function render(){{
  const list = document.getElementById('list'); list.innerHTML='';
  const total = view.length, pages = Math.max(1, Math.ceil(total/per));
  if(page>=pages) page = pages-1;
  const start = page*per;
  view.slice(start, start+per).forEach((q,k)=>list.appendChild(card(q, start+k+1)));
  document.getElementById('count').textContent = total ? `${{AD(total)}} سؤالًا — صفحة ${{AD(page+1)}} من ${{AD(pages)}}` : 'لا توجد نتائج';
  const pg = document.getElementById('pager'); pg.innerHTML='';
  const mk=(txt,fn,dis)=>{{const b=document.createElement('button');b.textContent=txt;b.disabled=!!dis;b.onclick=fn;pg.appendChild(b);}};
  mk('« الأولى',()=>{{page=0;render();scrollTop();}},page===0);
  mk('السابق',()=>{{page--;render();scrollTop();}},page===0);
  const sel=document.createElement('select');
  for(let i=0;i<pages;i++){{const o=document.createElement('option');o.value=i;o.textContent='صفحة '+AD(i+1);if(i===page)o.selected=true;sel.appendChild(o);}}
  sel.onchange=()=>{{page=+sel.value;render();scrollTop();}}; pg.appendChild(sel);
  mk('التالي',()=>{{page++;render();scrollTop();}},page>=pages-1);
  mk('الأخيرة »',()=>{{page=pages-1;render();scrollTop();}},page>=pages-1);
  const psel=document.createElement('select');
  [10,25,50,100].forEach(v=>{{const o=document.createElement('option');o.value=v;o.textContent=AD(v)+' بالصفحة';if(v===per)o.selected=true;psel.appendChild(o);}});
  psel.onchange=()=>{{per=+psel.value;page=0;render();}}; pg.appendChild(psel);
}}
function scrollTop(){{document.getElementById('bank').scrollIntoView({{behavior:'smooth'}});}}

/* ---------- exam ---------- */
const exAxis = document.getElementById('exAxis');
exAxis.innerHTML = '<option value="">كل المحاور</option>' +
  D.axes.map(a=>`<option value="${{a.id}}">${{a.name}}</option>`).join('');
let exam = [], answers = {{}};
document.getElementById('exStart').onclick = ()=>{{
  const ax = exAxis.value, n = +document.getElementById('exCount').value;
  let pool = QS.filter(q=>!ax||q.x===ax);
  pool = pool.slice();
  for(let i=pool.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]];}}
  exam = pool.slice(0,n); answers = {{}};
  document.getElementById('exResult').innerHTML='';
  document.getElementById('exSubmitBar').classList.remove('hide');
  const box = document.getElementById('exList'); box.innerHTML='';
  exam.forEach((q,k)=>{{
    const ax2 = AX[q.x];
    const el=document.createElement('div'); el.className='q'; el.style.borderRightColor=ax2.color;
    el.innerHTML = `<div class="meta"><span class="tag" style="background:${{ax2.color}}">${{ax2.name}}</span>
      <span class="tag soft">${{q.t}}</span><span style="margin-inline-start:auto">سؤال ${{AD(k+1)}}</span></div>
      <div class="qtext">${{q.q}}</div>
      <div class="opts">${{q.o.map((o,i)=>`<div class="opt" data-i="${{i}}"><span class="lab">${{LAB[i]}}</span><span>${{o}}</span></div>`).join('')}}</div>
      <div class="exp"></div>`;
    el.querySelectorAll('.opt').forEach(op=>{{
      op.onclick=()=>{{
        if(el.dataset.done) return;
        answers[k] = +op.dataset.i;
        el.querySelectorAll('.opt').forEach(o=>o.style.outline='');
        op.style.outline='3px solid #6366f1';
      }};
    }});
    box.appendChild(el);
  }});
  box.scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('exSubmit').onclick = ()=>{{
  let right=0;
  const cards = document.querySelectorAll('#exList .q');
  exam.forEach((q,k)=>{{
    const el = cards[k]; el.dataset.done='1';
    const pick = answers[k];
    if(pick===q.a) right++;
    el.querySelectorAll('.opt').forEach((o,j)=>{{
      o.style.outline='';
      if(j===q.a) o.classList.add('right');
      if(j===pick && pick!==q.a) o.classList.add('wrong');
    }});
    const exp = el.querySelector('.exp');
    exp.innerHTML = `<b>الإجابة الصحيحة: ${{LAB[q.a]}}) ${{q.o[q.a]}}</b><br>${{q.e}}`;
    exp.classList.add('on');
  }});
  const pct = Math.round(right/exam.length*100);
  const msg = pct>=85?'ممتاز 👏':pct>=70?'جيد جدًا ✅':pct>=50?'تحتاج مراجعة 📖':'راجع المحور كاملًا 💪';
  document.getElementById('exResult').innerHTML =
    `<div class="sc"><div class="big" style="color:${{pct>=70?'#16a34a':pct>=50?'#f59e0b':'#dc2626'}}">${{AD(pct)}}٪</div>
     <div>أجبت إجابة صحيحة عن <b>${{AD(right)}}</b> من <b>${{AD(exam.length)}}</b> سؤالًا — ${{msg}}</div></div>`;
  document.getElementById('exResult').scrollIntoView({{behavior:'smooth'}});
}};
document.getElementById('exAgain').onclick = ()=>document.getElementById('exStart').click();

/* ---------- review ---------- */
const kbList = document.getElementById('kbList'), kbChips = document.getElementById('kbChips');
let kbAxis='';
const kbAll = document.createElement('button'); kbAll.className='chip on'; kbAll.textContent='كل المحاور';
kbAll.style.background='#334155'; kbAll.style.color='#fff'; kbAll.dataset.v=''; kbChips.appendChild(kbAll);
D.axes.forEach(a=>{{
  const n = D.kb.filter(g=>g.axis===a.id).length; if(!n) return;
  const b=document.createElement('button'); b.className='chip'; b.textContent=a.name; b.dataset.v=a.id; b.dataset.c=a.color;
  kbChips.appendChild(b);
}});
kbChips.onclick = e=>{{
  const b=e.target.closest('.chip'); if(!b) return;
  [...kbChips.children].forEach(c=>{{c.classList.remove('on');c.style.background='';c.style.color='';}});
  b.classList.add('on'); b.style.background=b.dataset.c||'#334155'; b.style.color='#fff';
  kbAxis=b.dataset.v; kbRender();
}};
document.getElementById('kbSearch').oninput = ()=>kbRender();
document.getElementById('kbAll').onclick = ()=>{{
  const any = kbList.querySelector('.kbcard:not(.open)');
  kbList.querySelectorAll('.kbcard').forEach(c=>c.classList.toggle('open', !!any));
}};
function kbRender(){{
  const t = norm(document.getElementById('kbSearch').value.trim());
  kbList.innerHTML='';
  D.kb.forEach(g=>{{
    if(kbAxis && g.axis!==kbAxis) return;
    const items = t ? g.items.filter(it=>norm(it[0]+' '+it[1]+' '+it[2]).includes(t)) : g.items;
    if(!items.length) return;
    const ax = AX[g.axis];
    const c = document.createElement('div'); c.className='kbcard'+(t?' open':'');
    c.innerHTML = `<h3 style="background:${{ax.color}}">${{g.cat}}<span style="font-size:14px;opacity:.9">${{ax.name}} · ${{AD(items.length)}}</span></h3>
      <table>${{items.map(it=>`<tr><td class="n">${{it[0]}}${{it[2]?' <span style="color:#fde68a;background:#92400e;border-radius:6px;padding:1px 6px;font-size:12px">'+it[2]+'</span>':''}}</td>
      <td>${{it[1]}}${{it[3]?'<span class="ex">🧩 مثال: '+it[3]+'</span>':''}}</td></tr>`).join('')}}</table>
      ${{g.note?`<div class="note">📌 ${{g.note}}</div>`:''}}`;
    c.querySelector('h3').onclick = ()=>c.classList.toggle('open');
    kbList.appendChild(c);
  }});
  if(!kbList.children.length) kbList.innerHTML='<p style="text-align:center;color:#64748b">لا توجد نتائج</p>';
}}
kbRender();
render();
</script>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    kb = os.path.getsize(OUT) / 1024
    print(f"✅ {OUT}  ({kb:.0f} KB)  —  {len(qs)} سؤالًا، {len(topics)} موضوعًا، "
          f"{n_items} مفهومًا في {n_kb} مجموعة")
    return len(qs)


if __name__ == "__main__":
    build()
