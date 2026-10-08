# -*- coding: utf-8 -*-
"""تجميع بنوك التدريب المولَّدة وربط كل بنك بمحوره."""

from gen_num import number_bank, letter_bank
from gen_misc import numshape_bank, balance_bank, verbal_bank, logic_bank
from gen_shapes import (seq_bank, matrix_bank, rotate_bank, fold_bank, cube_bank,
                        spatial_bank, merge_bank, count_bank, odd_bank, faces_bank,
                        complete_bank, xyz_bank)

_rot = rotate_bank()
_mirror = [q for q in _rot if "مرآة" in q["prompt"] or "صورة الشكل" in q["prompt"]]
_same = [q for q in _rot if q not in _mirror]

DRILLS = {
    "seq": seq_bank(),
    "complete": complete_bank(),
    "matrix": matrix_bank(),
    "same": _same,
    "mirror": _mirror,
    "fold": fold_bank(),
    "cube": cube_bank(),
    "spatial": spatial_bank(),
    "xyz": xyz_bank(),
    "merge": merge_bank(),
    "count": count_bank(),
    "odd": odd_bank(),
    "numseq": number_bank(),
    "letters": letter_bank(),
    "numshape": numshape_bank(),
    "balance": balance_bank(),
    "verbal": verbal_bank(),
    "faces": faces_bank(),
    "logic": logic_bank(),
}


def attach(chapters):
    """يضيف بنك التدريب لكل محور ويحذف المكرّر داخل البنك."""
    for ch in chapters:
        bank = DRILLS.get(ch["id"], [])
        seen, clean = set(), []
        for q in bank:
            opts = [str(o) for o in q["options"]]
            if len(set(opts)) != len(opts):      # اختياران متطابقان ⇐ سؤال غير صالح
                continue
            key = (q["prompt"], tuple(opts))
            if key in seen:
                continue
            seen.add(key)
            clean.append(q)
        ch["drill"] = clean
    return chapters


def count():
    return sum(len(v) for v in DRILLS.values())
