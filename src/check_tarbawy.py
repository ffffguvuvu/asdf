# -*- coding: utf-8 -*-
"""فحص جودة بنك أسئلة التربوي قبل البناء: تكرار، مفاتيح، بدائل ملتبسة، توازن."""

import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tarbawy"))

import gen          # noqa: E402
import curated      # noqa: E402
from kb_core import G  # noqa: E402


def norm(t):
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        t = t.replace(a, b)
    return " ".join(t.split())


def toks(t):
    t = norm(t).replace("(", " ").replace(")", " ").replace("،", " ")
    return {w[2:] if w.startswith("ال") else w for w in t.split() if len(w) >= 5}


def main():
    problems = []

    # ---------- (١) قاعدة المعرفة: تعريف واحد لكل مفهوم ----------
    by_def = collections.defaultdict(list)
    for g in G:
        for it in g["items"]:
            by_def[norm(it["d"])].append((g["id"], it["n"]))
    for d, owners in by_def.items():
        names = {o[1] for o in owners}
        if len(names) > 1:
            problems.append(f"تعريف مشترك بين مفهومين: {names} ← «{d[:60]}»")

    by_name = collections.defaultdict(set)
    for g in G:
        for it in g["items"]:
            by_name[norm(it["n"])].add(norm(it["d"]))
    multi = [n for n, ds in by_name.items() if len(ds) > 1]

    # ---------- (٢) الأسئلة ----------
    qs = gen.kb_bank() + gen.num_bank() + curated.bank(gen.mk)
    seen = {}
    dups = 0
    for q in qs:
        if len(q["o"]) != 4:
            problems.append(f"بدائل ≠ ٤: {q['q'][:50]}")
        if len(set(q["o"])) != 4:
            problems.append(f"بدائل مكررة: {q['q'][:50]}")
        if not 0 <= q["a"] < 4:
            problems.append(f"مفتاح خاطئ: {q['q'][:50]}")
        if not q["e"].strip():
            problems.append(f"بلا شرح: {q['q'][:50]}")
        key = (norm(q["q"]), tuple(sorted(norm(o) for o in q["o"])))
        if key in seen:
            dups += 1
        seen[key] = 1
        # بدائل مطابقة فعليًا للإجابة بعد التطبيع (احتمال إجابتين صحيحتين)
        a = norm(q["o"][q["a"]]).replace("(", "").replace(")", "")
        for j, o in enumerate(q["o"]):
            if j == q["a"]:
                continue
            b = norm(o).replace("(", "").replace(")", "")
            close = min(len(a), len(b)) >= 8 and ((a in b and len(b) - len(a) <= 3) or
                                                  (b in a and len(a) - len(b) <= 3))
            if a == b or close:
                problems.append(f"بديل مطابق للإجابة: «{o[:45]}» مقابل «{q['o'][q['a']][:45]}»")

    # ---------- (٣) تحقق مستقل من مفاتيح أسئلة النزعة المركزية ----------
    import re
    import statistics
    tr = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    checked = bad = 0
    for q in qs:
        if q["t"] not in ("المتوسط الحسابي", "الوسيط", "المنوال", "المدى") or "درجات" not in q["q"]:
            continue
        nums = [int(x.translate(tr)) for x in re.findall(r"[٠-٩]+", q["q"].split(":")[1].split(".")[0])]
        if len(nums) < 5:
            continue
        key = float(q["o"][q["a"]].replace("٫", ".").translate(tr))
        want = {"المتوسط الحسابي": statistics.mean(nums), "الوسيط": statistics.median(nums),
                "المنوال": statistics.mode(nums), "المدى": max(nums) - min(nums)}[q["t"]]
        checked += 1
        if abs(key - want) > 0.011:
            bad += 1
            problems.append(f"مفتاح حسابي خاطئ ({q['t']}): {nums} ← {key} بدل {want}")
    print(f"تحقق مستقل من {checked} سؤالًا حسابيًا في النزعة المركزية — أخطاء: {bad}")

    print(f"إجمالي الأسئلة المولَّدة: {len(qs)}  (مكررة قبل الحذف: {dups})")
    print("التوزيع على المحاور:", dict(collections.Counter(q["x"] for q in qs)))
    print("توزيع موضع الإجابة:", dict(collections.Counter(q["a"] for q in qs)))
    print("المصادر:", dict(collections.Counter(q["s"] for q in qs)))
    print("أكبر ١٢ موضوعًا:", collections.Counter(q["t"] for q in qs).most_common(12))
    if multi:
        print(f"\nℹ️ مفاهيم تتكرر بتعريفات مختلفة حسب السياق ({len(multi)}): {', '.join(multi[:14])}")

    if problems:
        print(f"\n⚠️ ملاحظات تحتاج مراجعة: {len(problems)}")
        for p in problems[:40]:
            print("  •", p)
    else:
        print("\n✅ لا توجد ملاحظات بنيوية.")
    return len(problems)


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
