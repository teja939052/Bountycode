import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

const TEAM_PRESETS = [
  { name: "IIT Bombay", emoji: "🏛️", color: "#ef4444" },
  { name: "IIT Delhi", emoji: "🎓", color: "#3b82f6" },
  { name: "IIT Madras", emoji: "⚙️", color: "#10b981" },
  { name: "IIT Kharagpur", emoji: "🔧", color: "#f59e0b" },
  { name: "IIT Kanpur", emoji: "🚀", color: "#8b5cf6" },
  { name: "BITS Pilani", emoji: "💡", color: "#14b8a6" },
  { name: "NIT Trichy", emoji: "🏅", color: "#f97316" },
  { name: "Google", emoji: "🔍", color: "#4285f4" },
  { name: "Microsoft", emoji: "🪟", color: "#00a4ef" },
  { name: "Amazon", emoji: "📦", color: "#ff9900" },
];

export default function TeamCompetitions() {
  const { showXP, play } = useJuice();
  const [myTeam, setMyTeam] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [collegeLeaderboard, setCollegeLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [newTeamName, setNewTeamName] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [myTeamData, lbData, collegeData] = await Promise.all([
        api.teams?.getMyTeam?.() || { team: null, role: null },
        api.teams?.getLeaderboard?.() || { teams: [] },
        api.teams?.getCollegeLeaderboard?.() || { colleges: [] },
      ]);
      setMyTeam(myTeamData.team || null);
      setLeaderboard(lbData.teams || []);
      setCollegeLeaderboard(collegeData.colleges || []);
    } catch {
      setMyTeam(null);
      setLeaderboard([]);
      setCollegeLeaderboard([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTeam = async () => {
    setLoading(true);
    try {
      await api.teams?.create?.({ name: newTeamName }) || {};
      setMessage("Team created!");
      setShowCreate(false);
      setNewTeamName("");
      play("badgeUnlock");
      showXP(50, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch {
      setMessage("Failed to create team");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinTeam = async (teamName) => {
    setLoading(true);
    try {
      await api.teams?.join?.({ team_id: teamName }) || {};
      setMessage(`Joined ${teamName}!`);
      play("levelUp");
      showXP(25, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch {
      setMessage("Failed to join team");
    } finally {
      setLoading(false);
    }
  };

  const handleLeaveTeam = async () => {
    setLoading(true);
    try {
      await api.teams?.leave?.() || {};
      setMessage("Left the team");
      setMyTeam(null);
      await loadData();
    } catch {
      setMessage("Failed to leave team");
    } finally {
      setLoading(false);
    }
  };

  const handleContributeXP = async (amount: number) => {
    setLoading(true);
    try {
      await api.teams?.contributeXP?.({ amount }) || {};
      setMessage(`Shared ${amount} XP with team!`);
      play("xpGain");
      showXP(amount, window.innerWidth / 2, window.innerHeight / 2);
    } catch {
      setMessage("Failed to share XP");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-brand-muted text-lg">Loading teams...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">⚔️ Team Competitions</h1>
        {!myTeam && (
          <button
            onClick={() => setShowCreate(!showCreate)}
            className="px-4 py-2 bg-indigo-600 text-text-primary rounded-lg hover:bg-indigo-700 text-sm font-medium"
          >
            Create Team
          </button>
        )}
      </div>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      {showCreate && (
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold">Create a Team</h2>
          <input
            type="text"
            placeholder="Team name"
            value={newTeamName}
            onChange={(e) => setNewTeamName(e.target.value)}
            className="w-full px-3 py-2 border border-brand-primary/20 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          />
          <div className="flex gap-3">
            <button
              onClick={handleCreateTeam}
              disabled={loading || !newTeamName}
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

      {myTeam && (
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl p-6">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">{myTeam.emoji || "🏆"}</span>
            <div>
              <h2 className="text-xl font-bold">{myTeam.name}</h2>
              <p className="text-sm text-brand-muted">{myTeam.members_count || 1} members</p>
            </div>
            <span className="ml-auto px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-semibold capitalize">
              {myTeam.user_role}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center p-3 bg-surface-base rounded-lg">
              <div className="text-2xl font-bold text-indigo-600">{myTeam.total_xp || 0}</div>
              <div className="text-xs text-brand-muted">Team XP</div>
            </div>
            <div className="text-center p-3 bg-surface-base rounded-lg">
              <div className="text-2xl font-bold text-green-600">{myTeam.wins || 0}</div>
              <div className="text-xs text-brand-muted">Wins</div>
            </div>
            <div className="text-center p-3 bg-surface-base rounded-lg">
              <div className="text-2xl font-bold text-red-600">{myTeam.losses || 0}</div>
              <div className="text-xs text-brand-muted">Losses</div>
            </div>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => handleContributeXP(10)}
              disabled={loading}
              className="px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100"
            >
              Contribute 10 XP
            </button>
            <button
              onClick={() => handleContributeXP(50)}
              disabled={loading}
              className="px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100"
            >
              Contribute 50 XP
            </button>
            <button
              onClick={handleLeaveTeam}
              disabled={loading}
              className="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100"
            >
              Leave Team
            </button>
          </div>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold mb-4">🏆 Team Leaderboard</h2>
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-surface-base">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Rank</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Team</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Members</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {leaderboard.map((team) => (
                <tr key={team.team_id} className="hover:bg-surface-base">
                  <td className="px-4 py-3 font-bold">#{team.rank}</td>
                  <td className="px-4 py-3">
                    <span className="text-lg mr-2">{team.emoji}</span>
                    <span className="font-medium">{team.name}</span>
                  </td>
                  <td className="px-4 py-3 text-brand-secondary">{team.members}</td>
                  <td className="px-4 py-3 font-semibold text-indigo-600">{team.total_xp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-4">🎓 College Leaderboard</h2>
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-surface-base">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Rank</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">College</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Members</th>
                <th className="px-4 py-3 text-left font-semibold text-brand-secondary">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {collegeLeaderboard.map((college) => (
                <tr key={college.college} className="hover:bg-surface-base">
                  <td className="px-4 py-3 font-bold">#{college.rank}</td>
                  <td className="px-4 py-3 font-medium">{college.college}</td>
                  <td className="px-4 py-3 text-brand-secondary">{college.members}</td>
                  <td className="px-4 py-3 font-semibold text-indigo-600">{college.total_xp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {!myTeam && (
        <div>
          <h2 className="text-lg font-semibold mb-4">Join a Team</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {TEAM_PRESETS.map((team) => (
              <div
                key={team.name}
                className="bg-surface-card border border-brand-primary/10 rounded-xl p-4 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-2xl">{team.emoji}</span>
                  <h3 className="font-semibold">{team.name}</h3>
                </div>
                <button
                  onClick={() => handleJoinTeam(team.name)}
                  disabled={loading}
                  className="w-full px-3 py-1.5 bg-indigo-600 text-text-primary rounded-lg text-xs font-medium hover:bg-indigo-700 disabled:opacity-50"
                >
                  Join Team
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}