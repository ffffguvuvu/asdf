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

/* ——— وضعُ الورقةِ: مقاسٌ وهامشٌ وترقيمٌ وتناسقُ خطٍّ ——— */
:root{--pw:21cm;--ph:29.7cm;--px:3.18cm;--py:2.54cm;--fsheet:11.5pt;--lh:1.95;--foot:1.05cm}
.toolbar{position:sticky;top:0;z-index:60;display:flex;gap:8px;align-items:center;justify-content:center;
  flex-wrap:wrap;padding:8px 12px;background:rgba(250,247,240,.94);border-bottom:1px solid var(--line);
  backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px)}
.toolbar button{font:inherit;font-size:14px;font-weight:700;color:var(--ink2);background:#fffdfa;
  border:1px solid var(--line);border-radius:9px;padding:6px 14px;cursor:pointer}
.toolbar button:hover{border-color:var(--gold);color:var(--green)}
.toolbar button[aria-pressed="true"]{background:var(--green);color:#f6f2e8;border-color:var(--green)}
.toolbar .hint{font-size:13px;color:var(--muted);max-width:72ch}
.irab ul{padding-inline-start:22px;margin:0}
.irab .alt{color:#cfe6dd}
body.sheets{background:#e7e4dc}
body.sheets .layout{display:block;max-width:none;padding:0 0 28px;margin:0}
body.sheets nav.toc{display:none}
body.sheets main{max-width:var(--pw);margin:0 auto;padding:16px 0 0}
body.sheets main > section{background:none;border:none;box-shadow:none;border-radius:0;padding:0;margin:0}
body.sheets .book{display:block;max-width:var(--pw);margin:0 auto}
body.sheets .sheet{position:relative;background:#fff;border:1px solid var(--line);border-radius:2px;
  box-shadow:0 4px 20px rgba(0,0,0,.10);box-sizing:border-box;min-height:var(--ph);
  padding:calc(var(--py) + var(--foot)) var(--px) calc(var(--py) + var(--foot));margin:0 0 18px;
  font-size:var(--fsheet);line-height:var(--lh);text-align:justify;color:var(--ink);
  font-family:inherit;font-feature-settings:"liga" 1;text-justify:auto}
/* تناسقُ الكتابةِ مع الورقةِ: كلُّ العناصرِ تُحاسَبُ على أساسِ قياسِ الصفحةِ */
body.sheets .sheet p,body.sheets .sheet li,body.sheets .sheet td,body.sheets .sheet th,body.sheets .sheet summary,
body.sheets .sheet .box,body.sheets .sheet .card,body.sheets .sheet .irab,body.sheets .sheet .stmt,
body.sheets .sheet .lede,body.sheets .sheet .idxlist,body.sheets .sheet .idxsub,body.sheets .sheet .subsub,
body.sheets .sheet .chip,body.sheets .sheet .kicker,body.sheets .sheet .qa,body.sheets .sheet .ar,
body.sheets .sheet small,body.sheets .sheet a,body.sheets .sheet b,body.sheets .sheet i,body.sheets .sheet span{
  font-family:inherit;line-height:inherit;font-size:1em}
body.sheets .sheet ol.rules > li{font-size:.98em}
body.sheets .sheet .badge,body.sheets .sheet .tag{font-family:inherit}
body.sheets .sheet .hero-inner{font-size:1em}
body.sheets .sheet:after{content:attr(data-page);position:absolute;bottom:calc(var(--py) - 1.35cm);
  inset-inline:var(--px);text-align:center;font-size:9pt;line-height:1.4;font-weight:600;
  color:var(--muted);font-family:inherit;letter-spacing:.15px}
body.sheets .sheet:before{content:attr(data-head);position:absolute;top:calc(var(--py) - 1.55cm);
  inset-inline:var(--px);text-align:center;font-size:8.6pt;line-height:1.35;color:var(--muted);
  border-bottom:.6pt solid var(--line);padding-bottom:.16cm;font-family:inherit}
body.sheets .sheet.cover:before,body.sheets .sheet.cover:after{display:none}
body.sheets .sheet.oversize{min-height:0}
.book.paginating .sheet{min-height:0;box-shadow:none;border-color:transparent;margin-bottom:0}
body.sheets main > section > .pager{display:none}
body.sheets .sheet.oversize:after{content:attr(data-page) " · ورقةٌ تجاوزتْ مِقدارَها لجدولٍ كبيرٍ"}
body.sheets .sheet table.pos th,body.sheets .sheet table.pos td{min-width:0}
body.sheets .sheet .box .tag,body.sheets .sheet .rule .tag{margin:0 0 .35em}
body.sheets .sheet ol.rules{counter-reset:rl}
body.sheets .sheet .irab .stmt{display:block;margin:0 0 .35em;font-size:1.05em}
body.sheets .sheet ul,body.sheets .sheet ol{padding-inline-start:1.6em;margin:.25em 0 .55em}
body.sheets .sheet .idxlist{padding-inline-start:1.2em}
body.sheets .hero{position:relative}
body.sheets .hero:after{content:attr(data-page);position:absolute;bottom:calc(var(--py) - 1.35cm);
  inset-inline:var(--px);text-align:center;font-size:9pt;color:#cfe0d9;font-family:inherit}
body.sheets main:not(:has(> .book)){max-width:none;padding:0}
body.sheets main:not(:has(> .book)) > section{background:#fff;border:1px solid var(--line);border-radius:2px;
  box-shadow:0 4px 20px rgba(0,0,0,.10);padding:calc(var(--py) + var(--foot)) var(--px);margin:0 0 18px;
  min-height:var(--ph);max-width:var(--pw);font-size:var(--fsheet);line-height:var(--lh);text-align:justify}
body.sheets .sheet > :first-child{margin-top:0}
body.sheets .sheet > :last-child{margin-bottom:0}
body.sheets .sheet h1{font-size:2.05em;line-height:1.5;text-align:center}
body.sheets .sheet h2{font-size:1.5em;line-height:1.5;margin:.3em 0 .55em;text-align:center}
body.sheets .sheet h3{font-size:1.2em;line-height:1.5;margin:1.05em 0 .4em}
body.sheets .sheet h4{font-size:1.05em;line-height:1.5;margin:.95em 0 .35em}
body.sheets .sheet p,body.sheets .sheet li{font-size:1em;margin:.3em 0 .6em}
body.sheets .sheet .box,body.sheets .sheet .irab,body.sheets .sheet .card{font-size:.97em;
  padding:.7em .9em;border-radius:.45em;margin:.55em 0}
body.sheets .sheet .small,body.sheets .sheet small{font-size:.87em}
body.sheets .sheet .tag{font-size:.8em}
body.sheets .sheet ol.rules{margin:.5em 0}
body.sheets .sheet ol.rules > li{padding:.5em 3em .5em .8em;font-size:.97em;border-radius:.45em}
body.sheets .sheet ol.rules > li:before{width:2.1em;font-size:1.05em}
body.sheets .sheet .tblwrap{overflow:visible;margin:.6em 0}
body.sheets .sheet table{width:100%;min-width:0;table-layout:fixed;font-size:.8em;line-height:1.62}
body.sheets .sheet th,body.sheets .sheet td{padding:.34em .42em;overflow-wrap:anywhere;font-size:1em}
body.sheets .sheet table.pos th,body.sheets .sheet table.pos td{font-size:.92em}
body.sheets .sheet .pager{margin:.9em 0 0;padding:.5em .8em;justify-content:space-between;font-size:.9em}
body.sheets .sheet .chip{font-size:.86em;padding:.1em .55em}
body.sheets .sheet details.qa > summary{padding:.55em .9em;font-size:.95em}
body.sheets .sheet .grid2{grid-template-columns:repeat(auto-fit,minmax(6.5em,1fr));gap:.55em}
body.sheets .hero{max-width:var(--pw);min-height:var(--ph);margin:16px auto 18px;padding:6cm var(--px) 3cm;
  box-sizing:border-box;border-radius:2px;border:1px solid var(--line);box-shadow:0 4px 20px rgba(0,0,0,.10);
  display:grid;place-items:center}
body.sheets .hero-inner{max-width:none;text-align:justify}
body.sheets .hero-inner > p.sub{text-align:justify}
body.sheets .hero-stats{justify-content:center;flex-wrap:wrap}
@page{size:A4;margin:var(--py) var(--px)}
@media print{
  .toolbar{display:none!important}
  body,body.sheets{background:#fff}
  body.sheets .layout,body.sheets main,body.sheets .book{max-width:none;margin:0;padding:0;display:block}
  body.sheets .hero{max-width:none;min-height:0;margin:0;padding:5cm 0 1cm;border:none;border-radius:0;
    box-shadow:none;page-break-after:always;break-after:print;
    background:#0d3b34!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  body.sheets main > section{padding:0;margin:0}
  body.sheets .sheet{border:none;box-shadow:none;border-radius:0;margin:0;min-height:0;
    padding:calc(var(--foot) / 2) 0 0;box-sizing:border-box;page-break-after:always;break-after:print}
  body.sheets .sheet:last-of-type{page-break-after:auto;break-after:auto}
  body.sheets .sheet:before{display:none}
  body.sheets .sheet:after{position:static;inset-inline:auto;margin:1.05em 0 0;padding:0;border:none}
  body.sheets .sheet,.sheet *{orphans:3;widows:3}
  body.sheets .sheet table{font-size:9pt}
  body.sheets .sheet th,body.sheets .sheet td{padding:.24em .34em}
  .tblwrap{overflow:visible}
  table{min-width:0}
  thead{display:table-header-group}
  .irab{background:#123a34!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .pager,.no-print{display:none!important}
  section{box-shadow:none;border:none;break-inside:auto}
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
  <button onclick="document.body.classList.toggle('each-lesson');renderPages()">كلُّ درسٍ في صفحةٍ مستقلةٍ</button>
  <button onclick="window.print()">طباعةٌ أو حفظٌ في ملفٍ مستقلٍّ</button>
  <span class="hint">قياسُ الورقةِ: ٢١ سم عرضًا × ٢٩٫٧ سم طولًا؛ وهوامشُها: ٢٫٥٤ سم أعلى وأسفلَ، ٣٫١٨ سم يمينًا ويسارًا. الخطُّ مضبوطٌ على ١١٫٥ نقطةً بمسافةِ سطرٍ ١٫٩٥، والكتابةُ مُبرَّرةٌ؛ والمحتوى مُدمَجٌ في أوراقٍ متَّصلةٍ تُرقَّمُ «صفحةُ كذا من كذا» مع عنوانٍ جارٍ أعلى كلِّ ورقةٍ.</span>
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
    JS = r'''<script>
/* تقطيعٌ متَّصلٌ إلى أوراقٍ بمقاسِ الورقةِ، مع ترقيمٍ متَّصلٍ وعنوانٍ جارٍ ومنعِ اليتيمِ */
var PG={pw:21,ph:29.7,px:3.18,py:2.54,foot:1.05,safe:18},AR='\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669';
function arNum(n){return String(n).split('').map(function(c){return AR[+c]||c;}).join('');}
function mmToPx(x){return x*96/2.54;}
function capPx(){return mmToPx(PG.ph)-2*mmToPx(PG.py)-2*mmToPx(PG.foot)-PG.safe;}
function one(s){return (s||'').replace(/\s+/g,' ').trim();}
var FALLBACK={toc:'فهرسُ الدروسِ',thawat:'ثوابتُ المواضعِ',thawat2:'بوّاباتُ الأبوابِ',matrix:'مصفوفةُ المواضعِ',sources:'المصادرُ والمنهجيةُ'};
function titleOf(sec){
  var t='';
  if(sec.id&&FALLBACK[sec.id]){t=FALLBACK[sec.id];}
  else{var h=sec.querySelector('h2');if(h){t=one(h.textContent);t=t.replace(/\s+/g,' ');t=t.replace(/([\u0660-\u0669]+)[\s\u00a0]*(?=[\u0621-\u064A])/,'$1 ');if(t.length>62)t=t.slice(0,62)+'…';}}
  return t||'دروسُ الإعرابِ';
}
function unPages(){
  var book=document.querySelector('main > .book');
  if(book){
    var groups={},order=[];
    [].slice.call(book.querySelectorAll(':scope > .sheet')).forEach(function(sh){
      [].slice.call(sh.children).forEach(function(el){
        var sid=el.getAttribute('data-sid')||'*';
        if(!groups[sid]){groups[sid]=[];order.push(sid);}
        groups[sid].push(el);el.removeAttribute('data-sid');
      });
    });
    order.forEach(function(sid){
      var host=(sid==='*')?document.querySelector('main'):document.getElementById(sid);
      if(!host)return;
      groups[sid].forEach(function(el){host.appendChild(el);});
    });
    if(book.parentNode)book.parentNode.removeChild(book);
  }
  var hero=document.querySelector('header.hero');
  if(hero){hero.removeAttribute('data-page');}
}
function renderPages(){
  unPages();
  if(!document.body.classList.contains('sheets'))return;
  var main=document.querySelector('main');if(!main)return;
  var cap=capPx();
  var book=document.createElement('div');book.className='book paginating';
  var each=document.body.classList.contains('each-lesson');
  var sheets=[],cur=null;
  function openSheet(){cur=document.createElement('div');cur.className='sheet';sheets.push(cur);book.appendChild(cur);return cur;}
  openSheet();
  function place(el,title){
    if(cur.children.length){
      cur.appendChild(el);
      if(cur.scrollHeight>cap){cur.removeChild(el);openSheet();}
    }
    cur.appendChild(el);
    if(!cur.getAttribute('data-head'))cur.setAttribute('data-head',title);
    if(cur.scrollHeight>cap)cur.classList.add('oversize');
  }
  [].slice.call(main.children).forEach(function(box){
    if(box.classList.contains('book'))return;
    if(box.tagName==='SECTION'){
      var sid=box.id||'*',t=titleOf(box);
      if(each&&cur.children.length)openSheet();
      [].slice.call(box.children).forEach(function(el){
        if(el.classList.contains('book')||el.classList.contains('pager'))return;
        if(sid!=='*')el.setAttribute('data-sid',sid);
        place(el,t);
      });
    }else{
      box.setAttribute('data-sid','*');
      place(box,'خاتمةُ الملفِ');
    }
  });
  for(var i=0;i<sheets.length-1;i++){
    var last=sheets[i].lastElementChild;
    if(last&&/^H[1-4]$/.test(last.tagName)){
      sheets[i].removeChild(last);
      sheets[i+1].insertBefore(last,sheets[i+1].firstElementChild);
      if(sheets[i+1].scrollHeight>cap)sheets[i+1].classList.add('oversize');
    }
  }
  if(!sheets[0].children.length&&sheets.length>1){book.removeChild(sheets[0]);sheets.shift();}
  main.appendChild(book);
  void book.offsetWidth;
  book.classList.remove('paginating');
  var hero=document.querySelector('header.hero');
  var first=hero?2:1,total=sheets.length+(hero?1:0);
  if(hero)hero.setAttribute('data-page','صفحةُ ١ من '+arNum(total));
  sheets.forEach(function(s,i){
    s.setAttribute('data-page','صفحةُ '+arNum(i+first)+' من '+arNum(total));
    if(!s.getAttribute('data-head'))s.setAttribute('data-head','دروسُ الإعرابِ');
  });
}
var rT=null;
window.addEventListener('resize',function(){clearTimeout(rT);rT=setTimeout(renderPages,250);});
window.addEventListener('load',renderPages);
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(function(){renderPages();});}
</script>'''
    doc = doc.replace('</body>', "\n" + JS + "\n</body>", 1)
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
