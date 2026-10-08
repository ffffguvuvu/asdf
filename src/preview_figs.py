# -*- coding: utf-8 -*-
"""أداة تطوير: ترسم كل أشكال الأسئلة في صور PNG للمراجعة البصرية (ليست جزءًا من الملف النهائي)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from content_a import CHAPTERS_A  # noqa: E402
from content_b import CHAPTERS_B  # noqa: E402
from content_c import CHAPTERS_C  # noqa: E402
from model import balance_answers  # noqa: E402

CHAPTERS = balance_answers(CHAPTERS_A + CHAPTERS_B + CHAPTERS_C)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/work/preview"
os.makedirs(OUT, exist_ok=True)

INNER = re.compile(r"<svg[^>]*>(.*)</svg>\s*$", re.S)


def inner_of(s):
    m = INNER.match(s.strip())
    return m.group(1) if m else None


def sheet(ch):
    """يبني ملف SVG واحدًا لكل أسئلة المحور."""
    rows = []
    y = 0
    body = ""
    for qi, q in enumerate(ch["questions"], 1):
        stem = [inner_of(c) for c in (q.get("stem") or [])]
        stem = [s for s in stem if s]
        opts = [inner_of(o) for o in q["options"]] if q["okind"] == "fig" else []
        opts = [o for o in opts if o]
        if not stem and not opts:
            continue
        body += f'<text x="4" y="{y + 16}" font-size="13" fill="#111">Q{qi}</text>'
        x = 40
        for s in stem:
            body += f'<rect x="{x}" y="{y}" width="90" height="90" fill="#fff" stroke="#ddd"/>'
            body += f'<g transform="translate({x},{y}) scale(0.9)">{s}</g>'
            x += 96
        x += 30
        for i, o in enumerate(opts):
            body += f'<rect x="{x}" y="{y}" width="90" height="90" fill="#fff" stroke="#8ab"/>'
            body += f'<text x="{x + 4}" y="{y + 12}" font-size="11" fill="#06c">{"ABCD"[i]}</text>'
            body += f'<g transform="translate({x},{y}) scale(0.9)">{o}</g>'
            x += 96
        rows.append(x)
        y += 100
    w = max(rows) + 20 if rows else 400
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{y + 10}" '
            f'viewBox="0 0 {w} {y + 10}"><rect width="100%" height="100%" fill="#f6f8fc"/>{body}</svg>')


def main():
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    for ch in CHAPTERS:
        svg_txt = sheet(ch)
        p = os.path.join(OUT, f'{ch["num"]:02d}-{ch["id"]}')
        with open(p + ".svg", "w", encoding="utf-8") as f:
            f.write(svg_txt)
        try:
            drawing = svg2rlg(p + ".svg")
            renderPM.drawToFile(drawing, p + ".png", fmt="PNG", dpi=110)
            print("ok ", p + ".png")
        except Exception as e:  # pragma: no cover
            print("fail", p, e)


if __name__ == "__main__":
    main()
