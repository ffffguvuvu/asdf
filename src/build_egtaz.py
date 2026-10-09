# -*- coding: utf-8 -*-
"""يبني صفحة egtaz-arabic-guide.html من وحدات البيانات في egtaz/."""
import json, os, sys, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "egtaz"))
sys.path.insert(0, HERE)

OUT = os.path.join(os.path.dirname(HERE), "egtaz-arabic-guide.html")

MODULES = [
    ("nahw", "data_nahw"),
    ("sarf", "data_sarf"),
    ("imla", "data_imla"),
    ("bala", "data_bala"),
    ("arud", "data_arud"),
    ("adab", "data_adab"),
    ("lugh", "data_lugha"),
    ("turq", "data_turuq"),
    ("mnsa", "data_mansa"),
    ("ex1", "data_ex1"),
    ("ex2", "data_ex2"),
    ("ex3", "data_ex3"),
    ("ex4", "data_ex4"),
    ("hsam", "data_hsam"),
]

# ملفات مجلد «تخصص عربي» في Google Drive كما ظهرت في فهرس المجلد
FILES = [
    ("360 سؤال في اللغة العربية", "بنك أسئلة عام",
     "تعذّر — جُرّبت ١٥ صيغة رابط فلم يستجب"),
    ("أسئلة تخصص لغة عربية لمسابقة وزارة التربية والتعليم", "أسئلة الجهاز المركزي", "قُرئ كاملًا"),
    ("الأسئلة التي وردت لتخصص اللغة العربية — نهائي", "أسئلة وردت فعلًا", "قُرئ كاملًا"),
    ("أساسيات في قواعد الإملاء (المرشد الإملائي)", "مرجع إملاء", "قُرئ كاملًا"),
    ("اللغة العربية تخصص للجميع", "بنك أسئلة", "قُرئ"),
    ("تسريبات الحسام — أحدث الأسئلة في تخصص اللغة العربية (3)", "بلاغة وعروض وأدب", "قُرئ"),
    ("تسريبات الحسام في العربية (خاص بتخصص اللغة العربية)", "أسئلة تخصص",
     "فُكّ بتصوير الصفحات — ١٠٠ صفحة، قُرئ منها ٣ حتى الآن"),
    ("تسريبات الحسام في اللغة العربية (خاص بالتخصص)", "أسئلة تخصص",
     "هو الملفّ السابق نفسه — وقد قُرئ منه بالتصوير لا بالنصّ"),
    ("تسريبات الحسام في اللغة العربية (عربي عام لجميع التخصصات)", "عربي عام",
     "فُتح أخيرًا وقُرئ كاملًا — ٢٩ صفحة ≈ ٢٠٠ سؤال ← الاختبار الثالث"),
    ("طرق تدريس اللغة العربية", "مرجع طرق تدريس", "قُرئ كاملًا"),
    ("طرق تدريس اللغة العربية — 1", "مرجع طرق تدريس", "نسخة مكررة"),
    ("مراجعة ما قبل الامتحان — أحدث أسئلة وردت بالفعل", "مراجعة",
     "قُرئ أخيرًا — جدارات وذكاء وحاسب ومعلومات عامة، لا تخصص"),
    ("أسئلة معلم فصل", "تخصص آخر", "خارج تخصص اللغة العربية"),
    ("أحدث أسئلة للحاسب الآلي — الجزء الثاني", "حاسب آلي", "خارج تخصص اللغة العربية"),
]

DRIVE = "https://drive.google.com/drive/folders/1YvqHviSNCHqECMZ0aslM0tJ5_1oKYnn3"

_HARAKAT = re.compile(r"[\u064B-\u0652\u0670\u0640]")


def nrm(s):
    s = _HARAKAT.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه"),
                 ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    return re.sub(r"[^\w\s]", " ", s)


def toks(s):
    return set(w for w in nrm(s).split() if len(w) > 2)


_IRAB = re.compile(r"(مرفوع|منصوب|مجرور|مجزوم|في محل|مبني على)")
_NAME = re.compile(r"(^|\s)(ابن|بن|أبو|أبي|امرؤ|امرئ)(\s|$)")

