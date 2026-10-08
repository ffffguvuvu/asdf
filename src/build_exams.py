# -*- coding: utf-8 -*-
"""يبني صفحة بنك أسئلة اللغة العربية لمسابقات التعيين: arabic-exams-bank.html"""

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "arabi"))

import core  # noqa: E402

MODULES = [
    "g_nahw", "g_sarf", "g_imla", "g_bala", "g_adab", "g_mjam",
    "g_uslb", "g_arud", "g_fiqh", "g_turq",
    "g_ext", "g_ext2", "g_ext3", "g_ext4", "g_ext5", "g_ext6",
]

OUT = os.path.join(ROOT, "arabic-exams-bank.html")

CSS = """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI","Tahoma",'Noto Naskh Arabic',sans-serif;
 direction:rtl;background:#eef2f7;color:#17222f;line-height:1.85;font-size:16px}
a{color:#0b6b57}
header{background:linear-gradient(135deg,#0d5c4a,#12836a 55%,#1aa184);
 color:#fff;padding:22px 18px 16px;box-shadow:0 2px 14px rgba(0,0,0,.18)}
header h1{margin:0 0 6px;font-size:1.55rem;letter-spacing:.2px}
header p{margin:0;opacity:.93;font-size:.95rem}
.kpi{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.kpi span{background:rgba(255,255,255,.17);border:1px solid rgba(255,255,255,.3);
 border-radius:999px;padding:3px 12px;font-size:.85rem}
nav{position:sticky;top:0;z-index:40;background:#fff;
 border-bottom:1px solid #d6dfea;box-shadow:0 2px 10px rgba(16,40,70,.07)}
.tabs{display:flex;flex-wrap:wrap;gap:4px;padding:8px 10px;max-width:1180px;margin:0 auto}
.tabs button{border:1px solid #cfdbe8;background:#f7fafc;color:#2a3b4d;
 border-radius:9px;padding:6px 13px;cursor:pointer;font-size:.9rem;
 font-family:inherit;transition:.14s}
.tabs button:hover{background:#e7f3ef;border-color:#9fd2c3}
.tabs button.on{background:#0d6b56;color:#fff;border-color:#0d6b56;font-weight:600}
main{max-width:1180px;margin:0 auto;padding:16px 12px 70px}
.panel{display:none}
.panel.on{display:block}
.toolbar{background:#fff;border:1px solid #dbe4ee;border-radius:12px;
 padding:11px;margin-bottom:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.toolbar input[type=search],.toolbar select{font-family:inherit;font-size:.92rem;
 padding:7px 11px;border:1px solid #cfdbe8;border-radius:8px;background:#fbfdff;color:#17222f}
.toolbar input[type=search]{flex:1;min-width:210px}
.btn{border:1px solid #cfdbe8;background:#f7fafc;border-radius:8px;padding:7px 13px;
 cursor:pointer;font-family:inherit;font-size:.9rem;color:#2a3b4d}
.btn:hover{background:#e7f3ef}
.btn.on{background:#0d6b56;color:#fff;border-color:#0d6b56}
.count{font-size:.88rem;color:#5a6c80;margin-inline-start:auto}
.q{background:#fff;border:1px solid #dbe4ee;border-left:4px solid #0d6b56;
 border-radius:11px;padding:13px 15px;margin-bottom:11px;
 box-shadow:0 1px 3px rgba(16,40,70,.05)}
.q .qh{display:flex;gap:8px;align-items:flex-start;margin-bottom:9px}
.q .num{background:#0d6b56;color:#fff;border-radius:7px;min-width:44px;
 text-align:center;font-size:.8rem;padding:2px 6px;flex:none;margin-top:3px}
.q .qt{font-weight:600;font-size:1.02rem}
.opts{list-style:none;margin:0 0 8px;padding:0;display:grid;gap:5px}
.opt{border:1px solid #d9e2ec;background:#fbfdff;border-radius:8px;
 padding:6px 11px;cursor:pointer;font-size:.96rem;transition:.12s}
.opt:hover{background:#eef6f3;border-color:#a8d6c8}
.opt.right{background:#e3f6ec;border-color:#36a06f;font-weight:600}
.opt.wrong{background:#fdeaea;border-color:#d4665f}
.exp{background:#f3f8f6;border:1px dashed #9ec9bb;border-radius:9px;
 padding:9px 12px;font-size:.94rem;color:#1d3b33;display:none}
.exp.show{display:block}
.exp b{color:#0d6b56}
.tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
.tag{font-size:.75rem;background:#eef3f8;border:1px solid #d6e0ea;
 border-radius:999px;padding:1px 9px;color:#4a5c70}
.tag.d1{background:#eaf7ee;border-color:#a9ddba;color:#226b3c}
.tag.d2{background:#fff6e5;border-color:#f0d08a;color:#7a5712}
.tag.d3{background:#fdecec;border-color:#eeb0ac;color:#8e2f29}
.tag.rep{background:#fdf0f7;border-color:#e8b6d4;color:#8d2f6a}
.more{display:block;width:100%;margin:12px 0;padding:11px;border-radius:10px;
 border:1px dashed #9fb6cc;background:#fff;cursor:pointer;font-family:inherit;
 font-size:.95rem;color:#36506b}
.none{text-align:center;color:#8193a6;padding:34px 10px;font-size:1rem}
.ex-setup{background:#fff;border:1px solid #dbe4ee;border-radius:12px;padding:16px}
.ex-setup label{font-size:.92rem;margin-inline-end:4px}
.res{background:#fff;border:1px solid #dbe4ee;border-radius:12px;
 padding:16px;margin-bottom:14px;display:none}
.res.show{display:block}
.res h3{margin:0 0 8px;color:#0d6b56}
.bar{height:11px;border-radius:999px;background:#e4ebf3;overflow:hidden;margin:8px 0}
.bar i{display:block;height:100%;background:linear-gradient(90deg,#15a37f,#0d6b56)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.card{background:#fff;border:1px solid #dbe4ee;border-radius:11px;padding:12px 14px}
.card h4{margin:0 0 4px;font-size:1rem;color:#0d6b56}
.card p{margin:0;font-size:.88rem;color:#55677c}
.card .big{font-size:1.5rem;font-weight:700;color:#12836a}
.guide{background:#fff;border:1px solid #dbe4ee;border-radius:12px;padding:16px 18px}
.guide h3{color:#0d6b56;margin:18px 0 6px}
.guide h3:first-child{margin-top:0}
.guide ul{margin:0;padding-inline-start:20px}
.guide li{margin-bottom:5px}
footer{text-align:center;color:#7b8ca0;font-size:.85rem;padding:18px 12px 34px}
@media print{
 nav,.toolbar,.more,header .kpi,footer,.tabs{display:none!important}
 body{background:#fff;font-size:11.5pt}
 .panel{display:block!important}
 .q{break-inside:avoid;box-shadow:none;border-left-width:3px}
 .exp{display:block!important}
 .opt{cursor:default}
}
@media(max-width:620px){
 header h1{font-size:1.2rem}
 .q .qt{font-size:.97rem}
 main{padding:12px 8px 60px}
}
"""

