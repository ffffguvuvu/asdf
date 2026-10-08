# -*- coding: utf-8 -*-
"""يبني صفحة «مرجع القواعد النحوية المفصّل» من azhar/nahw.py."""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "azhar"))

import nahw  # noqa: E402
import marwa  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "arabic-grammar-rules.html")

_TASH = re.compile("[\u0617-\u061a\u064b-\u0652\u0670\u0640]")
_PUNCT = re.compile("[«»\"'(),.:;!?؟\\-—–\\[\\]/]")
_WS = re.compile(r"\s+")


def norm(s):
    s = _TASH.sub("", s)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"),
                 ("ة", "ه"), ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    s = _PUNCT.sub(" ", s)
    return _WS.sub(" ", s).strip()


def ad(n):
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def esc(s):
    return html.escape(str(s), quote=True)


def rule_html(idx, r):
    parts = []
    bits = [r["t"], r["lead"]]
    extra = bool(r.get("extra"))
    if extra:
        bits.append("زيادة على الفيديوهات قاعدة إضافية لم تُشرح في الفيديو")

    parts.append(
        '<h3 class="rt"><span class="num">%s</span>'
        '<span class="ttl">%s</span>%s'
        '<button type="button" class="tg" aria-expanded="true">طيّ</button></h3>'
        % (ad(idx), esc(r["t"]),
           '<span class="ex" title="قاعدة لم تُشرح في الفيديوهات">'
           'زيادة على الفيديوهات</span>' if extra else ''))

    body = ['<div class="bd">']
    body.append('<p class="lead">%s</p>' % esc(r["lead"]))

    for head, items in r.get("sec", []):
        bits.append(head)
        bits.extend(items)
        body.append('<div class="sec"><h4>%s</h4><ul>%s</ul></div>' % (
            esc(head), "".join("<li>%s</li>" % esc(x) for x in items)))

    tbl = r.get("tbl")
    if tbl:
        heads, rows = tbl
        bits.extend(heads)
        for row in rows:
            bits.extend(row)
        body.append(
            '<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % ("".join("<th>%s</th>" % esc(h) for h in heads),
               "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(c) for c in row)
                       for row in rows)))

    shw = r.get("shw", [])
    if shw:
        rows = []
        for text, srcname, face in shw:
            bits.extend([text, srcname, face])
            rows.append(
                '<li><span class="txt">%s</span>'
                '<span class="ref">%s</span>'
                '<span class="face">وجه الاستشهاد: %s</span></li>'
                % (esc(text), esc(srcname), esc(face)))
        body.append('<div class="box shw"><h4>الشواهد</h4><ul>%s</ul></div>'
                    % "".join(rows))

    erab = r.get("erab", [])
    if erab:
        rows = []
        for sample, detail in erab:
            bits.extend([sample, detail])
            rows.append('<li><span class="smp">%s</span>'
                        '<span class="det">%s</span></li>'
                        % (esc(sample), esc(detail)))
        body.append('<div class="box erab"><h4>نماذج إعرابية</h4><ul>%s</ul></div>'
                    % "".join(rows))

    tan = r.get("tanbih", [])
    if tan:
        bits.extend(tan)
        body.append('<div class="box tan"><h4>تنبيهات وفروق دقيقة</h4><ul>%s</ul></div>'
                    % "".join("<li>%s</li>" % esc(x) for x in tan))

    src = r.get("src", [])
    if src:
        bits.extend(src)
        body.append('<p class="src"><b>مراجع الباب:</b> %s</p>'
                    % esc(" · ".join(src)))

    vids = sorted(set(r.get("v", [])))
    if extra and not vids:
        body.append('<p class="vids nov">هذه القاعدة <b>زيادة على ما ورد في الفيديوهات</b>'
                    ' — أُضيفت استكمالًا للباب من كتب النحو المذكورة أعلاه.</p>')
    if vids:
        chips = "".join(
            '<a class="vc" href="%s" target="_blank" rel="noopener">فيديو %s</a>'
            % (esc(marwa.url(n)), ad(n)) for n in vids)
        body.append('<p class="vids"><b>في الفيديوهات:</b> %s</p>' % chips)

    body.append("</div>")
    parts.append("".join(body))

    return '<article class="rule" data-x="%s" data-s="%s">%s</article>' % (
        "1" if extra else "0", esc(norm(" ".join(bits))), "".join(parts))


