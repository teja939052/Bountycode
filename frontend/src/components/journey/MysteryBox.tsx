import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Gift, Sparkles, Lock, Coins } from "lucide-react";

interface MysteryBoxProps {
  box: {
    id: string;
    title: string;
    icon: string;
    description: string;
    hint: string;
    mental_model: string;
    xp_reward: number;
    coin_reward: number;
    rarity: string;
    color: string;
  };
  index: number;
  isOpen: boolean;
  onOpen: () => void;
}

const RARITY_STYLES: Record<string, { bg: string; border: string; glow: string }> = {
  common: { bg: "from-slate-100 to-slate-200", border: "border-slate-300", glow: "shadow-slate-200" },
  rare: { bg: "from-blue-100 to-blue-200", border: "border-blue-300", glow: "shadow-blue-200" },
  epic: { bg: "from-purple-100 to-purple-200", border: "border-purple-300", glow: "shadow-purple-200" },
  legendary: { bg: "from-amber-100 to-amber-200", border: "border-amber-300", glow: "shadow-amber-200" },
};

/**
 * Mystery box — a gamified hint unlock.
 *
 * Closed: shows a locked box with rarity styling.
 * Opened: reveals the hint + mental model + reward.
 */
export function MysteryBox({ box, index, isOpen, onOpen }: MysteryBoxProps) {
  const [showHint, setShowHint] = useState(false);
  const style = RARITY_STYLES[box.rarity] || RARITY_STYLES.common;

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: index * 0.1 }}
      className="relative"
    >
      {!isOpen ? (
        /* Closed box */
        <motion.button
          whileHover={{ scale: 1.03, y: -2 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => {
            onOpen();
            setShowHint(true);
          }}
          className={`w-full flex items-center gap-3 rounded-xl border-2 ${style.border} bg-gradient-to-r ${style.bg} p-4 text-left shadow-sm hover:shadow-md transition-shadow`}
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-white/60 text-xl">
            <Lock className="w-5 h-5 text-slate-400" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-slate-700">{box.title}</span>
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-medium">{box.rarity}</span>
            </div>
            <p className="text-xs text-slate-500 truncate">{box.description}</p>
          </div>
          <div className="flex items-center gap-1 text-xs text-yellow-600 font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            <span>+{box.xp_reward}</span>
          </div>
        </motion.button>
      ) : (
        /* Opened box */
        <motion.div
          initial={{ rotateY: 90 }}
          animate={{ rotateY: 0 }}
          transition={{ type: "spring", damping: 20 }}
          className={`rounded-xl border ${style.border} bg-white p-4 shadow-md`}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{box.icon}</span>
            <span className="text-sm font-semibold text-slate-700">{box.title}</span>
            <span className="ml-auto text-xs text-yellow-600 font-medium flex items-center gap-1">
              <Sparkles className="w-3 h-3" /> +{box.xp_reward} Diamonds
            </span>
          </div>

          <AnimatePresence>
            {showHint && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="rounded-lg bg-slate-50 p-3 mb-2">
                  <p className="text-sm text-slate-700 font-medium">{box.hint}</p>
                </div>
                {box.mental_model && (
                  <div className="rounded-lg bg-primary/5 border border-primary/10 p-2">
                    <p className="text-[11px] text-primary font-medium">
                      💡 Remember: {box.mental_model}
                    </p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      )}
    </motion.div>
  );
}

/**
 * Mystery box container — shows all boxes for a problem.
 */
export function MysteryBoxContainer({
  boxes,
  openedIndices,
  onOpen,
}: {
  boxes: Array<MysteryBoxProps["box"]>;
  openedIndices: Set<number>;
  onOpen: (index: number) => void;
}) {
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 mb-3">
        <Gift className="w-4 h-4 text-primary" />
        <span className="text-xs font-mono uppercase tracking-widest text-text-muted">
          Mystery Boxes ({openedIndices.size}/{boxes.length} opened)
        </span>
      </div>
      {boxes.map((box, i) => (
        <MysteryBox
          key={box.id}
          box={box}
          index={i}
          isOpen={openedIndices.has(i)}
          onOpen={() => onOpen(i)}
        />
      ))}
    </div>
  );
}
