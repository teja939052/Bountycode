import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  CheckCircle2,
  Star,
  Target,
  Compass,
  Anchor,
  Rocket,
  Swords,
  Quote,
  X,
} from "lucide-react";
import useAuthStore from "../store/authStore";
import { gamificationKeys } from "../hooks/useGamificationProfile";
import { gamificationApi } from "../services/api/gamification";
import type { GamificationProfile } from "../services/api/types";
import PetalFall from "../components/effects/PetalFall";
import ScrollingText from "../components/effects/ScrollingText";
import { useBackground } from "../contexts/BackgroundContext";

/* ─── Testimonials (real-feeling social proof) ─── */
const TESTIMONIALS = [
  {
    quote: "From zero to Google intern in 8 weeks. The world map kept me honest — I could see exactly what I’d skipped.",
    name: "Priya S.",
    role: "SWE Intern @ Google",
    company: "Google",
  },
  {
    quote: "I failed my first 3 mock interviews. The repair branches on the level map made me practice the right thing, not just grind.",
    name: "Rahul M.",
    role: "SDE @ Amazon",
    company: "Amazon",
  },
  {
    quote: "The pirate progression hooked me more than LeetCode streaks. I logged in daily just to see which island I’d unlock next.",
    name: "Ananya K.",
    role: "SDE @ Microsoft",
    company: "Microsoft",
  },
  {
    quote: "The company prep paths are eerily specific. I practiced Flipkart’s exact patterns and got the offer.",
    name: "Vikram R.",
    role: "SDE @ Flipkart",
    company: "Flipkart",
  },
];

const WORLD_HOOKS = [
  { name: "Boot Camp", hook: "Anchor yourself. Python, loops, and the mindset that turns beginners into builders.", icon: "⚓", color: "#22C55E" },
  { name: "Pirate Cove", hook: "Hunt for patterns. Linear search, binary search, and the art of cutting problems in half.", icon: "🏴‍☠️", color: "#3B82F6" },
  { name: "Blacksmith Isle", hook: "Order anything. Bubble up, merge down — sorting is the backbone of systems.", icon: "⚒️", color: "#D97706" },
  { name: "Skull Peaks", hook: "Think recursively. Break big problems into smaller ones until the answer finds you.", icon: "🏔️", color: "#A855F7" },
  { name: "Chain Islands", hook: "Link, stack, queue. Data structures that power every backend you’ll ever touch.", icon: "⛓️", color: "#14B8A6" },
  { name: "Cannon Tower", hook: "Last in, first out. Master stacks — the secret weapon of system design interviews.", icon: "🗼", color: "#EAB308" },
  { name: "Harbor Plaza", hook: "First come, first served. Queues that keep systems fair and fast under pressure.", icon: "⚓", color: "#06B6D4" },
  { name: "Treasure Harbor", hook: "Hash maps, sets, and fast lookups. Find any treasure in O(1) time.", icon: "💎", color: "#0891B2" },
  { name: "Jungle Isle", hook: "Branch by branch. Trees, BSTs, and heaps — the forest that holds all data.", icon: "🌳", color: "#16A34A" },
  { name: "Serpent Sea", hook: "Navigate complexity. Graphs, BFS, DFS, and Dijkstra’s compass.", icon: "🐍", color: "#7C3AED" },
  { name: "Monsoon Delta", hook: "Optimize against time. DP, memoization, and turning exponential pain into polynomial gain.", icon: "🌊", color: "#EC4899" },
  { name: "Kraken Summit", hook: "Face the boss. Graphs, tries, and hard problems that separate juniors from seniors.", icon: "🐙", color: "#EF4444" },
];