def build():
    by_ch = {}
    for i, r in enumerate(nahw.R, 1):
        by_ch.setdefault(r["ch"], []).append((i, r))

    nav, main = [], []
    n_shw = sum(len(r.get("shw", [])) for r in nahw.R)
    n_erab = sum(len(r.get("erab", [])) for r in nahw.R)
    n_tbl = sum(1 for r in nahw.R if r.get("tbl"))
    n_extra = sum(1 for r in nahw.R if r.get("extra"))

    for ci, (cid, ctitle, cintro) in enumerate(nahw.CHAPTERS, 1):
        items = by_ch.get(cid, [])
        if not items:
            continue
        nav.append(
            '<li><a href="#%s" data-ch="%s"><span class="cn">%s</span>'
            '<span class="cl">%s</span><span class="cc">%s</span></a></li>'
            % (cid, cid, ad(ci), esc(ctitle), ad(len(items))))
        main.append(
            '<section class="chap" id="%s"><h2><span class="cn">الباب %s</span>%s</h2>'
            '<p class="intro">%s</p>%s</section>'
            % (cid, ad(ci), esc(ctitle), esc(cintro),
               "".join(rule_html(i, r) for i, r in items)))

    css = """
:root{--bg:#f6f7f9;--pa:#fff;--ink:#16202c;--mut:#5b6b7c;--line:#e3e8ee;
--acc:#0f766e;--acc2:#0d5c56;--warm:#9a3412;--gold:#92400e;--soft:#eef5f4}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:96px}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.95;
font-family:"Noto Naskh Arabic","Amiri","Scheherazade New","Traditional Arabic",
"Segoe UI",Tahoma,sans-serif;font-size:17px}
a{color:var(--acc)}
.top{position:sticky;top:0;z-index:30;background:linear-gradient(135deg,#0f766e,#134e4a);
color:#fff;padding:14px 20px;box-shadow:0 2px 14px rgba(0,0,0,.18)}
.top h1{margin:0 0 2px;font-size:22px;letter-spacing:.2px}
.top .sub{margin:0;opacity:.9;font-size:13.5px}
.bar{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-top:11px}
.bar input{flex:1 1 280px;min-width:200px;padding:9px 13px;border:0;border-radius:9px;
font:inherit;font-size:15px}
.btn{background:rgba(255,255,255,.17);color:#fff;border:1px solid rgba(255,255,255,.38);
padding:8px 14px;border-radius:9px;cursor:pointer;font:inherit;font-size:14px}
.btn:hover{background:rgba(255,255,255,.3)}
.btn.on{background:#fbbf24;color:#4a2c00;border-color:#fbbf24;font-weight:700}
.stat{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.stat span{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.26);
border-radius:999px;padding:3px 12px;font-size:12.5px}
.wrap{display:grid;grid-template-columns:300px 1fr;gap:22px;max-width:1280px;
margin:20px auto;padding:0 18px;align-items:start}
.nav{position:sticky;top:188px;max-height:calc(100vh - 210px);overflow:auto;
background:var(--pa);border:1px solid var(--line);border-radius:14px;padding:14px}
.nav h2{margin:0 0 10px;font-size:15px;color:var(--acc2);
border-bottom:2px solid var(--soft);padding-bottom:7px}
.nav ul{list-style:none;margin:0;padding:0}
.nav a{display:flex;gap:8px;align-items:baseline;padding:7px 9px;border-radius:8px;
text-decoration:none;color:var(--ink);font-size:14.5px;line-height:1.6}
.nav a:hover{background:var(--soft)}
.nav .cn{color:var(--acc);font-weight:700;font-size:12.5px;min-width:17px}
.nav .cl{flex:1}
.nav .cc{color:var(--mut);font-size:12px}
.chap{background:var(--pa);border:1px solid var(--line);border-radius:16px;
padding:20px 22px;margin-bottom:22px}
.chap>h2{margin:0 0 6px;font-size:21px;color:var(--acc2);display:flex;gap:11px;
align-items:baseline;flex-wrap:wrap}
.chap>h2 .cn{background:var(--acc);color:#fff;font-size:12.5px;padding:3px 11px;
border-radius:999px;font-weight:400}
.intro{margin:0 0 16px;color:var(--mut);font-size:15px;
border-inline-start:3px solid var(--soft);padding-inline-start:12px}
.rule{border:1px solid var(--line);border-radius:13px;margin-bottom:15px;overflow:hidden;
background:#fcfdfd}
.rt{margin:0;display:flex;gap:10px;align-items:center;padding:12px 15px;
background:var(--soft);font-size:17.5px;color:var(--acc2)}
.rt .num{background:var(--acc);color:#fff;border-radius:8px;min-width:30px;
text-align:center;font-size:13.5px;padding:2px 7px;font-weight:700}
.rt .ttl{flex:1}
.rt .ex{background:#fef3c7;color:#92400e;border:1px solid #fcd34d;border-radius:999px;
padding:2px 10px;font-size:11.5px;font-weight:700;white-space:nowrap}
.rule[data-x="1"]{border-color:#fcd34d;box-shadow:0 1px 10px rgba(146,64,14,.07)}
.rule[data-x="1"] .rt{background:#fffbeb;color:var(--gold)}
.rule[data-x="1"] .rt .num{background:var(--gold)}
.tg{background:#fff;border:1px solid var(--line);border-radius:7px;padding:3px 11px;
cursor:pointer;font:inherit;font-size:12.5px;color:var(--mut)}
.bd{padding:14px 16px}
.rule.sm .bd{display:none}
.lead{margin:0 0 13px;background:#fffbea;border:1px solid #fde68a;
border-inline-start:4px solid var(--gold);border-radius:9px;padding:10px 13px;font-size:16px}
.sec{margin:0 0 12px}
.sec h4{margin:0 0 5px;font-size:15px;color:var(--acc2)}
.sec ul,.box ul{margin:0;padding-inline-start:20px}
.sec li{margin-bottom:3px}
.tw{overflow:auto;margin:0 0 13px}
table{border-collapse:collapse;width:100%;font-size:14.5px;background:#fff}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:right;vertical-align:top}
th{background:var(--soft);color:var(--acc2);font-weight:700;white-space:nowrap}
.box{border-radius:10px;padding:11px 14px;margin:0 0 12px;border:1px solid var(--line)}
.box h4{margin:0 0 7px;font-size:14.5px}
.shw{background:#f3f8f7;border-color:#cfe6e2}
.shw h4{color:var(--acc2)}
.shw li{margin-bottom:9px}
.shw .txt{display:block;font-size:18px;color:#0b3b36;line-height:2.1}
.shw .ref{display:inline-block;background:#fff;border:1px solid #cfe6e2;border-radius:999px;
padding:1px 10px;font-size:12px;color:var(--mut);margin:3px 0}
.shw .face{display:block;font-size:14.5px;color:var(--mut)}
.erab{background:#f7f5fb;border-color:#ddd5ee}
.erab h4{color:#5b21b6}
.erab li{margin-bottom:8px}
.erab .smp{display:block;font-weight:700;color:#4c1d95}
.erab .det{display:block;font-size:14.8px;color:#3f3f55}
.tan{background:#fff6f3;border-color:#fcd9cc}
.tan h4{color:var(--warm)}
.src{margin:10px 0 4px;font-size:13.5px;color:var(--mut)}
.vids{margin:0;font-size:13.5px;color:var(--mut)}
.vids.nov{background:#fffbeb;border:1px dashed #fcd34d;border-radius:9px;
padding:8px 11px;color:var(--gold)}
.vc{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;
padding:2px 10px;margin:2px 3px 2px 0;font-size:12.5px;text-decoration:none}
.vc:hover{background:var(--soft)}
.hid{display:none !important}
.empty{text-align:center;color:var(--mut);padding:40px 10px;font-size:16px}
.foot{max-width:1280px;margin:0 auto 30px;padding:0 18px;color:var(--mut);font-size:13px;
text-align:center}
@media(max-width:900px){.wrap{grid-template-columns:1fr}
.nav{position:static;max-height:none}}
@media print{
.top{position:static;background:#fff;color:#000;box-shadow:none;border-bottom:2px solid #000}
.bar,.stat,.nav,.tg{display:none !important}
.wrap{display:block;max-width:100%;padding:0}
.rule.sm .bd{display:block !important}
.chap,.rule{break-inside:avoid;border:1px solid #999}
body{background:#fff;font-size:12.5pt}
a{color:#000;text-decoration:none}
}
"""

    js = """
(function(){
  var TASH=/[\\u0617-\\u061A\\u064B-\\u0652\\u0670\\u0640]/g;
  var PUNCT=/[«»"'(),.:;!?؟\\-—–\\[\\]/]/g;
  function nz(s){
    s=String(s).replace(TASH,'');
    s=s.replace(/[أإآٱ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي')
       .replace(/ؤ/g,'و').replace(/ئ/g,'ي');
    s=s.replace(PUNCT,' ').replace(/\\s+/g,' ');
    return s.trim();
  }
  function AD(n){
    return String(n).replace(/[0-9]/g,function(d){
      return '٠١٢٣٤٥٦٧٨٩'.charAt(+d); });
  }
  var rules=[].slice.call(document.querySelectorAll('.rule'));
  var chaps=[].slice.call(document.querySelectorAll('.chap'));
  var box=document.getElementById('q');
  var tally=document.getElementById('shown');
  var blank=document.getElementById('none');
  var navLinks=[].slice.call(document.querySelectorAll('#nav a'));
  var xBtn=document.getElementById('onlyExtra');
  var xOnly=false;

  function setCount(n){ tally.textContent=AD(n); }

  function apply(){
    var term=nz(box.value);
    var total=0;
    chaps.forEach(function(sec){
      var live=0;
      [].slice.call(sec.querySelectorAll('.rule')).forEach(function(card){
        var hit=(!term||card.getAttribute('data-s').indexOf(term)>=0)
                && (!xOnly||card.getAttribute('data-x')==='1');
        card.classList.toggle('hid',!hit);
        if(hit){ live++; total++; }
      });
      sec.classList.toggle('hid',live===0);
      var link=document.querySelector('#nav a[data-ch="'+sec.id+'"]');
      if(link){ link.parentNode.classList.toggle('hid',live===0);
        link.querySelector('.cc').textContent=AD(live); }
    });
    blank.classList.toggle('hid',total>0);
    setCount(total);
  }

  var timer=null;
  box.addEventListener('input',function(){
    if(timer) clearTimeout(timer);
    timer=setTimeout(apply,180);
  });

  document.addEventListener('click',function(ev){
    var btn=ev.target.closest ? ev.target.closest('.tg') : null;
    if(!btn) return;
    var card=btn.closest('.rule');
    var folded=card.classList.toggle('sm');
    btn.textContent=folded?'فتح':'طيّ';
    btn.setAttribute('aria-expanded',folded?'false':'true');
  });

  function setAll(folded){
    rules.forEach(function(card){
      card.classList.toggle('sm',folded);
      var btn=card.querySelector('.tg');
      if(btn){ btn.textContent=folded?'فتح':'طيّ';
        btn.setAttribute('aria-expanded',folded?'false':'true'); }
    });
  }
  document.getElementById('expand').addEventListener('click',function(){ setAll(false); });
  document.getElementById('fold').addEventListener('click',function(){ setAll(true); });
  document.getElementById('toPrint').addEventListener('click',function(){ window.print(); });
  document.getElementById('clear').addEventListener('click',function(){
    box.value=''; xOnly=false;
    xBtn.classList.remove('on'); xBtn.setAttribute('aria-pressed','false');
    apply(); box.focus();
  });
  xBtn.addEventListener('click',function(){
    xOnly=!xOnly;
    xBtn.classList.toggle('on',xOnly);
    xBtn.setAttribute('aria-pressed',xOnly?'true':'false');
    apply();
  });

  navLinks.forEach(function(a){
    a.addEventListener('click',function(){
      var sec=document.getElementById(a.getAttribute('data-ch'));
      if(sec) [].slice.call(sec.querySelectorAll('.rule.sm')).forEach(function(card){
        card.classList.remove('sm');
        var btn=card.querySelector('.tg');
        if(btn){ btn.textContent='طيّ'; btn.setAttribute('aria-expanded','true'); }
      });
    });
  });

  apply();
})();
"""

    page = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>مرجع القواعد النحوية المفصّل — شرح من كتب النحو</title>
