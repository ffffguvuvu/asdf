# -*- coding: utf-8 -*-
"""أدوات بناء بنك أسئلة مسابقة الأزهر (معلم لغة عربية): قاعدة معرفة + مولّدات + أسئلة منسوخة."""

AR = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
LAB = ["أ", "ب", "ج", "د"]

GA = []          # مجموعات قاعدة المعرفة
CUR = []         # الأسئلة المنقولة/المحررة يدويًا
_k = [0]

SRC_HOT = "من الأسئلة الأكثر تكرارًا في المسابقات"
SRC_CUR = "سؤال مختار على نمط المسابقات"
SRC_KB = "مشتق من بنك المفاهيم"


def ar(x):
    return str(x).translate(AR)


def grp(gid, sec, cat, items, note=None, hot=False):
    """hot=True ⇐ موضوع متكرر في الامتحانات، تُعلَّم أسئلته بعلامة التكرار."""
    GA.append({"id": gid, "sec": sec, "cat": cat, "items": items, "note": note, "hot": hot})
    return gid


def mk(q, correct, wrongs, e, sec, topic, src=SRC_KB, r=0):
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
    return {"q": q, "o": opts, "a": pos, "e": e, "x": sec, "t": topic, "s": src, "r": r}


def cq(sec, topic, q, correct, wrongs, e, r=2, src=None):
    """تسجيل سؤال منقول/محرر؛ r=2 ⇒ من الأكثر تكرارًا، r=1 ⇒ متكرر."""
    CUR.append((sec, topic, q, correct, wrongs, e, r,
                src or (SRC_HOT if r == 2 else SRC_CUR)))


def cur_bank():
    out = []
    for sec, topic, q, correct, wrongs, e, r, src in CUR:
        item = mk(q, correct, wrongs, e, sec, topic, src, r)
        if item:
            out.append(item)
    return out


# ------------------------------------------------------------------ مولّدات
DEF_STEMS = [
    "أيُّ المصطلحات الآتية يدل على: «{d}»؟",
    "«{d}» — هذا التعريف يخصّ:",
    "ما المصطلح الذي يُعرَّف بأنه «{d}»؟",
]
NAME_STEMS = [
    "ما المقصود بـ«{n}»؟",
    "أيُّ العبارات الآتية تعبّر عن «{n}»؟",
]

PEOPLE_LIKE = set()        # مجموعات أسماء الأعلام (مشتتاتها من جنسها)


def _norm(t):
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        t = t.replace(a, b)
    return t


def _tok(t):
    t = _norm(t).replace("(", " ").replace(")", " ").replace("،", " ").replace("«", " ").replace("»", " ")
    return {w[2:] if w.startswith("ال") else w for w in t.split() if len(w) >= 5}


def _far(name, names, cat):
    a = _tok(name)
    if not a or (a & _tok(cat)):
        return False
    return all(not (a & _tok(n)) for n in names)


def _pool(gid, field="n", same_sec=True, limit=90):
    me = next(g for g in GA if g["id"] == gid)
    out = []
    for g in GA:
        if g["id"] == gid:
            continue
        if (g["id"] in PEOPLE_LIKE) != (gid in PEOPLE_LIKE):
            continue
        if same_sec and g["sec"] != me["sec"]:
            continue
        if not same_sec and g["sec"] == me["sec"]:
            continue
        for it in g["items"]:
            if field in it:
                out.append(it[field])
    return out[:limit]


