import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Play, Pause, RotateCcw, BarChart3, Layers, Activity } from "lucide-react";
import AlgorithmVisualizer from "../components/AlgorithmVisualizer";
import CelebrationOverlay from "../components/CelebrationOverlay";
import { playSound } from "../utils/soundEffects";

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
  const [category, setCategory] = useState("sorting");
  const [selectedAlgo, setSelectedAlgo] = useState("bubble");
  const [data, setData] = useState([]);
  const [running, setRunning] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [showCelebration, setShowCelebration] = useState(false);
  const [traceData, setTraceData] = useState(null);

  useEffect(() => {
    const size = 12;
    const arr = Array.from({ length: size }, () => Math.floor(Math.random() * 90) + 10);
    setData(arr);
    setTraceData(null);
    setRunning(false);
  }, [selectedAlgo]);

  const algoInfo = ALGORITHMS[category]?.find((a) => a.id === selectedAlgo);

  return (
    <div className="min-h-screen py-6 px-4 max-w-6xl mx-auto">
      <CelebrationOverlay show={showCelebration} type="perfect" message="Algorithm Mastered!" onClose={() => setShowCelebration(false)} />
      <motion.div initial={reduced ? {} : { opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Activity size={28} className="text-primary-500" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">DSA Visualizer</h1>
        </div>
        <p className="text-gray-500 dark:text-gray-400 text-sm">Step through algorithm execution and watch data structures change in real-time.</p>
      </motion.div>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="space-y-4">
          <div className="bg-gray-900/40 rounded-xl p-1 flex flex-col gap-0.5">
            {Object.entries(ALGORITHMS).map(([cat, algos]) => (
              <button key={cat} onClick={() => { setCategory(cat); setSelectedAlgo(algos[0].id); }} className={`py-2.5 px-3 rounded-lg text-xs font-mono uppercase tracking-wider text-left transition-all ${category === cat ? "bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30" : "text-gray-500 hover:text-gray-300"}`}>
                <span className="block text-[10px] text-gray-500 mb-0.5">{cat}</span>
                <span className="font-bold">{algos[0].name}</span>
              </button>
            ))}
          </div>
          <div className="space-y-1">
            {(ALGORITHMS[category] || []).map((algo) => (
              <button key={algo.id} onClick={() => setSelectedAlgo(algo.id)} className={`w-full text-left p-2.5 rounded-lg border transition-all text-xs ${selectedAlgo === algo.id ? "bg-primary-50 dark:bg-primary-900/20 border-primary-300 dark:border-primary-700 text-primary-700 dark:text-primary-400" : "bg-gray-50 dark:bg-slate-800/30 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800/50"}`}>
                <div className="font-bold">{algo.name}</div>
                <div className="text-[10px] font-mono mt-0.5">{algo.complexity}</div>
              </button>
            ))}
          </div>
          <button onClick={() => { const size = 12; const arr = Array.from({ length: size }, () => Math.floor(Math.random() * 90) + 10); setData(arr); setTraceData(null); setRunning(false); }} className="w-full py-2.5 bg-gray-900 hover:bg-gray-800 text-white text-xs font-medium rounded-lg transition-colors flex items-center justify-center gap-2"><RotateCcw size={14} /> Generate New Data</button>
        </div>
        <div className="lg:col-span-3 space-y-6">
          {algoInfo && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl"><Layers size={20} className="text-primary-600" /></div>
                <div className="flex-1">
                  <h2 className="text-lg font-bold text-gray-900 dark:text-white">{algoInfo.name}</h2>
                  <div className="flex flex-wrap gap-3 mt-3">
                    <div className="px-2 py-1 bg-gray-100 dark:bg-slate-800 rounded text-[10px] font-mono"><span className="text-gray-500">TC:</span> {algoInfo.complexity}</div>
                    <div className="px-2 py-1 bg-gray-100 dark:bg-slate-800 rounded text-[10px] font-mono"><span className="text-gray-500">Best:</span> <span className="text-green-600">{algoInfo.best}</span></div>
                    <div className="px-2 py-1 bg-gray-100 dark:bg-slate-800 rounded text-[10px] font-mono"><span className="text-gray-500">Worst:</span> <span className="text-red-600">{algoInfo.worst}</span></div>
                    <div className="px-2 py-1 bg-gray-100 dark:bg-slate-800 rounded text-[10px] font-mono"><span className="text-gray-500">Space:</span> {algoInfo.space}</div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-gray-900 dark:text-white">Visualization</h3>
              <div className="flex items-center gap-2">
                {!running && <button onClick={() => { setRunning(true); playSound.badge(); }} className="flex items-center gap-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-medium rounded-lg"><Play size={12} /> Play</button>}
                {running && <button onClick={() => setRunning(false)} className="flex items-center gap-1 px-3 py-1.5 bg-yellow-600 hover:bg-yellow-700 text-white text-xs font-medium rounded-lg"><Pause size={12} /> Pause</button>}
                <button onClick={() => { setRunning(false); setTraceData(null); setData(Array.from({ length: 12 }, () => Math.floor(Math.random() * 90) + 10)); }} className="flex items-center gap-1 px-3 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-700 text-xs font-medium rounded-lg"><RotateCcw size={12} /> Reset</button>
              </div>
            </div>
            {traceData ? <AlgorithmVisualizer traceData={traceData} code={algoInfo.code || ""} /> : <div className="bg-gray-50 dark:bg-slate-950 rounded-xl p-4 min-h-[200px] flex items-center justify-center"><div className="text-center"><BarChart3 size={32} className="mx-auto mb-2 text-gray-400" /><p className="text-sm text-gray-500">Click Play to start visualization</p></div></div>}
            <div className="flex items-center gap-3 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
              <span className="text-xs text-gray-500 font-mono">Speed:</span>
              {[0.5, 1, 2, 4].map((spd) => (
                <button key={spd} onClick={() => setSpeed(spd)} className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-colors ${speed === spd ? "bg-gray-900 text-white" : "bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-gray-400"}`}>{spd}x</button>
              ))}
            </div>
          </div>
          <div className="card">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">Data Array</h3>
            <div className="flex items-end justify-center gap-1 h-40">
              {data.map((val, idx) => {
                const maxVal = Math.max(...data, 1);
                const height = Math.max(8, (val / maxVal) * 120);
                return <motion.div key={idx} initial={{ height: 0, opacity: 0 }} animate={{ height, opacity: 1 }} transition={{ duration: 0.3, delay: idx * 0.03 }} className="flex-1 bg-gradient-to-t from-primary-500 to-primary-400 rounded-t-md flex items-start justify-center pt-1 min-w-[16px]"><span className="text-[9px] font-bold text-white">{val}</span></motion.div>;
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
