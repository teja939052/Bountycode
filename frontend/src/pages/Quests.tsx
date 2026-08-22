import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ScrollText, CheckCircle2, Clock, Zap, TrendingUp, CircleDot } from "lucide-react";
import { rpgApi } from "../services/api/rpg";
import { useJuice } from "../juice/JuiceProvider";
import Spinner from "../components/ui/Spinner";

export default function Quests() {
  const [chains, setChains] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const { showXP, play } = useJuice();

  useEffect(() => {
    rpgApi.quests()
      .then((d: any) => { setChains(d || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleCompleteStep = async (questId: string, stepId: string) => {
    try {
      const res = await rpgApi.completeQuestStep(questId, stepId);
      const xp = res.xp_earned || 0;
      if (xp > 0) {
        showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
        play(res.chain_complete ? "levelUp" : "xpCollect");
        setMessage(`+${xp} XP! ${res.chain_complete ? "Chain Complete!" : ""}`);
      } else {
        setMessage("Step already completed");
      }
      const updated = await rpgApi.quests();
      setChains(updated || []);
      setTimeout(() => setMessage(""), 3000);
    } catch {
      setMessage("Failed to update progress");
      setTimeout(() => setMessage(""), 2000);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  const totalSteps = chains.reduce((s, c) => s + (c.total_steps || 0), 0);
  const completedSteps = chains.reduce((s, c) => s + (c.completed_steps || 0), 0);
  const totalXp = chains.reduce((s, c) => s + (c.reward_xp || 0), 0);

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-3">
          <ScrollText size={14} className="text-emerald-400" />
          <span className="text-xs font-mono text-emerald-400">QUESTS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Quest Chains</h1>
        <p className="text-sm text-gray-500 mt-1">Complete multi-step challenges for big XP rewards</p>
      </motion.div>

      {message && (
        <div className="mb-4 rounded-xl border border-green-500/30 bg-green-500/10 px-4 py-2 text-sm text-green-400 font-mono text-center">
          {message}
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
        <div className="glass rounded-xl p-4 text-center">
          <p className="text-2xl font-display font-black text-emerald-400">{completedSteps}/{totalSteps}</p>
          <p className="text-[10px] font-mono text-gray-500 mt-1">Steps Done</p>
        </div>
        <div className="glass rounded-xl p-4 text-center">
          <p className="text-2xl font-display font-black text-brand-sky">{chains.filter(c => c.unlocked).length}</p>
          <p className="text-[10px] font-mono text-gray-500 mt-1">Active Chains</p>
        </div>
        <div className="glass rounded-xl p-4 text-center">
          <p className="text-2xl font-display font-black text-amber-400">{chains.filter(c => c.is_complete).length}</p>
          <p className="text-[10px] font-mono text-gray-500 mt-1">Completed</p>
        </div>
      </div>

      <div className="space-y-3">
        {chains.map((chain: any) => (
          <motion.div key={chain.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            className={`rounded-2xl border p-5 transition-all ${chain.unlocked
              ? "border-nature-leaf/20 bg-surface-card hover:border-nature-leaf/30"
              : "border-nature-leaf/10 bg-white opacity-60"
            }`}>
            <div className="flex items-start gap-4 mb-3">
              <div className="text-3xl">{chain.icon}</div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h4 className="text-sm font-bold text-text-primary">{chain.title}</h4>
                  {!chain.unlocked && <span className="text-[10px] font-mono text-gray-400">🔒 Locked</span>}
                  {chain.is_complete && <CheckCircle2 className="w-4 h-4 text-green-400" />}
                </div>
                <p className="text-xs text-gray-500 mt-0.5">{chain.description}</p>
                <div className="flex items-center gap-3 mt-2 text-[10px] font-mono text-gray-400">
                  <span>{chain.completed_steps}/{chain.total_steps} steps</span>
                  <span>{chain.progress_pct}%</span>
                  <span>{chain.reward_xp} XP reward</span>
                </div>
                <div className="mt-2 h-2 rounded-full bg-gray-100 overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-blue-500 transition-all"
                    style={{ width: `${chain.progress_pct}%` }} />
                </div>
              </div>
            </div>
            {chain.unlocked && (
              <div className="space-y-2 ml-12">
                {chain.steps.map((step: any) => (
                  <div key={step.id} className="flex items-center gap-3 px-3 py-2 rounded-xl bg-gray-50 border border-gray-100">
                    <CircleDot className="w-4 h-4 text-gray-300 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-text-primary font-medium truncate">{step.title}</p>
                      <p className="text-[10px] text-gray-400">{step.description}</p>
                    </div>
                    {!chain.is_complete && (
                      <button onClick={() => handleCompleteStep(chain.id, step.id)}
                        className="text-[10px] font-mono text-emerald-600 hover:text-emerald-500 px-2 py-1 rounded-lg bg-emerald-50 border border-emerald-200 transition-all shrink-0">
                        Complete
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        ))}
        {chains.length === 0 && (
          <div className="text-center py-12 text-gray-400 text-sm">No quest chains available yet. Keep leveling up!</div>
        )}
      </div>
    </div>
  );
}
