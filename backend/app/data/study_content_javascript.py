"""JavaScript category expansion content for the Study Library.

Standalone module (no imports from app.data.study_materials) so that
study_materials can import NEW_ARTICLES and INTERACTIVES here without a
circular import. The helper functions below mirror the ones in study_materials.
"""

from typing import Any


def _section(heading, body, code=None, pro_tip=""):
    s = {"heading": heading, "body": body}
    if code:
        s["code"] = code
    if pro_tip:
        s["pro_tip"] = pro_tip
    return s


def _quiz(question, options, answer, explanation):
    return {"question": question, "options": options, "answer": answer, "explanation": explanation}


def _exercise(title, task, starter, solution, hint=""):
    ex = {"title": title, "task": task, "starter": starter, "solution": solution}
    if hint:
        ex["hint"] = hint
    return ex


NEW_ARTICLES = [
    # ────────────────────────── JavaScript ──────────────────────────
    {
        "id": "js-event-loop",
        "title": "The Event Loop: How JavaScript Really Executes",
        "category": "javascript",
        "summary": "JavaScript runs on one thread, yet pages stay responsive. The event loop is the traffic cop: call stack, microtask queue, and macrotask queue — and the exact order they drain in.",
        "level": "advanced",
        "read_time_min": 13,
        "related_topics": ["js-async", "js-functions"],
        "sections": [
            _section(
                "One thread, one call stack",
                "JavaScript is single-threaded: the engine executes code on a single call stack, one function frame at a time. When a function calls another, the new frame is pushed on top; when a function returns, its frame pops off. Because there is exactly one stack, a function that never returns (or takes 2 seconds of CPU) blocks everything else — clicks, renders, the lot. Everything else you hear about concurrency in JS is really about scheduling work around that single stack.",
                "const first = () => second();\nconst second = () => third();\nconst third = () => console.log('third');\n\nfirst(); // third\n// stack: first → second → third, each pushed then popped\n// when the stack is empty again, the event loop can breathe",
            ),
            _section(
                "The call stack and the task queue",
                "Browsers and Node.js are not single-threaded — the OS gives them extra threads for I/O. When you call setTimeout, the timer runs on a background thread, and when it fires, it does NOT run your callback immediately. It pushes your callback onto a task (macrotask) queue. The event loop constantly checks: is the call stack empty? If yes, pull one task off the queue and run it. If the stack is busy, the callback waits — no matter how long.",
                "console.log('hi');\n\nsetTimeout(() => {\n  console.log('later');\n}, 0);\n\nconsole.log('bye');\n// hi, bye, later\n// 'later' only runs after the stack clears, even with a 0ms delay",
            ),
            _section(
                "Microtasks vs macrotasks — the ordering rules",
                "There is not one queue but two, and their priority is the key insight. Macrotasks (setTimeout, setInterval, I/O callbacks, DOM events) run one at a time, and after each one the loop drains the ENTIRE microtask queue before touching the next macrotask. Microtasks are Promise.then handlers, queueMicrotask, and async/await continuations. That is why a promise scheduled after a setTimeout still runs first.",
                "console.log('1');\n\nsetTimeout(() => console.log('2'), 0);\n\nPromise.resolve().then(() => {\n  console.log('3');\n  queueMicrotask(() => console.log('4'));\n});\n\nconsole.log('5');\n\n// Output: 1, 5, 3, 4, 2\n// '2' is a macrotask; microtasks '3' and '4' drain before it",
            ),
            _section(
                "Why the loop keeps the UI fast",
                "Every await in your async functions returns control to the event loop, letting the page paint and respond. But the loop only helps if the stack stays empty — heavy synchronous CPU work (a giant loop, image processing) starves it. Offload such work to a Web Worker or chunk it, and remember that await is not parallelism; it is cooperation.",
                "// Blocking the stack for 2 seconds freezes clicks, hovers, everything\nconst t0 = performance.now();\nwhile (performance.now() - t0 < 2000) {}\nconsole.log('finally free');\n\n// Offload instead: new Worker('heavy.js')",
                "Pro tip: microtasks drain in a loop — if a microtask keeps queueing more microtasks, timers and I/O starve forever. Keep microtask work short and bounded.",
            ),
        ],
        "key_takeaways": [
            "JavaScript runs on one thread; blocking the call stack freezes the page",
            "setTimeout and I/O callbacks are macrotasks; promise handlers are microtasks",
            "Microtasks drain completely before the next macrotask runs",
            "Each await hands control back to the event loop, keeping the UI responsive",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Given this code:\nconsole.log('a');\nsetTimeout(() => console.log('b'), 0);\nPromise.resolve().then(() => console.log('c'));\nconsole.log('d');\n\nWhat is the output order?",
                ["a, b, c, d", "a, d, c, b", "a, d, b, c", "a, c, d, b"],
                1,
                "The synchronous lines run first (a, d). Then the entire microtask queue drains (c), and only after that does the setTimeout macrotask run (b).",
            ),
            _quiz(
                "Which of these is scheduled as a macrotask?",
                ["Promise.then callback", "queueMicrotask callback", "setTimeout callback", "async function body (before the first await)"],
                2,
                "Timers like setTimeout and setInterval produce macrotasks. Promise.then, queueMicrotask, and the parts of an async function after await are microtasks.",
            ),
            _quiz(
                "When does the event loop pull the next macrotask from the task queue?",
                ["After every synchronous line of code", "Only when the call stack is empty and the microtask queue is drained", "As soon as the task is scheduled", "Every 10 milliseconds"],
                1,
                "The loop runs when the stack clears, and before each macrotask it must fully empty the microtask queue. That two-step check is the entire event loop.",
            ),
        ],
        "exercise": _exercise(
            "Log before the timeout",
            "Queue a microtask that logs 'micro' so it prints after the synchronous logs but before the setTimeout callback.",
            "console.log('sync start');\n\nsetTimeout(() => console.log('timer'), 0);\n\n// queue a microtask that logs 'micro'\n\nconsole.log('sync end');",
            "console.log('sync start');\n\nsetTimeout(() => console.log('timer'), 0);\n\nqueueMicrotask(() => console.log('micro'));\n\nconsole.log('sync end');\n\n// Output: sync start, sync end, micro, timer",
            "queueMicrotask schedules a microtask — the whole microtask queue drains before any timer fires.",
        ),
        "curriculum": ["javascript"],
    },
    {
        "id": "js-dom-events",
        "title": "DOM Manipulation and Event Handling",
        "category": "javascript",
        "summary": "The DOM is the document as an object tree you can read and edit. Combine querySelector selection, addEventListener, and event delegation and you can build any interface.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["js-variables-types", "js-functions"],
        "sections": [
            _section(
                "Selecting elements",
                "getElementById is the fastest way to one element by its unique id. querySelector and querySelectorAll accept any CSS selector, which makes them the workhorse. querySelectorAll returns a NodeList — not an array — so spread it before using array methods like forEach, filter, or map.",
                "const header = document.getElementById('header');\n\nconst firstButton = document.querySelector('.btn');\nconst allButtons = document.querySelectorAll('.btn');\nconst buttons = [...allButtons]; // now a real array\n\nconsole.log(header.textContent, buttons.length);",
            ),
            _section(
                "addEventListener and removing listeners",
                "addEventListener(type, handler) runs the handler when the event fires. Anonymous handlers work but cannot be removed later — if you might need removeEventListener, keep a named reference. Unlike the old onclick attribute, addEventListener lets you attach multiple handlers and control the capture phase.",
                "const btn = document.getElementById('save');\n\nfunction onSave(event) {\n  event.preventDefault();\n  console.log('Saved!');\n}\n\nbtn.addEventListener('click', onSave);\n// later: remove exactly this listener\nbtn.removeEventListener('click', onSave);",
            ),
            _section(
                "Bubbling vs capturing",
                "An event does not just fire on the target — it travels. In the capturing phase it walks from the document DOWN to the target; in the bubbling phase it walks from the target back UP to the document. Handlers run in the bubble phase by default. Pass true as the third argument to addEventListener to run during capture instead. stopPropagation() halts the journey mid-flight.",
                "// default: bubble phase (target → document)\ndocument.querySelector('body').addEventListener('click', () => {\n  console.log('bubble phase');\n});\n\n// pass true to run during capture (document → target)\ndocument.querySelector('body').addEventListener('click', handler, true);\n\n// stop the event from traveling any further\nchild.addEventListener('click', (event) => event.stopPropagation());",
            ),
            _section(
                "Event delegation: one listener for many elements",
                "Because events bubble, you can attach ONE listener to a stable ancestor and let it handle events for any number of children — including ones added later. Read event.target, then use closest() to find the real element. This is the standard pattern for lists, menus, and tables, and it replaces hundreds of per-item listeners.",
                "const list = document.getElementById('todo-list');\n\nlist.addEventListener('click', (event) => {\n  const item = event.target.closest('li');\n  if (!item) return;\n  item.classList.toggle('done');\n});",
                "Pro tip: delegation survives dynamically added children — new list items need zero wiring because the ancestor listens for them. Use event.currentTarget for the listener element and event.target for the clicked element.",
            ),
        ],
        "key_takeaways": [
            "Use querySelector for single elements and querySelectorAll + spread for lists",
            "Named handlers can be removed; anonymous ones cannot",
            "Events bubble by default; pass true as the third argument for capturing",
            "Event delegation on an ancestor handles current and future child elements",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which method selects the FIRST element matching a CSS selector?",
                ["getElementsByClassName", "querySelectorAll", "querySelector", "getElementsByTagName"],
                2,
                "querySelector returns the first match for any CSS selector. querySelectorAll returns all matches as a NodeList, and the getElementsBy* methods return live HTMLCollections.",
            ),
            _quiz(
                "By default, addEventListener handlers run during which phase?",
                ["The capturing phase", "The bubbling phase", "Only on the target element", "Both phases simultaneously"],
                1,
                "The default third argument (false) registers the handler for the bubble phase. Pass true to switch to capturing.",
            ),
            _quiz(
                "What does event.stopPropagation() do?",
                ["Stops the browser's default action", "Prevents other listeners on the same element", "Stops the event from traveling further through the tree", "Removes the element from the DOM"],
                2,
                "stopPropagation cancels the event's journey up (bubbling) or down (capturing) the tree. To also stop the default action, call preventDefault() separately.",
            ),
        ],
        "exercise": _exercise(
            "Count clicks on any button",
            "Use event delegation on #toolbar to log 'Clicked:' plus the clicked button's text. It must work for buttons added after the listener is attached.",
            "const toolbar = document.getElementById('toolbar');\n\n// one listener on toolbar using event.target",
            "const toolbar = document.getElementById('toolbar');\n\ntoolbar.addEventListener('click', (event) => {\n  const button = event.target.closest('button');\n  if (button) {\n    console.log('Clicked:', button.textContent);\n  }\n});",
            "closest('button') walks up from the click target to find the nearest ancestor button.",
        ),
        "curriculum": ["javascript"],
    },
    {
        "id": "js-this-prototypes",
        "title": "this Binding and Prototypes Explained",
        "category": "javascript",
        "summary": "this is the single most-confused keyword in JavaScript, and prototypes are the engine behind classes and inheritance. Learn the four binding rules, call/apply/bind, and how the prototype chain actually looks up methods.",
        "level": "advanced",
        "read_time_min": 16,
        "related_topics": ["js-functions", "js-arrays-objects"],
        "sections": [
            _section(
                "The four this-binding rules",
                "In a regular function, this is decided at call time by HOW the function is invoked — not where it is written. Rule 1, default binding: a plain call gives you the global object (or undefined in strict mode). Rule 2, implicit binding: obj.method() makes this obj. Rule 3, explicit binding: call/apply/bind pick this for you. Rule 4, new binding: the new keyword makes this a fresh object. Arrow functions obey none of these — they capture this lexically from the enclosing scope.",
                "// 1. Default binding — plain call (undefined in strict mode)\nfunction standalone() {\n  return this;\n}\n\n// 2. Implicit binding — called on an object\nconst user = {\n  name: 'Ada',\n  whoAmI() { return this.name; },\n};\nuser.whoAmI(); // 'Ada'\n\n// 3. Explicit binding — call / apply / bind choose this\n// 4. new binding — this is the freshly created instance\nfunction Person(name) {\n  this.name = name;\n}\nconst ada = new Person('Ada');",
            ),
            _section(
                "call, apply, and bind",
                "These three control this explicitly. call(fn, arg1, arg2) invokes immediately with arguments one by one; apply(thisArg, [args]) invokes immediately with an array; bind(thisArg, ...args) returns a NEW function with this fixed, callable later. bind is what event handlers and setTimeout callbacks use when they need a specific this.",
                "function describe(role) {\n  return `${this.name} works as a ${role}`;\n}\n\nconst user = { name: 'Ada' };\n\ndescribe.call(user, 'engineer');     // args one by one\ndescribe.apply(user, ['engineer']);  // args as an array\nconst bound = describe.bind(user, 'engineer');\nbound();                             // call later, this fixed forever",
                "Pro tip: bind returns a NEW function on every call — describe.bind(user) called twice gives two different functions. Save the bound version once and reuse it, or removeEventListener will never find the original.",
            ),
            _section(
                "Prototypes: shared behavior",
                "Every object has a hidden link to a prototype object. A property lookup that fails on the object itself walks up the chain: object → its prototype → Object.prototype → null. Object.create(proto) builds a new object linked to proto, which is how you inherit methods without copying them. hasOwnProperty tells you whether a property is the object's own or inherited.",
                "const person = {\n  greet() {\n    return `Hi, I am ${this.name}`;\n  },\n};\n\nconst ada = Object.create(person);\nada.name = 'Ada';\n\nconsole.log(ada.greet());                   // Hi, I am Ada\nconsole.log(ada.hasOwnProperty('greet'));   // false — inherited\n\n// Lookup walks the chain: ada → person → Object.prototype → null",
            ),
            _section(
                "class syntax is sugar over prototypes",
                "class does not add a new object model — it is cleaner syntax over the same prototype mechanism. constructor sets up this, methods land on the prototype (shared, not copied per instance), and extends wires up the chain with super() calling the parent constructor. Understanding the prototype beneath the class is what makes advanced JS (mixin patterns, polyfills, monkey-patching) comprehensible.",
                "class Person {\n  constructor(name) {\n    this.name = name;\n  }\n  greet() {\n    return `Hi, I am ${this.name}`;\n  }\n}\n\nclass Developer extends Person {\n  constructor(name, language) {\n    super(name);\n    this.language = language;\n  }\n  code() {\n    return `${this.greet()} and I write ${this.language}`;\n  }\n}\n\nconst ada = new Developer('Ada', 'Python');\nada.code(); // Hi, I am Ada and I write Python",
            ),
        ],
        "key_takeaways": [
            "this depends on the call site: default, implicit, explicit, or new binding",
            "call passes args individually, apply passes an array, bind returns a reusable function",
            "Arrow functions ignore all four rules and use the enclosing this",
            "Objects inherit through the prototype chain; class is sugar over the same mechanism",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "In a regular function invoked as obj.method(), what is this?",
                ["The global object", "obj — the object it was called on", "undefined, always", "A brand new instance"],
                1,
                "Implicit binding: the object on the left of the dot becomes this. That is why const f = obj.method; f() loses the binding.",
            ),
            _quiz(
                "Which method invokes the function immediately, passing arguments as an array?",
                ["call", "apply", "bind", "new"],
                1,
                "apply(thisArg, [args]) takes its arguments as an array. call passes them one by one, and bind returns a new function instead of invoking.",
            ),
            _quiz(
                "What does Object.create(person) do?",
                ["Deep-clones person", "Creates a new object whose prototype is person", "Freezes person so it cannot change", "Returns person's constructor function"],
                1,
                "Object.create(proto) makes a fresh object linked to proto. Property lookups that miss on the new object fall through to person — the start of a prototype chain.",
            ),
        ],
        "exercise": _exercise(
            "Borrow a method with call",
            "Log person.greet() invoked with other as its context so the output is 'Hi, I am Grace'.",
            "const person = {\n  name: 'Ada',\n  greet() {\n    return `Hi, I am ${this.name}`;\n  },\n};\n\nconst other = { name: 'Grace' };\n\n// use person.greet with other as this",
            "const person = {\n  name: 'Ada',\n  greet() {\n    return `Hi, I am ${this.name}`;\n  },\n};\n\nconst other = { name: 'Grace' };\n\nconsole.log(person.greet.call(other)); // Hi, I am Grace",
            "call runs the function immediately and takes the this value as its first argument.",
        ),
        "curriculum": ["javascript"],
    },
    {
        "id": "js-es6-modules",
        "title": "ES6 Modules: import and export Done Right",
        "category": "javascript",
        "summary": "import and export split code into files that name their dependencies and share nothing accidentally. Learn named vs default exports, module scope, and dynamic import for code splitting.",
        "level": "intermediate",
        "read_time_min": 12,
        "related_topics": ["js-variables-types", "js-functions"],
        "sections": [
            _section(
                "Named exports and imports",
                "export const and export function mark bindings that importers pull in by their exact name, inside braces. Named exports are the default choice because the names make every dependency visible in one line — no guessing where a symbol came from.",
                "// math.js\nexport const PI = 3.14159;\n\nexport function double(n) {\n  return n * 2;\n}\n\n// main.js\nimport { PI, double } from './math.js';\n\nconsole.log(double(PI)); // 6.28318",
            ),
            _section(
                "Default exports and aliases",
                "export default marks a module's single primary export; importers name it whatever they like. A module can have one default export and any number of named exports. Use as to rename named imports, or import * as math to bring in the whole namespace object.",
                "// render.js\nexport default function render(app) {\n  app.innerHTML = '<h1>Hello</h1>';\n}\n\n// main.js\nimport render from './render.js';\n\n// rename a named import\nimport { double as twice } from './math.js';\n\n// namespace import — one object with every named export\nimport * as math from './math.js';\nmath.double(3);",
            ),
            _section(
                "Module scope, strict mode, and one instance",
                "Each module has its own top-level scope — no accidental globals, and every module runs in strict mode by default (no silent failures, no this === window). A module is evaluated exactly once per app, then cached: every file that imports it shares that single instance, so a counter or config object in one module is seen by all importers.",
                "// counter.js\nexport let count = 0;\nexport function bump() {\n  count += 1;\n}\n\n// a.js and b.js both import { count, bump } — ONE shared instance\nimport { count, bump } from './counter.js';\n\nbump(); // every importer sees count === 1",
            ),
            _section(
                "Dynamic import() for code splitting",
                "Static imports are hoisted and always run. import() is a runtime call that returns a promise, so the code loads only when the statement executes — perfect for feature flags, heavy libraries, and route-level code splitting. Modules also allow top-level await, so you can await an import directly.",
                "// loads only when this line runs — not at page load\nconst { default: chart } = await import('./chart.js');\nchart.draw(data);\n\n// top-level await is legal inside a module\nconst config = await fetch('/config.json').then(r => r.json());",
                "Pro tip: static imports must be top-level and unconditional — you cannot put them inside an if. When you need conditional or lazy loading, that is exactly what dynamic import() is for.",
            ),
        ],
        "key_takeaways": [
            "Named exports pair with named imports by exact name; default exports need no name",
            "Every module is its own strict-mode scope — no accidental globals",
            "A module is evaluated once and cached; every importer shares that instance",
            "Use dynamic import() to split bundles and load features on demand",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which syntax imports a named export?",
                ["import math from './math.js'", "import { double } from './math.js'", "require('./math.js')", "import * as double from './math.js'"],
                1,
                "Named exports use braces: import { double } from './math.js'. No braces is the default-import syntax, and import * as gives the whole namespace object.",
            ),
            _quiz(
                "How does a module's top-level code run?",
                ["In the global scope, sharing variables with other modules", "In its own scope in strict mode", "Only after every importer finishes loading", "Copied separately for each file that imports it"],
                1,
                "Modules have private top-level scope and always run in strict mode, which is why they never pollute globals the way <script> tags can.",
            ),
            _quiz(
                "When does a dynamic import() evaluate its module?",
                ["At parse time, before anything runs", "Whenever any static import references the module", "At runtime, when the statement executes", "When the browser unloads the page"],
                2,
                "import() is a runtime function call returning a promise; the module is fetched and evaluated only when that line runs — which is what enables code splitting.",
            ),
        ],
        "exercise": _exercise(
            "Create and use a module",
            "Write a named export add in math.js, then import it in main.js and log add(2, 3).",
            "// math.js\nexport function add(a, b) {\n  return a + b;\n}\n\n// main.js — import add and log the result",
            "// math.js\nexport function add(a, b) {\n  return a + b;\n}\n\n// main.js\nimport { add } from './math.js';\n\nconsole.log(add(2, 3)); // 5",
            "Named imports use braces: import { add } from './math.js';",
        ),
        "curriculum": ["javascript"],
    },
    {
        "id": "js-fetch-apis",
        "title": "Fetch and Working with APIs",
        "category": "javascript",
        "summary": "fetch is the modern way to talk to servers: a promise-based API that reads and writes JSON, sends headers, and — with AbortController — cancels requests cleanly. This is how every real app talks to a backend.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["js-async", "js-error-handling"],
        "sections": [
            _section(
                "The fetch() contract",
                "fetch(url, options) returns a Promise that resolves to a Response object — not the data. The response wraps status, headers, and a body you read with a method like res.json() or res.text(). The promise resolves as soon as headers arrive, so for large bodies you await the body read separately.",
                "const response = await fetch('https://api.github.com/users/octocat');\nconsole.log(response.status);        // 200\nconsole.log(response.ok);            // true\nconsole.log(response.headers.get('content-type'));\n\nconst data = await response.json(); // read the body",
            ),
            _section(
                "Reading the body and checking errors",
                "The single most common fetch bug: fetch only rejects on NETWORK failure (offline, DNS, refused connection). HTTP errors like 404 and 500 still resolve with a normal Response. Always check response.ok before trusting the body, and throw your own error with the status in the message so the failure is debuggable.",
                "const response = await fetch('/api/user/42');\n\n// fetch resolves on 404/500 — you must check\nif (!response.ok) {\n  throw new Error(`Request failed with ${response.status}`);\n}\n\nconst user = await response.json();\nconsole.log(user.name);",
            ),
            _section(
                "POST, headers, and JSON bodies",
                "To send data, pass a second options argument: method, headers, and body. For JSON, set Content-Type to application/json and serialize the payload with JSON.stringify. GET is the default — add method only for POST, PUT, PATCH, DELETE.",
                "const response = await fetch('/api/users', {\n  method: 'POST',\n  headers: {\n    'Content-Type': 'application/json',\n  },\n  body: JSON.stringify({ name: 'Ada', role: 'engineer' }),\n});\n\nconst created = await response.json();",
            ),
            _section(
                "AbortController: timeouts and cancellation",
                "An in-flight fetch cannot be cancelled from the outside — but you can tie it to an AbortController. Pass controller.signal in the request options; calling controller.abort() rejects the pending fetch with an AbortError. That is the idiomatic way to implement request timeouts and to cancel stale requests when a component unmounts.",
                "const controller = new AbortController();\nconst timeout = setTimeout(() => controller.abort(), 5000);\n\ntry {\n  const response = await fetch(url, { signal: controller.signal });\n  const data = await response.json();\n} catch (err) {\n  if (err.name === 'AbortError') {\n    console.log('Request timed out — cancelled');\n  } else {\n    console.error('Network error:', err);\n  }\n} finally {\n  clearTimeout(timeout);\n}",
                "Pro tip: a fetch only rejects on network failure or abort — 404s and 500s still resolve. Check response.ok before you parse, and let AbortController handle timeouts instead of a setTimeout race.",
            ),
        ],
        "key_takeaways": [
            "fetch returns a Promise<Response>; read the body with res.json() after headers arrive",
            "response.ok tells you about HTTP errors — fetch itself only rejects on network failure",
            "Send data with method, headers, and JSON.stringify in the body",
            "AbortController cancels a fetch mid-flight for timeouts and unmounts",
        ],
        "tag": "projects",
        "quiz": [
            _quiz(
                "What does res.json() return?",
                ["A plain string", "A Promise that resolves to the parsed JSON", "A JavaScript object, synchronously", "A DOM element"],
                1,
                "Body methods like res.json() and res.text() are async — they return promises. You need await or .then to get the actual data.",
            ),
            _quiz(
                "Which check should you perform after a fetch resolves?",
                ["response.json()", "response.error", "response.ok", "response.valid"],
                2,
                "response.ok is true only for 200-299 statuses. fetch itself only rejects on network failures, so without this check a 404 response would be treated as success.",
            ),
            _quiz(
                "How do you cancel an in-flight fetch?",
                ["Call fetch.abort()", "Call controller.abort() after passing controller.signal to the request", "Call clearTimeout on the promise", "In-flight fetches cannot be cancelled"],
                1,
                "An AbortController tied to the request via the signal option is the supported way. controller.abort() rejects the fetch with an AbortError.",
            ),
        ],
        "exercise": _exercise(
            "Fetch with error handling",
            "Complete loadUser so it fetches '/api/user/42', checks res.ok, parses the JSON, and logs user.name. Catch and log any failure.",
            "async function loadUser(id) {\n  // fetch, check res.ok, parse json, log user.name\n}\n\nloadUser(42);",
            "async function loadUser(id) {\n  try {\n    const res = await fetch(`/api/user/${id}`);\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n    const user = await res.json();\n    console.log(user.name);\n  } catch (err) {\n    console.error('Failed to load user:', err);\n  }\n}\n\nloadUser(42);",
            "fetch never throws on a 404 — check res.ok yourself before parsing.",
        ),
        "curriculum": ["javascript"],
    },
    {
        "id": "js-error-handling",
        "title": "Error Handling and Debugging in JavaScript",
        "category": "javascript",
        "summary": "throw, try/catch/finally, and custom error classes turn crashes into recoverable, explainable failures. Then debug with console methods and breakpoints instead of logging everything.",
        "level": "beginner",
        "read_time_min": 11,
        "related_topics": ["js-functions", "js-async"],
        "sections": [
            _section(
                "throw and the Error object",
                "throw aborts the current execution and hands an error to the nearest catch. The Error object carries name (the type) and message (the detail). Use the built-in constructors when they fit — SyntaxError, TypeError, RangeError, ReferenceError — and reserve throw for genuine failure, not for control flow.",
                "throw new Error('Something went wrong');\n\nconst err = new Error('Missing name');\nconsole.log(err.name);    // 'Error'\nconsole.log(err.message); // 'Missing name'",
            ),
            _section(
                "try / catch / finally",
                "Wrap risky code in try. If anything inside throws, control jumps to catch with the error object. finally always runs — after a successful try or after a catch — which makes it the right home for cleanup like clearing timers or closing connections. In async functions the same pattern catches rejected promises when combined with await.",
                "function parseJson(raw) {\n  try {\n    return JSON.parse(raw);\n  } catch (err) {\n    console.error('Parse failed:', err.message);\n    return null;\n  } finally {\n    console.log('always runs');\n  }\n}",
            ),
            _section(
                "Custom error classes",
                "Extend Error to give failures a name, extra context, and a place to live. A ValidationError carrying the offending field makes a 100-line error handler redundant — callers can inspect err.field directly. Set this.name explicitly; name is not auto-inherited from the class in every environment.",
                "class ValidationError extends Error {\n  constructor(message, field) {\n    super(message);\n    this.name = 'ValidationError';\n    this.field = field;\n  }\n}\n\nfunction register(user) {\n  if (!user.email) {\n    throw new ValidationError('Email is required', 'email');\n  }\n}",
                "Pro tip: never swallow what you cannot handle. A catch that logs and returns silently hides bugs — recover, rethrow, or at least log the error with context so it survives the session.",
            ),
            _section(
                "Debugging without console.log spew",
                "Console has better tools: console.table for arrays and objects, console.time/timeEnd for measuring a block, console.assert for conditions that should hold, and the debugger statement, which pauses execution at that line when devtools are open. Browser devtools breakpoints — set by clicking the line-number gutter — beat console.log because they pause and inspect instead of printing.",
                "console.table(users);        // readable arrays/objects\nconsole.time('pipeline');    // start a timer\npipeline();\nconsole.timeEnd('pipeline'); // prints elapsed ms\n\n// pauses if devtools are open — inspect state right here\ndebugger;",
            ),
        ],
        "key_takeaways": [
            "throw new Error(message) creates an error with name and message",
            "try/catch/finally always runs finally — the home for cleanup",
            "Extend Error to build domain-specific errors with context",
            "Breakpoints and console methods beat piles of console.log",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which of these is NOT a built-in Error constructor?",
                ["SyntaxError", "TypeError", "RangeError", "FormatError"],
                3,
                "JavaScript ships SyntaxError, TypeError, RangeError, ReferenceError and a few more — but there is no FormatError. Building your own subclass is the way to get one.",
            ),
            _quiz(
                "After an exception is thrown, what runs in a try/catch/finally?",
                ["Nothing — execution stops forever", "Only the catch block", "The catch block, then the finally block", "Only the finally block"],
                2,
                "The catch block runs and receives the error, then finally always runs — even when the catch rethrows.",
            ),
            _quiz(
                "What is the most effective way to inspect state at one specific line?",
                ["Add console.log around every line", "Set a breakpoint (or use the debugger statement) in devtools", "Throw exceptions in production code", "Use alert() to pause the page"],
                1,
                "A breakpoint pauses execution exactly at that line, so you can inspect variables and the call stack in devtools instead of guessing from printed values.",
            ),
        ],
        "exercise": _exercise(
            "Guard against division by zero",
            "Make divide throw a clear error when b is 0, then return a / b otherwise.",
            "function divide(a, b) {\n  // throw a clear error when b is 0\n}\n\nconsole.log(divide(10, 2)); // 5\nconsole.log(divide(10, 0)); // throws",
            "function divide(a, b) {\n  if (b === 0) {\n    throw new Error('Cannot divide by zero');\n  }\n  return a / b;\n}\n\nconsole.log(divide(10, 2)); // 5\nconsole.log(divide(10, 0)); // throws",
            "Check the invalid input first, throw, and only then compute.",
        ),
        "curriculum": ["javascript"],
    },
]


