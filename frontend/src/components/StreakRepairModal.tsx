import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Flame, Coins, X, AlertTriangle, Lock } from "lucide-react";
import api from "../services/api";
import { useGamification } from "../hooks/useGamification";
import { StreakRepairResult } from "../services/api/gamification";

interface StreakRepairModalProps {
  open: boolean;
  onClose: () => void;
}

interface RepairStatus {
  cost?: number;
  streak_freezes?: number;
  streak?: number;
  days_since_practice?: number;
  streak_in_danger?: boolean;
  plan?: string;
  monthly_quota?: number | null;
  remaining?: number | null;
}

export default function StreakRepairModal({ open, onClose }: StreakRepairModalProps) {
  const { refetch } = useGamification();
  const [status, setStatus] = useState<RepairStatus | null>(null);
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
      .getStreakRepairStatus()
      .then((s) => setStatus(s))
      .catch(() => setError("Could not load streak repair status"));
  }, [open]);

  const handleBuy = async () => {
    setBuying(true);
    setMessage(null);
    setError(null);
    try {
      const res = (await api.gamification.buyStreakRepair()) as StreakRepairResult;
      if (res?.success) {
        setMessage(res.message || "Streak repaired!");
        refetch();
      } else if (res?.upgrade_required) {
        // Show paywall: free users exhausted their monthly Streak Repair quota.
        setError(
          res.message ||
            "Your free Streak Repairs for this month are used up. Upgrade to Pro to protect your streak anytime."
        );
      } else {
        setError(res?.message || "Purchase failed");
      }
    } catch (e) {
      setError((e as Error)?.message || "Purchase failed");
    } finally {
      setBuying(false);
    }
  };

  const streak = status?.streak || 0;
  const cost = status?.cost || 0;
  const inDanger = status?.streak_in_danger;
  const isFree = !status?.plan || status.plan === "free";
  const quota = isFree ? status?.monthly_quota : null;
  const remaining = isFree ? status?.remaining : null;

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
            className="bg-white rounded-3xl p-6 max-w-sm w-full shadow-lg border border-white/60"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-orange-400 to-red-600 flex items-center justify-center shadow-md">
                  <Flame size={22} className="text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-text-primary leading-tight">Streak Repair</h3>
                  <p className="text-xs text-gray-500">Restore a streak broken today</p>
                </div>
              </div>
              <button onClick={onClose} className="p-1 text-gray-500 hover:text-gray-700">
                <X size={18} />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="rounded-2xl border border-gray-200 bg-gray-50 p-3 text-center">
                <Flame size={16} className={`mx-auto mb-1 ${inDanger ? "text-red-500" : "text-orange-400"}`} />
                <div className="text-2xl font-bold text-gray-800">{streak}</div>
                <div className="text-[10px] font-mono text-gray-500">day streak</div>
              </div>
              <div className="rounded-2xl border border-gray-200 bg-gray-50 p-3 text-center">
                <Coins size={16} className="mx-auto text-yellow-500 mb-1" />
                <div className="text-2xl font-bold text-gray-800">{status?.streak_freezes || 0}</div>
                <div className="text-[10px] font-mono text-gray-500">freezes held</div>
              </div>
            </div>

            {inDanger && (
              <div className="flex items-start gap-2 mb-4 px-3 py-2.5 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600">
                <AlertTriangle size={16} className="shrink-0 mt-0.5" />
                <span>
                  You missed yesterday — a freeze/streak repair will keep your streak alive.
                </span>
              </div>
            )}

            {isFree && quota != null && (
              <div className="flex items-center gap-2 mb-4 px-3 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-sm text-gray-700">
                <Lock size={16} className="text-blue-500" />
                <span>Free users get {quota} streak repair{quota !== 1 ? "s" : ""} per month — {remaining} left.</span>
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
              className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-gradient-to-r from-orange-500 to-red-600 text-white font-bold text-sm disabled:opacity-50 shadow-md"
            >
              {buying ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Repairing...
                </span>
              ) : (
                <>
                  <Flame size={16} />
                  Repair Streak
                  <Coins size={14} className="text-yellow-300" />
                  {cost}
                </>
              )}
            </button>
            {isFree && (
              <p className="mt-2 text-center text-[10px] font-mono text-gray-500">
                Pro/Lifetime: never run out of streak repairs.
              </p>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
