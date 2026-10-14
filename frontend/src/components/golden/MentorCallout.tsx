// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";
import { MentorAvatar } from "../../design-system/Mentor";
import { useMentor } from "../../hooks/useMentor";
import type { MentorMood } from "../../design-system/Mentor";

export interface MentorCalloutProps {
  phase: "idle" | "loading" | "intro" | "active" | "correcting" | "repair" | "success" | "mastery" | "boss" | "stuck" | "complete";
  mistakeCount?: number;
  idleSeconds?: number;
  /** override automatic line */
  message?: string;
  mood?: MentorMood;
  /** compact places avatar inline; full becomes a larger card */
  size?: "compact" | "full";
  className?: string;
  /** backend-derived mentor line from journey state */
  backendMentor?: { mood: MentorMood; message: string; phase: string };
}

export function MentorCallout({
  phase,
  mistakeCount,
  idleSeconds,
  message,
  mood,
  size = "compact",
  className = "",
  backendMentor,
}: MentorCalloutProps) {
  const derived = useMentor({ phase, mistakeCount, idleSeconds });
  const resolvedMood = backendMentor ? backendMentor.mood : (mood || derived.mood);
  const resolvedMessage = backendMentor ? backendMentor.message : (message || derived.message);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 8, scale: 0.98 }}
        transition={{ duration: 0.28 }}
        className={`flex items-start gap-3 ${className}`}
      >
        <MentorAvatar size={size === "full" ? 72 : 44} mood={resolvedMood} />
        <div
          className={
            size === "full"
              ? "bounty-card flex-1"
              : "surface-bg surface-border relative rounded-xl border px-4 py-2.5 shadow-card"
          }
        >
          <p className="text-xs font-bold uppercase tracking-widest text-primary-dark">Captain Byte</p>
          <p className={`text-sm leading-snug text-text ${size === "full" ? "mt-1" : ""}`}>{resolvedMessage}</p>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
