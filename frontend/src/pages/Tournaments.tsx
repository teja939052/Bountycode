import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function Tournaments() {
  const { showXP, play } = useJuice();
  const [presets, setPresets] = useState([]);
  const [activeTournaments, setActiveTournaments] = useState([]);
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [newTournamentName, setNewTournamentName] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [presetsData, activeData, historyData] = await Promise.all([
        api.tournaments?.getPresets?.() || { tournaments: [] },
        api.tournaments?.getActive?.() || { tournaments: [] },
        api.tournaments?.getHistory?.() || {},
      ]);
      setPresets(presetsData.tournaments || []);
      setActiveTournaments(activeData.tournaments || []);
      setHistory(historyData);
    } catch {
      setPresets([]);
      setActiveTournaments([]);
      setHistory(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTournament = async () => {
    setLoading(true);
    try {
      await api.tournaments?.create?.({ name: newTournamentName, preset_key: selectedPreset }) || {};
      setMessage("Tournament created!");
      setShowCreate(false);
      setNewTournamentName("");
      setSelectedPreset("");
      play("badgeUnlock");
      showXP(50, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch {
      setMessage("Failed to create tournament");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinTournament = async (tournamentId) => {
    setLoading(true);
    try {
      await api.tournaments?.join?.({ tournament_id: tournamentId }) || {};
      setMessage("Joined tournament!");
      play("levelUp");
      showXP(25, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch {
      setMessage("Failed to join tournament");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitResult = async (tournamentId, opponentId, result) => {
    try {
      const data = await api.tournaments?.submit?.({
        tournament_id: tournamentId,
        opponent_id: opponentId,
        result,
      }) || {};
      setMessage(`Result submitted! +${data.xp_earned || 10} XP`);
      play(result === "win" ? "levelUp" : "xpCollect");
      showXP(data.xp_earned || 10, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch {
      setMessage("Failed to submit result");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading tournaments...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">🏟️ Tournaments</h1>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="px-4 py-2 bg-indigo-600 text-text-primary rounded-lg hover:bg-indigo-700 text-sm font-medium"
        >
          Create Tournament
        </button>
      </div>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      {showCreate && (
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold">Create Tournament</h2>
          <input
            type="text"
            placeholder="Tournament name"
            value={newTournamentName}
            onChange={(e) => setNewTournamentName(e.target.value)}
            className="w-full px-3 py-2 border border-brand-primary/20 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          />
          <select
            value={selectedPreset}
            onChange={(e) => setSelectedPreset(e.target.value)}
            className="w-full px-3 py-2 border border-brand-primary/20 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          >
            <option value="">Select a preset...</option>
            {presets.map((p) => (
              <option key={p.name} value={p.name.toLowerCase().replace(/\s+/g, "_")}>
                {p.emoji} {p.name} ({p.format})
              </option>
            ))}
          </select>
          <div className="flex gap-3">
            <button
              onClick={handleCreateTournament}
              disabled={loading || !newTournamentName}
              className="px-4 py-2 bg-indigo-600 text-text-primary rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              Create
            </button>
            <button onClick={() => setShowCreate(false)} className="px-4 py-2 border border-brand-primary/20 rounded-lg text-sm">
              Cancel
            </button>
          </div>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold mb-4">⚡ Active Tournaments</h2>
        <div className="space-y-4">
          {activeTournaments.map((t) => (
            <div key={t.tournament_id} className="bg-surface-card border border-brand-primary/10 rounded-xl p-5">
              <div className="flex items-center gap-4 mb-3">
                <span className="text-3xl">{t.emoji}</span>
                <div className="flex-1">
                  <h3 className="font-semibold">{t.name}</h3>
                  <p className="text-xs text-gray-500">
                    {t.format} • {t.round} • {t.participants}/{t.max_participants} players
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-indigo-600">+{t.xp_reward} XP</div>
                  <div className="text-xs text-gray-500">{t.badge_reward}</div>
                </div>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={() => handleJoinTournament(t.tournament_id)}
                  disabled={loading}
                  className="px-3 py-1.5 bg-indigo-600 text-text-primary rounded-lg text-xs font-medium hover:bg-indigo-700 disabled:opacity-50"
                >
                  Join
                </button>
                <button
                  onClick={() => handleSubmitResult(t.tournament_id, "opponent_1", "win")}
                  disabled={loading}
                  className="px-3 py-1.5 bg-green-600 text-text-primary rounded-lg text-xs font-medium hover:bg-green-700 disabled:opacity-50"
                >
                  Submit Win
                </button>
                <button
                  onClick={() => handleSubmitResult(t.tournament_id, "opponent_1", "loss")}
                  disabled={loading}
                  className="px-3 py-1.5 bg-red-600 text-text-primary rounded-lg text-xs font-medium hover:bg-red-700 disabled:opacity-50"
                >
                  Submit Loss
                </button>
              </div>
            </div>
          ))}
          {activeTournaments.length === 0 && (
            <div className="text-center py-8 text-gray-400">No active tournaments</div>
          )}
        </div>
      </div>

      {history && (
        <div>
          <h2 className="text-lg font-semibold mb-4">📊 Your Tournament History</h2>
          <div className="bg-surface-card border border-brand-primary/10 rounded-xl p-5">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-indigo-600">{history.total_tournaments || 0}</div>
                <div className="text-xs text-gray-500">Total Tournaments</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{history.joined?.length || 0}</div>
                <div className="text-xs text-gray-500">Joined</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-amber-600">{history.hosted?.length || 0}</div>
                <div className="text-xs text-gray-500">Hosted</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}