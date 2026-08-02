import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import {
  Shield, Calendar, CheckCircle2, ShoppingCart, Lock,
  AlertTriangle, Sparkles, Coins, History,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function StreakFreeze() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [purchasing, setPurchasing] = useState(false);
  const [activating, setActivating] = useState(false);

  useEffect(() => {
    fetchStatus();
  }, []);

  async function fetchStatus() {
    try {
      setLoading(true);
      const data = await api.gamification.getStreakFreezeStatus();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to load streak freeze status");
    } finally {
      setLoading(false);
    }
  }

  const handleBuy = useCallback(async () => {
    setPurchasing(true);
    try {
      await api.gamification.buyStreakFreeze();
      await fetchStatus();
      setPurchasing(false);
    } catch (err) {
      setError(err.message || "Purchase failed");
      setPurchasing(false);
    }
  }, []);

  const handleActivate = useCallback(async () => {
    setActivating(true);
    try {
      await api.gamification.buyStreakFreeze();
      await fetchStatus();
      setActivating(false);
    } catch (err) {
      setError(err.message || "Activation failed");
      setActivating(false);
    }
  }, []);

  if (loading) return <div className="p-6"><Spinner /></div>;

  const streak = status?.current_streak || 0;
  const freezeCount = status?.streak_freeze_count || 0;
  const freezeCost = status?.streak_freeze_cost || 300;
  const hasActiveFreeze = status?.active_freeze || false;
  const freezeHistory = status?.freeze_history || [];
  const canAfford = (status?.coins || 0) >= freezeCost;

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-display font-black text-text-primary flex items-center gap-2">
          <Shield size={24} className="text-blue-400" />
          Streak Freeze
        </h1>
        <div className="flex items-center gap-2 bg-blue-500/10 px-4 py-2 rounded-xl border border-blue-500/20">
          <span className="font-mono text-blue-400">Streak: {streak} 🔥</span>
        </div>
      </div>

      {error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl p-3 mb-4 text-sm font-mono">
          {error}
        </motion.div>
      )}

      <div className="space-y-4">
        <motion.div className="glass rounded-xl p-6 text-center">
          <div className="w-16 h-16 bg-blue-500/10 border-2 border-blue-500/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <Shield size={32} className="text-blue-400" />
          </div>
          <h2 className="text-xl font-bold text-text-primary mb-2">Protect Your Streak</h2>
          <p className="text-sm text-gray-400 font-mono mb-4">
            Your current streak is <span className="text-orange-400 font-bold">{streak} days</span>.
            A Streak Freeze protects your streak when you can't practice.
          </p>

          {hasActiveFreeze ? (
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
              className="bg-green-500/10 border border-green-500/20 rounded-xl p-4 mb-4">
              <p className="text-green-400 font-mono text-sm flex items-center justify-center gap-2">
                <CheckCircle2 size={16} /> Your streak is protected!
              </p>
            </motion.div>
          ) : freezeCount > 0 ? (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleActivate}
              disabled={activating}
              className="mx-auto px-6 py-3 bg-blue-500/20 border border-blue-500/30 text-blue-400 rounded-xl font-mono text-sm hover:bg-blue-500/30 transition-all flex items-center gap-2">
              {activating ? <Spinner size={16} /> : <Shield size={16} />}
              {activating ? "Activating..." : `Activate Streak Freeze (${freezeCount} owned)`}
            </motion.button>
          ) : (
            <motion.button
              whileHover={canAfford ? { scale: 1.02 } : {}}
              whileTap={canAfford ? { scale: 0.98 } : {}}
              onClick={handleBuy}
              disabled={purchasing || !canAfford}
              className={`mx-auto px-6 py-3 rounded-xl font-mono text-sm flex items-center gap-2 transition-all ${
                canAfford
                  ? "bg-blue-500/20 border border-blue-500/30 text-blue-400 hover:bg-blue-500/30"
                  : "bg-gray-500/10 border border-gray-500/30 text-gray-500 cursor-not-allowed"
              }`}>
              {purchasing ? <Spinner size={16} /> : <ShoppingCart size={16} />}
              {purchasing ? "Purchasing..." : !canAfford ? <><Lock size={14} /> Need {freezeCost} <Coins size={14} className="inline text-yellow-400" /></> : "Buy Streak Freeze"}
            </motion.button>
          )}

          {!canAfford && freezeCount === 0 && (
            <p className="text-xs text-gray-500 font-mono mt-2 flex items-center justify-center gap-1">
              <AlertTriangle size={12} /> You need {freezeCost} coins to buy a Streak Freeze
            </p>
          )}
        </motion.div>

        <motion.div className="glass rounded-xl p-4">
          <h3 className="font-bold text-text-primary mb-3 flex items-center gap-2">
            <History size={16} className="text-gray-400" /> Freeze History
          </h3>
          {freezeHistory.length > 0 ? (
            <div className="space-y-2">
              {freezeHistory.slice(0, 5).map((entry, i) => (
                <div key={i} className="flex items-center justify-between text-xs font-mono">
                  <span className="text-gray-400">
                    {entry.date || "Unknown date"}
                  </span>
                  <span className={entry.saved ? "text-green-400" : "text-red-400"}>
                    {entry.saved ? "Saved streak" : "Expired"}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-gray-500 font-mono">No freeze history yet. Buy one to protect your streak!</p>
          )}
        </motion.div>

        <motion.div className="bg-blue-500/5 border border-blue-500/20 rounded-xl p-4">
          <div className="flex items-start gap-2">
            <AlertTriangle size={14} className="text-blue-400 mt-0.5 shrink-0" />
            <div>
              <p className="text-xs font-bold text-blue-300 uppercase tracking-wider mb-1">How It Works</p>
              <ul className="text-xs font-mono text-gray-400 space-y-0.5">
                <li>• Buy a Streak Freeze before your streak breaks</li>
                <li>• It activates automatically when you miss a day</li>
                <li>• Your streak continues — no interruption</li>
                <li>• One freeze per purchase, lasts 24 hours once activated</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
