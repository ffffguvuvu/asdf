# -*- coding: utf-8 -*-
"""مولّدات أسئلة التربوي من قاعدة المعرفة + الأسئلة الحسابية (القياس والإحصاء)."""

import kb_core
import kb_eval          # noqa: F401  (يسجّل مجموعاته في kb_core.G)
import kb_extra         # noqa: F401
import kb_more          # noqa: F401
from kb_core import G

AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
LAB = ["أ", "ب", "ج", "د"]
_k = [0]                      # عدّاد لتوزيع موضع الإجابة الصحيحة


def ar(x):
    return str(x).translate(AR_DIGITS)


def arnum(x):
    """رقم عشري بصيغة عربية (الفاصلة العشرية العربية ٫)."""
    if isinstance(x, float):
        s = f"{x:.2f}".rstrip("0").rstrip(".")
    else:
        s = str(x)
    return s.translate(AR_DIGITS).replace(".", "٫")


def mk(q, correct, wrongs, e, x, t, s="مشتق من بنك المفاهيم التربوية"):
    """يبني سؤالًا بأربعة بدائل متمايزة وبإجابة موزّعة على الحروف."""
    opts, seen = [correct], {str(correct).strip()}
    for w in wrongs:
        w = str(w).strip()
        if w and w not in seen:
            seen.add(w)
            opts.append(w)
        if len(opts) == 4:
            break
    if len(opts) < 4:
        return None
    pos = _k[0] % 4
    _k[0] += 1
    opts = opts[1:]
    opts.insert(pos, correct)
    return {"q": q, "o": opts, "a": pos, "e": e, "x": x, "t": t, "s": s}


PEOPLEY = {"pioneers", "verbs"}      # أسماء أعلام وأفعال: لا تصلح مشتتات للمفاهيم


def _others(gid, field="n", limit=40, same_axis=True):
    """عناصر من مجموعات أخرى تصلح مشتتات."""
    out = []
    me = next(g for g in G if g["id"] == gid)
    for g in G:
        if g["id"] == gid:
            continue
        if (g["id"] in PEOPLEY) != (gid in PEOPLEY):
            continue
        if same_axis and g["axis"] != me["axis"]:
            continue
        if not same_axis and g["axis"] == me["axis"]:
            continue
        for it in g["items"]:
            if field in it:
                out.append(it[field])
    return out[:limit]


def _norm(t):
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        t = t.replace(a, b)
    return t


def _tok(t):
    t = _norm(t).replace("(", " ").replace(")", " ").replace("،", " ")
    return {w[2:] if w.startswith("ال") else w for w in t.split() if len(w) >= 5}


def _far(name, group_names, cat):
    """هل المصطلح بعيد دلاليًا عن كل أسماء المجموعة وعن عنوانها؟"""
    a = _tok(name)
    if not a:
        return False
    if a & _tok(cat):
        return False
    return all(not (a & _tok(n)) for n in group_names)


def _name_defs():
    m = {}
    for g in G:
        for it in g["items"]:
            m.setdefault(it["n"], set()).add(it["d"])
    return m


NAME2DEFS = _name_defs()


# ======================================================= مولّدات قاعدة المعرفة
DEF_STEMS = [
    "أيُّ المصطلحات الآتية يُشير إلى: «{d}»؟",
    "«{d}» — هذا التعريف يخصّ:",
    "المفهوم الذي يُعرَّف بأنه «{d}» هو:",
]
NAME_STEMS = [
    "أيُّ العبارات الآتية تُعبّر عن «{n}»؟",
    "ما المقصود بـ«{n}»؟",
]


