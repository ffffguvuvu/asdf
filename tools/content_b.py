# -*- coding: utf-8 -*-
"""الباب الثاني: أسئلة الأشكال (المكمل - المكعبات - التدوير والتصور المكاني - المتطابقة)."""
from iq_svg import (svg, cell, box, shape, sym, cube3d, cube_net, cube_isometric_row,
                    dots, C, INK, _star, hstack)

CH = []


def add(key, title, color, icon, intro, rules, qs):
    CH.append(dict(key=key, title=title, color=color, icon=icon, intro=intro, rules=rules, qs=qs))


# ---------------------------------------------------------------- helpers
def crow(drawers, cw=66, ch=66, gap=8, highlight=(), labels=()):
    """صف خلايا: drawers = دوال (cx, cy, s) -> svg"""
    n = len(drawers)
    W = n * cw + (n - 1) * gap
    out = []
    for i, d in enumerate(drawers):
        x = i * (cw + gap)
        hi = i in highlight
        body = d(x + cw / 2, ch / 2, min(cw, ch) * 0.33)
        out.append(cell(x, 0, cw, ch, body, fill="#fff5f5" if hi else "#ffffff",
                        stroke=C["red"] if hi else C["gray"], sw=3 if hi else 2,
                        dash="6 4" if hi else None,
                        label=labels[i] if labels and i < len(labels) else None))
    return svg(W, ch, "".join(out))


def cgrid(drawers, cw=66, ch=66, gap=8, highlight=()):
    nr = len(drawers)
    nc = max(len(r) for r in drawers)
    W = nc * cw + (nc - 1) * gap
    H = nr * ch + (nr - 1) * gap
    out = []
    for r in range(nr):
        for c in range(nc):
            if c >= len(drawers[r]):
                continue
            x = c * (cw + gap)
            y = r * (ch + gap)
            hi = (r, c) in highlight
            body = drawers[r][c](x + cw / 2, y + ch / 2, min(cw, ch) * 0.33)
            out.append(cell(x, y, cw, ch, body, fill="#fff5f5" if hi else "#ffffff",
                            stroke=C["red"] if hi else C["gray"], sw=3 if hi else 2,
                            dash="6 4" if hi else None))
    return svg(W, H, "".join(out))


def qsq(cx, cy, s, filled=(0, 0, 0, 0)):
    """مربع مقسم 4 أرباع: filled = (أعلى يمين، أعلى يسار، أسفل يمين، أسفل يسار)"""
    o = [f'<rect x="{cx - s}" y="{cy - s}" width="{2 * s}" height="{2 * s}" fill="#fff" '
         f'stroke="{INK}" stroke-width="2.5"/>',
         f'<path d="M {cx} {cy - s} V {cy + s} M {cx - s} {cy} H {cx + s}" stroke="{INK}" stroke-width="2"/>']
    pos = [(cx, cy - s / 2), (cx - s, cy - s / 2), (cx, cy + s / 2), (cx - s, cy + s / 2)]
    for i, qx in enumerate(pos):
        if filled[i]:
            o.append(f'<rect x="{qx[0]}" y="{qx[1]}" width="{s}" height="{s}" fill="{INK}"/>')
    return "".join(o)


def lamp(cx, cy, s):
    """الشكل المرسوم باليد (شبه المصباح): دائرة نصفها مظلل + ذراع من 3 خطوط + جزء علوي."""
    return "".join([
        f'<rect x="{cx - s * 0.55:.1f}" y="{cy - s:.1f}" width="{s * 1.1:.1f}" height="{s * 0.4:.1f}" '
        f'rx="3" fill="{C["gold"]}" stroke="{INK}" stroke-width="2.2"/>',
        f'<path d="M {cx - s * 0.45:.1f} {cy - s * 0.6:.1f} V {cy + s * 0.15:.1f} '
        f'M {cx:.1f} {cy - s * 0.6:.1f} V {cy + s * 0.15:.1f} '
        f'M {cx + s * 0.45:.1f} {cy - s * 0.6:.1f} V {cy + s * 0.15:.1f}" stroke="{INK}" stroke-width="2.2"/>',
        f'<path d="M {cx - s * 0.7:.1f} {cy + s:.1f} A {s * 0.7:.1f} {s * 0.7:.1f} 0 0 1 {cx + s * 0.7:.1f} {cy + s:.1f} Z" '
        f'fill="{INK}"/>',
        f'<path d="M {cx - s * 0.7:.1f} {cy + s:.1f} A {s * 0.7:.1f} {s * 0.7:.1f} 0 0 0 {cx + s * 0.7:.1f} {cy + s:.1f} Z" '
        f'fill="#fff" stroke="{INK}" stroke-width="2.2"/>',
    ])


def circle_line(cx, cy, s, circle_side=1, line_side=-1):
    """دائرة على جانب + خط في المنتصف على الجانب الآخر."""
    ccx = cx + circle_side * s * 0.55
    return "".join([
        f'<circle cx="{ccx:.1f}" cy="{cy:.1f}" r="{s * 0.38:.1f}" fill="none" stroke="{INK}" stroke-width="2.6"/>',
        f'<path d="M {cx + line_side * s * 0.9:.1f} {cy:.1f} H {cx + line_side * s * 0.1:.1f}" '
        f'stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
        f'<path d="M {cx:.1f} {cy + s * 0.85:.1f} H {cx - s * 0.85:.1f}" stroke="{INK}" stroke-width="3" '
        f'stroke-linecap="round"/>',
    ])


def nested(cx, cy, s, outer="pentagon", inner="square", fill_outer="#fff", fill_inner=INK, n=2):
    o = [shape(outer, cx, cy, s, fill=fill_outer, stroke=INK, sw=2.6)]
    if n == 1:
        o.append(shape(inner, cx, cy, s * 0.42, fill=fill_inner, stroke=INK, sw=2))
    else:
        o.append(shape(inner, cx - s * 0.32, cy + s * 0.22, s * 0.3, fill=fill_inner, stroke=INK, sw=2))
        o.append(shape(inner, cx + s * 0.32, cy + s * 0.22, s * 0.3, fill=fill_inner, stroke=INK, sw=2))
    return "".join(o)


def two_circles(cx, cy, s, overlap=True, colors=("#fff", INK)):
    if overlap:
        return "".join([
            f'<circle cx="{cx - s * 0.28:.1f}" cy="{cy:.1f}" r="{s * 0.62:.1f}" fill="{colors[0]}" '
            f'stroke="{INK}" stroke-width="2.6"/>',
            f'<circle cx="{cx + s * 0.34:.1f}" cy="{cy + s * 0.2:.1f}" r="{s * 0.34:.1f}" fill="{colors[1]}" '
            f'stroke="{INK}" stroke-width="2.6"/>'])
    return "".join([
        f'<circle cx="{cx - s * 0.55:.1f}" cy="{cy:.1f}" r="{s * 0.42:.1f}" fill="{colors[0]}" '
        f'stroke="{INK}" stroke-width="2.6"/>',
        f'<circle cx="{cx + s * 0.55:.1f}" cy="{cy:.1f}" r="{s * 0.42:.1f}" fill="{colors[1]}" '
        f'stroke="{INK}" stroke-width="2.6"/>'])


