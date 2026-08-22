"""Study Library — in-depth blog-style study articles for the Learning Hub.

Each article mirrors the depth of W3Schools / freeCodeCamp tutorials:
the deep-dive theory, a real analogy, worked code, common mistakes,
practice exercises, and key takeaways. Organized by category so the
frontend can render a W3Schools-style table of contents.

Categories follow the Scrimba full-stack path + freeCodeCamp certifications:
  - html-css     Web foundations
  - javascript   The language of the web
  - typescript   Typed JavaScript
  - react        Component UIs
  - node         Backend & APIs
  - sql          Data & persistence
  - full-stack   End-to-end building
"""

from typing import Any


def _article(
    article_id: str,
    title: str,
    category: str,
    summary: str,
    level: str,
    read_time_min: int,
    related_topics: list[str],
    sections: list[dict[str, Any]],
    key_takeaways: list[str],
    tag: str = "",
    quiz: list[dict[str, Any]] | None = None,
    exercise: dict[str, Any] | None = None,
    curriculum: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": article_id,
        "title": title,
        "category": category,
        "summary": summary,
        "level": level,
        "read_time_min": read_time_min,
        "related_topics": related_topics,
        "sections": sections,
        "key_takeaways": key_takeaways,
        "tag": tag,
        "quiz": quiz or [],
        "exercise": exercise,
        "curriculum": curriculum or [],
    }


def _section(heading: str, body: str, code: str | None = None, pro_tip: str = ""):
    s: dict[str, Any] = {"heading": heading, "body": body}
    if code:
        s["code"] = code
    if pro_tip:
        s["pro_tip"] = pro_tip
    return s


def _quiz(question: str, options: list[str], answer: int, explanation: str) -> dict[str, Any]:
    """A multiple-choice question. `answer` is the index of the correct option (0-based)."""
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


def _exercise(
    title: str,
    task: str,
    starter: str,
    solution: str,
    hint: str = "",
) -> dict[str, Any]:
    """A hands-on coding exercise. `starter` is what the user edits; `solution` is the answer."""
    ex: dict[str, Any] = {
        "title": title,
        "task": task,
        "starter": starter,
        "solution": solution,
    }
    if hint:
        ex["hint"] = hint
    return ex


STUDY_CATEGORIES = [
    {"id": "html-css", "name": "HTML & CSS", "icon": "🎨", "color": "#E34F26",
     "description": "Structure and style the web — from your first tag to responsive layouts."},
    {"id": "javascript", "name": "JavaScript", "icon": "🟨", "color": "#F7DF1E",
     "description": "The language of the browser — variables, functions, async, DOM."},
    {"id": "typescript", "name": "TypeScript", "icon": "🔷", "color": "#3178C6",
     "description": "Types on top of JavaScript — interfaces, generics, strict mode."},
    {"id": "react", "name": "React", "icon": "⚛️", "color": "#61DAFB",
     "description": "Component-driven UI — hooks, state, effects, performance."},
    {"id": "node", "name": "Node.js", "icon": "🟢", "color": "#339933",
     "description": "JavaScript on the server — Express, files, streams, databases."},
    {"id": "sql", "name": "SQL & Databases", "icon": "🗄️", "color": "#4479A1",
     "description": "Model and query data — SELECT, JOINs, indexing, normalization."},
    {"id": "c-programming", "name": "C Programming", "icon": "⚙️", "color": "#6B7280",
     "description": "The foundation of modern systems — pointers, memory, files, enums."},
    {"id": "full-stack", "name": "Full-Stack Projects", "icon": "🚀", "color": "#8B5CF6",
     "description": "End-to-end builds that tie the whole path together."},
]