INTERACTIVES = {
    "js-variables-types": {
        "quiz": [
            _quiz(
                "Which keyword creates a variable whose binding can never be reassigned?",
                ["let", "const", "var", "static"],
                1,
                "const forbids reassignment of the binding. let and var both allow reassignment, and static is not a variable keyword.",
            ),
            _quiz(
                "What does typeof null evaluate to?",
                ["'null'", "'undefined'", "'object'", "'number'"],
                2,
                "A historical bug: null's type tag was set to the object tag in the first ECMAScript spec, and typeof has preserved it ever since for backwards compatibility.",
            ),
            _quiz(
                "Which comparison evaluates to true?",
                ["5 === '5'", "5 == '5'", "'5' === 5", "5 === 5.0"],
                3,
                "5 and 5.0 are the same number, so strict equality holds. === never coerces, which rules out every string-versus-number option.",
            ),
        ],
        "exercise": _exercise(
            "const by default",
            "Rewrite the code so every value that is never reassigned uses const.",
            "let name = 'Ada';\nlet age = 36;\nlet greeting = 'Hello ' + name;",
            "const name = 'Ada';\nconst age = 36;\nconst greeting = `Hello ${name}`;",
            "Only change let to const — none of these bindings are reassigned.",
        ),
    },
    "js-functions": {
        "quiz": [
            _quiz(
                "What is the key thing arrow functions do NOT do that regular functions do?",
                ["Get hoisted", "Bind their own this", "Accept arguments", "Return a value"],
                1,
                "Arrow functions capture this from the enclosing scope instead of binding their own. That is their defining difference and why they are ideal for callbacks.",
            ),
            _quiz(
                "Given function createCounter() { let count = 0; return () => ++count; }, calling counter() then counter() returns:",
                ["1 then 1", "1 then 2", "0 then 1", "undefined"],
                1,
                "The inner arrow closes over count, so each call mutates the same surviving binding — the closure is what keeps count alive after createCounter returns.",
            ),
            _quiz(
                "Inside a regular function called as obj.method(), this refers to:",
                ["The global object", "obj — the object it was called on", "undefined, always", "A brand new instance"],
                1,
                "Implicit binding: the object on the left of the dot becomes this. Detach the method and call it bare, and this is lost.",
            ),
        ],
        "exercise": _exercise(
            "A closure counter",
            "Finish createCounter so it returns a function that increments count and returns the new value each time.",
            "function createCounter() {\n  let count = 0;\n  // return a function that increments and returns count\n}",
            "function createCounter() {\n  let count = 0;\n  return () => ++count;\n}",
            "The returned arrow closes over count, so the variable survives between calls.",
        ),
    },
    "js-arrays-objects": {
        "quiz": [
            _quiz(
                "Which array method collapses an array into a single value?",
                ["map", "filter", "reduce", "find"],
                2,
                "reduce folds every element through an accumulator to produce one value. map transforms, filter keeps matches, and find returns the first match.",
            ),
            _quiz(
                "Which of these does NOT mutate the original array?",
                ["push", "splice", "sort", "slice"],
                3,
                "slice returns a copy of a portion of the array. push, splice, and sort all modify the array in place.",
            ),
            _quiz(
                "const a = { n: 1 }; const b = { n: 1 }; console.log(a === b) logs:",
                ["true", "false", "TypeError", "null"],
                1,
                "Objects compare by reference, not by content. a and b point to two different objects, so strict equality is false even though their fields match.",
            ),
        ],
        "exercise": _exercise(
            "A data pipeline",
            "Filter prices to the values at or below 30, then use reduce to total the filtered values, and log the result.",
            "const prices = [5, 15, 30, 45];\n\n// filter → total the filtered values with reduce → log",
            "const prices = [5, 15, 30, 45];\n\nconst total = prices\n  .filter(p => p <= 30)\n  .reduce((sum, p) => sum + p, 0);\n\nconsole.log(total); // 50",
            "Chain filter before reduce, and give reduce an initial value of 0.",
        ),
    },
    "js-async": {
        "quiz": [
            _quiz(
                "Given:\nsetTimeout(() => console.log('a'), 0);\nPromise.resolve().then(() => console.log('b'));\nconsole.log('c');\n\nWhat prints first and what prints last?",
                ["b first, a last", "c first, a last", "a first, c last", "b first, c last"],
                1,
                "The synchronous 'c' prints immediately, then the microtask 'b' drains before the setTimeout macrotask 'a' — microtasks always win the race.",
            ),
            _quiz(
                "Which of these fetches run concurrently?",
                ["for (const url of urls) await fetch(url)", "Promise.all(urls.map(fetch))", "await fetch(urls[0]); fetch(urls[1])", "await fetch(url)"],
                1,
                "Promise.all starts every fetch immediately, so they overlap. Awaiting inside a loop runs the requests one after another, serializing them.",
            ),
            _quiz(
                "Inside an async function, await:",
                ["Blocks the entire thread", "Pauses only the async function and yields to the event loop", "Starts a new thread", "Is required before every statement"],
                1,
                "await suspends just that function; the event loop keeps running everything else until the promise settles. That is why the page stays responsive.",
            ),
        ],
        "exercise": _exercise(
            "async/await loader",
            "Rewrite loadUser as an async function that awaits fetch, checks res.ok, and returns the parsed JSON.",
            "function loadUser(id) {\n  return fetch(`/api/user/${id}`).then(r => r.json());\n}",
            "async function loadUser(id) {\n  const res = await fetch(`/api/user/${id}`);\n  if (!res.ok) throw new Error(`HTTP ${res.status}`);\n  return res.json();\n}",
            "Mark the function async, then use await before fetch and res.json().",
        ),
    },
}