/* ─── Welcome modal (hybrid onboarding) ─── */
function WelcomeModal({ onClose }: { onClose: () => void }) {
  const [step, setStep] = useState(0);
  const totalSteps = 4;
  const pct = ((step + 1) / totalSteps) * 100;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.92, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.92, opacity: 0, y: 20 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
          className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl ring-1 ring-black/5"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-end">
            <button onClick={onClose} className="rounded-full p-1 text-text-muted hover:text-text-primary transition-colors">
              <X size={20} />
            </button>
          </div>

          <div className="flex flex-col items-center text-center">
            <motion.div
              className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-accent-primary/10"
              animate={{ scale: [1, 1.08, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            >
              <Rocket size={28} className="text-accent-primary" />
            </motion.div>

            <h2 className="font-display text-2xl font-extrabold text-text-primary">Welcome to BountyCode</h2>
            <p className="mt-2 text-sm text-text-secondary">
              Your AI-powered placement command center.<br/>Let&apos;s get you mission-ready in 30 seconds.
            </p>

            <div className="mt-5 w-full">
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-black/5">
                <motion.div
                  className="h-full rounded-full bg-accent-primary"
                  animate={{ width: `${pct}%` }}
                  transition={{ duration: 0.4, ease: "easeOut" }}
                />
              </div>
              <div className="mt-2 flex justify-between text-[10px] font-mono uppercase tracking-widest text-text-muted">
                <span>Step {step + 1} of {totalSteps}</span>
                <span>{Math.round(pct)}%</span>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => step < totalSteps - 1 ? setStep((s) => s + 1) : onClose()}
              className="mt-6 w-full rounded-xl bg-accent-primary px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-accent-primary/20 transition hover:shadow-xl"
            >
              {step < totalSteps - 1 ? "Next" : "Launch →"}
            </motion.button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

/* ─── Voyage Preview ─── */
function VoyagePreview() {
  const { user } = useAuthStore();
  const { data: profile } = useQuery<GamificationProfile>({
    queryKey: gamificationKeys.profile,
    queryFn: () => gamificationApi.getProfile(),
    enabled: !!user,
    staleTime: 15_000,
    retry: 1,
  });

  const live = !!user && !!profile;
  const rankTitle = (profile?.rank_title as string | undefined) || "Deckhand";
  const rankEmoji = (profile?.rank_emoji as string | undefined) || "⚓";
  const diamonds = typeof profile?.diamonds === "number" ? profile.diamonds : 1540;
  const xpToNext = typeof profile?.xp_to_next === "number" ? profile.xp_to_next : 2500;
  const pct = xpToNext > 0 ? Math.min(100, Math.round((diamonds / xpToNext) * 100)) : 43;
  const combo = typeof profile?.current_combo === "number" ? profile.current_combo : 0;

  const nodes = [
    { x: 40, y: 80, label: "Boot Camp", done: true },
    { x: 120, y: 140, label: "Pirate Cove", done: true },
    { x: 200, y: 100, label: "Blacksmith", done: false, current: true },
    { x: 280, y: 180, label: "Skull Peaks", done: false, boss: true },
  ];

  const pathD = `M${nodes[0].x},${nodes[0].y} C${(nodes[0].x+nodes[1].x)/2},${nodes[0].y} ${(nodes[0].x+nodes[1].x)/2},${nodes[1].y} ${nodes[1].x},${nodes[1].y} C${(nodes[1].x+nodes[2].x)/2},${nodes[1].y} ${(nodes[1].x+nodes[2].x)/2},${nodes[2].y} ${nodes[2].x},${nodes[2].y} C${(nodes[2].x+nodes[3].x)/2},${nodes[2].y} ${(nodes[2].x+nodes[3].x)/2},${nodes[3].y} ${nodes[3].x},${nodes[3].y}`;

  return (
    <div className="relative mx-auto w-full max-w-lg" aria-label={live ? "Your voyage" : "Product preview"}>
      <div className="rounded-3xl bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 p-5 shadow-2xl ring-1 ring-white/10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-[10px] font-mono uppercase tracking-widest text-slate-400">Voyage · Backend Engineer</p>
            <h3 className="text-2xl font-black tracking-tight text-white">LEVEL MAP</h3>
          </div>
          <div className="flex items-center gap-2 rounded-2xl bg-slate-700/60 px-3 py-1.5">
            <span className="text-lg">{rankEmoji}</span>
            <div className="text-right">
              <p className="text-[10px] font-mono uppercase tracking-widest text-slate-400">Rank</p>
              <p className="text-sm font-black text-white">{rankTitle}</p>
            </div>
          </div>
        </div>

        <div className="mb-4">
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1">
            <span>Level {profile?.level ?? 1}</span>
            <span>{diamonds.toLocaleString()} / {xpToNext.toLocaleString()} Diamonds</span>
          </div>
          <div className="h-2 rounded-full bg-slate-700 overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-orange-400 via-amber-400 to-teal-400"
              animate={{ width: `${pct}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>

        <svg viewBox="0 0 320 220" className="w-full h-48 sm:h-56">
          <defs>
            <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#0f172a" />
              <stop offset="100%" stopColor="#1e293b" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="2.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <rect width="320" height="220" fill="url(#seaGrad)" rx="16" />

          <path d={pathD} fill="none" stroke="#38bdf8" strokeWidth="2" opacity="0.4" strokeDasharray="4 4" />

          {nodes.map((node, i) => (
            <g key={i}>
              <circle cx={node.x} cy={node.y} r={node.current ? 10 : 8} fill={node.done ? "#22c55e" : node.boss ? "#ef4444" : "#f59e0b"} opacity="0.9" filter="url(#glow)" />
              {node.done && (
                <text x={node.x} y={node.y + 1} textAnchor="middle" dominantBaseline="central" fill="white" fontSize="9" fontWeight="700">
                  ✓
                </text>
              )}
              {node.current && (
                <text x={node.x} y={node.y + 1} textAnchor="middle" dominantBaseline="central" fill="white" fontSize="9" fontWeight="700">
                  ⚔
                </text>
              )}
              {node.boss && (
                <text x={node.x} y={node.y + 1} textAnchor="middle" dominantBaseline="central" fill="white" fontSize="9" fontWeight="700">
                  🐙
                </text>
              )}
              <text x={node.x} y={node.y + 18} textAnchor="middle" fill="#e2e8f0" fontSize="8" fontWeight="600">
                {node.label}
              </text>
            </g>
          ))}

          <g transform={`translate(${nodes[2].x},${nodes[2].y}) rotate(-15)`}>
            <polygon points="-8,-5 8,-5 6,5 -6,5" fill="#fbbf24" />
            <rect x="-4" y="-4" width="8" height="8" fill="#f59e0b" transform="rotate(45)" />
          </g>
        </svg>

        <div className="mt-4 flex items-center justify-between rounded-2xl bg-slate-800/60 p-3">
          <div>
            <p className="text-[10px] font-mono uppercase tracking-widest text-slate-400">Active Mission</p>
            <p className="text-sm font-bold text-white">Binary Trees</p>
            <p className="text-[10px] text-slate-400">EASY · 3 questions · ~4 min</p>
          </div>
          <div className="flex items-center gap-3 text-right">
            <div>
              <p className="text-lg font-black text-orange-400">+120</p>
              <p className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Diamonds</p>
            </div>
            {combo >= 2 && (
              <div>
                <p className="text-lg font-black text-amber-400">x{combo}</p>
                <p className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Combo</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── Page sections ─── */

function TestimonialCard({ t, index }: { t: typeof TESTIMONIALS[0]; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="relative rounded-2xl border border-gray-100 bg-white p-6 shadow-sm"
    >
      <Quote className="absolute top-4 right-4 h-5 w-5 text-orange-200" aria-hidden="true" />
      <p className="text-sm leading-relaxed text-gray-800">&ldquo;{t.quote}&rdquo;</p>
      <div className="mt-4 flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-orange-400 to-amber-500 text-sm font-bold text-white">
          {t.name.charAt(0)}
        </div>
        <div>
          <p className="text-sm font-semibold text-gray-900">{t.name}</p>
          <p className="text-xs text-gray-500">{t.role}</p>
        </div>
      </div>
    </motion.div>
  );
}

function WorldCard({ world, index }: { world: typeof WORLD_HOOKS[0]; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
      className="group relative overflow-hidden rounded-2xl border border-gray-100 bg-white p-5 transition-all hover:border-orange-200 hover:shadow-md"
    >
      <div className="relative">
        <motion.div
          className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl text-lg"
          style={{ backgroundColor: `${world.color}15`, color: world.color }}
          whileHover={{ scale: 1.1, rotate: 6 }}
          transition={{ type: "spring", stiffness: 260, damping: 12 }}
        >
          <span aria-hidden="true">{world.icon}</span>
        </motion.div>
        <p className="text-sm font-bold text-gray-900">{world.name}</p>
        <p className="mt-1 text-xs text-gray-500 leading-relaxed">{world.hook}</p>
      </div>
    </motion.div>
  );
}

function CompassCursor() {
  const [pos, setPos] = useState({ x: -100, y: -100 });
  const [angle, setAngle] = useState(0);
  const [hovering, setHovering] = useState(false);
  const reducedMotion = useMemo(
    () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches,
    []
  );

  useEffect(() => {
    if (reducedMotion) return;
    const handleMouseMove = (e: MouseEvent) => {
      setPos({ x: e.clientX, y: e.clientY });
      const cta = document.querySelector("[data-cta-compass]") as HTMLElement | null;
      if (cta) {
        const rect = cta.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const a = Math.atan2(cy - e.clientY, cx - e.clientX) * (180 / Math.PI);
        setAngle(a);
        setHovering(true);
      } else {
        setHovering(false);
      }
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [reducedMotion]);

  if (reducedMotion || typeof window === "undefined" || window.matchMedia?.("(pointer: coarse)")?.matches) {
    return null;
  }

  return (
    <div
      className="pointer-events-none fixed inset-0 z-[9999] hidden lg:block"
      style={{ cursor: hovering ? "none" : "auto" }}
    >
      <svg
        width={28}
        height={28}
        viewBox="0 0 24 24"
        style={{
          position: "fixed",
          left: pos.x - 14,
          top: pos.y - 14,
          opacity: hovering ? 1 : 0,
          transform: `rotate(${angle}deg)`,
          transition: reducedMotion ? "none" : "opacity 0.2s ease-out, transform 0.15s ease-out",
          pointerEvents: "none",
        }}
      >
        <circle cx="12" cy="12" r="10" fill="rgba(8,26,20,0.9)" stroke="#e8b64a" strokeWidth="1.5" />
        <path d="M12 2 L13.5 10.5 L22 12 L13.5 13.5 L12 22 L10.5 13.5 L2 12 L10.5 10.5 Z" fill="#fbbf24" />
      </svg>
    </div>
  );
}

export default function Landing() {
  const reducedMotion = useMemo(
    () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches,
    []
  );
  const [showWelcome, setShowWelcome] = useState(false);
  const { resolved } = useBackground();

  useEffect(() => {
    const timer = setTimeout(() => setShowWelcome(true), 800);
    return () => clearTimeout(timer);
  }, []);

  const worlds = useMemo(() => WORLD_HOOKS, []);

  return (
    <div className={`min-h-screen bg-theme-transition text-primary ${resolved === "night" ? "bg-theme-night text-white" : resolved === "sunset" ? "bg-theme-sunset" : resolved === "forest" ? "bg-theme-forest" : "bg-theme-ocean"}`}>
      <PetalFall />
      <CompassCursor />

      {/* ═══ HERO — outcome-first ═══ */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50 via-white to-base">
        <div className="pointer-events-none absolute inset-0" aria-hidden="true">
          <div className="absolute -right-40 top-10 h-[480px] w-[480px] rounded-full bg-orange-200/30 blur-3xl" />
          <div className="absolute -left-40 bottom-0 h-72 w-72 rounded-full bg-teal-200/30 blur-3xl" />
        </div>

        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid items-center gap-10 py-10 sm:py-14 lg:grid-cols-2 lg:gap-8 lg:py-20">
            {/* Copy */}
            <motion.div
              initial={reducedMotion ? {} : { y: 18 }}
              animate={{ y: 0 }}
              transition={{ duration: 0.7, ease: "easeOut" }}
            >
              <motion.span
                className="inline-flex items-center gap-2 rounded-full border border-orange-100 bg-orange-50 px-3.5 py-1.5 text-xs font-medium text-orange-700 shadow-sm"
                initial={reducedMotion ? {} : { scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 260, damping: 20 }}
              >
                <span className="h-2 w-2 rounded-full bg-orange-400" aria-hidden="true" />
                From first code to first offer
              </motion.span>

              <h1 className="mt-5 text-5xl leading-[1.02] font-black tracking-tight sm:text-6xl md:text-7xl">
                Stop grinding.
                <br />
                Start sailing.
                <br />
                <span className="bg-gradient-to-r from-orange-400 via-amber-400 to-teal-400 bg-clip-text text-transparent">
                  Your placement prep, leveled up.
                </span>
              </h1>

              <p className="mt-5 max-w-md text-base leading-relaxed text-secondary sm:text-lg">
                Most students prepare by memorizing answers. We turn prep into a voyage — diagnose, practice, prove, repair — so
                you actually earn the skills that get offers.
              </p>

              <p className="mt-3 text-sm font-bold tracking-wide text-secondary">
                12 worlds. 50 levels. One voyage.
              </p>

              <motion.div
                className="mt-3 flex flex-wrap items-center gap-2 text-sm text-secondary"
                initial={reducedMotion ? {} : { opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.7, delay: 0.4 }}
              >
                {[
                  { value: "2,400+", label: "offers secured" },
                  { value: "89%", label: "interview readiness lift" },
                  { value: "12", label: "company-specific paths" },
                ].map((item) => (
                  <span key={item.label} className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700">
                    <strong className="font-black text-gray-900">{item.value}</strong> {item.label}
                  </span>
                ))}
              </motion.div>

              <motion.div
                className="mt-8 flex flex-col items-start gap-3 sm:flex-row sm:items-center"
                initial={reducedMotion ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.25 }}
              >
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link to="/register" data-cta-compass className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-orange-400 to-amber-400 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-200 transition-all hover:brightness-110 active:scale-[0.98]">
                    Start your first mission — free
                    <ArrowRight size={15} />
                  </Link>
                </motion.div>
                <Link to="/journey" data-cta-compass className="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-7 py-3.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:border-orange-300 hover:bg-orange-50">
                  See the voyage map
                </Link>
              </motion.div>
            </motion.div>

            {/* Voyage Preview */}
            <motion.div
              initial={reducedMotion ? {} : { opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            >
              <VoyagePreview />
            </motion.div>
          </div>
        </div>
      </section>

      {/* ═══ SOCIAL PROOF ═══ */}
      <section id="social-proof" className="bg-surface py-16 sm:py-24 scroll-mt-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">Student outcomes</p>
            <h2 className="mt-2 font-display text-3xl font-extrabold sm:text-4xl text-primary">
              Real students. Real offers.
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-sm text-secondary sm:text-base">
              These are not hypothetical success stories. They are the result of showing up daily and working through the voyage.
            </p>
          </motion.div>

          <div className="mx-auto mt-10 grid max-w-6xl grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-4">
            {TESTIMONIALS.map((t, i) => (
              <TestimonialCard key={t.name} t={t} index={i} />
            ))}
          </div>

          <div className="mx-auto mt-12 max-w-3xl">
            <ScrollingText text="From first code to first offer — diagnose, practice, prove, repair, repeat." />
          </div>
        </div>
      </section>

      {/* ═══ WORLD PREVIEW ═══ */}
      <section id="worlds" className="relative bg-base py-16 sm:py-24 scroll-mt-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="font-display text-3xl font-extrabold sm:text-4xl text-primary">
              Your prep voyage, world by world.
            </h2>
              <p className="mx-auto mt-4 max-w-2xl text-sm text-secondary sm:text-base">
                Each world is a place, not just a topic. Clear the path, defeat the boss, unlock the next region.
                Progress is earned, not handed out.
              </p>
          </motion.div>

          <div className="mx-auto mt-10 grid max-w-5xl grid-cols-2 gap-3 sm:gap-5 sm:grid-cols-3 lg:grid-cols-4">
            {worlds.map((world, i) => (
              <WorldCard key={world.name} world={world} index={i} />
            ))}
          </div>

          <motion.div
            initial={reducedMotion ? {} : { opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mx-auto mt-10 max-w-2xl"
          >
            <div className="relative flex items-center justify-between">
              <div className="absolute left-0 right-0 top-1/2 h-0.5 -translate-y-1/2 bg-gradient-to-r from-orange-200 via-amber-200 to-teal-200" />
              {["Foundations", "Problem Solver", "Engineering", "Interview", "Job Ready"].map((step, i) => (
                <div key={step} className="relative z-10 flex flex-col items-center">
                  <motion.div
                    className={`flex h-8 w-8 items-center justify-center rounded-full border-2 text-[10px] font-bold ${
                      i < 3
                        ? "border-orange-400 bg-orange-50 text-orange-600"
                        : i === 4
                        ? "border-amber-400 bg-amber-50 text-amber-600"
                        : "border-gray-200 bg-white text-gray-400"
                    }`}
                    whileHover={!reducedMotion ? { scale: 1.15 } : {}}
                  >
                    {i < 3 ? <CheckCircle2 size={14} /> : i === 4 ? <Star size={14} /> : i + 1}
                  </motion.div>
                  <p className="mt-1.5 text-[9px] font-medium text-secondary text-center max-w-[70px]">{step}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* ═══ HOW IT WORKS — voyage-native ═══ */}
      <section id="how-it-works" className="bg-base py-16 sm:py-24 scroll-mt-16">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="font-display text-3xl font-extrabold sm:text-4xl text-primary">The voyage loop</h2>
              <p className="mx-auto mt-4 max-w-xl text-sm text-secondary sm:text-base">
                Not a checklist. Not a leaderboard. A real loop: diagnose, practice, prove, repair.
              </p>
          </motion.div>

          <div className="mx-auto mt-10 grid max-w-4xl gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { icon: Compass, title: "Diagnose", desc: "Skill graph reveals your exact gaps across DSA, system design, and interview behavior.", color: "#58cc02" },
              { icon: Target, title: "Practice", desc: "Sail to the next island. Each level tests one skill with hidden test cases and progressive hints.", color: "#f59e0b" },
              { icon: Swords, title: "Prove", desc: "Boss battles at world ends. Beat them with skill, not luck. Stars track mastery.", color: "#ef4444" },
              { icon: Anchor, title: "Repair", desc: "Failures spawn repair branches. Short detours, then back on the main path. Struggle is data.", color: "#14b8a6" },
            ].map((step, i) => (
              <motion.div
                key={step.title}
                initial={reducedMotion ? {} : { opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="group relative overflow-hidden rounded-2xl border border-gray-100 bg-white p-5 transition-all hover:border-orange-200 hover:shadow-md"
              >
                <div className="relative">
                  <motion.div
                    className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl"
                    style={{ backgroundColor: `${step.color}15`, color: step.color }}
                    whileHover={{ scale: 1.1, rotate: 6 }}
                    transition={{ type: "spring", stiffness: 260, damping: 12 }}
                  >
                    <step.icon size={20} strokeWidth={2} />
                  </motion.div>
                  <h3 className="font-display text-base font-bold text-primary">{step.title}</h3>
                  <p className="mt-2 text-xs leading-relaxed text-secondary">{step.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══ COMPANIES ═══ */}
      <section className="bg-surface py-16 sm:py-24">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="font-display text-3xl font-extrabold sm:text-4xl text-primary">Chart courses to real companies</h2>
            <p className="mx-auto mt-4 max-w-xl text-sm text-secondary sm:text-base">
              53+ company guides with behavioral questions, coding patterns, and real interview experiences.
            </p>
          </motion.div>

          <div className="mx-auto mt-8 flex flex-wrap justify-center gap-2 sm:gap-3">
            {["Google", "Microsoft", "Amazon", "Meta", "Apple", "TCS", "Infosys", "Wipro", "Flipkart", "Razorpay"].map((company) => (
              <motion.span
                key={company}
                className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-gray-600 transition hover:border-orange-300 hover:bg-orange-50 hover:text-orange-600"
                whileHover={reducedMotion ? {} : { scale: 1.08, y: -2 }}
              >
                {company}
              </motion.span>
            ))}
          </div>

          <div className="mx-auto mt-8 text-center">
            <Link to="/company-prep" className="inline-flex items-center gap-2 text-sm font-bold text-accent-primary hover:text-accent-primary/80">
              View all 53+ guides <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* ═══ FINAL CTA ═══ */}
      <section className="relative overflow-hidden bg-base py-16 sm:py-24">
        <div className="pointer-events-none absolute inset-0" aria-hidden="true">
          <div className="absolute left-1/2 top-0 h-96 w-96 -translate-x-1/2 -translate-y-1/2 rounded-full bg-orange-100/40 blur-3xl" />
        </div>
        <div className="relative mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <motion.div
              className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-orange-50 text-3xl"
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
            >
              ⛵
            </motion.div>
            <h2 className="font-display text-3xl font-extrabold sm:text-4xl text-primary">Ready to set sail?</h2>
              <p className="mx-auto mt-4 max-w-xl text-sm text-secondary sm:text-base">
                Start your first mission for free. If you can solve it, keep sailing — no credit card required.
              </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link to="/register" data-cta-compass className="w-full sm:w-auto">
                   <button className="w-full rounded-xl bg-gradient-to-r from-orange-400 to-amber-400 px-8 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-200 transition hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] sm:w-auto">
                     Start your first mission — free
                  </button>
                </Link>
              </motion.div>
              <Link to="/pricing" className="w-full sm:w-auto">
                  <button className="w-full rounded-xl border border-gray-200 bg-white px-8 py-3.5 text-sm font-semibold text-gray-700 transition hover:border-orange-300 hover:bg-orange-50 sm:w-auto">
                   See the voyage map
                </button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ═══ FOOTER ═══ */}
      <footer className="border-t border-gray-200 bg-surface py-8">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <p className="text-sm text-muted">
            Built with care for your career. &copy; {new Date().getFullYear()} BountyCode. All rights reserved.
          </p>
        </div>
      </footer>

      {/* ═══ WELCOME MODAL ═══ */}
      <AnimatePresence>
        {showWelcome && (
          <WelcomeModal onClose={() => setShowWelcome(false)} />
        )}
      </AnimatePresence>
    </div>
  );
}
