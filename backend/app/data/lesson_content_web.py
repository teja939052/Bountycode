"""Lesson content templates for web & modern tracks (HTML, CSS, SQL, TypeScript,
React, Node.js, JavaScript, Go, Rust).

Provides W3Schools-depth generated lesson content so the newer tracks do not fall
through to the thin generic fallback. Mirrors the config shape used by
generate_template_content() in lesson_content.py.

Placeholders use the `__CONCEPT__` token (NOT `{concept}`) so that:
  - the module can be imported without a `concept` variable in scope, and
  - CSS/JS code templates containing literal `{` / `}` braces never collide
    with str.format() semantics.
"""


def _config(lang, lang_label, icon, header_desc, platform_note,
            analogies, mistakes, quiz_question, quiz_explanation,
            code_template, exercise_starter, output_example, code_comment,
            output_stmt, include_stmt="", main_header="", main_footer="", input_stmt="var = input()"):
    return {
        "lang": lang, "lang_label": lang_label, "icon": icon,
        "header_desc": header_desc, "platform_note": platform_note,
        "analogies": analogies, "mistakes": mistakes,
        "quiz_question": quiz_question, "quiz_explanation": quiz_explanation,
        "code_template": code_template, "exercise_starter": exercise_starter,
        "output_example": output_example, "code_comment": code_comment,
        "output_stmt": output_stmt, "include_stmt": include_stmt,
        "main_header": main_header, "main_footer": main_footer, "input_stmt": input_stmt,
    }


