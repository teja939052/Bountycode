// @ts-nocheck
/**
 * MissionPackRenderer — generic renderer for any Mission Pack.
 *
 * This component knows how to render every step type in the 9-step loop:
 *   discover → understand → manipulate → predict → build → break_step → debug → retrieval → transfer
 *
 * It receives a `pack` (MissionPack JSON) and `step` (current step index/name),
 * and renders the appropriate interaction widget based on `step.interaction_kind`.
 */

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Lightbulb,
  CheckCircle2,
  XCircle,
  ArrowRight,
  RefreshCw,
  Trophy,
  Timer,
  Sparkles,
  Target,
  Zap,
  BookOpen,
  Compass,
  Shield,
  XCircle as BreakIcon,
  RotateCcw,
} from "lucide-react";
import Spinner from "../../components/ui/Spinner";

const STEP_META: Record<string, { icon: any; color: string; label: string }> = {
  discover: { icon: Compass, color: "text-sky-600", label: "Discover" },
  understand: { icon: BookOpen, color: "text-indigo-600", label: "Understand" },
  manipulate: { icon: Zap, color: "text-amber-600", label: "Manipulate" },
  predict: { icon: Target, color: "text-purple-600", label: "Predict" },
  build: { icon: Sparkles, color: "text-emerald-600", label: "Build" },
  break_step: { icon: BreakIcon, color: "text-red-600", label: "Break" },
  debug: { icon: RotateCcw, color: "text-orange-600", label: "Debug" },
  retrieval: { icon: Shield, color: "text-teal-600", label: "Retrieve" },
  transfer: { icon: Trophy, color: "text-yellow-600", label: "Transfer" },
};

