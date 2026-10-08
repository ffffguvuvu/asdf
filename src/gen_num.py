# -*- coding: utf-8 -*-
"""بنك تدريب مولَّد: المتسلسلات العددية (محور ١٣) ومتتاليات الحروف (محور ١٤)."""

from content_c import chips, lchips
from genlib import gq, ar, fmt, ar_letter, en_letter, AR_ALPHA

BLUE, PURPLE = "#2563eb", "#7c3aed"


def _sq(vals, ans, steps, k, tip=None, title="أوجد الرقم التالي في المتسلسلة."):
    pool = [ans + 1, ans - 1, ans + 2, ans * 2, ans - 2, ans + 10]
    pool = [p for p in pool if p != ans and (not isinstance(p, int) or p > 0)]
    return gq(title, ans, pool, steps, [chips(vals, BLUE)], k=k, tip=tip)


def number_bank():
    """أكثر من ٢٠٠ سؤال متسلسلات بقواعد مختلفة، كل سؤال بخطوات حلّه."""
    out = []
    k = 0

    # ١) حسابية تصاعدية
    for d in range(2, 10):
        for a in (1, 4, 7):
            v = [a + i * d for i in range(5)]
            out.append(_sq(v + [None], a + 5 * d,
                           [f"اطرح كل حدّ من الذي يليه: {ar(v[1])} − {ar(v[0])} = {ar(d)}، و{ar(v[2])} − {ar(v[1])} = {ar(d)}.",
                            f"الفرق ثابت = {ar(d)} ⇐ متتالية حسابية.",
                            f"الحد التالي = {ar(v[-1])} + {ar(d)} = {ar(a + 5 * d)}."], k,
                           "ثبات الفرق هو أول ما تفحصه في أي متسلسلة."))
            k += 1

    # ٢) حسابية تنازلية
    for d in (3, 4, 5, 6, 7, 8):
        for a in (60, 95):
            v = [a - i * d for i in range(5)]
            out.append(_sq(v + [None], a - 5 * d,
                           [f"المتسلسلة تنازلية: {ar(v[0])} − {ar(d)} = {ar(v[1])}، و{ar(v[1])} − {ar(d)} = {ar(v[2])}.",
                            f"الفرق ثابت = −{ar(d)}.",
                            f"الحد التالي = {ar(v[-1])} − {ar(d)} = {ar(a - 5 * d)}."], k,
                           "الفرق السالب يعني طرحًا ثابتًا لا قسمة."))
            k += 1

    # ٣) هندسية (ضرب)
    for r in (2, 3, 4, 5):
        for a in (1, 2, 3, 6):
            v = [a * r ** i for i in range(4)]
            if v[-1] > 20000:
                continue
            out.append(_sq(v + [None], a * r ** 4,
                           [f"اقسم كل حدّ على سابقه: {ar(v[1])} ÷ {ar(v[0])} = {ar(r)}، و{ar(v[2])} ÷ {ar(v[1])} = {ar(r)}.",
                            f"النسبة ثابتة = {ar(r)} ⇐ متتالية هندسية.",
                            f"الحد التالي = {ar(v[-1])} × {ar(r)} = {ar(a * r ** 4)}."], k,
                           "لو قفزت الأرقام بسرعة فجرّب القسمة لا الطرح."))
            k += 1

    # ٤) هندسية (قسمة)
    for r in (2, 3):
        for a in (1458, 2430, 4096, 6561):
            if a % r ** 4:
                continue
            v = [a // r ** i for i in range(4)]
            out.append(_sq(v + [None], a // r ** 4,
                           [f"كل حدّ يساوي سابقه ÷ {ar(r)}: {ar(v[0])} ÷ {ar(r)} = {ar(v[1])}.",
                            f"النمط نازل بالقسمة على {ar(r)}.",
                            f"الحد التالي = {ar(v[-1])} ÷ {ar(r)} = {ar(a // r ** 4)}."], k,
                           "القسمة المتكرّرة هي الوجه الآخر للمتتالية الهندسية."))
            k += 1

    # ٥) فيبوناتشي ومتغيّراتها
    for a, b in ((1, 1), (2, 3), (3, 5), (1, 4), (2, 5), (4, 7)):
        v = [a, b]
        while len(v) < 6:
            v.append(v[-1] + v[-2])
        out.append(_sq(v + [None], v[-1] + v[-2],
                       [f"جرّب جمع كل حدّين متتاليين: {ar(v[0])} + {ar(v[1])} = {ar(v[2])}.",
                        f"وأيضًا {ar(v[1])} + {ar(v[2])} = {ar(v[3])} ⇐ القاعدة: كل حدّ = مجموع الحدّين قبله.",
                        f"الحد التالي = {ar(v[-2])} + {ar(v[-1])} = {ar(v[-1] + v[-2])}."], k,
                       "فيبوناتشي: لا فرق ثابت ولا نسبة ثابتة، بل جمع الحدّين السابقين."))
        k += 1
    for a, b, c in ((1, 2, 1), (2, 3, 2), (1, 3, 3)):
        v = [a, b]
        while len(v) < 6:
            v.append(v[-1] + v[-2] + c)
        out.append(_sq(v + [None], v[-1] + v[-2] + c,
                       [f"المجموع وحده لا يكفي: {ar(v[0])} + {ar(v[1])} = {ar(v[0] + v[1])} بينما الحد الثالث {ar(v[2])}.",
                        f"الفرق دائمًا {ar(c)} ⇐ القاعدة: مجموع الحدّين السابقين + {ar(c)}.",
                        f"الحد التالي = {ar(v[-2])} + {ar(v[-1])} + {ar(c)} = {ar(v[-1] + v[-2] + c)}."], k,
                       "لو كان المجموع قريبًا من الحد التالي فابحث عن ثابت صغير مضاف."))
        k += 1

    # ٦) فرق متزايد
    for d0 in (1, 2, 3):
        for step in (1, 2, 3):
            for a in (2, 5):
                v, d = [a], d0
                for _ in range(4):
                    v.append(v[-1] + d)
                    d += step
                out.append(_sq(v + [None], v[-1] + d,
                               [f"الفروق: " + "، ".join(ar(v[i + 1] - v[i]) for i in range(4)) + ".",
                                f"الفروق نفسها تزيد بمقدار {ar(step)} في كل مرة.",
                                f"الفرق التالي = {ar(d)} ⇐ الحد التالي = {ar(v[-1])} + {ar(d)} = {ar(v[-1] + d)}."], k,
                               "اكتب صفًّا ثانيًا للفروق؛ إن انتظم فالمسألة محلولة."))
                k += 1

    # ٧) مربعات ومشتقاتها
    for off, name in ((0, "مربعات كاملة"), (1, "مربع + ١"), (-1, "مربع − ١")):
        for s in (1, 2, 3, 4):
            v = [i * i + off for i in range(s, s + 5)]
            nxt = (s + 5) ** 2 + off
            out.append(_sq(v + [None], nxt,
                           [f"الأرقام قريبة من المربعات: " + "، ".join(f"{ar(i)}²" for i in range(s, s + 5)) + ".",
                            f"القاعدة: {name} ⇐ {ar(s)}² {'+' if off > 0 else ('−' if off < 0 else '')} {ar(abs(off)) if off else ''} = {ar(v[0])}.".replace("  ", " "),
                            f"الحد التالي = {ar(s + 5)}² {'+ ' + ar(off) if off > 0 else ('− ' + ar(-off) if off < 0 else '')} = {ar(nxt)}.".replace("  ", " ")], k,
                           "احفظ المربعات حتى ٢٠² = ٤٠٠؛ تكشف نصف أسئلة المتسلسلات."))
            k += 1

    # ٨) مكعبات
    for off in (0, 1):
        for s in (1, 2, 3):
            v = [i ** 3 + off for i in range(s, s + 4)]
            nxt = (s + 4) ** 3 + off
            out.append(_sq(v + [None], nxt,
                           ["الأرقام تكبر بسرعة كبيرة ⇐ فكّر في المكعبات.",
                            f"{ar(s)}³ = {ar(s ** 3)}، {ar(s + 1)}³ = {ar((s + 1) ** 3)}، {ar(s + 2)}³ = {ar((s + 2) ** 3)}" + (f" وكلها + {ar(off)}." if off else "."),
                            f"الحد التالي = {ar(s + 4)}³{' + ' + ar(off) if off else ''} = {ar(nxt)}."], k,
                           "المكعبات: ١، ٨، ٢٧، ٦٤، ١٢٥، ٢١٦، ٣٤٣، ٥١٢."))
            k += 1

    # ٩) الأعداد المثلثية
    for s in (1, 2, 3, 4, 5, 6):
        tri = [i * (i + 1) // 2 for i in range(s, s + 5)]
        nxt = (s + 5) * (s + 6) // 2
        out.append(_sq(tri + [None], nxt,
                       [f"الفروق: " + "، ".join(ar(tri[i + 1] - tri[i]) for i in range(4)) + " ⇐ تزيد واحدًا في كل خطوة.",
                        "هذه الأعداد المثلثية: ١، ٣، ٦، ١٠، ١٥، ٢١، ٢٨…",
                        f"الفرق التالي = {ar(s + 6)} ⇐ الحد التالي = {ar(tri[-1])} + {ar(s + 6)} = {ar(nxt)}."], k,
                       "الأعداد المثلثية = مجموع الأعداد من ١ إلى n."))
        k += 1

    # ١٠) الأعداد الأولية
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for s in range(0, 8, 2):
        v = primes[s:s + 5]
        nxt = primes[s + 5]
        out.append(_sq(v + [None], nxt,
                       ["لا يوجد فرق ثابت ولا نسبة ثابتة.",
                        "كل الأرقام لا تقبل القسمة إلا على نفسها وعلى الواحد ⇐ أعداد أولية.",
                        f"العدد الأولي التالي بعد {ar(v[-1])} هو {ar(nxt)}."], k,
                       "احفظ الأوّليات حتى ٥٠: ٢، ٣، ٥، ٧، ١١، ١٣، ١٧، ١٩، ٢٣، ٢٩، ٣١، ٣٧، ٤١، ٤٣، ٤٧."))
        k += 1

    # ١١) متتاليتان متداخلتان
    for a, da, b, db in ((3, 4, 20, -3), (5, 3, 40, 5), (2, 5, 30, -4), (7, 3, 22, 8),
                         (1, 6, 50, -7), (4, 7, 11, 9), (9, 2, 60, -6)):
        v = []
        for i in range(3):
            v += [a + i * da, b + i * db]
        nxt = a + 3 * da
        out.append(_sq(v + [None], nxt,
                       ["الأرقام تصعد وتهبط ⇐ غالبًا متتاليتان متداخلتان.",
                        f"الأماكن الفردية: " + "، ".join(ar(v[i]) for i in (0, 2, 4)) + f" ⇐ الفرق {ar(da)}.",
                        f"الأماكن الزوجية: " + "، ".join(ar(v[i]) for i in (1, 3, 5)) + f" ⇐ الفرق {ar(db)}.",
                        f"الدور الآن على المتتالية الأولى ⇐ {ar(v[4])} + {ar(da)} = {ar(nxt)}."], k,
                       "ارسم قوسين: واحد يربط الأماكن الفردية وآخر الزوجية."))
        k += 1
    for a, da, b, db in ((6, 5, 100, -10), (8, 4, 3, 6), (12, 6, 5, 4), (2, 9, 80, -8),
                         (15, 5, 7, 7), (3, 8, 44, -5), (10, 3, 25, 9)):
        v = []
        for i in range(3):
            v += [a + i * da, b + i * db]
        v = v[:-1]
        nxt = b + 2 * db
        out.append(_sq(v + [None], nxt,
                       ["افصل المتسلسلة إلى متتاليتين متداخلتين.",
                        f"الأماكن الفردية: " + "، ".join(ar(v[i]) for i in (0, 2, 4)) + f" ⇐ الفرق {ar(da)}.",
                        f"الأماكن الزوجية: {ar(v[1])}، {ar(v[3])} ⇐ الفرق {ar(db)}.",
                        f"المطلوب من المتتالية الثانية ⇐ {ar(v[3])} + {ar(db)} = {ar(nxt)}."], k,
                       "حدّد أي المتتاليتين عليها الدور قبل أن تحسب."))
        k += 1

    # ١٢) ×٢ ثم +١ (قاعدة مركّبة)
    for a in (1, 2, 3, 5):
        for m, c in ((2, 1), (2, 3), (3, 1), (3, 2)):
            v = [a]
            while len(v) < 5:
                v.append(v[-1] * m + c)
            nxt = v[-1] * m + c
            if nxt > 100000:
                continue
            out.append(_sq(v + [None], nxt,
                           [f"الفروق غير منتظمة ⇐ جرّب عمليتين معًا.",
                            f"{ar(v[0])} × {ar(m)} + {ar(c)} = {ar(v[1])}، و{ar(v[1])} × {ar(m)} + {ar(c)} = {ar(v[2])} ✔",
                            f"الحد التالي = {ar(v[-1])} × {ar(m)} + {ar(c)} = {ar(nxt)}."], k,
                           "القاعدة المركّبة (×ثم+) شائعة جدًا حين تكبر الأرقام بلا نسبة ثابتة."))
            k += 1

    # ١٣) عمليتان بالتناوب
    for down, up in ((2, 3), (3, 5), (4, 6), (5, 2)):
        for a in (20, 35):
            v = [a]
            for i in range(5):
                v.append(v[-1] - down if i % 2 == 0 else v[-1] + up)
            nxt = v[-1] - down
            out.append(_sq(v + [None], nxt,
                           [f"الأرقام تنزل ثم تصعد بالتناوب.",
                            f"الخطوات: −{ar(down)}، +{ar(up)}، −{ar(down)}، +{ar(up)} …",
                            f"الدور الآن على الطرح ⇐ {ar(v[-1])} − {ar(down)} = {ar(nxt)}."], k,
                           "تذبذب الأرقام لأعلى وأسفل = عمليتان متبادلتان."))
            k += 1

    # ١٤) الكسور العشرية (نصّف القيمة)
    for a in (400, 320, 200, 96, 48, 24):
        v = [a / 2 ** i for i in range(5)]
        nxt = a / 2 ** 5
        out.append(_sq([fmt(x) if False else x for x in v] + [None], nxt,
                       [f"كل حدّ نصف الذي قبله: {fmt(v[0])} ÷ ٢ = {fmt(v[1])}.",
                        "النمط مستمر حتى لو ظهر كسر عشري.",
                        f"الحد التالي = {fmt(v[-1])} ÷ ٢ = {fmt(nxt)}."], k,
                       "لا تتوقف لأن الناتج صار كسرًا؛ القاعدة لا تتغير."))
        k += 1

    # ١٥) ×٣ ثم −١ وما شابه
    for m, c in ((3, -1), (2, -2), (4, -3), (3, -4)):
        for a in (2, 4):
            v = [a]
            while len(v) < 5:
                v.append(v[-1] * m + c)
            nxt = v[-1] * m + c
            if nxt > 200000 or min(v) < 0:
                continue
            out.append(_sq(v + [None], nxt,
                           [f"جرّب الضرب أولًا: {ar(v[0])} × {ar(m)} = {ar(v[0] * m)} والحد التالي {ar(v[1])}.",
                            f"الفرق {ar(-c)} في كل مرة ⇐ القاعدة: × {ar(m)} − {ar(-c)}.",
                            f"الحد التالي = {ar(v[-1])} × {ar(m)} − {ar(-c)} = {ar(nxt)}."], k,
                           "بعد الضرب افحص الفرق الثابت؛ غالبًا تكون القاعدة مركّبة."))
            k += 1

    # ١٦) الرقم الناقص في المنتصف
    for d in (4, 6, 7, 9):
        for a in (3, 8):
            v = [a + i * d for i in range(6)]
            miss = 3
            shown = v[:miss] + [None] + v[miss + 1:]
            out.append(gq("أوجد الرقم الناقص في المنتصف.", v[miss],
                          [v[miss] + 1, v[miss] - 1, v[miss] + d, v[miss] - d],
                          [f"الفرق بين الحدود الظاهرة ثابت: {ar(v[1])} − {ar(v[0])} = {ar(d)}.",
                           f"الناقص = الحد الذي قبله + {ar(d)} = {ar(v[miss - 1])} + {ar(d)} = {ar(v[miss])}.",
                           f"تحقّق: {ar(v[miss])} + {ar(d)} = {ar(v[miss + 1])} ✔"],
                          [chips(shown, BLUE)], k=k,
                          tip="تحقّق من الحل بالاتجاهين: من اليمين ومن اليسار."))
            k += 1
    for r in (2, 3):
        for a in (2, 5):
            v = [a * r ** i for i in range(5)]
            shown = v[:2] + [None] + v[3:]
            out.append(gq("أوجد الرقم الناقص.", v[2],
                          [v[2] + r, v[2] - r, v[2] * r, v[2] + 1],
                          [f"النسبة بين الحدود ثابتة: {ar(v[1])} ÷ {ar(v[0])} = {ar(r)}.",
                           f"الناقص = {ar(v[1])} × {ar(r)} = {ar(v[2])}.",
                           f"تحقّق: {ar(v[2])} × {ar(r)} = {ar(v[3])} ✔"],
                          [chips(shown, BLUE)], k=k,
                          tip="في المتتالية الهندسية الحد الأوسط = الجذر التربيعي لحاصل ضرب جاريه."))
            k += 1

    # ١٧) الفروق مربعات
    for a in (1, 3, 5):
        v = [a]
        for i in range(1, 5):
            v.append(v[-1] + i * i)
        nxt = v[-1] + 25
        out.append(_sq(v + [None], nxt,
                       [f"الفروق: " + "، ".join(ar(v[i + 1] - v[i]) for i in range(4)) + ".",
                        "الفروق نفسها مربعات: ١، ٤، ٩، ١٦ ⇐ التالي ٢٥.",
                        f"الحد التالي = {ar(v[-1])} + ٢٥ = {ar(nxt)}."], k,
                       "لو كانت الفروق غريبة فافحص هل هي مربعات أو مكعبات."))
        k += 1

    # ١٨) ضرب بمعامل متزايد
    for a in (1, 2, 3):
        v = [a]
        for m in range(2, 6):
            v.append(v[-1] * m)
        nxt = v[-1] * 6
        out.append(_sq(v[:5] + [None], nxt,
                       [f"{ar(v[0])} × ٢ = {ar(v[1])}، و{ar(v[1])} × ٣ = {ar(v[2])}، و{ar(v[2])} × ٤ = {ar(v[3])}.",
                        "معامل الضرب نفسه يزيد واحدًا في كل خطوة.",
                        f"الحد التالي = {ar(v[4])} × ٦ = {ar(nxt)}."], k,
                       "راقب «المعامل المتغيّر»: ×٢ ثم ×٣ ثم ×٤…"))
        k += 1

    # ١٩) n² + n  و n(n+2)
    for kind in ("n2+n", "n(n+2)"):
        for s in (1, 2, 3):
            if kind == "n2+n":
                v = [i * i + i for i in range(s, s + 5)]
                nxt = (s + 5) ** 2 + (s + 5)
                rule = "n² + n"
            else:
                v = [i * (i + 2) for i in range(s, s + 5)]
                nxt = (s + 5) * (s + 7)
                rule = "n × (n + ٢)"
            out.append(_sq(v + [None], nxt,
                           [f"جرّب ربط كل حدّ برقم ترتيبه n = {ar(s)}، {ar(s + 1)}، {ar(s + 2)} …",
                            f"القاعدة: {rule} ⇐ تحقّق: {ar(v[0])} ثم {ar(v[1])} ثم {ar(v[2])} ✔",
                            f"للحد التالي n = {ar(s + 5)} ⇐ الناتج = {ar(nxt)}."], k,
                           "اربط الحد برقم ترتيبه؛ كثير من المتسلسلات تُحل بهذه الطريقة."))
            k += 1

    # ٢٠) مجموع الحدّين السابقين − ثابت
    for a, b, c in ((5, 8, 2), (9, 12, 3), (4, 10, 1)):
        v = [a, b]
        while len(v) < 5:
            v.append(v[-1] + v[-2] - c)
        nxt = v[-1] + v[-2] - c
        out.append(_sq(v + [None], nxt,
                       [f"{ar(v[0])} + {ar(v[1])} = {ar(v[0] + v[1])} والحد التالي {ar(v[2])} ⇐ الفرق {ar(c)}.",
                        f"القاعدة: مجموع الحدّين السابقين − {ar(c)}.",
                        f"الحد التالي = {ar(v[-2])} + {ar(v[-1])} − {ar(c)} = {ar(nxt)}."], k,
                       "جرّب الجمع أولًا، ثم اضبط الفرق الثابت."))
        k += 1

    return out


# ------------------------------------------------------------------ الحروف
def _lq(prompt, vals, ans, pool, steps, k, tip=None):
    return gq(prompt, ans, pool, steps, [lchips(vals, PURPLE)], k=k, tip=tip,
              formatter=lambda x: x)


def letter_bank():
    """أكثر من ٨٠ سؤال متتاليات حروف (عربية وإنجليزية)."""
    out = []
    k = 0
    order = "أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن هـ و ي"

    # عربي: قفزة ثابتة
    for step in (1, 2, 3, 4):
        for s in (1, 3, 5, 8, 11):
            idx = [s + i * step for i in range(4)]
            vals = [ar_letter(i) for i in idx] + [None]
            ans = ar_letter(s + 4 * step)
            pool = [ar_letter(s + 4 * step + j) for j in (1, -1, 2, -2)]
            out.append(_lq("أوجد الحرف التالي في المتتالية.", vals, ans, pool,
                           [f"رتّب الحروف: {order}.",
                            f"ترتيب الحروف المعطاة: " + "، ".join(ar(i) for i in idx) + ".",
                            f"القفزة ثابتة = {ar(step)} ⇐ الترتيب التالي {ar(s + 4 * step)}.",
                            f"الحرف رقم {ar(s + 4 * step)} هو «{ans}»."], k,
                           "اكتب الأبجدية مرقّمة على جانب ورقة الامتحان قبل أن تبدأ."))
            k += 1

    # عربي: تنازلي
    for step in (1, 2, 3):
        for s in (20, 24, 28):
            idx = [s - i * step for i in range(4)]
            if min(idx) - step < 1:
                continue
            vals = [ar_letter(i) for i in idx] + [None]
            ans = ar_letter(s - 4 * step)
            pool = [ar_letter(s - 4 * step + j) for j in (1, -1, 2, -2)]
            out.append(_lq("أوجد الحرف التالي (الترتيب تنازلي).", vals, ans, pool,
                           [f"ترتيب الحروف المعطاة: " + "، ".join(ar(i) for i in idx) + ".",
                            f"الترتيب ينقص {ar(step)} في كل خطوة.",
                            f"الترتيب التالي = {ar(s - 4 * step)} ⇐ الحرف «{ans}»."], k,
                           "التنازلي يربك كثيرين؛ اكتب الأرقام ولا تعتمد على الحفظ."))
            k += 1

    # عربي: قفزتان بالتناوب
    for a, b in ((1, 2), (2, 3), (1, 3), (2, 4)):
        for s in (1, 4, 7):
            idx, cur = [s], s
            for i in range(4):
                cur += a if i % 2 == 0 else b
                idx.append(cur)
            vals = [ar_letter(i) for i in idx] + [None]
            nxt = idx[-1] + (a if len(idx) % 2 == 1 else b)
            ans = ar_letter(nxt)
            pool = [ar_letter(nxt + j) for j in (1, -1, 2, -2)]
            out.append(_lq("أوجد الحرف التالي.", vals, ans, pool,
                           [f"ترتيب الحروف: " + "، ".join(ar(i) for i in idx) + ".",
                            f"القفزات بالتناوب: +{ar(a)} ثم +{ar(b)}.",
                            f"الدور الآن على +{ar(a if len(idx) % 2 == 1 else b)} ⇐ الترتيب {ar(nxt)} = «{ans}»."], k,
                           "لو لم تثبت القفزة فجرّب قفزتين متبادلتين."))
            k += 1

    # إنجليزي: قفزة ثابتة صعودًا وهبوطًا
    for step in (1, 2, 3, 4, 5):
        for s in (1, 2, 4, 6):
            idx = [s + i * step for i in range(4)]
            if max(idx) + step > 26:
                continue
            vals = [en_letter(i) for i in idx] + [None]
            ans = en_letter(s + 4 * step)
            pool = [en_letter(s + 4 * step + j) for j in (1, -1, 2, -2)]
            out.append(_lq("Find the next letter — أوجد الحرف التالي.", vals, ans, pool,
                           [f"A = ١، B = ٢ … Z = ٢٦.",
                            f"ترتيب الحروف: " + "، ".join(ar(i) for i in idx) + f" ⇐ القفزة {ar(step)}.",
                            f"الترتيب التالي = {ar(s + 4 * step)} ⇐ الحرف «{ans}»."], k,
                           "عدّ بالأرقام لا بالغناء: A=1 … Z=26."))
            k += 1
    for step in (2, 3, 4):
        for s in (26, 24, 22):
            idx = [s - i * step for i in range(4)]
            if min(idx) - step < 1:
                continue
            vals = [en_letter(i) for i in idx] + [None]
            ans = en_letter(s - 4 * step)
            pool = [en_letter(s - 4 * step + j) for j in (1, -1, 2, -2)]
            out.append(_lq("أوجد الحرف التالي (ترتيب عكسي).", vals, ans, pool,
                           [f"الحروف تسير للخلف: " + "، ".join(ar(i) for i in idx) + ".",
                            f"الطرح ثابت = {ar(step)}.",
                            f"الترتيب التالي = {ar(s - 4 * step)} ⇐ الحرف «{ans}»."], k,
                           "Z=26 نقطة بداية مريحة للعدّ العكسي."))
            k += 1

    # حرف + رقم ترتيبه
    for s in (1, 3, 5, 7, 9):
        vals = [f"{ar_letter(s + i)}{ar(s + i)}" for i in range(4)] + [None]
        ans = f"{ar_letter(s + 4)}{ar(s + 4)}"
        pool = [f"{ar_letter(s + 4)}{ar(s + 5)}", f"{ar_letter(s + 5)}{ar(s + 4)}",
                f"{ar_letter(s + 5)}{ar(s + 5)}", f"{ar_letter(s + 3)}{ar(s + 4)}"]
        out.append(_lq("حروف وأرقام معًا: ما الزوج التالي؟", vals, ans, pool,
                       ["انظر للحروف وحدها: متتالية هجائية بقفزة ١.",
                        "انظر للأرقام: كل رقم هو رقم ترتيب الحرف نفسه.",
                        f"الحرف التالي «{ar_letter(s + 4)}» وترتيبه {ar(s + 4)} ⇐ الزوج «{ans}»."], k,
                       "الفخ: زوج بحرف صحيح ورقم خاطئ."))
        k += 1
    for s in (2, 4, 6, 8):
        vals = [f"{en_letter(s + 2 * i)}{ar(s + 2 * i)}" for i in range(4)] + [None]
        ans = f"{en_letter(s + 8)}{ar(s + 8)}"
        pool = [f"{en_letter(s + 8)}{ar(s + 7)}", f"{en_letter(s + 7)}{ar(s + 8)}",
                f"{en_letter(s + 9)}{ar(s + 9)}", f"{en_letter(s + 6)}{ar(s + 8)}"]
        out.append(_lq("ما الزوج التالي؟", vals, ans, pool,
                       [f"الحروف تقفز ٢ في كل مرة (A=١ … Z=٢٦).",
                        "الرقم المصاحب = ترتيب الحرف نفسه.",
                        f"الحرف التالي «{en_letter(s + 8)}» وترتيبه {ar(s + 8)} ⇐ «{ans}»."], k,
                       "تحقّق من الحرف والرقم معًا قبل الاختيار."))
        k += 1

    # حروف مكرّرة بنمط
    for s in (1, 5, 9, 13):
        pairs = [f"{ar_letter(s + i)}{ar_letter(s + i + 1)}" for i in range(0, 6, 2)]
        vals = pairs + [None]
        ans = f"{ar_letter(s + 6)}{ar_letter(s + 7)}"
        pool = [f"{ar_letter(s + 6)}{ar_letter(s + 8)}", f"{ar_letter(s + 7)}{ar_letter(s + 8)}",
                f"{ar_letter(s + 5)}{ar_letter(s + 6)}", f"{ar_letter(s + 8)}{ar_letter(s + 9)}"]
        out.append(_lq("أكمل متتالية الأزواج الحرفية.", vals, ans, pool,
                       ["كل بطاقة تحوي حرفين متتاليين في الأبجدية.",
                        "وبين كل بطاقة والتالية قفزة حرفين.",
                        f"الزوج التالي = «{ans}»."], k,
                       "عامل كل بطاقة كوحدة واحدة ثم افحص القفزة بين البطاقات."))
        k += 1

    return out
