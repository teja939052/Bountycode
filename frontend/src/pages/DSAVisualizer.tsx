import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Play, Pause, SkipBack, SkipForward, RotateCcw, Activity, ChevronLeft, ChevronRight } from "lucide-react";
import AlgorithmVisualizer from "../components/AlgorithmVisualizer";
import { generateTrace, generateInputFor } from "../utils/traceGenerator";

const ALGORITHMS = {
  sorting: [
    { id: "bubble", name: "Bubble Sort", complexity: "O(n²)", best: "O(n)", avg: "O(n²)", worst: "O(n²)", space: "O(1)" },
    { id: "selection", name: "Selection Sort", complexity: "O(n²)", best: "O(n²)", avg: "O(n²)", worst: "O(n²)", space: "O(1)" },
    { id: "insertion", name: "Insertion Sort", complexity: "O(n²)", best: "O(n)", avg: "O(n²)", worst: "O(n²)", space: "O(1)" },
    { id: "merge", name: "Merge Sort", complexity: "O(n log n)", best: "O(n log n)", avg: "O(n log n)", worst: "O(n log n)", space: "O(n)" },
    { id: "quick", name: "Quick Sort", complexity: "O(n log n)", best: "O(n log n)", avg: "O(n log n)", worst: "O(n²)", space: "O(log n)" },
  ],
  searching: [
    { id: "linear", name: "Linear Search", complexity: "O(n)", best: "O(1)", avg: "O(n)", worst: "O(n)", space: "O(1)" },
    { id: "binary", name: "Binary Search", complexity: "O(log n)", best: "O(1)", avg: "O(log n)", worst: "O(log n)", space: "O(1)" },
  ],
  graph: [
    { id: "bfs", name: "Breadth-First Search", complexity: "O(V+E)", best: "O(1)", avg: "O(V+E)", worst: "O(V+E)", space: "O(V)" },
    { id: "dfs", name: "Depth-First Search", complexity: "O(V+E)", best: "O(1)", avg: "O(V+E)", worst: "O(V+E)", space: "O(V)" },
    { id: "dijkstra", name: "Dijkstra Shortest Path", complexity: "O((V+E) log V)", best: "O(V log V)", avg: "O((V+E) log V)", worst: "O((V+E) log V)", space: "O(V)" },
  ],
  data_structure: [
    { id: "stack", name: "Stack Operations", complexity: "O(1)", best: "O(1)", avg: "O(1)", worst: "O(1)", space: "O(n)" },
    { id: "queue", name: "Queue Operations", complexity: "O(1)", best: "O(1)", avg: "O(1)", worst: "O(1)", space: "O(n)" },
    { id: "heap", name: "Binary Heap", complexity: "O(log n)", best: "O(1)", avg: "O(log n)", worst: "O(log n)", space: "O(n)" },
  ],
};

