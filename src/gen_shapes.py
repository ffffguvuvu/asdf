# -*- coding: utf-8 -*-
"""بنك تدريب مولَّد للأسئلة المصوّرة: المحاور ١–١٢ و١٨ (كل شكل مرسوم داخل الملف)."""

from svgkit import (svg, bigsvg, transform, polygon, circle, dot, rect, line, star,
                    zigzag, arrow, pie, bar_split, quad_square, grid_cells,
                    question_cell, cube3d, cube_net, voxels, paper, face, place,
                    INK, BLUE, RED, GREEN, AMBER, PURPLE, PINK, TEAL, GREY, WHITE)
from genlib import gqf, rotate_options, ar

QM = svg(question_cell())


def fig(inner):
    return svg(inner)


def bfig(inner):
    return bigsvg(inner)


SYM = {
    "circle": dot(50, 50, 26, BLUE),
    "square": rect(24, 24, 52, 52, GREEN, INK, 4),
    "tri": '<polygon points="50,20 80,76 20,76" fill="%s" stroke="%s" stroke-width="4"/>' % (PINK, INK),
    "star": star(50, 50, 30, 13, 5, AMBER, INK, 3),
    "plus": line(50, 18, 50, 82, RED, 11) + line(18, 50, 82, 50, RED, 11),
    "diamond": '<polygon points="50,18 80,50 50,82 20,50" fill="%s" stroke="%s" stroke-width="3.5"/>' % (PURPLE, INK),
}
NAMES = {"circle": "الدائرة", "square": "المربع", "tri": "المثلث", "star": "النجمة",
         "plus": "الصليب", "diamond": "المعيّن"}
ARN = {3: "مثلث", 4: "مربع", 5: "خماسي", 6: "سداسي", 7: "سباعي", 8: "ثماني", 9: "تساعي", 10: "عشاري"}


# ===================================================== ١ الأشكال المتتابعة
def seq_bank():
    out, k = [], 0

    # (أ) عدد الأضلاع يزيد
    for step in (1, 2):
        for s in (3, 4, 5):
            if s + 3 * step > 10:
                continue
            sides = [s + i * step for i in range(3)]
            nxt = s + 3 * step
            opts = [fig(polygon(n, 32, fill="#dbeafe", stroke=BLUE, sw=4))
                    for n in (nxt, nxt + 1, nxt - 1, nxt + 2 if nxt + 2 <= 10 else nxt - 2)]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("ما الشكل التالي في المتتابعة؟", opts, ans,
                           [f"عدّ أضلاع كل شكل: " + "، ".join(ar(n) for n in sides) + ".",
                            f"الزيادة ثابتة = {ar(step)} ضلع في كل خطوة.",
                            f"الشكل التالي له {ar(nxt)} أضلاع ⇐ {ARN[nxt]}."],
                           [fig(polygon(n, 32, fill="#dbeafe", stroke=BLUE, sw=4)) for n in sides] + [QM],
                           tip="عُدّ الأضلاع ولا تنخدع بحجم الشكل أو لونه."))
            k += 1

    # (ب) عدد الأضلاع ينقص
    for s in (8, 7, 6):
        sides = [s - i for i in range(3)]
        nxt = s - 3
        opts = [fig(polygon(n, 32, fill="#fee2e2", stroke=RED, sw=4))
                for n in (nxt, nxt + 1, nxt + 2, nxt + 3)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الشكل التالي؟", opts, ans,
                       [f"الأضلاع: " + "، ".join(ar(n) for n in sides) + " ⇐ تنقص ضلعًا في كل خطوة.",
                        f"الشكل التالي له {ar(nxt)} أضلاع ⇐ {ARN[nxt]}.",
                        "النمط تنازلي، فلا تختر شكلًا أكبر."],
                       [fig(polygon(n, 32, fill="#fee2e2", stroke=RED, sw=4)) for n in sides] + [QM],
                       tip="المتتابعة قد تنقص لا تزيد؛ تأكّد من الاتجاه أولًا."))
        k += 1

    # (ج) دوران السهم
    for step, name in ((90, "ربع دورة"), (45, "ثُمن دورة"), (-90, "ربع دورة عكس العقارب")):
        for s in (0, 90, 180):
            angs = [s + i * step for i in range(3)]
            nxt = s + 3 * step
            opts = [fig(arrow(a, BLUE, 7)) for a in (nxt, nxt + 90, nxt + 180, nxt - 90)]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("إلى أين يشير السهم التالي؟", opts, ans,
                           [f"السهم يدور {ar(abs(step))}° في كل خطوة ({name}).",
                            f"المواضع: " + "، ".join(f"{ar(a % 360)}°" for a in angs) + ".",
                            f"الموضع التالي = {ar(nxt % 360)}°."],
                           [fig(arrow(a, BLUE, 7)) for a in angs] + [QM],
                           tip="حدّد زاوية الدوران من أول خطوتين ثم كرّرها."))
            k += 1

    # (د) تظليل متزايد في شريط
    for n in (4, 5, 6):
        for start in (1, 2):
            vals = [start + i for i in range(3)]
            nxt = start + 3
            if nxt > n:
                continue
            cand = [nxt, nxt - 1, nxt + 1, nxt - 2, n, 0]
            vals4, seen = [], set()
            for v in cand:
                if 0 <= v <= n and v not in seen:
                    seen.add(v); vals4.append(v)
                if len(vals4) == 4:
                    break
            opts = [fig(bar_split(n, v)) for v in vals4]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("ما الشكل التالي في المتتابعة؟", opts, ans,
                           [f"الشريط مقسّم إلى {ar(n)} خانات.",
                            f"عدد الخانات المظللة: " + "، ".join(ar(v) for v in vals) + " ⇐ تزيد خانة واحدة.",
                            f"التالي = {ar(nxt)} خانات مظللة من {ar(n)}."],
                           [fig(bar_split(n, v)) for v in vals] + [QM],
                           tip="اكتب الكسر: ١/٥ ثم ٢/٥ ثم ٣/٥ … يسهل عليك التتبّع."))
            k += 1

    # (هـ) دوران التظليل في دائرة مقسّمة
    for parts in (4, 8):
        for s in range(2):
            shaded = [(s + i) % parts for i in range(3)]
            nxt = (s + 3) % parts
            opts = [fig(pie(parts, (v,), fill=PURPLE))
                    for v in (nxt, (nxt + 1) % parts, (nxt + 2) % parts, (nxt + 3) % parts)]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("ما الشكل التالي؟", opts, ans,
                           ["الجزء المظلل يتحرك خطوة واحدة مع عقارب الساعة في كل شكل.",
                            f"الدائرة مقسّمة إلى {ar(parts)} أجزاء، والمظلل ينتقل: " +
                            "، ".join(f"الجزء {ar(v + 1)}" for v in shaded) + ".",
                            f"التالي = الجزء {ar(nxt + 1)}."],
                           [fig(pie(parts, (v,), fill=PURPLE)) for v in shaded] + [QM],
                           tip="ثبّت نقطة مرجعية (أعلى الدائرة) وعُدّ منها."))
            k += 1

    # (و) عدد النقاط داخل شكل
    for shape_n in (3, 4, 6):
        for step in (1, 2):
            counts = [1 + i * step for i in range(3)]
            nxt = 1 + 3 * step

            def with_dots(c):
                inner = polygon(shape_n, 34, fill="#ecfdf5", stroke=GREEN, sw=4)
                xs = [(50, 38), (38, 58), (62, 58), (50, 66), (34, 46), (66, 46), (50, 50)]
                for i in range(c):
                    x, y = xs[i % len(xs)]
                    inner += dot(x, y, 5.5, GREEN)
                return inner
            opts = [fig(with_dots(c)) for c in (nxt, nxt + 1, nxt - 1, nxt + 2)]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("أكمل المتتابعة.", opts, ans,
                           [f"الشكل ثابت ({ARN[shape_n]})، والمتغيّر هو عدد النقاط.",
                            f"عدد النقاط: " + "، ".join(ar(c) for c in counts) + f" ⇐ الزيادة {ar(step)}.",
                            f"التالي = {ar(nxt)} نقاط."],
                           [fig(with_dots(c)) for c in counts] + [QM],
                           tip="لو ثبت الشكل فالتغيير في التفاصيل: النقاط أو الخطوط أو التظليل."))
            k += 1

    # (ز) خطوط الزجزاج
    for s in (2, 3, 4):
        segs = [s + i for i in range(3)]
        nxt = s + 3
        opts = [fig(zigzag(n)) for n in (nxt, nxt + 1, nxt - 1, nxt + 2)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الشكل التالي؟", opts, ans,
                       [f"عدّ أضلاع الخط المنكسر: " + "، ".join(ar(n) for n in segs) + ".",
                        "الزيادة ضلع واحد في كل خطوة.",
                        f"التالي = {ar(nxt)} أضلاع."],
                       [fig(zigzag(n)) for n in segs] + [QM],
                       tip="عُدّ القمم أو الأضلاع بإصبعك على الشاشة حتى لا تخطئ."))
        k += 1

    # (ح) الحجم يتدرّج
    for color, st in ((BLUE, "#dbeafe"), (GREEN, "#dcfce7"), (PURPLE, "#ede9fe")):
        radii = [14, 20, 26]
        nxt = 32
        opts = [fig(circle(50, 50, r, st, color, 4)) for r in (nxt, 26, 20, 38)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الشكل التالي في المتتابعة؟", opts, ans,
                       ["الشكل نفسه يتكرّر لكن حجمه يكبر بانتظام.",
                        "الزيادة في نصف القطر ثابتة في كل خطوة.",
                        "إذن التالي هو الدائرة الأكبر بنفس مقدار الزيادة."],
                       [fig(circle(50, 50, r, st, color, 4)) for r in radii] + [QM],
                       tip="قِس بالعين نسبة الكبر بين الأول والثاني ثم طبّقها على الأخير."))
        k += 1

    # (ط) دوران شكل غير متماثل
    motif = ('<polygon points="26,26 62,26 62,46 44,46 44,74 26,74" fill="#fde68a" '
             f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>' + dot(33, 33, 5, RED))
    for step in (90, 180, -90):
        angs = [0, step, 2 * step]
        nxt = 3 * step
        opts = [fig(transform(motif, rotate=a)) for a in (nxt, nxt + 90, nxt + 180, nxt - 90)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أكمل نمط التدوير.", opts, ans,
                       [f"الشكل نفسه يدور {ar(abs(step))}° في كل خطوة" +
                        (" مع عقارب الساعة." if step > 0 else " عكس عقارب الساعة."),
                        "النقطة الحمراء علامة مرجعية تتبع الدوران.",
                        f"بعد ثلاث خطوات يكون الدوران الكلي = {ar(abs(nxt) % 360)}°."],
                       [fig(transform(motif, rotate=a)) for a in angs] + [QM],
                       tip="تتبّع العلامة الحمراء وحدها؛ أسرع من تتبّع الشكل كله."))
        k += 1

    return out


