// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";
import { X, RotateCcw, Lightbulb } from "lucide-react";
import { useMotion } from "../../hooks/useMotion";
import { BountyCodeButton } from "./BountyCodeButton";

interface RepairOverlayProps {
  visible: boolean;
  title: string;
  explanation: string;
  hint?: string;
  onDismiss: () => void;
  onRetry: () => void;
}

export function RepairOverlay({ visible, title, explanation, hint, onDismiss, onRetry }: RepairOverlayProps) {
  const { stateTransition } = useMotion();

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={stateTransition("repair")}
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
          onClick={onDismiss}
        >
          <motion.div
            initial={{ scale: 0.92, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.92, opacity: 0, y: 20 }}
            transition={stateTransition("repair")}
            className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-orange-100 flex items-center justify-center">
                  <Lightbulb size={16} className="text-orange-600" />
                </div>
                <h3 className="text-lg font-bold text-text-primary">{title}</h3>
              </div>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={onDismiss}
                className="rounded-full p-1 text-text-muted hover:text-text-primary transition-colors"
              >
                <X size={20} />
              </motion.button>
            </div>

            <div className="space-y-4">
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1, ...stateTransition("focus") }}
                className="p-4 rounded-xl bg-orange-50 border border-orange-200"
              >
                <p className="text-sm text-orange-800 leading-relaxed">{explanation}</p>
              </motion.div>

              {hint && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2, ...stateTransition("focus") }}
                  className="p-4 rounded-xl bg-amber-50 border border-amber-200"
                >
                  <p className="text-xs font-bold text-amber-700 uppercase tracking-widest mb-1">Hint</p>
                  <p className="text-sm text-amber-800">{hint}</p>
                </motion.div>
              )}

              <div className="flex gap-3">
                <BountyCodeButton
                  variant="secondary"
                  onClick={onDismiss}
                  className="flex-1"
                >
                  Dismiss
                </BountyCodeButton>
                <BountyCodeButton
                  variant="primary"
                  onClick={onRetry}
                  className="flex-1"
                  leftIcon={<RotateCcw size={14} />}
                >
                  Try Again
                </BountyCodeButton>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
