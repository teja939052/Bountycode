import { useState, useEffect, useCallback } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

const PRESET_GUILDS = [
  { name: "Code Ninjas", emoji: "🥷", color: "#ef4444", bonus: "10% XP boost on coding challenges", description: "Swift and deadly coders who strike fast." },
  { name: "Algo Knights", emoji: "⚔️", color: "#3b82f6", bonus: "Extra hint reveals on boss battles", description: "Champions of algorithmic warfare." },
  { name: "Debug Dragons", emoji: "🐉", color: "#f59e0b", bonus: "Double XP on daily challenges", description: "Masters of squashing bugs with fire." },
  { name: "Stack Sorcerers", emoji: "🔮", color: "#8b5cf6", bonus: "Free power-up spins every week", description: "Magical minds manipulating data structures." },
  { name: "Pixel Rangers", emoji: "🏹", color: "#10b981", bonus: "1.5x streak multiplier", description: "Precision marksmen hitting daily targets." },
  { name: "Binary Bandits", emoji: "💰", color: "#f97316", bonus: "Steal 10% XP from rival guilds", description: "Clever thieves of experience points." },
];

export default function Guilds() {
  const { showXP, play } = useJuice();
  const [guilds, setGuilds] = useState(PRESET_GUILDS);
  const [myGuild, setMyGuild] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [showCreate, setShowCreate] = useState(false);
  const [newGuildName, setNewGuildName] = useState("");
  const [newGuildDesc, setNewGuildDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("explore");
  const [leaderboard, setLeaderboard] = useState([]);
  const [members, setMembers] = useState([]);

  const loadMyGuild = useCallback(async () => {
    try {
      const data = await api.guilds?.getMyGuild?.() || { guild: null, role: null };
      setMyGuild(data.guild);
      setUserRole(data.role);
    } catch {
      setMyGuild(null);
      setUserRole(null);
    }
  }, []);

  const loadLeaderboard = useCallback(async () => {
    try {
      const data = await api.guilds?.getLeaderboard?.() || { guilds: [] };
      setLeaderboard(data.guilds || []);
    } catch {
      setLeaderboard([]);
    }
  }, []);

  useEffect(() => {
    loadMyGuild();
    loadLeaderboard();
  }, [loadMyGuild, loadLeaderboard]);

  const handleCreateGuild = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const data = await api.guilds?.create?.({ name: newGuildName, description: newGuildDesc }) || {};
      setMessage("Guild created successfully!");
      setShowCreate(false);
      setNewGuildName("");
      setNewGuildDesc("");
      await loadMyGuild();
      await loadLeaderboard();
      play("badgeUnlock");
      showXP(100, window.innerWidth / 2, window.innerHeight / 2);
    } catch (err) {
      setError(err.message || "Failed to create guild");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGuild = async (guildName) => {
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const preset = PRESET_GUILDS.find((g) => g.name === guildName);
      await api.guilds?.join?.({ guild_id: preset?.name || guildName }) || {};
      setMessage(`Joined ${guildName}!`);
      play("levelUp");
      showXP(50, window.innerWidth / 2, window.innerHeight / 2);
      await loadMyGuild();
      await loadLeaderboard();
    } catch (err) {
      setError(err.message || "Failed to join guild");
    } finally {
      setLoading(false);
    }
  };

  const handleLeaveGuild = async () => {
    setLoading(true);
    try {
      await api.guilds?.leave?.() || {};
      setMessage("Left the guild");
      setMyGuild(null);
      setUserRole(null);
      await loadLeaderboard();
    } catch (err) {
      setError(err.message || "Failed to leave guild");
    } finally {
      setLoading(false);
    }
  };

  const handleContributeXP = async (xp) => {
    if (!myGuild) return;
    try {
      await api.guilds?.contributeXP?.({ xp }) || {};
      setMessage(`Contributed ${xp} XP to your guild!`);
      play("xpCollect");
      showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
      await loadMyGuild();
      await loadLeaderboard();
    } catch {
      setError("Failed to contribute XP");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">⚔️ Guilds</h1>
        {!myGuild && (
          <button
            onClick={() => setShowCreate(!showCreate)}
            className="px-4 py-2 bg-indigo-600 text-text-primary rounded-lg hover:bg-indigo-700 text-sm font-medium"
          >
            Create Guild
          </button>
        )}
      </div>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {showCreate && (
        <form onSubmit={handleCreateGuild} className="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-semibold">Create a Guild</h2>
          <input
            type="text"
            placeholder="Guild name (max 30 chars)"
            value={newGuildName}
            onChange={(e) => setNewGuildName(e.target.value)}
            maxLength={30}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
          />
          <textarea
            placeholder="Describe your guild..."
            value={newGuildDesc}
            onChange={(e) => setNewGuildDesc(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm h-20"
          />
          <div className="flex gap-3">
            <button type="submit" disabled={loading} className="px-4 py-2 bg-indigo-600 text-text-primary rounded-lg hover:bg-indigo-700 text-sm font-medium disabled:opacity-50">
              {loading ? "Creating..." : "Create"}
            </button>
            <button type="button" onClick={() => setShowCreate(false)} className="px-4 py-2 border border-gray-300 rounded-lg text-sm">
              Cancel
            </button>
          </div>
        </form>
      )}

      {myGuild && (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">{myGuild.emoji || "🏰"}</span>
            <div>
              <h2 className="text-xl font-bold">{myGuild.name}</h2>
              <p className="text-sm text-gray-500">{myGuild.bonus}</p>
            </div>
            <span className="ml-auto px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-semibold capitalize">
              {userRole}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-indigo-600">{myGuild.total_xp || 0}</div>
              <div className="text-xs text-gray-500">Guild XP</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{myGuild.members_count || 0}</div>
              <div className="text-xs text-gray-500">Members</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-amber-600">{myGuild.rank || "—"}</div>
              <div className="text-xs text-gray-500">Rank</div>
            </div>
          </div>
          <div className="flex gap-3 flex-wrap">
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
              onClick={() => handleContributeXP(100)}
              disabled={loading}
              className="px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-medium hover:bg-indigo-100"
            >
              Contribute 100 XP
            </button>
            <button
              onClick={handleLeaveGuild}
              disabled={loading}
              className="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100"
            >
              Leave Guild
            </button>
          </div>
        </div>
      )}

      <div className="flex gap-2 border-b border-gray-200">
        <button
          onClick={() => setActiveTab("explore")}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === "explore" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500 hover:text-gray-700"}`}
        >
          Explore Guilds
        </button>
        <button
          onClick={() => setActiveTab("leaderboard")}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${activeTab === "leaderboard" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500 hover:text-gray-700"}`}
        >
          Leaderboard
        </button>
      </div>

      {activeTab === "explore" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {guilds.map((guild) => (
            <div
              key={guild.name}
              className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{guild.emoji}</span>
                <div>
                  <h3 className="font-semibold text-gray-900">{guild.name}</h3>
                  <p className="text-xs text-gray-500">{guild.description || "A guild of dedicated coders"}</p>
                </div>
              </div>
              <div className="text-xs text-indigo-600 font-medium mb-3">{guild.bonus}</div>
              {myGuild?.name === guild.name ? (
                <span className="text-xs text-green-600 font-medium">✓ Member</span>
              ) : (
                <button
                  onClick={() => handleJoinGuild(guild.name)}
                  disabled={loading}
                  className="w-full px-3 py-1.5 bg-indigo-600 text-text-primary rounded-lg text-xs font-medium hover:bg-indigo-700 disabled:opacity-50"
                >
                  {loading ? "Joining..." : "Join Guild"}
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {activeTab === "leaderboard" && (
        <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Rank</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Guild</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Members</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-600">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {leaderboard.map((g) => (
                <tr key={g.id || g.name} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-bold text-gray-900">#{g.rank || g.id}</td>
                  <td className="px-4 py-3">
                    <span className="text-lg mr-2">{g.emoji || "🏰"}</span>
                    <span className="font-medium">{g.name}</span>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{g.members_count || 0}</td>
                  <td className="px-4 py-3 font-semibold text-indigo-600">{g.total_xp || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {leaderboard.length === 0 && (
            <div className="text-center py-8 text-gray-400">No guilds yet. Be the first to create one!</div>
          )}
        </div>
      )}
    </div>
  );
}