# ===================================================== ٣ المصفوفات
def matrix_bank():
    out, k = [], 0

    # (أ) عدد النقاط يزيد عبر الصفوف
    def dots_cell(c, color=BLUE):
        pos = [(30, 30), (50, 30), (70, 30), (30, 50), (50, 50), (70, 50),
               (30, 70), (50, 70), (70, 70)]
        return "".join(dot(x, y, 7, color) for x, y in pos[:c])
    for start in (1, 2):
        for step in (1, 2):
            cells, vals = [], []
            for r in range(3):
                for c in range(3):
                    v = start + (r * 3 + c) * step
                    vals.append(v)
                    cells.append(None if (r, c) == (2, 2) else dots_cell(min(v, 9)))
            nxt = min(vals[-1], 9)
            cand = [nxt, nxt - 1, nxt + 1, nxt - 2, nxt + 2, nxt - 3]
            vals4, seen = [], set()
            for v in cand:
                if 1 <= v <= 9 and v not in seen:
                    seen.add(v); vals4.append(v)
                if len(vals4) == 4:
                    break
            opts = [fig(dots_cell(v)) for v in vals4]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("أكمل المصفوفة (الخانة الفارغة).", opts, ans,
                           [f"اقرأ الصفوف من اليسار لليمين: عدد النقاط " + "، ".join(ar(v) for v in vals[:3]) + " …",
                            f"الزيادة ثابتة = {ar(step)} نقطة بين كل خانة والتي تليها.",
                            f"الخانة الأخيرة = {ar(nxt)} نقاط."],
                           [bfig(grid_cells(cells))],
                           stem_note="اقرأ المصفوفة من اليسار إلى اليمين ومن أعلى لأسفل.",
                           tip="عالج المصفوفة صفًّا صفًّا ثم تحقّق بالأعمدة."))
            k += 1

    # (ب) دوران سهم داخل المصفوفة
    for step in (45, 90):
        cells = []
        angs = []
        for i in range(9):
            a = i * step
            angs.append(a)
            cells.append(None if i == 8 else arrow(a, PINK, 6))
        nxt = 8 * step
        opts = [fig(arrow(a, PINK, 6)) for a in (nxt, nxt + 90, nxt + 180, nxt - 90)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الخانة الناقصة؟", opts, ans,
                       [f"السهم يدور {ar(step)}° في كل خانة مع عقارب الساعة.",
                        f"في الخانة الأخيرة يكون الدوران الكلي = {ar(nxt % 360)}°.",
                        "إذن السهم المطلوب يشير إلى ذلك الاتجاه."],
                       [bfig(grid_cells(cells))],
                       stem_note="القراءة من اليسار لليمين.",
                       tip="احسب الدوران التراكمي لا الفرق بين خانتين فقط."))
        k += 1

    # (ج) تجميع الخطوط (العمود الثالث = اتحاد العمودين)
    parts = {"v": line(50, 16, 50, 84, PURPLE, 6), "h": line(16, 50, 84, 50, PURPLE, 6),
             "d1": line(22, 22, 78, 78, PURPLE, 6), "d2": line(78, 22, 22, 78, PURPLE, 6)}
    combos = [(("v",), ("h",), ("v", "h")), (("d1",), ("d2",), ("d1", "d2")),
              (("v",), ("d1",), ("v", "d1")), (("h",), ("d2",), ("h", "d2"))]
    for a, b, c in combos:
        cells = []
        rows = [(a, b, c), (b, c, tuple(sorted(set(b) | set(c)))), (a, c, None)]
        for r, (x, y, z) in enumerate(rows):
            cells.append("".join(parts[p] for p in x))
            cells.append("".join(parts[p] for p in y))
            cells.append(None if z is None else "".join(parts[p] for p in z))
        target = tuple(sorted(set(a) | set(c)))
        wrongs = [("v", "h", "d1", "d2"), a, c]
        opts = [fig("".join(parts[p] for p in t)) for t in [target] + wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الشكل الناقص في المصفوفة؟", opts, ans,
                       ["القاعدة في كل صف: الخانة الثالثة = الأولى + الثانية (اتحاد الخطوط).",
                        "تحقّق من الصف الأول ثم الثاني قبل التطبيق.",
                        "طبّق القاعدة على الصف الثالث: اجمع خطوط الخانتين الأوليين."],
                       [bfig(grid_cells(cells))],
                       stem_note="الخانة الثالثة في كل صف = دمج الخانتين قبلها.",
                       tip="لا تضف خطًا غير موجود في الخانتين؛ أشهر فخ في المصفوفات."))
        k += 1

    # (د) الشكل ثابت واللون/التظليل يتغيّر
    for shape_n, color in ((3, PINK), (4, GREEN), (6, BLUE)):
        fills = ["#ffffff", "#e5e7eb", "#9ca3af"]
        cells = []
        for r in range(3):
            for c in range(3):
                if (r, c) == (2, 2):
                    cells.append(None)
                else:
                    cells.append(polygon(shape_n, 28, fill=fills[c], stroke=color, sw=3.5))
        opts = [fig(polygon(shape_n, 28, fill=f, stroke=color, sw=3.5))
                for f in (fills[2], fills[0], fills[1], "#fecaca")]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أكمل المصفوفة.", opts, ans,
                       [f"الشكل ثابت في كل الخانات ({ARN[shape_n]}).",
                        "التظليل يتدرّج داخل كل صف: فاتح ← متوسط ← غامق.",
                        "الخانة الناقصة في نهاية الصف ⇐ التظليل الغامق."],
                       [bfig(grid_cells(cells))],
                       tip="افصل المتغيّرات: الشكل وحده، اللون وحده، العدد وحده."))
        k += 1

    # (هـ) تناوب شكلين وثالث
    trio = [["circle", "square", "tri"], ["square", "tri", "circle"], ["tri", "circle", None]]
    for shift in range(3):
        cells = []
        for r in range(3):
            for c in range(3):
                nm = trio[r][c]
                if nm is None:
                    cells.append(None)
                else:
                    idx = (["circle", "square", "tri"].index(nm) + shift) % 3
                    cells.append(SYM[["circle", "square", "tri"][idx]])
        target = ["circle", "square", "tri"][(["circle", "square", "tri"].index("square") + shift) % 3]
        others = [n for n in ("circle", "square", "tri", "diamond") if n != target][:3]
        opts = [fig(SYM[target])] + [fig(SYM[n]) for n in others]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما الشكل الناقص؟", opts, ans,
                       ["كل صف يحتوي الأشكال الثلاثة مرة واحدة فقط (مثل لعبة سودوكو).",
                        "وكذلك كل عمود لا يتكرّر فيه الشكل.",
                        f"الشكل الغائب من الصف الأخير هو {NAMES[target]}."],
                       [bfig(grid_cells(cells))],
                       tip="قاعدة «لا تكرار في الصف ولا العمود» تحسم كثيرًا من المصفوفات."))
        k += 1

    return out


