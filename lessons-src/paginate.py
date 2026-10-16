# -*- coding: utf-8 -*-
"""
تقطيعٌ ثابتٌ يجري وقتَ البناءِ: يُقسِّمُ محتوى «main» إلى أوراقٍ بمقاسِ الورقةِ المعتادةِ،
ويَحفرُ ترقيمَ الصفحاتِ والعناوينَ الجاريةَ في الملفِّ نفسه — فلا يختلفَ العرضُ في المتصفِّحِ
عن الطباعةِ ولا عن نسخةِ القراءةِ في المستنداتِ:عددُ الصفحاتِ واحدٌ، والكلماتُ في كلِّ صفحةٍ واحدةٍ.
"""
import math
import re
from html.parser import HTMLParser

VOID = {'br', 'hr', 'img', 'col', 'wbr', 'source', 'track', 'area', 'base', 'embed', 'param'}

# ورقةُ ٢٩٫٧ سم − (٢٫٥٤ + ١٫٠٥) × ٢ = ٢٢٫٥٢ سم للمحتوى؛ وسطرُ ١١٫٥ نقطةً × ١٫٩٥ = ٠٫٧٩ سم
PAGE_LINES = 27.0
CHARS_PER_LINE = 68.0
CELL_FACTOR = 92.0
AR_DIGITS = '\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669'


def ar_num(n):
    return ''.join(AR_DIGITS[int(d)] for d in str(int(n)))


