# -*- coding: utf-8 -*-
"""يتحقق أن كل رسم داخل IQ-guide.html يقع داخل حدود viewBox الخاص به."""
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"


def mat_mul(a, b):
    """a,b مصفوفتان 2×3: [a,b,c,d,e,f]"""
    return (a[0] * b[0] + a[2] * b[1],
            a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4],
            a[1] * b[4] + a[3] * b[5] + a[5])


def mat_apply(m, pt):
    x, y = pt
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def parse_transform(s):
    m = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    if not s:
        return m
    for op, argstr in re.findall(r"(matrix|translate|scale|rotate)\s*\(([^)]*)\)", s):
        a = [float(v) for v in re.split(r"[,\s]+", argstr.strip()) if v]
        if op == "translate":
            tx = a[0]
            ty = a[1] if len(a) > 1 else 0.0
            m = mat_mul(m, (1, 0, 0, 1, tx, ty))
        elif op == "scale":
            sx = a[0]
            sy = a[1] if len(a) > 1 else sx
            m = mat_mul(m, (sx, 0, 0, sy, 0, 0))
        elif op == "rotate":
            import math
            ang = math.radians(a[0])
            cx, cy = (a[1], a[2]) if len(a) > 2 else (0.0, 0.0)
            c, s = math.cos(ang), math.sin(ang)
            m = mat_mul(m, (1, 0, 0, 1, cx, cy))
            m = mat_mul(m, (c, s, -s, c, 0, 0))
            m = mat_mul(m, (1, 0, 0, 1, -cx, -cy))
        else:
            m = mat_mul(m, tuple(a[:6]))
    return m


def elem_points(el, m, out):
    f = lambda k: float(el.get(k, "0") or 0)
    t = el.tag.split("}")[-1]
    pts = []
    if t == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        pts = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    elif t == "circle":
        cx, cy, r = f("cx"), f("cy"), f("r")
        pts = [(cx - r, cy - r), (cx + r, cy - r), (cx - r, cy + r), (cx + r, cy + r)]
    elif t == "ellipse":
        cx, cy, rx, ry = f("cx"), f("cy"), f("rx"), f("ry")
        pts = [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx - rx, cy + ry), (cx + rx, cy + ry)]
    elif t == "line":
        pts = [(f("x1"), f("y1")), (f("x2"), f("y2"))]
    elif t == "polygon":
        vals = [float(v) for v in re.split(r"[,\s]+", el.get("points", "").strip()) if v]
        pts = list(zip(vals[0::2], vals[1::2]))
    elif t == "path":
        nums = re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", el.get("d", ""))
        xs = [float(v) for v in nums[0::2]]
        ys = [float(v) for v in nums[1::2]]
        pts = list(zip(xs, ys))
    elif t == "text":
        x, y = f("x"), f("y")
        size = f("font-size") or 14
        w = size * 0.62 * max(1, len(el.text or ""))
        anchor = el.get("text-anchor", "middle")
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        pts = [(x0, y - size), (x0 + w, y + size * 0.35)]
    for p in pts:
        out.append(mat_apply(m, p))


def walk(el, m, out, depth=0):
    m = mat_mul(m, parse_transform(el.get("transform")))
    if el.tag.split("}")[-1] in ("rect", "circle", "ellipse", "line", "polygon", "path", "text"):
        elem_points(el, m, out)
    for ch in el:
        walk(ch, m, out, depth + 1)


def check_svg(svg_text):
    svg_text = svg_text.strip()
    root = ET.fromstring(svg_text)
    vb = root.get("viewBox")
    if vb:
        vals = [float(v) for v in re.split(r"[,\s]+", vb.strip()) if v]
        W, H = vals[2], vals[3]
    else:
        W, H = float(root.get("width", 100)), float(root.get("height", 100))
    pts = []
    walk(root, (1, 0, 0, 1, 0, 0), pts)
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys), W, H


def main(path="IQ-guide.html", tol=2.0):
    html = open(path, encoding="utf-8").read()
    arts = re.findall(r'<article class="qcard" id="([^"]+)">(.*?)</article>', html, re.S)
    oob = []
    total = 0
    for qid, body in arts:
        for i, m in enumerate(re.finditer(r"<svg\b.*?</svg>", body, re.S)):
            total += 1
            txt = m.group(0)
            if "xmlns" not in txt.split(">")[0]:
                txt = txt.replace("<svg", '<svg xmlns="%s"' % SVG_NS, 1)
            try:
                r = check_svg(txt)
            except Exception as e:
                oob.append((qid, i, "parse error: %s" % e))
                continue
            if not r:
                continue
            x0, y0, x1, y1, W, H = r
            if x0 < -tol or y0 < -tol or x1 > W + tol or y1 > H + tol:
                oob.append((qid, i, "bbox=(%.1f,%.1f)-(%.1f,%.1f) viewBox=%.0fx%.0f"
                            % (x0, y0, x1, y1, W, H)))
    print("figures: %d   oob: %d" % (total, len(oob)))
    for qid, i, msg in oob[:40]:
        print("  %s [%d] %s" % (qid, i, msg))
    return len(oob)


if __name__ == "__main__":
    sys.exit(1 if main(*sys.argv[1:2]) else 0)
