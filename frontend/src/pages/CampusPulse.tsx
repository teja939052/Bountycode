import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { campusPulseApi } from "../services/api/campusPulse.ts";
import useAuthStore from "../store/authStore";
import { Sword, Shield, Trophy, Zap, Users, RefreshCw, Play, Clock, MapPin } from "lucide-react";

const CATEGORY_COLORS = {
  aptitude: "from-amber-500 to-orange-600",
  coding: "from-[#4F8F57] to-[#7BB661]",
  interview: "from-rose-500 to-pink-600",
  mixed: "from-[#4F8F57] to-[#7BB661]",
};

export default function CampusPulse() {
  const user = useAuthStore((s) => s.user);
  const [battles, setBattles] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionMsg, setActionMsg] = useState("");
  const [selectedBattle, setSelectedBattle] = useState(null);
  const [answerState, setAnswerState] = useState(null);

  const loadData = useCallback(async () => {
    try {
      const [b, r] = await Promise.all([
        campusPulseApi.activeBattles(),
        campusPulseApi.campusRankings(),
      ]);
      setBattles(b.battles || []);
      setRankings(r.rankings || []);
    } catch (e) {
      setError(e.message || "Could not load pulse data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreateBattle = async () => {
    setError("");
    try {
      const campuses = ["IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kharagpur", "NIT Trichy", "BITS Pilani"];
      const campusA = campuses[Math.floor(Math.random() * campuses.length)];
      let campusB = campuses[Math.floor(Math.random() * campuses.length)];
      while (campusB === campusA) {
        campusB = campuses[Math.floor(Math.random() * campuses.length)];
      }
      const res = await campusPulseApi.createBattle(campusA, campusB, "mixed");
      setActionMsg(res.message);
      loadData();
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Battle creation failed");
    }
  };

  const handleJoinBattle = async (battleId) => {
    setError("");
    try {
      const res = await campusPulseApi.joinBattle(battleId);
      setActionMsg(res.message);
      loadData();
      setTimeout(() => setActionMsg(""), 3000);
    } catch (e) {
      setError(e.message || "Join failed");
    }
  };

  const handleSubmitAnswer = async (battleId, correct) => {
    setError("");
    try {
      const res = await campusPulseApi.submitAnswer(battleId, { correct });
      setAnswerState(res);
      setActionMsg(res.message);
      setTimeout(() => {
        setAnswerState(null);
        setActionMsg("");
      }, 3000);
      loadData();
    } catch (e) {
      setError(e.message || "Answer submission failed");
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading Campus Pulse...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">
            <span className="bg-gradient-to-r from-[#4F8F57] via-[#7BB661] to-[#B8D9A8] bg-clip-text text-transparent">
              Campus Pulse
            </span>
          </h1>
          <p className="text-text-muted mt-2">
            Your campus vs the world. Battle in real-time. Earn glory.
          </p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {actionMsg && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-4 bg-green-500/10 border border-green-500/30 rounded-lg py-2 text-green-600 text-sm"
          >
            {actionMsg}
          </motion.div>
        )}

        {/* Create Battle */}
        <div className="text-center mb-8">
          <button
            onClick={handleCreateBattle}
            className="rounded-xl bg-gradient-to-r from-rose-500 to-pink-600 px-6 py-3 font-bold text-text-primary hover:from-rose-400 hover:to-pink-500 flex items-center gap-2 mx-auto"
          >
            <Sword className="h-5 w-5" />
            Start New Battle
          </button>
        </div>

        {/* Active Battles */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
            <Zap className="h-5 w-5 text-amber-400" />
            Active Battles
          </h2>
          {battles.length === 0 ? (
            <p className="text-text-muted text-center py-8">No active battles. Start one!</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {battles.map((battle) => (
                <motion.div
                  key={battle._id}
                  className="rounded-2xl border border-nature-leaf/20 bg-white p-5"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold px-2 py-1 rounded-full bg-surface-card text-nature-blossom">
                      {battle.category || "mixed"}
                    </span>
                    <span className="text-xs text-text-muted flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {battle.ends_at
                        ? new Date(battle.ends_at).toLocaleTimeString()
                        : "Unknown"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-center">
                      <div className="text-lg font-bold text-amber-400">
                        {battle.scores?.[battle.campus_a] || 0}
                      </div>
                      <div className="text-xs text-text-muted">{battle.campus_a}</div>
                    </div>
                    <div className="text-2xl">⚔️</div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-rose-400">
                        {battle.scores?.[battle.campus_b] || 0}
                      </div>
                      <div className="text-xs text-text-muted">{battle.campus_b}</div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleJoinBattle(battle._id)}
                      className="flex-1 rounded-lg bg-nature-leaf px-3 py-2 text-xs font-bold text-text-primary hover:bg-nature-moss"
                    >
                      Join Battle
                    </button>
                    <button
                      onClick={() => setSelectedBattle(battle)}
                      className="flex-1 rounded-lg bg-[#6B7280] px-3 py-2 text-xs font-bold text-text-primary hover:bg-[#4B5563]"
                    >
                      View Scores
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Campus Rankings */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-white border border-nature-leaf/20 rounded-2xl p-6"
        >
          <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
            <Trophy className="h-5 w-5 text-amber-400" />
            Campus Rankings
          </h2>
          <div className="space-y-2">
            {rankings.map((rank, idx) => (
              <div
                key={rank.campus}
                className="flex items-center justify-between py-2 px-3 rounded-lg bg-surface-card"
              >
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold">
                    {idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : `#${idx + 1}`}
                  </span>
                  <span className="text-sm font-bold text-text-primary flex items-center gap-1">
                    <MapPin className="h-3 w-3 text-nature-blossom" />
                    {rank.campus}
                  </span>
                </div>
                <span className="text-sm font-bold text-amber-400">{rank.total_points} pts</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Answer Battle Modal */}
        <AnimatePresence>
          {selectedBattle && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-surface-2 flex items-center justify-center z-50 p-4"
              onClick={() => setSelectedBattle(null)}
            >
              <motion.div
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.9 }}
                className="bg-white border border-nature-leaf/20 rounded-2xl p-6 max-w-md w-full"
                onClick={(e) => e.stopPropagation()}
              >
                <h3 className="text-xl font-bold text-text-primary mb-4">
                  {selectedBattle.campus_a} vs {selectedBattle.campus_b}
                </h3>
                <div className="flex justify-between mb-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-amber-400">
                      {selectedBattle.scores?.[selectedBattle.campus_a] || 0}
                    </div>
                    <div className="text-xs text-text-muted">{selectedBattle.campus_a}</div>
                  </div>
                  <div className="text-2xl">⚔️</div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-rose-400">
                      {selectedBattle.scores?.[selectedBattle.campus_b] || 0}
                    </div>
                    <div className="text-xs text-text-muted">{selectedBattle.campus_b}</div>
                  </div>
                </div>
                <p className="text-sm text-text-muted mb-4">
                  Submit your answer! Correct = +{selectedBattle.points_per_q || 10} points
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleSubmitAnswer(selectedBattle._id, true)}
                    className="flex-1 rounded-lg bg-green-600 px-4 py-3 font-bold text-text-primary hover:bg-green-500"
                  >
                    ✅ Correct
                  </button>
                  <button
                    onClick={() => handleSubmitAnswer(selectedBattle._id, false)}
                    className="flex-1 rounded-lg bg-rose-600 px-4 py-3 font-bold text-text-primary hover:bg-rose-500"
                  >
                    ❌ Wrong
                  </button>
                </div>
                {answerState && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-3 rounded-lg bg-surface-card text-center"
                  >
                    <p className="text-sm font-bold">{answerState.message}</p>
                    <p className="text-xs text-text-muted mt-1">
                      Your campus: {answerState.campus_score} | Opponent: {answerState.opponent_score}
                    </p>
                  </motion.div>
                )}
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}