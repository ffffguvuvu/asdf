# -*- coding: utf-8 -*-
"""أدوات توليد بنوك التدريب: بناء الاختيارات وتوزيع الإجابات بشكل ثابت (لا عشوائية متغيّرة)."""

from model import Q

_AR = "٠١٢٣٤٥٦٧٨٩"


def ar(x):
    """تحويل الأرقام إلى الأرقام العربية الهندية."""
    s = str(x)
    out = ""
    for ch in s:
        if ch.isdigit():
            out += _AR[int(ch)]
        elif ch == ".":
            out += "٫"
        elif ch == "-":
            out += "−"
        else:
            out += ch
    return out


def fmt(v):
    """عرض الأعداد: يحذف الكسر العشري غير الضروري."""
    if isinstance(v, float):
        v = int(v) if abs(v - round(v)) < 1e-9 else round(v, 2)
    return ar(v)


def pick4(ans, pool, k=0, formatter=fmt):
    """
    يبني أربعة اختيارات: الإجابة + ٣ مشتّتات من pool (أول ثلاثة صالحة)،
    ثم يضع الإجابة في الموضع (k % 4) بدوران ثابت.
    يُرجع (options, answer_index).
    """
    seen = {str(formatter(ans))}
    dis = []
    for d in pool:
        s = str(formatter(d))
        if s in seen:
            continue
        seen.add(s)
        dis.append(d)
        if len(dis) == 3:
            break
    i = 1
    while len(dis) < 3:                       # ضمان وجود ثلاثة مشتّتات دائمًا
        cand = ans + i if isinstance(ans, (int, float)) else f"{ans}{i}"
        if str(formatter(cand)) not in seen:
            seen.add(str(formatter(cand)))
            dis.append(cand)
        i += 1
    vals = [ans] + dis
    r = k % 4
    if r:
        vals = vals[-r:] + vals[:-r]
    return [formatter(v) for v in vals], r


def gq(prompt, ans, pool, steps, stem, k=0, tip=None, okind="text", formatter=fmt,
       stem_note=None):
    """سؤال تدريب جاهز (اختيارات نصية افتراضيًا)."""
    opts, idx = pick4(ans, pool, k, formatter)
    return Q(prompt, opts, idx, steps, stem=stem, tip=tip, okind=okind,
             stem_note=stem_note)


def gqf(prompt, options, answer, steps, stem, tip=None, stem_note=None):
    """سؤال تدريب باختيارات مرسومة (SVG) — الترتيب كما هو."""
    return Q(prompt, options, answer, steps, stem=stem, tip=tip, okind="fig",
             stem_note=stem_note)


def rotate_options(options, answer, k):
    """يدوّر الاختيارات المرسومة ليقع الصحيح في الموضع k % 4."""
    n = len(options)
    r = (k % n - answer) % n
    if r:
        options = options[-r:] + options[:-r]
    return options, (answer + r) % n


# ------------------------------------------------------------ الحروف
AR_ALPHA = ["أ", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش",
            "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "هـ",
            "و", "ي"]
EN_ALPHA = [chr(ord("A") + i) for i in range(26)]


def ar_letter(i):
    """حرف عربي بترتيب يبدأ من ١ (مع الالتفاف)."""
    return AR_ALPHA[(i - 1) % len(AR_ALPHA)]


def en_letter(i):
    return EN_ALPHA[(i - 1) % 26]


def ar_index(ch):
    return AR_ALPHA.index(ch) + 1
