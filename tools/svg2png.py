# -*- coding: utf-8 -*-
"""محوّل SVG بدائي إلى PNG (يكفي لرسوم هذا المشروع) — لاستخدامه في Word وExcel."""
import re
import math
import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

NS = "{http://www.w3.org/2000/svg}"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONTS = {"regular": os.path.join(FONT_DIR, "DejaVuSans.ttf"),
         "bold": os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")}

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    def shape_text(t):
        try:
            return get_display(arabic_reshaper.reshape(t))
        except Exception:
            return t
except Exception:  # pragma: no cover
    def shape_text(t):
        return t


def mul(m, n):
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + c * b2, b * a2 + d * b2, a * c2 + c * d2, b * c2 + d * d2,
            a * e2 + c * f2 + e, b * e2 + d * f2 + f)


def ap(m, p):
    a, b, c, d, e, f = m
    return (a * p[0] + c * p[1] + e, b * p[0] + d * p[1] + f)


def parse_transform(tr, m):
    if not tr:
        return m
    for op, args in re.findall(r'(\w+)\s*\(([^)]*)\)', tr):
        a = [float(x) for x in re.findall(r'-?\d*\.?\d+', args)]
        if op == 'translate':
            m = mul(m, (1, 0, 0, 1, a[0], a[1] if len(a) > 1 else 0))
        elif op == 'scale':
            sx = a[0]
            sy = a[1] if len(a) > 1 else a[0]
            m = mul(m, (sx, 0, 0, sy, 0, 0))
        elif op == 'rotate':
            ang = math.radians(a[0])
            cx = a[1] if len(a) > 1 else 0
            cy = a[2] if len(a) > 2 else 0
            c, s = math.cos(ang), math.sin(ang)
            m = mul(m, (1, 0, 0, 1, cx, cy))
            m = mul(m, (c, s, -s, c, 0, 0))
            m = mul(m, (1, 0, 0, 1, -cx, -cy))
    return m


def parse_path(d):
    toks = re.findall(r'[MLHVAQCZmlhvaqcz]|-?\d*\.?\d+', d)
    cmds, i, cmd = [], 0, 'M'
    while i < len(toks):
        tk = toks[i]
        if re.match(r'[A-Za-z]', tk):
            cmd = tk
            i += 1
            continue
        if cmd in 'ML':
            cmds.append((cmd, [float(toks[i]), float(toks[i + 1])])); i += 2
        elif cmd in 'ml':
            cmds.append((cmd, [float(toks[i]), float(toks[i + 1])])); i += 2
        elif cmd == 'A':
            cmds.append((cmd, [float(x) for x in toks[i:i + 7]])); i += 7
        elif cmd == 'a':
            cmds.append((cmd, [float(x) for x in toks[i:i + 7]])); i += 7
        elif cmd in 'HV':
            cmds.append((cmd, [float(toks[i])])); i += 1
        elif cmd in 'hv':
            cmds.append((cmd, [float(toks[i])])); i += 1
        elif cmd in 'QC':
            cmds.append((cmd, [float(x) for x in toks[i:i + 4]])); i += 4
        elif cmd in 'qc':
            cmds.append((cmd, [float(x) for x in toks[i:i + 4]])); i += 4
        elif cmd in 'Zz':
            cmds.append((cmd, [])); i += 1
        else:
            i += 1
    return cmds


def arc_points(p0, rx, ry, phi, large, sweep, p1, steps=28):
    x1, y1 = p0
    x2, y2 = p1
    if rx == 0 or ry == 0:
        return [p1]
    phi = math.radians(phi)
    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p = math.cos(phi) * dx2 + math.sin(phi) * dy2
    y1p = -math.sin(phi) * dx2 + math.cos(phi) * dy2
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        co = -co
    cxp = co * rx * y1p / ry
    cyp = -co * ry * x1p / rx
    cx = math.cos(phi) * cxp - math.sin(phi) * cyp + (x1 + x2) / 2
    cy = math.sin(phi) * cxp + math.cos(phi) * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        d = math.hypot(ux, uy) * math.hypot(vx, vy)
        c = max(-1, min(1, (ux * vx + uy * vy) / d)) if d else 1
        a = math.acos(c)
        return -a if (ux * vy - uy * vx) < 0 else a

    th1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dth = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dth > 0:
        dth -= 2 * math.pi
    elif sweep and dth < 0:
        dth += 2 * math.pi
    pts = []
    for k in range(1, steps + 1):
        th = th1 + dth * k / steps
        px = math.cos(phi) * rx * math.cos(th) - math.sin(phi) * ry * math.sin(th) + cx
        py = math.sin(phi) * rx * math.cos(th) + math.cos(phi) * ry * math.sin(th) + cy
        pts.append((px, py))
    return pts


