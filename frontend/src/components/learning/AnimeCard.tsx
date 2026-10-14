// @ts-nocheck
import { useState } from "react";
import type { TraceStep } from "./TracingAnimation";
import TracingAnimation from "./TracingAnimation";

export type AnimeCardData = {
  card_id: string;
  language_id: string;
  order: number;
  title: string;
  title_ja: string;
  concept: string;
  mental_model: string;
  difficulty: string;
  anime: {
    character: string;
    palette: string[];
    glow: string;
  };
  explain: { text: string; tutor: string; example: string };
  see: { type: string; alt: string };
  interact: {
    type: string;
    prompt: string;
    variables: { name: string; initial: any }[];
    move: string;
    answer: Record<string, any>;
    hint: string;
  };
  predict: { prompt: string; options: string[]; answer: number; explanation: string };
  solve: {
    prompt: string;
    language: string;
    starter: string;
    test_cases: any[];
    check: { required_patterns: string[]; forbidden: string[] };
  };
  break_: { prompt: string; buggy_code: string; expected_failure: string; expected_message: string };
  debug: {
    prompt: string;
    starter: string;
    fix_steps: string[];
    check: { required_patterns: string[]; forbidden: string[] };
  };
  recall: { prompt: string; answer: string; options: string[] };
  transfer: { prompt: string; context: string; hint: string };
  prove: {
    prompt: string;
    language: string;
    starter: string;
    test_cases: any[];
    check: { required_patterns: string[]; forbidden: string[] };
  };
  tracing: { type: string; inputs: any[]; steps: TraceStep[] };
};

type Props = {
  card: AnimeCardData;
  onProgress?: (step: string, score: number) => void;
};

