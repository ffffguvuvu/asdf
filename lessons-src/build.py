#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بناء «دروس الإعراب» — يجمع أجزاء الدروس من lessons-src/ ويولِّد الشريط الجانبي
والفهرس التفصيلي آليًّا من عناوين h2/h3/h4، ثم يتحقَّق من الوسوم والروابط.
شغِّله من جذر المستودع:  python3 lessons-src/build.py
"""
import re, os, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paginate as PG

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



body.sheets .sheet.oversize{min-height:0}
body.sheets .sheet > section,body.sheets .sheet > section.cont,body.sheets .sheet > section.loose{
  background:none;border:none;box-shadow:none;border-radius:0;padding:0;margin:0}
body:not(.sheets) .book{display:block;max-width:none}
body:not(.sheets) .sheet{display:contents}
/* ——— نسخةُ القراءةِ: أسودُ على أبيضَ، بلا زخرفةٍ، وبالأوراقِ نفسِها ——— */
body.reading{background:#fff}
body.reading .sheet{background:#fff;border:none;box-shadow:none;border-radius:0;margin:0 auto;
  color:#111;font-size:var(--fsheet);line-height:var(--lh);text-align:justify;padding:calc(var(--py) + var(--foot)) var(--px)}
body.reading .sheet .phead{display:none}
body.reading .sheet .pnum{color:#555;font-size:10pt;bottom:1.05cm;border-top:none}
body.reading h1,body.reading h2,body.reading h3,body.reading h4,body.reading b,body.reading strong,
body.reading .tag,body.reading .kicker,body.reading .num,body.reading .lede b,body.reading a{color:#111}
body.reading section>h2,body.reading h2,body.reading h3,body.reading h4{border-bottom:none}
body.reading .box,body.reading .rule,body.reading .ex,body.reading .note,body.reading .warn,
body.reading .card,body.reading details.qa,body.reading ol.rules,body.reading ol.rules>li,
body.reading .irab,body.reading .lede,body.reading .hero,body.reading .hero-callout{
  background:#fff!important;color:#111!important;border:1px solid #cfcfcf!important;box-shadow:none!important}
body.reading .irab .stmt,body.reading .irab li,body.reading .irab b{color:#111!important}
body.reading .tag,body.reading .chip,body.reading .lbl{background:#f1f1f1!important;border:1px solid #cfcfcf!important;color:#333!important}
body.reading ol.rules>li:before{background:#f1f1f1!important;color:#111!important;border-inline-end:1px solid #cfcfcf!important}
body.reading th,body.reading td{border-color:#cfcfcf!important;color:#111!important}
body.reading table th{background:#f1f1f1!important}
body.reading table.pos td:first-child,body.reading table.matrix td:first-child,body.reading table.thab td:first-child{
  background:#f7f7f7!important;color:#111!important}
body.reading a{text-decoration:underline}
body.reading .badge,body.reading .hero-stats span,body.reading .hero-inner .sub,body.reading .small{color:#333!important}
body.reading .pager,body.reading nav.toc{display:none}
.book.paginating .sheet{min-height:0;box-shadow:none;border-color:transparent;margin-bottom:0}
body.sheets main > section > .pager{display:none}

body.sheets .sheet table.pos th,body.sheets .sheet table.pos td{min-width:0}
body.sheets .sheet .box .tag,body.sheets .sheet .rule .tag{margin:0 0 .35em}
body.sheets .sheet ol.rules{counter-reset:rl}
body.sheets .sheet .irab .stmt{display:block;margin:0 0 .35em;font-size:1.05em}
body.sheets .sheet ul,body.sheets .sheet ol{padding-inline-start:1.6em;margin:.25em 0 .55em}
body.sheets .sheet .idxlist{padding-inline-start:1.2em}
body.sheets .hero{position:relative}

body.sheets main:not(:has(> .book)){max-width:none;padding:0}
body.sheets main:not(:has(> .book)) > section{background:#fff;border:1px solid var(--line);border-radius:2px;
  box-shadow:0 4px 20px rgba(0,0,0,.10);padding:calc(var(--py) + var(--foot)) var(--px);margin:0 0 18px;
  min-height:var(--ph);max-width:var(--pw);font-size:var(--fsheet);line-height:var(--lh);text-align:justify}
body.sheets .sheet .pnum,body.sheets .sheet .phead{position:absolute;inset-inline:var(--px);text-align:center;
  margin:0;font-family:inherit;color:var(--muted);font-weight:600;letter-spacing:.15px;line-height:1.4}
body.sheets .sheet .pnum{bottom:calc(var(--py) - 1.35cm);font-size:9pt}
body.sheets .sheet .phead{top:calc(var(--py) - 1.55cm);font-size:8.6pt;border-bottom:.6pt solid var(--line);padding-bottom:.16cm}
body.sheets .sheet .pnote{font-size:8.4pt;color:var(--muted);margin:.4em 0 0}
body.sheets .hero .pnum{position:absolute;bottom:calc(var(--py) - 1.35cm);inset-inline:var(--px);text-align:center;
  margin:0;font-size:9pt;color:#cfe0d9}
body:not(.sheets) .phead,body:not(.sheets) .pnum,body:not(.sheets) .pnote{display:none}
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
  body.sheets .sheet .phead{display:none}
  body.sheets .sheet .pnum{position:static;inset-inline:auto;margin:1.05em 0 0;padding:0;border:none}
  body.sheets .sheet,.sheet *{orphans:3;widows:3}
  body.sheets .sheet table{font-size:9pt}
  body.sheets .sheet th,body.sheets .sheet td{padding:.24em .34em}
  .tblwrap{overflow:visible}
  table{min-width:0}
  thead{display:table-header-group}
  .irab{background:#123a34!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  body.reading .irab,body.reading .box,body.reading .rule,body.reading .ex,body.reading .note,body.reading .warn,body.reading details.qa{background:#fff!important;color:#111!important}
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

    toc_html = ('<section id="toc">\n'
                '  <h2><span class="num">٭</span>الفهرسُ التفصيليّ</h2>\n'
                '  <p>فهرسٌ بكلِّ درسٍ ومبحثِه — كلُّ عنوانٍ رابطٌ مباشر. وللقارئِ أن يعود إلى جدولِ المواضع في آخرِ كلِّ درس، '
                'ثمَّ إلى <a href="#matrix">مصفوفةِ المواضع الجامعة</a> التي تجمع الدروسَ الأربعةَ عشر في مقابل الأبوابِ الستة.</p>\n'
                '  <ol class="idxlist">\n' + chr(10).join(idx) + '\n  </ol>\n</section>')
    foot_html = ('<footer>\n  <p>دروسُ الإعراب — وُضع هذا الملفُّ.self-contained: يعمل بلا إنترنت، وكلُّ رابطٍ داخليٍّ '
                 'مُتحقَّقٌ منه. راجِعْه مع «الدليل الشامل في النحو العربي والبلاغة».</p>\n</footer>')
    main_src = toc_html + '\n' + ''.join(body) + '\n' + foot_html
    titles = {(mt['sid'] or ''): ((mt['num'] or '') + ' ' + (mt['title'] or '')).strip() for mt in metas}
    sheets_html, total_pages = PG.paginate(main_src, titles, cover=True)
    pages_html = '<div class="book">\n' + sheets_html + '\n</div>'
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
  <button onclick="document.body.classList.toggle('sheets')">عرضٌ ورقيٌّ (أوراقٌ مثبَّتةٌ) / عرضٌ متَّصلٌ</button>
  <button onclick="setReading(!document.body.classList.contains('reading'))">نسخةُ قراءةٍ (أسودُ على أبيضَ)</button>
  <button onclick="window.print()">طباعةٌ أو حفظٌ في ملفٍ مستقلٍّ</button>
  <span class="hint">مقاسُ الورقةِ: ٢١ سم × ٢٩٫٧ سم؛ وهوامشُها ٢٫٥٤ سم أعلى وأسفلَ و٣٫١٨ سم جانبًا؛ الخطُّ ١١٫٥ نقطةً بسطرٍ ١٫٩٥ وكتابةٍ مُبرَّرةٍ. التقطيعُ حُفِرَ وقتَ البناءِ لا وقتَ العرضِ: {ar(total_pages)} صفحةً، برقمٍ متَّصلٍ وعنوانٍ جارٍ أعلى كلِّ صفحةٍ — فالشاشةُ والطباعةُ ونسخةُ القراءةِ صفحةٌ واحدةٌ بكلماتٍ واحدةٍ.</span>
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
      <span>📄 {ar(total_pages)} صفحةً مثبَّتةَ التقطيعِ</span>
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
  <p class="pnum">صفحةُ ١ من {ar(total_pages)}</p>
</header>
<div class="layout">
  <nav class="toc">
    <h4>الفهرس</h4>
    <a class="grp" href="#toc"><b>٭</b>الفهرسُ التفصيليّ</a>
{''.join(nav)}      <a class="grp" href="#matrix"><b>٭</b>مصفوفةُ المواضع</a>
  </nav>
  <main>
{pages_html}
  </main>
</div>
</body>
</html>
'''
    doc = doc.replace('ملفُّ.self-contained', 'ملفٌّ قائمٌ بنفسه،')
    READ_TPL = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>دروسُ الإعراب — نسخةُ القراءةِ</title>
<style>
:root{--pw:21cm;--ph:29.7cm;--px:3.18cm;--py:2.54cm}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#111;direction:rtl;
  font:11.5pt/1.95 "Amiri","Noto Naskh Arabic","Scheherazade New",serif}
main{max-width:var(--pw);margin:0 auto}
.sheet{position:relative;width:var(--pw);min-height:var(--ph);padding:var(--py) var(--px);
  margin:0 auto;text-align:justify;page-break-after:always;break-after:page}
.sheet:last-of-type{page-break-after:auto;break-after:auto}
.phead{display:none}
.pnum{position:absolute;bottom:1.05cm;inset-inline:var(--px);text-align:center;margin:0;font-size:.8em;color:#555}
.pnote{font-size:.8em;color:#555;margin:.4em 0 0}
.cover{display:block}
.hero-inner{max-width:none;text-align:justify}
.hero-inner h1{font-size:1.9em;text-align:center;margin:.5em 0}
.hero-inner .sub{font-size:.95em;text-align:center;color:#333}
.badge,.hero-stats span{display:inline-block;border:.6pt solid #bbb;border-radius:3px;padding:0 .5em;
  font-size:10pt;margin:.15em;color:#333}
.hero-stats{display:block;margin:.8em 0;text-align:center}
.hero-callout{border:.8pt solid #bbb;border-radius:3px;padding:.6em .8em;margin:1em 0;text-align:center}
.hero-callout .big{display:block;font-size:1.12em;margin-bottom:.3em}
h1{font-size:1.9em;text-align:center;margin:1.2em 0 .5em}
h2{font-size:1.45em;margin:0 0 .7em;border-bottom:.8pt solid #999;padding-bottom:.25em}
h3{font-size:1.22em;margin:1.1em 0 .35em}
h4{font-size:1.08em;margin:1em 0 .3em}
p{margin:.25em 0 .6em}
ul,ol{padding-inline-start:1.5em;margin:.3em 0 .6em}
table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:.8em;line-height:1.5;margin:.5em 0}
th,td{border:.6pt solid #999;padding:.3em .4em;text-align:right;font-size:inherit;overflow-wrap:anywhere}
th{background:#f2f2f2}
.box,.rule,.ex,.note,.warn,.card,.lede,.irab,details.qa,ol.rules{border:.8pt solid #bbb;border-radius:3px;
  padding:.5em .7em;margin:.5em 0;background:#fff}
.tag,.chip,.lbl{display:inline-block;border:.6pt solid #bbb;background:#f2f2f2;border-radius:3px;
  padding:0 .4em;font-size:.82em;font-weight:700}
.num{font-weight:700}
.small,.subsub,.idxsub{font-size:.9em}
a{color:#111;text-decoration:none}
.irab .stmt{display:block;font-size:11.5pt;margin:0 0 .3em}
ol.rules{list-style:none;padding:0;counter-reset:rl}
ol.rules>li{counter-increment:rl;position:relative;padding:.25em 2.6em .25em .5em;
  border-bottom:.5pt solid #ddd;list-style:none}
ol.rules>li:last-child{border-bottom:none}
ol.rules>li:before{content:counter(rl,arabic-indic);position:absolute;inset-inline-start:0;font-weight:700}
.tblwrap{overflow:visible}
img{max-width:100%}
@page{size:A4;margin:var(--py) var(--px)}
</style>
</head>
<body>
<main>
@@COVER@@
@@PAGES@@
</main>
</body>
</html>
"""
    hero_html = re.search(r'(?s)<header class="hero">.*?</header>', doc)
    hero_inner = re.sub(r'(?s)\s*</?header[^>]*>\s*', '', hero_html.group(0)) if hero_html else ''
    hero_inner = re.sub(r'(?s)\s*<p class="pnum">.*?</p>', '', hero_inner)   # يتولّاها الغلافُ أدناه
    cover = ('<div class="sheet cover">\n' + hero_inner +
             '\n  <p class="pnum">صفحةُ ١ من ' + ar(total_pages) + '</p>\n  </div>')
    read_doc = (READ_TPL
                .replace('@@TOTAL@@', ar(total_pages))
                .replace('@@PAGES@@', pages_html)
                .replace('@@COVER@@', cover))
    read_doc = read_doc.replace('ملفُّ.self-contained', 'ملفٌّ قائمٌ بنفسه،')
    open(os.path.join(HERE, '..', 'arabic-reading.html'), 'w', encoding='utf-8').write(read_doc)
    print('نسخةُ القراءةِ KB:', round(len(read_doc.encode()) / 1024, 1), '| أوراقٌ:', read_doc.count('<div class="sheet'))
    DOC_JS = '<script>\n' + (
        'function setReading(on){var c=document.body.classList;'
        'if(on){c.add("reading");c.add("sheets");}else{c.remove("reading");}}\n'
        'window.setReading=setReading;\n'
        '</script>'
    )
    doc = doc.replace('</body>', "\n" + DOC_JS + "\n</body>", 1)
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
