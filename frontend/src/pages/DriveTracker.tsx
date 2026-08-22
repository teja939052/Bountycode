import { useState, useEffect, useCallback } from "react";
import { driveApi } from "../services/api/driveTracker.ts";
import {
  Building2, Plus, Trash2, TrendingUp, Briefcase, CheckCircle,
  XCircle, Loader2, ClipboardList, UserCheck, FileCheck, Save,
} from "lucide-react";

const STAGE_COLORS = {
  applied: "bg-sky-100 text-sky-700",
  shortlisted: "bg-indigo-100 text-indigo-700",
  online_assessment: "bg-violet-100 text-violet-700",
  technical_interview: "bg-amber-100 text-amber-700",
  hr_interview: "bg-orange-100 text-orange-700",
  offer: "bg-green-100 text-green-700",
  joined: "bg-emerald-100 text-emerald-700",
  rejected: "bg-red-100 text-red-700",
};

const STAGE_LABELS = {
  applied: "Applied",
  shortlisted: "Shortlisted",
  online_assessment: "Online Assessment",
  technical_interview: "Technical Interview",
  hr_interview: "HR Interview",
  offer: "Offer",
  joined: "Joined",
  rejected: "Rejected",
};

const EMPTY_FORM = { company: "", role: "", location: "", package_lpa: "", stage: "applied", notes: "" };

