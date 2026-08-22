"""
Web development curriculum tracks — HTML, CSS, SQL, TypeScript, React, Node.js.
Adds 6 new language entries to LANGUAGES following the W3Schools + Scrimba
full-stack module structure. Each track has 20 themed levels with theory,
practice, challenge, project and boss lessons generated from topic pools.

Design notes:
  - Uses the same lesson/level dict shape as curriculum_50_levels so the
    Learning Hub API and frontend work unchanged.
  - Track order follows the Scrimba full-stack path: HTML -> CSS -> JavaScript
    (exists) -> SQL -> TypeScript -> React -> Node.
"""
#pylint: skip-file

import random
from .curriculum import LANGUAGES, _L

random.seed(7)

# ─── Web level themes (shared across web tracks) ───
WEB_THEMES = [
    ("First Steps", "🌱", "#22C55E", "Setup, boilerplate, hello world"),
    ("Structure", "🧱", "#3B82F6", "Core building blocks & document structure"),
    ("Syntax & Basics", "📖", "#F59E0B", "Fundamental syntax, values, comments"),
    ("Control Flow", "🔀", "#8B5CF6", "Conditionals, loops, branching"),
    ("Collections", "📦", "#EF4444", "Arrays, objects, lists, maps"),
    ("Functions & Modules", "🧩", "#06B6D4", "Reusable logic, parameters, imports"),
    ("Structuring Data", "📊", "#10B981", "Tables, records, relationships"),
    ("Building Components", "🏗️", "#F97316", "Reusable UI/logic building blocks"),
    ("Interactivity", "🖱️", "#EC4899", "Events, state, user interaction"),
    ("Styling & Layout", "🎨", "#6366F1", "Box model, flex, grid, layout"),
    ("Advanced Patterns", "🧠", "#14B8A6", "Advanced techniques & best practices"),
    ("Data & Persistence", "💾", "#F97316", "Storage, queries, databases"),
    ("State Management", "🎯", "#DB2777", "Managing shared & complex state"),
    ("APIs & Networking", "🌐", "#0EA5E9", "HTTP, fetch, REST, integration"),
    ("Auth & Security", "🔒", "#84CC16", "Authentication, validation, safety"),
    ("Performance", "🚀", "#D946EF", "Optimization, lazy loading, caching"),
    ("Testing", "🧪", "#0284C7", "Unit, integration & E2E testing"),
    ("Tooling & Build", "🛠️", "#E11D48", "Bundlers, config, CLIs, debugging"),
    ("Accessibility & SEO", "♿", "#64748B", "A11y, semantics, discoverability"),
    ("Full-Stack Capstone", "👑", "#EAB308", "Project + Grandmaster boss battle"),
]

WEB_PHASES = [
    (0, "Foundation"), (5, "Core"), (10, "Intermediate"),
    (15, "Advanced"), (18, "Expert"),
]


def _phase_for_web_level(idx):
    for start, phase in reversed(WEB_PHASES):
        if idx >= start:
            return phase
    return "Foundation"


# ─── Per-track topic pools ───

HTML_TOPICS = {
    "base": ["doctype", "html element", "head & meta", "headings", "paragraphs", "text formatting", "links & anchors", "images & alt text", "lists (ul/ol/dl)", "tables", "forms", "input types", "buttons", "div & span", "semantic tags", "media (audio/video)", "iframes", "comments", "attributes", "entities & symbols"],
    "advanced": ["block vs inline", "character encoding", "ARIA roles", "metadata & OG tags", "canvas API", "svg inline", "drag & drop", "details/summary", "data attributes", "template tags", "picture & srcset", "web components", "custom elements", "shadow DOM", "caching meta", "structured data (JSON-LD)", "forms validation API", "history API", "geolocation", "web storage"],
    "projects": ["Personal Portfolio", "Landing Page", "Blog Template", "Pricing Table", "Business Card Site", "Restaurant Menu", "Event Invitation", "Photo Gallery", "Contact Form", "Resume Page", "FAQ Accordion", "Recipe Page", "News Layout", "Dashboard Shell", "Product Showcase", "Survey Form", "Documentation Page", "Tribute Page", "Coming Soon Page", "Landing for SaaS"],
}

