# -*- coding: utf-8 -*-
"""نواة بنك أسئلة اللغة العربية لمسابقات التعيين.

كل سؤال: q نص السؤال · o أربعة خيارات · a رقم الإجابة · e الشرح المفصّل
          b الفرع · t الموضوع · d الصعوبة (1 سهل 2 متوسط 3 صعب) · r التكرار
"""

import random
import re
import unicodedata

QS = []
_SEEN = set()

RNG = random.Random(20261008)

BRANCHES = [
    ("nahw", "النحو والإعراب"),
    ("sarf", "الصرف والاشتقاق"),
    ("imla", "الإملاء وعلامات الترقيم"),
    ("bala", "البلاغة"),
    ("adab", "الأدب والنصوص"),
    ("naqd", "النقد الأدبي"),
    ("arud", "العروض والقافية"),
    ("fiqh", "فقه اللغة والأصوات"),
    ("mjam", "المعاجم والدلالة والمفردات"),
    ("uslb", "الأساليب والتعبير والأخطاء الشائعة"),
    ("turq", "طرق تدريس اللغة العربية"),
]
BR_NAMES = dict(BRANCHES)

_TASH = re.compile("[\u0617-\u061a\u064b-\u0652\u0670\u0640]")
_PUN = re.compile("[«»\"'(),.:;!?؟\\-—–\\[\\]/…]")
_WS = re.compile(r"\s+")


def norm(s):
    s = _TASH.sub("", str(s))
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ٱ", "ا"),
                 ("ة", "ه"), ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    s = _PUN.sub(" ", s)
    return _WS.sub(" ", s).strip()


def ad(n):
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def add(q, opts, correct, exp, br, topic, diff=2, rep=0, src=""):
    """يضيف سؤالًا. correct = نصّ الإجابة الصحيحة (يجب أن يكون ضمن opts)."""
    opts = [str(x).strip() for x in opts if str(x).strip()]
    seen, clean = set(), []
    for o in opts:
        k = norm(o)
        if k and k not in seen:
            seen.add(k)
            clean.append(o)
    if len(clean) != 4:
        return False
    if norm(correct) not in {norm(o) for o in clean}:
        return False
    key = (norm(q), norm(correct))
    if key in _SEEN:
        return False
    _SEEN.add(key)

    order = clean[:]
    RNG.shuffle(order)
    ai = [i for i, o in enumerate(order) if norm(o) == norm(correct)][0]
    QS.append({
        "q": q.strip(), "o": order, "a": ai, "e": exp.strip(),
        "b": br, "t": topic, "d": int(diff), "r": int(rep), "s": src,
    })
    return True


def distract(correct, pool, k=3, rng=None):
    """يختار k مشتتات من pool تختلف عن correct."""
    rng = rng or RNG
    cands = [p for p in pool if norm(p) != norm(correct)]
    uniq, seen = [], set()
    for c in cands:
        if norm(c) not in seen:
            seen.add(norm(c))
            uniq.append(c)
    if len(uniq) < k:
        return None
    return rng.sample(uniq, k)


def mk(q, correct, pool, exp, br, topic, diff=2, rep=0, src="", rng=None):
    """يبني سؤالًا بأربعة خيارات: الصحيح + ثلاثة مشتتات من pool."""
    ds = distract(correct, pool, 3, rng)
    if ds is None:
        return False
    return add(q, [correct] + ds, correct, exp, br, topic, diff, rep, src)


def stats():
    from collections import Counter
    c = Counter(x["b"] for x in QS)
    t = Counter((x["b"], x["t"]) for x in QS)
    return c, t
