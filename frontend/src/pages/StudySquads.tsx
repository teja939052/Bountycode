import { useState, useEffect, useCallback } from "react";
import { studySquadsApi } from "../services/api/studySquads.ts";
import {
  Users, Heart, Target, Code2, Clock, MessageSquare, Loader2,
  Send, Check, X, Sparkles, UserPlus,
} from "lucide-react";

export default function StudySquads() {
  const [options, setOptions] = useState({ goals: [], topics: [], languages: [], availabilities: [] });
  const [me, setMe] = useState(null);
  const [matches, setMatches] = useState([]);
  const [invites, setInvites] = useState({ received: [], sent: [] });
  const [squads, setSquads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [profile, setProfile] = useState({ goals: [], topics: [], languages: [], availability: "flexible", bio: "" });
  const [saving, setSaving] = useState(false);

  const [activeSquad, setActiveSquad] = useState(null);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);

  const loadAll = useCallback(async () => {
    setLoading(true);
    try {
      const [opts, my, inv, sq] = await Promise.all([
        studySquadsApi.goals(),
        studySquadsApi.me(),
        studySquadsApi.invites(),
        studySquadsApi.squads(),
      ]);
      setOptions(opts);
      setMe(my);
      if (my) {
        setProfile({
          goals: my.goals || [],
          topics: my.topics || [],
          languages: my.languages || [],
          availability: my.availability || "flexible",
          bio: my.bio || "",
        });
      }
      setInvites(inv);
      setSquads(sq.squads || []);
      if (!activeSquad && sq.squads?.length > 0) setActiveSquad(sq.squads[0]);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, [activeSquad]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const refreshMatches = useCallback(async () => {
    try {
      const res = await studySquadsApi.match(6);
      setMatches(res.matches || []);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    if (me) refreshMatches();
  }, [me, refreshMatches]);

  useEffect(() => {
    if (activeSquad) {
      studySquadsApi.messages(activeSquad.id).then((res) => setMessages(res.messages || [])).catch(() => {});
    }
  }, [activeSquad]);

  const toggle = (arr, value) =>
    arr.includes(value) ? arr.filter((v) => v !== value) : [...arr, value];

  const handleSaveProfile = async () => {
    setSaving(true);
    setError("");
    try {
      await studySquadsApi.profile(profile);
      setMe(profile);
      refreshMatches();
    } catch (e) {
      setError(e.message || "Could not save profile");
    } finally {
      setSaving(false);
    }
  };

  const handleInvite = async (userId) => {
    setError("");
    try {
      await studySquadsApi.invite(userId);
      const inv = await studySquadsApi.invites();
      setInvites(inv);
    } catch (e) {
      setError(e.message || "Could not send invite");
    }
  };

  const handleInviteAction = async (id, accept) => {
    try {
      if (accept) await studySquadsApi.acceptInvite(id);
      else await studySquadsApi.declineInvite(id);
      const [inv, sq] = await Promise.all([studySquadsApi.invites(), studySquadsApi.squads()]);
      setInvites(inv);
      setSquads(sq.squads || []);
      if (!activeSquad && sq.squads?.length > 0) setActiveSquad(sq.squads[0]);
    } catch {
      // ignore
    }
  };

  const handleSend = async () => {
    if (!activeSquad || !draft.trim()) return;
    setSending(true);
    try {
      await studySquadsApi.postMessage(activeSquad.id, draft.trim());
      setDraft("");
      const res = await studySquadsApi.messages(activeSquad.id);
      setMessages(res.messages || []);
    } catch (e) {
      setError(e.message || "Could not send message");
    } finally {
      setSending(false);
    }
  };

  const Chip = ({ label, active, onClick }) => (
    <button
      onClick={onClick}
      className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
        active ? "bg-brand-sky text-white" : "bg-white/70 border border-white/70 text-text-light hover:text-text-primary"
      }`}
    >
      {label}
    </button>
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
          <Users className="text-brand-coral" size={32} />
          Study Squads
        </h1>
        <p className="text-text-light mt-1">Find study partners who match your goals, topics and schedule</p>
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 size={28} className="animate-spin text-brand-sky" /></div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Profile setup */}
          <div className="p-6 rounded-2xl border border-white/60 bg-white/80 space-y-4 h-fit">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <Target size={18} className="text-brand-sky" /> Your Squad Profile
            </h2>

            <div>
              <div className="text-xs font-semibold text-text-light mb-2 flex items-center gap-1">
                <Target size={12} /> Goals
              </div>
              <div className="flex flex-wrap gap-1.5">
                {options.goals.map((g) => (
                  <Chip key={g} label={g} active={profile.goals.includes(g)} onClick={() => setProfile({ ...profile, goals: toggle(profile.goals, g) })} />
                ))}
              </div>
            </div>

            <div>
              <div className="text-xs font-semibold text-text-light mb-2 flex items-center gap-1">
                <Code2 size={12} /> Topics
              </div>
              <div className="flex flex-wrap gap-1.5">
                {options.topics.map((t) => (
                  <Chip key={t} label={t} active={profile.topics.includes(t)} onClick={() => setProfile({ ...profile, topics: toggle(profile.topics, t) })} />
                ))}
              </div>
            </div>

            <div>
              <div className="text-xs font-semibold text-text-light mb-2 flex items-center gap-1">
                <Code2 size={12} /> Languages
              </div>
              <div className="flex flex-wrap gap-1.5">
                {options.languages.map((l) => (
                  <Chip key={l} label={l} active={profile.languages.includes(l)} onClick={() => setProfile({ ...profile, languages: toggle(profile.languages, l) })} />
                ))}
              </div>
            </div>

            <div>
              <div className="text-xs font-semibold text-text-light mb-2 flex items-center gap-1">
                <Clock size={12} /> Availability
              </div>
              <select
                value={profile.availability}
                onChange={(e) => setProfile({ ...profile, availability: e.target.value })}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              >
                {options.availabilities.map((a) => <option key={a} value={a}>{a}</option>)}
              </select>
            </div>

            <textarea
              value={profile.bio}
              onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
              placeholder="Short bio — what you're preparing for…"
              rows={2}
              className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm resize-none"
            />

            <button onClick={handleSaveProfile} disabled={saving} className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50">
              {saving ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />} Save & Re-match
            </button>
          </div>

          <div className="lg:col-span-2 space-y-6">
            {/* Matches */}
            <div>
              <h2 className="text-lg font-bold text-text-primary mb-3 flex items-center gap-2">
                <Heart size={18} className="text-brand-lavender" /> Top Matches
                <span className="text-xs font-normal text-text-light">by tag + schedule overlap</span>
              </h2>
              {!me ? (
                <div className="p-6 rounded-2xl border border-white/60 bg-white/80 text-text-light text-sm">
                  Fill in your profile on the left to see compatible study partners.
                </div>
              ) : matches.length === 0 ? (
                <div className="p-6 rounded-2xl border border-white/60 bg-white/80 text-text-light text-sm">
                  No matches yet — try adding more goals and topics.
                </div>
              ) : (
                <div className="grid md:grid-cols-2 gap-3">
                  {matches.map((m) => (
                    <div key={m.user_id} className="p-4 rounded-2xl border border-white/60 bg-white/80">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <div className="font-semibold text-text-primary">{m.user_name}</div>
                          <div className="text-[11px] text-text-light">{m.availability}</div>
                        </div>
                        <span className="px-2 py-1 rounded-lg text-xs font-bold bg-brand-lavender/20 text-brand-lavender">
                          {m.compat.score} pts
                        </span>
                      </div>
                      {m.bio && <p className="text-xs text-text-secondary mb-2 line-clamp-2">{m.bio}</p>}
                      <div className="flex flex-wrap gap-1 mb-3">
                        {m.compat.goals_overlap > 0 && <span className="text-[10px] px-1.5 py-0.5 rounded bg-sky-50 text-sky-700">🎯 {m.compat.goals_overlap} goals</span>}
                        {m.compat.topics_overlap > 0 && <span className="text-[10px] px-1.5 py-0.5 rounded bg-violet-50 text-violet-700">📚 {m.compat.topics_overlap} topics</span>}
                        {m.compat.languages_overlap > 0 && <span className="text-[10px] px-1.5 py-0.5 rounded bg-green-50 text-green-700">💻 {m.compat.languages_overlap} langs</span>}
                        {m.compat.availability_match && <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-700">🕐 same schedule</span>}
                      </div>
                      <button
                        onClick={() => handleInvite(m.user_id)}
                        disabled={invites.sent.some((i) => i.to_id === m.user_id)}
                        className="w-full py-2 rounded-xl border border-brand-sky text-brand-sky text-sm font-semibold hover:bg-brand-sky hover:text-white transition-colors disabled:opacity-50"
                      >
                        <UserPlus size={15} className="inline mr-1" />
                        {invites.sent.some((i) => i.to_id === m.user_id) ? "Invited" : "Invite to Squad"}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Invites */}
            {(invites.received.length > 0 || invites.sent.length > 0) && (
              <div>
                <h2 className="text-lg font-bold text-text-primary mb-3 flex items-center gap-2">
                  <MessageSquare size={18} className="text-brand-coral" /> Invites
                </h2>
                <div className="space-y-2">
                  {invites.received.map((i) => (
                    <div key={i.id} className="p-3 rounded-xl border border-white/60 bg-white/80 flex items-center justify-between">
                      <div>
                        <span className="font-medium text-text-primary">{i.from_name}</span>{" "}
                        <span className="text-xs text-text-light">invited you</span>
                        <span className="ml-2 text-[10px] uppercase tracking-wide font-semibold text-amber-600">{i.status}</span>
                      </div>
                      {i.status === "pending" && (
                        <div className="flex gap-2">
                          <button onClick={() => handleInviteAction(i.id, true)} className="px-3 py-1.5 rounded-lg bg-green-500 text-white text-xs font-semibold flex items-center gap-1">
                            <Check size={13} /> Accept
                          </button>
                          <button onClick={() => handleInviteAction(i.id, false)} className="px-3 py-1.5 rounded-lg border border-red-200 text-red-600 text-xs font-semibold flex items-center gap-1">
                            <X size={13} /> Decline
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                  {invites.sent.map((i) => (
                    <div key={i.id} className="p-3 rounded-xl border border-white/60 bg-white/50 flex items-center justify-between">
                      <span className="text-sm text-text-primary">Invited <span className="font-medium">{i.to_name}</span></span>
                      <span className={`text-[10px] uppercase tracking-wide font-semibold ${i.status === "accepted" ? "text-green-600" : i.status === "declined" ? "text-red-500" : "text-amber-600"}`}>
                        {i.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Squads */}
            {squads.length > 0 && (
              <div>
                <h2 className="text-lg font-bold text-text-primary mb-3 flex items-center gap-2">
                  <Users size={18} className="text-brand-sky" /> Your Squads
                </h2>
                <div className="flex flex-wrap gap-2 mb-3">
                  {squads.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setActiveSquad(s)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold ${
                        activeSquad?.id === s.id ? "bg-brand-sky text-white" : "bg-white/80 border border-white/60 text-text-light"
                      }`}
                    >
                      {s.name}
                    </button>
                  ))}
                </div>
                {activeSquad && (
                  <div className="p-4 rounded-2xl border border-white/60 bg-white/80">
                    <div className="h-56 overflow-y-auto space-y-2 mb-3">
                      {messages.length === 0 ? (
                        <div className="text-center py-8 text-text-light text-sm">No messages yet — say hi!</div>
                      ) : (
                        messages.map((m) => (
                          <div key={m.id} className="p-2.5 rounded-xl bg-white/70 border border-white/70">
                            <div className="text-[11px] font-semibold text-brand-sky">{m.user_name}</div>
                            <div className="text-sm text-text-primary">{m.text}</div>
                          </div>
                        ))
                      )}
                    </div>
                    <div className="flex gap-2">
                      <input
                        value={draft}
                        onChange={(e) => setDraft(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        placeholder="Message your squad…"
                        className="flex-1 p-2.5 rounded-xl border border-white/60 bg-white text-sm"
                      />
                      <button onClick={handleSend} disabled={sending || !draft.trim()} className="px-4 rounded-xl bg-brand-sky text-white text-sm font-semibold flex items-center gap-1 disabled:opacity-50">
                        {sending ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />} Send
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
