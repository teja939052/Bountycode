import { useState, useEffect, useMemo, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronRight, TrendingUp, TrendingDown, Minus, Target,
  BarChart3, Network, CheckCircle2, Circle,
} from "lucide-react";
import api from "../services/api";

type SkillGraph = {
  categories: Record<string, {
    name: string;
    score: number;
    skills: Record<string, { score: number; attempts: number; last_practiced?: string }>;
  }>;
  overall_score: number;
};

type Readiness = {
  overall_readiness: number;
  readiness_level: string;
  category_scores: Record<string, number>;
  categories: Record<string, { score: number; weight: number; details?: Record<string, any> }>;
  weak_areas_count: number;
  strong_domains_count: number;
  recommendations: Array<{ category: string; current_score: number; priority: string; message: string }>;
};

const LEVEL_COLORS: Record<number, string> = {
  0: "#6b7280",
  1: "#ef4444",
  2: "#f59e0b",
  3: "#3b82f6",
  4: "#22c55e",
  5: "#a855f7",
};

function masteryLevel(attempts: number, score: number): number {
  if (attempts === 0) return 0;
  if (attempts <= 2) return 1;
  if (attempts <= 5) return score >= 0.5 ? 3 : 2;
  if (attempts <= 10) return score >= 0.75 ? 4 : 3;
  if (attempts <= 20) return score >= 0.9 ? 5 : 4;
  return score >= 0.9 ? 5 : 4;
}

function LevelBadge({ attempts, score }: { attempts: number; score: number }) {
  const lvl = masteryLevel(attempts, score);
  const labels = ["Unknown", "Introduced", "Practicing", "Competent", "Strong", "Mastered"];
  const color = LEVEL_COLORS[lvl];
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold" style={{ background: color + "18", color }}>
      {lvl === 5 ? <CheckCircle2 size={10} /> : <Circle size={10} />}
      {labels[lvl]}
    </span>
  );
}

function TrendIcon({ value }: { value: number }) {
  if (value > 0) return <TrendingUp size={12} className="text-emerald-500" />;
  if (value < 0) return <TrendingDown size={12} className="text-red-500" />;
  return <Minus size={12} className="text-gray-400" />;
}

