"""Extract the brand mark paths out of BountyCodeLogo.tsx into a standalone SVG.

The React component is the single source of truth for the mark. Rasterising it
directly (rather than cropping the original PNG) guarantees the favicon, PWA
icons and OG card are the same artwork the app renders in the navbar.

Usage: python frontend/scripts/extract_mark_svg.py [out.svg]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "frontend" / "src" / "components" / "brand" / "BountyCodeLogo.tsx"

# Mirrors NAVY / ORANGE in the component.
FILLS = {"navy": "#17263B", "orange": "#C96F3D"}
VIEWBOX = "120 35 600 560"


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing component: {SRC}")
    text = SRC.read_text(encoding="utf-8")

    vb = re.search(r'viewBox="([^"]+)"', text)
    if not vb:
        raise SystemExit("could not find viewBox in component")
    viewbox = vb.group(1)

    paths = re.findall(r'<path d="([^"]+)" fill=\{(navy|orange)\} />', text)
    if len(paths) != 3:
        raise SystemExit(f"expected 3 brand paths, found {len(paths)}")

    body = "".join(f'<path d="{d}" fill="{FILLS[f]}" />' for d, f in paths)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
        f'width="512" height="512" fill="none">{body}</svg>'
    )

    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "frontend" / "public" / "assets" / "logo" / "mark.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")

    print(f"component  : {SRC.relative_to(ROOT)}")
    print(f"viewBox    : {viewbox}")
    print(f"paths      : {len(paths)}")
    for _, f in paths:
        print(f"  fill {FILLS[f]}")
    print(f"wrote      : {out.relative_to(ROOT)}  ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()