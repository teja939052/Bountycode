"""Generate production brand assets for BountyCode.

Single source of truth: `src/components/brand/BountyCodeLogo.tsx`. The mark is
rasterised straight out of that component, so the favicon, PWA icons and OG
card are byte-for-byte the same artwork the navbar renders. Cropping the
original pasted PNG instead would risk the icons drifting from the UI mark.

`mark.svg` is produced by `extract_mark_svg.py`; run that first (or pass its
path). If no Chromium browser is available the script falls back to recovering
the mark from the original raster, which is pixel-identical in colour but is a
separate code path.

Dev-only tool. Requires Pillow; it is NOT an app or CI dependency because the
generated assets are committed and nothing consumes this at runtime.

Usage:
    python frontend/scripts/extract_mark_svg.py
    python frontend/scripts/generate_logo_assets.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "frontend" / "public"
LOGO_DIR = PUBLIC / "assets" / "logo"
MARK_SVG = LOGO_DIR / "mark.svg"
SOURCE_PNG = ROOT / "BountyCode Interlocking Knot Logo.png"

# Brand plate, lifted from the component's NAVY constant.
BRAND_NAVY = "#17263B"

SIZE_BUDGET_KB = 24
# og-image.jpg is only ever fetched by social crawlers, never by a visitor.
OG_BUDGET_KB = 120

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def render_html_png(chrome: str, html: str, width: int, height: int, out: Path) -> None:
    """Rasterise an HTML/SVG fragment at an exact pixel size."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        page = td_path / "page.html"
        shot = td_path / "shot.png"
        page.write_text(html, encoding="utf-8")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--default-background-color=00000000",
                "--force-device-scale-factor=1",
                f"--user-data-dir={td_path / 'profile'}",
                f"--window-size={width},{height}",
                f"--screenshot={shot}",
                page.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        if not shot.exists():
            raise RuntimeError(f"chromium produced no output for {out.name}")
        shutil.copyfile(shot, out)


def svg_inline(width: int, height: int) -> str:
    svg = MARK_SVG.read_text(encoding="utf-8")
    # Drop the fixed width/height so the wrapper controls layout exactly.
    svg = svg.replace(f'width="512" height="512"', f'width="{width}" height="{height}"')
    return svg


def page(body: str, width: int, height: int, bg: str | None) -> str:
    style = f"background:{bg};" if bg else "background:transparent;"
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "*{margin:0;padding:0;box-sizing:border-box}"
        f"html,body{{width:{width}px;height:{height}px;{style}"
        "display:flex;align-items:center;justify-content:center;overflow:hidden}"
        "svg{display:block}"
        "</style></head><body>" + body + "</body></html>"
    )