<style>%(css)s</style>
</head>
<body>
<header class="top">
  <h1>مرجع القواعد النحوية المفصّل</h1>
  <p class="sub">شرح موسّع لقواعد النحو والصرف والإملاء على أبواب كتب النحو —
     مع الشواهد ونماذج الإعراب والتنبيهات والمراجع</p>
  <div class="bar">
    <input id="q" type="search" placeholder="ابحث في القواعد والشواهد والتنبيهات…"
           autocomplete="off">
    <button type="button" class="btn" id="clear">مسح</button>
    <button type="button" class="btn" id="expand">فتح الكل</button>
    <button type="button" class="btn" id="fold">طيّ الكل</button>
    <button type="button" class="btn" id="onlyExtra" aria-pressed="false"
            title="عرض القواعد التي لم تُشرح في الفيديوهات فقط">★ الزيادات فقط</button>
    <button type="button" class="btn" id="toPrint">طباعة</button>
  </div>
  <div class="stat">
    <span><b id="shown">%(nr)s</b> قاعدة معروضة</span>
    <span>%(nc)s بابًا</span>
    <span>%(ns)s شاهدًا</span>
    <span>%(ne)s نموذجًا إعرابيًّا</span>
    <span>%(nt)s جدولًا</span>
    <span>منها <b>%(nx)s</b> قاعدة زائدة على الفيديوهات</span>
    <span><a style="color:#fff" href="arabic-grammar-playlist.html">← بنك الأسئلة (%(nq)s سؤالًا)</a></span>
  </div>
