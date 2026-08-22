"""
Curriculum depth expansion — doubles the Learning Hub:
  * Core tracks (C, C++, Java, Python, JS, Go, Rust): levels 51-100
    (Professional -> Senior -> Expert -> Architect -> Mastery).
  * Web tracks (HTML, CSS, SQL, TS, React, Node): levels 21-40
    (Advanced -> Professional -> Senior -> Mastery).
Each new level is denser in hands-on work: exercise sprints, code reviews,
challenges, quizzes and TWO projects per level so learners build real,
production-grade software by the end of the track.
"""
#pylint: skip-file

import random
from .curriculum import LANGUAGES, _L
from .curriculum_50_levels import LANG_TOPICS
from .curriculum_web import WEB_LANG_TOPICS

random.seed(2026)

# ─── Core depth themes (levels 51-100) ───
CORE_LEVELS_EXTRA = [
    ("Domain Modeling", "📐", "#B91C1C", "Model real-world problems cleanly"),
    ("Design Patterns in Depth", "🏛️", "#0369A1", "Creational, structural, behavioral"),
    ("SOLID Principles", "🧱", "#15803D", "Single responsibility to DI"),
    ("Functional Thinking", "⬡", "#7E22CE", "Immutability, purity, composition"),
    ("Concurrency Mastery", "⚙️", "#A21CAF", "Threads, races, coordination"),
    ("Parallel Computing", "🖥️", "#0E7490", "Parallelism, work stealing, GPU"),
    ("Distributed Systems", "🌍", "#92400E", "Consensus, replication, partitioning"),
    ("Microservices Architecture", "🧩", "#1E40AF", "Services, contracts, ownership"),
    ("Event-Driven Design", "📡", "#EAB308", "Events, streams, CQRS"),
    ("Message Queues & Streams", "📨", "#16A34A", "Pub/sub, brokers, replay"),
    ("Caching Systems", "🧊", "#DC2626", "Cache hierarchies, invalidation"),
    ("Database Internals", "🗃️", "#7C3AED", "Storage, transactions, MVCC"),
    ("Query Optimization", "🚀", "#0891B2", "Plans, statistics, indexes"),
    ("Indexing Strategies", "📑", "#F59E0B", "B-trees, hash, composite"),
    ("ORM & Data Mappers", "🔗", "#EC4899", "Object-relational impedance"),
    ("REST API Design", "🛣️", "#2563EB", "Resources, versions, pagination"),
    ("GraphQL & gRPC", "🕸️", "#9333EA", "Contract-first APIs"),
    ("Realtime Systems", "⚡", "#EF4444", "WebSockets, SSE, presence"),
    ("Web Security", "🛡️", "#065F46", "OWASP, injection, XSS, CSRF"),
    ("Authentication & Authorization", "🔐", "#6D28D9", "Sessions, tokens, RBAC"),
    ("OAuth & JWT", "🎫", "#B45309", "Flows, scopes, refresh"),
    ("Cryptography in Practice", "🗝️", "#9D174D", "Hashing, signing, TLS"),
    ("Performance Profiling", "📈", "#1E3A5F", "Profilers, flame graphs, hot paths"),
    ("Memory Optimization", "🧠", "#4C1D95", "Leaks, fragmentation, pooling"),
    ("CPU & Cache Locality", "💽", "#701A75", "Locality, vectorization, branch hints"),
    ("Network Protocols Deep", "🌐", "#0F766E", "TCP/UDP/TLS internals"),
    ("HTTP & Web Protocols", "🔄", "#A16207", "HTTP/2, HTTP/3, keep-alive"),
    ("Operating Systems Deep", "🖧", "#831843", "Schedulers, syscalls, memory maps"),
    ("Processes & Threads", "🧵", "#3730A3", "IPC, signals, thread pools"),
    ("Shell & Tooling Power", "🐚", "#0D9488", "Scripting, automation, workflow"),
    ("Build Systems & Packaging", "📦", "#6B21A8", "Incremental builds, artifacts"),
    ("CI/CD Pipelines", "🔄", "#B91C1C", "Stages, gates, rollbacks"),
    ("Containerization", "🐳", "#0369A1", "Images, layers, registries"),
    ("Orchestration & Cloud", "☁️", "#15803D", "Scheduling, autoscaling, HA"),
    ("Infrastructure as Code", "🏗️", "#7E22CE", "Declarative infra, drift"),
    ("Observability & Tracing", "🔭", "#A21CAF", "Metrics, traces, correlation"),
    ("Logging & Monitoring", "📊", "#0E7490", "Structured logs, dashboards"),
    ("Alerting & On-Call", "🚨", "#92400E", "SLOs, runbooks, paging"),
    ("Test-Driven Development", "🧪", "#1E40AF", "Red-green-refactor cycles"),
    ("Property & Fuzz Testing", "🎲", "#EAB308", "Invariants, random inputs"),
    ("Integration Testing", "🔌", "#16A34A", "Contract, snapshot, boundary"),
    ("End-to-End Testing", "🖱️", "#DC2626", "User journeys, flakiness"),
    ("Refactoring to Patterns", "🛠️", "#7C3AED", "Safe transformation workflows"),
    ("Code Smells & Clean Code", "🧹", "#0891B2", "Readability, maintainability"),
    ("Code Reviews at Scale", "👀", "#F59E0B", "Review checklists, mentoring"),
    ("Technical Interview Mastery", "🎯", "#EC4899", "Live coding, system design, STAR"),
    ("System Design Deep", "🏛️", "#2563EB", "End-to-end architecture"),
    ("Scalability & Reliability", "📶", "#9333EA", "Load, sharding, failover"),
    ("Big Data & Streaming", "💾", "#065F46", "Batch, stream, data pipelines"),
    ("Capstone: Production System", "👑", "#EAB308", "Full product + Grandmaster boss"),
]

