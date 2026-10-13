"""Pattern Pack — Directions."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "directions",
    "name": "Directions",
    "emoji": "🧭",
    "round_id": "aptitude",
    "purpose": "Track displacement from a sequence of turns, handle clock-wise and anti-clockwise angles, and solve shortest-path and shadow problems.",
    "prerequisites": ["basic-geometry", "angles", "time-work"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Left/right reversal",
            "description": "Reverses left and right when facing a non-default direction.",
        },
        {
            "id": "M2",
            "label": "Clockwise angle sign",
            "description": "Treats clockwise as negative in displacement calculation.",
        },
        {
            "id": "M3",
            "label": "Displacement vs distance",
            "description": "Confuses total distance walked with straight-line displacement.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Compass rose",
            "captain_message": "See the four cardinal points. Each turn moves you to a new direction.",
            "render": {
                "kind": "compass",
                "start": "north",
                "turns": ["right", "right"],
                "show_final": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the turns",
            "captain_message": "Add or remove turns. Watch displacement change.",
            "render": {
                "kind": "path_builder",
                "start": [0, 0],
                "directions": ["north", "east", "south", "east"],
                "highlight_diagonal": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict final direction",
            "captain_message": "Don't trace. Choose final facing direction.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Facing East. Turn right, then left, then 180°. Final direction?",
                "options": ["North", "South", "East", "West"],
                "answer_index": 2,
                "explanation": "East → right = South → left = East → 180° = West.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the displacement formula",
            "captain_message": "Write net east-west and north-south steps.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Net horizontal",
                        "placeholder": "Σ(steps east) - Σ(steps west)",
                        "answer": "Σ(steps east) - Σ(steps west)",
                    },
                    {
                        "label": "Net vertical",
                        "placeholder": "Σ(steps north) - Σ(steps south)",
                        "answer": "Σ(steps north) - Σ(steps south)",
                    },
                    {
                        "label": "Displacement",
                        "placeholder": "sqrt(east_west^2 + north_south^2)",
                        "answer": "sqrt(east_west^2 + north_south^2)",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the shadow rule",
            "captain_message": "Sun rises in East. Shadow points West at sunrise.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "At 7 AM, a person's shadow points West. Which direction is he facing?",
                "options": ["North", "South", "East", "West"],
                "answer_index": 1,
                "explanation": "Shadow opposite sun. At sunrise sun is East, shadow West. If shadow is West, person faces South.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix clockwise angle",
            "captain_message": "Clockwise from North to East is 90°. Track cumulative angle.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Clockwise angle",
                        "placeholder": "positive in standard math",
                        "answer": "positive",
                    },
                    {
                        "label": "Anti-clockwise angle",
                        "placeholder": "negative in standard math",
                        "answer": "negative",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to shortest path",
            "captain_message": "For shortest distance on a grid, use Pythagoras.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Walk 3 km East, then 4 km North. Shortest return to start?",
                "options": ["5 km", "7 km", "6 km", "8 km"],
                "answer_index": 0,
                "explanation": "Displacement = sqrt(3^2 + 4^2) = 5 km.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For left/right turns: turn right = 90° clockwise, turn left = 90° anti-clockwise.",
            "render": {
                "kind": "recall",
                "prompt": "Left turn from South faces?",
                "answer": "East",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Facing North. Turn right. Now facing?",
                "answer": "East",
                "explanation": "Right from North = East.",
            },
            {
                "id": "w2",
                "question": "Walk 5 km East, then 5 km West. Net displacement?",
                "answer": "0 km",
                "explanation": "Equal and opposite directions cancel.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Facing South. Turn left, then right, then about turn. Final direction?",
                "options": ["North", "South", "East", "West"],
                "answer": "East",
                "explanation": "South → left = East → right = South → about = North.",
            },
            {
                "id": "d2",
                "question": "A person walks 6 km North, turns right and walks 8 km. Shortest distance from start?",
                "options": ["10", "12", "14", "8"],
                "answer": "10",
                "explanation": "sqrt(6^2 + 8^2) = 10 km.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Facing East, turn 135° clockwise. Now facing?",
                "options": ["South-East", "South-West", "North-West", "North-East"],
                "answer": "South-East",
                "explanation": "East → 90° = South → 45° = South-East.",
            },
            {
                "id": "s2",
                "question": "A man faces West, walks 100 m, turns left, walks 100 m, turns left, walks 100 m. Distance from start?",
                "options": ["100√2", "200", "100", "0"],
                "answer": "100√2",
                "explanation": "Final position is South-West of start. Displacement = 100√2.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "At 9 AM, sun in East. Shadow of pole points?",
                "options": ["West", "East", "North", "South"],
                "answer": "West",
                "explanation": "Shadow opposite sun. Sun in East → shadow West.",
            },
            {
                "id": "wr2",
                "question": "Facing North-West. Turn 180°. Now facing?",
                "options": ["North-East", "South-East", "South-West", "West"],
                "answer": "South-East",
                "explanation": "Opposite of North-West is South-East.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "A man walks 10 km South, turns right 5 km, turns left 10 km. Distance from start?",
            "options": ["15.81", "20", "25", "18"],
            "answer": "15.81",
            "explanation": "Net South = 10, East = 5. Displacement = sqrt(10^2 + 5^2) = sqrt(125) ≈ 11.18.",
        },
        {
            "id": "a2",
            "question": "Facing West, turn 270° anti-clockwise. Now facing?",
            "answer": "South",
            "explanation": "West → 270° anti-clockwise = 90° clockwise = North? Wait, anti-clockwise from West: West→South→East→North. 270° anti-clockwise from West lands on South.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Right turn from North faces?",
            "answer": "East",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Displacement formula for perpendicular legs a and b?",
            "answer": "sqrt(a^2 + b^2)",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Shadow direction at sunrise?",
            "answer": "West",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Turns, displacement",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Direction puzzles",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Clock angles, shadows",
        },
    ],
    "interview_transfer": {
        "prompt": "You're navigating conflicting stakeholder priorities. How does the directions analogy apply?",
        "model_answer": "Track net displacement, not individual moves. Aggregate priorities by direction, not count, to find true alignment.",
    },
}
