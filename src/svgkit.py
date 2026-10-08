# -*- coding: utf-8 -*-
"""
svgkit.py
أدوات رسم SVG بسيطة تُستخدم لرسم كل أشكال أسئلة الذكاء (IQ) داخل الملف.
كل شكل يُرسم داخل مربع إحداثيات 100×100 حتى يسهل تركيبه ونقله وتدويره.
"""
import math

# ------------------------------------------------------------------ ألوان
INK = "#0f172a"
BLUE = "#2563eb"
SKY = "#38bdf8"
GREEN = "#16a34a"
MINT = "#34d399"
AMBER = "#f59e0b"
RED = "#ef4444"
PURPLE = "#8b5cf6"
PINK = "#ec4899"
TEAL = "#14b8a6"
GREY = "#94a3b8"
LIGHT = "#e2e8f0"
WHITE = "#ffffff"
YELLOW = "#fde047"


# ------------------------------------------------------------- أدوات عامة
def svg(inner, vb=100, cls="fig", extra=""):
    """يغلّف محتوى الرسم داخل وسم svg."""
    return (
        f'<svg class="{cls}" viewBox="0 0 {vb} {vb}" xmlns="http://www.w3.org/2000/svg" '
        f'preserveAspectRatio="xMidYMid meet" {extra}>{inner}</svg>'
    )


def g(inner, transform="", extra=""):
    t = f' transform="{transform}"' if transform else ""
    e = f" {extra}" if extra else ""
    return f"<g{t}{e}>{inner}</g>"


def rot(deg, cx=50, cy=50):
    return f"rotate({deg} {cx} {cy})"


def mirror_h(cx=50):
    """انعكاس أفقي (مرآة رأسية) حول المحور x=cx."""
    return f"translate({2 * cx} 0) scale(-1 1)"


def mirror_v(cy=50):
    """انعكاس رأسي (مرآة أفقية) حول المحور y=cy."""
    return f"translate(0 {2 * cy}) scale(1 -1)"


def place(inner, x, y, size, src=100):
    """يضع رسمًا مرسومًا في مربع 100 داخل مربع جديد عند (x,y) وبحجم size."""
    s = size / src
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.4f})">{inner}</g>'


def transform(inner, rotate=0, mirror=None, cx=50, cy=50):
    """تدوير و/أو عكس شكل كامل."""
    t = ""
    if mirror == "h":
        t += mirror_h(cx) + " "
    elif mirror == "v":
        t += mirror_v(cy) + " "
    if rotate:
        t += rot(rotate, cx, cy)
    return g(inner, t.strip())


def pts_str(pts):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def poly_pts(n, r=34, cx=50, cy=50, start=-90):
    out = []
    for i in range(n):
        a = math.radians(start + i * 360.0 / n)
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


