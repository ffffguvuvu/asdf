#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بناء «دروس الإعراب» — يجمع أجزاء الدروس من lessons-src/ ويولِّد الشريط الجانبي
والفهرس التفصيلي آليًّا من عناوين h2/h3/h4، ثم يتحقَّق من الوسوم والروابط.
شغِّله من جذر المستودع:  python3 lessons-src/build.py
"""
import re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT  = os.path.join(ROOT, 'arabic-lessons.html')
REF  = os.path.join(ROOT, 'arabic-grammar.html')

AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n):
    return ''.join(AR[int(c)] for c in str(n))

EXTRA_CSS = """

/* ——— وضعُ الصفحات: قياسُ A4 بهوامشَ كهيئاتِ Word (٢٫٥٤ سم أعلى/أسفل، ٣٫١٨ سم يمينًا ويسارًا) ——— */
:root{--pw:21cm;--ph:29.7cm;--px:3.18cm;--py:2.54cm}
.toolbar{position:sticky;top:0;z-index:60;display:flex;gap:8px;align-items:center;justify-content:center;
  flex-wrap:wrap;padding:8px 12px;background:rgba(250,247,240,.94);border-bottom:1px solid var(--line);
  backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px)}
.toolbar button{font:inherit;font-size:14px;font-weight:700;color:var(--ink2);background:#fffdfa;
  border:1px solid var(--line);border-radius:9px;padding:6px 14px;cursor:pointer}