export default function MissionPackRenderer({
  pack,
  step,
  onSubmit,
  onHint,
  onRetry,
  answerResult,
  loading,
  hint,
  showHint,
  diamondsEarned,
  mistakeCount,
}) {
  const [localAnswer, setLocalAnswer] = useState("");
  const [selectedOption, setSelectedOption] = useState(null);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [fixesApplied, setFixesApplied] = useState([]);
  const [matches, setMatches] = useState({});

  const content = step?.content || {};
  const stepName = step?.step_name || "";
  const meta = STEP_META[stepName] || STEP_META.discover;
  const StepIcon = meta.icon;

  const reset = useCallback(() => {
    setLocalAnswer("");
    setSelectedOption(null);
    setSelectedComponent(null);
    setFixesApplied([]);
    setMatches({});
  }, []);

  const handleSubmit = useCallback(() => {
    const payload: any = { step_index: step?.step_index, time_spent_seconds: 0 };

    if (["discover", "understand", "retrieval"].includes(stepName)) {
      payload.answer = localAnswer || content?.prompt || "";
    } else if (stepName === "manipulate") {
      if (selectedComponent) payload.selected_component = selectedComponent;
      else payload.answer = localAnswer || "manipulated";
    } else if (stepName === "predict") {
      if (selectedOption) payload.selected_option = selectedOption;
      else payload.answer = localAnswer;
    } else if (stepName === "build") {
      payload.code = localAnswer;
      payload.language = "python";
    } else if (stepName === "break_step") {
      payload.answer = localAnswer;
    } else if (stepName === "debug") {
      payload.improved_answer = localAnswer;
      payload.fixes_applied = fixesApplied;
    } else if (stepName === "transfer") {
      payload.answer = localAnswer;
      if (fixesApplied.length) payload.fixes_applied = fixesApplied;
    }

    onSubmit(payload);
  }, [step, stepName, localAnswer, selectedOption, selectedComponent, fixesApplied, onSubmit, content]);

  const canSubmit =
    localAnswer.trim() ||
    selectedOption !== null ||
    selectedComponent !== null ||
    fixesApplied.length > 0;

  return (
    <div className="space-y-4">
      {/* Step header */}
      <div className="flex items-center gap-3 rounded-2xl border border-black/5 bg-surface-2 p-4">
        <div className={`rounded-xl bg-white p-2 ${meta.color}`}>
          <StepIcon size={24} />
        </div>
        <div className="flex-1">
          <h3 className="font-display text-lg font-bold">{content?.prompt || meta.label}</h3>
          {content?.question && (
            <p className="mt-1 text-sm text-text-muted">{content.question}</p>
          )}
        </div>
      </div>

      {/* Feedback from previous submission */}
      {answerResult && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className={`rounded-2xl border p-4 ${
            answerResult.passed
              ? "border-emerald-200 bg-emerald-50"
              : "border-red-200 bg-red-50"
          }`}
        >
          <div className="flex items-start gap-2">
            {answerResult.passed ? (
              <CheckCircle2 size={18} className="shrink-0 text-emerald-600" />
            ) : (
              <XCircle size={18} className="shrink-0 text-red-600" />
            )}
            <div className="flex-1">
              <p className={`text-sm font-semibold ${answerResult.passed ? "text-emerald-900" : "text-red-900"}`}>
                {answerResult.passed ? "Correct!" : "Not quite right"}
              </p>
              {answerResult.message && (
                <p className="mt-1 text-sm text-text-secondary">{answerResult.message}</p>
              )}
              {answerResult.mastery_unlocked && (
                <div className="mt-3 rounded-xl bg-emerald-100 p-3">
                  <p className="text-sm font-bold text-emerald-900">🎉 Mastery Unlocked!</p>
                  {answerResult.reward?.diamonds && (
                    <p className="mt-1 font-mono text-xs text-emerald-700">
                      💎 +{answerResult.reward.diamonds}
                    </p>
                  )}
                </div>
              )}
              {answerResult.reteach_required && (
                <button
                  onClick={onRetry}
                  className="mt-3 inline-flex items-center gap-2 rounded-xl bg-orange-500 px-4 py-2 text-sm font-bold text-white"
                >
                  <RefreshCw size={14} /> Get Reteach Plan
                </button>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Hint display */}
      {showHint && hint && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-blue-200 bg-blue-50 p-4"
        >
          <div className="flex items-start gap-2">
            <Lightbulb size={18} className="shrink-0 text-blue-600" />
            <div>
              <p className="text-sm font-semibold text-blue-900">Hint</p>
              <p className="mt-1 text-sm text-blue-700">{hint}</p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Step content renderer */}
      <motion.div
        key={step?.step_index}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.18 }}
      >
        {renderStepContent(stepName, content, {
          localAnswer, setLocalAnswer,
          selectedOption, setSelectedOption,
          selectedComponent, setSelectedComponent,
          fixesApplied, setFixesApplied,
          matches, setMatches,
        })}
      </motion.div>

      {/* Action bar */}
      <div
        className="fixed inset-x-0 bottom-0 z-40 border-t border-black/10 bg-white/95 px-4 pt-3 backdrop-blur md:static md:rounded-2xl md:border"
        style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}
      >
        <div className="mx-auto flex w-full max-w-2xl gap-2">
          <button
            onClick={() => onHint?.()}
            className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl border border-black/10 px-4 text-sm font-semibold"
          >
            <Lightbulb size={15} /> Hint
          </button>
          <button
            onClick={() => { reset(); onRetry?.(); }}
            className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl border border-black/10 px-4 text-sm font-semibold"
          >
            Reset
          </button>
          <button
            onClick={handleSubmit}
            disabled={loading || !canSubmit}
            className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white shadow-lg shadow-orange-500/20 disabled:opacity-40"
          >
            {loading ? <Spinner size={15} /> : <ArrowRight size={15} />}
            {answerResult ? (answerResult.passed ? "Continue" : "Retry") : "Submit"}
          </button>
        </div>
        {!answerResult && !canSubmit && (
          <p className="mx-auto mt-1 w-full max-w-2xl text-center font-mono text-[11px] text-text-muted">
            Answer the question to continue.
          </p>
        )}
      </div>
    </div>
  );
}


