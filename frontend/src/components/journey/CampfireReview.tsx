import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";
import { sfx } from "../../utils/soundsea.ts";

interface ReviewCard {
  skill_id?: string;
  concept_id?: string;
  concept_name?: string;
  title?: string;
  estimated_minutes?: number;
  [key: string]: unknown;
}

interface Props {
  reviews: ReviewCard[];
  onClose: () => void;
}

/**
 * Campfire Rest — the map's SRS surface.
 *
 * First real consumer of the canonical review sink:
 * POST /api/v1/study/activity {type:"review", skill_id, passed}.
 * No new backend, no new collections. Closing (or finishing) refreshes
 * the map so the campfire node vanishes the moment reviews clear.
 */
export default function CampfireReview({ reviews, onClose }: Props) {
  const queryClient = useQueryClient();
  const [index, setIndex] = useState(0);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  const refresh = () => {
    void queryClient.invalidateQueries({ queryKey: ["map", "state"] });
    void queryClient.invalidateQueries({ queryKey: ["journey", "state"] });
  };

  const grade = async (passed: boolean) => {
    const card = reviews[index];
    if (!card || busy) return;
    setBusy(true);
    try {
      await api.journey.recordActivity({
        type: "review",
        skill_id: card.skill_id ?? card.concept_id ?? "",
        passed,
        score: passed ? 100 : 0,
        attempts: 1,
        time_spent: 0,
      });
      sfx(passed ? "chime" : "pop");
    } catch {
      /* best-effort: SRS never blocks the journey */
    } finally {
      setBusy(false);
    }
    if (index + 1 >= reviews.length) {
      setDone(true);
      refresh();
    } else {
      setIndex(index + 1);
    }
  };

  const close = () => {
    refresh();
    onClose();
  };

  const card = reviews[index];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-end justify-center bg-black/60 p-4 sm:items-center"
      role="dialog"
      aria-label="Campfire rest reviews"
      onClick={close}
    >
      <motion.div
        initial={{ y: 60, scale: 0.97 }}
        animate={{ y: 0, scale: 1 }}
        exit={{ y: 60, opacity: 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 28 }}
        className="w-full max-w-md rounded-3xl border border-orange-200/30 bg-gradient-to-b from-[#2a1608] to-[#120a04] p-6 text-amber-50"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="text-center text-4xl" aria-hidden>🔥</div>
        <h2 className="mt-1 text-center text-lg font-bold">Campfire Rest</h2>
        <AnimatePresence mode="wait">
          {done || reviews.length === 0 ? (
            <motion.div key="done" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-3 text-center">
              <p className="text-sm opacity-80">
                {reviews.length === 0
                  ? "No embers left — your memory is warm."
                  : "Embers settled. The guardian path is clear."}
              </p>
              <button
                onClick={close}
                className="mt-4 min-h-[52px] w-full rounded-xl bg-orange-400 py-3 font-bold text-orange-950"
              >
                ⛵ Back to the voyage
              </button>
            </motion.div>
          ) : (
            <motion.div key={index} initial={{ x: 40, opacity: 0 }} animate={{ x: 0, opacity: 1 }} exit={{ x: -40, opacity: 0 }}>
              <p className="mt-2 text-center text-xs opacity-60">
                Ember {index + 1} of {reviews.length}
              </p>
              <p className="mt-1 text-center font-mono text-sm text-amber-200">
                {String(card?.concept_name ?? card?.title ?? card?.skill_id ?? card?.concept_id ?? "a past lesson")}
              </p>
              <p className="mt-1 text-center text-xs opacity-60">
                Recall it cold. No notes, no hints — that&apos;s what makes it stick.
              </p>
              <div className="mt-4 grid grid-cols-2 gap-2">
                <button
                  onClick={() => void grade(false)}
                  disabled={busy}
                  className="min-h-[52px] rounded-xl border border-white/15 bg-white/5 py-3 text-sm font-bold disabled:opacity-50"
                >
                  🌫️ Still shaky
                </button>
                <button
                  onClick={() => void grade(true)}
                  disabled={busy}
                  className="min-h-[52px] rounded-xl bg-lime-500 py-3 text-sm font-bold text-emerald-950 disabled:opacity-50"
                >
                  🔥 Got it cold
                </button>
              </div>
              <button onClick={close} className="mt-2 w-full py-2 text-center text-xs opacity-50">
                Rest later
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}
