import { motion } from "framer-motion";
import { CheckCircle2, Lock, Star } from "lucide-react";
import type { JourneyLevel } from "../../hooks/useJourneyState";
import { useReducedMotion } from "framer-motion";

export default function LevelNode({
  level,
  isCharacterHere,
  onSelect,
}: {
  level: JourneyLevel;
  isCharacterHere: boolean;
  onSelect: () => void;
}) {
  const reduceMotion = useReducedMotion();
  const isCompleted = level.status === "completed";
  const isLocked = level.status === "locked";
  const isCurrent = level.status === "current" || isCharacterHere;

  return (
    <motion.button
      whileHover={!isLocked ? { x: 4 } : {}}
      whileTap={!isLocked ? { scale: 0.98 } : {}}
      onClick={onSelect}
      disabled={isLocked}
      className={`relative flex items-center gap-3 w-full rounded-lg border px-3 py-2.5 text-left transition-all min-h-[48px]
        ${isLocked ? "opacity-40 cursor-not-allowed border-default bg-card" : ""}
        ${isCurrent ? "border-accent-primary bg-accent-primary/5 shadow-sm" : ""}
        ${isCompleted ? "border-accent-primary/30 bg-accent-primary/5" : ""}
        ${!isLocked && !isCurrent && !isCompleted ? "border-default bg-card hover:border-accent-primary/30" : ""}
      `}
    >
      <div className={`absolute -left-[22px] top-1/2 -translate-y-1/2 flex h-6 w-6 items-center justify-center rounded-full border-2 text-[10px]
        ${isCompleted ? "bg-accent-primary border-accent-primary text-white" : ""}
        ${isCurrent ? "bg-accent-primary border-accent-primary text-white animate-pulse" : ""}
        ${isLocked ? "bg-card border-default" : ""}
        ${!isCompleted && !isCurrent && !isLocked ? "bg-card border-default" : ""}
      `}>
        {isCompleted ? <CheckCircle2 className="w-3 h-3" /> :
         isLocked ? <Lock className="w-2.5 h-2.5 text-muted" /> :
         isCurrent ? <Star className="w-3 h-3" /> :
         <span className="text-muted">{level.order}</span>}
      </div>
      <div className="flex h-8 w-8 items-center justify-center rounded-lg text-sm shrink-0 bg-surface">
        {level.icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className={`text-sm font-semibold leading-tight ${level.kind === "boss" ? "text-accent-warm" : "text-primary"}`}>
          {level.title} {level.kind === "boss" && "🐉"}
        </div>
        <div className="text-[10px] text-muted">{level.concept} · +{level.diamonds} Diamonds</div>
      </div>
      {isCharacterHere && (
        <span className="text-xs">🧑‍✈️</span>
      )}
    </motion.button>
  );
}
