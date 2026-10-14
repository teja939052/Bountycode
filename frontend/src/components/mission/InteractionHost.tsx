// @ts-nocheck
import { useState, type ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Eye, EyeOff, SlidersHorizontal, Link2, Brain, RefreshCw } from "lucide-react";
import AlgorithmTracer from "../interactive/AlgorithmTracer";
import PatternQuiz from "../interactive/PatternQuiz";
import FillInBlank from "../interactive/FillInBlank";
import PredictOutput from "../interactive/PredictOutput";
import OrderSteps from "../interactive/OrderSteps";
import ExplainAloud from "../interactivity/ExplainAloud";
import PatternTracer from "../interactivity/PatternTracer";
import CodeFillInTheBlank from "../interactivity/CodeFillInTheBlank";
import useReducedMotion from "../../hooks/useReducedMotion";
import type { MissionStage } from "../../data/missions/patterns";

/**
 * Interaction library — maps interaction subtypes under a canonical stage
 * onto existing widgets. No new engines; compositions only.
 */

type InteractionConfig = Record<string, unknown>;

function str(v: unknown, fallback = ""): string {
  return typeof v === "string" ? v : fallback;
}
function num(v: unknown, fallback: number): number {
  const n = typeof v === "number" ? v : Number(v);
  return Number.isFinite(n) ? n : fallback;
}
function arr<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v as T[]) : [];
}

function VisualHook({ config }: { config: InteractionConfig }) {
  const reduced = useReducedMotion();
  const visual = str(config.visual);
  const caption = str(config.caption);
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <motion.pre
        initial={reduced ? {} : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="overflow-x-auto rounded-lg bg-gray-950 p-3 font-mono text-[13px] leading-relaxed text-cyan-300"
      >
        {visual}
      </motion.pre>
      {caption && <p className="mt-2 text-xs text-text-muted">{caption}</p>}
    </div>
  );
}

function MicroAnimation({ config }: { config: InteractionConfig }) {
  const reduced = useReducedMotion();
  const frames = arr<string>(config.frames);
  const [i, setI] = useState(0);
  if (!frames.length) return null;
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="flex items-center justify-between gap-2 mb-2">
        <p className="text-xs font-mono text-text-muted">frame {i + 1}/{frames.length}</p>
        <button
          onClick={() => setI((x) => (x + 1) % frames.length)}
          className="rounded-lg border border-black/10 bg-white px-3 py-1.5 text-xs font-semibold"
        >
          Next frame
        </button>
      </div>
      <AnimatePresence mode="wait">
        <motion.pre
          key={i}
          initial={reduced ? {} : { opacity: 0, x: 12 }}
          animate={{ opacity: 1, x: 0 }}
          exit={reduced ? {} : { opacity: 0, x: -12 }}
          className="overflow-x-auto rounded-lg bg-gray-950 p-3 font-mono text-[13px] text-emerald-300"
        >
          {frames[i]}
        </motion.pre>
      </AnimatePresence>
    </div>
  );
}

function TapToReveal({ config }: { config: InteractionConfig }) {
  const [open, setOpen] = useState(false);
  const prompt = str(config.prompt, "What happens?");
  const reveal = str(config.reveal, "");
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <p className="text-sm font-semibold text-text-primary">{prompt}</p>
      <button
        onClick={() => setOpen((o) => !o)}
        className="mt-3 inline-flex min-h-[44px] items-center gap-2 rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold"
      >
        {open ? <EyeOff size={14} /> : <Eye size={14} />}
        {open ? "Hide" : "Reveal"}
      </button>
      {open && reveal && (
        <p className="mt-3 rounded-xl bg-emerald-50 p-3 text-sm text-emerald-800">{reveal}</p>
      )}
    </div>
  );
}

function ParameterSlider({ config, onPass }: { config: InteractionConfig; onPass?: (ok: boolean, score: number) => void }) {
  const label = str(config.label, "value");
  const min = num(config.min, 0);
  const max = num(config.max, 100);
  const step = num(config.step, 1);
  const target = num(config.target, min);
  const unit = str(config.unit, "");
  const formula = str(config.formula);
  const [v, setV] = useState(num(config.initial, min));
  const near = Math.abs(v - target) <= Math.max(step, (max - min) * 0.02);
  const score = near ? 100 : Math.max(0, 100 - Math.abs(v - target));
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <p className="flex items-center gap-2 text-sm font-semibold text-text-primary">
        <SlidersHorizontal size={14} /> {label}
      </p>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={v}
        onChange={(e) => setV(Number(e.target.value))}
        onMouseUp={() => onPass?.(near, score)}
        onTouchEnd={() => onPass?.(near, score)}
        className="mt-3 w-full accent-primary"
        aria-label={label}
      />
      <p className="mt-1 font-mono text-sm text-text-primary">
        {v}{unit}
        {formula && <span className="ml-2 text-text-muted">{formula.replace("{v}", String(v))}</span>}
      </p>
      <p className={`mt-2 text-xs ${near ? "text-emerald-600" : "text-text-muted"}`}>
        {near ? "Target hit." : `Move toward ${target}${unit}.`}
      </p>
    </div>
  );
}

