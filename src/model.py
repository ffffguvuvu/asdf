# -*- coding: utf-8 -*-
"""نماذج البيانات المشتركة لبناء دليل أسئلة الذكاء."""

AR_LABELS = ["أ", "ب", "ج", "د", "هـ"]


def Q(prompt, options, answer, steps, stem=None, tip=None, okind="fig",
      stem_note=None, answer_text=None, hint=None):
    """
    سؤال واحد.
      prompt     : نص السؤال.
      stem       : قائمة خلايا الشكل (SVG) أو None للأسئلة النصية.
      options    : قائمة الاختيارات (SVG إذا okind='fig'، أو نص إذا okind='text').
      answer     : رقم الاختيار الصحيح (يبدأ من 0).
      steps      : خطوات الحل (قائمة نصوص).
      tip        : تنبيه / فخ شائع.
      stem_note  : تعليق صغير أسفل الشكل.
      answer_text: نص يوضَع بجانب حرف الإجابة.
    """
    return dict(prompt=prompt, stem=stem, options=options, answer=answer,
                steps=steps, tip=tip, okind=okind, stem_note=stem_note,
                answer_text=answer_text, hint=hint)


def Chapter(cid, num, title, subtitle, icon, color, color2, idea, how, traps,
            questions, source=None):
    """
    محور كامل.
      idea  : فكرة السؤال (نص).
      how   : خطوات الحل (قائمة).
      traps : أخطاء شائعة (قائمة).
      source: اسم/رابط الفيديو المرجعي من القناة.
    """
    return dict(id=cid, num=num, title=title, subtitle=subtitle, icon=icon,
                color=color, color2=color2, idea=idea, how=how, traps=traps,
                questions=questions, source=source or [])


def reorder(q, perm):
    """
    إعادة ترتيب اختيارات سؤال (perm = ترتيب الفهارس القديمة) مع:
      • تصحيح رقم الإجابة،
      • وإعادة تسمية كل إشارة إلى حرف اختيار داخل الخطوات والتنبيه.
    تُستعمل لتوزيع الإجابات الصحيحة على الحروف الأربعة بدل تكرار حرف واحد.
    """
    assert sorted(perm) == list(range(len(q["options"]))), "ترتيب غير صالح"
    old_to_new = {old: new for new, old in enumerate(perm)}
    q["options"] = [q["options"][i] for i in perm]
    q["answer"] = old_to_new[q["answer"]]

    def remap(txt):
        if not txt:
            return txt
        for old, new in old_to_new.items():
            txt = txt.replace(f"({AR_LABELS[old]})", f"\0{new}\0")
        for new in range(len(perm)):
            txt = txt.replace(f"\0{new}\0", f"({AR_LABELS[new]})")
        return txt

    q["steps"] = [remap(s) for s in q["steps"]]
    q["tip"] = remap(q.get("tip"))
    q["answer_text"] = remap(q.get("answer_text"))
    return q


def balance_answers(chapters):
    """
    يوزّع مواضع الإجابات الصحيحة على الحروف الأربعة داخل كل محور،
    بتدوير ترتيب الاختيارات تدويرًا ثابتًا (نفس الناتج في كل بناء).
    السبب: بلا ذلك تتكرّر إجابة واحدة (مثلًا «ج») في محور كامل فيفقد التدريب قيمته.
    """
    for ch in chapters:
        counts = [0, 0, 0, 0]
        for q in ch["questions"]:
            n = len(q["options"])
            if n != 4 or q.get("fixed_order"):
                counts[q["answer"]] += 1
                continue
            target = min(range(4), key=lambda k: (counts[k], k))   # أقل حرف استُعمل
            shift = (target - q["answer"]) % 4
            if shift:
                perm = [(i - shift) % 4 for i in range(4)]         # تدوير دائري
                reorder(q, perm)
            counts[q["answer"]] += 1
    return chapters