def pac_cell(miss=0, size=1.0, filled=False):
    def d(cx, cy, s):
        return shape("pac", cx, cy, s * size, fill=INK if filled else "#fff",
                     stroke=INK, sw=2.6).replace("A ", "A ")
    # نرسم الدائرة الناقصة ربعًا باتجاه miss
    import iq_svg
    def dd(cx, cy, s):
        return iq_svg.pac(cx, cy, s * size, miss=miss, fill=INK if filled else "#fff", stroke=INK, sw=2.6)
    return dd


def block_count(rows_counts, cw=22, gap=3):
    """شكل من مربعات م stacked (لحساب عدد المربعات)."""
    H = len(rows_counts) * (cw + gap)
    W = max(rows_counts) * (cw + gap)
    out = []
    for r, n in enumerate(rows_counts):
        for c in range(n):
            x = c * (cw + gap) + (max(rows_counts) - n) * (cw + gap) / 2
            y = r * (cw + gap)
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw}" height="{cw}" fill="#dbe7ff" '
                       f'stroke="{INK}" stroke-width="1.6"/>')
    return svg(W, H, "".join(out))


def top_view_demo():
    """مثال النظر من أعلى: مجسم + ما نراه من أعلى."""
    o = [block_count([3, 2, 1], cw=26, gap=4)]
    return o[0]


