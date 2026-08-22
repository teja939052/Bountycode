"""HTML & CSS study articles — expansion content for the Study Library.

This module is imported BY app.data.study_materials and therefore must NOT
import from it. It provides:

  NEW_ARTICLES  — six in-depth HTML/CSS articles (forms, specificity,
                  animations/transitions, custom properties, accessibility,
                  responsive images & modern layout).
  INTERACTIVES  — quizzes + exercises added to the four core HTML/CSS
                  articles defined in study_materials (html-basics,
                  css-basics, css-flexbox-grid, css-responsive).
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
        "id": "html-forms",
        "title": "HTML Forms: Inputs, Validation, and Labels",
        "category": "html-css",
        "summary": "Forms are how the web collects data. Master the input types, label pairing, and native validation that turn a janky form into one users can actually fill out — without writing a single line of JavaScript.",
        "level": "beginner",
        "read_time_min": 12,
        "related_topics": ["html-basics", "web-accessibility", "css-basics"],
        "sections": [
            _section(
                "The form element and how browsers submit it",
                "A form is a collection of fields plus a submit action. The action attribute is the URL that receives the data, and method decides how it travels: get appends name=value pairs to the URL as a query string, while post sends them in the request body. Every input must carry a name — without it, its value is simply dropped from the submission.",
                "<form action=\"/search\" method=\"get\">\n  <input type=\"search\" name=\"q\" placeholder=\"Search...\">\n  <button type=\"submit\">Search</button>\n</form>",
            ),
            _section(
                "Input types: choose the right control",
                "The type attribute picks the control AND the browser behavior. type=\"email\" triggers format validation and the @ keypad on mobile; type=\"number\" brings up a numeric keypad; type=\"password\" masks input; checkbox and radio offer choices. Match the type to the data and you get free keyboard, validation, and autofill behavior.",
                "<input type=\"email\" name=\"email\" placeholder=\"you@example.com\">\n<input type=\"number\" name=\"age\" min=\"18\" max=\"120\">\n<input type=\"password\" name=\"password\">\n<input type=\"checkbox\" name=\"newsletter\" checked> Subscribe",
            ),
            _section(
                "Labels: making every field usable",
                "A label explains what a field is for. Pair it with the input using the same id: <label for=\"email\"> matches <input id=\"email\">. Clicking the label focuses the field, and screen readers announce the label when the input is focused. A placeholder is not a label — it disappears while typing and often fails contrast requirements.",
                "<label for=\"email\">Email address</label>\n<input id=\"email\" type=\"email\" name=\"email\" required>",
                "Make every input's label visually permanent. Floated labels are a nice aesthetic, but a visible <label> above or beside each field is the pattern that never hurts usability.",
            ),
            _section(
                "Native validation: required, minlength, pattern",
                "Modern browsers validate forms without JavaScript. required blocks submit on empty fields, minlength/maxlength and min/max bound values, and pattern enforces a regular expression. The :valid and :invalid pseudo-classes let you style the states. None of this replaces server-side validation — it is a UX layer, not a security boundary.",
                "<form>\n  <label for=\"user\">Username</label>\n  <input id=\"user\" name=\"user\" required minlength=\"3\" pattern=\"[a-z0-9_]+\">\n  <button type=\"submit\">Create account</button>\n</form>",
            ),
        ],
        "key_takeaways": [
            "The name attribute is what turns an input into part of the submitted data",
            "Choose the input type that matches the data to get the right keyboard and validation for free",
            "Every input needs a label; pair them with for and id",
            "Client-side validation is convenience, never a security boundary",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "When a form submits with method=\"get\", where does the data go?",
                ["In the response body", "Appended to the URL as a query string", "Stored in a cookie", "In the HTTP request headers"],
                1,
                "GET appends name=value pairs to the URL as a query string (?q=...). POST is the one that puts data in the request body — use it for anything sensitive or large.",
            ),
            _quiz(
                "Which input type gives mobile users a numeric keypad?",
                ["text", "email", "number", "password"],
                2,
                "type=\"number\" signals the browser to show a numeric keypad and to reject non-numeric input. text shows a full keyboard, email shows the @ keypad, and password masks the characters.",
            ),
            _quiz(
                "What is the main reason to pair a <label> with an input using for/id?",
                ["It makes the form submit faster", "Clicking the label focuses the input and screen readers announce it", "It is required for the pattern attribute to work", "It styles the input automatically"],
                1,
                "The for/id pairing links the label to its field: clicking anywhere on the label focuses the input, and assistive technology announces the label text when the field is focused. The other benefits simply do not exist.",
            ),
        ],
        "exercise": _exercise(
            "Build an accessible signup form",
            "Add labels to both fields, set the correct input types, and make email required with a pattern on the username.",
            "<form action=\"/signup\" method=\"post\">\n  Email:\n  <input type=\"text\" name=\"email\">\n  Username:\n  <input type=\"text\" name=\"username\">\n  <button type=\"submit\">Sign up</button>\n</form>",
            "<form action=\"/signup\" method=\"post\">\n  <label for=\"email\">Email</label>\n  <input id=\"email\" type=\"email\" name=\"email\" required>\n  <label for=\"username\">Username</label>\n  <input id=\"username\" type=\"text\" name=\"username\" minlength=\"3\" pattern=\"[a-z0-9_]+\" required>\n  <button type=\"submit\">Sign up</button>\n</form>",
            "Remember that type=\"email\" triggers native validation, and minlength + pattern check the username.",
        ),
        "curriculum": ["html", "css"],
    },
    {
        "id": "css-specificity",
        "title": "CSS Specificity and the Cascade: Who Wins and Why",
        "category": "html-css",
        "summary": "Two rules, one element, one winner. Learn how the cascade resolves conflicts with the specificity formula, why your CSS sometimes \"won't apply\", and how to keep stylesheets overridable instead of a war zone.",
        "level": "advanced",
        "read_time_min": 14,
        "related_topics": ["css-basics", "css-variables", "css-animations-transitions"],
        "sections": [
            _section(
                "The cascade: where conflicting rules meet",
                "The cascade is the algorithm that picks ONE winning declaration when several rules target the same element. It resolves in four passes: origin (user !important beats author beats browser defaults), importance, specificity, then source order. Two identical rules? The last one in the file wins. But specificity always beats recency — a low-specificity rule loses no matter how late it appears.",
                "p { color: blue; }\np { color: red; }\n/* same specificity, so the later rule wins: red */",
            ),
            _section(
                "Counting specificity: (a, b, c)",
                "Specificity is a tuple compared left to right: inline styles, then ids, then classes, attributes, and pseudo-classes, then types and pseudo-elements. A single id beats any number of classes. Write it as (a, b, c): #header .nav a is (1, 1, 1); .nav a:hover is (0, 3, 1) — the id wins despite having more classes.",
                "#header .nav a { color: green; }   /* (1,1,1) */\n.nav a:hover { color: red; }       /* (0,3,1) — loses to the id */",
            ),
            _section(
                "Debugging specificity battles",
                "When a rule \"doesn't apply\", you are almost always losing a specificity battle, not making a typo. DevTools shows the competing rules and names the winner. Raise specificity deliberately — add one class — instead of stacking !important, which re-orders the entire cascade and makes every future override harder.",
                "/* Bumping specificity on purpose: one class turns the tide */\n.nav a { color: gray; }\n.nav a.link-active { color: white; }   /* (0,2,1) beats (0,1,1) */",
                "Before adding !important, open DevTools and read the specificity of the rule you are losing to. One deliberate class usually beats a lifetime of !important.",
            ),
            _section(
                "Inheritance, the universal selector, and :where()",
                "Inheritance is the other way values arrive: color and font cascade down, margin and padding do not. The universal selector * matches everything at specificity 0 — but a matching 0-specificity rule still beats any inherited value. :where() and :is() are modern weapons: :where() always adds 0 specificity, while :is() takes the highest of its arguments.",
                ":where(.card, #special) h2 { color: teal; }   /* (0,0,1) — easy to override */\n:is(.card, #special) h2   { color: navy; }    /* (1,0,1) — takes the #special weight */",
            ),
        ],
        "key_takeaways": [
            "The cascade picks one winner: origin, importance, specificity, then source order",
            "Specificity is (inline, id, class, type) — compare left to right",
            "Most \"why won't my CSS apply\" problems are lost specificity wars",
            "Keep specificity low with classes and :where() so your CSS stays overridable",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "Which selector has the highest specificity?",
                ["div", ".card", "#hero", "nav a"],
                2,
                "An id is worth more than any number of classes or types: #hero scores (1,0,0), while .card scores (0,1,0), and div or nav a score (0,0,1) or (0,0,2).",
            ),
            _quiz(
                "Two rules have identical specificity. Which one wins?",
                ["The one with more declarations", "The one that appears later in source order", "The one using a class", "The one using a pseudo-class"],
                1,
                "When origin, importance, and specificity all tie, the cascade falls through to source order — the rule that appears later in the stylesheet wins.",
            ),
            _quiz(
                "What specificity does the :where() selector add?",
                ["It inherits the highest of its arguments", "0", "1,0,0", "It doubles the specificity"],
                1,
                ":where() is always 0 — its arguments never count. That is exactly why it is great for reset-style defaults you want trivially easy to override later.",
            ),
        ],
        "exercise": _exercise(
            "Win the specificity war",
            "Make the text inside <p class=\"intro\"> red without touching the HTML. The existing rules are fighting you — raise specificity deliberately.",
            "#page p { color: gray; }\n.intro { color: blue; }\n/* Make the intro text red using only CSS */",
            "#page p { color: gray; }\n.intro { color: blue; }\n#page .intro { color: red; }   /* (1,1,0) beats #page p (1,0,1) */",
            "Compare specificity left to right: you need to beat #page p = (1,0,1).",
        ),
        "curriculum": ["html", "css"],
    },
    {
        "id": "css-animations-transitions",
        "title": "CSS Transitions and Animations",
        "category": "html-css",
        "summary": "Motion communicates state — a button that lifts, a card that fades in, a badge that pulses. Learn transitions for state changes and keyframe animations for choreographed sequences, done cheaply and accessibly.",
        "level": "intermediate",
        "read_time_min": 13,
        "related_topics": ["css-basics", "css-variables", "responsive-images-layouts"],
        "sections": [
            _section(
                "Transitions: smooth state changes",
                "A transition animates a property when its value changes — on hover, on focus, or when a class is toggled. Declare it with the property, the duration, and a timing function. The old value and the new value are interpolated across the duration and the browser draws every frame for you.",
                ".button {\n  background: #2563eb;\n  transition: background 200ms ease-in-out, transform 200ms ease;\n}\n.button:hover {\n  background: #1d4ed8;\n  transform: translateY(-2px);\n}",
            ),
            _section(
                "Transform and timing functions",
                "Transform is the star: translate, scale, and rotate run on the compositor and cost almost nothing, while animating layout properties like width, top, or margin triggers reflow on every frame. Timing functions shape the feel — ease starts fast and slows, ease-out lands softly, and a custom cubic-bezier gives total control.",
                ".card {\n  transition: transform 300ms cubic-bezier(0.2, 0.8, 0.2, 1);\n}\n.card:hover { transform: scale(1.03); }",
            ),
            _section(
                "@keyframes: multi-step animations",
                "@keyframes defines a sequence with from/to or percentage steps. The animation shorthand reads as name duration timing iteration direction fill-mode. forwards keeps the final frame's styles after the animation ends; infinite repeats forever; alternate plays forward then backward.",
                "@keyframes pulse {\n  0%   { transform: scale(1); }\n  50%  { transform: scale(1.05); }\n  100% { transform: scale(1); }\n}\n.bell {\n  animation: pulse 2s ease-in-out infinite;\n}",
            ),
            _section(
                "Performance and respecting motion preferences",
                "The performance rule: animate transform and opacity only, and let the compositor handle it. And motion is not a requirement — respect users who reduce it. prefers-reduced-motion lets you collapse or disable animations, and animated elements should never carry information that only motion conveys.",
                "@media (prefers-reduced-motion: reduce) {\n  .bell { animation: none; }\n}",
                "If a layout property (top, width, margin) is animating, you are paying for a reflow on every frame. translate/scale/opacity are your friends.",
            ),
        ],
        "key_takeaways": [
            "Transitions smooth state changes; keyframe animations play predefined sequences",
            "Animating transform and opacity is GPU-cheap; layout properties are not",
            "The animation shorthand sets name, duration, timing, iteration, direction, and fill mode",
            "Honor prefers-reduced-motion so motion is an enhancement, not a barrier",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which property moves an element without causing layout reflow?",
                ["top", "margin-left", "transform: translateY()", "width"],
                2,
                "transform happens on the compositor after layout, so it never triggers reflow. top, margin-left, and width all force the browser to re-lay-out the page on every frame — the classic animation jank.",
            ),
            _quiz(
                "What does animation-fill-mode: forwards do?",
                ["Loops the animation forever", "Keeps the final keyframe styles after the animation ends", "Plays the animation backwards", "Delays the start of the animation"],
                1,
                "Without a fill mode the element snaps back to its unanimated styles when the animation finishes. forwards preserves the last keyframe so the ending state sticks.",
            ),
            _quiz(
                "Which media feature lets you respect users who dislike motion?",
                ["@media (max-width: 480px)", "@media (prefers-reduced-motion: reduce)", "@media (hover: none)", "@media (pointer: coarse)"],
                1,
                "prefers-reduced-motion reads the user's system motion setting. The others handle layout width, hover capability, and pointer type — none of them reflect motion preferences.",
            ),
        ],
        "exercise": _exercise(
            "Hover lift and pulse",
            "Add a transition so the button lifts 2px and darkens on hover, then give it a gentle load-in animation using a keyframe.",
            ".button {\n  background: #22c55e;\n  color: white;\n  padding: 12px 24px;\n  border: none;\n  border-radius: 8px;\n}",
            ".button {\n  background: #22c55e;\n  color: white;\n  padding: 12px 24px;\n  border: none;\n  border-radius: 8px;\n  transition: transform 200ms ease, background 200ms ease;\n  animation: pop-in 400ms ease-out both;\n}\n.button:hover {\n  background: #16a34a;\n  transform: translateY(-2px);\n}\n@keyframes pop-in {\n  from { transform: scale(0.9); opacity: 0; }\n  to   { transform: scale(1); opacity: 1; }\n}",
            "transition handles the hover state; a @keyframes block plus the animation property handles the load-in.",
        ),
        "curriculum": ["html", "css"],
    },
    {
        "id": "css-variables",
        "title": "CSS Custom Properties: Theming Without a Framework",
        "category": "html-css",
        "summary": "Custom properties are variables that live in the DOM, cascade, and change at runtime. Swap palettes, theme light and dark, and parameterize components — all without a single preprocessor.",
        "level": "intermediate",
        "read_time_min": 12,
        "related_topics": ["css-basics", "css-responsive", "css-specificity"],
        "sections": [
            _section(
                "Declaring and using custom properties",
                "Declare a custom property with --name and read it with var(--name). Unlike Sass variables, custom properties are real CSS properties: they cascade, inherit, and are resolved at computed-value time, which means JavaScript and media queries can change them on the fly and every consumer updates instantly.",
                ":root {\n  --brand: #2563eb;\n  --radius: 8px;\n}\n.button {\n  background: var(--brand);\n  border-radius: var(--radius);\n}",
            ),
            _section(
                "Scope and inheritance",
                "Because custom properties cascade, declaring --brand on :root makes it visible to the whole document, while declaring it on a subtree overrides it only there. That gives you component-scoped theming for free: redefine the variable on a wrapper and every descendant picks up the new value.",
                ".alert {\n  --brand: #dc2626;   /* overrides --brand inside this subtree */\n}\n.alert .button { background: var(--brand); }",
            ),
            _section(
                "Fallbacks and the invalid-at-computed-value rule",
                "var() takes a fallback: var(--spacing, 16px) uses 16px whenever --spacing is not defined. Custom properties also follow the invalid-at-computed-value rule — a wrong type invalidates only the declaration that uses it, at the moment it is used, without poisoning the rest of the stylesheet.",
                ".card {\n  padding: var(--spacing, 16px);\n  color: var(--text-color, #111);\n}",
                "var(--spacing, 16px) is a safety net: when a theme forgets to define --spacing, the fallback keeps the component looking right instead of collapsing.",
            ),
            _section(
                "Theming light and dark with a single attribute",
                "Theming becomes a single attribute. Define light values on :root, override them under [data-theme=\"dark\"], and flip the attribute on the <html> element from JavaScript. Every element that reads var(--bg) re-themes instantly — no framework, no re-download, no extra stylesheet.",
                ":root { --bg: #fff; --text: #111; }\n[data-theme=\"dark\"] {\n  --bg: #0f172a;\n  --text: #e2e8f0;\n}\nbody {\n  background: var(--bg);\n  color: var(--text);\n  transition: background 200ms, color 200ms;\n}",
            ),
        ],
        "key_takeaways": [
            "Custom properties are runtime CSS variables that cascade and inherit like any property",
            "var(--name, fallback) keeps components resilient to missing theme values",
            "Scoping variables to a subtree gives you local overrides for free",
            "Flip a data-theme attribute to swap entire palettes without a framework",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "How do you declare a CSS custom property?",
                ["$brand: #2563eb;", "var(--brand) = #2563eb;", "--brand: #2563eb;", "@define --brand: #2563eb;"],
                2,
                "Custom properties use the double-dash syntax: --brand: #2563eb;. The $ syntax is Sass, var() is how you read a property, and @define is not a thing.",
            ),
            _quiz(
                "What happens when var(--spacing, 16px) is used and --spacing is never defined?",
                ["The declaration is invalid", "16px is used", "The property is skipped entirely", "It inherits from the parent element"],
                1,
                "The second argument to var() is the fallback: if --spacing is not defined anywhere in scope, the browser uses 16px. That is what makes component CSS resilient.",
            ),
            _quiz(
                "Custom properties declared on :root are visible where?",
                ["Only on the html element itself", "Anywhere in the document, via inheritance", "Only inside other :root rules", "Only when using var() inside :root"],
                1,
                ":root is the top of the document tree, and custom properties inherit like any property. Declaring there makes them readable by every descendant element.",
            ),
        ],
        "exercise": _exercise(
            "Light/dark card theme",
            "Define color variables on :root and a dark override via [data-theme=\"dark\"], then make the card use the variables instead of hard-coded colors.",
            ".card {\n  background: #ffffff;\n  color: #111827;\n  border: 1px solid #e5e7eb;\n}",
            ":root {\n  --card-bg: #ffffff;\n  --card-text: #111827;\n  --card-border: #e5e7eb;\n}\n[data-theme=\"dark\"] {\n  --card-bg: #1f2937;\n  --card-text: #f9fafb;\n  --card-border: #374151;\n}\n.card {\n  background: var(--card-bg);\n  color: var(--card-text);\n  border: 1px solid var(--card-border);\n}",
            "Declare the variables once, then swap only the variable definitions inside the dark block — the .card rule never changes.",
        ),
        "curriculum": ["html", "css"],
    },
    {
        "id": "web-accessibility",
        "title": "Web Accessibility: Semantics, ARIA, and Contrast",
        "category": "html-css",
        "summary": "Around 15% of people live with a disability, and for some the web is the only door in. Write pages that work for keyboards, screen readers, and low-vision users by using semantics first, ARIA second, and readable contrast always.",
        "level": "intermediate",
        "read_time_min": 15,
        "related_topics": ["html-basics", "html-forms", "css-basics"],
        "sections": [
            _section(
                "Accessibility is a requirement, not a nicety",
                "WCAG 2.2 organizes accessibility into four principles: perceivable, operable, understandable, and robust — POUR. Accessibility is not a bolt-on feature. It is a legal requirement in many jurisdictions, and it makes your site faster to use for everyone, including the person navigating with a broken mouse on a crowded bus.",
            ),
            _section(
                "Semantics first, ARIA as a last resort",
                "Native HTML elements ship with roles, keyboard support, and screen-reader announcements for free. A real <button> is focusable, fires on Enter and Space, and announces itself; a <div onclick> does none of that until you rebuild it. Reach for ARIA only when no native element exists — and when you do, aria-label, aria-expanded, and aria-controls communicate names and state.",
                "<!-- Wrong: a div pretending to be a button -->\n<div class=\"tab\" onclick=\"open()\">Open</div>\n\n<!-- Right: a real button with explicit state -->\n<button aria-expanded=\"false\" aria-controls=\"panel\">Open</button>",
            ),
            _section(
                "Keyboard: focus, order, and skip links",
                "Every interactive element must be reachable and operable from the keyboard alone. The tab order follows the DOM order, so structure your markup in reading order. Provide a visible focus ring — never set outline: none without a replacement — and add a skip link so keyboard users can jump past the nav straight to the main content.",
                "a.skip-link {\n  position: absolute;\n  left: -9999px;\n}\na.skip-link:focus {\n  left: 16px;\n  top: 16px;\n}",
                "Never set outline: none without a replacement. The focus ring is how keyboard users see where they are — make it more visible, not less.",
            ),
            _section(
                "Color, contrast, and not relying on color alone",
                "Contrast is math: WCAG AA wants 4.5:1 for normal text, 3:1 for large text and UI components, and 1.5:1 for meaningful graphics. And never use color as the only signal — a required-field error should show an icon or helper text, not just turn red.",
                ".error-text { color: #b91c1c; }\ninput:invalid { border-color: #b91c1c; }\ninput:invalid + .error-hint { display: block; }   /* text hint, not color alone */",
            ),
        ],
        "key_takeaways": [
            "WCAG success criteria cluster around POUR: perceivable, operable, understandable, robust",
            "Native elements beat ARIA — use a real <button> before role=\"button\"",
            "Everything interactive must be keyboard-reachable with a visible focus ring",
            "Text needs 4.5:1 contrast, and meaning must never depend on color alone",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "Which is the best approach for an accessible button?",
                ["<div onclick> with role=\"button\"", "A native <button> element", "<span> with a click handler", "<a> without href"],
                1,
                "A native <button> gets keyboard focus, Enter/Space activation, and the correct role announced — all for free. Every other option means rebuilding that behavior by hand.",
            ),
            _quiz(
                "What contrast ratio does WCAG AA require for normal-size text?",
                ["2:1", "3:1", "4.5:1", "7:1"],
                2,
                "AA demands 4.5:1 for normal text and 3:1 for large text and UI components. The 7:1 figure belongs to the stricter AAA level, and 2:1 is far too low for text.",
            ),
            _quiz(
                "Why should you avoid setting outline: none on :focus?",
                ["It slows down the browser", "It removes the only visible indication of keyboard focus", "It breaks the cascade", "It is deprecated syntax"],
                1,
                "The focus outline is how keyboard and assistive-tech users track where they are on the page. Removing it without adding a visible alternative strands exactly the users accessibility is meant to protect.",
            ),
        ],
        "exercise": _exercise(
            "Make a search form accessible",
            "Give the input a label, keep the submit button native, and add a strong visible focus style so keyboard users always know where they are.",
            "<form>\n  <input type=\"search\" placeholder=\"Search...\">\n  <button type=\"submit\">Go</button>\n</form>",
            "<form>\n  <label for=\"search\">Search</label>\n  <input id=\"search\" type=\"search\" name=\"q\" placeholder=\"Search...\">\n  <button type=\"submit\">Go</button>\n</form>\n\ninput:focus {\n  outline: 3px solid #2563eb;\n  outline-offset: 2px;\n}",
            "A label pairs via for=\"search\" and id=\"search\"; a strong focus outline keeps the ring visible without resorting to outline: none.",
        ),
        "curriculum": ["html", "css"],
    },
    {
        "id": "responsive-images-layouts",
        "title": "Responsive Images and Modern Layout Techniques",
        "category": "html-css",
        "summary": "Serving a 2MB desktop hero to a phone is a sin. Learn srcset, the picture element, container queries, and the auto-fit/clamp toolkit that make images and layouts adapt to the device — and to the component — without breaking a sweat.",
        "level": "advanced",
        "read_time_min": 15,
        "related_topics": ["css-responsive", "css-flexbox-grid", "css-variables"],
        "sections": [
            _section(
                "srcset and sizes: let the browser choose",
                "srcset gives the browser a menu of candidates and sizes tells it how wide the image will actually render. The browser downloads the smallest candidate that still looks sharp — a phone on slow LTE gets the 400w file, a retina laptop gets 1600w. No JavaScript, no user-agent sniffing.",
                "<img\n  src=\"photo-800.jpg\"\n  srcset=\"photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w\"\n  sizes=\"(min-width: 1200px) 800px, (min-width: 600px) 50vw, 100vw\"\n  alt=\"A mountain lake at sunrise\">",
            ),
            _section(
                "The picture element: art direction",
                "srcset switches resolution; picture switches the image entirely — a different crop, a different aspect ratio, different art. Each source matches a media query and the browser uses the first match. The <img> fallback is mandatory: old browsers, assistive tech, and lazy loading all depend on it.",
                "<picture>\n  <source media=\"(min-width: 800px)\" srcset=\"hero-wide.webp\">\n  <source media=\"(min-width: 400px)\" srcset=\"hero-tablet.webp\">\n  <img src=\"hero-mobile.jpg\" alt=\"Team collaborating in a workshop\">\n</picture>",
            ),
            _section(
                "Container queries: respond to the component",
                "Container queries let a component respond to its own container instead of the viewport — the difference between a card that works in a sidebar and one tuned to the whole page. Declare container-type: inline-size on the parent and write media-style @container queries against it.",
                ".product-card {\n  container-type: inline-size;\n}\n@container (min-width: 400px) {\n  .product-card { display: flex; }\n}",
                "Declare @container-type: inline-size on the parent and write @container (min-width: ...) queries against it — component libraries become viewport-independent.",
            ),
            _section(
                "Modern layout: auto-fit, clamp, and subgrid",
                "The modern toolbox is mostly query-free: repeat(auto-fit, minmax(220px, 1fr)) creates as many tracks as fit and stretches the last row; clamp() makes type fluid between hard bounds; subgrid aligns nested grids to their parent's tracks. Write these and most breakpoints take care of themselves.",
                ".gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));\n  gap: 1rem;\n}\n.card-title {\n  font-size: clamp(1rem, 0.8rem + 1.2vw, 1.5rem);\n}",
            ),
        ],
        "key_takeaways": [
            "srcset + sizes hand the browser width-based candidates; picture handles art direction",
            "Always keep the <img> fallback inside <picture> so everything degrades gracefully",
            "Container queries make reusable components respond to their own width",
            "auto-fit + minmax + clamp replaces most hand-written media queries",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "What problem does the picture element solve that srcset does not?",
                ["Resolution switching", "Art direction — different crops per breakpoint", "Compression", "Lazy loading"],
                1,
                "srcset picks a different SIZE of the same image; picture picks a different IMAGE entirely, letting you serve a portrait crop on mobile and a wide crop on desktop.",
            ),
            _quiz(
                "In srcset=\"photo-400.jpg 400w\", what does 400w mean?",
                ["400 pixels per inch", "The image is intended for a 400px-wide rendering slot", "A 400 kilobyte file size", "A 400 millisecond load target"],
                1,
                "The w descriptor is the image's intrinsic width in pixels, matched against the sizes attribute. The browser uses both to pick the smallest candidate that fills the slot sharply.",
            ),
            _quiz(
                "What does @container (min-width: 400px) respond to?",
                ["The viewport width", "The width of the nearest container with container-type set", "The width of the image", "The browser window size"],
                1,
                "Container queries measure the nearest ancestor that declares container-type: inline-size — not the viewport. That is what makes a component reusable in any context.",
            ),
        ],
        "exercise": _exercise(
            "Self-balancing product grid",
            "Build a grid that shows one column on phones and balances into as many columns as fit as space grows, using auto-fit and minmax.",
            ".product-grid {\n  display: grid;\n  gap: 1rem;\n}",
            ".product-grid {\n  display: grid;\n  gap: 1rem;\n  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));\n}",
            "repeat(auto-fit, minmax(220px, 1fr)) creates as many 220px-or-wider tracks as fit and makes the last row stretch to fill.",
        ),
        "curriculum": ["html", "css"],
    },
]

INTERACTIVES = {
    "html-basics": {
        "quiz": [
            _quiz(
                "What does the <!DOCTYPE html> declaration tell the browser?",
                ["Which CSS file to load", "To render in standards mode rather than quirks mode", "The language of the page", "The title of the page"],
                1,
                "The doctype is a legacy switch: it puts the browser into standards mode so the page renders predictably, instead of quirks mode with buggy 90s behaviors.",
            ),
            _quiz(
                "Which tag best describes self-contained content like a blog post?",
                ["<section>", "<div>", "<article>", "<aside>"],
                2,
                "<article> means \"independently distributable content\" — a blog post, comment, or news item. <section> groups related content, <aside> is tangential, and <div> has no meaning at all.",
            ),
            _quiz(
                "Which attribute on an <img> is read aloud by screen readers and shown if the image fails to load?",
                ["src", "title", "alt", "loading"],
                2,
                "alt is the text alternative: assistive tech announces it and browsers display it when the image breaks. src is the file location and title is a hover tooltip, not a substitute.",
            ),
        ],
        "exercise": _exercise(
            "Add semantic structure",
            "Replace the div soup with semantic tags so the page structure is announced correctly to assistive tech and search engines.",
            "<div>\n  <div>Home About Contact</div>\n  <div>\n    <div>\n      <div>Post title</div>\n      <div>Post body...</div>\n    </div>\n  </div>\n  <div>&copy; 2026</div>\n</div>",
            "<nav>\n  <a href=\"/\">Home</a>\n  <a href=\"/about\">About</a>\n  <a href=\"/contact\">Contact</a>\n</nav>\n<main>\n  <article>\n    <h2>Post title</h2>\n    <p>Post body...</p>\n  </article>\n</main>\n<footer>&copy; 2026</footer>",
            "Use nav for the links, main for the content, article for the self-contained post, and h2/p instead of nested divs.",
        ),
    },
    "css-basics": {
        "quiz": [
            _quiz(
                "With the default content-box sizing, width: 200px plus padding: 20px renders how wide in total?",
                ["200px", "220px", "240px", "180px"],
                2,
                "content-box adds padding and border on top of the declared width: 200 + 20 left + 20 right = 240px. With box-sizing: border-box the total stays 200px — which is why the reset is everywhere.",
            ),
            _quiz(
                "Which selector has the highest specificity?",
                ["p", ".note", "#hero", "*"],
                2,
                "An id scores (1,0,0), a class (0,1,0), a type (0,0,1), and the universal selector * scores a flat 0. #hero wins outright.",
            ),
            _quiz(
                "Which of these properties typically inherits down the DOM tree?",
                ["margin", "padding", "color", "border"],
                2,
                "color, font-family, and line-height inherit; margin, padding, and border are box properties that each element owns. That is why setting body { color: ... } tints everything but margins do not stack up.",
            ),
        ],
        "exercise": _exercise(
            "Center a card with the box model",
            "Add a border-box reset, give the card padding inside and margin outside, and center it horizontally in its parent.",
            ".card {\n  width: 320px;\n  border: 1px solid #ddd;\n}",
            "* {\n  box-sizing: border-box;\n}\n\n.card {\n  width: 320px;\n  padding: 24px;\n  margin: 24px auto;\n  border: 1px solid #ddd;\n}",
            "box-sizing: border-box keeps the total at 320px; margin: 24px auto centers the card horizontally.",
        ),
    },
    "css-flexbox-grid": {
        "quiz": [
            _quiz(
                "Which rule makes a container lay its children out in a row?",
                ["display: block", "display: inline", "display: flex", "float: left"],
                2,
                "display: flex creates a flex container whose direct children become flex items laid out along the main axis — a row by default. Floats are a legacy hack, and block/inline do not re-layout children.",
            ),
            _quiz(
                "Which property aligns items on the MAIN axis of a flex container?",
                ["align-items", "justify-content", "text-align", "align-self"],
                1,
                "justify-content works on the main axis (flex-direction), align-items on the cross axis. align-self overrides alignment for one item; text-align has nothing to do with flex.",
            ),
            _quiz(
                "When should you choose grid over flexbox?",
                ["For a single row of buttons", "When you need to align items on the cross axis", "For layouts that span both rows and columns together", "Whenever you need gap between items"],
                2,
                "Grid is two-dimensional: it defines rows AND columns in one layout. Flexbox is one-dimensional — a single row or a single column. The moment both axes matter, reach for grid.",
            ),
        ],
        "exercise": _exercise(
            "Navbar with flex",
            "Make the navbar a flex row with the links spaced apart and vertically centered.",
            ".navbar {\n  padding: 12px 16px;\n  background: #1e293b;\n  color: white;\n}",
            ".navbar {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  gap: 16px;\n  padding: 12px 16px;\n  background: #1e293b;\n  color: white;\n}",
            "display: flex creates the row, justify-content: space-between pushes the ends apart, and align-items: center centers vertically.",
        ),
    },
    "css-responsive": {
        "quiz": [
            _quiz(
                "What is the mobile-first pattern?",
                ["Write desktop CSS, then remove it with max-width queries", "Write base CSS for small screens, then enhance with min-width queries", "Write only desktop CSS and let the browser shrink it", "Duplicate every rule inside a media query"],
                1,
                "Mobile-first starts with the base styles for the smallest screen and layers enhancements on with min-width queries. It keeps the core fast and never fights to \"undo\" desktop styles.",
            ),
            _quiz(
                "What does clamp(1rem, 2vw, 3rem) guarantee?",
                ["It always equals exactly 2vw", "The value never goes below 1rem or above 3rem", "It rounds to the nearest pixel", "It only applies on mobile devices"],
                1,
                "clamp(MIN, PREFERRED, MAX) clamps the preferred vw value between a hard minimum and maximum. Between 1rem and 3rem the size scales fluidly with the viewport.",
            ),
            _quiz(
                "Which CSS keeps an image from overflowing its container?",
                ["width: 100%; height: auto", "width: auto; height: 100%", "max-width: none", "overflow: hidden on the img itself"],
                0,
                "width: 100% caps the image at its container and height: auto preserves the aspect ratio. The others either ignore the container or hide parts of the picture.",
            ),
        ],
        "exercise": _exercise(
            "Fluid card grid",
            "Give the grid a responsive layout: one column on phones, three columns on wider screens.",
            ".cards {\n  display: grid;\n  gap: 16px;\n}",
            ".cards {\n  display: grid;\n  grid-template-columns: 1fr;\n  gap: 16px;\n}\n\n@media (min-width: 768px) {\n  .cards {\n    grid-template-columns: repeat(3, 1fr);\n  }\n}",
            "Start with a single column as the base, then switch to repeat(3, 1fr) inside a min-width: 768px media query.",
        ),
    },
}
