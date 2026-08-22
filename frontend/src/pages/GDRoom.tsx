import { useState, useEffect, useRef, useCallback } from "react";
import { useParams } from "react-router-dom";
import { gdApi } from "../services/api/gdRooms.ts";
import useAuthStore from "../store/authStore";
import {
  Users, Mic, MicOff, Clock, MessageSquare, Play, Square,
  Plus, Copy, Check, Send, Trophy, Star, ListChecks, Loader2, DoorOpen, Timer,
} from "lucide-react";

const RUBRIC = [
  { key: "clarity", label: "Clarity", desc: "How clearly they communicated ideas" },
  { key: "listening", label: "Listening", desc: "Acknowledged and responded to others" },
  { key: "initiative", label: "Initiative", desc: "Took the lead / spoke up when needed" },
];

const DURATION_OPTIONS = [10, 15, 20, 30];

function formatTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export default function GDRoom() {
  const { roomId: routeRoomId } = useParams();
  const me = useAuthStore((s) => s.user);
  const myId = me?.id || null;

  const [view, setView] = useState("lobby"); // lobby | room
  const [roomId, setRoomId] = useState(routeRoomId || null);
  const [rooms, setRooms] = useState([]);
  const [topics, setTopics] = useState([]);
  const [topic, setTopic] = useState("");
  const [customTopic, setCustomTopic] = useState("");
  const [duration, setDuration] = useState(15);
  const [maxP, setMaxP] = useState(5);
  const [joinCode, setJoinCode] = useState("");
  const [creating, setCreating] = useState(false);
  const [joining, setJoining] = useState(false);

  const [room, setRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [speaking, setSpeaking] = useState({});
  const [timerEndAt, setTimerEndAt] = useState(null);
  const [timerLeft, setTimerLeft] = useState(0);
  const [wsLive, setWsLive] = useState(false);
  const [copied, setCopied] = useState(false);
  const [ratings, setRatings] = useState({});
  const [ratingPeers, setRatingPeers] = useState([]);
  const [scores, setScores] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [error, setError] = useState("");

  const wsRef = useRef(null);
  const reconnectRef = useRef(null);
  const attemptRef = useRef(0);
  const listEndRef = useRef(null);

  const inRoom = room && roomId;

  const loadRooms = useCallback(async () => {
    try {
      const data = await gdApi.listRooms();
      setRooms(data.rooms || []);
    } catch {
      // ignore
    }
  }, []);

  const loadTopics = useCallback(async () => {
    try {
      const data = await gdApi.topics();
      setTopics(data.topics || []);
      if (!topic && data.topics?.length) setTopic(data.topics[0]);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    loadRooms();
    loadTopics();
    const iv = setInterval(loadRooms, 15000);
    return () => clearInterval(iv);
  }, [loadRooms, loadTopics]);

  // ── WebSocket for an active room ───────────────────────────────────────
  useEffect(() => {
    if (!roomId) return;

    let ws;
    const connect = () => {
      try {
        ws = new WebSocket(gdApi.wsUrl(roomId));
      } catch {
        return;
      }
      wsRef.current = ws;
      ws.onopen = () => {
        setWsLive(true);
        attemptRef.current = 0;
      };
      ws.onclose = () => {
        setWsLive(false);
        const delay = Math.min(1000 * 2 ** attemptRef.current, 20000);
        attemptRef.current += 1;
        reconnectRef.current = setTimeout(connect, delay);
      };
      ws.onmessage = (ev) => {
        let msg;
        try {
          msg = JSON.parse(ev.data);
        } catch {
          return;
        }
        handleWs(msg);
      };
    };

    connect();
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      if (wsRef.current) {
        wsRef.current.onclose = null;
        wsRef.current.close(1000, "cleanup");
        wsRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roomId]);

  const handleWs = (msg) => {
    const d = msg.data || {};
    if (msg.type === "sync") {
      setRoom({
        room_id: d.room_id,
        topic: d.topic,
        status: d.status,
        host_id: d.host_id,
        participants: d.participants || [],
      });
      setMessages((d.messages || []).slice().reverse());
      setSpeaking(d.speaking || {});
      if (d.timer_end_at) setTimerEndAt(d.timer_end_at);
    } else if (msg.type === "message") {
      setMessages((prev) => {
        const next = [...prev, d];
        return next.slice(-100);
      });
    } else if (msg.type === "speak") {
      setSpeaking((prev) => ({ ...prev, [d.user_id]: !!d.speaking }));
    } else if (msg.type === "timer") {
      setTimerEndAt(d.end_at);
    } else if (msg.type === "timer_done") {
      setTimerEndAt(null);
      setTimerLeft(0);
    } else if (msg.type === "session_start") {
      setRoom((r) => (r ? { ...r, status: "ongoing" } : r));
      refreshRoom();
    } else if (msg.type === "session_end") {
      setRoom((r) => (r ? { ...r, status: "completed" } : r));
      refreshRoom();
      loadScores();
    }
  };

  const refreshRoom = useCallback(async () => {
    if (!roomId) return;
    try {
      const r = await gdApi.getRoom(roomId);
      setRoom({
        room_id: r.room_id,
        topic: r.topic,
        status: r.status,
        host_id: r.host_id,
        participants: r.participants || [],
      });
    } catch {
      // ignore
    }
  }, [roomId]);

  const loadScores = useCallback(async () => {
    if (!roomId) return;
    try {
      const data = await gdApi.roomScores(roomId);
      setScores(data.scores || []);
    } catch {
      // ignore
    }
  }, [roomId]);

  const loadFeedback = useCallback(async () => {
    if (!roomId) return;
    try {
      setFeedback(await gdApi.myFeedback(roomId));
    } catch {
      // ignore
    }
  }, [roomId]);

  useEffect(() => {
    if (room?.status === "completed") {
      loadScores();
      loadFeedback();
    }
  }, [room?.status, loadScores, loadFeedback]);

  // ── Timer countdown ────────────────────────────────────────────────────
  useEffect(() => {
    if (!timerEndAt) return;
    const tick = () => {
      const left = Math.max(0, Math.round((new Date(timerEndAt).getTime() - Date.now()) / 1000));
      setTimerLeft(left);
      if (left <= 0) {
        setTimerEndAt(null);
        setTimerLeft(0);
      }
    };
    tick();
    const iv = setInterval(tick, 1000);
    return () => clearInterval(iv);
  }, [timerEndAt]);

  useEffect(() => {
    listEndRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages]);

  // ── Actions ────────────────────────────────────────────────────────────
  const handleCreate = async () => {
    setCreating(true);
    setError("");
    try {
      const r = await gdApi.createRoom({
        topic: customTopic || topic,
        duration_minutes: duration,
        max_participants: maxP,
      });
      setRoomId(r.room_id);
      setView("room");
      setRoom({ room_id: r.room_id, topic: r.topic, status: r.status, host_id: r.host_id, participants: r.participants });
      setMessages([]);
    } catch (e) {
      setError(e.message || "Could not create room");
    } finally {
      setCreating(false);
    }
  };

  const handleJoin = async (id) => {
    setJoining(true);
    setError("");
    try {
      const r = await gdApi.join(id);
      setRoomId(r.room_id);
      setView("room");
      setRoom({ room_id: r.room_id, topic: r.topic, status: r.status, host_id: r.host_id, participants: r.participants });
      setMessages([]);
    } catch (e) {
      setError(e.message || "Could not join room");
    } finally {
      setJoining(false);
    }
  };

  const handleJoinByCode = async () => {
    setError("");
    if (!joinCode.trim()) return;
    try {
      const r = await gdApi.joinByCode(joinCode);
      setRoomId(r.room_id);
      setView("room");
      setRoom({ room_id: r.room_id, topic: r.topic, status: r.status, host_id: r.host_id, participants: r.participants });
      setMessages([]);
    } catch (e) {
      setError(e.message || "Invalid code");
    }
  };

  const handleStart = async () => {
    setError("");
    try {
      await gdApi.start(roomId);
      refreshRoom();
    } catch (e) {
      setError(e.message || "Could not start");
    }
  };

  const handleEnd = async () => {
    setError("");
    try {
      await gdApi.end(roomId);
      refreshRoom();
      loadScores();
      loadFeedback();
    } catch (e) {
      setError(e.message || "Could not end session");
    }
  };

  const handleTimer = async (seconds) => {
    try {
      await gdApi.setTimer(roomId, seconds);
    } catch (e) {
      setError(e.message || "Could not set timer");
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !wsLive) return;
    setSending(true);
    try {
      wsRef.current?.send(JSON.stringify({ type: "message", text: input }));
      setInput("");
    } finally {
      setSending(false);
    }
  };

  const toggleSpeak = (val) => {
    wsRef.current?.send(JSON.stringify({ type: "speak", speaking: val }));
  };

  const submitRating = async (targetId) => {
    const r = ratings[targetId];
    if (!r) return;
    try {
      await gdApi.rate(roomId, {
        target_user_id: targetId,
        clarity: r.clarity,
        listening: r.listening,
        initiative: r.initiative,
        comment: r.comment || "",
      });
      setRatingPeers((prev) => prev.filter((p) => p.user_id !== targetId));
      loadScores();
    } catch (e) {
      setError(e.message || "Could not submit rating");
    }
  };

  const openRatings = () => {
    if (!room?.participants) return;
    setRatingPeers(room.participants.filter((p) => p.user_id !== myId));
  };

  const copyCode = () => {
    if (navigator.clipboard && room) {
      navigator.clipboard.writeText(room.room_id ? room.room_id : "");
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const fmtTimer = (s) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <Users className="text-brand-coral" size={32} />
            GD Practice Rooms
          </h1>
          <p className="text-text-light mt-1">Practice group discussions with peers, timed and peer-rated</p>
        </div>
        {inRoom && (
          <button
            onClick={() => { setView("lobby"); setRoomId(null); setRoom(null); setMessages([]); }}
            className="px-4 py-2 rounded-xl border border-white/60 text-sm font-medium flex items-center gap-2 hover:bg-white/60"
          >
            <DoorOpen size={16} /> Leave Room
          </button>
        )}
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      {view === "lobby" && (
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Create room */}
          <div className="p-6 rounded-2xl border border-white/60 bg-white/80 space-y-4">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <Plus size={18} className="text-brand-sky" /> Create Room
            </h2>
            <div>
              <label className="text-sm font-medium text-text-light mb-2 block">Topic</label>
              <select
                value={customTopic ? "__custom" : topic}
                onChange={(e) => { setTopic(e.target.value); if (e.target.value !== "__custom") setCustomTopic(""); }}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              >
                {topics.map((t) => <option key={t} value={t}>{t}</option>)}
                <option value="__custom">Custom topic…</option>
              </select>
            </div>
            {customTopic !== "" && (
              <div>
                <label className="text-sm font-medium text-text-light mb-2 block">Custom topic</label>
                <input
                  value={customTopic}
                  onChange={(e) => setCustomTopic(e.target.value)}
                  placeholder="Type your own topic"
                  className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
                />
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-text-light mb-2 block">Duration</label>
              <div className="flex gap-2">
                {DURATION_OPTIONS.map((d) => (
                  <button
                    key={d}
                    onClick={() => setDuration(d)}
                    className={`flex-1 p-2 rounded-xl border text-sm font-medium ${duration === d ? "border-brand-sky bg-brand-sky/10 text-brand-sky" : "border-white/60 text-text-secondary hover:border-brand-sky/30"}`}
                  >
                    {d}m
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-text-light mb-2 block">Max participants ({maxP})</label>
              <input
                type="range"
                min={4}
                max={6}
                value={maxP}
                onChange={(e) => setMaxP(Number(e.target.value))}
                className="w-full"
              />
            </div>
            <button onClick={handleCreate} disabled={creating} className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50">
              {creating ? <Loader2 size={18} className="animate-spin" /> : <Users size={18} />} Create Room
            </button>

            <div className="pt-2 border-t border-white/60">
              <label className="text-sm font-medium text-text-light mb-2 block">Or join with code</label>
              <div className="flex gap-2">
                <input
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                  placeholder="ABCDEF"
                  maxLength={6}
                  className="flex-1 p-2.5 rounded-xl border border-white/60 bg-white text-sm font-mono uppercase"
                />
                <button onClick={handleJoinByCode} className="px-4 py-2.5 rounded-xl border border-brand-lavender/50 text-brand-lavender text-sm font-medium hover:bg-brand-lavender/5">
                  Join
                </button>
              </div>
            </div>
          </div>

          {/* Open rooms */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <ListChecks size={18} className="text-brand-lavender" /> Open Rooms
            </h2>
            {rooms.length === 0 ? (
              <div className="p-6 rounded-2xl border border-white/60 bg-white/80 text-text-light text-sm">
                No open rooms yet. Create one and share the code!
              </div>
            ) : (
              rooms.map((r) => (
                <div key={r.room_id} className="p-5 rounded-2xl border border-white/60 bg-white/80 hover:bg-white transition-colors">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-base font-semibold text-text-primary">{r.topic}</div>
                      <div className="text-xs text-text-light mt-1 flex items-center gap-3">
                        <span className="flex items-center gap-1"><Clock size={12} /> {r.duration_minutes} min</span>
                        <span className="flex items-center gap-1"><Users size={12} /> {r.participant_count}/{r.max_participants}</span>
                        <span>Host: {r.participants?.[0]?.name || "—"}</span>
                        <span className="px-1.5 py-0.5 rounded bg-green-50 text-green-600 font-mono uppercase text-[10px]">{r.join_code}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleJoin(r.room_id)}
                      disabled={r.participant_count >= r.max_participants || joining}
                      className="px-4 py-2 rounded-xl btn-primary text-sm disabled:opacity-40"
                    >
                      {r.participant_count >= r.max_participants ? "Full" : "Join"}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {view === "room" && room && (
        <div className="space-y-6">
          {/* Room header */}
          <div className="p-6 rounded-2xl border border-white/60 bg-white/80">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h2 className="text-xl font-bold text-text-primary">{room.topic}</h2>
                <div className="text-xs text-text-light mt-1 flex items-center gap-3 flex-wrap">
                  <span className={`flex items-center gap-1 ${wsLive ? "text-green-600" : "text-amber-600"}`}>
                    <span className={`w-2 h-2 rounded-full ${wsLive ? "bg-green-500 animate-pulse" : "bg-amber-500"}`} />
                    {wsLive ? "Live" : "Reconnecting…"}
                  </span>
                  <span className="uppercase">{room.status}</span>
                  <span className="flex items-center gap-1">
                    <Users size={13} /> {room.participants?.length || 0} present
                  </span>
                  {room.host_id === myId ? <span className="px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 text-[10px] font-semibold">Host</span> : null}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {room.status === "open" && room.host_id === myId && (
                  <button onClick={handleStart} className="btn-primary px-4 py-2 text-sm flex items-center gap-2">
                    <Play size={16} /> Start Session
                  </button>
                )}
                {room.status === "ongoing" && room.host_id === myId && (
                  <button onClick={handleEnd} className="px-4 py-2 rounded-xl border border-red-200 text-red-600 text-sm font-medium hover:bg-red-50 flex items-center gap-2">
                    <Square size={14} /> End Session
                  </button>
                )}
                {room.status !== "open" && room.status !== "completed" && (
                  <button onClick={openRatings} className="btn-primary px-4 py-2 text-sm flex items-center gap-2">
                    <Star size={16} /> Rate Peers
                  </button>
                )}
              </div>
            </div>

            {/* Timer */}
            <div className="mt-4 flex items-center gap-3 flex-wrap">
              <span className="text-sm font-medium text-text-light flex items-center gap-1"><Timer size={15} /> Timer</span>
              {timerEndAt ? (
                <span className={`text-2xl font-bold font-mono ${timerLeft < 60 ? "text-red-600" : "text-text-primary"}`}>
                  {fmtTimer(timerLeft)}
                </span>
              ) : (
                <span className="text-sm text-text-light">Not running</span>
              )}
              {room.status === "ongoing" && room.host_id === myId && (
                <div className="flex items-center gap-1 ml-2">
                  {[60, 120, 300].map((s) => (
                    <button
                      key={s}
                      onClick={() => handleTimer(s)}
                      className={`px-2.5 py-1 rounded-lg border text-xs font-medium ${timerEndAt ? "border-white/60 text-text-secondary" : "border-brand-sky/40 text-brand-sky hover:bg-brand-sky/5"}`}
                    >
                      {s / 60}m
                    </button>
                  ))}
                  {timerEndAt && (
                    <button onClick={() => handleTimer(60)} className="px-2.5 py-1 rounded-lg border border-white/60 text-xs font-medium text-text-secondary hover:bg-white/60">
                      Reset
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Participants */}
            <div className="p-5 rounded-2xl border border-white/60 bg-white/80 space-y-3">
              <h3 className="text-sm font-bold text-text-primary flex items-center gap-2">
                <Users size={16} /> Participants
              </h3>
              {room.participants?.map((p) => (
                <div key={p.user_id} className="flex items-center justify-between p-2.5 rounded-xl border border-white/60 bg-white/50">
                  <div className="flex items-center gap-2">
                    {speaking[p.user_id] ? (
                      <Mic size={16} className="text-green-600 animate-pulse" />
                    ) : (
                      <MicOff size={16} className="text-text-light" />
                    )}
                    <div>
                      <div className="text-sm font-medium text-text-primary flex items-center gap-1">
                        {p.name}
                        {p.user_id === room.host_id && <span className="text-[9px] font-semibold text-amber-600 uppercase">Host</span>}
                      </div>
                    </div>
                  </div>
                  {p.user_id === myId && <span className="text-[10px] text-text-light">you</span>}
                </div>
              ))}

              {/* My mic */}
              <div className="pt-2 border-t border-white/60">
                <button
                  onClick={() => toggleSpeak(!speaking[myId])}
                  className={`w-full px-3 py-2 rounded-xl text-sm font-medium flex items-center justify-center gap-2 border ${
                    speaking[myId] ? "bg-green-50 border-green-200 text-green-700" : "border-white/60 text-text-secondary hover:bg-white/60"
                  }`}
                >
                  {speaking[myId] ? <Mic size={16} /> : <MicOff size={16} />}
                  {speaking[myId] ? "I'm Speaking" : "Mark me as speaking"}
                </button>
              </div>
            </div>

            {/* Chat */}
            <div className="lg:col-span-2 p-5 rounded-2xl border border-white/60 bg-white/80 flex flex-col" style={{ minHeight: "420px" }}>
              <h3 className="text-sm font-bold text-text-primary flex items-center gap-2 mb-3">
                <MessageSquare size={16} /> Discussion
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2 mb-3 pr-1" style={{ maxHeight: "300px" }}>
                {messages.length === 0 && (
                  <p className="text-sm text-text-light text-center py-8">No points yet. Kick off the discussion!</p>
                )}
                {messages.map((m, i) => (
                  <div
                    key={i}
                    className={`flex ${m.user_id === myId ? "justify-end" : "justify-start"}`}
                  >
                    <div className={`max-w-[80%] p-2.5 rounded-xl text-sm ${
                      m.user_id === myId ? "bg-brand-sky/10 text-text-primary" : "bg-white/60 border border-white/70 text-text-secondary"
                    }`}>
                      {m.user_id !== myId && <div className="text-[11px] font-semibold text-text-light mb-0.5">{m.name}</div>}
                      {m.text}
                      <div className="text-[10px] text-text-light mt-1 text-right">{formatTime(m.created_at)}</div>
                    </div>
                  </div>
                ))}
                <div ref={listEndRef} />
              </div>
              <div className="flex gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  placeholder="Share a point…"
                  className="flex-1 p-2.5 rounded-xl border border-white/60 bg-white text-sm"
                />
                <button onClick={handleSend} disabled={sending || !wsLive} className="px-4 py-2.5 rounded-xl btn-primary text-sm flex items-center gap-2 disabled:opacity-50">
                  <Send size={15} /> Send
                </button>
              </div>
            </div>
          </div>

          {/* Peer ratings */}
          {ratingPeers.length > 0 && (
            <div className="p-6 rounded-2xl border border-white/60 bg-white/80">
              <h3 className="text-lg font-bold text-text-primary mb-4 flex items-center gap-2">
                <Star size={18} className="text-yellow-500" /> Rate Your Peers
              </h3>
              <div className="space-y-6">
                {ratingPeers.map((p) => {
                  const r = ratings[p.user_id] || { clarity: 3, listening: 3, initiative: 3, comment: "" };
                  return (
                    <div key={p.user_id} className="p-4 rounded-xl border border-white/60 bg-white/50">
                      <div className="text-sm font-semibold text-text-primary mb-3">{p.name}</div>
                      <div className="grid sm:grid-cols-3 gap-4 mb-3">
                        {RUBRIC.map((rub) => (
                          <div key={rub.key}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs font-medium text-text-light">{rub.label}</span>
                              <span className="text-xs font-bold text-brand-sky">{r[rub.key]}/5</span>
                            </div>
                            <input
                              type="range"
                              min={1}
                              max={5}
                              value={r[rub.key]}
                              onChange={(e) => setRatings((prev) => ({
                                ...prev,
                                [p.user_id]: { ...(prev[p.user_id] || { comment: "" }), [rub.key]: Number(e.target.value) },
                              }))}
                              className="w-full"
                            />
                          </div>
                        ))}
                      </div>
                      <input
                        value={r.comment}
                        onChange={(e) => setRatings((prev) => ({
                          ...prev,
                          [p.user_id]: { ...(prev[p.user_id] || { clarity: 3, listening: 3, initiative: 3 }), comment: e.target.value },
                        }))}
                        placeholder="Optional note (what they did well, what to improve)"
                        className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm mb-3"
                      />
                      <button onClick={() => submitRating(p.user_id)} className="px-4 py-2 rounded-xl btn-primary text-sm">
                        Submit Rating
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Scores */}
          {room.status === "completed" && scores && (
            <div className="p-6 rounded-2xl border border-white/60 bg-white/80">
              <h3 className="text-lg font-bold text-text-primary mb-4 flex items-center gap-2">
                <Trophy size={18} className="text-yellow-500" /> Room Scores
              </h3>
              <div className="space-y-2">
                {scores.map((s, i) => (
                  <div key={s.user_id} className="flex items-center justify-between p-3 rounded-xl border border-white/60 bg-white/50">
                    <div className="flex items-center gap-3">
                      <span className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold bg-surface-base text-brand-muted">{i + 1}</span>
                      <div>
                        <div className="text-sm font-medium text-text-primary">{s.name} {s.user_id === myId && <span className="text-[10px] text-text-light">(you)</span>}</div>
                        <div className="text-[11px] text-text-light">
                          {s.ratings_count} rating{s.ratings_count === 1 ? "" : "s"} · clarity {s.averages?.clarity ?? "—"} · listening {s.averages?.listening ?? "—"} · initiative {s.averages?.initiative ?? "—"}
                        </div>
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-brand-sky">{s.overall ?? "—"}</div>
                  </div>
                ))}
              </div>
              {feedback && feedback.ratings_count > 0 && (
                <div className="mt-4 p-4 rounded-xl bg-brand-lavender/5 border border-brand-lavender/20">
                  <div className="text-sm font-bold text-text-primary mb-2">Your received feedback</div>
                  <div className="text-xs text-text-light mb-2">
                    Overall {feedback.overall}/5 from {feedback.ratings_count} peer rating{feedback.ratings_count === 1 ? "" : "s"}
                  </div>
                  {feedback.comments?.map((c, i) => (
                    <div key={i} className="text-sm text-text-secondary mb-1">"{c.comment}"</div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Share code */}
          <div className="p-4 rounded-2xl border border-white/60 bg-white/50 flex items-center justify-between">
            <div className="text-sm text-text-light">
              Share this room with friends — code <span className="font-mono font-bold text-brand-sky">{room.room_id}</span>
            </div>
            <button onClick={copyCode} className="px-3 py-1.5 rounded-lg border border-white/60 text-xs font-medium flex items-center gap-1.5 hover:bg-white/60">
              {copied ? <Check size={13} className="text-green-600" /> : <Copy size={13} />} {copied ? "Copied" : "Copy ID"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