// ═══════════════════════════════════════════════════════════════
// Step content renderer — switch on step_name + interaction_kind
// ═══════════════════════════════════════════════════════════════

function renderStepContent(stepName, content, controls) {
  const { localAnswer, setLocalAnswer, selectedOption, setSelectedOption, selectedComponent, setSelectedComponent, fixesApplied, setFixesApplied, matches, setMatches } = controls;

  switch (stepName) {
    case "discover":
      return renderDiscover(content, localAnswer, setLocalAnswer);
    case "understand":
      return renderUnderstand(content, localAnswer, setLocalAnswer);
    case "manipulate":
      return renderManipulate(content, localAnswer, setLocalAnswer, selectedComponent, setSelectedComponent, matches, setMatches);
    case "predict":
      return renderPredict(content, localAnswer, setLocalAnswer, selectedOption, setSelectedOption);
    case "build":
      return renderBuild(content, localAnswer, setLocalAnswer);
    case "break_step":
      return renderBreak(content, localAnswer, setLocalAnswer);
    case "debug":
      return renderDebug(content, localAnswer, setLocalAnswer, fixesApplied, setFixesApplied);
    case "retrieval":
      return renderRetrieval(content, localAnswer, setLocalAnswer);
    case "transfer":
      return renderTransfer(content, localAnswer, setLocalAnswer, fixesApplied, setFixesApplied);
    default:
      return <p className="text-sm text-text-muted">Complete this step to continue.</p>;
  }
}

function renderDiscover(content, value, set) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Explore the concept"}</h4>
        {content?.question && <p className="mt-2 text-sm text-text-secondary">{content.question}</p>}
        {content?.requirements && (
          <ul className="mt-3 space-y-1">
            {content.requirements.map((r, i) => <li key={i} className="text-sm text-text-secondary">• {r}</li>)}
          </ul>
        )}
        {content?.options && (
          <div className="mt-3 space-y-2">
            {content.options.map((opt, i) => (
              <button key={i} onClick={() => set(opt)} className={`w-full rounded-xl border px-4 py-3 text-left text-sm ${value === opt ? "border-primary bg-primary/5" : "border-black/10"}`}>
                {opt}
              </button>
            ))}
          </div>
        )}
      </div>
      {!content?.options && (
        <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="What do you observe?" className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={3} />
      )}
    </div>
  );
}

