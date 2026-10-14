"""Simple script to add quizzes and exercises to study_materials articles.

This reads study_materials.py, adds quiz/exercise data to each article,
and writes it back.
"""
import os
import re

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY_PATH = os.path.join(BACKEND_ROOT, "app", "data", "study_materials.py")


def _quiz(question, options, answer, explanation):
    return {"question": question, "options": options, "answer": answer, "explanation": explanation}


def _exercise(title, task, starter, solution, hint=""):
    ex = {"title": title, "task": task, "starter": starter, "solution": solution}
    if hint:
        ex["hint"] = hint
    return ex


def _mcq(question, options, explanation=""):
    return {"type": "mcq", "question": question, "options": options, "explanation": explanation}


def _fill(question, answer, hint=""):
    return {"type": "fill", "question": question, "answer": answer, "hint": hint}


def _run(description, starter, expected_output, hint=""):
    return {"type": "run", "description": description, "starter": starter, "expected_output": expected_output, "hint": hint}


# Article quiz data
ARTICLE_QUIZZES = {
    "html-basics": [
        _quiz("What does HTML stand for?", ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], 0, "HTML = HyperText Markup Language."),
        _quiz("Which tag creates the largest heading?", ["<h6>", "<head>", "<h1>", "<header>"], 2, "<h1> is the largest heading."),
        _quiz("What does the <a> tag create?", ["An image", "A link", "A paragraph", "A heading"], 1, "The <a> tag creates hyperlinks."),
        _quiz("Which attribute specifies alternative text for images?", ["src", "alt", "href", "title"], 1, "The alt attribute provides alternative text."),
        _quiz("What is the correct element for a line break?", ["<lb>", "<br>", "<break>", "<newline>"], 1, "<br> is the line break element."),
    ],
    "css-basics": [
        _quiz("What does CSS stand for?", ["Cascading Style Sheets", "Creative Style System", "Computer Style Sheets", "Cascading Simple Sheets"], 0, "CSS = Cascading Style Sheets."),
        _quiz("Which property changes text color?", ["font-color", "text-style", "color", "background"], 2, "The color property sets text color."),
        _quiz("What is the correct syntax for external CSS?", ["<css src='style.css'>", "<link rel='stylesheet' href='style.css'>", "<style src='style.css'>", "<import css='style.css'>"], 1, "External CSS uses <link rel='stylesheet' href='...'>."),
        _quiz("Which box-sizing includes padding and border in width?", ["content-box", "border-box", "padding-box", "margin-box"], 1, "border-box includes padding and border."),
        _quiz("What does the cascade resolve?", ["Animations", "Conflicts by specificity then source order", "Colors only", "Layout only"], 1, "The cascade resolves conflicts by specificity and source order."),
    ],
    "css-flexbox-grid": [
        _quiz("Which property aligns items along the cross axis?", ["justify-content", "align-items", "flex-direction", "gap"], 1, "align-items controls cross-axis alignment."),
        _quiz("What does flex: 1 mean?", ["flex-grow: 1 only", "flex-grow: 1, flex-shrink: 1, flex-basis: 0%", "width: 1px", "display: flex"], 1, "flex: 1 is shorthand for grow:1, shrink:1, basis:0%."),
        _quiz("Grid layout is:", ["One-dimensional", "Two-dimensional", "Three-dimensional", "Linear only"], 1, "Grid handles both rows and columns."),
        _quiz("Which unit is relative to the root font size?", ["em", "rem", "px", "%"], 1, "rem is relative to the root font-size."),
        _quiz("How do you create a gap between flex items?", ["margin", "gap", "padding", "spacing"], 1, "gap works in both flex and grid."),
    ],
    "css-responsive": [
        _quiz("What does a media query do?", ["Animates elements", "Applies styles conditionally based on viewport", "Loads external CSS", "Creates responsive images"], 1, "Media queries apply CSS based on viewport."),
        _quiz("Which meta tag enables responsive design?", ["<meta name='viewport' content='width=device-width, initial-scale=1.0'>", "<meta responsive='true'>", "<meta name='mobile'>", "<meta charset='UTF-8'>"], 0, "The viewport meta tag enables responsive design."),
        _quiz("Mobile-first means:", ["Design for desktop first", "Design for mobile first, then enhance", "Use only mobile devices", "Ignore tablets"], 1, "Mobile-first starts small and adds complexity."),
        _quiz("Which unit is viewport-relative for width?", ["rem", "em", "vw", "px"], 2, "1vw = 1% of viewport width."),
        _quiz("What is a breakpoint?", ["Pausing JavaScript", "Width where layout changes", "Color change point", "Animation delay"], 1, "Breakpoints are viewport widths where layout adapts."),
    ],
    "js-variables-types": [
        _quiz("Which keyword declares a block-scoped variable?", ["var", "let", "static", "global"], 1, "let and const are block-scoped; var is function-scoped."),
        _quiz("What is typeof null?", ["'null'", "'undefined'", "'object'", "'boolean'"], 2, "typeof null returns 'object'."),
        _quiz("Which type is immutable?", ["Object", "Array", "String", "Function"], 2, "Strings are immutable."),
        _quiz("What does == compare?", ["Type and value", "Value with coercion", "Reference only", "Type only"], 1, "== compares values with type coercion."),
        _quiz("Which is NOT a JavaScript data type?", ["Symbol", "BigInt", "Float", "Undefined"], 2, "JavaScript has number, not separate float."),
    ],
    "js-functions": [
        _quiz("How do you define a function expression?", ["function name() {}", "const name = function() {}", "define function() {}", "func name() {}"], 1, "Function expressions assign a function to a variable."),
        _quiz("What is a closure?", ["A closed HTML tag", "A function that remembers its outer scope", "A loop", "An error handler"], 1, "A closure retains access to its lexical scope."),
        _quiz("What does the rest parameter do?", ["Pauses execution", "Collects remaining arguments into an array", "Returns first argument", "Throws error"], 1, "...args collects remaining arguments into an array."),
        _quiz("Arrow functions do NOT have their own:", ["name", "this/arguments/super", "return value", "parameters"], 1, "Arrow functions lexically bind this, arguments, super."),
        _quiz("typeof function() {} returns:", ["'function'", "'object'", "'callable'", "'undefined'"], 0, "typeof a function returns 'function'."),
    ],
    "js-arrays-objects": [
        _quiz("Which method adds an item to the end of an array?", ["shift()", "unshift()", "push()", "pop()"], 2, "push() appends to the end."),
        _quiz("How do you shallow-copy an object?", ["Object.clone(obj)", "{...obj}", "obj.copy()", "Object.copy(obj)"], 1, "{...obj} is object spread for shallow copy."),
        _quiz("What does Array.map() return?", ["Original array", "New array of same length", "Single value", "undefined"], 1, "map returns a new transformed array."),
        _quiz("Which method finds the first matching element?", ["filter()", "find()", "includes()", "indexOf()"], 1, "find() returns the first match."),
        _quiz("Objects are stored:", ["By value", "By reference", "By index", "By hash"], 1, "Objects and arrays are reference types."),
    ],
    "js-async": [
        _quiz("What does async/await simplify?", ["Object creation", "Promise-based code", "CSS animations", "HTML parsing"], 1, "async/await simplifies Promises."),
        _quiz("What does Promise.all() do?", ["Runs sequentially", "Runs in parallel and waits for all", "Cancels all", "Runs only first"], 1, "Promise.all waits for all promises."),
        _quiz("Which is NOT a Promise state?", ["Pending", "Fulfilled", "Rejected", "Paused"], 3, "Promises are pending, fulfilled, or rejected."),
        _quiz("What does .then() return?", ["undefined", "A new Promise", "Original Promise", "An error"], 1, "then() returns a new Promise for chaining."),
        _quiz("How do you catch errors in async functions?", ["catch block", "try/catch", "onerror", "throw()"], 1, "try/catch works with async/await."),
    ],
    "ts-why-types": [
        _quiz("What is TypeScript's main purpose?", ["Replace JavaScript", "Add static types to JavaScript", "Make code faster", "Remove bugs automatically"], 1, "TypeScript adds optional static types."),
        _quiz("How do you declare a variable that must be a number?", ["var x", "let x", "let x: number", "number x"], 2, "TypeScript uses let x: number."),
        _quiz("What does the any type do?", ["Restricts to numbers", "Disables type checking", "Makes values immutable", "Forces string type"], 1, "any opts out of type checking."),
        _quiz("TypeScript compiles to:", ["Assembly", "Machine code", "JavaScript", "Python"], 2, "tsc outputs plain JavaScript."),
        _quiz("Which is a benefit of TypeScript?", ["Smaller files", "Catching errors at compile time", "Faster execution", "Less code"], 1, "Static types catch mistakes before runtime."),
    ],
    "ts-interfaces-generics": [
        _quiz("What does an interface define?", ["A class", "A type shape / contract", "A function", "A module"], 1, "Interfaces describe object shapes."),
        _quiz("Generics allow:", ["Writing without types", "Reusable multi-type components", "Hard-coding types", "Removing all types"], 1, "Generics preserve types while staying flexible."),
        _quiz("Which syntax defines an interface?", ["interface User {}", "def interface User:", "interface = User", "type interface User"], 0, "interface Name { ... } defines a shape."),
        _quiz("In Box<T>, T is:", ["A syntax error", "A type parameter", "Only for strings", "A class"], 1, "T stands in for whatever type is passed."),
        _quiz("Which is preferred for object shapes?", ["type alias only", "interface", "class", "enum"], 1, "interfaces are idiomatic for object contracts."),
    ],
    "react-components": [
        _quiz("What is a React component?", ["An HTML file", "A reusable UI building block", "A CSS class", "A database query"], 1, "Components are the reusable units of React UI."),
        _quiz("How do you pass data to a child component?", ["State", "Props", "Context only", "Redux only"], 1, "Props flow from parent to child."),
        _quiz("What hook replaces class state?", ["useEffect", "useState", "useContext", "useRef"], 1, "useState adds state to function components."),
        _quiz("JSX allows:", ["Writing HTML in JS", "Writing SQL", "Using only CSS", "Avoiding JavaScript"], 0, "JSX lets you write HTML-like syntax in JS."),
        _quiz("What does the key prop help with?", ["Styling", "Reconciliation / list rendering", "Form validation", "API calls"], 1, "keys help React match list items between renders."),
    ],
    "react-hooks": [
        _quiz("useEffect runs:", ["Only on mount", "After every render by default", "Never", "Only on unmount"], 1, "useEffect fires after render; deps control repeats."),
        _quiz("Which hook gives you a mutable ref?", ["useState", "useRef", "useMemo", "useCallback"], 1, "useRef returns an object with .current."),
        _quiz("useMemo is used for:", ["Side effects", "Memoizing expensive computations", "DOM manipulation", "Styling"], 1, "useMemo caches a computed value."),
        _quiz("Custom hooks must start with:", ["use_", "with", "use", "hook_"], 2, "Custom hooks must start with use."),
        _quiz("useContext returns:", ["A new context", "The current context value", "A provider", "A consumer"], 1, "useContext reads the nearest context value."),
    ],
    "react-performance": [
        _quiz("React.memo:", ["Caches all components", "Memoizes renders when props are equal", "Prevents useEffect", "Creates portals"], 1, "React.memo skips re-renders when props are unchanged."),
        _quiz("Code splitting uses:", ["React.memo", "React.lazy + Suspense", "useMemo", "useCallback"], 1, "React.lazy enables dynamic imports."),
        _quiz("What causes unnecessary re-renders?", ["Changing state", "New object/array references in props", "Using keys", "Using fragments"], 1, "New references in props cause extra renders."),
        _quiz("useCallback memoizes:", ["A value", "A function reference", "A component", "A context"], 1, "useCallback returns a memoized function reference."),
        _quiz("Virtualization helps with:", ["Styling", "Long lists performance", "Forms", "Routing"], 1, "Virtualization renders only visible items."),
    ],
    "node-server": [
        _quiz("What is Node.js?", ["A database", "JavaScript runtime for servers", "A frontend framework", "A CSS tool"], 1, "Node.js runs JavaScript on the server with V8."),
        _quiz("Which module creates HTTP servers?", ["fs", "http", "path", "url"], 1, "The http module handles servers."),
        _quiz("What does npm stand for?", ["Node Project Manager", "Node Package Manager", "New Package Manager", "Node Process Manager"], 1, "npm manages packages and dependencies."),
        _quiz("Express is:", ["A database", "A minimal web framework", "A testing library", "A build tool"], 1, "Express simplifies routing and responses."),
        _quiz("Middleware in Express:", ["Handles errors only", "Runs before the final handler", "Is optional only", "Replaces routes"], 1, "Middleware runs during the request/response cycle."),
    ],
    "node-files-streams": [
        _quiz("Which module handles files?", ["http", "fs", "path", "stream"], 1, "fs provides file operations."),
        _quiz("A stream is:", ["A music player", "A way to handle data piece by piece", "A database", "A logging tool"], 1, "Streams process data incrementally."),
        _quiz("What does piping do?", ["Pipes water", "Connects readable to writable stream", "Creates a new stream", "Stops a stream"], 1, "pipe() chains streams together."),
        _quiz("Which method reads a file synchronously?", ["fs.readFile", "fs.readFileSync", "fs.openSync", "fs.createReadStream"], 1, "The Sync suffix means blocking."),
        _quiz("Buffers are used for:", ["Routing", "Temporary binary storage", "Database queries", "HTML rendering"], 1, "Buffers handle raw binary data."),
    ],
    "sql-select": [
        _quiz("What does SQL stand for?", ["Simple Query Language", "Structured Query Language", "Standard Query Logic", "System Query Language"], 1, "SQL = Structured Query Language."),
        _quiz("Which clause filters rows?", ["ORDER BY", "WHERE", "GROUP BY", "LIMIT"], 1, "WHERE filters rows."),
        _quiz("Which JOIN returns all rows from both tables?", ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], 3, "FULL OUTER JOIN returns all rows."),
        _quiz("What does GROUP BY do?", ["Filters rows", "Aggregates by column values", "Sorts results", "Joins tables"], 1, "GROUP BY buckets rows for aggregates."),
        _quiz("Which function counts rows?", ["SUM()", "COUNT()", "AVG()", "MAX()"], 1, "COUNT() returns the number of rows."),
    ],
    "sql-database": [
        _quiz("What is a primary key?", ["A backup column", "A unique row identifier", "A foreign table", "An index type"], 1, "Primary keys uniquely identify each row."),
        _quiz("Normalization reduces:", ["Table size", "Data redundancy", "Query speed", "Indexes"], 1, "Normalization removes duplicate data."),
        _quiz("An index improves:", ["Storage size", "Read performance", "Write speed", "Security"], 1, "Indexes speed up queries."),
        _quiz("A foreign key:", ["Must be unique", "References another table's primary key", "Is always numeric", "Cannot be null"], 1, "Foreign keys enforce referential integrity."),
        _quiz("ACID means:", ["Atomicity, Consistency, Isolation, Durability", "All queries fast", "Data always available", "Indexes cached"], 0, "ACID guarantees reliable transactions."),
    ],
    "c-pointers": [
        _quiz("What does a pointer store?", ["A value", "A memory address", "A function name", "A type"], 1, "Pointers hold memory addresses."),
        _quiz("Which operator gets the address of a variable?", ["*", "&", "->", "@"], 1, "&x returns the address of x."),
        _quiz("What does *ptr do?", ["Creates a pointer", "Dereferences a pointer", "Deletes a pointer", "Checks null"], 1, "*ptr accesses the pointed-to value."),
        _quiz("What is a null pointer?", ["A pointer to 0", "An uninitialized pointer", "A pointer to nothing", "A deleted pointer"], 2, "NULL means the pointer points nowhere."),
        _quiz("Pointer arithmetic increments by:", ["1 byte always", "The size of the pointed type", "10", "Random"], 1, "ptr + 1 advances by sizeof(*ptr) bytes."),
    ],
    "c-memory": [
        _quiz("What does malloc do?", ["Frees memory", "Allocates dynamic memory", "Copies strings", "Deletes pointers"], 1, "malloc allocates heap memory."),
        _quiz("What happens if you lose a pointer to malloc'd memory?", ["It auto-frees", "Memory leak", "Segfault immediately", "Nothing"], 1, "Lost allocations are unrecoverable."),
        _quiz("Stack vs heap: stack is:", ["Slower", "Faster with fixed-size storage", "Unlimited", "For dynamic arrays"], 1, "Stack allocation is fast but size-limited."),
        _quiz("What is a segmentation fault?", ["A disk error", "Accessing invalid memory", "A network timeout", "A syntax error"], 1, "Segfaults happen when touching invalid memory."),
        _quiz("free() is needed because:", ["C has garbage collection", "C requires manual heap cleanup", "malloc is slow", "Pointers auto-delete"], 1, "C has no GC; malloc must be paired with free()."),
    ],
    "c-enums-structs": [
        _quiz("An enum defines:", ["A loop", "Named integer constants", "A function", "A string"], 1, "enum gives names to integer constants."),
        _quiz("A struct groups:", ["Functions", "Related data fields", "Loops", "Headers"], 1, "structs bundle related fields."),
        _quiz("How do you access a struct member via pointer?", ["ptr.member", "ptr->member", "ptr.member()", "ptr::member"], 1, "The arrow operator dereferences and accesses."),
        _quiz("Union memory is:", ["Sum of all members", "Size of the largest member", "Always 4 bytes", "Always 16 bytes"], 1, "A union shares memory among members."),
        _quiz("Which is typically faster?", ["struct", "union", "class", "enum"], 1, "Unions can be faster with one active member."),
    ],
    "c-preprocessors-files": [
        _quiz("#include does:", ["Compiles a file", "Copies header contents into source", "Links libraries", "Creates macros"], 1, "#include pastes header contents."),
        _quiz("#define is used for:", ["Variables", "Constants / macros", "Functions only", "Comments"], 1, "#define creates macros and constants."),
        _quiz("A header guard prevents:", ["Syntax errors", "Multiple inclusion", "Memory leaks", "Segfaults"], 1, "Include guards skip repeated inclusions."),
        _quiz("fprintf(stderr, ...) is used for:", ["Normal output", "Error messages", "File writing", "Debugging only"], 1, "stderr is the standard error stream."),
        _quiz("Binary file mode is:", ["'r'", "'rb'", "'w'", "'a'"], 1, "'rb'/'wb' preserve binary data."),
    ],
    "fullstack-architecture": [
        _quiz("In full-stack apps, the frontend:", ["Directly queries the database", "Talks to the backend API", "Runs SQL", "Handles auth alone"], 1, "Frontend consumes a backend API."),
        _quiz("REST stands for:", ["Remote Execution Service", "Representational State Transfer", "Real-time Event Streaming", "Resource Endpoint Standard"], 1, "REST is an architectural style for APIs."),
        _quiz("JWT is commonly used for:", ["Database indexing", "Stateless authentication", "CSS styling", "File compression"], 1, "JWTs encode user claims for auth."),
        _quiz("Horizontal scaling means:", ["Bigger server", "More server instances", "Faster CPU", "More RAM"], 1, "Horizontal scaling adds more machines."),
        _quiz("A load balancer:", ["Stores data", "Distributes traffic across servers", "Renders HTML", "Replaces the database"], 1, "Load balancers spread requests across instances."),
    ],
    "tcs-nqt-2026-guide": [
        _quiz("TCS NQT 2026 has no negative marking. What should you do with 10 seconds left?", ["Leave blanks to stay safe", "Attempt every unanswered question", "Skip to save time", "Review earlier answers"], 1, "Blank and wrong both score zero, so guess."),
        _quiz("How many Advanced Coding problems and how long?", ["3 in 60 minutes", "2 in 90 minutes", "1 in 45 minutes", "5 in 120 minutes"], 1, "Advanced Coding is 2 problems in 90 minutes."),
        _quiz("Which performance gates the Prime band?", ["Verbal Ability", "Foundation alone", "Advanced Coding at ~80th percentile", "Reasoning speed"], 2, "Prime is decided by Advanced Coding performance."),
    ],
}

