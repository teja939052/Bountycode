"""Route parity (Route Triad Rule): every internal frontend link must resolve
to a declared App.tsx route (directly, via <Navigate> redirect, or via a
:param pattern). A link with no route is a dead end — the exact class
removed in the dead-UI purge. Runs in CI forever so it never recurs.
"""
import pathlib
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "frontend" / "src"
APP_TSX = SRC / "App.tsx"


def _read(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_routes(text: str) -> tuple[set, dict]:
    """(route_patterns, redirects). Handles multi-line <Route> blocks and
    <Navigate> redirects (same-line or nested). :param segments kept."""
    patterns = set()
    redirects = {}
    for m in re.finditer(r"<Route\s+path=\"([^\"]+)\"([\s\S]{0,600}?)(/>|>)", text):
        path, chunk = m.group(1), m.group(2)
        nav = re.search(r'<Navigate\s+to="([^"]+)"', chunk)
        # self-closing with element={<Navigate/>} inline also lands in chunk
        if nav:
            redirects[path] = nav.group(1)
        else:
            patterns.add(path)
    return patterns, redirects


def _extract_links(text: str) -> set:
    links = set()
    for pat in (r'to="(/[^"]*)"', r"to=\{'(/[^'}]*)'\}",
                r'navigate\(\s*["\'](/[^"\']*)["\']',
                r'href="(/[^"]*)"'):
        for m in re.finditer(pat, text):
            raw = m.group(1)
            norm = re.sub(r"\$\{[^}]+\}", ":param", raw)
            norm = norm.split("?")[0].split("#")[0]
            if norm.startswith("/"):
                links.add(norm)
    # template literals: to={`/question/${id}`} — capture the whole literal
    for m in re.finditer(r"to=\{`(/[^`]*)`\}", text):
        raw = m.group(1)
        norm = re.sub(r"\$\{[^}]+\}", ":param", raw)
        norm = norm.split("?")[0].split("#")[0]
        if norm.startswith("/"):
            links.add(norm)
    return links


def _matches(link: str, patterns: set, redirects: dict) -> bool:
    # resolve redirect chains first
    seen = set()
    target = link
    while target in redirects and target not in seen:
        seen.add(target)
        target = redirects[target]
    if target in patterns:
        return True
    # a link matching a redirect SOURCE also resolves (redirects render)
    lp = target.strip("/").split("/")
    for pat in list(patterns) + [k for k in redirects.keys() if k not in patterns]:
        if pat in ("*", "/*"):
            continue
        pp = pat.strip("/").split("/")
        if len(pp) != len(lp):
            continue
        if all(a.startswith(":") or a == b for a, b in zip(pp, lp)):
            return True
    return False


def test_route_parity():
    if not APP_TSX.is_file():
        import pytest
        pytest.skip("frontend not checked out")
    text = _read(APP_TSX)
    patterns, redirects = _extract_routes(text)
    assert patterns, "no routes parsed from App.tsx — parser broken"
    dead = []
    for tsx in sorted(SRC.rglob("*.tsx")):
        if "generated" in tsx.parts:
            continue
        if ".backup." in tsx.name or "-backup." in tsx.name:
            continue  # backup snapshots are not bundled or routed
        for link in _extract_links(_read(tsx)):
            if link == "/" or link.startswith("/api/"):
                continue
            if not _matches(link, patterns, redirects):
                dead.append(f"{tsx.relative_to(SRC)} -> {link}")
    assert dead == [], f"Dead internal links (no App route):\n" + "\n".join(sorted(set(dead)))
