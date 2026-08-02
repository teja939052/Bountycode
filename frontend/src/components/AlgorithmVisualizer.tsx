import { useState, useEffect, useRef, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play, Pause, ChevronLeft, ChevronRight, RotateCcw,
  Sparkles, Zap, Eye, Volume2, VolumeX, Cpu, Layers,
  CheckCircle, ArrowRight, Code2, HelpCircle, GitBranch
} from "lucide-react";
import { playSound } from "../utils/soundEffects";

/* ── Data Structure Renderers ──────────────────────────────── */

function ArrayViz({ data, activeIndices = [], pointers = {} }) {
  if (!Array.isArray(data) || data.length === 0) return null;
  const maxVal = Math.max(...data.map(v => typeof v === "number" ? v : 0), 1);
  return (
    <div className="flex flex-col gap-4 items-center my-2 py-2 overflow-x-auto">
      <div className="flex items-end justify-center gap-2">
        {data.map((val, idx) => {
          const isActive = activeIndices.includes(idx);
          const matchedPointer = Object.entries(pointers).find(([_, i]) => i === idx);
          const height = typeof val === "number" ? Math.max(32, (val / maxVal) * 80) : 48;
          return (
            <div key={idx} className="flex flex-col items-center gap-1">
              {matchedPointer && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">
                  {matchedPointer[0]}
                </span>
              )}
              <motion.div layout animate={{ scale: isActive ? 1.12 : 1 }}
                className={`w-11 rounded-lg border flex items-center justify-center font-mono font-bold text-xs shadow-lg transition-colors ${
                  isActive ? "bg-amber-500/25 border-amber-400 text-amber-200" : "bg-slate-900 border-slate-700 text-slate-200"
                }`} style={{ height: `${height}px` }}>
                <span>{String(val)}</span>
              </motion.div>
              <span className="text-[10px] text-slate-500 font-mono">[{idx}]</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function BarChartViz({ data, activeIndices = [], comparing = [] }) {
  if (!Array.isArray(data) || data.length === 0) return null;
  const maxVal = Math.max(...data.map(v => typeof v === "number" ? v : 0), 1);
  return (
    <div className="flex items-end justify-center gap-[3px] h-[140px] my-2 px-4 overflow-x-auto">
      {data.map((val, idx) => {
        const h = typeof val === "number" ? Math.max(8, (val / maxVal) * 130) : 20;
        const isActive = activeIndices.includes(idx);
        const isComparing = comparing.includes(idx);
        return (
          <motion.div key={idx} layout animate={{ height: h }}
            className={`min-w-[18px] rounded-t-md transition-colors ${
              isActive ? "bg-amber-400" : isComparing ? "bg-rose-400" : "bg-indigo-500"
            }`} title={`[${idx}] = ${val}`}>
            <span className="text-[9px] text-white/80 font-mono w-full text-center block pt-1">{val}</span>
          </motion.div>
        );
      })}
    </div>
  );
}

function TreeViz({ tree, activeNode = null, highlightedNodes = [] }) {
  if (!tree || !tree.nodes || tree.nodes.length === 0) return null;
  const nodes = tree.nodes;
  const edges = tree.edges || [];

  const levels = {};
  nodes.forEach(n => {
    const depth = n.depth ?? 0;
    if (!levels[depth]) levels[depth] = [];
    levels[depth].push(n);
  });
  const maxDepth = Math.max(...Object.keys(levels).map(Number), 0);
  const nodeSize = 36;

  return (
    <div className="flex flex-col items-center my-2 py-2 overflow-x-auto">
      {Array.from({ length: maxDepth + 1 }, (_, d) => {
        const levelNodes = levels[d] || [];
        return (
          <div key={d} className="flex items-center justify-center gap-6 relative">
            {levelNodes.map(node => {
              const isActive = node.id === activeNode;
              const isHighlighted = highlightedNodes.includes(node.id);
              const isNull = node.value === null || node.value === undefined;
              return (
                <motion.div key={node.id} layout animate={{ scale: isActive ? 1.15 : 1 }}
                  className={`relative flex items-center justify-center rounded-full border-2 font-mono font-bold text-xs shadow-lg transition-all ${
                    isNull ? "w-6 h-6 border-dashed border-slate-600 bg-transparent" :
                    isActive ? "w-9 h-9 bg-amber-500/25 border-amber-400 text-amber-200 shadow-amber-500/30" :
                    isHighlighted ? "w-9 h-9 bg-emerald-500/25 border-emerald-400 text-emerald-200" :
                    "w-9 h-9 bg-slate-900 border-slate-600 text-slate-200"
                  }`}>
                  {!isNull && <span>{node.value}</span>}
                </motion.div>
              );
            })}
          </div>
        );
      })}
      {/* Edge indicators */}
      {edges.length > 0 && (
        <div className="mt-2 text-[10px] text-slate-500 font-mono">
          {edges.length} edge{edges.length !== 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}

function LinkedListViz({ nodes, activeNode = null, direction = "right" }) {
  if (!Array.isArray(nodes) || nodes.length === 0) return null;
  return (
    <div className="flex items-center justify-center gap-1 my-2 py-2 overflow-x-auto">
      {nodes.map((node, idx) => {
        const val = typeof node === "object" ? node.value : node;
        const isActive = (typeof node === "object" ? node.id : idx) === activeNode;
        const isNull = val === null || val === undefined;
        return (
          <div key={idx} className="flex items-center">
            <motion.div layout animate={{ scale: isActive ? 1.1 : 1 }}
              className={`flex items-center gap-1 rounded-lg border-2 px-3 py-2 font-mono font-bold text-xs shadow-lg ${
                isNull ? "border-dashed border-slate-600 bg-transparent text-slate-500" :
                isActive ? "bg-amber-500/25 border-amber-400 text-amber-200" :
                "bg-slate-900 border-indigo-500/50 text-slate-200"
              }`}>
              <span>{isNull ? "null" : val}</span>
              {typeof node === "object" && node.address && (
                <span className="text-[9px] text-slate-500 font-normal">@{node.address}</span>
              )}
            </motion.div>
            {idx < nodes.length - 1 && (
              <div className="flex items-center text-indigo-400 mx-1">
                <ArrowRight className="w-4 h-4" />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

function StackViz({ stack, activeIndex = null }) {
  if (!Array.isArray(stack) || stack.length === 0) return null;
  return (
    <div className="flex flex-col-reverse items-center gap-1 my-2 py-2">
      {stack.map((val, idx) => {
        const isActive = idx === activeIndex;
        const isTop = idx === stack.length - 1;
        return (
          <div key={idx} className="flex items-center gap-2">
            {isTop && <span className="text-[10px] text-amber-400 font-bold font-mono">TOP →</span>}
            <motion.div layout animate={{ scale: isActive ? 1.05 : 1 }}
              className={`w-32 h-9 rounded-lg border flex items-center justify-center font-mono font-bold text-xs ${
                isActive ? "bg-amber-500/25 border-amber-400 text-amber-200" :
                "bg-slate-900 border-slate-700 text-slate-200"
              }`}>
              {String(val)}
            </motion.div>
          </div>
        );
      })}
      <div className="w-36 h-0.5 bg-slate-600 rounded" />
    </div>
  );
}

function QueueViz({ queue, activeIndex = null }) {
  if (!Array.isArray(queue) || queue.length === 0) return null;
  return (
    <div className="flex items-center gap-1 my-2 py-2 overflow-x-auto">
      <span className="text-[10px] text-amber-400 font-bold font-mono rotate-180" style={{ writingMode: "vertical-rl" }}>FRONT →</span>
      {queue.map((val, idx) => {
        const isActive = idx === activeIndex;
        const isBack = idx === queue.length - 1;
        return (
          <div key={idx} className="flex flex-col items-center gap-1">
            <motion.div layout animate={{ scale: isActive ? 1.05 : 1 }}
              className={`w-14 h-10 rounded-lg border flex items-center justify-center font-mono font-bold text-xs ${
                isActive ? "bg-amber-500/25 border-amber-400 text-amber-200" :
                "bg-slate-900 border-slate-700 text-slate-200"
              }`}>
              {String(val)}
            </motion.div>
            {isBack && <span className="text-[10px] text-indigo-400 font-bold font-mono">← BACK</span>}
          </div>
        );
      })}
    </div>
  );
}

function MatrixViz({ matrix, activeCells = [] }) {
  if (!Array.isArray(matrix) || matrix.length === 0) return null;
  return (
    <div className="flex flex-col items-center my-2 py-2 gap-[2px] overflow-x-auto">
      {matrix.map((row, r) => (
        <div key={r} className="flex gap-[2px]">
          {Array.isArray(row) ? row.map((val, c) => {
            const isActive = activeCells.some(([ar, ac]) => ar === r && ac === c);
            return (
              <motion.div key={c} layout animate={{ scale: isActive ? 1.1 : 1 }}
                className={`w-9 h-9 rounded border flex items-center justify-center font-mono font-bold text-[11px] ${
                  isActive ? "bg-amber-500/25 border-amber-400 text-amber-200" :
                  "bg-slate-900 border-slate-700 text-slate-300"
                }`}>
                {String(val)}
              </motion.div>
            );
          }) : null}
        </div>
      ))}
    </div>
  );
}

function GraphViz({ graph, visitedNodes = [], currentNode = null, activeEdges = [] }) {
  if (!graph || !graph.nodes || graph.nodes.length === 0) return null;
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const nodeMap = {};
  nodes.forEach((n, i) => { nodeMap[n.id] = { ...n, index: i }; });
  const positions = {};
  const radius = 80;
  const cx = 120, cy = 100;
  nodes.forEach((n, i) => {
    const angle = (i / Math.max(1, nodes.length)) * 2 * Math.PI - Math.PI / 2;
    positions[n.id] = {
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    };
  });
  return (
    <div className="flex justify-center my-4">
      <svg width="260" height="220" className="max-w-full">
        {edges.map((e, i) => {
          const from = positions[e.from];
          const to = positions[e.to];
          if (!from || !to) return null;
          const isActive = activeEdges.some(([a, b]) => (a === e.from && b === e.to) || (a === e.to && b === e.from));
          const midX = (from.x + to.x) / 2;
          const midY = (from.y + to.y) / 2;
          const arrowX = to.x + (from.x - to.x) * 0.15;
          const arrowY = to.y + (from.y - to.y) * 0.15;
          return (
            <g key={i}>
              <line x1={from.x} y1={from.y} x2={arrowX} y2={arrowY}
                stroke={isActive ? "#fbbf24" : "#475569"} strokeWidth={isActive ? 2.5 : 1.5}
                strokeDasharray={e.weight ? "4 2" : "none"} />
              {e.weight && (
                <text x={midX} y={midY - 4} textAnchor="middle"
                  className="text-[9px] fill-amber-400 font-mono">{e.weight}</text>
              )}
            </g>
          );
        })}
        {nodes.map((n) => {
          const pos = positions[n.id];
          if (!pos) return null;
          const isVisited = visitedNodes.includes(n.id);
          const isActive = currentNode === n.id;
          return (
            <g key={n.id}>
              <circle cx={pos.x} cy={pos.y} r={isActive ? 22 : 18}
                fill={isVisited ? "#22c55e" : isActive ? "#fbbf24" : "#1e293b"}
                stroke={isVisited ? "#4ade80" : isActive ? "#f59e0b" : "#475569"}
                strokeWidth={isActive ? 3 : 2} />
              <text x={pos.x} y={pos.y + 4} textAnchor="middle"
                className={`font-mono text-[11px] font-bold ${
                  isVisited ? "fill-emerald-300" : isActive ? "fill-amber-200" : "fill-slate-500"
                }`}>
                {n.label || n.id}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function HashMapViz({ mapData, activeKey = null, activeBucket = null }) {
  if (!mapData || typeof mapData !== "object" || Object.keys(mapData).length === 0) return null;
  const entries = Object.entries(mapData);
  const bucketCount = Math.max(8, Math.ceil(entries.length / 2));
  const buckets = Array.from({ length: bucketCount }, () => []);
  entries.forEach(([k, v]) => {
    const hash = Math.abs(k.toString().split("").reduce((a, c) => a + c.charCodeAt(0), 0));
    buckets[hash % bucketCount].push({ key: k, value: v });
  });
  return (
    <div className="flex flex-col gap-2 my-2 overflow-x-auto">
      <div className="grid grid-cols-4 gap-2">
        {buckets.map((bucket, i) => (
          <div key={i} className="flex flex-col items-center gap-1">
            <span className="text-[10px] text-slate-500 font-mono">[{i}]</span>
            <div className={`border-2 border-dashed rounded-lg p-1 min-h-[30px] w-full flex flex-col items-center justify-center ${
              activeBucket === i ? "border-amber-400 bg-amber-500/5" : "border-slate-700"
            }`}>
              {bucket.map((item, j) => {
                const isKeyActive = activeKey === item.key;
                return (
                  <div key={j} className={`text-[10px] font-mono text-center px-1 py-0.5 rounded ${
                    isKeyActive ? "bg-amber-500/20 text-amber-200 border border-amber-400/30" : "text-slate-400"
                  }`}>
                    {item.key} → {String(item.value)}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SortingViz({ data, activeIndices = [], sortedIndices = [], comparing = [] }) {
  if (!Array.isArray(data) || data.length === 0) return null;
  const maxVal = Math.max(...data.map(v => typeof v === "number" ? v : 0), 1);
  return (
    <div className="flex items-end justify-center gap-[3px] h-[140px] my-2 px-4 overflow-x-auto">
      {data.map((val, idx) => {
        const h = typeof val === "number" ? Math.max(8, (val / maxVal) * 130) : 20;
        const isComparing = comparing.includes(idx);
        const isSorted = sortedIndices.includes(idx);
        const isActive = activeIndices.includes(idx);
        let bgClass = "bg-slate-700";
        let borderClass = "border-slate-700";
        if (isComparing) { bgClass = "bg-amber-500"; borderClass = "border-amber-400"; }
        else if (isSorted) { bgClass = "bg-emerald-500"; borderClass = "border-emerald-400"; }
        else if (isActive) { bgClass = "bg-indigo-500"; borderClass = "border-indigo-400"; }
        return (
          <motion.div key={idx} layout
            className={`w-5 rounded border transition-all ${bgClass} ${borderClass} flex items-end justify-center font-mono font-bold text-[9px] text-white`}
            style={{ height: `${h}px` }}>
            {val}
          </motion.div>
        );
      })}
    </div>
  );
}

/* ── Main Visualizer ───────────────────────────────────────── */

export default function AlgorithmVisualizer({ traceData, code, language = "python" }) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const playTimerRef = useRef(null);

  const steps = traceData?.steps || [];
  const currentStep = steps[currentStepIndex] || {};
  const totalSteps = steps.length;

  useEffect(() => { setCurrentStepIndex(0); setIsPlaying(false); }, [traceData]);

  useEffect(() => {
    if (isPlaying && totalSteps > 0) {
      const delay = 1200 / speed;
      playTimerRef.current = setTimeout(() => {
        if (currentStepIndex < totalSteps - 1) {
          setCurrentStepIndex(prev => prev + 1);
          if (soundEnabled) playSound.step();
        } else { setIsPlaying(false); }
      }, delay);
    }
    return () => { if (playTimerRef.current) clearTimeout(playTimerRef.current); };
  }, [isPlaying, currentStepIndex, totalSteps, speed, soundEnabled]);

  const handleNext = () => { if (currentStepIndex < totalSteps - 1) { setCurrentStepIndex(p => p + 1); if (soundEnabled) playSound.step(); } };
  const handlePrev = () => { if (currentStepIndex > 0) { setCurrentStepIndex(p => p - 1); if (soundEnabled) playSound.step(); } };
  const handleReset = () => { setIsPlaying(false); setCurrentStepIndex(0); if (soundEnabled) playSound.step(); };

  const codeLines = code ? code.split("\n") : [];
  const variables = currentStep.variables || {};
  const pointers = currentStep.pointers || {};
  const activeIndices = currentStep.active_indices || [];

  // Detect visualization type from step data
  const vizType: string = useMemo(() => {
    if (currentStep.tree) return "tree";
    if (currentStep.linked_list) return "linked_list";
    if (currentStep.stack) return "stack";
    if (currentStep.queue) return "queue";
    if (currentStep.matrix) return "matrix";
    if (currentStep.graph) return "graph";
    if (currentStep.hash_map) return "hash_map";
    if (traceData?.visualization_type === "sorting") return "sorting";
    const arr = currentStep.array_data || variables.nums || variables.arr;
    if (Array.isArray(arr)) {
      if (traceData?.visualization_type === "sorting" || currentStep.comparing) return "sorting";
      return "array";
    }
    return "none";
  }, [currentStep, traceData, variables]);

  const renderVisualization = () => {
    switch (vizType) {
      case "tree":
        return <TreeViz tree={currentStep.tree} activeNode={currentStep.active_node} highlightedNodes={currentStep.highlighted_nodes || []} />;
      case "linked_list":
        return <LinkedListViz nodes={currentStep.linked_list} activeNode={currentStep.active_node} />;
      case "stack":
        return <StackViz stack={currentStep.stack} activeIndex={currentStep.active_index} />;
      case "queue":
        return <QueueViz queue={currentStep.queue} activeIndex={currentStep.active_index} />;
      case "matrix":
        return <MatrixViz matrix={currentStep.matrix} activeCells={currentStep.active_cells || []} />;
      case "graph":
        return <GraphViz graph={currentStep.graph} visitedNodes={currentStep.visited_nodes || []} currentNode={currentStep.current_node} activeEdges={currentStep.active_edges || []} />;
      case "hash_map":
        return <HashMapViz mapData={variables} activeKey={currentStep.active_key} activeBucket={currentStep.active_bucket} />;
      case "sorting":
        return <SortingViz data={currentStep.sorting_data || variables.nums || variables.arr || []} activeIndices={activeIndices} sortedIndices={currentStep.sorted_indices || []} comparing={currentStep.comparing || []} />;
      case "bars":
        return <BarChartViz data={currentStep.array_data || variables.nums || variables.arr || []} activeIndices={activeIndices} comparing={currentStep.comparing || []} />;
      case "array": {
        const arr = currentStep.array_data || variables.nums || variables.arr;
        return <ArrayViz data={arr} activeIndices={activeIndices} pointers={pointers} />;
      }
      default:
        return (
          <div className="text-center text-slate-500 py-8 text-xs italic">
            Executing step... Variable state active in inspector below.
          </div>
        );
    }
  };

  const vizLabel = { array: "Array / Pointers", bars: "Bar Chart", tree: "Binary Tree", linked_list: "Linked List", stack: "Stack", queue: "Queue", matrix: "Matrix / Grid", graph: "Graph", hash_map: "Hash Map", sorting: "Sorting", none: "Runtime State" }[vizType] || "State";

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-6 shadow-2xl flex flex-col gap-5 text-slate-100 overflow-hidden">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="font-bold text-lg text-white flex items-center gap-2">
              Algorithm Visualizer
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                {totalSteps} steps
              </span>
              {traceData?.algorithm && (
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-mono">
                  {traceData.algorithm}
                </span>
              )}
            </h3>
            <p className="text-xs text-slate-400">
              Step through code execution, inspect variables, watch data structures change
            </p>
            {traceData?.source && (
              <p className="mt-1 text-[11px] text-slate-500 font-mono">
                Source: {traceData.source}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-3">
          {traceData?.time_complexity && (
            <div className="text-xs px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-cyan-400 font-mono flex items-center gap-1.5">
              <Zap className="w-3.5 h-3.5" /> {traceData.time_complexity}
            </div>
          )}
          {traceData?.space_complexity && (
            <div className="text-xs px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-purple-400 font-mono flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5" /> {traceData.space_complexity}
            </div>
          )}
          <button onClick={() => setSoundEnabled(!soundEnabled)}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors">
            {soundEnabled ? <Volume2 className="w-4 h-4 text-indigo-400" /> : <VolumeX className="w-4 h-4 text-slate-500" />}
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <button onClick={handleReset} className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors" title="Reset">
            <RotateCcw className="w-4 h-4" />
          </button>
          <button onClick={handlePrev} disabled={currentStepIndex === 0}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 transition-colors">
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button onClick={() => setIsPlaying(!isPlaying)}
            className={`px-4 py-2 rounded-xl font-medium text-sm flex items-center gap-2 transition-all shadow-lg ${
              isPlaying ? "bg-amber-500/20 text-amber-300 border border-amber-500/40" : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/25"
            }`}>
            {isPlaying ? <><Pause className="w-4 h-4" /> Pause</> : <><Play className="w-4 h-4 fill-current" /> Play</>}
          </button>
          <button onClick={handleNext} disabled={currentStepIndex === totalSteps - 1}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 transition-colors">
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
        <div className="flex items-center gap-4 flex-1 max-w-md">
          <span className="text-xs font-mono text-slate-400 whitespace-nowrap">
            {totalSteps > 0 ? currentStepIndex + 1 : 0}/{totalSteps}
          </span>
          <input type="range" min={0} max={Math.max(0, totalSteps - 1)} value={currentStepIndex}
            onChange={e => { setCurrentStepIndex(Number(e.target.value)); if (soundEnabled) playSound.step(); }}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500" />
        </div>
        <div className="flex items-center gap-1.5 text-xs font-mono bg-slate-900 border border-slate-800 p-1 rounded-xl">
          {[0.5, 1, 2, 4].map(spd => (
            <button key={spd} onClick={() => setSpeed(spd)}
              className={`px-2.5 py-1 rounded-lg transition-colors ${speed === spd ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"}`}>
              {spd}x
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Code Panel */}
        <div className="lg:col-span-5 bg-slate-950/80 border border-slate-800 rounded-xl p-4 flex flex-col gap-3 font-mono text-xs overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800">
            <span className="flex items-center gap-1.5 text-slate-300 font-semibold">
              <Code2 className="w-4 h-4 text-indigo-400" /> Source ({language})
            </span>
            <span className="text-indigo-400 font-bold">L{currentStep.line || "-"}</span>
          </div>
          <div className="overflow-y-auto max-h-[320px] space-y-1 pr-1">
            {codeLines.map((lineText, idx) => {
              const lineNum = idx + 1;
              const isCurrent = currentStep.line === lineNum;
              return (
                <div key={idx} className={`flex items-center gap-3 px-2.5 py-1 rounded-md transition-all ${
                  isCurrent ? "bg-indigo-500/20 border-l-4 border-indigo-500 text-indigo-200 font-bold" : "text-slate-400 hover:bg-slate-900/60"
                }`}>
                  <span className="w-6 text-right text-slate-600 select-none">{lineNum}</span>
                  <span className="whitespace-pre overflow-x-auto">{lineText || " "}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Visualization + Variables */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 flex flex-col gap-3 min-h-[180px]">
            <div className="text-xs font-semibold text-slate-400 flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-slate-300">
                <Cpu className="w-4 h-4 text-emerald-400" /> Data Structure
              </span>
              <span className="text-emerald-400 font-mono text-[11px]">{vizLabel}</span>
            </div>
            {renderVisualization()}
          </div>

          {/* Variable Inspector */}
          <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 flex flex-col gap-3">
            <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <Eye className="w-4 h-4 text-cyan-400" /> Variables
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
              {Object.keys(variables).length > 0 ? (
                Object.entries(variables).map(([k, v]) => (
                  <div key={k} className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 flex flex-col gap-0.5 font-mono">
                    <span className="text-[11px] text-slate-400 font-sans">{k}</span>
                    <span className="text-sm font-bold text-cyan-300 truncate">
                      {typeof v === "object" ? JSON.stringify(v) : String(v)}
                    </span>
                  </div>
                ))
              ) : (
                <div className="col-span-full text-center text-slate-500 text-xs py-2">No active variables</div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Explanation Footer */}
      <div className="bg-indigo-950/30 border border-indigo-500/30 rounded-xl p-4 flex items-start gap-3">
        <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400 shrink-0 mt-0.5">
          <HelpCircle className="w-5 h-5" />
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider">
            {currentStep.action || "Step execution"}
          </span>
          <p className="text-sm text-slate-200 leading-relaxed">
            {currentStep.explanation || "Tracing execution and state changes..."}
          </p>
        </div>
      </div>
    </div>
  );
}