# ============================================ ٤ و٥ التطابق والتدوير والمرايا
_MOTIFS = [
    ('<polygon points="24,70 44,30 64,54 76,34" fill="none" stroke="%s" stroke-width="5" '
     'stroke-linejoin="round" stroke-linecap="round"/>' % BLUE) + dot(76, 34, 6, RED),
    (rect(26, 30, 44, 44, "#bfdbfe", INK, 3.5) + dot(66, 38, 6, RED) +
     '<polygon points="22,52 34,44 34,60" fill="%s" stroke="%s" stroke-width="2"/>' % (AMBER, INK)),
    ('<path d="M 24 72 L 50 24 L 76 72 Z" fill="#dcfce7" stroke="%s" stroke-width="3.5"/>' % INK +
     dot(40, 60, 5.5, GREEN) + dot(62, 60, 5.5, RED)),
    (line(24, 76, 24, 24, PURPLE, 5) + line(24, 24, 68, 38, PURPLE, 5) + dot(68, 38, 6, RED)),
    (rect(28, 28, 44, 44, "#fef3c7", INK, 3.5) + line(28, 28, 72, 72, AMBER, 4) + dot(36, 64, 5.5, RED)),
    ('<polygon points="30,24 70,24 70,48 50,48 50,76 30,76" fill="#fbcfe8" stroke="%s" '
     'stroke-width="3.5" stroke-linejoin="round"/>' % INK + dot(60, 34, 5, INK)),
]


def rotate_bank():
    out, k = [], 0
    for mi, motif in enumerate(_MOTIFS):
        # مطابق تمامًا
        opts = [fig(motif), fig(transform(motif, rotate=90)),
                fig(transform(motif, mirror="h")), fig(transform(motif, rotate=180))]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أي الأشكال مطابق تمامًا للشكل المعطى (بنفس الاتجاه)؟", opts, ans,
                       ["السؤال يطلب المطابق بنفس الاتجاه، لا المُدار ولا المعكوس.",
                        "استبعد كل شكل تغيّر فيه موضع العلامة المميزة.",
                        "الشكل الباقي بلا أي تغيير هو الإجابة."],
                       [fig(motif)],
                       tip="«مطابق» غير «مماثل»: الأولى بنفس الاتجاه والثانية تقبل التدوير."))
        k += 1
        # تدوير محدد
        for deg in (90, 180, 270):
            opts = [fig(transform(motif, rotate=deg)), fig(transform(motif, rotate=(deg + 90) % 360)),
                    fig(transform(motif, rotate=(deg + 180) % 360)), fig(transform(motif, mirror="h"))]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf(f"أي شكل يمثّل الشكل المعطى بعد تدويره {ar(deg)}° مع عقارب الساعة؟", opts, ans,
                           [f"تدوير {ar(deg)}° يعني " +
                            {90: "ربع دورة: ما كان أعلى يصير يمينًا.",
                             180: "نصف دورة: الشكل ينقلب رأسًا على عقب.",
                             270: "ثلاثة أرباع دورة: ما كان أعلى يصير يسارًا."}[deg],
                            "تتبّع العلامة المميزة (النقطة أو الزاوية البارزة) وحدد موضعها الجديد.",
                            "الاختيار الوحيد الذي يضع العلامة في موضعها الصحيح هو الإجابة."],
                           [fig(motif)],
                           tip="لفّ الورقة فعليًا بزاوية السؤال إن سُمح لك؛ أسرع وأدق."))
            k += 1
        # المرآة
        for axis, desc in (("h", "مرآة رأسية (يمين ↔ يسار)"), ("v", "مرآة أفقية (أعلى ↔ أسفل)")):
            opts = [fig(transform(motif, mirror=axis)), fig(transform(motif, rotate=180)),
                    fig(motif), fig(transform(motif, rotate=90))]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf(f"ما صورة الشكل في {desc}؟", opts, ans,
                           [f"{desc}: ينعكس أحد المحورين فقط ويبقى الآخر كما هو.",
                            "الانعكاس ليس تدويرًا: في التدوير يتغيّر المحوران معًا.",
                            "تتبّع العلامة المميزة: أين تقع بعد الانعكاس؟"],
                           [fig(motif)],
                           tip="أشهر فخ: اختيار تدوير ١٨٠° بدل المرآة."))
            k += 1
        # الشاذ عن التدويرات (مرآة وسط تدويرات)
        opts = [fig(transform(motif, mirror="h")), fig(motif),
                fig(transform(motif, rotate=90)), fig(transform(motif, rotate=180))]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ثلاثة أشكال تدويرات لشكل واحد، فأيها الشاذ (صورة مرآة)؟", opts, ans,
                       ["اقرأ ترتيب العلامات في اتجاه عقارب الساعة في كل شكل.",
                        "التدوير يحافظ على هذا الترتيب مهما تغيّر وضع الشكل.",
                        "الشكل الذي انقلب فيه الترتيب هو صورة المرآة ⇐ الشاذ."],
                       None,
                       tip="حيلة: اقرأ العلامات في اتجاه واحد؛ انقلاب الترتيب = مرآة."))
        k += 1
    return out


# ===================================================== ٦ طي الورق والقصّ
def fold_bank():
    out, k = [], 0
    half_positions = [(0.35, 0.3), (0.3, 0.6), (0.5, 0.45), (0.6, 0.35), (0.4, 0.7)]
    for (hx, hy) in half_positions:
        # طيّة رأسية واحدة
        x = 16 + 68 * hx / 2 + 34
        y = 16 + 68 * hy
        folded = paper(holes=[(x, y)], x=50, y=16, s=34, fill="#fde68a")
        mx = 100 - x
        correct = paper(holes=[(x, y), (mx, y)])
        wrongs = [paper(holes=[(x, y)]), paper(holes=[(x, y), (x, 100 - y)]),
                  paper(holes=[(x, y), (mx, y), (x, 100 - y), (mx, 100 - y)])]
        opts = [fig(correct)] + [fig(w) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ورقة طُويت نصفين ثم ثُقبت. كيف تبدو بعد فردها؟", opts, ans,
                       ["الطيّة واحدة ⇒ عدد الثقوب يتضاعف: ثقب واحد ⇐ ثقبان.",
                        "الثقب الجديد يقابل الأصلي تمامًا على الجهة الأخرى من خط الطي.",
                        "ارتفاع الثقبين واحد؛ المتغيّر هو الجهة فقط."],
                       [fig(paper(folds=["v"])), fig(folded), QM],
                       stem_note="الورقة ← بعد الطي والثقب ← المطلوب بعد الفرد",
                       tip="عدد الثقوب = الثقوب المرسومة × ٢ لكل طيّة."))
        k += 1
        # طيّة أفقية واحدة
        xh = 16 + 68 * hx
        yh = 16 + 68 * hy / 2 + 34
        folded_h = paper(holes=[(xh, yh)], x=16, y=50, s=34, fill="#fde68a")
        correct_h = paper(holes=[(xh, yh), (xh, 100 - yh)])
        wrongs_h = [paper(holes=[(xh, yh)]), paper(holes=[(xh, yh), (100 - xh, yh)]),
                    paper(holes=[(xh, yh), (100 - xh, 100 - yh)])]
        opts = [fig(correct_h)] + [fig(w) for w in wrongs_h]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("طيّة أفقية واحدة وثقب واحد: ما شكل الورقة بعد الفرد؟", opts, ans,
                       ["خط الطي أفقي ⇒ الانعكاس يكون لأعلى/لأسفل.",
                        "الثقب ينعكس فوق خط الطي بنفس البُعد عنه.",
                        "الجهة اليمنى/اليسرى لا تتغيّر."],
                       [fig(paper(folds=["h"])), fig(folded_h), QM],
                       tip="حدّد محور الطي أولًا؛ هو الذي يحدد اتجاه الانعكاس."))
        k += 1
    # طيّتان
    for (hx, hy) in [(0.4, 0.4), (0.6, 0.35), (0.35, 0.65)]:
        x = 33 + 34 * hx
        y = 33 + 34 * hy
        quarter = paper(holes=[(x, y)], x=33, y=33, s=34, fill="#fde68a")
        pts = [(x, y), (100 - x, y), (x, 100 - y), (100 - x, 100 - y)]
        correct = paper(holes=pts, folds=["v", "h"])
        wrongs = [paper(holes=pts[:2], folds=["v", "h"]), paper(holes=pts[:1], folds=["v", "h"]),
                  paper(holes=[pts[0], pts[3]], folds=["v", "h"])]
        opts = [fig(correct)] + [fig(w) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ورقة طُويت مرتين (رأسيًا ثم أفقيًا) ثم ثُقبت ثقبًا واحدًا. كم ثقبًا بعد الفرد وأين؟",
                       opts, ans,
                       ["عدد الطيّات = ٢ ⇒ عدد الثقوب = ٢² = ٤ ثقوب.",
                        "كل ثقب ينعكس حول المحور الرأسي ثم حول الأفقي.",
                        "النتيجة أربعة ثقوب متناظرة حول مركز الورقة."],
                       [fig(paper(folds=["v", "h"])), fig(quarter), QM],
                       tip="احفظ: ثقب واحد و n طيّة ⇐ ٢ أُس n من الثقوب."))
        k += 1
    return out


