// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";

export function Toast({
  message,
  visible,
  onClose,
  tone = "info",
}: {
  message: string;
  visible: boolean;
  onClose?: () => void;
  tone?: "info" | "success" | "error";
}) {
  const tones: Record<string, string> = {
    info: "border-brand-sky/30 bg-brand-sky/10 text-brand-sky",
    success: "border-emerald-400/30 bg-emerald-400/10 text-emerald-600",
    error: "border-rose-400/30 bg-rose-400/10 text-rose-600",
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          className={`fixed bottom-6 right-6 z-50 rounded-xl border px-4 py-3 text-sm shadow-lg backdrop-blur-md ${tones[tone]}`}
        >
          <div className="flex items-center gap-3">
            <span>{message}</span>
            {onClose && (
              <button onClick={onClose} className="text-xs opacity-70 hover:opacity-100">
                Close
              </button>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export function NotificationCard({
  title,
  body,
  tone = "info",
  className = "",
}: {
  title: string;
  body: string;
  tone?: "info" | "success" | "error";
  className?: string;
}) {
  const tones: Record<string, string> = {
    info: "border-brand-sky/30 bg-brand-sky/5",
    success: "border-emerald-400/30 bg-emerald-400/5",
    error: "border-rose-400/30 bg-rose-400/5",
  };

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={`rounded-2xl border p-4 shadow-sm ${tones[tone]} ${className}`}
    >
      <div className="text-sm font-semibold text-text-primary">{title}</div>
      <div className="mt-1 text-sm text-text-secondary">{body}</div>
    </motion.div>
  );
}
