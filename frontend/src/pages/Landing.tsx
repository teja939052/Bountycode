import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Target, Code2, MessageSquare, FileText, TrendingUp, Users } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const JOURNEY_STEPS = [
  { label: "Your Target", sub: "Software Engineer" },
  { label: "Readiness", sub: "54%" },
  { label: "Your Gaps", sub: "DSA, System Design, OS" },
  { label: "Your Plan", sub: "8 weeks" },
  { label: "Mock OA", sub: "", icon: true },
  { label: "Interview", sub: "", icon: true },
  { label: "Job Ready", sub: "87%" },
];

const CORE_FEATURES = [
  { icon: Code2, title: "DSA Practice", desc: "Curated problems with hidden tests, progressive hints, and company filters.", color: "blue" },
  { icon: MessageSquare, title: "AI Mock Interviews", desc: "Company-specific questions with instant AI feedback after each round.", color: "primary" },
  { icon: FileText, title: "Resume & ATS", desc: "Upload, get an honest ATS score, and rewrite bullets that pass.", color: "gold" },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Streaks, XP, and weak-area detection — always know what's next.", color: "primary" },
  { icon: Users, title: "Company Prep", desc: "53+ company guides with patterns, behavioral questions, and experiences.", color: "purple" },
];

export default function Landing() {
  const reduced = useReducedMotion();

  return (
    <div className="min-h-screen page-surface">
      <div className="mx-auto max-w-5xl px-4 py-24 md:py-32">
        {/* Above the fold */}
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
            Choose a role. Test your skills. Follow a personalized preparation path. Prove you're ready.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/role-selector">
              <motion.button
                whileHover={reduced ? {} : { scale: 1.02 }}
                whileTap={reduced ? {} : { scale: 0.98 }}
                className="px-8 py-3 rounded-[10px] bg-primary text-white font-medium text-sm tracking-wide transition-all hover:bg-primary-dark hover:shadow-[0_4px_16px_rgba(34,197,94,0.25)]"
              >
                Find my readiness
              </motion.button>
            </Link>
            <Link to="/pricing">
              <button className="px-8 py-3 rounded-[10px] border border-border text-text-primary font-medium text-sm hover:bg-primary-soft transition-colors">
                Explore the journey
              </button>
            </Link>
          </div>
        </motion.div>

        {/* Journey Visualization */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="mt-24"
        >
          <div className="relative">
            <div className="absolute left-6 right-6 top-7 hidden border-t-2 border-dashed border-border md:block" />

            <div className="grid grid-cols-2 gap-x-4 gap-y-6 sm:grid-cols-3 md:grid-cols-7">
              {JOURNEY_STEPS.map((step, i) => (
                <div key={step.label} className="relative flex flex-col items-center text-center">
                  <div className="relative z-10 flex h-12 w-12 items-center justify-center rounded-[10px] bg-primary-soft text-primary-dark font-bold">
                    {step.icon ? (
                      <Target size={18} />
                    ) : (
                      <span className="text-xs">{i + 1}</span>
                    )}
                  </div>
                  <p className="mt-2 text-sm font-medium text-text-primary">{step.label}</p>
                  {step.sub && <p className="text-xs text-text-muted">{step.sub}</p>}
                  {i === JOURNEY_STEPS.length - 1 && (
                    <span className="mt-1 rounded-full bg-primary px-2.5 py-0.5 text-[10px] font-semibold text-white">
                      The goal
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Core Features */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-20"
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
                <div className={`flex h-12 w-12 items-center justify-center rounded-[10px] mb-4 ${
                  feature.color === "blue" ? "bg-blue-100 text-blue-600" :
                  feature.color === "gold" ? "bg-gold-100 text-gold-700" :
                  feature.color === "purple" ? "bg-purple-100 text-purple-600" :
                  "bg-primary-soft text-primary-dark"
                }`}>
                  <feature.icon size={22} strokeWidth={1.8} />
                </div>
                <h3 className="font-display text-lg font-semibold text-text-primary">{feature.title}</h3>
                <p className="mt-2 text-sm text-text-muted">{feature.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Final CTA */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-24 text-center"
        >
          <h2 className="font-display text-3xl font-bold text-text-primary sm:text-4xl">
            Ready to start your journey?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-text-muted">
            Join thousands of students who landed offers at top companies.
            Free to start — upgrade anytime.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/role-selector">
              <button className="px-8 py-3 rounded-[10px] bg-primary text-white font-medium text-sm tracking-wide transition-all hover:bg-primary-dark hover:shadow-[0_4px_16px_rgba(34,197,94,0.25)]">
                Start free →
              </button>
            </Link>
            <Link to="/pricing">
              <button className="px-8 py-3 rounded-[10px] border border-border text-text-primary font-medium text-sm hover:bg-primary-soft transition-colors">
                See all plans
              </button>
            </Link>
          </div>
        </motion.div>

        <footer className="mt-20 border-t border-border pt-8">
          <p className="text-center text-sm text-text-muted">
            Built with care for your career. © {new Date().getFullYear()} PlacementPro. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
}
