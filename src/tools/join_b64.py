"""يجمع قطع base64 لصورة صفحة، ويكشف الحرف الشارد ويصلحه.
المعيار: صفحة ممسوحة بيضاء في معظمها، والضجيج ليس كذلك."""
import base64, io, sys, glob
from PIL import Image

def score(b):
    try:
        im = Image.open(io.BytesIO(b)); g = im.convert('L'); s = g.tobytes()[::17]
        return sum(1 for v in s if v > 200) / max(1, len(s)), im.size
    except Exception:
        return -1.0, None

def main(pattern, out):
    parts = sorted(glob.glob(pattern))
    full = ''.join(open(p).read().strip() for p in parts)
    print("parts", len(parts), "chars", len(full), "mod4", len(full) % 4)
    try:
        b = base64.b64decode(full); w, sz = score(b)
    except Exception:
        w, sz, b = -1.0, None, None
    if w > 0.55:
        open(out, 'wb').write(b); print("CLEAN white=%.3f %s %dB" % (w, sz, len(b))); return 0
    print("damaged (white=%.3f) — searching a single stray character…" % w)
    best = (-1.0, None, None)
    for i in range(len(full)):
        c = full[:i] + full[i+1:]
        if len(c) % 4: continue
        try: bb = base64.b64decode(c)
        except Exception: continue
        ww, _ = score(bb)
        if ww > best[0]: best = (ww, i, bb)
        if ww > 0.70:
            open(out, 'wb').write(bb); print("FIXED at %d (%r) white=%.3f" % (i, full[i], ww)); return 0
    ww, i, bb = best
    if bb is not None and ww > 0.55:
        open(out, 'wb').write(bb); print("best at %d white=%.3f" % (i, ww)); return 0
    print("NO FIX (best white=%.3f) — refetch" % ww); return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
