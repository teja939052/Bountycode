import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Gift, Sparkles } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function MysteryBoxPage() {
  const [reward, setReward] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [claiming, setClaiming] = useState(false);

  const claim = async () => {
    setClaiming(true);
    try {
      const r = await api.post("/api/v1/mystery-box/claim");
      setReward(r.reward || r);
    } catch (e: any) {
      setReward({ error: e?.message || "Could not claim mystery box" });
    }
    setClaiming(false);
  };

  return (
    <div className="min-h-screen px-4 py-8 max-w-2xl mx-auto flex flex-col items-center justify-center">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3">
          <Gift size={14} className="text-amber-400" />
          <span className="text-xs font-mono text-amber-400">MYSTERY BOX</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Mystery Box</h1>
        <p className="text-sm text-gray-500 mt-1">Claim your daily reward — you never know what you'll get!</p>
      </motion.div>

      {/* Box */}
      {!reward && (
        <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }}
          className="w-48 h-48 rounded-3xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border-2 border-dashed border-amber-500/30 flex flex-col items-center justify-center cursor-pointer hover:scale-105 transition-transform mb-8"
          onClick={claim}>
          <Gift size={48} className="text-amber-400 mb-2" />
          <p className="text-sm font-mono text-amber-400">{claiming ? "Opening..." : "Tap to Open"}</p>
        </motion.div>
      )}

      {/* Reward */}
      {reward && !reward.error && (
        <motion.div initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }}
          className="glass rounded-2xl p-8 text-center w-full">
          <Sparkles size={40} className="text-amber-400 mx-auto mb-4" />
          <p className="text-lg font-display font-bold text-text-primary mb-2">{reward.label || reward.type}</p>
          <p className="text-3xl font-display font-black text-amber-400 mb-2">
            {reward.emoji || "🎉"} +{reward.amount || 0}
          </p>
          {reward.rarity && (
            <span className="inline-block text-[10px] font-mono px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 mt-2">
              {reward.rarity}
            </span>
          )}
          <button onClick={() => { setReward(null); }}
            className="mt-6 px-6 py-2.5 rounded-xl bg-white border-border shadow-card border border-white/10 text-sm font-mono text-gray-400 hover:text-text-primary transition-colors">
            Close
          </button>
        </motion.div>
      )}

      {reward?.error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="glass rounded-2xl p-8 text-center w-full">
          <p className="text-sm text-red-400 font-mono">{reward.error}</p>
          <button onClick={() => setReward(null)}
            className="mt-4 px-6 py-2.5 rounded-xl bg-white border-border shadow-card border border-white/10 text-sm font-mono text-gray-400 hover:text-text-primary transition-colors">
            Try Again
          </button>
        </motion.div>
      )}
    </div>
  );
}
