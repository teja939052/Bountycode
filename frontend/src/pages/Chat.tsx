import { useState, useEffect, useRef, useCallback } from "react";
import { chatApi } from "../services/api/chat.ts";
import { friendsApi } from "../services/api/friends.ts";
import { collegeNetworkApi } from "../services/api/collegeNetwork.ts";
import { guildsApi } from "../services/api/guilds.ts";
import useAuthStore from "../store/authStore";

const TABS = [
  { key: "global", label: "Global" },
  { key: "guild", label: "Guild" },
  { key: "college", label: "College" },
  { key: "dm", label: "Friends" },
];

function formatTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

function roomLabel(type, id) {
  if (type === "global") return "Global Chat";
  if (type === "guild") return "Guild | " + id.slice(0, 8);
  if (type === "college") return "College | " + id;
  if (type === "dm") return "DM | " + id.slice(0, 10);
  return type + " | " + id;
}

export default function Chat() {
  const user = useAuthStore((s) => s.user);
  const [tab, setTab] = useState("global");
  const [rooms, setRooms] = useState({ global: { type: "global", id: "" } });
  const [room, setRoom] = useState({ type: "global", id: "" });

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [emoji, setEmoji] = useState("");
  const [emojis, setEmojis] = useState({ reactions: [], emojis: [] });
  const [showAllEmojis, setShowAllEmojis] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [typing, setTyping] = useState(false);

  const [guildId, setGuildId] = useState("");
  const [college, setCollege] = useState("");
  const [friendId, setFriendId] = useState("");
  const [peers, setPeers] = useState([]);

  const [recentRooms, setRecentRooms] = useState([]);
  const [live, setLive] = useState(false);
  const [unreadCounts, setUnreadCounts] = useState({});
  const [totalUnread, setTotalUnread] = useState(0);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [showRoomInfo, setShowRoomInfo] = useState(false);
  const [roomStats, setRoomStats] = useState(null);
  const [roomMembers, setRoomMembers] = useState([]);
  const [showMembers, setShowMembers] = useState(false);
  const [myUid, setMyUid] = useState("");
  const [myUidCopied, setMyUidCopied] = useState(false);
  const [friends, setFriends] = useState([]);
  const [received, setReceived] = useState([]);
  const [sent, setSent] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [newUidInput, setNewUidInput] = useState("");
  const [addingFriend, setAddingFriend] = useState(false);

  const lastIdRef = useRef(null);
  const listEndRef = useRef(null);
  const typingTimer = useRef(null);
  const inputRef = useRef(null);
  const wsRef = useRef(null);
  const pollTimerRef = useRef(null);
  const searchTimerRef = useRef(null);

  const roomKey = room ? `${room.type}:${room.id}` : "";

  const showFakeTyping = useCallback(() => {
    setTyping(true);
    if (typingTimer.current) clearTimeout(typingTimer.current);
    typingTimer.current = setTimeout(() => setTyping(false), 1800);
  }, []);

  const loadEmotes = useCallback(async () => {
    try {
      const data = await chatApi.emotes();
      setEmojis({ reactions: data.reactions || [], emojis: data.emojis || [] });
    } catch {
      setEmojis({ reactions: ["🔥", "😂", "💯", "👍", "👏", "🎉", "🤯", "💀", "🐛", "🧠"], emojis: [] });
    }
  }, []);

  const loadRecent = useCallback(async () => {
    try {
      const data = await chatApi.recent();
      setRecentRooms(data.rooms || []);
    } catch {
      // ignore - recent rooms are best-effort
    }
  }, []);

  const loadUnread = useCallback(async () => {
    try {
      const data = await chatApi.unreadCount();
      const counts = {};
      (data.unread_rooms || []).forEach((r) => {
        counts[`${r.room_type}:${r.room_id || ""}`] = r.unread_count;
      });
      setUnreadCounts(counts);
      setTotalUnread(data.total_unread || 0);
    } catch {
      // ignore
    }
  }, []);

  const loadPrefill = useCallback(async () => {
    try {
      const [myGuild, profile, batch] = await Promise.allSettled([
        guildsApi.my(),
        collegeNetworkApi.profile(),
        collegeNetworkApi.sameBatch(),
      ]);
      if (myGuild.status === "fulfilled" && myGuild.value) {
        setGuildId(myGuild.value._id || myGuild.value.id || "");
      }
      if (profile.status === "fulfilled" && profile.value?.profile) {
        setCollege(profile.value.profile.college || "");
      }
      if (batch.status === "fulfilled" && batch.value?.peers) {
        setPeers(batch.value.peers);
      }
    } catch {
      // ignore prefill failures
    }
  }, []);

  useEffect(() => {
    loadEmotes();
    loadRecent();
    loadPrefill();
    loadUnread();
    const interval = setInterval(loadUnread, 30000);
    return () => clearInterval(interval);
  }, [loadEmotes, loadRecent, loadPrefill, loadUnread]);

  useEffect(() => {
    return () => {
      if (typingTimer.current) clearTimeout(typingTimer.current);
      if (searchTimerRef.current) clearTimeout(searchTimerRef.current);
    };
  }, []);

  useEffect(() => {
    async function loadMyUid() {
      try {
        const uidRes = await friendsApi.uid();
        setMyUid(uidRes.uid || "");
        const ovRes = await friendsApi.overview();
        setFriends(ovRes.friends || []);
        setReceived(ovRes.received || []);
        setSent(ovRes.sent || []);
        // Generate suggestions: non-friends with names
        const allUserIds = new Set([user?.id || "", ...friends.map(f => f.friend_id).filter(Boolean)]);
        // Simple suggestion fetch — just a few random users; could be enhanced with server search
        setSuggestions([]);
      } catch {
        // ignore — uid will remain empty; user can manually generate later
      }
    }
    loadMyUid();
  }, [user?.id]);

  // Append messages with dedup by id; shared by WS frames, polling and local sends.
  const appendMessages = useCallback((msgs) => {
    if (!msgs.length) return;
    setMessages((prev) => {
      const existing = new Set(prev.map((m) => m.id));
      const fresh = msgs.filter((m) => !existing.has(m.id));
      return fresh.length ? [...prev, ...fresh] : prev;
    });
    lastIdRef.current = msgs[msgs.length - 1].id;
  }, []);

  // Live messages: WebSocket fan-out with REST polling fallback.
  useEffect(() => {
    if (!room) return;
    let cancelled = false;

    const loadInitial = async () => {
      try {
        const data = await chatApi.messages(room.type, room.id, 50, null);
        if (cancelled) return;
        const msgs = data.messages || [];
        setMessages(msgs);
        lastIdRef.current = msgs.length ? msgs[msgs.length - 1].id : null;
      } catch {
        if (!cancelled) setMessages([]);
      }
    };

    const poll = async () => {
      if (cancelled) return;
      try {
        const data = await chatApi.messages(room.type, room.id, 50, lastIdRef.current || null);
        if (cancelled) return;
        appendMessages(data.messages || []);
      } catch {
        // transient failure; try again next tick
      }
    };

    const connect = () => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;
      let ws;
      try {
        ws = new WebSocket(chatApi.wsUrl(room.type, room.id));
      } catch {
        startPollFallback();
        return;
      }
      wsRef.current = ws;

      ws.onopen = () => {
        if (cancelled) return;
        setLive(true);
        if (pollTimerRef.current) {
          clearInterval(pollTimerRef.current);
          pollTimerRef.current = null;
        }
      };

      ws.onmessage = (evt) => {
        if (cancelled) return;
        try {
          const parsed = JSON.parse(evt.data);
          if (parsed.type === "message" && parsed.data) {
            appendMessages([parsed.data]);
          } else if (parsed.type === "typing") {
            showFakeTyping();
          }
        } catch {
          // ignore malformed frames
        }
      };

      ws.onerror = () => {
        // fall through to onclose
      };

      ws.onclose = () => {
        if (cancelled) return;
        setLive(false);
        wsRef.current = null;
        startPollFallback();
      };
    };

    const startPollFallback = () => {
      if (pollTimerRef.current) return;
      poll();
      pollTimerRef.current = setInterval(poll, 3000);
    };

    loadInitial();
    connect();

    return () => {
      cancelled = true;
      if (pollTimerRef.current) {
        clearInterval(pollTimerRef.current);
        pollTimerRef.current = null;
      }
      if (wsRef.current) {
        wsRef.current.onclose = null;
        try {
          wsRef.current.close();
        } catch {
          // already closed
        }
        wsRef.current = null;
      }
    };
  }, [roomKey, room]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    listEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  const switchTab = (key) => {
    setError("");
    setSearchQuery("");
    setSearchResults([]);
    setShowSearch(false);
    setRoomStats(null);
    setRoomMembers([]);
    setTab(key);
    setRoom(rooms[key] || null);
  };

  const joinRoom = (type, id) => {
    if (!id || !id.trim()) {
      setError("Enter a room id first");
      return;
    }
    const newRoom = { type, id: id.trim() };
    setError("");
    setRooms((prev) => ({ ...prev, [type]: newRoom }));
    setRoom(newRoom);
    setRoomStats(null);
    setRoomMembers([]);
    if (type === "dm" || type === "college") setTab(type);
  };

  const openRecentRoom = (r) => {
    const newRoom = { type: r.room_type, id: r.room_id || "" };
    setError("");
    setRooms((prev) => ({ ...prev, [r.room_type]: newRoom }));
    setRoom(newRoom);
    setRoomStats(null);
    setRoomMembers([]);
    setTab(r.room_type);
  };

  const wsSend = (payload) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "send", ...payload }));
      return true;
    }
    return false;
  };

  const handleSend = async () => {
    const text = input.trim().slice(0, 500);
    if ((!text && !emoji) || !room || sending) return;
    setSending(true);
    setError("");
    try {
      if (!wsSend({ text, emoji: emoji || undefined })) {
        const msg = await chatApi.send({
          room_type: room.type,
          room_id: room.id || undefined,
          text,
          emoji: emoji || undefined,
        });
        appendMessages([msg]);
      }
      setInput("");
      setEmoji("");
      showFakeTyping();
      loadRecent();
      loadUnread();
    } catch (e) {
      setError(e.message || "Failed to send message");
    } finally {
      setSending(false);
    }
  };

  const pickEmoji = (e) => {
    setEmoji((prev) => (prev === e ? "" : e));
    inputRef.current?.focus();
  };

  const sendEmojiOnly = (e) => {
    if (!room) return;
    setEmoji("");
    const text = input.trim();
    const payload: any = { room_type: room.type, room_id: room.id || undefined };
    if (text) payload.text = text.slice(0, 500);
    else payload.emoji = e;
    setSending(true);
    if (!wsSend(text ? { text: payload.text } : { emoji: payload.emoji })) {
      chatApi.send(payload)
        .then((msg) => {
          appendMessages([msg]);
          setInput("");
          showFakeTyping();
          loadRecent();
          loadUnread();
        })
        .catch((err) => setError(err.message || "Failed to send"))
        .finally(() => setSending(false));
    } else {
      setInput("");
      showFakeTyping();
      loadRecent();
      loadUnread();
      setSending(false);
    }
  };

  const handleSearch = useCallback((query) => {
    setSearchQuery(query);
    if (searchTimerRef.current) clearTimeout(searchTimerRef.current);
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    searchTimerRef.current = setTimeout(async () => {
      try {
        const data = await chatApi.search(room.type, room.id || undefined, query);
        setSearchResults(data.results || []);
      } catch {
        setSearchResults([]);
      }
    }, 300);
  }, [room]);

  const handleMarkRead = useCallback(async () => {
    try {
      await chatApi.markRead(room.type, room.id || undefined);
      loadUnread();
    } catch {
      // ignore
    }
  }, [room, loadUnread]);

  const handleLeaveRoom = useCallback(async () => {
    try {
      await chatApi.leaveRoom(room.type, room.id || undefined);
      setRoom({ type: "global", id: "" });
      setRoomStats(null);
      setRoomMembers([]);
      setTab("global");
    } catch (e) {
      setError(e.message || "Failed to leave room");
    }
  }, [room]);

  const handleLoadRoomStats = useCallback(async () => {
    try {
      const data = await chatApi.messageStats(room.type, room.id || undefined);
      setRoomStats(data);
    } catch {
      setRoomStats(null);
    }
  }, [room]);

  const handleLoadRoomMembers = useCallback(async () => {
    try {
      const data = await chatApi.roomMembers(room.type, room.id || undefined);
      setRoomMembers(data.members || []);
      setShowMembers(true);
    } catch {
      setRoomMembers([]);
    }
  }, [room]);

  const peerName = (id) => {
    const p = peers.find((x) => x.user_id === id);
    return p ? p.name : null;
  };

  const ownId = user?.id;

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="mx-auto max-w-4xl px-4 py-6">
        <header className="mb-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">💬 Chat</h1>
            <p className="text-sm text-text-muted">Real-time rooms — messages expire after 7 days</p>
          </div>
          <div className="flex items-center gap-3">
            {totalUnread > 0 && (
              <span className="rounded-full bg-red-600 px-2 py-0.5 text-xs font-bold text-white">
                {totalUnread} unread
              </span>
            )}
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="rounded-lg bg-white border border-nature-leaf/20 px-3 py-1.5 text-sm text-text-secondary hover:bg-surface-card"
              title="Search messages"
            >
              🔍 Search
            </button>
            <button
              onClick={() => setShowRoomInfo(!showRoomInfo)}
              className="rounded-lg bg-white border border-nature-leaf/20 px-3 py-1.5 text-sm text-text-secondary hover:bg-surface-card"
              title="Room info"
            >
              ℹ️ Info
            </button>
          </div>
        </header>

        {/* Search bar */}
        {showSearch && (
          <div className="mb-3 rounded-xl border border-nature-leaf/20 bg-white p-3">
            <input
              type="text"
              placeholder="Search messages..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              className="w-full rounded-lg bg-white border border-nature-leaf/20 px-3 py-2 text-sm outline-none ring-[#4F8F57] focus:ring-2 text-text-primary placeholder-text-muted"
            />
            {searchResults.length > 0 && (
              <div className="mt-2 max-h-40 overflow-y-auto space-y-1">
                {searchResults.map((m) => (
                  <div key={m.id} className="rounded-lg bg-surface-card px-3 py-2 text-sm">
                    <span className="text-nature-blossom text-xs">{m.name}</span>
                    <span className="text-text-muted text-xs ml-2">{formatTime(m.created_at)}</span>
                    <p className="text-text-secondary mt-1">{m.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Room info panel */}
        {showRoomInfo && room && (
          <div className="mb-3 rounded-xl border border-nature-leaf/20 bg-white p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-sm">Room Info</h3>
              <button onClick={() => setShowRoomInfo(false)} className="text-text-muted hover:text-text-secondary text-sm">✕</button>
            </div>
            <div className="flex gap-3 mb-3">
              <button onClick={handleLoadRoomStats} className="px-3 py-1.5 bg-nature-leaf text-white rounded-lg text-xs font-medium hover:bg-nature-moss">
                Load Stats
              </button>
              <button onClick={handleLoadRoomMembers} className="px-3 py-1.5 bg-nature-leaf text-white rounded-lg text-xs font-medium hover:bg-nature-moss">
                Members
              </button>
              <button onClick={handleMarkRead} className="px-3 py-1.5 bg-green-600 text-white rounded-lg text-xs font-medium hover:bg-green-700">
                Mark Read
              </button>
              {room.type !== "global" && (
                <button onClick={handleLeaveRoom} className="px-3 py-1.5 bg-red-600 text-white rounded-lg text-xs font-medium hover:bg-red-700">
                  Leave
                </button>
              )}
            </div>
            {roomStats && (
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-text-muted">Total messages</span><span className="font-semibold">{roomStats.total_messages}</span></div>
                <div className="flex justify-between"><span className="text-text-muted">First message</span><span className="text-text-secondary">{roomStats.first_message ? formatTime(roomStats.first_message.created_at) : "—"}</span></div>
                <div className="flex justify-between"><span className="text-text-muted">Last message</span><span className="text-text-secondary">{roomStats.last_message ? formatTime(roomStats.last_message.created_at) : "—"}</span></div>
                {roomStats.top_senders.length > 0 && (
                  <div>
                    <div className="text-text-muted mb-1">Top senders</div>
                    {roomStats.top_senders.map((s, i) => (
                      <div key={s.user_id} className="flex justify-between text-xs">
                        <span className="text-text-secondary">#{i + 1}</span>
                        <span className="text-nature-blossom">{s.message_count} msgs</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
            {showMembers && roomMembers.length > 0 && (
              <div className="mt-3 space-y-1">
                <div className="text-text-muted text-xs mb-1">Members ({roomMembers.length})</div>
                {roomMembers.map((m) => (
                  <div key={m.user_id} className="flex justify-between text-xs">
                    <span className="text-text-secondary">{m.name}</span>
                    <span className="text-text-muted">{m.message_count} msgs</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Room switcher tabs */}
        <div className="mb-3 flex flex-wrap gap-2">
          {TABS.map((t) => (
            <button
              key={t.key}
              onClick={() => switchTab(t.key)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
                tab === t.key
                  ? "bg-nature-leaf text-white shadow"
                  : "bg-white text-text-secondary hover:bg-surface-card border border-nature-leaf/20"
              }`}
            >
              {t.label}
              {unreadCounts[`${t.key}:`] > 0 && (
                <span className="ml-1 rounded-full bg-red-600 px-1.5 py-0.5 text-xs text-white">
                  {unreadCounts[`${t.key}:`]}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Recent rooms strip */}
        {recentRooms.length > 0 && (
          <div className="mb-4 flex gap-2 overflow-x-auto pb-1">
            {recentRooms.map((r) => (
              <button
                key={`${r.room_type}:${r.room_id}`}
                onClick={() => openRecentRoom(r)}
                className={`shrink-0 rounded-lg border px-3 py-1.5 text-xs transition ${
                  roomKey === `${r.room_type}:${r.room_id || ""}`
                    ? "border-[#4F8F57] bg-nature-bark text-nature-blossom"
                    : "border-nature-leaf/20 bg-white text-text-secondary hover:border-[#4F8F57]"
                }`}
              >
                {roomLabel(r.room_type, r.room_id)}
                {unreadCounts[`${r.room_type}:${r.room_id || ""}`] > 0 && (
                  <span className="ml-1 rounded-full bg-red-600 px-1 py-0.5 text-xs text-white">
                    {unreadCounts[`${r.room_type}:${r.room_id || ""}`]}
                  </span>
                )}
              </button>
            ))}
          </div>
        )}

        {/* Room config panels */}
        {tab !== "global" && !room && (
          <div className="mb-4 rounded-2xl border border-nature-leaf/20 bg-white p-4">
            {tab === "guild" && (
              <div className="flex flex-col gap-2">
                <p className="text-sm text-text-muted">Open a guild room with its guild id.</p>
                <div className="flex gap-2">
                  <input
                    value={guildId}
                    onChange={(e) => setGuildId(e.target.value)}
                    placeholder="Guild ID"
                    className="flex-1 rounded-lg bg-white border border-nature-leaf/20 px-3 py-2 text-sm outline-none ring-[#4F8F57] focus:ring-2"
                  />
                  <button onClick={() => joinRoom("guild", guildId)} className="rounded-lg bg-nature-leaf px-4 py-2 text-sm font-medium hover:bg-nature-moss">
                    Open
                  </button>
                </div>
              </div>
            )}
            {tab === "college" && (
              <div className="flex flex-col gap-2">
                <p className="text-sm text-text-muted">Open your college room (must have joined a college).</p>
                <div className="flex gap-2">
                  <input
                    value={college}
                    onChange={(e) => setCollege(e.target.value)}
                    placeholder="College name"
                    className="flex-1 rounded-lg bg-white border border-nature-leaf/20 px-3 py-2 text-sm outline-none ring-[#4F8F57] focus:ring-2"
                  />
                  <button onClick={() => joinRoom("college", college)} className="rounded-lg bg-nature-leaf px-4 py-2 text-sm font-medium hover:bg-nature-moss">
                    Open
                  </button>
                </div>
              </div>
            )}
            {tab === "dm" && (
              <div className="flex flex-col gap-3">
                {/* Your UID section */}
                {myUid ? (
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">Your chat ID:</span>
                    <span className="monospace bg-white/80 px-2 py-1 rounded text-sm">{myUid}</span>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(myUid);
                        setMyUidCopied(true);
                        setTimeout(() => setMyUidCopied(false), 2000);
                      }}
                      className="px-2 py-1 text-xs text-blue-600 hover underline"
                    >
                      Copy
                    </button>
                  </div>
                ) : (
                  <p className="text-sm text-text-muted">Generating your chat ID…</p>
                )}

                {/* Friends list */}
                {friends.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-text-muted">Friends ({friends.length})</p>
                    <div className="grid grid-cols-2 gap-2">
                      {friends.map((f) => (
                        <button
                          key={f.friend_id}
                          className="px-2 py-1 rounded text-xs text-blue-600 underline hover"
                          onClick={() => joinRoom("dm", f.friend_id)}
                        >
                          {f.name}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Received requests */}
                {(received.length > 0 || sent.length > 0) && (
                  <div>
                    <p className="text-xs font-medium text-text-muted">Requests</p>
                    <div className="space-y-2">
                      {received.map((req) => (
                        <div
                          key={req.id}
                          className="p-2 rounded bg-white/80 border border-white/60"
                        >
                          <span className="font-medium text-primary">
                            {req.from_name}</span> invited you
                          <div className="flex gap-2 mt-1">
                            <button
                              onClick={() => acceptRequest(req.id)}
                              className="px-2 py-1 rounded bg-green-500 text-white text-xs"
                            >
                              Accept
                            </button>
                            <button
                              onClick={() => declineRequest(req.id)}
                              className="px-2 py-1 rounded border border-red-500 text-red-600 text-xs"
                            >
                              Decline
                            </button>
                          </div>
                        </div>
                      ))}
                      {sent.map((req) => (
                        <div
                          key={req.id}
                          className="p-2 rounded bg-white/50 text-xs"
                        >
                          <span className="font-medium">Invited {req.to_name}</span> — {req.status}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Add by UID */}
                <div>
                  <p className="text-xs font-medium text-text-muted">Add by Chat ID</p>
                  <div className="flex gap-2 mt-1">
                    <input
                      value={newUidInput}
                      onChange={(e) => setNewUidInput(e.target.value)}
                      placeholder="UID_XXXXXX"
                      className="flex-1 rounded-lg bg-white border border-nature-leaf/20 px-3 py-2 text-sm outline-none ring-[#4F8F57] focus:ring-2"
                    />
                    <button
                      onClick={() => {
                        if (!/^UID_[A-Z2-9]{6}$/i.test(newUidInput)) {
                          setError("Invalid UID format");
                          return;
                        }
                        setAddingFriend(true);
                        friendsApi
                          .request(newUidInput)
                          .then(() => {
                            setError("");
                            setNewUidInput("");
                            setAddingFriend(false);
                            friendsApi.overview().then((ov: any) => {
                              setFriends(ov.friends || []);
                              setReceived(ov.received || []);
                              setSent(ov.sent || []);
                            });
                          })
                          .catch((e: any) => {
                            setError(e.message || "Failed to send request");
                            setAddingFriend(false);
                          });
                      }}
                      disabled={addingFriend}
                      className="px-4 py-2 rounded-lg bg-nature-leaf text-white text-sm font-medium hover:bg-nature-moss disabled:opacity-50"
                    >
                      {addingFriend ? "Sending…" : "Add"}
                    </button>
                    {error && <span className="text-red-600 text-xs mt-1">{error}</span>}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error banner */}
        {error && (
          <div className="mb-3 rounded-xl border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-600">
            {error}
          </div>
        )}

        {/* Message list */}
        <div className="mb-4 flex h-[52vh] flex-col rounded-2xl border border-nature-leaf/20 bg-white">
          <div className="flex items-center justify-between border-b border-[#EDEAE0] px-4 py-3">
            <span className="text-sm font-semibold text-nature-blossom">
              {room && room.type === "dm" && peerName(room.id)
                ? "DM with " + peerName(room.id)
                : room
                  ? roomLabel(room.type, room.id)
                  : "Select a room"}
            </span>
            <span className="text-xs text-text-muted">
              {!room
                ? "idle"
                : live
                  ? "live • websocket"
                  : "reconnecting • polling 3s"}
            </span>
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
            {messages.length === 0 ? (
              <div className="flex h-full items-center justify-center text-sm text-text-muted">
                {room ? "No messages yet. Say hello!" : "Open a room to start chatting."}
              </div>
            ) : (
              messages.map((m) => {
                const own = ownId && m.user_id === ownId;
                const name = m.name || (own ? "You" : "Anonymous");
                return (
                  <div key={m.id} className={`flex ${own ? "justify-end" : "justify-start"}`}>
                    <div
                      className={`max-w-[75%] rounded-xl px-4 py-2 shadow ${
                        own ? "bg-nature-leaf text-white" : "bg-white border border-nature-leaf/20 text-text-primary"
                      }`}
                    >
                      {!own && (
                        <div className={`text-xs font-medium ${own ? "" : "text-nature-blossom"}`}>{name}</div>
                      )}
                      {m.emoji && <div className="py-1 text-4xl leading-none">{m.emoji}</div>}
                      {m.text && <div className="whitespace-pre-wrap break-words text-sm">{m.text}</div>}
                      <div className={`mt-1 text-right text-xs ${own ? "text-white/80" : "text-text-muted"}`}>
                        {formatTime(m.created_at)}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
            {typing && (
              <div className="flex justify-start">
                <div className="flex items-center gap-1 rounded-2xl bg-white border border-nature-leaf/20 px-4 py-3">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#9CA3AF]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#9CA3AF] [animation-delay:150ms]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-[#9CA3AF] [animation-delay:300ms]" />
                </div>
              </div>
            )}
            <div ref={listEndRef} />
          </div>
        </div>

        {/* Emoji picker + input bar */}
        <div className="rounded-2xl border border-nature-leaf/20 bg-white p-3">
          {emoji && (
            <div className="mb-2 flex items-center gap-2">
              <span className="text-xs text-text-muted">Attached:</span>
              <span className="rounded-lg bg-surface-card border border-nature-leaf/20 px-2 py-1 text-2xl leading-none">{emoji}</span>
              <button onClick={() => setEmoji("")} className="text-xs text-text-muted hover:text-red-500">
                remove
              </button>
            </div>
          )}
          <div className="mb-2 flex flex-wrap items-center gap-1">
            {emojis.reactions.map((e) => (
              <button
                key={e}
                onClick={() => pickEmoji(e)}
                title={emoji === e ? "Selected - click again to remove" : "Attach emoji"}
                className={`rounded-lg p-1.5 text-xl leading-none transition ${
                  emoji === e ? "bg-nature-bark ring-1 ring-[#4F8F57]" : "hover:bg-surface-card"
                }`}
              >
                {e}
              </button>
            ))}
            {emojis.emojis.length > 0 && (
              <button
                onClick={() => setShowAllEmojis((s) => !s)}
                className="ml-1 rounded-lg border border-nature-leaf/20 px-2 py-1 text-xs text-text-muted hover:text-text-secondary"
              >
                {showAllEmojis ? "less" : "+more"}
              </button>
            )}
          </div>
          {showAllEmojis && emojis.emojis.length > 0 && (
            <div className="mb-2 flex flex-wrap gap-1">
              {emojis.emojis.map((e) => (
                <button
                  key={e}
                  onClick={() => sendEmojiOnly(e)}
                  title="Send emoji"
                  className="rounded-lg p-1.5 text-2xl leading-none transition hover:bg-surface-card"
                >
                  {e}
                </button>
              ))}
            </div>
          )}
          <div className="flex items-end gap-2">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              onFocus={showFakeTyping}
              rows={1}
              placeholder="Type a message..."
              maxLength={500}
              className="max-h-32 flex-1 resize-none rounded-xl bg-white border border-nature-leaf/20 px-3 py-2 text-sm text-text-primary placeholder-text-muted outline-none ring-[#4F8F57] focus:ring-2"
            />
            <button
              onClick={handleSend}
              disabled={(!input.trim() && !emoji) || !room || sending}
              className="rounded-xl bg-nature-leaf px-4 py-2 text-sm font-semibold text-white transition hover:bg-nature-moss disabled:cursor-not-allowed disabled:opacity-40"
            >
              {sending ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}