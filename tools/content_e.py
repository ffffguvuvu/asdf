# -*- coding: utf-8 -*-
"""أبواب جديدة (2): طي الورق والقص - مصفوفات متقدمة (قاعدة الأعمدة / القطر / التكرار)."""
from iq_svg import svg, box, shape, C, INK, hstack

CH = []


def add(key, title, color, icon, intro, rules, qs):
    CH.append(dict(key=key, title=title, color=color, icon=icon, intro=intro, rules=rules, qs=qs))


def txt(t, x, y, size=14, color=INK, weight="700", anchor="middle"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{t}</text>')


# ------------------------------------------------------------ طي الورق والقص
def cut_corner(pw, ph, f=0.34):
    """مثلث مقصوص من الزاوية العلوية اليُمنى للقطعة المطوية."""
    w, h = pw * f, ph * f
    return (f'<polygon points="{pw:.1f},0 {pw - w:.1f},0 {pw:.1f},{h:.1f}" '
            f'fill="{C["red"]}" fill-opacity="0.55" stroke="{C["red"]}" stroke-width="2"/>')


def cut_square_corner(pw, ph, f=0.32):
    w, h = pw * f, ph * f
    return (f'<rect x="{pw - w:.1f}" y="0" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{C["red"]}" fill-opacity="0.55" stroke="{C["red"]}" stroke-width="2"/>')


def cut_edge_mid(pw, ph, f=0.3):
    """مثلث مقصوص من وسط الحد الأيمن."""
    h = ph * f
    cy = ph / 2
    return (f'<polygon points="{pw:.1f},{cy - h / 2:.1f} {pw - h:.1f},{cy:.1f} '
            f'{pw:.1f},{cy + h / 2:.1f}" fill="{C["red"]}" fill-opacity="0.55" '
            f'stroke="{C["red"]}" stroke-width="2"/>')


def cut_half_circle_fold(pw, ph, f=0.34):
    """نصف دائرة مقصوصة من حدّ الطية (الأيسر) — بعد الفرد تظهر دوائر كاملة."""
    r = min(pw, ph) * f
    cy = ph / 2
    return (f'<path d="M 0 {cy - r:.1f} A {r:.1f} {r:.1f} 0 0 1 0 {cy + r:.1f} Z" '
            f'fill="{C["red"]}" fill-opacity="0.55" stroke="{C["red"]}" stroke-width="2"/>')


def cut_strip_top(pw, ph, f=0.22):
    """شريط مقصوص من أعلى القطعة."""
    h = ph * f
    return (f'<rect x="0" y="0" width="{pw:.1f}" height="{h:.1f}" '
            f'fill="{C["red"]}" fill-opacity="0.55" stroke="{C["red"]}" stroke-width="2"/>')


def fold_demo(folds, cut_fn, W=186, H=128, gap=22, labels=None, arrow_w=26):
    """يرسم: الورقة كاملة → بعد كل طية → القص على القطعة المطوية → الشكل بعد الفرد."""
    sizes = [(W, H)]
    w, h = W, H
    for f in folds:
        w, h = (w / 2, h) if f == "v" else (w, h / 2)
        sizes.append((w, h))
    pw, ph = sizes[-1]
    panels = []
    for i, (ww, hh) in enumerate(sizes):
        body = [box(0, 0, ww, hh, fill="#ffffff", stroke=INK, sw=2.6)]
        if i < len(folds):
            f = folds[i]
            if f == "v":
                body.append(f'<line x1="{ww / 2:.1f}" y1="0" x2="{ww / 2:.1f}" y2="{hh:.1f}" '
                            f'stroke="{C["gray"]}" stroke-width="2" stroke-dasharray="6 5"/>')
            else:
                body.append(f'<line x1="0" y1="{hh / 2:.1f}" x2="{ww:.1f}" y2="{hh / 2:.1f}" '
                            f'stroke="{C["gray"]}" stroke-width="2" stroke-dasharray="6 5"/>')
        else:
            body.append(cut_fn(ww, hh))
        panels.append((ww, hh, body))

    nv, nh = folds.count("v"), folds.count("h")
    cw, ch = W / (2 ** nv), H / (2 ** nh)
    res = [box(0, 0, W, H, fill="#ffffff", stroke=INK, sw=2.6)]
    for i in range(1, 2 ** nv):
        res.append(f'<line x1="{i * cw:.1f}" y1="0" x2="{i * cw:.1f}" y2="{H:.1f}" '
                   f'stroke="{C["gray"]}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    for j in range(1, 2 ** nh):
        res.append(f'<line x1="0" y1="{j * ch:.1f}" x2="{W:.1f}" y2="{j * ch:.1f}" '
                   f'stroke="{C["gray"]}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    for i in range(2 ** nv):
        for j in range(2 ** nh):
            fx = f' translate({cw:.1f},0) scale(-1,1)' if i % 2 == 1 else ""
            fy = f' translate(0,{ch:.1f}) scale(1,-1)' if j % 2 == 1 else ""
            res.append(f'<g transform="translate({i * cw:.1f},{j * ch:.1f}){fx}{fy}">'
                       f'{cut_fn(cw, ch)}</g>')
    panels.append((W, H, res))

    total_w = sum(p[0] for p in panels) + (len(panels) - 1) * (gap + arrow_w)
    H_out = H + 34
    o, cursor = [], total_w
    for idx, (ww, hh, body) in enumerate(panels):
        cursor -= ww
        for b in body:
            o.append(f'<g transform="translate({cursor:.1f},20)">{b}</g>')
        if labels and idx < len(labels):
            o.append(txt(labels[idx], cursor + ww / 2, 13, size=13, color=C["blue"]))
        if idx < len(panels) - 1:
            o.append(txt("◄", cursor - gap - arrow_w / 2, 20 + H / 2 + 7, size=19, color=C["green"]))
            cursor -= (gap + arrow_w)
    return svg(total_w, H_out, "".join(o))


FOLD_RULES = [
    "كل طية = مرآة: ما يُقص في القطعة المطوية يظهر منعكسًا بعدد الطيات (طيتان = 4 نسخ، طية واحدة = نسختان).",
    "القص على حدّ الطية (الخط المتقطع) يظهر شكلًا مزدوجًا متماسكًا في منتصف الورقة.",
    "القص على الحدود الخارجية (الزاوية) يظهر في الأركان؛ والقص في المنتصف يظهر في المنتصف.",
    "لا تتخيّل الورقة وهي تُفتح: تخيّل الشكل المقصوص وهو ينعكس مرة مع كل طية.",
    "تدرب بورقة ومقص حقيقيين مرة واحدة — بعدها ستحل هذه الأسئلة بمجرد النظر.",
]

FOLD_QS = [
    dict(id="fd1", title="طيتان رأسيتان + قص زاوية ⇒ أربع قصّات",
         fig=fold_demo(["v", "v"], cut_corner, labels=["الورقة", "طية 1", "طية 2 + القص", "بعد الفرد"]),
         ask="ورقة مستطيلة تُثنى نصفين ثم نصفين مرة ثانية (طيتان رأسيتان)، ثم يُقص مثلث من زاوية الربع. "
             "ما شكل الورقة بعد فردها؟",
         steps=["الطية الأولى تنصف الورقة، والثانية تنصفها مرة أخرى ⇒ أربعة أرباع متساوية.",
                "المثلث المقصوص من زاوية الربع سينعكس مرة مع كل طية ⇒ 2 × 2 = 4 مثلثات.",
                "تظهر القصّات الأربع على الحد العلوي للورقة بعد فردها: واحدة في كل ربع.",
                "طابق النتيجة مع الاختيارات — الشكل «ج» في الفيديو هو المطابق."],
         answer="أربعة مثلثات مقصوصة على الحد الأعلى، مثلث في كل ربع (الشكل ج كما في الفيديو)",
         tip="عدد النسخ = 2^عدد الطيات: طيتان ⇒ أربع نسخ."),
    dict(id="fd2", title="طية أفقية واحدة + قص من الأعلى ⇒ تناظر أفقي",
         fig=fold_demo(["h"], cut_strip_top, labels=["الورقة", "بعد الطي + القص", "بعد الفرد"]),
         ask="ورقة مستطيلة تُثنى نصفين أفقيًّا (مرة واحدة)، ثم يُقص شريط من أعلاها. ما شكلها بعد الفرد؟",
         steps=["طية واحدة ⇒ نسختان من الشكل المقصوص.",
                "القص من أعلى القطعة المطوية ينعكس إلى أسفل الورقة بعد الفرد.",
                "فتظهر القصّة شريطًا في الأعلى وآخر مماثلًا في الأسفل (تناظر حول خط الطي)."],
         answer="شريط مقصوص في الأعلى وآخر مقابل له في الأسفل (الشكل ج كما في الفيديو)",
         tip="القاعدة العامة: القص من أعلى/أسفل ⇒ تناظر رأسي، والقص من اليمين/اليسار ⇒ تناظر أفقي."),
    dict(id="fd3", title="طية رأسية ثم أفقية + قص مربع من الزاوية ⇒ أربعة مربعات",
         fig=fold_demo(["v", "h"], cut_square_corner, labels=["الورقة", "طية 1", "طية 2 + القص", "بعد الفرد"]),
         ask="ورقة تُثنى نصفين رأسيًّا ثم نصفين أفقيًّا، ثم يُقص مربع صغير من زاوية الربع. ما الشكل بعد الفرد؟",
         steps=["طيتان في اتجاهين مختلفين ⇒ أربعة أرباع (2 × 2).",
                "المربع المقصوص من الزاوية الخارجية يظهر في الأركان الأربعة للورقة.",
                "كل نسخة منعكسة أفقيًّا أو رأسيًّا عن جارتها، فتبدو متناظرة حول خطّي الطي."],
         answer="أربعة مربعات مقصوصة، واحد في كل ركن من أركان الورقة",
         tip="حدّد أولًا: هل الطيتان في نفس الاتجاه (أربعة أعمدة) أم في اتجاهين (أربعة أرباع)؟"),
    dict(id="fd4", title="طيتان رأسيتان + قص من حدّ الطية ⇒ شكل في المنتصف",
         fig=fold_demo(["v", "v"], cut_half_circle_fold, labels=["الورقة", "طية 1", "طية 2 + القص", "بعد الفرد"]),
         ask="ورقة تُثنى نصفين ثم نصفين (طيتان رأسيتان)، ثم يُقص نصف دائرة من حدّ الطية. ما الشكل بعد الفرد؟",
         steps=["القص على حدّ الطية ينعكس مع كل طية، فتتضاعف أنصاف الدوائر لتكوّن دوائر كاملة.",
                "الطية الأولى تعطي دائرة كاملة عند خط المنتصف الأول.",
                "الطية الثانية تنقل المشهد إلى النصف الآخر ⇒ دائرتان كاملتان على خطوط الطي."],
         answer="دائرتان كاملتان مقصوصتان على خطّي الطي (في ثلثَي الورقة)",
         tip="القص من «نص الورقة» (حدّ الطية) ينتج شكلًا مزدوجًا — لا نصف شكل."),
    dict(id="fd5", title="طية رأسية وأفقية + نصف دائرة على الطية ⇒ دائرتان رأسيتان",
         fig=fold_demo(["v", "h"], cut_half_circle_fold, labels=["الورقة", "طية 1", "طية 2 + القص", "بعد الفرد"]),
         ask="ورقة تُثنى رأسيًّا ثم أفقيًّا، ثم يُقص نصف دائرة من حدّ الطية الرأسية. ما الشكل بعد الفرد؟",
         steps=["نصف الدائرة على الطية الرأسية يصير دائرة كاملة عند الفرد الأول.",
                "الطية الأفقية تنقل الدائرة إلى النصف السفلي.",
                "النتيجة: دائرتان كاملتان فوق بعضهما في منتصف الورقة رأسيًّا."],
         answer="دائرتان كاملتان في منتصف الورقة، واحدة فوق الأخرى"),
    dict(id="fd6", title="طيتان رأسيتان + قص مربع من الزاوية السفلية",
         fig=fold_demo(["v", "v"], cut_square_corner, labels=["الورقة", "طية 1", "طية 2 + القص", "بعد الفرد"]),
         ask="ورقة تُثنى نصفين ثم نصفين (طيتان رأسيتان)، ثم يُقص مربع من الزاوية. كيف تظهر القصّات بعد الفرد؟",
         steps=["أربع نسخ من المربع (2 × 2).",
                "كل نسخة في ربع، وتتجاور النسخ على خطوط الطي فتكوّن في المنتصف شكلًا مزدوجًا متماسكًا.",
                "النتيجة: أربعة مربعات على الحد، يندمج كل اثنين منها عند خط الطي."],
         answer="أربعة مربعات مقصوصة على الحد، يندمج كل متجاورين عند خطّي الطي",
         tip="عند القص من حدّ الطية تتلامس النسخ، وعند القص من الحدود الخارجية تتباعد."),
]

add(
    "folding2", "طي الورق والقص — نماذج إضافية", "#5a189a", "✂️",
    "أسئلة طي الورق من أسهل ما يأتي في محور IQ لكنها تحتاج تركيزًا وتخيّلًا: "
    "تُثنى الورقة مرة أو مرتين، ثم يُقص جزء منها، ثم يُطلب منك شكلها بعد الفرد. "
    "القاعدة الذهبية: كل طية مرآة، والقصّة تتضاعف مع كل طية.",
    FOLD_RULES, FOLD_QS,
)


# ------------------------------------------------------- مصفوفات متقدمة
def mini(kind, x, y, s, style):
    fill = INK if style == "black" else ("#cfd9ea" if style == "striped" else "#ffffff")
    return shape(kind, x, y, s, fill=fill, stroke=INK, sw=2.2)


def tri_cell(items, cw, ch, unknown=False):
    """خلية فيها حتى 3 أشكال صغيرة + علامة استفهام إن كانت مجهولة."""
    o = []
    n = len(items) + (1 if unknown else 0)
    step = cw / (n + 1)
    for i, (kind, style) in enumerate(items):
        o.append(mini(kind, step * (i + 1), ch / 2, 17, style))
    if unknown:
        o.append(txt("؟", step * n, ch / 2 + 8, size=26, color=C["red"]))
    return "".join(o)


def grid3(drawers, cw=112, ch=70, gap=8, unknown=None, numbers=False):
    """شبكة 3×3 — العمود الأول على اليمين (قراءة عربية)."""
    unk = set(unknown) if isinstance(unknown, (list, tuple, set)) else (
        {unknown} if unknown is not None else set())
    out = []
    for i, d in enumerate(drawers):
        r, c = divmod(i, 3)
        x = (2 - c) * (cw + gap)
        y = r * (ch + gap)
        is_u = (i in unk)
        out.append(box(x, y, cw, ch, fill="#fff5f7" if is_u else "#ffffff",
                       stroke=C["red"] if is_u else C["gray"], sw=2.4,
                       dash="6 4" if is_u else None))
        out.append(f'<g transform="translate({x:.1f},{y:.1f})">{d(cw, ch)}</g>')
        if numbers:
            out.append(txt(str(i + 1), x + 12, y + 16, size=13, color=C["gray"]))
    W, H = 3 * cw + 2 * gap, 3 * ch + 2 * gap
    return svg(W, H, "".join(out))


def tri_up(x, y, s, style):
    """مثلث رأسه لأعلى: style = 'striped' (مخطط) أو 'empty' (فاضي)."""
    striped = (style == "striped")
    o = shape("triangle", x, y, s, fill="#dbe3f0" if striped else "#ffffff", stroke=INK, sw=2.4)
    if striped:
        for k in (-0.30, 0.05, 0.40):
            o += (f'<line x1="{x - s * 0.40:.1f}" y1="{y + s * k:.1f}" x2="{x + s * 0.40:.1f}" '
                  f'y2="{y + s * k:.1f}" stroke="{INK}" stroke-width="1.6"/>')
    return o


def tri_down(x, y, s, style):
    """مثلث رأسه لأسفل."""
    striped = (style == "striped")
    o = shape("triangle_down", x, y, s, fill="#dbe3f0" if striped else "#ffffff", stroke=INK, sw=2.4)
    if striped:
        for k in (-0.30, 0.05, 0.40):
            o += (f'<line x1="{x - s * 0.40:.1f}" y1="{y - s * k:.1f}" x2="{x + s * 0.40:.1f}" '
                  f'y2="{y - s * k:.1f}" stroke="{INK}" stroke-width="1.6"/>')
    return o


def two_tri(top, bottom, cw, ch):
    """خلية فيها مثلث فوق (رأسه لأعلى) ومثلث تحت (رأسه لأسفل)."""
    return tri_up(cw / 2, ch * 0.29, 17, top) + tri_down(cw / 2, ch * 0.71, 17, bottom)


def dots_cell(n, cw, ch, kind="triangle"):
    """خلية فيها n أشكال: 1 = مفرد، 2 = زوج، 3 = تشكيل مثلثي، 4 = تشكيل مربع."""
    cx, cy = cw / 2, ch / 2
    s = 15
    if n == 1:
        return shape(kind, cx, cy, s + 3, fill="#eef4ff", stroke=C["blue"], sw=2.4)
    if n == 2:
        return (shape(kind, cx - s, cy, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
                + shape(kind, cx + s, cy, s, fill="#eef4ff", stroke=C["blue"], sw=2.2))
    if n == 3:
        return (shape(kind, cx, cy - s * 0.95, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
                + shape(kind, cx - s, cy + s * 0.75, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
                + shape(kind, cx + s, cy + s * 0.75, s, fill="#eef4ff", stroke=C["blue"], sw=2.2))
    return (shape(kind, cx - s, cy - s * 0.8, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
            + shape(kind, cx + s, cy - s * 0.8, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
            + shape(kind, cx - s, cy + s * 0.8, s, fill="#eef4ff", stroke=C["blue"], sw=2.2)
            + shape(kind, cx + s, cy + s * 0.8, s, fill="#eef4ff", stroke=C["blue"], sw=2.2))


def opts_row(items, labels=("1", "2", "3", "4")):
    parts = []
    for lab, body in zip(labels, items):
        parts.append(svg(112, 96, body + txt(lab, 56, 90, size=14, color=C["gray"])))
    return hstack(parts, gap=14, labels=["الاختيارات"])


M1_ROWS = [
    [("triangle", "black"), ("square", "white"), ("circle", "black")],
    [("circle", "black"), ("triangle", "black"), ("square", "white")],
    [("square", "white"), ("circle", "black")],
    [("circle", "black"), ("circle", "striped"), ("square", "black")],
    [("square", "black"), ("circle", "black"), ("circle", "striped")],
    [("circle", "black"), ("square", "black")],
    [("triangle", "striped"), ("square", "black"), ("circle", "striped")],
    [("circle", "striped"), ("triangle", "striped"), ("square", "black")],
    [("square", "black"), ("circle", "striped")],
]
M1_UNKNOWN = {2, 5, 8}


def m1_drawer(i):
    row = M1_ROWS[i]
    unk = i in M1_UNKNOWN
    return lambda cw, ch: tri_cell(row, cw, ch, unknown=unk)


MATRIX_QS = [
    dict(id="mx1", title="قاعدة الصفوف: نفس المجموعة تتكرر في كل صف",
         fig=grid3([m1_drawer(i) for i in range(9)], cw=124, ch=74, unknown=M1_UNKNOWN),
         ask="كل صف يحتوي على ثلاث خلايا، وفي كل خلية ثلاثة أشكال. الخلية الثالثة (على اليسار) "
             "في كل صف ناقصها شكل واحد — أكمل الأشكال الثلاثة الناقصة.",
         steps=["لا تبحث عن تتابع بين الصفوف: احسب «مجموعة الأشكال» في خلايا الصف الواحد.",
                "الصف الأول: كل خلية فيها نفس الثلاثة (مثلث أسود + مربع أبيض + دائرة سوداء) "
                "بترتيب مختلف ⇒ الناقص هو المثلث الأسود.",
                "الصف الثاني: كل خلية فيها (دائرتان + مربع أسود) ⇒ الناقص هو الدائرة المقلّمة.",
                "الصف الثالث: كل خلية فيها (مثلث مقلّم + مربع أسود + دائرة مقلّمة) ⇒ الناقص المثلث المقلّم.",
                "تحقق بالأعمدة: أول خلية في كل صف تعطي (3 مختلفين، دائرتين + مربع، 3 مختلفين) — "
                "وهو نفس نمط الخلايا الباقية.",
                "النتيجة: مثلث أسود + دائرة مقلّمة + مثلث مقلّم ⇒ الاختيار 1."],
         answer="الاختيار 1 — مثلث أسود في الصف الأول، دائرة مقلّمة في الثاني، مثلث مقلّم في الثالث",
         tip="سرّ هذا النوع: لا تتابع بين الصفوف بل «نفس المجموعة تتكرر» — اجمع الأشكال كمجموعة وقارن."),
    dict(id="mx2", title="شكل منسا الصعب — الحل على الأقطار",
         fig=grid3([
             lambda cw, ch: two_tri("empty", "striped", cw, ch),      # 1
             lambda cw, ch: two_tri("empty", "striped", cw, ch),      # 2
             lambda cw, ch: two_tri("striped", "empty", cw, ch),      # 3
             lambda cw, ch: two_tri("striped", "empty", cw, ch),      # 4
             lambda cw, ch: two_tri("empty", "striped", cw, ch),      # 5
             lambda cw, ch: two_tri("empty", "striped", cw, ch),      # 6
             lambda cw, ch: two_tri("striped", "empty", cw, ch),      # 7
             lambda cw, ch: two_tri("striped", "empty", cw, ch),      # 8
             lambda cw, ch: txt("؟", cw / 2, ch / 2 + 12, size=34, color=C["red"]),
         ], cw=104, ch=86, unknown=8, numbers=True),
         ask="رقّم المربعات من 1 إلى 9 (من اليمين لليسار، صفًّا بصفٍّ). المربع 9 ناقص — "
             "ما الشكل الصحيح؟",
         steps=["لا تعمل بالصفوف والأعمدة هنا — الشكل يُحل بالأقطار (النمط المائل).",
                "القطر الأول (3، 5، 7): المثلث المخطط فوق في 3 ⇒ نزل تحت في 5 ⇒ رجع فوق في 7.",
                "القطر الثاني (6، 8، 1): نفس القاعدة — ما فوق ينزل تحت وما تحت يطلع فوق.",
                "القطر الثالث (2، 4، 9): في 2 المخطط تحت والفاضي فوق، وفي 4 انعكس (المخطط فوق)، "
                "إذن في 9 يعود كما في 2.",
                "النتيجة: مثلث فوق فاضي + مثلث تحت مخطط."],
         answer="الاختيار E — مثلث فوق فارغ ومثلث تحت مخطط",
         tip="الشكل صعب ويحتاج وقتًا؛ احفظ صورته وطريقته (الأقطار) إن ظهر لك في الامتحان."),
    dict(id="mx3", title="قاعدة التكرار: الوحدات الثلاثية والرباعية تتكرر",
         fig=grid3([
             lambda cw, ch: dots_cell(3, cw, ch),
             lambda cw, ch: dots_cell(2, cw, ch),
             lambda cw, ch: dots_cell(4, cw, ch),
             lambda cw, ch: dots_cell(2, cw, ch),
             lambda cw, ch: dots_cell(4, cw, ch),
             lambda cw, ch: dots_cell(3, cw, ch),
             lambda cw, ch: dots_cell(4, cw, ch),
             lambda cw, ch: dots_cell(3, cw, ch),
             lambda cw, ch: txt("؟", cw / 2, ch / 2 + 12, size=34, color=C["red"]),
         ], cw=104, ch=86, unknown=8),
         ask="لا يوجد تتابع بين الصفوف ولا الأعمدة. ما الشكل الذي يملأ المربع الناقص؟",
         steps=["جرّب الصفوف والأعمدة أولًا — لن تجد أي تتابع، فهذا الشكل يُحل بملاحظة التكرار.",
                "لاحظ أن وحدات الثلاثة أشكال تتكرر بنفس التشكيل (واحد فوق واثنان تحت) في أكثر من مربع.",
                "كذلك وحدات الأربعة أشكال تتكرر بنفس التشكيل (مربع 2×2).",
                "أما الوحدات المفردة والمزدوجة فلا تتكرر، فلا تُبنَى عليها النتيجة.",
                "إذن المربع الناقص يكرر تشكيل الثلاثة أشكال ⇒ الاختيار «د»."],
         answer="الاختيار «د» — تشكيل الثلاثة أشكال (واحد فوق واثنان تحت)",
         tip="حين يفشل التتابع: ابحث عن «ما يتكرر» — التكرار نفسه هو القاعدة."),
]

add(
    "matrix2", "مصفوفات متقدمة (قاعدة الأعمدة / الأقطار / التكرار)", "#e76f51", "🔲",
    "أشكال مصفوفية صعبة وردت بالفعل في الاختبارات: لا تصلح معها قاعدة «التتابع» المعتادة. "
    "ثلاث أفكار تحلّها: (1) نفس المجموعة تتكرر في كل صف وعمود، (2) العمل على الأقطار لا الصفوف، "
    "(3) البحث عن الوحدة التي تتكرر بنصّها.",
    ["إن لم تجد تتابعًا في الصفوف ولا في الأعمدة — انتقل فورًا إلى الأقطار أو إلى «ما يتكرر».",
     "في قاعدة «نفس المجموعة»: اجمع أشكال الخلية الواحدة كمجموعة (3 مختلفة / 2 + 1) وقارنها بباقي الصف.",
     "حدّد الشكل أولًا ثم اللون ثانيًا — خطوتان منفصلتان تمنعان الخلط.",
     "جرّب الحل من الصفوف مرة ومن الأعمدة مرة: إن وصلت لنفس النتيجة فأنت في الطريق الصحيح."],
    MATRIX_QS,
)