export default function AnimeCard({ card, onProgress }: Props) {
  const [step, setStep] = useState<"idle" | "explain" | "see" | "interact" | "predict" | "solve" | "break" | "debug" | "recall" | "transfer" | "prove" | "trace">("explain");
  const [recallSelection, setRecallSelection] = useState<string>("");
  const [predictSelection, setPredictSelection] = useState<string>("");
  const [interactInputs, setInteractInputs] = useState<Record<string, any>>(() => {
    const init: Record<string, any> = {};
    for (const v of card.interact.variables) init[v.name] = v.initial;
    return init;
  });
  const [solveCode, setSolveCode] = useState(card.solve.starter);
  const [debugCode, setDebugCode] = useState(card.debug?.starter || "");
  const [proveCode, setProveCode] = useState(card.prove.starter);
  const [traceSteps] = useState<TraceStep[]>(card.tracing?.steps || []);

  const glow = card.anime?.glow || "#D4A843";

  return (
    <div className="rounded-2xl border border-border-muted bg-surface-raised">
      <div className="flex items-center justify-between p-4">
        <div>
          <div className="text-xs font-semibold text-brand">{card.card_id}</div>
          <div className="text-lg font-bold text-text-primary">{card.title}</div>
          <div className="text-sm text-text-secondary">{card.title_ja}</div>
        </div>
        <div
          className="h-2 w-2 rounded-full"
          style={{ backgroundColor: glow }}
          title="character glow"
        />
      </div>

      {step === "explain" && (
        <div className="space-y-3 p-4">
          <div className="rounded-xl border border-border-muted bg-surface p-4">
            <div className="text-sm font-bold text-brand">{card.explain?.tutor}</div>
            <div className="text-sm text-text-primary">{card.explain?.text}</div>
            <pre className="mt-2 rounded-lg bg-surface-raised p-2 font-mono text-xs text-text-primary">
              {card.explain?.example}
            </pre>
          </div>
          <div className="text-xs text-text-secondary">{card.mental_model}</div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("see");
              onProgress?.("explain", 10);
            }}
          >
            Explain understood
          </button>
        </div>
      )}

      {step === "see" && (
        <div className="space-y-3 p-4">
          <div className="rounded-xl border border-border-muted bg-surface p-4 text-sm text-text-primary">
            <span className="text-xs font-semibold text-brand">See</span>
            <div>{card.see?.alt}</div>
          </div>
          <div className="rounded-xl border border-brand/20 bg-brand/5 p-3 text-xs text-brand">
            Deterministic animation: {card.see?.type}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("interact");
              onProgress?.("see", 10);
            }}
          >
            Seen
          </button>
        </div>
      )}

      {step === "interact" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.interact?.prompt}</div>
          <div className="flex flex-wrap gap-2">
            {card.interact?.variables?.map((v) => (
              <div
                key={v.name}
                className="rounded-xl border border-brand/30 bg-surface p-3"
              >
                <div className="text-xs font-semibold text-brand">{v.name}</div>
                <input
                  className="mt-1 w-32 rounded-md border border-border-muted bg-surface-raised p-1 text-xs text-text-primary"
                  value={interactInputs[v.name] ?? ""}
                  onChange={(e) =>
                    setInteractInputs((s) => ({ ...s, [v.name]: e.target.value }))
                  }
                />
              </div>
            ))}
          </div>
          <div className="rounded-lg border border-brand/20 bg-brand/5 p-2 text-xs text-brand">
            Hint: {card.interact?.hint}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("predict");
              onProgress?.("interact", 10);
            }}
          >
            Done
          </button>
        </div>
      )}

      {step === "predict" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.predict?.prompt}</div>
          <div className="flex flex-wrap gap-2">
            {card.predict?.options?.map((opt, i) => (
              <button
                key={i}
                className={`rounded-lg border px-3 py-2 text-xs ${
                  predictSelection === opt
                    ? "border-brand bg-brand/10 text-brand"
                    : "border-border-muted text-text-secondary hover:border-brand"
                }`}
                onClick={() => {
                  setPredictSelection(opt);
                  onProgress?.("predict", predictSelection === card.predict?.options?.[card.predict.answer] ? 10 : 0);
                }}
              >
                {opt}
              </button>
            ))}
          </div>
          <div className="rounded-lg border border-brand/20 bg-brand/5 p-2 text-xs text-brand">
            {card.predict?.explanation}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("solve");
              onProgress?.("predict", predictSelection === card.predict?.options?.[card.predict.answer] ? 10 : 0);
            }}
          >
            Done
          </button>
        </div>
      )}

      {step === "solve" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.solve?.prompt}</div>
          <textarea
            className="h-40 w-full rounded-xl border border-border-muted bg-surface p-3 font-mono text-xs text-text-primary"
            value={solveCode}
            onChange={(e) => setSolveCode(e.target.value)}
          />
          <div className="flex items-center gap-2">
            <button
              className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("break");
              onProgress?.("solve", 10);
            }}
            >
              Solved
            </button>
          </div>
        </div>
      )}

      {step === "break" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.break_?.prompt}</div>
          <pre className="h-40 w-full overflow-auto rounded-xl border border-border-muted bg-surface p-3 font-mono text-xs text-red-700">
            {card.break_?.buggy_code}
          </pre>
          <div className="rounded-lg border border-red-300 bg-red-50 p-2 text-xs text-red-700">
            <span className="font-semibold">Expected failure:</span> {card.break_?.expected_failure}
            <span className="ml-2">({card.break_?.expected_message})</span>
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("debug");
              onProgress?.("break", 10);
            }}
          >
            Fixed
          </button>
        </div>
      )}

      {step === "debug" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.debug?.prompt}</div>
          <textarea
            className="h-40 w-full rounded-xl border border-border-muted bg-surface p-3 font-mono text-xs text-text-primary"
            value={debugCode}
            onChange={(e) => setDebugCode(e.target.value)}
          />
          <div className="space-y-1">
            {card.debug?.fix_steps?.map((f, i) => (
              <div key={i} className="rounded-lg border border-brand/20 bg-brand/5 p-2 text-xs text-brand">
                {i + 1}. {f}
              </div>
            ))}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("recall");
              onProgress?.("debug", 10);
            }}
          >
            Repaired
          </button>
        </div>
      )}

      {step === "recall" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.recall?.prompt}</div>
          <div className="flex flex-wrap gap-2">
            {card.recall?.options?.map((opt, i) => (
              <button
                key={i}
                className={`rounded-lg border px-3 py-2 text-xs ${
                  recallSelection === opt
                    ? "border-brand bg-brand/10 text-brand"
                    : "border-border-muted text-text-secondary hover:border-brand"
                }`}
                onClick={() => {
                  setRecallSelection(opt);
                  onProgress?.("recall", recallSelection === card.recall?.answer ? 10 : 0);
                }}
              >
                {opt}
              </button>
            ))}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("transfer");
              onProgress?.("recall", recallSelection === card.recall?.answer ? 10 : 0);
            }}
          >
            Recalled
          </button>
        </div>
      )}

      {step === "transfer" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.transfer?.prompt}</div>
          <div className="rounded-lg border border-brand/20 bg-brand/5 p-2 text-xs text-brand">
            {card.transfer?.context}
          </div>
          <div className="rounded-lg border border-brand/20 bg-brand/5 p-2 text-xs text-brand">
            Hint: {card.transfer?.hint}
          </div>
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("prove");
              onProgress?.("transfer", 10);
            }}
          >
            Done
          </button>
        </div>
      )}

      {step === "prove" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-text-primary">{card.prove?.prompt}</div>
          <textarea
            className="h-40 w-full rounded-xl border border-border-muted bg-surface p-3 font-mono text-xs text-text-primary"
            value={proveCode}
            onChange={(e) => setProveCode(e.target.value)}
          />
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => {
              setStep("trace");
              onProgress?.("prove", 10);
            }}
          >
            Submitted
          </button>
        </div>
      )}

      {step === "trace" && (
        <div className="space-y-3 p-4">
          <div className="text-sm font-semibold text-brand">World 4 tracing animation</div>
          <TracingAnimation steps={traceSteps} cardId={card.card_id} autoPlay />
        </div>
      )}

      {step === "idle" && (
        <div className="p-4">
          <button
            className="rounded-md border border-brand px-3 py-2 text-sm font-semibold text-brand hover:bg-brand/10"
            onClick={() => setStep("explain")}
          >
            Start
          </button>
        </div>
      )}
    </div>
  );
}
