# -*- coding: utf-8 -*-
"""مدقّق مستقل لبنك أسئلة الأزهر: البنية + التكرار + التناقض + إعادة حساب المفاتيح الرقمية."""

import io
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "azhar"), os.path.join(HERE, "tarbawy"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import build_azhar as B  # noqa: E402

AR = "٠١٢٣٤٥٦٧٨٩"
TASH = re.compile(r"[\u064B-\u0652\u0640]")


def de_ar(s):
    """يحوّل الأرقام العربية إلى إنجليزية."""
    return "".join(str(AR.index(c)) if c in AR else c for c in s)


def nums(s):
    return [int(x) for x in re.findall(r"\d+", de_ar(s))]


def norm(s):
    s = TASH.sub("", str(s))
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()



# ====================================================================
#   فحص الملف المُنتَج: أخطاء تظهر في المتصفح فقط ولا يكشفها node --check
# ====================================================================
# أسماء محجوزة في كائن window؛ تعريف أيٍّ منها في النطاق العام يُبطل السكربت
# كاملًا برسالة "Identifier 'x' has already been declared" قبل تنفيذ أي سطر.
RESERVED = ("top", "name", "status", "length", "self", "parent", "origin",
            "history", "location", "closed", "event", "screen", "frames",
            "print", "focus", "blur", "open", "close", "scroll", "external",
            "navigator", "document", "alert", "confirm", "menubar", "toolbar",
            "personalbar", "scrollbars", "statusbar", "locationbar", "opener",
            "window", "innerWidth", "innerHeight", "origin")


def lint_html(path):
    import json as _json
    out = []
    h = io.open(path, encoding="utf-8").read()

    m = re.search(r'<script id="DATA" type="application/json">(.*?)</script>', h, re.S)
    if not m:
        return [f"{path}: لا توجد حمولة بيانات"]
    try:
        data = _json.loads(m.group(1))
    except Exception as ex:
        return [f"{path}: حمولة JSON تالفة — {ex}"]

    js = "\n".join(re.findall(r"<script>(.*?)</script>", h, re.S))

    # (أ) تعريف اسم محجوز في النطاق العام (سطر بلا إزاحة)
    for kw in ("function", "let", "const", "var"):
        for mm in re.finditer(r"^" + kw + r"\s+([A-Za-z_$][\w$]*)", js, re.M):
            if mm.group(1) in RESERVED:
                out.append(f"{path}: تعريف «{kw} {mm.group(1)}» في النطاق العام "
                           f"يتعارض مع window.{mm.group(1)} ويُبطل السكربت كاملًا")

    # (ب) مراجع DOM غير موجودة
    ids = set(re.findall(r'id="([^"]+)"', h))
    for ref in set(re.findall(r"getElementById\(['\"]([^'\"]+)", js)):
        if ref not in ids:
            out.append(f"{path}: getElementById('{ref}') بلا عنصر مقابل")

    # (ج) سلامة الصفوف
    nt = len(data.get("topics", []))
    for i, r in enumerate(data.get("q", [])):
        if len(r) not in (6, 8) or len(r[1]) != 4 or not (0 <= r[2] < 4) \
                or not (0 <= r[5] < nt):
            out.append(f"{path}: الصف {i} تالف")
            break
    return out


def main():
    qs = B.collect()
    errs, warns, checked = [], [], Counter()

    # الموضوعات التي يكون التمايز فيها بالهمزة/الشكل مقصودًا، فلا يُحسب تطابقًا
    ORTH = ("الإملاء", "الميزان الصرفي", "تصويب الأخطاء", "همزة", "الألف اللينة",
            "التاء المربوطة")

    def is_orth(q):
        return any(k in q["t"] for k in ORTH)

    NEG = ("غير ", "لا ", "ليس ", "عدم ", "بدون ")

    def sub_bound(a, b):
        """هل a كلمةٌ تامة داخل b؟ (مع مراعاة حدود الكلمات واستثناء النفي)"""
        if len(a) < 10 or a not in b or a == b:
            return False
        # «غير مهم وغير عاجل» مقابل «مهم وغير عاجل»: تضادّ مقصود لا التباس
        if any(b.startswith(n) and b[len(n):] == a for n in NEG):
            return False
        i = b.find(a)
        while i >= 0:
            pre_ok = i == 0 or b[i - 1] == " "
            j = i + len(a)
            post_ok = j == len(b) or b[j] == " "
            if pre_ok and post_ok:
                return True
            i = b.find(a, i + 1)
        return False

    # ---------------------------------------------------------- (١) البنية
    for i, q in enumerate(qs):
        tag = f"[{i}] {q['q'][:60]}"
        if len(q["o"]) != 4:
            errs.append(f"{tag} :: عدد البدائل {len(q['o'])}")
        if len(set(q["o"])) != 4:
            errs.append(f"{tag} :: بدائل مكرّرة حرفيًّا")
        elif len(set(map(norm, q["o"]))) != 4 and not is_orth(q):
            errs.append(f"{tag} :: بدائل تتطابق بعد تطبيع الهمزات")
        if not 0 <= q["a"] < len(q["o"]):
            errs.append(f"{tag} :: مفتاح خارج النطاق")
        for k in ("q", "e", "t", "s"):
            if not str(q.get(k, "")).strip():
                errs.append(f"{tag} :: الحقل {k} فارغ")
        if q["x"] not in B.SEC_NAME:
            errs.append(f"{tag} :: قسم مجهول {q['x']}")
        if q["r"] not in (0, 1, 2):
            errs.append(f"{tag} :: رتبة تكرار غير صالحة {q['r']}")
        if len(q["q"]) < 8:
            warns.append(f"{tag} :: نص السؤال قصير جدًّا")

    # ------------------------------------------- (٢) بدائل ملتبسة (احتواء)
    for i, q in enumerate(qs):
        on = [norm(o) for o in q["o"]]
        c = on[q["a"]]
        for j, o in enumerate(on):
            if j == q["a"] or o == c:
                continue
            if sub_bound(c, o) or sub_bound(o, c):
                errs.append(f"[{i}] بديل يحتوي الإجابة (التباس) — {q['q'][:46]} "
                            f"| ✔{q['o'][q['a']]} ✘{q['o'][j]}")

    # --------------------------- (٣) تناقض حقيقي (ثلاثة اختبارات مستقلة)
    # (٣-أ) نفس المتن ونفس البدائل بمفتاحين مختلفين
    exact = defaultdict(set)
    for q in qs:
        exact[(norm(q["q"]), frozenset(map(norm, q["o"])))].add(norm(q["o"][q["a"]]))
    for (stem, _), v in exact.items():
        if len(v) > 1:
            errs.append(f"تناقض قاطع: «{stem[:60]}» بنفس البدائل ومفاتيح مختلفة {sorted(v)}")

    # (٣-ب) خيار صحيح في نسخة وخاطئ في نسخة أخرى من المتن نفسه
    keys, nonkeys = defaultdict(set), defaultdict(set)
    for q in qs:
        # الأسئلة التي تتوقف إجابتها على مجموعة البدائل نفسها لا تصلح لهذا الاختبار
        if is_orth(q) or norm(q["q"]).startswith(("اي ", "ايُّ ")):
            continue
        st = norm(q["q"])
        for j, o in enumerate(q["o"]):
            (keys if j == q["a"] else nonkeys)[st].add(norm(o))
    for st in keys:
        both = keys[st] & nonkeys[st]
        if both:
            errs.append(f"تناقض: «{st[:60]}» الخيار {sorted(both)[:2]} صحيح وخاطئ معًا")

    # (٣-ج) متن واحد بإجابات مختلفة في موضوعات مختلفة (اشتراك لفظي)
    bytopic = defaultdict(set)
    for q in qs:
        bytopic[norm(q["q"])].add((q["t"], norm(q["o"][q["a"]])))
    for st, v in bytopic.items():
        tps = {t for t, _ in v}
        if len(tps) > 1 and len({a for _, a in v}) > 1:
            warns.append(f"متن مشترك بين موضوعات: «{st[:55]}» {sorted(tps)[:3]}")

    # ------------------------------------------------- (٤) توازن المفاتيح
    pos = Counter(q["a"] for q in qs)
    tot = len(qs)
    for k, v in sorted(pos.items()):
        if not 0.15 <= v / tot <= 0.35:
            warns.append(f"توزيع المفاتيح غير متوازن: الموضع {k} = {v / tot:.1%}")

    # ====================================================================
    #           (٥) إعادة الحساب المستقلة للمفاتيح الرقمية
    # ====================================================================
    def key(q):
        return q["o"][q["a"]]

    def expect(q, want, label):
        """يتحقق أن المفتاح يساوي القيمة المحسوبة مستقلًّا."""
        got = nums(key(q))
        checked[label] += 1
        if not got or got[0] != want:
            errs.append(f"[{label}] مفتاح خاطئ: «{q['q'][:70]}» ⇐ {key(q)} (المتوقع {want})")

    UNITS = {"جيجابايت": 1024 ** 3, "ميجابايت": 1024 ** 2, "كيلوبايت": 1024, "بايت": 1}
    for q in qs:
        t, n = q["q"], nums(q["q"])

        # — تحويلات وحدات التخزين —
        m = re.search(r"كم (ميجابايت|كيلوبايت|بايت|بت) في (\d+) (جيجابايت|ميجابايت|كيلوبايت|بايت)",
                      de_ar(t))
        if m and n:
            dst, cnt, src = m.group(1), int(m.group(2)), m.group(3)
            if dst == "بت" and src == "بايت":
                expect(q, cnt * 8, "بايت←بت")
            elif dst in UNITS and src in UNITS:
                expect(q, cnt * UNITS[src] // UNITS[dst], "وحدات التخزين")

        # — النسبة المئوية —
        m = re.search(r"كم يساوي (\d+)% من (\d+)", de_ar(t))
        if m:
            expect(q, int(m.group(1)) * int(m.group(2)) // 100, "النسبة المئوية")

        # — المسافة = السرعة × الزمن —
        m = re.search(r"سرعته[اً]? (\d+) كم/س.*?(\d+) ساعات?", de_ar(t))
        if m and "المسافة" in t:
            expect(q, int(m.group(1)) * int(m.group(2)), "المسافة")

        # — السرعة = المسافة ÷ الزمن —
        m = re.search(r"قطعت?\s*(?:سيارة\s*)?(\d+) كم في (\d+) ساعات?", de_ar(t))
        if m and "سرعت" in t:
            d, h = int(m.group(1)), int(m.group(2))
            if d % h == 0:
                expect(q, d // h, "السرعة")

        # — متتابعة حسابية —
        if "أكمل المتتابعة" in t or "ما العدد التالي" in t:
            seq = nums(t)
            if len(seq) >= 4:
                d = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
                if len(set(d)) == 1:
                    expect(q, seq[-1] + d[0], "متتابعة حسابية")
                elif len(seq) >= 4 and all(seq[i] and seq[i + 1] % seq[i] == 0
                                           for i in range(len(seq) - 1)) \
                        and len({seq[i + 1] // seq[i] for i in range(len(seq) - 1)}) == 1:
                    expect(q, seq[-1] * (seq[1] // seq[0]), "متتابعة هندسية")

    # ---------------------------------------------- (٦) تغطية ومجاميع
    bysec = Counter(q["x"] for q in qs)
    byrank = Counter(q["r"] for q in qs)
    topics = len({q["t"] for q in qs})
    noexp = sum(1 for q in qs if len(q["e"]) < 12)

    print("=" * 66)
    print(f"إجمالي الأسئلة: {tot} | موضوعات: {topics}")
    print(f"⭐ الأكثر تكرارًا: {byrank[2]} | 🔁 متكرر: {byrank[1]} | عادي: {byrank[0]}")
    for s, name, _ in B.SECS:
        print(f"  - {name}: {bysec[s]}")
    print(f"تعليلات قصيرة (<12 حرفًا): {noexp}")
    print("-" * 66)
    print("إعادة حساب مستقلة للمفاتيح الرقمية:")
    for k, v in sorted(checked.items()):
        print(f"  ✓ {k}: {v} سؤالًا أُعيد حسابه")
    print("-" * 66)
    html = os.path.join(os.path.dirname(HERE), "azhar-arabic-guide.html")
    if os.path.exists(html):
        le = lint_html(html)
        print(f"فحص الملف المُنتَج (أخطاء المتصفح): "
              f"{'سليم ✓' if not le else str(len(le)) + ' خطأ'}")
        errs += le
    print("-" * 66)
    print(f"أخطاء: {len(errs)} | تنبيهات: {len(warns)}")
    for e in errs[:40]:
        print("  ✗", e)
    for w in warns[:15]:
        print("  ⚠", w)
    print("=" * 66)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