class Svg2Png:
    def __init__(self, scale=2.0, bg="white"):
        self.scale = scale
        self.bg = bg
        self._cache = {}

    def font(self, size, bold=False):
        key = (int(size), bold)
        if key not in self._cache:
            path = FONTS["bold"] if bold else FONTS["regular"]
            self._cache[key] = ImageFont.truetype(path, max(8, int(size)))
        return self._cache[key]

    def render(self, svg_string, out_path, pad=10):
        root = ET.fromstring(svg_string)
        vb = [float(x) for x in root.get('viewBox').replace(',', ' ').split()]
        w, h = vb[2], vb[3]
        W = int(w * self.scale) + pad * 2
        H = int(h * self.scale) + pad * 2
        img = Image.new('RGB', (W, H), self.bg)
        dr = ImageDraw.Draw(img, 'RGBA')
        self._draw(root, (self.scale, 0, 0, self.scale, pad, pad), dr)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img.save(out_path)
        return out_path, W, H

    def _draw(self, el, m, dr):
        for child in el:
            self._el(child, m, dr)

    def _el(self, el, m, dr):
        t = el.tag.replace(NS, '')
        if t == 'g':
            self._draw(el, parse_transform(el.get('transform'), m), dr)
            return
        m = parse_transform(el.get('transform'), m)
        fill = el.get('fill', '#000000')
        stroke = el.get('stroke')
        sw = max(1, int(round(float(el.get('stroke-width', 1)) * self.scale)))
        if t == 'rect':
            x = float(el.get('x', 0)); y = float(el.get('y', 0))
            w = float(el.get('width')); h = float(el.get('height'))
            pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            pts = [(ap(m, p)[0], ap(m, p)[1]) for p in pts]
            if fill and fill != 'none':
                dr.polygon(pts, fill=fill)
            if stroke and stroke != 'none':
                dr.line(pts + [pts[0]], fill=stroke, width=sw, joint='curve')
        elif t in ('circle', 'ellipse'):
            if t == 'circle':
                r = float(el.get('r'))
                rx = ry = r
            else:
                rx = float(el.get('rx')); ry = float(el.get('ry'))
            cx = float(el.get('cx')); cy = float(el.get('cy'))
            a = ap(m, (cx - rx, cy - ry)); b = ap(m, (cx + rx, cy + ry))
            box = [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
            if fill and fill != 'none':
                dr.ellipse(box, fill=fill)
            if stroke and stroke != 'none':
                dr.ellipse(box, outline=stroke, width=sw)
        elif t == 'polygon':
            nums = [float(x) for x in re.findall(r'-?\d*\.?\d+', el.get('points'))]
            pts = [(ap(m, (nums[i], nums[i + 1]))[0], ap(m, (nums[i], nums[i + 1]))[1])
                   for i in range(0, len(nums) - 1, 2)]
            if len(pts) >= 2:
                if fill and fill != 'none':
                    dr.polygon(pts, fill=fill)
                if stroke and stroke != 'none':
                    dr.line(pts + [pts[0]], fill=stroke, width=sw, joint='curve')
        elif t == 'line':
            p1 = ap(m, (float(el.get('x1')), float(el.get('y1'))))
            p2 = ap(m, (float(el.get('x2')), float(el.get('y2'))))
            dr.line([p1[0], p1[1], p2[0], p2[1]], fill=stroke or '#000', width=sw)
        elif t == 'path':
            self._path(el.get('d'), m, dr, fill, stroke, sw)
        elif t == 'text':
            self._text(el, m, dr)
        self._draw(el, m, dr)

    def _path(self, d, m, dr, fill, stroke, sw):
        cmds = parse_path(d or '')
        cur = (0.0, 0.0)
        sub, subs = [], []

        def flush(closed):
            if len(sub) > 1:
                subs.append((list(sub), closed))

        for cmd, args in cmds:
            if cmd in 'Mm':
                flush(False)
                nx, ny = args
                if cmd == 'm':
                    nx += cur[0]; ny += cur[1]
                cur = (nx, ny); sub = [cur]
            elif cmd in 'Ll':
                nx, ny = args
                if cmd == 'l':
                    nx += cur[0]; ny += cur[1]
                cur = (nx, ny); sub.append(cur)
            elif cmd in 'Hh':
                nx = args[0] + (cur[0] if cmd == 'h' else 0)
                cur = (nx, cur[1]); sub.append(cur)
            elif cmd in 'Vv':
                ny = args[0] + (cur[1] if cmd == 'v' else 0)
                cur = (cur[0], ny); sub.append(cur)
            elif cmd in 'Qq':
                x1, y1, x, y = args
                if cmd == 'q':
                    x1 += cur[0]; y1 += cur[1]; x += cur[0]; y += cur[1]
                p0 = cur
                for k in range(1, 10):
                    t2 = k / 9
                    px = (1 - t2) ** 2 * p0[0] + 2 * (1 - t2) * t2 * x1 + t2 ** 2 * x
                    py = (1 - t2) ** 2 * p0[1] + 2 * (1 - t2) * t2 * y1 + t2 ** 2 * y
                    sub.append((px, py))
                cur = (x, y)
            elif cmd in 'Cc':
                x1, y1, x2, y2, x, y = args
                p0 = cur
                for k in range(1, 10):
                    t2 = k / 9
                    px = ((1 - t2) ** 3 * p0[0] + 3 * (1 - t2) ** 2 * t2 * x1 +
                          3 * (1 - t2) * t2 ** 2 * x2 + t2 ** 3 * x)
                    py = ((1 - t2) ** 3 * p0[1] + 3 * (1 - t2) ** 2 * t2 * y1 +
                          3 * (1 - t2) * t2 ** 2 * y2 + t2 ** 3 * y)
                    sub.append((px, py))
                cur = (x, y)
            elif cmd in 'Aa':
                rx, ry, phi, large, sweep, x, y = args
                if cmd == 'a':
                    x += cur[0]; y += cur[1]
                sub.extend(arc_points(cur, rx, ry, phi, int(large), int(sweep), (x, y)))
                cur = (x, y)
            elif cmd in 'Zz':
                flush(True)
                sub = [cur] if cur else []
        flush(False)
        for sp, closed in subs:
            pts = [(ap(m, p)[0], ap(m, p)[1]) for p in sp]
            if len(pts) >= 3 and fill and fill != 'none':
                dr.polygon(pts, fill=fill)
            if stroke and stroke != 'none':
                if closed and len(pts) > 2:
                    dr.line(pts + [pts[0]], fill=stroke, width=sw, joint='curve')
                elif len(pts) > 1:
                    dr.line(pts, fill=stroke, width=sw, joint='curve')

    def _text(self, el, m, dr):
        content = ''.join(el.itertext()).strip()
        if not content:
            return
        size = float(el.get('font-size', 12)) * self.scale
        weight = el.get('font-weight', '400')
        bold = str(weight) in ('700', '800', '900', 'bold')
        fill = el.get('fill', '#000000')
        anchor = el.get('text-anchor', 'start')
        x = float(el.get('x', 0)); y = float(el.get('y', 0))
        p = ap(m, (x, y))
        font = self.font(size, bold)
        txt = shape_text(content)
        bbox = dr.textbbox((0, 0), txt, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        px = p[0] - (tw / 2 if anchor == 'middle' else (tw if anchor == 'end' else 0))
        py = p[1] - th - (bbox[1])
        dr.text((px, py), txt, font=font, fill=fill)


def render_all(chapters, outdir, scale=2.0):
    """يرسم كل أشكال الأسئلة ويعيد dict: qid -> (path, W, H)"""
    r = Svg2Png(scale=scale)
    out = {}
    for ch in chapters:
        for q in ch["qs"]:
            p, W, H = r.render(q["fig"], os.path.join(outdir, f'{q["id"]}.png'))
            out[q["id"]] = (p, W, H)
    return out