CSS_TOPICS = {
    "base": ["selectors", "colors & backgrounds", "text properties", "fonts & typography", "box model", "margin & padding", "border & radius", "display property", "positioning", "float & clear", "flexbox basics", "grid basics", "pseudo-classes", "pseudo-elements", "specificity", "cascade", "units (px/em/rem)", "links styling", "lists styling", "buttons styling"],
    "advanced": ["custom properties", "CSS functions (calc, clamp)", "gradients", "shadows", "transforms", "transitions", "keyframe animations", "media queries", "responsive units", "container queries", "aspect ratio", "object-fit", "clip-path", "filter effects", "writing modes", "logical properties", "scroll-snap", "isolation & stacking", "content-visibility", "print styles"],
    "projects": ["Responsive Navbar", "Pricing Card", "Button Library", "Loader Collection", "Profile Card", "Login Form", "Hero Section", "Hover Effects", "Animated Background", "CSS Grid Gallery", "Flexbox Dashboard", "Timeline Layout", "Modal Component", "Toggle Switch", "Progress Bar", "Badge System", "Tooltip System", "Breadcrumb", "Footer Layout", "Tribute Page Styling"],
}

SQL_TOPICS = {
    "base": ["SELECT basics", "WHERE clauses", "ORDER BY", "LIMIT & OFFSET", "DISTINCT", "AND/OR/NOT", "IN operator", "BETWEEN", "LIKE & wildcards", "aliases", "functions (COUNT/SUM)", "GROUP BY", "HAVING", "JOIN basics", "INNER JOIN", "LEFT/RIGHT JOIN", "INSERT", "UPDATE", "DELETE", "CREATE TABLE"],
    "advanced": ["primary keys", "foreign keys", "unique constraints", "check constraints", "indexes", "views", "subqueries", "CTEs", "window functions", "PARTITION BY", "UNION/INTERSECT", "CASE expressions", "date/time functions", "string functions", "aggregations deep", "transactions", "stored procedures", "triggers", "normalization", "query optimization"],
    "projects": ["Library Catalog", "Student Roster", "E-Commerce Schema", "Employee Database", "Blog Engine Schema", "Inventory System", "Event Booking", "Movie Database", "Chat Message Store", "Order Management", "Hotel Reservation", "Music Playlist DB", "CRM Schema", "Attendance Tracker", "Expense Tracker", "Forum Schema", "Delivery Tracking", "Warehouse Inventory", "Banking Ledger", "Hospital Scheduling"],
}

TYPESCRIPT_TOPICS = {
    "base": ["setup & tsconfig", "type annotations", "type inference", "primitives", "arrays & tuples", "objects & readonly", "enums", "literal types", "union types", "intersection types", "function types", "optional params", "default params", "type assertions", "interfaces", "classes", "access modifiers", "getters & setters", "abstract classes", "type aliases"],
    "advanced": ["generics basics", "generic constraints", "generic classes", "keyof & typeof", "mapped types", "conditional types", "utility types (Partial, Pick)", "infer keyword", "template literal types", "discriminated unions", "type narrowing", "never & unknown", "overloads", "decorators", "namespaces vs modules", "declaration merging", "module resolution", "strict mode flags", "type-only imports", "declaration files (.d.ts)"],
    "projects": ["Typed Todo API", "Config Loader", "Type-safe Event Bus", "Generic Store", "Typed Form Validator", "API Client Builder", "State Machine", "Command Line Tool", "Typed Router", "Data Mapper", "DI Container", "Typed Pub/Sub", "Schema Validator", "Generic Cache", "ORM-like Repository", "Typed Logger", "GraphQL Client Types", "Mock Service", "Strategy Registry", "Typed Scheduler"],
}

