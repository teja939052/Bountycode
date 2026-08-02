import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function AchievementChains() {
  const { showXP, play } = useJuice();
  const [chains, setChains] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [chainsData, statsData] = await Promise.all([
        api.achievements?.getChains?.() || { chains: [] },
        api.achievements?.getStats?.() || {},
      ]);
      setChains(chainsData.chains || []);
      setStats(statsData);
    } catch {
      setChains([]);
      setStats(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteStep = async (stepId, chainKey) => {
    try {
      const data = await api.achievements?.updateProgress?.({
        step_id: stepId,
        chain_key: chainKey,
        xp: 20,
      }) || {};

      setMessage(`+${data.total_xp || 20} XP! ${data.chain_complete ? "🏆 Chain Complete!" : ""}`);
      play(data.chain_complete ? "levelUp" : "xpCollect");
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
        <div className="text-gray-400 text-lg">Loading achievements...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">🏆 Achievement Chains</h1>
        {stats && (
          <div className="text-sm text-gray-500">
            {stats.completed_chains}/{stats.total_chains} chains complete
          </div>
        )}
      </div>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      {stats && (
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="text-sm font-medium text-gray-600">Overall Progress</div>
              <div className="mt-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-600 rounded-full transition-all"
                  style={{ width: `${stats.progress_percentage || 0}%` }}
                />
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-indigo-600">{stats.completed_steps}/{stats.total_steps}</div>
              <div className="text-xs text-gray-500">steps completed</div>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-6">
        {chains.map((chain) => (
          <div
            key={chain.key}
            className={`bg-white border rounded-xl overflow-hidden ${chain.is_complete ? "border-green-300" : "border-gray-200"}`}
          >
            <div className="p-5 border-b border-gray-100">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{chain.emoji}</span>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold">{chain.name}</h3>
                  <p className="text-sm text-gray-500">{chain.description}</p>
                </div>
                {chain.is_complete && (
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                    Complete ✓
                  </span>
                )}
              </div>
            </div>
            <div className="p-5 space-y-3">
              {chain.steps.map((step) => {
                const isCompleted = step.completed;
                return (
                  <div
                    key={step.id}
                    className={`flex items-center justify-between p-3 rounded-lg ${isCompleted ? "bg-green-50" : "bg-gray-50"}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-lg">{isCompleted ? "✅" : "⬜"}</span>
                      <div>
                        <div className="font-medium text-sm">{step.name}</div>
                        <div className="text-xs text-gray-500">+{step.xp} XP</div>
                      </div>
                    </div>
                    {!isCompleted && (
                      <button
                        onClick={() => handleCompleteStep(step.id, chain.key)}
                        className="px-3 py-1 bg-indigo-600 text-white rounded-lg text-xs font-medium hover:bg-indigo-700"
                      >
                        Complete
                      </button>
                    )}
                  </div>
                );
              })}
              {chain.bonus && (
                <div className="mt-3 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <div className="text-sm font-semibold text-amber-800">
                    🎁 Chain Bonus: {chain.bonus.badge}
                  </div>
                  <div className="text-xs text-amber-600">+{chain.bonus.xp_bonus} XP</div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}