function MiniBar({ value, max = 100, color = "#3b82f6" }: { value: number; max?: number; color?: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return (
    <div className="h-1.5 w-full rounded-full bg-white/10 overflow-hidden">
      <motion.div
        className="h-full rounded-full"
        style={{ background: color }}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      />
    </div>
  );
}

type Node = {
  id: string;
  label: string;
  x: number;
  y: number;
  score: number;
  attempts: number;
  radius?: number;
};

function buildNeighborhoodNodes(categoryId: string, category: SkillGraph["categories"][string]): Node[] {
  const nodes: Node[] = [];
  const cx = 0;
  const cy = 0;

  nodes.push({ id: categoryId, label: category.name, x: cx, y: cy, score: category.score, attempts: 1, radius: 18 });

  const skills = Object.entries(category.skills || {});
  const skillRadius = 110;
  skills.forEach(([skillId, skill], idx) => {
    const angle = (2 * Math.PI * idx) / Math.max(skills.length, 1) - Math.PI / 2;
    const sx = cx + skillRadius * Math.cos(angle);
    const sy = cy + skillRadius * Math.sin(angle);
    nodes.push({ id: `${categoryId}:${skillId}`, label: skillId.replace(/_/g, " "), x: sx, y: sy, score: skill.score, attempts: skill.attempts, radius: 12 });
  });

  return nodes;
}

function SkillGraphCanvas({ categoryId, category, onBack }: { categoryId: string; category: SkillGraph["categories"][string]; onBack: () => void }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const hoverRef = useRef<{ x: number; y: number; label: string; score: number; attempts: number } | null>(null);
  const [tooltip, setTooltip] = useState<{ left: number; top: number; label: string; score: number; attempts: number } | null>(null);

  const nodes = useMemo(() => buildNeighborhoodNodes(categoryId, category), [categoryId, category]);

  const draw = useCallback((width: number, height: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;

    ctx.strokeStyle = "rgba(0,0,0,0.08)";
    ctx.lineWidth = 1;
    nodes.forEach((node) => {
      if (node.id === categoryId) return;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(node.x + cx, node.y + cy);
      ctx.stroke();
    });

    nodes.forEach((node) => {
      const lvl = masteryLevel(node.attempts, node.score);
      const color = LEVEL_COLORS[lvl];
      const r = node.radius ?? (node.id === categoryId ? 18 : 12);

      ctx.beginPath();
      ctx.arc(node.x + cx, node.y + cy, r, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = "#374151";
      ctx.font = "10px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(node.label, node.x + cx, node.y + cy + r + 12);
    });
  }, [categoryId, nodes]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const measure = () => {
      const width = container.clientWidth;
      const height = Math.max(320, Math.min(520, window.innerHeight * 0.55));
      draw(width, height);
    };

    measure();

    const observer = new ResizeObserver(() => measure());
    observer.observe(container);
    return () => observer.disconnect();
  }, [draw]);

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const width = rect.width;
    const height = rect.height;
    const cx = width / 2;
    const cy = height / 2;

    const hit = nodes.find((node) => {
      const nx = node.x + cx;
      const ny = node.y + cy;
      const r = node.radius ?? (node.id === categoryId ? 18 : 12);
      const dx = mx - nx;
      const dy = my - ny;
      return dx * dx + dy * dy <= (r + 4) * (r + 4);
    });

    if (hit) {
      setTooltip({ left: e.clientX - rect.left + 12, top: e.clientY - rect.top + 12, label: hit.label, score: hit.score, attempts: hit.attempts });
      hoverRef.current = hit;
    } else {
      setTooltip(null);
      hoverRef.current = null;
    }
  }, [categoryId, nodes]);

  const handleMouseLeave = useCallback(() => {
    setTooltip(null);
    hoverRef.current = null;
  }, []);

  return (
    <div className="space-y-3">
      <button onClick={onBack} className="text-xs text-brand-muted hover:text-text-primary flex items-center gap-1">
        <ChevronRight size={12} className="rotate-180" /> Back to graph view
      </button>
      <div ref={containerRef} className="relative rounded-xl border border-black/5 bg-white overflow-hidden">
        <canvas
          ref={canvasRef}
          className="w-full h-auto block"
          style={{ height: Math.max(320, Math.min(520, window.innerHeight * 0.55)) }}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        {tooltip && (
          <div
            className="absolute pointer-events-none rounded-lg bg-gray-900/90 text-white px-2 py-1.5 text-[10px] leading-tight"
            style={{ left: tooltip.left, top: tooltip.top }}
          >
            <div className="font-semibold capitalize">{tooltip.label}</div>
            <div className="text-gray-300">{Math.round(tooltip.score * 100)}% · {tooltip.attempts} attempts</div>
          </div>
        )}
      </div>
      <p className="text-[10px] text-brand-muted">Only the selected category neighborhood is rendered. Hover a node for details.</p>
    </div>
  );
}

