import { useState, useEffect } from "react";
import api from "../services/api";
import {
  Trophy, Medal, Star, TrendingUp, Shield,
  ChevronRight, Award, Target, Zap,
  Loader2, BarChart3, Crown,
} from "lucide-react";

const RANK_GRADIENTS = {
  8: "from-gray-400 to-gray-300",
  7: "from-stone-400 to-stone-300",
  6: "from-zinc-400 to-zinc-300",
  5: "from-yellow-600 to-yellow-500",
  4: "from-amber-600 to-amber-500",
  3: "from-orange-600 to-orange-500",
  2: "from-red-500 to-red-400",
  1: "from-purple-600 to-purple-500",
};

const DAN_GRADIENTS = {
  1: "from-blue-600 to-blue-500",
  2: "from-indigo-600 to-indigo-500",
  3: "from-violet-600 to-violet-500",
  4: "from-pink-600 to-pink-500",
  5: "from-rose-600 to-rose-500",
  6: "from-amber-500 to-yellow-400",
};

export default function RankProfile() {
  const [profile, setProfile] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lbPage, setLbPage] = useState(1);
  const [lbTotal, setLbTotal] = useState(0);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [p, lb, bg] = await Promise.all([
        api.getRankProfile(),
        api.getRankLeaderboard(lbPage, 20),
        api.getAllBadges(),
      ]);
      setProfile(p);
      setLeaderboard(lb.leaderboard || []);
      setLbTotal(lb.total || 0);
      setBadges(bg.badges || []);
    } catch (err) {
      console.error("Rank load error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadAll(); }, [lbPage]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 size={32} className="animate-spin text-brand-sky" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-text-light">Could not load rank profile.</p>
      </div>
    );
  }

  const isDan = profile.rank_type === "dan";
  const gradient = isDan ? DAN_GRADIENTS[profile.rank_number] || DAN_GRADIENTS[1] : RANK_GRADIENTS[profile.rank_number] || RANK_GRADIENTS[8];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Rank Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
          <Award className="text-brand-coral" size={32} />
          Rank & Honor
        </h1>
        <p className="text-text-light mt-1">Your Codewars-style progression system</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column — Rank Card */}
        <div className="lg:col-span-1 space-y-6">
          {/* Rank Badge */}
          <div className={`p-6 rounded-2xl bg-gradient-to-br ${gradient} text-text-primary shadow-lg text-center`}>
            <div className="text-6xl font-black mb-2">{profile.rank_number}</div>
            <div className="text-lg font-bold uppercase tracking-widest">{profile.rank_type}</div>
            <div className="text-sm opacity-80 mt-1">{profile.rank_title}</div>
          </div>

          {/* Honor Progress */}
          <div className="p-6 rounded-2xl border border-brand-primary/20 bg-surface-card/90">
            <h3 className="text-sm font-semibold text-text-primary mb-4 flex items-center gap-2">
              <Star size={16} className="text-yellow-500" /> Honor Progress
            </h3>
            <div className="flex items-baseline justify-center gap-1 mb-3">
              <span className="text-4xl font-bold text-text-primary">{profile.honor}</span>
              <span className="text-text-light">honor</span>
            </div>
            <div className="w-full h-3 rounded-full bg-surface-card/50 overflow-hidden mb-2">
              <div
                className="h-full rounded-full bg-gradient-to-r from-brand-sky to-brand-lavender transition-all duration-500"
                style={{ width: `${Math.min(100, profile.progress_percent)}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-text-light">
              <span>{profile.current_tier_honor} honor</span>
              <span>{profile.progress_percent}%</span>
              <span>{profile.next_rank_honor} honor</span>
            </div>
            <div className="mt-3 text-center text-sm text-text-secondary">
              <span className="font-semibold">{profile.honor_needed}</span> honor needed for next rank
            </div>
          </div>

          {/* Badge Collection */}
          <div className="p-6 rounded-2xl border border-brand-primary/20 bg-surface-card/90">
            <h3 className="text-sm font-semibold text-text-primary mb-4 flex items-center gap-2">
              <Medal size={16} className="text-amber-500" /> Badges
              <span className="text-text-light font-normal">({profile.badge_count}/{profile.total_badges})</span>
            </h3>
            <div className="grid grid-cols-3 gap-3">
              {badges.map((badge) => {
                const earned = (profile.badges || []).some((b) => b.id === badge.id);
                return (
                  <div
                    key={badge.id}
                    className={`p-3 rounded-xl border text-center transition-all ${
                      earned
                        ? "border-amber-200 bg-amber-50/50"
                        : "border-brand-primary/20 bg-surface-base/50 opacity-40"
                    }`}
                    title={`${badge.name}: ${badge.description}`}
                  >
                    <div className="text-2xl mb-1">{badge.icon}</div>
                    <div className="text-[9px] font-mono uppercase tracking-wider text-text-light">
                      {badge.name}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column — Leaderboard */}
        <div className="lg:col-span-2 space-y-6">
          {/* Honor Leaderboard */}
          <div className="p-6 rounded-2xl border border-brand-primary/20 bg-surface-card/90">
            <h2 className="text-lg font-bold text-text-primary mb-4 flex items-center gap-2">
              <Trophy size={20} className="text-yellow-500" />
              Honor Leaderboard
            </h2>
            {leaderboard.length === 0 ? (
              <p className="text-text-light text-sm">No rankings yet.</p>
            ) : (
              <div className="space-y-1">
                {leaderboard.map((entry, i) => {
                  const isMe = profile && entry.name;
                  return (
                    <div
                      key={entry.user_id}
                      className={`flex items-center justify-between p-3 rounded-xl transition-colors ${
                        i === 0 ? "bg-yellow-50 border border-yellow-200" :
                        i === 1 ? "bg-surface-base border border-gray-200" :
                        i === 2 ? "bg-orange-50 border border-orange-200" :
                        "hover:bg-surface-card"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          i === 0 ? "bg-yellow-200 text-yellow-800" :
                          i === 1 ? "bg-surface-card/50 text-brand-primary" :
                          i === 2 ? "bg-orange-200 text-orange-800" :
                          "bg-surface-card/50 text-brand-muted"
                        }`}>
                          {entry.rank}
                        </span>
                        <div>
                          <div className="text-sm font-medium text-text-primary">{entry.name}</div>
                          <div className="text-[11px] text-text-light">{entry.rank_title}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-bold text-text-primary flex items-center gap-1">
                          <Star size={12} className="text-yellow-500" /> {entry.honor}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Pagination */}
            {lbTotal > 20 && (
              <div className="flex items-center justify-center gap-2 mt-4">
                <button
                  disabled={lbPage <= 1}
                  onClick={() => setLbPage((p) => Math.max(1, p - 1))}
                  className="px-3 py-1.5 rounded-lg border border-brand-primary/20 text-sm disabled:opacity-40"
                >
                  Prev
                </button>
                <span className="text-sm text-text-light">Page {lbPage} of {Math.ceil(lbTotal / 20)}</span>
                <button
                  disabled={lbPage >= Math.ceil(lbTotal / 20)}
                  onClick={() => setLbPage((p) => p + 1)}
                  className="px-3 py-1.5 rounded-lg border border-brand-primary/20 text-sm disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            )}
          </div>

          {/* Honor Actions Reference */}
          <div className="p-6 rounded-2xl border border-brand-primary/20 bg-surface-card/90">
            <h2 className="text-lg font-bold text-text-primary mb-4 flex items-center gap-2">
              <Zap size={20} className="text-amber-500" />
              Earn Honor
            </h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {[
                { action: "Solve a problem", honor: 5, icon: Target },
                { action: "Optimal solution bonus", honor: 3, icon: Star },
                { action: "Win a battle", honor: 15, icon: Trophy },
                { action: "Perfect score", honor: 10, icon: Award },
                { action: "7-day streak", honor: 20, icon: TrendingUp },
                { action: "30-day streak", honor: 50, icon: Crown },
                { action: "Daily login", honor: 1, icon: Zap },
                { action: "Create a scrim", honor: 10, icon: Shield },
              ].map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl border border-brand-primary/20 bg-surface-card/70">
                  <div className="flex items-center gap-2">
                    <item.icon size={14} className="text-brand-sky" />
                    <span className="text-sm text-text-secondary">{item.action}</span>
                  </div>
                  <span className="text-sm font-bold text-brand-coral">+{item.honor}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
