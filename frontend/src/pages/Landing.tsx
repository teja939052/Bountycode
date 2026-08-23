import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Search,
  Brain,
  Code2,
  Bug,
  Wrench,
  Shield,
  ArrowRight,
  Clock,
  Users,
  FileText,
  TrendingUp,
  MessageSquare,
  Compass,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { MentorAvatar } from "../design-system/Mentor";
import { IslandNode, type NodeState } from "../design-system/JourneyMap";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";

const JOURNEY_STEPS = [
  { label: "Foundations", sub: "Variables, types, conditions", pct: null, status: "done" as const },
  { label: "Problem Solver", sub: "DSA through real scenarios", pct: 72, status: "in_progress" as const },
  { label: "Engineering", sub: "APIs, databases, scaling", pct: 31, status: "available" as const },
  { label: "Interview", sub: "Mock OA, behavioral, system design", pct: null, status: "locked" as const },
  { label: "Job Ready", sub: "Prove it to employers", pct: null, status: "locked" as const },
];

const SIMULATION_LOOP = [
  { icon: Search, label: "Investigate", desc: "Read the broken system" },
  { icon: Brain, label: "Predict", desc: "Guess what is wrong" },
  { icon: Code2, label: "Build", desc: "Write the fix" },
  { icon: Bug, label: "Break", desc: "Find edge cases" },
  { icon: Wrench, label: "Debug", desc: "Fix the bugs" },
  { icon: Shield, label: "Prove", desc: "Pass hidden tests" },
];

const CORE_FEATURES = [
  { icon: Code2, title: "DSA Practice", desc: "Curated problems with hidden tests, progressive hints, and company filters.", tone: "tech" },
  { icon: MessageSquare, title: "AI Mock Interviews", desc: "Company-specific questions with instant AI feedback after each round.", tone: "primary" },
  { icon: FileText, title: "Resume & ATS", desc: "Upload, get an honest ATS score, and rewrite bullets that pass.", tone: "gold" },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Streaks, XP, and weak-area detection — always know what is next.", tone: "primary" },
  { icon: Users, title: "Company Prep", desc: "53+ company guides with patterns, behavioral questions, and experiences.", tone: "rare" },
] as const;

const ROLE_CARDS = [
  { id: "sde", title: "Software Developer", desc: "Full-stack SDE roles" },
  { id: "data_analyst", title: "Data Analyst", desc: "SQL, Python, dashboards" },
  { id: "data_scientist", title: "Data Scientist", desc: "ML, stats, models" },
  { id: "qa", title: "QA Engineer", desc: "Testing, automation" },
  { id: "devops", title: "DevOps Engineer", desc: "CI/CD, cloud, infra" },
  { id: "pm", title: "Product Manager", desc: "Strategy, execution" },
];

/** Map journey step status → IslandNode state. */
const STEP_STATE: Record<string, NodeState> = {
  done: "completed",
  active: "in_progress",
  partial: "in_progress",
  available: "available",
  in_progress: "in_progress",
  locked: "locked",
};

/** Small SVG glyphs for journey steps — no emoji. */
const STEP_GLYPHS = [
  <svg key="0" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 3v18M5 10l7-7 7 7" stroke="#15803D" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/></svg>,
  <svg key="1" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M8 6l-5 6 5 6M16 6l5 6-5 6M13 4l-2 16" stroke="#15803D" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>,
  <svg key="2" width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="3" y="8" width="18" height="12" rx="1.5" stroke="#5BA7A0" strokeWidth="2"/><path d="M9 8V5a2 2 0 012-2h2a2 2 0 012 2v3M3 13h18" stroke="#5BA7A0" strokeWidth="2"/></svg>,
  <svg key="3" width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="2" stroke="#EAB74D" strokeWidth="2"/><path d="M7 9h4M15 9l2 2M17 13h-4M9 15H7" stroke="#EAB74D" strokeWidth="1.8" strokeLinecap="round"/></svg>,
  <svg key="4" width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 3l2.4 5.4L20 9l-4 3.8L17 19l-5-2.8L7 19l1-6.2L4 9l5.6-.6L12 3z" fill="#EAB74D"/></svg>,
];