export default function SkillGraph() {
  const [graph, setGraph] = useState<SkillGraph | null>(null);
  const [readiness, setReadiness] = useState<Readiness | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<"overview" | "skill" | "graph">("overview");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [g, r] = await Promise.all([
        api.gamification.getSkillGraph().catch(() => null),
        api.gamification.getReadinessScore().catch(() => null),
      ]);
      setGraph((g as any) || null);
      setReadiness((r as any) || null);
    } catch {} finally {
      setLoading(false);
    }
  };

  const categories = graph?.categories || {};
  const catEntries = useMemo(() => Object.entries(categories), [categories]);
  const selectedCat = selectedCategory ? categories[selectedCategory] : null;

  const openGraph = useCallback((catId: string) => {
    setSelectedCategory(catId);
    setView("graph");
  }, []);

  const openSkillDetail = useCallback((catId: string) => {
    setSelectedCategory(catId);
    setView("skill");
  }, []);

  if (loading) {
    return (
      <div className="page-surface min-h-screen py-12 px-4">
        <div className="max-w-5xl mx-auto space-y-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-24 bg-white/5 rounded-2xl animate-pulse border border-white/10" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="page-surface min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
              <Network size={22} className="text-indigo-400" /> Capability Graph
            </h1>
            <p className="text-xs sm:text-sm text-gray-400 mt-1">Your skill ontology, mastery, and readiness in one view.</p>
          </div>
          <div className="flex gap-2">
            {["overview", "skill", "graph"].map((v) => (
              <button
                key={v}
                onClick={() => { setView(v as any); if (v !== "skill") setSelectedCategory(null); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                  view === v ? "glass-button text-white" : "bg-white/5 text-gray-400 hover:text-white"
                }`}
              >
                {v === "skill" ? "Skill Detail" : v}
              </button>
            ))}
          </div>
        </motion.div>

        <AnimatePresence mode="wait">
          {view === "overview" && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="space-y-4"
            >
              {readiness && (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {[
                    { label: "Overall Readiness", value: `${Math.round(readiness.overall_readiness)}%`, sub: readiness.readiness_level, color: "text-indigo-600" },
                    { label: "Strong Domains", value: readiness.strong_domains_count, sub: "mastered areas", color: "text-emerald-600" },
                    { label: "Weak Areas", value: readiness.weak_areas_count, sub: "needs focus", color: "text-amber-600" },
                    { label: "Categories", value: Object.keys(readiness.category_scores || {}).length, sub: "tracked", color: "text-text-primary" },
                  ].map((stat, i) => (
                    <motion.div
                      key={stat.label}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="gamification-card rounded-2xl p-4"
                    >
                      <p className="text-[10px] uppercase tracking-wide text-gray-500 font-semibold">{stat.label}</p>
                      <p className={`text-2xl font-black mt-1 ${stat.color}`}>{stat.value}</p>
                      <p className="text-[10px] text-gray-500 mt-0.5">{stat.sub}</p>
                    </motion.div>
                  ))}
                </div>
              )}

              <div className="gamification-card rounded-2xl overflow-hidden">
                <div className="px-4 py-3 border-b border-white/10 flex items-center gap-2">
                  <BarChart3 size={14} className="text-gray-400" />
                  <span className="text-xs font-semibold text-white uppercase tracking-wide">Capability Overview</span>
                </div>
                <div className="divide-y divide-white/10">
                  {catEntries.map(([catId, cat], idx) => {
                    const score = readiness?.category_scores?.[catId] ?? cat.score * 10;
                    const trend = score - 50;
                    return (
                      <motion.button
                        key={catId}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: idx * 0.03 }}
                        onClick={() => openSkillDetail(catId)}
                        className="w-full px-4 py-3 flex items-center gap-3 hover:bg-white/5 transition-colors text-left"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-white truncate">{cat.name}</span>
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-mono font-semibold" style={{ color: score >= 70 ? "#34d399" : score >= 40 ? "#fbbf24" : "#f87171" }}>
                                {Math.round(score)}%
                              </span>
                              <TrendIcon value={trend} />
                            </div>
                          </div>
                          <MiniBar value={score} max={100} color={score >= 70 ? "#34d399" : score >= 40 ? "#fbbf24" : "#f87171"} />
                        </div>
                        <ChevronRight size={14} className="text-gray-400 flex-shrink-0" />
                      </motion.button>
                    );
                  })}
                </div>
              </div>

              {readiness?.recommendations && readiness.recommendations.length > 0 && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="gamification-card rounded-2xl overflow-hidden">
                  <div className="px-4 py-3 border-b border-white/10 flex items-center gap-2">
                    <Target size={14} className="text-gray-400" />
                    <span className="text-xs font-semibold text-white uppercase tracking-wide">Recommendations</span>
                  </div>
                  <div className="divide-y divide-white/10">
                    {readiness.recommendations.slice(0, 5).map((rec, i) => (
                      <motion.div key={i} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }} className="px-4 py-3 flex items-start gap-2">
                        <span className={`mt-0.5 px-1.5 py-0.5 rounded text-[9px] font-bold uppercase ${
                          rec.priority === "high" ? "bg-red-500/20 text-red-300" :
                          rec.priority === "medium" ? "bg-amber-500/20 text-amber-200" :
                          "bg-indigo-500/20 text-indigo-200"
                        }`}>
                          {rec.priority}
                        </span>
                        <p className="text-xs text-gray-300 leading-relaxed">{rec.message}</p>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}

          {view === "skill" && (
            <motion.div
              key="skill"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="space-y-4"
            >
              {!selectedCat ? (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="gamification-card rounded-2xl overflow-hidden">
                  <div className="px-4 py-3 border-b border-white/10">
                    <span className="text-xs font-semibold text-white uppercase tracking-wide">Select a Category</span>
                  </div>
                  <div className="divide-y divide-white/10">
                    {catEntries.map(([catId, cat], idx) => {
                      const score = readiness?.category_scores?.[catId] ?? cat.score * 10;
                      return (
                        <motion.button
                          key={catId}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.03 }}
                          onClick={() => openSkillDetail(catId)}
                          className="w-full px-4 py-3 flex items-center gap-3 hover:bg-white/5 transition-colors text-left"
                        >
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-sm font-medium text-white">{cat.name}</span>
                              <span className="text-xs font-mono font-semibold" style={{ color: score >= 70 ? "#34d399" : score >= 40 ? "#fbbf24" : "#f87171" }}>
                                {Math.round(score)}%
                              </span>
                            </div>
                            <p className="text-[10px] text-gray-400">{Object.keys(cat.skills || {}).length} skills tracked</p>
                          </div>
                          <ChevronRight size={14} className="text-gray-400" />
                        </motion.button>
                      );
                    })}
                  </div>
                </motion.div>
              ) : (
                <div className="space-y-3">
                  <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-2">
                    <button onClick={() => setSelectedCategory(null)} className="text-xs text-gray-400 hover:text-white flex items-center gap-1 transition-colors">
                      <ChevronRight size={12} className="rotate-180" /> Back
                    </button>
                  </motion.div>
                  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="gamification-card rounded-2xl overflow-hidden">
                    <div className="px-4 py-3 border-b border-white/10 flex items-center justify-between">
                      <span className="text-xs font-semibold text-white uppercase tracking-wide">{selectedCat.name} — Skills</span>
                      <span className="text-[10px] text-gray-400">{Object.keys(selectedCat.skills || {}).length} skills</span>
                    </div>
                    <div className="divide-y divide-white/10">
                      {Object.entries(selectedCat.skills || {}).map(([skillId, skill], idx) => {
                        const lvl = masteryLevel(skill.attempts, skill.score);
                        const pct = Math.round(skill.score * 100);
                        const color = LEVEL_COLORS[lvl];
                        return (
                          <motion.div
                            key={skillId}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.03 }}
                            className="px-4 py-3"
                          >
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs font-medium text-white capitalize">{skillId.replace(/_/g, " ")}</span>
                              <LevelBadge attempts={skill.attempts} score={skill.score} />
                            </div>
                            <MiniBar value={pct} max={100} color={color} />
                            <div className="flex items-center justify-between mt-1">
                              <span className="text-[10px] text-gray-400 font-mono">{pct}%</span>
                              <span className="text-[10px] text-gray-400">{skill.attempts} attempts</span>
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                  </motion.div>
                  <motion.button
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                    onClick={() => openGraph(selectedCategory!)}
                    className="w-full py-2.5 rounded-xl glass-button text-white text-xs font-semibold flex items-center justify-center gap-2"
                  >
                    <Network size={14} /> Open Graph View
                  </motion.button>
                </div>
              )}
            </motion.div>
          )}

          {view === "graph" && selectedCategory && categories[selectedCategory] && (
            <motion.div
              key="graph"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
            >
              <SkillGraphCanvas categoryId={selectedCategory} category={categories[selectedCategory]} onBack={() => setView("overview")} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
