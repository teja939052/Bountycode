import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { HullScanner } from "../components/space";
import { motion } from "framer-motion";
import { Target, ArrowRight, Brain, BarChart3, AlertTriangle, CheckCircle } from "lucide-react";

export default function ATSOptimizer() {
  const [resumeId, setResumeId] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [optimization, setOptimization] = useState<any>(null);
  const [semanticScore, setSemanticScore] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [step, setStep] = useState(1);
  const [analyzingSemantic, setAnalyzingSemantic] = useState(false);

  const handleUploadResume = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.uploadResume(file);
      setResumeId(data.resume_id);
      setResumeText(data.text);
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
      setStep(3);
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
      a.download = `optimized-resume.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert("Export failed: " + err.message);
    }
  };

  const handleSemanticAnalysis = async () => {
    if (!resumeText || !jobDescription.trim()) return;
    setAnalyzingSemantic(true);
    try {
      const data = await api.getSemanticATS(resumeText, jobDescription);
      setSemanticScore(data);
    } catch {}
    setAnalyzingSemantic(false);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-10"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <span className="section-subheader mb-3 block">Hull Integrity Scanner</span>
          <h1 className="section-header text-3xl mb-2">
            <Target className="text-cyber-orange inline mr-2" size={28} />
            ATS Score <span className="text-cyber-orange">Optimizer</span>
          </h1>
          <p className="text-gray-500 font-mono text-sm">
            Match your resume to any job description. Get ATS-optimized version.
          </p>
        </motion.div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center gap-4 mb-10">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-display font-bold ${step >= s ? "bg-cyber-orange text-space-void" : "bg-space-panel border border-brand-primary/10 text-gray-500"}`}>
                {s}
              </div>
              <span className={`text-xs font-mono ${step >= s ? "text-text-primary" : "text-gray-500"}`}>
                {s === 1 ? "Upload" : s === 2 ? "Paste JD" : "Optimize"}
              </span>
              {s < 3 && <ArrowRight size={12} className="text-brand-secondary" />}
            </div>
          ))}
        </div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">{error}</div>
        )}

        {/* Step 1: Upload */}
        {step === 1 && !loading && (
          <div className="card">
            <h2 className="font-display font-bold text-text-primary text-lg mb-4">Step 1: Upload Resume</h2>
            <div className="border-2 border-dashed border-brand-primary/10 rounded-lg p-8 text-center hover:border-cyber-orange/50 transition-colors">
              <input type="file" accept=".pdf" onChange={handleUploadResume} className="hidden" id="ats-upload" />
              <label htmlFor="ats-upload" className="cursor-pointer">
                <Target className="mx-auto text-gray-500 mb-3" size={40} />
                <p className="text-gray-400 font-mono text-sm">Click to upload PDF resume</p>
                <p className="text-xs text-brand-secondary font-mono mt-1">Max 5MB</p>
              </label>
            </div>
          </div>
        )}

        {/* Step 2: Paste JD */}
        {step === 2 && !loading && (
          <div className="card">
            <h2 className="font-display font-bold text-text-primary text-lg mb-4">Step 2: Paste Mission Parameters</h2>
            <div className="bg-surface-base border border-brand-primary/10 rounded-lg p-3 mb-4">
              <p className="text-xs font-mono text-gray-400">
                Resume loaded: <span className="text-text-primary">{resumeText.substring(0, 80)}...</span>
              </p>
            </div>
            <textarea
              className="input min-h-[200px] resize-y mb-4 font-mono text-sm"
              placeholder="Paste the full job description here...&#10;&#10;Include title, requirements, responsibilities, keywords."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
            <div className="flex gap-4">
              <button onClick={handleOptimize} disabled={!jobDescription.trim()} className="btn-primary flex-1">
                Initiate Scan
              </button>
              <button onClick={() => setStep(1)} className="btn-secondary">Back</button>
            </div>
          </div>
        )}

        {/* Step 3: Results */}
        {step === 3 && optimization && (
          <div className="space-y-6">
            {/* Hull Scanner Display */}
            <HullScanner atsScore={optimization.ats_score} />

            {/* Semantic ATS */}
            {semanticScore && (
              <div className="card border-cyber-purple/20">
                <h3 className="font-display font-bold text-cyber-purple text-sm mb-3 flex items-center gap-2">
                  <Brain size={18} /> Semantic Match
                </h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Overall semantic score</p>
                    <p className="text-2xl font-bold text-text-primary">{semanticScore.semantic?.overall_score ?? 0}%</p>
                    <p className="text-[10px] text-gray-500 font-mono mt-1">Method: {semanticScore.semantic?.method || "n/a"}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Section breakdown</p>
                    <div className="space-y-1">
                      {Object.entries(semanticScore.section_scores || {}).map(([sec, val]: [string, any]) => (
                        <div key={sec} className="flex items-center justify-between text-xs">
                          <span className="capitalize text-gray-400">{sec}</span>
                          <span className="text-text-primary font-mono">{val}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {semanticScore.semantic_gaps?.gaps?.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs font-mono text-gray-400 mb-2">Semantic gaps</p>
                    <div className="space-y-2">
                      {semanticScore.semantic_gaps.gaps.slice(0, 5).map((g, i) => (
                        <div key={i} className="bg-surface-base border border-brand-primary/10 rounded-lg p-3">
                          <p className="text-xs text-gray-300 mb-1">{g.jd_sentence}</p>
                          <p className="text-[10px] text-gray-500 font-mono">Best match: {g.best_resume_match || "None"}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Keywords */}
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="card border-cyber-green/20">
                <h3 className="font-display font-bold text-cyber-green text-sm mb-3">
                  ✅ Detected Keywords ({optimization.present_keywords?.length || 0})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {optimization.present_keywords?.map((kw, i) => (
                    <span key={i} className="px-3 py-1 bg-cyber-green/10 border border-cyber-green/20 text-cyber-green rounded-full text-[10px] font-mono">{kw}</span>
                  ))}
                </div>
              </div>
              <div className="card border-cyber-red/20">
                <h3 className="font-display font-bold text-cyber-red text-sm mb-3">
                  ❌ Missing Keywords ({optimization.missing_keywords?.length || 0})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {optimization.missing_keywords?.map((kw, i) => (
                    <span key={i} className="px-3 py-1 bg-cyber-red/10 border border-cyber-red/20 text-cyber-red rounded-full text-[10px] font-mono">{kw}</span>
                  ))}
                </div>
              </div>
            </div>

            {!semanticScore ? (
              <div className="card">
                <button onClick={handleSemanticAnalysis} disabled={analyzingSemantic} className="btn-primary w-full">
                  {analyzingSemantic ? "Running semantic analysis..." : "Run Semantic Analysis"}
                </button>
                <p className="text-xs text-gray-500 mt-2 text-center">Hybrid scoring: semantic similarity + keyword + formatting checks</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="card bg-gradient-to-r from-cyber-blue/10 to-cyber-purple/10 border border-cyber-blue/20">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-display font-bold text-text-primary flex items-center gap-2">
                      <Brain size={18} className="text-cyber-blue" />
                      Semantic Analysis
                    </h3>
                    <span className="text-xs px-2 py-1 rounded-full bg-cyber-blue/20 text-cyber-blue font-mono">
                      {semanticScore.mode === "semantic" ? "Embedding Model" : "Keyword Fallback"}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {Object.entries(semanticScore.breakdown || {}).map(([key, val]: [string, any]) => (
                      <div key={key} className="bg-surface-base border border-brand-primary/10 rounded-lg p-3 text-center">
                        <p className="text-[10px] font-mono text-gray-400 uppercase tracking-wider mb-1">{key.replace(/_/g, " ")}</p>
                        <p className="text-lg font-bold text-text-primary">{val.score}</p>
                        <p className="text-[10px] font-mono text-gray-500">{val.weight}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {semanticScore.semantic_matches?.length > 0 && (
                  <div className="card border-cyber-green/20">
                    <h3 className="font-display font-bold text-cyber-green text-sm mb-3">Semantic Matches</h3>
                    <div className="space-y-2">
                      {semanticScore.semantic_matches.map((m, i) => (
                        <div key={i} className="bg-surface-base border border-brand-primary/10 rounded-lg p-3">
                          <p className="text-xs text-gray-400 mb-1">JD: {m.jd}</p>
                          <p className="text-xs text-cyber-green">Resume: {m.resume}</p>
                          <p className="text-[10px] font-mono text-gray-500 mt-1">Similarity: {m.score}%</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {semanticScore.semantic_gaps?.length > 0 && (
                  <div className="card border-cyber-orange/20">
                    <h3 className="font-display font-bold text-cyber-orange text-sm mb-3">Semantic Gaps</h3>
                    <div className="space-y-2">
                      {semanticScore.semantic_gaps.map((g, i) => (
                        <div key={i} className="bg-surface-base border border-brand-primary/10 rounded-lg p-3">
                          <p className="text-xs text-gray-400">JD requirement: {g.jd_requirement}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {semanticScore.semantic_sections && Object.keys(semanticScore.semantic_sections).length > 0 && (
                  <div className="card">
                    <h3 className="font-display font-bold text-text-primary text-sm mb-3">Section Similarity</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {Object.entries(semanticScore.semantic_sections).map(([section, score]: [string, any]) => (
                        <div key={section} className="bg-surface-base border border-brand-primary/10 rounded-lg p-3 text-center">
                          <p className="text-[10px] font-mono text-gray-400 uppercase mb-1">{section}</p>
                          <p className="text-lg font-bold text-text-primary">{score}%</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Changes */}
            {optimization.changes_made?.length > 0 && (
              <div className="card">
                <h3 className="font-display font-bold text-text-primary text-sm mb-3">🔧 Modifications Applied</h3>
                <ul className="space-y-2">
                  {optimization.changes_made.map((change, i) => (
                    <li key={i} className="text-xs font-mono text-gray-400 flex items-start gap-2">
                      <span className="text-cyber-orange">•</span> {change}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Optimized Resume */}
            {optimization.optimized_resume && (
              <div className="card">
                <h3 className="font-display font-bold text-text-primary text-sm mb-4">📄 Optimized Manifest</h3>
                <pre className="whitespace-pre-wrap text-xs font-mono text-brand-primary bg-surface-base border border-brand-primary/10 p-4 rounded-lg max-h-96 overflow-y-auto">
                  {optimization.optimized_resume}
                </pre>
              </div>
            )}

            <div className="flex gap-4">
              <button onClick={() => handleExport("docx")} className="btn-primary flex-1">Download DOCX</button>
              <button onClick={() => handleExport("pdf")} className="btn-secondary flex-1">Download PDF</button>
            </div>
            <div className="flex gap-4">
              <button onClick={() => { setStep(1); setOptimization(null); setJobDescription(""); }} className="btn-ghost">← New Scan</button>
              <Link to="/dashboard" className="btn-ghost">Command Deck</Link>
            </div>
          </div>
        )}

        {loading && (
          <div className="card text-center py-12">
            <Spinner size="lg" />
            <p className="text-gray-400 font-mono text-sm mt-4">
              {step === 1 ? "Scanning hull integrity..." : "Optimizing for ATS scanners..."}
            </p>
            <p className="text-xs font-mono text-brand-secondary mt-1">Estimated: 15-30 seconds</p>
          </div>
        )}
      </div>
    </div>
  );
}