CORE_DEPTH_PHASES = [
    (0, "Professional"), (10, "Senior"), (20, "Expert"),
    (30, "Architect"), (40, "Mastery"),
]

# ─── Web depth themes (levels 21-40) ───
WEB_LEVELS_EXTRA = [
    ("Advanced Layout Mastery", "🧭", "#B91C1C", "Complex responsive layouts, container queries"),
    ("Component Architecture", "🧱", "#0369A1", "Composition, boundaries, reuse"),
    ("Design Systems", "🎨", "#15803D", "Tokens, primitives, documentation"),
    ("State Machines & Logic", "🎯", "#7E22CE", "Transitions, guards, effects"),
    ("Data Fetching Patterns", "📡", "#A21CAF", "Cache, stale-while-revalidate, mutations"),
    ("Realtime Features", "⚡", "#0E7490", "Sockets, presence, live updates"),
    ("Progressive Web Apps", "📱", "#92400E", "Offline, install, push"),
    ("Web Performance", "🚀", "#1E40AF", "Rendering, bundling, hydration"),
    ("Core Web Vitals", "📊", "#EAB308", "LCP, CLS, INP optimization"),
    ("Browser Internals", "🌐", "#16A34A", "Parsing, painting, compositing"),
    ("Web Security Deep", "🛡️", "#DC2626", "XSS, CSRF, injection, headers"),
    ("Auth Flows in Production", "🔐", "#7C3AED", "OAuth, sessions, RBAC"),
    ("API Design & Contracts", "🛣️", "#0891B2", "REST, GraphQL, versioning"),
    ("Internationalization", "🌍", "#F59E0B", "i18n, l10n, locale formats"),
    ("Animation & Motion", "🎬", "#EC4899", "Timing, spring, reduced-motion"),
    ("Testing Web Apps", "🧪", "#2563EB", "Unit, integration, E2E"),
    ("Monorepos & Tooling", "🛠️", "#9333EA", "Workspaces, caching, linting"),
    ("Edge & Serverless", "⚡", "#065F46", "CDN, edge functions, FaaS"),
    ("Full-Stack Integration", "🔗", "#6D28D9", "Frontend + backend + data"),
    ("Capstone: Production App", "👑", "#EAB308", "Full product + Grandmaster boss"),
]

WEB_DEPTH_PHASES = [
    (0, "Advanced"), (5, "Professional"), (10, "Senior"), (15, "Mastery"),
]