</header>

<div class="wrap">
  <aside class="nav" id="nav">
    <h2>فهرس الأبواب</h2>
    <ul>%(nav)s</ul>
  </aside>
  <main id="main">
    %(main)s
    <div class="empty hid" id="none">لا توجد قاعدة تطابق بحثك.</div>
  </main>
</div>

<p class="foot">القواعد مشروحة ومصوغة خصّيصًا لهذا المرجع، والشواهد من القرآن الكريم
والشعر العربي القديم، وأسماء الكتب مذكورة للاستزادة والرجوع.</p>

<script>%(js)s</script>
</body>
</html>
""" % {
        "css": css,
        "js": js,
        "nav": "".join(nav),
        "main": "\n".join(main),
        "nr": ad(len(nahw.R)),
        "nc": ad(len([c for c in nahw.CHAPTERS if by_ch.get(c[0])])),
        "ns": ad(n_shw),
        "ne": ad(n_erab),
        "nt": ad(n_tbl),
        "nx": ad(n_extra),
        "nq": ad(len(marwa.QS)),
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)

    kb = os.path.getsize(OUT) // 1024
    print("✅ %s (%d KB)" % (OUT, kb))
    print("   %d قاعدة في %d بابًا | %d شاهدًا | %d نموذجًا إعرابيًّا | %d جدولًا"
          % (len(nahw.R), len([c for c in nahw.CHAPTERS if by_ch.get(c[0])]),
             n_shw, n_erab, n_tbl))
    for ci, (cid, ctitle, _) in enumerate(nahw.CHAPTERS, 1):
        if by_ch.get(cid):
            print("   - الباب %d: %d قاعدة — %s" % (ci, len(by_ch[cid]), ctitle))


if __name__ == "__main__":
    build()
