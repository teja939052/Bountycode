import { useState } from "react";
import { Lightbulb, Loader2 } from "lucide-react";
import api from "../../services/api";

type Props = {
  slug: string;
  stepIndex: number;
  localHints?: string[];
};

/**
 * Progressive hints for a lesson step.
 * Prefers authored `step.hints` from the lesson payload; if empty, asks the server.
 * Server policy: hints never award mastery.
 */
export function LessonStepHints({ slug, stepIndex, localHints = [] }: Props) {
  const [revealed, setRevealed] = useState(0);
  const [serverHints, setServerHints] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [exhausted, setExhausted] = useState(false);

  const combined = [...localHints, ...serverHints.filter((h) => !localHints.includes(h))];
  const canRevealMore = !exhausted && (revealed < combined.length || localHints.length === 0);

  async function revealNext() {
    if (revealed < combined.length) {
      setRevealed((n) => n + 1);
      return;
    }
    // Need server hint
    setLoading(true);
    try {
      const res = await api.companyLessons.getHint(slug, stepIndex, revealed);
      const hint = (res as any)?.hint;
      if (hint) {
        setServerHints((prev) => (prev.includes(hint) ? prev : [...prev, hint]));
        setRevealed((n) => n + 1);
      }
      if ((res as any)?.exhausted || !(res as any)?.hint) {
        setExhausted(true);
      }
    } catch {
      setExhausted(true);
    } finally {
      setLoading(false);
    }
  }

  if (localHints.length === 0 && exhausted && revealed === 0) {
    return null;
  }

  return (
    <div className="mb-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3">
      <button
        type="button"
        onClick={() => void revealNext()}
        disabled={loading || (!canRevealMore && revealed >= combined.length)}
        className="inline-flex items-center gap-2 text-xs font-semibold text-amber-200 disabled:opacity-50"
      >
        {loading ? <Loader2 size={14} className="animate-spin" /> : <Lightbulb size={14} />}
        {revealed >= combined.length && exhausted
          ? "All hints revealed"
          : `Reveal hint ${Math.min(revealed + 1, Math.max(combined.length, revealed + 1))}`}
      </button>
      {revealed > 0 && combined[revealed - 1] && (
        <p className="mt-2 text-xs leading-relaxed text-text-secondary">{combined[revealed - 1]}</p>
      )}
      <p className="mt-2 text-[10px] text-text-secondary/80">Hints help you learn — they never grant mastery.</p>
    </div>
  );
}
