import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Shield, Snowflake, Flame, Coins, X, AlertTriangle } from "lucide-react";
import api from "../services/api";
import { useGamification } from "../hooks/useGamification";

interface StreakFreezeModalProps {
  open: boolean;
  onClose: () => void;
}

interface FreezeStatus {
  streak_freezes?: number;
  streak?: number;
  days_since_practice?: number;
  streak_in_danger?: boolean;
  can_freeze?: boolean;
  cost?: number;
}

export default function StreakFreezeModal({ open, onClose }: StreakFreezeModalProps) {
  const { refetch } = useGamification();
  const [status, setStatus] = useState<FreezeStatus | null>(null);
  const [buying, setBuying] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setMessage(null);
    setError(null);
    setBuying(false);
    setStatus(null);
    api.gamification
      .getStreakFreezeStatus()
      .then((s) => setStatus(s))
      .catch(() => setError("Could not load streak protection status"));
  }, [open]);

  const handleBuy = async () => {
    setBuying(true);
    setMessage(null);
    setError(null);
    try {
      const res = await api.gamification.buyStreakFreeze();
      if (res?.success) {
        setMessage(`❄️ Freeze added! You now have ${(status?.streak_freezes || 0) + 1}.`);
        setStatus((prev) => ({ ...prev, streak_freezes: (prev?.streak_freezes || 0) + 1 }));
        window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp: 0 } }));
        refetch();
      } else {
        setError(res?.message || "Purchase failed");
      }
    } catch (e) {
      setError(e.message || "Purchase failed");
    } finally {
      setBuying(false);
    }
  };

  const danger = status?.streak_in_danger;
  const freezes = status?.streak_freezes || 0;
  const cost = status?.cost || 50;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-3xl p-6 max-w-sm w-full shadow-soft-lg border border-white/60"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-sky-400 to-blue-600 flex items-center justify-center shadow-soft-md">
                  <Snowflake size={22} className="text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-display font-bold text-text-primary leading-tight">Streak Freeze</h3>
                  <p className="text-xs text-text-light">Protect your streak, one missed day forgiven</p>
                </div>
              </div>
              <button onClick={onClose} className="p-1 text-text-light hover:text-text-primary">
                <X size={18} />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="rounded-2xl border border-white/60 bg-brand-primary/5 p-3 text-center">
                <Shield size={16} className="mx-auto text-sky-500 mb-1" />
                <div className="text-2xl font-display font-bold text-text-primary">{freezes}</div>
                <div className="text-[10px] font-mono text-text-light">freezes held</div>
              </div>
              <div className="rounded-2xl border border-white/60 bg-brand-primary/5 p-3 text-center">
                <Flame size={16} className={`mx-auto mb-1 ${danger ? "text-red-500" : "text-orange-400"}`} />
                <div className="text-2xl font-display font-bold text-text-primary">{status?.streak || 0}</div>
                <div className="text-[10px] font-mono text-text-light">day streak</div>
              </div>
            </div>

            {danger && (
              <div className="flex items-start gap-2 mb-4 px-3 py-2.5 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600">
                <AlertTriangle size={16} className="shrink-0 mt-0.5" />
                <span>
                  {status?.days_since_practice === 1
                    ? "You missed yesterday — a freeze will keep your streak alive."
                    : "Your streak is in danger. Practice today or use a freeze."}
                </span>
              </div>
            )}

            {message && (
              <div className="mb-4 px-3 py-2.5 rounded-xl bg-green-50 border border-green-200 text-sm text-green-600">
                {message}
              </div>
            )}
            {error && (
              <div className="mb-4 px-3 py-2.5 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600">
                {error}
              </div>
            )}

            <button
              onClick={handleBuy}
              disabled={buying}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-blue-600 text-white font-display font-bold text-sm disabled:opacity-50 shadow-soft-md hover:shadow-soft-lg transition-shadow"
            >
              {buying ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Buying...
                </span>
              ) : (
                <>
                  <Snowflake size={16} />
                  Buy Streak Freeze
                  <Coins size={14} className="text-yellow-300" />
                  {cost}
                </>
              )}
            </button>
            <p className="mt-2 text-center text-[10px] font-mono text-text-light">
              Freezes are auto-consumed if you miss a day and open the app.
            </p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
