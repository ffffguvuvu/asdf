# -*- coding: utf-8 -*-
"""
يحوّل أجزاء الـMarkdown (part*.md) إلى ملف HTML واحد مستقل (RTL، بفهرس جانبي قابل للنقر، وجداول، وتنسيق للطباعة).
"""
import os
import re
import html
import datetime

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)
OUT_HTML = os.path.join(ROOT, "قواعد_اسئلة_تخصص_اللغة_العربية.html")

PARTS = [
    "part00_intro.md", "part01_imla.md", "part02_aswat.md",
    "part03a_nahw.md", "part03b_nahw.md", "part04_sarf.md",
    "part05_balagha.md", "part06_arud.md", "part07_adab.md",
    "part08_moajam.md", "part09_tadrees.md", "part09b_shawahid.md", "part10_appendix.md",
]

CSS = r"""
:root{
  --bg:#fbfaf7; --paper:#ffffff; --ink:#1f2328; --muted:#5b6470;
  --h1:#7b1e1e; --h2:#1f3a6e; --h3:#2e5e2e; --line:#e3e1dc;
  --accent:#b8860b; --qbg:#fff8e6; --qline:#f0d9a0; --thead:#e8eef8; --stripe:#f6f8fb;
  --side-w:300px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Noto Naskh Arabic","Amiri","Segoe UI","Tahoma","Traditional Arabic","Arial",sans-serif;
  font-size:18px;line-height:1.9;direction:rtl}
a{color:var(--h2);text-decoration:none}
a:hover{text-decoration:underline}
.layout{display:flex;min-height:100vh}
nav.toc{width:var(--side-w);flex:0 0 var(--side-w);position:sticky;top:0;height:100vh;overflow-y:auto;
  background:#f3f1ec;border-left:1px solid var(--line);padding:14px 14px 40px;font-size:14.5px;line-height:1.7}
nav.toc h2{font-size:17px;margin:4px 0 10px;color:var(--h1)}
nav.toc input{width:100%;padding:7px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;margin-bottom:10px;background:#fff}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc li.l1{margin-top:10px;font-weight:700}
nav.toc li.l1>a{color:var(--h1)}
nav.toc li.l2{padding-right:14px;font-weight:400}
nav.toc li.l2>a{color:#2d3a4a}
nav.toc li.hidden{display:none}
main{flex:1;min-width:0;padding:28px 44px 80px;max-width:1050px;margin:0 auto}
header.cover{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:34px 30px;margin-bottom:28px;text-align:center;
  box-shadow:0 2px 10px rgba(0,0,0,.04)}
header.cover h1{font-size:30px;color:var(--h1);margin:0 0 12px;line-height:1.5}
header.cover p{margin:6px 0;color:var(--muted);font-size:16px}
h1.bab{font-size:27px;color:var(--h1);margin:48px 0 14px;padding:12px 16px;border-right:7px solid var(--h1);background:#fff;border-radius:8px;
  box-shadow:0 1px 4px rgba(0,0,0,.04);line-height:1.5}
h2{font-size:22px;color:var(--h2);margin:34px 0 10px;padding-bottom:6px;border-bottom:2px solid #d5deee;line-height:1.5}
h3{font-size:19px;color:var(--h3);margin:24px 0 8px;line-height:1.5}
p{margin:8px 0 12px;text-align:justify}
ul,ol{margin:6px 0 14px;padding-right:28px;padding-left:0}
li{margin:4px 0;text-align:justify}
strong{color:#111;font-weight:700}
p.q,li.q{background:var(--qbg);border:1px solid var(--qline);border-right:5px solid var(--accent);border-radius:8px;padding:10px 14px;margin:12px 0}
li.q{list-style:none;margin-right:-28px}
.tablewrap{overflow-x:auto;margin:12px 0 18px;border:1px solid var(--line);border-radius:10px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.7}
th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:right}
th{background:var(--thead);font-weight:700;color:#1b2a44;position:sticky;top:0}
tbody tr:nth-child(even) td{background:var(--stripe)}
.totop{position:fixed;bottom:22px;left:22px;background:var(--h2);color:#fff;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;
  font-size:22px;box-shadow:0 2px 8px rgba(0,0,0,.25);opacity:.85}
.totop:hover{opacity:1;text-decoration:none}
.menu-btn{display:none}
footer{margin-top:60px;color:var(--muted);font-size:14px;text-align:center;border-top:1px solid var(--line);padding-top:14px}
@media (max-width:980px){
  .layout{display:block}
  nav.toc{position:static;width:auto;height:auto;max-height:50vh;border-left:0;border-bottom:1px solid var(--line)}
  main{padding:18px 16px 60px}
  body{font-size:17px}
}
@media print{
  nav.toc,.totop{display:none}
  body{background:#fff;font-size:12.5pt}
  main{max-width:none;padding:0}
  h1.bab{page-break-before:always;box-shadow:none;background:none}
  header.cover{box-shadow:none}
  .tablewrap{overflow:visible;border:0}
  th{position:static}
  a{color:inherit}
}
"""

JS = r"""
(function(){
  var box=document.getElementById('tocfilter');
  if(!box) return;
  var items=Array.prototype.slice.call(document.querySelectorAll('nav.toc li'));
  box.addEventListener('input',function(){
    var q=box.value.trim();
    items.forEach(function(li){
      if(!q){li.classList.remove('hidden');return;}
      var hit=li.textContent.indexOf(q)!==-1;
      li.classList.toggle('hidden',!hit);
    });
  });
})();
"""

INLINE_RE = re.compile(r"\*\*(.+?)\*\*")


def inline(text):
    """تهريب HTML ثم تحويل **غامق** إلى <strong>."""
    esc = html.escape(text, quote=False)
    return INLINE_RE.sub(r"<strong>\1</strong>", esc)


