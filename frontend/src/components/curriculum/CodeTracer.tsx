// @ts-nocheck
import { useState } from "react";
import { motion } from "framer-motion";
import { Play, RotateCcw } from "lucide-react";

interface CodeTracerProps {
  code: string;
  language: string;
}

export default function CodeTracer({ code, language }: CodeTracerProps) {
  const lines = code.split("\n");
  const [currentLine, setCurrentLine] = useState(0);
  const [variables, setVariables] = useState<Record<string, string>>({});
  const [output, setOutput] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const simulateStep = () => {
    // Simple line-by-line simulation for curriculum traces
    // In production, this would use a real Python/JS tracer
    setIsRunning(true);
    if (currentLine < lines.length - 1) {
      setCurrentLine((l) => l + 1);
    }
    setIsRunning(false);
  };

  const reset = () => {
    setCurrentLine(0);
    setVariables({});
    setOutput([]);
  };

  return (
    <div className="rounded-2xl border border-black/10 bg-slate-900 p-4 text-white">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-xs font-mono uppercase tracking-widest text-slate-400">{language} Tracer</span>
        <div className="flex gap-2">
          <button onClick={simulateStep} disabled={isRunning} className="flex items-center gap-1 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold hover:bg-emerald-700 disabled:opacity-40">
            <Play className="h-3 w-3" /> Step
          </button>
          <button onClick={reset} className="flex items-center gap-1 rounded-lg bg-slate-700 px-3 py-1.5 text-xs font-bold hover:bg-slate-600">
            <RotateCcw className="h-3 w-3" /> Reset
          </button>
        </div>
      </div>

      <div className="flex gap-4">
        {/* Code */}
        <div className="flex-1 font-mono text-xs leading-6">
          {lines.map((line, idx) => (
            <div
              key={idx}
              className={`flex gap-3 rounded-lg px-2 py-0.5 ${
                idx === currentLine ? "bg-emerald-900/40 text-emerald-300" : "text-slate-300"
              }`}
            >
              <span className="w-6 text-right text-slate-500 select-none">{idx + 1}</span>
              <span className="flex-1">{line || " "}</span>
            </div>
          ))}
        </div>

        {/* Variables panel */}
        <div className="w-48 shrink-0 rounded-xl border border-slate-700 bg-slate-800/60 p-3">
          <p className="mb-2 text-[10px] font-mono uppercase tracking-widest text-slate-400">Variables</p>
          {Object.keys(variables).length === 0 ? (
            <p className="text-[11px] text-slate-500">No variables yet</p>
          ) : (
            <div className="space-y-1">
              {Object.entries(variables).map(([k, v]) => (
                <div key={k} className="flex justify-between text-[11px]">
                  <span className="font-mono text-slate-300">{k}</span>
                  <span className="font-mono text-emerald-400">{v}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {output.length > 0 && (
        <div className="mt-3 rounded-xl border border-slate-700 bg-slate-800/60 p-3">
          <p className="mb-1 text-[10px] font-mono uppercase tracking-widest text-slate-400">Output</p>
          {output.map((line, i) => <div key={i} className="font-mono text-xs text-slate-300">{line}</div>)}
        </div>
      )}
    </div>
  );
}