# سُلَّم التنازل: إن لم تكفِ أمثالُ الصنف جُرِّبت الأصناف المجاورة بالترتيب
_NEAR = {
    "num":  ["num", "w1", "w3"],
    "name": ["name", "w3", "w1"],
    "irab": ["irab", "w3", "p"],
    "w1":   ["w1", "w3", "num"],
    "w3":   ["w3", "w1", "name", "irab"],
    "p":    ["p", "irab", "w3", "p2"],
    "p2":   ["p2", "p", "L"],
    "L":    ["L", "p2", "p"],
}


def cls(s):
    """يصنّف الإجابة حتى تُختار بدائلُها من جنسها، فلا يُفضح الصواب بالشكل."""
    if re.search(r"[0-9\u0660-\u0669]", s):
        return "num"
    n = len(s.split())
    if n <= 4 and _NAME.search(s):
        return "name"
    if _IRAB.search(s):
        return "irab"
    if n == 1:
        return "w1"
    if n <= 3:
        return "w3"
    if len(s) <= 45:
        return "p"
    if len(s) <= 95:
        return "p2"
    return "L"


def inline_choices(q, ans):
    """إن كان السؤال يسرد خياراته بنفسه («اختر: أ / ب / ج») فالبدائل منه أولى."""
    if "/" not in q:
        return []
    tail = re.split(r"[:：]", q)[-1]
    parts = [p.strip(" .،؟…") for p in tail.split("/")]
    parts = [p for p in parts if 1 < len(p) <= 60]
    if len(parts) < 3:
        return []
    a_n = nrm(ans).strip()
    hit = [p for p in parts if nrm(p).strip() in a_n or a_n in nrm(p).strip()]
    if not hit:
        return []
    out, seen = [], {a_n}
    for p in parts:
        k = nrm(p).strip()
        if k in seen:            # الفروق الدقيقة مقصودة هنا، فلا يُستبعد المتشابه
            continue
        seen.add(k)
        out.append(p)
    return out[:3]


def distractors(ans, pool, seed, qtext="", prefer=()):
    """يختار ثلاثة بدائل معقولة من إجابات القسم نفسه، من صنف الإجابة ذاته."""
    a_n = nrm(ans).strip()
    a_t = toks(ans)
    q_t = toks(qtext)
    la = len(ans)
    a_c = cls(ans)
    buckets = {}
    for other, oq in pool:
        o_n = nrm(other).strip()
        if o_n == a_n:
            continue
        if o_n in a_n or a_n in o_n:      # يمنع البديل المتضمَّن فيكون ملتبسًا
            continue
        ov = len(a_t & toks(other))
        if a_t and ov >= max(2, len(a_t) * 0.6):  # قريب جدًّا ⇒ قد يصير صحيحًا
            continue
        if abs(len(other) - la) > max(40, la * 1.6):   # تفاوت الطول يفضح الصواب
            continue
        aff = len(q_t & toks(oq))          # قرب الموضوع: سؤالان متجاوران موضوعًا
        score = 2.0 * ov + 1.4 * aff - abs(len(other) - la) / 14.0
        buckets.setdefault(cls(other), []).append((score, o_n, other))

    rng = random.Random(seed)
    out, seen = [], set()
    for p in prefer:                      # خيارات مذكورة في نصّ السؤال تُقدَّم
        k = nrm(p).strip()
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
        if len(out) == 3:
            return out
    for c in _NEAR.get(a_c, [a_c]):
        lst = buckets.get(c, [])
        if not lst:
            continue
        lst.sort(key=lambda x: -x[0])
        top = lst[:18]
        rng.shuffle(top)
        for _, o_n, other in top:
            if o_n in seen:
                continue
            seen.add(o_n)
            out.append(other)
            if len(out) == 3:
                return out
    return []