ARTICLE_EXERCISES = {
    "html-basics": _exercise(
        "Build a profile card",
        "Create an HTML file with a profile card containing an image, name, bio paragraph, and three social links. Use semantic tags: header, main, section, footer. Include alt text for the image and a title in head.",
        "<!DOCTYPE html>\n<html>\n  <head>\n    <title>My Profile</title>\n  </head>\n  <body>\n    <!-- Add your profile card here -->\n  </body>\n</html>",
        "<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset='UTF-8'>\n    <title>Ada Lovelace</title>\n  </head>\n  <body>\n    <header><h1>Ada Lovelace</h1></header>\n    <main>\n      <section class='profile'>\n        <img src='ada.jpg' alt='Portrait of Ada Lovelace' width='200'>\n        <p>The first computer programmer.</p>\n        <nav>\n          <a href='#github'>GitHub</a>\n          <a href='#linkedin'>LinkedIn</a>\n          <a href='#twitter'>Twitter</a>\n        </nav>\n      </section>\n    </main>\n    <footer><p>Built with HTML5</p></footer>\n  </body>\n</html>",
        "Use <article> inside <main> for the profile card."
    ),
    "css-basics": _exercise(
        "Style a card with the box model",
        "Create a .card with width: 300px, padding: 16px, border: 1px solid #ddd, margin: 12px, and box-sizing: border-box. Add an h2 and paragraph inside. Make the card background light gray and center it on the page.",
        "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    /* Add your styles here */\n  </style>\n</head>\n<body>\n  <div class='card'>\n    <h2>Hello</h2>\n    <p>This is a card.</p>\n  </div>\n</body>\n</html>",
        "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    * { box-sizing: border-box; }\n    body { display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; font-family: system-ui; }\n    .card { width: 300px; padding: 16px; border: 1px solid #ddd; margin: 12px; background: #f9f9f9; border-radius: 8px; }\n    .card h2 { margin-top: 0; }\n  </style>\n</head>\n<body>\n  <div class='card'>\n    <h2>Hello</h2>\n    <p>This is a card styled with the box model.</p>\n  </div>\n</body>\n</html>",
        "Remember: border-box makes width include padding and border."
    ),
    "css-flexbox-grid": _exercise(
        "Build a responsive navbar with flexbox",
        "Create a navbar with 4 links. Use flexbox with justify-content: space-between. Add a logo on the left and links on the right. Make it wrap on small screens.",
        "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    nav { display: flex; /* add flex properties */ }\n  </style>\n</head>\n<body>\n  <nav>\n    <div class='logo'>MyLogo</div>\n    <div class='links'>\n      <a href='#'>Home</a>\n      <a href='#'>About</a>\n      <a href='#'>Contact</a>\n      <a href='#'>Blog</a>\n    </div>\n  </nav>\n</body>\n</html>",
        "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    * { box-sizing: border-box; margin: 0; }\n    nav { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: #1a1a1a; flex-wrap: wrap; gap: 12px; }\n    .logo { color: white; font-weight: bold; font-size: 1.25rem; }\n    .links { display: flex; gap: 16px; }\n    .links a { color: #ccc; text-decoration: none; }\n    .links a:hover { color: white; }\n  </style>\n</head>\n<body>\n  <nav>\n    <div class='logo'>MyLogo</div>\n    <div class='links'>\n      <a href='#'>Home</a>\n      <a href='#'>About</a>\n      <a href='#'>Contact</a>\n      <a href='#'>Blog</a>\n    </div>\n  </nav>\n</body>\n</html>",
        "Use flex-wrap to prevent overflow on small screens."
    ),
    "css-responsive": _exercise(
        "Make a two-column layout responsive",
        "Create a two-column layout with CSS Grid that collapses to a single column below 768px. Use a media query with max-width: 768px.",
        "<!DOCTYPE html>\n<html>\n<head>\n  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n  <style>\n    .container { display: grid; /* add grid template */ }\n  </style>\n</head>\n<body>\n  <div class='container'>\n    <aside>Sidebar</aside>\n    <main>Main content here</main>\n  </div>\n</body>\n</html>",
        "<!DOCTYPE html>\n<html>\n<head>\n  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n  <style>\n    * { box-sizing: border-box; }\n    .container { display: grid; grid-template-columns: 1fr 3fr; gap: 16px; padding: 16px; }\n    aside { background: #f4f4f4; padding: 16px; }\n    main { background: #fff; padding: 16px; border: 1px solid #eee; }\n    @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }\n  </style>\n</head>\n<body>\n  <div class='container'>\n    <aside>Sidebar</aside>\n    <main>Main content here</main>\n  </div>\n</body>\n</html>",
        "Mobile-first means default styles are for small screens; min-width adds complexity."
    ),
    "js-variables-types": _exercise(
        "Type coercion detective",
        "Predict the output of each console.log statement without running it. Then run the code to check. Focus on == vs === and type coercion.",
        "console.log(5 == '5');\nconsole.log(5 === '5');\nconsole.log(true + 1);\nconsole.log('10' - 1);\nconsole.log(null == undefined);\nconsole.log(Boolean(''));",
        "console.log(5 == '5');   // true\nconsole.log(5 === '5');  // false\nconsole.log(true + 1);   // 2\nconsole.log('10' - 1);   // 9\nconsole.log(null == undefined); // true\nconsole.log(Boolean('')); // false",
        "Remember: == allows coercion; === does not."
    ),
    "js-functions": _exercise(
        "Write a reusable counter",
        "Create a function createCounter() that returns an object with increment(), decrement(), and count() methods. The count should be private using a closure.",
        "function createCounter() {\n  // Add your code here\n}\n\nconst counter = createCounter();\ncounter.increment();\ncounter.increment();\nconsole.log(counter.count()); // 2\ncounter.decrement();\nconsole.log(counter.count()); // 1",
        "function createCounter() {\n  let count = 0;\n  return {\n    increment() { count++; },\n    decrement() { count--; },\n    count() { return count; }\n  };\n}",
        "Use a local variable inside createCounter — that is the closure."
    ),
    "js-arrays-objects": _exercise(
        "Transform student grades",
        "Given an array of student objects with name and score, return a new array of names of students who scored above 60. Use .filter() and .map(). Do not mutate the original array.",
        "const students = [\n  { name: 'Ada', score: 82 },\n  { name: 'Bob', score: 45 },\n  { name: 'Cara', score: 91 },\n];\n\n// Write your code here\nconsole.log(passing); // ['Ada', 'Cara']",
        "const passing = students\n  .filter(s => s.score > 60)\n  .map(s => s.name);",
        "filter returns a new array; map transforms each item."
    ),
    "js-async": _exercise(
        "Fetch and display posts",
        "Write an async function that fetches from https://jsonplaceholder.typicode.com/posts/1 and logs the title. Use try/catch for error handling.",
        "async function loadPost() {\n  // Add your code here\n}\n\nloadPost();",
        "async function loadPost() {\n  try {\n    const res = await fetch('https://jsonplaceholder.typicode.com/posts/1');\n    const data = await res.json();\n    console.log(data.title);\n  } catch (err) {\n    console.error('Failed:', err);\n  }\n}",
        "Remember to call res.json() on the response object."
    ),
    "ts-why-types": _exercise(
        "Add types to a function",
        "Convert this JavaScript function to TypeScript. Add types for parameters and return value. Use an interface for the user object.",
        "function greet(user) {\n  return `Hello, ${user.name}`;\n}\n\nconsole.log(greet({ name: 'Ada' }));",
        "interface User { name: string; age?: number; }\nfunction greet(user: User): string {\n  return `Hello, ${user.name}`;\n}\n\nconsole.log(greet({ name: 'Ada' }));",
        "Use interface to describe the expected shape of user."
    ),
    "ts-interfaces-generics": _exercise(
        "Build a generic storage box",
        "Create a generic Box<T> interface with contents: T and a get() method that returns T. Create a StringBox and NumberBox from it.",
        "// Define Box interface here\n\n// Create instances\nconst stringBox = { contents: 'hello', get() { return this.contents; } };\nconst numberBox = { contents: 42, get() { return this.contents; } };\n\nconsole.log(stringBox.get());\nconsole.log(numberBox.get());",
        "interface Box<T> { contents: T; get(): T; }\n\nconst stringBox: Box<string> = { contents: 'hello', get() { return this.contents; } };\nconst numberBox: Box<number> = { contents: 42, get() { return this.contents; } };\n\nconsole.log(stringBox.get());\nconsole.log(numberBox.get());",
        "Generics let one interface work with many types safely."
    ),
    "react-components": _exercise(
        "Build a greeting component",
        "Create a Greeting component that accepts a name prop and displays 'Hello, {name}!'. Render it with name='Ada'.",
        "function Greeting() {\n  return <div>Hello!</div>;\n}\n\n// Render with name='Ada'",
        "function Greeting({ name }) {\n  return <div>Hello, {name}!</div>;\n}\n\n// Usage:\n// <Greeting name='Ada' />",
        "Props are passed as the first argument to a function component."
    ),
    "react-hooks": _exercise(
        "Toggle with useState",
        "Create a Toggle component using useState that shows 'ON' when true and 'OFF' when false. Clicking the button toggles the state.",
        "import { useState } from 'react';\n\nfunction Toggle() {\n  // Add state here\n  return (\n    <button onClick={/* add handler */}>\n      {/* show state */}\n    </button>\n  );\n}",
        "import { useState } from 'react';\n\nfunction Toggle() {\n  const [on, setOn] = useState(false);\n  return (\n    <button onClick={() => setOn(!on)}>\n      {on ? 'ON' : 'OFF'}\n    </button>\n  );\n}",
        "useState returns [state, setter] — call setter to update."
    ),
    "react-performance": _exercise(
        "Memoize an expensive list",
        "You have a list of 1000 items being rendered. Wrap the list item component in React.memo to prevent re-renders when item data does not change.",
        "const Item = ({ item }) => {\n  console.log('Render:', item.id);\n  return <div>{item.name}</div>;\n};\n\nfunction List({ items }) {\n  return items.map(i => <Item key={i.id} item={i} />);\n}",
        "const Item = React.memo(({ item }) => {\n  console.log('Render:', item.id);\n  return <div>{item.name}</div>;\n});\n\n// Optional: use useMemo for the list if parent re-renders\nconst memoizedItems = useMemo(() => items, [items]);",
        "React.memo does a shallow prop comparison."
    ),
    "node-server": _exercise(
        "Create a basic Express server",
        "Create an Express server on port 3000 with GET /health returning {status: 'ok'} and GET /api/items returning a JSON array of 3 items.",
        "const express = require('express');\nconst app = express();\n\n// Add routes here\n\napp.listen(3000, () => console.log('Server running'));",
        "const express = require('express');\nconst app = express();\n\napp.get('/health', (req, res) => {\n  res.json({ status: 'ok' });\n});\n\napp.get('/api/items', (req, res) => {\n  res.json([{ id: 1, name: 'Pen' }, { id: 2, name: 'Notebook' }, { id: 3, name: 'Laptop' }]);\n});\n\napp.listen(3000, () => console.log('Server running on 3000'));",
        "app.get(path, handler) registers a route; res.json sends JSON."
    ),
    "node-files-streams": _exercise(
        "Copy a file using streams",
        "Create a script that reads from notes.txt and writes to backup.txt using fs.createReadStream and fs.createWriteStream. Pipe the streams together and log 'Done' when finished.",
        "const fs = require('fs');\n\nconst read = fs.createReadStream('notes.txt');\nconst write = fs.createWriteStream('backup.txt');\n\n// Pipe and log completion\n\nread.on('error', err => console.error('Read error:', err));\nwrite.on('error', err => console.error('Write error:', err));\nwrite.on('finish', () => console.log('Done'));",
        "const fs = require('fs');\n\nconst read = fs.createReadStream('notes.txt');\nconst write = fs.createWriteStream('backup.txt');\n\nread.pipe(write);\n\nread.on('error', err => console.error('Read error:', err));\nwrite.on('error', err => console.error('Write error:', err));\nwrite.on('finish', () => console.log('Done'));",
        "pipe() connects a readable stream to a writable stream automatically."
    ),
    "sql-select": _exercise(
        "Query employees by department",
        "Write a SQL query that selects name and salary from employees where department = 'Engineering' and salary > 80000, ordered by salary descending.",
        "SELECT name, salary\nFROM employees\n-- Add WHERE and ORDER BY",
        "SELECT name, salary\nFROM employees\nWHERE department = 'Engineering'\n  AND salary > 80000\nORDER BY salary DESC;",
        "Use WHERE for filtering and ORDER BY for sorting."
    ),
    "sql-database": _exercise(
        "Design a simple school schema",
        "Create two tables: students(id, name, grade) and enrollments(id, student_id, course). Add a primary key to each and a foreign key from enrollments.student_id to students.id.",
        "CREATE TABLE students (\n  id INT,\n  name TEXT,\n  grade INT\n);\n\nCREATE TABLE enrollments (\n  id INT,\n  student_id INT,\n  course TEXT\n);",
        "CREATE TABLE students (\n  id INT PRIMARY KEY,\n  name TEXT NOT NULL,\n  grade INT\n);\n\nCREATE TABLE enrollments (\n  id INT PRIMARY KEY,\n  student_id INT REFERENCES students(id),\n  course TEXT NOT NULL\n);",
        "Foreign keys use REFERENCES to point to another table's primary key."
    ),
    "c-pointers": _exercise(
        "Swap two numbers using pointers",
        "Write a swap function that takes two int pointers and swaps the values they point to. Call it from main and print both values after.",
        "#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n  // swap values here\n}\n\nint main() {\n  int x = 5, y = 10;\n  swap(&x, &y);\n  printf(\"x=%d, y=%d\", x, y);\n  return 0;\n}",
        "#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n  int temp = *a;\n  *a = *b;\n  *b = temp;\n}\n\nint main() {\n  int x = 5, y = 10;\n  swap(&x, &y);\n  printf(\"x=%d, y=%d\", x, y); // x=10, y=5\n  return 0;\n}",
        "Dereference with * to read/write the pointed-to value."
    ),
    "c-memory": _exercise(
        "Find the leak",
        "This C program allocates memory for 10 integers but has a memory leak. Identify and fix it using free().",
        "#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n  int *arr = malloc(10 * sizeof(int));\n  for (int i = 0; i < 10; i++) arr[i] = i;\n  // Missing free here\n  return 0;\n}",
        "#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n  int *arr = malloc(10 * sizeof(int));\n  for (int i = 0; i < 10; i++) arr[i] = i;\n  free(arr); // cleanup\n  arr = NULL;\n  return 0;\n}",
        "Every malloc needs a matching free in the same scope."
    ),
    "c-enums-structs": _exercise(
        "Model a book with struct",
        "Create a Book struct with title (string), pages (int), and price (float). Write a function printBook that takes a Book pointer and prints its fields.",
        "#include <stdio.h>\n#include <string.h>\n\n// Define Book struct here\n\nvoid printBook(/* add parameter */) {\n  // print fields\n}\n\nint main() {\n  Book b = {\"C Programming\", 300, 29.99};\n  printBook(&b);\n  return 0;\n}",
        "#include <stdio.h>\n#include <string.h>\n\ntypedef struct {\n  char title[100];\n  int pages;\n  float price;\n} Book;\n\nvoid printBook(const Book *b) {\n  printf(\"Title: %s\\nPages: %d\\nPrice: %.2f\\n\", b->title, b->pages, b->price);\n}\n\nint main() {\n  Book b = {\"C Programming\", 300, 29.99};\n  printBook(&b);\n  return 0;\n}",
        "Use typedef with struct for cleaner syntax."
    ),
    "c-preprocessors-files": _exercise(
        "Write a safe header",
        "Create a header file calculator.h with add and subtract function declarations. Add include guards. Then use it in main.c.",
        "// calculator.h\n#ifndef CALCULATOR_H\n#define CALCULATOR_H\n// Add declarations\n#endif",
        "// calculator.h\n#ifndef CALCULATOR_H\n#define CALCULATOR_H\n\nint add(int a, int b);\nint subtract(int a, int b);\n\n#endif\n\n// main.c\n#include <stdio.h>\n#include \"calculator.h\"\n\nint add(int a, int b) { return a + b; }\nint subtract(int a, int b) { return a - b; }\n\nint main() {\n  printf(\"%d\\n\", add(5, 3));\n  return 0;\n}",
        "Include guards use #ifndef / #define / #endif with a unique macro name."
    ),
    "fullstack-architecture": _exercise(
        "Sketch a URL shortener API",
        "Design 3 REST endpoints for a URL shortener: POST /api/links to create, GET /api/links/:id to retrieve, and GET /:code to redirect. Describe the request/response bodies.",
        "POST /api/links\nBody: { url: \"https://example.com\" }\n\nGET /api/links/:id\n\nGET /:code",
        "POST /api/links — Body: { url: string }; Response: { id, code, short_url }\nGET /api/links/:id — Response: { id, code, url, clicks }\nGET /:code — 302 redirect to the original URL",
        "Keep routes RESTful and return consistent JSON shapes."
    ),
}


