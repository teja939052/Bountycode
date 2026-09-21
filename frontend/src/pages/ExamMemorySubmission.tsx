import { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import { useSearchParams } from "react-router-dom";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import type { ExamMemory, ExamMemoryHeatmap, SubmitMemoryRequest } from "../services/api/examMemories";
import {
  Database,
  Medal,
  ShieldCheck,
  Plus,
  Trash2,
  Send,
  CheckCircle2,
  Clock,
  Info,
  Flame,
} from "lucide-react";

const FORMATS = [
  { id: "mcq", label: "MCQ", hint: "Multiple-choice with 4 options" },
  { id: "verbal", label: "Fill-in / Verbal", hint: "Short answer or sentence completion" },
  { id: "code", label: "Coding", hint: "Programming problem statement" },
] as const;

const EXAMS_FALLBACK = [
  { id: "tcs_nqt", name: "TCS NQT" },
  { id: "tcs_ipa", name: "TCS IPA" },
  { id: "infytq", name: "Infosys InfyTQ" },
  { id: "wipro_nlth", name: "Wipro NLTH" },
  { id: "accenture", name: "Accenture" },
  { id: "cognizant_genc", name: "Cognizant GenC" },
  { id: "capgemini_amcat", name: "Capgemini" },
  { id: "ibm_entry", name: "IBM" },
  { id: "amazon_sde", name: "Amazon SDE" },
  { id: "google", name: "Google" },
  { id: "microsoft", name: "Microsoft" },
  { id: "other", name: "Other" },
];

const DEFAULT_SECTIONS = ["aptitude", "logical", "verbal", "cs_fundamentals", "coding", "other"];

const SECTION_LABEL: Record<string, string> = {
  aptitude: "Aptitude",
  logical: "Logical",
  verbal: "Verbal",
  cs_fundamentals: "Programming Logic",
  coding: "Coding",
  other: "Other",
};

const STATUS_STYLE: Record<string, string> = {
  new: "bg-surface-2 text-text-secondary border-black/10",
  verified_crowd: "bg-emerald-50 text-emerald-700 border-emerald-200",
  approved: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30",
  dismissed: "bg-red-50 text-red-500 border-red-200",
};

export default function ExamMemorySubmission() {
  const [searchParams] = useSearchParams();
  const initialExam = searchParams.get("exam") || "tcs_nqt";
  const [config, setConfig] = useState<{
    exams: { id: string; name: string }[];
    sections: string[];
    verify_threshold: number;
    daily_cap: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState<{
    status: string;
    report_count: number;
    threshold: number;
    note: string;
    diamonds?: number;
    coins?: number;
    badges?: { id: string; name: string; icon: string }[];
  } | null>(null);

  const [exam, setExam] = useState(initialExam);
  const [section, setSection] = useState("aptitude");
  const [topic, setTopic] = useState("");
  const [format, setFormat] = useState<"mcq" | "code" | "verbal">("mcq");
  const [questionText, setQuestionText] = useState("");
  const [options, setOptions] = useState<string[]>(["", "", "", ""]);
  const [knownAnswer, setKnownAnswer] = useState("");
  const [notes, setNotes] = useState("");

  const [myMemories, setMyMemories] = useState<ExamMemory[]>([]);
  const [heatmap, setHeatmap] = useState<ExamMemoryHeatmap | null>(null);

  const exams = config?.exams || EXAMS_FALLBACK;
  const sections = config?.sections || DEFAULT_SECTIONS;
  const threshold = config?.verify_threshold ?? 5;
  const dailyCap = config?.daily_cap ?? 5;

  useEffect(() => {
    (async () => {
      try {
        const [cfg, mine, hm] = await Promise.all([api.examMemories.config(), api.examMemories.mySubmissions(), api.examMemories.heatmap(7)]);
        setConfig(cfg);
        setSection(cfg.sections[0] || "aptitude");
        if (!cfg.exams.some((e: { id: string }) => e.id === exam)) {
          setExam(cfg.exams[0]?.id || "tcs_nqt");
        }
setMyMemories(mine.memories || []);
        setHeatmap(hm);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load exam memory config");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const validMcq = useMemo(() => {
    const clean = options.filter((o) => o.trim().length > 0);
    return {
      clean,
      valid: clean.length >= 2,
    };
  }, [options]);

  const canSubmit = useMemo(() => {
    if (questionText.trim().length < 15) return false;
    if (format === "mcq" && !validMcq.valid) return false;
    return true;
  }, [questionText, format, validMcq]);

  const updateOption = (idx: number, value: string) => {
    setOptions((prev) => prev.map((o, i) => (i === idx ? value : o)));
  };

  const submitMemory = async () => {
    setSaving(true);
    setError("");
    setSuccess(null);
    try {
      const payload: SubmitMemoryRequest = {
        exam,
        section,
        topic: topic.trim().slice(0, 120),
        question_text: questionText.trim(),
        format,
        known_answer: knownAnswer.trim(),
        notes: notes.trim(),
      };
      if (format === "mcq") payload.options = validMcq.clean;
      const res = (await api.examMemories.submit(payload)) as {
        status: string;
        report_count: number;
        note: string;
        reward?: {
          xp_gained?: number;
          coins_earned?: number;
          new_badges?: { id: string; name: string; icon: string }[];
        };
      };
      setSuccess({
        status: res.status,
        report_count: res.report_count,
        threshold,
        note: res.note,
        diamonds: res.reward?.xp_gained,
        coins: res.reward?.coins_earned,
        badges: res.reward?.new_badges,
      });
      setQuestionText("");
      setOptions(["", "", "", ""]);
      setKnownAnswer("");
      setNotes("");
      const mine = await api.examMemories.mySubmissions();
      setMyMemories(mine.memories || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit memory");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="page-surface min-h-screen py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div className="mb-8 text-center" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <span className="section-subheader mb-3 block">Student Memory · Crowdsourced Bank</span>
          <h1 className="section-header text-3xl mb-3 flex items-center justify-center gap-2">
            <Database className="text-nature-blossom" size={30} />
            Exam <span className="text-nature-blossom">Memory</span>
          </h1>
          <p className="text-text-muted font-mono text-sm max-w-2xl mx-auto">
            Remember questions from an assessment you just took? Contribute them.
            When{" "}
            <span className="text-nature-blossom font-medium">
              {threshold} independent students
            </span>{" "}
            report the same question it becomes a verified_crowd item, and a human
            review can promote it into the live bank. No screenshots, no code dumps —
            just honest recollections.
          </p>
          <div className="mt-4 flex flex-wrap justify-center gap-2 font-mono text-[11px]">
            <span className="rounded-full bg-blossom-50 border border-nature-blossom/30 px-3 py-1 text-nature-blossom flex items-center gap-1">
              <ShieldCheck size={12} /> Threshold: {threshold} reports
            </span>
            <span className="rounded-full bg-surface-2 px-3 py-1 text-text-secondary flex items-center gap-1">
              <Clock size={12} /> Daily cap: {dailyCap} submissions
            </span>
          </div>
        </motion.div>

        {heatmap && (
          <motion.div
            className="card rounded-3xl mb-6 p-5"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 }}
          >
            <div className="flex items-start justify-between gap-3 mb-1">
              <h2 className="section-header text-base flex items-center gap-2">
                <Flame size={18} className="text-amber-500" /> Real Question Heatmap
              </h2>
              <span className="font-mono text-[10px] text-text-muted shrink-0">
                last {heatmap.window_days} days
              </span>
            </div>
            <p className="font-mono text-xs text-text-secondary mb-4">
              {heatmap.total_submissions} recollections reported by students this week — the hotter the row, the more independent test-takers recalled it.
            </p>

            {(heatmap.by_section || []).slice(0, 8).length > 0 && (
              <div className="space-y-2 mb-5">
                {(heatmap.by_section || []).slice(0, 8).map((row) => {
                  const max = Math.max(1, ...(heatmap.by_section || []).map((r) => r.reports));
                  return (
                    <div key={`${row.exam}-${row.section}`} className="flex items-center gap-3">
                      <span className="w-40 shrink-0 font-mono text-[11px] text-text-primary truncate">
                        {row.exam_name} · {SECTION_LABEL[row.section]?.toLowerCase()}
                      </span>
                      <div className="flex-1 h-2 rounded-full bg-surface-2 overflow-hidden">
                        <div
                          className="h-full rounded-full bg-amber-500/80"
                          style={{ width: `${Math.max(4, (row.reports / max) * 100)}%` }}
                        />
                      </div>
                      <span className="w-16 text-right font-mono text-[11px] font-bold text-amber-600 shrink-0">
                        {row.reports} reports
                      </span>
                      <span className="w-10 text-right font-mono text-[10px] text-text-muted shrink-0">
                        {row.verified_crowd > 0 && `${row.verified_crowd}★`}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}

            <h3 className="font-display font-bold text-sm text-text-primary mb-2 flex items-center gap-2">
              Most-reported this week <span className="font-mono text-[10px] text-text-muted font-normal">({heatmap.verify_threshold}+ reports flags for review)</span>
            </h3>
            <div className="space-y-2">
              {(heatmap.hot_questions || []).length === 0 && (
                <p className="font-mono text-xs text-text-muted">
                  No recollections yet. Yours could be the first — start reporting above.
                </p>
              )}
              {(heatmap.hot_questions || []).slice(0, 6).map((h) => (
                <div key={h.memory_id} className="rounded-xl border border-black/5 bg-surface-2/60 px-3 py-2">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className="rounded-full bg-amber-50 border border-amber-200 px-2 py-0.5 font-mono text-[10px] text-amber-700">
                      {h.report_count} reports
                    </span>
                    <span className="rounded-full bg-surface-2 px-2 py-0.5 font-mono text-[10px] text-text-secondary">
                      {h.exam_name} · {SECTION_LABEL[h.section]?.toLowerCase()}
                    </span>
                    {h.reviewed ? (
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 font-mono text-[10px] text-emerald-700 flex items-center gap-1">
                        <ShieldCheck size={10} /> human-reviewed
                      </span>
                    ) : (
                      <span className="rounded-full bg-surface-2 px-2 py-0.5 font-mono text-[10px] text-text-muted">
                        in review
                      </span>
                    )}
                  </div>
                  <p className="font-mono text-[11px] text-text-primary leading-relaxed">
                    {h.reviewed && h.question_text ? (
                      h.question_text
                    ) : h.topic ? (
                      <>Topic: {h.topic}</>
                    ) : (
                      "Topic not disclosed — question under review"
                    )}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center font-mono text-sm text-red-600">
            {error}
          </div>
        )}

        {success && (
          <motion.div
            className="mb-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <div className="flex items-start gap-3">
              <CheckCircle2 size={20} className="text-emerald-600 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-emerald-800">Memory recorded</p>
                <p className="font-mono text-xs text-emerald-700 mt-1">
                  {success.note} · {success.report_count}/{success.threshold} reports so far
                </p>
                {(success.diamonds !== undefined || success.coins !== undefined) && (
                  <p className="mt-2 flex flex-wrap items-center gap-2 font-mono text-xs text-emerald-800">
                    <span className="rounded-full bg-emerald-100 px-2 py-0.5">
                      +{success.diamonds ?? 0} Diamonds
                    </span>
                    <span className="rounded-full bg-emerald-100 px-2 py-0.5">
                      +{success.coins ?? 0} coins
                    </span>
                    {(success.badges || []).map((b) => (
                      <span
                        key={b.id}
                        className="rounded-full bg-amber-100 px-2 py-0.5 text-amber-800"
                        title={`${b.name} badge`}
                      >
                        {b.icon} {b.name}
                      </span>
                    ))}
                    <span className="text-emerald-600">· reward for your contribution</span>
                  </p>
                )}
              </div>
            </div>
          </motion.div>
        )}

        <div className="grid gap-6 md:grid-cols-3">
          <motion.div className="card md:col-span-2 rounded-3xl" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}>
            <h2 className="font-display font-bold text-text-primary mb-4 text-sm">Tell us what you remember</h2>

            <div className="grid sm:grid-cols-2 gap-3 mb-4">
              <label className="block">
                <span className="label-text">Exam</span>
                <select value={exam} onChange={(e) => setExam(e.target.value)} className="field">
                  {exams.map((e) => (
                    <option key={e.id} value={e.id}>{e.name}</option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="label-text">Section</span>
                <select value={section} onChange={(e) => setSection(e.target.value)} className="field">
                  {sections.map((s) => (
                    <option key={s} value={s}>{s.replace(/_/g, " ")}</option>
                  ))}
                </select>
              </label>
              <label className="block sm:col-span-1">
                <span className="label-text">Topic (optional)</span>
                <input
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g. percentages, arrays"
                  maxLength={120}
                  className="field"
                />
              </label>
              <label className="block">
                <span className="label-text">Format</span>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value as typeof format)}
                  className="field"
                >
                  {FORMATS.map((f) => (
                    <option key={f.id} value={f.id}>{f.label}</option>
                  ))}
                </select>
              </label>
            </div>

            <div className="mb-4 flex flex-wrap gap-1.5 font-mono text-[10px] text-text-muted">
              {FORMATS.map((f) => (
                <span key={f.id} className={format === f.id ? "text-nature-blossom" : ""}>
                  {f.hint}
                </span>
              ))}
            </div>

            <label className="block mb-3">
              <span className="label-text">Question as you remember it</span>
              <textarea
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                rows={4}
                placeholder="Type the question, lengths, or answer options you recall. Include numbers/units if you remember them."
                className="field resize-y"
              />
              <span className={questionText.trim().length >= 15 ? "text-nature-blossom" : ""}>
                {questionText.trim().length}/15 min chars
              </span>
            </label>

            {format === "mcq" && (
              <div className="mb-4">
                <span className="label-text">Answer options (reconstruct what you remember)</span>
                <div className="space-y-2 mt-1">
                  {options.map((opt, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <span className="font-mono font-bold text-[10px] shrink-0 w-5 h-5 rounded-full border border-black/10 flex items-center justify-center text-text-muted">
                        {String.fromCharCode(65 + idx)}
                      </span>
                      <input
                        value={opt}
                        onChange={(e) => updateOption(idx, e.target.value)}
                        placeholder={`Option ${String.fromCharCode(65 + idx)}`}
                        className="field"
                      />
                      {idx >= 4 && (
                        <button
                          type="button"
                          onClick={() => setOptions((prev) => prev.filter((_, i) => i !== idx))}
                          className="text-red-400 hover:text-red-600 shrink-0"
                          aria-label="Remove option"
                        >
                          <Trash2 size={15} />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
                <button
                  type="button"
                  onClick={() => setOptions((prev) => [...prev, ""])}
                  className="btn-ghost text-xs flex items-center gap-1 mt-2"
                >
                  <Plus size={13} /> Add option
                </button>
              </div>
            )}

            <label className="block mb-3">
              <span className="label-text">{format === "code" ? "What did it ask you to do?" : "Known answer (if sure)"}</span>
              <textarea
                value={knownAnswer}
                onChange={(e) => setKnownAnswer(e.target.value)}
                rows={format === "code" ? 4 : 2}
                placeholder={format === "code" ? "Function to write, inputs/outputs, constraints..." : "Write the correct answer if you are confident."}
                className="field resize-y"
              />
            </label>

            <label className="block mb-4">
              <span className="label-text">Notes (optional)</span>
              <input
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Clarify wording, difficulty, or anything uncertain"
                className="field"
              />
            </label>

            <button
              onClick={submitMemory}
              disabled={!canSubmit || saving}
              className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-40"
            >
              {saving ? <Spinner size="sm" className="text-space-void" /> : <><Send size={16} /> Submit memory</>}
            </button>

            {!canSubmit && (
              <p className="mt-2 text-center font-mono text-[11px] text-text-muted flex items-center justify-center gap-1">
                <Info size={12} />
                {questionText.trim().length < 15
                  ? "Question text needs at least 15 characters"
                  : "MCQ needs at least 2 non-empty options"}
              </p>
            )}
          </motion.div>

          <motion.div className="space-y-4" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.12 }}>
            <div className="card rounded-3xl">
              <h3 className="font-display font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                <Medal size={16} className="text-nature-blossom" /> My submissions
              </h3>
              {myMemories.length === 0 ? (
                <p className="font-mono text-xs text-text-muted">Nothing yet. Your first memory helps build the bank.</p>
              ) : (
                <ul className="space-y-3">
                  {myMemories.map((m) => {
                    const id = String(m.id);
                    const st = String(m.status || "new");
                    const q = String(m.question_text || "");
                    return (
                      <li key={id} className="rounded-xl border border-black/5 bg-white p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-mono text-[10px] uppercase tracking-wider text-text-muted">
                            {String(m.exam_name || m.exam)} · {String(m.section || "")}
                          </span>
                          <span className={`rounded-full border px-2 py-0.5 font-mono text-[9px] ${STATUS_STYLE[st] || STATUS_STYLE.new}`}>
                            {st.replace(/_/g, " ")}
                          </span>
                        </div>
                        <p className="text-xs leading-relaxed text-text-secondary line-clamp-2">{q.slice(0, 200)}</p>
                        <p className="font-mono text-[10px] text-text-muted mt-1">
                          {Number(m.report_count || 0)}/{threshold} reports
                          {m.status === "new" && m.report_count >= threshold ? " → verified_crowd ✓" : ""}
                        </p>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>

            <div className="card rounded-3xl">
              <h4 className="font-display font-bold text-text-primary text-sm mb-2">How promotion works</h4>
              <ol className="list-decimal pl-4 space-y-1 font-mono text-[11px] leading-relaxed text-text-muted">
                <li>Your memory lands as UNVERIFIED raw material.</li>
                <li>{threshold}+ independent students report the same question → verified_crowd.</li>
                <li>A human reviewer with the answer key promotes it into the live bank.</li>
                <li>It is never served to students before review.</li>
              </ol>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}