# ===================================================== ٧ المكعبات
NET_SETS = [
    {0: "circle", 1: "star", 2: "square", 3: "tri", 4: "plus", 5: "diamond"},
    {0: "star", 1: "square", 2: "diamond", 3: "circle", 4: "tri", 5: "plus"},
    {0: "plus", 1: "tri", 2: "circle", 3: "diamond", 4: "square", 5: "star"},
    {0: "square", 1: "diamond", 2: "star", 3: "plus", 4: "circle", 5: "tri"},
    {0: "diamond", 1: "circle", 2: "tri", 3: "star", 4: "plus", 5: "square"},
    {0: "tri", 1: "plus", 2: "star", 3: "square", 4: "diamond", 5: "circle"},
]
OPP = [(0, 2), (1, 3), (4, 5)]


def _opp_pairs(net):
    return {frozenset((net[a], net[b])) for a, b in OPP}


def _ok(view, pairs):
    return len(set(view)) == 3 and not any(
        frozenset(p) in pairs for p in ((view[0], view[1]), (view[0], view[2]), (view[1], view[2])))


def cube_bank():
    out, k = [], 0
    for net in NET_SETS:
        pairs = _opp_pairs(net)
        names = list(net.values())
        # س: أي مكعب يمكن تكوينه
        good = None
        bad = []
        for i in range(6):
            for j in range(6):
                for m in range(6):
                    v = (names[i], names[j], names[m])
                    if _ok(v, pairs) and good is None:
                        good = v
                    elif len(set(v)) == 3 and not _ok(v, pairs) and len(bad) < 3:
                        if all(v != b for b in bad):
                            bad.append(v)
        opts = [fig(cube3d(SYM[good[0]], SYM[good[1]], SYM[good[2]]))] + \
               [fig(cube3d(SYM[b[0]], SYM[b[1]], SYM[b[2]])) for b in bad]
        opts, ans = rotate_options(opts, 0, k)
        pair_txt = "، و".join(f"{NAMES[list(p)[0]]} ↔ {NAMES[list(p)[1]]}" for p in pairs)
        out.append(gqf("أي مكعب يمكن تكوينه من الشبكة المفرودة؟", opts, ans,
                       [f"من الشبكة نستخرج المتقابلات: {pair_txt}.",
                        "أي صورة تجمع وجهين متقابلين = مستحيلة.",
                        f"الاختيار الصحيح يجمع: {NAMES[good[0]]} و{NAMES[good[1]]} و{NAMES[good[2]]} وكلها متجاورة."],
                       [bfig(cube_net({i: SYM[n] for i, n in net.items()}))],
                       stem_note="القاعدة: في الصف الأفقي الأول ↔ الثالث والثاني ↔ الرابع، والعلوي ↔ السفلي.",
                       tip="اكتب المتقابلات الثلاثة فور رؤية الشبكة قبل النظر للاختيارات."))
        k += 1
        # س: الوجه المقابل
        for idx in (0, 1, 4):
            target = net[[b for a, b in OPP + [(b, a) for a, b in OPP] if a == idx][0]]
            others = [n for n in names if n not in (net[idx], target)][:3]
            opts = [fig(SYM[target])] + [fig(SYM[n]) for n in others]
            opts, ans = rotate_options(opts, 0, k)
            pos = {0: "الأول في الصف", 1: "الثاني في الصف", 4: "العلوي"}[idx]
            rule = {0: "الأول يقابل الثالث", 1: "الثاني يقابل الرابع", 4: "العلوي يقابل السفلي"}[idx]
            out.append(gqf(f"أي رمز يقع على الوجه المقابل لـ{NAMES[net[idx]]}؟", opts, ans,
                           [f"{NAMES[net[idx]]} هو الوجه {pos} في الشبكة.",
                            f"القاعدة: {rule}.",
                            f"إذن المقابل هو {NAMES[target]}."],
                           [bfig(cube_net({i: SYM[n] for i, n in net.items()}))],
                           tip="في صفّ من أربعة: اقفز وجهًا واحدًا لتصل إلى المقابل."))
            k += 1
        # س: المكعب المستحيل
        impossible = None
        possibles = []
        for i in range(6):
            for j in range(6):
                for m in range(6):
                    v = (names[i], names[j], names[m])
                    if len(set(v)) != 3:
                        continue
                    if _ok(v, pairs) and len(possibles) < 3 and all(v != p for p in possibles):
                        possibles.append(v)
                    elif not _ok(v, pairs) and impossible is None:
                        impossible = v
        opts = [fig(cube3d(SYM[impossible[0]], SYM[impossible[1]], SYM[impossible[2]]))] + \
               [fig(cube3d(SYM[p[0]], SYM[p[1]], SYM[p[2]])) for p in possibles]
        opts, ans = rotate_options(opts, 0, k)
        bad_pair = [p for p in ((impossible[0], impossible[1]), (impossible[0], impossible[2]),
                                (impossible[1], impossible[2])) if frozenset(p) in pairs][0]
        out.append(gqf("كل المكعبات ممكنة من الشبكة ما عدا واحدًا. أيّها المستحيل؟", opts, ans,
                       [f"المتقابلات من الشبكة: {pair_txt}.",
                        "افحص كل صورة: هل تجمع وجهين متقابلين؟",
                        f"الصورة المستحيلة تجمع {NAMES[bad_pair[0]]} مع {NAMES[bad_pair[1]]} وهما متقابلان."],
                       [bfig(cube_net({i: SYM[n] for i, n in net.items()}))],
                       tip="انتبه: السؤال يطلب المستحيل لا الممكن."))
        k += 1
    # س: نفس المكعب بعد التدوير (الترتيب الدوري)
    for base in [("circle", "star", "square"), ("tri", "plus", "diamond"),
                 ("star", "square", "circle"), ("plus", "circle", "tri")]:
        same = (base[1], base[2], base[0])
        mirrors = [(base[2], base[1], base[0]), (base[0], base[2], base[1]), (base[1], base[0], base[2])]
        opts = [fig(cube3d(SYM[same[0]], SYM[same[1]], SYM[same[2]]))] + \
               [fig(cube3d(SYM[m[0]], SYM[m[1]], SYM[m[2]])) for m in mirrors]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أي مكعب هو نفس المكعب المعروض بعد تدويره؟", opts, ans,
                       ["الوجوه الثلاثة تلتقي عند رأس واحد، وترتيبها الدوري لا يتغيّر بالتدوير.",
                        f"الترتيب في الأصل: {NAMES[base[0]]} ← {NAMES[base[1]]} ← {NAMES[base[2]]}.",
                        "الاختيار الصحيح يحافظ على نفس الترتيب الدوري (ولو بدأ من رمز آخر).",
                        "الاختيارات الأخرى ترتيبها معكوس ⇐ مكعب مرآة مختلف."],
                       [bfig(cube3d(SYM[base[0]], SYM[base[1]], SYM[base[2]]))],
                       tip="دوّر الأسماء دورانًا دائريًا؛ إن تطابقت فهو نفس المكعب."))
        k += 1
    return out


# ============================================ ٨ التصور المكاني (المجسمات)
SOLIDS = [
    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (0, 0, 1)],
    [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1), (2, 1, 1)],
    [(0, 0, 0), (1, 0, 0), (1, 0, 1), (2, 0, 1), (2, 0, 2)],
    [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 1, 1)],
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (1, 0, 1)],
]


def _norm(vs):
    mx, my, mz = (min(v[i] for v in vs) for i in range(3))
    return tuple(sorted((x - mx, y - my, z - mz) for x, y, z in vs))


