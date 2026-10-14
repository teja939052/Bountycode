// @ts-nocheck
/**
 * Mission content registry (ADR: BOUNTYCODE_CURRICULUM_STRUCTURE).
 *
 * Schema (Phase 0 — one canonical curriculum grammar):
 *
 *   CANONICAL STAGE (backend STEP_TYPES)
 *      discover | manipulate | predict | build | break | debug | retrieve | transfer | mastery
 *
 *   Composition chrome (not teaching stages):
 *      intro | practice | recognize (→ predict) | prove (→ mastery / timed_prove)
 *
 *   INTERACTION SUBTYPE (stage.interaction.kind) — never a top-level step type:
 *      visual_hook, micro_animation, state_trace, drag_or_manipulate, tap_to_reveal,
 *      predict_output, multiple_choice_reasoning, change_one_thing, fill_in_blank,
 *      code_reorder, tiny_build, interactive_diagram, match_relationships, sort_steps,
 *      parameter_slider, before_after, break_and_debug, error_hunt, explain_the_bug,
 *      recall_check, srs_card, transfer_problem, timed_prove
 *
 * Content rules: every code sample hand-traced; every MCQ answer verified;
 * skill ids canonical (domain.subskill). Add content, never pages.
 */

export interface MissionMCQ {
  id: string;
  q: string;
  code?: string;
  options: string[];
  correct: number;
  explain: string;
  codeIfMissed: string;
}

/** Canonical teaching stages from backend STEP_TYPES (lesson_definitions.py). */
export type CanonicalStageType =
  | "discover"
  | "manipulate"
  | "predict"
  | "build"
  | "break"
  | "debug"
  | "retrieve"
  | "transfer"
  | "mastery";

/** Mission chrome + legacy aliases. prove ≡ mastery; recognize ≡ predict. */
export type CompositionStageType = "intro" | "practice" | "recognize" | "prove";

export type MissionStageKind = CanonicalStageType | CompositionStageType;

/**
 * Interaction subtypes under a canonical stage.
 * Maps to MissionExperience InteractionHost → existing widgets.
 */
export type InteractionKind =
  | "visual_hook"
  | "micro_animation"
  | "state_trace"
  | "drag_or_manipulate"
  | "change_one_thing"
  | "parameter_slider"
  | "interactive_diagram"
  | "match_relationships"
  | "tap_to_reveal"
  | "predict_output"
  | "multiple_choice_reasoning"
  | "before_after"
  | "sort_steps"
  | "fill_in_blank"
  | "code_reorder"
  | "tiny_build"
  | "break_and_debug"
  | "error_hunt"
  | "explain_the_bug"
  | "explain_aloud"
  | "recall_check"
  | "srs_card"
  | "transfer_problem"
  | "timed_prove"
  | "pattern_tracer"
  | "code_fill"
  | "algorithm_tracer"
  | "pattern_quiz";

export interface StageInteraction {
  kind: InteractionKind;
  /** Freeform renderer payload (code, options, steps, keywords, …). */
  config?: Record<string, unknown>;
  /** Flat fields also allowed for compact content authoring. */
  [key: string]: unknown;
}

export interface MissionStage {
  kind: MissionStageKind;
  title?: string;
  subtitle?: string;
  /** Canonical stage override (preferred over kind for new content). */
  type?: CanonicalStageType;
  /** Interaction subtype beneath the canonical stage. */
  interaction?: StageInteraction;
  /** Legacy component embed (Discover/Manipulate/Build). */
  component?: "ExplainAloud" | "PatternTracer" | "CodeFillInTheBlank";
  judgeTo?: string;
  judgeLabel?: string;
  sequence?: Array<{ level: string; items: Array<{ label: string; to: string }> }>;
  mcqs?: MissionMCQ[];
  timeLimitSeconds?: number;
  passScore?: number;
}

export interface MissionContent {
  id: string;
  title: string;
  briefing: string;
  /** Why this mission matters for the learner right now. */
  why?: string;
  skillId: string;
  estimatedMinutes: number;
  stages: MissionStage[];
  /** Optional tags for journey/company relevance (never fabricated claims). */
  tags?: string[];
}

/** Six flagship lessons — content only, one renderer. */
export const FLAGSHIP_MISSION_IDS = [
  "trace_variables",
  "for_loops",
  "percentages",
  "blood_relations",
  "two_pointers",
  "sql_joins",
  "email_format",
  "sliding_window_001",
] as const;

