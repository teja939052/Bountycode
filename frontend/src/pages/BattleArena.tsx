import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";
import useBattleLive, { BattleLiveMessage } from "../hooks/useBattleLive";
import useAuthStore from "../store/authStore";
import {
  Sword, Swords, Timer, Trophy, Users, Code2,
  Target, Zap, SkipForward, ChevronRight, Clock,
  CheckCircle, XCircle, Loader2, ScrollText,
  Medal, Star, BarChart3, History,
  Rocket, BrainCircuit,
} from "lucide-react";

const MODES = [
  { id: "fastest", label: "Fastest", icon: Zap, desc: "Solve fastest to win" },
  { id: "shortest", label: "Shortest", icon: Target, desc: "Shortest code wins" },
  { id: "reverse", label: "Reverse", icon: BrainCircuit, desc: "Guess problem from tests" },
];
const DIFFICULTIES = ["easy", "medium", "hard"];
const LANGUAGES = ["python", "javascript", "typescript", "java", "cpp", "go", "rust"];

const TABS = ["arena", "history", "leaderboard"];

const INITIAL_OPP_LIVE = { lines: 0, submitted: false, score: null, online: false, left: false };

export default function BattleArena() {
  const { battleId: routeBattleId } = useParams();
  const navigate = useNavigate();
  const { user: me } = useAuthStore();
  const myUserId = me?.id || null;
  const [tab, setTab] = useState("arena");
  const [mode, setMode] = useState("fastest");
  const [difficulty, setDifficulty] = useState("easy");
  const [language, setLanguage] = useState("python");
  const [inQueue, setInQueue] = useState(false);
  const [queuePos, setQueuePos] = useState(0);
  const [battle, setBattle] = useState(null);
  const [battleId, setBattleId] = useState(routeBattleId || null);
  const [code, setCode] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [stats, setStats] = useState(null);
  const [oppLive, setOppLive] = useState(INITIAL_OPP_LIVE);
  const pollRef = useRef(null);
  const battlePollRef = useRef(null);
  const progressTimerRef = useRef(null);

  // Start matchmaking
  const findMatch = async () => {
    try {
      const data = await api.joinBattleQueue({ mode, difficulty, language });
      if (data.matched) {
        setOppLive(INITIAL_OPP_LIVE);
        setBattleId(data.battle_id);
        setBattle(data.battle);
        setInQueue(false);
      } else {
        setInQueue(true);
      }
    } catch (err) {
      console.error("Queue error:", err);
    }
  };

  // Poll queue status
  useEffect(() => {
    if (!inQueue) {
      if (pollRef.current) clearInterval(pollRef.current);
      return;
    }
    pollRef.current = setInterval(async () => {
      try {
        const data = await api.getBattleQueueStatus();
        if (data.matched) {
          setOppLive(INITIAL_OPP_LIVE);
          setBattleId(data.battle_id);
          setInQueue(false);
          return;
        }
        if (!data.in_queue) {
          setInQueue(false);
          return;
        }
        setQueuePos(data.position);
      } catch (err) {
        console.error("Queue poll error:", err);
      }
    }, 3000);
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [inQueue]);

  // Poll battle state
  useEffect(() => {
    if (!battleId) {
      if (battlePollRef.current) clearInterval(battlePollRef.current);
      return;
    }
    battlePollRef.current = setInterval(async () => {
      try {
        const data = await api.getBattleState(battleId);
        setBattle(data);
        if (data.status === "completed") {
          if (battlePollRef.current) clearInterval(battlePollRef.current);
        }
      } catch (err) {
        console.error("Battle poll error:", err);
      }
    }, 2000);
    fetchHistory();
    return () => { if (battlePollRef.current) clearInterval(battlePollRef.current); };
  }, [battleId]);

  // Fetch history & leaderboard
  const fetchHistory = useCallback(async () => {
    try {
      const data = await api.getBattleHistory();
      setHistory(data.battles || []);
      setStats(data.stats || null);
    } catch (err) { /* ignore */ }
  }, []);

  const fetchLeaderboard = useCallback(async () => {
    try {
      const data = await api.getBattleLeaderboard();
      setLeaderboard(data.leaderboard || []);
    } catch (err) { /* ignore */ }
  }, []);

  useEffect(() => { fetchHistory(); fetchLeaderboard(); }, [fetchHistory, fetchLeaderboard]);

  // Submit code
  const handleSubmit = async () => {
    if (!battleId || !code.trim()) return;
    setSubmitting(true);
    try {
      const data = await api.submitBattleSolution(battleId, code);
      setResult(data);
    } catch (err) {
      console.error("Submit error:", err);
    } finally {
      setSubmitting(false);
    }
  };

  // Surrender
  const handleSurrender = async () => {
    if (!battleId) return;
    try {
      await api.surrenderBattle(battleId);
      setBattle((prev) => ({ ...prev, status: "completed" }));
    } catch (err) {
      console.error("Surrender error:", err);
    }
  };

  // Cancel queue
  const cancelQueue = () => {
    setInQueue(false);
    if (pollRef.current) clearInterval(pollRef.current);
  };

  const activeBattle = battle && battle.status === "in_progress";

  // Live opponent feed (WebSocket). Sanitized: lines + submit status, no code.
  const handleLiveMessage = useCallback((msg: BattleLiveMessage) => {
    const d = msg.data || {};
    if (msg.type === "sync") {
      setOppLive((o) => ({
        ...o,
        online: true,
        left: false,
        submitted: !!d.opponent_submitted,
        score: (d.opponent_score as number | null) ?? o.score,
      }));
      setBattle((prev) =>
        prev
          ? {
              ...prev,
              status: (d.status as string) || prev.status,
              opponent_submitted: d.opponent_submitted ?? prev.opponent_submitted,
              opponent_score: d.opponent_score ?? prev.opponent_score,
              winner_id: d.winner_id || prev.winner_id,
            }
          : prev
      );
      return;
    }
    if (msg.type === "progress") {
      if (myUserId && d.user_id === myUserId) return;
      setOppLive((o) => ({
        ...o,
        online: true,
        left: false,
        lines: Number(d.lines) || o.lines,
        submitted: !!d.submitted || o.submitted,
      }));
      return;
    }
    if (msg.type === "battle_update") {
      const fromOpponent = myUserId ? d.user_id && d.user_id !== myUserId : false;
      if (fromOpponent) {
        setBattle((prev) =>
          prev
            ? {
                ...prev,
                opponent_submitted: true,
                opponent_score: (d.score as number) ?? prev.opponent_score,
              }
            : prev
        );
        setOppLive((o) => ({
          ...o,
          submitted: true,
          score: (d.score as number | null) ?? o.score,
        }));
      }
      if (d.status === "completed") {
        setBattle((prev) =>
          prev ? { ...prev, status: "completed", winner_id: d.winner_id || prev.winner_id } : prev
        );
      }
      return;
    }
    if (msg.type === "opponent_left") {
      if (myUserId && d.user_id === myUserId) return;
      setOppLive((o) => ({ ...o, online: false, left: true }));
    }
  }, [myUserId]);

  const { status: liveStatus, send: sendLive } = useBattleLive({
    battleId: activeBattle ? battleId : null,
    onMessage: handleLiveMessage,
  });

  // Broadcast throttled lines-of-code progress while the battle is live.
  useEffect(() => {
    if (!activeBattle || !battleId) return;
    if (progressTimerRef.current) clearTimeout(progressTimerRef.current);
    progressTimerRef.current = setTimeout(() => {
      sendLive({ type: "progress", lines: code.split("\n").length });
    }, 800);
    return () => {
      if (progressTimerRef.current) clearTimeout(progressTimerRef.current);
    };
  }, [code, activeBattle, battleId, sendLive]);

  return (
    <div className="page-surface mx-auto max-w-7xl px-4 py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <Swords className="text-brand-coral" size={32} />
            Battle Arena
          </h1>
          <p className="text-text-light mt-1">Compete in real-time coding battles</p>
        </div>
        {stats && (
          <div className="flex items-center gap-4 text-sm">
            <div className="rounded-xl border border-black/5 bg-white px-4 py-2 shadow-sm">
              <span className="text-text-light">W/L </span>
              <span className="font-bold text-green-600">{stats.wins}</span>
              <span className="text-text-light">/</span>
              <span className="font-bold text-red-500">{stats.losses}</span>
              <span className="text-text-light ml-2">({stats.win_rate}%)</span>
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="mb-6 flex w-fit gap-1 rounded-2xl border border-black/5 bg-white border-border/70 p-1 shadow-sm">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center gap-2 ${
              tab === t ? "bg-white shadow-sm text-text-primary" : "text-text-light hover:text-text-secondary"
            }`}
          >
            {t === "arena" && <Sword size={16} />}
            {t === "history" && <History size={16} />}
            {t === "leaderboard" && <Trophy size={16} />}
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {tab === "arena" && (
        <>
          {!battleId && !inQueue && (
            <div className="grid lg:grid-cols-2 gap-8">
              {/* Queue Panel */}
              <div className="space-y-6">
                <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
                  <h2 className="text-lg font-bold text-text-primary mb-4">Configure Battle</h2>

                  {/* Mode */}
                  <label className="text-sm font-medium text-text-light mb-2 block">Mode</label>
                  <div className="grid grid-cols-3 gap-2 mb-4">
                    {MODES.map((m) => (
                      <button
                        key={m.id}
                        onClick={() => setMode(m.id)}
                        className={`p-3 rounded-xl border text-center transition-all ${
                          mode === m.id
                            ? "border-brand-sky bg-brand-sky/10 text-brand-sky"
                            : "border-black/5 hover:border-brand-sky/30 text-text-secondary"
                        }`}
                      >
                        <m.icon size={20} className="mx-auto mb-1" />
                        <div className="text-xs font-semibold">{m.label}</div>
                        <div className="text-[10px] text-text-light mt-0.5">{m.desc}</div>
                      </button>
                    ))}
                  </div>

                  {/* Difficulty */}
                  <label className="text-sm font-medium text-text-light mb-2 block">Difficulty</label>
                  <div className="flex gap-2 mb-4">
                    {DIFFICULTIES.map((d) => (
                      <button
                        key={d}
                        onClick={() => setDifficulty(d)}
                        className={`flex-1 p-2.5 rounded-xl border text-sm font-medium transition-all ${
                          difficulty === d
                            ? "border-brand-lavender bg-brand-lavender/10 text-brand-lavender"
                            : "border-black/5 hover:border-brand-lavender/30 text-text-secondary"
                        }`}
                      >
                        {d.charAt(0).toUpperCase() + d.slice(1)}
                      </button>
                    ))}
                  </div>

                  {/* Language */}
                  <label className="text-sm font-medium text-text-light mb-2 block">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full rounded-xl border border-black/5 bg-white p-2.5 text-sm"
                  >
                    {LANGUAGES.map((l) => (
                      <option key={l} value={l}>{l.charAt(0).toUpperCase() + l.slice(1)}</option>
                    ))}
                  </select>

                  <button
                    onClick={findMatch}
                    className="w-full mt-6 btn-primary py-3 flex items-center justify-center gap-2"
                  >
                    <Swords size={18} />
                    Find Match
                  </button>
                </div>
              </div>

              {/* Info Panel */}
              <div className="space-y-4">
                <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
                  <h2 className="text-lg font-bold text-text-primary mb-3 flex items-center gap-2">
                    <Rocket size={20} className="text-brand-coral" />
                    How It Works
                  </h2>
                  <ul className="space-y-3 text-sm text-text-secondary">
                    <li className="flex items-start gap-2">
                      <ChevronRight size={16} className="text-brand-sky mt-0.5 shrink-0" />
                      <span><strong>Fastest Mode</strong> — First correct solution wins. Speed bonus points.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ChevronRight size={16} className="text-brand-sky mt-0.5 shrink-0" />
                      <span><strong>Shortest Mode</strong> — Minimal code wins. Shorter = better score.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ChevronRight size={16} className="text-brand-sky mt-0.5 shrink-0" />
                      <span><strong>Reverse Mode</strong> — Figure out the problem from test cases alone.</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ChevronRight size={16} className="text-brand-sky mt-0.5 shrink-0" />
                      <span>Win battles to earn <strong>honor points</strong> and rank up!</span>
                    </li>
                  </ul>
                </div>
                <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
                  <h2 className="text-lg font-bold text-text-primary mb-2 flex items-center gap-2">
                    <BarChart3 size={20} className="text-brand-lavender" />
                    Your Stats
                  </h2>
                  {stats ? (
                    <div className="grid grid-cols-3 gap-3 text-center">
                      <div>
                        <div className="text-2xl font-bold text-text-primary">{stats.total}</div>
                        <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Battles</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-green-600">{stats.wins}</div>
                        <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Wins</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-text-primary">{stats.win_rate}%</div>
                        <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Win Rate</div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-text-light">No battles yet. Start your first!</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Queue Status */}
          {inQueue && (
            <div className="max-w-lg mx-auto text-center py-12">
              <div className="animate-pulse mb-6">
                <Swords size={64} className="mx-auto text-brand-sky" />
              </div>
              <h2 className="text-2xl font-bold text-text-primary mb-2">Searching for Opponent...</h2>
              <p className="text-text-light mb-4">Position in queue: #{queuePos}</p>
              <Loader2 size={24} className="animate-spin mx-auto mb-6 text-brand-lavender" />
              <button onClick={cancelQueue} className="text-sm text-text-light hover:text-error underline">
                Cancel
              </button>
            </div>
          )}

          {/* Active Battle */}
          {activeBattle && battle && (
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Problem Panel */}
              <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold text-text-primary">{battle.problem?.title || "Loading..."}</h2>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-1 rounded-lg bg-brand-coral/10 text-brand-coral text-xs font-semibold capitalize">{battle.difficulty}</span>
                    <span className="px-2 py-1 rounded-lg bg-brand-sky/10 text-brand-sky text-xs font-semibold capitalize">{battle.mode}</span>
                  </div>
                </div>

                {battle.time_remaining_seconds !== undefined && (
                  <div className="flex items-center gap-2 mb-4 p-3 rounded-xl bg-amber-50 border border-amber-200">
                    <Clock size={16} className="text-amber-600" />
                    <span className={`font-bold ${battle.time_remaining_seconds < 120 ? "text-red-600" : "text-amber-700"}`}>
                      {Math.floor(battle.time_remaining_seconds / 60)}:{(battle.time_remaining_seconds % 60).toString().padStart(2, "0")}
                    </span>
                  </div>
                )}

                <div className="prose prose-sm max-w-none mb-4 text-text-secondary">
                  <p>{battle.problem?.description}</p>
                </div>

                {battle.problem?.examples?.length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-sm font-semibold text-text-primary mb-2 flex items-center gap-1">
                      <ScrollText size={14} /> Examples
                    </h3>
                    {battle.problem.examples.map((ex, i) => (
                      <div key={i} className="mb-2 p-2 rounded-lg bg-surface-base text-xs font-mono">
                        <div>Input: {ex.input}</div>
                        <div>Output: {ex.output}</div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Starter code */}
                {battle.problem?.starter_code && (
                  <div className="mb-4">
                    <h3 className="text-sm font-semibold text-text-primary mb-2">Starter Code</h3>
                    <pre className="overflow-x-auto rounded-xl bg-surface-base p-3 text-xs text-emerald-700">{battle.problem.starter_code}</pre>
                  </div>
                )}

                {/* Opponent Status — live via WebSocket */}
                <div className="rounded-xl border border-black/5 bg-white border-border/70 p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${liveStatus === "open" ? "bg-green-500 animate-pulse" : "bg-gray-400"}`} />
                      <span className="text-sm text-text-secondary">{battle.opponent_name || "Opponent"}</span>
                      <span className="text-[9px] font-mono uppercase tracking-wider text-brand-sky">
                        {liveStatus === "open" ? "Live" : liveStatus === "connecting" ? "Connecting" : "Offline"}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      {battle.opponent_submitted ? (
                        <span className="flex items-center gap-1 text-xs text-green-600"><CheckCircle size={14} /> Submitted</span>
                      ) : oppLive.left ? (
                        <span className="flex items-center gap-1 text-xs text-gray-400"><XCircle size={14} /> Left</span>
                      ) : (
                        <span className="flex items-center gap-1 text-xs text-amber-600"><Loader2 size={14} className="animate-spin" /> Solving...</span>
                      )}
                      {battle.opponent_score !== null && battle.opponent_score !== undefined && (
                        <span className="text-sm font-bold text-text-primary">{battle.opponent_score} pts</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 rounded-full bg-white border-border/60 border border-white/70 overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500 bg-gradient-to-r from-brand-sky to-brand-lavender"
                        style={{ width: `${Math.min(100, (oppLive.lines / 40) * 100)}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-text-light w-16 text-right">{oppLive.lines} lines</span>
                  </div>
                </div>
              </div>

              {/* Code Editor Panel */}
              <div className="space-y-4">
                <div className="rounded-2xl border border-black/5 bg-white p-4 shadow-sm">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-text-primary flex items-center gap-1">
                      <Code2 size={16} /> Your Solution
                    </h3>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-text-light">
                      {language}
                    </span>
                  </div>
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    className="h-64 w-full resize-none rounded-xl border border-black/5 bg-surface-base p-3 font-mono text-sm text-emerald-700 focus:outline-none focus:ring-2 focus:ring-brand-sky/50"
                    placeholder="Write your code here..."
                    spellCheck={false}
                  />
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={handleSubmit}
                      disabled={submitting || !code.trim() || battle.my_submitted}
                      className="flex-1 btn-primary py-2.5 flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                      {submitting ? <Loader2 size={16} className="animate-spin" /> : <Rocket size={16} />}
                      {battle.my_submitted ? "Submitted" : "Submit"}
                    </button>
                    <button
                      onClick={handleSurrender}
                      className="px-4 py-2.5 rounded-xl border border-red-200 text-red-600 text-sm font-medium hover:bg-red-50 transition-colors flex items-center gap-2"
                    >
                      <SkipForward size={16} /> Surrender
                    </button>
                  </div>

                  {/* Result */}
                  {result && (
                    <div className={`mt-4 p-4 rounded-xl border ${
                      result.passed === result.total ? "border-green-200 bg-green-50" : "border-amber-200 bg-amber-50"
                    }`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold">{result.passed === result.total ? "All Passed!" : `${result.passed}/${result.total} Passed`}</span>
                        <span className="text-lg font-bold">{result.score} pts</span>
                      </div>
                      {result.passed === result.total ? (
                        <CheckCircle size={20} className="text-green-600" />
                      ) : (
                        <XCircle size={20} className="text-amber-600" />
                      )}
                    </div>
                  )}
                </div>

                {/* My Score */}
                {battle.my_score !== null && battle.my_score !== undefined && (
                  <div className="p-4 rounded-2xl border border-brand-sky/30 bg-brand-sky/5 text-center">
                    <div className="text-sm text-text-light">Your Score</div>
                    <div className="text-3xl font-bold text-brand-sky">{battle.my_score}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Completed Battle */}
          {battleId && !activeBattle && battle && (
            <div className="max-w-lg mx-auto text-center py-12">
              {battle.winner_id === myUserId && battle.my_submitted ? (
                <div>
                  <Trophy size={64} className="mx-auto text-yellow-500 mb-4" />
                  <h2 className="text-2xl font-bold text-text-primary mb-2">You Won!</h2>
                </div>
              ) : (
                <div>
                  <XCircle size={64} className="mx-auto text-gray-400 mb-4" />
                  <h2 className="text-2xl font-bold text-text-primary mb-2">Battle Over</h2>
                </div>
              )}
              <p className="text-text-light">Your score: {battle.my_score} | Opponent: {battle.opponent_score}</p>
              <button
                onClick={() => { setBattleId(null); setBattle(null); setCode(""); setResult(null); setOppLive(INITIAL_OPP_LIVE); }}
                className="mt-6 btn-primary px-8 py-3"
              >
                Battle Again
              </button>
            </div>
          )}
        </>
      )}

      {/* History Tab */}
      {tab === "history" && (
        <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-bold text-text-primary mb-4">Battle History</h2>
          {history.length === 0 ? (
            <p className="text-text-light text-sm">No battles yet. Queue up and fight!</p>
          ) : (
            <div className="space-y-2">
              {history.map((b, i) => (
                <div key={i} className="flex items-center justify-between rounded-xl border border-black/5 bg-white border-border/70 p-3 transition-colors hover:bg-white">
                  <div className="flex items-center gap-3">
                    {b.won === true ? (
                      <Medal size={20} className="text-yellow-500" />
                    ) : b.won === false ? (
                      <XCircle size={20} className="text-red-400" />
                    ) : (
                      <MinusCircle size={20} className="text-gray-400" />
                    )}
                    <div>
                      <div className="text-sm font-medium text-text-primary">
                        vs <span className="font-bold">{b.opponent_name}</span>
                      </div>
                      <div className="text-[11px] text-text-light flex items-center gap-2">
                        <span className="capitalize">{b.mode}</span>
                        <span className="capitalize">{b.difficulty}</span>
                        <span>{new Date(b.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-text-primary">{b.my_score ?? "-"} pts</div>
                    <div className="text-[11px] text-text-light">{b.opponent_score ?? "-"} pts</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Leaderboard Tab */}
      {tab === "leaderboard" && (
        <div className="rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-bold text-text-primary mb-4">Battle Leaderboard</h2>
          {leaderboard.length === 0 ? (
            <p className="text-text-light text-sm">No rankings yet.</p>
          ) : (
            <div className="space-y-1">
              {leaderboard.map((entry, i) => (
                <div key={i} className="flex items-center justify-between rounded-xl p-3 transition-colors hover:bg-surface-2">
                  <div className="flex items-center gap-3">
                    <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                      i === 0 ? "bg-yellow-100 text-yellow-700" :
                      i === 1 ? "bg-surface-2 text-brand-secondary" :
                      i === 2 ? "bg-orange-100 text-orange-700" :
                      "bg-surface-2 text-brand-muted"
                    }`}>
                      {i + 1}
                    </span>
                    <div>
                      <div className="text-sm font-medium text-text-primary">{entry.name}</div>
                      <div className="text-[11px] text-text-light">{entry.wins} wins · {entry.total_battles} battles</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-green-600">{entry.win_rate}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function MinusCircle(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={props.size || 24} height={props.size || 24} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="8" y1="12" x2="16" y2="12" />
    </svg>
  );
}
