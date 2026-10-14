"""Structural analysis of the pasted logo PNG.

Read-only: reports geometry, palette and whether the raster is a mark-only
lockup or a mark + wordmark. Run before generating any asset.
"""

import sys
from collections import Counter

from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "BountyCode Interlocking Knot Logo.png"

im = Image.open(SRC).convert("RGB")
W, H = im.size
print(f"file        : {SRC}")
print(f"size        : {W} x {H}")
print(f"aspect      : {W / H:.4f}")

# The background is a light warm cream with compression noise, so an exact
# match on one RGB triple is unreliable. Use luminance distance instead.
px = im.load()
corner = (
    sum(px[0, 0]) / 3,
    sum(px[W - 1, 0]) / 3,
    sum(px[0, H - 1]) / 3,
    sum(px[W - 1, H - 1]) / 3,
)
bg_lum = sum(corner) / 4
print(f"bg luminance: {bg_lum:.1f} (corners {corner})")

# Threshold: anything clearly darker than the cream field is ink.
THRESH = bg_lum - 28
ink = [[0] * W for _ in range(H)]
rows_with_ink = []
for y in range(H):
    row = ink[y]
    n = 0
    for x in range(W):
        r, g, b = px[x, y]
        if (r + g + b) / 3 < THRESH:
            row[x] = 1
            n += 1
    if n:
        rows_with_ink.append((y, n))

print(f"ink thresh  : lum < {THRESH:.0f}")

if not rows_with_ink:
    print("RESULT      : no ink detected below threshold")
    sys.exit(0)

top = rows_with_ink[0][0]
bottom = rows_with_ink[-1][0]
left = min(x for y in range(H) for x in range(W) if ink[y][x])
right = max(x for y in range(H) for x in range(W) if ink[y][x])
print(f"ink bbox    : x {left}..{right}  y {top}..{bottom}")
print(f"ink box size: {right - left + 1} x {bottom - top + 1}")
print(f"margins     : L{left} R{W - 1 - right} T{top} B{H - 1 - bottom}")

# Row profile: a mark + wordmark shows up as one dense band followed by a
# second, much shorter band separated by a gap of empty rows.
print("\nrow profile (every 1% of height, ink px count):")
step = max(1, H // 100)
for y in range(0, H, step):
    n = sum(ink[y])
    bar = "#" * min(60, n // 40)
    print(f"  y={y:4d} {n:5d} {bar}")

# Find contiguous vertical bands of ink.
bands = []
cur_start = None
for y in range(H):
    n = sum(ink[y])
    if n and cur_start is None:
        cur_start = y
    elif not n and cur_start is not None:
        bands.append((cur_start, y - 1))
        cur_start = None
if cur_start is not None:
    bands.append((cur_start, H - 1))

bands = [b for b in bands if b[1] - b[0] >= 2]
print(f"\nink bands   : {len(bands)} (>=3px tall)")
for i, (a, b) in enumerate(bands):
    width_ink = max(sum(ink[y]) for y in range(a, b + 1))
    xs = [x for y in range(a, b + 1) for x in range(W) if ink[y][x]]
    print(
        f"  band {i}: y {a}..{b} (h={b - a + 1}) "
        f"x {min(xs)}..{max(xs)} (w={max(xs) - min(xs) + 1}) maxrow={width_ink}"
    )
if len(bands) >= 2:
    print("\nVERDICT     : multiple bands -> likely mark + text/wordmark lockup")
elif len(bands) == 1:
    print("\nVERDICT     : single band -> likely mark only")
else:
    print("\nVERDICT     : inconclusive")

# Palette of the ink itself, so the generated assets can be colour-matched.
ink_colors = Counter()
for y in range(H):
    for x in range(W):
        if ink[y][x]:
            ink_colors[px[x, y]] += 1
print(f"\nink colors  : {len(ink_colors)} distinct")
for c, n in ink_colors.most_common(12):
    r, g, b = c
    print(f"  #{r:02X}{g:02X}{b:02X}  {n:>7}  lum {(r + g + b) / 3:.0f}")