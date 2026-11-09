import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Building2,
  Check,
  Flame,
  Gauge,
  Lock,
  ShieldCheck,
  Star,
  Target,
  Timer,
  Trophy,
  Wrench,
  Zap,
} from "lucide-react";

import { PageShell } from "../design-system/PageShell";
import { Card } from "../design-system/Card";
import { SakuraPetals } from "../components/SakuraPetals";
import useReducedMotion from "../hooks/useReducedMotion";
import { ReadinessRing, MasteryBar, TreasureBadge } from "../design-system/Progress";
import { Emblem } from "../components/emblems/Emblem";
import { MasteryRadar } from "../components/MasteryRadar";
import { BountyCard } from "../components/BountyCard";
import { PatternTracer } from "../components/interactivity/PatternTracer";
import { StreakConstellation } from "../components/StreakConstellation";
import { JourneyMap, IslandNode, BountyCard as JourneyBountyCard } from "../design-system/JourneyMap";
import { CandyCard } from "../components/candy/CandyCard";
import { CandyButton } from "../components/candy/CandyButton";
import { OrganicPath } from "../components/candy/OrganicPath";
import { HeroBadge } from "../components/hero/HeroBadge";
import SplashScreen from "../components/hero/SplashScreen";

/* ------------------------------------------------------------------ */
/*  Palette — warm paper, deep ink, gold, and one colour per phase.    */
/* ------------------------------------------------------------------ */
const INK = "#0E1813";
const MUTED = "#4A5A51";
const FAINT = "#7A8A80";
const HAIRLINE = "#E3E9DF";
const PAPER = "#FFFCF8";
const GOLD = "#D4A843";
const GREEN = "#22C55E";
const GREEN_DARK = "#15803D";
const PINK = "#E85D8A";
const TEAL = "#5BA7A0";
const CORAL = "#E96A5B";
const AMBER = "#EAB74D";

