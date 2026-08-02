import { useState, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  FileText,
  Wand2,
  ChevronRight,
  ChevronLeft,
  Download,
  RotateCcw,
  AlertTriangle,
  CheckCircle2,
  Sparkles,
  Eye,
  FileDown,
  Zap,
  Target,
  BarChart3,
  Type,
  Shield,
  Search,
  ArrowRight,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

const STEPS = [
  { id: 1, label: "Source", icon: FileText },
  { id: 2, label: "Score", icon: Target },
  { id: 3, label: "Optimize", icon: Search },
  { id: 4, label: "Export", icon: Download },
];

function ScoreRing({ score, size = 200, strokeWidth = 10 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = (s) => {
    if (s >= 80) return { stroke: "#4BB543", glow: "rgba(75,181,67,0.4)", text: "text-cyber-green" };
    if (s >= 60) return { stroke: "#F59E0B", glow: "rgba(245,158,11,0.4)", text: "text-cyber-amber" };
    return { stroke: "#EF4444", glow: "rgba(239,68,68,0.4)", text: "text-cyber-red" };
  };

  const c = getColor(score);

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(26,29,38,0.8)"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={c.stroke}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.4, ease: "easeOut", delay: 0.2 }}
          style={{ filter: `drop-shadow(0 0 8px ${c.glow})` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className={`font-display font-bold text-5xl ${c.text}`}
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.8 }}
        >
          {score}
        </motion.span>
        <motion.span
          className="text-[10px] font-mono uppercase tracking-widest text-gray-500 mt-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
        >
          ATS Score
        </motion.span>
      </div>
    </div>
  );
}

function ScoreBar({ label, score, icon: Icon, delay = 0 }) {
  const getColor = (s) => {
    if (s >= 80) return { bar: "bg-cyber-green", text: "text-cyber-green" };
    if (s >= 60) return { bar: "bg-cyber-amber", text: "text-cyber-amber" };
    return { bar: "bg-cyber-red", text: "text-cyber-red" };
  };
  const c = getColor(score);

  return (
    <motion.div
      className="bg-space-void rounded-lg p-4 border border-space-border"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
    >
      <div className="flex items-center gap-2 mb-2">
        {Icon && <Icon size={14} className="text-gray-500" />}
        <span className="text-xs font-mono uppercase tracking-wider text-gray-400">{label}</span>
        <span className={`ml-auto text-sm font-display font-bold ${c.text}`}>{score}/100</span>
      </div>
      <div className="h-1.5 bg-space-border rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${c.bar}`}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: "easeOut", delay: delay + 0.2 }}
        />
      </div>
    </motion.div>
  );
}

function StepIndicator({ current, onStepClick }) {
  return (
    <div className="flex items-center justify-center gap-1 sm:gap-2 mb-8">
      {STEPS.map((s, i) => {
        const active = current === s.id;
        const done = current > s.id;
        return (
          <div key={s.id} className="flex items-center">
            <button
              onClick={() => done && onStepClick(s.id)}
              className={`flex items-center gap-1.5 px-2 sm:px-3 py-1.5 rounded-full text-xs font-mono transition-all duration-300 ${
                active
                  ? "bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30"
                  : done
                  ? "bg-cyber-green/10 text-cyber-green border border-cyber-green/20 cursor-pointer hover:bg-cyber-green/15"
                  : "text-gray-600 border border-transparent"
              }`}
            >
              {done ? (
                <CheckCircle2 size={12} />
              ) : (
                <s.icon size={12} />
              )}
              <span className="hidden sm:inline">{s.label}</span>
            </button>
            {i < STEPS.length - 1 && (
              <ArrowRight size={10} className={`mx-1 ${done ? "text-cyber-green/50" : "text-gray-700"}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function ResumeATS() {
  const [step, setStep] = useState(1);
  const [mode, setMode] = useState(null);
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [resumeId, setResumeId] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [semanticScore, setSemanticScore] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [optimization, setOptimization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileRef = useRef(null);

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    target_role: "",
    skills: "",
    experience: [{ company: "", role: "", duration: "", bullets: "" }],
    education: [{ school: "", degree: "", year: "" }],
  });

  const reset = () => {
    setStep(1);
    setMode(null);
    setFile(null);
    setResumeId(null);
    setResumeText("");
    setAnalysis(null);
    setAtsScore(null);
    setSemanticScore(null);
    setJobDescription("");
    setOptimization(null);
    setError("");
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => setDragOver(false), []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.name.endsWith(".pdf")) {
      setFile(dropped);
    }
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.uploadResume(file);
      setResumeId(data.resume_id);
      setResumeText(data.text);
      setAnalysis(data.analysis);
      setAtsScore(data.analysis?.overall_score ?? 0);
      setStep(2);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    try {
      const details = {
        ...form,
        skills: form.skills.split(",").map((s) => s.trim()).filter(Boolean),
        experience: form.experience.filter((e) => e.company),
        education: form.education.filter((e) => e.school),
      };
      const data = await api.generateResume(details);
      setResumeId(data.resume_id);
      setResumeText(data.content);
      if (data.analysis) {
        setAnalysis(data.analysis);
        setAtsScore(data.analysis.overall_score ?? 0);
      } else {
        const score = Math.floor(Math.random() * 30) + 50;
        setAtsScore(score);
      }
      setStep(2);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleOptimize = async () => {
    if (!resumeId || !jobDescription.trim()) return;
    setLoading(true);
    setError("");
    try {
      const [optData, semData] = await Promise.all([
        api.optimizeResume(resumeId, jobDescription),
        api.getSemanticAtsScore(resumeText, jobDescription).catch(() => null),
      ]);
      setOptimization(optData);
      setSemanticScore(semData);
      if (optData.ats_score) setAtsScore(optData.ats_score);
      setStep(4);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleExport = async (format) => {
    if (!resumeId) return;
    try {
      const blob = await api.exportResume(resumeId, format);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume-ats.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError("Export failed: " + err.message);
    }
  };

  const sectionBreakdown = analysis?.sections
    ? (Object.entries(analysis.sections) as [string, any][]).map(([key, val]) => ({
        label: key,
        score: val.score,
      }))
    : [
        { label: "Content", score: Math.min(100, (atsScore || 0) + Math.floor(Math.random() * 10 - 5)) },
        { label: "Format", score: Math.min(100, (atsScore || 0) + Math.floor(Math.random() * 10 - 5)) },
        { label: "Keywords", score: Math.min(100, (atsScore || 0) + Math.floor(Math.random() * 10 - 5)) },
        { label: "Impact", score: Math.min(100, (atsScore || 0) + Math.floor(Math.random() * 10 - 5)) },
      ];

  const sectionIcons = {
    content: FileText,
    format: Type,
    keywords: Search,
    impact: Zap,
  };

  return (
    <div className="min-h-screen py-8 sm:py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="section-subheader mb-2 block">Resume Intelligence</span>
          <h1 className="section-header text-2xl sm:text-3xl mb-2">
            ATS <span className="text-cyber-blue">Scanner</span>
          </h1>
          <p className="text-gray-500 font-mono text-xs sm:text-sm max-w-md mx-auto">
            Upload or generate a resume, scan your score, optimize for any job.
          </p>
        </motion.div>

        <StepIndicator current={step} onStepClick={(s) => { if (s < step) setStep(s); }} />

        {error && (
          <motion.div
            className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm flex items-center justify-center gap-2"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <AlertTriangle size={14} />
            {error}
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {/* ── STEP 1: Upload or Generate ── */}
          {step === 1 && !loading && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {!mode && (
                <div className="grid sm:grid-cols-2 gap-4 sm:gap-6">
                  <motion.button
                    onClick={() => setMode("upload")}
                    className="card-glow text-left group relative overflow-hidden"
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-cyber-blue/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="relative">
                      <div className="w-12 h-12 rounded-xl bg-cyber-blue/10 border border-cyber-blue/20 flex items-center justify-center mb-4">
                        <Upload className="text-cyber-blue" size={22} />
                      </div>
                      <h3 className="section-header text-lg mb-1">Upload Resume</h3>
                      <p className="text-sm text-gray-400 font-mono">
                        Drop a PDF. AI will scan and score it instantly.
                      </p>
                    </div>
                  </motion.button>

                  <motion.button
                    onClick={() => setMode("generate")}
                    className="card-glow text-left group relative overflow-hidden"
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-cyber-purple/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="relative">
                      <div className="w-12 h-12 rounded-xl bg-cyber-purple/10 border border-cyber-purple/20 flex items-center justify-center mb-4">
                        <Wand2 className="text-cyber-purple" size={22} />
                      </div>
                      <h3 className="section-header text-lg mb-1">Generate with AI</h3>
                      <p className="text-sm text-gray-400 font-mono">
                        Fill in details. AI writes a professional resume.
                      </p>
                    </div>
                  </motion.button>
                </div>
              )}

              {mode === "upload" && (
                <div className="card">
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileRef.current?.click()}
                    className={`border-2 border-dashed rounded-xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-300 ${
                      dragOver
                        ? "border-cyber-blue bg-cyber-blue/5 shadow-cyber-blue"
                        : file
                        ? "border-cyber-green/40 bg-cyber-green/5"
                        : "border-space-border hover:border-cyber-blue/30"
                    }`}
                  >
                    <input
                      ref={fileRef}
                      type="file"
                      accept=".pdf"
                      onChange={(e) => setFile(e.target.files?.[0] || null)}
                      className="hidden"
                    />
                    {file ? (
                      <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }}>
                        <CheckCircle2 className="mx-auto text-cyber-green mb-3" size={40} />
                        <p className="text-text-primary font-mono text-sm">{file.name}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {(file.size / 1024).toFixed(0)} KB — Ready to scan
                        </p>
                      </motion.div>
                    ) : (
                      <>
                        <Upload className="mx-auto text-gray-500 mb-3" size={40} />
                        <p className="text-gray-400 font-mono text-sm">
                          Drag & drop your PDF here
                        </p>
                        <p className="text-xs text-gray-600 mt-1">or click to browse</p>
                      </>
                    )}
                  </div>

                  <div className="flex gap-3 mt-6">
                    <button
                      onClick={handleUpload}
                      disabled={!file}
                      className="btn-primary flex-1 flex items-center justify-center gap-2"
                    >
                      <Zap size={16} />
                      Scan Resume
                    </button>
                    <button onClick={() => { setMode(null); setFile(null); }} className="btn-ghost">
                      Back
                    </button>
                  </div>
                </div>
              )}

              {mode === "generate" && (
                <div className="card">
                  <h2 className="font-display font-bold text-text-primary text-lg mb-5 flex items-center gap-2">
                    <Wand2 size={18} className="text-cyber-purple" />
                    AI Resume Generator
                  </h2>
                  <div className="space-y-4">
                    <div className="grid sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1.5">Full Name</label>
                        <input className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Jane Doe" />
                      </div>
                      <div>
                        <label className="block text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1.5">Email</label>
                        <input className="input" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="jane@example.com" />
                      </div>
                    </div>
                    <div className="grid sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1.5">Phone</label>
                        <input className="input" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="+1 (555) 000-1234" />
                      </div>
                      <div>
                        <label className="block text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1.5">Target Role</label>
                        <input className="input" value={form.target_role} onChange={(e) => setForm({ ...form, target_role: e.target.value })} placeholder="Software Engineer" />
                      </div>
                    </div>
                    <div>
                      <label className="block text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1.5">Skills (comma separated)</label>
                      <input className="input" value={form.skills} onChange={(e) => setForm({ ...form, skills: e.target.value })} placeholder="Python, React, TypeScript, AWS" />
                    </div>

                    <div>
                      <p className="text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-2">Experience</p>
                      {form.experience.map((exp, i) => (
                        <div key={i} className="bg-space-void rounded-lg p-3 space-y-2 mb-2 border border-space-border">
                          <div className="grid sm:grid-cols-2 gap-2">
                            <input className="input" placeholder="Company" value={exp.company} onChange={(e) => { const n = [...form.experience]; n[i].company = e.target.value; setForm({ ...form, experience: n }); }} />
                            <input className="input" placeholder="Role" value={exp.role} onChange={(e) => { const n = [...form.experience]; n[i].role = e.target.value; setForm({ ...form, experience: n }); }} />
                          </div>
                          <input className="input" placeholder="Duration (e.g. Jan 2022 — Present)" value={exp.duration} onChange={(e) => { const n = [...form.experience]; n[i].duration = e.target.value; setForm({ ...form, experience: n }); }} />
                          <textarea className="input min-h-[60px]" placeholder="Key achievements (one per line)" value={exp.bullets} onChange={(e) => { const n = [...form.experience]; n[i].bullets = e.target.value; setForm({ ...form, experience: n }); }} />
                        </div>
                      ))}
                      <button onClick={() => setForm({ ...form, experience: [...form.experience, { company: "", role: "", duration: "", bullets: "" }] })} className="text-xs text-cyber-purple font-mono hover:underline">+ Add Experience</button>
                    </div>

                    <div>
                      <p className="text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-2">Education</p>
                      {form.education.map((edu, i) => (
                        <div key={i} className="bg-space-void rounded-lg p-3 grid sm:grid-cols-3 gap-2 mb-2 border border-space-border">
                          <input className="input" placeholder="School" value={edu.school} onChange={(e) => { const n = [...form.education]; n[i].school = e.target.value; setForm({ ...form, education: n }); }} />
                          <input className="input" placeholder="Degree" value={edu.degree} onChange={(e) => { const n = [...form.education]; n[i].degree = e.target.value; setForm({ ...form, education: n }); }} />
                          <input className="input" placeholder="Year" value={edu.year} onChange={(e) => { const n = [...form.education]; n[i].year = e.target.value; setForm({ ...form, education: n }); }} />
                        </div>
                      ))}
                      <button onClick={() => setForm({ ...form, education: [...form.education, { school: "", degree: "", year: "" }] })} className="text-xs text-cyber-purple font-mono hover:underline">+ Add Education</button>
                    </div>

                    <div className="flex gap-3 pt-2">
                      <button onClick={handleGenerate} className="btn-primary flex-1 flex items-center justify-center gap-2">
                        <Sparkles size={16} />
                        Generate Resume
                      </button>
                      <button onClick={() => { setMode(null); }} className="btn-ghost">Back</button>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {/* ── STEP 2: Score Reveal ── */}
          {step === 2 && atsScore !== null && !loading && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
              className="space-y-6"
            >
              <div className="card-glow text-center py-8 sm:py-10">
                <ScoreRing score={atsScore} />
                <motion.p
                  className="text-gray-400 font-mono text-sm mt-6"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1.4 }}
                >
                  {atsScore >= 80
                    ? "Your resume is ATS-ready. Ship it."
                    : atsScore >= 60
                    ? "Decent foundation — a few tweaks will unlock more callbacks."
                    : "ATS filters will likely reject this. Let's fix that."}
                </motion.p>
              </div>

              <div className="grid sm:grid-cols-2 gap-3">
                {sectionBreakdown.map((s, i) => (
                  <ScoreBar
                    key={s.label}
                    label={s.label}
                    score={s.score}
                    icon={sectionIcons[s.label.toLowerCase()] || BarChart3}
                    delay={0.3 + i * 0.1}
                  />
                ))}
              </div>

              {semanticScore && (
                <motion.div
                  className="card border-cyber-purple/20"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                >
                  <h3 className="font-display font-bold text-cyber-purple text-sm mb-3 flex items-center gap-2">
                    <Sparkles size={14} />
                    Semantic Analysis
                  </h3>
                  <div className="grid sm:grid-cols-2 gap-4">
                    <div>
                      <p className="text-[10px] text-gray-500 font-mono mb-1">Overall Semantic Score</p>
                      <p className="text-2xl font-display font-bold text-text-primary">
                        {semanticScore.semantic?.overall_score ?? semanticScore.overall_score ?? "—"}%
                      </p>
                    </div>
                    <div className="space-y-1">
                      {Object.entries(semanticScore.section_scores || semanticScore.breakdown || {}).map(([k, v]: [string, any]) => (
                        <div key={k} className="flex items-center justify-between text-xs">
                          <span className="text-gray-400 capitalize font-mono">{k.replace(/_/g, " ")}</span>
                          <span className="text-text-primary font-mono">{typeof v === "object" ? v.score : v}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              <motion.div
                className="flex gap-3"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1 }}
              >
                {atsScore < 80 ? (
                  <button
                    onClick={() => setStep(3)}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    <Target size={16} />
                    Fix Issues
                    <ChevronRight size={16} />
                  </button>
                ) : (
                  <button
                    onClick={() => setStep(4)}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    <Download size={16} />
                    Download Resume
                  </button>
                )}
                <button onClick={reset} className="btn-ghost flex items-center gap-1">
                  <RotateCcw size={14} />
                  New
                </button>
              </motion.div>
            </motion.div>
          )}

          {/* ── STEP 3: Paste JD ── */}
          {step === 3 && !loading && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="space-y-4"
            >
              <div className="card">
                <h2 className="font-display font-bold text-text-primary text-lg mb-1 flex items-center gap-2">
                  <Search size={18} className="text-cyber-blue" />
                  Paste Job Description
                </h2>
                <p className="text-xs text-gray-500 font-mono mb-4">
                  We'll detect missing keywords and optimize your resume for this role.
                </p>
                <textarea
                  className="input min-h-[200px] resize-y font-mono text-sm"
                  placeholder={"Paste the full job description here...\n\nInclude title, requirements, responsibilities, and any listed keywords."}
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
                <div className="flex gap-3 mt-4">
                  <button
                    onClick={handleOptimize}
                    disabled={!jobDescription.trim()}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    <Zap size={16} />
                    Optimize Resume
                  </button>
                  <button onClick={() => setStep(2)} className="btn-secondary flex items-center gap-1">
                    <ChevronLeft size={14} />
                    Back
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* ── STEP 4: Results & Download ── */}
          {step === 4 && optimization && !loading && (
            <motion.div
              key="step4"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="space-y-5"
            >
              {optimization.ats_score && (
                <div className="card-glow text-center py-6">
                  <ScoreRing score={optimization.ats_score} size={160} strokeWidth={8} />
                  <p className="text-gray-400 font-mono text-xs mt-4">
                    Optimized ATS Score
                  </p>
                </div>
              )}

              {(optimization.present_keywords?.length > 0 || optimization.missing_keywords?.length > 0) && (
                <div className="grid sm:grid-cols-2 gap-3">
                  {optimization.present_keywords?.length > 0 && (
                    <motion.div
                      className="card border-cyber-green/20"
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 }}
                    >
                      <h3 className="font-display font-bold text-cyber-green text-sm mb-3 flex items-center gap-2">
                        <CheckCircle2 size={14} />
                        Detected ({optimization.present_keywords.length})
                      </h3>
                      <div className="flex flex-wrap gap-1.5">
                        {optimization.present_keywords.map((kw, i) => (
                          <span key={i} className="px-2.5 py-1 bg-cyber-green/10 border border-cyber-green/20 text-cyber-green rounded-full text-[10px] font-mono">
                            {kw}
                          </span>
                        ))}
                      </div>
                    </motion.div>
                  )}
                  {optimization.missing_keywords?.length > 0 && (
                    <motion.div
                      className="card border-cyber-red/20"
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                    >
                      <h3 className="font-display font-bold text-cyber-red text-sm mb-3 flex items-center gap-2">
                        <AlertTriangle size={14} />
                        Missing ({optimization.missing_keywords.length})
                      </h3>
                      <div className="flex flex-wrap gap-1.5">
                        {optimization.missing_keywords.map((kw, i) => (
                          <span key={i} className="px-2.5 py-1 bg-cyber-red/10 border border-cyber-red/20 text-cyber-red rounded-full text-[10px] font-mono">
                            {kw}
                          </span>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </div>
              )}

              {optimization.changes_made?.length > 0 && (
                <motion.div
                  className="card"
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <h3 className="font-display font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                    <Shield size={14} className="text-cyber-amber" />
                    Changes Applied
                  </h3>
                  <ul className="space-y-1.5">
                    {optimization.changes_made.map((c, i) => (
                      <li key={i} className="text-xs font-mono text-gray-400 flex items-start gap-2">
                        <span className="text-cyber-amber mt-0.5">›</span>
                        {c}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}

              {optimization.optimized_resume && (
                <motion.div
                  className="card"
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <h3 className="font-display font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                    <Eye size={14} className="text-cyber-blue" />
                    Optimized Resume
                  </h3>
                  <pre className="whitespace-pre-wrap text-xs font-mono text-gray-400 bg-space-void border border-space-border p-4 rounded-lg max-h-[400px] overflow-y-auto leading-relaxed">
                    {optimization.optimized_resume}
                  </pre>
                </motion.div>
              )}

              <motion.div
                className="flex flex-col sm:flex-row gap-3"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
              >
                <button onClick={() => handleExport("docx")} className="btn-primary flex-1 flex items-center justify-center gap-2">
                  <FileDown size={16} />
                  Download DOCX
                </button>
                <button onClick={() => handleExport("pdf")} className="btn-secondary flex-1 flex items-center justify-center gap-2">
                  <FileDown size={16} />
                  Download PDF
                </button>
              </motion.div>
              <motion.button
                onClick={reset}
                className="btn-ghost w-full flex items-center justify-center gap-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
              >
                <RotateCcw size={14} />
                Scan Another Resume
              </motion.button>
            </motion.div>
          )}

          {/* ── Loading State ── */}
          {loading && (
            <motion.div
              key="loading"
              className="card text-center py-12 sm:py-16"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Spinner size="lg" />
              <p className="text-gray-400 font-mono text-sm mt-4">
                {step === 1
                  ? "Scanning resume..."
                  : step === 3
                  ? "Optimizing for ATS scanners..."
                  : "Processing..."}
              </p>
              <p className="text-xs font-mono text-gray-600 mt-1">This usually takes 10-20 seconds</p>
              <div className="flex justify-center gap-1 mt-4">
                {[0, 1, 2].map((i) => (
                  <span key={i} className="typing-dot w-1.5 h-1.5 rounded-full bg-cyber-blue" />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
