import { useState, useCallback, useEffect, useRef } from "react";
import {
  Play,
  Pause,
  SkipForward,
  SkipBack,
  Code2,
  Zap,
  Timer,
  Layers,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { compilerApi } from "../../services/api/coding";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";

interface TraceStep {
  step: number;
  line: number;
  action: string;
  variables: Record<string, string>;
  explanation?: string;
}

interface TraceResult {
  algorithm: string;
  steps: TraceStep[];
  output?: string;
  time_complexity?: string;
  space_complexity?: string;
  key_insights?: string[];
  source?: string;
}

interface CodeTracerProps {
  code: string;
  language?: string;
  stdin?: string;
  className?: string;
}

export default function CodeTracer({ code, language = "python", stdin = "", className = "" }: CodeTracerProps) {
  const [trace, setTrace] = useState<TraceResult | null>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const animationRef = useRef<number>(0);

  const generateTrace = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await compilerApi.traceCode({ code, language, stdin });
      setTrace({
        algorithm: "Code Trace",
        steps: (result.trace || []).map((step: string, idx: number) => ({
          step: idx + 1,
          line: idx + 1,
          action: step,
          variables: {},
        })),
        output: result.output,
        key_insights: result.errors?.length ? result.errors : ["Trace completed successfully"],
        source: "ast_trace",
      } as TraceResult);
      setCurrentStepIndex(0);
    } catch (e: any) {
      setTrace({
        algorithm: "Unknown",
        steps: [],
        output: "",
        key_insights: ["Trace generation failed: " + (e?.detail || e?.message || "Unknown error")],
        source: "error",
      } as TraceResult);
    } finally {
      setIsLoading(false);
    }
  }, [code, language, stdin]);

  useEffect(() => {
    generateTrace();
    return () => cancelAnimationFrame(animationRef.current);
  }, [generateTrace]);

  const currentStep = trace?.steps?.[currentStepIndex] || null;
  const totalSteps = trace?.steps.length || 0;
  const progressPct = totalSteps > 0 ? Math.round(((currentStepIndex + 1) / totalSteps) * 100) : 0;

  const playAnimation = useCallback(() => {
    if (!trace || isRunning) return;
    setIsRunning(true);
    let i = currentStepIndex;
    const tick = () => {
      if (i < trace.steps.length - 1) {
        i++;
        setCurrentStepIndex(i);
        animationRef.current = window.setTimeout(() => tick(), 800) as unknown as number;
      } else {
        setIsRunning(false);
      }
    };
    tick();
  }, [trace, currentStepIndex, isRunning]);

  const goToStep = (index: number) => {
    if (index >= 0 && index < totalSteps) {
      setCurrentStepIndex(index);
    }
  };

  const lineNumbers = code.split("\n").map((_, i) => i + 1);
  const currentLine = currentStep?.line || 0;

  return (
    <div className={`${className} w-full`}>
      <div className="flex items-center justify-between mb-4 px-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-ocean flex items-center justify-center">
            <Code2 size={16} className="text-white" />
          </div>
          <div>
            <h3 className="font-bold text-text-primary">Code Execution Trace</h3>
            <p className="text-xs text-text-muted capitalize">
              {language} • {trace?.algorithm || "Analyzing..."}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={trace?.source === "ast_trace" ? "success" : "default"}>
            {trace?.source === "ast_trace" ? "Live Trace" : "AI Trace"}
          </Badge>
          <button
            onClick={generateTrace}
            className="text-xs font-mono text-primary hover:text-primary-dark transition-colors"
          >
            Re-run
          </button>
        </div>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <div className="flex flex-col items-center gap-3">
            <div className="w-10 h-10 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
            <p className="text-text-muted text-sm">Generating execution trace...</p>
          </div>
        </div>
      )}

      {trace && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7">
            <Card variant="dark" padding="none" radius="lg" className="overflow-hidden shadow-card-hover">
              <div className="bg-[#0d1117] border-b border-white/5 px-4 py-2 flex items-center justify-between">
                <span className="text-xs font-mono text-text-muted">{language}</span>
                <div className="flex items-center gap-1">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: i === 1 ? "#ff5f56" : i === 2 ? "#ffbd2e" : "#27c93f" }} />
                  ))}
                </div>
              </div>
              <div className="relative overflow-x-auto">
                <div className="flex min-w-full">
                  <div className="w-14 shrink-0 bg-[#0d1117] border-r border-white/5">
                    {lineNumbers.map((ln) => (
                      <div
                        key={ln}
                        className={`w-full h-[24px] text-[11px] font-mono flex items-center justify-end pr-4 ${ln === currentLine ? "text-cyber-green font-bold bg-[rgba(34,197,94,0.1)]" : "text-brand-muted"}`}
                      >
                        {ln}
                      </div>
                    ))}
                  </div>
                  <div className="min-w-full p-4 font-mono text-sm leading-6 text-[#c9d1d9]">
                    {code.split("\n").map((line, idx) => {
                      const lineNum = idx + 1;
                      const isCurrent = lineNum === currentLine;
                      return (
                        <div key={idx} className="flex items-start" style={{ backgroundColor: isCurrent ? "rgba(34, 197, 94, 0.08)" : "transparent" }}>
                          <span className="inline-block w-14 shrink-0 pr-4 text-[11px] font-mono text-brand-muted select-none">{lineNum}</span>
                          <span className="block break-whitespace">{line.replace(/ /g, "\u00A0")}</span>
                        </div>
                      );
                    })}
                  </div>
                  {currentLine > 0 && (
                    <div className="absolute left-0 right-0 h-1 bg-gradient-to-r from-primary to-ocean pointer-events-none" style={{ top: `${(currentLine - 1) * 24 + 50}px` }} />
                  )}
                </div>
              </div>
              <div className="bg-[#0d1117] border-t border-white/5 px-4 py-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded flex items-center justify-center bg-cyber-green/20 text-cyber-green text-xs font-bold">▶</div>
                    <span className="text-sm font-medium text-text-primary">Line {currentLine} • {currentStep?.action || "Executing..."}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1/2 bg-white/10 rounded-full h-1.5 overflow-hidden">
                      <div className="h-full bg-cyber-green transition-all duration-300" style={{ width: `${progressPct}%` }} />
                    </div>
                    <span className="text-[10px] font-mono text-text-muted">{progressPct}%</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          <div className="lg:col-span-5 space-y-6">
            <Card variant="default" padding="md" radius="lg">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-text-primary text-sm">Step {currentStepIndex + 1} / {totalSteps}</h4>
                <div className="flex items-center gap-1">
                  <Zap size={14} className="text-primary" />
                  <span className="text-[10px] font-mono text-text-muted uppercase">{trace.source}</span>
                </div>
              </div>
              <div className="mb-3">
                <p className="text-text-secondary text-sm leading-relaxed">{currentStep?.action || ""}</p>
              </div>
              {currentStep?.explanation && (
                <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-3 mb-3">
                  <p className="text-xs text-blue-800 leading-relaxed">{currentStep.explanation}</p>
                </div>
              )}
              <div className="mb-4">
                <h5 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2">Variable State</h5>
                {currentStep?.variables && Object.keys(currentStep.variables).length > 0 ? (
                  <div className="space-y-1">
                    {Object.entries(currentStep.variables).map(([name, value]) => (
                      <div key={name} className="flex items-center justify-between p-2 rounded bg-[#0d1117] border border-white/5 text-xs font-mono">
                        <span className="text-text-primary">{name}</span>
                        <span className="text-cyber-green">{value}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <span className="text-xs text-brand-muted">No variables in scope</span>
                  </div>
                )}
              </div>
              <div className="flex items-center justify-between pt-4 border-t border-border/40">
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" onClick={() => goToStep(0)} disabled={currentStepIndex === 0 || isRunning}>
                    <SkipBack size={14} /> First
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => goToStep(Math.max(0, currentStepIndex - 1))} disabled={currentStepIndex === 0 || isRunning}>
                    <ChevronLeft size={14} /> Prev
                  </Button>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" onClick={() => goToStep(Math.min(totalSteps - 1, currentStepIndex + 1))} disabled={currentStepIndex >= totalSteps - 1 || isRunning}>
                    Next <ChevronRight size={14} />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => goToStep(totalSteps - 1)} disabled={currentStepIndex >= totalSteps - 1 || isRunning}>
                    Last <SkipForward size={14} />
                  </Button>
                </div>
              </div>
            </Card>

            <Card variant="outlined" padding="md" radius="lg" className="border-primary/40">
              <h4 className="font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                <Timer size={14} className="text-primary" /> Output & Complexity
              </h4>
              <div className="space-y-3">
                <div className="bg-[#0d1117] rounded-lg p-3 border border-white/5">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-mono text-text-muted">Output</span>
                    <span className="text-[10px] font-mono text-text-muted">{trace.steps.length} steps</span>
                  </div>
                  <pre className="text-[10px] font-mono text-[#4ade80] overflow-x-auto">{trace.output || "(no output)"}</pre>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-lg bg-surface-2 border border-border/40">
                    <span className="text-[10px] font-mono text-text-muted block mb-1">Time Complexity</span>
                    <span className="text-sm font-bold text-text-primary">{trace.time_complexity || "O(n)"}</span>
                  </div>
                  <div className="p-3 rounded-lg bg-surface-2 border border-border/40">
                    <span className="text-[10px] font-mono text-text-muted block mb-1">Space Complexity</span>
                    <span className="text-sm font-bold text-text-primary">{trace.space_complexity || "O(1)"}</span>
                  </div>
                </div>
              </div>
            </Card>

            {trace.key_insights && trace.key_insights.length > 0 && (
              <Card variant="glass" padding="md" radius="lg">
                <h4 className="font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                  <Layers size={14} className="text-ocean" /> Key Insights
                </h4>
                <ul className="space-y-2">
                  {trace.key_insights.map((insight, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs text-text-secondary leading-relaxed">
                      <span className="mt-0.5 text-primary">▹</span>
                      {insight}
                    </li>
                  ))}
                </ul>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function Badge({ variant = "default", children }: { variant?: "default" | "success"; children: React.ReactNode }) {
  const styles: Record<string, string> = {
    default: "px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-surface-2 border border-border/40 text-text-muted",
    success: "px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E]",
  };
  return <span className={styles[variant]}>{children}</span>;
}