# ─── Extra project titles (extend the existing pools) ───
CORE_PROJECTS_EXTRA = {
    "c": ["Embedded RTOS", "Zero-copy Proxy", "Real-time Trading Engine", "P2P Chat Mesh", "Distributed Cache", "Vector Database", "Neural Net Runtime", "JIT for Toy Language", "Memory Debugger", "Zero-downtime Server", "Packet Analyzer", "USB Driver", "FPGA Simulator", "Realtime Ray Tracer", "Concurrent Web Crawler", "Blockchain Node", "Database Replicator", "DNS Resolver", "Load Balancer", "Event Bus"],
    "cpp": ["Game Server", "Physics Sandbox", "Coroutine Runtime", "Metal Renderer", "Audio Synthesizer", "CAD Application", "Machine Vision", "Robotics Controller", "Compiler Optimizer", "Header-only Library", "IPC Framework", "Memory Profiler", "Unit Test Framework", "Benchmark Suite", "Distributed KV Store", "Transaction Engine", "Vulkan Pipeline", "Neural Network Engine", "Big Integer Library", "Serialization Framework"],
    "java": ["Payment Platform", "E-Commerce Backend", "Booking Engine", "Recommendation Engine", "Data Warehouse", "ETL Framework", "Workflow Orchestrator", "API Gateway", "Config Center", "Distributed Lock Service", "Message Broker", "Streaming Processor", "Batch Scheduler", "Fraud Detection", "Credit Scoring", "Saga Orchestrator", "Inventory Service", "Notification Service", "Search Platform", "Analytics Pipeline"],
    "python": ["ML Platform", "Feature Pipeline", "Model Serving", "Hyperparameter Tuner", "Data Lake Manager", "Orchestration Engine", "Async Crawler Farm", "Knowledge Base", "RAG Service", "AI Agent Framework", "Code Interpreter", "Notebook Runner", "Scheduler Cluster", "Cache-aside Service", "Blob Storage", "Workflow DSL", "Rule Engine", "Scoring Service", "Event Sourcing Store", "Metasearch Engine"],
    "javascript": ["Framework Runtime", "State Machine Library", "Bundler Plugin System", "DevTools Extension", "Playwright Testing Kit", "Realtime Dashboard", "CRDT Editor", "Offline Sync Engine", "Streaming Data Grid", "Design System Kit", "Headless CMS", "Web Worker Pool", "IndexedDB Abstraction", "Meta-Framework Router", "Form Engine", "Animation Engine", "WebGL Scene Graph", "Audio Workstation", "Plugin Marketplace", "SSR Framework"],
    "go": ["Gateway Mesh", "Config Agent", "Secrets Vault", "File Sync Daemon", "K8s Operator", "Telemetry Agent", "Trace Collector", "Queue Consumer", "Storage Engine", "Snapshot Manager", "Health Checker", "Service Mesh Dataplane", "Edge Router", "Rate Limit Service", "Pub/Sub Broker", "Cache Proxy", "DB Migration Tool", "Env Var Resolver", "Feature Server", "Benchmark Driver"],
    "rust": ["Async Runtime Scheduler", "Zero-Copy Parser", "WebGPU Wrapper", "Bytecode VM", "Memory Allocator Bench", "Networking Stack", "Cryptographic Engine", "Static Site Generator", "Terminal App Framework", "Game ECS", "Serial Port Monitor", "Embedded HAL", "State Machine Compiler", "Hot Reload Engine", "Custom Lint Pass", "Lock-Free HashMap", "Vector Clock Store", "Arena GC", "Foreign Function Bridge", "SIMD Image Processor"],
}