REACT_TOPICS = {
    "base": ["JSX syntax", "components", "props", "children", "state (useState)", "events", "conditional rendering", "lists & keys", "forms & controlled inputs", "lifting state", "effect (useEffect)", "refs (useRef)", "memoization (useMemo)", "callbacks (useCallback)", "context API", "reducers (useReducer)", "router basics", "styled components", "css modules", "composing components"],
    "advanced": ["custom hooks", "compound components", "render props", "higher-order components", "error boundaries", "portals", "suspense & lazy", "concurrent rendering", "transitions (startTransition)", "state libraries (zustand/redux)", "server components", "data fetching patterns", "optimistic updates", "form libraries (react-hook-form)", "virtualized lists", "test components (RTL)", "performance profiling", "code splitting", "memo vs pure components", "headless UI patterns"],
    "projects": ["Todo App", "Expense Tracker", "Weather Dashboard", "Movie Search", "Shopping Cart", "Notes App", "Kanban Board", "Chat UI", "E-Commerce Storefront", "Quiz App", "Recipe Finder", "Pomodoro Timer", "Crypto Ticker", "Job Board", "Portfolio Site", "Social Feed", "Calendar App", "Type-Racer Clone", "Reddit Clone", "Full-Stack SaaS Landing"],
}

NODE_TOPICS = {
    "base": ["runtime basics", "npm & package.json", "CommonJS vs ESM", "event loop", "modules & exports", "global objects", "process & argv", "file system (fs)", "path module", "os module", "http server", "express basics", "routing", "middleware", "query params", "JSON APIs", "static files", "environment variables", "error handling", "async patterns"],
    "advanced": ["event emitters", "streams & buffers", "child processes", "worker threads", "clusters", "database drivers", "ORM (prisma/mongoose)", "JWT auth", "bcrypt hashing", "rate limiting", "input validation (zod)", "testing (jest/vitest)", "loggers (pino/winston)", "configuration", "graceful shutdown", "security headers", "Helmet & CORS", "upload handling (multer)", "websockets (socket.io)", "microservices patterns"],
    "projects": ["REST API Server", "URL Shortener", "Task Manager API", "File Upload Service", "Auth Service", "Blog API", "Real-time Chat Server", "Rate-Limited API", "Todo API with DB", "Weather Proxy", "Markdown Server", "Screenshot Service", "Email Sender", "Cron Job Service", "Payment Webhook", "Search API", "Webhook Receiver", "CLI Tool", "Web Crawler", "Full-Stack Notes App"],
}

WEB_LANG_TOPICS = {
    "html": HTML_TOPICS,
    "css": CSS_TOPICS,
    "sql": SQL_TOPICS,
    "typescript": TYPESCRIPT_TOPICS,
    "react": REACT_TOPICS,
    "node": NODE_TOPICS,
}

# ─── Lesson generators ───

_ALGOS = [
    "Two Sum", "FizzBuzz", "Palindrome Check", "Array Flatten",
    "Debounce", "Throttle", "Deep Merge", "Async Map",
]