export default function DriveTracker() {
  const [drives, setDrives] = useState([]);
  const [stages, setStages] = useState([]);
  const [stats, setStats] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [d, s, st] = await Promise.all([driveApi.list(), driveApi.stages(), driveApi.stats()]);
      setDrives(d.drives || []);
      setStages(s.stages || []);
      setStats(st);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleCreate = async () => {
    if (!form.company.trim()) return;
    setSaving(true);
    setError("");
    try {
      await driveApi.create({
        company: form.company,
        role: form.role,
        location: form.location,
        package_lpa: form.package_lpa ? Number(form.package_lpa) : null,
        stage: form.stage,
        notes: form.notes,
      });
      setForm(EMPTY_FORM);
      load();
    } catch (e) {
      setError(e.message || "Could not add drive");
    } finally {
      setSaving(false);
    }
  };

  const handleStageChange = async (id, stage) => {
    try {
      await driveApi.update(id, { stage });
      load();
    } catch {
      // ignore
    }
  };

  const handleReject = async (id) => {
    try {
      await driveApi.update(id, { stage: "rejected", status: "rejected" });
      load();
    } catch {
      // ignore
    }
  };

  const handleDelete = async (id) => {
    try {
      await driveApi.remove(id);
      load();
    } catch {
      // ignore
    }
  };

  const activeDrives = drives.filter((d) => d.status !== "rejected");

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <Building2 className="text-brand-coral" size={32} />
            Drive Outcome Tracker
          </h1>
          <p className="text-text-light mt-1">Track every placement drive from application to offer</p>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
          <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
            <div className="text-3xl font-extrabold text-text-primary">{stats.total}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Total Drives</div>
          </div>
          <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
            <div className="text-3xl font-extrabold text-brand-sky">{stats.active}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Active</div>
          </div>
          <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
            <div className="text-3xl font-extrabold text-green-600">{stats.offers}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Offers</div>
          </div>
          <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
            <div className="text-3xl font-extrabold text-emerald-600">{stats.joined}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Joined</div>
          </div>
          <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
            <div className="text-3xl font-extrabold text-brand-lavender">{stats.offer_rate}%</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Offer Rate</div>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Add drive */}
        <div className="p-6 rounded-2xl border border-white/60 bg-white/80 space-y-4 h-fit">
          <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
            <Plus size={18} className="text-brand-sky" /> Track New Drive
          </h2>
          <input
            value={form.company}
            onChange={(e) => setForm({ ...form, company: e.target.value })}
            placeholder="Company name *"
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
          />
          <input
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
            placeholder="Role (e.g. SDE)"
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
          />
          <input
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            placeholder="Location"
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
          />
          <input
            value={form.package_lpa}
            onChange={(e) => setForm({ ...form, package_lpa: e.target.value })}
            placeholder="Package (LPA, optional)"
            type="number"
            step="0.1"
            min="0"
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
          />
          <select
            value={form.stage}
            onChange={(e) => setForm({ ...form, stage: e.target.value })}
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
          >
            {stages.map((s) => <option key={s} value={s}>{STAGE_LABELS[s] || s}</option>)}
          </select>
          <textarea
            value={form.notes}
            onChange={(e) => setForm({ ...form, notes: e.target.value })}
            placeholder="Notes"
            rows={2}
            className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm resize-none"
          />
          <button onClick={handleCreate} disabled={saving || !form.company.trim()} className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50">
            {saving ? <Loader2 size={18} className="animate-spin" /> : <Save size={18} />} Add Drive
          </button>
        </div>

        {/* Drives list */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <ClipboardList size={18} className="text-brand-lavender" /> Your Drives
            </h2>
            <span className="text-xs text-text-light">{drives.length} tracked</span>
          </div>

          {loading ? (
            <div className="flex justify-center py-12"><Loader2 size={28} className="animate-spin text-brand-sky" /></div>
          ) : activeDrives.length === 0 && drives.filter((d) => d.status === "rejected").length === 0 ? (
            <div className="p-6 rounded-2xl border border-white/60 bg-white/80 text-text-light text-sm">
              No drives tracked yet. Add your first placement drive.
            </div>
          ) : (
            <>
              {activeDrives.map((d) => (
                <div key={d.id} className="p-4 rounded-2xl border border-white/60 bg-white/80">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <div className="font-semibold text-text-primary">{d.company}</div>
                      <div className="text-xs text-text-light">
                        {[d.role, d.location].filter(Boolean).join(" · ")}
                        {d.package_lpa ? ` · ₹${d.package_lpa} LPA` : ""}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${STAGE_COLORS[d.stage] || "bg-gray-100 text-gray-700"}`}>
                        {STAGE_LABELS[d.stage] || d.stage}
                      </span>
                      <button onClick={() => handleDelete(d.id)} className="text-text-light hover:text-red-500">
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <select
                      value={d.stage}
                      onChange={(e) => handleStageChange(d.id, e.target.value)}
                      className="flex-1 p-2 rounded-lg border border-white/60 bg-white text-sm"
                    >
                      {stages.map((s) => <option key={s} value={s}>{STAGE_LABELS[s] || s}</option>)}
                    </select>
                    <button
                      onClick={() => handleReject(d.id)}
                      className="px-3 py-2 rounded-lg border border-red-200 text-red-600 text-xs font-medium hover:bg-red-50"
                    >
                      Reject
                    </button>
                  </div>
                  {d.notes && <div className="mt-2 text-xs text-text-light">{d.notes}</div>}
                </div>
              ))}

              {drives.filter((d) => d.status === "rejected").length > 0 && (
                <>
                  <div className="pt-4 text-sm font-semibold text-text-light uppercase tracking-wide">Rejected</div>
                  {drives.filter((d) => d.status === "rejected").map((d) => (
                    <div key={d.id} className="p-3 rounded-xl border border-white/60 bg-white/50 flex items-center justify-between">
                      <div>
                        <div className="text-sm font-medium text-text-primary flex items-center gap-2">
                          <XCircle size={14} className="text-red-400" /> {d.company}
                        </div>
                        <div className="text-[11px] text-text-light">{d.role || "—"}</div>
                      </div>
                      <button onClick={() => handleDelete(d.id)} className="text-text-light hover:text-red-500">
                        <Trash2 size={14} />
                      </button>
                    </div>
                  ))}
                </>
              )}
            </>
          )}

          {/* Funnel */}
          {stats && stats.funnel?.length > 0 && (
            <div className="mt-4 p-5 rounded-2xl border border-white/60 bg-white/80">
              <h3 className="text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
                <TrendingUp size={16} /> Funnel
              </h3>
              <div className="space-y-2">
                {stats.funnel.map((f) => (
                  <div key={f.stage} className="flex items-center gap-2">
                    <span className="w-36 text-xs text-text-light shrink-0">{STAGE_LABELS[f.stage] || f.stage}</span>
                    <div className="flex-1 h-4 rounded-full bg-white/60 border border-white/70 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-brand-sky to-brand-lavender"
                        style={{ width: `${Math.min(100, f.rate)}%` }}
                      />
                    </div>
                    <span className="w-16 text-right text-xs font-mono text-text-secondary">{f.count} · {f.rate}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