def main():
    import tanbih, tanbih_b, tanbih_c, tanbih_d
    TN = dict(tanbih.T)
    TN.update(tanbih_b.T2)
    TN.update(tanbih_c.T3)
    TN.update(tanbih_d.T4)

    secs, total_q, total_r, exam_n = [], 0, 0, 0
    used_tn = set()

    for code, mod in MODULES:
        m = __import__(mod)
        answers = [(b, a) for (a, b, _c) in m.QS]
        qs = []
        for i, (q, a, e) in enumerate(m.QS):
            d = distractors(a, answers, seed=(abs(hash((code, i))) % 999983),
                            qtext=q, prefer=inline_choices(q, a))
            rec = {"q": q, "a": a, "e": e}
            if d:
                rec["d"] = d
                exam_n += 1
            qs.append(rec)
        rs = []
        for (t, b) in m.RULES:
            extra = TN.get(t, "")
            if extra:
                used_tn.add(t)
            rs.append({"t": t, "b": b + extra})
        total_q += len(qs)
        total_r += len(rs)
        secs.append({"c": code, "n": m.NAME, "q": qs, "r": rs})

    data = {"s": secs, "f": [{"n": a, "k": b, "st": c} for (a, b, c) in FILES]}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    page = (TPL.replace("__DATA__", blob)
               .replace("__NQ__", str(total_q))
               .replace("__NR__", str(total_r))
               .replace("__NS__", str(len(secs)))
               .replace("__NX__", str(exam_n))
               .replace("__DRIVE__", DRIVE))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("WROTE", OUT, os.path.getsize(OUT), "bytes")
    print("sections", len(secs), "| questions", total_q, "| rules", total_r,
          "| exam-ready", exam_n, "| tanbih used", len(used_tn))
    for s in secs:
        ex = sum(1 for q in s["q"] if "d" in q)
        print("   %-28s %3d سؤال / %2d قاعدة / %3d صالح للاختبار"
              % (s["n"], len(s["q"]), len(s["r"]), ex))


