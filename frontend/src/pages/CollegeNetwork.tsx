import { useState, useEffect, useCallback } from "react";
import { collegeNetworkApi } from "../services/api/collegeNetwork.ts";

const BRANCHES = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Chemical", "Biotech", "MCA", "MBA"];
const YEARS = ["1", "2", "3", "4", "5"];

export default function CollegeNetwork() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("leaderboard");
  const [college, setCollege] = useState("");
  const [branch, setBranch] = useState("");
  const [year, setYear] = useState("");
  const [leaderboard, setLeaderboard] = useState([]);
  const [peers, setPeers] = useState([]);
  const [feed, setFeed] = useState([]);
  const [cell, setCell] = useState(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const loadProfile = useCallback(async () => {
    setLoading(true);
    try {
      const data = await collegeNetworkApi.profile();
      setProfile(data.profile);
      if (data.profile) {
        setCollege(data.profile.college || "");
        setBranch(data.profile.branch || "");
        setYear(data.profile.year || "");
      }
    } catch (e) {
      setProfile(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadAll = useCallback(async (col) => {
    try {
      const [lb, pd, fd, cl] = await Promise.all([
        collegeNetworkApi.leaderboard(col),
        collegeNetworkApi.sameBatch(),
        collegeNetworkApi.feed(col),
        collegeNetworkApi.cell(),
      ]);
      setLeaderboard(lb.leaderboard || []);
      setPeers(pd.peers || []);
      setFeed(fd.events || []);
      setCell(cl);
    } catch (e) {
      // ignore partial failures
    }
  }, []);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  useEffect(() => {
    if (profile) loadAll(profile.college);
  }, [profile, loadAll]);

  const join = async () => {
    setSaving(true);
    setError("");
    try {
      const data = await collegeNetworkApi.join({ college, branch, year });
      setProfile(data.profile);
      setCollege(data.profile.college);
      setBranch(data.profile.branch);
      setYear(data.profile.year);
      await loadAll(data.profile.college);
    } catch (e) {
      setError(e.message || "Could not join college");
    } finally {
      setSaving(false);
    }
  };

  const statCard = (label, value) => (
    <div className="bg-white border border-nature-leaf/20 rounded-xl p-4 text-center">
      <div className="text-2xl font-bold text-nature-blossom">{value}</div>
      <div className="text-xs text-text-muted uppercase tracking-wide mt-1">{label}</div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center">
        <div className="text-text-muted animate-pulse">Connecting to your college...</div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-bold text-center mb-1">Join Your College</h1>
          <p className="text-text-muted text-center mb-8">Compete with your college, branch and batch. Bring your friends.</p>
          <div className="bg-white border border-nature-leaf/20 rounded-2xl p-6 space-y-4">
            <div>
              <label className="text-xs text-text-muted uppercase">College</label>
              <input
                value={college}
                onChange={(e) => setCollege(e.target.value)}
                placeholder="e.g. VIT Vellore"
                className="mt-1 w-full bg-surface-card rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="text-xs text-text-muted uppercase">Branch</label>
              <select
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="mt-1 w-full bg-surface-card rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Select branch</option>
                {BRANCHES.map((b) => <option key={b} value={b}>{b}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-text-muted uppercase">Year</label>
              <select
                value={year}
                onChange={(e) => setYear(e.target.value)}
                className="mt-1 w-full bg-surface-card rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Select year</option>
                {YEARS.map((y) => <option key={y} value={y}>Year {y}</option>)}
              </select>
            </div>
            {error && <p className="text-red-400 text-sm">{error}</p>}
            <button
              onClick={join}
              disabled={saving || !college || !branch || !year}
              className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-text-primary font-semibold rounded-lg py-3 transition"
            >
              {saving ? "Joining..." : "Join My College"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: "leaderboard", label: "Leaderboard" },
    { id: "peers", label: "Same Batch" },
    { id: "feed", label: "Campus Feed" },
    { id: "cell", label: "Placement Cell" },
  ];

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">{profile.college}</h1>
            <p className="text-text-muted">
              {profile.branch} · Year {profile.year}
            </p>
          </div>
          <div className="flex gap-3 mt-4 md:mt-0">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  tab === t.id ? "bg-emerald-600 text-text-primary" : "bg-surface-card text-text-secondary hover:bg-[#EDEAE0]"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {cell && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {statCard("Students", cell.total_students || 0)}
            {statCard("Avg XP", cell.avg_xp || 0)}
            {statCard("Offers", cell.offers_count || 0)}
            {statCard("Top Student", cell.top_student?.name || "—")}
          </div>
        )}

        {tab === "leaderboard" && (
          <div className="bg-white border border-nature-leaf/20 rounded-2xl overflow-hidden">
            <div className="px-6 py-3 grid grid-cols-12 text-xs text-text-muted uppercase tracking-wide border-b border-[#EDEAE0]">
              <div className="col-span-1">#</div>
              <div className="col-span-5">Student</div>
              <div className="col-span-2">Branch</div>
              <div className="col-span-2">Year</div>
              <div className="col-span-2 text-right">XP</div>
            </div>
            {leaderboard.map((s) => (
              <div key={s.user_id} className={`px-6 py-3 grid grid-cols-12 items-center border-b border-[#EDEAE0] ${s.is_me ? "bg-surface-card" : ""}`}>
                <div className="col-span-1 font-bold text-text-muted">{s.rank}</div>
                <div className="col-span-5">
                  {s.name} {s.is_me && <span className="text-nature-blossom text-xs">(you)</span>}
                </div>
                <div className="col-span-2 text-text-muted text-sm">{s.branch}</div>
                <div className="col-span-2 text-text-muted text-sm">Y{s.year}</div>
                <div className="col-span-2 text-right font-semibold text-nature-blossom">{s.xp.toLocaleString()}</div>
              </div>
            ))}
            {!leaderboard.length && <div className="px-6 py-10 text-center text-text-muted">No students yet — invite your batch!</div>}
          </div>
        )}

        {tab === "peers" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {peers.map((p) => (
              <div key={p.user_id} className="bg-white border border-nature-leaf/20 rounded-xl p-4">
                <div className="font-semibold">{p.name}</div>
                <div className="text-sm text-text-muted">{p.branch} · Y{p.year}</div>
                <div className="text-nature-blossom font-semibold mt-2">{p.xp.toLocaleString()} XP</div>
              </div>
            ))}
            {!peers.length && <div className="col-span-full text-center text-text-muted py-10">No batchmates yet. Share the link!</div>}
          </div>
        )}

        {tab === "feed" && (
          <div className="space-y-3">
            {feed.map((e) => (
              <div key={e.id} className="bg-white border border-nature-leaf/20 rounded-xl px-5 py-4">
                <div className="flex items-center justify-between">
                  <span className="font-semibold">{e.name}</span>
                  <span className="text-xs text-text-muted">{e.created_at ? new Date(e.created_at).toLocaleDateString() : ""}</span>
                </div>
                <p className="text-text-secondary text-sm mt-1">{e.text}</p>
              </div>
            ))}
            {!feed.length && <div className="text-center text-text-muted py-10">The campus feed is quiet — be the first story.</div>}
          </div>
        )}

        {tab === "cell" && cell && (
          <div className="bg-white border border-nature-leaf/20 rounded-2xl p-6">
            <h2 className="text-xl font-bold mb-1">Placement Cell Overview</h2>
            <p className="text-text-muted text-sm mb-6">Snapshot of your college on PlacementPro</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              {statCard("Students", cell.total_students || 0)}
              {statCard("Avg XP", cell.avg_xp || 0)}
              {statCard("Offers", cell.offers_count || 0)}
            </div>
            {cell.top_student && (
              <div className="bg-surface-card rounded-xl p-4 flex items-center justify-between">
                <div>
                  <div className="text-xs text-text-muted uppercase">Top Student</div>
                  <div className="font-bold text-lg">{cell.top_student.name}</div>
                </div>
                <div className="text-nature-blossom font-bold">{cell.top_student.xp.toLocaleString()} XP</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