JS = r"""
var BANK=JSON.parse(document.getElementById('BANK').textContent);
var QS=BANK.q,BR=BANK.br,TP=BANK.tp;
var AR='\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669';
function ad(n){return String(n).replace(/[0-9]/g,function(d){return AR[+d]});}
function esc(s){return String(s).replace(/[&<>]/g,function(c){
 return c==='&'?'&amp;':c==='<'?'&lt;':'&gt;';});}
var TASH=/[\u0617-\u061a\u064b-\u0652\u0670\u0640]/g;
function nrm(s){return String(s).replace(TASH,'')
 .replace(/[\u0623\u0625\u0622\u0671]/g,'\u0627')
 .replace(/\u0629/g,'\u0647').replace(/\u0649/g,'\u064a')
 .replace(/[\u0624\u0626]/g,'\u0621')
 .replace(/[\u00ab\u00bb"'(),.:;!?\u061f\-\u2014\u2013\[\]\/\u2026]/g,' ')
 .replace(/\s+/g,' ').trim();}

/* فهرس الأسئلة حسب الفرع */
var BYBR={};
for(var i=0;i<QS.length;i++){var b=QS[i][4];(BYBR[b]=BYBR[b]||[]).push(i);}
for(var k in BYBR){} 
var HAY=QS.map(function(r){return nrm(r[0]+' '+r[1].join(' ')+' '+r[3]+' '+TP[r[5]]);});

var state={};
function mkCard(idx,n){
 var r=QS[idx],d=document.createElement('div');d.className='q';d.dataset.i=idx;
 var o='';
 for(var j=0;j<4;j++)o+='<li class="opt" data-o="'+j+'">'+esc(r[1][j])+'</li>';
 var tags='<span class="tag">'+esc(BR[r[4]])+'</span>'+
  '<span class="tag">'+esc(TP[r[5]])+'</span>'+
  '<span class="tag d'+r[6]+'">'+(r[6]==1?'\u0633\u0647\u0644':r[6]==2?'\u0645\u062a\u0648\u0633\u0637':'\u0635\u0639\u0628')+'</span>'+
  (r[7]>=3?'<span class="tag rep">\u0643\u062b\u064a\u0631 \u0627\u0644\u062a\u0643\u0631\u0627\u0631</span>':'');
 d.innerHTML='<div class="qh"><span class="num">'+ad(n)+'</span>'+
  '<span class="qt">'+esc(r[0])+'</span></div>'+
  '<ul class="opts">'+o+'</ul>'+
  '<div class="exp"><b>\u0627\u0644\u0625\u062c\u0627\u0628\u0629:</b> '+
  esc(r[1][r[2]])+'<br><b>\u0627\u0644\u0634\u0631\u062d:</b> '+esc(r[3])+'</div>'+
  '<div class="tags">'+tags+'</div>';
 return d;
}
function reveal(card){
 var idx=+card.dataset.i,r=QS[idx];
 card.querySelectorAll('.opt').forEach(function(el,j){
  el.classList.add(j===r[2]?'right':'wrong');});
 card.querySelector('.exp').classList.add('show');
}
function hideAll(card){
 card.querySelectorAll('.opt').forEach(function(el){
  el.classList.remove('right','wrong');});
 card.querySelector('.exp').classList.remove('show');
}

function filt(br){
 var st=state[br],q=nrm(st.search),tp=st.topic,df=st.diff,rep=st.rep;
 return BYBR[br].filter(function(i){
  var r=QS[i];
  if(tp && TP[r[5]]!==tp)return false;
  if(df && String(r[6])!==df)return false;
  if(rep && r[7]<3)return false;
  if(q && HAY[i].indexOf(q)<0)return false;
  return true;});
}
function render(br,reset){
 var st=state[br],host=document.getElementById('list-'+br);
 if(reset){st.hits=filt(br);st.shown=0;host.innerHTML='';}
 var end=Math.min(st.shown+80,st.hits.length),fr=document.createDocumentFragment();
 for(var i=st.shown;i<end;i++)fr.appendChild(mkCard(st.hits[i],i+1));
 host.appendChild(fr);st.shown=end;
 var mb=document.getElementById('more-'+br);
 mb.style.display=st.shown<st.hits.length?'block':'none';
 mb.textContent='\u0639\u0631\u0636 \u0627\u0644\u0645\u0632\u064a\u062f ('+
  ad(st.hits.length-st.shown)+' \u0645\u062a\u0628\u0642\u064d)';
 document.getElementById('cnt-'+br).textContent=
  '\u0627\u0644\u0646\u062a\u0627\u0626\u062c: '+ad(st.hits.length)+
  ' \u0645\u0646 '+ad(BYBR[br].length);
 var none=document.getElementById('none-'+br);
 if(none)none.style.display=st.hits.length?'none':'block';
}

document.querySelectorAll('button[data-tab]').forEach(function(b){
 b.addEventListener('click',function(){
  document.querySelectorAll('button[data-tab]').forEach(function(x){
   x.classList.remove('on');});
  b.classList.add('on');
  document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('on');});
  var p=document.getElementById('p-'+b.dataset.tab);
  if(p)p.classList.add('on');
  window.scrollTo(0,0);
 });
});

Object.keys(BYBR).forEach(function(br){
 state[br]={search:'',topic:'',diff:'',rep:false,shown:0,hits:[]};
 var host=document.getElementById('list-'+br);
 if(!host)return;
 var t;
 var si=document.getElementById('s-'+br);
 si.addEventListener('input',function(){
  clearTimeout(t);t=setTimeout(function(){
   state[br].search=si.value;render(br,true);},180);});
 document.getElementById('t-'+br).addEventListener('change',function(e){
  state[br].topic=e.target.value;render(br,true);});
 document.getElementById('d-'+br).addEventListener('change',function(e){
  state[br].diff=e.target.value;render(br,true);});
 document.getElementById('r-'+br).addEventListener('click',function(e){
  state[br].rep=!state[br].rep;e.target.classList.toggle('on',state[br].rep);
  render(br,true);});
 document.getElementById('more-'+br).addEventListener('click',function(){
  render(br,false);});
 document.getElementById('sa-'+br).addEventListener('click',function(){
  document.querySelectorAll('#list-'+br+' .q').forEach(reveal);});
 document.getElementById('ha-'+br).addEventListener('click',function(){
  document.querySelectorAll('#list-'+br+' .q').forEach(hideAll);});
 host.addEventListener('click',function(e){
  var op=e.target.closest('.opt');if(!op)return;
  reveal(op.closest('.q'));});
 render(br,true);
});

/* ------------------------------- وضع الامتحان ------------------------------ */
var exQ=[],exA=[];
document.getElementById('exStart').addEventListener('click',function(){
 var br=document.getElementById('exBranch').value;
 var n=+document.getElementById('exCount').value;
 var pool=br?BYBR[br].slice():QS.map(function(_,i){return i;});
 for(var i=pool.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));
  var tmp=pool[i];pool[i]=pool[j];pool[j]=tmp;}
 exQ=pool.slice(0,Math.min(n,pool.length));exA=exQ.map(function(){return -1;});
 var host=document.getElementById('exList');host.innerHTML='';
 exQ.forEach(function(idx,k){host.appendChild(mkCard(idx,k+1));});
 document.getElementById('exSubmit').style.display='block';
 document.getElementById('exResult').classList.remove('show');
 host.scrollIntoView({behavior:'smooth'});
});
document.getElementById('exList').addEventListener('click',function(e){
 var op=e.target.closest('.opt');if(!op)return;
 var card=op.closest('.q'),k=[].indexOf.call(card.parentNode.children,card);
 card.querySelectorAll('.opt').forEach(function(x){x.classList.remove('right');});
 op.classList.add('right');exA[k]=+op.dataset.o;
});
document.getElementById('exSubmit').addEventListener('click',function(){
 var ok=0;
 document.querySelectorAll('#exList .q').forEach(function(card,k){
  var r=QS[exQ[k]];
  card.querySelectorAll('.opt').forEach(function(el,j){
   el.classList.remove('right','wrong');
   if(j===r[2])el.classList.add('right');
   else if(j===exA[k])el.classList.add('wrong');});
  card.querySelector('.exp').classList.add('show');
  if(exA[k]===r[2])ok++;});
 var pct=exQ.length?Math.round(ok*100/exQ.length):0;
 var box=document.getElementById('exResult');
 box.innerHTML='<h3>\u0627\u0644\u0646\u062a\u064a\u062c\u0629</h3>'+
  '<p>\u0623\u062c\u0628\u062a \u0625\u062c\u0627\u0628\u0629 \u0635\u062d\u064a\u062d\u0629 \u0639\u0646 <b>'+
  ad(ok)+'</b> \u0645\u0646 <b>'+ad(exQ.length)+
  '</b> \u0633\u0624\u0627\u0644\u064b\u0627 \u0628\u0646\u0633\u0628\u0629 <b>'+ad(pct)+
  '%</b>.</p><div class="bar"><i style="width:'+pct+'%"></i></div>';
 box.classList.add('show');box.scrollIntoView({behavior:'smooth'});
});
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def build():
    for m in MODULES:
        __import__(m).run()
    qs = core.QS
    topics = sorted({q["t"] for q in qs})
    tix = {t: i for i, t in enumerate(topics)}
    rows = [[q["q"], q["o"], q["a"], q["e"], q["b"], tix[q["t"]],
             q["d"], q["r"]] for q in qs]
    br_names = dict(core.BRANCHES)
    data = {"q": rows, "br": br_names, "tp": topics}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    from collections import Counter
    cb = Counter(q["b"] for q in qs)
    bt = {}
    for q in qs:
        bt.setdefault(q["b"], set()).add(q["t"])

    present = [(c, n) for c, n in core.BRANCHES if cb.get(c)]

    tabs = ['<button data-tab="guide">\u062f\u0644\u064a\u0644 '
            '\u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645</button>']
    for c, n in present:
        tabs.append('<button data-tab="%s">%s <small>(%s)</small></button>'
                    % (c, esc(n), core.ad(cb[c])))
    tabs.append('<button data-tab="exam" class="on">\u0648\u0636\u0639 '
                '\u0627\u0644\u0627\u0645\u062a\u062d\u0627\u0646</button>')
    # اجعل أول فرع هو المفتوح افتراضيًّا
    tabs[1] = tabs[1].replace('<button data-tab="%s">' % present[0][0],
                              '<button data-tab="%s" class="on">'
                              % present[0][0])
    tabs[-1] = tabs[-1].replace(' class="on"', '')

    panels = []
    for i, (c, n) in enumerate(present):
        tops = sorted(bt[c])
        opts = "".join('<option value="%s">%s</option>' % (esc(t), esc(t))
                       for t in tops)
        panels.append("""
