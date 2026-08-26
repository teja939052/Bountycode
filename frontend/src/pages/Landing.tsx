import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Code2,
  FileText,
  TrendingUp,
  Users,
  MessageSquare,
  Compass,
  ArrowRight,
  CheckCircle2,
  Building2,
  Star,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { SakuraPetals } from "../components/SakuraPetals";

const ROLE_PATHS = [
  { id: "sde", title: "Software Developer", desc: "Full-stack SDE roles", icon: Code2, color: "#22C55E" },
  { id: "data_analyst", title: "Data Analyst", desc: "SQL, Python, dashboards", icon: TrendingUp, color: "#5BA7A0" },
  { id: "data_scientist", title: "Data Scientist", desc: "ML, stats, models", icon: Star, color: "#8B6BD9" },
  { id: "qa", title: "QA Engineer", desc: "Testing, automation", icon: CheckCircle2, color: "#EAB74D" },
];

const CORE_FEATURES = [
  { icon: Code2, title: "DSA Practice", desc: "Curated problems with hidden tests, progressive hints, and company filters." },
  { icon: MessageSquare, title: "AI Mock Interviews", desc: "Company-specific questions with instant AI feedback after each round." },
  { icon: FileText, title: "Resume & ATS", desc: "Upload, get an honest ATS score, and rewrite bullets that pass." },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Streaks, XP, and weak-area detection — always know what is next." },
  { icon: Users, title: "Company Prep", desc: "53+ company guides with patterns, behavioral questions, and experiences." },
];

const COMPANIES = [
  "Google", "Microsoft", "Amazon", "Meta", "Apple",
  "TCS", "Infosys", "Wipro", "Flipkart", "Razorpay",
];