# ============================================================ الشكل المكمل
add(
    "complete", "الشكل المكمل (النمط المتكرر)", "#e63946", "🧩",
    "السؤال: سلسلة من الأشكال تتكرر، والمطلوب الشكل الناقص. "
    "الحل دائمًا <b>على خطوتين</b>: (1) حدّد الشكل (مثلث/دائرة/مربع …) من دورة التكرار، "
    "ثم (2) حدّد <b>صفته الثانية</b>: مصمت أم مفرغ، كبير أم صغير، عدد النقاط، عدد الخطوط، "
    "أو مكان الجزء الناقص من الشكل.",
    [
        "اكتب تحت كل شكل اسمه (مثلث، دائرة، مربع) لتكشف دورة التكرار.",
        "ابحث عن صفة ثانية تتغير بالتوازي: مصمت/مفرغ - كبير/صغير - عدد النقاط - عدد الخطوط.",
        "في «الدائرة ناقصة ربع»: تابع أي الأرباع أُكلت بالترتيب، فالمطلوب هو الربع الباقي.",
        "في «المرآة/الانعكاس»: الشكل المطلوب يكون معكوسًا كأن أمامه مرآة.",
        "احذف الاختيارات المستحيلة أولًا (طريقة الاستبعاد) قبل أن تتخيل.",
    ],
    [
        dict(id="s1", title="دورة: مثلث مصمت / دائرة مفرغة",
             fig=crow([lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(5,), labels=["1", "2", "3", "4", "5", "6"]),
             ask="ما الشكل الناقص في نهاية السلسلة؟",
             steps=["الدورة: مثلث ثم دائرة، مثلث ثم دائرة ⇒ التالي دائرة.",
                    "الصفة الثانية: المثلث دائمًا «مصمت»، والدائرة دائمًا «مفرغة».",
                    "إذن المطلوب: دائرة مفرغة."],
             answer="دائرة مفرغة", tip=""),
        dict(id="s2", title="دورة ثلاثية + صفة المصمت/المفرغ",
             fig=crow([lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: shape("square", x, y, s, fill=INK),
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(5,), labels=["1", "2", "3", "4", "5", "6"]),
             ask="ما الشكل الناقص؟",
             steps=["الدورة: مثلث ← دائرة ← مربع ← (تعيد نفسها) مثلث ← دائرة ⇒ التالي مربع.",
                    "الصفة الثانية تتناوب: مصمت، مفرغ، مصمت، مفرغ، مصمت ⇒ التالي مفرغ."],
             answer="مربع مفرّغ",
             tip="حلّها دائمًا على خطوتين: الشكل أولًا، ثم صفته (مصمت/مفرغ)."),
        dict(id="s3", title="الدائرة ناقصة ربع: أي ربع هو المطلوب؟",
             fig=crow([pac_cell(0), pac_cell(2), pac_cell(3),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(3,), labels=["1", "2", "3", "4"]),
             ask="السلسلة: مربع، دائرة ناقصة ربع، مربع، دائرة ناقصة ربع … أي دائرة هي المطلوبة؟",
             steps=["الخطوة 1: الدورة تعطينا «دائرة ناقصة ربع».",
                    "الخطوة 2: تابع الأرباع المأكولة: يمين أعلى ← يسار أسفل ← يسار أعلى.",
                    "المتبقي من الأرباع الأربعة هو الربع الذي لم يُؤكل بعد ⇒ الدائرة التي ينقصها ذلك الربع."],
             answer="الدائرة الناقصة الربع الرابع (يمين أسفل)",
             tip="ارسم الدائرة وقسّمها 4 أرباع على ورقتك، وظلّل الأرباع التي ظهرت، فالباقي هو الإجابة."),
        dict(id="s4", title="شروط ثلاثة: مصمت/مفرغ + كبير/صغير + انعكاس مرآتي",
             fig=crow([pac_cell(0, 1.1, True), pac_cell(0, 1.1, False), pac_cell(2, 0.75, True),
                       pac_cell(2, 0.75, False), pac_cell(3, 1.1, True),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(5,), labels=["1", "2", "3", "4", "5", "6"]),
             ask="أكمل السلسلة (دوائر ناقصة ربع).",
             steps=["الشرط 1 (مصمت/مفرغ): مصمت، مفرغ، مصمت، مفرغ، مصمت ⇒ المطلوب مفرغ (فاضي).",
                    "الشرط 2 (الحجم): المصمت دائمًا صغير، والمفرغ دائمًا كبير ⇒ المطلوب كبير.",
                    "الشرط 3 (الانعكاس): الشكل المطلوب هو انعكاس مرآتي للذي قبله (كأن بينهما مرآة)."],
             answer="دائرة مفرغة كبيرة، وانعكاسها مطابق للشكل الخامس",
             tip="كلما زادت الشروط زادت دقة الاستبعاد: استبعد بشرط واحد فقط لتصل للإجابة بسرعة."),
        dict(id="s5", title="دورة رباعية مع المصمت/المفرغ",
             fig=crow([lambda x, y, s: shape("square", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: shape("star", x, y, s, fill=C["gold"], stroke=INK, sw=2),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: shape("square", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s, fill=INK),
                       lambda x, y, s: shape("star", x, y, s, fill=C["gold"], stroke=INK, sw=2),
                       lambda x, y, s: shape("circle", x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 14}" text-anchor="middle" font-size="32" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      cw=58, ch=64, highlight=(8,)),
             ask="ما الشكل التالي؟",
             steps=["الدورة الرباعية: مربع ← مثلث ← نجمة ← دائرة (تتكرر مرتين).",
                    "بعد الدائرة الثانية تعود الدورة ⇒ المطلوب مربع.",
                    "الصفة: مفرغ، مصمت، مفرغ، مصمت … ⇒ المربع المطلوب مفرّغ."],
             answer="مربع مفرّغ", tip=""),
        dict(id="s6", title="الإشارة (+) والمثلث: الاتجاه والخطوط الداخلية",
             fig=crow([lambda x, y, s: shape("cross", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("cross", x, y, s),
                       lambda x, y, s: shape("triangle_down", x, y, s),
                       lambda x, y, s: shape("cross", x, y, s),
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("cross", x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(7,), labels=["1", "2", "3", "4", "5", "6", "7", "8"]),
             ask="أكمل السلسلة.",
             steps=["الدورة: + then مثلث then + then مثلث ⇒ التالي مثلث.",
                    "اتجاه المثلث: معتدل then مقلوب then معتدل then مقلوب ⇒ التالي مقلوب.",
                    "واتجاه الخطوط الداخلية يتبع نفس فكرة التكرار: خط، خط، معكوس، خط، خط، معكوس …"],
             answer="مثلث مقلوب", tip=""),
        dict(id="s7", title="نوع الشكل + عدد النقاط يتزايد",
             fig=crow([lambda x, y, s: shape("triangle", x, y, s) ,
                       lambda x, y, s: shape("hexagon", x, y, s),
                       lambda x, y, s: f'{shape("circle", x, y, s)}{dots(x, y, 3, r=3, spread=8)}',
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("hexagon", x, y, s),
                       lambda x, y, s: f'{shape("circle", x, y, s)}{dots(x, y, 3, r=3, spread=8)}',
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("hexagon", x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      cw=60, ch=66, highlight=(8,)),
             ask="أكمل (الدورة: مثلث، سداسي، دائرة).",
             steps=["الدورة الثلاثية: مثلث ← سداسي ← دائرة ⇒ التالي دائرة.",
                    "ننتقل لعدد النقاط داخل الدائرة: 3، 3، 4 … (يثبت، يثبت، يزيد 1).",
                    "ثم 5، 5 ⇒ التالي يزيد نقطة ⇒ 6 نقاط (وليس 7)."],
             answer="دائرة بداخلها 6 نقاط",
             tip="عدّ النقاط بصوت منخفض أو بإصبعك على الشاشة؛ الخطأ في العدّ سبب شائع للخسارة."),
        dict(id="s8", title="كبير/صغير + عدد الخطوط الداخلية",
             fig=crow([lambda x, y, s: f'{shape("circle", x, y, s)}',
                       lambda x, y, s: f'{shape("circle", x, y, s * 0.6)}',
                       lambda x, y, s: f'{shape("triangle", x, y, s)}',
                       lambda x, y, s: f'{shape("triangle", x, y, s * 0.6)}',
                       lambda x, y, s: f'{shape("star", x, y, s, fill=C["gold"], stroke=INK, sw=2)}',
                       lambda x, y, s: f'{shape("star", x, y, s * 0.6, fill=C["gold"], stroke=INK, sw=2)}',
                       lambda x, y, s: f'{shape("square", x, y, s)}',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(7,)),
             ask="النمط: شكل كبير ثم نفس الشكل صغيرًا. فما التالي؟",
             steps=["كل شكل يظهر مرتين: كبير then صغير.",
                    "بعد النجمة الكبيرة then النجمة الصغيرة يأتي المربع الكبير then المربع الصغير.",
                    "وفي الشكل الصغير عدد الخطوط الداخلية يتكرر: 1، 2، 3، 1، 2، 3 ⇒ المطلوب 3 خطوط."],
             answer="مربع صغير بداخله 3 خطوط", tip=""),
        dict(id="s9", title="حركة مربع صغير داخل مصفوفة 3×3",
             fig=cgrid([[lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.55, y - s * 0.55, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.25, y - s * 0.55, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x + s * 0.05, y - s * 0.55, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}'],
                        [lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.55, y - s * 0.25, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.25, y - s * 0.25, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x + s * 0.05, y - s * 0.25, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}'],
                        [lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.55, y + s * 0.05, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}{box(x - s * 0.25, y + s * 0.05, s * 0.5, s * 0.5, fill=INK, stroke=INK, sw=1)}',
                         lambda x, y, s: f'{shape("square", x, y, s * 1.15)}<text x="{x}" y="{y + 10}" '
                                         f'text-anchor="middle" font-size="26" font-weight="800" fill="{C["red"]}">؟</text>']],
                       highlight=[(2, 2)]),
             ask="أين يكون المربع الصغير في الخانة الأخيرة؟",
             steps=["المربع الكبير ثابت، والمربع الصغير هو الذي يتحرك.",
                    "الصف الأول: فوق يسار ← فوق وسط ← فوق يمين.",
                    "الصف الثاني: وسط يسار ← وسط ← وسط يمين.",
                    "الصف الثالث: تحت يسار ← تحت وسط ⇒ التالي تحت يمين."],
             answer="المربع الصغير في «تحت يمين»",
             tip="تتبّع الجزء المتحرك فقط وتجاهل الثابت — هذا يختصر الوقت لأقل من 10 ثوانٍ."),
        dict(id="s10", title="مصفوفة: نوع الخلفية + الخط الداخلي",
             fig=cgrid([[lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#fff", stroke=INK, sw=2.4)}<path d="M {x} {y - s * 0.5} V {y + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<path d="M {x - s * 0.5} {y} H {x + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<path d="M {x - s * 0.5} {y - s * 0.3} H {x + s * 0.5} M {x - s * 0.5} {y + s * 0.3} H {x + s * 0.5}" stroke="{INK}" stroke-width="3"/>'],
                        [lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<path d="M {x - s * 0.5} {y} H {x + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<path d="M {x - s * 0.5} {y - s * 0.3} H {x + s * 0.5} M {x - s * 0.5} {y + s * 0.3} H {x + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#fff", stroke=INK, sw=2.4)}<path d="M {x} {y - s * 0.5} V {y + s * 0.5}" stroke="{INK}" stroke-width="3"/>'],
                        [lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<path d="M {x - s * 0.5} {y - s * 0.3} H {x + s * 0.5} M {x - s * 0.5} {y + s * 0.3} H {x + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#fff", stroke=INK, sw=2.4)}<path d="M {x} {y - s * 0.5} V {y + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                         lambda x, y, s: f'{box(x - s * 0.8, y - s * 0.8, s * 1.6, s * 1.6, fill="#dfe7ff", stroke=INK, sw=2.4)}<text x="{x}" y="{y + 10}" text-anchor="middle" font-size="26" font-weight="800" fill="{C["red"]}">؟</text>']],
                       highlight=[(2, 2)]),
             ask="أكمل المصفوفة (الخلفية والخط الداخلي).",
             steps=["انظر للأشكال الكبيرة أولًا: الخلفيات ثلاثة أنواع (فاضي، مخطط، مربعات/مظلل) "
                    "ولا يتكرر أي نوع مرتين في نفس الصف.",
                    "الصف الثالث فيه: مظلل + فاضي ⇒ الناقص «مخطط».",
                    "ثم نراجع الخط الداخلي: طولي، عرضي، خطّين ⇒ الطولي تكرر مرتين، والعرضي ثلاث مرات، "
                    "والخطّان ثلاث مرات ⇒ الناقص هو الخط الطولي."],
             answer="خلفية مخطّطة + خط داخلي طولي",
             tip="في مصفوفات الأشكال: كل صف وكل عمود يحتوي كل الأنواع مرة واحدة."),
        dict(id="s11", title="تزايد عدد النقاط في كل صف",
             fig=cgrid([[lambda x, y, s: dots(x, y, 1, r=4, spread=9),
                         lambda x, y, s: dots(x, y, 2, r=4, spread=9),
                         lambda x, y, s: dots(x, y, 3, r=4, spread=9)],
                        [lambda x, y, s: dots(x, y, 2, r=4, spread=9),
                         lambda x, y, s: dots(x, y, 4, r=4, spread=9),
                         lambda x, y, s: dots(x, y, 6, r=4, spread=9)],
                        [lambda x, y, s: dots(x, y, 3, r=4, spread=9),
                         lambda x, y, s: dots(x, y, 6, r=4, spread=9),
                         lambda x, y, s: f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-size="26" '
                                         f'font-weight="800" fill="{C["red"]}">؟</text>']],
                       highlight=[(2, 2)]),
             ask="كم نقطة في الخانة الناقصة؟",
             steps=["الصف الأول: 1، 2، 3 ⇒ يزيد 1.", "الصف الثاني: 2، 4، 6 ⇒ يزيد 2.",
                    "الصف الثالث: 3، 6، … ⇒ يزيد 3 ⇒ 9."],
             answer="9 نقاط", tip=""),
        dict(id="s12", title="نفس المجموعة تتكرر في كل صف",
             fig=cgrid([[lambda x, y, s: "".join(f'<circle cx="{x + (i - 1) * s * 0.5:.1f}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}"/>' for i in range(3)),
                         lambda x, y, s: "".join(f'<circle cx="{x + (i - 0.5) * s * 0.5:.1f}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}"/>' for i in range(2)),
                         lambda x, y, s: f'<circle cx="{x}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}" />'],
                        [lambda x, y, s: "".join(f'<circle cx="{x + (i - 0.5) * s * 0.5:.1f}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}"/>' for i in range(2)),
                         lambda x, y, s: f'<circle cx="{x}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}" />',
                         lambda x, y, s: "".join(f'<circle cx="{x + (i - 1) * s * 0.5:.1f}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}"/>' for i in range(3))],
                        [lambda x, y, s: f'<circle cx="{x}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}" />',
                         lambda x, y, s: "".join(f'<circle cx="{x + (i - 1) * s * 0.5:.1f}" cy="{y}" r="{s * 0.2:.1f}" fill="{INK}"/>' for i in range(3)),
                         lambda x, y, s: f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-size="26" '
                                         f'font-weight="800" fill="{C["red"]}">؟</text>']],
                       highlight=[(2, 2)]),
             ask="كم دائرة في الخانة الناقصة؟",
             steps=["كل صف يحتوي نفس المجموعة {1، 2، 3} بترتيب مختلف.",
                    "الصف الثالث فيه: 1 then 3 ⇒ الناقص 2."],
             answer="دائرتان", tip=""),
        dict(id="s13", title="تزايد عدد الأضلاع",
             fig=crow([lambda x, y, s: f'<path d="M {x - s * 0.5} {y - s * 0.5} L {x + s * 0.5} {y + s * 0.5}" stroke="{INK}" stroke-width="3"/>',
                       lambda x, y, s: shape("triangle", x, y, s),
                       lambda x, y, s: shape("square", x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="30" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(3,)),
             ask="ما الشكل التالي؟",
             steps=["عدد الأضلاع/الخطوط: 2 then 3 then 4 ⇒ يزيد 1.", "التالي: 5 أضلاع ⇒ مخمّس."],
             answer="مخمّس (5 أضلاع)", tip=""),
        dict(id="s14", title="الدمج: شكل + شكل = شكل",
             fig=crow([lambda x, y, s: f'{shape("circle", x, y, s * 0.55)}',
                       lambda x, y, s: f'{shape("square", x, y, s * 0.5)}',
                       lambda x, y, s: f'{shape("circle", x, y, s * 0.55)}{shape("square", x, y, s * 0.28, fill=INK)}',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(3,)),
             ask="الشكل الأول + الثاني = الثالث. طبّق الفكرة.",
             steps=["لاحظ أن الشكل الثالث هو نتيجة وضع الثاني داخل الأول (دمج).",
                    "طبّق نفس الدمج على الصف الثاني من السؤال لتختار الناتج."],
             answer="الشكل الناتج عن إدخال الجزء الثاني داخل الأول في نفس الموضع",
             tip="في الدمج: انتبه لموضع الإدخال (المنتصف أم الطرف) — هذا هو الفرق بين الإجابتين المتشابهتين."),
    ],
)

# ============================================================ المكعبات
NET_A = {(1, 1): "arrow_down", (2, 1): "white_square", (3, 1): "black_triangle",
         (4, 1): "black_circle", (2, 0): "cross", (2, 2): "dots5"}
NET_B = {(1, 1): "dots5", (2, 1): "cross", (3, 1): "dots4",
         (4, 1): "white_circle", (2, 0): "black_square", (2, 2): "star"}

add(
    "cubes", "المكعبات وطي المكعبات", "#f4a261", "🎲",
    "يعطونك <b>مكعبًا مفرودًا</b> (6 مربعات) وتحتاج أن تتخيّل شكله بعد الطيّ. "
    "التخيل وحده يخطئ كثيرًا، فالحل بطرق ثابتة: <b>الاستبعاد</b>، <b>المثلثات</b>، "
    "<b>الترقيم</b>، و<b>اتجاه عقارب الساعة</b>. "
    "وقبل كل شيء: <b>اقرأ رأس السؤال</b> — هل يطلب الصحيح أم «كلها صحيح ما عدا…»؟",
    [
        "القاعدة الذهبية (الاستبعاد): أي مربعين بينهما مربع فاصل (أو فراغ) لا يمكن أن يظهرا معًا "
        "في نفس المنظور ⇒ إن ظهرا معًا في اختيار فهو خاطئ.",
        "طريقة المثلثات: الأوجه الثلاثة التي تلتقي في ركن واحد تظهر معًا ⇒ اختر منها الصحيح.",
        "طريقة الترقيم: رقم كل وجهين متقابلين بنفس الرقم؛ الصحيح يجمع 1 و2 و3، والمكرّر خاطئ "
        "(لا تُنصح بها داخل الامتحان لأنها تحتاج قلمًا).",
        "طريقة عقارب الساعة: تُستخدم عندما يثبت الوجه الأمامي في كل الاختيارات؛ "
        "تحرّك فوق ← يمين ← أسفل ← يسار؛ مع عقارب الساعة = صحيح، وعكسها = خاطئ.",
        "إن كان شكل مكرر 4 مرات وآخر مكرر مرتين ⇒ خذ 2 من الأول و1 من الثاني.",
    ],
    [
        dict(id="c1", title="الاستبعاد: الوجهان بينهما فاصل لا يجتمعان",
             fig=hstack([cube_net(NET_A),
                         cube_isometric_row(
                             [{"top": "cross", "left": "arrow_down", "right": "black_circle"},
                              {"top": "arrow_down", "left": "black_triangle", "right": "white_square"},
                              {"top": "white_square", "left": "black_circle", "right": "black_triangle"},
                              {"top": "black_triangle", "left": "cross", "right": "dots5"}],
                             L=48, gap=22, labels=["1", "2", "3", "4"])],
                        gap=26, labels=["المكعب المفرود", "الاختيارات"]),
             ask="أيّ الأشكال يمثّل المكعب بعد طيّه؟",
             steps=["حدّد الأزواج التي بينها مربع فاصل: (السهم ↔ المربع الفاضي) و(الدائرة ↔ المثلث).",
                    "هذان الزوجان لا يظهران معًا في أي منظور.",
                    "الاختيار 1: يظهر فيه السهم مع الدائرة (لا مانع بينهما) لكن اتجاه السهمين مختلف ⇒ يُستبعد.",
                    "الاختيار 3: يظهر المربع مع الدائرة وهما بينهما فاصل ⇒ خاطئ.",
                    "الاختيار 4: يظهر السهم مع المربع الفاضي وهما بينهما فاصل ⇒ خاطئ.",
                    "يبقى الاختيار 2: الوجوه الثلاثة فيه لا تمنعها قاعدة الفاصل."],
             answer="الشكل 2", tip="ارسم على المكعب المفرود علامة ✗ على كل زوج «بينهما فاصل» قبل النظر للاختيارات."),
        dict(id="c2", title="طريقة الترقيم (1،1 / 2،2 / 3،3)",
             fig=hstack([cube_net(NET_B),
                         cube_isometric_row(
                             [{"top": "dots5", "left": "dots5", "right": "cross"},
                              {"top": "white_circle", "left": "black_square", "right": "dots5"},
                              {"top": "black_square", "left": "black_square", "right": "white_circle"},
                              {"top": "cross", "left": "white_circle", "right": "star"}],
                             L=50, gap=22, labels=["1", "2", "3", "4"])],
                        gap=24, labels=["المكعب المفرود", "الاختيارات"]),
             ask="أيّ الاختيارات يمثّل مكعبًا صحيحًا؟",
             steps=["في المكعب المفرود: رقم كل وجهين بينهما فاصل بنفس الرقم ⇒ "
                    "(5 نقاط، 4 نقاط) = 1 و(الإكس، الدائرة) = 2 و(المربع الأسود، النجمة) = 3.",
                    "المنظور الصحيح يظهر وجهًا واحدًا من كل زوج: أي 1 و2 و3 معًا بدون تكرار.",
                    "الاختيار 1: يكرر «5 نقاط» مرتين ⇒ خاطئ.",
                    "الاختيار 3: يكرر المربع الأسود مرتين ⇒ خاطئ.",
                    "الاختيار 4: يظهر الإكس مع الدائرة (نفس الرقم 2) ⇒ خاطئ.",
                    "الاختيار 2: دائرة (2) + مربع أسود (3) + 5 نقاط (1) ⇒ 1 و2 و3 بدون تكرار ⇒ صحيح."],
             answer="الشكل 2", tip="الترقيم ممتاز للتدرّب في البيت، لكن في الامتحان استخدم الاستبعاد لأنه أسرع."),
        dict(id="c3", title="طريقة المثلثات (الأوجه التي تلتقي في ركن)",
             fig=cube_isometric_row(
                 [{"top": "star", "left": "star", "right": "star"},
                  {"top": "star", "left": "white_circle", "right": "white_circle"},
                  {"top": "star", "left": "star", "right": "white_circle"},
                  {"top": "white_circle", "left": "white_circle", "right": "white_circle"}],
                 L=52, gap=24, labels=["1", "2", "3", "4"]),
             ask="المكعب المفرود فيه نجمة مكررة 4 مرات ودائرة مكررة مرتين. أيّ منظور صحيح؟",
             steps=["النجمة مكررة 4 مرات والدائرة مرتان ⇒ في أي ركن تلتقي: نجمتان + دائرة.",
                    "الاختيار 1: ثلاث نجم ⇒ خاطئ (لا تلتقي ثلاث نجم في ركن واحد).",
                    "الاختيار 2: دائرتان ⇒ خاطئ (الدائرتان وجهان متقابلان).",
                    "الاختيار 4: ثلاث دوائر ⇒ خاطئ.",
                    "الاختيار 3: نجمتان + دائرة ⇒ صحيح."],
             answer="الشكل 3 (نجمتان + دائرة)",
             tip="قاعدة سريعة: مكرّر 4 مرات + مكرّر مرتين ⇒ خذ 2 من الأول و1 من الثاني."),
        dict(id="c4", title="اتجاه عقارب الساعة",
             fig=cube_isometric_row(
                 [{"top": "dots5", "left": "white_square", "right": "black_square"},
                  {"top": "black_square", "left": "dots5", "right": "white_square"},
                  {"top": "white_square", "left": "black_square", "right": "dots5"},
                  {"top": "dots4", "left": "white_square", "right": "black_square"}],
                 L=52, gap=24, labels=["1", "2", "3", "4"]),
             ask="كل الأشكال صحيحة ما عدا شكلًا واحدًا — استخرج الشكل الخاطئ.",
             steps=["هذا النوع يُحل بعقارب الساعة: علامته أن <b>الوجه الأمامي ثابت</b> في كل الاختيارات.",
                    "امشِ من الوجه الأمامي ← الأعلى ← اليمين ← الأسفل ← اليسار (ترتيب عقارب الساعة).",
                    "اختبر كل خيار: إن ظهرت الأوجه الثلاثة بنفس ترتيب عقارب الساعة ⇒ صحيح.",
                    "الاختيار 4 يخالف ترتيب بقية الاختيارات (يسير عكس عقارب الساعة) ⇒ هو الخاطئ المطلوب."],
             answer="الشكل 4", tip="ارسم بإصبعك دورة الساعة على الشكل: فوق ← يمين ← تحت ← يسار."),
        dict(id="c5", title="حل «بمجرد النظر» — عدّ الأشكال",
             fig=cube_isometric_row(
                 [{"top": "black_circle", "left": "black_circle", "right": "black_circle"},
                  {"top": "black_circle", "left": "white_square", "right": "black_circle"},
                  {"top": "dots5", "left": "white_square", "right": "black_circle"},
                  {"top": "dots5", "left": "black_circle", "right": "white_square"}],
                 L=52, gap=24, labels=["1", "2", "3", "4"]),
             ask="المكعب المفرود فيه دائرتان سوداوان فقط. أيّ شكل هو الخاطئ؟",
             steps=["عدد الدوائر السوداء في المفرود = 2 ⇒ لا يمكن أن يظهر منظور فيه 3 دوائر سوداء.",
                    "الاختيار 1 يظهر ثلاث دوائر سوداء ⇒ هو الخاطئ فورًا، بلا ترقيم ولا تخيل."],
             answer="الشكل 1", tip="قبل أي طريقة: قارن «عدد مرات تكرار كل شكل» مع ما ظهر في الاختيار."),
        dict(id="c6", title="الطول والعرض (اتجاه الوجه المجاور)",
             fig=cube_isometric_row(
                 [{"top": "dots2", "left": "black_square", "right": "cross"},
                  {"top": "dots2", "left": "cross", "right": "black_square"},
                  {"top": "cross", "left": "dots2", "right": "black_square"},
                  {"top": "black_square", "left": "dots2", "right": "cross"}],
                 L=52, gap=24, labels=["1", "2", "3", "4"]),
             ask="استخرج الشكل الخاطئ.",
             steps=["انظر للوجه المجاور: في المفرود، وجه «النقطتان» يلي وجه «الخط المتقاطع» بالطول.",
                    "أي اختيار يجعل أحد الوجهين بالعرض بدل الطول ⇒ خاطئ بمجرد النظر."],
             answer="الاختيار الذي يجاور فيه الوجه بوضع عرضي",
             tip="قاعدة الطول/العرض تنهي السؤال في ثانيتين: قارن اتجاه الرمز على الوجه المجاور."),
    ],
)

# ============================================================ التصور المكاني
add(
    "spatial", "تدوير الأشكال والتصور المكاني (بيردو)", "#48cae4", "🧊",
    "هذا نمط حديث ظهر في اختبارات التنظيم والإدارة وهو مأخوذ من <b>اختبار بيردو للتصور المكاني</b> "
    "(Purdue Spatial Visualization Test) التابع لجامعة بيردو الأمريكية، ويقيس قدرة الفرد على "
    "التدوير الذهني وإدراك الشكل من جميع الزوايا. "
    "الصيغة: «الشكل (أ) دُوِّر فأصبح (ب) — فإذا دوّرنا (ج) بنفس الطريقة فماذا ينتج؟»",
    [
        "لا تحسب عدد اللفّات — راقب <b>علامة مميزة واحدة</b> (نقطة، حرف L، زاوية، مربع ناقص ضلع) وتابع مكانها.",
        "بسّط الحركة إلى خطوتين: «تعديل/قلب» + «لفّة أو انعكاس كالمرآة».",
        "قاعدة الوشّ والضهر: إن كان الشكل الأصلي يواجهك وأعطى «ضهره» في النموذج ⇒ المطلوب أيضًا «ضهر» الشكل الثالث.",
        "قاعدة القاعدة (القاع): عند قلب الشكل تصبح القاعدة للأسفل ⇒ ما كان خلفيًا يختفي من المنظور.",
        "تدريب عملي: خذ مكعبًا حقيقيًا (أو علبة ثقاب) ودوّره بيدك مرة واثنتين وثلاثًا قبل الامتحان.",
    ],
    [
        dict(id="p1", title="حدّد نوع الحركة أولًا",
             fig=cube_isometric_row(
                 [{"top": "white_square", "left": "cross", "right": "dots3"},
                  {"top": "cross", "left": "dots3", "right": "white_square"},
                  {"top": "star", "left": "black_square", "right": "dots5"}],
                 L=54, gap=30, labels=["الشكل (أ)", "بعد التدوير (ب)", "المطلوب (ج)"]),
             ask="الشكل (أ) تحوّل إلى (ب). طبّق نفس التحويل على (ج).",
             steps=["قارن (أ) بـ(ب): أي وجه صار في الأعلى؟ وأي وجه صار أمامك؟",
                    "الوجه الذي كان على اليسار صار أمامك، والذي كان فوق صار على اليمين ⇒ حركة دوران باتجاه واحد.",
                    "طبّق نفس الدوران على (ج): حرّك الوجوه بنفس الاتجاه خطوة واحدة.",
                    "تأكد من علامة واحدة فقط (مثل المربع الأسود) أنها صارت في المكان المتوقّع."],
             answer="الشكل الذي ينتج عن نفس الدوران (اختره من البدائل بمقارنة علامة واحدة)",
             tip="لا تراقب كل الوجوه معًا — راقب علامة واحدة فقط؛ هذا أسرع وأقل خطأً."),
        dict(id="p2", title="قاعدة «الوشّ والضهر»",
             fig=cube_isometric_row(
                 [{"top": "black_square", "left": "white_circle", "right": "cross"},
                  {"top": "white_circle", "left": "cross", "right": "black_square"},
                  {"top": "star", "left": "dots5", "right": "triangle_down"}],
                 L=54, gap=30, labels=["(أ) وش", "(ب) ضهر", "(ج) المطلوب"]),
             ask="الشكل (أ) كان يواجهك فأعطى (ب) ظهره. فما ظهر (ج)؟",
             steps=["الحركة من (أ) إلى (ب): الشكل أدار لك ظهره (180° حول المحور الرأسي).",
                    "إذن المطلوب من (ج) هو «ظهره».",
                    "الظهر: المستطيل/المربع الكبير يصبح في الواجهة، والجزء المائل يبقى في مكانه النسبي.",
                    "اختر البديل الذي يظهر الجزء الخلفي الكامل."],
             answer="البديل الذي يُظهر ظهر الشكل (الجزء الخلفي الكبير)", tip=""),
        dict(id="p3", title="قاعدة القاعدة: عند القلب يختفي ما خلف",
             fig=cube_isometric_row(
                 [{"top": "black_square", "left": "dots2", "right": "cross"},
                  {"top": "white_square", "left": "dots2", "right": "cross"},
                  {"top": "star", "left": "dots3", "right": "white_circle"}],
                 L=54, gap=30, labels=["(أ)", "(ب) بعد التعديل", "(ج) المطلوب"]),
             ask="في النموذج: تم «تعديل» الشكل (إقامته على قاعدته). طبّق ذلك على (ج).",
             steps=["عند إقامة الشكل على قاعدته: القاعدة تصبح للأسفل وما كان ظاهرًا من الأعلى يبقى ظاهرًا.",
                    "الجزء الصغير الخلفي يختفي لأنه يصير خلف المنظور.",
                    "المطلوب إذن: شكل «واقف» يظهر وجهه الكامل بدون الجزء الخلفي الصغير."],
             answer="البديل الذي يظهر الشكل واقفًا على قاعدته بدون الجزء الخلفي", tip=""),
        dict(id="p4", title="الزاوية والانعكاس (كأنه أمام مرآة)",
             fig=cube_isometric_row(
                 [{"top": "cross", "left": "dots3", "right": "black_circle"},
                  {"top": "black_circle", "left": "cross", "right": "dots3"},
                  {"top": "star", "left": "white_square", "right": "dots5"}],
                 L=54, gap=30, labels=["(أ)", "(ب)", "(ج) المطلوب"]),
             ask="الزاوية انعكست في النموذج. طبّق نفس الانعكاس على (ج).",
             steps=["لاحظ النقطة/الزاوية في (أ): كانت في جهة فصارت في الجهة المعاكسة في (ب) ⇒ انعكاس مرآتي.",
                    "طبّق الانعكاس نفسه على (ج): بدّل جهة اليمين باليسار.",
                    "تجاهل البدائل التي تدوّر الشكل بدل عكسه."],
             answer="البديل المعكوس (مرآة) للشكل (ج)",
             tip="الفرق بين الدوران والانعكاس: الدوران يحافظ على ترتيب الوجوه، والانعكاس يعكسه."),
    ],
)

# ============================================================ المتطابقة والمماثلة
add(
    "identical", "الأشكال المتطابقة والمماثلة وتدوير الأشكال", "#ef5da8", "🔄",
    "المطلوب: اختر الشكل <b>المطابق تمامًا</b> للشكل المعطى — حتى لو تغيّر اتجاهه بالدوران. "
    "ثلاث طرق للحل كما شرحتها المدرّبة: <b>الاستبعاد</b>، <b>التخيّل</b>، و<b>مجرد النظر</b>. "
    "تنبيه مهم: <b>الانعكاس (المرآة) ليس تدويرًا</b> — فالشكل المنعكس ليس «نفس الشكل».",
    [
        "ابحث أولًا: هل الشكل نفسه موجود بين الخيارات بدون أي تغيير؟ إن وُجد فهو الإجابة.",
        "إن لم يوجد: تخيّل تدوير الشكل 90° أو 180° يمينًا أو يسارًا.",
        "استبعد بالصفات: أي خيار يغيّر عدد الأضلاع، أو يضيف مربعًا مكان دائرة، أو يعكس الشكل ⇒ خاطئ.",
        "في أسئلة «إذا تحوّل هذا إلى هذا»: استخرج التحويل من المثال العلوي وطبّقه حرفيًا على السفلي.",
        "في «التصور المكاني»: تخيّل أنك تنظر من أعلى (كأنك تنظر لطاولة أو لمبنى من السماء).",
    ],
    [
        dict(id="i1", title="المطابق موجود كما هو",
             fig=crow([lambda x, y, s: circle_line(x, y, s, 1, -1),
                       lambda x, y, s: f'{circle_line(x, y, s, 1, -1)}',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      highlight=(2,), labels=["الشكل", "الخيارات", ""]),
             ask="اختر الشكل المطابق.",
             steps=["الدائرة على اليمين في الشكل الأصلي ⇒ أي خيار يجعلها على اليسار يُستبعد.",
                    "الخط في المنتصف جهة اليسار ⇒ الخيار الذي يغيّر مكانه يُستبعد.",
                    "الخط السفلي جهة اليسار ⇒ الخيار الذي يوجّهه لجهة أخرى يُستبعد.",
                    "يبقى الخيار المطابق تمامًا."],
             answer="الخيار المطابق (2 في الفيديو)", tip=""),
        dict(id="i2", title="مقارنة الأرباع المظللة واحدًا واحدًا",
             fig=crow([lambda x, y, s: qsq(x, y, s, (1, 0, 1, 0)),
                       lambda x, y, s: qsq(x, y, s, (1, 0, 1, 0)),
                       lambda x, y, s: qsq(x, y, s, (0, 1, 1, 0))],
                      labels=["الأصل", "(ب)", "(ج)"]),
             ask="أيّ الخيارين (ب) أم (ج) مطابق للأصل؟",
             steps=["قارن الأرباع واحدًا واحدًا: أعلى يمين مظلل؟ — نعم في الاثنين.",
                    "أعلى يسار مظلل؟ — في (ب) نعم، وفي (ج) لا ⇒ يُستبعد (ج).",
                    "أسفل يمين وأسفل يسار: يطابقان في (ب).",
                    "(ب) هو نفس الشكل بدون أي تدوير أو انعكاس."],
             answer="(ب)", tip="لا تنظر للشكل كله مرة واحدة — قارن «ربع ربع»، فهذا يمنع الخداع البصري."),
        dict(id="i3", title="تدوير 180 درجة (وليس انعكاسًا)",
             fig=crow([lambda x, y, s: nested(x, y, s, "square", "square", "#fff", INK, n=1),
                       lambda x, y, s: nested(x, y, s, "square", "square", "#fff", INK, n=1),
                       lambda x, y, s: f'{shape("square", x, y, s, fill="#fff", stroke=INK, sw=2.6)}'
                                       f'<rect x="{x - s * 0.22:.1f}" y="{y + s * 0.25:.1f}" width="{s * 0.44:.1f}" '
                                       f'height="{s * 0.44:.1f}" fill="{INK}"/>'],
                      labels=["الأصل", "خيار (ب)", "خيار (د)"]),
             ask="مربع أبيض كبير بداخله مربع أسود صغير — أي الخيارات مطابق بعد التدوير؟",
             steps=["لا يوجد شكل مطابق تمامًا بدون تغيير ⇒ نتخيل التدوير.",
                    "الانعكاس (المرآة) مرفوض: السؤال يطلب «نفس الشكل» وليس صورته في المرآة.",
                    "ندوّر 180°: المربع الأسود ينتقل من أعلى إلى أسفل (نفس الموضع النسبي بعد نصف دورة).",
                    "الخيار (د) هو نتيجة دوران 180° ⇒ هو الصحيح."],
             answer="(د) — بعد تدوير 180°", tip="الانعكاس ≠ التدوير. هذه النقطة تسقط فيها أعلى النسب المئوية."),
        dict(id="i4", title="«إذا تحوّل هذا إلى هذا» — استخرج التحويل وطبّقه",
             fig=crow([lambda x, y, s: f'{shape("circle", x - s * 0.5, y, s * 0.4)}',
                       lambda x, y, s: f'<circle cx="{x - s * 0.5:.1f}" cy="{y:.1f}" r="{s * 0.62:.1f}" '
                                       f'fill="none" stroke="{INK}" stroke-width="2.6" stroke-dasharray="6 4"/>',
                       lambda x, y, s: f'{shape("square", x - s * 0.5, y, s * 0.36, fill=INK)}',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["(1)", "(2)", "(المطلوب)", ""]),
             ask="الدائرة الصغيرة بحدّ أسود تحوّلت إلى دائرة كبيرة منقّطة. فما نتيجة تحويل المربع الصغير الأسود؟",
             steps=["استخرج التحويل: صغير ⇒ كبير، وحدّ أسود ⇒ حدّ منقّط.",
                    "طبّقه على المربع: مربع صغير أسود ⇒ مربع كبير منقّط."],
             answer="مربع كبير منقّط", tip=""),
        dict(id="i5", title="زيادة الأضلاع للشكل الخارجي والداخلي",
             fig=crow([lambda x, y, s: nested(x, y, s, "pentagon", "square", "#fff", INK, n=2),
                       lambda x, y, s: nested(x, y, s, "hexagon", "pentagon", "#fff", INK, n=2),
                       lambda x, y, s: nested(x, y, s, "square", "triangle", "#fff", INK, n=1),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["(1)", "(2)", "(المطلوب)", ""]),
             ask="المخمّس (5) الذي بداخله مربعان تحوّل إلى مسدّس (6) بداخله مخمّسان. فما مصير المربع الذي بداخله مثلث؟",
             steps=["القاعدة: الشكل الخارجي يزيد ضلعًا (+1) والشكل الداخلي يزيد ضلعًا (+1).",
                    "مخمّس (5) ⇒ مسدّس (6)، ومربع (4) ⇒ مخمّس (5).",
                    "نطبّقها: المربع (4) ⇒ مخمّس (5)، والمثلث (3) ⇒ مربع (4)."],
             answer="مخمّس بداخله مربع", tip=""),
        dict(id="i6", title="تصغير الحجم مع بقاء الشكل",
             fig=crow([lambda x, y, s: shape("diamond", x, y, s, fill=INK),
                       lambda x, y, s: shape("diamond", x, y, s * 0.55, fill=INK),
                       lambda x, y, s: shape("pentagon", x, y, s, fill=INK),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["(1)", "(2)", "(المطلوب)", ""]),
             ask="المعيّن الكبير أصبح معيّنًا صغيرًا. فما مصير المخمّس الكبير؟",
             steps=["التحويل: نفس الشكل ولكن مصغّر، مع بقاء اللون.",
                    "إذن المخمّس الكبير الأسود ⇒ مخمّس صغير أسود."],
             answer="مخمّس صغير أسود", tip=""),
        dict(id="i7", title="الدمج في موضع محدّد (ليس المنتصف!)",
             fig=crow([lambda x, y, s: f'{shape("star", x - s * 0.9, y, s * 0.6, fill=C["gold"], stroke=INK, sw=2)}'
                                       f'<path d="M {x + s * 0.4:.1f} {y - s * 0.5:.1f} L {x + s * 1.0:.1f} {y:.1f} '
                                       f'L {x + s * 0.4:.1f} {y + s * 0.5:.1f} Z" fill="{INK}"/>',
                       lambda x, y, s: f'{shape("star", x, y, s * 0.9, fill=C["gold"], stroke=INK, sw=2)}'
                                       f'<path d="M {x + s * 0.05:.1f} {y - s * 0.35:.1f} L {x + s * 0.55:.1f} {y:.1f} '
                                       f'L {x + s * 0.05:.1f} {y + s * 0.35:.1f} Z" fill="{INK}"/>',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["النموذج", "النتيجة", "المطلوب"]),
             ask="في النموذج دُمج الشكلان بوضع الثاني قريبًا من الطرف (لا في المنتصف). طبّق ذلك.",
             steps=["تأكد من موضع الإدخال: في النموذج لم يوضع السهم في منتصف النجمة بل مال للطرف.",
                    "استبعد: السهم المقلوب، والسهم الجانبي، والسهم في اليسار، والسهم في المنتصف.",
                    "الصحيح هو الذي يضع السهم في نفس الموضع النسبي."],
             answer="الخيار (ب) — لأنه نفس الموضع النسبي",
             tip="أشهر خطأ في هذا السؤال: اختيار الشكل الذي يضع الجزء في المنتصف."),
        dict(id="i8", title="الفصل + تبديل الألوان",
             fig=crow([lambda x, y, s: two_circles(x, y, s, True, ("#fff", INK)),
                       lambda x, y, s: two_circles(x, y, s, False, (INK, "#fff")),
                       lambda x, y, s: f'{shape("square", x, y, s * 0.95, fill="#fff", stroke=INK, sw=2.6)}'
                                       f'{shape("hexagon", x, y, s * 0.42, fill=INK)}',
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["(1)", "(2)", "(المطلوب)", ""]),
             ask="الدائرتان المتداخلتان انفصلتا وتبادلتا الألوان. طبّق ذلك على المربع والسداسي.",
             steps=["ما حدث: (أ) فصل الشكلين عن بعضهما، (ب) تبديل الألوان (الأبيض صار أسود والعكس).",
                    "نُخرج السداسي من داخل المربع.",
                    "نبدّل اللونين: المربع كان أبيض ⇒ يصبح بلون السداسي (رمادي/أسود)، والسداسي ⇒ أبيض."],
             answer="مربع كبير بلون السداسي + سداسي أبيض بجانبه (الخيار د)", tip=""),
        dict(id="i9", title="التصور المكاني: النظر من أعلى",
             fig=hstack([block_count([3, 2, 2], cw=26, gap=4),
                         svg(180, 92,
                             cell(0, 0, 56, 44, "", fill="#eef4ff", stroke=C["blue"], sw=2.4)
                             + cell(58, 0, 56, 44, "", fill="#eef4ff", stroke=C["blue"], sw=2.4)
                             + cell(116, 0, 56, 44, "", fill="#eef4ff", stroke=C["blue"], sw=2.4)
                             + cell(58, 46, 56, 44, "", fill="#cfe0ff", stroke=C["blue"], sw=2.4)
                             + cell(116, 46, 56, 44, "", fill="#cfe0ff", stroke=C["blue"], sw=2.4))],
                        gap=30, labels=["المجسم (من الجانب)", "ما نراه من أعلى"]),
             ask="انظر للمجسم من أعلى: ماذا ترى؟",
             steps=["ما تحت المجسم لن تراه — انظر للسطح العلوي فقط.",
                    "الصف العلوي: 3 مربعات بالعرض.",
                    "والصف الذي يليه: مربعان (وليس ثلاثة) ⇒ أي اختيار يعطي 3 مربعات في الأسفل خاطئ.",
                    "تأكد أيضًا: المربع الملاصق على نفس المستوى أم أعلى؟"],
             answer="مستطيل من 3 مربعات + مربعان في الصف الذي يليه",
             tip="تخيّل نفسك في السماء تنظر لأسفل: ترى الأسطح فقط، ولا ترى الجوانب الجانبية."),
        dict(id="i10", title="الشكل المرسوم باليد: الاستبعاد بالصفات",
             fig=crow([lambda x, y, s: lamp(x, y, s),
                       lambda x, y, s: lamp(x, y, s),
                       lambda x, y, s: f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="28" '
                                       f'font-weight="800" fill="{C["red"]}">؟</text>'],
                      labels=["الأصل", "١", ""]),
             ask="اختر الشكل المطابق للشكل المرسوم (شبيه المصباح).",
             steps=["الصفات: جزء علوي (كالغطاء) + ذراع من 3 خطوط + دائرة مقسومة نصفين نصفها مظلل.",
                    "يُستبعد الخيار الذي يجعل الدائرة غير مظللة.",
                    "يُستبعد الخيار الذي يجعل الذراع خطّين فقط.",
                    "يُستبعد الخيار الذي يجعل الأسفل مربعًا بدل الدائرة.",
                    "الصحيح هو الذي يميل/يستند على قاعدته (دوران) مع بقاء كل الصفات."],
             answer="الخيار 1 (بعد ميل الشكل على قاعدته)", tip=""),
        dict(id="i11", title="نفس الشكل «بالعدد» (عدّ المربعات)",
             fig=svg(360, 150, f'<g transform="translate(6,10)">{block_count([5, 4, 3, 2, 1], cw=22, gap=3).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>'
                     + f'<text x="60" y="140" text-anchor="middle" font-size="15" fill="{C["dark"]}">5+4+3+2+1 = 15 مربعًا</text>'
                     + f'<g transform="translate(180,10)">{block_count([4, 4, 3, 3, 1], cw=22, gap=3).split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>'
                     + f'<text x="235" y="140" text-anchor="middle" font-size="15" fill="{C["dark"]}">4+4+3+3+1 = 15 ✓</text>'),
             ask="إن لم تجد نفس الشكل بين الخيارات، فابحث عن الشكل الذي يحتوي نفس <b>العدد</b> من المربعات.",
             steps=["عدّ مربعات الشكل الأصلي: 5 + 4 + 3 + 2 + 1 = 15.",
                    "ابحث بين الخيارات عن شكل عدد مربعاته 15 (حتى لو اختلف ترتيبها).",
                    "استبعد أي خيار مجموعه 14 أو 12."],
             answer="الشكل الذي مجموع مربعاته 15",
             tip="يأتي السؤال بصيغتين: (1) نفس الشكل بالضبط، (2) نفس الشكل بالعدد. انتبه لأي صيغة مطلوبة."),
    ],
)