<section class="panel%s" id="p-%s">
 <div class="toolbar">
  <input type="search" id="s-%s" placeholder="ابحث في نصّ السؤال أو الخيارات أو الشرح…">
  <select id="t-%s"><option value="">كل الموضوعات (%s)</option>%s</select>
  <select id="d-%s"><option value="">كل المستويات</option>
   <option value="1">سهل</option><option value="2">متوسط</option>
   <option value="3">صعب</option></select>
  <button class="btn" id="r-%s">الأكثر تكرارًا</button>
  <button class="btn" id="sa-%s">إظهار الإجابات</button>
  <button class="btn" id="ha-%s">إخفاء</button>
  <span class="count" id="cnt-%s"></span>
 </div>
 <div id="list-%s"></div>
 <div class="none" id="none-%s" style="display:none">لا توجد نتائج مطابقة.</div>
 <button class="more" id="more-%s" style="display:none">عرض المزيد</button>
</section>""" % (" on" if i == 0 else "", c, c, c, core.ad(len(tops)), opts,
                 c, c, c, c, c, c, c, c))

    exam_branches = "".join('<option value="%s">%s</option>' % (c, esc(n))
                            for c, n in present)
    panels.append("""
<section class="panel" id="p-exam">
 <div class="ex-setup">
  <h3 style="margin:0 0 10px;color:#0d6b56">امتحان تجريبي عشوائي</h3>
  <p style="margin:0 0 12px;font-size:.93rem;color:#55677c">
   اختر الفرع وعدد الأسئلة، ثم أجب باختيار البديل الذي تراه صوابًا،
   ثم اضغط «صحّح الإجابات» لترى درجتك والشرح التفصيلي لكل سؤال.</p>
  <label>الفرع:</label>
  <select id="exBranch"><option value="">جميع الفروع</option>%s</select>
  &nbsp;<label>عدد الأسئلة:</label>
  <select id="exCount"><option>10</option><option selected>20</option>
   <option>30</option><option>50</option><option>100</option></select>
  &nbsp;<button class="btn on" id="exStart">ابدأ الامتحان</button>
 </div>
 <div class="res" id="exResult"></div>
 <div id="exList" style="margin-top:14px"></div>
 <button class="btn" id="exSubmit" style="display:none;width:100%%;margin-top:10px;
  padding:12px;background:#0d6b56;color:#fff;border-color:#0d6b56;font-size:1rem">
  صحّح الإجابات</button>