# --------------------------------------------------------- أشكال أساسية
def polygon(n, r=34, cx=50, cy=50, start=-90, fill="none", stroke=INK, sw=3.5):
    if n == 4 and start == -90:   # حتى يظهر المربع مربعًا لا معيّنًا
        start = -45
    return (
        f'<polygon points="{pts_str(poly_pts(n, r, cx, cy, start))}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    )


def circle(cx=50, cy=50, r=30, fill="none", stroke=INK, sw=3.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def dot(cx=50, cy=50, r=7, fill=INK, stroke="none", sw=0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def rect(x=18, y=18, w=64, h=64, fill="none", stroke=INK, sw=3.5, rx=0):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def line(x1, y1, x2, y2, stroke=INK, sw=3.5, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>'
    )


def star(cx=50, cy=50, r=32, ri=14, points=5, fill=AMBER, stroke=INK, sw=2.5, start=-90):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else ri
        a = math.radians(start + i * 180.0 / points)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f'<polygon points="{pts_str(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def text(s, x=50, y=56, size=26, fill=INK, weight="700", anchor="middle", family="inherit"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'text-anchor="{anchor}" font-family="{family}" dominant-baseline="middle">{s}</text>'
    )


def zigzag(n, stroke=BLUE, sw=5, y_hi=30, y_lo=72, x0=10, x1=90):
    """خط متكسر مكوّن من n قطعة مستقيمة (لأسئلة عدّ الأضلاع/الخطوط)."""
    step = (x1 - x0) / n
    pts = []
    for i in range(n + 1):
        x = x0 + i * step
        y = y_lo if i % 2 == 0 else y_hi
        pts.append((x, y))
    return (
        f'<polyline points="{pts_str(pts)}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def arrow(deg=0, color=BLUE, sw=6):
    """سهم يشير لأعلى ثم يُدار بزاوية deg باتجاه عقارب الساعة."""
    inner = (
        line(50, 80, 50, 28, color, sw)
        + f'<polyline points="34,42 50,24 66,42" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    return g(inner, rot(deg))


def sector(i, parts, r=32, cx=50, cy=50, fill=BLUE, start=-90, stroke="none", sw=0):
    a0 = math.radians(start + i * 360.0 / parts)
    a1 = math.radians(start + (i + 1) * 360.0 / parts)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    large = 1 if (360.0 / parts) > 180 else 0
    return (
        f'<path d="M {cx} {cy} L {x0:.2f} {y0:.2f} A {r} {r} 0 {large} 1 {x1:.2f} {y1:.2f} Z" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def pie(parts=4, shaded=(0,), r=32, fill=BLUE, stroke=INK, sw=3, rotate=0, spokes=True):
    """دائرة مقسّمة إلى قطاعات، بعضها مظلل."""
    inner = ""
    for i in shaded:
        inner += sector(i % parts, parts, r=r, fill=fill)
    if spokes:
        for i in range(parts):
            a = math.radians(-90 + i * 360.0 / parts)
            inner += line(50, 50, 50 + r * math.cos(a), 50 + r * math.sin(a), stroke, sw * 0.7)
    inner += circle(50, 50, r, "none", stroke, sw)
    return g(inner, rot(rotate)) if rotate else inner


def bar_split(n=5, shaded=0, x=10, y=36, w=80, h=28, fill=TEAL, stroke=INK, sw=3):
    """مستطيل مقسّم إلى n خانة، أول shaded خانة مظللة."""
    cw = w / n
    inner = ""
    for i in range(n):
        f = fill if i < shaded else "none"
        inner += f'<rect x="{x + i * cw:.2f}" y="{y}" width="{cw:.2f}" height="{h}" fill="{f}" stroke="{stroke}" stroke-width="{sw * 0.6}"/>'
    inner += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
    return inner


def quad_square(shaded=(), x=18, y=18, s=64, fill=PURPLE, stroke=INK, sw=3):
    """مربع مقسّم 4 أرباع: 0=أعلى يسار 1=أعلى يمين 2=أسفل يمين 3=أسفل يسار."""
    h = s / 2
    boxes = [(x, y), (x + h, y), (x + h, y + h), (x, y + h)]
    inner = ""
    for i, (bx, by) in enumerate(boxes):
        f = fill if i in shaded else "none"
        inner += f'<rect x="{bx}" y="{by}" width="{h}" height="{h}" fill="{f}" stroke="none"/>'
    inner += line(x + h, y, x + h, y + s, stroke, sw * 0.7)
    inner += line(x, y + h, x + s, y + h, stroke, sw * 0.7)
    inner += rect(x, y, s, s, "none", stroke, sw)
    return inner


def grid_cells(cells, cols=3, rows=3, pad=6, gap=3, stroke=GREY, sw=1.6, box=True, bg=WHITE):
    """شبكة (مصفوفة) تحتوي رسومًا صغيرة. cells: قائمة نصوص SVG (مربع 100) أو None."""
    total = 100 - 2 * pad
    cw = (total - gap * (cols - 1)) / cols
    ch = (total - gap * (rows - 1)) / rows
    inner = ""
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            x = pad + c * (cw + gap)
            y = pad + r * (ch + gap)
            if box:
                inner += f'<rect x="{x:.2f}" y="{y:.2f}" width="{cw:.2f}" height="{ch:.2f}" rx="2" fill="{bg}" stroke="{stroke}" stroke-width="{sw}"/>'
            if i < len(cells) and cells[i]:
                inner += place(cells[i], x, y, cw)
    return inner


def question_cell(color=RED):
    """خانة علامة الاستفهام."""
    return (
        f'<rect x="8" y="8" width="84" height="84" rx="8" fill="#fff7ed" stroke="{color}" '
        f'stroke-width="5" stroke-dasharray="9 7"/>' + text("؟", 50, 54, 52, color, "800")
    )


# ------------------------------------------------------- مجسمات ومكعبات
def cube3d(front=None, top=None, side=None, cx=50, cy=52, s=33, color="#fef3c7",
           top_color="#fde68a", side_color="#fcd34d", stroke=INK, sw=2.6):
    """مكعب بمنظور بسيط، مع إمكانية وضع رمز على كل وجه."""
    d = s * 0.60
    fx, fy = cx - s / 2, cy - s / 2 + d / 2
    front_pts = [(fx, fy), (fx + s, fy), (fx + s, fy + s), (fx, fy + s)]
    top_pts = [(fx, fy), (fx + d, fy - d), (fx + s + d, fy - d), (fx + s, fy)]
    side_pts = [(fx + s, fy), (fx + s + d, fy - d), (fx + s + d, fy + s - d), (fx + s, fy + s)]
    inner = (
        f'<polygon points="{pts_str(front_pts)}" fill="{color}" stroke="{stroke}" stroke-width="{sw}"/>'
        f'<polygon points="{pts_str(top_pts)}" fill="{top_color}" stroke="{stroke}" stroke-width="{sw}"/>'
        f'<polygon points="{pts_str(side_pts)}" fill="{side_color}" stroke="{stroke}" stroke-width="{sw}"/>'
    )
    pad, pads = 0.15, 0.05          # هامش داخل الوجه الأمامي / الوجهين المائلين
    if front:
        inner += place(front, fx + s * pad, fy + s * pad, s * (1 - 2 * pad))
    if top:
        # تحويل يطابق متوازي الأضلاع العلوي: (0,0)→خلف-يسار، (100,0)→خلف-يمين، (0,100)→أمام-يسار
        m = f"matrix({s / 100:.4f},0,{-d / 100:.4f},{d / 100:.4f},{fx + d:.2f},{fy - d:.2f})"
        inner += g(place(top, 100 * pads, 100 * pads, 100 * (1 - 2 * pads)), m)
    if side:
        # الوجه الأيمن: (0,0)→أمام-أعلى، (100,0)→خلف-أعلى، (0,100)→أمام-أسفل
        m = f"matrix({d / 100:.4f},{-d / 100:.4f},0,{s / 100:.4f},{fx + s:.2f},{fy:.2f})"
        inner += g(place(side, 100 * pads, 100 * pads, 100 * (1 - 2 * pads)), m)
    return inner


def cube_net(faces, layout="cross", stroke=INK, sw=2.4, fill="#f8fafc"):
    """
    شبكة مكعب مفرودة.
    layout="cross": صف أفقي من 4 مربعات + مربع أعلى + مربع أسفل.
    faces: قاموس {index: svg} حسب ترتيب: 0..3 الصف الأفقي، 4 الأعلى، 5 الأسفل.
    """
    s = 22
    x0, y0 = 6, 39
    coords = {
        0: (x0, y0), 1: (x0 + s, y0), 2: (x0 + 2 * s, y0), 3: (x0 + 3 * s, y0),
        4: (x0 + s, y0 - s), 5: (x0 + s, y0 + s),
    }
    inner = ""
    for i, (x, y) in coords.items():
        inner += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        sym = faces.get(i)
        if sym:
            inner += place(sym, x + s * 0.14, y + s * 0.14, s * 0.72)
    return inner


# --------------------------------------------- مجسم مكعبات (تصور مكاني)
def _rot_vox(v, rx=0, ry=0, rz=0):
    x, y, z = v
    for _ in range(rz % 4):
        x, y = -y, x
    for _ in range(rx % 4):
        y, z = -z, y
    for _ in range(ry % 4):
        x, z = z, -x
    return (x, y, z)


def voxels(vox, rx=0, ry=0, rz=0, cx=50, cy=58, u=11, top="#bfdbfe", left="#60a5fa",
           right="#3b82f6", stroke=INK, sw=1.5):
    """
    يرسم مجسمًا مكوّنًا من مكعبات صغيرة بإسقاط أيزومتري، مع إمكانية تدويره.
    vox: قائمة إحداثيات صحيحة (x, y, z).
    """
    cubes = [_rot_vox(v, rx, ry, rz) for v in vox]
    # ترتيب الرسم من الخلف للأمام
    cubes.sort(key=lambda v: (v[0] + v[1] + v[2]))
    mx = sum(v[0] for v in cubes) / len(cubes)
    my = sum(v[1] for v in cubes) / len(cubes)
    mz = sum(v[2] for v in cubes) / len(cubes)
    inner = ""
    for (x, y, z) in cubes:
        px = cx + (x - mx - (y - my)) * u * 0.866
        py = cy + ((x - mx) + (y - my)) * u * 0.5 - (z - mz) * u
        top_pts = [(px, py - u), (px + u * 0.866, py - u * 0.5), (px, py), (px - u * 0.866, py - u * 0.5)]
        left_pts = [(px - u * 0.866, py - u * 0.5), (px, py), (px, py + u), (px - u * 0.866, py + u * 0.5)]
        right_pts = [(px + u * 0.866, py - u * 0.5), (px, py), (px, py + u), (px + u * 0.866, py + u * 0.5)]
        inner += (
            f'<polygon points="{pts_str(top_pts)}" fill="{top}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<polygon points="{pts_str(left_pts)}" fill="{left}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<polygon points="{pts_str(right_pts)}" fill="{right}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
        )
    return inner


# ------------------------------------------------------------ ورق وطيّ
def paper(holes=(), folds=(), cut=None, x=16, y=16, s=68, stroke=INK, sw=3,
          fill="#fffbeb", hole_fill=INK, hole_r=5.5):
    """
    ورقة مربعة مع ثقوب. holes: نسب (u, v) بين 0 و1 داخل الورقة.
    folds: قائمة من "v" (طيّة رأسية) أو "h" (طيّة أفقية) تُرسم متقطعة.
    """
    inner = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="2"/>'
    for f in folds:
        if f == "v":
            inner += line(x + s / 2, y, x + s / 2, y + s, GREY, 2, dash="6 5")
        if f == "h":
            inner += line(x, y + s / 2, x + s, y + s / 2, GREY, 2, dash="6 5")
    if cut:
        inner += cut
    for (u, v) in holes:
        inner += dot(x + u * s, y + v * s, hole_r, hole_fill)
    return inner


def fold_arrow(x1=30, y1=50, x2=70, y2=50, color=RED):
    return (
        f'<path d="M {x1} {y1} Q {(x1 + x2) / 2} {y1 - 18} {x2} {y2}" fill="none" stroke="{color}" '
        f'stroke-width="3" stroke-dasharray="5 4"/>'
        f'<polyline points="{x2 - 7},{y2 - 7} {x2},{y2} {x2 - 8},{y2 + 6}" fill="none" stroke="{color}" stroke-width="3"/>'
    )


# ------------------------------------------------------------ وجوه وميزان
def face(mouth="smile", eyes="dots", color="#fde68a", stroke=INK, sw=3, brow=None):
    inner = circle(50, 50, 32, color, stroke, sw)
    if eyes == "dots":
        inner += dot(38, 42, 4.5) + dot(62, 42, 4.5)
    elif eyes == "closed":
        inner += line(32, 42, 44, 42, INK, 3) + line(56, 42, 68, 42, INK, 3)
    elif eyes == "wide":
        inner += circle(38, 42, 7, WHITE, INK, 2.2) + circle(62, 42, 7, WHITE, INK, 2.2) + dot(38, 42, 3) + dot(62, 42, 3)
    if brow == "angry":
        inner += line(30, 32, 44, 37, INK, 3) + line(70, 32, 56, 37, INK, 3)
    elif brow == "sad":
        inner += line(30, 37, 44, 32, INK, 3) + line(70, 37, 56, 32, INK, 3)
    if mouth == "smile":
        inner += f'<path d="M 34 60 Q 50 74 66 60" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round"/>'
    elif mouth == "frown":
        inner += f'<path d="M 34 68 Q 50 54 66 68" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round"/>'
    elif mouth == "flat":
        inner += line(36, 64, 64, 64, INK, sw)
    elif mouth == "open":
        inner += f'<ellipse cx="50" cy="64" rx="10" ry="8" fill="{INK}"/>'
    return inner


def balance(left_items, right_items, tilt=0, stroke=INK):
    """
    ميزان ذو كفتين. left_items / right_items: نصوص SVG صغيرة (مربع 100) توضع فوق الكفتين.
    tilt: -1 يسار أثقل، 1 يمين أثقل، 0 متزن.
    """
    dy = 7 * tilt
    inner = (
        line(50, 86, 50, 40, stroke, 4)
        + f'<polygon points="38,88 62,88 50,74" fill="{GREY}" stroke="{stroke}" stroke-width="2"/>'
        + line(19, 40 + dy, 81, 40 - dy, stroke, 4)
    )
    for side, items in (("l", left_items), ("r", right_items)):
        bx = 22 if side == "l" else 78
        by = (40 + dy * 0.9) if side == "l" else (40 - dy * 0.9)
        inner += line(bx, by, bx, by + 11, stroke, 2)
        inner += f'<path d="M {bx - 15} {by + 11} L {bx + 15} {by + 11} L {bx + 9} {by + 21} L {bx - 9} {by + 21} Z" fill="#e0f2fe" stroke="{stroke}" stroke-width="2"/>'
        n = max(1, len(items))
        w = min(16.0, 30.0 / n)                     # الأشكال تتسع داخل الكفة ولا تخرج منها
        for i, it in enumerate(items):
            x = bx - (n * w) / 2 + i * w
            inner += place(it, x, by + 11 - w, w)
    return inner


def bigsvg(inner, vb=100):
    """شكل بحجم أكبر داخل الصفحة (للمصفوفات والمكعبات والمجسمات)."""
    return svg(inner, vb=vb, cls="fig big")