def kb_bank():
    out = []
    for g in G:
        items = g["items"]
        names = [i["n"] for i in items]
        defs = [i["d"] for i in items]
        axis, cat, gid = g["axis"], g["cat"], g["id"]
        foreign_n = _others(gid, "n")
        foreign_d = _others(gid, "d")
        alien_n = [n for n in _others(gid, "n", same_axis=False, limit=80)
                   if _far(n, names, cat)]                # من محور آخر وبعيد دلاليًا

        # (١) تعريف ← مصطلح (ثلاث صياغات بمشتتات مختلفة)
        for idx, it in enumerate(items):
            pool = [n for n in names if n != it["n"]]
            extra = [n for n in foreign_n if n != it["n"]]
            for v, stem in enumerate(DEF_STEMS):
                if v == 0:
                    wr = pool[:3] if len(pool) >= 3 else pool + extra
                elif v == 1:
                    wr = (pool[1:] + pool[:1])[:2] + extra[v:v + 2]
                else:
                    wr = extra[idx % max(len(extra), 1):][:2] + pool[-2:]
                q = mk(stem.format(d=it["d"]), it["n"], wr,
                       f"«{it['n']}» = {it['d']}." + (f" ({g['note']})" if g.get("note") and v == 0 else ""),
                       axis, cat)
                if q:
                    out.append(q)

        # (٢) مصطلح ← تعريف
        for idx, it in enumerate(items):
            bad = NAME2DEFS.get(it["n"], set())           # تعريفات تخص الاسم نفسه في مجموعة أخرى
            pool = [d for d in defs if d not in bad]
            extra = [d for d in foreign_d if d not in bad]
            for v, stem in enumerate(NAME_STEMS):
                wr = (pool[idx % max(len(pool), 1):] + pool)[:3] if v == 0 else (pool[:2] + extra[:2])
                q = mk(stem.format(n=it["n"]), it["d"], wr,
                       f"التعريف الدقيق لـ«{it['n']}»: {it['d']}.", axis, cat)
                if q:
                    out.append(q)

        # (٣) صاحب النظرية في الاتجاهين
        people = [i["p"] for i in items if i.get("p")]
        for it in items:
            if not it.get("p"):
                continue
            wr = [p for p in people if p != it["p"]] + \
                 [p for p in ("سكينر", "بياجيه", "فيجوتسكي", "جاردنر", "ثورندايك",
                              "أوزوبل", "برونر", "بافلوف", "ماسلو", "جانييه") if p != it["p"]]
            q = mk(f"من صاحب «{it['n']}»؟", it["p"], wr,
                   f"{it['p']} هو صاحب «{it['n']}»: {it['d']}.", axis, cat)
            if q:
                out.append(q)
            wr2 = [n for n in names if n != it["n"]] + foreign_n
            q = mk(f"يرتبط اسم «{it['p']}» في الفكر التربوي بـ:", it["n"], wr2,
                   f"{it['p']} صاحب «{it['n']}»: {it['d']}.", axis, cat)
            if q:
                out.append(q)

        # (٤) موقف ← مفهوم
        for it in items:
            if not it.get("ex"):
                continue
            wr = [n for n in names if n != it["n"]] + foreign_n
            q = mk(f"{it['ex']} — هذا الموقف يمثّل:", it["n"], wr,
                   f"الموقف تطبيق مباشر على «{it['n']}»: {it['d']}.", axis, cat)
            if q:
                out.append(q)

        # (٥) الانتماء للفئة
        for i2, it in enumerate([] if gid in PEOPLEY else items[:6]):
            wr = alien_n[i2 * 3:i2 * 3 + 3] or alien_n[:3]
            q = mk(f"أيٌّ مما يلي يُعدّ من {cat}؟", it["n"], wr,
                   f"«{it['n']}» أحد عناصر {cat}؛ وباقي البدائل تنتمي لموضوعات أخرى.", axis, cat)
            if q:
                out.append(q)

        # (٦) الاستبعاد من الفئة (المشتت من محور مختلف تمامًا لضمان صحة المفتاح)
        for i2 in range(0 if gid in PEOPLEY else min(4, max(1, len(alien_n) // 4))):
            alien = alien_n[i2]
            wr = (names[i2:] + names)[:3]
            q = mk(f"أيٌّ مما يلي لا يُعدّ من {cat}؟", alien, wr,
                   f"«{alien}» لا ينتمي إلى {cat}، أما البدائل الأخرى فكلها منها.", axis, cat)
            if q:
                out.append(q)

        # (٧) الترتيب (للمجموعات المرتبة)
        if gid in ("bloom", "bloom_new", "affective", "psychomotor", "piaget",
                   "erikson", "kohlberg", "maslow", "law_jobs", "teaching_steps",
                   "obj_levels", "stages", "research_steps", "bandura"):
            for i2 in range(len(items) - 1):
                cur, nxt = items[i2]["n"], items[i2 + 1]["n"]
                wr = [n for n in names if n not in (cur, nxt)]
                q = mk(f"في {cat}، ما المستوى الذي يلي «{cur}» مباشرة؟", nxt, wr,
                       f"الترتيب: {' ← '.join(names)}.", axis, cat)
                if q:
                    out.append(q)
            q = mk(f"ما أول مستويات {cat}؟", items[0]["n"], names[1:],
                   f"الترتيب: {' ← '.join(names)}.", axis, cat)
            if q:
                out.append(q)
            q = mk(f"ما آخر (أعلى) مستويات {cat}؟", items[-1]["n"], names[:-1],
                   f"الترتيب: {' ← '.join(names)}.", axis, cat)
            if q:
                out.append(q)
    return out


# ======================================================= أسئلة حسابية
def nstud(n, sing="طالب", dual="طالبان", plur="طلاب", acc="طالبًا"):
    """صياغة عربية سليمة لتمييز العدد."""
    n = int(n)
    if n == 1:
        return f"{sing} واحد"
    if n == 2:
        return dual
    if 3 <= n % 100 <= 10:
        return f"{ar(n)} {plur}"
    return f"{ar(n)} {acc}"


SUBJ = ["اللغة العربية", "الرياضيات", "العلوم", "الدراسات الاجتماعية", "اللغة الإنجليزية",
        "التربية الدينية", "الحاسب الآلي", "التربية الفنية", "الفيزياء", "الأحياء",
        "الكيمياء", "الجغرافيا", "التاريخ", "النحو", "البلاغة"]
GRADE = ["الصف الرابع الابتدائي", "الصف الخامس الابتدائي", "الصف السادس الابتدائي",
         "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي",
         "الصف الأول الثانوي", "الصف الثاني الثانوي"]


def _numopts(val, cands, fmt=arnum):
    seen, out = {fmt(val)}, []
    for c in cands:
        f = fmt(c)
        if f not in seen and (isinstance(c, str) or c >= 0):
            seen.add(f)
            out.append(f)
    return out


def num_bank():
    out = []
    i = 0

    # (١) معامل السهولة والصعوبة
    for total in range(10, 61, 2):
        for right in range(2, total, 2):
            i += 1
            ease = right / total
            diff = 1 - ease
            s, g = SUBJ[i % len(SUBJ)], GRADE[i % len(GRADE)]
            if i % 2 == 0:
                q = (f"في اختبار {s} لتلاميذ {g}، أجاب عن أحد الأسئلة إجابة صحيحة "
                     f"{nstud(right)} من إجمالي {nstud(total)}. ما معامل السهولة لهذا السؤال؟")
                correct, other = arnum(round(ease, 2)), round(diff, 2)
                e = (f"معامل السهولة = عدد الإجابات الصحيحة ÷ العدد الكلي = "
                     f"{ar(right)} ÷ {ar(total)} = {arnum(round(ease, 2))}.")
            else:
                q = (f"سؤال في اختبار {s} أجاب عنه إجابة صحيحة {nstud(right)} "
                     f"من {nstud(total)}. ما معامل الصعوبة لهذا السؤال؟")
                correct, other = arnum(round(diff, 2)), round(ease, 2)
                e = (f"معامل الصعوبة = ١ − معامل السهولة = ١ − ({ar(right)} ÷ {ar(total)}) = "
                     f"{arnum(round(diff, 2))}.")
            wr = _numopts(correct, [other, round(ease + 0.1, 2), round(abs(diff - 0.15), 2),
                                    round(min(ease + 0.25, 0.99), 2)])
            qq = mk(q, correct, wr, e + " وكلما زاد معامل السهولة كان السؤال أسهل.",
                    "calc", "معامل السهولة والصعوبة")
            if qq:
                out.append(qq)
            if len(out) > 620:
                break
        if len(out) > 620:
            break

    # (٢) معامل التمييز
    n0 = len(out)
    for upper in range(6, 31):
        for lower in range(0, upper, 2):
            i += 1
            grp_n = (20, 25, 30, 40)[i % 4]
            if upper > grp_n:
                continue
            disc = (upper - lower) / grp_n
            q = (f"في تحليل مفردات اختبار، أجاب عن سؤال إجابة صحيحة {nstud(upper)} من الفئة العليا "
                 f"و{nstud(lower)} من الفئة الدنيا، وعدد أفراد كل فئة {nstud(grp_n)}. "
                 f"ما معامل التمييز لهذا السؤال؟")
            e = (f"معامل التمييز = (عدد الصواب في الفئة العليا − عدد الصواب في الفئة الدنيا) ÷ عدد أفراد الفئة "
                 f"= ({ar(upper)} − {ar(lower)}) ÷ {ar(grp_n)} = {arnum(round(disc, 2))}. "
                 f"والسؤال يُعد مقبول التمييز إذا بلغ ٠٫٣ فأكثر.")
            wr = _numopts(arnum(round(disc, 2)),
                          [round((upper + lower) / grp_n, 2), round(disc + 0.12, 2),
                           round(abs(disc - 0.2), 2), round(upper / grp_n, 2)])
            qq = mk(q, arnum(round(disc, 2)), wr, e, "calc", "معامل التمييز")
            if qq:
                out.append(qq)
            if len(out) - n0 > 420:
                break
        if len(out) - n0 > 420:
            break

    # (٣) جدول المواصفات: عدد أسئلة الموضوع
    n0 = len(out)
    for weight in (5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75):
        for total_q in (20, 24, 25, 30, 36, 40, 45, 50, 60, 72, 80, 100):
            i += 1
            cnt = weight * total_q // 100
            if cnt < 1:
                continue
            s = SUBJ[i % len(SUBJ)]
            q = (f"إذا كان الوزن النسبي لموضوع في مادة {s} يساوي {ar(weight)}٪ وعدد أسئلة "
                 f"الاختبار الكلية {ar(total_q)} سؤالًا، فكم عدد أسئلة هذا الموضوع؟")
            e = (f"عدد أسئلة الموضوع = الوزن النسبي × العدد الكلي = {ar(weight)}٪ × {ar(total_q)} "
                 f"= {ar(cnt)} سؤالًا، وهذا هو أساس جدول المواصفات.")
            wr = _numopts(ar(cnt), [cnt + 2, max(cnt - 2, 1), cnt * 2, weight, total_q - cnt], fmt=ar)
            qq = mk(q, ar(cnt), wr, e, "calc", "جدول المواصفات")
            if qq:
                out.append(qq)
            if len(out) - n0 > 420:
                break
        if len(out) - n0 > 420:
            break

    # (٤) الوزن النسبي من عدد الحصص
    n0 = len(out)
    for part in range(2, 26):
        for whole in range(part + 2, 61, 2):
            i += 1
            w = round(part / whole * 100)
            s = SUBJ[i % len(SUBJ)]
            q = (f"دُرِّس موضوع في {s} في {nstud(part, 'حصة واحدة', 'حصتان', 'حصص', 'حصة')} "
                 f"من إجمالي {ar(whole)} حصة للمقرر. "
                 f"ما الوزن النسبي للموضوع في جدول المواصفات؟")
            e = (f"الوزن النسبي = (عدد حصص الموضوع ÷ إجمالي الحصص) × ١٠٠ = "
                 f"({ar(part)} ÷ {ar(whole)}) × ١٠٠ ≈ {ar(w)}٪.")
            wr = _numopts(ar(w) + "٪", [f"{ar(w + 7)}٪", f"{ar(max(w - 6, 1))}٪",
                                        f"{ar(min(w * 2, 99))}٪", f"{ar(part * 2)}٪"], fmt=str)
            qq = mk(q, ar(w) + "٪", wr, e, "calc", "جدول المواصفات")
            if qq:
                out.append(qq)
            if len(out) - n0 > 380:
                break
        if len(out) - n0 > 380:
            break

    # (٥) المتوسط والوسيط والمنوال والمدى
    n0 = len(out)
    base = [3, 5, 7, 9, 11, 13, 4, 6, 8, 10, 12, 14, 2, 15, 17]
    for a in range(4, 46):
      for shape in (0, 1):
        for b in range(1, 10):
            i += 1
            if shape:
                data = sorted([a, a + b, a + 2 * b, a + 3 * b, a + 3 * b, a + 5 * b, a + 6 * b])
            else:
                data = sorted([a, a + b, a + 2 * b, a + 2 * b, a + 4 * b])  # القيمة المكررة = المنوال
            n_v = len(data)
            who = "خمسة طلاب" if n_v == 5 else "سبعة طلاب"
            mean = sum(data) / n_v
            med = data[n_v // 2]
            mode = (a + 3 * b) if shape else (a + 2 * b)
            rng = data[-1] - data[0]
            kind = i % 4
            ds = "، ".join(ar(v) for v in data)
            if kind == 0:
                q = f"درجات {who} هي: {ds}. ما المتوسط الحسابي؟"
                correct, e = arnum(round(mean, 2)), (
                    f"المتوسط = مجموع الدرجات ÷ عددها = {ar(sum(data))} ÷ {ar(n_v)} = {arnum(round(mean, 2))}.")
                wr = _numopts(correct, [med, mode, rng, round(mean + 2, 2)])
                t = "المتوسط الحسابي"
            elif kind == 1:
                q = f"درجات {who} هي: {ds}. ما الوسيط؟"
                correct, e = ar(med), (
                    f"نرتّب القيم تصاعديًا ثم نأخذ القيمة الوسطى = {ar(med)}؛ "
                    f"والوسيط لا يتأثر بالقيم المتطرفة.")
                wr = _numopts(correct, [ar(round(mean)), ar(mode), ar(rng), ar(data[1])], fmt=str)
                t = "الوسيط"
            elif kind == 2:
                q = f"درجات {who} هي: {ds}. ما المنوال؟"
                correct, e = ar(mode), (
                    f"المنوال هو القيمة الأكثر تكرارًا، وهي {ar(mode)} (تكررت مرتين).")
                wr = _numopts(correct, [ar(round(mean)), ar(med + 1), ar(rng), ar(data[0])], fmt=str)
                t = "المنوال"
            else:
                q = f"درجات {who} هي: {ds}. ما المدى؟"
                correct, e = ar(rng), (
                    f"المدى = أكبر قيمة − أصغر قيمة = {ar(data[-1])} − {ar(data[0])} = {ar(rng)}، "
                    f"وهو أبسط مقاييس التشتت.")
                wr = _numopts(correct, [ar(round(mean)), ar(med), ar(mode), ar(rng + 3)], fmt=str)
                t = "المدى"
            qq = mk(q, correct, wr, e, "calc", t)
            if qq:
                out.append(qq)
            if len(out) - n0 > 820:
                break
        if len(out) - n0 > 820:
            break
      if len(out) - n0 > 820:
          break

    # (٦) الدرجة المعيارية Z والتائية T
    n0 = len(out)
    for mean in range(28, 81, 2):
        for sd in (2, 3, 4, 5, 6, 8, 10):
            for z in (-2, -1, 1, 2, 3):
                i += 1
                score = mean + z * sd
                if score < 0:
                    continue
                if i % 2 == 0:
                    q = (f"حصل طالب على {ar(score)} درجة في اختبار متوسطه {ar(mean)} وانحرافه "
                         f"المعياري {ar(sd)}. ما درجته المعيارية Z؟")
                    correct = arnum(z)
                    e = (f"Z = (الدرجة − المتوسط) ÷ الانحراف المعياري = "
                         f"({ar(score)} − {ar(mean)}) ÷ {ar(sd)} = {arnum(z)}.")
                    wr = _numopts(correct, [z + 1, z - 1, -z if z else 2, round(z / 2, 2)])
                    t = "الدرجة المعيارية Z"
                else:
                    tscore = 10 * z + 50
                    q = (f"حصل طالب على {ar(score)} درجة في اختبار متوسطه {ar(mean)} وانحرافه "
                         f"المعياري {ar(sd)}. ما درجته التائية T؟")
                    correct = ar(tscore)
                    e = (f"أولًا: Z = ({ar(score)} − {ar(mean)}) ÷ {ar(sd)} = {arnum(z)}، "
                         f"ثم T = ١٠ × Z + ٥٠ = {ar(tscore)}؛ "
                         f"والدرجة التائية متوسطها ٥٠ وانحرافها المعياري ١٠.")
                    wr = _numopts(correct, [ar(tscore + 10), ar(tscore - 10), ar(50), ar(abs(z) * 50)],
                                  fmt=str)
                    t = "الدرجة التائية"
                qq = mk(q, correct, wr, e, "calc", t)
                if qq:
                    out.append(qq)
                if len(out) - n0 > 300:
                    break
            if len(out) - n0 > 300:
                break
        if len(out) - n0 > 300:
            break

    # (٧) النسب المئوية للنجاح والحضور
    n0 = len(out)
    for total in range(16, 81, 2):
        for pas in range(6, total, 3):
            i += 1
            pct = round(pas / total * 100)
            s, g = SUBJ[i % len(SUBJ)], GRADE[i % len(GRADE)]
            q = (f"نجح {nstud(pas)} من {nstud(total)} في اختبار {s} بـ{g}. "
                 f"ما نسبة النجاح تقريبًا؟")
            e = (f"نسبة النجاح = (عدد الناجحين ÷ العدد الكلي) × ١٠٠ = "
                 f"({ar(pas)} ÷ {ar(total)}) × ١٠٠ ≈ {ar(pct)}٪.")
            wr = _numopts(f"{ar(pct)}٪", [f"{ar(min(pct + 8, 100))}٪", f"{ar(max(pct - 9, 1))}٪",
                                          f"{ar(100 - pct)}٪", f"{ar(pas)}٪"], fmt=str)
            qq = mk(q, f"{ar(pct)}٪", wr, e, "calc", "النسب المئوية")
            if qq:
                out.append(qq)
            if len(out) - n0 > 380:
                break
        if len(out) - n0 > 380:
            break

    # (٨) تفسير معامل الارتباط
    n0 = len(out)
    vals = [round(v / 100, 2) for v in range(-96, 100, 3)]
    for v in vals:
        for mode2 in range(4):
            i += 1
            if v > 0.7:
                desc = "علاقة طردية قوية"
            elif v > 0.3:
                desc = "علاقة طردية متوسطة"
            elif v > 0:
                desc = "علاقة طردية ضعيفة"
            elif v == 0:
                desc = "لا توجد علاقة"
            elif v > -0.3:
                desc = "علاقة عكسية ضعيفة"
            elif v > -0.7:
                desc = "علاقة عكسية متوسطة"
            else:
                desc = "علاقة عكسية قوية"
            pair = [("ساعات المذاكرة", "درجات التحصيل"), ("عدد مرات الغياب", "درجة الطالب"),
                    ("القلق المرتفع", "الأداء في الامتحان"), ("الدافعية", "المشاركة الصفية")][mode2]
            q = (f"بلغ معامل الارتباط بين {pair[0]} و{pair[1]} {arnum(v)}. "
                 f"كيف تُفسَّر هذه النتيجة؟")
            e = (f"إشارة المعامل تحدد الاتجاه وقيمته المطلقة تحدد القوة؛ والقيمة {arnum(v)} تعني {desc}. "
                 f"ولا يعني الارتباط وجود علاقة سببية.")
            wr = ["علاقة طردية قوية", "علاقة عكسية قوية", "علاقة طردية متوسطة",
                  "علاقة عكسية متوسطة", "لا توجد علاقة", "علاقة طردية ضعيفة"]
            wr = [w for w in wr if w != desc]
            qq = mk(q, desc, wr, e, "calc", "معامل الارتباط")
            if qq:
                out.append(qq)
            if len(out) - n0 > 260:
                break
        if len(out) - n0 > 260:
            break

    # (٩) عدد الحصص والزمن وتوزيع الدرجات
    n0 = len(out)
    for marks in (10, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120):
        for share in (5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 75, 80):
            i += 1
            val = marks * share // 100
            if val < 1:
                continue
            s = SUBJ[i % len(SUBJ)]
            lvl = ("التذكر", "الفهم", "التطبيق", "التحليل", "التركيب", "التقويم")[i % 6]
            q = (f"اختبار {s} من {ar(marks)} درجة، وخُصّص {ar(share)}٪ من الدرجة الكلية لمستوى "
                 f"{lvl} في جدول المواصفات. كم درجة تُخصَّص لهذا المستوى؟")
            e = (f"الدرجة = النسبة × الدرجة الكلية = {ar(share)}٪ × {ar(marks)} = {ar(val)} درجة.")
            wr = _numopts(ar(val), [val + 3, max(val - 3, 1), marks - val, share], fmt=ar)
            qq = mk(q, ar(val), wr, e, "calc", "توزيع الدرجات")
            if qq:
                out.append(qq)
            if len(out) - n0 > 320:
                break
        if len(out) - n0 > 320:
            break

    # (١٠) الانحراف المعياري لمجموعة بسيطة
    n0 = len(out)
    for m in range(4, 60):
        for d in (1, 2, 3, 4, 5, 6):
            i += 1
            data = [m - 2 * d, m - d, m, m + d, m + 2 * d]
            if data[0] < 0:
                continue
            var = sum((v - m) ** 2 for v in data) / len(data)
            sd = var ** 0.5
            ds = "، ".join(ar(v) for v in data)
            q = (f"درجات خمسة طلاب: {ds}. متوسطها {ar(m)}. ما الانحراف المعياري "
                 f"(لأقرب منزلتين عشريتين)؟")
            e = (f"التباين = مجموع مربعات الانحرافات ÷ العدد = {arnum(round(var, 2))}، "
                 f"والانحراف المعياري = الجذر التربيعي للتباين ≈ {arnum(round(sd, 2))}.")
            wr = _numopts(arnum(round(sd, 2)), [round(var, 2), round(sd + 1, 2),
                                                round(sd / 2, 2), round(sd * 2, 2)])
            qq = mk(q, arnum(round(sd, 2)), wr, e, "calc", "الانحراف المعياري")
            if qq:
                out.append(qq)
            if len(out) - n0 > 260:
                break
        if len(out) - n0 > 260:
            break

    # (١١) الوسيط لعدد زوجي من القيم
    n0 = len(out)
    for a in range(3, 50):
        for b in range(1, 8):
            i += 1
            data = [a, a + b, a + 2 * b, a + 3 * b, a + 4 * b, a + 5 * b]
            med = (data[2] + data[3]) / 2
            ds = "، ".join(ar(v) for v in data)
            q = f"درجات ستة طلاب مرتبة تصاعديًا: {ds}. ما الوسيط؟"
            e = (f"عدد القيم زوجي، فالوسيط = متوسط القيمتين الوسطيتين = "
                 f"({ar(data[2])} + {ar(data[3])}) ÷ ٢ = {arnum(med)}.")
            wr = _numopts(arnum(med), [data[2], data[3], round(sum(data) / 6, 2), data[-1] - data[0]])
            qq = mk(q, arnum(med), wr, e, "calc", "الوسيط")
            if qq:
                out.append(qq)
            if len(out) - n0 > 240:
                break
        if len(out) - n0 > 240:
            break

    # (١٢) المتوسط المرجّح (أعمال السنة + الامتحان)
    n0 = len(out)
    for w1 in (20, 25, 30, 40, 50):
        for y in range(10, 101, 5):
            for e1 in range(20, 101, 10):
                i += 1
                w2 = 100 - w1
                val = (y * w1 + e1 * w2) / 100
                s2 = SUBJ[i % len(SUBJ)]
                q = (f"في مادة {s2} تُحسب أعمال السنة بوزن {ar(w1)}٪ والامتحان النهائي بوزن {ar(w2)}٪. "
                     f"حصل طالب على {ar(y)}٪ في أعمال السنة و{ar(e1)}٪ في الامتحان. ما درجته النهائية؟")
                e = (f"الدرجة = ({ar(y)} × {ar(w1)}٪) + ({ar(e1)} × {ar(w2)}٪) = {arnum(round(val, 2))}٪ "
                     f"(متوسط مرجّح وليس متوسطًا حسابيًا بسيطًا).")
                wr = _numopts(arnum(round(val, 2)) + "٪",
                              [f"{arnum(round((y + e1) / 2, 2))}٪", f"{arnum(round(val + 5, 2))}٪",
                               f"{arnum(round(abs(val - 7), 2))}٪", f"{ar(y)}٪"], fmt=str)
                qq = mk(q, arnum(round(val, 2)) + "٪", wr, e, "calc", "المتوسط المرجّح")
                if qq:
                    out.append(qq)
                if len(out) - n0 > 320:
                    break
            if len(out) - n0 > 320:
                break
        if len(out) - n0 > 320:
            break

    # (١٣) تصحيح ثبات التجزئة النصفية (سبيرمان - براون)
    n0 = len(out)
    for r in [round(v / 100, 2) for v in range(30, 96, 1)]:
        for _ in range(3):
            i += 1
            full = 2 * r / (1 + r)
            q = (f"بلغ معامل الارتباط بين نصفي اختبار {arnum(r)}. ما معامل ثبات الاختبار كاملًا "
                 f"باستخدام معادلة سبيرمان–براون؟")
            e = (f"معادلة سبيرمان–براون: ٢ر ÷ (١ + ر) = (٢ × {arnum(r)}) ÷ (١ + {arnum(r)}) "
                 f"= {arnum(round(full, 2))}؛ لأن التجزئة النصفية تقلل طول الاختبار فيُصحَّح معاملها.")
            wr = _numopts(arnum(round(full, 2)), [r, round(r / 2, 2), round(min(full + 0.1, 0.99), 2),
                                                  round(abs(full - 0.15), 2)])
            qq = mk(q, arnum(round(full, 2)), wr, e, "calc", "ثبات الاختبار")
            if qq:
                out.append(qq)
            if len(out) - n0 > 150:
                break
        if len(out) - n0 > 150:
            break

    # (١٤) نسبة الحضور والغياب
    n0 = len(out)
    for total in range(20, 61, 2):
        for absent in range(1, 16):
            i += 1
            if absent >= total:
                continue
            pct = round((total - absent) / total * 100)
            g = GRADE[i % len(GRADE)]
            q = (f"فصل بـ{g} عدد تلاميذه {nstud(total)}، غاب منهم {nstud(absent)}. "
                 f"ما نسبة الحضور تقريبًا؟")
            e = (f"نسبة الحضور = (الحاضرون ÷ العدد الكلي) × ١٠٠ = "
                 f"(({ar(total)} − {ar(absent)}) ÷ {ar(total)}) × ١٠٠ ≈ {ar(pct)}٪.")
            wr = _numopts(f"{ar(pct)}٪", [f"{ar(100 - pct)}٪", f"{ar(min(pct + 6, 100))}٪",
                                          f"{ar(max(pct - 8, 1))}٪", f"{ar(absent)}٪"], fmt=str)
            qq = mk(q, f"{ar(pct)}٪", wr, e, "calc", "نسبة الحضور")
            if qq:
                out.append(qq)
            if len(out) - n0 > 220:
                break
        if len(out) - n0 > 220:
            break

    # (١٥) توزيع أسئلة المستويات في جدول المواصفات
    n0 = len(out)
    LEVELS = [("التذكر", 30), ("الفهم", 25), ("التطبيق", 20), ("التحليل", 15), ("التقويم", 10)]
    for total_q in range(20, 121, 2):
        for lv, pc in LEVELS:
            i += 1
            cnt = total_q * pc // 100
            if cnt < 1:
                continue
            q = (f"اختبار مكوّن من {ar(total_q)} سؤالًا، وخُصّص لمستوى {lv} ما نسبته {ar(pc)}٪ "
                 f"من الأسئلة. كم سؤالًا لهذا المستوى؟")
            e = f"عدد الأسئلة = {ar(pc)}٪ × {ar(total_q)} = {ar(cnt)} سؤالًا."
            wr = _numopts(ar(cnt), [cnt + 2, max(cnt - 2, 1), cnt * 2, pc], fmt=ar)
            qq = mk(q, ar(cnt), wr, e, "calc", "جدول المواصفات")
            if qq:
                out.append(qq)
            if len(out) - n0 > 260:
                break
        if len(out) - n0 > 260:
            break

    return out