</section>""" % exam_branches)

    cards = "".join(
        '<div class="card"><h4>%s</h4><p class="big">%s</p>'
        '<p>%s موضوعًا فرعيًّا</p></div>'
        % (esc(n), core.ad(cb[c]), core.ad(len(bt[c]))) for c, n in present)

    panels.append("""
<section class="panel" id="p-guide">
 <div class="guide">
  <h3>ما هذا البنك؟</h3>
  <p>بنك أسئلة في اللغة العربية بجميع فروعها، مصوغ على نمط ما يَرِد في
  <b>مسابقات التعيين</b> (مسابقات التربية والتعليم والأزهر، واختبارات
  الجهاز المركزي للتنظيم والإدارة، واختبارات الرخصة المهنية، ومسابقات
  توظيف الأساتذة في عدد من البلاد العربية). كل سؤال معه
  <b>الإجابة الصحيحة</b> و<b>شرح مفصّل يعلّل الحكم</b> لا يكتفي بذكر الصواب.</p>

  <h3>الفروع المشمولة</h3>
  <div class="cards">%s</div>

  <h3>كيف تستعمله؟</h3>
  <ul>
   <li><b>التبويبات أعلى الصفحة:</b> كل فرع في تبويب مستقلّ، وبجانب اسمه عدد أسئلته.</li>
   <li><b>البحث:</b> اكتب أي كلمة فيبحث عنها في نصّ السؤال والخيارات والشرح
       والموضوع، مع تجاهل الحركات واختلاف رسم الهمزة والألف والتاء.</li>
   <li><b>المرشّحات:</b> «الموضوع» يحصر الأسئلة في باب بعينه، و«المستوى»
       يفرزها سهلًا ومتوسطًا وصعبًا، و«الأكثر تكرارًا» يعرض ما يتردّد كثيرًا
       في الاختبارات الفعلية.</li>
   <li><b>الإجابة:</b> اضغط أي خيار ليظهر الصواب والخطأ ومعهما الشرح،
       أو استعمل «إظهار الإجابات» لكشف المعروض كله دفعة واحدة.</li>
   <li><b>وضع الامتحان:</b> يولّد اختبارًا عشوائيًّا من ١٠ إلى ١٠٠ سؤال
       في فرع واحد أو في جميع الفروع، ثم يصحّح ويحسب النسبة ويعرض الشرح.</li>
   <li><b>الطباعة:</b> من قائمة الطباعة في المتصفّح تُطبع الأسئلة المعروضة
       مع إجاباتها وشروحها في تنسيق مناسب للورق.</li>
  </ul>

  <h3>منهج بناء المحتوى</h3>
  <ul>
   <li>الأسئلة مصوغة صياغة أصلية على أنماط الأسئلة الشائعة في هذه المسابقات
       (الإعراب التطبيقي، الميزان الصرفي، رسم الهمزة، تحليل الشواهد البلاغية،
       الكشف في المعاجم، تصويب الأخطاء الشائعة، طرق التدريس…).</li>
   <li>الشواهد الأدبية من القرآن الكريم والشعر العربي القديم، وهي نصوص
       متاحة للعموم، ويُذكر معها وجه الاستشهاد.</li>
   <li>الكتب والمؤلّفات يُشار إليها بعناوينها وأصحابها فقط.</li>
   <li>الشرح في كل سؤال مكتوب أصلًا لهذا البنك، ويُعنى بـ«لماذا» لا بـ«ماذا».</li>
  </ul>

  <h3>نصائح لاجتياز المسابقة</h3>
  <ul>
   <li>ابدأ بالفروع ذات الوزن الأكبر: النحو والصرف والإملاء، فهي عماد أكثر الأسئلة.</li>
   <li>ركّز على <b>التعليل</b> لا الحفظ؛ فكثير من الأسئلة يُعاد بصياغة مختلفة
       وبالأمثلة نفسها معكوسة.</li>
   <li>استعمل «وضع الامتحان» بزمن محدّد لتعتاد الضغط وسرعة الاختيار.</li>
   <li>راجع ما أخطأت فيه فقط في الجولة الثانية؛ فهو أسرع طريق لرفع الدرجة.</li>
  </ul>
 </div>