def spatial_bank():
    from svgkit import _rot_vox
    out, k = [], 0
    for solid in SOLIDS:
        mirror = [(-x, y, z) for x, y, z in solid]
        rots = {_norm([_rot_vox(v, rx, ry, rz) for v in solid])
                for rx in range(4) for ry in range(4) for rz in range(4)}
        chiral = _norm(mirror) not in rots
        # عدد المكعبات
        n = len(solid)
        opts = [fig(f'<text x="50" y="62" font-size="42" text-anchor="middle" '
                    f'fill="{INK}" font-weight="800">{ar(v)}</text>')
                for v in (n, n + 1, n - 1, n + 2)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("كم مكعبًا صغيرًا يتكوّن منه المجسم؟", opts, ans,
                       ["عُدّ المكعبات طبقة طبقة من الأسفل لأعلى.",
                        "لا تنسَ المكعبات المختفية خلف غيرها (التي تحمل مكعبًا فوقها لا بد أن تكون موجودة).",
                        f"المجموع = {ar(n)} مكعبات."],
                       [bfig(voxels(solid, u=12))],
                       tip="أي مكعب معلّق في الهواء يعني وجود مكعب تحته لا تراه."))
        k += 1
        # المنظر العلوي
        top = sorted({(x, y) for x, y, _ in solid})
        maxc = max(c for c, _ in top) + 1
        maxr = max(r for _, r in top) + 1

        def grid_top(cells, cols=3, rows=3):
            inner = ""
            s = 22
            for r in range(rows):
                for c in range(cols):
                    fillc = "#93c5fd" if (c, r) in cells else WHITE
                    inner += rect(14 + c * s, 14 + r * s, s, s, fillc, INK, 2)
            return inner
        wrong1 = {(c, r) for c, r in top if c > 0} or {(0, 0)}
        wrong2 = {((c + 1) % 3, r) for c, r in top}
        wrong3 = set(top) | {(maxc % 3, maxr % 3)}
        opts = [fig(grid_top(set(top)))] + [fig(grid_top(w)) for w in (wrong1, wrong2, wrong3)]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما المنظر العلوي للمجسم (الرؤية من أعلى)؟", opts, ans,
                       ["المنظر العلوي = ظل المجسم على الأرض: أي مربع يوجد فوقه مكعب واحد على الأقل.",
                        "الارتفاع لا يظهر في المنظر العلوي إطلاقًا، والاتجاه يبقى كما هو (اليمين يمين واليسار يسار).",
                        f"المربعات المشغولة عددها {ar(len(top))}."],
                       [bfig(voxels(solid, u=12))],
                       tip="تخيّل أنك تنظر من السقف: الطول يختفي ويبقى الموضع."))
        k += 1
        # نفس المجسم بعد التدوير
        if chiral:
            opts = [bfig(voxels(solid, rz=1, u=11)), bfig(voxels(mirror, u=11)),
                    bfig(voxels(mirror, rz=1, u=11)), bfig(voxels(mirror, ry=2, u=11))]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("أي مجسم هو نفس المجسم المعطى بعد تدويره (وليس صورته في المرآة)؟", opts, ans,
                           ["التدوير يحافظ على «يد» المجسم (اتجاه الالتفاف)، أما المرآة فتعكسه.",
                            "تتبّع اتجاه الدرجة العليا بالنسبة لقاعدة المجسم.",
                            "ثلاثة اختيارات هي أوضاع مختلفة لصورة المرآة، وواحد فقط دوران حقيقي للأصل."],
                           [bfig(voxels(solid, u=11))],
                           tip="المجسم اللولبي لا ينطبق على صورته في المرآة مهما درت به."))
            k += 1
    return out


# ===================================================== ١٠ الدمج والطرح
PARTS = {"v": line(50, 14, 50, 86, BLUE, 6), "h": line(14, 50, 86, 50, BLUE, 6),
         "d1": line(22, 22, 78, 78, BLUE, 6), "d2": line(78, 22, 22, 78, BLUE, 6),
         "o": circle(50, 50, 24, "none", BLUE, 5), "sq": rect(24, 24, 52, 52, "none", BLUE, 5),
         "tri": '<polygon points="50,22 78,74 22,74" fill="none" stroke="%s" stroke-width="5"/>' % BLUE}
PNAMES = {"v": "خط رأسي", "h": "خط أفقي", "d1": "قطر مائل", "d2": "قطر معاكس",
          "o": "دائرة", "sq": "مربع", "tri": "مثلث"}


def _draw(keys):
    return "".join(PARTS[x] for x in keys)


def merge_bank():
    out, k = [], 0
    plus_sign = line(50, 32, 50, 68, GREY, 6) + line(32, 50, 68, 50, GREY, 6)
    eq_sign = line(28, 44, 72, 44, GREY, 5) + line(28, 58, 72, 58, GREY, 5)
    combos = [(("v",), ("o",)), (("h",), ("sq",)), (("d1", "d2"), ("o",)), (("v", "h"), ("sq",)),
              (("o",), ("tri",)), (("sq",), ("d1",)), (("tri",), ("h",)), (("o", "h"), ("v",)),
              (("sq", "o"), ("d2",)), (("v",), ("d1", "d2"))]
    for a, b in combos:
        merged = tuple(sorted(set(a) | set(b)))
        wrongs = [a, b, tuple(sorted(set(merged) | ({"tri"} if "tri" not in merged else {"o"})))]
        opts = [fig(_draw(merged))] + [fig(_draw(w)) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما ناتج دمج الشكلين؟", opts, ans,
                       [f"الشكل الأول يحوي: " + "، ".join(PNAMES[x] for x in a) + ".",
                        f"الشكل الثاني يحوي: " + "، ".join(PNAMES[x] for x in b) + ".",
                        "الدمج = وضع الشكلين فوق بعضهما ⇒ كل العناصر معًا بلا زيادة ولا نقصان.",
                        f"الناتج يحوي: " + "، ".join(PNAMES[x] for x in merged) + "."],
                       [fig(_draw(a)), fig(plus_sign), fig(_draw(b)), fig(eq_sign), QM],
                       tip="استبعد فورًا أي اختيار فيه عنصر غير موجود في الشكلين."))
        k += 1
    # حذف المشترك
    for a, b in [(("d1", "sq"), ("d2", "sq")), (("o", "v"), ("o", "h")), (("sq", "h"), ("tri", "h")),
                 (("o", "d1"), ("sq", "d1")), (("v", "tri"), ("v", "o")), (("h", "d2"), ("sq", "d2"))]:
        res = tuple(sorted(set(a) ^ set(b)))
        common = tuple(set(a) & set(b))
        wrongs = [tuple(sorted(set(a) | set(b))), a, b]
        opts = [fig(_draw(res))] + [fig(_draw(w)) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("القاعدة: يختفي كل عنصر مشترك بين الشكلين. ما الناتج؟", opts, ans,
                       [f"الشكل الأول: " + "، ".join(PNAMES[x] for x in a) + ".",
                        f"الشكل الثاني: " + "، ".join(PNAMES[x] for x in b) + ".",
                        f"العنصر المشترك: {PNAMES[common[0]]} ⇒ يُحذف من الناتج.",
                        f"يتبقى: " + "، ".join(PNAMES[x] for x in res) + "."],
                       [fig(_draw(a)), fig(plus_sign), fig(_draw(b)), fig(eq_sign), QM],
                       tip="المثال المعطى في رأس السؤال هو الذي يحدد: دمج أم حذف المشترك."))
        k += 1
    # القطعة الناقصة
    for whole, part in [(("o", "h", "tri"), ("o", "h")), (("sq", "d1", "d2"), ("sq", "d1")),
                        (("v", "h", "o"), ("v", "h")), (("tri", "v", "o"), ("tri", "v")),
                        (("sq", "o", "h"), ("sq", "o")), (("d1", "d2", "o"), ("d1", "d2"))]:
        need = tuple(sorted(set(whole) - set(part)))
        wrongs = [(x,) for x in whole if (x,) != need][:2] + [("sq",) if "sq" not in whole else ("tri",)]
        opts = [fig(_draw(need))] + [fig(_draw(w)) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("ما القطعة التي تُضاف للشكل الأول ليصير مثل الثاني؟", opts, ans,
                       [f"الشكل الأول: " + "، ".join(PNAMES[x] for x in part) + ".",
                        f"الشكل الثاني: " + "، ".join(PNAMES[x] for x in whole) + ".",
                        f"الفرق بينهما = {PNAMES[need[0]]} فقط.",
                        "هذا هو الطرح: الناتج ناقص المعطى."],
                       [fig(_draw(part)), fig(plus_sign), QM, fig(eq_sign), fig(_draw(whole))],
                       tip="قارن عنصرًا بعنصر ولا تضف شيئًا من عندك."))
        k += 1
    return out