WEB_PROJECTS_EXTRA = {
    "html": ["Accessible Form Suite", "Semantic Blog Layout", "Email Newsletter", "Icon System", "Pattern Library", "Storybook HTML", "Static Site Shell", "Landing Page Kit", "Portfolio Generator", "Resume Builder", "Event Calendar", "Blog Platform", "E-Commerce Storefront", "SaaS Marketing Site", "Documentation Generator", "FAQ Knowledge Base", "Local Business Site", "Crypto Landing Page", "Podcast Website", "Course Landing Page"],
    "css": ["CSS Framework Mini", "Utility Class Generator", "Motion Design System", "Chart Library", "CSS Art Gallery", "Theme Switcher", "Glassmorphism Kit", "Neumorphism Kit", "Print Stylesheet Kit", "Component Showcase", "Gallery Lightbox", "Timeline Component", "Skill Meter Components", "Loading Screen Suite", "404 Page Collection", "CSS-only Game", "Card Library", "Badge & Status System", "Table Styling Kit", "Form Styling Kit"],
    "sql": ["Analytics Warehouse", "Event Tracking Schema", "Inventory Optimization", "Support Ticket System", "Learning Management DB", "Gaming Stats DB", "Booking Engine", "Recommendation Engine SQL", "Fraud Detection Schema", "Geospatial Queries", "Log Aggregation Schema", "ML Feature Store", "A/B Testing Store", "Billing Ledger", "Content Moderation DB", "Shipping & Logistics", "HR Payroll Schema", "Survey Platform DB", "Fintech Ledger", "Multi-tenant SaaS Schema"],
    "typescript": ["Typed Event Store", "Schema Codegen", "API Contract Types", "Generic Data Grid", "Command Handler Bus", "Plugin System Types", "Typed i18n Kit", "Type-safe Router", "Entity Component System", "Config Schema Gen", "Mock Server Types", "Stream Processor Types", "Validator Compiler", "Typed Task Queue", "Migration Runner", "Feature Flag SDK", "Type-safe WebSocket", "RPC Types", "Observability Types", "Typed ORM"],
    "react": ["AI Chat UI", "Dashboard Framework", "Form Builder", "Survey App", "Project Management App", "E-Learning Platform", "Social Media Clone", "Music Player App", "Fitness Tracker", "Travel Planner", "Marketplace UI", "Admin Panel Kit", "Chat Widget", "File Manager", "Kanban with Drag-drop", "Code Playground UI", "News Aggregator", "Community Forum", "Video Platform UI", "Real-Time Collab Editor"],
    "node": ["Realtime Analytics Service", "Webhook Manager", "Screenshot Pipeline", "File Processing Queue", "Email Automation", "Cron Scheduler Service", "API Versioning Gateway", "Payment Splitter", "Notification Dispatcher", "Export/Import Engine", "Webhook Validator", "Feature Toggle Server", "Background Job Dashboard", "Streaming Proxy", "Auth Microservice", "Log Stream Server", "Rate Limit Proxy", "Image Processing Server", "PDF Report Generator", "GraphQL Federation Gateway"],
}

_DEPTH_ALGOS = [
    "Two Sum Variant", "Median of Two Arrays", "Merge K Sorted Lists", "LRU Cache",
    "Top K Frequent", "Word Ladder", "Min Window Substring", "Course Schedule",
    "Design Twitter", "Find Median Stream", "Longest Increasing Path", "Alien Dictionary",
    "Sliding Window Max", "Word Break II", "Kth Smallest Matrix", "Serialize Tree",
]


def _depth_phase(idx):
    for start, phase in reversed(CORE_DEPTH_PHASES):
        if idx >= start:
            return phase
    return "Professional"


def _web_depth_phase(idx):
    for start, phase in reversed(WEB_DEPTH_PHASES):
        if idx >= start:
            return phase
    return "Advanced"


