"""
Web Development Track — HTML, CSS, React, Node.js
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
Focus: frontend + backend full-stack development.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

WEB_LEVELS = [
    # Level 1: HTML Foundations 🌐
    {"id": "l01", "difficulty": 1, "name": "HTML Foundations", "lessons": [
        _L("HTML Document Structure", 10, 1), _L("Head & Metadata", 10, 1),
        _L("Text Elements: headings, paragraphs, lists", 10, 1), _L("Links & Anchors", 10, 1),
        _L("Images & Alt Text", 10, 1), _L("Semantic HTML (header, nav, main, footer)", 15, 2),
        _L("Practice: Personal Profile Page", 20, 2, "practice"),
        _L("Challenge: Semantic Blog Layout", 25, 2, "challenge"),
        _L("Project: Resume HTML Page", 60, 3, "project",
           "A semantic HTML resume page with proper document structure, metadata, and accessibility."),
    ]},
    # Level 2: CSS Styling 🎨
    {"id": "l02", "difficulty": 1, "name": "CSS Styling", "lessons": [
        _L("CSS Selectors", 10, 1), _L("Box Model: margin, border, padding", 10, 1),
        _L("Colors & Backgrounds", 10, 1), _L("Typography: font-family, font-size, line-height", 15, 2),
        _L("Display: block, inline, inline-block", 15, 2), _L("CSS Units: px, em, rem, %, vw, vh", 15, 2),
        _L("Practice: Styled Profile Card", 20, 2, "practice"),
        _L("Challenge: CSS-Only Landing Page", 30, 3, "challenge"),
        _L("Project: Styled Blog Post", 60, 3, "project",
           "A styled blog post using CSS selectors, box model, typography, and responsive units."),
    ]},
    # Level 3: Layouts 📐
    {"id": "l03", "difficulty": 2, "name": "Layouts", "lessons": [
        _L("Flexbox Basics", 10, 1), _L("Flexbox: justify-content, align-items", 15, 2),
        _L("CSS Grid Basics", 10, 1), _L("Grid: template-columns, template-rows", 15, 2),
        _L("Position: static, relative, absolute, fixed, sticky", 15, 2),
        _L("Z-Index & Stacking Context", 15, 2),
        _L("Practice: Flexbox Dashboard", 20, 2, "practice"),
        _L("Challenge: Grid-Based Gallery", 30, 3, "challenge"),
        _L("Project: Responsive Dashboard Layout", 60, 3, "project",
           "A responsive dashboard using Flexbox, CSS Grid, and positioning."),
    ]},
    # Level 4: Responsive Design 📱
    {"id": "l04", "difficulty": 2, "name": "Responsive Design", "lessons": [
        _L("Media Queries", 10, 1), _L("Breakpoints", 10, 1),
        _L("Mobile-First Design", 15, 2), _L("Fluid Layouts", 15, 2),
        _L("Responsive Images", 15, 2), _L("Viewport Meta Tag", 10, 1),
        _L("Practice: Responsive Navigation", 20, 2, "practice"),
        _L("Challenge: Mobile-First Card Layout", 30, 3, "challenge"),
        _L("Project: Responsive Landing Page", 60, 3, "project",
           "A mobile-first responsive landing page with media queries and fluid layouts."),
    ]},
    # Level 5: JavaScript for Web 🟨
    {"id": "l05", "difficulty": 2, "name": "JavaScript for Web", "lessons": [
        _L("DOM Selection: querySelector, getElementById", 10, 1), _L("DOM Manipulation", 10, 1),
        _L("Event Listeners", 15, 2), _L("Event Bubbling & Delegation", 15, 2),
        _L("Form Handling", 15, 2), _L("LocalStorage & SessionStorage", 15, 2),
        _L("Practice: Interactive Todo List", 20, 2, "practice"),
        _L("Challenge: Form Validation", 30, 3, "challenge"),
        _L("Project: Interactive Task Manager", 60, 3, "project",
           "An interactive task manager with DOM manipulation, events, forms, and localStorage."),
    ]},
    # Level 6: React Fundamentals ⚛️
    {"id": "l06", "difficulty": 3, "name": "React Fundamentals", "lessons": [
        _L("JSX & Components", 10, 1), _L("Props & PropTypes", 10, 1),
        _L("useState Hook", 15, 2), _L("useEffect Hook", 15, 2),
        _L("Conditional Rendering", 15, 2), _L("Lists & Keys", 15, 2),
        _L("Practice: Counter Component", 20, 2, "practice"),
        _L("Challenge: Fetch & Display Data", 35, 3, "challenge"),
        _L("Project: Weather App with React", 60, 3, "project",
           "A React weather app using JSX, props, useState, useEffect, and conditional rendering."),
    ]},
    # Level 7: React Advanced 🚀
    {"id": "l07", "difficulty": 3, "name": "React Advanced", "lessons": [
        _L("Custom Hooks", 15, 2), _L("useRef & useMemo", 15, 2),
        _L("useCallback", 15, 2), _L("Context API", 20, 3),
        _L("React Router", 20, 3), _L("Form Handling in React", 20, 3),
        _L("Practice: Custom Hook Library", 25, 2, "practice"),
        _L("Challenge: Multi-Page App with Router", 40, 3, "challenge"),
        _L("Project: E-commerce Product Catalog", 60, 3, "project",
           "An e-commerce product catalog with React Router, Context API, custom hooks, and forms."),
    ]},
    # Level 8: State Management 📦
    {"id": "l08", "difficulty": 3, "name": "State Management", "lessons": [
        _L("Lifting State Up", 15, 2), _L("Redux Basics", 20, 3),
        _L("Redux Toolkit", 20, 3), _L("Zustand", 20, 3),
        _L("React Query / SWR", 20, 3), _L("Server State vs Client State", 15, 2),
        _L("Practice: Redux Todo App", 25, 2, "practice"),
        _L("Challenge: Global State Migration", 45, 3, "challenge"),
        _L("Project: Dashboard with Global State", 60, 3, "project",
           "A dashboard with Redux Toolkit, Zustand, and React Query for state management."),
    ]},
    # Level 9: Node.js Backend 🟢
    {"id": "l09", "difficulty": 3, "name": "Node.js Backend", "lessons": [
        _L("Node.js Runtime", 10, 1), _L("npm & package.json", 10, 1),
        _L("HTTP Module", 15, 2), _L("Express.js Basics", 15, 2),
        _L("Middleware", 15, 2), _L("Routing", 15, 2),
        _L("Practice: REST API Endpoint", 20, 2, "practice"),
        _L("Challenge: CRUD API", 35, 3, "challenge"),
        _L("Project: Task Management API", 60, 3, "project",
           "A REST API with Express.js, middleware, routing, and CRUD operations."),
    ]},
    # Level 10: Database Integration 🗄️
    {"id": "l10", "difficulty": 3, "name": "Database Integration", "lessons": [
        _L("SQL with Node.js (pg/mysql2)", 15, 2), _L("MongoDB with Mongoose", 15, 2),
        _L("Prisma ORM", 20, 3), _L("Database Migrations", 20, 3),
        _L("Connection Pooling", 15, 2), _L("Transactions in Node.js", 20, 3),
        _L("Practice: Database Query API", 25, 2, "practice"),
        _L("Challenge: Relational Data Modeling", 40, 3, "challenge"),
        _L("Project: Blog Platform with Database", 60, 3, "project",
           "A blog platform with database integration using Prisma ORM and connection pooling."),
    ]},
    # Level 11: Authentication & Security 🔐
    {"id": "l11", "difficulty": 3, "name": "Authentication & Security", "lessons": [
        _L("JWT (JSON Web Tokens)", 15, 2), _L("Bcrypt Password Hashing", 15, 2),
        _L("Session-Based Auth", 15, 2), _L("OAuth 2.0", 20, 3),
        _L("CORS", 15, 2), _L("Helmet & Security Headers", 15, 2),
        _L("Practice: Login API", 25, 2, "practice"),
        _L("Challenge: Role-Based Access Control", 45, 3, "challenge"),
        _L("Project: Secure Auth System", 60, 3, "project",
           "A secure authentication system with JWT, bcrypt, OAuth 2.0, and RBAC."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("WebSockets (Socket.io)", 30, 3), _L("File Upload (multer)", 30, 3),
        _L("Image Processing (Sharp)", 30, 3), _L("Email Integration (Nodemailer)", 30, 3),
        _L("Practice: Real-Time Chat", 40, 3, "practice"),
        _L("Challenge: File Sharing Platform", 50, 3, "challenge"),
        _L("Capstone: Full-Stack SaaS Platform", 80, 3, "project",
           "A full-stack SaaS platform with React, Node.js, database, authentication, and real-time features."),
        _L("👑 Web Dev Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Testing 🧪
    {"id": "l13", "difficulty": 3, "name": "Testing", "lessons": [
        _L("Jest Basics", 15, 2), _L("React Testing Library", 20, 3),
        _L("Supertest for API Testing", 20, 3), _L("End-to-End Testing (Cypress/Playwright)", 25, 3),
        _L("Test-Driven Development (TDD)", 20, 3), _L("Mocking & Stubbing", 20, 3),
        _L("Practice: Unit Tests", 25, 2, "practice"),
        _L("Challenge: E2E Test Suite", 45, 3, "challenge"),
        _L("Project: Tested Application", 60, 3, "project",
           "A fully tested application with Jest, React Testing Library, Supertest, and E2E tests."),
    ]},
    # Level 14: Deployment & DevOps 🚀
    {"id": "l14", "difficulty": 3, "name": "Deployment & DevOps", "lessons": [
        _L("Docker Basics", 20, 3), _L("Dockerfile for Node.js", 20, 3),
        _L("Docker Compose", 20, 3), _L("CI/CD Pipeline (GitHub Actions)", 25, 3),
        _L("Environment Variables", 15, 2), _L("Reverse Proxy (Nginx)", 20, 3),
        _L("Practice: Containerize App", 30, 3, "practice"),
        _L("Challenge: Multi-Stage Docker Build", 45, 3, "challenge"),
        _L("Project: Deployed Full-Stack App", 80, 3, "project",
           "A deployed full-stack application with Docker, CI/CD, environment variables, and Nginx."),
    ]},
]

# Append levels 15-40 for Web Development
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = [
        _L(f"{_meta['emoji']} {_meta['name']} — Core Concepts", 15, 1, "theory"),
        _L(f"🛠️ {_meta['name']} — Hands-On Practice", 20, 2, "practice"),
        _L(f"⚔️ {_meta['name']} — Challenge Problem", 35, 3, "challenge"),
    ]
    if _i + 1 in (20, 25, 30, 35, 40):
        _lessons.append(_L(f"🐉 {_meta['name']} — Boss Battle", 100, 3, "boss"))
    elif _i + 1 in (36, 37, 38):
        _lessons.append(_L(f"🏗️ {_meta['name']} — Capstone Project", 70, 3, "project",
            f"A comprehensive {_meta['name'].lower()} project demonstrating {_meta['desc'].lower()}"))
    else:
        _lessons.append(_L(f"🎯 {_meta['name']} — Mini Project", 60, 3, "project",
            f"A mini project exploring {_meta['desc'].lower()}"))
    WEB_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
