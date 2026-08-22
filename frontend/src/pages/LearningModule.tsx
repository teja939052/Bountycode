import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useParams, Link } from "react-router-dom";
import { Play, Pause, RotateCcw, Check, Brain, Target, Code2, Trophy, ArrowRight, Eye, Zap } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const PHASES = ["concept", "predict", "lab", "mastery"] as const;
type Phase = (typeof PHASES)[number];

const MODULES = [
  { id: "arrays", title: "Arrays & Strings", description: "Master array manipulation, sliding windows, and two-pointer techniques." },
  { id: "linked-lists", title: "Linked Lists", description: "Understand pointers, node operations, and common linked list patterns." },
  { id: "trees", title: "Binary Trees", description: "Tree traversal, DFS/BFS, and recursive problem patterns." },
  { id: "graphs", title: "Graph Algorithms", description: "BFS, DFS, shortest paths, and topological sorting." },
];

export default function LearningModule() {
  const reduced = useReducedMotion();
  const { moduleId } = useParams<{ moduleId: string }>();
  const [phase, setPhase] = useState<Phase>("concept");
  const [completed, setCompleted] = useState<Record<Phase, boolean>>({
    concept: true,
    predict: false,
    lab: false,
    mastery: false,
  });

  useEffect(() => {
    setPhase("concept");
    setCompleted({ concept: true, predict: false, lab: false, mastery: false });
  }, [moduleId]);

  const moduleInfo = MODULES.find((m) => m.id === moduleId) || MODULES[0];
  const currentPhaseIndex = PHASES.indexOf(phase);
  const currentPhase = PHASES[currentPhaseIndex];

  const completePhase = () => {
    setCompleted((prev) => ({ ...prev, [currentPhase]: true }));
    const next = PHASES[currentPhaseIndex + 1];
    if (next) setPhase(next);
  };

  return (
    <div className="page-surface min-h-screen py-6 px-4 max-w-5xl mx-auto">
      <div className="max-w-3xl mx-auto">
        {/* Progress bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2 text-sm">
            <span className="text-text-muted">Progress</span>
            <span className="text-text-primary font-medium">
              {currentPhaseIndex + 1} of {PHASES.length}
            </span>
          </div>
          <div className="h-2 bg-border rounded-full overflow-hidden">
            <div
              className="h-full bg-primary rounded-full transition-all duration-500 ease-out"
              style={{ width: `${((currentPhaseIndex + 1) / PHASES.length) * 100}%` }}
            />
          </div>
          <div className="flex justify-between mt-2 text-xs text-text-muted">
            {PHASES.map((p, i) => (
              <span key={p} className={i <= currentPhaseIndex ? "text-primary" : ""}>
                {p === "concept" ? "Concept" : p === "predict" ? "Predict" : p === "lab" ? "Lab" : "Mastery"}
              </span>
            ))}
          </div>
        </div>

        {/* Phase content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPhase}
            initial={reduced ? {} : { opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduced ? {} : { opacity: 0, x: -20 }}
            transition={{ duration: 0.4 }}
            className="rounded-[16px] p-8 bg-white border border-border shadow-card"
          >
            <ConceptPhase
              key="concept"
              module={moduleInfo}
              onComplete={completePhase}
              isActive={currentPhase === "concept"}
              reduced={reduced}
            />
            <PredictPhase
              key="predict"
              module={moduleInfo}
              onComplete={completePhase}
              isActive={currentPhase === "predict"}
              reduced={reduced}
            />
            <LabPhase
              key="lab"
              module={moduleInfo}
              onComplete={completePhase}
              isActive={currentPhase === "lab"}
              reduced={reduced}
              completed={completed.lab}
            />
            <MasteryPhase
              key="mastery"
              module={moduleInfo}
              onComplete={completePhase}
              isActive={currentPhase === "mastery"}
              completed={completed.mastery}
              reduced={reduced}
            />
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className="mt-8 flex items-center justify-between">
          <button
            onClick={() => setPhase(PHASES[Math.max(0, currentPhaseIndex - 1)])}
            disabled={currentPhaseIndex === 0}
            className="px-4 py-2 text-sm text-text-muted hover:text-text-primary disabled:opacity-50 transition-colors"
          >
            ← Back
          </button>
          {currentPhase !== "mastery" && (
            <button
              onClick={completePhase}
              className="px-6 py-3 rounded-[10px] bg-primary text-white font-medium text-sm transition-all hover:bg-primary-dark"
            >
              {currentPhase === "concept" ? "Start Predicting →" :
               currentPhase === "predict" ? "Run the Lab →" :
               currentPhase === "lab" ? "Test Mastery →" : "Finish"}
            </button>
          )}
        </div>
      </div>

      {/* Module selector */}
      <div className="mt-12">
        <Link to="/prepare" className="flex items-center gap-2 text-sm text-text-muted hover:text-primary transition-colors">
          <ArrowRight size={16} className="rotate-180" />
          Back to Journey
        </Link>
      </div>
    </div>
  );
}