def _gen_level_depth(topics_pool, lang_id, idx):
    """Generate a dense hands-on level (levels 51-100)."""
    lessons = []
    theme = CORE_LEVELS_EXTRA[idx]
    phase = _depth_phase(idx)
    base_topic = theme[0]
    base_pool = topics_pool["base"]
    adv_pool = topics_pool["advanced"]
    proj_pool = topics_pool["projects"]

    diff = 2 if idx < 15 else 3
    xp = 40 + idx * 2
    xp_proj = 80 + idx * 3

    lessons.append(_L(f"{phase} Phase: {base_topic} — {lang_id.upper()} Professional", xp, 1, "theory"))
    lessons.append(_L(f"{base_topic}: Architecture Overview", xp + 5, diff, "theory"))

    bt = base_pool[(idx * 3 + 50) % len(base_pool)]
    lessons.append(_L(f"{bt} — Advanced Theory", xp + 10, diff, "theory"))
    bt2 = base_pool[(idx * 3 + 51) % len(base_pool)]
    lessons.append(_L(f"{bt2} — In Practice", xp + 15, diff, "practice"))

    at = adv_pool[(idx * 5 + 40) % len(adv_pool)]
    lessons.append(_L(f"{at} — Deep Dive", xp + 20, 3, "theory"))
    at2 = adv_pool[(idx * 5 + 41) % len(adv_pool)]
    lessons.append(_L(f"Practice: {at2}", xp + 25, 3, "practice"))

    lessons.append(_L(f"Sprint: {base_topic} — 3 Build Exercises", xp + 20, diff, "practice"))
    lessons.append(_L(f"Sprint: {bt} — Mini Builds", xp + 25, diff + 1, "practice"))

    lessons.append(_L(f"Challenge: {base_topic} Implementation", xp + 30, 3, "challenge"))
    lessons.append(_L(f"Challenge: {at} Production Case", xp + 40, 3, "challenge"))

    algo = _DEPTH_ALGOS[(idx * 3) % len(_DEPTH_ALGOS)]
    lessons.append(_L(f"Algo: {algo} — Optimized {lang_id.upper()} Solution", xp + 35, 3, "challenge"))

    lessons.append(_L(f"Review: {base_topic} Code Samples", xp + 15, diff, "practice"))
    lessons.append(_L(f"Quiz: {base_topic} Mastery Check", xp + 10, diff, "practice"))

    if proj_pool:
        p1 = proj_pool[(idx * 5 + 23) % len(proj_pool)]
        lessons.append(_L(f"Mini Project: {p1} v1", xp_proj, 3, "project"))
        p2 = proj_pool[(idx * 7 + 50) % len(proj_pool)]
        lessons.append(_L(f"Project: {p2} — Production Build", xp_proj + 20, 3, "project"))

    if idx == 9:
        lessons.append(_L(f"🏆 Senior Boss: {base_topic} Trial", 140, 3, "boss"))
    elif idx == 19:
        lessons.append(_L(f"🏆 Expert Boss: {base_topic} Exam", 150, 3, "boss"))
    elif idx == 29:
        lessons.append(_L(f"🏆 Architect Boss: {base_topic} Defense", 160, 3, "boss"))
    elif idx == 39:
        lessons.append(_L(f"🏆 Mastery Boss: {base_topic} Gauntlet", 170, 3, "boss"))
    elif idx == 49:
        lessons.append(_L("👑 Grandmaster: Final Capstone Battle", 200, 3, "boss"))

    return {"id": f"l{idx+51:02d}", "lessons": lessons}