export default function Landing() {
  const reduced = useReducedMotion();

  return (
    <PageShell theme="spring">
      {/* Skip link for keyboard navigation */}
      <a href="#main" className="skip-link absolute -top-4 left-6 z-50 inline-flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-2 text-sm font-medium text-text-primary hover:bg-primary/10 transition-colors">
        Skip to main content
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M7 10l5 5 5-5M12 15L3 9l9-9"/></svg>
      </a>

      {/* ═══ SAKURA PETALS — realistic falling cherry blossoms ═══ */}
      <SakuraPetals density="hero" />

      {/* ═══ HERO — open spring morning, not a wall of trees ═══ */}
      <section className="spring-hero min-h-[600px] relative">
        {/* Warm white / extremely pale blue background with subtle sunrise gradient */}
        <div
          className="absolute inset-0 bg-white/95 from-amber-50 via-white to-amber-50 gradient-blur"
          aria-hidden="true"
        />
        {/* Subtle film grain + sunlight bloom */}
        <div
          className="absolute inset-0 pointer-events-none overflow-hidden"
          style={{
            backgroundImage:
              "url('data:image/svg+xml,%3Csvg viewBox=\"0 0 256 256\" xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noise%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%222%22 stitchTiles=%22stretch%22/%3E%3C/filter%3E%3Crect width=%22256%22 height=%22256%22 fill=%22%23ffffff%22 filter=%22url(%23noise)%22/%3E%3C/svg%22')",
            opacity: 0.03,
          }}
        />
        {/* Subtle branch silhouettes at peripheral edges only — muted brown, NOT lime green */}
        <div
          className="absolute top-0 left-0 right-0 h-96 md:h-[400px] overflow-hidden pointer-events-none"
          style={{
            backgroundImage:
              "url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 120%22%3E%3Cpath fill=%22%235a2d11%22 opacity=%220.08%22 d=%22M20 60 C 40 10, 60 10, 80 60 C 100 10, 120 10, 140 60 C 160 10, 180 10, 200 60%22 /%3E%3C/svg%22')",
          }}
        />

        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="spring-hero-content relative z-10 max-w-3xl mx-auto px-4 w-full"
        >
          {/* Center section — open 60% atmospheric space */}
          <div className="mx-auto w-full max-w-2xl">
            <div className="mb-6 flex justify-center">
              <div className="flex items-center gap-2 rounded-full border border-border bg-surface px-4 py-1.5 shadow-sm backdrop-blur-sm">
                <Compass size={16} className="text-primary-soft" />
                <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
                  The career adventure for engineers
                </span>
              </div>
            </div>

            <h1 id="main" className="font-display text-4xl font-extrabold tracking-tight text-text sm:text-5xl md:text-[3.4rem] md:leading-[1.08]">
              Know exactly what stands between you and your next job.
            </h1>
            <p className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-text-muted sm:text-lg">
              BountyCode diagnoses your skills, charts your course, and trains you through real
              coding bounties, company OAs, interviews, and projects — one island at a time.
            </p>

            <p className="mx-auto mt-2 max-w-xl text-sm text-text-muted">
              -- Diagnose in 2 minutes | -- Real coding bounties, not theoretical quizzes | -- 53+ company guides | -- Free to start, upgrade anytime
            </p>

            <div className="mt-6 flex flex-col items-center justify-center gap-4 sm:flex-row">
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
          </div>
        </motion.div>

        {/* Subtle scroll indicator */}
        <motion.div
          initial={reduced ? {} : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.5 }}
          className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10"
        >
          <div className="flex flex-col items-center gap-2 text-text-muted text-xs">
            <span className="font-medium tracking-wide">Scroll to explore</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 5v14M19 12l-7 7-7-7" />
            </svg>
          </div>
        </motion.div>
      </section>

      {/* ═══ PATH CONNECTOR ═══ */}
      <div className="relative h-24 bg-gradient-to-b from-[#FFF8F9] to-white">
        <div className="spring-path absolute left-1/2 top-0 h-full -translate-x-1/2" />
        <div className="spring-path-dot" style={{ top: "33%", left: "calc(50% - 4px)" }} />
        <div className="spring-path-dot" style={{ top: "66%", left: "calc(50% - 4px)" }} />
      </div>

      {/* ═══ DISCOVER YOUR ROLE — Path branching ═══ */}
      <motion.section
        initial={reduced ? {} : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="spring-section spring-section-pink"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Discover your role
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-500">
            Every journey begins with a destination. Pick your path.
          </p>

          <div className="mx-auto mt-12 grid max-w-3xl grid-cols-2 gap-6 sm:grid-cols-4">
            {ROLE_PATHS.map((role, i) => (
              <Link key={role.id} to="/role-selector" className="group">
                <motion.div
                  initial={reduced ? {} : { opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.15 + i * 0.08 }}
                  className="role-path-card"
                >
                  <div
                    className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl transition-transform duration-300 group-hover:scale-110 group-hover:ring-primary/20 group-hover:border-primary/40"
                    style={{ backgroundColor: `${role.color}12`, color: role.color }}
                  >
                    <role.icon size={26} strokeWidth={1.8} />
                  </div>
                  <p className="text-sm font-bold text-gray-900">{role.title}</p>
                  <p className="mt-1 text-xs text-gray-500">{role.desc}</p>
                </motion.div>
              </Link>
            ))}
          </div>
        </div>
      </motion.section>

      {/* ═══ PATH CONTINUATION ═══ */}
      <div className="relative h-16 bg-gradient-to-b from-white via-white to-white">
        <div className="spring-path absolute left-1/2 top-0 h-full -translate-x-1/2" style={{ height: "100%" }} />
      </div>

      {/* ═══ EACH PATH = YOUR CURRICULUM ═══ */}
      <motion.section
        initial={reduced ? {} : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="spring-section spring-section-green"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Each path becomes your curriculum
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-500">
            Not a generic course. A personalized roadmap built from your role, your weak areas, and your target companies.
          </p>

          <div className="mx-auto mt-12 grid max-w-3xl gap-6 sm:grid-cols-3">
            {CORE_FEATURES.slice(0, 3).map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={reduced ? {} : { opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.25 + i * 0.1 }}
              >
                <Card className="h-full">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-green-50 text-green-600">
                    <feature.icon size={22} strokeWidth={1.8} />
                  </div>
                  <h3 className="font-display text-lg font-bold text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-gray-500">{feature.desc}</p>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Journey progress visualization */}
          <div className="mx-auto mt-12 max-w-2xl">
            <div className="relative flex items-center justify-between">
              {/* Background line */}
              <div className="absolute left-0 right-0 top-1/2 h-0.5 -translate-y-1/2 bg-gradient-to-r from-pink-200 via-green-200 to-amber-200" />

              {["Foundations", "Problem Solver", "Engineering", "Interview", "Job Ready"].map((step, i) => (
                <div key={step} className="relative z-10 flex flex-col items-center">
                  <div
                    className={`flex h-10 w-10 items-center justify-center rounded-full border-2 text-xs font-bold ${
                      i < 3
                        ? "border-green-400 bg-green-50 text-green-700"
                        : i === 3
                        ? "border-amber-300 bg-amber-50 text-amber-700"
                        : "border-gray-200 bg-gray-50 text-gray-400"
                    }`}
                  >
                    {i < 3 ? (
                      <CheckCircle2 size={18} />
                    ) : i === 4 ? (
                      <Star size={18} />
                    ) : (
                      i + 1
                    )}
                  </div>
                  <p className="mt-2 text-[11px] font-medium text-gray-600 text-center max-w-[80px]">{step}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.section>

      {/* ═══ PATH CONTINUATION ═══ */}
      <div className="relative h-16 bg-gradient-to-b from-white via-white to-white">
        <div className="spring-path absolute left-1/2 top-0 h-full -translate-x-1/2" style={{ height: "100%" }} />
      </div>

      {/* ═══ COMPANY PREPARATION ═══ */}
      <motion.section
        initial={reduced ? {} : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="spring-section"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Prepare for the companies you want
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-500">
            Company-specific patterns, behavioral questions, and real interview experiences.
          </p>

          <div className="mx-auto mt-10 flex flex-wrap justify-center gap-3">
            {COMPANIES.map((company) => (
              <Link
                key={company}
                to="/company-prep"
                className="flex items-center gap-2 rounded-full border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-green-300 hover:shadow-md hover:-translate-y-0.5"
              >
                <Building2 size={14} className="text-gray-400" />
                {company}
              </Link>
            ))}
          </div>

          <div className="mt-8 text-center">
            <Link
              to="/company-prep"
              className="inline-flex items-center gap-2 text-sm font-bold text-green-600 hover:text-green-700"
            >
              View all 53+ company guides
              <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </motion.section>

      {/* ═══ PATH CONTINUATION — transitions to gold ═══ */}
      <div className="relative h-16 bg-gradient-to-b from-white via-white to-white">
        <div className="spring-path absolute left-1/2 top-0 h-full -translate-x-1/2" style={{ height: "100%" }} />
      </div>

      {/* ═══ JOB READY — Achievement moment ═══ */}
      <motion.section
        initial={reduced ? {} : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.35 }}
        className="spring-section spring-section-gold"
      >
        <div className="mx-auto max-w-3xl px-4 text-center">
          <div className="gold-glow mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-amber-50 to-yellow-100 shadow-lg">
            <Star size={36} className="text-amber-500" strokeWidth={1.5} />
          </div>

          <h2 className="font-display text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Job Ready
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base text-gray-500">
            You have completed the journey. Your skills are proven. Your resume is optimized.
            Your interview performance is real. You are ready.
          </p>

          <div className="mx-auto mt-8 grid max-w-md grid-cols-3 gap-4">
            {[
              { label: "Problems Solved", value: "200+" },
              { label: "Mock Interviews", value: "50+" },
              { label: "Companies Covered", value: "53+" },
            ].map((stat) => (
              <div key={stat.label} className="rounded-xl border border-amber-200/60 bg-white/80 p-4 shadow-sm">
                <p className="text-2xl font-extrabold text-amber-600">{stat.value}</p>
                <p className="mt-1 text-xs text-gray-500">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* ═══ FINAL CTA ═══ */}
      <motion.section
        initial={reduced ? {} : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="spring-section bg-white"
      >
        <div className="mx-auto max-w-3xl px-4 text-center">
          <h2 className="font-display text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Ready to start your journey?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-gray-500">
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
        </div>
      </motion.section>

      {/* ═══ FOOTER ═══ */}
      <footer className="border-t border-gray-100 bg-white py-8">
        <p className="text-center text-sm text-gray-400">
          Built with care for your career. &copy; {new Date().getFullYear()} BountyCode. All rights reserved.
        </p>
      </footer>
    </PageShell>
  );
}