export const MISSIONS: Record<string, MissionContent> = {
  // ─────────────────────────────────────────────────────────────
  // 1. TRACE VARIABLES — gold-standard reference for the renderer
  // ─────────────────────────────────────────────────────────────
  trace_variables: {
    id: "trace_variables",
    title: "Trace Variables",
    briefing:
      "A variable is a named box. Assignment stores a value; reassignment overwrites it. Trace the boxes line by line — the program only knows what the last store left behind.",
    why:
      "Programming Logic is one of the highest-weight screening sections for service-company assessments. If you can trace state accurately, you will cut careless errors in timed coding and aptitude questions.",
    skillId: "coding.variables",
    estimatedMinutes: 16,
    tags: ["foundations", "world1"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~16 minutes." },
      {
        kind: "discover",
        title: "Discover — see the boxes",
        subtitle: "Assignment is a store, not a math equals. Look at what each line leaves in memory.",
        interaction: {
          kind: "visual_hook",
          visual: "x = 5     →  [x | 5]\ny = x     →  [y | 5]  [x | 5]\nx = 10    →  [y | 5]  [x | 10]",
          caption: "y copied the value 5 when x was 5. Later x=10 does not update y.",
        },
        mcqs: [
          {
            id: "discover",
            q: "After x = 5; y = x; x = 10 — what does y hold?",
            options: ["5", "10", "15", "undefined"],
            correct: 0,
            explain:
              "y stored the value 5 at assignment time. Reassigning x does not write through to y — boxes hold values, not links (for ints).",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One shared mechanism. Name it before you touch code.",
        interaction: {
          kind: "pattern_quiz",
          questions: [
            {
              id: "r1",
              problemStatement: "x=5; y=x; x=10 leaves y at 5. Swapping a and b needs a temp. total=0 mid-loop wipes the sum. What single mechanism explains all three?",
              options: [
                "Assignment copies the current value — later rebinding never rewrites earlier copies",
                "Python runs lines bottom-to-top when confused",
                "All variables are global by default",
                "print() freezes values at first use",
              ],
              correctIndex: 0,
              explanation: "Store-timing is the shape: each assignment snapshots a value. y kept 5, swap needs a temp holder, and reset-to-0 discards the snapshot.",
              pattern: "trace-variables",
            },
          ],
        },
        mcqs: [
          {
            id: "recognize",
            q: "x=5; y=x; x=10 leaves y at 5. Swapping a and b needs a temp. total=0 mid-loop wipes the sum. What single mechanism explains all three?",
            options: [
              "Assignment copies the current value — later rebinding never rewrites earlier copies",
              "Python runs lines bottom-to-top when confused",
              "All variables are global by default",
              "print() freezes values at first use",
            ],
            correct: 0,
            explain:
              "Store-timing is the shape: each assignment snapshots a value. y kept 5, swap needs a temp holder, and reset-to-0 discards the snapshot.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — step the state",
        subtitle: "Walk each line. Watch which box changes and which stays.",
        interaction: {
          kind: "state_trace",
          title: "Variable state trace",
          steps: [
            {
              step: 1,
              description: "x = 5 — create box x, store 5",
              array: [5, 0, 0],
              pointers: { i: 0 },
              highlight: [0],
              variables: { x: 5, y: "—" },
            },
            {
              step: 2,
              description: "y = x — read x (5), create box y, store 5",
              array: [5, 5, 0],
              pointers: { i: 1 },
              highlight: [0, 1],
              variables: { x: 5, y: 5 },
            },
            {
              step: 3,
              description: "x = 10 — overwrite box x with 10; y is untouched",
              array: [10, 5, 0],
              pointers: { i: 0 },
              highlight: [0],
              variables: { x: 10, y: 5 },
            },
          ],
        },
      },
      {
        kind: "predict",
        title: "Change one thing — what survives?",
        subtitle: "Reassign x to a new value. Watch what y keeps.",
        interaction: {
          kind: "change_one_thing",
          label: "Reassign x to",
          min: 0,
          max: 20,
          step: 1,
          target: 10,
          unit: "",
          formula: "y stays 5 — y copied x when x was 5",
          initial: 6,
        },
        mcqs: [
          {
            id: "change",
            q: "x = 5; y = x; x = 10. What does y hold?",
            options: ["5", "10", "15", "undefined"],
            correct: 0,
            explain: "y snapped the value 5 before x was overwritten to 10.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "predict",
        title: "Predict — no running it first",
        subtitle: "Commit to an answer before you check.",
        interaction: {
          kind: "predict_output",
          questions: [
            {
              id: "tv-p1",
              code: "a = 3\nb = a\na = a + 4\nprint(a, b)",
              options: ["7 3", "7 7", "3 3", "4 3"],
              correctIndex: 0,
              explanation: "b kept 3; a became 3+4=7.",
              language: "python",
            },
          ],
        },
        mcqs: [
          {
            id: "predict",
            q: "a = 3; b = a; a = a + 4. print(a, b) → ?",
            code: "a = 3\nb = a\na = a + 4\nprint(a, b)",
            options: ["7 3", "7 7", "3 3", "4 3"],
            correct: 0,
            explain: "b copied 3 when assigned; a was then overwritten to 7.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — fill the store",
        subtitle: "Complete the assignment sequence. Then open the judge if you want hidden tests.",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "score = 0\nscore = {blank:inc}\nbonus = score\nscore = {blank:final}\n# bonus is still ____",
          blanks: [
            { id: "inc", placeholder: "line", correctAnswer: "score + 10", hint: "Add 10 to score", width: 140 },
            { id: "final", placeholder: "line", correctAnswer: "score + 5", hint: "Add 5 more after bonus was copied", width: 140 },
          ],
          explanation: "bonus copied score after +10 (so bonus=10). Later score+5 does not change bonus.",
          language: "python",
        },
        judgeTo: "/lesson/things-1",
        judgeLabel: "Open Variables lesson",
      },
      {
        kind: "practice",
        title: "Practice — a sequenced set, not 50 random",
        subtitle: "Copy-timing → accumulators → references. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — copy timing",
            items: [
              { label: "Variables lesson drills · easy", to: "/lesson/things-1" },
              { label: "Swap / temp-holder reps · easy", to: "/question-bank?topic=variables" },
            ],
          },
          {
            level: "Level 2 — accumulators",
            items: [
              { label: "Running-total variants · easy", to: "/question-bank?topic=variables" },
            ],
          },
          {
            level: "Level 3 — references",
            items: [
              { label: "List aliasing vs copying · medium", to: "/question-bank" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — poison the box",
        subtitle: "This code prints the wrong total. What broke?",
        interaction: { kind: "error_hunt" },
        mcqs: [
          {
            id: "break",
            q: "total is 0 but should be 15. What broke?",
            code: "total = 0\ntotal = total + 10\ntotal = 0\ntotal = total + 5\nprint(total)  # prints 5",
            options: [
              "total + 10 never ran",
              "total = 0 resets the accumulated value — overwriting wipes the +10",
              "print is broken",
              "strings vs ints",
            ],
            correct: 1,
            explain:
              "Reassignment to 0 discards the previous total. Accumulators must read-modify-write, not reset.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        title: "Debug — explain the bug",
        subtitle: "Name the fix in your own words (keyword match, not a speech grade).",
        interaction: {
          kind: "explain_the_bug",
          skillId: "coding.variables",
          keywords: ["accumulate", "reset", "overwrite", "total", "keep"],
          title: "Why did total become 5 instead of 15?",
          prompt: "Type the diagnosis: what line wiped the earlier value, and what should replace it?",
          pattern: "trace-variables",
        },
        mcqs: [
          {
            id: "debug",
            q: "Which line keeps the running total?",
            options: [
              "total = 0",
              "total = total + 10  (and never reset total to 0 mid-sequence)",
              "print(total)",
              "bonus = score",
            ],
            correct: 1,
            explain: "Accumulate with total = total + delta; do not reset total to 0 between adds.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        title: "Retrieve — no notes",
        subtitle: "Recall from memory before you peek.",
        interaction: {
          kind: "recall_check",
          prompt: "Without scrolling: what are the three parts of an assignment statement?",
          answer: "name (left) · = (store) · value (right) — e.g. apples = 5",
        },
        mcqs: [
          {
            id: "retrieve",
            q: "Assignment (=) in Python means…",
            options: [
              "mathematical equality",
              "store the right-hand value in the left-hand name",
              "compare two boxes",
              "print the value",
            ],
            correct: 1,
            explain: "In code, = stores; == compares.",
            codeIfMissed: "KNOWLEDGE_RECALL",
          },
        ],
      },
      {
        kind: "transfer",
        title: "Transfer — new disguise",
        subtitle: "Same mental model, unfamiliar surface.",
        mcqs: [
          {
            id: "transfer",
            q: "cart_total = 100; discount = cart_total; cart_total = cart_total - 20. discount is…",
            options: ["80", "100", "120", "20"],
            correct: 1,
            explain: "discount copied 100 before cart_total was reduced.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass. Timeout submits automatically.",
        interaction: { kind: "timed_prove" },
        timeLimitSeconds: 180,
        passScore: 60,
        mcqs: [
          {
            id: "prove-1",
            q: "x = 1; y = x; x = 2. y = ?",
            options: ["1", "2", "3", "undefined"],
            correct: 0,
            explain: "y stored 1 before x was overwritten.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "prove-2",
            q: "Which pattern accumulates a running sum?",
            options: [
              "s = 0 then s = 0 each loop",
              "s = 0 then s = s + item each loop",
              "sum = item only",
              "print(s)",
            ],
            correct: 1,
            explain: "Read-modify-write without resetting the accumulator.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
          {
            id: "prove-3",
            q: "After a = [1]; b = a; a.append(2) — b is…",
            options: ["[1]", "[1, 2]", "[2]", "error"],
            correct: 1,
            explain: "Lists are references: b and a name the same box until rebound.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 2. PERCENTAGES
  // ─────────────────────────────────────────────────────────────
  percentages: {
    id: "percentages",
    title: "Percentages",
    briefing:
      "Percent means per hundred. Percentage change is always (change / original) × 100 — the base is the 'old' value. Successive changes compound: a% then b% → net = a + b + ab/100.",
    why:
      "Aptitude is unavoidable in service-company screening. Percentages appear in every major assessment, and mastering the base-anchor rule prevents the most common careless errors.",
    skillId: "aptitude.quantitative",
    estimatedMinutes: 14,
    tags: ["aptitude", "quantitative"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~14 minutes." },
      {
        kind: "discover",
        title: "Discover — part out of 100",
        subtitle: "See the base, then the share.",
        interaction: {
          kind: "visual_hook",
          visual: "40,000  ──×15%──►  +6,000  ──►  46,000\nbase (old)          change      new",
          caption: "Change ÷ original × 100 = percent change.",
        },
        mcqs: [
          {
            id: "discover",
            q: "25% of 80 = ?",
            options: ["20", "25", "40", "16"],
            correct: 0,
            explain: "25/100 × 80 = 20. Quarter of 80.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One shared mechanism. Name it before you compute.",
        mcqs: [
          {
            id: "recognize",
            q: "40,000→46,000 is +15%. +10% then −10% is −1%, not 0. 20% off then 10% off is 28% off. What single idea explains all three?",
            options: [
              "Every percent is anchored to a base — change the base, change the meaning",
              "Percentages always add up directly",
              "Discounts compound by simple addition",
              "Always round to the nearest 5%",
            ],
            correct: 0,
            explain:
              "The base is the shape: change÷original×100. Second changes act on the new base, so +10/−10 and stacked discounts never simply add.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — move the rate",
        subtitle: "Slide the percent; watch the absolute change follow the base.",
        interaction: {
          kind: "parameter_slider",
          label: "Percent of 200",
          min: 0,
          max: 100,
          step: 5,
          target: 40,
          unit: "%",
          formula: "→ {v}% of 200 = {(v*2)}",
          initial: 10,
        },
      },
      {
        kind: "predict",
        title: "Predict — commit first",
        subtitle: "Salary 40,000 → 46,000. Percent increase?",
        interaction: {
          kind: "before_after",
          before: "old = 40000\nnew = 46000",
          after: "change = 6000\npct = change/old*100",
          note: "6000/40000 = 0.15 → 15%.",
        },
        mcqs: [
          {
            id: "predict",
            q: "₹40,000 → ₹46,000 is a rise of…",
            options: ["15%", "6%", "20%", "10%"],
            correct: 0,
            explain: "(46000−40000)/40000 × 100 = 15%.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — successive change",
        subtitle: "Fill the net formula for +10% then −10%.",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "a, b = 10, -10\nnet = a + b + {blank:term}\n# net = -1  (not 0!)",
          blanks: [
            {
              id: "term",
              placeholder: "cross term",
              correctAnswer: "(a*b)/100",
              hint: "a×b/100",
              width: 160,
            },
          ],
          explanation: "10 + (−10) + (10×−10)/100 = 0 − 1 = −1%. Order matters on the same base.",
          language: "python",
        },
        judgeTo: "/aptitude?topic=percentages",
        judgeLabel: "Drill percentages",
      },
      {
        kind: "practice",
        title: "Practice — a sequenced set, not 50 random",
        subtitle: "Base discipline → successive change → mixed words. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — base discipline",
            items: [
              { label: "Percent-of drills · easy", to: "/aptitude?topic=percentages" },
              { label: "Change-over-original reps · easy", to: "/aptitude?topic=percentages" },
            ],
          },
          {
            level: "Level 2 — successive change",
            items: [
              { label: "a% then b% compounding · medium", to: "/aptitude?topic=percentages" },
            ],
          },
          {
            level: "Level 3 — mixed words",
            items: [
              { label: "Discount / growth word problems · medium", to: "/aptitude" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — wrong base",
        subtitle: "This '15%' answer is wrong. What broke?",
        mcqs: [
          {
            id: "break",
            q: "Price 100 → 120 → 100. Student says net 0%. What broke?",
            options: [
              "Arithmetic is fine",
              "Percent bases differ: +20% on 100, then −16.67% on 120 — net not 0% on wealth",
              "Need multiplication only",
              "None — 0% is correct",
            ],
            correct: 1,
            explain:
              "100→120 is +20% of 100; 120→100 is −20/120 ≈ −16.67% of 120. Successive net on original is −0% only if you misuse the same base.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        title: "Debug — explain the base error",
        interaction: {
          kind: "explain_the_bug",
          skillId: "aptitude.quantitative",
          keywords: ["base", "original", "old", "percent", "change"],
          title: "Why must the denominator be the original?",
          prompt: "Type why change must be divided by the OLD value, not the new value.",
          pattern: "percentages",
        },
        mcqs: [
          {
            id: "debug",
            q: "Correct percent change formula uses…",
            options: [
              "change / new × 100",
              "change / original × 100",
              "new / change × 100",
              "original / change × 100",
            ],
            correct: 1,
            explain: "Base is the starting (old) quantity.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        title: "Retrieve — fraction table",
        interaction: {
          kind: "recall_check",
          prompt: "Recall: 1/8 as a percent?",
          answer: "12.5%  (also: 1/2=50%, 1/4=25%, 1/5=20%, 1/10=10%)",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — successive discounts",
        mcqs: [
          {
            id: "transfer",
            q: "20% off then 10% off on same price list → net discount?",
            options: ["30%", "28%", "25%", "18%"],
            correct: 1,
            explain: "Successive a=−20, b=−10: net = −20−10+(200/100)= −28%.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "p1",
            q: "15% of 240?",
            options: ["36", "30", "40", "24"],
            correct: 0,
            explain: "0.15 × 240 = 36.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "p2",
            q: "Population 800 → 1000. % increase?",
            options: ["25%", "20%", "80%", "12.5%"],
            correct: 0,
            explain: "200/800 × 100 = 25%.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "p3",
            q: "+5% then +5% on 100 → final?",
            options: ["110", "110.25", "110.5", "105"],
            correct: 1,
            explain: "100×1.05×1.05 = 110.25 (net +10.25%).",
            codeIfMissed: "COMPLEXITY_ERROR",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 3. BLOOD RELATIONS
  // ─────────────────────────────────────────────────────────────
  blood_relations: {
    id: "blood_relations",
    title: "Blood Relations",
    briefing:
      "Map every person to a family tree: □ male, ○ female, = marriage, | parent→child. Solve from the target person backwards through the clues. 'Only son of X' collapses branches — use it first.",
    why:
      "Logical reasoning is a high-frequency screening section. Blood relations train precise mapping and backwards inference — the same skill used in coding problem statements and system design interviews.",
    skillId: "aptitude.logical",
    estimatedMinutes: 15,
    tags: ["aptitude", "logical"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~15 minutes." },
      {
        kind: "discover",
        title: "Discover — draw the tree",
        subtitle: "A is B's brother; B is C's mother → one clear chain.",
        interaction: {
          kind: "visual_hook",
          visual: "A(□) ── sibling ── B(○)\n                    |\n                   C\nA is C's uncle (brother of mother).",
          caption: "Start at the target (C) and walk each clue as an edge.",
        },
        mcqs: [
          {
            id: "discover",
            q: "A is B's brother. B is C's mother. A is C's…",
            options: ["father", "uncle", "brother", "cousin"],
            correct: 1,
            explain: "B is mother of C; A is brother of B → A is uncle of C.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One shared discipline. Name it before you draw.",
        mcqs: [
          {
            id: "recognize",
            q: "'Only son of X' collapses whole branches. 'Child of Q' never reveals gender. 'P # Q @ R' codes relations as operators. What single discipline handles all three?",
            options: [
              "Treat every clue as a constraint on one tree — apply the strongest constraint first",
              "Guess genders early to prune fast",
              "Always draw marriages before people",
              "Solve each sentence as a separate puzzle",
            ],
            correct: 0,
            explain:
              "Constraints-on-one-tree is the shape: only-* collapses, gender stays unknown until stated, coded operators map to the same edges.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — match clue → edge",
        subtitle: "Pair each phrase with the tree operation it forces.",
        interaction: {
          kind: "match_relationships",
          left: ["brother of X", "mother of X", "only son of X", "wife of X"],
          right: [
            "same parent, □ child",
            "○ → | → child",
            "collapse to single □ child",
            "= marriage edge from □",
          ],
          pairs: [
            ["brother of X", "same parent, □ child"],
            ["mother of X", "○ → | → child"],
            ["only son of X", "collapse to single □ child"],
            ["wife of X", "= marriage edge from □"],
          ],
        },
      },
      {
        kind: "predict",
        title: "Predict — before you draw",
        mcqs: [
          {
            id: "predict",
            q: "Pointing to a photo: 'He is the son of my grandfather's only son.' Speaker is male. Photo is…",
            options: ["brother", "uncle", "cousin", "father"],
            correct: 0,
            explain:
              "Grandfather's only son = speaker's father (or uncle if only-son rule differs — with only son: father). Son of father = brother. Speaker male → brother.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — code the symbols",
        subtitle: "Fill the mapping used by every solution.",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "MALE = '{blank:m}'\nFEMALE = '{blank:f}'\nMARRIAGE = '='\n# P is Q's brother → same parents, P is {blank:r}",
          blanks: [
            { id: "m", placeholder: "symbol", correctAnswer: "□", width: 60 },
            { id: "f", placeholder: "symbol", correctAnswer: "○", width: 60 },
            { id: "r", placeholder: "gender", correctAnswer: "male", width: 80 },
          ],
          explanation: "Standard notation: □ male, ○ female, = marriage, | generation edge.",
          language: "python",
        },
        judgeTo: "/aptitude?topic=blood-relations",
        judgeLabel: "Drill blood relations",
      },
      {
        kind: "practice",
        title: "Practice — a sequenced set, not 50 random",
        subtitle: "Single chains → coded operators → full trees. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — single chains",
            items: [
              { label: "Two-clue chains · easy", to: "/aptitude?topic=blood-relations" },
              { label: "Uncle / aunt / sibling reps · easy", to: "/aptitude?topic=blood-relations" },
            ],
          },
          {
            level: "Level 2 — coded relations",
            items: [
              { label: "# @ $ operator decoding · medium", to: "/aptitude?topic=blood-relations" },
            ],
          },
          {
            level: "Level 3 — full trees",
            items: [
              { label: "Only-son + marriage trees · medium", to: "/aptitude" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — gender assumption",
        mcqs: [
          {
            id: "break",
            q: "'P is the child of Q' — can we know P's gender?",
            options: [
              "Yes, always male",
              "No — statement never gives gender",
              "Yes, always female",
              "Depends on spelling",
            ],
            correct: 1,
            explain: "Never assume gender the statement does not give (audit pitfall).",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        title: "Debug — explain the wrong tree",
        interaction: {
          kind: "explain_the_bug",
          skillId: "aptitude.logical",
          keywords: ["gender", "assume", "clue", "only", "tree"],
          title: "Why did the tree fork wrong?",
          prompt: "Type which clue was misread (gender? only-son? generation?).",
          pattern: "blood-relations",
        },
        mcqs: [
          {
            id: "debug",
            q: "'Only son of X' should…",
            options: [
              "allow multiple sons",
              "collapse X's children to one □",
              "ignore marriage",
              "imply X is female",
            ],
            correct: 1,
            explain: "Only-son collapses branches — apply it first.",
            codeIfMissed: "DEBUGGING",
          },
        ],
      },
      {
        kind: "retrieve",
        interaction: {
          kind: "recall_check",
          prompt: "Recall the four symbols without notes.",
          answer: "□ male · ○ female · = marriage · | parent→child",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — coded relations",
        mcqs: [
          {
            id: "transfer",
            q: "A # B means A is brother of B; A @ B means A is sister of B. P # Q @ R → P is R's…",
            options: ["brother", "sister", "uncle", "aunt"],
            correct: 0,
            explain:
              "P # Q → P brother of Q. Q @ R → Q sister of R. Siblings P and R share parents → P is brother of R.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "b1",
            q: "A is B's brother, B is C's mother. A is C's…",
            options: ["uncle", "father", "brother", "cousin"],
            correct: 0,
            explain: "Uncle — brother of mother.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "b2",
            q: "X is Y's wife; Z is X's brother. Y is Z's…",
            options: ["brother-in-law", "sister-in-law", "uncle", "father"],
            correct: 0,
            explain:
              "X wife of Y → Y spouse of X. Z brother of X → Y is brother-in-law of Z (spouse of sibling).",
            codeIfMissed: "KNOWLEDGE_RECALL",
          },
          {
            id: "b3",
            q: "Drawing order that usually works?",
            options: [
              "Guess genders first",
              "Target person first, apply only-son early",
              "Marriages last always",
              "Ignore 'only'",
            ],
            correct: 1,
            explain: "Start at target; collapse with only-* clues first.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 4. TWO POINTERS
  // ─────────────────────────────────────────────────────────────
  two_pointers: {
    id: "two_pointers",
    title: "Two Pointers",
    briefing:
      "Two pointers walk from opposite ends (or same direction) — O(n) instead of O(n²). When sum > target, move right inward; when sum < target, move left outward. One pass, no nested loops.",
    why:
      "Two pointers is a flagship DSA pattern that appears in almost every coding interview. Mastering it first makes sliding window, three-way partition, and container problems much easier.",
    skillId: "dsa.two_pointers",
    estimatedMinutes: 18,
    tags: ["dsa", "arrays"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~18 minutes." },
      {
        kind: "discover",
        title: "Discover — the mirror hallway",
        subtitle: "Both ends at once: [2, 7, 11, 15], target 9.",
        interaction: {
          kind: "visual_hook",
          visual: "L                 R   2+15=17 > 9 → R--\nL             R      2+11=13 > 9 → R--\nL           R        2+7=9  ✓",
          caption: "Each pair checked at most once → O(n).",
        },
        mcqs: [
          {
            id: "discover",
            q: "Why do both ends walk inward on a sorted array?",
            options: [
              "To sort the array",
              "Monotonic sum: only one direction can fix an overshoot/undershoot",
              "To use O(n²)",
              "Random walk",
            ],
            correct: 1,
            explain: "Sorted order makes sum monotonic in each pointer — greedy inward moves are correct.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One shared movement. Name it before you trace.",
        mcqs: [
          {
            id: "recognize",
            q: "Sorted two-sum walks both ends. Palindrome compares ends inward. Remove-duplicates runs slow/fast. What single shape is hiding underneath?",
            options: [
              "Two positions walk an ordered structure in one pass — no nesting",
              "Always sort the array first, whatever the question",
              "Binary search works on every array problem",
              "Recursion is required for all three",
            ],
            correct: 0,
            explain:
              "Two walkers, one pass: ends-inward on sorted sums and palindromes, slow/fast on dedup. Sortedness (or order) is what makes each step safe.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — step the pointers",
        interaction: {
          kind: "state_trace",
          title: "Two-pointer walk (target 9)",
          steps: [
            {
              step: 1,
              description: "left=0,right=3 → 2+15=17 > 9 → right--",
              array: [2, 7, 11, 15],
              pointers: { left: 0, right: 3 },
              highlight: [0, 3],
              variables: { sum: 17, target: 9 },
            },
            {
              step: 2,
              description: "left=0,right=2 → 2+11=13 > 9 → right--",
              array: [2, 7, 11, 15],
              pointers: { left: 0, right: 2 },
              highlight: [0, 2],
              variables: { sum: 13, target: 9 },
            },
            {
              step: 3,
              description: "left=0,right=1 → 2+7=9 ✓ found",
              array: [2, 7, 11, 15],
              pointers: { left: 0, right: 1 },
              highlight: [0, 1],
              variables: { sum: 9, target: 9 },
            },
          ],
        },
      },
      {
        kind: "predict",
        title: "Change one thing — new target",
        subtitle: "Slide the target. Watch which pointer must move.",
        interaction: {
          kind: "change_one_thing",
          label: "Target sum",
          min: 9,
          max: 26,
          step: 1,
          target: 17,
          unit: "",
          formula: "2+15=17 → hit target at right=3",
          initial: 9,
        },
        mcqs: [
          {
            id: "change",
            q: "target = 20 on [2,7,11,15]. 2+15=17 < 20. First move?",
            options: ["right--", "left++", "return [0,3]", "right++"],
            correct: 1,
            explain: "17 is under 20 — undershoot → advance the left pointer for a larger sum.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "predict",
        interaction: {
          kind: "predict_output",
          questions: [
            {
              id: "tp-p1",
              code: "nums = [2, 7, 11, 15]\ntarget = 9\n# first check: nums[0]+nums[3] = ?",
              options: ["17", "9", "13", "22"],
              correctIndex: 0,
              explanation: "2+15=17 > 9 → move right pointer left.",
              language: "python",
            },
          ],
        },
        mcqs: [
          {
            id: "predict",
            q: "nums=[2,7,11,15], target=9. First iteration sum?",
            options: ["17", "9", "13", "22"],
            correct: 0,
            explain: "2+15=17.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — two_sum template",
        interaction: {
          kind: "code_fill",
          title: "Which line moves on overshoot?",
          code: "left, right = 0, len(nums)-1\nwhile left < right:\n    s = nums[left] + nums[right]\n    if s == target: return [left, right]\n    ?????",
          options: [
            "right -= 1 if s > target else left += 1",
            "left += 1 always",
            "right += 1",
            "break",
          ],
          correct: "right -= 1 if s > target else left += 1",
          prompt: "On a sorted array, overshoot → move right inward; undershoot → move left outward.",
          pattern: "two-pointers",
          successNote: "Correct — overshoot shrinks from the right, undershoot grows from the left.",
          failNote: "Not quite — sorted sum only fixes overshoot by decreasing the larger side.",
        },
        judgeTo: "/lesson/arrays-1",
        judgeLabel: "Open Two Pointers lesson",
      },
      {
        kind: "practice",
        title: "Practice — sequenced set",
        subtitle: "Easy → variants. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — opposite ends",
            items: [
              { label: "Two Sum (sorted) · easy", to: "/question-bank?topic=two_pointers" },
              { label: "Valid Palindrome · easy", to: "/question-bank?topic=two_pointers" },
            ],
          },
          {
            level: "Level 2 — same direction",
            items: [
              { label: "Remove duplicates in-place · medium", to: "/question-bank?topic=two_pointers" },
            ],
          },
        ],
      },
      {
        kind: "break",
        mcqs: [
          {
            id: "break",
            q: "Unsorted array + both-ends two pointers. What breaks?",
            options: [
              "Nothing",
              "Sum is no longer monotonic — greedy pointer moves can skip the true pair",
              "Always O(n²)",
              "Stack overflow",
            ],
            correct: 1,
            explain: "Two-ends greedy needs sorted (or a hash) — otherwise the invariant fails.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        interaction: {
          kind: "explain_the_bug",
          skillId: "dsa.two_pointers",
          keywords: ["sorted", "sum", "target", "pointer", "move"],
          title: "Why must the array be sorted?",
          prompt: "Type why both-ends movement is only correct on sorted input.",
          pattern: "two-pointers",
        },
        mcqs: [
          {
            id: "debug",
            q: "Fix: sum < target. Which pointer moves?",
            options: ["right--", "left++", "both", "neither"],
            correct: 1,
            explain: "Need a larger sum → advance the left (smaller) pointer.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        interaction: {
          kind: "recall_check",
          prompt: "Recall the three branch outcomes in two_sum.",
          answer: "sum == target → return; sum > target → right--; sum < target → left++",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — palindrome check",
        mcqs: [
          {
            id: "transfer",
            q: "Is 'abba' a palindrome? First compare…",
            options: [
              "a vs a (ends)",
              "a vs b (middle)",
              "all at once",
              "sort first",
            ],
            correct: 0,
            explain: "Both ends inward: s[0] vs s[n-1], then s[1] vs s[n-2].",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "t1",
            q: "Two-sum on sorted, sum > target → ?",
            options: ["left++", "right--", "restart", "sort again"],
            correct: 1,
            explain: "Decrease the larger end.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "t2",
            q: "Complexity of opposite-ends two-sum?",
            options: ["O(n)", "O(n log n)", "O(n²)", "O(1)"],
            correct: 0,
            explain: "Each pointer moves at most n steps.",
            codeIfMissed: "COMPLEXITY_ERROR",
          },
          {
            id: "t3",
            q: "Invariant that makes greedy correct?",
            options: [
              "array length even",
              "sorted order → sum monotonic in each pointer",
              "all positive only",
              "target prime",
            ],
            correct: 1,
            explain: "Monotonicity justifies one-way moves.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 5. EMAIL FORMAT VALIDATION
  // ─────────────────────────────────────────────────────────────
  email_format: {
    id: "email_format",
    title: "Email Format Validation",
    briefing:
      "A local part, exactly one @, a domain with a dot — and no empty sides. Validate with clear checks, not hope. Production also rejects header injection and normalizes case on the domain.",
    why:
      "String validation and pattern matching appear in coding assessments and take-home assignments. The same structure-thinking applies to regex, parser edge cases, and input sanitization in real backend work.",
    skillId: "coding.strings",
    estimatedMinutes: 14,
    tags: ["coding", "validation"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~14 minutes." },
      {
        kind: "discover",
        title: "Discover — the shape",
        interaction: {
          kind: "visual_hook",
          visual: "local  @  domain.tld\nuser   @  example.com\n^^^^   ^  ^^^^^^^ ^^^\nnon-empty  one @  has dot  TLD",
          caption: "Split on @ → exactly two non-empty sides; domain must contain a dot.",
        },
        mcqs: [
          {
            id: "discover",
            q: "Which is invalid?",
            options: ["a@b.co", "a@@b.com", "user@site.org", "x+y@z.in"],
            correct: 1,
            explain: "Two @ signs → more than one split → invalid.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One shared rule. Name it before you validate.",
        mcqs: [
          {
            id: "recognize",
            q: "'a@@b.com' fails. 'user@site' fails. A newline smuggled in From: injects extra headers. What single rule judges all three?",
            options: [
              "Validity is structural — shape first, and never trust raw input inside headers",
              "Longer strings are always more valid",
              "Only .com domains are real",
              "Headers can safely contain newlines",
            ],
            correct: 0,
            explain:
              "Shape-first is the rule: exactly one @, non-empty sides, dotted domain — plus sanitize anything user-controlled before it touches mail headers.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — change one thing",
        subtitle: "Slide a failing input toward valid.",
        interaction: {
          kind: "parameter_slider",
          label: "Missing pieces (0 = shape OK)",
          min: 0,
          max: 3,
          step: 1,
          target: 0,
          unit: " issues",
          formula: "issues={v} → {v}===0 ? shape_ok : invalid",
          initial: 3,
        },
      },
      {
        kind: "predict",
        interaction: {
          kind: "predict_output",
          questions: [
            {
              id: "em-p1",
              code: "s = 'user@site'\nprint('@' in s and '.' in s.split('@')[-1])",
              options: ["True", "False", "error", "None"],
              correctIndex: 1,
              explanation: "domain 'site' has no '.' → False.",
              language: "python",
            },
          ],
        },
        mcqs: [
          {
            id: "predict",
            q: "'user@site' — has @ and letters — valid?",
            options: [
              "Yes",
              "No — domain has no dot",
              "Yes if uppercase",
              "Depends on SMTP",
            ],
            correct: 1,
            explain: "Practical format check requires a dot in the domain (site.com).",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — fill the validator",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "def is_email(s):\n    if s.count('@') != 1: return False\n    local, domain = s.split('@')\n    if not local or not domain: return False\n    return '.' in {blank:dot}\n# header safety: never trust raw {blank:hdr} in From",
          blanks: [
            { id: "dot", placeholder: "expr", correctAnswer: "domain", width: 100 },
            { id: "hdr", placeholder: "field", correctAnswer: "user", width: 80 },
          ],
          explanation: "Exactly one @, both sides non-empty, domain has a dot; sanitize user input before mail headers.",
          language: "python",
        },
        judgeTo: "/lesson/things-1",
        judgeLabel: "Practice string checks",
      },
      {
        kind: "practice",
        title: "Practice — a sequenced set, not 50 random",
        subtitle: "Shape checks → edge inputs → injection safety. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — shape checks",
            items: [
              { label: "One-@ / dot drills · easy", to: "/lesson/things-1" },
              { label: "Empty-side edge cases · easy", to: "/question-bank?topic=strings" },
            ],
          },
          {
            level: "Level 2 — hostile inputs",
            items: [
              { label: "Multiple @ / missing dot · medium", to: "/question-bank?topic=strings" },
            ],
          },
          {
            level: "Level 3 — header safety",
            items: [
              { label: "Newline-injection spotting · medium", to: "/question-bank" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — injection",
        mcqs: [
          {
            id: "break",
            q: "Display name from user concatenated into mail headers. What breaks?",
            options: [
              "Nothing",
              "Newlines in the name can inject extra headers (BCC)",
              "Only performance",
              "JSON only",
            ],
            correct: 1,
            explain: "CRLF / newline in user-controlled header values → header injection. Sanitize + validate.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        interaction: {
          kind: "explain_the_bug",
          skillId: "coding.strings",
          keywords: ["sanitize", "header", "newline", "validate", "at"],
          title: "Why did the mailer accept a bad From?",
          prompt: "Type what check was missing and what must be stripped.",
          pattern: "email-format",
        },
        mcqs: [
          {
            id: "debug",
            q: "Minimum robust local checks?",
            options: [
              "len > 0 only",
              "exactly one @, non-empty sides, domain has dot",
              "contains a letter",
              "ends with .com only",
            ],
            correct: 1,
            explain: "Structure checks first; full RFC is larger but this catches common OAs.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        interaction: {
          kind: "recall_check",
          prompt: "Recall the four shape rules.",
          answer: "exactly one @ · local non-empty · domain non-empty · domain contains '.'",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — TCS-style structure (writing)",
        subtitle: "Same discipline: structure before prose.",
        mcqs: [
          {
            id: "transfer",
            q: "NQT email body order that scores?",
            options: [
              "closing → greeting → points",
              "greeting → purpose → cover keywords → closing",
              "slang then points",
              "points with no greeting",
            ],
            correct: 1,
            explain: "Structure is graded: subject, greeting, purpose, all prompt keywords, sign-off.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "e1",
            q: "'a@b.c' minimal valid under our rules?",
            options: ["valid", "no local", "no dot in domain", "two @"],
            correct: 0,
            explain: "local a, domain b.c has a dot.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "e2",
            q: "'user@.com' valid?",
            options: ["yes", "no — empty domain label before dot", "yes if user", "no @"],
            correct: 1,
            explain: "Empty left label in domain fails practical checks.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
          {
            id: "e3",
            q: "Header injection is prevented by…",
            options: [
              "longer passwords",
              "stripping CR/LF and validating structure",
              "uppercase only",
              "SSL",
            ],
            correct: 1,
            explain: "Sanitize newlines + validate format before building headers.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 6. SLIDING WINDOW (existing gold content — canonical schema)
  // ─────────────────────────────────────────────────────────────
  sliding_window_001: {
    id: "sliding_window_001",
    title: "Sliding Window",
    briefing:
      "Brute force re-sums every window — O(n·k). The window slides: one element enters, one leaves, each index touched twice. That is the whole trick, and it buys you O(n).",
    why:
      "Sliding window turns up in array, string, and subarray problems across every major company's screening. Recognizing the pattern early prevents brute-force TLEs in timed assessments.",
    skillId: "dsa.sliding_window",
    estimatedMinutes: 18,
    tags: ["dsa", "arrays"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~18 minutes." },
      {
        kind: "discover",
        type: "discover",
        title: "Discover — say it in your words",
        subtitle: "Why does the window stay O(n)? Type it. Keyword match, not a speech grade.",
        interaction: { kind: "explain_aloud" },
        component: "ExplainAloud",
      },
      {
        kind: "recognize",
        title: "Recognize — name the hidden shape",
        subtitle: "Pattern recognition is the skill. Which problem smells like a window?",
        mcqs: [
          {
            id: "recognize",
            q: "Which problem is likely Sliding Window?",
            options: [
              "Find shortest path in a graph",
              "Maximum sum subarray of size K",
              "Detect a cycle in a linked list",
              "Binary search in a rotated array",
            ],
            correct: 1,
            explain:
              "Contiguous subarray + fixed width K = window. Shortest path is graphs, cycle is two pointers/Floyd, rotated search is binary search.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        type: "manipulate",
        title: "Manipulate — drag the window",
        subtitle: "Step through. Watch left chase right. Feel the O(n).",
        interaction: { kind: "pattern_tracer" },
        component: "PatternTracer",
      },
      {
        kind: "predict",
        type: "predict",
        title: "Predict — no running it first",
        subtitle: "Trace it in your head, then commit.",
        mcqs: [
          {
            id: "predict",
            q: "Trace it in your head first — what is best after the loop?",
            code: "arr = [2, 1, 5, 1, 3]\nk = 3\nwindow_sum = sum(arr[:k])  # 8\nbest = window_sum\nfor right in range(k, len(arr)):\n    window_sum += arr[right] - arr[right - k]\n    best = max(best, window_sum)",
            options: ["9", "8", "7", "6"],
            correct: 0,
            explain: "right=3: 8+1−2=7 (best 8). right=4: 7+3−1=9 (best 9).",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        type: "build",
        title: "Build — write the shrink",
        subtitle: "Choose the line, then prove it on the real judge.",
        interaction: { kind: "code_fill" },
        component: "CodeFillInTheBlank",
        judgeTo: "/problems/sliding-window",
        judgeLabel: "Browse all window problems",
      },
      {
        kind: "practice",
        title: "Practice — a sequenced set, not 50 random",
        subtitle: "Fixed → variable → hard. Real bank problems, same evidence loop.",
        sequence: [
          {
            level: "Level 1 — Fixed window",
            items: [
              { label: "Maximum Average Subarray I · easy", to: "/question-bank/verify-076" },
              { label: "First negative in every window · easy", to: "/question-bank/ind-code-sw-1" },
            ],
          },
          {
            level: "Level 2 — Variable window",
            items: [
              { label: "Contains Duplicate II · easy", to: "/question-bank/verify-077" },
              {
                label: "Two Pointer / Sliding Window variant · medium",
                to: "/question-bank/6fc73af4-df26-4a91-9f5a-382d0585af8e",
              },
            ],
          },
          {
            level: "Level 3 — Hard",
            items: [
              { label: "Sliding Window Maximum · hard", to: "/question-bank/tcs_coding_084" },
              { label: "Peak of every sliding window · hard", to: "/question-bank/ind-code-sw-6" },
            ],
          },
        ],
      },
      {
        kind: "break",
        type: "break",
        title: "Break — find the bug",
        subtitle: "This code returns 12 instead of 9 on [2,1,5,1,3], k=3. What broke?",
        interaction: { kind: "break_and_debug" },
        mcqs: [
          {
            id: "break",
            q: "What broke?",
            code: "def max_window_sum(arr, k):\n    window_sum = sum(arr[:k])\n    best = window_sum\n    for right in range(k, len(arr)):\n        window_sum += arr[right]\n        best = max(best, window_sum)\n    return best",
            options: [
              "best starts too low",
              "Old elements never leave — arr[right-k] is never subtracted, the sum grows forever",
              "range should start at 0",
              "max() should be min()",
            ],
            correct: 1,
            explain: "A window must slide both ways: +arr[right], −arr[right−k]. Without the subtraction it is a growing prefix sum.",
            codeIfMissed: "DEBUGGING",
          },
        ],
      },
      {
        kind: "debug",
        type: "debug",
        title: "Debug — fix it",
        subtitle: "Pick the line that belongs inside the loop.",
        interaction: { kind: "explain_the_bug" },
        mcqs: [
          {
            id: "debug",
            q: "Which line belongs inside the loop after adding arr[right]?",
            options: [
              "window_sum -= arr[right - k]",
              "window_sum += arr[right - k]",
              "window_sum = sum(arr[:k])",
              "left += k",
            ],
            correct: 0,
            explain: "Subtract the element falling out of the window's left edge.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        title: "Retrieve — close the notes",
        subtitle: "Recall the window contract from memory before the transfer test.",
        interaction: {
          kind: "recall_check",
          prompt: "Without scrolling: what three facts define a fixed-size window?",
          answer: "width k · right enters, left leaves each step · each element enters once and leaves once → O(n)",
        },
        mcqs: [
          {
            id: "retrieve",
            q: "Why is fixed sliding window O(n)?",
            options: [
              "Each element enters once and leaves once",
              "Sorting makes it linear",
              "k is always small",
              "max() runs in O(1) amortized",
            ],
            correct: 0,
            explain: "Enter-once, leave-once bounds total work at 2n operations.",
            codeIfMissed: "KNOWLEDGE_RECALL",
          },
        ],
      },
      {
        kind: "transfer",
        type: "transfer",
        title: "Transfer — new disguise",
        subtitle: "Same pattern, unfamiliar problem.",
        interaction: { kind: "transfer_problem" },
        mcqs: [
          {
            id: "transfer",
            q: "Longest substring without repeating characters. When do you move left?",
            options: [
              "When s[right] is already inside the current window",
              "After every 3 steps",
              "Only at the end",
              "Never — left stays at 0",
            ],
            correct: 0,
            explain: "Variable windows shrink exactly when the constraint breaks — here, a duplicate appears.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass. Timeout submits automatically.",
        interaction: { kind: "timed_prove" },
        timeLimitSeconds: 180,
        passScore: 60,
        mcqs: [
          {
            id: "prove-1",
            q: "k=3 over [2,1,5,1,3]. Maximum window sum?",
            options: ["8", "7", "9", "6"],
            correct: 2,
            explain: "[2,1,5]=8, [1,5,1]=7, [5,1,3]=9.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "prove-2",
            q: "Time complexity of fixed sliding-window max?",
            options: ["O(n)", "O(n log n)", "O(n·k)", "O(k)"],
            correct: 0,
            explain: "Each element enters and leaves once.",
            codeIfMissed: "COMPLEXITY_ERROR",
          },
          {
            id: "prove-3",
            q: "Variable window: when to shrink from the left?",
            options: [
              "When the window violates its constraint",
              "Always after k steps",
              "When the sum is too large",
              "At each step",
            ],
            correct: 0,
            explain: "Shrink on constraint violation — duplicates, sum over target, too many distinct.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
    ],
  },
  // ─────────────────────────────────────────────────────────────
  // 7. FOR LOOPS
  // ─────────────────────────────────────────────────────────────
  for_loops: {
    id: "for_loops",
    title: "For Loops",
    briefing:
      "A for loop repeats a block with a changing variable. The three parts — start, stop, step — determine exactly how many times the body runs. Trace the counter, not the whole program.",
    why:
      "Loop tracing is the single most common programming-logic question in service-company screenings. Mastering for-loop state changes directly improves coding aptitude and DSA problem solving.",
    skillId: "coding.loops",
    estimatedMinutes: 16,
    tags: ["foundations", "world1"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~16 minutes." },
      {
        kind: "discover",
        title: "Discover — the counter",
        subtitle: "A for loop is just a counter that updates itself.",
        interaction: {
          kind: "visual_hook",
          visual: "for i in range(3):\n    print(i)\n# i=0 → 0\n# i=1 → 1\n# i=2 → 2",
          caption: "range(3) yields 0, 1, 2. The body runs once per value.",
        },
        mcqs: [
          {
            id: "discover",
            q: "range(3) produces how many iterations?",
            options: ["2", "3", "4", "0"],
            correct: 1,
            explain: "range(stop) yields 0..stop-1 → 3 values.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three loop forms. One discipline. Name it before you trace.",
        mcqs: [
          {
            id: "recognize",
            q: "for i in range(n), while count > 0, and do..while all repeat. What single idea makes them predictable?",
            options: [
              "The loop variable and termination condition fully determine iteration count",
              "Loops always run exactly 10 times",
              "break is required for every loop",
              "The body never changes the counter",
            ],
            correct: 0,
            explain: "Start, stop, and step are the contract. The body may change other state, but the counter's path is fixed unless you break.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — step the counter",
        subtitle: "Walk each iteration. Watch i change.",
        interaction: {
          kind: "state_trace",
          title: "For-loop trace",
          steps: [
            {
              step: 1,
              description: "i=0 → print 0",
              array: [0, 1, 2],
              pointers: { i: 0 },
              highlight: [0],
              variables: { i: 0 },
            },
            {
              step: 2,
              description: "i=1 → print 1",
              array: [0, 1, 2],
              pointers: { i: 1 },
              highlight: [1],
              variables: { i: 1 },
            },
            {
              step: 3,
              description: "i=2 → print 2",
              array: [0, 1, 2],
              pointers: { i: 2 },
              highlight: [2],
              variables: { i: 2 },
            },
          ],
        },
      },
      {
        kind: "predict",
        title: "Predict — what prints?",
        subtitle: "Commit before you run.",
        mcqs: [
          {
            id: "predict",
            q: "for i in range(1, 4): print(i*2) outputs…",
            options: ["2 4 6", "1 2 3", "2 4 6 8", "0 2 4"],
            correct: 0,
            explain: "i takes 1, 2, 3 → doubled → 2, 4, 6.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — fill the loop",
        subtitle: "Complete the missing loop header.",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "for i in {blank:range}:\n    print(i)\n# prints 0 1 2",
          blanks: [
            {
              id: "range",
              placeholder: "range",
              correctAnswer: "range(3)",
              hint: "range(3) gives 0, 1, 2",
              width: 120,
            },
          ],
          explanation: "range(stop) yields 0 through stop-1.",
          language: "python",
        },
        judgeTo: "/lesson/loops-1",
        judgeLabel: "Open Loops lesson",
      },
      {
        kind: "practice",
        title: "Practice — sequenced set",
        subtitle: "Counters → accumulators → nested. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — counters",
            items: [
              { label: "Range drills · easy", to: "/question-bank?topic=loops" },
            ],
          },
          {
            level: "Level 2 — accumulators",
            items: [
              { label: "Sum/product in a loop · easy", to: "/question-bank?topic=loops" },
            ],
          },
          {
            level: "Level 3 — nested",
            items: [
              { label: "Nested loop traces · medium", to: "/question-bank?topic=nested_loops" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — off-by-one",
        mcqs: [
          {
            id: "break",
            q: "range(1, 5) produces…",
            options: ["1 2 3 4", "1 2 3 4 5", "0 1 2 3 4", "1 2 3"],
            correct: 3,
            explain: "range(start, stop) yields start..stop-1 → 1,2,3,4.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        interaction: {
          kind: "explain_the_bug",
          skillId: "coding.loops",
          keywords: ["range", "stop", "start", "counter", "iteration"],
          title: "Why did the loop run one too many times?",
          prompt: "Type which bound is wrong and what it should be.",
          pattern: "for-loops",
        },
        mcqs: [
          {
            id: "debug",
            q: "Correct fix for off-by-one in range?",
            options: [
              "Always use range(0, n)",
              "Match stop to the desired count: range(start, start+count)",
              "Add 1 to the result",
              "Use while True",
            ],
            correct: 1,
            explain: "stop is exclusive; set it to the first value you do NOT want.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        interaction: {
          kind: "recall_check",
          prompt: "Recall: range(1, 4) yields what?",
          answer: "1, 2, 3",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — new context",
        mcqs: [
          {
            id: "transfer",
            q: "Build a list of the first 5 even numbers using a for loop. Which range is correct?",
            options: [
              "range(5)",
              "range(1, 11)",
              "range(0, 10, 2)",
              "range(2, 12)",
            ],
            correct: 2,
            explain: "range(0, 10, 2) yields 0,2,4,6,8 — five evens.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "f1",
            q: "range(3) yields…",
            options: ["0 1 2", "1 2 3", "0 1 2 3", "3 2 1"],
            correct: 0,
            explain: "stop is exclusive.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "f2",
            q: "Loop that sums numbers 1..100: best pattern?",
            options: [
              "for i in range(100): total += i",
              "for i in range(1, 101): total += i",
              "while total < 100",
              "for i in range(1, 100)",
            ],
            correct: 1,
            explain: "Include the endpoint by making stop 101.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
          {
            id: "f3",
            q: "Nested loops over n×n grid run…",
            options: ["O(n)", "O(n log n)", "O(n²)", "O(1)"],
            correct: 2,
            explain: "Outer n times inner n → n².",
            codeIfMissed: "COMPLEXITY_ERROR",
          },
        ],
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────
  // 8. SQL JOINS
  // ─────────────────────────────────────────────────────────────
  sql_joins: {
    id: "sql_joins",
    title: "SQL JOINs",
    briefing:
      "JOINs combine rows from two tables using a matching key. INNER keeps only matches. LEFT keeps every left row even when there is no match. RIGHT is the mirror of LEFT. Start with the key, then choose the shape.",
    why:
      "SQL is a core skill for data and backend roles. JOIN questions appear in written assessments and take-home assignments. Understanding INNER vs LEFT is also the foundation for window functions and analytics interviews.",
    skillId: "sql.joins",
    estimatedMinutes: 16,
    tags: ["sql", "data"],
    stages: [
      { kind: "intro", title: "Mission briefing", subtitle: "What you will prove in ~16 minutes." },
      {
        kind: "discover",
        title: "Discover — the Venn intuition",
        subtitle: "INNER is overlap. LEFT is left circle plus overlap. RIGHT is right circle plus overlap.",
        interaction: {
          kind: "visual_hook",
          visual: "INNER  = overlap only\nLEFT    = left ∪ overlap\nRIGHT   = right ∪ overlap",
          caption: "Every join is a set choice driven by the ON condition.",
        },
        mcqs: [
          {
            id: "discover",
            q: "Which join drops rows that have no match in the right table?",
            options: ["INNER", "LEFT", "RIGHT", "FULL"],
            correct: 0,
            explain: "INNER returns only rows where the ON condition matches on both sides.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "recognize",
        title: "Recognize — the hidden shape",
        subtitle: "Three situations. One rule. Name it before you query.",
        mcqs: [
          {
            id: "recognize",
            q: "'Show all users even if they have no orders' needs…",
            options: [
              "INNER JOIN",
              "LEFT JOIN with users on the left",
              "RIGHT JOIN with orders on the left",
              "FULL JOIN only",
            ],
            correct: 1,
            explain: "LEFT preserves the left table; unmatched right columns become NULL.",
            codeIfMissed: "PATTERN_RECOGNITION",
          },
        ],
      },
      {
        kind: "manipulate",
        title: "Manipulate — match the key",
        subtitle: "Pair each business question with the correct join shape.",
        interaction: {
          kind: "match_relationships",
          left: [
            "Orders with their user email",
            "All users, even users with zero orders",
            "All orders, even if the user was deleted",
          ],
          right: [
            "INNER on users.id = orders.user_id",
            "LEFT JOIN users ON users.id = orders.user_id",
            "LEFT JOIN orders ON orders.user_id = users.id",
          ],
          pairs: [
            ["Orders with their user email", "INNER on users.id = orders.user_id"],
            ["All users, even users with zero orders", "LEFT JOIN users ON users.id = orders.user_id"],
            ["All orders, even if the user was deleted", "LEFT JOIN orders ON orders.user_id = users.id"],
          ],
        },
      },
      {
        kind: "predict",
        title: "Predict — row count",
        subtitle: "Predict before you execute.",
        mcqs: [
          {
            id: "predict",
            q: "users has 4 rows, orders has 6 rows, and exactly 3 users have orders. LEFT JOIN users → orders returns…",
            options: ["4", "6", "9", "3"],
            correct: 1,
            explain: "LEFT keeps all 4 users; the 3 matched users may each have multiple orders, so the result can be up to 6. With the given numbers, the LEFT result count equals the orders-side row count after matching.",
            codeIfMissed: "CONCEPT_GAP",
          },
        ],
      },
      {
        kind: "build",
        title: "Build — write the join",
        subtitle: "Fill the query that lists every order with its user name.",
        interaction: {
          kind: "fill_in_blank",
          codeTemplate: "SELECT orders.id, users.name\nFROM orders\n{blank:join} users ON orders.user_id = users.id",
          blanks: [
            {
              id: "join",
              placeholder: "join",
              correctAnswer: "INNER JOIN",
              hint: "INNER JOIN when you only want matched rows",
              width: 140,
            },
          ],
          explanation: "INNER JOIN keeps only orders whose user_id exists in users.",
          language: "sql",
        },
        judgeTo: "/problems?topic=sql",
        judgeLabel: "Practice SQL problems",
      },
      {
        kind: "practice",
        title: "Practice — sequenced set",
        subtitle: "INNER → LEFT → RIGHT. Same evidence loop.",
        sequence: [
          {
            level: "Level 1 — INNER",
            items: [
              { label: "Match orders to users · easy", to: "/question-bank?topic=sql" },
            ],
          },
          {
            level: "Level 2 — LEFT",
            items: [
              { label: "Users with zero orders · medium", to: "/question-bank?topic=sql" },
            ],
          },
          {
            level: "Level 3 — RIGHT / edge",
            items: [
              { label: "Orphan orders and duplicate keys · medium", to: "/question-bank?topic=sql" },
            ],
          },
        ],
      },
      {
        kind: "break",
        title: "Break — duplicate rows",
        mcqs: [
          {
            id: "break",
            q: "One user has 3 orders. INNER JOIN users → orders returns…",
            options: [
              "1 row",
              "3 rows for that user",
              "4 rows",
              "0 rows",
            ],
            correct: 1,
            explain: "A join replicates the left row once per matching right row.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
      {
        kind: "debug",
        interaction: {
          kind: "explain_the_bug",
          skillId: "sql.joins",
          keywords: ["left", "right", "inner", "null", "key"],
          title: "Why did the query drop users with no orders?",
          prompt: "Type which join type was used and what it should be.",
          pattern: "sql-joins",
        },
        mcqs: [
          {
            id: "debug",
            q: "Fix: show all users even without orders. Which join?",
            options: ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
            correct: 1,
            explain: "LEFT preserves the left table.",
            codeIfMissed: "IMPLEMENTATION_ERROR",
          },
        ],
      },
      {
        kind: "retrieve",
        interaction: {
          kind: "recall_check",
          prompt: "Recall the three join shapes and when to use each.",
          answer: "INNER = matches only · LEFT = all left + matches · RIGHT = all right + matches",
        },
      },
      {
        kind: "transfer",
        title: "Transfer — new schema",
        mcqs: [
          {
            id: "transfer",
            q: "Products and categories: every product must have a category, but some categories have no products yet. Show all categories with product count. Which join?",
            options: [
              "INNER JOIN products → categories",
              "LEFT JOIN categories → products",
              "RIGHT JOIN products → categories",
              "FULL JOIN only",
            ],
            correct: 1,
            explain: "LEFT preserves categories; unmatched products become NULL.",
            codeIfMissed: "TRANSFER_FAILURE",
          },
        ],
      },
      {
        kind: "mastery",
        type: "mastery",
        title: "Mastery — timed prove",
        subtitle: "3 questions. ≥60 to pass.",
        timeLimitSeconds: 180,
        passScore: 60,
        interaction: { kind: "timed_prove" },
        mcqs: [
          {
            id: "s1",
            q: "INNER JOIN keeps…",
            options: [
              "All left rows",
              "Only rows with matching keys on both sides",
              "All right rows",
              "All rows from both sides",
            ],
            correct: 1,
            explain: "INNER is the intersection.",
            codeIfMissed: "CONCEPT_GAP",
          },
          {
            id: "s2",
            q: "LEFT JOIN preserves…",
            options: ["Right table", "Left table", "Neither", "Only matches"],
            correct: 1,
            explain: "LEFT keeps every row from the left table.",
            codeIfMissed: "KNOWLEDGE_RECALL",
          },
          {
            id: "s3",
            q: "One user has 5 orders. LEFT JOIN users → orders produces at least…",
            options: ["1 row", "5 rows", "6 rows", "0 rows"],
            correct: 1,
            explain: "Each matching order becomes a row; unmatched users still appear once.",
            codeIfMissed: "EDGE_CASE_FAILURE",
          },
        ],
      },
    ],
  },
};

export function getMission(id: string): MissionContent | null {
  return MISSIONS[id] ?? null;
}

/** Normalize route slug → registry key (`two-pointers` → `two_pointers`). */
export function missionIdFromRoute(slug: string): string {
  return slug.replace(/-/g, "_");
}
