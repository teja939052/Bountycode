"""Study Library content: TypeScript + React expansion.

Plain dict schema (this module is imported BY study_materials, so it must NOT
import from study_materials — the helpers are copied here to avoid a cycle).
"""


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
    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ TypeScript â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    {
        "id": "ts-type-narrowing",
        "title": "Type Narrowing: typeof, instanceof, and Discriminated Unions",
        "category": "typescript",
        "summary": "Inside a conditional, TypeScript shrinks a union type to one of its members. Learn typeof, instanceof, 'in' checks, and discriminated unions — the pattern that makes switch statements type-safe.",
        "level": "intermediate", "read_time_min": 14,
        "related_topics": ["ts-interfaces-generics", "ts-utility-types"],
        "sections": [
            _section(
                "Why narrowing exists",
                "A union type says a value could be one of several shapes. Narrowing is TypeScript's ability to figure out which one you're actually holding based on a check in your code. Once narrowed, you get full autocomplete and type safety for that branch — the compiler follows your logic.",
                "function format(value: string | number): string {\n  if (typeof value === 'string') {\n    return value.toUpperCase();   // value: string here\n  }\n  return value.toFixed(2);        // value: number here\n}",
            ),
            _section(
                "typeof, instanceof, and the in operator",
                "typeof works for primitives (string, number, boolean, symbol, undefined, object, function). instanceof narrows class instances. The in operator checks for a property name and narrows object unions that differ by their fields.",
                "class Dog { bark() {} }\nclass Cat { meow() {} }\n\nfunction speak(pet: Dog | Cat) {\n  if (pet instanceof Dog) return pet.bark();\n  return pet.meow();\n}\n\ninterface Circle { kind: 'circle'; radius: number }\ninterface Square { kind: 'square'; side: number }\nfunction area(s: Circle | Square) {\n  if ('radius' in s) return Math.PI * s.radius ** 2;\n  return s.side ** 2;\n}",
            ),
            _section(
                "Discriminated unions: the switch pattern",
                "Give every member of a union a common literal field (the discriminator), then switch on it. TypeScript narrows each case to exactly one member, so a missing case becomes a compile error instead of a runtime bug.",
                "type Shape =\n  | { kind: 'circle'; radius: number }\n  | { kind: 'rect'; width: number; height: number };\n\nfunction area(s: Shape): number {\n  switch (s.kind) {\n    case 'circle': return Math.PI * s.radius ** 2;\n    case 'rect':   return s.width * s.height;\n  }\n}",
                "Add a new member to the union and the compiler forces you to handle it — that is the payoff of discriminated unions.",
            ),
            _section(
                "Exhaustiveness with never",
                "The never type means 'this should never happen'. An exhaustive check assigns the remaining value to never: if a future union member slips through unhandled, the variable is no longer never and TypeScript errors at compile time.",
                "function assertNever(x: never): never {\n  throw new Error('Unexpected value: ' + x);\n}\n\nfunction area(s: Shape): number {\n  switch (s.kind) {\n    case 'circle': return Math.PI * s.radius ** 2;\n    case 'rect':   return s.width * s.height;\n    default:       return assertNever(s);\n  }\n}",
            ),
        ],
        "key_takeaways": [
            "Narrowing shrinks a union to the member your code proves",
            "typeof for primitives, instanceof for classes, in for object fields",
            "Discriminated unions + switch = exhaustive, compile-checked handling",
            "never catches unhandled union members in the default branch",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("What does the compiler know inside an if (typeof x === 'number') branch when x: string | number?",
                  ["x is string", "x is number", "x is string | number", "x is any"],
                  1, "After the typeof check for 'number', the string arm is excluded, so x narrows to number."),
            _quiz("Which check narrows a Dog | Cat union based on class instances?",
                  ["typeof pet", "in pet", "instanceof", "Array.isArray(pet)"],
                  2, "instanceof tests the prototype chain at runtime, letting TypeScript narrow class unions."),
            _quiz("Why is the 'kind' field in a discriminated union a literal type?",
                  ["So it is unique", "So the switch can narrow each case to one member", "So it can be any string", "It must be a number"],
                  1, "A literal type like 'circle' is the discriminator — the switch on it lets TS narrow each case exactly."),
        ],
        "exercise": _exercise(
            "Narrow a user object",
            "Write a function getRole(user: Admin | Member) that returns 'admin' or 'member'. Admin has an 'adminSince' Date; Member has a 'joinDate'. Use the 'in' operator to narrow.",
            "interface Admin { adminSince: Date }\ninterface Member { joinDate: Date }\n\ntype User = Admin | Member;\n\nfunction getRole(user: User): string {\n  // your narrowing here\n}",
            "function getRole(user: User): string {\n  if ('adminSince' in user) return 'admin';\n  return 'member';\n}",
            "The 'in' operator narrows object unions by presence of a property.",
        ),
        "curriculum": ["typescript"],
    },
    {
        "id": "ts-utility-types",
        "title": "TypeScript Utility Types: Partial, Pick, Omit, Record",
        "category": "typescript",
        "summary": "Utility types are ready-made type transformations. Partial makes fields optional, Pick and Omit select or drop keys, Record builds maps, and ReturnType reads function signatures.",
        "level": "intermediate", "read_time_min": 12,
        "related_topics": ["ts-interfaces-generics", "ts-type-narrowing"],
        "sections": [
            _section(
                "Partial and Required",
                "Partial<T> turns every property optional — perfect for update functions where a caller may change just one field. Required<T> does the opposite. Never hand-write a second 'Update' interface when Partial<T> gives it to you.",
                "interface User {\n  name: string;\n  email: string;\n  age: number;\n}\n\nfunction updateUser(id: string, patch: Partial<User>) {\n  // patch.age is optional; only included fields change\n}",
            ),
            _section(
                "Pick and Omit",
                "Pick<T, K> keeps only the listed keys; Omit<T, K> removes them. Pick a public subset for API responses, Omit a password field before sending a user to the client.",
                "type PublicUser = Pick<User, 'name' | 'email'>;\n\nfunction safeUser(u: User): Omit<User, 'secret'> {\n  const { secret, ...rest } = u;\n  return rest;\n}",
            ),
            _section(
                "Record and keyof",
                "Record<K, V> builds an object type mapping keys K to values V. Combined with keyof it enforces 'one value per known key', killing the any-object smell.",
                "type Status = 'pending' | 'active' | 'blocked';\nconst labels: Record<Status, string> = {\n  pending: 'Waiting',\n  active: 'Live',\n  blocked: 'Suspended',\n};\n// Missing a key? Compile error. Typo a key? Compile error.",
            ),
            _section(
                "Function utilities: Parameters and ReturnType",
                "Parameters<T> extracts a function's argument types; ReturnType<T> extracts its return type. Useful when you want a type that matches what a function produces without naming it twice.",
                "const createUser = (name: string, age: number) => ({ id: 1, name, age });\n\ntype NewUser = ReturnType<typeof createUser>;\n// NewUser = { id: number; name: string; age: number }\ntype CreateArgs = Parameters<typeof createUser>;\n// CreateArgs = [name: string, age: number]",
            ),
        ],
        "key_takeaways": [
            "Partial makes all fields optional; Required makes them mandatory",
            "Pick keeps keys, Omit drops keys",
            "Record<K, V> enforces one value per known key",
            "ReturnType and Parameters derive types from function signatures",
        ],
        "tag": "core",
        "quiz": [
            _quiz("Which utility type makes every field of T optional?",
                  ["Pick<T, K>", "Partial<T>", "Omit<T, K>", "Required<T>"],
                  1, "Partial<T> maps every property to optional."),
            _quiz("How do you expose a User type without the 'password' field?",
                  ["Pick<User, 'password'>", "Partial<User>", "Omit<User, 'password'>", "Record<User>"],
                  2, "Omit removes the named keys from the type."),
            _quiz("Record<'a' | 'b', number> describes what?",
                  ["An array of two numbers", "An object with exactly keys 'a' and 'b' whose values are numbers", "A number", "A tuple"],
                  1, "Record maps the union of keys to a value type, producing { a: number; b: number }."),
        ],
        "exercise": _exercise(
            "Typed status labels",
            "Define labels: Record<Status, string> where Status = 'draft' | 'published' | 'archived', with sensible label values, then write a function getLabel(s: Status): string that returns labels[s].",
            "type Status = 'draft' | 'published' | 'archived';\n\nconst labels: Record<Status, string> = {\n  // fill in\n};\n\nfunction getLabel(s: Status): string {\n  return labels[s];\n}",
            "const labels: Record<Status, string> = {\n  draft: 'Draft',\n  published: 'Published',\n  archived: 'Archived',\n};\n\nfunction getLabel(s: Status): string {\n  return labels[s];\n}",
            "Record requires every key in the union to be present.",
        ),
        "curriculum": ["typescript"],
    },
    {
        "id": "ts-generics-advanced",
        "title": "Advanced Generics: Constraints, infer, and Mapped Types",
        "category": "typescript",
        "summary": "Generics are more than type parameters — they are a small programming language for types. Constraints limit what a generic accepts, mapped types transform shapes, and infer extracts types from inside others.",
        "level": "advanced", "read_time_min": 16,
        "related_topics": ["ts-interfaces-generics", "ts-utility-types"],
        "sections": [
            _section(
                "Constraints: extends keeps generics honest",
                "A bare T accepts anything. A constrained T extends something, so inside the function you can use that something's properties without casts. This is the difference between a generic that works and a generic that type-checks.",
                "interface HasId { id: number }\n\nfunction findById<T extends HasId>(items: T[], id: number): T | undefined {\n  return items.find(item => item.id === id);\n}",
            ),
            _section(
                "keyof and mapped types",
                "Mapped types iterate over keys with [K in keyof T]. Utility types are built from them: Partial<T> is { [K in keyof T]?: T[K] }. You can map keys to new value types, filter keys, and add modifiers.",
                "type Readonly<T> = { readonly [K in keyof T]: T[K] };\n\ntype NullableValues<T> = { [K in keyof T]: T[K] | null };\n\ninterface Config { host: string; port: number }\ntype NullableConfig = NullableValues<Config>;\n// { host: string | null; port: number | null }",
            ),
            _section(
                "infer: asking the compiler a question",
                "Inside a conditional type, infer lets you capture a type from inside another type. ReturnType<T> is implemented with it: T extends (...args: any) => infer R ? R : never. It reads 'if T looks like a function, R is its return type'.",
                "type MyReturnType<T> =\n  T extends (...args: any[]) => infer R ? R : never;\n\ntype A = MyReturnType<() => string>;  // string\ntype B = MyReturnType<() => number>;  // number\n\ntype ElementType<T> =\n  T extends (infer E)[] ? E : never;\ntype C = ElementType<string[]>;       // string",
            ),
            _section(
                "A real-world chain: extracting an awaited value",
                "Promise<Awaited<T>> composes these ideas. Awaited<T> uses infer + recursion to unwrap nested promises. This is how modern libraries derive types from async functions without you naming the resolved type.",
                "type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;\n\ntype FetchResult = Awaited<Promise<Promise<string>>>;  // string\n\nasync function getUser() { return { id: 1, name: 'Ada' }; }\ntype User = Awaited<ReturnType<typeof getUser>>;\n// { id: number; name: string } — no manual annotation needed",
            ),
        ],
        "key_takeaways": [
            "extends constrains what a generic T can be",
            "Mapped types transform one object shape into another",
            "infer captures a type from inside another type",
            "Awaited<T> recursively unwraps promises to the resolved type",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("What does T extends HasId do in a generic function?",
                  ["Makes T any", "Limits T to types assignable to HasId", "Makes T required", "Adds an id to T"],
                  1, "The constraint says T must be assignable to HasId, so inside the function item.id is legal."),
            _quiz("What does the mapped type { [K in keyof T]?: T[K] } produce?",
                  ["A type identical to T", "An array of T", "A type where every key of T is optional", "A function type"],
                  2, "The ? modifier on each key makes every property optional — that is Partial<T>."),
            _quiz("In T extends Promise<infer U> ? Awaited<U> : T, what does infer U do?",
                  ["Declares a type variable", "Captures the resolved type inside Promise", "Imports a type", "Makes T a promise"],
                  1, "infer captures the type parameter of Promise so the conditional can recurse into it."),
        ],
        "exercise": _exercise(
            "Build a Pick<T, K>",
            "Write a mapped type MyPick<T, K> using a generic constraint that K extends keyof T and a mapped type that selects only keys in K. Then verify: type X = MyPick<{a: number; b: string; c: boolean}, 'a' | 'c'> should be {a: number; c: boolean}.",
            "type MyPick<T, K extends keyof T> = {\n  // your mapped type\n};\n\ntype X = MyPick<{ a: number; b: string; c: boolean }, 'a' | 'c'>;",
            "type MyPick<T, K extends keyof T> = {\n  [P in K]: T[P];\n};\n\ntype X = MyPick<{ a: number; b: string; c: boolean }, 'a' | 'c'>;\n// X = { a: number; c: boolean }",
            "Iterate [P in K] — K is already constrained to keyof T so T[P] is safe.",
        ),
        "curriculum": ["typescript"],
    },
    {
        "id": "ts-config-build",
        "title": "tsconfig.json and the Strict Mode Flags",
        "category": "typescript",
        "summary": "The compiler is only as strict as your tsconfig. Learn what each strict flag really protects you from, the module resolution rules, and how to build for production without surprises.",
        "level": "intermediate", "read_time_min": 13,
        "related_topics": ["ts-why-types", "ts-generics-advanced"],
        "sections": [
            _section(
                "The strict family, one flag at a time",
                "strict: true turns on a family of checks. strictNullChecks forbids assigning null/undefined to typed variables. noImplicitAny rejects untyped parameters. noUncheckedIndexedAccess makes every array/object index access possibly undefined. Each one converts a silent runtime bug into a compile error.",
                "// strictNullChecks off:\nlet name: string = maybeNull();  // allowed, crashes later\n\n// strictNullChecks on:\nlet name: string = maybeNull();  // error: string | null\nlet clean: string = maybeNull() ?? 'unknown';",
                "Adopt strictNullChecks first — it catches the majority of real crashes.",
            ),
            _section(
                "module, target, and moduleResolution",
                "target sets the emitted JS version; module sets the module system; moduleResolution must match how you import files. Bundlers (Vite) need module: ESNext + moduleResolution: Bundler. Node needs NodeNext. Get these wrong and imports silently break.",
                "{\n  \"compilerOptions\": {\n    \"target\": \"ES2022\",\n    \"module\": \"ESNext\",\n    \"moduleResolution\": \"Bundler\",\n    \"strict\": true,\n    \"outDir\": \"dist\",\n    \"skipLibCheck\": true\n  },\n  \"include\": [\"src\"]\n}",
            ),
            _section(
                "paths and baseUrl: cleaner imports",
                "paths lets you alias directories so imports read '@/components/Button' instead of '../../../../components/Button'. The bundler must know about the alias too — tsconfig alone does not rewrite anything at runtime.",
                "{\n  \"compilerOptions\": {\n    \"baseUrl\": \".\",\n    \"paths\": {\n      \"@/*\": [\"src/*\"]\n    }\n  }\n}",
                "Vite needs the same alias in vite.config.ts (resolve.alias) or the build breaks even though tsc is happy.",
            ),
            _section(
                "Build scripts and incremental speed",
                "Use separate tsconfigs for app and for type-checking (tsc --noEmit). Vite/esbuild transpile fast but do not type-check — so CI runs tsc --noEmit as the real gate, and the bundler handles emit.",
                "// package.json\n\"scripts\": {\n  \"typecheck\": \"tsc --noEmit\",\n  \"build\": \"vite build\",\n  \"ci\": \"npm run typecheck && npm run build\"\n}",
            ),
        ],
        "key_takeaways": [
            "strictNullChecks and noImplicitAny prevent most real crashes",
            "moduleResolution must match your runtime (Bundler vs NodeNext)",
            "paths aliases need a matching bundler config",
            "Vite transpiles without type-checking — run tsc --noEmit in CI",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("Which flag makes index access like arr[i] possibly undefined?",
                  ["noImplicitAny", "noUncheckedIndexedAccess", "allowJs", "declaration"],
                  1, "noUncheckedIndexedAccess adds undefined to every index access result."),
            _quiz("Which moduleResolution should a Vite/bundler project use?",
                  ["Node10", "NodeNext", "Bundler", "Classic"],
                  2, "Bundler resolution matches how Vite resolves bare imports and extensionless files."),
            _quiz("Why does `npm run build` with Vite not catch type errors?",
                  ["Vite has no types", "Vite transpiles with esbuild and skips full type-checking", "TypeScript is unused", "tsc is broken"],
                  1, "esbuild strips types for speed; the type-check must run separately via tsc --noEmit."),
        ],
        "exercise": _exercise(
            "Fix the config",
            "The following config allows null crashes and untyped params. Rewrite it so strictNullChecks, noImplicitAny, and strict are all on, target is ES2022, and module is ESNext.",
            "{\n  \"compilerOptions\": {\n    \"target\": \"ES5\",\n    \"strict\": false\n  }\n}",
            "{\n  \"compilerOptions\": {\n    \"target\": \"ES2022\",\n    \"module\": \"ESNext\",\n    \"moduleResolution\": \"Bundler\",\n    \"strict\": true,\n    \"noImplicitAny\": true,\n    \"skipLibCheck\": true\n  }\n}",
            "strict: true already enables noImplicitAny and strictNullChecks.",
        ),
        "curriculum": ["typescript"],
    },
    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ React â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    {
        "id": "react-forms",
        "title": "React Forms: Controlled Inputs and Validation",
        "category": "react",
        "summary": "React forms are state, not DOM. Controlled inputs store every keystroke in state; uncontrolled inputs read from the DOM on demand. Validation can run live, on blur, or on submit — and errors belong in state.",
        "level": "intermediate", "read_time_min": 14,
        "related_topics": ["react-hooks", "react-components"],
        "sections": [
            _section(
                "Controlled vs uncontrolled",
                "A controlled input's value comes from state and its onChange writes back — React owns the text. An uncontrolled input uses ref to read the DOM when needed (file inputs must be uncontrolled). Controlled is the default choice: it enables validation and derived UI.",
                "function NameForm() {\n  const [name, setName] = useState('');\n  return (\n    <input\n      value={name}\n      onChange={e => setName(e.target.value)}\n      placeholder=\"Full name\"\n    />\n  );\n}",
            ),
            _section(
                "One state object for the whole form",
                "Group fields into a single state object and update by key. handleChange becomes one reusable function, and the submit handler reads the whole object at once.",
                "const [form, setForm] = useState({ email: '', password: '' });\n\nconst handleChange = (e) =>\n  setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));\n\n<input name=\"email\" value={form.email} onChange={handleChange} />",
                "Use a name attribute matching each state key — one handler for every field.",
            ),
            _section(
                "Validating and showing errors",
                "Validate on change (instant feedback), on blur (calmer), and always on submit. Store errors in state and disable submit until valid. Keep validation as a pure function so you can test it without rendering.",
                "function validate(email, password) {\n  const errors = {};\n  if (!email.includes('@')) errors.email = 'Enter a valid email';\n  if (password.length < 8) errors.password = 'Min 8 characters';\n  return errors;\n}\n\nconst [errors, setErrors] = useState({});\n\nfunction handleSubmit(e) {\n  e.preventDefault();\n  const errs = validate(form.email, form.password);\n  setErrors(errs);\n  if (Object.keys(errs).length === 0) submit(form);\n}",
            ),
            _section(
                "Common pitfalls",
                "Don't default an uncontrolled input after it mounts (React won't reset it). Use defaultValue only for initial values. For selects, set value on the select and option values accordingly. Number inputs: e.target.value is a string — parse it.",
                "<select value={form.country} onChange={handleChange} name=\"country\">\n  <option value=\"\">Select…</option>\n  <option value=\"in\">India</option>\n  <option value=\"us\">USA</option>\n</select>\n\n<input\n  type=\"number\"\n  name=\"age\"\n  value={form.age}\n  onChange={e =>\n    handleChange(e, e.target.value === '' ? '' : Number(e.target.value))\n  }\n/>",
            ),
        ],
        "key_takeaways": [
            "Controlled inputs: value from state, onChange writes state",
            "Keep one form state object updated by field name",
            "Validate on change/blur/submit; errors live in state",
            "Parse number inputs and set select values explicitly",
        ],
        "tag": "core",
        "quiz": [
            _quiz("What makes an input 'controlled'?",
                  ["It has a ref", "Its value comes from state and onChange updates it", "It is inside a form tag", "It has a name attribute"],
                  1, "React controls the value, so every change flows through state."),
            _quiz("When must an input be uncontrolled?",
                  ["Never", "For file inputs", "For text inputs", "For selects"],
                  1, "File inputs need direct DOM access; React cannot set their value."),
            _quiz("Where do validation errors belong?",
                  ["In the DOM", "In component state", "In the event object", "In local storage"],
                  1, "Errors render from state so the UI reacts to them like any data."),
        ],
        "exercise": _exercise(
            "Validated email form",
            "Build a controlled email input that disables the submit button unless the value contains '@'. Store value in state, validate inline, and pass disabled={!isValid}.",
            "function EmailForm() {\n  const [email, setEmail] = useState('');\n  const isValid = email.includes('@');\n  return (\n    <form onSubmit={e => e.preventDefault()}>\n      <input\n        type=\"email\"\n        value={email}\n        onChange={e => setEmail(e.target.value)}\n      />\n      <button type=\"submit\" /* disabled when invalid */>\n        Sign up\n      </button>\n    </form>\n  );\n}",
            "function EmailForm() {\n  const [email, setEmail] = useState('');\n  const isValid = email.includes('@');\n  return (\n    <form onSubmit={e => e.preventDefault()}>\n      <input\n        type=\"email\"\n        value={email}\n        onChange={e => setEmail(e.target.value)}\n      />\n      <button type=\"submit\" disabled={!isValid}>\n        Sign up\n      </button>\n    </form>\n  );\n}",
            "Derive isValid from state instead of storing it separately.",
        ),
        "curriculum": ["react"],
    },
    {
        "id": "react-context",
        "title": "React Context and useReducer: State Without Prop Drilling",
        "category": "react",
        "summary": "When many components need the same data, prop drilling becomes a mess. Context provides it to the whole subtree; useReducer centralizes updates. Together they replace hand-rolled global state in many apps.",
        "level": "intermediate", "read_time_min": 15,
        "related_topics": ["react-hooks", "react-performance"],
        "sections": [
            _section(
                "The problem context solves",
                "Prop drilling is passing data through components that don't use it, only to forward it deeper. Context lets you provide a value once and consume it anywhere below — no drilling, no global library.",
                "// Before: drill theme through every layer\n<App theme={theme}>\n  <Header theme={theme}>\n    <Nav theme={theme} />\n  </Header>\n</App>\n\n// After: provide once, consume anywhere\n<ThemeProvider value={theme}>\n  <Header><Nav /></Header>\n</ThemeProvider>",
            ),
            _section(
                "createContext, Provider, useContext",
                "createContext makes a context object with a default. Wrap your tree in <Provider value={...}>. Any descendant calls useContext to read it. Change the value and every consumer re-renders — so keep the value stable.",
                "const ThemeContext = createContext('light');\n\nfunction App() {\n  return (\n    <ThemeContext.Provider value=\"dark\">\n      <Toolbar />\n    </ThemeContext.Provider>\n  );\n}\n\nfunction Toolbar() {\n  const theme = useContext(ThemeContext);  // 'dark'\n  return <div className={theme}>...</div>;\n}",
                "Wrap value={...} in useMemo or useCallback when it is an object/function, or every consumer re-renders on each parent render.",
            ),
            _section(
                "useReducer: predictable state transitions",
                "useReducer replaces many useState calls with a reducer: (state, action) => nextState. Actions are plain objects describing intent — dispatch({ type: 'increment' }). Complex forms, carts, and game state become auditable and testable.",
                "function reducer(state, action) {\n  switch (action.type) {\n    case 'increment': return { count: state.count + 1 };\n    case 'decrement': return { count: state.count - 1 };\n    default: return state;\n  }\n}\n\nconst [state, dispatch] = useReducer(reducer, { count: 0 });\n<button onClick={() => dispatch({ type: 'increment' })}>+</button>",
            ),
            _section(
                "Combining context + reducer safely",
                "Provide state and dispatch through two contexts. Components that only dispatch don't re-render when state changes, which keeps large trees fast. This is the pattern libraries like Redux formalize.",
                "const StateCtx = createContext();\nconst DispatchCtx = createContext();\n\nfunction Provider({ children }) {\n  const [state, dispatch] = useReducer(reducer, initialState);\n  return (\n    <DispatchCtx.Provider value={dispatch}>\n      <StateCtx.Provider value={state}>{children}</StateCtx.Provider>\n    </DispatchCtx.Provider>\n  );\n}\n\nfunction useDispatch() { return useContext(DispatchCtx); }\nfunction useStore() { return useContext(StateCtx); }",
            ),
        ],
        "key_takeaways": [
            "Context removes prop drilling but adds re-render scope",
            "Keep context values stable (useMemo/useCallback) to avoid re-renders",
            "useReducer centralizes state transitions into pure functions",
            "Split state and dispatch contexts so consumers re-render minimally",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("What is the main downside of a new Context Provider?",
                  ["It cannot hold objects", "Every consumer re-renders when the value changes", "It is slower than props", "It requires a library"],
                  1, "A changing value triggers re-renders in all consumers of that context."),
            _quiz("Why split state and dispatch into two contexts?",
                  ["To have more files", "Dispatch-only consumers skip re-renders when state changes", "Because context is limited to one value", "For styling"],
                  1, "The dispatch function reference is stable, so its consumers don't re-render on state change."),
            _quiz("What does dispatch({ type: 'increment' }) do?",
                  ["Mutates state directly", "Sends an action to the reducer, which returns new state", "Renders a component", "Logs to console"],
                  1, "Reducers compute the next state from the previous state and the action — never mutate."),
        ],
        "exercise": _exercise(
            "Theme toggle with context",
            "Create a ThemeContext holding { theme, toggle }. The App provides 'light' and a toggle that flips to 'dark'. A Button consumes it and renders a label showing the current theme.",
            "const ThemeContext = createContext(null);\n\nfunction App() {\n  return (\n    <ThemeContext.Provider value={{ theme: 'light', toggle: () => {} }}>\n      <Button />\n    </ThemeContext.Provider>\n  );\n}\n\nfunction Button() {\n  // consume context here\n  return <button>{/* current theme */}</button>;\n}",
            "const ThemeContext = createContext(null);\n\nfunction App() {\n  const [theme, setTheme] = useState('light');\n  const toggle = useCallback(() => setTheme(t => t === 'light' ? 'dark' : 'light'), []);\n  return (\n    <ThemeContext.Provider value={{ theme, toggle }}>\n      <Button />\n    </ThemeContext.Provider>\n  );\n}\n\nfunction Button() {\n  const { theme, toggle } = useContext(ThemeContext);\n  return <button onClick={toggle}>Theme: {theme}</button>;\n}",
            "useCallback keeps the toggle stable so consumers don't re-render every App render.",
        ),
        "curriculum": ["react"],
    },
    {
        "id": "react-custom-hooks",
        "title": "Custom Hooks: Extract and Reuse Stateful Logic",
        "category": "react",
        "summary": "Custom hooks let you package stateful logic into reusable functions. Anything that combines useState, useEffect, and event listeners can be lifted into a hook and shared across components.",
        "level": "intermediate", "read_time_min": 13,
        "related_topics": ["react-hooks", "react-data-fetching"],
        "sections": [
            _section(
                "A hook is just a function that uses hooks",
                "Name it useSomething, call other hooks inside it, return whatever the component needs. The rules of hooks still apply: no hooks in conditions or loops, and hooks must be called unconditionally at the top level.",
                "function useWindowWidth() {\n  const [width, setWidth] = useState(window.innerWidth);\n  useEffect(() => {\n    const onResize = () => setWidth(window.innerWidth);\n    window.addEventListener('resize', onResize);\n    return () => window.removeEventListener('resize', onResize);\n  }, []);\n  return width;\n}\n\nconst width = useWindowWidth();  // reuse anywhere",
            ),
            _section(
                "The cleanup contract",
                "Effects that subscribe must clean up: remove listeners, clear timers, abort fetches. Returning a function from useEffect does that automatically when the component unmounts or the deps change. Encapsulating it in a hook means you write the cleanup once.",
                "function useCountdown(seconds) {\n  const [left, setLeft] = useState(seconds);\n  useEffect(() => {\n    const id = setInterval(() => setLeft(s => s - 1), 1000);\n    return () => clearInterval(id);  // no leaked interval\n  }, []);\n  return left;\n}",
                "A leaked interval is invisible until your app slows down. Always return the cleanup.",
            ),
            _section(
                "Hooks that return setters and helpers",
                "The best hooks return both data and actions. A form hook can return { values, errors, handleChange, reset }. Consumers stay declarative while the messy wiring lives in one tested place.",
                "function useForm(initial) {\n  const [values, setValues] = useState(initial);\n  const handleChange = useCallback((e) => {\n    setValues(v => ({ ...v, [e.target.name]: e.target.value }));\n  }, []);\n  const reset = useCallback(() => setValues(initial), [initial]);\n  return { values, handleChange, reset };\n}",
            ),
            _section(
                "Composing hooks into bigger hooks",
                "Hooks compose. useUserData = useFetch + useLocalStorage fallback. Build a small library of primitives (useFetch, useLocalStorage, useDebounce) and your feature components read like prose.",
                "function useDebounced(value, delay = 300) {\n  const [debounced, setDebounced] = useState(value);\n  useEffect(() => {\n    const id = setTimeout(() => setDebounced(value), delay);\n    return () => clearTimeout(id);\n  }, [value, delay]);\n  return debounced;\n}\n\nfunction useSearchResults(query) {\n  const debounced = useDebounced(query);\n  return useFetch('/api/search?q=' + encodeURIComponent(debounced));\n}",
            ),
        ],
        "key_takeaways": [
            "A custom hook is a function that calls other hooks",
            "Always return cleanup for subscriptions and timers",
            "Return { values, actions } so consumers stay declarative",
            "Compose small hooks (useFetch, useDebounce) into feature hooks",
        ],
        "tag": "core",
        "quiz": [
            _quiz("What is the most important naming rule for custom hooks?",
                  ["They must start with 'use'", "They must return JSX", "They must be classes", "They must use useReducer"],
                  0, "The use prefix lets React (and the lint rule) detect violations of the rules of hooks."),
            _quiz("Why must effects return cleanup?",
                  ["To be fast", "To remove listeners/timers and prevent leaks", "Because React requires it", "To avoid rendering"],
                  1, "Cleanup prevents duplicate listeners and leaked timers when the component unmounts."),
            _quiz("Can a custom hook call another custom hook?",
                  ["No, only built-ins", "Yes, hooks compose", "Only once", "Only with a library"],
                  1, "Hooks are just functions, so they compose like any functions."),
        ],
        "exercise": _exercise(
            "useDocumentTitle hook",
            "Write a custom hook useDocumentTitle(title) that sets document.title in an effect and restores the previous title on cleanup.",
            "function useDocumentTitle(title) {\n  // your effect here\n}",
            "function useDocumentTitle(title) {\n  useEffect(() => {\n    const previous = document.title;\n    document.title = title;\n    return () => { document.title = previous; };\n  }, [title]);\n}",
            "Capture the previous title before overwriting, then restore it in cleanup.",
        ),
        "curriculum": ["react"],
    },
    {
        "id": "react-data-fetching",
        "title": "Data Fetching in React: Effects, React Query, and Caching",
        "category": "react",
        "summary": "Fetching in effects works but re-implements caching, retries, and loading states every time. Learn the effect pattern first, then the library pattern that removes the boilerplate and keeps data fresh.",
        "level": "advanced", "read_time_min": 16,
        "related_topics": ["react-hooks", "js-async"],
        "sections": [
            _section(
                "Fetching in useEffect, done correctly",
                "State machine: data, loading, error. Use an AbortController so unmounting cancels the request. Guard against state updates after unmount. The dependency array must include everything the fetch depends on.",
                "function User({ id }) {\n  const [user, setUser] = useState(null);\n  const [error, setError] = useState(null);\n  const [loading, setLoading] = useState(true);\n\n  useEffect(() => {\n    const controller = new AbortController();\n    setLoading(true);\n    fetch(`/api/users/${id}`, { signal: controller.signal })\n      .then(r => r.json())\n      .then(setUser)\n      .catch(err => { if (err.name !== 'AbortError') setError(err); })\n      .finally(() => setLoading(false));\n    return () => controller.abort();\n  }, [id]);\n\n  if (loading) return <Spinner />;\n  if (error) return <Error message={error.message} />;\n  return <Profile user={user} />;\n}",
            ),
            _section(
                "Why raw effects get painful",
                "Caching (don't refetch the same user), deduping concurrent requests, background refetch on window focus, retry on failure, pagination — each one is a feature you hand-roll in effects and get subtly wrong. That's the exact gap libraries fill.",
                "// Hand-rolled costs:\n// 1. cache invalidation\n// 2. abort on unmount\n// 3. stale-while-revalidate\n// 4. retry + backoff\n// 5. focus refetch\n// 6. optimistic updates",
            ),
            _section(
                "React Query / TanStack Query",
                "useQuery takes a key and a fetcher. It caches by key, dedupes, retries, and refetches on focus. useMutation handles writes with optimistic updates and invalidation. The library owns the async state machine so your components stay synchronous-looking.",
                "import { useQuery } from '@tanstack/react-query';\n\nfunction useUser(id) {\n  return useQuery({\n    queryKey: ['user', id],\n    queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),\n  });\n}\n\nfunction User({ id }) {\n  const { data, isLoading, error } = useUser(id);\n  if (isLoading) return <Spinner />;\n  if (error) return <Error />;\n  return <Profile user={data} />;\n}",
                "queryKey is the cache address — include every value the fetch depends on, or you'll read stale data.",
            ),
            _section(
                "Invalidation and optimistic updates",
                "After a mutation, invalidate the queries it affected so they refetch. For snappy UX, set the cache optimistically before the server responds, then roll back on error. Libraries make both one-liners.",
                "const queryClient = useQueryClient();\nconst mutation = useMutation({\n  mutationFn: updateUser,\n  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),\n});",
            ),
        ],
        "key_takeaways": [
            "Raw effect fetches need abort + loading/error states",
            "Caching, dedup, retry, and focus refetch are library territory",
            "queryKey is the cache address — include all fetch dependencies",
            "Invalidate queries after mutations to keep data fresh",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("What does the effect cleanup (controller.abort()) do?",
                  ["Stops rendering", "Cancels the in-flight fetch when unmounting", "Clears state", "Closes the app"],
                  1, "Aborting prevents setState on an unmounted component and saves bandwidth."),
            _quiz("What is queryKey in TanStack Query?",
                  ["A password", "The cache address for the query result", "A CSS class", "A database key"],
                  1, "Query results are cached under their key; changing it refetches with the new args."),
            _quiz("After a mutation succeeds, what should you do?",
                  ["Nothing", "Invalidate related queries so they refetch", "Unmount the component", "Reload the page"],
                  1, "Invalidation marks cached data stale so dependent UI refetches the truth."),
        ],
        "exercise": _exercise(
            "Abort-aware fetch hook",
            "Write a useFetch(url) hook that returns { data, loading, error } and aborts on unmount or when the URL changes.",
            "function useFetch(url) {\n  const [data, setData] = useState(null);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() => {\n    // add abort + fetch here\n  }, [url]);\n\n  return { data, loading, error };\n}",
            "function useFetch(url) {\n  const [data, setData] = useState(null);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() => {\n    const controller = new AbortController();\n    setLoading(true);\n    fetch(url, { signal: controller.signal })\n      .then(r => r.json())\n      .then(setData)\n      .catch(err => { if (err.name !== 'AbortError') setError(err); })\n      .finally(() => setLoading(false));\n    return () => controller.abort();\n  }, [url]);\n\n  return { data, loading, error };\n}",
            "The cleanup aborts the previous request whenever url changes or the component unmounts.",
        ),
        "curriculum": ["react"],
    },
    {
        "id": "react-error-boundaries",
        "title": "Error Boundaries, Suspense, and Graceful Failures",
        "category": "react",
        "summary": "A render error unmounts the whole tree unless you catch it. Error boundaries contain crashes to a region; Suspense defers loading; together they turn failures into designed UX instead of white screens.",
        "level": "advanced", "read_time_min": 12,
        "related_topics": ["react-components", "react-data-fetching"],
        "sections": [
            _section(
                "What an error boundary catches",
                "Error boundaries catch errors during rendering, in lifecycle methods, and in constructors of the tree below them. They catch nothing in event handlers, async code, SSR, or the boundary itself — those need try/catch.",
                "class ErrorBoundary extends React.Component {\n  state = { hasError: false };\n\n  static getDerivedStateFromError() {\n    return { hasError: true };\n  }\n\n  componentDidCatch(error, info) {\n    console.error(error, info);\n  }\n\n  render() {\n    if (this.state.hasError) {\n      return <h1>Something went wrong. Reload.</h1>;\n    }\n    return this.props.children;\n  }\n}",
            ),
            _section(
                "Wrapping regions, not the whole app",
                "One boundary around the entire app shows a full-page crash. Boundaries around cards, feeds, and dashboards mean one failed widget shows its own fallback while the rest of the page keeps working.",
                "// Granular: one bad card doesn't kill the feed\n<div className=\"grid\">\n  {posts.map(p => (\n    <ErrorBoundary key={p.id}>\n      <PostCard post={p} />\n    </ErrorBoundary>\n  ))}\n</div>",
                "Design a reusable <Boundary fallback={<Skeleton />}> component so every region has a consistent recovery UI.",
            ),
            _section(
                "Suspense: declarative loading",
                "Suspense lets components say 'I'm waiting for data' and shows a fallback until they resolve. With lazy() it powers code splitting; with data libraries it powers streaming load states — all without per-component spinners.",
                "import { Suspense, lazy } from 'react';\n\nconst Profile = lazy(() => import('./Profile'));\n\n<Suspense fallback={<Skeleton />}>\n  <Profile userId={id} />\n</Suspense>",
            ),
            _section(
                "The failure plan",
                "Build a failure ladder: 1) validate inputs, 2) try/catch event handlers and async, 3) boundaries for render errors, 4) a top-level boundary as the last resort, 5) telemetry on every caught error. Design fallbacks for each rung.",
                "function handleClick() {\n  try {\n    await save();\n  } catch (e) {\n    reportError(e);\n    toast('Save failed — try again');\n  }\n}\n\n// Render errors below are caught by the boundary,\n// not by try/catch (which cannot see render crashes).",
            ),
        ],
        "key_takeaways": [
            "Boundaries catch render errors; try/catch handles events + async",
            "Wrap regions, not the whole app, so one failure is contained",
            "Suspense shows fallbacks while lazy/data load",
            "Ladder: validate â†’ try/catch â†’ boundary â†’ top boundary â†’ telemetry",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz("Which errors does an error boundary catch?",
                  ["Errors in event handlers", "Errors during rendering of the tree below it", "Errors in async functions", "Network errors"],
                  1, "Boundaries catch render/lifecycle/constructor errors in their subtree."),
            _quiz("What must an error boundary render?",
                  ["A <div>", "A fallback UI when hasError is true", "The same children", "An error object"],
                  1, "When hasError is set, the boundary renders its fallback instead of children."),
            _quiz("What does <Suspense fallback={...}> show?",
                  ["An error", "The fallback while a suspended child loads", "The children", "Nothing"],
                  1, "Suspense renders the fallback until suspended (lazy/data) children resolve."),
        ],
        "exercise": _exercise(
            "Safe widget",
            "Wrap a <StatsWidget /> (which may throw) in an error boundary that shows 'Stats unavailable' instead of crashing the page.",
            "function SafeStats({ data }) {\n  return (\n    // wrap StatsWidget in an ErrorBoundary here\n    <StatsWidget data={data} />\n  );\n}",
            "class StatsErrorBoundary extends React.Component {\n  state = { hasError: false };\n  static getDerivedStateFromError() { return { hasError: true }; }\n  render() {\n    if (this.state.hasError) return <p>Stats unavailable</p>;\n    return this.props.children;\n  }\n}\n\nfunction SafeStats({ data }) {\n  return (\n    <StatsErrorBoundary>\n      <StatsWidget data={data} />\n    </StatsErrorBoundary>\n  );\n}",
            "getDerivedStateFromError flips the flag that switches to the fallback.",
        ),
        "curriculum": ["react"],
    },
]