# ===================================================== ١١ عدّ الأشكال
def count_bank():
    out, k = [], 0

    def grid(cols, rows, color=TEAL):
        inner = rect(14, 14, 72, 72, "#f0fdfa", color, 4)
        for c in range(1, cols):
            inner += line(14 + c * 72 / cols, 14, 14 + c * 72 / cols, 86, color, 3)
        for r in range(1, rows):
            inner += line(14, 14 + r * 72 / rows, 86, 14 + r * 72 / rows, color, 3)
        return inner

    def comb2(n):
        return n * (n - 1) // 2
    for cols, rows in ((2, 2), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 2), (5, 3)):
        rects = comb2(cols + 1) * comb2(rows + 1)
        squares = sum((cols - i) * (rows - i) for i in range(min(cols, rows)))
        out.append(gqf(f"كم مستطيلًا (بما فيها المربعات) في الشبكة {ar(cols)}×{ar(rows)}؟",
                       *rotate_options([fig(f'<text x="50" y="62" font-size="40" text-anchor="middle" '
                                            f'fill="{INK}" font-weight="800">{ar(v)}</text>')
                                        for v in (rects, rects - 3, rects + 4, cols * rows)], 0, k),
                       [f"عدد الخطوط الرأسية = {ar(cols + 1)} والأفقية = {ar(rows + 1)}.",
                        f"أي مستطيل يتحدّد باختيار خطين رأسيين وخطين أفقيين.",
                        f"عدد الطرق = C({ar(cols + 1)}،٢) × C({ar(rows + 1)}،٢) = {ar(comb2(cols + 1))} × {ar(comb2(rows + 1))}.",
                        f"المجموع = {ar(rects)} مستطيلًا."],
                       [bfig(grid(cols, rows))],
                       tip="احفظ القانون: C(ع+١،٢) × C(ص+١،٢)."))
        k += 1
        out.append(gqf(f"كم مربعًا (بكل الأحجام) في الشبكة {ar(cols)}×{ar(rows)}؟",
                       *rotate_options([fig(f'<text x="50" y="62" font-size="40" text-anchor="middle" '
                                            f'fill="{INK}" font-weight="800">{ar(v)}</text>')
                                        for v in (squares, squares + 2, squares - 2, cols * rows)], 0, k),
                       [f"مربعات ١×١ عددها {ar(cols * rows)}.",
                        "ثم مربعات ٢×٢ وهكذا حتى أكبر مربع ممكن.",
                        f"المجموع = " + " + ".join(ar((cols - i) * (rows - i)) for i in range(min(cols, rows))) +
                        f" = {ar(squares)}."],
                       [bfig(grid(cols, rows))],
                       tip="المربعات أقل من المستطيلات دائمًا؛ انتبه لصيغة السؤال."))
        k += 1

    # مثلثات داخل مثلث بخطوط المنتصف
    def tri_mid(levels):
        inner = '<polygon points="50,12 90,84 10,84" fill="#ede9fe" stroke="%s" stroke-width="3.5"/>' % PURPLE
        if levels >= 1:
            inner += line(30, 48, 70, 48, PURPLE, 3) + line(30, 48, 50, 84, PURPLE, 3) + line(70, 48, 50, 84, PURPLE, 3)
        if levels >= 2:
            inner += line(20, 66, 80, 66, PURPLE, 2.5) + line(40, 30, 30, 48, PURPLE, 0.1)
        return inner
    for levels, total in ((1, 5), (2, 13)):
        out.append(gqf("كم مثلثًا في الشكل؟",
                       *rotate_options([fig(f'<text x="50" y="62" font-size="40" text-anchor="middle" '
                                            f'fill="{INK}" font-weight="800">{ar(v)}</text>')
                                        for v in (total, total - 1, total + 1, total + 3)], 0, k),
                       ["عُدّ المثلثات الصغيرة أولًا (بما فيها المقلوبة).",
                        "ثم المثلثات المكوَّنة من اتحاد مثلثين أو أربعة.",
                        f"وأخيرًا المثلث الكبير الكلي ⇒ المجموع = {ar(total)}."],
                       [bfig(tri_mid(levels))],
                       tip="المثلثات المقلوبة هي الأكثر نسيانًا."))
        k += 1

    # مثلثات في مربع بقطريه / نصف قطريه
    sq_d = rect(16, 16, 68, 68, "#fff7ed", AMBER, 4) + line(16, 16, 84, 84, AMBER, 3) + line(84, 16, 16, 84, AMBER, 3)
    sq_1 = rect(16, 16, 68, 68, "#fff7ed", AMBER, 4) + line(16, 16, 84, 84, AMBER, 3)
    for shape, total, desc in ((sq_d, 8, "مربع بقطريه"), (sq_1, 2, "مربع بقطر واحد")):
        out.append(gqf(f"كم مثلثًا في الشكل ({desc})؟",
                       *rotate_options([fig(f'<text x="50" y="62" font-size="40" text-anchor="middle" '
                                            f'fill="{INK}" font-weight="800">{ar(v)}</text>')
                                        for v in (total, total + 2, max(total - 2, 1), total + 4)], 0, k),
                       ["ابدأ بالمثلثات الصغيرة التي لا تحوي خطوطًا بداخلها.",
                        "ثم ادمج كل مثلثين متجاورين وانظر: هل يكوّنان مثلثًا أكبر؟",
                        f"المجموع في هذا الشكل = {ar(total)} مثلثات."],
                       [bfig(shape)],
                       tip="رقّم المثلثات الصغيرة على الورقة ثم اجمع التوليفات."))
        k += 1
    return out


# ===================================================== ١٢ الشكل الشاذ
def odd_bank():
    out, k = [], 0
    # (أ) عدد الأضلاع فردي/زوجي
    for group, odd in (((4, 6, 8), 5), ((3, 5, 7), 6), ((4, 8, 6), 7), ((5, 7, 9), 4)):
        shapes = [polygon(n, 32, fill="#dbeafe", stroke=BLUE, sw=4) for n in group]
        oddsh = polygon(odd, 32, fill="#dbeafe", stroke=BLUE, sw=4)
        opts, ans = rotate_options([fig(oddsh)] + [fig(s) for s in shapes], 0, k)
        parity = "زوجي" if group[0] % 2 == 0 else "فردي"
        out.append(gqf("أي شكل مختلف عن البقية؟", opts, ans,
                       [f"عُدّ أضلاع كل شكل: " + "، ".join(ar(n) for n in sorted(group + (odd,))) + ".",
                        f"ثلاثة أشكال عدد أضلاعها {parity}.",
                        f"الشكل ذو {ar(odd)} أضلاع وحده يخالف ⇐ هو الشاذ."],
                       None,
                       tip="ابدأ دائمًا بعدّ الأضلاع قبل النظر إلى اللون أو الحجم."))
        k += 1
    # (ب) عدد النقاط
    for base, odd in ((3, 4), (4, 5), (5, 3), (2, 3)):
        def shape_dots(c, color=GREEN):
            inner = circle(50, 50, 32, "#f0fdf4", color, 4)
            pos = [(50, 32), (34, 60), (66, 60), (50, 66), (34, 40), (66, 40)]
            return inner + "".join(dot(x, y, 6, color) for x, y in pos[:c])
        opts, ans = rotate_options([fig(shape_dots(odd))] + [fig(shape_dots(base)) for _ in range(3)], 0, k)
        # تمييز الثلاثة المتشابهة بترتيب مختلف للنقاط حتى لا تتطابق الصور
        variants = []
        for i in range(3):
            inner = circle(50, 50, 32, "#f0fdf4", GREEN, 4)
            pos = [[(50, 32), (34, 60), (66, 60)], [(34, 40), (66, 40), (50, 66)],
                   [(50, 34), (36, 62), (64, 62)], [(40, 36), (62, 44), (50, 66)]][i % 4][:base]
            while len(pos) < base:
                pos.append((50, 50))
            variants.append(fig(inner + "".join(dot(x, y, 6, GREEN) for x, y in pos)))
        opts, ans = rotate_options([fig(shape_dots(odd))] + variants, 0, k)
        out.append(gqf("أي شكل لا ينتمي للمجموعة؟", opts, ans,
                       ["كل الأشكال دوائر متطابقة ⇒ الفرق ليس في الشكل.",
                        f"عُدّ النقاط: ثلاثة أشكال بها {ar(base)} نقاط.",
                        f"الشكل الذي به {ar(odd)} نقاط هو الشاذ."],
                       None,
                       tip="غيّر زاوية نظرك: الشكل، العدد، التظليل، الاتجاه."))
        k += 1
    # (ج) الشاذ = صورة مرآة وسط تدويرات
    for motif in _MOTIFS[:4]:
        opts, ans = rotate_options([fig(transform(motif, mirror="h")), fig(motif),
                                    fig(transform(motif, rotate=90)), fig(transform(motif, rotate=180))], 0, k)
        out.append(gqf("ثلاثة أشكال تدويرات لشكل واحد. أيها الشاذ؟", opts, ans,
                       ["جرّب تدوير كل شكل ذهنيًا حتى يطابق الأول.",
                        "ثلاثة منها تتطابق بالتدوير فقط.",
                        "الشكل الذي لا يطابق إلا بعد قلبه (مرآة) هو الشاذ."],
                       None,
                       tip="اقرأ ترتيب العلامات مع عقارب الساعة: ينقلب في المرآة فقط."))
        k += 1
    # (د) التظليل
    for parts, shaded_ok, shaded_odd in ((4, [(0, 1), (1, 2), (2, 3)], (0, 2)),
                                         (6, [(0, 1), (2, 3), (4, 5)], (0, 3)),
                                         (8, [(0, 1), (3, 4), (5, 6)], (1, 5))):
        opts = [fig(pie(parts, shaded_odd, fill=TEAL))] + [fig(pie(parts, s, fill=TEAL)) for s in shaded_ok]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أي دائرة مختلفة في التظليل؟", opts, ans,
                       ["في ثلاث دوائر يكون الجزآن المظللان متجاورين (يشكلان قطعة واحدة متصلة).",
                        "في دائرة واحدة الجزآن متباعدان (غير متصلين).",
                        "إذن الشاذة هي الدائرة ذات التظليل غير المتصل."],
                       None,
                       tip="انظر إلى «شكل المنطقة المظللة» لا إلى موضعها."))
        k += 1
    # (هـ) شكل مختلف في النوع
    for group, odd_name in ((["circle", "square", "diamond"], "tri"), (["tri", "star", "diamond"], "circle"),
                            (["square", "diamond", "tri"], "circle"), (["circle", "star", "tri"], "square")):
        opts = [fig(SYM[odd_name])] + [fig(SYM[n]) for n in group]
        opts, ans = rotate_options(opts, 0, k)
        has_curve = odd_name == "circle"
        reason = ("ثلاثة أشكال مضلّعة بخطوط مستقيمة، والدائرة وحدها منحنية." if has_curve
                  else f"الأشكال الثلاثة الأخرى تشترك في صفة لا تنطبق على {NAMES[odd_name]}.")
        out.append(gqf("أي شكل لا ينتمي للمجموعة؟", opts, ans,
                       ["ابحث عن صفة مشتركة بين ثلاثة أشكال.",
                        reason,
                        f"إذن الشاذ هو {NAMES[odd_name]}."],
                       None,
                       tip="الصفات الشائعة: عدد الأضلاع، الاستقامة أو الانحناء، التماثل، التظليل."))
        k += 1
    return out


