import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Search, Brain, Code2, Bug, Wrench, Shield, Lock, CheckCircle2, ArrowRight, Clock, Users, FileText, TrendingUp, MessageSquare } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const JOURNEY_STEPS = [
  { label: "Foundations", sub: "Variables, types, conditions", pct: null, status: "done" as const },
  { label: "Problem Solver", sub: "DSA through real scenarios", pct: 72, status: "active" as const },
  { label: "Engineering", sub: "APIs, databases, scaling", pct: 31, status: "partial" as const },
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
  { icon: Code2, title: "DSA Practice", desc: "Curated problems with hidden tests, progressive hints, and company filters.", color: "blue" },
  { icon: MessageSquare, title: "AI Mock Interviews", desc: "Company-specific questions with instant AI feedback after each round.", color: "primary" },
  { icon: FileText, title: "Resume & ATS", desc: "Upload, get an honest ATS score, and rewrite bullets that pass.", color: "gold" },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Streaks, XP, and weak-area detection \u2014 always know what is next.", color: "primary" },
  { icon: Users, title: "Company Prep", desc: "53+ company guides with patterns, behavioral questions, and experiences.", color: "purple" },
];

const ROLE_CARDS = [
  { id: "sde", title: "Software Developer", emoji: "\ud83d\udcbb", desc: "Full-stack SDE roles" },
  { id: "data_analyst", title: "Data Analyst", emoji: "\ud83d\udcca", desc: "SQL, Python, dashboards" },
  { id: "data_scientist", title: "Data Scientist", emoji: "\ud83e\udde0", desc: "ML, stats, models" },
  { id: "qa", title: "QA Engineer", emoji: "\ud83d\udd0d", desc: "Testing, automation" },
  { id: "devops", title: "DevOps Engineer", emoji: "\u2699\ufe0f", desc: "CI/CD, cloud, infra" },
  { id: "pm", title: "Product Manager", emoji: "\ud83d\udccb", desc: "Strategy, execution" },
];

const STEP_ICONS = ["\ud83c\udf31", "\u2694\ufe0f", "\ud83c\udfd7\ufe0f", "\ud83c\udf99\ufe0f", "\ud83c\udfc6"];