function renderUnderstand(content, value, set) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Understand the concept"}</h4>
        {content?.explanation && <p className="mt-2 text-sm text-text-secondary">{content.explanation}</p>}
        {content?.components && (
          <div className="mt-3 space-y-2">
            {Object.entries(content.components).map(([k, v]) => (
              <div key={k} className="rounded-xl bg-white p-3">
                <span className="font-mono text-xs font-bold text-primary">{k}</span>
                <p className="text-sm text-text-secondary">{v.label || v.description}</p>
              </div>
            ))}
          </div>
        )}
        {content?.dimensions && (
          <div className="mt-3 space-y-2">
            {content.dimensions.map((d, i) => (
              <div key={i} className="rounded-xl bg-white p-3">
                <span className="font-mono text-xs font-bold text-primary">{d.name}</span>
                <p className="text-sm text-text-secondary">{d.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Explain in your own words..." className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={3} />
    </div>
  );
}

function renderManipulate(content, value, set, selected, setSelected, matches, setMatches) {
  if (content?.sentences) {
    return (
      <div className="space-y-3">
        {content.sentences.map((s, i) => (
          <div key={i} className="rounded-2xl border border-black/5 bg-surface-2 p-4">
            <p className="text-sm">{s.text}</p>
            <div className="mt-3 flex gap-2">
              {["S", "T", "A", "R"].map((c) => (
                <button key={c} onClick={() => setSelected(c)} className={`rounded-lg px-3 py-1.5 text-xs font-bold ${selected === c ? "bg-primary text-white" : "bg-black/5"}`}>
                  {c}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }
  if (content?.components) {
    return (
      <div className="space-y-3">
        {content.components.map((c, i) => (
          <div key={i} className="rounded-2xl border border-black/5 bg-white p-4">
            <p className="text-sm font-semibold">{c.name}</p>
            <p className="text-xs text-text-muted">{c.purpose}</p>
          </div>
        ))}
      </div>
    );
  }
  return <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Your answer..." className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={3} />;
}

function renderPredict(content, value, set, selected, setSelected) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Predict the outcome"}</h4>
        {content?.sample_answer && <pre className="mt-2 rounded-xl bg-gray-950 p-3 font-mono text-xs text-cyan-300">{content.sample_answer}</pre>}
        {content?.simple_design && <p className="mt-2 text-sm text-text-secondary">{content.simple_design}</p>}
      </div>
      {content?.options && (
        <div className="space-y-2">
          {content.options.map((opt, i) => (
            <button key={i} onClick={() => setSelected(opt.id)} className={`w-full rounded-xl border px-4 py-3 text-left text-sm ${selected === opt.id ? "border-primary bg-primary/5" : "border-black/10"}`}>
              {opt.text}
            </button>
          ))}
        </div>
      )}
      {!content?.options && (
        <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Your prediction..." className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={2} />
      )}
    </div>
  );
}

function renderBuild(content, value, set) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Build the solution"}</h4>
        {content?.guidelines && <ul className="mt-2 space-y-1">{content.guidelines.map((g, i) => <li key={i} className="text-sm text-text-secondary">• {g}</li>)}</ul>}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Write your solution here..." className="w-full rounded-2xl border border-black/10 bg-gray-950 p-4 font-mono text-sm text-cyan-300" rows={8} />
    </div>
  );
}

function renderBreak(content, value, set) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Find the bug"}</h4>
        {content?.sample_bad && <pre className="mt-2 rounded-xl bg-red-50 p-3 font-mono text-xs text-red-700">{content.sample_bad}</pre>}
        {content?.broken_design && <p className="mt-2 text-sm text-text-secondary">{content.broken_design}</p>}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="What's wrong here?" className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={3} />
    </div>
  );
}

function renderDebug(content, value, set, fixes, setFixes) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Fix the problem"}</h4>
        {content?.fixes_required && (
          <div className="mt-3 space-y-2">
            {content.fixes_required.map((f, i) => (
              <label key={i} className="flex items-center gap-2 rounded-xl bg-white p-3">
                <input type="checkbox" checked={fixes.includes(f)} onChange={(e) => { if (e.target.checked) setFixes([...fixes, f]); else setFixes(fixes.filter((x) => x !== f)); }} className="h-4 w-4 rounded" />
                <span className="text-sm">{f}</span>
              </label>
            ))}
          </div>
        )}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Write your improved answer..." className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={4} />
    </div>
  );
}

function renderRetrieval(content, value, set) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Recall what you learned"}</h4>
        {content?.answer && <div className="mt-2 rounded-xl bg-blue-50 p-3"><p className="text-xs font-semibold text-blue-700">Expected:</p><p className="text-sm text-text-secondary">{content.answer}</p></div>}
        {content?.explanation && <p className="mt-2 text-sm text-text-secondary">{content.explanation}</p>}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Recall and write the answer..." className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm" rows={3} />
    </div>
  );
}

function renderTransfer(content, value, set, fixes, setFixes) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
        <h4 className="font-display text-base font-bold">{content?.prompt || "Transfer your knowledge"}</h4>
        {content?.guidelines && <ul className="mt-2 space-y-1">{content.guidelines.map((g, i) => <li key={i} className="text-sm text-text-secondary">• {g}</li>)}</ul>}
        {content?.requirements && <ul className="mt-2 space-y-1">{content.requirements.map((r, i) => <li key={i} className="text-sm text-text-secondary">• {r}</li>)}</ul>}
      </div>
      <textarea value={value} onChange={(e) => set(e.target.value)} placeholder="Write your solution here..." className="w-full rounded-2xl border border-black/10 bg-gray-950 p-4 font-mono text-sm text-cyan-300" rows={8} />
    </div>
  );
}