# ===================================================== ١٨ تعبيرات الوجه
def faces_bank():
    out, k = [], 0
    specs = [("smile", "dots", None, "الفرح"), ("frown", "dots", None, "الحزن"),
             ("frown", "dots", "angry", "الغضب"), ("open", "wide", None, "الدهشة"),
             ("flat", "dots", None, "الحياد"), ("smile", "closed", None, "الرضا")]
    # الشاذ
    for i, (m, e, b, name) in enumerate(specs):
        same = [s for s in specs if s[3] != name][:3]
        opts = [fig(face(m, e, brow=b))] + [fig(face(s[0], s[1], brow=s[2])) for s in same]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أي وجه شاذ عن المجموعة؟", opts, ans,
                       ["ابدأ بالفم: هو العلامة الأقوى على الشعور.",
                        "ثم الحاجبان: الميل نحو الأنف = غضب، والميل لأعلى = حزن أو خوف.",
                        f"الوجه المعبّر عن {name} يختلف عن بقية المجموعة ⇐ هو الشاذ."],
                       None,
                       tip="العيون وحدها لا تكفي؛ الفم والحاجب يحسمان الشعور."))
        k += 1
    # إكمال التدرّج
    ladders = [(("smile", "dots", None), ("flat", "dots", None), ("frown", "dots", None), "من الفرح إلى الحياد ثم الحزن"),
               (("frown", "dots", None), ("flat", "dots", None), ("smile", "dots", None), "من الحزن إلى الحياد ثم الفرح"),
               (("smile", "closed", None), ("smile", "dots", None), ("open", "wide", None), "ازدياد انفعال الوجه تدريجيًا")]
    for a, b, c, desc in ladders:
        wrongs = [("frown", "dots", "angry"), ("flat", "dots", None), ("smile", "closed", None)]
        wrongs = [w for w in wrongs if w != c][:3]
        opts = [fig(face(c[0], c[1], brow=c[2]))] + [fig(face(w[0], w[1], brow=w[2])) for w in wrongs]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf("أكمل نمط الوجوه.", opts, ans,
                       [f"رتّب المشاعر على سُلّم: {desc}.",
                        "لاحظ أن التغيير يسير في اتجاه واحد بخطوة ثابتة.",
                        "الوجه التالي يكمل هذا التدرّج."],
                       [fig(face(a[0], a[1], brow=a[2])), fig(face(b[0], b[1], brow=b[2])), QM],
                       tip="حدّد اتجاه التدرّج أولًا (صعودًا أم هبوطًا) قبل الاختيار."))
        k += 1
    # مطابقة الشعور
    for m, e, b, name in specs:
        others = [s for s in specs if s[3] != name][:3]
        opts = [fig(face(m, e, brow=b))] + [fig(face(s[0], s[1], brow=s[2])) for s in others]
        opts, ans = rotate_options(opts, 0, k)
        out.append(gqf(f"أي وجه يعبّر عن {name}؟", opts, ans,
                       [f"{name} له علامة واضحة في الفم والحاجبين.",
                        "قارن كل وجه بالوصف واستبعد ما لا يطابق.",
                        f"الوجه المطابق لـ{name} هو الإجابة."],
                       None,
                       tip="احفظ العلامات: ابتسامة = فرح، فم مقلوب = حزن، حاجب مائل للداخل = غضب، فم مفتوح وعين واسعة = دهشة."))
        k += 1
    return out