function ConceptPhase({ module, onComplete, isActive, reduced }: Record<string, any>) {
  return (
    <div style={{ display: isActive ? "block" : "none" }}>
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center">
          <Brain size={20} className="text-primary" />
        </div>
        <h2 className="text-xl font-bold text-text-primary">What you'll learn</h2>
      </div>
      <h3 className="text-2xl font-bold text-text-primary mb-3">{module.title}</h3>
      <p className="text-text-muted mb-6">{module.description}</p>

      <div className="space-y-3 text-sm">
        <div className="flex items-start gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
          <p className="text-text-muted">Understanding the core concept through examples.</p>
        </div>
        <div className="flex items-start gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
          <p className="text-text-muted">Identifying the problem pattern and edge cases.</p>
        </div>
        <div className="flex items-start gap-3">
          <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5" />
          <p className="text-text-muted">Writing clean, maintainable code that solves it.</p>
        </div>
      </div>

      <div className="mt-8 p-4 bg-surface-2 rounded-[10px] border border-border">
        <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-primary mb-2">
          <Target size={12} /> Today's focus
        </div>
        <p className="text-sm text-text-muted">
          By the end of this module, you'll solve any {module.title.toLowerCase()} problem in under 20 minutes.
        </p>
      </div>
    </div>
  );
}

function PredictPhase({ module, onComplete, isActive, reduced }: Record<string, any>) {
  return (
    <div style={{ display: isActive ? "block" : "none" }}>
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center">
          <Eye size={20} className="text-primary" />
        </div>
        <h2 className="text-xl font-bold text-text-primary">Predict the output</h2>
      </div>

      <p className="text-text-muted mb-6">Before writing code, trace through the algorithm and predict what happens.</p>

      <div className="rounded-[10px] p-4 bg-surface-2 border border-border font-mono text-sm text-text-primary whitespace-pre">
{`function twoSum(arr, target) {
  const map = new Map();
  for (let i = 0; i < arr.length; i++) {
    const complement = target - arr[i];
    if (map.has(complement)) return [map.get(complement), i];
    map.set(arr[i], i);
  }
  return [];
}

Input: [3, 5, 1, 7, 2], target = 8
Expected output: ?`}
      </div>

      <div className="mt-6 space-y-3">
        <p className="text-sm text-text-muted">What does this return?</p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <label className="flex items-center gap-2 p-2 rounded-[10px] border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="predict" className="text-primary" />
            <span className="text-text-muted">[1, 3]</span>
          </label>
          <label className="flex items-center gap-2 p-2 rounded-[10px] border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="predict" className="text-primary" />
            <span className="text-text-muted">[2, 3]</span>
          </label>
          <label className="flex items-center gap-2 p-2 rounded-[10px] border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="predict" className="text-primary" />
            <span className="text-text-muted">[1, 4]</span>
          </label>
          <label className="flex items-center gap-2 p-2 rounded-[10px] border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="predict" className="text-primary" />
            <span className="text-text-muted">[0, 3]</span>
          </label>
        </div>
      </div>

      <button
        onClick={onComplete}
        className="mt-6 px-6 py-3 rounded-[10px] bg-primary text-white font-medium text-sm transition-all hover:bg-primary-dark"
      >
        Run the Lab →
      </button>
    </div>
  );
}