def read_all_parts():
    chunks = []
    for name in PARTS:
        with open(os.path.join(BUILD_DIR, name), encoding="utf-8") as f:
            chunks.append(f.read().strip("\n"))
    return "\n\n".join(chunks) + "\n"


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator_row(cells):
    return any(cells) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip() != "")


def render_table(rows):
    rows = [split_row(r) for r in rows]
    rows = [r for r in rows if not is_separator_row(r)]
    if not rows:
        return ""
    ncols = max(len(r) for r in rows)
    out = ['<div class="tablewrap"><table>']
    head = rows[0]
    out.append("<thead><tr>" + "".join(
        "<th>%s</th>" % inline(head[j] if j < len(head) else "") for j in range(ncols)) + "</tr></thead>")
    out.append("<tbody>")
    for r in rows[1:]:
        out.append("<tr>" + "".join(
            "<td>%s</td>" % inline(r[j] if j < len(r) else "") for j in range(ncols)) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def is_question_block(text):
    t = text.lstrip("*• ").strip()
    return t.startswith("من الأسئلة") or t.startswith("من أسئلة")


def build_html(md_text):
    lines = md_text.splitlines()
    body = []
    toc = []
    hid = 0
    title = None
    seen_h1 = 0

    i, n = 0, len(lines)
    para_buf = []
    list_stack = None  # 'ul' / 'ol' currently open

    def close_list():
        nonlocal list_stack
        if list_stack:
            body.append("</%s>" % list_stack)
            list_stack = None

    def flush_para():
        nonlocal para_buf
        if para_buf:
            text = " ".join(s.strip() for s in para_buf)
            cls = ' class="q"' if is_question_block(text) else ""
            body.append("<p%s>%s</p>" % (cls, inline(text)))
            para_buf = []

    while i < n:
        raw = lines[i]
        s = raw.strip()
        if not s:
            flush_para()
            close_list()
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush_para()
            close_list()
            lvl = len(m.group(1))
            text = m.group(2).replace("**", "").strip()
            if lvl == 1:
                seen_h1 += 1
                if seen_h1 == 1:
                    title = text
                    i += 1
                    continue
            hid += 1
            anchor = "h%03d" % hid
            if lvl == 1:
                body.append('<h1 class="bab" id="%s">%s</h1>' % (anchor, html.escape(text)))
                toc.append((1, anchor, text))
            elif lvl == 2:
                body.append('<h2 id="%s">%s</h2>' % (anchor, html.escape(text)))
                toc.append((2, anchor, text))
            else:
                body.append('<h3 id="%s">%s</h3>' % (anchor, html.escape(text)))
            i += 1
            continue

        if s.startswith("|"):
            flush_para()
            close_list()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body.append(render_table(rows))
            continue

        mb = re.match(r"^[-•]\s+(.*)$", s)
        if mb:
            flush_para()
            if list_stack != "ul":
                close_list()
                body.append("<ul>")
                list_stack = "ul"
            cls = ' class="q"' if is_question_block(mb.group(1)) else ""
            body.append("<li%s>%s</li>" % (cls, inline(mb.group(1))))
            i += 1
            continue

        mn = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if mn:
            flush_para()
            if list_stack != "ol":
                close_list()
                body.append("<ol>")
                list_stack = "ol"
            body.append("<li>%s</li>" % inline(mn.group(2)))
            i += 1
            continue

        if s.startswith("---"):
            flush_para()
            close_list()
            i += 1
            continue

        # نص عادي: إن كنا داخل قائمة فالسطر تابع للعنصر الأخير؛ وإلا فقرة
        if list_stack and para_buf == []:
            # سطر متابعة داخل قائمة (نادر) — نلحقه بعنصر القائمة الأخير
            body[-1] = body[-1][:-5] + " " + inline(s) + "</li>"
            i += 1
            continue
        para_buf.append(s)
        i += 1

    flush_para()
    close_list()

    # ----- TOC -----
    toc_html = ['<nav class="toc"><h2>فهرس المحتويات</h2>',
                '<input id="tocfilter" type="search" placeholder="ابحث في الفهرس…">', "<ul>"]
    for lvl, anchor, text in toc:
        toc_html.append('<li class="l%d"><a href="#%s">%s</a></li>' % (lvl, anchor, html.escape(text)))
    toc_html.append("</ul></nav>")

    today = datetime.date.today().strftime("%Y/%m/%d")
    page = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title or 'القواعد')}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="layout">
{chr(10).join(toc_html)}
<main id="top">
<header class="cover">
<h1>{html.escape(title or '')}</h1>
<p>مستخرج من: تجميعة كافة أسئلة تخصص اللغة العربية (بنك الـ360 سؤالًا + التسريبات + نهائي المراجعة + أسئلة الوزارة)</p>
<p>إملاء ـ أصوات ـ نحو ـ صرف ـ بلاغة ـ عروض ـ أدب ونقد ـ معاجم ومفردات ـ طرق تدريس</p>
<p>{today}</p>
</header>
{chr(10).join(body)}
<footer>كل قاعدة معروضة بـ: التعريف ← التفصيل ← الأمثلة ← «من الأسئلة» (نماذج من أسئلة التجميعة مع الإجابة والتعليل).</footer>
</main>
</div>
<a class="totop" href="#top" title="إلى الأعلى">↑</a>
<script>{JS}</script>
</body>
</html>
"""
    return page


def main():
    md_text = read_all_parts()
    page = build_html(md_text)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)
    print("written:", OUT_HTML, os.path.getsize(OUT_HTML), "bytes")


if __name__ == "__main__":
    main()
