import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Users, UserPlus, Search, Check, X, Trash2 } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function FriendsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [lookupEmail, setLookupEmail] = useState("");
  const [lookupResult, setLookupResult] = useState<any>(null);

  const load = async () => {
    try {
      const d = await api.get("/api/v1/friends/overview");
      setData(d);
    } catch { }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const lookup = async () => {
    if (!lookupEmail.trim()) return;
    try {
      const r = await api.post("/api/v1/friends/lookup", { identifier: lookupEmail });
      setLookupResult(r);
    } catch { setLookupResult(null); }
  };

  const sendRequest = async (userId: string) => {
    try {
      await api.post("/api/v1/friends/request", { to_id: userId });
      load();
      setLookupResult(null);
      setLookupEmail("");
    } catch { }
  };

  const acceptRequest = async (id: string) => {
    await api.post(`/api/v1/friends/requests/${id}/accept`);
    load();
  };

  const declineRequest = async (id: string) => {
    await api.post(`/api/v1/friends/requests/${id}/decline`);
    load();
  };

  const removeFriend = async (friendId: string) => {
    await api.delete(`/api/v1/friends/${friendId}`);
    load();
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-teal/10 border border-brand-teal/20 mb-3">
          <Users size={14} className="text-brand-teal" />
          <span className="text-xs font-mono text-brand-teal">FRIENDS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Friends</h1>
        <p className="text-sm text-gray-500 mt-1">{data?.friends?.length || 0} friends</p>
      </motion.div>

      {/* Lookup */}
      <div className="glass rounded-xl p-4 mb-6">
        <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-2">Find a friend</p>
        <div className="flex gap-2">
          <input value={lookupEmail} onChange={e => setLookupEmail(e.target.value)} onKeyDown={e => e.key === "Enter" && lookup()}
            className="flex-1 px-3 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-sm text-gray-300 font-mono focus:outline-none focus:border-brand-teal/40"
            placeholder="Email or name..." />
          <button onClick={lookup} className="px-4 py-2 rounded-lg bg-brand-teal/20 text-brand-teal text-sm font-mono hover:bg-brand-teal/30 transition-all">
            <Search size={14} />
          </button>
        </div>
        {lookupResult && lookupResult.user_id && (
          <div className="mt-3 flex items-center gap-3 p-3 rounded-lg bg-white/[0.02]">
            <div className="w-8 h-8 rounded-full bg-white border-border shadow-card flex items-center justify-center text-xs font-mono text-gray-400">
              {(lookupResult.name || "?")[0]}
            </div>
            <span className="text-sm text-gray-300">{lookupResult.name}</span>
            <button onClick={() => sendRequest(lookupResult.user_id)} className="ml-auto px-3 py-1 rounded-lg bg-brand-teal/20 text-brand-teal text-xs font-mono">
              <UserPlus size={12} />
            </button>
          </div>
        )}
      </div>

      {/* Friend Requests */}
      {data?.received?.length > 0 && (
        <div className="glass rounded-xl p-4 mb-6">
          <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-3">Pending Requests</p>
          <div className="space-y-2">
            {data.received.map((r: any) => (
              <div key={r.id} className="flex items-center gap-3 p-2 rounded-lg bg-white/[0.02]">
                <div className="w-8 h-8 rounded-full bg-white border-border shadow-card flex items-center justify-center text-xs font-mono text-gray-400">
                  {(r.from_name || "?")[0]}
                </div>
                <span className="text-sm text-gray-300">{r.from_name}</span>
                <div className="ml-auto flex gap-1">
                  <button onClick={() => acceptRequest(r.id)} className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400"><Check size={12} /></button>
                  <button onClick={() => declineRequest(r.id)} className="p-1.5 rounded-lg bg-red-500/20 text-red-400"><X size={12} /></button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Friends List */}
      <div className="glass rounded-xl p-4">
        <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-3">Your Friends</p>
        <div className="space-y-2">
          {(data?.friends || []).map((f: any) => (
            <div key={f.friend_id} className="flex items-center gap-3 p-2 rounded-lg bg-white/[0.02]">
              <div className="w-8 h-8 rounded-full bg-brand-teal/10 flex items-center justify-center text-xs font-mono text-brand-teal">
                {(f.name || "?")[0]}
              </div>
              <div>
                <p className="text-sm text-gray-300">{f.name || "Anonymous"}</p>
                {f.uid && <p className="text-[10px] font-mono text-gray-600">@{f.uid}</p>}
              </div>
              <button onClick={() => removeFriend(f.friend_id)} className="ml-auto p-1.5 rounded-lg text-gray-600 hover:text-red-400 transition-colors">
                <Trash2 size={12} />
              </button>
            </div>
          ))}
          {(!data?.friends || data.friends.length === 0) && (
            <p className="text-sm text-gray-500 font-mono text-center py-6">No friends yet. Search above to find someone!</p>
          )}
        </div>
      </div>
    </div>
  );
}
