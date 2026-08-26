import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Code2,
  FileText,
  TrendingUp,
  Users,
  MessageSquare,
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
      {/* Skip link — keyboard only, visually hidden until focused */}
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-6 focus:z-[100] focus:inline-flex focus:items-center focus:gap-2 focus:rounded-lg focus:border focus:border-gray-300 focus:bg-white/90 focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-[#14201B] focus:shadow-lg focus:backdrop-blur-sm"
      >
        Skip to content
      </a>

      {/* ═══ SAKURA PETALS — sparse, realistic ═══ */}
      <SakuraPetals density="hero" />

      {/* ═══ THE SPRING PATH — hero as immersive world ═══ */}
      <section className="spring-hero relative overflow-hidden" style={{ background: "#F4FAF8" }}>

        {/* ── Photographic environment ── */}
        <div
          className="absolute inset-0"
          aria-hidden="true"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920&q=80')",
            backgroundSize: "cover",
            backgroundPosition: "center 35%",
            backgroundRepeat: "no-repeat",
          }}
        />

        {/* ── Atmospheric overlay — sky bleeds into content, photo shows through ── */}
        <div
          className="absolute inset-0"
          aria-hidden="true"
          style={{
            background: `linear-gradient(
              180deg,
              rgba(244,250,248,0.25) 0%,
              rgba(244,250,248,0.35) 25%,
              rgba(244,250,248,0.50) 50%,
              rgba(244,250,248,0.70) 75%,
              rgba(244,250,248,0.90) 100%
            )`,
          }}
        />

        {/* ── Sunlight — warm wash from upper right (static) ── */}
        <div
          className="absolute inset-0 pointer-events-none"
          aria-hidden="true"
          style={{
            background: "radial-gradient(ellipse 50% 40% at 78% 15%, rgba(255,240,200,0.18) 0%, transparent 70%)",
          }}
        />

        {/* ── Branch silhouettes — only at peripheral edges (static) ── */}
        <div
          className="absolute top-0 left-0 w-[28%] h-[65%] overflow-hidden pointer-events-none"
          aria-hidden="true"
          style={{ opacity: 0.10 }}
        >
          <svg viewBox="0 0 300 450" className="w-full h-full" style={{ transform: "scaleX(-1)" }}>
            <path d="M0 0 C 25 70, 50 110, 35 180 C 28 230, 45 270, 70 310" stroke="#4a2510" strokeWidth="2.5" fill="none" opacity="0.7" />
            <path d="M35 180 C 60 170, 85 160, 110 175" stroke="#4a2510" strokeWidth="1.8" fill="none" opacity="0.5" />
            <path d="M70 310 C 85 300, 105 285, 130 300" stroke="#4a2510" strokeWidth="1.5" fill="none" opacity="0.4" />
            <circle cx="110" cy="172" r="5" fill="#FFC8D6" opacity="0.45" />
            <circle cx="106" cy="168" r="3" fill="#FFB7C5" opacity="0.35" />
            <circle cx="114" cy="176" r="2.5" fill="#FFE4E8" opacity="0.25" />
          </svg>
        </div>

        <div
          className="absolute top-0 right-0 w-[28%] h-[65%] overflow-hidden pointer-events-none"
          aria-hidden="true"
          style={{ opacity: 0.10 }}
        >
          <svg viewBox="0 0 300 450" className="w-full h-full">
            <path d="M300 0 C 275 70, 250 110, 265 180 C 272 230, 255 270, 230 310" stroke="#4a2510" strokeWidth="2.5" fill="none" opacity="0.7" />
            <path d="M265 180 C 240 170, 215 160, 190 175" stroke="#4a2510" strokeWidth="1.8" fill="none" opacity="0.5" />
            <path d="M230 310 C 215 300, 195 285, 170 300" stroke="#4a2510" strokeWidth="1.5" fill="none" opacity="0.4" />
            <circle cx="190" cy="172" r="5" fill="#FFC8D6" opacity="0.45" />
            <circle cx="194" cy="168" r="3" fill="#FFB7C5" opacity="0.35" />
            <circle cx="186" cy="176" r="2.5" fill="#FFE4E8" opacity="0.25" />
          </svg>
        </div>

        {/* ── Distant landscape / horizon — lower 25% (static) ── */}
        <div
          className="absolute bottom-0 left-0 right-0 pointer-events-none"
          aria-hidden="true"
          style={{ height: "28%" }}
        >
          {/* Ground fade into content */}
          <div className="absolute inset-0" style={{
            background: "linear-gradient(to top, rgba(244,250,248,0.95) 0%, rgba(244,250,248,0.6) 50%, transparent 100%)"
          }} />
          {/* Subtle rolling hills */}
          <svg viewBox="0 0 1440 200" className="absolute bottom-0 w-full" preserveAspectRatio="none" style={{ height: "60%" }}>
            <path d="M0 120 C 180 80, 360 100, 540 90 C 720 80, 900 95, 1080 85 C 1200 78, 1350 88, 1440 84 L 1440 200 L 0 200 Z" fill="rgba(160,185,160,0.10)" />
            <path d="M0 140 C 240 115, 480 125, 720 118 C 960 112, 1200 120, 1440 115 L 1440 200 L 0 200 Z" fill="rgba(150,175,150,0.07)" />
          </svg>
        </div>

        {/* ── Film grain ── */}
        <div
          className="absolute inset-0 pointer-events-none"
          aria-hidden="true"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='256' height='256' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E")`,
            opacity: 0.05,
          }}
        />

        {/* ═══ CONTENT — sits within the environment ═══ */}
        <div className="relative z-10 min-h-screen flex flex-col">
          {/* Top bar — transparent, lets photo show through */}
          <nav className="flex items-center justify-between px-6 py-4 md:px-12">
            <Link to="/" className="flex items-center gap-2.5 group">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-[#22C55E] to-[#16A34A] flex items-center justify-center shadow-sm">
                <img src="/assets/logo/bountycode-icon.svg" alt="" className="h-5 w-5" aria-hidden="true" />
              </div>
              <span className="text-sm font-bold tracking-tight text-[#14201B]">BountyCode</span>
            </Link>
            <div className="flex items-center gap-4">
              <Link to="/login" className="text-sm font-medium text-[#14201B]/70 hover:text-[#14201B] transition-colors">
                Log in
              </Link>
              <Link to="/register" className="text-sm font-bold text-white bg-[#22C55E] hover:bg-[#16A34A] px-4 py-2 rounded-lg transition-colors shadow-sm">
                Get started
              </Link>
            </div>
          </nav>

          {/* Hero center — headline floats in the atmospheric space */}
          <div className="flex-1 flex items-center justify-center px-6 pb-20">
            <motion.div
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="text-center max-w-2xl mx-auto"
            >
              <h1
                id="main"
                className="font-display text-[2.6rem] leading-[1.1] font-extrabold tracking-tight sm:text-5xl md:text-[3.5rem] md:leading-[1.06]"
                style={{ color: "#14201B" }}
              >
                From your first line of code
                <br />
                to your first offer.
              </h1>

              <p className="mt-5 text-base sm:text-lg leading-relaxed max-w-xl mx-auto" style={{ color: "#14201B", opacity: 0.55 }}>
                BountyCode builds your role-specific path, trains your weak skills, and puts you
                through the coding challenges, company OAs and interviews that matter.
              </p>

              <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
                <Link to="/role-selector">
                  <button className="hero-cta-primary inline-flex items-center gap-2 rounded-xl px-7 py-3.5 text-sm font-bold text-white shadow-lg transition-all hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]">
                    Begin your journey
                    <ArrowRight size={15} />
                  </button>
                </Link>
                <Link to="/pricing" className="text-sm font-medium text-[#14201B]/50 hover:text-[#14201B]/80 transition-colors">
                  Explore how it works
                </Link>
              </div>
            </motion.div>
          </div>

          {/* ═══ JOURNEY PATH — the product, visualized in the landscape ═══ */}
          <div className="relative pb-8" aria-hidden="true">
            <div className="flex flex-col items-center">
              {/* Journey milestones — vertical path fading into the horizon */}
              {[
                { label: "You are here", active: true },
                { label: "Programming", active: false },
                { label: "DSA", active: false },
                { label: "Projects", active: false },
                { label: "OA", active: false },
                { label: "Interview", active: false },
                { label: "Offer", milestone: true },
              ].map((step, i) => (
                <div key={step.label} className="flex flex-col items-center" style={{ opacity: 1 - i * 0.1 }}>
                  {/* Dot */}
                  <div
                    className={`w-2 h-2 rounded-full ${
                      step.active
                        ? "bg-[#22C55E] shadow-[0_0_8px_rgba(34,197,94,0.4)]"
                        : step.milestone
                        ? "bg-[#D4A843] shadow-[0_0_8px_rgba(212,168,67,0.3)]"
                        : "bg-[#14201B]/20"
                    }`}
                  />
                  {/* Label */}
                  <span
                    className={`text-[10px] font-medium tracking-wide mt-1 mb-2 ${
                      step.active
                        ? "text-[#22C55E]"
                        : step.milestone
                        ? "text-[#D4A843]"
                        : "text-[#14201B]/25"
                    }`}
                  >
                    {step.label}
                  </span>
                  {/* Connecting line — except after last */}
                  {i < 6 && (
                    <div className="w-px h-3" style={{
                      background: `linear-gradient(to bottom, rgba(20,32,27,${0.15 - i * 0.015}), transparent)`
                    }} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ═══ PATH CONNECTOR ═══ */}
      <div className="relative h-24 bg-gradient-to-b from-[#F4FAF8] to-white">
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