function LabPhase({ module, onComplete, isActive, reduced, completed }: Record<string, any>) {
  const [code, setCode] = useState(`function twoSum(arr, target) {
  const map = new Map();
  for (let i = 0; i < arr.length; i++) {
    const complement = target - arr[i];
    if (map.has(complement)) return [map.get(complement), i];
    map.set(arr[i], i);
  }
  return [];
}

console.log(twoSum([3, 5, 1, 7, 2], 8));`);
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = () => {
    setIsRunning(true);
    setTimeout(() => setIsRunning(false), 800);
  };

  return (
    <div style={{ display: isActive ? "block" : "none" }}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center">
            <Code2 size={20} className="text-primary" />
          </div>
          <h2 className="text-xl font-bold text-text-primary">Run the code</h2>
        </div>
        <button
          onClick={handleRun}
          disabled={isRunning}
          className="px-4 py-2 rounded-[10px] bg-primary text-white text-sm font-medium hover:bg-primary-dark disabled:opacity-50 transition-colors flex items-center gap-2"
        >
          {isRunning ? <Pause size={14} /> : <Play size={14} />}
          {isRunning ? "Running..." : "Run"}
        </button>
      </div>

      <div className="mb-4 flex items-center gap-2 text-xs text-text-muted">
        <span>Language:</span>
        <select className="px-2 py-1 rounded bg-surface-2 border border-border text-text-primary text-xs">
          <option>JavaScript</option>
          <option>Python</option>
          <option>Java</option>
          <option>C++</option>
        </select>
      </div>

      <div className="border border-border rounded-[10px] overflow-hidden mb-4">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full h-40 p-4 font-mono text-sm bg-surface-2 text-text-primary resize-none focus:outline-none focus:ring-2 focus:ring-primary/20"
        />
      </div>

      <div className="rounded-[10px] p-4 bg-surface-2 border border-border font-mono text-sm">
        <div className="flex items-center gap-2 text-primary font-medium mb-2">
          <Zap size={14} /> Output
        </div>
        <code className="text-text-muted">
          [ 1, 3 ]  — indices of 5 and 3, which sum to 8
        </code>
      </div>

      {completed && (
        <div className="mt-6 flex items-center gap-2 text-sm">
          <Check size={16} className="text-primary" />
          <span className="text-text-muted">Lab complete</span>
        </div>
      )}

      <button
        onClick={onComplete}
        className="mt-6 px-6 py-3 rounded-[10px] bg-primary text-white font-medium text-sm transition-all hover:bg-primary-dark"
      >
        Test Mastery →
      </button>
    </div>
  );
}

function MasteryPhase({ module, onComplete, isActive, reduced, completed }: Record<string, any>) {
  return (
    <div style={{ display: isActive ? "block" : "none" }}>
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center">
          <Trophy size={20} className="text-primary" />
        </div>
        <h2 className="text-xl font-bold text-text-primary">Mastery Check</h2>
      </div>

      <p className="text-text-muted mb-6">Answer this correctly to mark this module as complete.</p>

      <div className="rounded-[10px] p-4 bg-surface-2 border border-border mb-6">
        <p className="font-medium text-text-primary mb-3">What is the time complexity of twoSum?</p>
        <div className="space-y-2 text-sm">
          <label className="flex items-center gap-3 p-2 rounded-lg border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="mastery" className="text-primary" />
            <span className="text-text-muted">O(n)</span>
          </label>
          <label className="flex items-center gap-3 p-2 rounded-lg border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="mastery" className="text-primary" />
            <span className="text-text-muted">O(n²)</span>
          </label>
          <label className="flex items-center gap-3 p-2 rounded-lg border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="mastery" className="text-primary" />
            <span className="text-text-muted">O(log n)</span>
          </label>
          <label className="flex items-center gap-3 p-2 rounded-lg border border-border cursor-pointer hover:border-primary">
            <input type="radio" name="mastery" className="text-primary" />
            <span className="text-text-muted">O(1)</span>
          </label>
        </div>
      </div>

      {completed && (
        <div className="mb-6 p-4 rounded-[10px] bg-primary-soft flex items-center gap-3">
          <Trophy size={20} className="text-primary" />
          <span className="text-primary-dark font-medium">Mastery achieved! Module complete.</span>
        </div>
      )}

      <div className="flex items-center justify-between">
        <button
          onClick={() => {}}
          className="px-6 py-3 rounded-[10px] bg-primary text-white font-medium text-sm transition-all hover:bg-primary-dark"
        >
          {completed ? "Continue" : "Submit answer"}
        </button>
        <Link
          to="/prepare"
          className="text-sm text-text-muted hover:text-primary transition-colors"
        >
          ← Back to Journey
        </Link>
      </div>
    </div>
  );
}
