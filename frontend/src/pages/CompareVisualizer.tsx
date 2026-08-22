import { useState, useEffect, useRef, useMemo, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play, RotateCcw, ArrowLeft, BarChart3, GitBranch, Search,
  Layers, ChevronRight, Cpu,
  Share2, Network, TreePine,
} from "lucide-react";
import AlgorithmVisualizer from "../components/AlgorithmVisualizer";
import { normalizeTemplateTrace } from "../utils/traceGenerator";

const ALGO_COMPLEXITIES: Record<string, { time: string; space: string }> = {
  bfs: { time: "O(V+E)", space: "O(V)" },
  dfs: { time: "O(V+E)", space: "O(V)" },
  bubble: { time: "O(n²)", space: "O(1)" },
  quick: { time: "O(n log n)", space: "O(log n)" },
  merge: { time: "O(n log n)", space: "O(n)" },
  linear: { time: "O(n)", space: "O(1)" },
  binary: { time: "O(log n)", space: "O(1)" },
  dijkstra: { time: "O((V+E) log V)", space: "O(V)" },
  bellman_ford: { time: "O(VE)", space: "O(V)" },
  prim: { time: "O(E log V)", space: "O(V)" },
  kruskal: { time: "O(E log E)", space: "O(V)" },
};

const ALGO_NAMES = {
  bfs: "BFS", dfs: "DFS", bubble: "Bubble Sort", quick: "Quick Sort",
  merge: "Merge Sort", linear: "Linear Search", binary: "Binary Search",
  dijkstra: "Dijkstra", bellman_ford: "Bellman-Ford", prim: "Prim's",
  kruskal: "Kruskal's",
};

const COMPARISON_META = {
  sorting_bfs_vs_dfs: { gradient: "from-emerald-500/20 to-cyan-500/20" },
  sorting_bubble_vs_quick: { gradient: "from-amber-500/20 to-orange-500/20" },
  sorting_merge_vs_quick: { gradient: "from-indigo-500/20 to-purple-500/20" },
  search_linear_vs_binary: { gradient: "from-blue-500/20 to-teal-500/20" },
  dijkstra_vs_bellman: { gradient: "from-violet-500/20 to-pink-500/20" },
  prim_vs_kruskal: { gradient: "from-rose-500/20 to-amber-500/20" },
};

const COMPARISON_ICONS = [GitBranch, BarChart3, Layers, Search, Network, TreePine];

function getComplexityKey(algoId, algoName) {
  const lower = (algoId || algoName || "").toLowerCase();
  if (lower.includes("bfs")) return "bfs";
  if (lower.includes("dfs")) return "dfs";
  if (lower.includes("bubble")) return "bubble";
  if (lower.includes("quick")) return "quick";
  if (lower.includes("merge")) return "merge";
  if (lower.includes("linear")) return "linear";
  if (lower.includes("binary")) return "binary";
  if (lower.includes("dijkstra")) return "dijkstra";
  if (lower.includes("bellman")) return "bellman_ford";
  if (lower.includes("prim")) return "prim";
  if (lower.includes("kruskal")) return "kruskal";
  return null;
}

