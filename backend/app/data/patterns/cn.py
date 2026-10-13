"""Pattern Pack — Computer Networks."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "cn",
    "name": "Computer Networks",
    "emoji": "🌐",
    "round_id": "cs-core",
    "purpose": "Compare OSI/TCP-IP layers, identify protocols, and reason about subnetting and DNS.",
    "prerequisites": ["computer-basics", "os"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "OSI layer off-by-one",
            "description": "Confuses session and presentation layers.",
        },
        {
            "id": "M2",
            "label": "TCP vs UDP",
            "description": "Uses UDP when reliability matters.",
        },
        {
            "id": "M3",
            "label": "Subnet mask math",
            "description": "Counts host bits incorrectly for /24 vs /25.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "OSI layers",
            "captain_message": "See the 7 layers as a stack.",
            "render": {
                "kind": "layer_stack",
                "layers": ["Physical", "Data Link", "Network", "Transport", "Session", "Presentation", "Application"],
                "highlight": ["Network", "Transport"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Map protocols",
            "captain_message": "Drag protocols to layers.",
            "render": {
                "kind": "protocol_map",
                "protocols": ["HTTP", "TCP", "IP", "Ethernet"],
                "layers": ["Application", "Transport", "Network", "Data Link"],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the layer",
            "captain_message": "Choose the correct layer.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "TCP operates at which OSI layer?",
                "options": ["Network", "Transport", "Session", "Application"],
                "answer_index": 1,
                "explanation": "TCP is transport layer (layer 4).",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the packet journey",
            "captain_message": "Write the encapsulation chain.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Sender adds",
                        "placeholder": "headers from layer 7 down to 1",
                        "answer": "headers from layer 7 down to 1",
                    },
                    {
                        "label": "Receiver removes",
                        "placeholder": "headers from layer 1 up to 7",
                        "answer": "headers from layer 1 up to 7",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break TCP vs UDP",
            "captain_message": "TCP is reliable, UDP is fast.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Which uses UDP?",
                "options": ["HTTP", "DNS query", "SSH", "Email"],
                "answer_index": 1,
                "explanation": "DNS commonly uses UDP for speed; TCP used for HTTP, SSH, email.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix subnet math",
            "captain_message": "Hosts = 2^(32-mask) - 2.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Mask",
                        "placeholder": "/24 → 255.255.255.0",
                        "answer": "/24 → 255.255.255.0",
                    },
                    {
                        "label": "Host bits",
                        "placeholder": "32 - 24 = 8",
                        "answer": "32 - 24 = 8",
                    },
                    {
                        "label": "Hosts",
                        "placeholder": "2^8 - 2 = 254",
                        "answer": "2^8 - 2 = 254",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to DNS",
            "captain_message": "DNS maps names to IPs at application layer.",
            "render": {
                "kind": "recall",
                "prompt": "DNS operates at OSI layer?",
                "answer": "Application",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Remember: HTTP=app, TCP=transport, IP=network, Ethernet=data link.",
            "render": {
                "kind": "recall",
                "prompt": "Ethernet operates at OSI layer?",
                "answer": "Data Link",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Which layer is responsible for routing?",
                "options": ["Data Link", "Network", "Transport", "Application"],
                "answer": "Network",
                "explanation": "Network layer handles IP and routing.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "How many host addresses in 192.168.1.0/24?",
                "options": ["254", "256", "255", "128"],
                "answer": "254",
                "explanation": "/24 has 8 host bits: 2^8 - 2 = 254 usable hosts.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Which protocol is connectionless?",
                "options": ["TCP", "UDP", "HTTP", "SSH"],
                "answer": "UDP",
                "explanation": "UDP is connectionless; TCP is connection-oriented.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Full form of HTTP?",
                "options": ["HyperText Transfer Protocol", "High Tech Transfer Protocol", "HyperText Transmission Protocol", "None"],
                "answer": "HyperText Transfer Protocol",
                "explanation": "HTTP = HyperText Transfer Protocol.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Which layer ensures reliable delivery?",
            "options": ["Network", "Transport", "Data Link", "Application"],
            "answer": "Transport",
            "explanation": "Transport layer (TCP) ensures reliable delivery.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "TCP vs UDP main difference?",
            "answer": "TCP is reliable, UDP is fast",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "IP operates at OSI layer?",
            "answer": "Network",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "/24 usable hosts?",
            "answer": "254",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "OSI, TCP/UDP",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Subnetting, protocols",
        },
    ],
    "interview_transfer": {
        "prompt": "How does OSI layering thinking apply to microservices?",
        "model_answer": "Each layer has a contract. Microservices should expose clean transport-layer contracts and avoid leaking network concerns into application logic.",
    },
}