</section>""" % cards)

    html = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>بنك أسئلة اللغة العربية لمسابقات التعيين</title>
<meta name="description" content="بنك أسئلة اللغة العربية بجميع فروعها لمسابقات التعيين مع الإجابات والشرح المفصّل.">
<style>%s</style>
</head>
<body>
<header>
 <h1>بنك أسئلة اللغة العربية لمسابقات التعيين</h1>
 <p>أسئلة بجميع فروع اللغة &mdash; مع الإجابة الصحيحة وشرح مفصّل يعلّل الحكم</p>
 <div class="kpi">
  <span>%s سؤالًا</span><span>%s فروع رئيسة</span>
  <span>%s موضوعًا فرعيًّا</span><span>بحث ومرشّحات</span>
  <span>وضع امتحان مصحَّح</span><span>قابل للطباعة</span>
 </div>
</header>
<nav><div class="tabs">%s</div></nav>
<main>%s</main>
<footer>بنك أسئلة اللغة العربية لمسابقات التعيين &mdash; %s سؤالًا في %s فرعًا.</footer>
<script id="BANK" type="application/json">%s</script>
<script>%s</script>
</body>
</html>
""" % (CSS, core.ad(len(qs)), core.ad(len(present)), core.ad(len(topics)),
       "".join(tabs), "".join(panels), core.ad(len(qs)),
       core.ad(len(present)), blob, JS)

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  (%d bytes)" % (OUT, len(html.encode("utf-8"))))
    print("questions: %d | branches: %d | topics: %d"
          % (len(qs), len(present), len(topics)))
    for c, n in present:
        print("  %-5s %-38s %5d" % (c, n, cb[c]))


if __name__ == "__main__":
    build()
