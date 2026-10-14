from pathlib import Path

p = Path(r'D:\Project-Fremen\backend\app\services\journey_engine.py')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()

# Insert after line 172 (0-indexed: 171)
insert_after = 172
new_lines = [
    '',
    '',
    'def _build_mentor_state(',
    '    *,',
    '    level: int,',
    '    streak: int,',
    '    interview_readiness: float,',
    '    oa_readiness: float,',
    '    winner_category: str,',
    '    srs_due_count: int,',
    '    failed_repairs: int,',
    '    prerequisite_blocked: bool,',
    '    completed_count: int,',
    '    target_company: str,',
    ') -> Dict[str, Any]:',
    '    """Derive Captain Byte\'s mood and message from actual journey state."""',
    '    if completed_count == 0 and level <= 1:',
    '        mood = "welcome"',
    '        message = "Welcome aboard. Pick your first mission below — no experience needed."',
    '        phase = "onboarding"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if prerequisite_blocked:',
    '        mood = "stuck"',
    '        message = "Progress is blocked by an incomplete prerequisite. Complete the current mission to unlock what comes next."',
    '        phase = "repair"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if failed_repairs > 0:',
    '        mood = "correcting"',
    '        message = f"You have {failed_repairs} concept{\'s\' if failed_repairs > 1 else \'\'} that need reinforcement. Repair those first — they compound fast."',
    '        phase = "repair"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if winner_category == "mock_prep" or interview_readiness < 70 or oa_readiness < 70:',
    '        mood = "serious"',
    '        message = "Mock readiness is below target. Treat the next mock like the real thing — format, pressure, and all."',
    '        phase = "assessment"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if winner_category in {"srs_overdue", "challenge"}:',
    '        mood = "thinking"',
    '        message = "This next task sharpens recall under pressure. Focus on one question at a time."',
    '        phase = "practice"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if winner_category == "failed_repair":',
    '        mood = "correcting"',
    '        message = "A concept you learned earlier is still shaky. Strengthen it now so it holds under pressure later."',
    '        phase = "repair"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if winner_category in {"current_lesson", "prerequisite", "role_practice"}:',
    '        mood = "explaining"',
    '        message = "We\'re building something real here. This step connects directly to the next mission — trust the sequence."',
    '        phase = "learning"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if winner_category == "explore":',
    '        mood = "briefing"',
    '        message = "You\'re clear to explore. Pick one direction and go deep — shallow browsing won\'t build lasting skill."',
    '        phase = "exploration"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if interview_readiness >= 85 and oa_readiness >= 85:',
    '        mood = "proud"',
    '        message = "Your readiness signals are strong. One more focused pass and you\'ll be interview-ready."',
    '        phase = "readiness"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    if streak >= 7:',
    '        mood = "celebrating"',
    '        message = f"A {streak}-day streak is excellent momentum. Keep the session short if you need to — consistency wins."',
    '        phase = "celebration"',
    '        return {"mood": mood, "message": message, "phase": phase}',
    '',
    '    mood = "briefing"',
    '    message = "Here\'s your best next move. Complete it, then come back for the next one."',
    '    phase = "briefing"',
    '    return {"mood": mood, "message": message, "phase": phase}',
    '',
    '',
]

# Verify we're inserting at the right place
if lines[insert_after - 1].strip() != 'return []':
    print(f'Unexpected anchor line: {repr(lines[insert_after - 1])}')
    raise SystemExit(1)

new_lines_str = '\n'.join(new_lines)
lines.insert(insert_after, new_lines_str)
# But insert() adds as one element, we need to split
lines = lines[:insert_after] + new_lines + lines[insert_after:]

p.write_text('\n'.join(lines), encoding='utf-8')
print('OK')
