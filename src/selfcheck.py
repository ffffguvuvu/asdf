#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""فحص ذاتي لبنك الأسئلة قبل البناء: سلامة البيانات ومنطق الأشكال."""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import _rot_vox                      # noqa: E402
from content_a import CHAPTERS_A                 # noqa: E402
from content_b import (CHAPTERS_B, SCREW, SCREW_M, OPPOSITE, NET1_OPPOSITES,
                       Q1_VIEWS, Q2_VIEWS, Q4_NETS, Q4_STEM_VIEW,
                       Q5_VIEWS, Q5_STEM_VIEW)   # noqa: E402
from content_c import CHAPTERS_C                 # noqa: E402

from model import balance_answers, AR_LABELS     # noqa: E402

ALL_CHAPTERS = balance_answers(CHAPTERS_A + CHAPTERS_B + CHAPTERS_C)
from extras import EXAM, QUICKTABLE, TIPS, PLAN, SOURCES  # noqa: E402

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ---------- 1) سلامة كل سؤال ----------
total = 0
for ci, ch in enumerate(ALL_CHAPTERS, 1):
    for qi, q in enumerate(ch["questions"], 1):
        total += 1
        tag = f"محور {ci} ({ch['title']}) — سؤال {qi}"
        opts = q["options"]
        if len(opts) != 4:
            err(f"{tag}: عدد الاختيارات {len(opts)} بدل 4")
        if not isinstance(q["answer"], int) or not (0 <= q["answer"] < len(opts)):
            err(f"{tag}: رقم الإجابة خارج النطاق ({q['answer']})")
        if len(q.get("steps", [])) < 2:
            err(f"{tag}: الخطوات أقل من سطرين")
        if not q.get("stem") and len(q["prompt"]) < 20:
            err(f"{tag}: سؤال بلا معطى ولا نص كافٍ")
        if len(set(map(str, opts))) != len(opts):
            err(f"{tag}: يوجد اختياران متطابقان")
        for s in q.get("steps", []):
            if "؟ لا" in s or "لنجرّب" in s:
                warn(f"{tag}: خطوة فيها تجريب مرتبك: {s[:40]}…")
        letter = AR_LABELS[q["answer"]]
        for txt in list(q.get("steps", [])) + [q.get("tip") or "", q.get("answer_text") or ""]:
            for m in re.finditer(r"(?:الإجابة|الصحيحة|الشاذ هو|الناتج هو|الصواب)\s*(?:هو\s*)?\(([أبجد])\)", txt):
                if m.group(1) != letter:
                    err(f"{tag}: الشرح يشير إلى ({m.group(1)}) والإجابة ({letter})")
        if q.get("okind") == "text":
            for o in opts:
                if "<svg" in str(o):
                    err(f"{tag}: اختيار نصي يحوي رسمة")

# ---------- 2) منطق المكعبات ----------
if sorted(sum(([a, b] for a, b in OPPOSITE), [])) != [0, 1, 2, 3, 4, 5]:
    err("جدول المتقابلات لا يغطي الوجوه الستة مرة واحدة")


def possible(view, opposites):
    """هل يمكن أن تظهر هذه الوجوه الثلاثة معًا؟ (لا يوجد بينها زوج متقابل ولا تكرار)"""
    if len(set(view)) != 3:
        return False
    return not any(frozenset(p) in opposites for p in
                   ((view[0], view[1]), (view[0], view[2]), (view[1], view[2])))


def opposites_of(net):
    return {frozenset((net[a], net[b])) for a, b in OPPOSITE}


# س١: المكعب الوحيد الممكن من الشبكة
ok1 = [i for i, v in enumerate(Q1_VIEWS) if possible(v, NET1_OPPOSITES)]
if ok1 != [1]:
    err(f"محور المكعبات س١: المكعبات الممكنة {ok1} والمفروض [1] فقط")
# س٢: المكعب الوحيد المستحيل
bad2 = [i for i, v in enumerate(Q2_VIEWS) if not possible(v, NET1_OPPOSITES)]
if bad2 != [3]:
    err(f"محور المكعبات س٢: المستحيل {bad2} والمفروض [3] فقط")
# س٤: الشبكة الوحيدة التي تسمح بالصورة
ok4 = [i for i, n in enumerate(Q4_NETS) if possible(Q4_STEM_VIEW, opposites_of(n))]
if ok4 != [0]:
    err(f"محور المكعبات س٤: الشبكات الممكنة {ok4} والمفروض [0] فقط")
for i, n in enumerate(Q4_NETS):
    if sorted(n.values()) != sorted(["circle", "square", "star", "tri", "plus", "diamond"]):
        err(f"محور المكعبات س٤: الشبكة {i} لا تحوي الرموز الستة مرة واحدة")
# س٥: التطابق بالدوران = نفس الترتيب الدوري للوجوه الثلاثة
def cyc(t):
    return {(t[0], t[1], t[2]), (t[1], t[2], t[0]), (t[2], t[0], t[1])}
same5 = [i for i, v in enumerate(Q5_VIEWS) if tuple(v) in cyc(Q5_STEM_VIEW)]
if same5 != [0]:
    err(f"محور المكعبات س٥: المطابق بالدوران {same5} والمفروض [0] فقط")


def norm(vs):
    mx, my, mz = (min(v[i] for v in vs) for i in range(3))
    return tuple(sorted((x - mx, y - my, z - mz) for x, y, z in vs))


def all_rotations(vs):
    return {norm([_rot_vox(v, rx, ry, rz) for v in vs])
            for rx in range(4) for ry in range(4) for rz in range(4)}

# ---------- 3) انعكاس المجسم (محور التصور المكاني) ----------
rots = all_rotations(SCREW)
if norm(SCREW_M) in rots:
    err("مجسم اللولب غير متباين مع صورته في المرآة ⇐ السؤال بلا إجابة وحيدة")
if norm([_rot_vox(v, 0, 0, 1) for v in SCREW]) not in rots:
    err("الخيار الصحيح في سؤال المجسم ليس دورانًا للأصل")

# ---------- 4) الملاحق ----------
for i, (qq, opts, ai, why) in enumerate(EXAM, 1):
    if len(opts) != 4:
        err(f"الاختبار الشامل — سؤال {i}: عدد الاختيارات {len(opts)}")
    if not (0 <= ai < len(opts)):
        err(f"الاختبار الشامل — سؤال {i}: رقم الإجابة خارج النطاق")
    if len(why) < 10:
        err(f"الاختبار الشامل — سؤال {i}: شرح قصير جدًا")
for t, u in SOURCES:
    if not u.startswith("https://"):
        err(f"رابط غير صالح: {t}")

print(f"الأسئلة المفحوصة: {total} في {len(ALL_CHAPTERS)} محورًا "
      f"+ {len(EXAM)} سؤال اختبار + {len(QUICKTABLE)} صفًا في الجدول السريع "
      f"+ {len(TIPS)} نصيحة + {len(PLAN)} أيام + {len(SOURCES)} مصدرًا")
for w in warnings:
    print("⚠️ ", w)
if errors:
    for e in errors:
        print("❌", e)
    sys.exit(1)
print("✅ كل الفحوص سليمة")