export default function Landing() {
  const reduced = useReducedMotion();

  return (
    <div className="min-h-screen page-surface relative overflow-hidden">
      {/* Subtle organic background texture */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        {/* Topographic contour rings - top right */}
        <svg className="absolute -top-20 -right-32 w-[600px] h-[600px] text-primary/[0.04]" viewBox="0 0 600 600" fill="none">
          <path d="M300 50C400 50 550 150 550 300S400 550 300 550S50 400 50 300S150 50 300 50Z" stroke="currentColor" strokeWidth="1.5" />
          <path d="M300 100C380 100 500 180 500 300S380 500 300 500S100 400 100 300S180 100 300 100Z" stroke="currentColor" strokeWidth="1" />
          <path d="M300 160C350 160 440 220 440 300S350 440 300 440S160 370 160 300S220 160 300 160Z" stroke="currentColor" strokeWidth="0.8" />
        </svg>
        {/* Bottom left contour */}
        <svg className="absolute -bottom-40 -left-20 w-[500px] h-[500px] text-primary/[0.03]" viewBox="0 0 500 500" fill="none">
          <path d="M50 250C50 120 150 30 250 30S450 120 450 250S350 470 250 470S50 380 50 250Z" stroke="currentColor" strokeWidth="1.5" />
          <path d="M80 250C80 140 170 60 250 60S420 140 420 250S330 440 250 440S80 360 80 250Z" stroke="currentColor" strokeWidth="1" />
        </svg>
        {/* Leaf silhouettes */}
        <svg className="absolute top-40 right-8 w-20 h-20 text-primary/[0.05] rotate-12" viewBox="0 0 80 80" fill="currentColor">
          <path d="M40 5C40 5 65 20 65 45C65 60 55 75 40 75C25 75 15 60 15 45C15 20 40 5 40 5Z" />
          <path d="M40 20V65" stroke="white" strokeWidth="1" fill="none" />
        </svg>
        <svg className="absolute bottom-60 left-6 w-16 h-16 text-primary/[0.04] -rotate-12" viewBox="0 0 60 60" fill="currentColor">
          <path d="M30 2C30 2 52 15 52 35C52 48 42 58 30 58C18 58 8 48 8 35C8 15 30 2 30 2Z" />
        </svg>
      </div>

      <div className="relative mx-auto max-w-5xl px-4 py-24 md:py-32">
        {/* ═══ HERO ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="text-center"
        >
          <h1 className="font-display text-4xl font-extrabold tracking-tight text-text-primary sm:text-5xl md:text-6xl">
            Know exactly what stands between you and your next job.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-text-muted">
            PlacementPro diagnoses your skills, builds your role-specific path, and trains you
            through real coding missions, company OAs, interviews, and projects.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/role-selector">
              <motion.button
                whileHover={reduced ? {} : { scale: 1.02 }}
                whileTap={reduced ? {} : { scale: 0.98 }}
                className="px-8 py-3 rounded-[10px] bg-primary text-navy font-bold text-sm tracking-wide transition-all hover:bg-primary-dark hover:shadow-[0_4px_16px_rgba(255,215,0,0.25)]"
              >
                Find my readiness
              </motion.button>
            </Link>
            <Link to="/pricing">
              <button className="px-8 py-3 rounded-[10px] border border-border text-text-muted hover:text-text-primary hover:bg-primary-soft transition-colors">
                Explore the journey
              </button>
            </Link>
          </div>
        </motion.div>

        {/* ═══ JOURNEY PATH ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-xl font-bold text-text-primary mb-2">
            Your Path to Job Ready
          </h2>
          <p className="text-center text-sm text-text-muted mb-10">
            A progression through real capabilities, not just topic checkboxes.
          </p>

          <div className="relative">
            {/* Connector line (desktop) */}
            <div className="absolute left-0 right-0 top-8 hidden md:block">
              <div className="h-[2px] bg-border mx-8" />
              <div className="absolute left-8 top-0 h-[2px] bg-primary/40" style={{ width: "35%" }} />
            </div>

            <div className="grid grid-cols-2 gap-x-4 gap-y-6 sm:grid-cols-3 md:grid-cols-5">
              {JOURNEY_STEPS.map((step, i) => (
                <div key={step.label} className="relative flex flex-col items-center text-center">
                  <div
                    className={`relative z-10 flex h-16 w-16 items-center justify-center rounded-[14px] text-2xl transition-all ${
                      step.status === "done"
                        ? "bg-primary/10 ring-2 ring-primary/30"
                        : step.status === "active"
                          ? "bg-primary/10 ring-2 ring-primary shadow-[0_0_20px_rgba(255,215,0,0.15)]"
                          : step.status === "partial"
                            ? "bg-primary-soft"
                            : "bg-surface-2 opacity-50"
                    }`}
                  >
                    {step.status === "done" ? (
                      <CheckCircle2 className="w-6 h-6 text-primary" />
                    ) : step.status === "locked" ? (
                      <Lock className="w-5 h-5 text-text-muted" />
                    ) : (
                      <span>{STEP_ICONS[i]}</span>
                    )}
                  </div>

                  <p className="mt-3 text-sm font-semibold text-text-primary">{step.label}</p>
                  <p className="text-xs text-text-muted mt-0.5">{step.sub}</p>

                  {step.pct !== null && (
                    <div className="mt-2 w-full max-w-[100px]">
                      <div className="h-1.5 bg-border rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary rounded-full transition-all"
                          style={{ width: `${step.pct}%` }}
                        />
                      </div>
                      <p className="text-[11px] text-primary-dark font-medium mt-1">{step.pct}%</p>
                    </div>
                  )}

                  {step.status === "locked" && (
                    <span className="mt-2 text-[10px] text-text-muted">Locked</span>
                  )}

                  {i === JOURNEY_STEPS.length - 1 && (
                    <span className="mt-2 rounded-full bg-primary px-3 py-0.5 text-[10px] font-semibold text-white">
                      The goal
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* ═══ HOW IT WORKS — THE MISSION LOOP ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.25 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-xl font-bold text-text-primary mb-2">
            Not a course. Missions.
          </h2>
          <p className="text-center text-sm text-text-muted mb-10">
            Every task follows a simulation loop: investigate, predict, build, break, debug, prove.
          </p>

          <div className="grid grid-cols-3 md:grid-cols-6 gap-4">
            {SIMULATION_LOOP.map((step, i) => (
              <div key={step.label} className="flex flex-col items-center text-center group">
                <div className="relative">
                  <div className="flex h-12 w-12 items-center justify-center rounded-[10px] bg-surface-2 text-text-primary transition-colors group-hover:bg-primary-soft group-hover:text-primary-dark">
                    <step.icon size={20} strokeWidth={1.8} />
                  </div>
                  {i < SIMULATION_LOOP.length - 1 && (
                    <ArrowRight className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 w-3 h-3 text-text-muted/40" />
                  )}
                </div>
                <p className="mt-2 text-xs font-semibold text-text-primary">{step.label}</p>
                <p className="text-[11px] text-text-muted leading-tight mt-0.5">{step.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ═══ TODAY'S MISSION ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-20"
        >
          <h2 className="text-center font-display text-xl font-bold text-text-primary mb-2">
            Today's Mission
          </h2>
          <p className="text-center text-sm text-text-muted mb-8">
            A real task, not a toy problem.
          </p>

          <Link to="/capability-worlds" className="block max-w-md mx-auto">
            <div className="rounded-[16px] p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/20 hover:shadow-card-hover cursor-pointer">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-[11px] uppercase tracking-wider font-semibold text-primary-dark">Problem Solver</p>
                  <h3 className="mt-1 text-base font-semibold text-text-primary">
                    Repair the broken registration system
                  </h3>
                  <p className="mt-1.5 text-sm text-text-muted leading-relaxed">
                    A user registration API is failing silently. Investigate the code, predict the root cause, and ship a fix that passes all test cases.
                  </p>
                </div>
                <div className="flex items-center gap-1 rounded-full bg-primary-soft px-2.5 py-1 text-xs font-semibold text-primary-dark whitespace-nowrap">
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

              <div className="mt-4 flex items-center gap-1.5 text-sm font-medium text-primary-dark">
                Start mission <ArrowRight size={14} />
              </div>
            </div>
          </Link>
        </motion.div>

        {/* ═══ CORE FEATURES ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.35 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-2xl font-bold text-text-primary sm:text-3xl">
            Everything included
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-text-muted">
            Six tools. One path to the offer.
          </p>

          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {CORE_FEATURES.map((feature) => (
              <div
                key={feature.title}
                className="rounded-[16px] p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/10"
              >
                <div
                  className={`flex h-12 w-12 items-center justify-center rounded-[10px] mb-4 ${
                    feature.color === "blue"
                      ? "bg-blue-100 text-blue-600"
                      : feature.color === "gold"
                        ? "bg-gold-100 text-gold-700"
                        : feature.color === "purple"
                          ? "bg-purple-100 text-purple-600"
                          : "bg-primary-soft text-primary-dark"
                  }`}
                >
                  <feature.icon size={22} strokeWidth={1.8} />
                </div>
                <h3 className="font-display text-lg font-semibold text-text-primary">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm text-text-muted">{feature.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ═══ ROLE SELECTION ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-24"
        >
          <h2 className="text-center font-display text-2xl font-bold text-text-primary sm:text-3xl">
            What role are you targeting?
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-text-muted">
            Every path starts with your destination.
          </p>

          <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3">
            {ROLE_CARDS.map((role) => (
              <Link key={role.id} to="/role-selector">
                <div className="rounded-[14px] p-5 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/20 hover:shadow-card-hover cursor-pointer text-center">
                  <span className="text-3xl">{role.emoji}</span>
                  <p className="mt-3 text-sm font-semibold text-text-primary">{role.title}</p>
                  <p className="text-xs text-text-muted mt-1">{role.desc}</p>
                </div>
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
          <h2 className="font-display text-3xl font-bold text-text-primary sm:text-4xl">
            Ready to start your journey?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-text-muted">
            Join thousands of students who landed offers at top companies.
            Free to start \u2014 upgrade anytime.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/role-selector">
              <button className="px-8 py-3 rounded-[10px] bg-primary text-white font-medium text-sm tracking-wide transition-all hover:bg-primary-dark hover:shadow-[0_4px_16px_rgba(255,215,0,0.25)]">
                Start free &rarr;
              </button>
            </Link>
            <Link to="/pricing">
              <button className="px-8 py-3 rounded-[10px] border border-border text-text-primary font-medium text-sm hover:bg-primary-soft transition-colors">
                See all plans
              </button>
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
    </div>
  );
}