INTERACTIVES = {
    "ts-why-types": {
        "quiz": [
            _quiz("What does TypeScript add to JavaScript?",
                  ["A runtime engine", "A compile-time type system", "New CSS", "A database"],
                  1, "Types are checked before runtime and erased at build time."),
            _quiz("When is a TypeScript type error reported?",
                  ["At runtime", "At compile time", "In the browser console", "Never"],
                  1, "The compiler catches type mistakes before the code ever runs."),
            _quiz("What is the benefit of strict typing for refactors?",
                  ["Faster runtime", "The compiler finds every place that breaks", "Smaller bundles", "No runtime"],
                  1, "Changing a type surfaces every usage that no longer fits."),
        ],
        "exercise": _exercise(
            "Annotate a function",
            "Annotate the parameters and return type of a function that greets a user by name.",
            "function greet(name) {\n  return 'Hello, ' + name;\n}",
            "function greet(name: string): string {\n  return 'Hello, ' + name;\n}",
            "Type the parameter as string and the return as string.",
        ),
    },
    "ts-interfaces-generics": {
        "quiz": [
            _quiz("What does an interface describe?",
                  ["A class", "The shape of an object", "A function body", "A runtime value"],
                  1, "Interfaces define contracts: which properties and methods a value must have."),
            _quiz("Why use generics instead of any?",
                  ["Less typing", "Generics keep the type relationship between input and output", "Generics run faster", "any is forbidden"],
                  1, "Generics preserve type information so the return type follows the input."),
            _quiz("What is the key word to constrain a generic type parameter?",
                  ["implements", "extends", "super", "with"],
                  1, "T extends SomeType limits T to types assignable to SomeType."),
        ],
        "exercise": _exercise(
            "Generic identity",
            "Write a generic function firstElement that takes an array of T and returns the first element (T | undefined).",
            "function firstElement(arr: any): any {\n  return arr[0];\n}",
            "function firstElement<T>(arr: T[]): T | undefined {\n  return arr[0];\n}",
            "Add a type parameter T and type the array as T[].",
        ),
    },
    "react-components": {
        "quiz": [
            _quiz("What do props do in React?",
                  ["Store local state", "Pass data from parent to child", "Handle CSS", "Query the database"],
                  1, "Props flow down from parent to child and are read-only in the child."),
            _quiz("What is JSX?",
                  ["A templating engine", "A syntax extension that describes UI in JavaScript", "A CSS preprocessor", "A database"],
                  1, "JSX compiles to React.createElement calls — UI expressed as expressions."),
            _quiz("How does a child tell its parent something happened?",
                  ["By mutating props", "By calling a callback prop", "By returning a value", "By editing state directly"],
                  1, "Events flow up: the parent passes a callback, the child invokes it."),
        ],
        "exercise": _exercise(
            "Greeting component",
            "Write a function component Greeting that takes a name prop and renders 'Hello, <name>!' in an h1.",
            "function Greeting(props) {\n  return <div>Replace me</div>;\n}",
            "function Greeting(props) {\n  return <h1>Hello, {props.name}!</h1>;\n}",
            "Access the name through props and render it inside JSX braces.",
        ),
    },
    "react-hooks": {
        "quiz": [
            _quiz("What does useState return?",
                  ["A single value", "A pair: the current value and an updater function", "An object", "The DOM node"],
                  1, "const [state, setState] = useState(initial) is the canonical destructure."),
            _quiz("When does useEffect run?",
                  ["Every render unconditionally", "After render when deps change", "Before render", "Never"],
                  1, "Effects run after the commit phase; changing deps re-runs them."),
            _quiz("Why should derived values not be stored in state?",
                  ["It is slower", "It risks stale copies when the source changes", "It uses more memory", "It is forbidden"],
                  1, "Compute derived values during render so they always reflect their inputs."),
        ],
        "exercise": _exercise(
            "Counter with a step",
            "Create a counter that starts at 0 and increments by a step value using useState.",
            "function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={/* increment */}>{count}</button>;\n}",
            "function Counter() {\n  const [count, setCount] = useState(0);\n  const step = 2;\n  return <button onClick={() => setCount(c => c + step)}>{count}</button>;\n}",
            "Use the functional updater setCount(c => c + step) to read the latest count.",
        ),
    },
    "react-performance": {
        "quiz": [
            _quiz("What triggers a re-render?",
                  ["State change, prop change, or parent re-render", "Any DOM change", "Console logs", "Network requests"],
                  0, "A component re-renders when its state/props change or its parent re-renders."),
            _quiz("When does React.memo help?",
                  ["Always", "When the component re-renders often but its props rarely change", "When it uses useEffect", "When it is large"],
                  1, "memo skips re-renders when props are referentially equal."),
            _quiz("What does code splitting shrink?",
                  ["The server", "The initial JS bundle", "The database", "The CSS"],
                  1, "Splitting with React.lazy loads chunks on demand, shrinking the initial download."),
        ],
        "exercise": _exercise(
            "Stabilize a callback",
            "Fix the re-render: wrap handleClick in useCallback so <ExpensiveButton> (memoized) does not re-render on every keystroke.",
            "function App() {\n  const [text, setText] = useState('');\n  const handleClick = () => console.log('click');\n  return (\n    <input value={text} onChange={e => setText(e.target.value)} />\n    <ExpensiveButton onClick={handleClick} />\n  );\n}",
            "function App() {\n  const [text, setText] = useState('');\n  const handleClick = useCallback(() => console.log('click'), []);\n  return (\n    <input value={text} onChange={e => setText(e.target.value)} />\n    <ExpensiveButton onClick={handleClick} />\n  );\n}",
            "useCallback keeps the function identity stable so memo can skip the re-render.",
        ),
    },
}


