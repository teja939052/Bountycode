import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function SeasonalEvents() {
  const { showXP, play } = useJuice();
  const [currentSeason, setCurrentSeason] = useState(null);
  const [allSeasons, setAllSeasons] = useState([]);
  const [activeTab, setActiveTab] = useState("current");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [current, all] = await Promise.all([
        api.seasons?.getCurrent?.() || { season: null },
        api.seasons?.getAll?.() || { seasons: [] },
      ]);
      setCurrentSeason(current.season || null);
      setAllSeasons(all.seasons || []);
    } catch {
      setCurrentSeason(null);
      setAllSeasons([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteQuest = async (questId) => {
    if (!currentSeason) return;
    try {
      const data = await api.seasons?.updateProgress?.({ quest_id: questId, xp: 20 }) || {};
      setMessage(`+${data.total_xp || 20} XP earned!`);
      play("xpCollect");
      showXP(data.total_xp || 20, window.innerWidth / 2, window.innerHeight / 2);
      setTimeout(() => setMessage(""), 3000);
      await loadData();
    } catch {
      setMessage("Failed to update progress");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading seasonal events...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">🎯 Seasonal Events</h1>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      <div className="flex gap-2 border-b border-brand-primary/10">
        <button
          onClick={() => setActiveTab("current")}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === "current" ? "border-indigo-500 text-indigo-600" : "border-transparent text-brand-muted"}`}
        >
          Current Event
        </button>
        <button
          onClick={() => setActiveTab("all")}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === "all" ? "border-indigo-500 text-indigo-600" : "border-transparent text-brand-muted"}`}
        >
          All Seasons
        </button>
        <button
          onClick={() => setActiveTab("leaderboard")}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === "leaderboard" ? "border-indigo-500 text-indigo-600" : "border-transparent text-brand-muted"}`}
        >
          Leaderboard
        </button>
      </div>

      {activeTab === "current" && currentSeason && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-text-primary">
            <div className="text-4xl mb-2">{currentSeason.season?.emoji}</div>
            <h2 className="text-2xl font-bold mb-2">{currentSeason.season?.name}</h2>
            <p className="text-indigo-100 mb-4">{currentSeason.season?.description}</p>
            <div className="flex gap-4 text-sm">
              <span>⏰ {currentSeason.days_remaining} days remaining</span>
              <span>🎁 {currentSeason.season?.bonus_rewards?.badge || "Exclusive badge"}</span>
              <span>⚡ {currentSeason.season?.bonus_rewards?.xp_multiplier || 1}x XP</span>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Daily Quests</h3>
            <div className="space-y-3">
              {currentSeason.daily_quests?.map((quest) => {
                const progress = currentSeason.progress?.[quest.id];
                const completed = progress?.completed;
                return (
                  <div
                    key={quest.id}
                    className={`bg-surface-card border rounded-xl p-4 flex items-center justify-between ${completed ? "border-green-200 bg-green-50" : "border-brand-primary/10"}`}
                  >
                    <div>
                      <div className="font-medium">{quest.name}</div>
                      <div className="text-sm text-brand-muted">{quest.desc}</div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold text-indigo-600">+{quest.xp} XP</span>
                      {completed ? (
                        <span className="text-green-600 text-sm font-medium">✓ Done</span>
                      ) : (
                        <button
                          onClick={() => handleCompleteQuest(quest.id)}
                          className="px-3 py-1 bg-indigo-600 text-text-primary rounded-lg text-xs font-medium hover:bg-indigo-700"
                        >
                          Complete
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <h3 className="font-semibold text-amber-800 mb-2">🎁 Bonus Rewards</h3>
            <div className="text-sm text-amber-700">
              <p>Badge: <strong>{currentSeason.season?.bonus_rewards?.badge}</strong></p>
              <p>Title: <strong>{currentSeason.season?.bonus_rewards?.title}</strong></p>
              <p>XP Multiplier: <strong>{currentSeason.season?.bonus_rewards?.xp_multiplier}x</strong></p>
            </div>
          </div>
        </div>
      )}

      {activeTab === "current" && !currentSeason && (
        <div className="text-center py-12 text-gray-400">
          <div className="text-4xl mb-4">📅</div>
          <p>No active seasonal event right now.</p>
          <p className="text-sm mt-2">Check back during the next season!</p>
        </div>
      )}

      {activeTab === "all" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {allSeasons.map((season) => (
            <div
              key={season.key}
              className={`bg-surface-card border rounded-xl p-5 ${season.is_active ? "border-indigo-300 bg-indigo-50" : "border-brand-primary/10 opacity-60"}`}
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{season.emoji}</span>
                <div>
                  <h3 className="font-semibold">{season.name}</h3>
                  {season.isActive && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Active</span>
                  )}
                </div>
              </div>
              <p className="text-sm text-brand-muted mb-3">{season.description}</p>
              <div className="text-xs text-gray-400">
                {new Date(season.start).toLocaleDateString()} — {new Date(season.end).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === "leaderboard" && (
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-surface-base">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Rank</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">User</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Quests</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {currentSeason?.leaderboard?.map((entry) => (
                <tr key={entry.user_id} className="hover:bg-surface-card">
                  <td className="px-4 py-3 font-bold">#{entry.rank}</td>
                  <td className="px-4 py-3 font-medium">{entry.name}</td>
                  <td className="px-4 py-3 text-brand-secondary">{entry.quests_completed}</td>
                  <td className="px-4 py-3 font-semibold text-indigo-600">{entry.total_xp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}