.toolbar button:hover{border-color:var(--gold);color:var(--green)}
.toolbar .hint{font-size:13px;color:var(--muted)}
.irab ul{padding-inline-start:22px;margin:0}
.irab .alt{color:#cfe6dd}
body.sheets .layout{display:block;max-width:none;padding:0;margin:0}
body.sheets nav.toc{display:none}
body.sheets .hero{max-width:var(--pw);margin:22px auto;padding:var(--py) var(--px);min-height:var(--ph);
  display:grid;place-items:center;box-sizing:border-box;border-radius:3px;box-shadow:0 3px 18px rgba(0,0,0,.10)}
body.sheets .hero-inner{max-width:none}
body.sheets main{max-width:var(--pw);margin:0 auto;padding:20px 0 70px}
body.sheets .book{display:block}
body.sheets .sheet{position:relative;background:#fff;border:1px solid var(--line);border-radius:2px;
  box-shadow:0 3px 16px rgba(0,0,0,.10);min-height:var(--ph);padding:var(--py) var(--px);
  margin:0 0 20px;box-sizing:border-box;overflow-wrap:break-word}
body.sheets .sheet:after{content:attr(data-page);position:absolute;bottom:.75cm;inset-inline:var(--px);
  display:flex;justify-content:space-between;font-size:12.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:5px}
body.sheets .sheet.oversize:after{content:attr(data-page) " · صفحةٌ أطولُ من ورقةٍ لجدولٍ كبير"}
body.sheets main > section:not(:has(.book)){background:#fff;border:1px solid var(--line);border-radius:2px;
  box-shadow:0 3px 16px rgba(0,0,0,.10);padding:var(--py) var(--px);margin:0 0 20px}
body.sheets .sheet > :first-child{margin-top:0}
body.sheets .pager{max-width:var(--pw);margin:0 auto 22px;justify-content:space-between}
body.sheets .tblwrap table{min-width:0}
body.sheets table{font-size:14.6px}
@page{size:A4;margin:var(--py) var(--px)}
@media print{
  .toolbar{display:none!important}
  body{background:#fff;font-size:11.5pt}
  body.sheets .layout,body.sheets main{max-width:none;margin:0;padding:0;display:block}
  body.sheets .hero{max-width:none;min-height:0;margin:0 0 8mm;padding:12mm 0;box-shadow:none;border:none;display:block}
  body.sheets .sheet{border:none;box-shadow:none;border-radius:0;margin:0;padding:0;min-height:0;page-break-after:auto}
  body.sheets .sheet:after{display:none}
  body.sheets .book{page-break-before:always;break-before:page}
  body.sheets .book:first-of-type{page-break-before:auto;break-before:auto}
  .tblwrap{overflow:visible}
  table{min-width:0;font-size:9.5pt}
  th,td{padding:6px 7px}
  .irab{background:#123a34!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .pager,.no-print{display:none!important}
}
/* ——— إضافات «دروس الإعراب» ——— */
ol.rules{list-style:none;counter-reset:rl;padding:0;margin:14px 0;
  border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fffdfa}
ol.rules>li{counter-increment:rl;position:relative;padding:11px 58px 11px 15px;
  border-bottom:1px solid var(--line);font-size:15.6px;line-height:1.95}
ol.rules>li:last-child{border-bottom:none}
ol.rules>li:before{content:counter(rl,arabic-indic);position:absolute;inset-inline-start:0;top:0;bottom:0;
  width:42px;display:grid;place-items:center;background:var(--green-soft);
  color:var(--green);font-weight:800;font-size:15px;border-inline-end:1px solid var(--line)}
ol.rules>li b{color:var(--green)}
.lede{font-size:16.6px;color:var(--ink2);background:var(--gold-soft);border-radius:12px;
  padding:12px 16px;margin:0 0 18px;line-height:1.95}
.lede b{color:#6b4f12}
h4{color:var(--ink2);margin-top:20px}
h4:before{content:"◂ ";color:var(--gold)}
table.pos th:first-child,table.pos td:first-child{white-space:nowrap;font-weight:800;color:var(--green);background:#faf6ec}
table.pos{font-size:15px}
table.pos td{padding:11px 13px}
table.pos td .lbl{display:inline-block;background:var(--gold-soft);border:1px solid #e6d4ab;
  color:#6b4f12;border-radius:6px;padding:0 8px;font-size:13.2px;font-weight:700;margin:2px 3px 2px 0}
table.matrix{font-size:14.2px}
table.matrix td:first-child{white-space:nowrap;font-weight:800;color:var(--green)}
table.matrix td,table.matrix th{padding:9px 10px}
table.thab td:first-child{white-space:nowrap;font-weight:700;color:#6b4f12}
details.qa{border:1px solid var(--line);border-radius:11px;padding:10px 15px;margin:12px 0;background:#fffdfa}
details.qa>summary{cursor:pointer;font-weight:800;color:var(--green);list-style:none}
details.qa>summary:before{content:"▸ ";color:var(--gold)}
details.qa[open]>summary{margin-bottom:8px;border-bottom:1px dashed var(--line);padding-bottom:6px}
.pager{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0;font-size:14.5px}
.pager a{border:1px solid var(--line);border-radius:10px;padding:7px 14px;background:#fffdfa}
.pager a:hover{border-color:var(--gold);text-decoration:none}
.kicker{font-size:13.5px;letter-spacing:.5px;color:var(--muted);font-weight:700;margin-bottom:4px}
nav.toc a.grp{margin-top:7px;font-weight:800;color:var(--ink2)}
"""

def slug_titles(html, sid):
    """يضيف id تلقائيًّا لكل h3/h4 داخل الجزء، ويعيد قائمة الفهرس."""
    idx = {'h3':0,'h4':0}
    items = []
    def repl(m):
        tag, attrs, txt = m.group(1), m.group(2), m.group(3)
        idx[tag] += 1
        new_id = f"{sid}-{tag[1]}{idx[tag]}"
        if 'id=' not in attrs:
            m2 = re.match(r'\s*(?:<span class="num">(.*?)</span>)?(.*)', txt, re.S)
            label = re.sub(r'<[^>]+>', '', txt).strip()
            items.append((tag, new_id, label))
            return f'<{tag}{attrs} id="{new_id}">{txt}</{tag}>'
        return m.group(0)
    out = re.sub(r'<(h3|h4)((?:[^>]|\n)*?)>((?:(?!</h3>|</h4>)[\s\S])*)</h[34]>', repl, html)
    return out, items

def main():
    parts = sorted(glob.glob(os.path.join(HERE, 'p*.html')))
    if not parts:
        sys.exit('لا توجد أجزاء في lessons-src/')
    style = ''
    if os.path.exists(REF):
        style = re.search(r'<style>.*?</style>', open(REF, encoding='utf-8').read(), re.S).group(0)
    style = style.replace('</style>', EXTRA_CSS + '\n</style>')
    metas = []
    for path in parts:
        sid = os.path.basename(path)[1:-5]           # p01 -> 01
        raw = open(path, encoding='utf-8').read().strip()
        m = re.search(r'<section id="([^"]+)"', raw)
        sid = m.group(1) if m else sid
        raw, items = slug_titles(raw, sid)
        h2 = re.search(r'<h2>((?:(?!</h2>)[\s\S])*)</h2>', raw)
        title = re.sub(r'<[^>]+>', '', h2.group(1)).strip() if h2 else sid
        num = ''
        if h2:
            nn = re.search(r'<span class="num">(.*?)</span>', h2.group(1))
            num = nn.group(1) if nn else ''
            if nn:  # لا نكرّر الرقم مع العنوان في الفهرس والشرائط
                title = re.sub(r'^\s*' + re.escape(num) + r'\s*', '', title).strip()
        metas.append({'sid': sid, 'num': num, 'title': title, 'raw': raw, 'items': items})

    n_all = len(metas)
    for i, mt in enumerate(metas):
        cells = []
        if i > 0:
            p_ = metas[i-1]
            cells.append(f'<a href="#{p_["sid"]}"><span class="small">الدرسُ السابق</span> <b>{p_["num"]}</b>{p_["title"]}</a>')
        if i + 1 < n_all:
            n_ = metas[i+1]
            cells.append(f'<a href="#{n_["sid"]}"><span class="small">الدرسُ التالي</span> <b>{n_["num"]}</b>{n_["title"]}</a>')
        if cells:
            pager = '\n  <div class="pager">' + ''.join(cells) + '</div>'
            pos = mt['raw'].rfind('</section>')
            if pos > -1:
                mt['raw'] = mt['raw'][:pos] + pager + mt['raw'][pos:]

    body, nav, idx = [], [], []
    for mt in metas:
        sid, num, title, items, raw = mt['sid'], mt['num'], mt['title'], mt['items'], mt['raw']
        nav.append(f'      <a class="grp" href="#{sid}"><b>{num}</b>{title}</a>\n')
        sub = ' '.join(f'<a href="#{i}" class="{"subsub" if t=="h4" else ""}">{l}</a>' for t, i, l in items)
        idx.append(f'    <li><a href="#{sid}"><b>{num}</b>{title}</a>'
                   + (f'\n      <div class="idxsub">{sub}</div>' if sub else '') + '\n    </li>')
        body.append(raw)

    total_h = len(idx) and sum(1 for _ in re.finditer(r'<h[34]', ' '.join(body)))
    stats = {
        'lessons': sum(1 for mt in metas if re.match(r'^l\d+$', mt['sid'])),
        'appendix': sum(1 for mt in metas if not re.match(r'^l\d+$', mt['sid'])),
        'heads': len(re.findall(r'<h3', ''.join(body))) + len(re.findall(r'<h4', ''.join(body))),
        'tables': ''.join(body).count('<table'),
    }
    doc = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>دروسُ الإعراب — أربعةَ عشرَ درسًا مع الثوابتِ ومصفوفةِ المواضع</title>
<meta name="description" content="أربعةَ عشرَ درسًا مفصَّلًا: المبتدأ، الخبر، الفعل، الفاعل، المفعول، أسماء الإشارة، الأسماء الموصولة، العطف، التوكيد، البدل، النعت، الحال، التمييز، الإضافة — مع جمعِ الثوابت في آخر الملفِّ مصنَّفةً، وبيانِ جميع مواضع كلِّ درسٍ: الأساليب، والتقديم والتأخير، والحذف، والنواصب، والنواسخ، والتراكيب الخاصة.">
{style}
</head>
<body class="sheets">
<div class="toolbar no-print">
  <button onclick="document.body.classList.toggle('sheets');renderPages()">عرضٌ ورقيٌّ (ورقةٌ مقطَّعةٌ) / عرضٌ متَّصل</button>
  <button onclick="window.print()">طباعةٌ أو حفظٌ في ملفٍ مستقلٍّ</button>
  <span class="hint">قياسُ الورقةِ: ٢١ سم عرضًا × ٢٩٫٧ سم طولًا؛ وهوامشُها: ٢٫٥٤ سم أعلى وأسفلَ، ٣٫١٨ سم يمينًا ويسارًا — كصفحةِ المستنداتِ المعتادةِ.</span>
</div>
<header class="hero">
  <div class="hero-inner">
    <span class="badge">دروسٌ مفصَّلة · مواضعُ مطرَّدة · ثوابتُ مصنَّفة</span>
    <h1>دروسُ الإعرابِ الأربعةَ عشر</h1>
    <p class="sub">كلُّ درسٍ قائمٌ بنفسه: حدُّه، وأركانُه، وأحكامُه رقماً رقماً، وتقسيماتُه جداول، وأمثلةٌ مشكولةٌ مُعربة، ثمَّ <b>«مواضعُ الدرس»</b>: أين يقع هذا المبحثُ في الأساليب، وفي التقديمِ والتأخير، وفي الحذف، وفي النواصب، وفي النواسخ، وفي التراكيب الخاصة. وفي آخرِ الملفِّ <b>الثوابتُ</b> مصنَّفة، و<b>مصفوفةُ المواضع</b> لكلِّ الدروس في صفحةٍ واحدة.</p>
    <div class="hero-stats">
      <span>📚 {ar(stats['lessons'])} درسًا مفصَّلًا</span>
      <span>🧾 {ar(stats['appendix'])} ملاحقَ جامعة</span>
      <span>🗂️ {ar(stats['heads'])} مبحثًا فرعيًّا</span>
      <span>📐 {ar(stats['tables'])} جدولًا</span>
      <span>🧷 مواضعُ كلِّ درسٍ في ستةِ أبواب</span>
      <span>✅ ثوابتٌ مصنَّفةٌ في الختام</span>
      <span>🖋️ أمثلةٌ مشكولةٌ مُعربة</span>
      <span>🔎 بحثٌ في مصادرِ النحو والتراث</span>
    </div>
    <div class="hero-callout">
      <span class="big">﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ﴾</span>
      <span class="small" style="color:#d9e6de">نموذجٌ يُطبَّق في درسَي المبتدأ والخبر: جملةُ «الحَيُّ القَيُّومُ» خبرٌ لمبتدأ محذوفٍ وجوبًا، و«إلَّا» أداةُ حصر، و«هُوَ» ضميرٌ منفصلٌ في محلِّ رفعٍ مبتدأ.</span>
    </div>
  </div>
</header>
<div class="layout">
  <nav class="toc">
    <h4>الفهرس</h4>
    <a class="grp" href="#toc"><b>٭</b>الفهرسُ التفصيليّ</a>
{''.join(nav)}      <a class="grp" href="#matrix"><b>٭</b>مصفوفةُ المواضع</a>
  </nav>
  <main>
<section id="toc">
  <h2><span class="num">٭</span>الفهرسُ التفصيليّ</h2>
  <p>فهرسٌ بكلِّ درسٍ ومبحثِه — كلُّ عنوانٍ رابطٌ مباشر. وللقارئِ أن يعود إلى جدولِ المواضع في آخرِ كلِّ درس، ثمَّ إلى <a href="#matrix">مصفوفةِ المواضع الجامعة</a> التي تجمع الدروسَ الأربعةَ عشر في مقابل الأبوابِ الستة.</p>
  <ol class="idxlist">
{chr(10).join(idx)}
  </ol>
</section>
{''.join(body)}
<footer>
  <p>دروسُ الإعراب — وُضع هذا الملفُّ.self-contained: يعمل بلا إنترنت، وكلُّ رابطٍ داخليٍّ مُتحقَّقٌ منه. راجِعْه مع «الدليل الشامل في النحو العربي والبلاغة».</p>
</footer>
  </main>
</div>
</body>
</html>
'''
    doc = doc.replace('ملفُّ.self-contained', 'ملفٌّ قائمٌ بنفسه،')
    doc = doc.replace('</body>', "\n<script>\n" + ('''/* تقطيعُ المحتوى إلى أوراقٍ بحجمِ الورقةِ المعتادةِ (شاشةً)؛ والطباعةُ تُولِّي قواعدَ @page */
var PG={pw:21,ph:29.7,px:3.18,py:2.54},AR='٠١٢٣٤٥٦٧٨٩';
function arNum(n){return String(n).split('').map(function(c){return AR[+c]||c;}).join('');}
function mmToPx(x){return x*96/2.54;}
function unPages(){
  document.querySelectorAll('main > section').forEach(function(sec){
    var book=sec.querySelector(':scope > .book');
    if(!book)return;
    var sheets=[].slice.call(book.querySelectorAll(':scope > .sheet'));
    sheets.forEach(function(sh){
      while(sh.firstChild){book.parentNode.insertBefore(sh.firstChild,book);}
    });
    book.remove();
  });
}
function renderPages(){
  unPages();
  if(!document.body.classList.contains('sheets'))return;
  var inner=mmToPx(PG.ph)-2*mmToPx(PG.py)-10;
  document.querySelectorAll('main > section').forEach(function(sec){
    var kids=[].slice.call(sec.children).filter(function(el){
      return !el.classList.contains('book')&&!el.classList.contains('pager');
    });
    if(!kids.length)return;
    var pager=sec.querySelector(':scope > .pager');
    var book=document.createElement('div');book.className='book';
    var pages=[],cur=null;
    function newPage(){cur=document.createElement('div');cur.className='sheet';pages.push(cur);book.appendChild(cur);}
    newPage();
    kids.forEach(function(el){
      cur.appendChild(el);
      if(cur.scrollHeight>inner&&cur.children.length>1){cur.removeChild(el);newPage();cur.appendChild(el);}
    });
    if(pager)pages[pages.length-1].appendChild(pager);
    sec.appendChild(book);
    pages.forEach(function(p){
      if(p.scrollHeight>inner+8)p.classList.add('oversize');
    });
  });
  var all=[].slice.call(document.querySelectorAll('main .sheet'));
  all.forEach(function(p,i){
    p.setAttribute('data-page','دروسُ الإعراب — صفحةُ '+arNum(i+1)+' من '+arNum(all.length));
  });
}
var rT=null;
window.addEventListener('resize',function(){clearTimeout(rT);rT=setTimeout(renderPages,250);});
window.addEventListener('load',renderPages);
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(function(){renderPages();});}''') + '</script>\n</body>', 1)
    open(OUT, 'w', encoding='utf-8').write(doc)
    # تحقَّق
    from html.parser import HTMLParser
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    class P(HTMLParser):
        def __init__(s):
            super().__init__(convert_charrefs=True); s.st=[]; s.err=[]
        def handle_starttag(s,t,a):
            if t not in VOID: s.st.append((t,s.getpos()[0]))
        def handle_endtag(s,t):
            if t in VOID: return
            if s.st and s.st[-1][0]==t: s.st.pop()
            else: s.err.append(f'</{t}> سطر {s.getpos()[0]}')
    p=P(); p.feed(doc)
    for t,l in p.st: p.err.append(f'وسمٌ غيرُ مغلق <{t}> سطر {l}')
    ids=set(re.findall(r'id="([^"]+)"',doc))
    broken=[h for h in set(re.findall(r'href="#([^"]+)"',doc)) if h not in ids]
    # تطابق أعمدة الجداول
    mism=[]
    for tm in re.finditer(r'<table.*?</table>', doc, re.S):
        blk=tm.group(0)
        head=len(re.findall(r'<th[ >]',blk))
        active=[]                                   # صفوفٌ متبقّيةٌ لخلايا mمتدة
        for rm in re.finditer(r'<tr>(.*?)</tr>', blk, re.S):
            row=rm.group(1)
            cells=len(re.findall(r'<t[dh][ >]',row)) + len(active)
            active=[a-1 for a in active if a>1]
            active+= [int(x)-1 for x in re.findall(r'rowspan="(\d+)"', row) if int(x)>1]
            if head and cells and cells!=head:
                mism.append((head,cells,re.sub(r'\s+',' ',row)[:44]))
    print('KB:', round(len(doc.encode())/1024,1))
    print('أقسام:', doc.count('<section'), '| جداول:', doc.count('<table'), '| روابط الفهرس:', len(re.findall(r'<a href="#', ''.join(idx))))
    print('أخطاء الوسوم:', len(p.err), p.err[:4])
    print('روابط معطوبة:', broken[:6], len(broken))
    print('خلايا جداول غير متوافقة:', mism[:4], len(mism))
    print('أرقام لاتينية مرئية:', len(re.findall(r'[0-9]+', re.sub(r'<[^>]+>',' ',re.sub(r'<style.*?</style>|<script.*?</script>','',doc,flags=re.S)))))

main()
