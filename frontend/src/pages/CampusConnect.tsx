import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { campusConnectApi } from "../services/api/campusConnect.ts";
import useAuthStore from "../store/authStore";
import { Share2, Copy, Users, Trophy, Swords, Search } from "lucide-react";

export default function CampusConnect() {
  const user = useAuthStore((s) => s.user);
  const [colleges, setColleges] = useState([]);
  const [selectedCollege, setSelectedCollege] = useState("");
  const [invite, setInvite] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [duelState, setDuelState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const loadColleges = useCallback(async () => {
    try {
      const data = await campusConnectApi.colleges();
      setColleges(data);
    } catch (e) {
      setError(e.message || "Could not load colleges");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadColleges();
    // Try preselect user's college if they have one
    // Try preselect user's college if saved globally
    if (typeof window !== 'undefined' && window.USER_COLLEGE) {
      setSelectedCollege(window.USER_COLLEGE);
    }
  }, [loadColleges]);

  const generateInvite = async () => {
    if (!selectedCollege) {
      setError("Please select a college first");
      return;
    }
    try {
      const data = await campusConnectApi.generateInvite(selectedCollege);
      setInvite(data);
    } catch (e) {
      setError(e.message || "Could not generate invite");
    }
  };

  const startDuel = async () => {
    if (!selectedCollege) {
      setError("Please select a college first");
      return;
    }
    try {
      const data = await campusConnectApi.startDuel(selectedCollege);
      setDuelState(data);
    } catch (e) {
      setError(e.message || "Could not start duel");
    }
  };

  const copyInvite = () => {
    if (invite) {
      navigator.clipboard.writeText(invite.invite_url);
      alert("Invite link copied! Share it with classmates.");
    }
  };

  const loadLeaderboard = async (college) => {
    try {
      const data = await campusConnectApi.getCollegeLeaderboard(college || selectedCollege);
      setLeaderboard(data.leaderboard || []);
    } catch (e) {
      // best-effort
    }
  };

  useEffect(() => {
    if (selectedCollege) {
      loadLeaderboard(selectedCollege);
    }
  }, [selectedCollege]);

  const filteredColleges = searchQuery
    ? colleges.filter((c) => c.toLowerCase().includes(searchQuery.toLowerCase()))
    : colleges;

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <div className="animate-pulse">Loading colleges...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">🏫 Campus Connect</h1>
          <p className="text-slate-400 mt-2">
            Find classmates, share invites, and battle it out in 1v1 duels.
          </p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4">
            {error}
          </p>
        )}

        {/* College Selection */}
        <div className="mb-8">
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-500" />
            <input
              type="text"
              placeholder="Search your college..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-900 pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 max-h-60 overflow-y-auto">
            {filteredColleges.map((college) => (
              <button
                key={college}
                onClick={() => {
                  setSelectedCollege(college);
                  setSearchQuery("");
                }}
                className={"text-left rounded-lg border px-3 py-2 text-sm transition " +
                  (selectedCollege === college
                    ? "border-indigo-500 bg-indigo-600/20 text-white"
                    : "border-slate-700 bg-slate-800/50 text-slate-300 hover:border-slate-500")}
              >
                {college}
              </button>
            ))}
          </div>
          {colleges.length === 0 && (
            <p className="text-center text-slate-500 text-sm py-4">
              No colleges found. Type to search.
            </p>
          )}
        </div>

        {!selectedCollege && (
          <p className="text-slate-500 text-sm text-center mb-6">
            Select your college above to unlock invites and duels.
          </p>
        )}

        {/* Actions */}
        {selectedCollege && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid sm:grid-cols-2 gap-4 mb-8"
          >
            <button
              onClick={generateInvite}
              className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white shadow hover:bg-indigo-500"
            >
              <Share2 className="h-5 w-5" />
              Generate Invite Link
            </button>
            <button
              onClick={startDuel}
              className="flex items-center justify-center gap-2 rounded-xl bg-amber-500 px-6 py-3 font-semibold text-slate-900 shadow hover:bg-amber-400"
            >
              <Swords className="h-5 w-5" />
              Start 1v1 Duel
            </button>
          </motion.div>
        )}

        {/* Invite Link */}
        {invite && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 mb-8"
          >
            <h3 className="text-lg font-bold text-slate-200 mb-3">Your Invite Link</h3>
            <p className="text-sm text-slate-400 mb-3">
              Share this link with classmates at <span className="text-indigo-300">{invite.college}</span>
            </p>
            <div className="flex items-center gap-2">
              <code className="flex-1 break-all rounded-lg bg-slate-800 px-3 py-2 text-sm text-amber-300">
                {invite.invite_url}
              </code>
              <button
                onClick={copyInvite}
                className="rounded-lg bg-slate-700 px-3 py-2 text-sm text-slate-200 hover:bg-slate-600"
                title="Copy link"
              >
                <Copy className="h-4 w-4" />
              </button>
            </div>
          </motion.div>
        )}

        {/* Duel State */}
        {duelState && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 mb-8"
          >
            <h3 className="text-lg font-bold text-slate-200 mb-3">Duel Created</h3>
            <p className="text-sm text-slate-400 mb-2">
              Duel ID: <span className="font-mono text-indigo-300">{duelState.duel_id}</span>
            </p>
            <p className="text-sm text-slate-400">
              Status: <span className="text-amber-300">{duelState.status}</span>
            </p>
            <p className="text-sm text-slate-400 mt-2">{duelState.message}</p>
          </motion.div>
        )}

        {/* Leaderboard */}
        {selectedCollege && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Trophy className="h-5 w-5 text-amber-400" />
              <h3 className="text-lg font-bold text-slate-200">
                {selectedCollege} Leaderboard
              </h3>
            </div>
            {leaderboard.length === 0 ? (
              <p className="text-sm text-slate-500">No duel winners yet. Be the first!</p>
            ) : (
              <ul className="space-y-2">
                {leaderboard.map((entry, idx) => (
                  <div
                    key={entry.user_id}
                    className="flex items-center justify-between rounded-lg bg-slate-800/50 px-3 py-2"
                  >
                    <span className="flex items-center gap-3">
                      <span className="text-sm font-bold text-slate-500">#{idx + 1}</span>
                      <Users className="h-4 w-4 text-slate-500" />
                      <span className="text-sm text-slate-300">
                        {entry.user_id?.slice(0, 8) || "Anonymous"}
                      </span>
                    </span>
                    <span className="text-sm font-bold text-amber-400">{entry.wins} wins</span>
                  </div>
                ))}
              </ul>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