def _gen_web_level(topics_pool, lang_id, idx):
    """Generate lessons for a single web-track level from topic pools."""
    lessons = []
    theme = WEB_THEMES[idx]
    phase = _phase_for_web_level(idx)
    base_pool = topics_pool["base"]
    adv_pool = topics_pool["advanced"]
    proj_pool = topics_pool["projects"]
    theme_name = theme[0]

    diff_base = min(3, 1 + idx // 6)
    diff_adv = min(3, 1 + idx // 4)
    xp_base = 10 + idx
    xp_adv = 20 + idx * 2
    xp_proj = 50 + idx * 3

    # Phase intro lessons
    lessons.append(_L(f"{phase} Phase: Welcome to {theme_name}", xp_base, diff_base, "theory"))
    lessons.append(_L(f"{theme_name}: Key Concepts", xp_base, diff_base, "theory"))

    if base_pool:
        bt = base_pool[(idx * 3) % len(base_pool)]
        lessons.append(_L(f"{bt} — Theory", xp_base + 5, diff_base, "theory"))
    if len(base_pool) > 1:
        bt2 = base_pool[(idx * 3 + 1) % len(base_pool)]
        lessons.append(_L(f"{bt2} — In Practice", xp_base + 10, diff_base, "practice"))

    for p_idx in range(2):
        if base_pool:
            bt = base_pool[(idx * 3 + p_idx * 2) % len(base_pool)]
            lessons.append(_L(f"Practice: {bt}", xp_base + 5 + p_idx * 5, diff_base + p_idx, "practice"))

    if base_pool:
        bt = base_pool[(idx * 7) % len(base_pool)]
        lessons.append(_L(f"Challenge: {bt} Mastery", xp_adv, min(3, diff_adv + 1), "challenge"))

    if idx >= 10 and adv_pool:
        at = adv_pool[(idx * 5) % len(adv_pool)]
        lessons.append(_L(f"{at} — Deep Dive", xp_adv, diff_adv, "theory"))
        lessons.append(_L(f"Practice: {at}", xp_adv + 10, diff_adv, "practice"))
        lessons.append(_L(f"Challenge: {at} Implementation", xp_adv + 20, min(3, diff_adv + 1), "challenge"))

    algo = _ALGOS[(idx * 3) % len(_ALGOS)]
    lessons.append(_L(f"Algo: {algo} — {lang_id.upper()} Build", xp_adv + 15, diff_adv, "challenge"))

    if idx >= 15:
        it = ["System Design", "Code Review", "Performance", "Accessibility"]
        lessons.append(_L(f"Review: {it[idx % len(it)]} Audit", xp_adv + 10, diff_adv, "practice"))
        lessons.append(_L(f"Mock: {it[(idx + 1) % len(it)]} Session", xp_adv + 20, 3, "challenge"))

    lessons.append(_L(f"Sprint: {theme_name} Exercises", xp_adv, diff_adv, "practice"))
    lessons.append(_L(f"Quiz: {theme_name} Fundamentals", xp_base, diff_base, "practice"))
    lessons.append(_L(f"Weekly Challenge: {theme_name}", xp_adv + 10, min(3, diff_adv + 1), "challenge"))

    if proj_pool:
        project = proj_pool[(idx * 7) % len(proj_pool)]
        lessons.append(_L(f"Project: {project}", xp_proj, 3, "project"))

    if idx == 4:
        lessons.append(_L(f"🏆 Core Boss: {theme_name} Gauntlet", 80, 3, "boss"))
    elif idx == 9:
        lessons.append(_L(f"🏆 Intermediate Boss: {theme_name} Challenge", 90, 3, "boss"))
    elif idx == 14:
        lessons.append(_L(f"🏆 Advanced Boss: {theme_name} Trial", 100, 3, "boss"))
    elif idx == 19:
        lessons.append(_L(f"👑 Grandmaster: Final {lang_id.upper()} Boss Battle", 150, 3, "boss"))

    return {"id": f"l{idx+1:02d}", "lessons": lessons}


def _build_web_language(lang_id, lang_name, icon, color, desc):
    """Build a 20-level web curriculum language from topic pools."""
    topics = WEB_LANG_TOPICS.get(lang_id)
    levels = {}
    total = 0
    for i in range(20):
        raw = _gen_web_level(topics, lang_id, i)
        theme = WEB_THEMES[i]
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
        levels[raw["id"]] = {
            "id": raw["id"],
            "name": theme[0],
            "emoji": theme[1],
            "color": theme[2],
            "bg": "from-gray-500/20 to-gray-600/20",
            "border": "border-gray-500/30",
            "text": "text-gray-400",
            "description": theme[3],
            "order": i + 1,
            "lessons": lessons,
            "total_lessons": len(lessons),
            "total_xp": total_xp,
        }
        total += len(lessons)
    return {
        "id": lang_id,
        "name": lang_name,
        "icon": icon,
        "color": color,
        "description": desc,
        "total_lessons": total,
        "levels": levels,
    }


def install_web_curriculum():
    """Add the 6 web development tracks to LANGUAGES (idempotent)."""
    web_langs = [
        ("html", "HTML", "🌐", "#E34F26", "Structure the web — semantic markup, forms, media, accessibility, SEO"),
        ("css", "CSS", "🎨", "#1572B6", "Style the web — box model, flex, grid, animations, responsive design"),
        ("sql", "SQL", "🗄️", "#4479A1", "Query and model data — joins, aggregates, indexes, normalization"),
        ("typescript", "TypeScript", "🔷", "#3178C6", "Typed JavaScript — interfaces, generics, strict mode, utility types"),
        ("react", "React", "⚛️", "#61DAFB", "Build interactive UIs — components, hooks, state, performance"),
        ("node", "Node.js", "🟢", "#339933", "Run JavaScript everywhere — servers, APIs, streams, databases"),
    ]
    for lid, name, icon, color, desc in web_langs:
        LANGUAGES[lid] = _build_web_language(lid, name, icon, color, desc)
    return LANGUAGES