export default function Landing() {
  const reduced = useReducedMotion();

  return (
    <PageShell theme="adventure">
      <div className="mx-auto max-w-5xl px-4 py-20 md:py-28">
        {/* ═══ HERO ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="text-center"
        >
          <div className="mb-6 flex justify-center">
            <div className="flex items-center gap-2 rounded-full border border-border bg-surface px-4 py-1.5 shadow-card">
              <Compass size={16} className="text-ocean" />
              <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
                The career adventure for engineers
              </span>
            </div>
          </div>

          <h1 className="font-display mx-auto max-w-3xl text-4xl font-extrabold tracking-tight text-text sm:text-5xl md:text-[3.4rem] md:leading-[1.08]">
            Know exactly what stands between you and your next job.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-text-muted sm:text-lg">
            PlacementPro diagnoses your skills, charts your course, and trains you through real
            coding bounties, company OAs, interviews, and projects — one island at a time.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link to="/role-selector" className="w-full sm:w-auto">
              <Button variant="primary" size="xl" fullWidth className="sm:w-auto">
                Find my readiness
              </Button>
            </Link>
            <Link to="/pricing" className="w-full sm:w-auto">
              <Button variant="outline" size="xl" fullWidth className="sm:w-auto">
                Explore the journey
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* ═══ BOUNTY MAP PREVIEW — the signature visual ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="mt-20"
        >
          <Card pad="none" tone="bounty" className="overflow-hidden">
            <div className="parchment-bg relative px-6 pb-8 pt-6 sm:px-10">
              {/* Map corner flourishes */}
              <span aria-hidden="true" className="absolute left-3 top-3 h-5 w-5 rounded-full border-2 border-dashed border-wood/30" />
              <span aria-hidden="true" className="absolute right-3 top-3 h-5 w-5 rounded-full border-2 border-dashed border-wood/30" />
              <span aria-hidden="true" className="absolute bottom-3 left-3 h-5 w-5 rounded-full border-2 border-dashed border-wood/30" />
              <span aria-hidden="true" className="absolute bottom-3 right-3 h-5 w-5 rounded-full border-2 border-dashed border-wood/30" />

              <p className="adventure-label mb-1">Your Voyage</p>
              <h2 className="font-display text-center text-xl font-extrabold text-text sm:text-2xl">
                Five islands between here and the offer
              </h2>
              <p className="mx-auto mt-2 max-w-md text-center text-sm text-text-muted">
                A progression through real capabilities, not just topic checkboxes.
              </p>

              {/* Islands on desktop; scrollable row on mobile */}
              <div className="mt-8 overflow-x-auto pb-2">
                <div className="relative flex min-w-[640px] items-start justify-between gap-2 px-4">
                  {/* Dotted route behind islands */}
                  <svg
                    aria-hidden="true"
                    className="pointer-events-none absolute left-6 right-6 top-8 hidden h-4 sm:block"
                    preserveAspectRatio="none"
                    viewBox="0 0 100 4"
                  >
                    <line x1="0" y1="2" x2="100" y2="2" stroke="#A8754F" strokeWidth="0.6" strokeDasharray="2 2.4" opacity="0.55" />
                  </svg>

                  {JOURNEY_STEPS.map((step, i) => (
                    <div key={step.label} className="relative z-10 flex flex-col items-center">
                      <IslandNode
                        state={STEP_STATE[step.status] ?? "locked"}
                        title=""
                        mastery={step.pct ?? undefined}
                        icon={STEP_GLYPHS[i]}
                        isBoss={i === JOURNEY_STEPS.length - 1}
                      />
                      {/* Replace node's internal label with richer card below */}
                      <p className="mt-1 text-sm font-bold text-text">{step.label}</p>
                      <p className="max-w-[110px] text-center text-[11px] leading-tight text-text-muted">{step.sub}</p>
                      {step.pct !== null && (
                        <p className="mt-0.5 text-[11px] font-bold text-ocean">{step.pct}% charted</p>
                      )}
                      {i === JOURNEY_STEPS.length - 1 && (
                        <span className="badge-gold badge mt-1">The goal</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Mentor greeting strip */}
              <div className="surface-bg mt-6 flex items-center gap-3 rounded-xl border border-border p-3 shadow-card sm:mx-8">
                <MentorAvatar size={44} mood="welcome" />
                <p className="text-xs leading-snug text-text-muted sm:text-sm">
                  <span className="font-bold text-text">Captain Byte:</span>{" "}
                  Every engineer's map looks different. Answer a few questions and I'll chart yours.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* ═══ HOW IT WORKS — THE MISSION LOOP ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.25 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-xl font-extrabold text-text sm:text-2xl">
            Not a course. Bounties.
          </h2>
          <p className="mx-auto mt-2 max-w-lg text-center text-sm text-text-muted">
            Every task follows a simulation loop: investigate, predict, build, break, debug, prove.
          </p>

          <div className="mt-10 grid grid-cols-3 gap-4 md:grid-cols-6">
            {SIMULATION_LOOP.map((step, i) => (
              <div key={step.label} className="group flex flex-col items-center text-center">
                <div className="relative">
                  <div className="surface-border flex h-12 w-12 items-center justify-center rounded-xl border bg-surface text-text transition-colors group-hover:border-primary/40 group-hover:bg-mint group-hover:text-primary-dark">
                    <step.icon size={20} strokeWidth={1.8} />
                  </div>
                  {i < SIMULATION_LOOP.length - 1 && (
                    <ArrowRight className="absolute -right-3 top-1/2 hidden h-3 w-3 -translate-y-1/2 text-text-muted/40 md:block" />
                  )}
                </div>
                <p className="mt-2 text-xs font-bold text-text">{step.label}</p>
                <p className="mt-0.5 text-[11px] leading-tight text-text-muted">{step.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ═══ TODAY'S BOUNTY ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-20"
        >
          <h2 className="text-center font-display text-xl font-extrabold text-text sm:text-2xl">
            Today's Bounty
          </h2>
          <p className="mx-auto mt-2 max-w-lg text-center text-sm text-text-muted">
            A real task, not a toy problem.
          </p>

          <Link to="/capability-worlds" className="mx-auto mt-8 block max-w-md">
            <Card interactive tone="bounty">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <span className="adventure-label">Problem Solver</span>
                  <h3 className="font-display mt-2 text-base font-bold text-text">
                    Repair the broken registration system
                  </h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-text-muted">
                    A user registration API is failing silently. Investigate the code, predict the
                    root cause, and ship a fix that passes all test cases.
                  </p>
                </div>
                <div className="shrink-0 rounded-full bg-reward-soft px-2.5 py-1 text-xs font-extrabold text-wood">
                  +120 XP
                </div>
              </div>

              <div className="mt-4 flex items-center gap-4 text-xs text-text-muted">
                <span className="flex items-center gap-1">
                  <Clock size={13} /> 18 min
                </span>
                <span>Programming</span>
                <span>Intermediate</span>
              </div>

              <div className="mt-4 flex items-center gap-1.5 text-sm font-bold text-primary-dark">
                Accept bounty <ArrowRight size={14} />
              </div>
            </Card>
          </Link>
        </motion.div>

        {/* ═══ CORE FEATURES ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.35 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-2xl font-extrabold text-text sm:text-3xl">
            Everything included
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-text-muted">
            Six tools. One path to the offer.
          </p>

          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {CORE_FEATURES.map((feature) => {
              const toneClass =
                feature.tone === "tech" ? "bg-tech-soft text-tech" :
                feature.tone === "gold" ? "bg-reward-soft text-wood" :
                feature.tone === "rare" ? "bg-rare-soft text-rare" :
                "bg-primary-soft text-primary-dark";
              return (
                <Card key={feature.title}>
                  <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-xl ${toneClass}`}>
                    <feature.icon size={22} strokeWidth={1.8} />
                  </div>
                  <h3 className="font-display text-lg font-bold text-text">{feature.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-text-muted">{feature.desc}</p>
                </Card>
              );
            })}
          </div>
        </motion.div>

        {/* ═══ ROLE SELECTION ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-2xl font-extrabold text-text sm:text-3xl">
            What role are you targeting?
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-text-muted">
            Every voyage starts with a destination.
          </p>

          <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3">
            {ROLE_CARDS.map((role) => (
              <Link key={role.id} to="/role-selector">
                <Card interactive className="text-center">
                  <div className="mx-auto mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-sky-soft text-ocean">
                    <Compass size={22} strokeWidth={1.8} />
                  </div>
                  <p className="text-sm font-bold text-text">{role.title}</p>
                  <p className="mt-1 text-xs text-text-muted">{role.desc}</p>
                </Card>
              </Link>
            ))}
          </div>
        </motion.div>

        {/* ═══ FINAL CTA ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.45 }}
          className="mt-24 text-center"
        >
          <h2 className="font-display text-3xl font-extrabold text-text sm:text-4xl">
            Ready to start your journey?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-text-muted">
            Join thousands of students who landed offers at top companies. Free to start — upgrade
            anytime.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link to="/role-selector" className="w-full sm:w-auto">
              <Button variant="primary" size="xl" fullWidth className="sm:w-auto">
                Start free
              </Button>
            </Link>
            <Link to="/pricing" className="w-full sm:w-auto">
              <Button variant="outline" size="xl" fullWidth className="sm:w-auto">
                See all plans
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* ═══ FOOTER ═══ */}
        <footer className="mt-20 border-t border-border pt-8">
          <p className="text-center text-sm text-text-muted">
            Built with care for your career. &copy; {new Date().getFullYear()} PlacementPro. All rights reserved.
          </p>
        </footer>
      </div>
    </PageShell>
  );
}