ARTICLES: list[dict[str, Any]] = [
    # ────────────────────────── HTML & CSS ──────────────────────────
    _article(
        "html-basics",
        "HTML Basics: The Skeleton of Every Web Page",
        "html-css",
        "HTML is not a programming language — it is the markup that gives every web page its structure. Learn the document skeleton, semantic tags, and why the browser renders what it renders.",
        "beginner", 10, ["html-structure", "html-semantic", "css-basics"],
        [
            _section(
                "What HTML actually is",
                "HTML (HyperText Markup Language) describes the structure of a page using tags. The browser reads those tags and builds a tree of elements — the DOM. HTML has no logic: no if/else, no loops. That logic lives in JavaScript. Your job with HTML is to choose the right tags so the meaning (semantics) of the content is clear to both humans and machines.",
                "<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset=\"UTF-8\">\n    <title>My Page</title>\n  </head>\n  <body>\n    <h1>Hello, world!</h1>\n    <p>This is a paragraph.</p>\n  </body>\n</html>",
            ),
            _section(
                "The document skeleton",
                "Every modern page starts with <!DOCTYPE html> — a hint that tells the browser to render in standards mode, not quirks mode. Inside <html> you get <head> (metadata: title, charset, links to CSS) and <body> (everything visible). Get this skeleton right once and reuse it forever.",
                "boilerplate",
            ),
            _section(
                "Semantic tags over div soup",
                "Prefer <header>, <nav>, <main>, <section>, <article>, <aside>, <footer> over a pile of <div>s. Semantic tags give free accessibility and SEO: screen readers announce them, and search engines understand your page's structure. A <div> says nothing; <article> says 'this is self-contained content'.",
                "<nav>  <a href=\"/\">Home</a>  <a href=\"/about\">About</a></nav>\n<main>  <article>    <h2>Post title</h2>    <p>Post body...</p>  </article></main>",
                "If a screen-reader user can't navigate your page, neither can search engines. Semantics are not optional decoration.",
            ),
            _section(
                "Attributes and self-closing tags",
                "Tags carry attributes: id, class, href, src, alt, data-*. Void elements like <img>, <br>, <input>, <meta> have no closing tag. Always give images an alt attribute — it is read aloud by screen readers and shown when an image fails to load.",
                "<img src=\"photo.jpg\" alt=\"A red panda climbing a branch\" width=\"400\">\n<a href=\"https://example.com\" target=\"_blank\">Example</a>\n<input type=\"email\" placeholder=\"you@example.com\" required>",
            ),
        ],
        [
            "HTML is markup, not logic — it defines structure and meaning",
            "The head holds metadata, the body holds visible content",
            "Semantic tags improve accessibility and SEO for free",
            "Attributes configure elements; alt text is mandatory for images",
        ],
        "first-steps",
    ),
    _article(
        "css-basics",
        "CSS Fundamentals: The Box Model, Selectors, and the Cascade",
        "html-css",
        "CSS is how you make the web beautiful. Understand the box model, how selectors match elements, and — most importantly — how the cascade decides which rule wins.",
        "beginner", 14, ["css-selectors", "css-flexbox", "html-basics"],
        [
            _section(
                "The box model",
                "Every element is a box with four layers: content, padding, border, and margin. Content holds the text; padding adds space inside the border; margin adds space outside it. With box-sizing: border-box, width includes padding and border, which is almost always what you want. Debug layout problems by first asking 'which box is this?'.",
                "/* Reset is the most common first line of any project */\n* {\n  box-sizing: border-box;\n}\n\n.card {\n  width: 300px;\n  padding: 16px;   /* inside the border */\n  border: 1px solid #ddd;\n  margin: 12px;     /* outside the border */\n}",
            ),
            _section(
                "Selectors and specificity",
                "Selectors target elements: type (p), class (.card), id (#hero), attribute ([type=\"email\"]), and combinators (nav > a, section p). The cascade resolves conflicts by specificity, then source order. A dirty trick: when a rule 'won't apply', you are usually losing the specificity war — not the class-name war.",
                "nav > a { color: #fff; }          /* direct child */\nsection p { line-height: 1.6; }      /* descendant */\na:hover { text-decoration: underline; }",
                "A quick specificity scale: inline styles > id > class > type. When debugging, count the specificity, not the CSS.",
            ),
            _section(
                "Colors, typography, and units",
                "Use rem for font sizes (it scales with the root font-size and respects user settings), px for borders, and % or flex/grid for layout. Contrast matters: pick text colors that pass at least WCAG AA (4.5:1 for normal text).",
                "body {\n  font-family: system-ui, sans-serif;\n  font-size: 1rem;\n  color: #1a1a1a;          /* near-black on white */\n  background: #ffffff;\n}\n\nh1 { font-size: 2.5rem; }\np  { line-height: 1.7; }",
            ),
            _section(
                "The cascade, inheritance, and !important",
                "Styles inherit down the tree (color, font) or not (margin, padding). The cascade resolves in this order: origin → specificity → source order. Reserve !important for genuinely un-overridable cases (user stylesheets) — using it everywhere creates rules you can no longer fight.",
                ".btn { color: white; }          /* specificity 0,1,0 */\nbody .btn { color: black; }      /* specificity 0,2,0 — wins */\n#app .btn { color: red; }        /* specificity 1,1,0 — wins harder */",
            ),
        ],
        [
            "Every element is a box: content, padding, border, margin",
            "Prefer border-box so width includes padding and border",
            "The cascade resolves conflicts by specificity, then source order",
            "Use rem for text and semantic units everywhere else",
        ],
        "first-steps",
    ),
    _article(
        "css-flexbox-grid",
        "Flexbox and Grid: The Modern Layout Engines",
        "html-css",
        "Float-based layouts are dead. Learn flexbox for one-dimensional alignment and grid for two-dimensional layouts, and know when to reach for each.",
        "intermediate", 18, ["css-basics", "css-responsive"],
        [
            _section(
                "Flexbox: one axis, powerful alignment",
                "A flex container lays children along a main axis (flex-direction) and wraps the cross axis. The magic is alignment: justify-content for the main axis, align-items for the cross axis. This one mental model replaces vertical-centering hacks forever.",
                ".navbar {\n  display: flex;\n  justify-content: space-between; /* main axis */\n  align-items: center;            /* cross axis */\n  gap: 16px;\n}\n\n.center-forever {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}",
                "gap works in both flex and grid in every modern browser — stop using margin hacks for spacing.",
            ),
            _section(
                "Grid: rows and columns together",
                "Grid defines a track layout (rows + columns) and places items into it. Use grid-template-columns for the column skeleton, and grid-template-areas to make the whole layout readable at a glance. Grid is two-dimensional; flex is one-dimensional. That's the whole decision rule.",
                ".layout {\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  grid-template-areas:\n    \"header header\"\n    \"sidebar main\"\n    \"footer footer\";\n}\n\n.sidebar { grid-area: sidebar; }\n.main    { grid-area: main; }",
            ),
            _section(
                "Responsive: think fluid first",
                "Start with the mobile layout, then use min-width media queries to enhance. Prefer auto-fit/auto-fill with minmax() so grids shrink gracefully without media queries at all.",
                ".cards {\n  display: grid;\n  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));\n  gap: 16px;\n}\n\n@media (min-width: 768px) {\n  .sidebar { display: block; }\n}",
            ),
        ],
        [
            "Flexbox for one axis, grid for two",
            "justify-content aligns the main axis, align-items the cross axis",
            "minmax + auto-fill makes responsive grids without media queries",
            "Mobile-first: design narrow, then enhance with min-width queries",
        ],
    ),
    _article(
        "css-responsive",
        "Responsive Design: One Site, Every Screen",
        "html-css",
        "Responsive design is not a technique, it's a default. Media queries, fluid units, and mobile-first thinking keep your layout usable from a 320px phone to a 4K monitor.",
        "intermediate", 16, ["css-flexbox-grid", "html-basics"],
        [
            _section(
                "Mobile-first strategy",
                "Write the base CSS for the smallest screen, then layer on enhancements with min-width media queries. Mobile-first naturally keeps the core fast and avoids fighting to 'remove' desktop styles.",
                "/* Base: single column, big tap targets */\n.actions { display: flex; flex-direction: column; gap: 8px; }\n\n/* Tablet and up */\n@media (min-width: 600px) {\n  .actions { flex-direction: row; }\n}",
            ),
            _section(
                "Fluid type and spacing",
                "clamp() sets a size that scales with the viewport while respecting hard min/max bounds. Combine it with the viewport unit vw for type that never needs a media query.",
                "h1 {\n  font-size: clamp(1.5rem, 1rem + 3vw, 3rem);\n}",
                "clamp(MIN, PREFERRED, MAX) — preferred is usually a vw-based value so text scales with the screen.",
            ),
            _section(
                "Images and containers",
                "Cap layout width (max-width: 1200px with a centered margin), make images width: 100% with height: auto so they never blow out their container, and use the picture element or srcset for device-appropriate resolution.",
                "img {\n  max-width: 100%;\n  height: auto;\n}\n\n.container {\n  max-width: 1200px;\n  margin-inline: auto;\n  padding-inline: 16px;\n}",
            ),
        ],
        [
            "Design mobile-first, enhance with min-width queries",
            "clamp() gives fluid type without media queries",
            "Images should never exceed their container",
            "Center content with margin-inline: auto and a max-width",
        ],
    ),

    # ────────────────────────── JavaScript ──────────────────────────
    _article(
        "js-variables-types",
        "JavaScript Variables and Data Types",
        "javascript",
        "let, const, and var do different jobs. Combined with JavaScript's dynamic typing, coercing rules, and the seven primitive types, this is the foundation everything else stands on.",
        "beginner", 12, ["js-functions", "js-arrays-objects"],
        [
            _section(
                "let vs const vs var",
                "Use const by default, let when you must reassign, and never var in modern code. const does not mean immutable — it means the binding cannot be reassigned. Objects and arrays declared with const can still be mutated.",
                "const name = 'Ada';       // binding, cannot be reassigned\nlet score = 0;              // can be reassigned\nscore = 10;                 // ok\n\nconst user = { role: 'admin' };\nuser.role = 'viewer';       // ok — object is mutable",
            ),
            _section(
                "The seven primitive types",
                "string, number, bigint, boolean, undefined, symbol, null. Everything else — objects, arrays, functions, dates — is an object. typeof is your introspection tool, but it has a famous quirk: typeof null === 'object'.",
                "typeof 'hi'     // 'string'\ntypeof 42       // 'number'\ntypeof true     // 'boolean'\ntypeof undefined// 'undefined'\ntypeof null     // 'object'  ← the famous bug\n",
                "use Number.isNaN(x) instead of global isNaN() — the global coerces first and misleads you.",
            ),
            _section(
                "Type coercion: know the rules",
                "JavaScript coerces types in comparisons and arithmetic. The == operator coerces; === does not. Always use === and !==, and be explicit with String(), Number(), Boolean() when you mean to convert.",
                "5 == '5'    // true  — coerced\n5 === '5'   // false — no coercion\n\nNumber('42')      // 42\nBoolean('')       // false\nBoolean('hello')  // true — non-empty string is truthy",
            ),
            _section(
                "Truthy and falsy",
                "Six falsy values: false, 0, '', null, undefined, NaN. Everything else is truthy, including '0' (a string), [], and {}. Truthiness drives if/else, &&, ||, and the nullish operator ??.",
                "const value = user?.email ?? 'anonymous';\n// ?? only falls through on null/undefined\n// || falls through on ANY falsy value",
            ),
        ],
        [
            "const by default, let when reassigning, never var",
            "Prefer === and explicit conversion over accidental coercion",
            "Six falsy values: false, 0, '', null, undefined, NaN",
            "?? checks null/undefined only; || checks all falsy values",
        ],
    ),
    _article(
        "js-functions",
        "Functions, Scope, and Closures",
        "javascript",
        "Functions are the heart of JavaScript. Understand declarations vs arrows, the this-binding rules, and closures — the mechanism that powers event handlers, hooks, and a thousand interview questions.",
        "intermediate", 16, ["js-arrays-objects", "js-async"],
        [
            _section(
                "Declarations vs arrow functions",
                "function declarations hoist; arrow functions do not bind their own this. Use arrows for callbacks and array methods; use function declarations for named reusable logic you may call before its definition.",
                "// Hoisted — callable before its line\nsayHi('Ada');\nfunction sayHi(name) {\n  return `Hi, ${name}`;\n}\n\n// Not hoisted — this would throw\nconst greet = (name) => `Hi, ${name}`;",
            ),
            _section(
                "Scope and hoisting",
                "var is function-scoped; let and const are block-scoped. 'Temporal dead zone' just means: a let/const variable exists in its block from the top, but you can't touch it before its declaration line.",
                "if (true) {\n  var leaked = 'var leaks out';\n  let blocked = 'let stays inside';\n}\nconsole.log(leaked);   // works\nconsole.log(blocked);  // ReferenceError",
            ),
            _section(
                "Closures: functions that remember",
                "A closure is a function bundled with the variables in scope at creation time. Even after the outer function returns, the inner function keeps access to those bindings. This powers counters, memoization, and React's useEffect dependencies.",
                "function createCounter() {\n  let count = 0;\n  return () => ++count;  // closes over `count`\n}\n\nconst counter = createCounter();\ncounter(); // 1\ncounter(); // 2  // count survives",
                "If you can answer 'why does the counter remember count?', you understand closures.",
            ),
            _section(
                "this: it depends on how you call",
                "this is not lexically bound (except in arrows). It is determined by the call site: method call → the object; plain call → undefined in strict mode; new → the new instance. Bind it explicitly with .bind(), .call(), .apply() when needed.",
                "const obj = {\n  name: 'object',\n  greet() { return `Hi from ${this.name}`; }\n};\nobj.greet();              // Hi from object\nconst lone = obj.greet;\nlone();                   // this is undefined (strict) — no object to bind",
            ),
        ],
        [
            "Arrows for callbacks, declarations for hoisted reusable logic",
            "let/const are block-scoped; var leaks out of blocks",
            "A closure keeps access to its creation-time scope",
            "this depends on the call site, not the definition",
        ],
    ),
    _article(
        "js-arrays-objects",
        "Arrays and Objects: The Data Workhorses",
        "javascript",
        "Arrays store ordered lists; objects store keyed data. Master the modern methods — map, filter, reduce, find — and destructuring, and you'll write data pipelines instead of for-loop spaghetti.",
        "intermediate", 15, ["js-functions", "js-variables-types"],
        [
            _section(
                "Array methods that replace loops",
                "map transforms every element, filter keeps elements that pass a test, reduce collapses a list to one value, find returns the first match, some/every answer yes/no questions. Chain them — each returns a new array and never mutates the original.",
                "const prices = [10, 20, 30, 40];\n\nconst withTax = prices.map(p => p * 1.2);\nconst affordable = prices.filter(p => p <= 30);\nconst total = prices.reduce((sum, p) => sum + p, 0);\nconst firstBig = prices.find(p => p > 25);",
                "reduce without an initial value throws on an empty array — always pass the seed.",
            ),
            _section(
                "Mutating vs non-mutating",
                "push, pop, shift, unshift, splice mutate in place. concat, slice, map, filter, spread return new arrays. Mutating shared state causes bugs nobody can trace — prefer producing new arrays.",
                "const copy = [...original, newItem];   // new array, original untouched\nconst rest = original.slice(1);             // drop first item, non-mutating\noriginal.push(newItem);                     // mutates in place",
            ),
            _section(
                "Objects and destructuring",
                "Destructuring unpacks properties into variables in one line — for objects and arrays, including nested and with defaults. The spread operator copies properties when building new objects.",
                "const user = { name: 'Ada', age: 36, role: 'dev' };\nconst { name, role = 'unknown' } = user;\nconst updated = { ...user, age: 37 };\n\nconst [head, ...tail] = [1, 2, 3, 4];",
            ),
            _section(
                "Object identity and references",
                "Objects compare by reference, not value. Two objects with identical fields are still different objects. Copy carefully: {...obj} is shallow — nested objects are still shared.",
                "const a = { n: 1 };\nconst b = { n: 1 };\nconsole.log(a === b); // false — different references\n\nconst shallow = { ...a };   // top level copied\nshallow.n = 99;             // a.n unaffected\n",
            ),
        ],
        [
            "map/filter/reduce replace loops and read better",
            "Prefer producing new arrays over mutating shared ones",
            "Destructuring + spread make data juggling one-liners",
            "Objects compare by reference; spread copies are shallow",
        ],
    ),
    _article(
        "js-async",
        "Async JavaScript: Callbacks, Promises, and async/await",
        "javascript",
        "The event loop never blocks. Promises and async/await make asynchronous code read like synchronous code, and error handling finally becomes linear.",
        "advanced", 18, ["js-functions", "js-arrays-objects"],
        [
            _section(
                "Why async matters",
                "Browsers run JavaScript on a single thread. If that thread blocked on a network call, the whole page would freeze. So I/O is async: the thread keeps working, and your continuation runs when the data arrives.",
                "console.log('start');\nsetTimeout(() => console.log('timeout'), 0);\nPromise.resolve().then(() => console.log('microtask'));\nconsole.log('end');\n// start, end, microtask, timeout",
            ),
            _section(
                "Promises in one mental model",
                "A Promise is a placeholder for a future value. It is pending, then settled as fulfilled (resolved) or rejected. .then() handles success, .catch() handles failure, and .finally() runs either way.",
                "fetch('/api/user')\n  .then(r => r.json())\n  .then(user => console.log(user.name))\n  .catch(err => console.error('failed:', err))\n  .finally(() => console.log('done'));",
            ),
            _section(
                "async/await: readable async",
                "await unwraps a promise inside an async function. Use try/catch for errors. One rule of thumb: await inside loops is often a bug — fetch in parallel with Promise.all instead.",
                "async function loadUser(id) {\n  try {\n    const res = await fetch(`/api/user/${id}`);\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n    return await res.json();\n  } catch (err) {\n    console.error(err);\n    return null;\n  }\n}",
            ),
            _section(
                "Promise.all, allSettled, race",
                "Promise.all runs promises concurrently and fails fast; allSettled waits for every result regardless of failure; race resolves on the first settlement — useful for timeouts.",
                "const [user, posts] = await Promise.all([\n  api.get('/user'),\n  api.get('/posts'),\n]);\n\nconst results = await Promise.allSettled(urls.map(fetch));\n// results: [{status:'fulfilled', value}, {status:'rejected', reason}]",
            ),
        ],
        [
            "The event loop never blocks — I/O is scheduled, not waited on",
            "Promises settle as fulfilled or rejected",
            "async/await + try/catch reads linearly and handles errors",
            "Promise.all for concurrency, allSettled when failures are OK",
        ],
    ),

    # ────────────────────────── TypeScript ──────────────────────────
    _article(
        "ts-why-types",
        "Why TypeScript: Types as Documentation and Safety Net",
        "typescript",
        "TypeScript adds a compile-time type system to JavaScript. The payoff: refactors that are safe, autocomplete that knows your data, and a whole class of runtime bugs moved to compile time.",
        "beginner", 12, ["js-variables-types", "ts-interfaces"],
        [
            _section(
                "The type-annotation model",
                "Annotate parameters, return values, and variables. TypeScript checks your code before it runs and erases the types at compile time — the output is plain JavaScript.",
                "function add(a: number, b: number): number {\n  return a + b;\n}\n\nconst name: string = 'Ada';\n// add('1', 2)  ← error: '1' is not assignable to number",
            ),
            _section(
                "Inference beats annotation",
                "TypeScript infers types from initial values. Annotate the boundaries (function signatures, API responses) and let inference handle the inside.",
                "const total = add(1, 2); // inferred as number\nconst items = ['a', 'b'];    // string[]",
            ),
            _section(
                "The type system basics",
                "primitives (string, number, boolean), arrays (string[]), tuples ([number, string]), unions (string | null), literals ('asc' | 'desc'), and any/unknown. Prefer unknown over any — unknown forces you to narrow before use.",
                "type SortOrder = 'asc' | 'desc';\ntype Result = { ok: true; data: string } | { ok: false; error: string };\n\nfunction parse(input: string): Result { ... }",
            ),
            _section(
                "strict mode is the real product",
                "noImplicitAny, strictNullChecks and the rest of strict make the compiler useful instead of ornamental. strictNullChecks alone kills an entire class of runtime crashes.",
                "// tsconfig.json\n{\n  \"compilerOptions\": {\n    \"strict\": true\n  }\n}",
            ),
        ],
        [
            "Types are checked at compile time and erased at runtime",
            "Let inference work inside functions; annotate the boundaries",
            "Prefer unknown over any — narrowing is forced",
            "strict: true is non-negotiable for real projects",
        ],
    ),
    _article(
        "ts-interfaces-generics",
        "Interfaces and Generics: Contracts for Your Data",
        "typescript",
        "Interfaces describe shapes; generics make functions work across many types without losing type information. Together they model almost any domain safely.",
        "intermediate", 15, ["ts-why-types", "react"],
        [
            _section(
                "Interfaces and type aliases",
                "interface describes an object shape: required fields, optional fields (?), readonly, methods. type aliases can also describe unions and primitives. Pick interface for object shapes you extend, type for everything else.",
                "interface User {\n  id: string;\n  name: string;\n  email: string;\n  role?: 'admin' | 'viewer';   // optional\n  readonly createdAt: Date;\n}",
            ),
            _section(
                "Generics: types as parameters",
                "A generic function takes a type parameter and returns a type built from it. Instead of any, you preserve the exact type through the function — this is what makes typed libraries type-safe.",
                "function first<T>(items: T[]): T | undefined {\n  return items[0];\n}\n\nconst num = first([1, 2, 3]);       // number | undefined\nconst str = first(['a', 'b']);      // string | undefined",
                "Generic constraints keep you honest: function max<T extends { value: number }>",
            ),
            _section(
                "Discriminated unions",
                "Give every variant a literal tag and TypeScript narrows automatically. This is the cleanest way to model 'either/or' data like API results.",
                "type ApiResponse<T> =\n  | { status: 'success'; data: T }\n  | { status: 'error'; error: string };\n\nfunction handle(res: ApiResponse<User>) {\n  if (res.status === 'success') {\n    console.log(res.data.name); // narrowed to data\n  }\n}",
            ),
            _section(
                "Utility types you will use daily",
                "Partial<T> makes every field optional; Pick<T, K> selects fields; Omit<T, K> removes them; Record<K, V> builds maps; Readonly<T> freezes shapes at the type level.",
                "type DraftUser = Partial<User>;        // updates without all fields\nconst byId = new Map<string, User>();       // Record-style keying\nconst summary = Pick<User, 'id' | 'name'>;",
            ),
        ],
        [
            "Interfaces for extendable object shapes, type aliases for unions",
            "Generics preserve type information through functions",
            "Discriminated unions + narrowing model result/error states",
            "Partial/Pick/Omit/Record cover most transformation needs",
        ],
    ),

    # ────────────────────────── React ──────────────────────────
    _article(
        "react-components",
        "React Components and Props",
        "react",
        "React is a component model for UIs. Components accept props and return JSX. The one rule that makes React predictable: data flows down, events flow up.",
        "beginner", 14, ["js-functions", "react-hooks"],
        [
            _section(
                "The component mental model",
                "A component is a function returning JSX. Every render is a pure function of its props — same props in, same UI out. That purity is what makes React fast and predictable.",
                "function Greeting({ name }) {\n  return <h1>Hello, {name}!</h1>;\n}\n\n// Usage: <Greeting name=\"Ada\" />",
            ),
            _section(
                "Props: read-only inputs",
                "Props come from the parent and must never be mutated by the child. When a prop changes, React re-renders the component. Children passed between tags arrive as the special props.children prop.",
                "function Card({ title, children }) {\n  return (\n    <div className=\"card\">\n      <h2>{title}</h2>\n      <div>{children}</div>\n    </div>\n  );\n}",
            ),
            _section(
                "Composition over inheritance",
                "Build small components and compose them. Extract repeated UI into components, lift shared state up, and pass callbacks down. This keeps the tree flat and the logic discoverable.",
                "function App() {\n  return (\n    <Layout>\n      <Sidebar items={sections} />\n      <Main>\n        <PostList posts={posts} />\n      </Main>\n    </Layout>\n  );\n}",
            ),
        ],
        [
            "Components are pure functions of their props",
            "Props are read-only; mutate nothing owned by a parent",
            "children prop enables composition",
            "Data flows down, events flow up",
        ],
    ),
    _article(
        "react-hooks",
        "Hooks: useState, useEffect, and State Management",
        "react",
        "Hooks give function components state and side effects. useState for local state, useEffect for effects that must sync with the world, and derived state computed instead of stored.",
        "intermediate", 18, ["react-components", "js-async"],
        [
            _section(
                "useState: local state",
                "useState returns [value, setter]. State changes trigger re-renders. Update state immutably — never mutate the previous object and expect a re-render.",
                "const [count, setCount] = useState(0);\n\n// prefer the updater form when relying on previous value\nsetCount(prev => prev + 1);",
                "If you can compute a value from existing state, compute it — don't store it.",
            ),
            _section(
                "useEffect: syncing with the outside world",
                "Effects run after render. The dependency array decides when: [] runs once on mount, [x] reruns when x changes. Missed deps cause stale closures; extra deps cause infinite loops. The lint rule is your friend here.",
                "useEffect(() => {\n  let cancelled = false;\n  fetch(`/api/user/${id}`)\n    .then(r => r.json())\n    .then(data => { if (!cancelled) setUser(data); });\n  return () => { cancelled = true; }; // cleanup on unmount\n}, [id]);",
            ),
            _section(
                "Lifting state and derived values",
                "Share state by lifting it to the nearest common parent and passing value + setter down as props. Compute derived values with useMemo only when they are genuinely expensive — otherwise compute inline.",
                "function App() {\n  const [query, setQuery] = useState('');\n  const filtered = items.filter(i => i.name.includes(query));\n  return <SearchBox query={query} onChange={setQuery} items={filtered} />;\n}",
            ),
            _section(
                "Custom hooks: extract reusable logic",
                "Any function starting with use that calls other hooks is a custom hook. They let you share stateful logic without duplicating components.",
                "function useDebounced(value, delay = 300) {\n  const [debounced, setDebounced] = useState(value);\n  useEffect(() => {\n    const t = setTimeout(() => setDebounced(value), delay);\n    return () => clearTimeout(t);\n  }, [value, delay]);\n  return debounced;\n}",
            ),
        ],
        [
            "State changes re-render; always update state immutably",
            "useEffect syncs with the world; the dep array controls when",
            "Lift state to share it; derive values instead of storing them",
            "Custom hooks share stateful logic across components",
        ],
    ),
    _article(
        "react-performance",
        "React Performance: Memoization, Code Splitting, and Re-renders",
        "react",
        "React is fast by default; your job is to not make it slow. Understand what triggers re-renders, when memoization actually helps, and how code splitting shrinks the initial bundle.",
        "advanced", 16, ["react-hooks", "node"],
        [
            _section(
                "What triggers a re-render",
                "A component re-renders when its state changes, its props change, or its parent re-renders. Re-renders are cheap unless work is heavy or the tree is huge. Measure before you memoize.",
                "const App = () => {\n  const [count, setCount] = useState(0);\n  // every render, <HeavyTree> re-renders too unless memoized\n  return <><button onClick={() => setCount(c => c + 1)}>{count}</button><HeavyTree /></>;\n};",
            ),
            _section(
                "useMemo, useCallback, React.memo",
                "React.memo skips re-rendering a component when props are unchanged. useCallback stabilizes function references; useMemo stabilizes computed values. They only pay off when the child render is genuinely expensive.",
                "const Expensive = memo(function Expensive({ data }) {\n  return <Chart data={data} />;\n});\n\nconst handleClick = useCallback(() => { ... }, []);\nconst summary = useMemo(() => compute(data), [data]);",
            ),
            _section(
                "Code splitting with lazy",
                "React.lazy + Suspense splits the bundle so routes load on demand. The initial HTML/JS shrinks and users get a meaningful first paint faster.",
                "const Dashboard = lazy(() => import('./Dashboard'));\n\n<React.Suspense fallback={<Spinner />}>\n  <Dashboard />\n</React.Suspense>",
            ),
        ],
        [
            "Re-renders cascade from state, props, and parent renders",
            "Memoize only when a child render is genuinely expensive",
            "React.lazy + Suspense splits the bundle per route",
            "Measure first — premature memoization is clutter",
        ],
    ),

    # ────────────────────────── Node.js ──────────────────────────
    _article(
        "node-server",
        "Node.js and Express: Building Your First API",
        "node",
        "Node runs JavaScript on the server. Express adds routing, middleware, and JSON handling. Together they ship your first real HTTP API in minutes — and teach the request/response model that underlies everything.",
        "intermediate", 18, ["js-async", "sql-database"],
        [
            _section(
                "The request/response model",
                "Every HTTP exchange is a request and a response. The request has a method (GET, POST, ...), a path, headers, and an optional body. The response has a status code, headers, and a body. That's the whole contract.",
                "GET /api/users    → 200, JSON list\nPOST /api/users    → 201, created user\nGET /api/users/42  → 200 or 404",
            ),
            _section(
                "Your first Express app",
                "app.get, app.post register handlers. Each handler receives (req, res). Respond with res.json() to serialize an object into JSON and set the content-type for you.",
                "const express = require('express');\nconst app = express();\n\napp.use(express.json()); // parse JSON bodies\n\napp.get('/health', (req, res) => res.json({ ok: true }));\n\napp.post('/users', (req, res) => {\n  const { name } = req.body;\n  res.status(201).json({ id: 1, name });\n});\n\napp.listen(3000, () => console.log('up on :3000'));",
            ),
            _section(
                "Middleware: the pipeline",
                "Middleware runs between the request arriving and the handler responding. express.json is middleware. You write middleware for logging, auth, error handling, and validation. Order matters: define before the routes that use them.",
                "app.use((req, res, next) => {\n  console.log(`${req.method} ${req.path}`);\n  next();\n});\n\n// error-handling middleware has 4 args (err, req, res, next)\napp.use((err, req, res, next) => {\n  res.status(err.status || 500).json({ error: err.message });\n});",
            ),
            _section(
                "Async errors and validation",
                "Async handlers that throw must be caught. Validate input before you trust it — hand-rolled checks are fine to start; zod makes it declarative at scale.",
                "app.post('/users', async (req, res) => {\n  try {\n    const user = await db.users.create(req.body);\n    res.status(201).json(user);\n  } catch (err) {\n    next(err); // forward to error middleware\n  }\n});",
            ),
        ],
        [
            "HTTP is request + response with method, path, headers, body",
            "res.json() serializes and sets headers for you",
            "Middleware is a pipeline; order matters",
            "Validate input and forward async errors to error middleware",
        ],
    ),
    _article(
        "node-files-streams",
        "Files, Streams, and the Event Loop in Node",
        "node",
        "Node's fs module reads and writes files, and streams process data chunk-by-chunk so memory stays flat even for huge files. Both ride on the same event loop that makes Node non-blocking.",
        "advanced", 15, ["node-server", "js-async"],
        [
            _section(
                "fs promises vs callbacks",
                "Prefer fs/promises and await. Reading a file is async — never block the loop with the sync variants (fs.readFileSync) in a server.",
                "const { readFile, writeFile } = require('fs/promises');\n\nconst data = await readFile('./data.json', 'utf8');\nawait writeFile('./out.json', JSON.stringify(parsed, null, 2));",
            ),
            _section(
                "Streams: chunked processing",
                "A stream passes data in chunks without loading the whole thing. readFile of a 2 GB log would blow up memory; piping a stream stays flat. Use streams for large payloads and file transfers.",
                "const { createReadStream, createWriteStream } = require('fs');\n\ncreateReadStream('big.log')\n  .pipe(createWriteStream('copy.log'))\n  .on('finish', () => console.log('done'));",
            ),
            _section(
                "The event loop in one breath",
                "Node runs your code on one thread, delegating I/O to the OS. When I/O completes, a callback goes onto a queue and runs when the call stack is empty. Never block the loop with sync CPU work — offload to worker threads if you must.",
                "// blocking the loop\nwhile (true) {}\n// ...everything else in the process starves",
                "setImmediate, process.nextTick, and timers each have their own queue phase — know which you're in.",
            ),
        ],
        [
            "Use fs/promises and await, not the sync variants in servers",
            "Streams keep memory flat for large data",
            "The event loop never blocks; delegate I/O and heavy CPU",
            "Piping is the idiomatic way to move file data",
        ],
    ),

    # ────────────────────────── SQL & Databases ──────────────────────────
    _article(
        "sql-select",
        "SQL SELECT: Querying Data Like a Pro",
        "sql",
        "SELECT is how you read data. WHERE filters rows, JOINs combine tables, GROUP BY aggregates, and ORDER BY sorts. Master these five clauses and you can answer almost any data question.",
        "beginner", 14, ["sql-database", "js-node-sql"],
        [
            _section(
                "SELECT and WHERE",
                "SELECT chooses columns; WHERE filters rows before they reach you. WHERE runs before aggregation — a common beginner mix-up that silently changes answers.",
                "SELECT name, salary\nFROM employees\nWHERE salary > 60000\nORDER BY salary DESC\nLIMIT 10;",
            ),
            _section(
                "JOINs: bringing tables together",
                "INNER JOIN keeps only matching rows; LEFT JOIN keeps all left rows plus matches. JOIN ... ON says which columns link the tables. A missing ON is a Cartesian product — often accidental, sometimes useful.",
                "SELECT e.name, d.name AS department\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;",
            ),
            _section(
                "GROUP BY and HAVING",
                "GROUP BY collapses rows into groups; aggregate functions (COUNT, SUM, AVG, MIN, MAX) summarize each group. HAVING filters groups after aggregation — WHERE cannot see aggregates.",
                "SELECT dept_id, COUNT(*) AS headcount, AVG(salary) AS avg_salary\nFROM employees\nGROUP BY dept_id\nHAVING COUNT(*) > 5\nORDER BY headcount DESC;",
            ),
            _section(
                "LIMIT, ORDER BY, DISTINCT",
                "ORDER BY sorts (default ascending, DESC for descending). LIMIT caps rows. DISTINCT removes duplicate rows from the result — handy for finding the set of unique values in a column.",
                "SELECT DISTINCT city FROM customers ORDER BY city;\nSELECT * FROM orders ORDER BY created_at DESC LIMIT 25;",
            ),
        ],
        [
            "WHERE filters rows; HAVING filters groups",
            "INNER JOIN for matches, LEFT JOIN to preserve the left side",
            "GROUP BY + aggregates summarize; ORDER BY + LIMIT shape output",
            "Always specify the JOIN key — a missing ON is a Cartesian product",
        ],
    ),
    _article(
        "sql-database",
        "Designing Databases: Tables, Keys, and Normalization",
        "sql",
        "A good schema makes queries simple; a bad one makes everything painful. Understand primary/foreign keys, the trade-offs of normalization, and the indexes that keep queries fast.",
        "intermediate", 16, ["sql-select", "node"],
        [
            _section(
                "Tables and keys",
                "A primary key uniquely identifies a row. A foreign key references a row in another table and enforces referential integrity — the database refuses to create orphans.",
                "CREATE TABLE users (\n  id SERIAL PRIMARY KEY,\n  email TEXT UNIQUE NOT NULL\n);\n\nCREATE TABLE posts (\n  id SERIAL PRIMARY KEY,\n  user_id INTEGER REFERENCES users(id),\n  title TEXT NOT NULL\n);",
            ),
            _section(
                "Normalization: one fact, one place",
                "Normalize to avoid duplication and update anomalies. Third normal form (no transitive dependencies) is the pragmatic sweet spot for most apps. Denormalize later, deliberately, for reads.",
                "-- 3NF: user info lives once in users, posts only reference user_id\nSELECT p.title, u.email\nFROM posts p JOIN users u ON p.user_id = u.id;",
            ),
            _section(
                "Indexes: the query accelerator",
                "An index on a column makes equality and range lookups fast, at the cost of slower writes. Index foreign keys and the columns you filter or sort on. Start with the obvious ones; add more when EXPLAIN tells you to.",
                "CREATE INDEX idx_posts_user_id ON posts(user_id);\nCREATE INDEX idx_orders_created ON orders(created_at DESC);",
            ),
            _section(
                "Relationships",
                "One-to-many is a foreign key on the many side. Many-to-many needs a join table with two foreign keys. One-to-one is a foreign key with a UNIQUE constraint.",
                "CREATE TABLE book_authors (\n  book_id INTEGER REFERENCES books(id),\n  author_id INTEGER REFERENCES authors(id),\n  PRIMARY KEY (book_id, author_id)\n);",
            ),
        ],
        [
            "Primary keys identify rows; foreign keys enforce integrity",
            "Aim for 3NF, denormalize deliberately for reads",
            "Index the columns you filter, join, and sort on",
            "Many-to-many needs a join table",
        ],
    ),

    # ────────────────────────── C Programming ──────────────────────────
    _article(
        "c-pointers",
        "C Pointers and Memory: Addresses, Dereferencing, and Why They Matter",
        "c-programming",
        "Pointers are the feature that scares beginners and powers the entire language. A pointer stores an address, not a value. Master them and you master C — and understand every modern language better.",
        "intermediate", 18, ["c-memory", "c-enums", "js-functions"],
        [
            _section(
                "What a pointer actually is",
                "Every variable lives at a memory address. The address-of operator (&) reveals it; a pointer variable stores that address. Declare with * and read the pointed-to value with *. This is the whole mental model — the rest is syntax.",
                "int age = 25;\nint *p = &age;    // p stores the address of age\n\nprintf(\"%d\", age);   // 25 — the value\nprintf(\"%p\", &age);  // address (hex)\nprintf(\"%d\", *p);    // 25 — dereference p",
                "Read declarations right-to-left: int *p means 'p is a pointer to int'.",
            ),
            _section(
                "Why bother? The three real uses",
                "Pointers exist for three reasons: (1) passing large structs by reference so you don't copy them, (2) modifying variables from inside functions (call by reference), and (3) dynamic memory — when you don't know at compile time how much data you'll need.",
                "void swap(int *a, int *b) {\n  int tmp = *a;\n  *a = *b;\n  *b = tmp;\n}\n\nint main(void) {\n  int x = 1, y = 2;\n  swap(&x, &y);   // x and y really change\n  return 0;\n}",
            ),
            _section(
                "Pointers and arrays are cousins",
                "An array name decays to a pointer to its first element: arr == &arr[0]. Subscripting arr[i] is literally shorthand for *(arr + i). That's why pointers and arrays interchange so freely.",
                "int nums[3] = {10, 20, 30};\nint *p = nums;         // points to nums[0]\n\nprintf(\"%d\", *p);       // 10\nprintf(\"%d\", *(p + 1)); // 20  — pointer arithmetic\nprintf(\"%d\", p[2]);     // 30  — pointer subscripting",
            ),
            _section(
                "The dangers: uninitialized and NULL pointers",
                "An uninitialized pointer holds garbage and dereferencing it is undefined behavior. A NULL pointer crashes cleanly. Always initialize pointers, check for NULL before dereferencing, and set freed pointers to NULL.",
                "int *p;      // uninitialized — garbage address\nprintf(\"%d\", *p); // UB — could crash anything\n\nint *q = NULL;\nif (q != NULL) printf(\"%d\", *q); // safe check",
            ),
        ],
        [
            "A pointer stores an address; * dereferences, & takes the address",
            "Pointers enable call-by-reference and avoid copying large structs",
            "arr[i] is equivalent to *(arr + i)",
            "Initialize pointers, check NULL before dereferencing",
        ],
    ),
    _article(
        "c-memory",
        "C Memory Management: Stack, Heap, malloc, and Leaks",
        "c-programming",
        "Unlike Python or JavaScript, C gives you raw control over memory — and the responsibility to free it. Understand the stack, the heap, malloc/free, and how leaks happen.",
        "advanced", 17, ["c-pointers", "c-enums", "node-files-streams"],
        [
            _section(
                "Stack vs heap",
                "The stack holds local variables and is managed automatically — allocation and cleanup happen as functions enter and exit. The heap is a big pool you request from with malloc() and must return with free(). Stack is fast and automatic; heap is flexible and manual.",
                "int stackVar = 5;   // stack — auto-cleaned\n\nint *heapVar = malloc(sizeof(int));  // heap — manual\n*heapVar = 5;\nfree(heapVar);                        // your job!",
            ),
            _section(
                "malloc, calloc, realloc",
                "malloc allocates but does not zero memory; calloc zero-initializes; realloc resizes (and may move) a block. Always check the return for NULL before using.",
                "int *arr = malloc(10 * sizeof(int));\nif (arr == NULL) {\n  fprintf(stderr, \"Allocation failed\\n\");\n  return 1;\n}\narr[0] = 42;\n\narr = realloc(arr, 20 * sizeof(int));\nfree(arr);",
                "Prefer sizeof(int) over a magic number like 4 — it stays correct when int changes size.",
            ),
            _section(
                "Memory leaks and double frees",
                "Every malloc must eventually have a matching free. Leak = you lose the pointer without freeing (memory stays reserved). Double free = freeing twice, which corrupts the allocator. Use a discipline: allocate and free in the same logical layer.",
                "// LEAK — p is overwritten, old block can never be freed\nint *p = malloc(100);\np = malloc(200);\n\n// DOUBLE FREE\nint *q = malloc(50);\nfree(q);\nfree(q);   // UB — allocator corruption",
            ),
            _section(
                "Tools that catch what your eyes miss",
                "Memory bugs rarely crash at the guilty line. Valgrind catches leaks and invalid access; AddressSanitizer (ASan) compiles guards into your binary. Run your tests under ASan to find use-after-free and buffer overflows.",
                "valgrind --leak-check=full ./program\n\ngcc -fsanitize=address -g program.c -o program\n./program  # reports exact leak/overflow lines",
            ),
        ],
        [
            "Stack is automatic, heap is manual (malloc/free)",
            "malloc doesn't zero memory; calloc does; realloc resizes",
            "Every malloc needs one free; avoid leaks and double frees",
            "Valgrind and ASan find memory bugs your eyes miss",
        ],
    ),
    _article(
        "c-enums-structs",
        "C Enums and Structs: Named Constants and Custom Types",
        "c-programming",
        "Enums turn magic numbers into readable names; structs group related fields into one custom type. Together they let you model real-world data without scattering magic values.",
        "intermediate", 14, ["c-pointers", "c-memory"],
        [
            _section(
                "Enums: names for integers",
                "enum declares a set of named integer constants. By default the first is 0 and each subsequent increments, but you can set explicit values. The win is readability: switch statements become self-documenting.",
                "enum Color { RED, GREEN, BLUE };        // 0, 1, 2\ntypedef enum { MONDAY=1, TUESDAY, ... } Weekday;\n\nenum Color c = GREEN;\nif (c == GREEN) { /* obvious what this means */ }",
            ),
            _section(
                "Structs: grouped data",
                "struct bundles several fields into one type. Combined with typedef you get a clean custom type. Access fields with . on a struct value and -> through a pointer.",
                "typedef struct {\n  char name[32];\n  int age;\n  double score;\n} Student;\n\nStudent s = {\"Ada\", 36, 99.5};\nprintf(\"%s %d\", s.name, s.age);\n\nStudent *p = &s;\np->score = 100.0;   // -> is shorthand for (*p).score",
            ),
            _section(
                "Structs, pointers, and the heap",
                "structs can live on the stack or heap. Passing a struct by value copies it — expensive for big structs. Pass a pointer instead. Self-referential structs (containing a pointer to their own type) build linked lists and trees.",
                "typedef struct Node {\n  int data;\n  struct Node *next;  // self-reference = linked list\n} Node;\n\nNode *head = malloc(sizeof(Node));\nhead->data = 1;\nhead->next = NULL;",
            ),
        ],
        [
            "Enums name integers for readability",
            "Structs group fields into one custom type",
            ". accesses through a value, -> through a pointer",
            "Structs can point to themselves to build linked structures",
        ],
    ),
    _article(
        "c-preprocessors-files",
        "C Preprocessors and File I/O",
        "c-programming",
        "The preprocessor runs before compilation and handles #include, #define, and conditional compilation. File I/O — reading and writing files with fopen/fread/fprintf — is how your programs persist data.",
        "intermediate", 15, ["c-enums-structs", "c-memory"],
        [
            _section(
                "The preprocessor: what runs before your code",
                "Lines starting with # are handled before compilation. #define creates macros and constants; #include pastes in headers; #ifndef/#endif guard against double-includes. The preprocessor is textual — it's not the language itself.",
                "#ifndef UTILS_H\n#define UTILS_H\n\n#define MAX_BUFFER 256\n#define SQUARE(x) ((x) * (x))\n\n#endif\n\n// Note the extra parens in SQUARE — they prevent\n// SQUARE(a + b) from turning into a + b * a + b",
            ),
            _section(
                "Opening and closing files",
                "fopen opens a file with a mode: r (read), w (write, truncates), a (append), r+ (read/write). Always check that fopen didn't return NULL, and always fclose when done. Leaked FILE handles corrupt your program's bookkeeping.",
                "FILE *f = fopen(\"notes.txt\", \"r\");\nif (f == NULL) {\n  perror(\"open\");\n  return 1;\n}\nchar line[256];\nwhile (fgets(line, sizeof line, f)) {\n  printf(\"%s\", line);\n}\nfclose(f);",
            ),
            _section(
                "Writing and appending",
                "fprintf writes formatted text; fputs writes a string; fputc writes one char. For binary data use fwrite/fread with the number of bytes. Choose 'w' to overwrite or 'a' to append.",
                "FILE *f = fopen(\"log.txt\", \"a\");  // append\nfprintf(f, \"%s: score=%d\\n\", \"Ada\", 99);\nfclose(f);\n\n// binary write\nint data[3] = {1, 2, 3};\nfwrite(data, sizeof(int), 3, f);",
            ),
            _section(
                "Conditional compilation",
                "#ifdef / #ifndef / #if let you compile different code per platform, debug build, or feature flag. This is how one source file supports Windows and Linux.",
                "#ifdef _WIN32\n  printf(\"Windows build\\n\");\n#elif defined(__linux__)\n  printf(\"Linux build\\n\");\n#else\n  printf(\"Other platform\\n\");\n#endif",
            ),
        ],
        [
            "#include, #define, #ifdef run before compilation",
            "Always check fopen for NULL and fclose when done",
            "r/w/a modes: read, overwrite, append",
            "#ifdef lets one file build for many platforms",
        ],
    ),

    # ────────────────────────── Full-Stack ──────────────────────────
    _article(
        "fullstack-architecture",
        "Full-Stack Architecture: How the Pieces Fit",
        "full-stack",
        "React in the browser, Express on the server, SQL in the database. See how a request travels through all three layers, and the decisions — where state lives, who owns the schema, how they talk — that define a full-stack app.",
        "advanced", 20, ["react-components", "node-server", "sql-database"],
        [
            _section(
                "The request's journey",
                "A click in React fires a fetch. The browser sends an HTTP request; the Express route validates it, queries SQL, and returns JSON; React re-renders with the response. Every full-stack feature is this loop, repeated with different shapes.",
                "React → fetch('/api/posts') → Express GET /api/posts\n  → SQL SELECT ... → JSON → React setState → render",
            ),
            _section(
                "Where does the schema live?",
                "The database owns truth. The server validates and shapes data for the client. React renders and caches (React Query) for UX. Duplicate ownership of the schema is a maintenance trap — pick one source of truth per field.",
                "// server: validate\nconst schema = z.object({ title: z.string().min(1) });\nconst { title } = schema.parse(req.body);\n\n// client: render + cache\nuseQuery(['posts'], () => api.get('/api/posts'));",
            ),
            _section(
                "Auth in the full-stack flow",
                "Sessions or JWTs prove identity. The server sets a secure httpOnly cookie (or the client stores a token) and every protected route verifies it. Never trust the client about who it is — verify on every request.",
                "POST /api/auth/login → server verifies credentials → sets httpOnly cookie\nGET /api/me → server reads cookie → returns user\n// The client can't read an httpOnly cookie — XSS can't steal it",
            ),
            _section(
                "Shipping it",
                "Build the React app, serve it from Express, run the DB with migrations checked into git, and deploy behind a reverse proxy. Environment variables for secrets; never commit them.",
                "// .env (never committed)\nDATABASE_URL=postgres://...\nJWT_SECRET=...\nPORT=3000",
            ),
        ],
        [
            "Every feature is a request/response loop through three layers",
            "One source of truth per field; validation at the server boundary",
            "Verify identity server-side on every protected request",
            "Migrations + env vars + reverse proxy = shippable",
        ],
    ),
]