def patch_study_materials():
    with open(STUDY_PATH, "r", encoding="utf-8") as f:
        src = f.read()

    # Find each article block by id and inject quiz/exercise before closing )
    import re

    updated = 0
    for article_id, quiz in ARTICLE_QUIZZES.items():
        # Find the _article call for this id
        pattern = rf'(_article\(\s*\n\s*"{re.escape(article_id)}"[,)]+)'
        match = re.search(pattern, src)
        if not match:
            continue

        start = match.start()
        # Find matching closing paren
        paren_start = src.find('(', match.start(1))
        depth = 1
        i = paren_start + 1
        while i < len(src) and depth > 0:
            if src[i] == '(':
                depth += 1
            elif src[i] == ')':
                depth -= 1
            i += 1

        block = src[start:i]
        trimmed = block.rstrip()
        if trimmed.endswith(')'):
            trimmed = trimmed[:-1].rstrip()

        additions = []
        if "quiz=" not in trimmed:
            additions.append(f"        quiz={repr(quiz)},")
        if article_id in ARTICLE_EXERCISES and "exercise=" not in trimmed:
            additions.append(f"        exercise={repr(ARTICLE_EXERCISES[article_id])},")

        if additions:
            new_block = trimmed + "\n" + "\n".join(additions) + "\n    )"
            src = src[:start] + new_block + src[i:]
            updated += 1

    with open(STUDY_PATH, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"Updated {updated} articles in study_materials.py")


