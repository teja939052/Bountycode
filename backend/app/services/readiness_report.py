import io
from datetime import datetime, timezone
import fitz


def _wrap(text: str, max_chars: int = 90) -> list:
    if len(text) <= max_chars:
        return [text]
    lines = []
    while text:
        if len(text) <= max_chars:
            lines.append(text)
            break
        break_at = text.rfind(" ", 0, max_chars)
        if break_at == -1:
            break_at = max_chars
        lines.append(text[:break_at])
        text = text[break_at:].lstrip()
    return lines


async def generate_readiness_pdf(user_name: str, user_email: str, readiness: dict, company: str | None = None) -> bytes:
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    y = 40

    page.insert_text((40, y), "Placement Readiness Report", fontsize=22, fontname="helv", color=(0.1, 0.1, 0.1))
    y += 28
    page.insert_text((40, y), f"Generated: {datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M UTC')}", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    y += 16
    page.insert_text((40, y), f"User: {user_name or 'N/A'}  ·  {user_email or 'N/A'}", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    if company:
        y += 14
        page.insert_text((40, y), f"Target: {company.title()}", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    y += 24

    overall = readiness.get("overall_readiness", readiness.get("overall", 0))
    level = readiness.get("readiness_level", "")

    page.draw_rect(fitz.Rect(40, y, 200, y + 12), fill=(0.93, 0.93, 0.93), color=(0,))
    pct = min(100.0, max(0.0, float(overall)))
    bar_w = int(160 * pct / 100)
    color = (0.48, 0.72, 0.36) if pct >= 75 else (0.85, 0.62, 0.04) if pct >= 55 else (0.93, 0.27, 0.27)
    page.draw_rect(fitz.Rect(40, y, 40 + bar_w, y + 12), fill=color, color=(0,))
    page.insert_text((40, y + 18), f"Overall Readiness: {int(pct)}%  ({level})", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
    y += 44

    cats = readiness.get("categories", {})
    if cats:
        page.insert_text((40, y), "Category Breakdown", fontsize=13, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 14
        for name, info in cats.items():
            score = float(info.get("score", info) if isinstance(info, dict) else info)
            bar_w = int(min(160, max(4, score * 1.6)))
            page.insert_text((40, y), name.replace("_", " ").title(), fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            page.draw_rect(fitz.Rect(180, y - 7, 180 + 160, y + 1), fill=(0.93, 0.93, 0.93), color=(0,))
            color = (0.48, 0.72, 0.36) if score >= 75 else (0.85, 0.62, 0.04) if score >= 55 else (0.93, 0.27, 0.27)
            page.draw_rect(fitz.Rect(180, y - 7, 180 + bar_w, y + 1), fill=color, color=(0,))
            page.insert_text((345, y - 7), f"{int(score)}%", fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1))
            y += 14
        y += 6

    company_specific = readiness.get("company_specific")
    if company_specific:
        y += 2
        page.insert_text((40, y), "Company Match", fontsize=13, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 14
        cs_score = company_specific.get("score")
        if cs_score is not None:
            page.insert_text((40, y), f"Company Score: {int(cs_score)}%", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 12
        match = company_specific.get("match") or {}
        gaps = match.get("gaps") or []
        if gaps:
            page.insert_text((40, y), "Gaps", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 12
            for g in gaps[:8]:
                txt = f"- {g.get('area', '')}: current {g.get('current', '?')}, required {g.get('required', '?')}"
                for line in _wrap(txt, 90):
                    if y > 740:
                        page = doc.new_page(width=612, height=792)
                        y = 40
                    page.insert_text((50, y), line, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                    y += 12
        strengths = match.get("strengths") or []
        if strengths:
            y += 6
            page.insert_text((40, y), "Strengths", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 12
            for s in strengths[:8]:
                txt = f"- {s.get('area', '')}: {s.get('current', '?')}"
                for line in _wrap(txt, 90):
                    if y > 740:
                        page = doc.new_page(width=612, height=792)
                        y = 40
                    page.insert_text((50, y), line, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                    y += 12
        y += 6

    weak = readiness.get("weak_areas") or readiness.get("gaps") or []
    if weak:
        y += 2
        page.insert_text((40, y), "Weak Areas", fontsize=13, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 14
        for w in weak[:10]:
            label = w.get("category", w) if isinstance(w, dict) else w
            score = w.get("score") if isinstance(w, dict) else None
            txt = f"- {label}" + (f" ({int(score)}%)" if score is not None else "")
            for line in _wrap(txt, 90):
                if y > 740:
                    page = doc.new_page(width=612, height=792)
                    y = 40
                page.insert_text((50, y), line, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                y += 12
        y += 6

    recs = readiness.get("recommendations") or []
    if recs:
        y += 2
        page.insert_text((40, y), "Recommendations", fontsize=13, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 14
        for r in recs[:10]:
            msg = r.get("message", r) if isinstance(r, dict) else str(r)
            txt = f"- [{r.get('priority', '?').upper()}] {msg}" if isinstance(r, dict) else f"- {msg}"
            for line in _wrap(txt, 90):
                if y > 740:
                    page = doc.new_page(width=612, height=792)
                    y = 40
                page.insert_text((50, y), line, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                y += 12

    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    buffer.seek(0)
    return buffer.read()
