import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Skull, Trophy, Flame, RefreshCw, Crown } from "lucide-react";
import BountyCard from "../components/BountyCard";
import { requestWithRetry } from "../services/api/request";
import Skeleton from "../components/ui/Skeleton";

export default function BountyPage() {
  const [card, setCard] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"card" | "leaderboard">("card");

  const load = async () => {
    setLoading(true);
    try {
      const [c, lb] = await Promise.all([
        requestWithRetry("/api/v1/bounty/card"),
        requestWithRetry("/api/v1/bounty/leaderboard?limit=20"),
      ]);
      setCard(c);
      setLeaderboard(Array.isArray(lb) ? lb : []);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  if (loading) {
    return (
      <div className="min-h-screen page-surface px-4 py-8 max-w-4xl mx-auto">
        <Skeleton className="h-10 w-48 mb-6 bg-border" />
        <div className="flex justify-center"><Skeleton className="h-80 w-72 rounded-2xl bg-border" /></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen page-surface px-4 py-6 sm:py-10 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Skull className="w-6 h-6 text-amber-400" />
          <div>
            <h1 className="text-2xl font-display font-black text-text-primary">Bounty Card</h1>
            <p className="text-xs text-text-muted">Your placement wanted poster</p>
          </div>
        </div>
        <button onClick={load}
          className="flex items-center gap-2 px-3 py-2 rounded-xl bg-surface-2 border border-border text-text-primary text-xs hover:bg-primary-soft transition-all">
          <RefreshCw className="w-3.5 h-3.5" /> Refresh
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-8">
        {([["card", "My Bounty"], ["leaderboard", "Leaderboard"]] as const).map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)}
            className={`px-4 py-2 rounded-xl text-xs font-mono transition-all ${
              tab === key ? "bg-gold-soft text-gold border border-gold/30" : "text-text-muted border border-transparent hover:text-primary"
            }`}>
            {label}
          </button>
        ))}
      </div>

      {tab === "card" && card && (
        <div className="flex flex-col items-center gap-8">
          <BountyCard user={card} size="large" showStats={true} />

          {/* Tier progress */}
          {card.tier?.next_tier && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="w-full max-w-xs rounded-2xl border border-border bg-white p-4 shadow-card">
              <div className="flex items-center justify-between text-xs font-mono mb-2">
                <span style={{ color: card.tier.color }}>{card.tier.title}</span>
                <span className="text-text-muted">{card.tier.next_tier.title}</span>
              </div>
              <div className="h-2 rounded-full bg-border overflow-hidden">
                <motion.div className="h-full rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${(card.tier.progress || 0) * 100}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                  style={{ background: card.tier.color }} />
              </div>
              <p className="text-[10px] text-text-muted font-mono mt-2 text-center">
                {(card.tier.gap_to_next || 0).toLocaleString()} BELLI to next tier
              </p>
            </motion.div>
          )}

          {/* Quick stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-lg">
            {[
              { label: "Problems", value: card.problems_solved || 0, icon: "📋" },
              { label: "Badges", value: card.badges_count || 0, icon: "🏅" },
              { label: "Bosses", value: card.bosses_defeated || 0, icon: "💀" },
              { label: "Readiness", value: `${Math.round(card.readiness || 0)}%`, icon: "🎯" },
            ].map((s) => (
              <div key={s.label} className="rounded-xl border border-border bg-white p-3 text-center shadow-card">
                <p className="text-lg">{s.icon}</p>
                <p className="text-sm font-bold text-text-primary">{s.value}</p>
                <p className="text-[9px] font-mono text-text-muted">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "leaderboard" && (
        <div className="space-y-4">
          {leaderboard.length === 0 && (
            <p className="text-center text-text-muted text-sm py-8">No bounty data yet.</p>
          )}
          {leaderboard.map((entry) => (
            <motion.div key={entry.user_id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-4 rounded-2xl border border-border bg-white p-4 shadow-card hover:border-amber-500/20 transition-all">
              <span className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-black ${
                entry.rank === 1 ? "bg-yellow-500/20 text-yellow-400" :
                entry.rank === 2 ? "bg-gray-300/20 text-gray-300" :
                entry.rank === 3 ? "bg-amber-600/20 text-amber-600" :
                "bg-surface-2 text-text-muted"
              }`}>
                {entry.rank <= 3 ? ["🥇", "🥈", "🥉"][entry.rank - 1] : `#${entry.rank}`}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold text-text-primary truncate">{entry.name}</p>
                <p className="text-[10px] font-mono" style={{ color: entry.tier?.color }}>
                  {entry.tier?.title} · LVL {entry.level}
                </p>
              </div>
              <div className="text-right">
                <p className="text-sm font-black text-gold">{entry.bounty_formatted}</p>
                <p className="text-[9px] text-text-muted">BELLI</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