def _gen_web_level_depth(topics_pool, lang_id, idx):
    """Generate a dense hands-on web level (levels 21-40)."""
    lessons = []
    theme = WEB_LEVELS_EXTRA[idx]
    phase = _web_depth_phase(idx)
    theme_name = theme[0]
    base_pool = topics_pool["base"]
    adv_pool = topics_pool["advanced"]
    proj_pool = topics_pool["projects"]

    diff = 2 if idx < 10 else 3
    xp = 40 + idx * 2
    xp_proj = 80 + idx * 3

    lessons.append(_L(f"{phase} Phase: {theme_name} — {lang_id.title()} Professional", xp, 1, "theory"))
    lessons.append(_L(f"{theme_name}: Key Architecture", xp + 5, diff, "theory"))

    bt = base_pool[(idx * 3 + 30) % len(base_pool)]
    lessons.append(_L(f"{bt} — Advanced Theory", xp + 10, diff, "theory"))
    bt2 = base_pool[(idx * 3 + 31) % len(base_pool)]
    lessons.append(_L(f"{bt2} — In Practice", xp + 15, diff, "practice"))

    if adv_pool:
        at = adv_pool[(idx * 5 + 22) % len(adv_pool)]
        lessons.append(_L(f"{at} — Deep Dive", xp + 20, 3, "theory"))
        at2 = adv_pool[(idx * 5 + 23) % len(adv_pool)]
        lessons.append(_L(f"Practice: {at2}", xp + 25, 3, "practice"))

    lessons.append(_L(f"Sprint: {theme_name} — 3 Build Exercises", xp + 20, diff, "practice"))
    lessons.append(_L(f"Sprint: {bt} — Mini Builds", xp + 25, diff + 1, "practice"))

    lessons.append(_L(f"Challenge: {theme_name} Implementation", xp + 30, 3, "challenge"))

    algo = _DEPTH_ALGOS[(idx * 3 + 5) % len(_DEPTH_ALGOS)]
    lessons.append(_L(f"Algo: {algo} — {lang_id.title()} Build", xp + 35, 3, "challenge"))

    lessons.append(_L(f"Review: {theme_name} Audit", xp + 15, diff, "practice"))
    lessons.append(_L(f"Quiz: {theme_name} Mastery Check", xp + 10, diff, "practice"))

    if proj_pool:
        p1 = proj_pool[(idx * 5 + 12) % len(proj_pool)]
        lessons.append(_L(f"Mini Project: {p1} v1", xp_proj, 3, "project"))
        p2 = proj_pool[(idx * 7 + 26) % len(proj_pool)]
        lessons.append(_L(f"Project: {p2} — Production Build", xp_proj + 20, 3, "project"))

    if idx == 4:
        lessons.append(_L(f"🏆 Professional Boss: {theme_name} Trial", 140, 3, "boss"))
    elif idx == 9:
        lessons.append(_L(f"🏆 Senior Boss: {theme_name} Exam", 150, 3, "boss"))
    elif idx == 14:
        lessons.append(_L(f"🏆 Mastery Boss: {theme_name} Defense", 160, 3, "boss"))
    elif idx == 19:
        lessons.append(_L(f"👑 Grandmaster: Final {lang_id.title()} Capstone Battle", 200, 3, "boss"))

    return {"id": f"l{idx+21:02d}", "lessons": lessons}


def _build_level_dict(lang_id, raw, theme, order):
    lessons = []
    for j, l in enumerate(raw["lessons"]):
        lessons.append({
            "id": f"{lang_id}-{raw['id']}-{j+1:02d}",
            "title": l["title"],
            "xp": l["xp"],
            "difficulty": l["difficulty"],
            "type": l["type"],
        })
    total_xp = sum(l["xp"] for l in lessons)
    return {
        "id": raw["id"],
        "name": theme[0],
        "emoji": theme[1],
        "color": theme[2],
        "bg": "from-gray-500/20 to-gray-600/20",
        "border": "border-gray-500/30",
        "text": "text-gray-400",
        "description": theme[3],
        "order": order,
        "lessons": lessons,
        "total_lessons": len(lessons),
        "total_xp": total_xp,
    }


def install_depth_curriculum():
    """Append levels 51-100 (core) and 21-40 (web), doubling every track."""
    for lang_id in list(LANG_TOPICS.keys()):
        topics = LANG_TOPICS[lang_id]
        extra = CORE_PROJECTS_EXTRA.get(lang_id, [])
        for p in extra:
            if p not in topics["projects"]:
                topics["projects"].append(p)
        entry = LANGUAGES.get(lang_id)
        if not entry:
            continue
        levels = entry["levels"]
        start = len(levels)
        for i in range(50):
            raw = _gen_level_depth(topics, lang_id, i)
            levels[raw["id"]] = _build_level_dict(lang_id, raw, CORE_LEVELS_EXTRA[i], start + i + 1)
        entry["total_lessons"] = sum(len(lv["lessons"]) for lv in levels.values())

    for lang_id in list(WEB_LANG_TOPICS.keys()):
        topics = WEB_LANG_TOPICS[lang_id]
        extra = WEB_PROJECTS_EXTRA.get(lang_id, [])
        for p in extra:
            if p not in topics["projects"]:
                topics["projects"].append(p)
        entry = LANGUAGES.get(lang_id)
        if not entry:
            continue
        levels = entry["levels"]
        start = len(levels)
        for i in range(20):
            raw = _gen_web_level_depth(topics, lang_id, i)
            levels[raw["id"]] = _build_level_dict(lang_id, raw, WEB_LEVELS_EXTRA[i], start + i + 1)
        entry["total_lessons"] = sum(len(lv["lessons"]) for lv in levels.values())

    return LANGUAGES
