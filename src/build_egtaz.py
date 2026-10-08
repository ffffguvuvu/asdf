# -*- coding: utf-8 -*-
"""يبني صفحة egtaz-arabic-guide.html من وحدات البيانات في egtaz/."""
import json, os, sys, html

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
]

# ملفات مجلد «تخصص عربي» في Google Drive كما ظهرت في فهرس المجلد
FILES = [
    ("360 سؤال في اللغة العربية", "بنك أسئلة عام", "تعذّرت قراءته — الملف لا يستجيب للتنزيل المباشر"),
    ("أسئلة تخصص لغة عربية لمسابقة وزارة التربية والتعليم", "أسئلة الجهاز المركزي", "قُرئ كاملًا"),
    ("الأسئلة التي وردت لتخصص اللغة العربية — مراجعة ما قبل الامتحان", "أسئلة وردت فعلًا", "قُرئ كاملًا"),
    ("أساسيات في قواعد الإملاء (المرشد الإملائي)", "مرجع إملاء", "قُرئ كاملًا"),
    ("اللغة العربية تخصص للجميع", "بنك أسئلة", "قُرئ"),
    ("تسريبات الحسام — أحدث الأسئلة في تخصص اللغة العربية (3)", "بلاغة وعروض وأدب", "قُرئ"),
    ("تسريبات الحسام في العربية (خاص بتخصص اللغة العربية)", "أسئلة تخصص", "تالف الترميز — نص مشوّش غير مقروء"),
    ("تسريبات الحسام في اللغة العربية (خاص بالتخصص)", "أسئلة تخصص", "نسخة مكررة"),
    ("تسريبات الحسام في اللغة العربية (عربي عام لجميع التخصصات)", "عربي عام", "نسخة مكررة"),
    ("طرق تدريس اللغة العربية", "مرجع طرق تدريس", "قُرئ كاملًا"),
    ("طرق تدريس اللغة العربية — 1", "مرجع طرق تدريس", "نسخة مكررة"),
    ("مراجعة ما قبل الامتحان — أحدث أسئلة وردت بالفعل", "مراجعة", "تعذّر التنزيل"),
    ("أسئلة معلم فصل", "تخصص آخر", "خارج تخصص اللغة العربية"),
    ("أحدث أسئلة للحاسب الآلي — الجزء الثاني", "حاسب آلي", "خارج تخصص اللغة العربية"),
]

DRIVE = "https://drive.google.com/drive/folders/1YvqHviSNCHqECMZ0aslM0tJ5_1oKYnn3"


def main():
    secs = []
    total_q = 0
    total_r = 0
    for code, mod in MODULES:
        m = __import__(mod)
        qs = [{"q": a, "a": b, "e": c} for (a, b, c) in m.QS]
        rs = [{"t": a, "b": b} for (a, b) in m.RULES]
        total_q += len(qs)
        total_r += len(rs)
        secs.append({"c": code, "n": m.NAME, "q": qs, "r": rs})

    data = {"s": secs, "f": [{"n": a, "k": b, "st": c} for (a, b, c) in FILES]}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    page = TPL.replace("__DATA__", blob) \
              .replace("__NQ__", str(total_q)) \
              .replace("__NR__", str(total_r)) \
              .replace("__NS__", str(len(secs))) \
              .replace("__DRIVE__", DRIVE)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("WROTE", OUT, os.path.getsize(OUT), "bytes")
    print("sections", len(secs), "| questions", total_q, "| rules", total_r)
    for s in secs:
        print("  ", s["n"], len(s["q"]), "سؤال /", len(s["r"]), "قاعدة")


TPL = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ملفات المسابقة — تخصص لغة عربية: حلّ الأسئلة وشرح القواعد</title>
<style>
:root{--bg:#f4f6fb;--card:#fff;--ink:#17202e;--mut:#5d6b84;--pri:#1d5fa8;--pri2:#e8f0fb;
--ok:#0f7a4d;--ok2:#e4f5ec;--wr:#b3261e;--line:#dfe5f0;--acc:#8b5cf6}
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
.toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin-bottom:14px}
input[type=search],select{font-family:inherit;font-size:.92rem;padding:8px 12px;border:1px solid var(--line);
border-radius:9px;background:#fff;color:var(--ink)}
input[type=search]{flex:1;min-width:190px}
.btn{font-family:inherit;font-size:.88rem;padding:8px 14px;border:1px solid var(--line);background:#fff;
border-radius:9px;cursor:pointer;color:var(--mut);font-weight:600}
.btn:hover{background:var(--pri2);color:var(--pri);border-color:var(--pri)}
.btn.on{background:var(--pri);color:#fff;border-color:var(--pri)}
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
@media print{nav,.toolbar,header .chips{display:none}.panel{display:block!important}
.card,.q{break-inside:avoid;box-shadow:none}body{background:#fff}}
</style>
</head>
<body>
<header><div class="wrap">
<h1>ملفات المسابقة — تخصص لغة عربية</h1>
<div class="sub">حلّ كامل لأسئلة ملفات المجلد مع شرح مفصّل للقواعد التي بُنيت عليها</div>
<div class="chips">
<span class="chip">__NQ__ سؤالًا محلولًا</span>
<span class="chip">__NR__ قاعدة مشروحة</span>
<span class="chip">__NS__ فروع</span>
<span class="chip">المصدر: مجلد «تخصص عربي»</span>
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

function mkTab(id,label){
  var b=document.createElement('button');
  b.className='tab'; b.setAttribute('data-tab',id); b.textContent=label;
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