# ===================================================== ٢ الشكل المكمِّل
def complete_bank():
    out, k = [], 0

    # (أ) دائرة ينقصها قطاع
    for parts in (4, 6, 8, 3):
        ang = 360 / parts
        missing = f'<circle cx="50" cy="50" r="32" fill="#dbeafe" stroke="{BLUE}" stroke-width="4"/>'
        from svgkit import sector
        missing += sector(0, parts, 32, fill=WHITE)
        missing += sector(0, parts, 32, fill="none", stroke=RED, sw=2.5)
        correct = sector(0, parts, 30, fill="#bfdbfe", stroke=BLUE, sw=3)
        wrongs = [sector(0, max(parts - 1, 2), 30, fill="#bfdbfe", stroke=BLUE, sw=3),
                  sector(0, parts + 2, 30, fill="#bfdbfe", stroke=BLUE, sw=3),
                  sector(0, parts, 22, fill="#bfdbfe", stroke=BLUE, sw=3)]
        opts, ans = rotate_options([fig(correct)] + [fig(w) for w in wrongs], 0, k)
        out.append(gqf("أي قطعة تكمل الدائرة تمامًا؟", opts, ans,
                       [f"الجزء الناقص هو {ar(1)}/{ar(parts)} من الدائرة (زاوية {ar(int(ang))}°).",
                        "القطعة الصحيحة يجب أن تطابق الزاوية ونصف القطر معًا.",
                        "استبعد القطع الأصغر أو الأكبر زاويةً، والقطعة القصيرة نصف القطر."],
                       [bfig(missing), QM],
                       tip="قِس الزاوية بالمقارنة مع ربع الدائرة (٩٠°) أو نصفها (١٨٠°)."))
        k += 1

    # (ب) مربع مخطّط ينقصه جزء
    import math

    def hatched(x, y, w, h, angle, color=GREEN, step=11, bg="#f0fdf4", sw=3):
        """مستطيل بخطوط مائلة محسوبة هندسيًا بحيث لا تخرج عن حدوده إطلاقًا."""
        th = math.radians(angle)
        dx, dy = math.cos(th), math.sin(th)
        nx, ny = -dy, dx
        cx, cy = x + w / 2, y + h / 2
        span = (abs(w * nx) + abs(h * ny)) / 2 + step
        segs = ""
        t = -span
        while t <= span:
            px, py = cx + t * nx, cy + t * ny
            # قصّ الخط (px,py)+s(dx,dy) على المستطيل بخوارزمية Liang–Barsky
            t0, t1 = -1e9, 1e9
            ok = True
            for pp, qq in ((-dx, px - x), (dx, x + w - px), (-dy, py - y), (dy, y + h - py)):
                if abs(pp) < 1e-9:
                    if qq < 0:
                        ok = False
                        break
                else:
                    r = qq / pp
                    if pp < 0:
                        t0 = max(t0, r)
                    else:
                        t1 = min(t1, r)
            if ok and t0 < t1:
                segs += line(px + t0 * dx, py + t0 * dy, px + t1 * dx, py + t1 * dy, color, sw, cap="butt")
            t += step
        return rect(x, y, w, h, bg, color, 3.5) + segs + rect(x, y, w, h, "none", color, 3.5)

    for ang, name in ((45, "مائلة من أعلى اليسار إلى أسفل اليمين"),
                      (135, "مائلة من أعلى اليمين إلى أسفل اليسار"),
                      (90, "رأسية"), (0, "أفقية")):
        stem_fig = hatched(16, 16, 68, 68, ang) + rect(44, 38, 26, 24, WHITE, RED, 2.5)
        correct = hatched(26, 34, 48, 32, ang)
        wrongs = [hatched(26, 34, 48, 32, (ang + 45) % 180),
                  hatched(26, 34, 48, 32, (ang + 90) % 180),
                  hatched(26, 34, 48, 32, (ang + 135) % 180)]
        opts, ans = rotate_options([fig(correct)] + [fig(w) for w in wrongs], 0, k)
        out.append(gqf("أي قطعة تكمل نمط الخطوط؟", opts, ans,
                       [f"خطوط الشكل {name}.",
                        "القطعة الصحيحة تحافظ على زاوية الميل نفسها وعلى التباعد نفسه.",
                        "أي قطعة بزاوية مختلفة ستكسر استمرار الخطوط عند التركيب."],
                       [bfig(stem_fig), QM],
                       tip="ضع إصبعك على خط واحد وتتبّعه عبر الفجوة؛ يجب أن يستمر بنفس الميل."))
        k += 1

    # (ج) شبكة نقاط ينقصها ربع
    for n, color in ((2, PURPLE), (3, TEAL), (4, PINK)):
        def dotgrid(cols, rows, x=16, y=16, s=68, color=PURPLE):
            inner = rect(x, y, s, s, "#faf5ff", color, 3.5)
            for r in range(rows):
                for c in range(cols):
                    inner += dot(x + s * (c + 0.5) / cols, y + s * (r + 0.5) / rows, 5, color)
            return inner
        stem_fig = dotgrid(n, n, color=color) + rect(52, 52, 32, 32, WHITE, RED, 2.5)
        cnt = (n // 2) ** 2 if n > 1 else 1
        cnt = max(cnt, 1)

        def patch(c, color=color):
            inner = rect(34, 34, 32, 32, "#faf5ff", color, 3)
            pos = [(42, 42), (58, 42), (42, 58), (58, 58), (50, 50)]
            return inner + "".join(dot(x, y, 4.5, color) for x, y in pos[:c])
        opts, ans = rotate_options([fig(patch(cnt))] + [fig(patch(v)) for v in (cnt + 1, max(cnt - 1, 0), cnt + 2)], 0, k)
        out.append(gqf("أي قطعة تكمل الشبكة؟", opts, ans,
                       ["النقاط موزّعة بانتظام: نفس العدد في كل صف وكل عمود.",
                        f"الجزء المقطوع يغطي مساحة تحوي {ar(cnt)} نقطة بنفس التوزيع.",
                        "استبعد القطع التي تزيد أو تنقص نقطة."],
                       [bfig(stem_fig), QM],
                       tip="عُدّ النقاط في الصفوف الكاملة ثم استنتج عدد النقاط الناقصة."))
        k += 1

    # (د) زاوية مقطوعة من مربع
    corners = {"tr": ("العليا اليمنى", "80,20 80,46 54,20", "24,24 76,24 76,76"),
               "tl": ("العليا اليسرى", "20,20 46,20 20,46", "24,24 76,24 24,76"),
               "br": ("السفلى اليمنى", "80,80 80,54 54,80", "76,24 76,76 24,76"),
               "bl": ("السفلى اليسرى", "20,80 20,54 46,80", "24,24 24,76 76,76")}
    keys = list(corners)
    for ci, key in enumerate(keys):
        name, cutpts, piecepts = corners[key]
        shape = rect(20, 20, 60, 60, "#fef3c7", AMBER, 4)
        cut = f'<polygon points="{cutpts}" fill="{WHITE}" stroke="{RED}" stroke-width="2.5"/>'
        correct = f'<polygon points="{piecepts}" fill="#fef3c7" stroke="{AMBER}" stroke-width="3"/>'
        wrongs = []
        for other in keys:
            if other == key:
                continue
            wrongs.append(f'<polygon points="{corners[other][2]}" fill="#fef3c7" '
                          f'stroke="{AMBER}" stroke-width="3"/>')
        opts, ans = rotate_options([fig(correct)] + [fig(w) for w in wrongs[:3]], 0, k)
        out.append(gqf("أي قطعة تُعيد المربع كاملًا؟", opts, ans,
                       [f"الجزء المقطوع مثلث قائم الزاوية في الزاوية {name} من المربع.",
                        "القطعة الصحيحة مثلث قائم الزاوية بنفس اتجاه الزاوية المقطوعة.",
                        "كل الاختيارات مثلثات قائمة، لكن ثلاثة منها باتجاه زاوية مختلفة ⇐ لن تملأ الفجوة."],
                       [bfig(shape + cut), QM],
                       tip="حدّد موضع الزاوية القائمة في الفجوة ثم ابحث عن المثلث المطابق لها."))
        k += 1
    return out


# ===================================================== ٩ تركيب الأشكال X و Y
_EDGE_DEG = {"right": 0, "bottom": 90, "left": 180, "top": 270}


def _attached(kind):
    """القطعة مرسومة ملتصقة بالحافة اليمنى للمربع (قبل التدوير)."""
    if kind == "tri":
        return ('<polygon points="70,30 70,70 92,50" fill="#fecaca" stroke="%s" '
                'stroke-width="3" stroke-linejoin="round"/>' % INK)
    if kind == "semi":
        return '<path d="M 70 30 A 20 20 0 0 1 70 70 Z" fill="#bbf7d0" stroke="%s" stroke-width="3"/>' % INK
    return rect(70, 38, 18, 24, "#fde68a", INK, 3)


def _asm(edge, kind):
    """مربع مع قطعة ملتصقة بحافة محدّدة."""
    base = rect(30, 30, 40, 40, "#bfdbfe", INK, 3)
    return base + transform(_attached(kind), rotate=_EDGE_DEG[edge])


def _asm2(e1, kind1, e2, kind2):
    """مربع مع قطعتين على حافتين."""
    base = rect(30, 30, 40, 40, "#bfdbfe", INK, 3)
    return (base + transform(_attached(kind1), rotate=_EDGE_DEG[e1])
            + transform(_attached(kind2), rotate=_EDGE_DEG[e2]))


def _piece(kind, label):
    if kind == "tri":
        body = '<polygon points="34,26 34,74 76,50" fill="#fecaca" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % INK
        mark = line(34, 26, 34, 74, RED, 4)
        lx, ly = 24, 52
    elif kind == "semi":
        body = '<path d="M 36 26 A 24 24 0 0 1 36 74 Z" fill="#bbf7d0" stroke="%s" stroke-width="3"/>' % INK
        mark = line(36, 26, 36, 74, RED, 4)
        lx, ly = 26, 52
    else:
        body = rect(36, 32, 30, 36, "#fde68a", INK, 3)
        mark = line(36, 32, 36, 68, RED, 4)
        lx, ly = 26, 52
    from svgkit import text as _t
    return body + mark + _t(label, lx, ly, 18, RED, "800")


def xyz_bank():
    from svgkit import text as _t
    out, k = [], 0
    edges = ["right", "top", "left", "bottom"]
    enames = {"right": "الحافة اليمنى", "top": "الحافة العليا", "left": "الحافة اليسرى",
              "bottom": "الحافة السفلى"}
    kinds = {"tri": "المثلث", "semi": "نصف الدائرة", "sq": "المستطيل الصغير"}
    for kind, kname in kinds.items():
        for edge in edges:
            marks = {"right": (line(70, 30, 70, 70, RED, 4), 80, 52),
                     "top": (line(30, 30, 70, 30, RED, 4), 50, 22),
                     "left": (line(30, 30, 30, 70, RED, 4), 20, 52),
                     "bottom": (line(30, 70, 70, 70, RED, 4), 50, 84)}[edge]
            sq = rect(30, 30, 40, 40, "#bfdbfe", INK, 3) + marks[0] + _t("X", marks[1], marks[2], 18, RED, "800")
            others = [e for e in edges if e != edge]
            opts = [fig(_asm(edge, kind))] + [fig(_asm(e, kind)) for e in others]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("ما شكل القطعتين بعد لصقهما عند الحرف X؟", opts, ans,
                           [f"الحرف X مكتوب على {enames[edge]} من المربع.",
                            f"وعلى الحافة المستقيمة من {kname} (المعلَّمة بالأحمر).",
                            f"نلصق الحافتين معًا ⇒ يلتصق {kname} على {enames[edge]} للمربع.",
                            "الاختيارات الأخرى تضع القطعة على حافة خاطئة."],
                           [fig(sq), fig(_piece(kind, "X")), QM],
                           tip="الحرف المكرر على قطعتين هو نقطة اللصق؛ ابدأ دائمًا بتحديد موضعه."))
            k += 1
    # قطعتان على مربع واحد
    for kind1, kind2 in (("tri", "semi"), ("semi", "sq"), ("sq", "tri")):
        for e1, e2 in (("right", "top"), ("left", "bottom"), ("top", "left")):
            m1 = {"right": (line(70, 30, 70, 70, RED, 4), 80, 52), "top": (line(30, 30, 70, 30, RED, 4), 50, 22),
                  "left": (line(30, 30, 30, 70, RED, 4), 20, 52), "bottom": (line(30, 70, 70, 70, RED, 4), 50, 84)}[e1]
            m2 = {"right": (line(70, 30, 70, 70, RED, 4), 80, 52), "top": (line(30, 30, 70, 30, RED, 4), 50, 22),
                  "left": (line(30, 30, 30, 70, RED, 4), 20, 52), "bottom": (line(30, 70, 70, 70, RED, 4), 50, 84)}[e2]
            sq = (rect(30, 30, 40, 40, "#bfdbfe", INK, 3) + m1[0] + _t("X", m1[1], m1[2], 18, RED, "800")
                  + m2[0] + _t("Y", m2[1], m2[2], 18, RED, "800"))

            def both(a, b):
                return _asm2(a, kind1, b, kind2)
            wrongs = [(e2, e1), (e1, e1), (e2, e2)]
            opts = [fig(both(e1, e2))] + [fig(both(a, b)) for a, b in wrongs]
            opts, ans = rotate_options(opts, 0, k)
            out.append(gqf("أي شكل ينتج عن لصق القطع الثلاث (X مع X و Y مع Y)؟", opts, ans,
                           [f"ابدأ بالقطعة التي تحمل حرفين: المربع، فعليه X على {enames[e1]} وY على {enames[e2]}.",
                            f"{kinds[kind1]} يحمل X ⇒ يلتصق على {enames[e1]}.",
                            f"{kinds[kind2]} يحمل Y ⇒ يلتصق على {enames[e2]}.",
                            "أي اختيار يبدّل مكان القطعتين يكون خاطئًا."],
                           [fig(sq), fig(_piece(kind1, "X")), fig(_piece(kind2, "Y")), QM],
                           tip="ابدأ دائمًا بالقطعة التي تحمل حرفين؛ هي التي تحدد الباقي."))
            k += 1
    return out