def kb_bank():
    name2defs = {}
    for g in GA:
        for it in g["items"]:
            name2defs.setdefault(_norm(it["n"]), set()).add(it["d"])

    out = []
    for g in GA:
        items, sec, cat, gid = g["items"], g["sec"], g["cat"], g["id"]
        r = 1 if g["hot"] else 0
        names = [i["n"] for i in items]
        defs = [i["d"] for i in items]
        near_n = _pool(gid, "n")
        near_d = _pool(gid, "d")
        alien = [n for n in _pool(gid, "n", same_sec=False) if _far(n, names, cat)]

        for idx, it in enumerate(items):
            sib = [n for n in names if n != it["n"]]
            far = [n for n in near_n if n != it["n"]]
            for v, stem in enumerate(DEF_STEMS):
                if v == 0:
                    wr = sib[:3] if len(sib) >= 3 else sib + far
                elif v == 1:
                    wr = (sib[1:] + sib[:1])[:2] + far[idx % max(len(far), 1):][:2]
                else:
                    wr = far[(idx + 2) % max(len(far), 1):][:2] + sib[-2:]
                item = mk(stem.format(d=it["d"]), it["n"], wr,
                          f"«{it['n']}»: {it['d']}." +
                          (f" ({g['note']})" if g.get("note") and v == 0 else ""),
                          sec, cat, SRC_KB, r)
                if item:
                    out.append(item)

            bad = name2defs.get(_norm(it["n"]), set())
            sibd = [d for d in defs if d not in bad]
            fard = [d for d in near_d if d not in bad]
            for v, stem in enumerate(NAME_STEMS):
                wr = (sibd[idx % max(len(sibd), 1):] + sibd)[:3] if v == 0 else (sibd[:2] + fard[:2])
                item = mk(stem.format(n=it["n"]), it["d"], wr,
                          f"التعريف الدقيق لـ«{it['n']}»: {it['d']}.", sec, cat, SRC_KB, r)
                if item:
                    out.append(item)

        # صاحب العمل / العلم
        people = [i["p"] for i in items if i.get("p")]
        for it in items:
            if not it.get("p"):
                continue
            wr = [p for p in people if p != it["p"]]
            item = mk(f"من صاحب «{it['n']}»؟", it["p"], wr,
                      f"{it['p']} صاحب «{it['n']}»: {it['d']}.", sec, cat, SRC_KB, r)
            if item:
                out.append(item)
            item = mk(f"يرتبط اسم «{it['p']}» بـ:", it["n"],
                      [n for n in names if n != it["n"]] + near_n,
                      f"{it['p']} صاحب «{it['n']}»: {it['d']}.", sec, cat, SRC_KB, r)
            if item:
                out.append(item)

        # مثال تطبيقي / شاهد
        for it in items:
            if not it.get("ex"):
                continue
            item = mk(f"{it['ex']} — هذا مثال على:", it["n"],
                      [n for n in names if n != it["n"]] + near_n,
                      f"المثال تطبيق على «{it['n']}»: {it['d']}.", sec, cat, SRC_KB, max(r, 1))
            if item:
                out.append(item)

        # معلومة إضافية
        for it in items:
            if not it.get("xt"):
                continue
            item = mk(f"أيُّ العبارات الآتية صحيحة عن «{it['n']}»؟", it["xt"],
                      [x.get("xt") or x["d"] for x in items if x["n"] != it["n"]] + near_d,
                      f"«{it['n']}»: {it['xt']}", sec, cat, SRC_KB, r)
            if item:
                out.append(item)

        if gid not in PEOPLE_LIKE and alien:
            for i2, it in enumerate(items[:6]):
                item = mk(f"أيٌّ مما يلي يُعدّ من {cat}؟", it["n"],
                          alien[i2 * 3:i2 * 3 + 3] or alien[:3],
                          f"«{it['n']}» من {cat}؛ وباقي البدائل من موضوعات أخرى.", sec, cat, SRC_KB, r)
                if item:
                    out.append(item)
            for i2 in range(min(4, max(1, len(alien) // 4))):
                item = mk(f"أيٌّ مما يلي ليس من {cat}؟", alien[i2],
                          (names[i2:] + names)[:3],
                          f"«{alien[i2]}» لا ينتمي إلى {cat}، وباقي البدائل منها.", sec, cat, SRC_KB, r)
                if item:
                    out.append(item)
    return out


def ordered_bank(gid_list):
    """أسئلة الترتيب للمجموعات المرتبة."""
    out = []
    for g in GA:
        if g["id"] not in gid_list:
            continue
        names = [i["n"] for i in g["items"]]
        r = 1 if g["hot"] else 0
        for i2 in range(len(names) - 1):
            item = mk(f"في {g['cat']}، ما الذي يأتي بعد «{names[i2]}» مباشرة؟", names[i2 + 1],
                      [n for n in names if n not in (names[i2], names[i2 + 1])],
                      f"الترتيب: {' ← '.join(names)}.", g["sec"], g["cat"], SRC_KB, r)
            if item:
                out.append(item)
        for q, c in ((f"ما أول {g['cat']}؟", names[0]), (f"ما آخر {g['cat']}؟", names[-1])):
            item = mk(q, c, [n for n in names if n != c],
                      f"الترتيب: {' ← '.join(names)}.", g["sec"], g["cat"], SRC_KB, r)
            if item:
                out.append(item)
    return out
