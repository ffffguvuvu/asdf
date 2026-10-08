# -*- coding: utf-8 -*-
"""يرسم كل الأشكال إلى PNG ويتحقق ألا يلامس أي رسم حدود الإطار (علامة قص/خروج عن viewBox)."""
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402
from svg2png import Svg2Png  # noqa: E402
import content_a, content_b, content_c, content_d, content_e  # noqa: E402

CHAPTERS = content_a.CH + content_b.CH + content_c.CH + content_d.CH + content_e.CH
PAD = 12
RING = 7  # عدد البكسلات المفحوصة من كل حد


def main():
    r = Svg2Png(scale=2.0)
    figs = {}
    os.makedirs(os.path.join("assets", "figs"), exist_ok=True)
    for ch in CHAPTERS:
        for q in ch["qs"]:
            figs[q["id"]] = r.render(q["fig"], os.path.join("assets", "figs", q["id"] + ".png"), pad=PAD)
    bad = []
    for qid, (path, W, H) in figs.items():
        im = Image.open(path).convert("L")
        px = im.load()
        hit = False
        for x in range(W):
            for y in list(range(RING)) + list(range(H - RING, H)):
                if px[x, y] < 245:
                    hit = True
                    break
            if hit:
                break
        if not hit:
            for y in range(H):
                for x in list(range(RING)) + list(range(W - RING, W)):
                    if px[x, y] < 245:
                        hit = True
                        break
                if hit:
                    break
        if hit:
            bad.append(qid)
    print("figures: %d   clipped: %d" % (len(figs), len(bad)))
    if bad:
        print("  " + ", ".join(sorted(bad)))
    return len(bad)


if __name__ == "__main__":
    sys.exit(main())