function Badge({ children, color = "indigo" }) {
  const map = { indigo: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30", emerald: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30", amber: "bg-amber-500/20 text-amber-300 border-amber-500/30", blue: "bg-blue-500/20 text-blue-300 border-blue-500/30", purple: "bg-purple-500/20 text-purple-300 border-purple-500/30", cyan: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30" };
  return <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold border ${map[color] || map.indigo}`}>{children}</span>;
}

function ComparisonCard({ comparison, index, onClick }) {
  const Icon = COMPARISON_ICONS[index % COMPARISON_ICONS.length];
  const meta = COMPARISON_META[comparison.id] || {};
  const grad = meta.gradient || "from-indigo-500/20 to-purple-500/20";

  return (
    <motion.button
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.4 }}
      onClick={() => onClick(comparison)}
      className="group relative overflow-hidden rounded-2xl border border-black/10 bg-white/90 p-5 text-left transition-all duration-300 hover:border-indigo-500/40 hover:shadow-[0_0_30px_-5px_rgba(99,102,241,0.12)] shadow-sm card-rpg"
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${grad} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
      <div className="relative z-10 flex flex-col gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-black/5 border border-black/5 text-indigo-500 group-hover:scale-110 transition-transform duration-300">
            <Icon className="w-5 h-5" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-bold text-text-primary truncate">{comparison.title}</h3>
            <p className="text-xs text-brand-muted font-mono mt-0.5">{comparison.id}</p>
          </div>
          <ChevronRight className="w-4 h-4 text-brand-muted group-hover:text-indigo-500 group-hover:translate-x-1 transition-all" />
        </div>
        <p className="text-xs text-brand-secondary leading-relaxed line-clamp-2">{comparison.description}</p>
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
    </motion.button>
  );
}

function StatsRow({ label, value1, value2, color1 = "text-cyan-400", color2 = "text-purple-400" }) {
  return (
    <div className="flex items-center justify-between py-2 px-3 rounded-lg bg-black/5 border border-black/10">
      <span className="text-xs text-brand-secondary font-mono w-20 shrink-0">{label}</span>
      <div className="flex items-center gap-4 flex-1 justify-center">
        <span className={`text-xs font-mono font-bold ${color1}`}>{value1}</span>
        <span className="text-[10px] text-brand-muted font-bold">VS</span>
        <span className={`text-xs font-mono font-bold ${color2}`}>{value2}</span>
      </div>
    </div>
  );
}

export default function CompareVisualizer() {
  const [comparisons, setComparisons] = useState([]);
  const [selectedComparison, setSelectedComparison] = useState(null);
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState(null);

  const viz1Ref = useRef(null);
  const viz2Ref = useRef(null);
  const syncTokenRef = useRef(0);
  const [syncToken, setSyncToken] = useState(0);
  const pendingActionRef = useRef(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/v1/visualizations/compare", { credentials: "include" })
      .then(r => r.json())
      .then(data => setComparisons(data.comparisons || []))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const loadDetail = useCallback(async (comparison) => {
    setSelectedComparison(comparison);
    setDetailLoading(true);
    setDetail(null);
    try {
      const res = await fetch(`/api/v1/visualizations/compare/${comparison.id}`, { credentials: "include" });
      const data = await res.json();
      setDetail(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setDetailLoading(false);
    }
  }, []);

  const handleBack = () => {
    setSelectedComparison(null);
    setDetail(null);
  };

  const algo1Trace = useMemo(() => {
    if (!detail || !detail.algorithms || detail.algorithms.length < 1) return null;
    const algo = detail.algorithms[0];
    const ck = getComplexityKey(algo.id, algo.name);
    const comp = ck ? ALGO_COMPLEXITIES[ck] : { time: "—", space: "—" };
    const trace = normalizeTemplateTrace({ type: algo.type, steps: algo.steps || [], example_input: algo.example_input });
    return {
      ...trace,
      time_complexity: comp.time || "—",
      space_complexity: comp.space || "—",
    };
  }, [detail]);

  const algo2Trace = useMemo(() => {
    if (!detail || !detail.algorithms || detail.algorithms.length < 2) return null;
    const algo = detail.algorithms[1];
    const ck = getComplexityKey(algo.id, algo.name);
    const comp = ck ? ALGO_COMPLEXITIES[ck] : { time: "—", space: "—" };
    const trace = normalizeTemplateTrace({ type: algo.type, steps: algo.steps || [], example_input: algo.example_input });
    return {
      ...trace,
      time_complexity: comp.time || "—",
      space_complexity: comp.space || "—",
    };
  }, [detail]);

  const triggerAction = useCallback((action) => {
    pendingActionRef.current = action;
    syncTokenRef.current += 1;
    setSyncToken(syncTokenRef.current);
  }, []);

  const handlePlayAll = () => triggerAction("toggle");
  const handleResetAll = () => triggerAction("reset");

  const handleSpeedChange = (newSpeed) => {
    triggerAction(`speed:${newSpeed}`);
  };

  useEffect(() => {
    const action = pendingActionRef.current;
    if (!action) return;
    pendingActionRef.current = null;

    const refs = [viz1Ref, viz2Ref];
    if (action === "toggle") {
      refs.forEach(ref => {
        if (!ref.current) return;
        const btns = ref.current.querySelectorAll("button");
        for (const btn of btns) {
          const t = btn.textContent?.trim() || "";
          if (t.includes("Play") || t.includes("Pause")) {
            btn.click();
            break;
          }
        }
      });
    } else if (action === "reset") {
      refs.forEach(ref => {
        if (!ref.current) return;
        const resetBtn = ref.current.querySelector('button[title="Reset"]');
        if (resetBtn) resetBtn.click();
      });
    } else if (action.startsWith("speed:")) {
      const targetSpeed = action.split(":")[1];
      refs.forEach(ref => {
        if (!ref.current) return;
        const btns = ref.current.querySelectorAll("button");
        for (const btn of btns) {
          if (btn.textContent?.trim() === `${targetSpeed}x`) {
            btn.click();
            break;
          }
        }
      });
    }
  }, [syncToken]);

  const algo1 = detail?.algorithms?.[0];
  const algo2 = detail?.algorithms?.[1];

  const speedOptions = [0.5, 1, 2, 4];

  return (
    <div className="page-surface min-h-screen py-6 px-4 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 rounded-xl bg-indigo-500/15 border border-indigo-500/30 text-indigo-400 pixel-float">
            <Share2 className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Algorithm Arena</h1>
            <p className="text-xs text-brand-muted font-mono mt-0.5">Side-by-side algorithm comparison</p>
          </div>
        </div>
      </motion.div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* List View */}
      {!selectedComparison && (
        <div>
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="h-32 rounded-2xl bg-white/75 border border-black/5 shadow-sm animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {comparisons.map((comp, idx) => (
                <ComparisonCard key={comp.id} comparison={comp} index={idx} onClick={loadDetail} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Detail View */}
      {selectedComparison && (
        <AnimatePresence mode="wait">
          <motion.div key="detail" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col gap-6">
            {/* Back + Title Bar */}
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <button onClick={handleBack} className="p-2 rounded-xl bg-white border border-black/10 hover:bg-black/5 text-text-primary transition-colors shadow-sm">
                  <ArrowLeft className="w-4 h-4" />
                </button>
                <div>
                  <h2 className="text-lg font-bold text-text-primary">{detail?.title || selectedComparison.title}</h2>
                  <p className="text-xs text-brand-muted">{detail?.description || selectedComparison.description}</p>
                </div>
              </div>
            </div>

            {detailLoading ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {[1, 2].map(i => (
                  <div key={i} className="h-64 rounded-2xl bg-white/75 border border-black/5 shadow-sm animate-pulse" />
                ))}
              </div>
            ) : detail ? (
              <>
                {/* Stats Comparison Card */}
                <motion.div
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="relative overflow-hidden rounded-2xl border border-black/10 bg-white/90 p-5 shadow-sm card-rpg"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/8 via-purple-500/5 to-transparent pointer-events-none" />
                  <div className="relative z-10 flex flex-col gap-4">
                    <div className="flex items-center justify-between pb-3 border-b border-black/10">
                      <div className="flex items-center gap-3">
                        <Cpu className="w-4 h-4 text-indigo-400" />
                        <span className="text-xs font-bold text-brand-secondary uppercase tracking-wider font-mono">Complexity Comparison</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono text-indigo-400 font-bold">{algo1?.name || "Algo 1"}</span>
                        <span className="text-[10px] text-slate-600 font-bold">⚡</span>
                        <span className="text-xs font-mono text-purple-400 font-bold">{algo2?.name || "Algo 2"}</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 gap-2">
                      <StatsRow label="Time" value1={algo1Trace?.time_complexity || "—"} value2={algo2Trace?.time_complexity || "—"} color1="text-cyan-400" color2="text-purple-400" />
                      <StatsRow label="Space" value1={algo1Trace?.space_complexity || "—"} value2={algo2Trace?.space_complexity || "—"} color1="text-emerald-400" color2="text-amber-400" />
                    </div>
                    <div className="flex flex-wrap items-center gap-3 pt-2">
                      <Badge color="indigo">{algo1?.type || "Algo"}</Badge>
                      <span className="text-[10px] text-brand-muted">vs</span>
                      <Badge color="purple">{algo2?.type || "Algo"}</Badge>
                    </div>
                  </div>
                </motion.div>

                {/* Global Controls */}
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl bg-white/90 border border-black/10 shadow-sm"
                >
                  <div className="flex items-center gap-2">
                    <button onClick={handleResetAll} className="p-2 rounded-lg bg-white border border-black/10 hover:bg-black/5 text-text-primary transition-colors" title="Reset All">
                      <RotateCcw className="w-4 h-4" />
                    </button>
                    <button onClick={handlePlayAll} className="px-4 py-2 rounded-xl font-medium text-xs flex items-center gap-2 transition-all bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/25">
                      <Play className="w-3.5 h-3.5 fill-current" /> Play Both
                    </button>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-brand-muted font-mono">Speed</span>
                    <div className="flex items-center gap-1 bg-white border border-black/10 rounded-lg p-0.5 shadow-sm">
                      {speedOptions.map(spd => (
                        <button key={spd} onClick={() => handleSpeedChange(spd)}
                          className="px-2.5 py-1 rounded-md text-[11px] font-mono text-brand-secondary hover:text-text-primary hover:bg-black/5 transition-colors">
                          {spd}x
                        </button>
                      ))}
                    </div>
                  </div>
                </motion.div>

                {/* Side-by-side Visualizers */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Algo 1 */}
                  <div ref={viz1Ref} className="flex flex-col gap-3">
                    <div className="flex items-center gap-2 px-1">
                      <div className="w-2 h-2 rounded-full bg-indigo-500" />
                      <span className="text-xs font-mono font-bold text-indigo-300">{algo1?.name || "Algorithm 1"}</span>
                      <span className="text-[10px] text-slate-500 font-mono">· {algo1?.id}</span>
                    </div>
                    {algo1Trace ? (
                      <AlgorithmVisualizer traceData={algo1Trace} code={algo1Trace.code} language={algo1Trace.language} />
                    ) : (
                      <div className="h-40 rounded-2xl bg-white/80 border border-black/5 flex items-center justify-center text-brand-muted text-xs shadow-sm">
                        No trace data available
                      </div>
                    )}
                  </div>

                  {/* Algo 2 */}
                  <div ref={viz2Ref} className="flex flex-col gap-3">
                    <div className="flex items-center gap-2 px-1">
                      <div className="w-2 h-2 rounded-full bg-purple-500" />
                      <span className="text-xs font-mono font-bold text-purple-300">{algo2?.name || "Algorithm 2"}</span>
                      <span className="text-[10px] text-slate-500 font-mono">· {algo2?.id}</span>
                    </div>
                    {algo2Trace ? (
                      <AlgorithmVisualizer traceData={algo2Trace} code={algo2Trace.code} language={algo2Trace.language} />
                    ) : (
                      <div className="h-40 rounded-2xl bg-white/80 border border-black/5 flex items-center justify-center text-brand-muted text-xs shadow-sm">
                        No trace data available
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : null}
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
}
