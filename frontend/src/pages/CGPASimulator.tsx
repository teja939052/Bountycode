import { useState, useEffect, useCallback } from "react";
import { cgpaApi } from "../services/api/cgpa.ts";
import {
  Calculator, Target, History, Plus, Trash2, GraduationCap,
  Save, Loader2, CheckCircle, XCircle, TrendingUp,
} from "lucide-react";

const TABS = [
  { key: "calculate", label: "Calculate CGPA", icon: Calculator },
  { key: "target", label: "Target CGPA", icon: Target },
  { key: "history", label: "History", icon: History },
];

const EMPTY_SEMESTER = { name: "Semester 1", subjects: [{ name: "", credits: 3, grade_point: 8 }] };

function emptySemester(n) {
  return { name: `Semester ${n}`, subjects: [{ name: "", credits: 3, grade_point: 8 }] };
}

export default function CGPASimulator() {
  const [tab, setTab] = useState("calculate");
  const [semesters, setSemesters] = useState([emptySemester(1)]);
  const [calcResult, setCalcResult] = useState(null);
  const [calcLoading, setCalcLoading] = useState(false);

  const [targetForm, setTargetForm] = useState({ current_cgpa: 7.5, credits_completed: 60, target_cgpa: 8.5, credits_remaining: 30 });
  const [targetResult, setTargetResult] = useState(null);
  const [targetLoading, setTargetLoading] = useState(false);

  const [history, setHistory] = useState([]);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  const loadHistory = useCallback(async () => {
    try {
      const data = await cgpaApi.history();
      setHistory(data.history || []);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  // ── Calculate tab helpers ──────────────────────────────────────────────
  const updateSemester = (si, patch) => {
    setSemesters((prev) => prev.map((s, i) => (i === si ? { ...s, ...patch } : s)));
  };

  const updateSubject = (si, ti, patch) => {
    setSemesters((prev) => prev.map((s, i) => {
      if (i !== si) return s;
      const subjects = s.subjects.map((sub, j) => (j === ti ? { ...sub, ...patch } : sub));
      return { ...s, subjects };
    }));
  };

  const addSubject = (si) => {
    setSemesters((prev) => prev.map((s, i) => (i === si ? { ...s, subjects: [...s.subjects, { name: "", credits: 3, grade_point: 8 }] } : s)));
  };

  const removeSubject = (si, ti) => {
    setSemesters((prev) => prev.map((s, i) => (i === si ? { ...s, subjects: s.subjects.filter((_, j) => j !== ti) } : s)));
  };

  const addSemester = () => {
    setSemesters((prev) => [...prev, emptySemester(prev.length + 1)]);
  };

  const removeSemester = (si) => {
    setSemesters((prev) => prev.filter((_, i) => i !== si));
  };

  const handleCalculate = async () => {
    setCalcLoading(true);
    setError("");
    setSaved(false);
    try {
      const data = await cgpaApi.calculate({ semesters });
      setCalcResult(data);
    } catch (e) {
      setError(e.message || "Calculation failed");
    } finally {
      setCalcLoading(false);
    }
  };

  const handleSaveCalc = async () => {
    if (!calcResult) return;
    try {
      await cgpaApi.save({ title: `${calcResult.cumulative_cgpa} CGPA · ${calcResult.semesters.length} sems`, kind: "calculate", result: calcResult });
      setSaved(true);
      loadHistory();
    } catch {
      // ignore
    }
  };

  // ── Target tab helpers ─────────────────────────────────────────────────
  const handleTarget = async () => {
    setTargetLoading(true);
    setError("");
    setSaved(false);
    try {
      const data = await cgpaApi.target(targetForm);
      setTargetResult(data);
    } catch (e) {
      setError(e.message || "Calculation failed");
    } finally {
      setTargetLoading(false);
    }
  };

  const handleSaveTarget = async () => {
    if (!targetResult) return;
    try {
      await cgpaApi.save({
        title: `${targetForm.target_cgpa} target · ${targetForm.credits_remaining} credits left`,
        kind: "target",
        result: targetResult,
      });
      setSaved(true);
      loadHistory();
    } catch {
      // ignore
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <GraduationCap className="text-brand-lavender" size={32} />
            CGPA Simulator
          </h1>
          <p className="text-text-light mt-1">Plan semesters and figure out exactly what you need to hit your target CGPA</p>
        </div>
      </div>

      <div className="flex gap-1 mb-6 p-1 rounded-2xl bg-white border-border/50 border border-white/60 w-fit">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center gap-2 ${
              tab === t.key ? "bg-white shadow-sm text-text-primary" : "text-text-light hover:text-text-secondary"
            }`}
          >
            <t.icon size={16} />
            {t.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      {tab === "calculate" && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-text-primary">Your Semesters</h2>
              <button onClick={addSemester} className="px-3 py-2 rounded-xl border border-brand-sky/40 text-brand-sky text-sm font-medium hover:bg-brand-sky/5 flex items-center gap-1">
                <Plus size={15} /> Add Semester
              </button>
            </div>

            {semesters.map((sem, si) => (
              <div key={si} className="mb-4 p-4 rounded-xl border border-white/60 bg-white border-border/50">
                <div className="flex items-center justify-between mb-3">
                  <input
                    value={sem.name}
                    onChange={(e) => updateSemester(si, { name: e.target.value })}
                    className="p-2 rounded-lg border border-white/60 bg-white text-sm font-semibold"
                  />
                  {semesters.length > 1 && (
                    <button onClick={() => removeSemester(si)} className="text-text-light hover:text-red-500">
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>
                <div className="space-y-2">
                  {sem.subjects.map((sub, ti) => (
                    <div key={ti} className="flex items-center gap-2">
                      <input
                        value={sub.name}
                        onChange={(e) => updateSubject(si, ti, { name: e.target.value })}
                        placeholder="Subject name"
                        className="flex-1 p-2 rounded-lg border border-white/60 bg-white text-sm"
                      />
                      <select
                        value={sub.credits}
                        onChange={(e) => updateSubject(si, ti, { credits: Number(e.target.value) })}
                        className="p-2 rounded-lg border border-white/60 bg-white text-sm"
                        title="Credits"
                      >
                        {[1, 2, 3, 4, 5].map((c) => <option key={c} value={c}>{c} cr</option>)}
                      </select>
                      <select
                        value={sub.grade_point}
                        onChange={(e) => updateSubject(si, ti, { grade_point: Number(e.target.value) })}
                        className="p-2 rounded-lg border border-white/60 bg-white text-sm"
                        title="Grade point (0-10)"
                      >
                        {[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0].map((p) => <option key={p} value={p}>{p} pts</option>)}
                      </select>
                      <button onClick={() => removeSubject(si, ti)} className="text-text-light hover:text-red-500">
                        <Trash2 size={15} />
                      </button>
                    </div>
                  ))}
                </div>
                <button onClick={() => addSubject(si)} className="mt-2 text-sm text-brand-sky hover:underline flex items-center gap-1">
                  <Plus size={14} /> Add subject
                </button>
              </div>
            ))}

            <button
              onClick={handleCalculate}
              disabled={calcLoading}
              className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {calcLoading ? <Loader2 size={18} className="animate-spin" /> : <Calculator size={18} />} Calculate CGPA
            </button>
          </div>

          {calcResult && (
            <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-text-primary">Result</h2>
                <button onClick={handleSaveCalc} disabled={saved} className="px-3 py-2 rounded-xl border border-white/60 text-sm font-medium flex items-center gap-1.5 hover:bg-white border-border/60 disabled:opacity-50">
                  {saved ? <CheckCircle size={15} className="text-green-600" /> : <Save size={15} />} {saved ? "Saved" : "Save"}
                </button>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl text-center bg-brand-lavender/10 border border-brand-lavender/20">
                  <div className="text-xs text-text-light uppercase tracking-wide">Cumulative CGPA</div>
                  <div className="text-4xl font-extrabold text-brand-lavender">{calcResult.cumulative_cgpa}</div>
                </div>
                <div className="p-4 rounded-xl text-center bg-brand-sky/10 border border-brand-sky/20">
                  <div className="text-xs text-text-light uppercase tracking-wide">Total Credits</div>
                  <div className="text-4xl font-extrabold text-brand-sky">{calcResult.total_credits}</div>
                </div>
                <div className="p-4 rounded-xl text-center bg-green-50 border border-green-200">
                  <div className="text-xs text-text-light uppercase tracking-wide">Classification</div>
                  <div className="text-lg font-bold text-green-700 mt-2">{calcResult.classification}</div>
                </div>
              </div>
              <div className="space-y-2">
                {calcResult.semesters.map((s, i) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-xl border border-white/60 bg-white border-border/50">
                    <div>
                      <div className="text-sm font-medium text-text-primary">{s.name}</div>
                      <div className="text-[11px] text-text-light">{s.credits} credits · {s.grade_points} grade points</div>
                    </div>
                    <div className="text-xl font-bold text-text-primary">{s.gpa}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "target" && (
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 space-y-4">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <Target size={18} className="text-brand-coral" /> What-if Planning
            </h2>
            <div>
              <label className="text-sm font-medium text-text-light mb-1 block">Current CGPA</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                value={targetForm.current_cgpa}
                onChange={(e) => setTargetForm({ ...targetForm, current_cgpa: Number(e.target.value) })}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-text-light mb-1 block">Credits completed</label>
              <input
                type="number"
                min="0"
                value={targetForm.credits_completed}
                onChange={(e) => setTargetForm({ ...targetForm, credits_completed: Number(e.target.value) })}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-text-light mb-1 block">Target CGPA</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                value={targetForm.target_cgpa}
                onChange={(e) => setTargetForm({ ...targetForm, target_cgpa: Number(e.target.value) })}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-text-light mb-1 block">Credits remaining</label>
              <input
                type="number"
                min="1"
                value={targetForm.credits_remaining}
                onChange={(e) => setTargetForm({ ...targetForm, credits_remaining: Number(e.target.value) })}
                className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
              />
            </div>
            <button onClick={handleTarget} disabled={targetLoading} className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50">
              {targetLoading ? <Loader2 size={18} className="animate-spin" /> : <TrendingUp size={18} />} Calculate
            </button>
          </div>

          {targetResult && (
            <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-text-primary">Path to {targetResult.target_cgpa}</h2>
                <button onClick={handleSaveTarget} disabled={saved} className="px-3 py-2 rounded-xl border border-white/60 text-sm font-medium flex items-center gap-1.5 hover:bg-white border-border/60 disabled:opacity-50">
                  {saved ? <CheckCircle size={15} className="text-green-600" /> : <Save size={15} />} {saved ? "Saved" : "Save"}
                </button>
              </div>
              <div className={`p-4 rounded-xl border ${targetResult.feasible ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}`}>
                <div className="flex items-center gap-2 mb-1">
                  {targetResult.feasible ? <CheckCircle size={18} className="text-green-600" /> : <XCircle size={18} className="text-red-500" />}
                  <span className={`font-bold ${targetResult.feasible ? "text-green-700" : "text-red-600"}`}>
                    {targetResult.feasible ? "Feasible" : "Not feasible right now"}
                  </span>
                </div>
                <div className="text-sm text-text-secondary">
                  You need an average of <strong className="text-text-primary">{targetResult.required_gpa}/10</strong> in the next {targetResult.credits_remaining} credits
                  {!targetResult.feasible && <span> — still {targetResult.shortfall} points short even with all 10s</span>}.
                </div>
              </div>
              <div>
                <div className="text-sm font-semibold text-text-primary mb-2">If you average each grade for the remaining credits:</div>
                <div className="space-y-1">
                  {targetResult.breakdown.map((b) => (
                    <div key={b.grade} className={`flex items-center justify-between p-2.5 rounded-xl border text-sm ${
                      b.hits_target ? "border-green-200 bg-green-50" : "border-white/60 bg-white border-border/50"
                    }`}>
                      <div className="flex items-center gap-2">
                        <span className="w-8 h-8 rounded-lg bg-surface-base flex items-center justify-center font-bold text-text-primary">{b.grade}</span>
                        <span className="text-text-light text-xs">{b.points} pts</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {b.hits_target && <CheckCircle size={15} className="text-green-600" />}
                        <span className="font-bold">{b.final_cgpa}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "history" && (
        <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80">
          <h2 className="text-lg font-bold text-text-primary mb-4">Saved Calculations</h2>
          {history.length === 0 ? (
            <p className="text-text-light text-sm">Nothing saved yet. Run a calculation and hit Save.</p>
          ) : (
            <div className="space-y-2">
              {history.map((h) => (
                <div key={h.id} className="flex items-center justify-between p-3 rounded-xl border border-white/60 bg-white border-border/50">
                  <div>
                    <div className="text-sm font-medium text-text-primary">{h.title}</div>
                    <div className="text-[11px] text-text-light">
                      {h.kind === "target" ? "Target planner" : "CGPA calculation"} · {new Date(h.created_at).toLocaleString()}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      if (h.kind === "target") { setTargetResult(h.result); setTab("target"); }
                      else { setCalcResult(h.result); setTab("calculate"); }
                    }}
                    className="px-3 py-1.5 rounded-lg border border-white/60 text-xs font-medium hover:bg-white border-border/60"
                  >
                    View
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