ARTICLES_BY_ID: dict[str, dict[str, Any]] = {a["id"]: a for a in ARTICLES}


# ────────────────────────────────────────────────────────────────────────────
# Expansion content authored in per-category modules. Each module defines:
#   NEW_ARTICLES : list of full article dicts (with quiz/exercise/curriculum)
#   INTERACTIVES : {article_id: {"quiz": [...], "exercise": {...}}} for articles
#                  defined above, adding quizzes + exercises to them.
# Imported here so get_articles()/get_article()/search_articles() see everything.
# ────────────────────────────────────────────────────────────────────────────

CATEGORY_CURRICULUM: dict[str, list[str]] = {
    "html-css": ["html", "css"],
    "javascript": ["javascript"],
    "typescript": ["typescript"],
    "react": ["react"],
    "node": ["node"],
    "sql": ["sql"],
    "c-programming": ["c"],
    "full-stack": ["html", "css", "javascript", "typescript", "react", "node", "sql"],
}


def _apply_curriculum(article: dict[str, Any]) -> dict[str, Any]:
    if not article.get("curriculum"):
        article["curriculum"] = CATEGORY_CURRICULUM.get(article.get("category", ""), [])
    return article


def _load_expansion() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    from app.data.study_content_html_css import NEW_ARTICLES as HC, INTERACTIVES as HI
    from app.data.study_content_javascript import NEW_ARTICLES as JN, INTERACTIVES as JI
    from app.data.study_content_typescript_react import NEW_ARTICLES as TR, INTERACTIVES as TI
    from app.data.study_content_node import NEW_ARTICLES as NN, INTERACTIVES as NI
    from app.data.study_content_sql_c_fullstack import NEW_ARTICLES as SF, INTERACTIVES as SI

    new_articles = []
    for group in (HC, JN, TR, NN, SF):
        new_articles.extend(group)
    interactives: dict[str, dict[str, Any]] = {}
    for group in (HI, JI, TI, NI, SI):
        interactives.update(group)

    for a in new_articles:
        _apply_curriculum(a)
    for a in ARTICLES:
        _apply_curriculum(a)
    return new_articles, interactives