TPL = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ملفات المسابقة — تخصص لغة عربية: حلّ الأسئلة وشرح القواعد ووضع الاختبار</title>
<style>
:root{--bg:#f4f6fb;--card:#fff;--ink:#17202e;--mut:#5d6b84;--pri:#1d5fa8;--pri2:#e8f0fb;
--ok:#0f7a4d;--ok2:#e4f5ec;--wr:#b3261e;--wr2:#fdeceb;--line:#dfe5f0;--acc:#8b5cf6}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI","Tahoma",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.95}
header{background:linear-gradient(135deg,#123a6b,#1d5fa8 55%,#2a7fd4);color:#fff;padding:26px 18px 20px}
.wrap{max-width:1120px;margin:0 auto;padding:0 14px}
h1{margin:0 0 6px;font-size:1.5rem;font-weight:800}
.sub{opacity:.93;font-size:.93rem;margin-bottom:12px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:4px 11px;border-radius:999px;font-size:.82rem}
nav{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:40;
box-shadow:0 2px 10px rgba(16,30,60,.07)}
.tabs{display:flex;gap:4px;overflow-x:auto;padding:8px 14px;max-width:1120px;margin:0 auto;scrollbar-width:thin}
.tab{flex:0 0 auto;border:1px solid var(--line);background:#fbfcfe;color:var(--mut);padding:7px 15px;
border-radius:9px;cursor:pointer;font-size:.9rem;font-family:inherit;white-space:nowrap;font-weight:600}
.tab:hover{background:var(--pri2);color:var(--pri)}
.tab.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.tab.xm{background:#f3ecff;color:#6b36d6;border-color:#dccdfa}
.tab.xm.on{background:#6b36d6;color:#fff;border-color:#6b36d6}
main{padding:18px 0 60px}
.panel{display:none}.panel.on{display:block}
.card{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:17px 19px;margin:0 0 14px;
box-shadow:0 1px 3px rgba(16,30,60,.05)}
.card h3{margin:0 0 10px;font-size:1.08rem;color:var(--pri);font-weight:800;border-bottom:2px solid var(--pri2);padding-bottom:7px}
.card p{margin:.55em 0}
.card ul,.card ol{margin:.5em 0;padding-inline-start:1.5em}
.card li{margin:.3em 0}
table{width:100%;border-collapse:collapse;margin:.8em 0;font-size:.9rem}
th,td{border:1px solid var(--line);padding:7px 9px;text-align:right;vertical-align:top}
th{background:var(--pri2);color:var(--pri);font-weight:700}
tr:nth-child(even) td{background:#fafbfe}
.tnb{margin-top:13px;background:#fff8ee;border:1px solid #f6d8a8;border-right:4px solid #dd8c16;
border-radius:10px;padding:11px 15px}
.tnb h4{margin:0 0 5px;font-size:.94rem;color:#9a5b06;font-weight:800}
.tnb ol{margin:.3em 0;padding-inline-start:1.35em}
.tnb li{margin:.4em 0;font-size:.93rem;line-height:1.85}
.tnb .src{margin:.7em 0 0;font-size:.82rem;color:#8a6a3a;border-top:1px dashed #ecd3a8;padding-top:6px}
.toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin-bottom:14px}
input[type=search],select{font-family:inherit;font-size:.92rem;padding:8px 12px;border:1px solid var(--line);
border-radius:9px;background:#fff;color:var(--ink)}
input[type=search]{flex:1;min-width:190px}
.btn{font-family:inherit;font-size:.88rem;padding:8px 14px;border:1px solid var(--line);background:#fff;
border-radius:9px;cursor:pointer;color:var(--mut);font-weight:600}
.btn:hover{background:var(--pri2);color:var(--pri);border-color:var(--pri)}
.btn.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.btn.go{background:#6b36d6;color:#fff;border-color:#6b36d6}
.btn.go:hover{background:#5a2bb8;color:#fff}
.cnt{color:var(--mut);font-size:.86rem}
.q{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--pri);border-radius:11px;
padding:14px 17px;margin-bottom:11px}
.q .num{color:var(--acc);font-weight:800;font-size:.8rem;letter-spacing:.4px}
.qt{font-weight:700;margin:5px 0 9px;font-size:1rem}
.ans{background:var(--ok2);border:1px solid #bfe6d2;border-radius:8px;padding:8px 12px;margin-bottom:8px;
color:var(--ok);font-weight:700;font-size:.95rem}
.ans::before{content:"الإجابة: ";font-weight:800;opacity:.75}
.exp{color:#36425a;font-size:.93rem;background:#f8f9fc;border-radius:8px;padding:9px 12px;border:1px dashed var(--line)}
.exp::before{content:"الشرح — ";font-weight:800;color:var(--pri)}
.none{text-align:center;color:var(--mut);padding:34px;background:var(--card);border-radius:12px;border:1px dashed var(--line)}
.lead{background:#fffaf0;border:1px solid #f0e0bd;border-radius:11px;padding:13px 17px;margin-bottom:15px;font-size:.93rem}
.lead b{color:#92610b}
.fl{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;border:1px solid var(--line);
border-radius:10px;padding:10px 13px;margin-bottom:8px;background:var(--card);flex-wrap:wrap}
.fl .nm{font-weight:700;font-size:.93rem;flex:1;min-width:220px}
.fl .kd{font-size:.8rem;color:var(--pri);background:var(--pri2);padding:2px 9px;border-radius:999px}
.fl .st{font-size:.8rem;color:var(--mut)}
.ok{color:var(--ok)!important;font-weight:700}
.bad{color:var(--wr)!important}
a{color:var(--pri)}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0}
.g div{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:12px;text-align:center}
.g b{display:block;font-size:1.45rem;color:var(--pri);font-weight:800}
.g span{font-size:.81rem;color:var(--mut)}
mark{background:#fff3a3;padding:0 2px;border-radius:3px}
/* ---- وضع الاختبار ---- */
.exbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;
background:#2b1a52;color:#fff;border-radius:11px;padding:10px 16px;margin-bottom:14px;
position:sticky;top:53px;z-index:30}
.exbar .pill{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.26);
padding:3px 12px;border-radius:999px;font-size:.85rem;font-weight:700}
.exq{background:var(--card);border:1px solid var(--line);border-right:4px solid #6b36d6;border-radius:11px;
padding:14px 17px;margin-bottom:11px}
.exq .num{color:#6b36d6;font-weight:800;font-size:.8rem}
.opt{display:block;border:1px solid var(--line);border-radius:9px;padding:9px 13px;margin:7px 0;
cursor:pointer;background:#fff;font-size:.95rem;transition:background .12s}
.opt:hover{background:#f3ecff}
.opt input{margin-inline-end:9px;vertical-align:middle}
.opt.sel{border-color:#6b36d6;background:#f3ecff}
.opt.good{border-color:#0f7a4d;background:var(--ok2);font-weight:700}
.opt.bad{border-color:var(--wr);background:var(--wr2)}
.verdict{font-weight:800;font-size:.88rem;margin:8px 0 4px}
.verdict.y{color:var(--ok)}.verdict.n{color:var(--wr)}
.score{background:linear-gradient(135deg,#2b1a52,#6b36d6);color:#fff;border-radius:13px;
padding:20px;margin-bottom:16px;text-align:center}
.score .pc{font-size:2.6rem;font-weight:800;display:block;line-height:1.2}
.score .gr{font-size:1.05rem;font-weight:700;opacity:.95}
.score .dt{font-size:.88rem;opacity:.85;margin-top:6px}
@media print{nav,.toolbar,.exbar,header .chips{display:none}.panel{display:block!important}
.card,.q,.exq{break-inside:avoid;box-shadow:none}body{background:#fff}}
</style>
</head>
<body>
<header><div class="wrap">
<h1>ملفات المسابقة — تخصص لغة عربية</h1>
<div class="sub">حلّ كامل لأسئلة ملفات المجلد، وشرح مفصّل للقواعد بتنبيهات كتب النحو، ووضع اختبار مصحَّح</div>
<div class="chips">
<span class="chip">__NQ__ سؤالًا محلولًا</span>
<span class="chip">__NR__ قاعدة مشروحة</span>
<span class="chip">__NS__ فروع</span>
<span class="chip">__NX__ سؤالًا في وضع الاختبار</span>
</div></div></header>

<nav><div class="tabs" id="tabs"></div></nav>

<main class="wrap">
<div id="panels"></div>
</main>

<script id="DATA" type="application/json">__DATA__</script>
<script>
(function(){
var D=JSON.parse(document.getElementById('DATA').textContent);
var AR='٠١٢٣٤٥٦٧٨٩';
function ad(n){return String(n).replace(/[0-9]/g,function(d){return AR[+d]});}
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function norm(s){return s.replace(/[\u064B-\u0652\u0670]/g,'').replace(/[أإآ]/g,'ا')
  .replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/ؤ/g,'و').replace(/ئ/g,'ي');}

var tabs=document.getElementById('tabs'), panels=document.getElementById('panels');

function mkTab(id,label,cls){
  var b=document.createElement('button');
  b.className='tab'+(cls?' '+cls:''); b.setAttribute('data-tab',id); b.textContent=label;
  tabs.appendChild(b); return b;
}
function mkPanel(id){
  var d=document.createElement('section');
  d.className='panel'; d.id='p-'+id; panels.appendChild(d); return d;
}

/* ---------- تبويب الملفات ---------- */
mkTab('files','الملفات');
var pf=mkPanel('files');
var okc=0; D.f.forEach(function(f){ if(/قُرئ/.test(f.st)) okc++; });
pf.innerHTML='<div class="lead"><b>ماذا في هذا التبويب؟</b> جردٌ لمحتويات مجلد '+
 '<a href="__DRIVE__" target="_blank" rel="noopener">«تخصص عربي»</a> المرتبط من صفحة المسابقة، '+
 'وبيانُ ما أمكن قراءته منها وما تعذّر. وقد استُخرجت كل الأسئلة والقواعد في التبويبات التالية '+
 'من الملفات المقروءة، وصيغت الحلول والشروح صياغةً أصليةً لا نقلًا حرفيًّا.</div>'+
 '<div class="g"><div><b>'+ad(D.f.length)+'</b><span>ملفًا في المجلد</span></div>'+
 '<div><b>'+ad(okc)+'</b><span>ملفًا قُرئ</span></div>'+
 '<div><b>'+ad(__NQ__)+'</b><span>سؤالًا محلولًا</span></div>'+
 '<div><b>'+ad(__NR__)+'</b><span>قاعدة مشروحة</span></div></div>'+
 '<div class="card"><h3>فهرس ملفات المجلد</h3><div id="flist"></div></div>';
var fl=document.getElementById('flist');
D.f.forEach(function(f){
  var ok=/قُرئ/.test(f.st), bad=/تالف|تعذّر|تعذر/.test(f.st);
  var d=document.createElement('div'); d.className='fl';
  d.innerHTML='<span class="nm">'+esc(f.n)+'</span>'+
    '<span class="kd">'+esc(f.k)+'</span>'+
    '<span class="st'+(ok?' ok':'')+(bad?' bad':'')+'">'+esc(f.st)+'</span>';
  fl.appendChild(d);
});

/* ---------- تبويب وضع الاختبار (يُملأ بعد بناء الفروع) ---------- */
mkTab('exam','وضع الاختبار','xm');
var px=mkPanel('exam');

/* ---------- تبويبات الفروع ---------- */
D.s.forEach(function(s){
  mkTab(s.c,s.n);
  var p=mkPanel(s.c);
  p.innerHTML=
   '<div class="toolbar">'+
   '<input type="search" id="q-'+s.c+'" placeholder="ابحث في '+esc(s.n)+'…">'+
   '<button class="btn on" data-v="all" id="va-'+s.c+'">الكل</button>'+
   '<button class="btn" data-v="rules" id="vr-'+s.c+'">القواعد ('+ad(s.r.length)+')</button>'+
   '<button class="btn" data-v="qs" id="vq-'+s.c+'">الأسئلة ('+ad(s.q.length)+')</button>'+
   '<span class="cnt" id="c-'+s.c+'"></span></div>'+
   '<div id="r-'+s.c+'"></div><div id="l-'+s.c+'"></div>'+
   '<div class="none" id="n-'+s.c+'" style="display:none">لا توجد نتائج مطابقة.</div>';

  var rbox=document.getElementById('r-'+s.c), lbox=document.getElementById('l-'+s.c);
  s.r.forEach(function(r){
    var c=document.createElement('div'); c.className='card rule';
    c.innerHTML='<h3>'+esc(r.t)+'</h3>'+r.b;
    c.setAttribute('data-k',norm(r.t+' '+r.b.replace(/<[^>]+>/g,' ')));
    rbox.appendChild(c);
  });
  s.q.forEach(function(q,i){
    var c=document.createElement('div'); c.className='q';
    c.innerHTML='<div class="num">سؤال '+ad(i+1)+'</div>'+
      '<div class="qt">'+esc(q.q)+'</div>'+
      '<div class="ans">'+esc(q.a)+'</div>'+
      '<div class="exp">'+esc(q.e)+'</div>';
    c.setAttribute('data-k',norm(q.q+' '+q.a+' '+q.e));
    lbox.appendChild(c);
  });

  var mode='all';
  function render(){
    var term=norm(document.getElementById('q-'+s.c).value.trim());
    var rs=rbox.querySelectorAll('.rule'), qq=lbox.querySelectorAll('.q');
    var nr=0,nq=0,k;
    for(k=0;k<rs.length;k++){
      var vis=(mode!=='qs')&&(!term||rs[k].getAttribute('data-k').indexOf(term)>=0);
      rs[k].style.display=vis?'':'none'; if(vis)nr++;
    }
    for(k=0;k<qq.length;k++){
      var v2=(mode!=='rules')&&(!term||qq[k].getAttribute('data-k').indexOf(term)>=0);
      qq[k].style.display=v2?'':'none'; if(v2)nq++;
    }
    document.getElementById('c-'+s.c).textContent='ظاهر: '+ad(nr)+' قاعدة · '+ad(nq)+' سؤال';
    document.getElementById('n-'+s.c).style.display=(nr+nq===0)?'':'none';
  }
  document.getElementById('q-'+s.c).addEventListener('input',render);
  ['va','vr','vq'].forEach(function(pre){
    var b=document.getElementById(pre+'-'+s.c);
    b.addEventListener('click',function(){
      mode=b.getAttribute('data-v');
      ['va','vr','vq'].forEach(function(o){
        document.getElementById(o+'-'+s.c).classList.toggle('on',o===pre);});
      render();
    });
  });
  render();
});

/* ================= وضع الاختبار ================= */
var POOL=[];
D.s.forEach(function(s){
  s.q.forEach(function(q){ if(q.d&&q.d.length===3) POOL.push({s:s.c,n:s.n,q:q.q,a:q.a,e:q.e,d:q.d}); });
});

var secOpts='<option value="*">كل الفروع ('+ad(POOL.length)+' سؤالًا)</option>';
D.s.forEach(function(s){
  var c=0; s.q.forEach(function(q){ if(q.d&&q.d.length===3) c++; });
  if(c>=5) secOpts+='<option value="'+s.c+'">'+esc(s.n)+' ('+ad(c)+')</option>';
});

px.innerHTML=
 '<div class="lead"><b>كيف يعمل وضع الاختبار؟</b> اختر الفرع وعدد الأسئلة ثم اضغط «ابدأ الاختبار». '+
 'تُسحب الأسئلة عشوائيًّا في كل مرة، وتُخلط البدائل الأربعة، ويعمل المؤقّت تلقائيًّا. '+
 'وعند التصحيح تُحتسب الدرجة والنسبة والتقدير، ويُعرض تحت كل سؤال وجهُ الصواب وسببه. '+
 'والبدائل مولَّدة من إجابات الفرع نفسه حتى تكون قريبةً مُلبِسة كما في الاختبار الحقيقي.</div>'+
 '<div class="toolbar">'+
 '<label class="cnt" for="ex-sec">الفرع:</label><select id="ex-sec">'+secOpts+'</select>'+
 '<label class="cnt" for="ex-n">عدد الأسئلة:</label>'+
 '<select id="ex-n"><option>10</option><option selected>20</option><option>30</option>'+
 '<option>50</option></select>'+
 '<button class="btn go" id="ex-go">ابدأ الاختبار</button>'+
 '<button class="btn" id="ex-again" style="display:none">اختبار جديد</button></div>'+
 '<div id="ex-live"></div>';

var live=document.getElementById('ex-live');
var exT0=0, exTimer=null, exItems=[], exDone=false;

function two(n){return (n<10?'0':'')+n;}
function tick(){
  var el=document.getElementById('ex-clock'); if(!el) return;
  var s=Math.floor((Date.now()-exT0)/1000);
  el.textContent=ad(two(Math.floor(s/60))+':'+two(s%60));
}
function shuffle(arr,rnd){
  var i,j,t;
  for(i=arr.length-1;i>0;i--){ j=Math.floor(rnd()*(i+1)); t=arr[i];arr[i]=arr[j];arr[j]=t; }
  return arr;
}
function answered(){
  return live.querySelectorAll('input[type=radio]:checked').length;
}
function refreshProg(){
  var el=document.getElementById('ex-prog');
  if(el) el.textContent='أجبتَ عن '+ad(answered())+' من '+ad(exItems.length);
}

function startExam(){
  var code=document.getElementById('ex-sec').value;
  var want=parseInt(document.getElementById('ex-n').value,10);
  var src=POOL.filter(function(p){ return code==='*'||p.s===code; });
  var seed=Date.now()%2147483647;
  var rnd=function(){ seed=(seed*16807)%2147483647; return (seed-1)/2147483646; };
  var picked=shuffle(src.slice(),rnd).slice(0,Math.min(want,src.length));
  exItems=picked.map(function(p){
    var opts=shuffle([p.a].concat(p.d),rnd);
    return {p:p,opts:opts};
  });
  exDone=false;

  var h='<div class="exbar"><span class="pill" id="ex-clock">٠٠:٠٠</span>'+
    '<span class="pill" id="ex-prog">أجبتَ عن ٠ من '+ad(exItems.length)+'</span>'+
    '<button class="btn go" id="ex-submit">تصحيح الاختبار</button></div>';
  exItems.forEach(function(it,i){
    h+='<div class="exq" data-i="'+i+'"><div class="num">سؤال '+ad(i+1)+' — '+esc(it.p.n)+'</div>'+
       '<div class="qt">'+esc(it.p.q)+'</div>';
    it.opts.forEach(function(o,k){
      h+='<label class="opt" data-o="'+k+'"><input type="radio" name="ex'+i+'" value="'+k+'">'+
         esc(o)+'</label>';
    });
    h+='<div class="fb" style="display:none"></div></div>';
  });
  h+='<div style="text-align:center;margin:18px 0">'+
     '<button class="btn go" id="ex-submit2">تصحيح الاختبار</button></div>';
  live.innerHTML=h;
  document.getElementById('ex-again').style.display='';

  live.addEventListener('change',function(ev){
    var t=ev.target;
    if(!t||t.type!=='radio'||exDone) return;
    var box=t.closest('.exq');
    var ls=box.querySelectorAll('.opt');
    for(var k=0;k<ls.length;k++) ls[k].classList.remove('sel');
    t.closest('.opt').classList.add('sel');
    refreshProg();
  });
  document.getElementById('ex-submit').addEventListener('click',grade);
  document.getElementById('ex-submit2').addEventListener('click',grade);

  exT0=Date.now();
  if(exTimer) clearInterval(exTimer);
  exTimer=setInterval(tick,1000); tick();
  window.scrollTo(0,0);
}

function grade(){
  if(exDone) return;
  exDone=true;
  if(exTimer){ clearInterval(exTimer); exTimer=null; }
  var secs=Math.floor((Date.now()-exT0)/1000);
  var right=0, blank=0;
  exItems.forEach(function(it,i){
    var box=live.querySelector('.exq[data-i="'+i+'"]');
    var sel=box.querySelector('input[type=radio]:checked');
    var ls=box.querySelectorAll('.opt');
    var good=-1,k;
    for(k=0;k<it.opts.length;k++) if(it.opts[k]===it.p.a) good=k;
    for(k=0;k<ls.length;k++){
      ls[k].classList.remove('sel');
      var oi=parseInt(ls[k].getAttribute('data-o'),10);
      var inp=ls[k].querySelector('input'); if(inp) inp.disabled=true;
      if(oi===good) ls[k].classList.add('good');
      else if(sel&&parseInt(sel.value,10)===oi) ls[k].classList.add('bad');
    }
    var fb=box.querySelector('.fb');
    var hit=sel&&parseInt(sel.value,10)===good;
    if(hit) right++; if(!sel) blank++;
    fb.style.display='';
    fb.innerHTML='<div class="verdict '+(hit?'y':'n')+'">'+
      (hit?'إجابة صحيحة ✓':(sel?'إجابة خاطئة ✗':'لم تُجب ✗'))+'</div>'+
      '<div class="ans">'+esc(it.p.a)+'</div>'+
      '<div class="exp">'+esc(it.p.e)+'</div>';
  });
  var pc=exItems.length?Math.round(right*100/exItems.length):0;
  var gr = pc>=90?'ممتاز':(pc>=80?'جيد جدًّا':(pc>=70?'جيد':(pc>=60?'مقبول':'يحتاج مراجعة')));
  var sc=document.createElement('div');
  sc.className='score'; sc.id='ex-score';
  sc.innerHTML='<span class="pc">'+ad(pc)+'٪</span>'+
    '<div class="gr">'+gr+' — '+ad(right)+' من '+ad(exItems.length)+' إجابة صحيحة</div>'+
    '<div class="dt">الزمن: '+ad(two(Math.floor(secs/60))+':'+two(secs%60))+
    ' · غير مُجاب: '+ad(blank)+' · خطأ: '+ad(exItems.length-right-blank)+'</div>';
  live.insertBefore(sc,live.firstChild);
  window.scrollTo(0,0);
}

document.getElementById('ex-go').addEventListener('click',startExam);
document.getElementById('ex-again').addEventListener('click',startExam);

/* ---------- تبديل التبويبات ---------- */
var all=tabs.querySelectorAll('.tab');
for(var i=0;i<all.length;i++){
  all[i].addEventListener('click',function(){
    var id=this.getAttribute('data-tab'),j;
    for(j=0;j<all.length;j++) all[j].classList.toggle('on',all[j]===this);
    var ps=panels.querySelectorAll('.panel');
    for(j=0;j<ps.length;j++) ps[j].classList.toggle('on',ps[j].id==='p-'+id);
    window.scrollTo(0,0);
  });
}
all[0].classList.add('on');
document.getElementById('p-files').classList.add('on');
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