WEB_LANG_CONFIGS = {
    "html": _config(
        lang="html", lang_label="HTML", icon="🌐",
        header_desc="HTML is the markup language that structures every web page using tags and elements.",
        platform_note="The browser parses HTML into the DOM (Document Object Model) before rendering it.",
        analogies=[
            "Think of __CONCEPT__ as the blueprint of a building — it defines the rooms, not how they look.",
            "Like the bones of a skeleton, __CONCEPT__ gives the page its structure and meaning.",
        ],
        mistakes=[
            {"mistake": "Forgetting to close a tag when using __CONCEPT__",
             "fix": "Every opening tag needs a matching closing tag (except void elements like <img> and <br>) when using __CONCEPT__",
             "code": "<p>Hello world",
             "fixed_code": "<p>Hello world</p>"},
            {"mistake": "Using div instead of a semantic element for __CONCEPT__",
             "fix": "Prefer semantic tags like <article>, <section>, <nav> for __CONCEPT__ — they help accessibility and SEO",
             "code": "<div class=\"nav\">...",
             "fixed_code": "<nav>..."},
            {"mistake": "Missing alt text on images when using __CONCEPT__",
             "fix": "Always add a descriptive alt attribute for __CONCEPT__",
             "code": "<img src=\"photo.jpg\">",
             "fixed_code": "<img src=\"photo.jpg\" alt=\"A photo of a red panda\">"},
        ],
        quiz_question="What is the correct way to structure __CONCEPT__?",
        quiz_explanation="Use the proper tags and attributes so the browser and assistive technology can understand __CONCEPT__.",
        code_template="<section>\n  <h2>__CONCEPT__</h2>\n  <p>Example content for __CONCEPT__.</p>\n</section>",
        exercise_starter="<!-- Implement __CONCEPT__ -->\n",
        output_example="<p>Learning about __CONCEPT__</p>",
        code_comment="<!--",
        output_stmt="<p>{}</p>",
    ),
    "css": _config(
        lang="css", lang_label="CSS", icon="🎨",
        header_desc="CSS styles the web — selectors target elements, declarations set properties.",
        platform_note="The cascade, specificity, and inheritance decide which rule wins when conflicts occur.",
        analogies=[
            "Think of __CONCEPT__ as the interior designer — it decides colors, spacing, and layout.",
            "Like a paintbrush, __CONCEPT__ turns a plain HTML structure into a polished visual design.",
        ],
        mistakes=[
            {"mistake": "Misusing specificity when writing __CONCEPT__",
             "fix": "Keep specificity flat — prefer classes over IDs for __CONCEPT__ so rules are easy to override",
             "code": "#header h1 { color: red; }",
             "fixed_code": ".page-title { color: red; }"},
            {"mistake": "Forgetting units when using __CONCEPT__",
             "fix": "Most length properties need units (px, rem, %, vw) — unitless values fail silently for __CONCEPT__",
             "code": "margin: 10;",
             "fixed_code": "margin: 10px;"},
            {"mistake": "Using !important everywhere for __CONCEPT__",
             "fix": "Reserve !important for truly special cases — overusing it makes the cascade impossible to manage",
             "code": "p { color: red !important; }",
             "fixed_code": ".notice { color: red; }"},
        ],
        quiz_question="What determines which CSS rule wins for __CONCEPT__?",
        quiz_explanation="The cascade resolves conflicts by origin, specificity, and source order for __CONCEPT__.",
        code_template=".__CONCEPT__slug__ {\n  /* your __CONCEPT__ styles here */\n}",
        exercise_starter="/* Implement __CONCEPT__ */\n",
        output_example="/* Learning about __CONCEPT__ */",
        code_comment="/*",
        output_stmt="/* {} */",
    ),
    "sql": _config(
        lang="sql", lang_label="SQL", icon="🗄️",
        header_desc="SQL queries relational databases — SELECT reads, JOIN combines, aggregates summarize.",
        platform_note="SQL is declarative: you describe the result you want, the database engine figures out how.",
        analogies=[
            "Think of __CONCEPT__ as asking a librarian a precise question — you describe the answer, not the search steps.",
            "Like filtering a spreadsheet, __CONCEPT__ picks exactly the rows and columns you need.",
        ],
        mistakes=[
            {"mistake": "Filtering aggregates with WHERE instead of HAVING for __CONCEPT__",
             "fix": "WHERE filters rows before grouping; HAVING filters groups after aggregation for __CONCEPT__",
             "code": "SELECT dept, COUNT(*) FROM emp WHERE COUNT(*) > 5",
             "fixed_code": "SELECT dept, COUNT(*) FROM emp GROUP BY dept HAVING COUNT(*) > 5"},
            {"mistake": "Missing the join key when using __CONCEPT__",
             "fix": "Always specify the ON condition for __CONCEPT__ — a missing ON produces a Cartesian product",
             "code": "SELECT * FROM a JOIN b",
             "fixed_code": "SELECT * FROM a JOIN b ON a.id = b.a_id"},
            {"mistake": "Forgetting the semicolon with __CONCEPT__",
             "fix": "End statements with a semicolon so the engine knows where one query ends",
             "code": "SELECT * FROM users",
             "fixed_code": "SELECT * FROM users;"},
        ],
        quiz_question="Which clause summarizes data when using __CONCEPT__?",
        quiz_explanation="GROUP BY with aggregate functions (COUNT, SUM, AVG) collapses rows into groups for __CONCEPT__.",
        code_template="SELECT ... FROM ... WHERE ...;\n-- __CONCEPT__",
        exercise_starter="-- Implement __CONCEPT__\n",
        output_example="-- Learning about __CONCEPT__",
        code_comment="--",
        output_stmt="-- {}",
    ),
    "typescript": _config(
        lang="typescript", lang_label="TypeScript", icon="🔷",
        header_desc="TypeScript adds static types to JavaScript — caught at compile time, erased at runtime.",
        platform_note="Compiles to plain JavaScript; strict mode is what makes the type checker genuinely useful.",
        analogies=[
            "Think of __CONCEPT__ as a contract between teams — it states what each part expects and provides.",
            "Like spell-check before you hit send, __CONCEPT__ catches mistakes before the code ever runs.",
        ],
        mistakes=[
            {"mistake": "Using any to dodge the type system for __CONCEPT__",
             "fix": "Prefer unknown and narrow it, or define a real type for __CONCEPT__ — any defeats the purpose of TypeScript",
             "code": "const x: any = getData();",
             "fixed_code": "const x: ApiResponse = getData();"},
            {"mistake": "Forgetting strict mode when using __CONCEPT__",
             "fix": "Enable \"strict\": true in tsconfig so null checks and implicit-any rules protect you with __CONCEPT__",
             "code": "// tsconfig without strict",
             "fixed_code": "// \"strict\": true in compilerOptions"},
            {"mistake": "Confusing interface and type for __CONCEPT__",
             "fix": "interface extends cleanly; type aliases compose unions — pick deliberately for __CONCEPT__",
             "code": "type A = { x: number }; type B = A & { y: string };",
             "fixed_code": "interface A { x: number } interface B extends A { y: string }"},
        ],
        quiz_question="What does strict mode guarantee for __CONCEPT__?",
        quiz_explanation="strictNullChecks and noImplicitAny catch null/undefined access and untyped code at compile time for __CONCEPT__.",
        code_template="// __CONCEPT__\ntype Example = { value: string };\nconst demo: Example = { value: 'hi' };",
        exercise_starter="// Implement __CONCEPT__\n",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
    "react": _config(
        lang="react", lang_label="React", icon="⚛️",
        header_desc="React builds UIs from components — functions returning JSX, driven by props and state.",
        platform_note="Data flows down (props) and events flow up (callbacks). React re-renders when state changes.",
        analogies=[
            "Think of __CONCEPT__ as a recipe card — same ingredients (props), same dish (UI), every time.",
            "Like Lego bricks, __CONCEPT__ lets you compose small reusable pieces into complex interfaces.",
        ],
        mistakes=[
            {"mistake": "Mutating state directly when using __CONCEPT__",
             "fix": "Always update state immutably with the setter — mutation may not trigger a re-render for __CONCEPT__",
             "code": "state.items.push(newItem);",
             "fixed_code": "setState(prev => [...prev, newItem]);"},
            {"mistake": "Missing dependencies in useEffect for __CONCEPT__",
             "fix": "List every value the effect reads in the dependency array for __CONCEPT__",
             "code": "useEffect(() => { ... }, []); // uses count",
             "fixed_code": "useEffect(() => { ... }, [count]);"},
            {"mistake": "Calling hooks conditionally for __CONCEPT__",
             "fix": "Hooks must run in the same order every render — never inside if/loops for __CONCEPT__",
             "code": "if (x) { useState(0); }",
             "fixed_code": "useState(0); // always at top level"},
        ],
        quiz_question="Which rule keeps React hooks working for __CONCEPT__?",
        quiz_explanation="Hooks must be called at the top level, unconditionally, in the same order every render for __CONCEPT__.",
        code_template="// __CONCEPT__\nfunction Component() {\n  return <div>Example for __CONCEPT__</div>;\n}",
        exercise_starter="// Implement __CONCEPT__\nfunction App() {\n  return null;\n}",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
    "node": _config(
        lang="node", lang_label="Node.js", icon="🟢",
        header_desc="Node.js runs JavaScript on the server — event-driven, non-blocking, backed by npm.",
        platform_note="The event loop handles I/O asynchronously so a single process serves many connections.",
        analogies=[
            "Think of __CONCEPT__ as a kitchen with many waiters — the chef (event loop) never blocks on one order.",
            "Like a manager delegating tasks, __CONCEPT__ lets I/O complete in the background while code keeps running.",
        ],
        mistakes=[
            {"mistake": "Blocking the event loop with sync I/O for __CONCEPT__",
             "fix": "Use the async APIs (fs/promises, await) instead of *Sync versions for __CONCEPT__ in a server",
             "code": "const data = fs.readFileSync('big.txt');",
             "fixed_code": "const data = await readFile('big.txt');"},
            {"mistake": "Not catching promise rejections with __CONCEPT__",
             "fix": "Wrap async handlers in try/catch or forward errors to error middleware for __CONCEPT__",
             "code": "app.get('/x', async (req, res) => { await db.find() });",
             "fixed_code": "app.get('/x', async (req, res, next) => { try { await db.find() } catch (e) { next(e) } });"},
            {"mistake": "Forgetting next() in middleware for __CONCEPT__",
             "fix": "Always call next() (or respond) so the request is not left hanging when using __CONCEPT__",
             "code": "app.use((req, res) => { console.log('log'); });",
             "fixed_code": "app.use((req, res, next) => { console.log('log'); next(); });"},
        ],
        quiz_question="Why does Node use an event loop for __CONCEPT__?",
        quiz_explanation="The event loop delegates blocking I/O to the OS and runs callbacks when data is ready, keeping the process responsive.",
        code_template="// __CONCEPT__\nconst result = await getData();\nconsole.log(result);",
        exercise_starter="// Implement __CONCEPT__\n",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
    "javascript": _config(
        lang="javascript", lang_label="JavaScript", icon="🟨",
        header_desc="JavaScript powers the interactive web — dynamically typed, prototype-based, async-first.",
        platform_note="Runs in the browser and Node.js; the event loop keeps single-threaded code responsive.",
        analogies=[
            "Think of __CONCEPT__ as a Swiss Army knife — one tool, many uses, always at hand.",
            "Like a live conversation, __CONCEPT__ reacts to what happens in real time.",
        ],
        mistakes=[
            {"mistake": "Using == instead of === when checking __CONCEPT__",
             "fix": "Always use === to avoid unexpected type coercion when comparing __CONCEPT__",
             "code": "if (x == '5')",
             "fixed_code": "if (x === '5')"},
            {"mistake": "Overusing var when writing __CONCEPT__",
             "fix": "Use const by default and let only when reassigning for __CONCEPT__",
             "code": "var count = 0;",
             "fixed_code": "let count = 0;"},
            {"mistake": "Forgetting to await promises with __CONCEPT__",
             "fix": "Always await (or .then) promises — forgetting gives you a pending Promise, not the value",
             "code": "const user = fetch('/api/user');",
             "fixed_code": "const user = await fetch('/api/user');"},
        ],
        quiz_question="What is the safest way to compare values for __CONCEPT__?",
        quiz_explanation="Strict equality (===) compares type and value without coercion, avoiding surprises for __CONCEPT__.",
        code_template="// __CONCEPT__\nfunction example() {\n  // your __CONCEPT__ code here\n}",
        exercise_starter="// Implement __CONCEPT__\n",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
    "go": _config(
        lang="go", lang_label="Go", icon="🔵",
        header_desc="Go is a statically typed, compiled language built for concurrency and simple tooling.",
        platform_note="Goroutines + channels make concurrency first-class; gofmt enforces one canonical style.",
        analogies=[
            "Think of __CONCEPT__ as a well-organized toolbox — everything has its place and works predictably.",
            "Like a highway with dedicated lanes, __CONCEPT__ lets many tasks run without colliding.",
        ],
        mistakes=[
            {"mistake": "Ignoring the returned error for __CONCEPT__",
             "fix": "Go uses explicit error returns — check and handle them, or wrap with fmt.Errorf for __CONCEPT__",
             "code": "f, _ := os.Open(\"file\")",
             "fixed_code": "f, err := os.Open(\"file\")\nif err != nil { return err }"},
            {"mistake": "Using := outside a function for __CONCEPT__",
             "fix": "Short declaration only works inside functions — use var at package level for __CONCEPT__",
             "code": "count := 0 // top level",
             "fixed_code": "var count = 0"},
            {"mistake": "Not running gofmt when writing __CONCEPT__",
             "fix": "Run gofmt so the whole team shares one formatting standard for __CONCEPT__",
             "code": "// misaligned code",
             "fixed_code": "// gofmt-clean code"},
        ],
        quiz_question="How does Go handle errors with __CONCEPT__?",
        quiz_explanation="Go returns errors as explicit values and expects you to check them — no exceptions for __CONCEPT__.",
        code_template="// __CONCEPT__\nfunc main() {\n  // your __CONCEPT__ code here\n}",
        exercise_starter="// Implement __CONCEPT__\npackage main\n\nfunc main() {}",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
    "rust": _config(
        lang="rust", lang_label="Rust", icon="🦀",
        header_desc="Rust delivers memory safety without garbage collection through ownership and borrowing.",
        platform_note="The borrow checker enforces safety at compile time; zero-cost abstractions keep runtime fast.",
        analogies=[
            "Think of __CONCEPT__ as a library with a strict checkout system — every reference knows who owns it.",
            "Like a traffic controller, __CONCEPT__ guarantees exactly one owner so nothing is double-freed.",
        ],
        mistakes=[
            {"mistake": "Borrowing mutably and immutably at once for __CONCEPT__",
             "fix": "You cannot hold immutable and mutable references simultaneously — reorder or clone for __CONCEPT__",
             "code": "let a = &x; let b = &mut x;",
             "fixed_code": "let a = &x; drop(a); let b = &mut x;"},
            {"mistake": "Forgetting the comma between match arms for __CONCEPT__",
             "fix": "Match arms that are expressions need commas between arms for __CONCEPT__",
             "code": "match x { 1 => println!(\"one\") 2 => println!(\"two\") }",
             "fixed_code": "match x { 1 => println!(\"one\"), 2 => println!(\"two\"), }"},
            {"mistake": "Using unwrap on Option/Result blindly for __CONCEPT__",
             "fix": "Prefer pattern matching or ? to handle None/Err gracefully for __CONCEPT__",
             "code": "let v = map.get(&key).unwrap();",
             "fixed_code": "let Some(v) = map.get(&key) else { return; };"},
        ],
        quiz_question="What does the borrow checker enforce for __CONCEPT__?",
        quiz_explanation="It guarantees references never outlive their data and prevents data races at compile time for __CONCEPT__.",
        code_template="// __CONCEPT__\nfn main() {\n    // your __CONCEPT__ code here\n}",
        exercise_starter="// Implement __CONCEPT__\nfn main() {}",
        output_example="// Learning about __CONCEPT__",
        code_comment="//",
        output_stmt="// {}",
    ),
}


def get_web_language_config(language_id):
    """Return the content config for a web/modern language, or None."""
    return WEB_LANG_CONFIGS.get(language_id)


def _extract_concept(title: str) -> str:
    """Extract the main concept keyword (or short phrase) from a lesson title."""
    t = title.lower()
    for ch in "():\u2014\u2013":
        t = t.replace(ch, " ")
    t = t.replace("-", " ")
    words = t.split()
    skip = ["practice", "challenge", "project", "lab", "review", "blitz",
            "builder", "hunt", "quick", "session", "theory", "deep", "dive",
            "mastery", "master", "fundamentals", "introduction", "concepts",
            "overview", "implementation", "in", "with", "from", "that", "this",
            "your", "into", "what", "core", "mini", "pro", "for", "and", "of",
            "the", "a", "an", "to", "using", "lesson", "clause", "statement"]
    # compound terms worth keeping together
    keep_next = {"inner", "left", "right", "outer", "full", "group", "order",
                 "primary", "foreign", "natural", "cross"}
    keep_after = {"join", "by", "key", "id", "table"}
    kept = []
    for i, w in enumerate(words):
        if w in skip and w not in keep_next:
            continue
        kept.append(w)
        if w in keep_next:
            continue
        if w in keep_after:
            continue
        break
    concept = " ".join(kept)
    if concept:
        return concept
    return words[-1] if words else title


def _fill(value, concept, lang_label):
    """Replace the __CONCEPT__ token and (optionally) slugify for class names."""
    if isinstance(value, dict):
        return {k: _fill(v, concept, lang_label) for k, v in value.items()}
    if isinstance(value, list):
        return [_fill(v, concept, lang_label) for v in value]
    if not isinstance(value, str):
        return value
    slug = concept.lower().replace(" ", "-").replace("'", "")
    return value.replace("__CONCEPT__slug__", slug).replace("__CONCEPT__", concept)


def generate_web_template_content(
    language_id: str,
    lesson_title: str,
    lesson_type: str,
) -> dict[str, object]:
    """Generate W3Schools-depth lesson content for a web/modern language."""
    config = get_web_language_config(language_id)
    if not config:
        raise ValueError(f"No config for language {language_id}")

    concept = _extract_concept(lesson_title)
    lang_label = config["lang_label"]
    fill = lambda v: _fill(v, concept, lang_label)

    theory_by_type = {
        "theory": (
            f"{config['header_desc']} This lesson focuses on {concept} — one of the "
            f"core building blocks you will use in almost every {lang_label} project."
        ),
        "practice": (
            f"Time to practice {concept}. The best way to learn {lang_label} is by writing "
            f"code, so this hands-on session applies what you have learned about {concept} "
            f"to real problems."
        ),
        "challenge": (
            f"Challenge yourself with {concept}. This problem tests your understanding and "
            f"pushes you to think creatively. Try to solve it before peeking at hints!"
        ),
        "project": (
            f"Build a project using {concept}. Combine it with everything else you have "
            f"learned to create something real and complete."
        ),
        "boss": (
            f"Boss battle! This comprehensive challenge tests everything you have learned "
            f"about {concept} and related topics. Show what you have mastered!"
        ),
        "quiz": (
            f"Test your knowledge of {concept} with these questions. Quizzes reinforce "
            f"what you have learned and reveal what to review."
        ),
    }

    is_project = lesson_type == "project"

    mistakes = config["mistakes"]
    quiz_first = {
        "question": fill(config["quiz_question"]),
        "options": [
            f"To use {concept} properly in {lang_label}",
            f"To replace variables with {concept}",
            f"To make programs run faster automatically",
            f"To delete unnecessary code",
        ],
        "correct": 0,
        "explanation": fill(config["quiz_explanation"]),
    }
    quiz_second = {
        "question": f"Which practice should you follow when working with {concept}?",
        "options": [
            fill(mistakes[0]["fix"]) if mistakes else f"Follow {lang_label} best practices for {concept}",
            f"Ignore edge cases in {concept}",
            f"Use {concept} without reading the docs",
            f"Copy-paste {concept} code without understanding it",
        ],
        "correct": 0,
        "explanation": f"Reviewing the common mistakes above shows the recommended way to apply {concept}.",
    }
    quiz_third = {
        "question": f"Your {lang_label} code using {concept} is not working. What is the best first step?",
        "options": [
            f"Check the {concept} syntax and test with a minimal example",
            f"Rewrite the entire program from scratch",
            f"Delete the code and move on",
            f"Add more {concept} everywhere until it works",
        ],
        "correct": 0,
        "explanation": f"Debugging {concept} starts with a minimal reproduction and verifying the syntax.",
    }
    quizzes = [] if is_project else [quiz_first, quiz_second, quiz_third]

    exercises = [
        {
            "description": (
                f"Warm-up: write the simplest possible {lang_label} snippet that uses {concept}. "
                f"Get it running first — correctness beats elegance."
            ),
            "starter_code": fill(config["exercise_starter"]),
            "hints": [
                f"Review the basic {concept} syntax first",
                f"Keep the warm-up to 5-10 lines",
                f"Print or render something visible so you can verify it works",
            ],
            "expected_output": fill(config["output_example"]),
        },
        {
            "description": (
                f"Main task: build a small {lang_label} feature that applies {concept} to a "
                f"realistic input. Handle at least two different cases."
            ),
            "starter_code": fill(config["exercise_starter"]),
            "hints": [
                f"Plan the input and expected output for {concept} first",
                f"Split the task into small steps and test each one",
                f"Combine {concept} with related {lang_label} features",
            ],
            "expected_output": f"Your feature should correctly apply {concept} and handle edge cases.",
        },
        {
            "description": (
                f"Stretch: extend your solution so it handles edge cases and integrates "
                f"{concept} with another {lang_label} feature. Think about what a real "
                f"project would need."
            ),
            "starter_code": fill(config["exercise_starter"]),
            "hints": [
                f"List at least two edge cases for {concept}",
                f"Refactor your solution into a reusable function or component",
                f"Add comments explaining your {concept} decisions",
            ],
            "expected_output": f"Your extended solution should handle edge cases gracefully and be reusable.",
        },
    ]

    project_brief = {
        "brief": (
            f"Build a complete {lang_label} project centered on {concept}. Make it real, "
            f"runnable, and polished enough to show off."
        ),
        "phases": [
            {
                "title": "1. Setup & scaffold",
                "tasks": [
                    f"Create the project structure for a {lang_label} project",
                    f"Add a README describing the {concept}-based project",
                    f"Wire up a minimal working shell that runs end-to-end",
                    f"Commit your initial scaffold",
                ],
            },
            {
                "title": "2. Core feature",
                "tasks": [
                    f"Implement the main feature built on {concept}",
                    f"Handle the primary happy path first, then one edge case",
                    f"Test the feature with real inputs",
                    f"Refactor any duplicated {concept} code into helpers",
                ],
            },
            {
                "title": "3. Polish & ship",
                "tasks": [
                    "Add error handling and graceful failure paths",
                    "Write a short usage guide (how to run, what it does)",
                    "Review the code for readability and remove dead code",
                    "Final run: demo the complete project",
                ],
            },
        ],
        "checklist": [
            f"Project runs without errors using {concept}",
            "Core feature works for the happy path",
            "At least one edge case is handled",
            "Code is readable and commented where needed",
            "README explains how to run and what the project does",
        ],
        "deliverables": [
            f"A working {lang_label} project that demonstrates {concept}",
            "At least two tests or manual verification runs",
            "A short write-up of design decisions",
        ],
    }

    return {
        "theory": theory_by_type.get(lesson_type, f"Learn about {concept} in {lang_label}."),
        "analogy": fill(config["analogies"][0]),
        "sections": [
            {
                "heading": f"Understanding {concept}",
                "body": (
                    f"When working with {concept} in {lang_label}, first understand the core "
                    f"idea and syntax. Then practice with small examples. Finally, combine "
                    f"{concept} with other features to build something bigger."
                ),
                "code": fill(config["code_template"]),
                "pro_tip": (
                    f"Start with the simplest {concept} example and add complexity "
                    f"step by step, testing as you go."
                ),
            },
            {
                "heading": f"How {concept} works",
                "body": (
                    f"{config['platform_note']} This is exactly why {concept} behaves the way it "
                    f"does in {lang_label} — understanding the mechanism beats memorizing syntax."
                ),
                "code": fill(config["code_template"]),
                "pro_tip": (
                    f"Change one part of the {concept} example at a time and observe the result "
                    f"to build an intuition."
                ),
            },
            {
                "heading": f"Common uses of {concept}",
                "body": (
                    f"{config['header_desc']} Professionals use {concept} constantly in real "
                    f"projects. Master it and you add a powerful tool to your {lang_label} toolkit."
                ),
                "code": fill(config["code_template"]),
                "pro_tip": (
                    f"Write at least three different {lang_label} programs that use "
                    f"{concept} in different ways."
                ),
            },
            {
                "heading": f"{lang_label} specific notes",
                "body": f"{config['platform_note']} Keep this in mind whenever you use {concept}.",
                "pro_tip": f"Read the {lang_label} docs for {concept} to go even deeper.",
            },
        ],
        "code_example": {
            "code": fill(config["code_template"]),
            "annotations": [
                {"line": 1, "text": f"Example that demonstrates {concept}"},
                {"line": 2, "text": f"Each line builds on the previous one"},
            ],
        },
        "common_mistakes": [fill(m) for m in config["mistakes"]],
        "exercise": exercises[0] if exercises else None,
        "exercises": exercises,
        "quiz": quiz_first if quizzes else None,
        "quizzes": quizzes,
        "project": project_brief if is_project else None,
        "key_takeaways": [
            f"{concept} is a core {lang_label} concept used in real projects",
            f"Practice with {concept} builds mastery faster than passive reading",
            f"Combine {concept} with related features for powerful results",
            f"{config['platform_note']}",
            f"Real projects exercise {concept} in many small ways — build to learn",
        ],
        "next_steps": f"Great progress! Keep practicing {concept} in your own {lang_label} projects.",
    }