/* ------------------------------------------------------------------ */
/*  Motion helpers                                                    */
/* ------------------------------------------------------------------ */
function Reveal({
  children,
  className = "",
  delay = 0,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  const reduced = useReducedMotion();
  if (reduced) return <div className={className}>{children}</div>;
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

function Eyebrow({ children, color = GREEN }: { children: React.ReactNode; color?: string }) {
  return (
    <p
      className="flex items-center justify-center gap-2 text-[11px] font-bold uppercase tracking-[0.2em]"
      style={{ color: MUTED }}
    >
      <span className="h-1.5 w-1.5 rounded-full" style={{ background: color }} aria-hidden="true" />
      {children}
    </p>
  );
}

function SectionHeading({
  eyebrow,
  eyebrowColor,
  title,
  children,
}: {
  eyebrow: string;
  eyebrowColor?: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <Eyebrow color={eyebrowColor}>{eyebrow}</Eyebrow>
      <h2
        className="mt-3 font-display text-3xl font-extrabold tracking-tight sm:text-4xl"
        style={{ color: INK }}
      >
        {title}
      </h2>
      <p className="mt-4 text-[15px] leading-relaxed sm:text-base" style={{ color: MUTED }}>
        {children}
      </p>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Brand mark — a five-petal blossom, drawn rather than imported.    */
/* ------------------------------------------------------------------ */
function Blossom({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      <g fill="none" stroke="currentColor" strokeWidth="1.5" opacity="0.9">
        {[0, 72, 144, 216, 288].map((angle) => (
          <ellipse key={angle} cx="16" cy="9.2" rx="4.1" ry="6.8" transform={`rotate(${angle} 16 16)`} />
        ))}
      </g>
      <circle cx="16" cy="16" r="2.1" fill="currentColor" />
    </svg>
  );
}

/* ------------------------------------------------------------------ */
/*  The loop — 12 stations on one trail, built as a real SVG.         */
/* ------------------------------------------------------------------ */
type PhaseKey = "plan" | "learn" | "prove" | "repair" | "ready";

const PHASES: Record<PhaseKey, { label: string; color: string }> = {
  plan: { label: "Plan", color: GREEN },
  learn: { label: "Learn", color: PINK },
  prove: { label: "Prove", color: TEAL },
  repair: { label: "Repair", color: CORAL },
  ready: { label: "Ready", color: GOLD },
};

const LOOP_STATIONS: { label: string[]; phase: PhaseKey }[] = [
  { label: ["Company"], phase: "plan" },
  { label: ["Blueprint"], phase: "plan" },
  { label: ["Skill"], phase: "plan" },
  { label: ["Pattern"], phase: "plan" },
  { label: ["Interactive", "Lesson"], phase: "learn" },
  { label: ["Practice"], phase: "prove" },
  { label: ["Assessment"], phase: "prove" },
  { label: ["Evidence"], phase: "prove" },
  { label: ["Diagnosis"], phase: "repair" },
  { label: ["Repair"], phase: "repair" },
  { label: ["Retest"], phase: "repair" },
  { label: ["Readiness"], phase: "ready" },
];

const LOOP_POINTS = LOOP_STATIONS.map((_, i) => ({
  x: 48 + i * 100,
  y: 104 + Math.sin(i * 0.82) * 22,
}));

function smoothPath(points: { x: number; y: number }[]): string {
  if (points.length < 2) return "";
  let d = `M ${points[0].x} ${points[0].y}`;
  for (let i = 0; i < points.length - 1; i += 1) {
    const p0 = points[i - 1] ?? points[i];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[i + 2] ?? p2;
    const t = 0.17;
    const c1x = p1.x + (p2.x - p0.x) * t;
    const c1y = p1.y + (p2.y - p0.y) * t;
    const c2x = p2.x - (p3.x - p1.x) * t;
    const c2y = p2.y - (p3.y - p1.y) * t;
    d += ` C ${c1x.toFixed(1)} ${c1y.toFixed(1)}, ${c2x.toFixed(1)} ${c2y.toFixed(1)}, ${p2.x} ${p2.y}`;
  }
  return d;
}

function LoopTrail() {
  const path = smoothPath(LOOP_POINTS);
  return (
    <figure className="m-0">
      <div className="overflow-x-auto pb-2">
        <svg
          viewBox="0 0 1200 200"
          role="img"
          aria-labelledby="loop-trail-title"
          className="h-auto w-full"
          style={{ minWidth: 1040 }}
        >
          <title id="loop-trail-title">
            The BountyCode loop: company, blueprint, skill, pattern, interactive lesson,
            practice, assessment, evidence, diagnosis, repair, retest, readiness.
          </title>
          <defs>
            <linearGradient id="loop-trail-stroke" x1="0%" y1="0%" x2="1" y2="0">
              <stop offset="0%" stopColor={GREEN} />
              <stop offset="38%" stopColor={PINK} />
              <stop offset="58%" stopColor={TEAL} />
              <stop offset="82%" stopColor={CORAL} />
              <stop offset="100%" stopColor={GOLD} />
            </linearGradient>
          </defs>

          <path
            d={path}
            fill="none"
            stroke="url(#loop-trail-stroke)"
            strokeWidth="4"
            strokeLinecap="round"
            opacity="0.16"
          />
          <path
            d={path}
            fill="none"
            stroke="url(#loop-trail-stroke)"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeDasharray="2 10"
          />

          {LOOP_POINTS.map((point, i) => {
            const station = LOOP_STATIONS[i];
            const color = PHASES[station.phase].color;
            const labelY = station.label.length === 2 ? 146 : 154;
            return (
              <g key={station.label.join(" ")}>
                <circle cx={point.x} cy={point.y} r="24" fill={color} opacity="0.1" />
                <circle
                  cx={point.x}
                  cy={point.y}
                  r="16"
                  fill="#FFFFFF"
                  stroke={color}
                  strokeWidth="2.5"
                />
                <text
                  x={point.x}
                  y={point.y + 4}
                  textAnchor="middle"
                  fontSize="12"
                  fontWeight="700"
                  fill={color}
                  fontFamily="Inter, system-ui, sans-serif"
                >
                  {i + 1}
                </text>
                {station.label.map((line, li) => (
                  <text
                    key={line}
                    x={point.x}
                    y={labelY + li * 15}
                    textAnchor="middle"
                    fontSize="12.5"
                    fontWeight={i === LOOP_STATIONS.length - 1 ? 700 : 500}
                    fill={i === LOOP_STATIONS.length - 1 ? GOLD : "#33453B"}
                    fontFamily="Inter, system-ui, sans-serif"
                  >
                    {line}
                  </text>
                ))}
              </g>
            );
          })}
        </svg>
      </div>

      <figcaption className="mt-4 flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
        {(Object.keys(PHASES) as PhaseKey[]).map((key) => (
          <span
            key={key}
            className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.16em]"
            style={{ color: FAINT }}
          >
            <span
              className="h-2 w-2 rounded-full"
              style={{ background: PHASES[key].color }}
              aria-hidden="true"
            />
            {PHASES[key].label}
          </span>
        ))}
      </figcaption>
    </figure>
  );
}

/* ------------------------------------------------------------------ */
/*  Company blueprints — weights taken from the Vision Lock.           */
/* ------------------------------------------------------------------ */
const BLUEPRINTS = [
  {
    company: "Accenture",
    pattern: "Cognitive + Technical + Coding",
    critical: "Verbal · Pseudo-code · DSA",
    weights: [
      { label: "Verbal", value: 20, color: PINK },
      { label: "DSA", value: 20, color: GREEN },
      { label: "Pseudo-code", value: 15, color: TEAL },
      { label: "Reasoning", value: 15, color: AMBER },
      { label: "Numerical", value: 15, color: CORAL },
      { label: "CS fundamentals", value: 15, color: "#8B6BD9" },
    ],
  },
  {
    company: "TCS",
    pattern: "Numerical + Reasoning + Technical",
    critical: "",
    weights: [
      { label: "Numerical", value: 20, color: CORAL },
      { label: "Verbal", value: 15, color: PINK },
      { label: "Reasoning", value: 15, color: AMBER },
      { label: "DSA", value: 15, color: GREEN },
      { label: "Pseudo-code", value: 10, color: TEAL },
      { label: "Email writing", value: 10, color: "#8B6BD9" },
      { label: "CS fundamentals", value: 15, color: "#4A90E2" },
    ],
  },
];

const TARGET_COMPANIES = [
  "TCS",
  "Accenture",
  "Infosys",
  "Wipro",
  "Cognizant",
  "Capgemini",
  "HCL",
  "Tech Mahindra",
  "LTI",
  "Mphasis",
];

function BlueprintCard({ blueprint }: { blueprint: (typeof BLUEPRINTS)[number] }) {
  return (
    <Card className="h-full border-[#E3E9DF] bg-white" pad="md">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <span
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl"
            style={{ background: "#F1F7EF", color: GREEN_DARK }}
          >
            <Building2 size={18} />
          </span>
          <div>
            <h3 className="font-display text-lg font-extrabold leading-tight" style={{ color: INK }}>
              {blueprint.company}
            </h3>
            <p className="mt-0.5 text-[11px] font-semibold uppercase tracking-wider" style={{ color: FAINT }}>
              {blueprint.pattern}
            </p>
          </div>
        </div>
        <span
          className="rounded-full border px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider"
          style={{ borderColor: HAIRLINE, background: "#F7FAF7", color: FAINT }}
        >
          Blueprint
        </span>
      </div>

      <ul className="mt-5 space-y-2.5">
        {blueprint.weights.map((weight) => (
          <li key={weight.label}>
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium" style={{ color: "#33453B" }}>
                {weight.label}
              </span>
              <span className="font-mono font-semibold tabular-nums" style={{ color: FAINT }}>
                {weight.value}%
              </span>
            </div>
            <div className="mt-1 h-1.5 overflow-hidden rounded-full" style={{ background: "#EDF2EA" }}>
              <div
                className="h-full rounded-full"
                style={{ width: `${weight.value}%`, background: weight.color }}
              />
            </div>
          </li>
        ))}
      </ul>

      {blueprint.critical && (
        <p className="mt-4 text-[11px] font-medium" style={{ color: FAINT }}>
          Critical sections: <span style={{ color: INK }}>{blueprint.critical}</span>
        </p>
      )}
    </Card>
  );
}

/* ------------------------------------------------------------------ */
/*  Lesson demo — trace table + a real predict check.                  */
/* ------------------------------------------------------------------ */
const TRACE_ROWS = [
  { i: "—", total: "0", note: "before the loop" },
  { i: "0", total: "0", note: "0 + 0" },
  { i: "1", total: "1", note: "0 + 1" },
  { i: "2", total: "3", note: "1 + 2" },
  { i: "3", total: "6", note: "3 + 3" },
];

function TraceDemo() {
  const [pick, setPick] = useState<string | null>(null);
  const answered = pick !== null;
  const correct = pick === "6";

  return (
    <div className="overflow-hidden rounded-2xl border border-[#DCE8DE] bg-white shadow-[0_22px_60px_-30px_rgba(14,24,19,0.45)]">
      <div className="flex items-center gap-1.5 border-b border-white/10 bg-[#0E1813] px-4 py-2.5">
        <span className="h-2.5 w-2.5 rounded-full" style={{ background: CORAL }} aria-hidden="true" />
        <span className="h-2.5 w-2.5 rounded-full" style={{ background: AMBER }} aria-hidden="true" />
        <span className="h-2.5 w-2.5 rounded-full" style={{ background: GREEN }} aria-hidden="true" />
        <span className="ml-2 font-mono text-[11px] text-white/45">trace_variables.py</span>
      </div>

      <pre className="overflow-x-auto bg-[#0E1813] px-4 py-4 font-mono text-[12.5px] leading-relaxed text-[#D9E8DE]">
        <code>{`total = 0
for i in range(4):
    total += i
print(total)`}</code>
      </pre>

      <div className="px-4 pt-4">
        <table className="w-full text-left text-xs">
          <caption className="sr-only">Variable trace for the loop above</caption>
          <thead>
            <tr className="text-[10px] uppercase tracking-wider" style={{ color: FAINT }}>
              <th scope="col" className="pb-1.5 font-bold">Step</th>
              <th scope="col" className="pb-1.5 font-bold">i</th>
              <th scope="col" className="pb-1.5 font-bold">total</th>
              <th scope="col" className="pb-1.5 font-bold">Running sum</th>
            </tr>
          </thead>
          <tbody className="font-mono tabular-nums">
            {TRACE_ROWS.map((row, index) => {
              const last = index === TRACE_ROWS.length - 1;
              return (
                <tr
                  key={row.i}
                  className={last ? "" : "border-b border-[#F0F4ED]"}
                  style={last ? { background: "#EAF7EE", color: "#14653A" } : { color: "#33453B" }}
                >
                  <td className="py-1.5 pl-1 font-semibold">{index}</td>
                  <td className="py-1.5">{row.i}</td>
                  <td className="py-1.5 font-bold">{row.total}</td>
                  <td className="py-1.5 font-sans text-[11px]" style={{ color: last ? "#14653A" : FAINT }}>
                    {row.note}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-3 border-t px-4 py-4" style={{ borderColor: "#EDF2EA" }}>
        <p className="text-[10px] font-bold uppercase tracking-[0.16em]" style={{ color: FAINT }}>
          Predict
        </p>
        <p className="mt-1 text-sm font-semibold" style={{ color: INK }}>
          What does <code className="rounded bg-[#F1F5EE] px-1 font-mono text-[12px]">print(total)</code>{" "}
          output?
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          {["0", "3", "6", "10"].map((option) => {
            const selected = pick === option;
            const isRight = option === "6";
            let style: React.CSSProperties = { borderColor: HAIRLINE, background: "#FFFFFF", color: "#33453B" };
            if (selected && isRight) style = { borderColor: "#9FD8B0", background: "#EAF7EE", color: "#14653A" };
            if (selected && !isRight) style = { borderColor: "#EDC0B6", background: "#FDF0EC", color: "#8A3A2C" };
            if (answered && !selected && isRight) style = { borderColor: "#9FD8B0", background: "#F6FBF7", color: "#14653A" };
            return (
              <button
                key={option}
                type="button"
                aria-pressed={selected}
                onClick={() => setPick(option)}
                className="min-w-[52px] rounded-lg border px-3 py-1.5 font-mono text-xs font-bold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
                style={style}
              >
                {option}
              </button>
            );
          })}
        </div>
        <p
          className="mt-3 min-h-[18px] text-xs font-medium"
          style={{ color: answered ? (correct ? GREEN_DARK : "#8A3A2C") : FAINT }}
          aria-live="polite"
        >
          {!answered && "Pick an answer — the table above is the clue."}
          {answered && correct && "Correct. 0 + 1 + 2 + 3 = 6."}
          {answered && !correct && "Not yet. Read the table row by row: total keeps the running sum."}
        </p>
      </div>
    </div>
  );
}

const SHIPPED_STEPS = [
  { n: 1, title: "What is it", body: "One sentence, no hedging." },
  { n: 2, title: "See", body: "The pattern animated — variables, pointers, windows." },
  { n: 3, title: "Interact", body: "Change the inputs and watch the output move." },
  { n: 4, title: "Predict", body: "Commit to an answer before the reveal." },
  { n: 5, title: "Solve", body: "Build the answer yourself, not by copying." },
  { n: 6, title: "Prove", body: "A timed check that counts toward readiness." },
];

/* ------------------------------------------------------------------ */
/*  Evidence board — qualitative states, no invented numbers.          */
/* ------------------------------------------------------------------ */
type EvidenceState = "mastered" | "developing" | "failed" | "none";

const EVIDENCE_STYLE: Record<EvidenceState, { label: string; cell: string; dot: string }> = {
  mastered: {
    label: "Mastered",
    cell: "border-[#9FD8B0] bg-[#EAF7EE] text-[#14653A]",
    dot: GREEN,
  },
  developing: {
    label: "Developing",
    cell: "border-[#EBD39A] bg-[#FFF7E3] text-[#7A5B12]",
    dot: AMBER,
  },
  failed: {
    label: "Needs repair",
    cell: "border-[#EDC0B6] bg-[#FDF0EC] text-[#8A3A2C]",
    dot: CORAL,
  },
  none: {
    label: "No evidence",
    cell: "border-dashed border-[#D9DED7] bg-[#F8F9F6] text-[#7B8A80]",
    dot: "#C2CCC4",
  },
};

const EVIDENCE_PATTERNS: { name: string; state: EvidenceState }[] = [
  { name: "Percentages", state: "mastered" },
  { name: "Ratios", state: "mastered" },
  { name: "Profit & loss", state: "developing" },
  { name: "Averages", state: "mastered" },
  { name: "Time & work", state: "failed" },
  { name: "Number series", state: "developing" },
  { name: "Blood relations", state: "mastered" },
  { name: "Syllogism", state: "developing" },
  { name: "Coding-decoding", state: "none" },
  { name: "Seating", state: "none" },
  { name: "Grammar", state: "developing" },
  { name: "Para jumble", state: "none" },
  { name: "Two pointers", state: "failed" },
  { name: "Binary search", state: "mastered" },
  { name: "Stack & queue", state: "developing" },
  { name: "Trace variables", state: "none" },
];

const REPAIR_STEPS = [
  { title: "Fail", body: "A mock or a timed check misses." },
  { title: "Diagnose", body: "Wrong answer vs timeout, per pattern." },
  { title: "Repair", body: "Targeted exercises and lessons on the same pattern." },
  { title: "Retest", body: "A fresh attempt, not a rerun." },
  { title: "Mastery", body: "Readiness moves only on new evidence." },
];

/* ------------------------------------------------------------------ */
/*  Game layer cards                                                  */
/* ------------------------------------------------------------------ */
const GAME_CARDS = [
  {
    icon: Target,
    title: "Daily challenge",
    body: "Three problems drawn from your weakest domains, sized for five to fifteen minutes, so the habit also moves readiness.",
    to: "/daily-challenge",
    cta: "Open today's challenge",
    color: GREEN,
  },
  {
    icon: Star,
    title: "Stars that mean something",
    body: "The third star needs 9 out of 10 inside five minutes. It is earned on the attempt, not handed out for showing up.",
    to: "/tower",
    cta: "See the tower",
    color: AMBER,
  },
  {
    icon: Trophy,
    title: "Weekly league",
    body: "A cohort of peers, promoted or relegated on the ISO week, ranked by the XP your practice actually earned.",
    to: "/leaderboard",
    cta: "View the leaderboard",
    color: TEAL,
  },
];

/* ------------------------------------------------------------------ */
/*  Page                                                              */
/* ------------------------------------------------------------------ */
export default function Landing() {
  const reduced = useReducedMotion();
  return (
    <PageShell theme="spring">
      <SplashScreen />
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-6 focus:top-4 focus:z-[100] focus:inline-flex focus:items-center focus:gap-2 focus:rounded-lg focus:border focus:border-gray-300 focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-[#14201B] focus:shadow-lg"
      >
        Skip to content
      </a>

      {/* ═══ Hero ═══ */}
      <section className="spring-hero relative overflow-hidden min-h-screen" style={{ background: "#fbe4ec" }}>

        <SakuraPetals density="hero" />

        <div className="relative z-10 flex min-h-screen flex-col">
          {/* One minimal nav — the global Navbar is hidden on "/" */}
          <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-5">
            <Link to="/" className="flex items-center gap-2.5" style={{ color: INK }} aria-label="BountyCode home">
              <Blossom className="h-8 w-8" />
              <span className="font-display text-lg font-extrabold tracking-tight">BountyCode</span>
            </Link>
            <nav className="flex items-center gap-3 sm:gap-5" aria-label="Account">
              <Link
                to="/login"
                className="rounded-lg px-2 py-2 text-sm font-semibold transition-colors hover:bg-white/60"
                style={{ color: INK }}
              >
                Log in
              </Link>
              <Link
                to="/register"
                className="hero-btn-ghost inline-flex items-center gap-1.5 rounded-xl px-4 py-2 text-sm font-bold shadow-sm transition-transform hover:scale-[1.02] active:scale-[0.98]"
              >
                Get started
                <ArrowRight size={14} />
              </Link>
            </nav>
          </header>

          <div className="flex flex-1 items-center justify-center px-6 pb-24 pt-6">
            <motion.div
              className="mx-auto max-w-3xl text-center hero-fade-up"
              initial={reduced ? false : { opacity: 0, y: 22 }}
              animate={{
                opacity: 1,
                y: 0,
                filter: "blur(0px)",
              }}
              transition={{
                duration: 0.9,
                ease: "easeOut",
                filter: { type: "spring", stiffness: 300, damping: 30 },
              }}
            >
              <HeroBadge />

              <h1
                className="mt-6 font-display text-[3rem] font-extrabold leading-[1.05] tracking-tight sm:text-7xl md:text-8xl md:leading-[1.02]"
                style={{ color: INK }}
              >
                From your first line of code
                <br />
                <span className="hero-gradient-text">to your first offer.</span>
              </h1>

              <p className="mt-7 text-lg font-bold sm:text-xl md:text-lg" style={{ color: INK }}>
                A guided path from learning to getting hired.
              </p>
              <p
                className="mx-auto mt-4 max-w-2xl text-[15px] leading-relaxed sm:text-base md:text-lg"
                style={{ color: INK, opacity: 0.85 }}
              >
                Pick your target company. Learn the patterns these assessments test, in the
                order a blueprint weights them. Prove it in a company-style mock, then let
                evidence — not guesswork — decide what you repair next.
              </p>

              <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link
                  to="/register"
                  className="hero-cta-primary inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl px-8 py-4 text-sm font-bold shadow-xl transition-all hover:scale-[1.03] hover:shadow-2xl active:scale-[0.98]"
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Start free
                  <ArrowRight size={17} />
                </Link>
                <Link
                  to="/percentages-academy"
                  className="inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl border border-white/60 bg-white px-8 py-4 text-sm font-bold shadow-sm transition-colors hover:bg-white/60 hero-soft-glow"
                  style={{ borderColor: "rgba(255,255,255,0.5)", color: INK }}
                >
                  Try a lesson
                </Link>
              </div>

              {/* The product, in four words */}
              <ol
                className="mt-10 flex flex-wrap items-center justify-center gap-2"
                aria-label="How BountyCode works"
              >
                {[1, 2, 3, 4].map((chip, index) => (
                  <li key={chip} className="flex items-center gap-2">
                    <span
                      className="inline-flex items-center gap-1.5 rounded-full border border-white/80 bg-white px-3.5 py-1.5 text-xs font-bold shadow-sm"
                      style={{ color: "#14201B" }}
                    >
                      <span
                        className="flex h-4 w-4 items-center justify-center rounded-full text-[10px] font-bold text-white"
                        style={{ background: index === 3 ? GOLD : GREEN_DARK }}
                        aria-hidden="true"
                      >\n                        {chip}
                      </span>
                      {chip === 1 ? "Diagnose" : chip === 2 ? "Learn" : chip === 3 ? "Practice" : "Get Hired"}
                    </span>
                    {index < 3 && (
                      <span className="text-xs" style={{ color: "rgba(20,32,27,0.3)" }} aria-hidden="true">
                        →
                      </span>
                    )}
                  </li>
                ))}
              </ol>
            </motion.div>
          </div>
        </div>
      </section>

      <main id="main" className="relative z-10" style={{ background: PAPER }}>
        {/* ═══ The loop ═══ */}
        <section className="px-6 py-20 sm:py-24">
          <div className="mx-auto max-w-6xl">
            <Reveal>
              <SectionHeading
                eyebrow="The product"
                eyebrowColor={GREEN}
                title="One loop. Repeated until you're ready."
              >
                Company → blueprint → skill → pattern → interactive lesson →
                practice → assessment → evidence → diagnosis → repair → retest → readiness. Every station writes the
                state the next one reads.
              </SectionHeading>
            </Reveal>

            <Reveal className="mt-12" delay={0.05}>
              <LoopTrail />
            </Reveal>

            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              {[
                { title: "Diagnose" },
                { title: "Learn" },
                { title: "Practice" },
              ].map((item, index) => (
                <Reveal key={item.title} delay={0.05 + index * 0.05}>
                  <div
                    className="flex h-full gap-3 rounded-2xl border p-4"
                    style={{ borderColor: HAIRLINE, background: "#FFFFFF" }}
                  >
                    <span
                      className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl"
                      style={{ background: "#F1F7EF", color: GREEN_DARK }}
                    >
                      <Gauge size={17} />
                    </span>
                    <div>
                      <h3 className="text-sm font-bold" style={{ color: INK }}>
                        Plan with the blueprint
                      </h3>
                      <p className="mt-1 text-[13px] leading-relaxed" style={{ color: MUTED }}>
                        Section weights decide which skills get your hours — not a generic course order.
                      </p>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ═══ Blueprints ═══ */}
        <section className="spring-section spring-section-pink">
          <div className="mx-auto max-w-6xl">
            <Reveal>
              <SectionHeading
                eyebrow="Company blueprints"
                eyebrowColor={PINK}
                title="The assessment is a measurement config."
              >
                A blueprint turns a company into section weights, a practice order and a mock
                timing. Accenture and TCS carry measured weights today; the rest follow the same
                structure as their blueprints land.
              </SectionHeading>
            </Reveal>

            <div className="mx-auto mt-12 grid max-w-4xl gap-5 md:grid-cols-2">
              {BLUEPRINTS.map((blueprint, index) => (
                <Reveal key={blueprint.company} delay={0.05 + index * 0.06}>
                  <BlueprintCard blueprint={blueprint} />
                </Reveal>
              ))}
            </div>

            <Reveal className="mt-10" delay={0.1}>
              <div className="mx-auto max-w-4xl">
                <p
                  className="text-center text-[11px] font-bold uppercase tracking-[0.16em]"
                  style={{ color: FAINT }}
                >
                  Ten companies the platform is built around
                </p>
                <ul className="mt-4 flex flex-wrap items-center justify-center gap-2">
                  {TARGET_COMPANIES.map((company) => (
                    <li
                      key={company}
                      className="rounded-full border bg-white px-3.5 py-1.5 text-xs font-semibold"
                      style={{ borderColor: HAIRLINE, color: "#33453B" }}
                      title="Target company — practice is company-pattern practice"
                    >
                      {company}
                    </li>
                  ))}
                </ul>

                <p className="mx-auto mt-5 max-w-2xl text-center text-[12px] leading-relaxed" style={{ color: FAINT }}>
                  Weights are BountyCode's platform measurement config. They are not a claim about
                  any company's current paper, and company practice is labelled company-pattern
                  practice unless provenance says otherwise.
                </p>

                <div className="mt-7 flex flex-col items-center justify-center gap-3 sm:flex-row">
                  <Link
                    to="/aptitude"
                    className="btn-primary inline-flex items-center justify-center gap-2 px-6 py-3 text-sm"
                  >
                    Practice the sections
                    <ArrowRight size={15} />
                  </Link>
                  <Link
                    to="/mock-oa"
                    className="inline-flex items-center justify-center gap-2 rounded-xl border bg-white px-6 py-3 text-sm font-bold transition-colors hover:bg-[#F7FAF7]"
                    style={{ borderColor: "#CFDDD2", color: INK }}
                  >
                    Take a mock assessment
                  </Link>
                </div>
              </div>
            </Reveal>
          </div>
        </section>

        {/* ═══ Lesson template ═══ */}
        <section className="spring-section spring-section-green">
          <div className="mx-auto max-w-6xl">
            <Reveal>
              <SectionHeading
                eyebrow="Interactive lessons"
                eyebrowColor={TEAL}
                title="A lesson is a loop, not a video."
              >
                Define the pattern, watch it move, change it yourself, commit to a prediction,
                then solve and prove. No step is decorative — each one leaves evidence.
              </SectionHeading>
            </Reveal>

            <div className="mt-12 grid items-start gap-8 lg:grid-cols-[1fr_1.05fr] lg:gap-10">
              <Reveal>
                <ol className="space-y-3">
                  {SHIPPED_STEPS.map((step) => (
                    <li
                      key={step.n}
                      className="flex items-start gap-3 rounded-xl border bg-white p-3.5"
                      style={{ borderColor: HAIRLINE }}
                    >
                      <span
                        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-[11px] font-extrabold text-white"
                        style={{ background: step.n === 6 ? GOLD : GREEN_DARK }}
                        aria-hidden="true"
                      >
                        {step.n}
                      </span>
                      <div>
                        <p className="text-sm font-bold" style={{ color: INK }}>
                          {step.title}
                        </p>
                        <p className="mt-0.5 text-[13px] leading-snug" style={{ color: MUTED }}>
                          {step.body}
                        </p>
                      </div>
                    </li>
                  ))}
                </ol>

                <p className="mt-4 rounded-xl border border-dashed p-3 text-[12px] leading-relaxed" style={{ borderColor: "#CFDDD2", color: FAINT }}>
                  Break, Debug, Recall and Transfer are rolling out with each verified content
                  batch — they are not shown as shipped until the lessons exist.
                </p>
              </Reveal>

              <Reveal delay={0.08}>
                <TraceDemo />
                <p className="mt-3 text-center text-[12px]" style={{ color: FAINT }}>
                  World 4 — pseudocode and trace variables. Try the predict step above.
                </p>
                <div className="mt-5 flex flex-col items-center justify-center gap-3 sm:flex-row">
                  <Link to="/percentages-academy" className="btn-primary inline-flex items-center justify-center gap-2 px-6 py-3 text-sm">
                    Open a World 1 lesson
                    <ArrowRight size={15} />
                  </Link>
                  <Link to="/lessons" className="text-sm font-bold underline-offset-4 hover:underline" style={{ color: GREEN_DARK }}>
                    Browse the lesson catalog
                  </Link>
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* ═══ Evidence & repair ═══ */}
        <section className="px-6 py-20 sm:py-24">
          <div className="mx-auto max-w-6xl">
            <Reveal>
              <SectionHeading
                eyebrow="Evidence, not vibes"
                eyebrowColor={CORAL}
                title="A score is not a diagnosis."
              >
                Your board is pattern-level: what you've proven, what's developing, and where
                there is no evidence yet. Failed attempts split into wrong answer versus timeout,
                so the repair targets the cause.
              </SectionHeading>
            </Reveal>

            <div className="mt-12 grid items-start gap-8 lg:grid-cols-[1.15fr_1fr] lg:gap-10">
              <Reveal>
                <div className="rounded-2xl border bg-white p-4" style={{ borderColor: HAIRLINE }}>
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-bold" style={{ color: INK }}>
                      Pattern evidence
                    </p>
                    <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: FAINT }}>
                      Sample board
                    </span>
                  </div>

                  <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
                    {EVIDENCE_PATTERNS.map((pattern) => {
                      const style = EVIDENCE_STYLE[pattern.state];
                      return (
                        <div
                          key={pattern.name}
                          className={`rounded-xl border px-2.5 py-2 text-[11px] font-semibold leading-tight ${style.cell}`}
                          title={`${pattern.name}: ${style.label}`}
                        >
                          {pattern.name}
                        </div>
                      );
                    })}
                  </div>

                  <div className="mt-4 flex flex-wrap gap-x-4 gap-y-2">
                    {(Object.keys(EVIDENCE_STYLE) as EvidenceState[]).map((key) => (
                      <span key={key} className="inline-flex items-center gap-1.5 text-[11px] font-medium" style={{ color: MUTED }}>
                        <span className="h-2 w-2 rounded-full" style={{ background: EVIDENCE_STYLE[key].dot }} aria-hidden="true" />
                        {EVIDENCE_STYLE[key].label}
                      </span>
                    ))}
                  </div>

                  <p className="mt-4 border-t pt-3 text-[11px] leading-relaxed" style={{ borderColor: "#F0F4ED", color: FAINT }}>
                    Sample layout only. Yours fills from your first attempt — no seeded scores.
                  </p>
                </div>
              </Reveal>

              <div className="space-y-5">
                <Reveal delay={0.05}>
                  <div className="rounded-2xl border bg-white p-4" style={{ borderColor: HAIRLINE }}>
                    <p className="text-sm font-bold" style={{ color: INK }}>
                      Failure mix
                    </p>
                    <p className="mt-1 text-[13px] leading-relaxed" style={{ color: MUTED }}>
                      Two failures can look identical in a score and need opposite repairs.
                    </p>
                    <div className="mt-3 grid gap-2 sm:grid-cols-3">
                      {[
                        { label: "Syntax error", bg: "#FEE2E2", icon: Zap, color: "#DC2626", body: "Fix the crash, then resubmit" },
                        { label: "Logic error", bg: "#FEF3C7", icon: Flame, color: "#D97706", body: "Trace the flow, then rewrite" },
                        { label: "Edge case", bg: "#DBEAFE", icon: Target, color: "#2563EB", body: "Add the missing guard" },
                      ].map((item) => (
                        <div key={item.label} className="rounded-xl p-3" style={{ background: item.bg }}>
                          <item.icon size={15} style={{ color: item.color }} aria-hidden="true" />
                          <p className="mt-1.5 text-xs font-bold" style={{ color: item.color }}>
                            {item.label}
                          </p>
                          <p className="mt-0.5 text-[11px] leading-snug" style={{ color: MUTED }}>
                            {item.body}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </Reveal>

                <Reveal delay={0.1}>
                  <div className="rounded-2xl border bg-white p-4" style={{ borderColor: HAIRLINE }}>
                    <p className="text-sm font-bold" style={{ color: INK }}>
                      The repair rail
                    </p>
                    <ol className="mt-3 space-y-2">
                      {REPAIR_STEPS.map((step, index) => (
                        <li key={step.title} className="flex items-start gap-2.5">
                          <span
                            className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold"
                            style={{
                              background: index === REPAIR_STEPS.length - 1 ? "#FFF3D0" : "#F1F5EE",
                              color: index === REPAIR_STEPS.length - 1 ? "#7A5B12" : FAINT,
                            }}
                            aria-hidden="true"
                          >
                            {index + 1}
                          </span>
                          <p className="text-[12.5px] leading-snug" style={{ color: MUTED }}>
                            <span className="font-bold" style={{ color: INK }}>
                              {step.title}.
                            </span>{" "}
                            {step.body}
                          </p>
                        </li>
                      ))}
                    </ol>
                  </div>
                </Reveal>

                <Reveal delay={0.15}>
                  <div className="flex flex-wrap items-center gap-3">
                    <Link to="/skills" className="btn-primary inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm">
                      Open your skill map
                      <ArrowRight size={14} />
                    </Link>
                    <Link to="/practice" className="text-sm font-bold underline-offset-4 hover:underline" style={{ color: GREEN_DARK }}>
                      Practice a pattern
                    </Link>
                  </div>
                </Reveal>
              </div>
            </div>
          </div>
        </section>

        {/* ═══ Game layer ═══ */}
        <section className="spring-section spring-section-pink">
          <div className="mx-auto max-w-6xl">
            <Reveal>
              <SectionHeading
                eyebrow="Retention layer"
                eyebrowColor={AMBER}
                title="The game brings you back to the loop."
              >
                XP, streaks and leagues exist to make daily practice a habit — not to replace the
                work. Rewards are written by one engine, from the same score that grades your
                attempt.
              </SectionHeading>
            </Reveal>

            <Reveal className="mt-8" delay={0.05}>
              <ol className="flex flex-wrap items-center justify-center gap-2" aria-label="The game wrapper">
                {[
                  { label: "Practice", icon: Target, color: "#2563EB" },
                  { label: "XP", icon: Star, color: "#D97706" },
                  { label: "Streak", icon: Flame, color: "#DC2626" },
                  { label: "League", icon: Trophy, color: "#7C3AED" },
                ].map((item, index) => (
                  <li key={item.label} className="flex items-center gap-2">
                    <span
                      className="inline-flex items-center gap-1.5 rounded-full border bg-white px-3 py-1.5 text-xs font-bold"
                      style={{ borderColor: HAIRLINE, color: "#33453B" }}
                    >
                      <item.icon size={13} aria-hidden="true" />
                      {item.label}
                    </span>
                    {index < 4 && (
                      <span className="text-xs" style={{ color: "#C2CCC4" }} aria-hidden="true">
                        →
                      </span>
                    )}
                  </li>
                ))}
              </ol>
            </Reveal>

            <div className="mt-10 grid gap-5 md:grid-cols-3">
              {GAME_CARDS.map((card, index) => (
                <Reveal key={card.title} delay={0.05 + index * 0.06}>
                  <Card className="flex h-full flex-col border-[#E3E9DF] bg-white" pad="md">
                    <span
                      className="flex h-10 w-10 items-center justify-center rounded-xl"
                      style={{ background: "#F7FAF7", color: card.color }}
                    >
                      <card.icon size={18} />
                    </span>
                    <h3 className="mt-3 font-display text-base font-extrabold" style={{ color: INK }}>
                      {card.title}
                    </h3>
                    <p className="mt-1.5 flex-1 text-[13px] leading-relaxed" style={{ color: MUTED }}>
                      {card.body}
                    </p>
                    <Link
                      to={card.to}
                      className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold underline-offset-4 hover:underline"
                      style={{ color: GREEN_DARK }}
                    >
                      {card.cta}
                      <ArrowRight size={13} />
                    </Link>
                  </Card>
                </Reveal>
              ))}
            </div>

            <p className="mx-auto mt-6 max-w-2xl text-center text-[12px] leading-relaxed" style={{ color: FAINT }}>
              XP, coins and stars are scored from the attempt itself — the same number that grades
              your work — by one reward engine, not by the screen you are looking at.
            </p>
          </div>
        </section>

        {/* ═══ Final CTA ═══ */}
        <section className="spring-section spring-section-gold">
          <div className="mx-auto max-w-3xl text-center">
            <div
              className="gold-glow mx-auto mb-7 flex h-20 w-20 items-center justify-center rounded-full"
              style={{ background: "linear-gradient(135deg,#FFF7E3 0%,#FFEFC2 100%)" }}
            >
              <Star size={34} style={{ color: AMBER }} strokeWidth={1.5} aria-hidden="true" />
            </div>

            <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl" style={{ color: INK }}>
              Pick a company. Follow the path. Prove it.
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-[15px] leading-relaxed" style={{ color: MUTED }}>
              Start with one blueprint, one world and one honest assessment. Readiness is earned
              one piece of evidence at a time.
            </p>

            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link
                to="/register"
                className="hero-btn-primary inline-flex w-full items-center justify-center gap-2 rounded-xl px-7 py-3.5 text-sm font-bold shadow-lg transition-all hover:scale-[1.02] hover:shadow-xl active:scale-[0.98] sm:w-auto"
              >
                Start free
                <ArrowRight size={16} />
              </Link>
              <Link
                to="/pricing"
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl border bg-white px-7 py-3.5 text-sm font-bold transition-colors hover:bg-[#FFFDF8] sm:w-auto"
                style={{ borderColor: "#E4D6B2", color: INK }}
              >
                See the plans
              </Link>
            </div>

            <p className="mt-5 text-[12px]" style={{ color: FAINT }}>
              Free tier resets every month. Upgrade only when the free limits actually pinch.
            </p>
          </div>
        </section>

        {/* ═══ Footer ═══ */}
        <footer className="border-t bg-white px-6 py-8" style={{ borderColor: "#EDF0EA" }}>
          <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2" style={{ color: INK }}>
              <Blossom className="h-5 w-5" />
              <span className="font-display text-sm font-extrabold">BountyCode</span>
              <span className="text-[11px]" style={{ color: FAINT }}>
                Placement preparation for the service-company pipeline.
              </span>
            </div>
            <nav className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-[12px] font-medium" aria-label="Footer">
              <Link to="/percentages-academy" className="hover:underline" style={{ color: MUTED }}>
                Sample lesson
              </Link>
              <Link to="/pricing" className="hover:underline" style={{ color: MUTED }}>
                Pricing
              </Link>
              <Link to="/terms" className="hover:underline" style={{ color: MUTED }}>
                Terms
              </Link>
              <Link to="/privacy" className="hover:underline" style={{ color: MUTED }}>
                Privacy
              </Link>
              <Link to="/login" className="hover:underline" style={{ color: MUTED }}>
                Log in
              </Link>
            </nav>
          </div>
          <p className="mt-6 text-center text-[11px]" style={{ color: "#9AA79F" }}>
            © {new Date().getFullYear()} BountyCode. Built for students, not for résumé keywords.
          </p>
        </footer>
      </main>
    </PageShell>
  );
}

// TypeScript namespace augmentation for JSX
import React from "react";