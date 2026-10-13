"""Pattern Pack — TCP/IP."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "tcp-ip",
    "name": "TCP/IP",
    "emoji": "📡",
    "round_id": "technical-interview",
    "purpose": "Explain TCP handshake, flow control, congestion control, and compare TCP vs UDP for application requirements.",
    "prerequisites": ["cn", "os"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "3-way handshake is slow",
            "description": "Believes 3-way handshake is always a performance problem.",
        },
        {
            "id": "M2",
            "label": "TCP guarantees delivery instantly",
            "description": "Confuses reliability with latency.",
        },
        {
            "id": "M3",
            "label": "Port is IP address",
            "description": "Treats port as part of IP rather than transport demultiplexing.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Handshake sequence",
            "captain_message": "See SYN, SYN-ACK, ACK.",
            "render": {
                "kind": "sequence",
                "steps": ["Client SYN", "Server SYN-ACK", "Client ACK"],
                "highlight": ["SYN", "ACK"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change window size",
            "captain_message": "Adjust TCP window. See throughput change.",
            "render": {
                "kind": "slider",
                "rtt_ms": 100,
                "min_window": 1,
                "max_window": 100,
                "default_window": 10,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict handshake packets",
            "captain_message": "Count packets to establish connection.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "TCP connection establishment needs how many packets?",
                "options": ["1", "2", "3", "4"],
                "answer_index": 2,
                "explanation": "3-way handshake: SYN, SYN-ACK, ACK.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the handshake",
            "captain_message": "Write packet types in order.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Client sends",
                        "placeholder": "SYN",
                        "answer": "SYN",
                    },
                    {
                        "label": "Server replies",
                        "placeholder": "SYN-ACK",
                        "answer": "SYN-ACK",
                    },
                    {
                        "label": "Client confirms",
                        "placeholder": "ACK",
                        "answer": "ACK",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break TCP vs UDP choice",
            "captain_message": "Video streaming often uses UDP.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Which prefers UDP?",
                "options": ["Email", "File transfer", "Video streaming", "SSH"],
                "answer_index": 2,
                "explanation": "Video streaming tolerates some loss for lower latency.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix congestion",
            "captain_message": "Reduce window on loss.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Detect loss",
                        "placeholder": "timeout or duplicate ACK",
                        "answer": "timeout or duplicate ACK",
                    },
                    {
                        "label": "Reduce window",
                        "placeholder": "cwnd = cwnd / 2",
                        "answer": "cwnd = cwnd / 2",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to HTTP/3",
            "captain_message": "QUIC runs over UDP to avoid TCP head-of-line blocking.",
            "render": {
                "kind": "recall",
                "prompt": "HTTP/3 uses?",
                "answer": "QUIC over UDP",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "TCP = reliable, ordered. UDP = fast, unreliable.",
            "render": {
                "kind": "recall",
                "prompt": "TCP guarantees?",
                "answer": "reliable, ordered delivery with congestion control",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "TCP handshake packets?",
                "options": ["1", "2", "3", "4"],
                "answer": "3",
                "explanation": "3-way handshake: SYN, SYN-ACK, ACK.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Which protocol is connectionless?",
                "options": ["TCP", "UDP", "HTTP", "SSH"],
                "answer": "UDP",
                "explanation": "UDP is connectionless.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "TCP port 80 defaults to?",
                "options": ["FTP", "HTTP", "SSH", "DNS"],
                "answer": "HTTP",
                "explanation": "Port 80 = HTTP.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "TCP slow start aims to?",
                "options": ["Reduce latency", "Find available bandwidth", "Encrypt data", "Route packets"],
                "answer": "Find available bandwidth",
                "explanation": "Slow start probes for available bandwidth.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Which is TCP flow control?",
            "options": ["Sliding window", "Congestion window", "Three-way handshake", "IP routing"],
            "answer": "Sliding window",
            "explanation": "Sliding window provides flow control.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "TCP handshake steps?",
            "answer": "SYN, SYN-ACK, ACK",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "TCP vs UDP?",
            "answer": "TCP reliable, UDP fast",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "TCP port 80?",
            "answer": "HTTP",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "TCP vs UDP, handshake",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "OSI, protocols",
        },
    ],
    "interview_transfer": {
        "prompt": "How does TCP congestion control thinking apply to API rate limiting?",
        "model_answer": "Both detect overload and back off. Slow start maps to ramp-up, packet loss maps to 429/backoff.",
    },
}
