# -*- coding: utf-8 -*-
"""أدوات رسم الأشكال (SVG) المستخدمة في ملف مرجع IQ الشامل."""
import math

INK = "#1f2a44"
C = {
    "red": "#e63946", "blue": "#2a6fdb", "green": "#2a9d8f", "orange": "#f4a261",
    "purple": "#7b4bd8", "pink": "#ef5da8", "gold": "#e9c46a", "gray": "#8d99ae",
    "dark": "#1f2a44", "light": "#fdfdff", "cyan": "#48cae4", "lime": "#90be6d",
}


# --------------------------------------------------------------- primitives
def _p(n, cx, cy, r, rot=-90):
    a0 = math.radians(rot)
    return " ".join(
        f"{cx + r * math.cos(a0 + 2 * math.pi * i / n):.2f},{cy + r * math.sin(a0 + 2 * math.pi * i / n):.2f}"
        for i in range(n)
    )


def _star(cx, cy, r, n=5, inner=0.45, rot=-90):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot) + math.pi * i / n
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def pac(cx, cy, r, miss=0, fill="#fff", stroke=INK, sw=3):
    """دائرة ناقصة ربع. miss: 0=أعلى يمين 1=أسفل يمين 2=أسفل يسار 3=أعلى يسار"""
    ang = {0: (-90, 0), 1: (0, 90), 2: (90, 180), 3: (180, 270)}[miss % 4]
    a1, a2 = math.radians(ang[0]), math.radians(ang[1])
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
    return (f'<path d="M {cx} {cy} L {x2:.2f} {y2:.2f} A {r} {r} 0 1 1 {x1:.2f} {y1:.2f} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def dots(cx, cy, n, r=3.2, spread=7, color=INK):
    """نقاط مرتبة في صف/دائرة صغيرة."""
    if n <= 0:
        return ""
    if n <= 6:
        out = []
        cols = min(n, 3)
        rows = math.ceil(n / cols)
        for i in range(n):
            rr, cc = divmod(i, cols)
            out.append(f'<circle cx="{cx + (cc - (cols - 1) / 2) * spread:.2f}" '
                       f'cy="{cy + (rr - (rows - 1) / 2) * spread:.2f}" r="{r}" fill="{color}"/>')
        return "".join(out)
    out = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        out.append(f'<circle cx="{cx + (spread + 3) * math.cos(a):.2f}" '
                   f'cy="{cy + (spread + 3) * math.sin(a):.2f}" r="{r}" fill="{color}"/>')
    return "".join(out)


def shape(kind, cx, cy, s, fill="none", stroke=INK, sw=3, dash=None, rotate=0, dotn=0):
    """رسم شكل هندسي بسيط في المركز (cx,cy) بنصف قطر s."""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    tr = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
    if kind in ("circle", "ring"):
        el = (f'<circle cx="{cx}" cy="{cy}" r="{s}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind == "square":
        el = (f'<rect x="{cx - s * 0.9:.2f}" y="{cy - s * 0.9:.2f}" width="{s * 1.8:.2f}" '
              f'height="{s * 1.8:.2f}" rx="{s * 0.12:.2f}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind in ("triangle", "pentagon", "hexagon", "heptagon", "octagon", "nonagon"):
        n = {"triangle": 3, "pentagon": 5, "hexagon": 6, "heptagon": 7, "octagon": 8, "nonagon": 9}[kind]
        el = (f'<polygon points="{_p(n, cx, cy, s)}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind in ("diamond", "rhombus"):
        el = (f'<polygon points="{_p(4, cx, cy, s, 0)}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind == "triangle_down":
        el = (f'<polygon points="{_p(3, cx, cy, s, 90)}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind == "star":
        el = (f'<polygon points="{_star(cx, cy, s)}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"{da}{tr}/>')
    elif kind in ("cross", "plus"):
        el = (f'<path d="M {cx - s:.2f} {cy:.2f} H {cx + s:.2f} M {cx:.2f} {cy - s:.2f} V {cy + s:.2f}" '
              f'stroke="{stroke}" stroke-width="{sw * 1.5:.1f}" stroke-linecap="round" fill="none"/>')
    elif kind.startswith("arrow"):
        d = "up" if kind.endswith("up") else "down"
        sg = -1 if d == "up" else 1
        el = (f'<path d="M {cx:.2f} {cy - sg * s:.2f} L {cx - s * 0.8:.2f} {cy + sg * s * 0.2:.2f} '
              f'M {cx:.2f} {cy - sg * s:.2f} L {cx + s * 0.8:.2f} {cy + sg * s * 0.2:.2f} '
              f'M {cx:.2f} {cy - sg * s:.2f} V {cy + sg * s:.2f}" stroke="{stroke}" '
              f'stroke-width="{sw * 1.4:.1f}" fill="none" stroke-linecap="round"/>')
    elif kind == "shaded_half_left":
        el = (f'<rect x="{cx - s:.2f}" y="{cy - s:.2f}" width="{s * 2:.2f}" height="{s * 2:.2f}" '
              f'fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
              f'<path d="M {cx:.2f} {cy - s:.2f} V {cy + s:.2f} H {cx - s:.2f} V {cy - s:.2f} Z" fill="{stroke}"/>')
    elif kind.startswith("quarter_sq"):  # quarter_sq:TR/TL/BR/BL مظلل
        q = kind.split(":")[1] if ":" in kind else "TR"
        ax, ay = {"TR": (1, -1), "TL": (-1, -1), "BR": (1, 1), "BL": (-1, 1)}[q]
        el = (f'<rect x="{cx - s:.2f}" y="{cy - s:.2f}" width="{s * 2:.2f}" height="{s * 2:.2f}" '
              f'fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
              f'<rect x="{cx - s if ax < 0 else cx:.2f}" y="{cy - s if ay < 0 else cy:.2f}" '
              f'width="{s:.2f}" height="{s:.2f}" fill="{stroke}"/>')
    elif kind == "pac":
        el = pac(cx, cy, s, 0, fill, stroke, sw)
    else:
        el = (f'<circle cx="{cx}" cy="{cy}" r="{s}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{sw}"/>')
    if dotn:
        el += dots(cx, cy, dotn)
    return el


# --------------------------------------------------------------- symbol set
SYM = {
    "black_circle": lambda cx, cy, s: shape("circle", cx, cy, s, fill=INK),
    "white_circle": lambda cx, cy, s: shape("circle", cx, cy, s),
    "black_square": lambda cx, cy, s: shape("square", cx, cy, s, fill=INK),
    "white_square": lambda cx, cy, s: shape("square", cx, cy, s),
    "black_triangle": lambda cx, cy, s: shape("triangle", cx, cy, s, fill=INK),
    "white_triangle": lambda cx, cy, s: shape("triangle", cx, cy, s),
    "triangle_down": lambda cx, cy, s: shape("triangle_down", cx, cy, s),
    "star": lambda cx, cy, s: shape("star", cx, cy, s, fill=C["gold"], stroke=INK, sw=2),
    "white_star": lambda cx, cy, s: shape("star", cx, cy, s),
    "cross": lambda cx, cy, s: shape("cross", cx, cy, s),
    "arrow_up": lambda cx, cy, s: shape("arrow_up", cx, cy, s),
    "arrow_down": lambda cx, cy, s: shape("arrow_down", cx, cy, s),
    "hexagon": lambda cx, cy, s: shape("hexagon", cx, cy, s),
    "diamond": lambda cx, cy, s: shape("diamond", cx, cy, s),
    "black_diamond": lambda cx, cy, s: shape("diamond", cx, cy, s, fill=INK),
    "pentagon": lambda cx, cy, s: shape("pentagon", cx, cy, s),
    "empty": lambda cx, cy, s: "",
}


def sym(name, cx, cy, s, color=None):
    if isinstance(name, str) and "|" in name:
        parts = name.split("|")
        step = s * 1.5
        x0 = cx - (len(parts) - 1) * step / 2
        return "".join(sym(p, x0 + i * step, cy, s * 0.8, color) for i, p in enumerate(parts))
    if name in SYM:
        return SYM[name](cx, cy, s)
    if isinstance(name, str) and name.startswith("dots"):
        try:
            n = int(name[4:])
        except ValueError:
            n = 3
        return (f'<circle cx="{cx}" cy="{cy}" r="{s * 0.95:.2f}" fill="none" stroke="{INK}" '
                f'stroke-width="2.5"/>' + dots(cx, cy, n, r=max(2.2, s * 0.09), spread=s * 0.42, color=color or INK))
    if isinstance(name, str) and name.startswith("dot"):
        n = int(name[3:])
        return dots(cx, cy, n, r=max(2.4, s * 0.1), spread=s * 0.5, color=color or INK)
    if isinstance(name, str) and name.isdigit():
        return (f'<text x="{cx:.2f}" y="{cy + s * 0.35:.2f}" text-anchor="middle" '
                f'font-size="{s * 1.25:.1f}" font-weight="700" fill="{C["blue"]}">{name}</text>')
    if isinstance(name, str) and name.startswith("?"):
        return (f'<text x="{cx:.2f}" y="{cy + s * 0.38:.2f}" text-anchor="middle" '
                f'font-size="{s * 1.5:.1f}" font-weight="800" fill="{C["red"]}">؟</text>')
    if isinstance(name, str) and name.startswith("ar_"):  # حرف عربي
        ch = name[3:]
        return (f'<text x="{cx:.2f}" y="{cy + s * 0.38:.2f}" text-anchor="middle" '
                f'font-size="{s * 1.3:.1f}" font-weight="700" fill="{C["purple"]}">{ch}</text>')
    if isinstance(name, str) and name.startswith("num_"):  # رقم
        ch = name[4:]
        return (f'<text x="{cx:.2f}" y="{cy + s * 0.36:.2f}" text-anchor="middle" '
                f'font-size="{s * 1.15:.1f}" font-weight="800" fill="{C["blue"]}">{ch}</text>')
    return f'<circle cx="{cx}" cy="{cy}" r="{s * 0.6:.2f}" fill="{C["gray"]}"/>'


# --------------------------------------------------------------- containers
def box(x, y, w, h, fill="#fff", stroke=C["gray"], sw=2, dash=None, radius=10):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{da}/>')


def cell(x, y, w, h, content, fill="#fff", stroke=C["gray"], sw=2, dash=None, label=None):
    out = [box(x, y, w, h, fill, stroke, sw, dash)]
    out.append(content)
    if label:
        out.append(f'<text x="{x + w / 2}" y="{y + h - 6}" text-anchor="middle" font-size="11" '
                   f'fill="{C["gray"]}">{label}</text>')
    return "".join(out)


import re as _re


def hstack(parts, gap=18, pad=4, labels=()):
    """دمج عدة رسوم SVG أفقيًا في رسم واحد."""
    items, x, H = [], pad, 0
    for i, s in enumerate(parts):
        m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
        w, h = float(m.group(1)), float(m.group(2))
        inner = _re.sub(r'^<svg[^>]*>', '', s)
        inner = _re.sub(r'</svg>$', '', inner)
        items.append(f'<g transform="translate({x:.1f},{0})">{inner}</g>')
        if labels and i < len(labels) and labels[i]:
            items.append(f'<text x="{x + w / 2:.1f}" y="{h + 16}" text-anchor="middle" '
                         f'font-size="13" font-weight="700" fill="{C["gray"]}">{labels[i]}</text>')
        x += w + gap
        H = max(H, h)
    return svg(x - gap + pad, H + (18 if labels else 0), "".join(items))


def vstack(parts, gap=14, pad=4):
    """دمج عدة رسوم SVG رأسيًا."""
    items, y, W = [], pad, 0
    for s in parts:
        m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
        w, h = float(m.group(1)), float(m.group(2))
        inner = _re.sub(r'^<svg[^>]*>', '', s)
        inner = _re.sub(r'</svg>$', '', inner)
        items.append(f'<g transform="translate(0,{y:.1f})">{inner}</g>')
        y += h + gap
        W = max(W, w)
    return svg(W, y - gap + pad, "".join(items))


def svg(w, h, body, cls="fig"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'width="100%" role="img">{body}</svg>')


def row(seq, cw=64, ch=64, gap=8, unknown=False, labels=(), highlight=()):
    """صف من الخلايا: seq = قائمة أسماء رموز أو دوال رسم."""
    n = len(seq)
    w = n * cw + (n - 1) * gap
    h = ch
    out = []
    for i, item in enumerate(seq):
        x = i * (cw + gap)
        hi = i in highlight
        body = item if isinstance(item, str) and item.startswith("<") else sym(item, x + cw / 2, ch / 2, min(cw, ch) * 0.32)
        out.append(cell(x, 0, cw, ch, body,
                        fill="#fff5f5" if hi else "#ffffff",
                        stroke=C["red"] if hi else C["gray"],
                        sw=3 if hi else 2,
                        dash="6 4" if hi else None,
                        label=labels[i] if labels and i < len(labels) else None))
    return svg(w, h, "".join(out))


def grid(rows, cw=64, ch=64, gap=8, highlight=(), labels_on=False):
    """شبكة (مصفوفة) من الرموز."""
    nr = len(rows)
    nc = max(len(r) for r in rows)
    w = nc * cw + (nc - 1) * gap
    h = nr * ch + (nr - 1) * gap
    out = []
    for r in range(nr):
        for c in range(nc):
            if c >= len(rows[r]):
                continue
            item = rows[r][c]
            x = c * (cw + gap)
            y = r * (ch + gap)
            hi = (r, c) in highlight
            body = item if isinstance(item, str) and item.startswith("<") else sym(item, x + cw / 2, y + ch / 2, min(cw, ch) * 0.32)
            out.append(cell(x, y, cw, ch, body,
                            fill="#fff5f5" if hi else "#ffffff",
                            stroke=C["red"] if hi else C["gray"],
                            sw=3 if hi else 2,
                            dash="6 4" if hi else None))
    return svg(w, h, "".join(out))


# --------------------------------------------------------------- cubes
def cube3d(cx, cy, L, top=None, left=None, right=None, face_colors=("#f6f9ff", "#e3ecfb", "#cfdef7")):
    """مكعب منظور ثلاثي الأوجه مع رمز على كل وجه."""
    w, h = L * 0.866, L * 0.5
    T = (cx, cy)
    u, v, z = (w, h), (-w, h), (0, L)

    def add(p, q):
        return (p[0] + q[0], p[1] + q[1])

    tf = [T, add(T, u), add(add(T, u), v), add(T, v)]
    lf = [add(T, v), add(add(T, v), u), add(add(add(T, v), u), z), add(add(T, v), z)]
    rf = [add(T, u), add(add(T, u), v), add(add(add(T, u), v), z), add(add(T, u), z)]

    def pts(seq):
        return " ".join(f"{px:.2f},{py:.2f}" for px, py in seq)

    out = [f'<polygon points="{pts(tf)}" fill="{face_colors[0]}" stroke="{INK}" stroke-width="2.5"/>',
           f'<polygon points="{pts(lf)}" fill="{face_colors[1]}" stroke="{INK}" stroke-width="2.5"/>',
           f'<polygon points="{pts(rf)}" fill="{face_colors[2]}" stroke="{INK}" stroke-width="2.5"/>']
    cs = L * 0.26
    tc = (cx, cy + h)
    lc = (cx - w / 2, cy + h + (h + L) / 2)
    rc = (cx + w / 2, cy + h + (h + L) / 2)
    for content, (ccx, ccy) in ((top, tc), (left, lc), (right, rc)):
        if content:
            out.append(content if isinstance(content, str) and content.startswith("<")
                       else sym(content, ccx, ccy, cs))
    return "".join(out)


def cube_isometric_row(items, L=58, gap=26, labels=(), pad=8):
    """صف من المكعبات المنظورية (خيارات)."""
    w, h = L * 0.866, L * 0.5
    step = 2 * w + gap
    W = pad * 2 + len(items) * step - gap
    H = pad * 2 + 2 * h + L + (22 if labels else 0)
    out = []
    for i, it in enumerate(items):
        cx = pad + w + i * step
        cy = pad
        if isinstance(it, dict):
            out.append(cube3d(cx, cy, L, it.get("top"), it.get("left"), it.get("right"),
                              face_colors=it.get("colors", ("#f6f9ff", "#e3ecfb", "#cfdef7"))))
        else:
            out.append(cube3d(cx, cy, L, it[0], it[1], it[2]))
        if labels and i < len(labels):
            out.append(f'<text x="{cx:.2f}" y="{pad + 2 * h + L + 17:.1f}" text-anchor="middle" '
                       f'font-size="13" font-weight="700" fill="{C["dark"]}">{labels[i]}</text>')
    return svg(W, H, "".join(out))


def cube_net(cells_map, cw=58, gap=4, pad=6, marks=(), w=6, h=4):
    """مكعب مفرود: cells_map = {(col,row): symbol}"""
    W = w * cw + (w - 1) * gap + pad * 2
    H = h * cw + (h - 1) * gap + pad * 2
    out = []
    for (c, r), s in cells_map.items():
        x = pad + c * (cw + gap)
        y = pad + r * (cw + gap)
        out.append(box(x, y, cw, cw, fill="#f4f8ff", stroke=INK, sw=2.2))
        if s:
            out.append(sym(s, x + cw / 2, y + cw / 2, cw * 0.28))
    for (c1, r1), (c2, r2) in marks:  # علامات × على خيارات خاطئة
        x = pad + c1 * (cw + gap)
        y = pad + r1 * (cw + gap)
        out.append(f'<path d="M {x + 10} {y + 10} L {x + cw - 10} {y + cw - 10} '
                   f'M {x + cw - 10} {y + 10} L {x + 10} {y + cw - 10}" stroke="{C["red"]}" '
                   f'stroke-width="4" stroke-linecap="round"/>')
    return svg(W, H, "".join(out))


# --------------------------------------------------------------- numbers
def pills(nums, gap=10, h=52, unknown_index=None, w=64, sub=None):
    """سلسلة أرقام بشكل أقراص ملونة."""
    W = len(nums) * w + (len(nums) - 1) * gap
    out = []
    for i, n in enumerate(nums):
        x = i * (w + gap)
        fill = "#fff0f3" if i == unknown_index else "#eef4ff"
        stroke = C["red"] if i == unknown_index else C["blue"]
        txt = "؟" if i == unknown_index else str(n)
        col = C["red"] if i == unknown_index else C["blue"]
        out.append(f'<rect x="{x}" y="{16 if sub else 0}" width="{w}" height="{h}" rx="12" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        out.append(f'<text x="{x + w / 2}" y="{(16 if sub else 0) + h / 2 + 7}" text-anchor="middle" '
                   f'font-size="22" font-weight="800" fill="{col}">{txt}</text>')
        if sub and i < len(sub) and sub[i]:
            out.append(f'<text x="{x + w / 2}" y="12" text-anchor="middle" font-size="13" '
                       f'fill="{C["green"]}">{sub[i]}</text>')
        if i < len(nums) - 1:
            out.append(f'<text x="{x + w + gap / 2}" y="{(16 if sub else 0) + h / 2 + 6}" '
                       f'text-anchor="middle" font-size="18" fill="{C["gray"]}">،</text>')
    return svg(W, h + (16 if sub else 0), "".join(out))


def matrix(rows, cw=70, ch=56, gap=6, highlight=(), head=None):
    nr, nc = len(rows), max(len(r) for r in rows)
    W = nc * cw + (nc - 1) * gap
    H = nr * ch + (nr - 1) * gap
    out = []
    for r in range(nr):
        for c in range(nc):
            if c >= len(rows[r]):
                continue
            x = c * (cw + gap)
            y = r * (ch + gap)
            hi = (r, c) in highlight
            v = rows[r][c]
            fill = "#fff0f3" if hi else "#f7faff"
            stroke = C["red"] if hi else C["blue"]
            sw = 3 if hi else 2
            dash = ' stroke-dasharray="6 4"' if hi else ""
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
            out.append(f'<text x="{x + cw / 2}" y="{y + ch / 2 + 8}" text-anchor="middle" '
                       f'font-size="21" font-weight="800" fill="{C["red"] if hi else C["dark"]}">{v}</text>')
    return svg(W, H, "".join(out))


# --------------------------------------------------------------- faces
def face(kind, cx, cy, r):
    """وجه تعبيري."""
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff4e0" stroke="{INK}" stroke-width="3"/>']
    ey = cy - r * 0.15
    ex = r * 0.38
    eyec = f'<circle cx="{cx - ex}" cy="{ey}" r="{r * 0.10:.1f}" fill="{INK}"/><circle cx="{cx + ex}" cy="{ey}" r="{r * 0.10:.1f}" fill="{INK}"/>'
    if kind == "surprise":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.34:.1f} Q {cx - ex} {ey - r * 0.55:.1f} {cx - ex + 10} {ey - r * 0.30:.1f}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx + ex - 10} {ey - r * 0.30:.1f} Q {cx + ex} {ey - r * 0.55:.1f} {cx + ex + 10} {ey - r * 0.34:.1f}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx - ex} {ey - r * 0.20:.1f} h {r * 0.20:.1f} M {cx + ex - r * 0.20:.1f} {ey - r * 0.20:.1f} h {r * 0.20:.1f}" stroke="{INK}" stroke-width="2.5"/>')
        o.append(eyec)
        o.append(f'<ellipse cx="{cx}" cy="{cy + r * 0.42:.1f}" rx="{r * 0.20:.1f}" ry="{r * 0.24:.1f}" fill="{INK}"/>')
    elif kind == "fear":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.30:.1f} L {cx - ex + 10} {ey - r * 0.44:.1f}" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx + ex + 10} {ey - r * 0.30:.1f} L {cx + ex - 10} {ey - r * 0.44:.1f}" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx} {ey - r * 0.55:.1f} v {r * 0.18:.1f} M {cx - 7} {ey - r * 0.42:.1f} v {r * 0.12:.1f} M {cx + 7} {ey - r * 0.42:.1f} v {r * 0.12:.1f}" stroke="{INK}" stroke-width="2"/>')
        o.append(eyec)
        o.append(f'<path d="M {cx - r * 0.26:.1f} {cy + r * 0.45:.1f} q {r * 0.26:.1f} -{r * 0.20:.1f} {r * 0.52:.1f} 0 q -{r * 0.26:.1f} {r * 0.20:.1f} -{r * 0.52:.1f} 0 Z" fill="{INK}"/>')
    elif kind == "disgust":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.26:.1f} q {r * 0.16:.1f} -{r * 0.12:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M {cx + ex + 10} {ey - r * 0.26:.1f} q -{r * 0.16:.1f} -{r * 0.12:.1f} -{r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M {cx - ex} {ey + r * 0.06:.1f} q {r * 0.12:.1f} {r * 0.14:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="2.4" fill="none"/>')
        o.append(f'<path d="M {cx + ex - r * 0.24:.1f} {ey + r * 0.06:.1f} q {r * 0.12:.1f} {r * 0.14:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="2.4" fill="none"/>')
        o.append(f'<path d="M {cx - ex - 8} {ey - r * 0.16:.1f} l -12 -6 M {cx - ex - 8} {ey - r * 0.02:.1f} l -12 2" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<path d="M {cx + ex + 8} {ey - r * 0.16:.1f} l 12 -6 M {cx + ex + 8} {ey - r * 0.02:.1f} l 12 2" stroke="{INK}" stroke-width="2"/>')
        o.append(eyec)
        o.append(f'<path d="M {cx - r * 0.36:.1f} {cy + r * 0.44:.1f} q {r * 0.18:.1f} {r * 0.16:.1f} {r * 0.36:.1f} 0 q {r * 0.18:.1f} -{r * 0.16:.1f} {r * 0.36:.1f} 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    elif kind == "anger":
        o.append(f'<path d="M {cx - ex - 12} {ey - r * 0.46:.1f} L {cx - ex + 8} {ey - r * 0.22:.1f}" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx + ex + 12} {ey - r * 0.46:.1f} L {cx + ex - 8} {ey - r * 0.22:.1f}" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx - ex - 9} {ey - r * 0.34:.1f} v {r * 0.12:.1f} M {cx - ex - 1} {ey - r * 0.30:.1f} v {r * 0.10:.1f}" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<path d="M {cx + ex + 9} {ey - r * 0.34:.1f} v {r * 0.12:.1f} M {cx + ex + 1} {ey - r * 0.30:.1f} v {r * 0.10:.1f}" stroke="{INK}" stroke-width="2"/>')
        o.append(eyec)
        o.append(f'<path d="M {cx - r * 0.34:.1f} {cy + r * 0.46:.1f} q {r * 0.34:.1f} -{r * 0.30:.1f} {r * 0.68:.1f} 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    elif kind == "happy":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.30:.1f} q {r * 0.14:.1f} -{r * 0.12:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M {cx + ex - r * 0.14:.1f} {ey - r * 0.30:.1f} q {r * 0.14:.1f} -{r * 0.12:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M {cx - ex - 6} {ey - r * 0.02:.1f} q {r * 0.18:.1f} {r * 0.16:.1f} {r * 0.34:.1f} 0" stroke="{INK}" stroke-width="3.2" fill="none"/>')
        o.append(f'<path d="M {cx + ex - r * 0.28:.1f} {ey - r * 0.02:.1f} q {r * 0.18:.1f} {r * 0.16:.1f} {r * 0.34:.1f} 0" stroke="{INK}" stroke-width="3.2" fill="none"/>')
        o.append(f'<path d="M {cx - r * 0.38:.1f} {cy + r * 0.30:.1f} q {r * 0.38:.1f} {r * 0.40:.1f} {r * 0.76:.1f} 0 Z" fill="{INK}"/>')
        o.append(f'<path d="M {cx - r * 0.30:.1f} {cy + r * 0.32:.1f} h {r * 0.60:.1f}" stroke="#fff" stroke-width="2.4"/>')
    elif kind == "sad":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.26:.1f} L {cx - ex + 10} {ey - r * 0.40:.1f}" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
        o.append(f'<path d="M {cx + ex + 10} {ey - r * 0.26:.1f} L {cx + ex - 10} {ey - r * 0.40:.1f}" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
        o.append(eyec)
        o.append(f'<path d="M {cx - ex - 8} {ey + r * 0.16:.1f} l 14 -8" stroke="{INK}" stroke-width="2.2"/>')
        o.append(f'<path d="M {cx + ex + 8} {ey + r * 0.16:.1f} l -14 -8" stroke="{INK}" stroke-width="2.2"/>')
        o.append(f'<path d="M {cx - r * 0.34:.1f} {cy + r * 0.52:.1f} q {r * 0.34:.1f} -{r * 0.32:.1f} {r * 0.68:.1f} 0" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    elif kind == "contempt":
        o.append(f'<path d="M {cx - ex - 10} {ey - r * 0.30:.1f} q {r * 0.14:.1f} -{r * 0.10:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M {cx + ex - r * 0.14:.1f} {ey - r * 0.30:.1f} q {r * 0.14:.1f} -{r * 0.10:.1f} {r * 0.24:.1f} 0" stroke="{INK}" stroke-width="3" fill="none"/>')
        o.append(eyec)
        o.append(f'<path d="M {cx - r * 0.10:.1f} {cy + r * 0.34:.1f} q {r * 0.30:.1f} {r * 0.20:.1f} {r * 0.48:.1f} -{r * 0.10:.1f}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    return "".join(o)


FACES_AR = {
    "surprise": "مفاجأة", "fear": "خوف", "disgust": "اشمئزاز", "anger": "غضب",
    "happy": "سعادة", "sad": "حزن", "contempt": "ازدراء/سخرية",
}


def faces_row(kinds, r=44, gap=18):
    w = len(kinds) * (2 * r + gap)
    out = []
    for i, k in enumerate(kinds):
        cx = (i + 0.5) * (2 * r + gap)
        out.append(face(k, cx, r + 6, r))
        out.append(f'<text x="{cx:.1f}" y="{2 * r + 26}" text-anchor="middle" font-size="14" '
                   f'font-weight="700" fill="{C["purple"]}">{FACES_AR[k]}</text>')
    return svg(w, 2 * r + 36, "".join(out))


# --------------------------------------------------------------- paper & mirror
def folded_square(kind, cx=90, cy=90, s=70):
    """ورقة مطبقة 4 أرباع مع شكل مقصوص/مرسوم."""
    o = [box(cx - s, cy - s, 2 * s, 2 * s, fill="#fff", stroke=INK, sw=3),
         f'<path d="M {cx} {cy - s} V {cy + s} M {cx - s} {cy} H {cx + s}" stroke="{C["blue"]}" '
         f'stroke-width="2" stroke-dasharray="7 5"/>']
    if kind == "cut_corner":
        o.append(f'<path d="M {cx - s} {cy - s} L {cx - s + 34} {cy - s} L {cx - s} {cy - s + 34} Z" fill="{INK}"/>')
        o.append(f'<path d="M {cx + s} {cy - s} L {cx + s - 34} {cy - s} L {cx + s} {cy - s + 34} Z" fill="{C["gray"]}" opacity=".45"/>')
        o.append(f'<path d="M {cx - s} {cy + s} L {cx - s + 34} {cy + s} L {cx - s} {cy + s - 34} Z" fill="{C["gray"]}" opacity=".45"/>')
        o.append(f'<path d="M {cx + s} {cy + s} L {cx + s - 34} {cy + s} L {cx + s} {cy + s - 34} Z" fill="{C["gray"]}" opacity=".45"/>')
    elif kind == "circle_line":
        o.append(f'<circle cx="{cx + 30}" cy="{cy - 30}" r="16" fill="none" stroke="{INK}" stroke-width="3"/>')
        o.append(f'<circle cx="{cx - 30}" cy="{cy - 30}" r="16" fill="none" stroke="{C["gray"]}" stroke-width="3" opacity=".5"/>')
        o.append(f'<path d="M {cx + 14} {cy + 16} L {cx + 46} {cy + 44}" stroke="{INK}" stroke-width="3"/>')
        o.append(f'<path d="M {cx - 14} {cy + 16} L {cx - 46} {cy + 44}" stroke="{C["gray"]}" stroke-width="3" opacity=".5"/>')
    elif kind == "two_circles":
        o.append(f'<circle cx="{cx + 26}" cy="{cy + 22}" r="12" fill="none" stroke="{INK}" stroke-width="3"/>')
        o.append(f'<circle cx="{cx + 50}" cy="{cy + 40}" r="12" fill="none" stroke="{INK}" stroke-width="3"/>')
    return "".join(o)


def mirror_pair(draw_left, draw_right, w=300, h=170):
    """شكل وانعكاسه في المرآة."""
    o = [draw_left(80, h / 2), draw_right(w - 80, h / 2),
         f'<path d="M {w / 2} 14 V {h - 14}" stroke="{C["purple"]}" stroke-width="3" stroke-dasharray="8 6"/>',
         f'<text x="{w / 2}" y="{h - 2}" text-anchor="middle" font-size="13" fill="{C["purple"]}">المرآة</text>']
    return svg(w, h, "".join(o))