function BeforeAfter({ config }: { config: InteractionConfig }) {
  const before = str(config.before);
  const after = str(config.after);
  const note = str(config.note);
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <p className="mb-1 font-mono text-[10px] uppercase tracking-widest text-text-muted">Before</p>
          <pre className="overflow-x-auto rounded-lg bg-gray-950 p-3 font-mono text-[12px] text-rose-300">{before}</pre>
        </div>
        <div>
          <p className="mb-1 font-mono text-[10px] uppercase tracking-widest text-text-muted">After</p>
          <pre className="overflow-x-auto rounded-lg bg-gray-950 p-3 font-mono text-[12px] text-emerald-300">{after}</pre>
        </div>
      </div>
      {note && <p className="mt-2 text-xs text-text-muted">{note}</p>}
    </div>
  );
}

function MatchRelationships({ config, onPass }: { config: InteractionConfig; onPass?: (ok: boolean, score: number) => void }) {
  const left = arr<string>(config.left);
  const right = arr<string>(config.right);
  const pairs = arr<[string, string]>(config.pairs);
  const [selL, setSelL] = useState<number | null>(null);
  const [matched, setMatched] = useState<Set<number>>(new Set());
  const [wrongFlash, setWrongFlash] = useState(false);

  const pairIndexForLeft = (li: number) => pairs.findIndex((p) => p[0] === left[li]);

  const pickRight = (ri: number) => {
    if (selL == null) return;
    const expected = pairIndexForLeft(selL);
    const chosenPair = pairs.findIndex((p) => p[1] === right[ri]);
    if (expected >= 0 && expected === chosenPair) {
      const next = new Set(matched);
      next.add(selL);
      setMatched(next);
      setSelL(null);
      setWrongFlash(false);
      if (next.size === left.length) onPass?.(true, 100);
    } else {
      setWrongFlash(true);
      setTimeout(() => setWrongFlash(false), 400);
      onPass?.(false, Math.round((matched.size / Math.max(left.length, 1)) * 100));
    }
  };

  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <p className="mb-2 flex items-center gap-2 text-sm font-semibold text-text-primary">
        <Link2 size={14} /> Match each pair
      </p>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-2">
          {left.map((item, i) => (
            <button
              key={item}
              disabled={matched.has(i)}
              onClick={() => setSelL(i)}
              className={`min-h-[44px] w-full rounded-xl border px-3 py-2 text-left text-sm ${
                matched.has(i)
                  ? "border-emerald-400 bg-emerald-50 text-emerald-800"
                  : selL === i
                    ? "border-primary/60 bg-primary/5"
                    : "border-black/10 bg-white"
              }`}
            >
              {item}
            </button>
          ))}
        </div>
        <div className="space-y-2">
          {right.map((item, i) => (
            <button
              key={item}
              onClick={() => pickRight(i)}
              className={`min-h-[44px] w-full rounded-xl border px-3 py-2 text-left text-sm ${
                wrongFlash ? "border-red-400 bg-red-50" : "border-black/10 bg-white"
              }`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>
      <p className="mt-2 font-mono text-[11px] text-text-muted">
        Matched {matched.size}/{left.length} · pick left then right
      </p>
    </div>
  );
}

function RecallCard({ config }: { config: InteractionConfig }) {
  const prompt = str(config.prompt, "Recall without notes.");
  const answer = str(config.answer);
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <p className="flex items-center gap-2 text-sm font-semibold text-text-primary">
        <Brain size={14} /> {prompt}
      </p>
      <button
        onClick={() => setOpen((o) => !o)}
        className="mt-3 inline-flex min-h-[44px] items-center gap-2 rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold"
      >
        <RefreshCw size={14} /> {open ? "Hide answer" : "Check recall"}
      </button>
      {open && answer && (
        <p className="mt-3 rounded-xl bg-surface-2 p-3 text-sm text-text-primary">{answer}</p>
      )}
    </div>
  );
}

function inferLegacyKind(stage: MissionStage): string {
  if (stage.interaction?.kind) return stage.interaction.kind;
  if (stage.component === "ExplainAloud") return "explain_aloud";
  if (stage.component === "PatternTracer") return "state_trace";
  if (stage.component === "CodeFillInTheBlank") return "fill_in_blank";
  return "";
}

export default function InteractionHost({
  stage,
  skillId,
  onInteractionPass,
}: {
  stage: MissionStage;
  skillId: string;
  onInteractionPass?: (ok: boolean, score: number) => void;
}): ReactNode {
  const kind = inferLegacyKind(stage);
  const cfg = (stage.interaction?.config ?? stage.interaction ?? {}) as InteractionConfig;
  // interaction object itself may carry config fields alongside kind
  const payload: InteractionConfig = { ...cfg };
  if (stage.interaction) {
    for (const [k, v] of Object.entries(stage.interaction)) {
      if (k !== "kind" && k !== "config") payload[k] = v;
    }
  }

  switch (kind) {
    case "visual_hook":
      return <VisualHook config={payload} />;
    case "micro_animation":
      return <MicroAnimation config={payload} />;
    case "tap_to_reveal":
      return <TapToReveal config={payload} />;
    case "parameter_slider":
    case "change_one_thing":
    case "drag_or_manipulate":
      return <ParameterSlider config={payload} onPass={onInteractionPass} />;
    case "before_after":
      return <BeforeAfter config={payload} />;
    case "match_relationships":
      return <MatchRelationships config={payload} onPass={onInteractionPass} />;
    case "recall_check":
    case "srs_card":
      return <RecallCard config={payload} />;
    case "state_trace":
    case "algorithm_tracer": {
      const steps = arr<Record<string, unknown>>(payload.steps);
      if (!steps.length) return null;
      return (
        <AlgorithmTracer
          steps={steps as never}
          title={str(payload.title, "State trace")}
          onComplete={(ok) => onInteractionPass?.(ok, ok ? 100 : 0)}
        />
      );
    }
    case "pattern_tracer":
      return (
        <PatternTracer
          skillId={skillId}
          values={arr<number>(payload.values).length ? arr<number>(payload.values) : undefined}
          k={payload.k != null ? num(payload.k, 3) : undefined}
          title={str(payload.title) || undefined}
          description={str(payload.description) || undefined}
          pattern={str(payload.pattern, "sliding-window")}
        />
      );
    case "explain_aloud":
    case "explain_the_bug":
      return (
        <ExplainAloud
          skillId={skillId}
          keywords={arr<string>(payload.keywords).length ? arr<string>(payload.keywords) : undefined}
          title={str(payload.title) || undefined}
          prompt={str(payload.prompt) || undefined}
          pattern={str(payload.pattern, "sliding-window")}
        />
      );
    case "fill_in_blank":
    case "code_fill":
    case "tiny_build": {
      const blanks = arr<{ id: string; placeholder?: string; correctAnswer: string; hint?: string; width?: number }>(
        payload.blanks,
      );
      if (payload.codeTemplate || blanks.length) {
        return (
          <FillInBlank
            codeTemplate={str(payload.codeTemplate)}
            blanks={blanks}
            language={str(payload.language, "python")}
            explanation={str(payload.explanation) || undefined}
            onComplete={(ok, attempts) => onInteractionPass?.(ok, ok ? 100 : Math.max(0, 100 - attempts * 20))}
          />
        );
      }
      return (
        <CodeFillInTheBlank
          skillId={skillId}
          options={arr<string>(payload.options).length ? arr<string>(payload.options) : undefined}
          correct={str(payload.correct) || undefined}
          code={str(payload.code) || undefined}
          title={str(payload.title) || undefined}
          prompt={str(payload.prompt) || undefined}
          pattern={str(payload.pattern, "sliding-window")}
          successNote={str(payload.successNote) || undefined}
          failNote={str(payload.failNote) || undefined}
        />
      );
    }
    case "predict_output": {
      const questions = arr(payload.questions);
      if (!questions.length) return null;
      return (
        <PredictOutput
          questions={questions as never}
          onComplete={(score, total) => onInteractionPass?.(score === total, (score / Math.max(total, 1)) * 100)}
        />
      );
    }
    case "multiple_choice_reasoning":
    case "pattern_quiz": {
      const questions = arr(payload.questions);
      if (!questions.length) return null;
      return (
        <PatternQuiz
          questions={questions as never}
          onComplete={(score, total) => onInteractionPass?.(score === total, (score / Math.max(total, 1)) * 100)}
        />
      );
    }
    case "sort_steps":
    case "code_reorder": {
      const steps = arr(payload.steps);
      if (!steps.length) return null;
      return (
        <OrderSteps
          steps={steps as never}
          title={str(payload.title, "Order the steps")}
          explanation={str(payload.explanation) || undefined}
          onComplete={(ok, attempts) => onInteractionPass?.(ok, ok ? 100 : Math.max(0, 100 - attempts * 20))}
        />
      );
    }
    case "interactive_diagram":
      return <VisualHook config={{ ...payload, visual: str(payload.visual, str(payload.diagram)) }} />;
    default:
      return null;
  }
}
