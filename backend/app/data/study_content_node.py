"""Node.js Study Library expansion — in-depth articles for the Learning Hub.

Five new Node articles (npm, Express middleware, auth/JWT, testing, databases)
plus interactives (quiz + exercise) for the two existing Node articles
(node-server, node-files-streams). Imported by app.data.study_materials.
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
    {
        "id": "node-npm-modules",
        "title": "npm, package.json, and Managing Dependencies",
        "category": "node",
        "summary": "npm is how Node projects get libraries, and package.json is the manifest that declares them. Learn dependencies vs devDependencies, lockfiles, and semantic versioning so installs are reproducible and CI never surprises you.",
        "level": "beginner",
        "read_time_min": 12,
        "related_topics": ["node-server", "js-async"],
        "sections": [
            _section(
                "What npm is and what package.json declares",
                "npm (Node Package Manager) ships with Node and installs libraries from the npm registry. Running npm init in a folder writes a package.json manifest. The two fields that matter most are dependencies (libraries your app needs at runtime) and scripts (shortcut commands). Every project you clone should already have one — if a repo is missing it, that's your first clue something is wrong.",
                "{\n  \"name\": \"my-api\",\n  \"version\": \"1.0.0\",\n  \"main\": \"index.js\",\n  \"scripts\": {\n    \"start\": \"node index.js\"\n  },\n  \"dependencies\": {\n    \"express\": \"^4.19.0\"\n  }\n}",
            ),
            _section(
                "dependencies vs devDependencies",
                "npm install express saves the package into dependencies. The --save-dev flag (or -D) saves into devDependencies. The rule: anything your production server needs at runtime — Express, bcrypt, a DB driver — goes in dependencies. Anything only used while developing or building — Jest, ESLint, nodemon, Babel — goes in devDependencies. When you deploy with NODE_ENV=production (or npm ci --omit=dev), dev packages are skipped entirely, shrinking installs and attack surface.",
                "npm install express          # runtime dependency → \"dependencies\"\nnpm install --save-dev jest  # dev-only tooling → \"devDependencies\"\nnpm install -D nodemon",
            ),
            _section(
                "Lockfiles and reproducible installs",
                "npm install reads package.json and writes package-lock.json, which pins the exact resolved version of every package and its transitive dependencies. Commit it. The file exists so two developers (and CI) install the same tree. npm install may update the lockfile as it resolves ranges; npm ci wipes node_modules and installs exactly what the lockfile pins, which is why CI scripts should use npm ci, never npm install.",
                "npm install   # reads package.json + lockfile; may update the lockfile\nnpm ci        # wipes node_modules, installs exactly what the lockfile pins",
            ),
            _section(
                "Semantic versioning and npm scripts",
                "Dependency ranges use semver: a caret ^4.19.0 allows any 4.x (minor + patch), a tilde ~4.17.0 allows only 4.17.x (patch), and an exact 4.3.2 means exactly that version. Lockfiles remove the guesswork, but the range still decides what npm update can pull. Scripts turn long commands into npm run <name>: npm start, npm test, npm run lint. Node, npm and common tools know the conventional names, so keep them conventional.",
                "{\n  \"scripts\": {\n    \"start\": \"node index.js\",\n    \"test\": \"jest\",\n    \"lint\": \"eslint .\"\n  },\n  \"dependencies\": {\n    \"express\": \"^4.19.0\",\n    \"lodash\": \"~4.17.0\",\n    \"debug\": \"4.3.2\"\n  }\n}",
                "Commit package-lock.json and run npm ci in CI, never npm install. If two machines must build identical output, a shared lockfile plus npm ci is the only thing that guarantees it. And when you deploy a production server, install with NODE_ENV=production so devDependencies are skipped.",
            ),
        ],
        "key_takeaways": [
            "package.json declares metadata, scripts, and dependency lists",
            "Runtime libraries live in dependencies; build/test tooling in devDependencies",
            "Commit package-lock.json and install with npm ci for reproducible builds",
            "npm run <name> runs scripts; ^ allows minor versions, ~ allows patches only",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which command creates a new package.json interactively in the current folder?",
                ["npm new", "npm create app", "npm init", "npm install"],
                2,
                "npm init walks you through the fields and writes a package.json manifest. npm install installs dependencies — it does not scaffold a project. npm new and npm create app are not npm commands.",
            ),
            _quiz(
                "Where should Jest (a test runner used only while developing) live?",
                ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"],
                1,
                "Jest runs during development and in CI, never in production, so it belongs in devDependencies. Production installs with NODE_ENV=production (or --omit=dev) skip it, keeping the runtime install lean.",
            ),
            _quiz(
                "Which command guarantees a byte-for-byte reproducible install from the lockfile?",
                ["npm install", "npm update", "npm ci", "npm audit"],
                2,
                "npm ci deletes node_modules and installs exactly what package-lock.json pins, so every machine gets the same tree. npm install may drift by re-resolving ranges and updating the lockfile.",
            ),
        ],
        "exercise": _exercise(
            "Write a package.json by hand",
            "Create a package.json for an Express API. It needs: name \"todo-api\", version 1.0.0, a \"start\" script that runs node index.js, express in dependencies, and jest in devDependencies.",
            "{\n  \"name\": \"todo-api\",\n  \"version\": \"1.0.0\",\n  \"scripts\": {},\n  \"dependencies\": {},\n  \"devDependencies\": {}\n}",
            "{\n  \"name\": \"todo-api\",\n  \"version\": \"1.0.0\",\n  \"scripts\": {\n    \"start\": \"node index.js\"\n  },\n  \"dependencies\": {\n    \"express\": \"^4.19.0\"\n  },\n  \"devDependencies\": {\n    \"jest\": \"^29.7.0\"\n  }\n}",
            "Express is a runtime server library, so it goes in dependencies. Jest only runs tests, so it belongs in devDependencies.",
        ),
        "curriculum": ["node"],
    },
    {
        "id": "node-express-middleware",
        "title": "Express Middleware: Requests, Validation, and Error Handling",
        "category": "node",
        "summary": "Middleware is the engine of Express: a pipeline that every request flows through. Master the order, next(), validation, and the four-argument error handler, and you control exactly what your API does — and what it lets through.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["node-server", "node-auth-jwt", "js-async"],
        "sections": [
            _section(
                "The middleware pipeline and why order matters",
                "A request enters your app and flows through every matching middleware function in the order they were registered. Each function either ends the cycle by sending a response, or calls next() to hand control to the next middleware in line. If none respond and next() is never called, the request hangs until the client gives up. This ordering is why app.use(express.json()) must come before the routes that read req.body.",
                "const express = require('express');\nconst app = express();\n\napp.use((req, res, next) => {\n  console.log(req.method + ' ' + req.path);\n  next();\n});\n\napp.get('/health', (req, res) => res.json({ ok: true }));\n\napp.listen(3000);",
            ),
            _section(
                "Built-in and third-party middleware",
                "Express ships a few battle-tested middlewares and the ecosystem provides the rest. express.json() parses JSON request bodies into req.body. express.static('public') serves static files. cors() adds CORS headers for browser clients, and morgan logs requests. Each is just a function that processes the request and calls next() — composing them is the whole design.",
                "app.use(express.json());\napp.use(express.static('public'));\napp.use(cors());\n\napp.post('/users', (req, res) => {\n  res.json({ received: req.body });\n});",
            ),
            _section(
                "Validation middleware",
                "Never trust input. A validation middleware checks the request, rejects bad data with a 400 before any handler runs, and calls next() only for good data. Because it is middleware, you can attach it to a single route or chain multiple validators. This keeps handlers lean: by the time the handler runs, the data is already safe to use.",
                "function validateEmail(req, res, next) {\n  const email = req.body && req.body.email;\n  if (!email || !email.includes('@')) {\n    return res.status(400).json({ error: 'A valid email is required' });\n  }\n  next();\n}\n\napp.post('/users', validateEmail, (req, res) => {\n  res.status(201).json({ email: req.body.email });\n});",
            ),
            _section(
                "Error-handling middleware",
                "Error middleware has exactly four parameters (err, req, res, next) — Express detects it by that arity. It runs last and is the single place that turns thrown errors into HTTP responses. When an async handler fails, catch the rejection and call next(err): that skips every normal middleware and jumps straight to the error handler. Never respond from inside a handler that already called next(err), and never swallow errors.",
                "// route: forwards async errors to the error middleware\napp.post('/users', async (req, res, next) => {\n  try {\n    const user = await db.create(req.body);\n    res.status(201).json(user);\n  } catch (err) {\n    next(err); // skip ahead to the error middleware\n  }\n});\n\n// error middleware: 4 params, registered LAST\napp.use((err, req, res, next) => {\n  console.error(err.message);\n  res.status(err.status || 500).json({ error: err.message });\n});",
                "Register error middleware after every route. next() with no argument continues the pipeline; next(err) jumps straight to the error handler. In the error handler itself, call next(err) only when delegating to another error handler — if you call next() plain, the client may never receive a response.",
            ),
        ],
        "key_takeaways": [
            "Middleware runs in registration order; call next() to continue the pipeline",
            "express.json() and express.static() are just middleware that must be registered early",
            "Validation middleware rejects bad input with a 400 before handlers run",
            "Error middleware has exactly 4 parameters, runs last, and is reached via next(err)",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "In what order does Express run middleware and route handlers for a request?",
                ["Alphabetical by path", "In the order they were registered", "Reverse registration order", "Randomly per request"],
                1,
                "Express matches and executes handlers in the order they are registered with app.use or app.METHOD. That's why middleware like express.json() must be registered before the routes that depend on req.body.",
            ),
            _quiz(
                "A handler runs, never calls next(), and never sends a response. What happens?",
                ["Express responds 404", "The request hangs until the client times out", "Express auto-responds 500", "The handler runs again"],
                1,
                "Express only runs the pipeline once. If nothing responded and next() was never called, the request stays open — typically until the client or a reverse proxy times out. Every path must either respond or call next().",
            ),
            _quiz(
                "How does Express know a function is error-handling middleware?",
                ["It is named errorHandler", "It is registered with app.error()", "It has exactly 4 parameters (err, req, res, next)", "It returns a rejected promise"],
                2,
                "Express inspects the function's arity: a 4-parameter function is treated as error middleware and is only invoked when an error is forwarded via next(err). Plain middleware has 3 parameters and won't catch errors.",
            ),
        ],
        "exercise": _exercise(
            "Time every request",
            "Add middleware that measures how long each request took and logs it. Register it before the routes so it wraps everything.",
            "const express = require('express');\nconst app = express();\n\napp.get('/health', (req, res) => res.json({ ok: true }));\n\napp.listen(3000, () => console.log('up on :3000'));",
            "const express = require('express');\nconst app = express();\n\napp.use((req, res, next) => {\n  const start = Date.now();\n  res.on('finish', () => {\n    console.log(req.method + ' ' + req.path + ' took ' + (Date.now() - start) + 'ms');\n  });\n  next();\n});\n\napp.get('/health', (req, res) => res.json({ ok: true }));\n\napp.listen(3000, () => console.log('up on :3000'));",
            "Grab Date.now() before next(), then listen for the response 'finish' event and log the elapsed milliseconds. Registering with app.use before the routes ensures every request passes through it.",
        ),
        "curriculum": ["node"],
    },
    {
        "id": "node-auth-jwt",
        "title": "Authentication in Node: Passwords, Sessions, and JWTs",
        "category": "node",
        "summary": "Authentication is hashing, not storing. Protect passwords with bcrypt, keep users logged in with a session or a signed JWT, and lock down routes with middleware that verifies the token on every request.",
        "level": "intermediate",
        "read_time_min": 16,
        "related_topics": ["node-server", "node-databases", "node-express-middleware"],
        "sections": [
            _section(
                "Hashing passwords with bcrypt",
                "Never store a plaintext password — a leaked database then leaks every account. bcrypt hashes passwords with a unique random salt and a tunable cost factor that makes each attempt deliberately slow, so brute-forcing is impractical. You store only the hash. On login you compare the incoming password against the stored hash with bcrypt.compare; the function is async and always returns a boolean.",
                "const bcrypt = require('bcrypt');\n\nasync function register(email, password) {\n  const saltRounds = 10;\n  const hash = await bcrypt.hash(password, saltRounds);\n  return db.users.insert({ email, passwordHash: hash });\n}\n\nasync function login(email, password, storedHash) {\n  const ok = await bcrypt.compare(password, storedHash);\n  if (!ok) throw new Error('Invalid credentials');\n  return ok;\n}",
            ),
            _section(
                "Sessions vs tokens",
                "A session is stateful: after login the server stores a session record and gives the client a session ID, usually in an httpOnly cookie. Every request looks the session up — easy to revoke, but the server carries the state. A JWT is stateless: after login the server signs a token that carries the claims (userId, role) and the client sends it on every request. Nothing is stored, which scales beautifully but means a leaked token is valid until it expires.",
                "// stateful session: the server remembers the session\nres.cookie('sessionId', session.id, { httpOnly: true });\n\n// stateless JWT: the token carries the claims itself\nconst token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });",
            ),
            _section(
                "Signing and verifying JWTs",
                "The jsonwebtoken package signs and verifies tokens. jwt.sign creates a token from a payload, a secret, and options like expiresIn. jwt.verify recomputes the signature with the same secret — if the token was tampered with, or has expired, it throws. The payload is only base64-encoded, not encrypted, so never put secrets in it; the signature is what proves authenticity.",
                "const jwt = require('jsonwebtoken');\n\nconst token = jwt.sign(\n  { userId: user.id, role: user.role },\n  process.env.JWT_SECRET,\n  { expiresIn: '1h' }\n);\n\ntry {\n  const payload = jwt.verify(token, process.env.JWT_SECRET);\n  console.log(payload.userId);\n} catch (err) {\n  console.log('token invalid or expired');\n}",
            ),
            _section(
                "Auth middleware that protects routes",
                "The pattern is simple and powerful: write an authRequired middleware that reads the token, verifies it, attaches the decoded payload to req, and calls next(). Any route that lists authRequired in its handler chain is protected. Because middleware runs in order, the handler only executes for verified requests — no token, no handler.",
                "function authRequired(req, res, next) {\n  const header = req.headers.authorization || '';\n  const token = header.startsWith('Bearer ') ? header.slice(7) : null;\n  if (!token) return res.status(401).json({ error: 'Missing token' });\n  try {\n    req.user = jwt.verify(token, process.env.JWT_SECRET);\n    next();\n  } catch (err) {\n    return res.status(401).json({ error: 'Invalid or expired token' });\n  }\n}\n\napp.get('/profile', authRequired, (req, res) => {\n  res.json({ userId: req.user.userId });\n});",
                "Prefer httpOnly cookies over localStorage for tokens — a cookie never touches JavaScript, so an XSS attack can't read it. Keep JWT_SECRET in a .env file, never in source control. Use short expirations (15 minutes to 1 hour) plus a refresh token for long-lived sessions, and always run bcrypt with at least 10 salt rounds.",
            ),
        ],
        "key_takeaways": [
            "Hash passwords with bcrypt (10+ rounds); never store plaintext or a fast hash",
            "Sessions are stateful and revocable; JWTs are stateless and self-contained",
            "jwt.sign creates a token, jwt.verify validates signature and expiry",
            "Protect routes with authRequired middleware that verifies the token before the handler",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Why is bcrypt preferred over a fast hash like SHA-256 for passwords?",
                ["It is easier to type", "It is deliberately slow and salted, making brute-force and rainbow tables impractical", "It is reversible", "It stores plaintext"],
                1,
                "bcrypt's cost factor makes each attempt slow, and every hash gets a unique salt, so precomputed tables are useless. Fast hashes like SHA-256 let an attacker test billions of guesses per second — the exact opposite of what you want.",
            ),
            _quiz(
                "What does jwt.verify(token, secret) check?",
                ["That the token is under 1 KB", "Only the expiry date", "The signature, expiry, and that claims are valid", "That the user is online"],
                2,
                "jwt.verify recomputes the HMAC signature with the secret to prove the token wasn't modified, then checks the exp claim. It throws for tampered or expired tokens, which your catch turns into a 401.",
            ),
            _quiz(
                "Which is the correct middleware pattern to protect a route?",
                ["app.get('/profile', authRequired, handler)", "Pass the token as a query string and ignore it", "Check the password on every request", "app.get('/profile', handler, authRequired)"],
                0,
                "Express runs middleware in registration order, so authRequired runs before the handler: it can reject with a 401 or attach req.user for the handler to use. Listing it after the handler would leave the route wide open.",
            ),
        ],
        "exercise": _exercise(
            "Hash passwords on signup",
            "The signup route currently stores the plaintext password. Hash it with bcrypt (10 salt rounds) before saving, and reject a missing email or password with a 400.",
            "const bcrypt = require('bcrypt');\nconst express = require('express');\nconst app = express();\napp.use(express.json());\n\nconst users = [];\n\napp.post('/signup', async (req, res) => {\n  const { email, password } = req.body;\n  users.push({ email, password }); // TODO: hash me\n  res.status(201).json({ email });\n});\n\napp.listen(3000);",
            "const bcrypt = require('bcrypt');\nconst express = require('express');\nconst app = express();\napp.use(express.json());\n\nconst users = [];\n\napp.post('/signup', async (req, res) => {\n  const { email, password } = req.body;\n  if (!email || !password) {\n    return res.status(400).json({ error: 'email and password are required' });\n  }\n  const passwordHash = await bcrypt.hash(password, 10);\n  users.push({ email, passwordHash });\n  res.status(201).json({ email });\n});\n\napp.listen(3000);",
            "bcrypt.hash(password, 10) returns a Promise — await it before saving, and store passwordHash, never the raw password.",
        ),
        "curriculum": ["node"],
    },
    {
        "id": "node-testing",
        "title": "Testing Node Apps: Unit, Integration, and Mocking",
        "category": "node",
        "summary": "Tests turn 'it works on my machine' into 'it works, and stays working'. Learn the testing pyramid, describe/it/expect syntax, how to mock external services, and how supertest exercises your real Express routes.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["node-server", "node-express-middleware", "js-async"],
        "sections": [
            _section(
                "The test runner and the testing pyramid",
                "A test runner (Jest, Vitest, or the built-in node:test) executes test files and reports pass/fail. The syntax is a suite of describe blocks containing individual it (or test) cases, each ending in assertions via expect. The pyramid says: many fast unit tests at the base, fewer integration tests in the middle, and a handful of end-to-end tests on top — slow, broad tests are the expensive ones.",
                "const { sum } = require('./math');\n\ndescribe('sum', () => {\n  it('adds two positive numbers', () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n  it('adds zero', () => {\n    expect(sum(5, 0)).toBe(5);\n  });\n});",
            ),
            _section(
                "Unit tests for pure functions",
                "A pure function returns the same output for the same input and touches nothing external — no files, no network, no database. Those are the easiest things to test and the most valuable: they cover your business logic in milliseconds. Test the happy path plus the edge cases: zero, negatives, rounding, and error paths.",
                "// lib/price.js\nfunction withTax(amount, rate) {\n  return Math.round((amount * (1 + rate)) * 100) / 100;\n}\nmodule.exports = { withTax };\n\n// lib/price.test.js\nconst { withTax } = require('./price');\n\ndescribe('withTax', () => {\n  it('applies a 20% rate', () => {\n    expect(withTax(100, 0.2)).toBe(120);\n  });\n  it('rounds to two decimals', () => {\n    expect(withTax(9.99, 0.2)).toBe(11.99);\n  });\n});",
            ),
            _section(
                "Mocking external dependencies",
                "A unit test should run fast, deterministically, and without real infrastructure. jest.mock replaces a module — like your email or database layer — with a stub, and you assert on how it was called. The test proves your code calls sendEmail with the right arguments without actually sending a single email.",
                "const { sendEmail } = require('./mailer');\n\njest.mock('./mailer');\n\nfunction notify(user) {\n  return sendEmail(user.email, 'Welcome!');\n}\n\ntest('sendEmail is called with the user address', async () => {\n  const user = { email: 'ada@example.com' };\n  await notify(user);\n  expect(sendEmail).toHaveBeenCalledWith('ada@example.com', 'Welcome!');\n});",
            ),
            _section(
                "Integration tests with supertest",
                "Unit tests prove pieces; integration tests prove the wiring. supertest sends real HTTP requests through your Express app without binding a port, and you assert on status and body. To make it work, export the app from app.js and keep app.listen in a separate server.js. One integration test can catch a middleware ordering bug that a hundred unit tests miss.",
                "const request = require('supertest');\nconst app = require('./app'); // exports the express app, no listen()\n\ndescribe('GET /health', () => {\n  it('returns ok: true', async () => {\n    const res = await request(app).get('/health');\n    expect(res.status).toBe(200);\n    expect(res.body).toEqual({ ok: true });\n  });\n});",
                "Split app.js (exports the app) from server.js (calls app.listen) — supertest needs the app without a bound port. Run tests with npm test, and during development use watch mode (npx jest --watch) so failures surface the instant you save.",
            ),
        ],
        "key_takeaways": [
            "describe groups tests; it/test defines a case; expect(...).toBe(...) asserts",
            "Unit tests cover pure business logic — fast, no IO, no network",
            "Mock external modules so tests are fast, deterministic, and side-effect-free",
            "supertest exercises real routes: request(app).get('/users') without a port",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "Which functions does Jest use to group related tests and define a single test?",
                ["group + case", "describe + it/test", "suite + check", "block + assert"],
                1,
                "describe() creates a suite that groups related tests, and it() or test() defines one test case containing assertions. There is no group/case or suite/check API in Jest.",
            ),
            _quiz(
                "Why mock the database layer in a unit test?",
                ["It makes tests slow so you appreciate them", "To keep tests fast, deterministic, and free of external state", "Because mocks are required by law", "To hide bugs"],
                1,
                "A real database adds latency, needs setup, and makes results depend on external state. Mocking replaces it so the test exercises only the code under test and passes or fails reliably.",
            ),
            _quiz(
                "What does request(app).get('/health') from supertest do?",
                ["Calls fetch in the browser", "Sends a real HTTP request through your Express app and returns the response", "Starts a second server", "Loads the page in a headless browser"],
                1,
                "supertest wires the request directly into the Express app without binding a port, exercising the real route stack and middleware. You then assert on status, headers, and body — an integration test of your API.",
            ),
        ],
        "exercise": _exercise(
            "Write your first unit test",
            "isEven lives in math.js. Write a test file that verifies isEven(4) is true, isEven(7) is false, and that a non-number throws.",
            "// math.js\nfunction isEven(n) {\n  if (typeof n !== 'number') throw new Error('n must be a number');\n  return n % 2 === 0;\n}\nmodule.exports = { isEven };",
            "// math.test.js\nconst { isEven } = require('./math');\n\ndescribe('isEven', () => {\n  it('returns true for even numbers', () => {\n    expect(isEven(4)).toBe(true);\n  });\n  it('returns false for odd numbers', () => {\n    expect(isEven(7)).toBe(false);\n  });\n  it('throws for non-numbers', () => {\n    expect(() => isEven('4')).toThrow('n must be a number');\n  });\n});",
            "Use expect(...).toThrow() with a function wrapper, because the error is thrown when the function runs — the wrapper lets Jest catch it.",
        ),
        "curriculum": ["node"],
    },
    {
        "id": "node-databases",
        "title": "Databases in Node: SQL, NoSQL, ORMs, and Migrations",
        "category": "node",
        "summary": "Your data outlives your process. Choose SQL or NoSQL for the data shape, drive it with a pooled client and parameterized queries, model it with an ORM, and keep the schema honest with migrations.",
        "level": "advanced",
        "read_time_min": 16,
        "related_topics": ["node-server", "sql-database", "node-auth-jwt"],
        "sections": [
            _section(
                "SQL vs NoSQL",
                "Relational databases (PostgreSQL, MySQL) impose a schema and shine at joins, integrity, and transactions — the right default for users, orders, and anything with relationships. Document databases (MongoDB) accept flexible, varying documents and scale out horizontally, ideal for loosely structured data. There is no universal winner: match the database to the query patterns and consistency guarantees your app needs.",
                "-- relational (SQL): normalized, joined across tables\nSELECT u.name, o.total\nFROM users u\nJOIN orders o ON o.user_id = u.id\nWHERE u.id = 42;\n\n// document (MongoDB): denormalized, embed related data\n// { _id: 42, name: 'Ada', orders: [{ total: 299 }] }",
            ),
            _section(
                "Drivers and raw SQL with parameterized queries",
                "pg (PostgreSQL) and mysql2 are thin drivers that execute SQL and return rows. Use a connection pool: establishing a database connection is expensive, so a pool keeps a set of live connections to reuse across requests. The critical rule is to never build SQL by concatenating user input — pass values as bind parameters ($1, $2 in pg) so the driver sends them as data, never as SQL.",
                "const { Pool } = require('pg');\n\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL });\n\n// SAFE: $1 is a bind parameter, the driver escapes it\nconst res = await pool.query(\n  'SELECT * FROM users WHERE email = $1',\n  [email]\n);\n\n// DANGEROUS: template interpolation injects raw text into SQL\n// await pool.query(`SELECT * FROM users WHERE email = '${email}'`);",
            ),
            _section(
                "ORMs: modeling data in code",
                "An ORM (Sequelize, Prisma, Drizzle) maps tables and documents to typed objects and generates queries from a model definition. You get productivity, type safety, and a consistent API; you trade away fine-grained control over generated SQL and some raw performance. Prisma is schema-first — you declare the schema and it generates a type-safe client.",
                "const { Sequelize, DataTypes } = require('sequelize');\nconst sequelize = new Sequelize(process.env.DATABASE_URL);\n\nconst User = sequelize.define('User', {\n  email: { type: DataTypes.STRING, allowNull: false, unique: true },\n  passwordHash: DataTypes.STRING\n});\n\nawait User.create({ email: 'ada@example.com', passwordHash });\nconst ada = await User.findOne({ where: { email: 'ada@example.com' } });\n\n// Prisma (schema-first):\n// model User {\n//   id    Int    @id @default(autoincrement())\n//   email String @unique\n// }\n// const ada = await prisma.user.create({ data: { email } });",
            ),
            _section(
                "Migrations: versioning the schema",
                "A migration is a versioned change to your schema: an up() that applies the change and a down() that reverses it. They run in order, in every environment, so staging and production converge on the same schema. The rule of thumb: never hand-edit a production table — add a new migration instead. That's how a team of ten changes the same schema without stepping on each other.",
                "// migrations/20260101001-create-users.cjs (Sequelize style)\nmodule.exports = {\n  async up(queryInterface, Sequelize) {\n    await queryInterface.createTable('users', {\n      id: { type: Sequelize.INTEGER, autoIncrement: true, primaryKey: true },\n      email: { type: Sequelize.STRING, allowNull: false, unique: true },\n      createdAt: Sequelize.DATE,\n      updatedAt: Sequelize.DATE\n    });\n  },\n  async down(queryInterface) {\n    await queryInterface.dropTable('users');\n  }\n};",
                "Always write a down() that fully reverses up() — even if it seems unlikely you'll need it, a broken rollback blocks every teammate behind you. Run migrations as an explicit deploy step (never from inside request handlers) so the schema change and the code that relies on it land together.",
            ),
        ],
        "key_takeaways": [
            "SQL suits relational data and joins; NoSQL suits flexible, scale-out documents",
            "Use a connection pool and parameterized queries — never interpolate user input into SQL",
            "ORMs model data in code and generate queries, trading control for productivity",
            "Migrations version schema changes with reversible up/down steps",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "What is the main reason to use parameterized queries ($1, $2 in pg) instead of concatenating user input into SQL strings?",
                ["It is faster to type", "It prevents SQL injection by sending values separately from the SQL text", "It makes queries shorter", "It avoids indexes"],
                1,
                "With bind parameters the driver and database treat the value strictly as data, never as SQL. An attacker's input cannot escape into the query text, so injection becomes impossible.",
            ),
            _quiz(
                "What does an ORM like Prisma or Sequelize do?",
                ["Replaces your database", "Maps tables/documents to code objects and generates queries for you", "Only works with MongoDB", "Runs migrations automatically"],
                1,
                "An ORM gives you typed model objects and a query API so you rarely write raw SQL — a productivity win at the cost of some control over generated SQL and raw performance.",
            ),
            _quiz(
                "Why use a connection pool (pg Pool) instead of opening a new connection per query?",
                ["Because Pool is shorter to type", "Connections are expensive to establish; a pool reuses them across requests", "Pools are required by law", "A pool disables SQL"],
                1,
                "Every new database connection costs a network round-trip plus authentication handshake. A pool keeps a set of live connections ready to reuse, which is what keeps an API responsive under concurrent load.",
            ),
        ],
        "exercise": _exercise(
            "Parameterize a login query",
            "Rewrite findUser so the user-supplied email is passed as a bind parameter instead of being interpolated into the SQL string.",
            "const { Pool } = require('pg');\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL });\n\nasync function findUser(email) {\n  const sql = `SELECT * FROM users WHERE email = '${email}'`;\n  const res = await pool.query(sql);\n  return res.rows[0];\n}",
            "const { Pool } = require('pg');\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL });\n\nasync function findUser(email) {\n  const res = await pool.query(\n    'SELECT * FROM users WHERE email = $1',\n    [email]\n  );\n  return res.rows[0];\n}",
            "Pass an array of values as the second argument to pool.query and use $1 as the placeholder — the driver handles escaping, not string concatenation.",
        ),
        "curriculum": ["node"],
    },
]


INTERACTIVES = {
    "node-server": {
        "quiz": [
            _quiz(
                "Which line must appear before your routes so req.body contains parsed JSON?",
                ["app.use(express.static('public'))", "app.use(express.json())", "app.set('view engine', 'ejs')", "app.listen(3000)"],
                1,
                "express.json() is middleware that reads the request body and parses JSON into req.body. Because middleware runs in registration order, it must be registered before the routes that read req.body.",
            ),
            _quiz(
                "What does res.status(201).json(user) do?",
                ["Sets the HTTP status to 201 and sends the user object as JSON", "Redirects to /user", "Sets a cookie", "Logs the user"],
                0,
                "res.status(201) sets the status code to 201 Created, and res.json(user) serializes the object to JSON, sets Content-Type: application/json, and ends the response.",
            ),
            _quiz(
                "You register error-handling middleware before your routes. What goes wrong?",
                ["It works perfectly", "Route errors skip it — error middleware must be registered after routes to catch them", "Express crashes on startup", "It runs for every request twice"],
                1,
                "Express matches handlers in registration order. Error middleware is only reached by a request that fell through, so it must be the last thing registered to catch errors from every route and middleware before it.",
            ),
        ],
        "exercise": _exercise(
            "Health check and echo endpoints",
            "Add a GET /health route that returns JSON { ok: true } and a POST /echo route that returns whatever JSON body was sent.",
            "const express = require('express');\nconst app = express();\napp.use(express.json());\n\napp.get('/', (req, res) => res.send('Welcome'));\n\napp.listen(3000, () => console.log('up on :3000'));",
            "const express = require('express');\nconst app = express();\napp.use(express.json());\n\napp.get('/', (req, res) => res.send('Welcome'));\n\napp.get('/health', (req, res) => res.json({ ok: true }));\n\napp.post('/echo', (req, res) => res.json(req.body));\n\napp.listen(3000, () => console.log('up on :3000'));",
            "Use res.json() — it serializes an object and sets the Content-Type header for you.",
        ),
    },
    "node-files-streams": {
        "quiz": [
            _quiz(
                "Why should a server prefer readFile from 'fs/promises' over readFileSync?",
                ["readFileSync is slower", "readFileSync blocks the event loop while the file is read", "readFile is the only one that works", "readFileSync doesn't return a value"],
                1,
                "readFileSync performs blocking I/O on Node's single JavaScript thread — the whole server stalls while the disk responds. The async version delegates to the OS and resumes when the file is ready.",
            ),
            _quiz(
                "What does this pipeline do: createReadStream('big.log').pipe(createWriteStream('copy.log'))?",
                ["Copies the file in chunks without loading it entirely into memory", "Reads it and logs the contents", "Deletes both files", "Compresses the log"],
                0,
                "A readable stream emits data in chunks, and pipe() wires them straight into the writable stream with backpressure handling. Memory stays flat no matter how large the file is.",
            ),
            _quiz(
                "What best describes Node's event loop?",
                ["A separate thread per request", "A single thread that delegates I/O to the OS and runs callbacks when the call stack is empty", "A queue of microtasks only", "The C++ garbage collector"],
                1,
                "Node runs JavaScript on one thread and hands long-running I/O to the OS; completion callbacks are scheduled onto the loop. That is why synchronous CPU work blocks everything — the loop can't pick up callbacks.",
            ),
        ],
        "exercise": _exercise(
            "Uppercase a file with a Transform stream",
            "Pipe input.txt through a Transform that uppercases each chunk, then write the result to output.txt.",
            "const { createReadStream, createWriteStream } = require('fs');\nconst { Transform } = require('stream');\n\ncreateReadStream('input.txt')\n  .pipe(createWriteStream('output.txt'))\n  .on('finish', () => console.log('done'));",
            "const { createReadStream, createWriteStream } = require('fs');\nconst { Transform } = require('stream');\n\nconst upper = new Transform({\n  transform(chunk, encoding, callback) {\n    this.push(chunk.toString().toUpperCase());\n    callback();\n  }\n});\n\ncreateReadStream('input.txt')\n  .pipe(upper)\n  .pipe(createWriteStream('output.txt'))\n  .on('finish', () => console.log('done'));",
            "Build a Transform whose transform(chunk, encoding, callback) pushes the converted chunk and calls callback() — then pipe the source through it.",
        ),
    },
}