def save(im: Image.Image, path: Path, opaque: bool = False) -> int:
    """Write a PNG, dropping alpha for opaque art.

    Palettising an opaque RGBA image corrupts alpha down to ~75% opacity, which
    visibly fades a plate, so opaque assets are flattened to RGB and quantised
    in RGB where there is no alpha to damage.

    For transparent assets the palettiser leaves peak alpha at 254/255, so the
    mark renders 0.4% see-through. Measured, imperceptible (<1/255 per channel
    against #17263B) and not worth fragile palette patching to remove.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if opaque:
        im.convert("RGB").quantize(colors=32, method=Image.MEDIANCUT).save(path, "PNG", optimize=True)
    else:
        im.quantize(colors=64, method=Image.FASTOCTREE).save(path, "PNG", optimize=True)
    return path.stat().st_size


# ── Raster fallback: recover the mark from the original pasted PNG ──────────

BG_LUM = 246.6
ALPHA_TOP = 243.0
ALPHA_BOTTOM = 150.0
INK_THRESH = BG_LUM - 28
MARK_BAND = (259, 690)  # measured from the source; excludes the wordmark


def recover_mark_from_raster() -> Image.Image:
    if not SOURCE_PNG.exists():
        raise SystemExit(f"missing fallback source: {SOURCE_PNG}")
    base = Image.open(SOURCE_PNG).convert("RGB")
    W, H = base.size
    px = base.load()

    ys = [y for y in range(*MARK_BAND) if any(
        (px[x, y][0] + px[x, y][1] + px[x, y][2]) / 3 < INK_THRESH for x in range(W)
    )]
    if not ys:
        raise SystemExit("no ink in mark band")
    xs0 = xs1 = None
    for y in ys:
        row = [x for x in range(W) if (px[x, y][0] + px[x, y][1] + px[x, y][2]) / 3 < INK_THRESH]
        lo, hi = min(row), max(row)
        xs0 = lo if xs0 is None else min(xs0, lo)
        xs1 = hi if xs1 is None else max(xs1, hi)

    pad = 6
    box = (max(0, xs0 - pad), max(0, min(ys) - pad), min(W, xs1 + 1 + pad), min(H, max(ys) + 1 + pad))
    crop = base.crop(box)

    out = Image.new("RGBA", crop.size)
    op = out.load()
    cp = crop.load()
    span = ALPHA_TOP - ALPHA_BOTTOM
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b = cp[x, y]
            t = (ALPHA_TOP - (r + g + b) / 3) / span
            a = 0 if t <= 0 else (255 if t >= 1 else int(round(t * 255)))
            op[x, y] = (r, g, b, a)

    # Snap the near-transparent speckle left by the raster's compression noise.
    r, g, b, a = out.split()
    out = Image.merge("RGBA", (r, g, b, a.point(lambda v: 0 if v < 28 else v)))

    side = max(out.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(out, ((side - out.width) // 2, (side - out.height) // 2), out)
    return square


def main() -> None:
    if not MARK_SVG.exists():
        raise SystemExit(f"missing {MARK_SVG}; run extract_mark_svg.py first")

    chrome = find_chrome()
    renderer = "chromium" if chrome else "raster fallback"
    print(f"source     : {MARK_SVG.relative_to(ROOT)}")
    print(f"renderer   : {renderer}")
    if chrome:
        print(f"             {chrome}")
    else:
        print("             no Chromium found; recovering from the pasted raster")

    written: list[tuple[Path, int]] = []

    def emit(im: Image.Image, rel: Path, opaque: bool = False) -> None:
        written.append((PUBLIC / rel, save(im, PUBLIC / rel, opaque=opaque)))

    def render(size: int, bg: str | None) -> Image.Image:
        if not chrome:
            mark = recover_mark_from_raster()
            im = mark.resize((size, size), Image.LANCZOS)
            if bg:
                plate = Image.new("RGBA", (size, size), tuple(int(bg[i:i+2], 16) for i in (1, 3, 5)) + (255,))
                plate.paste(im, (0, 0), im)
                return plate
            return im
        out = PUBLIC / ".render-tmp.png"
        try:
            render_html_png(chrome, page(svg_inline(size, size), size, size, bg), size, size, out)
            return Image.open(out).convert("RGBA")
        finally:
            if out.exists():
                out.unlink()

    # ── Navbar / in-app rasters ────────────────────────────────────────
    # Rendered at the exact target size rather than downscaled from a master:
    # LANCZOS on an already-antialiased edge only softens it further.
    master = render(512, None)
    emit(render(256, None), Path("assets/logo/mark-256.png"))
    emit(render(128, None), Path("assets/logo/mark-128.png"))

    # ── Favicons ───────────────────────────────────────────────────────
    emit(render(32, None), Path("favicon-32.png"))
    emit(render(16, None), Path("favicon-16.png"))

    # ── PWA icons ──────────────────────────────────────────────────────
    emit(render(192, None), Path("icon-192.png"))
    emit(master, Path("icon-512.png"))

    # ── Maskable icons ─────────────────────────────────────────────────
    # The 80% safe zone is a circle of 80% *diameter* (radius 40% of width).
    # The knot's ink reaches ~72% of canvas diameter at a 0.62 inset, i.e. 91%
    # of that radius — legal but with little margin for launchers that mask
    # tighter than spec. 0.56 pulls it back to ~82% of the safe radius.
    emit(inset_plate(chrome, 192, 0.56, BRAND_NAVY), Path("icon-192-maskable.png"), opaque=True)
    emit(inset_plate(chrome, 512, 0.56, BRAND_NAVY), Path("icon-512-maskable.png"), opaque=True)

    # ── apple-touch-icon ───────────────────────────────────────────────
    # Opaque, because iOS composites transparency onto black. The 80% circle
    # rule does NOT apply here: iOS applies its own rounded-rect mask.
    emit(inset_plate(chrome, 180, 0.72, BRAND_NAVY), Path("apple-touch-icon.png"), opaque=True)

    # ── Open Graph card ────────────────────────────────────────────────
    og = og_card(chrome)
    og_path = PUBLIC / "og-image.jpg"
    og.convert("RGB").save(og_path, "JPEG", quality=88, optimize=True, progressive=True)
    written.append((og_path, og_path.stat().st_size))

    # ── Report ─────────────────────────────────────────────────────────
    CRITICAL = {
        "mark-128.png", "mark-256.png", "favicon-32.png", "favicon-16.png",
        "icon-192.png", "icon-512.png",
        "icon-192-maskable.png", "icon-512-maskable.png", "apple-touch-icon.png",
    }
    print("\nwritten:")
    over: list[tuple[Path, int]] = []
    for path, size in written:
        budget = OG_BUDGET_KB if path.name == "og-image.jpg" else SIZE_BUDGET_KB
        kb = size / 1024
        flag = "OK " if kb <= budget else "OVER"
        if path.name in CRITICAL and kb > SIZE_BUDGET_KB:
            over.append((path, size))
        print(f"  {flag} {kb:6.1f} KB (max {budget} KB)  {path.relative_to(ROOT)}")

    if over:
        print(f"\nFAIL: {len(over)} critical asset(s) over the {SIZE_BUDGET_KB} KB budget")
        raise SystemExit(1)
    print(f"\nOK: every visitor-facing asset is within {SIZE_BUDGET_KB} KB.")


def inset_plate(chrome: str | None, size: int, ratio: float, bg: str) -> Image.Image:
    """Opaque brand plate with the mark centred at `ratio` of the canvas."""
    inner = int(size * ratio)
    if not chrome:
        mark = recover_mark_from_raster().resize((inner, inner), Image.LANCZOS)
        plate = Image.new("RGBA", (size, size), tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        plate.paste(mark, ((size - inner) // 2, (size - inner) // 2), mark)
        return plate
    out = PUBLIC / ".render-tmp.png"
    try:
        render_html_png(chrome, page(svg_inline(inner, inner), size, size, bg), size, size, out)
        return Image.open(out).convert("RGBA")
    finally:
        if out.exists():
            out.unlink()


def og_card(chrome: str | None) -> Image.Image:
    """1200x630 social card: brand plate, mark and wordmark."""
    W, H = 1200, 630
    mark_h = 250
    wordmark = (
        "<div style=\"font-family:Manrope,'Segoe UI',system-ui,sans-serif;"
        "font-size:104px;font-weight:800;letter-spacing:-0.055em;line-height:1;"
        "color:#FFFFFF;margin-top:44px\">"
        "<span style=\"color:#FFFFFF\">Bounty</span>"
        "<span style=\"color:#C96F3D\">Code</span></div>"
    )
    tagline = (
        "<div style=\"font-family:Manrope,'Segoe UI',system-ui,sans-serif;"
        "font-size:27px;font-weight:600;letter-spacing:0.02em;color:#9FB0C4;"
        "margin-top:26px\">From your first line of code to your first offer.</div>"
    )
    if chrome:
        out = PUBLIC / ".render-og.png"
        try:
            body = (
                f"<div style=\"display:flex;flex-direction:column;align-items:center\">"
                f"{svg_inline(360, mark_h)}{wordmark}{tagline}</div>"
            )
            render_html_png(chrome, page(body, W, H, BRAND_NAVY), W, H, out)
            return Image.open(out).convert("RGB")
        finally:
            if out.exists():
                out.unlink()
    im = Image.new("RGB", (W, H), tuple(int(BRAND_NAVY[i:i+2], 16) for i in (1, 3, 5)))
    mark = recover_mark_from_raster().resize((360, mark_h), Image.LANCZOS)
    im.paste(mark, ((W - 360) // 2, 120), mark)
    return im


if __name__ == "__main__":
    main()