NEW_ARTICLES, ARTICLE_INTERACTIVES = _load_expansion()

ALL_ARTICLES = ARTICLES + NEW_ARTICLES
ALL_ARTICLES_BY_ID: dict[str, dict[str, Any]] = {a["id"]: a for a in ALL_ARTICLES}


def get_categories() -> list[dict[str, Any]]:
    return STUDY_CATEGORIES


def get_articles(category: str | None = None) -> list[dict[str, Any]]:
    if not category:
        return ALL_ARTICLES
    return [a for a in ALL_ARTICLES if a["category"] == category]


def get_article(article_id: str) -> dict[str, Any] | None:
    article = ALL_ARTICLES_BY_ID.get(article_id)
    if not article:
        return None
    interactive = ARTICLE_INTERACTIVES.get(article_id, {})
    if interactive:
        article = {**article, **interactive}
    return article


def search_articles(query: str) -> list[dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return ALL_ARTICLES
    return [
        a for a in ALL_ARTICLES
        if q in a["title"].lower()
        or q in a["summary"].lower()
        or q in " ".join(a["related_topics"]).lower()
        or q in " ".join(a.get("curriculum", [])).lower()
        or any(q in s["heading"].lower() for s in a["sections"])
    ]


def get_related_articles(
    language_id: str,
    query: str = "",
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Find Study Library articles relevant to a curriculum language + lesson topic.

    Matches on the article's `curriculum` languages, then on keyword overlap
    with the lesson title. Used by LessonView to "connect the dots" between
    a lesson and in-depth study material.
    """
    q = query.lower().strip()
    lang = language_id.lower()

    def relevance(a: dict[str, Any]) -> tuple[int, str]:
        score = 0
        if lang in a.get("curriculum", []):
            score += 2
        if a["category"] == lang or lang in a.get("related_topics", []):
            score += 1
        if q:
            haystack = " ".join(
                [a["title"], a["summary"], " ".join(a["related_topics"])] + [s["heading"] for s in a["sections"]]
            ).lower()
            if q in haystack:
                score += 3
        return score, a["title"]

    scored = sorted(ALL_ARTICLES, key=relevance, reverse=True)
    return [a for a in scored if relevance(a)[0] > 0][:limit]