def strip_tags(html):
    t = re.sub(r'(?is)<(script|style).*?</\1>', ' ', html)
    t = re.sub(r'(?s)<[^>]+>', ' ', t)
    for a, b in (('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
                 ('&quot;', '"'), ('&#39;', "'")):
        t = t.replace(a, b)
    return re.sub(r'\s+', ' ', t).strip()


def plain_len(html):
    return len(strip_tags(html))


def lines_of(chars, width=CHARS_PER_LINE):
    if chars <= 0:
        return 0.0
    return max(1.0, math.ceil(chars / float(width)))


class TopSplit(HTMLParser):
    """تقطيعٌ إلى عناصرَ عليا مع حفظِ ترتيبِها وخامتها."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.blocks, self.depth, self.cur, self.open_tag = [], 0, None, None

    def _push(self, txt):
        if self.cur is not None:
            self.cur.append(txt)

    def handle_starttag(self, tag, attrs):
        text = self.get_starttag_text() or ''
        if self.depth == 0:
            self.open_tag, self.cur = tag, [text]
        else:
            self._push(text)
        if tag not in VOID:
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        text = self.get_starttag_text() or ''
        if self.depth == 0:
            self.blocks.append((tag, text))
        else:
            self._push(text)

    def handle_endtag(self, tag):
        if self.depth == 0:
            self._push('</%s>' % tag)
            return
        self.depth -= 1
        self._push('</%s>' % tag)
        if self.depth == 0 and self.cur is not None:
            self.blocks.append((self.open_tag, ''.join(self.cur)))
            self.cur = None

    def handle_data(self, d):
        if self.depth == 0:
            if d.strip():
                self.blocks.append(('#text', d.strip()))
        else:
            self._push(d)

    def handle_entityref(self, name):
        self._push('&%s;' % name)

    def handle_charref(self, name):
        self._push('&#%s;' % name)

    def handle_comment(self, data):
        self._push('<!--%s-->' % data)

    def close(self):
        super().close()
        if self.cur is not None:
            self.blocks.append((self.open_tag or 'div', ''.join(self.cur)))
            self.cur = None


def top_blocks(html):
    p = TopSplit()
    p.feed(html)
    p.close()
    out = []
    for tag, raw in p.blocks:
        if tag == '#text':
            if out:
                t0, r0 = out[-1]
                out[-1] = (t0, r0 + ' ' + raw)
            else:
                out.append(('p', '<p>%s</p>' % raw))
        else:
            out.append((tag, raw))
    return out


# ————— تقديرُ الكلفةِ بأسطرِ الورقةِ —————

def table_rows(html):
    m = re.search(r'(?is)<thead\b.*?</thead>', html)
    thead = m.group(0) if m else ''
    rows = re.findall(r'(?is)<tr\b.*?</tr>', html)
    if thead:
        rows = [r for r in rows if r not in thead]
    return thead, rows


def row_cost(row_html):
    cells = re.findall(r'(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>', row_html)
    ncols = max(1, len(cells))
    width = max(10.0, CELL_FACTOR / max(1.0, ncols * 0.72))
    ln = max(1, int(max((lines_of(plain_len(c), width) for c in cells), default=1)))
    return ln * 0.82 + 0.5


def cost_of(tag, html):
    t = html.strip()
    m = re.match(r'(?is)^\s*<[a-z0-9]+\b([^>]*)>', t)
    cls = ''
    if m:
        cm = re.search(r'class="([^"]*)"', m.group(1))
        cls = cm.group(1) if cm else ''
    cs = set(cls.split())

    if tag in ('h1', 'h2'):
        return 2.5
    if tag == 'h3':
        return 1.9
    if tag == 'h4':
        return 1.35
    if tag == 'table' or 'tblwrap' in cs or re.search(r'(?is)<table\b', t):
        thead, rows = table_rows(t)
        total = 0.9 if thead else 0.0
        for r in rows:
            total += row_cost(r)
        return total + 0.8
    if tag in ('ul', 'ol'):
        inner = re.sub(r'(?is)^\s*<(?:ul|ol)\b[^>]*>|</(?:ul|ol)>\s*$', '', t)
        total = 0.35
        for itag, iraw in top_blocks(inner):
            if itag != 'li':
                total += lines_of(plain_len(iraw)) * 1.05
                continue
            body = re.sub(r'(?is)^\s*<li\b[^>]*>|</li>\s*$', '', iraw)
            if 'rules' in cs:
                total += lines_of(plain_len(body), CHARS_PER_LINE * 0.86) * 1.12 + 0.95
            else:
                total += lines_of(plain_len(body), CHARS_PER_LINE * 0.94) * 1.04 + 0.22
        return total
    if tag == 'details':
        sm = re.search(r'(?is)<summary\b.*?</summary>', t)
        return lines_of(plain_len(sm.group(0))) * 1.1 + 1.1 if sm else 1.1
    if 'irab' in cs:
        stmt = re.search(r'(?is)<span class="stmt">.*?</span>', t)
        total = 1.5
        if stmt:
            total += lines_of(plain_len(stmt.group(0)), CHARS_PER_LINE * 0.9) * 1.15
        for li in re.findall(r'(?is)<li\b.*?</li>', t):
            total += lines_of(plain_len(li), CHARS_PER_LINE * 0.9) * 1.05 + 0.1
        return total
    if cs & {'box', 'rule', 'ex', 'note', 'warn', 'card', 'lede', 'grid2'}:
        inner = re.sub(r'(?is)^\s*<div\b[^>]*>|</div>\s*$', '', t)
        n = lines_of(plain_len(inner), CHARS_PER_LINE * 0.9)
        tg = 0.6 if re.search(r'(?is)<span class="tag">', t) else 0.0
        return n * 1.03 + 1.35 + tg
    if tag in ('p', 'blockquote'):
        return lines_of(plain_len(t)) * 1.02 + 0.35
    if tag == 'div':
        inner = re.sub(r'(?is)^\s*<div\b[^>]*>|</div>\s*$', '', t)
        return lines_of(plain_len(inner)) * 1.0 + 0.5
    return lines_of(plain_len(t)) * 1.0 + 0.5


# ————— تقطيعُ ما طالَ من جداولَ وقوائمِ —————

def split_table(html, limit):
    thead, rows = table_rows(html)
    if len(rows) < 2:
        return None
    m = re.match(r'(?is)^(\s*<div\b[^>]*>)?\s*(<table\b[^>]*>)', html)
    wrap_open = m.group(1) or '' if m else ''
    open_tag = (m.group(2) if m and m.group(2) else '<table>')
    cap = re.search(r'(?is)<caption\b.*?</caption>', html)
    colg = ''.join(re.findall(r'(?is)<colgroup\b.*?</colgroup>', html))
    chunks, cur, cost = [], [], (0.9 if thead else 0.0)
    for r in rows:
        c = row_cost(r)
        if cur and cost + c > limit * 0.9:
            chunks.append((cur, cost))
            cur, cost = [], (0.9 if thead else 0.0)
        cur.append(r)
        cost += c
    if cur:
        chunks.append((cur, cost))
    if len(chunks) < 2:
        return None
    out = []
    for i, (part, c) in enumerate(chunks):
        cap_part = cap.group(0) if (cap and i == 0) else ''
        th_part = thead if i == 0 else (thead.replace('<thead', '<thead class="rep"', 1) if thead else '')
        raw = ('%s%s%s%s%s' + '</table>' + '%s') % (wrap_open, open_tag, cap_part, colg + th_part,
                                                    '\n'.join(part), '</div>' if wrap_open else '')
        out.append(('table', raw, c))
    return out


def split_list(html, limit):
    m = re.match(r'(?is)^\s*<(ul|ol)\b([^>]*)>(.*)</\1>\s*$', html)
    if not m:
        return None
    ltag, attrs, inner = m.group(1), m.group(2), m.group(3)
    items = [raw for tag, raw in top_blocks(inner) if tag == 'li']
    if len(items) < 2:
        return None
    chunks, cur, cost = [], [], 0.3
    for li in items:
        c = cost_of('ul', '<ul>' + li + '</ul>')
        if cur and cost + c > limit * 0.9:
            chunks.append((cur, cost))
            cur, cost = [], 0.3
        cur.append(li)
        cost += c
    if cur:
        chunks.append((cur, cost))
    if len(chunks) < 2:
        return None
    out, used = [], 0
    for part, c in chunks:
        extra = ''
        if 'rules' in attrs or 'idxlist' in attrs or ltag == 'ol':
            extra = ' start="%d" style="counter-reset:rl %d"' % (used + 1, used)
        out.append((ltag, '<%s%s%s>%s</%s>' % (ltag, attrs, extra, '\n'.join(part), ltag), c))
        used += len(part)
    return out


def linearize(main_html, titles):
    seq = []
    for stag, sraw in top_blocks(main_html):
        if stag != 'section':
            raw = sraw if sraw.lstrip().startswith('<') else '<p>%s</p>' % sraw
            seq.append(('*', 'دروسُ الإعرابِ', raw, cost_of(stag, raw)))
            continue
        mm = re.match(r'(?is)^\s*<section\b([^>]*)>(.*)</section>\s*$', sraw)
        attrs, inner = (mm.group(1), mm.group(2)) if mm else ('', '')
        im = re.search(r'id="([^"]+)"', attrs)
        sid = im.group(1) if im else ''
        title = titles.get(sid, 'دروسُ الإعرابِ')
        h = re.search(r'(?is)<h2\b[^>]*>(.*?)</h2>', inner)
        if h:
            txt = re.sub(r'([\u0660-\u0669]+)\s*(?=[\u0621-\u064A])', r'\g<1> ', strip_tags(h.group(1)))
            if txt:
                title = (txt[:58] + '…') if len(txt) > 58 else txt
        for btag, braw in top_blocks(inner):
            cost = cost_of(btag, braw)
            parts = None
            if cost > PAGE_LINES * 0.92:
                if btag == 'table' or re.search(r'(?is)<table\b', braw):
                    parts = split_table(braw, PAGE_LINES)
                elif btag in ('ul', 'ol'):
                    parts = split_list(braw, PAGE_LINES)
            if not parts:
                parts = [(btag, braw, cost)]
            for _t, raw, c in parts:
                seq.append((sid, title, raw, c))
    return seq


def paginate(main_html, titles, cover=True, page_lines=None):
    """يُعيدُ (وسمَ الأوراقِ, عددَ صفحاتِ الملفِّ كلِّه بما فيه الغلافُ)."""
    global PAGE_LINES
    old = PAGE_LINES
    if page_lines:
        PAGE_LINES = float(page_lines)
    pages, cur, cur_cost, cur_head = [], [], 0.0, []
    for sid, title, raw, cost in linearize(main_html, titles):
        if cur and cur_cost + cost > PAGE_LINES:
            pages.append({'head': cur_head[0], 'blocks': cur, 'cost': cur_cost})
            cur, cur_cost, cur_head = [], 0.0, []
        cur.append((sid, raw))
        cur_head.append(title)
        cur_cost += cost
    if cur:
        pages.append({'head': cur_head[0], 'blocks': cur, 'cost': cur_cost})

    i = 0
    while i < len(pages) - 1:
        blocks = pages[i]['blocks']
        if blocks and re.match(r'(?is)^\s*<h[1-4]\b', blocks[-1][1]):
            moved = blocks.pop()
            pages[i]['cost'] -= 2.0
            pages[i + 1]['blocks'].insert(0, moved)
            pages[i + 1]['cost'] += 2.0
            if not pages[i]['blocks']:
                pages.pop(i)
                continue
        i += 1

    total = len(pages) + (1 if cover else 0)
    seen = set()
    out = []
    for n, pg in enumerate(pages, start=1):
        num = n + (1 if cover else 0)
        head = (pg['head'] or 'دروسُ الإعرابِ').replace('"', "'")
        over = ' oversize' if pg['cost'] > PAGE_LINES else ''
        brk = '' if n == 1 else ' style="page-break-before:always"'
        parts, open_sid = [], None
        for sid, html in pg['blocks']:
            if sid != open_sid:
                if open_sid is not None:
                    parts.append('</section>')
                if sid == '*':
                    parts.append('<section class="loose">')
                elif sid and sid not in seen:
                    seen.add(sid)
                    parts.append('<section id="%s">' % sid)
                else:
                    parts.append('<section class="cont">')
                open_sid = sid
            parts.append('  ' + html.strip())
        if open_sid is not None:
            parts.append('</section>')
        label = 'صفحةُ %s من %s' % (ar_num(num), ar_num(total))
        body_ = '\n'.join(parts)
        if pg['cost'] > PAGE_LINES:
            body_ += '\n<p class="pnote">هذه الورقةُ أطولُ من مِقدارِها لجدولٍ كبيرٍ.</p>'
        out.append('<div class="sheet%s"%s>\n  <p class="phead">%s</p>\n%s\n  <p class="pnum">%s</p>\n  </div>'
                   % (over, brk, head, body_, label))
    PAGE_LINES = old
    return '\n'.join(out), total
