import { useCallback, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, useMotionValue, useTransform, useSpring } from "framer-motion";
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
  Target,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";

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

function AnimatedNumber({ value, suffix = "", delay = 0 }: { value: number; suffix?: string; delay?: number }) {
  const spring = useSpring(0, { stiffness: 70, damping: 18 });
  const display = useTransform(spring, (v) => Math.round(v));

  useEffect(() => {
    const t = setTimeout(() => spring.set(value), delay);
    return () => clearTimeout(t);
  }, [value, delay, spring]);

  return (
    <span className="inline-flex items-baseline">
      <motion.span>{display}</motion.span>
      <span className="text-[10px] font-semibold text-[#14201B]/40 ml-0.5">{suffix}</span>
    </span>
  );
}

function HeroOrbs() {
  const reduced = useReducedMotion();
  if (reduced) return null;
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      <motion.div
        className="absolute -top-24 -left-24 h-72 w-72 rounded-full"
        style={{ background: "radial-gradient(circle, rgba(34,197,94,0.12) 0%, transparent 70%)" }}
        animate={{ x: [0, 40, -20, 0], y: [0, -30, 20, 0] }}
        transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="absolute top-32 right-0 h-96 w-96 rounded-full"
        style={{ background: "radial-gradient(circle, rgba(20,32,27,0.06) 0%, transparent 70%)" }}
        animate={{ x: [0, -30, 20, 0], y: [0, 25, -15, 0] }}
        transition={{ duration: 22, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="absolute bottom-0 left-1/3 h-64 w-64 rounded-full"
        style={{ background: "radial-gradient(circle, rgba(212,168,67,0.08) 0%, transparent 70%)" }}
        animate={{ x: [0, 25, -25, 0], y: [0, -20, 30, 0] }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      />
    </div>
  );
}

function HeroMockup({ reduced }: { reduced: boolean }) {
  const mouseX = useMotionValue(0.5);
  const mouseY = useMotionValue(0.5);
  const springX = useSpring(mouseX, { stiffness: 180, damping: 16 });
  const springY = useSpring(mouseY, { stiffness: 180, damping: 16 });
  const rotateX = useTransform(springY, [0, 1], [6, -6]);
  const rotateY = useTransform(springX, [0, 1], [-6, 6]);
  const glare = useTransform(
    [springX, springY],
    // Framer Motion infers array callback params as `unknown`; values are numeric motion values.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ([x, y]: any) =>
      `radial-gradient(circle at ${x * 100}% ${y * 100}%, rgba(255,255,255,0.25) 0%, transparent 55%)`
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      const rect = e.currentTarget.getBoundingClientRect();
      mouseX.set((e.clientX - rect.left) / rect.width);
      mouseY.set((e.clientY - rect.top) / rect.height);
    },
    [mouseX, mouseY]
  );

  const handleMouseLeave = useCallback(() => {
    mouseX.set(0.5);
    mouseY.set(0.5);
  }, [mouseX, mouseY]);

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, y: 18, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.7, delay: 0.1, ease: "easeOut" }}
      className="relative"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ perspective: 1200 }}
    >
      <motion.div
        className="relative rounded-2xl border border-[#14201B]/10 bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.12)]"
        style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
      >
        <div className="absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
          style={{ background: glare as any }}
        />
        {/* Browser chrome */}
        <div className="flex items-center gap-2 border-b border-[#14201B]/5 px-4 py-3">
          <span className="h-2.5 w-2.5 rounded-full bg-red-400/80" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-400/80" />
          <span className="h-2.5 w-2.5 rounded-full bg-green-400/80" />
          <span className="ml-3 text-[10px] font-medium text-[#14201B]/40">placementpro.app/dashboard</span>
        </div>
        <div className="p-4 sm:p-5">
          {/* Header row */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#22C55E]/10 text-lg">👤</div>
              <div>
                <p className="text-sm font-bold text-[#0E1813]">Good morning, Alex</p>
                <p className="text-[10px] font-medium text-[#14201B]/50">SDE · 68% ready</p>
              </div>
            </div>
            <div className="relative flex h-12 w-12 items-center justify-center">
              <svg className="h-12 w-12 -rotate-90" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="none" stroke="#14201B" strokeWidth="3" opacity="0.06" />
                <motion.circle
                  cx="24" cy="24" r="20" fill="none" stroke="#22C55E" strokeWidth="3" strokeDasharray="125.6" strokeDashoffset="40.2" strokeLinecap="round"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 1.4, ease: "easeOut", delay: 0.5 }}
                />
              </svg>
              <AnimatedNumber value={68} suffix="%" delay={500} />
            </div>
          </div>

          {/* Next Mission */}
          <motion.div
            className="mt-4 rounded-xl border border-dashed border-[#14201B]/10 bg-gradient-to-r from-[#14201B]/[0.02] to-transparent p-3"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-widest text-[#22C55E]">
              <Target size={12} /> Next Mission
            </div>
            <p className="mt-1.5 text-sm font-bold text-[#0E1813]">Repair: Graph Traversal patterns</p>
            <div className="mt-2 flex items-center gap-3">
              <span className="rounded-full bg-[#22C55E]/10 px-2 py-0.5 text-[10px] font-bold text-[#22C55E]">+120 XP</span>
              <span className="text-[10px] text-[#14201B]/50">~15 min</span>
            </div>
          </motion.div>

          {/* Skill grid */}
          <motion.div
            className="mt-4 grid grid-cols-2 gap-2 sm:gap-3"
            initial="hidden"
            animate="show"
            variants={{
              hidden: { opacity: 0 },
              show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.7 } },
            }}
          >
            {[
              { label: "DSA", value: 82, color: "#22C55E", level: "Strong" },
              { label: "SQL", value: 74, color: "#22C55E", level: "Competent" },
              { label: "Interview", value: 61, color: "#f59e0b", level: "Practicing" },
              { label: "System Design", value: 43, color: "#ef4444", level: "Introduced" },
            ].map((item) => (
              <motion.div
                key={item.label}
                variants={{
                  hidden: { opacity: 0, y: 10 },
                  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 260, damping: 20 } },
                }}
                className="rounded-xl border border-[#14201B]/5 bg-[#14201B]/[0.01] p-2.5 sm:p-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-[#14201B]/60">{item.label}</span>
                  <span className="rounded-full px-1.5 py-0.5 text-[9px] font-bold" style={{ background: item.color + "18", color: item.color }}>{item.level}</span>
                </div>
                <div className="mt-2 flex items-end justify-between">
                  <span className="text-xl font-black text-[#0E1813] leading-none">
                    <AnimatedNumber value={item.value} suffix="%" delay={700 + item.value * 5} />
                  </span>
                </div>
                <div className="mt-2 h-1.5 w-full rounded-full bg-[#14201B]/5 overflow-hidden">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: item.color }}
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value}%` }}
                    transition={{ duration: 0.9, delay: 0.8, ease: "easeOut" }}
                  />
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}

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

      {/* ═══ HERO — product-first, no stock photo ═══ */}
      <section className="relative overflow-hidden bg-white">
        <HeroOrbs />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid items-center gap-10 py-12 sm:py-16 lg:grid-cols-2 lg:gap-14 lg:py-24">
            {/* Copy */}
            <motion.div
              initial={reduced ? {} : { opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, ease: "easeOut" }}
            >
              <motion.h1
                className="font-display text-[2.1rem] leading-[1.08] font-extrabold tracking-tight text-[#0E1813] sm:text-5xl md:text-6xl md:leading-[1.05]"
                initial={reduced ? {} : { opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.05 }}
              >
                Stop preparing randomly.
                <br />
                <span className="text-[#22C55E]">Prepare like your target role actually tests.</span>
              </motion.h1>

              <motion.p
                className="mt-5 text-base sm:text-lg leading-relaxed text-[#14201B]/80"
                initial={reduced ? {} : { opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.7, delay: 0.15 }}
              >
                PlacementPro maps the exact skills companies test, then builds a personal curriculum around your gaps — practice, prove, repair, repeat.
              </motion.p>

              <motion.div
                className="mt-8 flex flex-col items-start gap-3 sm:flex-row sm:items-center"
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.25 }}
              >
                <Link to="/role-selector" className="inline-flex items-center gap-2 rounded-xl bg-[#0E1813] px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]">
                  Start free
                  <ArrowRight size={15} />
                </Link>
                <Link to="/pricing" className="inline-flex items-center gap-2 rounded-xl border border-[#14201B]/10 bg-white px-6 py-3 text-sm font-semibold text-[#14201B] transition-colors hover:border-[#14201B]/20">
                  See how it works
                </Link>
              </motion.div>

              <motion.div
                className="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-[#14201B]/70"
                initial={reduced ? {} : { opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.7, delay: 0.35 }}
              >
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 size={14} className="text-[#22C55E]" />
                  Skill-graph driven practice
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 size={14} className="text-[#22C55E]" />
                  Adaptive repair on weak areas
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 size={14} className="text-[#22C55E]" />
                  Company-pattern mocks
                </span>
              </motion.div>
            </motion.div>

            {/* Product mockup — wow moment */}
            <HeroMockup reduced={reduced} />
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
        className="spring-section spring-section-pink cvauto"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Discover your role
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-600">
            Every journey begins with a destination. Pick your path.
          </p>

          <div className="mx-auto mt-12 grid max-w-3xl grid-cols-2 gap-4 sm:gap-6 sm:grid-cols-4">
            {ROLE_PATHS.map((role, i) => (
              <Link key={role.id} to="/role-selector" className="group">
                <motion.div
                  initial={reduced ? {} : { opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.15 + i * 0.08 }}
                  className="role-path-card h-full"
                >
                  <div
                    className="mx-auto mb-3 sm:mb-4 flex h-12 w-12 sm:h-14 sm:w-14 items-center justify-center rounded-xl transition-transform duration-300 group-hover:scale-110 group-hover:ring-primary/20 group-hover:border-primary/40"
                    style={{ backgroundColor: `${role.color}12`, color: role.color }}
                  >
                    <role.icon size={22} strokeWidth={1.8} />
                  </div>
                  <p className="text-sm font-bold text-gray-900 text-center">{role.title}</p>
                  <p className="mt-1 text-xs text-gray-600 text-center">{role.desc}</p>
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
        className="spring-section spring-section-green cvauto"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Each path becomes your curriculum
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-600">
            Not a generic course. A personalized roadmap built from your role, your weak areas, and your target companies.
          </p>

          <div className="mx-auto mt-10 sm:mt-12 grid max-w-3xl gap-4 sm:gap-6 sm:grid-cols-3">
            {CORE_FEATURES.slice(0, 3).map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={reduced ? {} : { opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.25 + i * 0.1 }}
              >
                <Card className="h-full">
                  <div className="mb-3 sm:mb-4 flex h-10 w-10 sm:h-11 sm:w-11 items-center justify-center rounded-xl bg-green-50 text-green-600">
                    <feature.icon size={20} strokeWidth={1.8} />
                  </div>
                  <h3 className="font-display text-base sm:text-lg font-bold text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-gray-600">{feature.desc}</p>
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
        className="spring-section cvauto"
      >
        <div className="mx-auto max-w-5xl px-4">
          <h2 className="text-center font-display text-2xl font-extrabold text-gray-900 sm:text-3xl">
            Prepare for the companies you want
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-sm text-gray-600">
            Company-specific patterns, behavioral questions, and real interview experiences.
          </p>

          <div className="mx-auto mt-8 sm:mt-10 flex flex-wrap justify-center gap-2 sm:gap-3">
            {COMPANIES.map((company) => (
              <Link
                key={company}
                to="/company-prep"
                className="flex items-center gap-1.5 sm:gap-2 rounded-full border border-gray-200 bg-white px-3 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-green-300 hover:shadow-md hover:-translate-y-0.5"
              >
                <Building2 size={12} className="text-gray-400 sm:hidden" />
                <Building2 size={14} className="text-gray-400 hidden sm:block" />
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
        className="spring-section spring-section-gold cvauto"
      >
        <div className="mx-auto max-w-3xl px-4 text-center">
          <div className="gold-glow mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-amber-50 to-yellow-100 shadow-lg">
            <Star size={36} className="text-amber-500" strokeWidth={1.5} />
          </div>

          <h2 className="font-display text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Job Ready
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base text-gray-600">
            You have completed the journey. Your skills are proven. Your resume is optimized.
            Your interview performance is real. You are ready.
          </p>

          <div className="mx-auto mt-8 sm:mt-10 grid max-w-md grid-cols-3 gap-3 sm:gap-4">
            {[
              { label: "Verified Questions", value: "2,652" },
              { label: "Mock Interviews", value: "50+" },
              { label: "Companies Covered", value: "53+" },
            ].map((stat) => (
              <div key={stat.label} className="rounded-xl border border-amber-200/60 bg-white/80 p-3 sm:p-4 shadow-sm">
                <p className="text-xl sm:text-2xl font-extrabold text-amber-600">{stat.value}</p>
                <p className="mt-1 text-[10px] sm:text-xs text-gray-600">{stat.label}</p>
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
        className="spring-section bg-white cvauto"
      >
        <div className="mx-auto max-w-3xl px-4 text-center">
          <h2 className="font-display text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Ready to start your journey?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm text-gray-600">
            Join thousands of students who landed offers at top companies. Free to start — upgrade
            anytime.
          </p>
          <div className="mt-8 sm:mt-10 flex flex-col items-center justify-center gap-3 sm:gap-4">
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
