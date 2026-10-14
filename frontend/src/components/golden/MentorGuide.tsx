// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";
import { Lightbulb } from "lucide-react";
import { useMotion } from "../../hooks/useMotion";

interface MentorGuideProps {
  mood?: "neutral" | "encouraging" | "explaining" | "correcting" | "celebrating";
  message: string;
  visible?: boolean;
}

const MOOD_STYLES: Record<string, { bg: string; border: string; text: string; icon: string }> = {
  neutral: {
    bg: "bg-brand-softMint",
    border: "border-brand-primary/20",
    text: "text-brand-deep",
    icon: "💬",
  },
  encouraging: {
    bg: "bg-sky-50",
    border: "border-brand-sky/30",
    text: "text-brand-sky",
    icon: "🌱",
  },
  explaining: {
    bg: "bg-amber-50",
    border: "border-reward-gold/30",
    text: "text-amber-700",
    icon: "💡",
  },
  correcting: {
    bg: "bg-orange-50",
    border: "border-orange-200",
    text: "text-orange-700",
    icon: "🔧",
  },
  celebrating: {
    bg: "bg-emerald-50",
    border: "border-emerald-200",
    text: "text-emerald-700",
    icon: "🎉",
  },
};

export function MentorGuide({ mood = "neutral", message, visible = true }: MentorGuideProps) {
  const { stateTransition } = useMotion();
  const style = MOOD_STYLES[mood];

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: 12, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 8, scale: 0.98 }}
          transition={stateTransition("focus")}
          className={`flex items-start gap-3 rounded-2xl border p-4 ${style.bg} ${style.border}`}
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/60 text-lg">
            {style.icon}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Lightbulb size={14} className={style.text} />
              <span className={`text-xs font-bold uppercase tracking-widest ${style.text}`}>
                Teacher
              </span>
            </div>
            <p className={`text-sm leading-relaxed ${style.text}`}>{message}</p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
