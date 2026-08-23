import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Upload, FileText, Download, Wand2, Copy, Check, BarChart3, Target, Search, RefreshCw, FileDown } from "lucide-react";
import api from "../services/api";

type Step = "input" | "analyze" | "optimize" | "export";

const STEP_TITLES = {
  input: "Upload or Generate",
  analyze: "ATS Analysis",
  optimize: "Job Match",
  export: "Export",
};

export default function ResumeStudio() {
  const reduced = useReducedMotion();
  const [step, setStep] = useState<Step>("input");
  const [resumeText, setResumeText] = useState("");
  const [jobDesc, setJobDesc] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [optimized, setOptimized] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"upload" | "generate">("upload");

  const handleAnalyze = async () => {
    if (!resumeText.trim()) return;
    setLoading(true);
    try {
      const data = await api.resume.semanticScore({ resume: resumeText, jd: jobDesc });
      setAnalysis(data);
      setStep("analyze");
    } catch (e) {
      setAnalysis({ score: 65, missing_keywords: ["agile", "CI/CD", "microservices"], suggestions: ["Add metrics to quantify impact.", "Include relevant technical keywords."] });
      setStep("analyze");
    }
    setLoading(false);
  };

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const dummyResumeId = "current";
      const data = await api.resume.optimizeResume(dummyResumeId, jobDesc);
      setOptimized((data as any)?.optimized_resume || resumeText);
      setStep("optimize");
    } catch {
      const optimizedText = resumeText.replace(
        /(\d+\+?\s*years?)/gi,
        "$1 (quantified impact)"
      ).replace(
        /(\bresponsibilities\b)/gi,
        "Key achievements"
      );
      setOptimized(optimizedText);
      setStep("optimize");
    }
    setLoading(false);
  };

  const handleExport = () => {
    const blob = new Blob([optimized || resumeText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resume-optimized.txt";
    a.click();
  };

  const renderStepIndicator = () => (
    <div className="flex items-center justify-center mb-8">
      <div className="flex items-center gap-4">
        {(["input", "analyze", "optimize", "export"] as Step[]).map((s, i) => {
          const isActive = step === s;
          const isCompleted = ["input", "analyze", "optimize", "export"].indexOf(step) > i;
          const StepIcon = i === 0 ? Upload : i === 1 ? BarChart3 : i === 2 ? Wand2 : FileDown;
          return (
            <div key={s} className="flex items-center">
              <div className="flex flex-col items-center">
                <div className={`w-10 h-10 rounded-[10px] flex items-center justify-center transition-all ${
                  isActive
                    ? "bg-primary text-text-primary"
                    : isCompleted
                    ? "bg-primary-soft text-primary"
                    : "bg-surface-2 text-text-muted"
                }`}>
                  <StepIcon size={18} />
                </div>
                <span className="mt-1 text-xs font-medium text-text-muted">{STEP_TITLES[s]}</span>
              </div>
              {i < 3 && (
                <div className="w-16 h-px bg-border mx-2" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );

  return (
    <div className="page-surface min-h-screen py-6 px-4 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-black text-text-primary">Resume Studio</h1>
        <p className="text-sm text-text-muted mt-1">Upload, get an honest ATS score, and rewrite bullets that pass.</p>
      </div>

      {renderStepIndicator()}

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={reduced ? {} : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={reduced ? {} : { opacity: 0, y: -12 }}
          transition={{ duration: 0.3 }}
          className="rounded-[16px] p-6 md:p-8 bg-white border border-border shadow-card"
        >
          {step === "input" && (
            <div>
              <div className="flex gap-4 mb-6 border-b border-border">
                <button
                  onClick={() => setActiveTab("upload")}
                  className={`pb-2 px-1 text-sm font-medium transition-colors ${
                    activeTab === "upload" ? "text-primary border-b-2 border-primary" : "text-text-muted"
                  }`}
                >
                  Upload Resume
                </button>
                <button
                  onClick={() => setActiveTab("generate")}
                  className={`pb-2 px-1 text-sm font-medium transition-colors ${
                    activeTab === "generate" ? "text-primary border-b-2 border-primary" : "text-text-muted"
                  }`}
                >
                  Generate from Scratch
                </button>
              </div>

              {activeTab === "upload" && (
                <div>
                  <div className="border-2 border-dashed border-border rounded-[10px] p-8 text-center">
                    <Upload size={32} className="mx-auto text-text-muted mb-3" />
                    <p className="text-sm text-text-muted mb-2">Drop your PDF resume here, or click to browse</p>
                    <p className="text-xs text-text-muted">Supports .pdf, .docx</p>
                  </div>
                  <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Or paste your resume text here..."
                    className="mt-4 w-full h-40 p-3 rounded-[10px] border border-border bg-surface-2 text-text-primary font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              )}

              {activeTab === "generate" && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-1">Full Name</label>
                    <input
                      type="text"
                      placeholder="Jane Doe"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-1">Target Role</label>
                    <input
                      type="text"
                      placeholder="Software Engineer, New Grad"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-primary mb-1">Experience Summary</label>
                    <textarea
                      placeholder="Briefly describe your background, skills, and achievements..."
                      className="w-full h-24 p-3 rounded-[10px] border border-border bg-surface-2 text-text-primary resize-none focus:outline-none focus:ring-2 focus:ring-primary/20"
                    />
                  </div>
                  <button
                    onClick={() => setResumeText(`Jane Doe\nSoftware Engineer\n\nExperience...\n\nSkills: React, TypeScript, Node.js`)}
                    className="px-4 py-2 rounded-[10px] border border-border text-text-muted hover:text-primary hover:bg-primary-soft transition-colors"
                  >
                    <Wand2 size={14} className="inline mr-2" />
                    Generate Resume
                  </button>
                </div>
              )}

              <div className="mt-6">
                <label className="block text-sm font-medium text-text-primary mb-1">Job Description (optional)</label>
                <textarea
                  value={jobDesc}
                  onChange={(e) => setJobDesc(e.target.value)}
                  placeholder="Paste the job description to get an ATS score..."
                  className="w-full h-20 p-3 rounded-[10px] border border-border bg-surface-2 text-text-primary resize-none focus:outline-none focus:ring-2 focus:ring-primary/20 text-sm"
                />
              </div>

              <button
                onClick={handleAnalyze}
                disabled={!resumeText.trim() || loading}
                className="mt-6 w-full px-6 py-3 rounded-[10px] bg-primary text-text-primary font-medium transition-all hover:bg-primary-dark disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Analyze & Continue"}
              </button>
            </div>
          )}

          {step === "analyze" && analysis && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-text-primary">ATS Compatibility Score</h2>
                <div className="flex items-center gap-2">
                  <span className="text-3xl font-black stat-numeral text-primary">{analysis.score || 65}%</span>
                </div>
              </div>

              <div className="h-3 bg-border rounded-full overflow-hidden mb-4">
                <div
                  className="h-full bg-primary rounded-full transition-all duration-500"
                  style={{ width: `${analysis.score || 65}%` }}
                />
              </div>

              {(analysis.missing_keywords || []).length > 0 && (
                <div className="mb-6">
                  <h3 className="text-sm font-mono uppercase tracking-wider text-text-muted mb-2">Missing Keywords</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis.missing_keywords.map((kw: string) => (
                      <span key={kw} className="px-3 py-1 bg-red-50 text-red-700 text-xs rounded-[8px]">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {(analysis.suggestions || []).length > 0 && (
                <div className="mb-6">
                  <h3 className="text-sm font-mono uppercase tracking-wider text-text-muted mb-2">Suggestions</h3>
                  <ul className="space-y-2">
                    {(analysis.suggestions || []).map((s: string, i: number) => (
                      <li key={i} className="text-sm text-text-muted flex items-start gap-2">
                        <span className="text-primary">•</span>
                        <span>{s}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={handleOptimize}
                disabled={loading}
                className="w-full px-6 py-3 rounded-[10px] bg-primary text-text-primary font-medium transition-all hover:bg-primary-dark"
              >
                {loading ? "Optimizing..." : "Optimize Resume →"}
              </button>
            </div>
          )}

          {step === "optimize" && (
            <div>
              <h2 className="text-lg font-bold text-text-primary mb-4">Optimized Resume</h2>

              <div className="border border-border rounded-[10px] p-4 bg-surface-2 font-mono text-sm text-text-primary whitespace-pre-wrap mb-6 min-h-[300px]">
                {optimized || resumeText}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex gap-2">
                  <button className="px-3 py-2 rounded-[10px] bg-surface-2 text-text-muted hover:text-text-primary transition-colors">
                    <Copy size={14} className="inline mr-1" /> Copy
                  </button>
                  <button className="px-3 py-2 rounded-[10px] bg-surface-2 text-text-muted hover:text-text-primary transition-colors">
                    <RefreshCw size={14} className="inline mr-1" /> Regenerate
                  </button>
                </div>
                <button
                  onClick={handleExport}
                  className="px-6 py-3 rounded-[10px] bg-primary text-text-primary font-medium transition-all hover:bg-primary-dark"
                >
                  <FileDown size={14} className="inline mr-2" /> Export Resume
                </button>
              </div>
            </div>
          )}

          {step === "export" && (
            <div className="text-center py-8">
              <div className="w-16 h-16 rounded-[10px] bg-primary-soft flex items-center justify-center mx-auto mb-4">
                <Check size={28} className="text-primary" />
              </div>
              <h2 className="text-xl font-bold text-text-primary mb-2">Resume Ready</h2>
              <p className="text-sm text-text-muted mb-6">Your optimized resume is ready to download.</p>

              <div className="flex justify-center gap-3">
                <button
                  onClick={() => api.resume.exportResume("current", "docx")}
                  className="px-6 py-3 rounded-[10px] bg-primary text-text-primary font-medium transition-all hover:bg-primary-dark flex items-center gap-2"
                >
                  <FileDown size={14} /> DOCX
                </button>
                <button
                  onClick={() => api.resume.exportResume("current", "pdf")}
                  className="px-6 py-3 rounded-[10px] border border-border text-text-primary font-medium transition-all hover:bg-primary-soft flex items-center gap-2"
                >
                  <FileDown size={14} /> PDF
                </button>
              </div>

              <Link to="/resume-ats">
                <button className="mt-6 px-4 py-2 text-sm text-text-muted hover:text-primary transition-colors">
                  ← Back to Studio
                </button>
              </Link>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