def patch_scrimba_lessons():
    scrimba_path = os.path.join(BACKEND_ROOT, "app", "content", "scrimba_lessons.py")
    with open(scrimba_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Add interactions to slides based on content keywords
    interaction_map = {
        "HTML is not a programming language — it is the markup": _mcq(
            "What is HTML?", [
                {"label": "A programming language", "correct": False},
                {"label": "A markup language for structure", "correct": True},
                {"label": "A database query language", "correct": False},
                {"label": "A CSS framework", "correct": False},
            ],
            "HTML provides structure and meaning; JavaScript provides behavior."
        ),
        "box-sizing: border-box": _mcq(
            "With border-box, what is included in width?", [
                {"label": "Only content", "correct": False},
                {"label": "Content + padding + border", "correct": True},
                {"label": "Content + margin", "correct": False},
                {"label": "Padding + margin", "correct": False},
            ],
            "border-box includes padding and border inside the declared width."
        ),
        "let and const are block-scoped": _mcq(
            "Which keyword declares a block-scoped variable?", [
                {"label": "var", "correct": False},
                {"label": "let", "correct": True},
                {"label": "static", "correct": False},
                {"label": "global", "correct": False},
            ],
            "let and const are block-scoped; var is function-scoped."
        ),
        "typeof null returns 'object'": _mcq(
            "What is the output of typeof null?", [
                {"label": "'null'", "correct": False},
                {"label": "'undefined'", "correct": False},
                {"label": "'object'", "correct": True},
                {"label": "'boolean'", "correct": False},
            ],
            "typeof null returns 'object' — a known JavaScript quirk."
        ),
        "A closure is a function that retains access": _mcq(
            "What is a closure?", [
                {"label": "A closed HTML tag", "correct": False},
                {"label": "A function that remembers its outer scope", "correct": True},
                {"label": "A loop structure", "correct": False},
                {"label": "An error handler", "correct": False},
            ],
            "A closure is a function that retains access to its lexical scope."
        ),
        "async/await makes Promise chains look synchronous": _mcq(
            "What does async/await simplify?", [
                {"label": "Object creation", "correct": False},
                {"label": "Promise-based code", "correct": True},
                {"label": "CSS animations", "correct": False},
                {"label": "HTML parsing", "correct": False},
            ],
            "async/await makes Promise chains look synchronous."
        ),
        "TypeScript adds optional static types": _mcq(
            "What is TypeScript's main purpose?", [
                {"label": "Replace JavaScript entirely", "correct": False},
                {"label": "Add static types to JavaScript", "correct": True},
                {"label": "Make code run faster", "correct": False},
                {"label": "Remove bugs automatically", "correct": False},
            ],
            "TypeScript adds optional static types to JavaScript."
        ),
        "React components are the reusable units": _mcq(
            "What is a React component?", [
                {"label": "An HTML file", "correct": False},
                {"label": "A reusable UI building block", "correct": True},
                {"label": "A CSS class", "correct": False},
                {"label": "A database query", "correct": False},
            ],
            "Components are the reusable units of React UI."
        ),
        "Node.js runs JavaScript on the server": _mcq(
            "What is Node.js?", [
                {"label": "A database", "correct": False},
                {"label": "JavaScript runtime for servers", "correct": True},
                {"label": "A frontend framework", "correct": False},
                {"label": "A CSS tool", "correct": False},
            ],
            "Node.js runs JavaScript on the server with V8."
        ),
        "SQL = Structured Query Language": _mcq(
            "What does SQL stand for?", [
                {"label": "Simple Query Language", "correct": False},
                {"label": "Structured Query Language", "correct": True},
                {"label": "Standard Query Logic", "correct": False},
                {"label": "System Query Language", "correct": False},
            ],
            "SQL = Structured Query Language."
        ),
        "Pointers hold memory addresses": _mcq(
            "What does a pointer store?", [
                {"label": "A value", "correct": False},
                {"label": "A memory address", "correct": True},
                {"label": "A function name", "correct": False},
                {"label": "A type", "correct": False},
            ],
            "Pointers hold memory addresses of other variables."
        ),
        "malloc allocates heap memory": _mcq(
            "What does malloc do?", [
                {"label": "Frees memory", "correct": False},
                {"label": "Allocates dynamic memory", "correct": True},
                {"label": "Copies strings", "correct": False},
                {"label": "Deletes pointers", "correct": False},
            ],
            "malloc allocates heap memory at runtime."
        ),
    }

    # Fill-in interactions for code slides
    fill_map = {
        "for i in range(3):": _fill("Complete: for i in ____(3):", "range", "Use range() to create a sequence."),
        "if x > 5:": _fill("Complete: if x ____ 5:", ">", "Use > for greater than comparison."),
        "def greet()": _fill("What keyword starts a function?", "def", "Python uses def to define functions."),
        "console.log": _fill("What method prints to the console?", "console.log", "Use console.log() to output values."),
        "SELECT": _fill("Complete: ____ * FROM users", "SELECT", "SELECT chooses columns in SQL."),
        "malloc": _fill("What allocates heap memory?", "malloc", "malloc() allocates dynamic memory."),
        "->": _fill("What operator accesses a struct member via pointer?", "->", "The arrow operator dereferences and accesses a member."),
        "#include": _fill("What directive includes header files?", "#include", "#include copies header contents into the source."),
        "interface User": _fill("What keyword defines an interface?", "interface", "interface Name { ... } defines a type shape."),
        "useState": _fill("What hook adds state to function components?", "useState", "useState returns [state, setter]."),
        "React.memo": _fill("What skips re-renders when props are equal?", "React.memo", "React.memo memoizes renders."),
        "app.get": _fill("What method registers a route in Express?", "app.get", "app.get(path, handler) registers a GET route."),
        "createReadStream": _fill("What creates a readable stream?", "createReadStream", "fs.createReadStream opens a file stream for reading."),
        "WHERE": _fill("Complete: SELECT * FROM users ____ age > 18", "WHERE", "WHERE filters rows."),
        "PRIMARY KEY": _fill("What makes a column unique?", "PRIMARY KEY", "PRIMARY KEY uniquely identifies each row."),
        "int main()": _fill("What is the entry point of a C program?", "main", "int main() is where execution starts."),
        "free(": _fill("What function frees heap memory?", "free", "free() deallocates heap memory."),
        "typedef struct": _fill("What keyword creates a struct type alias?", "typedef struct", "typedef struct { ... } Name; creates a new type."),
        "#define": _fill("What preprocessor directive creates constants?", "#define", "#define creates macros and constants."),
    }

    # Find all _slide( calls and inject interactions
    # We need to find each slide dict and add interaction if missing
    lines = src.split('\n')
    new_lines = []
    i = 0
    updated = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        i += 1

        # Look for _slide( calls
        if '_slide(' in line:
            # Find the end of this _slide call
            slide_lines = [line]
            depth = line.count('(') - line.count(')')
            while i < len(lines) and depth > 0:
                slide_lines.append(lines[i])
                depth += lines[i].count('(') - lines[i].count(')')
                i += 1

            slide_text = '\n'.join(slide_lines)

            # Skip if already has interaction
            if 'interaction=' in slide_text:
                new_lines.extend(slide_lines[1:])
                continue

            # Check for MCQ keywords
            interaction = None
            for keyword, mcq in interaction_map.items():
                if keyword in slide_text:
                    interaction = mcq
                    break

            # Check for fill-in keywords
            if not interaction:
                for keyword, fill in fill_map.items():
                    if keyword in slide_text:
                        interaction = fill
                        break

            if interaction:
                # Insert interaction before the closing )
                last_line = new_lines[-1]
                new_lines.pop()
                indent = '            '
                new_lines.append(f"{indent}interaction={repr(interaction)},")
                new_lines.append(last_line)
                updated += 1

    with open(scrimba_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))
    print(f"Updated {updated} slides in scrimba_lessons.py")


if __name__ == "__main__":
    patch_study_materials()
    patch_scrimba_lessons()
    print("Done. Restart backend to see changes.")