export default function DSAVisualizer() {
  const reduced = useReducedMotion();
  const [category, setCategory] = useState("searching");
  const [selectedAlgo, setSelectedAlgo] = useState("binary");
  const [traceData, setTraceData] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const trace = generateTrace(selectedAlgo, generateInputFor(selectedAlgo));
    setTraceData(trace);
    setCurrentStep(0);
  }, [selectedAlgo]);

  const regenerate = useCallback(() => {
    setTraceData(generateTrace(selectedAlgo, generateInputFor(selectedAlgo)));
    setCurrentStep(0);
  }, [selectedAlgo]);

  const algoInfo = ALGORITHMS[category]?.find((a) => a.id === selectedAlgo);
  const totalSteps = traceData?.steps?.length || 0;

  return (
    <div className="page-surface min-h-screen py-6 px-4 max-w-6xl mx-auto">
      <motion.div
        initial={reduced ? {} : { opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="mb-6"
      >
        <div className="flex items-center gap-3 mb-2">
          <Activity size={28} className="text-primary" />
          <h1 className="text-2xl font-black text-text-primary">DSA Visualizer</h1>
        </div>
        <p className="text-sm text-text-muted">Step through algorithm execution and watch data structures change in real-time.</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Controls */}
        <div className="space-y-4">
          <div className="rounded-[16px] border border-border bg-surface p-1 flex flex-col gap-0.5 shadow-card">
            {Object.entries(ALGORITHMS).map(([cat, algos]) => (
              <button
                key={cat}
                onClick={() => { setCategory(cat); setSelectedAlgo(algos[0].id); }}
                className={`py-2.5 px-3 rounded-[10px] text-xs font-mono uppercase tracking-wider text-left transition-all ${
                  category === cat
                    ? "bg-primary-soft text-primary-dark border border-primary/30"
                    : "text-text-muted hover:text-text-primary"
                }`}
              >
                <span className="block text-[10px] text-text-muted mb-0.5">{cat}</span>
                <span className="font-bold">{algos[0].name}</span>
              </button>
            ))}
          </div>

          <div className="space-y-1">
            {(ALGORITHMS[category] || []).map((algo) => (
              <button
                key={algo.id}
                onClick={() => setSelectedAlgo(algo.id)}
                className={`w-full text-left p-2.5 rounded-[10px] border transition-all text-xs ${
                  selectedAlgo === algo.id
                    ? "border-primary bg-primary-soft text-primary-dark"
                    : "border-border bg-white text-text-muted hover:text-text-primary"
                }`}
              >
                <div className="font-bold">{algo.name}</div>
                <div className="text-[10px] font-mono mt-0.5 text-text-muted">TC: {algo.complexity}</div>
              </button>
            ))}
          </div>

          <button
            onClick={regenerate}
            className="w-full py-2.5 rounded-[10px] bg-primary text-text-primary text-xs font-medium hover:bg-primary-dark transition-colors flex items-center justify-center gap-2"
          >
            <RotateCcw size={14} /> Generate New Data
          </button>
        </div>

        {/* Visualization */}
        <div className="lg:col-span-3 space-y-6">
          {algoInfo && (
            <motion.div
              initial={reduced ? {} : { opacity: 0 }}
              animate={{ opacity: 1 }}
              className="rounded-[16px] p-6 bg-white border border-border shadow-card"
            >
              <div className="flex items-start gap-4">
                <div className="p-3 rounded-[10px] bg-primary-soft">
                  <Activity size={20} className="text-primary" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-bold text-text-primary">{algoInfo.name}</h2>
                    <div className="flex items-center gap-2 text-xs text-text-muted">
                      <span>Step {currentStep + 1} of {totalSteps}</span>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-3 mt-3">
                    <div className="px-2 py-1 bg-surface-2 rounded text-[10px] font-mono">
                      <span className="text-text-muted">Complexity:</span> {algoInfo.complexity}
                    </div>
                    <div className="px-2 py-1 bg-surface-2 rounded text-[10px] font-mono">
                      <span className="text-text-muted">Best:</span> <span className="text-primary">{algoInfo.best}</span>
                    </div>
                    <div className="px-2 py-1 bg-surface-2 rounded text-[10px] font-mono">
                      <span className="text-text-muted">Worst:</span> <span className="text-red">{algoInfo.worst}</span>
                    </div>
                    <div className="px-2 py-1 bg-surface-2 rounded text-[10px] font-mono">
                      <span className="text-text-muted">Space:</span> {algoInfo.space}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {traceData ? (
            <div className="rounded-[16px] p-6 bg-white border border-border shadow-card">
              <AlgorithmVisualizer traceData={traceData} code={traceData.code || ""} language={traceData.language || "python"} />
            </div>
          ) : (
            <div className="rounded-[16px] p-6 bg-white border border-border shadow-card">
              <div className="py-12 flex items-center justify-center">
                <p className="text-sm text-text-muted">Generating visualization…</p>
              </div>
            </div>
          )}

          {/* Playback controls */}
          {traceData && totalSteps > 0 && (
            <motion.div
              initial={reduced ? {} : { opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="rounded-[16px] p-6 bg-white border border-border shadow-card"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-mono uppercase tracking-wider text-text-muted">Execution</h3>
                <div className="text-xs text-text-muted">
                  Step {currentStep + 1} / {totalSteps}
                </div>
              </div>

              <div className="h-2 bg-border rounded-full overflow-hidden mb-4">
                <div
                  className="h-full bg-primary rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
                />
              </div>

              <div className="flex items-center justify-center gap-4">
                <button
                  onClick={() => setCurrentStep(0)}
                  className="p-2 rounded-[10px] text-text-muted hover:text-primary hover:bg-primary-soft transition-colors"
                >
                  <SkipBack size={16} />
                </button>
                <button
                  onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                  className="p-2 rounded-[10px] text-text-muted hover:text-primary hover:bg-primary-soft transition-colors"
                >
                  <ChevronLeft size={18} />
                </button>
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="p-3 rounded-[10px] bg-primary text-text-primary hover:bg-primary-dark transition-colors"
                >
                  {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                </button>
                <button
                  onClick={() => setCurrentStep(Math.min(totalSteps - 1, currentStep + 1))}
                  className="p-2 rounded-[10px] text-text-muted hover:text-primary hover:bg-primary-soft transition-colors"
                >
                  <ChevronRight size={18} />
                </button>
                <button
                  onClick={() => setCurrentStep(totalSteps - 1)}
                  className="p-2 rounded-[10px] text-text-muted hover:text-primary hover:bg-primary-soft transition-colors"
                >
                  <SkipForward size={16} />
                </button>
              </div>

              <div className="mt-4 text-center">
                <div className="w-full h-px bg-border mb-3" />
                <p className="text-sm text-text-muted">
                  "Why did the algorithm take this path?"
                </p>
                <div className="mt-2 flex justify-center gap-6 text-sm">
                  <label className="flex items-center gap-2">
                    <input type="radio" name="predict" className="text-primary" defaultChecked />
                    <span className="text-text-muted">target &lt; mid</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="radio" name="predict" className="text-primary" />
                    <span className="text-text-muted">target &gt; mid</span>
                  </label>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
