import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { Upload, FileText, Download, Wand2, Copy, Check } from "lucide-react";

export default function ResumeBuilder() {
  const [mode, setMode] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState(null);
  const [resumeId, setResumeId] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [bulletRole, setBulletRole] = useState("");
  const [bulletsInput, setBulletsInput] = useState("");
  const [bulletResults, setBulletResults] = useState([]);
  const [improving, setImproving] = useState(false);
  const [bulletError, setBulletError] = useState("");
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    target_role: "",
    experience: [{ company: "", role: "", duration: "", bullets: "" }],
    education: [{ school: "", degree: "", year: "" }],
    skills: "",
  });

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.uploadResume(file);
      setAnalysis(data.analysis);
      setResumeId(data.resume_id);
      setResumeText(data.text);
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
      setResumeText(data.content);
      setResumeId(data.resume_id);
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
      a.download = `resume.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert("Export failed: " + err.message);
    }
  };

  const handleImproveBullets = async () => {
    const bullets = bulletsInput.split("\n").map((b) => b.trim()).filter(Boolean);
    if (!bullets.length) {
      setBulletError("Paste at least one bullet point.");
      return;
    }
    setImproving(true);
    setBulletError("");
    setBulletResults([]);
    try {
      const data = await api.improveBullets(bullets, bulletRole.trim());
      setBulletResults(data.improvements || []);
    } catch (err: any) {
      setBulletError(err.message || "Improvement failed. Free tier allows 3 per day.");
    }
    setImproving(false);
  };

  const copyBullet = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 1500);
    } catch {}
  };

  const copyAllBullets = async () => {
    const all = bulletResults.map((r: any) => r.improved).join("\n");
    try {
      await navigator.clipboard.writeText(all);
      setCopiedIndex(-1);
      setTimeout(() => setCopiedIndex(null), 1500);
    } catch {}
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-cyber-green bg-cyber-green/10";
    if (score >= 60) return "text-cyber-yellow bg-cyber-yellow/10";
    return "text-cyber-red bg-cyber-red/10";
  };

  if (resumeText) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="section-header text-3xl mb-2">Your Resume</h1>

          {analysis && (
            <div className="card mb-6">
              <h2 className="section-header text-xl mb-4">Analysis Results</h2>
              <div className="flex items-center gap-4 mb-4">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center text-2xl font-bold ${getScoreColor(analysis.overall_score)}`}>
                  {analysis.overall_score}
                </div>
                <p className="text-gray-400">Overall Resume Score</p>
              </div>
              <div className="grid sm:grid-cols-2 gap-4 mb-4">
                {Object.entries(analysis.sections || {}).map(([key, val]: [string, any]) => (
                  <div key={key} className="bg-space-void rounded-lg p-3">
                    <p className="text-sm font-mono uppercase tracking-wider text-gray-400 capitalize">{key}</p>
                    <p className={`text-lg font-bold ${getScoreColor(val.score)}`}>{val.score}/100</p>
                    <p className="text-xs text-gray-500">{val.feedback}</p>
                  </div>
                ))}
              </div>
              {analysis.improvements?.length > 0 && (
                <div>
                  <p className="font-mono uppercase tracking-wider text-gray-400 mb-2">Improvements Needed:</p>
                  <ul className="space-y-1">
                    {analysis.improvements.map((imp, i) => (
                      <li key={i} className="text-sm text-gray-400 flex items-start gap-2">
                        <span className="text-cyber-amber">•</span> {imp}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          <div className="card mb-6">
            <h2 className="section-header text-xl mb-4">Resume Content</h2>
            <pre className="whitespace-pre-wrap text-sm text-gray-300 bg-space-void p-4 rounded-lg max-h-96 overflow-y-auto font-mono">
              {resumeText}
            </pre>
          </div>

          <div className="flex flex-wrap gap-4">
            <button onClick={() => handleExport("docx")} className="btn-primary flex items-center gap-2">
              <Download size={18} /> Export DOCX
            </button>
            <button onClick={() => handleExport("pdf")} className="btn-secondary flex items-center gap-2">
              <Download size={18} /> Export PDF
            </button>
            <Link to="/ats" className="btn-ghost">
              Hull Scan →
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <div className="w-16 h-16 bg-cyber-green/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <FileText className="text-cyber-green" size={32} />
          </div>
          <span className="section-subheader mb-3 block">Hull Registry</span>
          <h1 className="section-header text-3xl mb-2">Resume Fabricator</h1>
          <p className="text-gray-400 mt-2">
            Upload an existing resume or let AI generate one for you
          </p>
        </motion.div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
            {error}
          </div>
        )}

        {!mode && (
          <div className="grid sm:grid-cols-2 gap-6">
            <button
              onClick={() => setMode("upload")}
              className="card text-left hover:shadow-lg transition-shadow border-2 border-transparent hover:border-cyber-green/40"
            >
              <Upload className="text-cyber-green mb-3" size={32} />
              <h3 className="section-header text-lg mb-2">Upload Resume</h3>
              <p className="text-sm text-gray-400">
                Upload your existing PDF resume. AI will analyze and score it.
              </p>
            </button>
            <button
              onClick={() => setMode("generate")}
              className="card text-left hover:shadow-lg transition-shadow border-2 border-transparent hover:border-cyber-green/40"
            >
              <FileText className="text-cyber-green mb-3" size={32} />
              <h3 className="section-header text-lg mb-2">Generate New</h3>
              <p className="text-sm text-gray-400">
                Fill in your details. AI will write a professional resume for you.
              </p>
            </button>
            <button
              onClick={() => setMode("improve")}
              className="card text-left hover:shadow-lg transition-shadow border-2 border-transparent hover:border-cyber-green/40 sm:col-span-2"
            >
              <Wand2 className="text-cyber-green mb-3" size={32} />
              <h3 className="section-header text-lg mb-2">Bullet Improver</h3>
              <p className="text-sm text-gray-400">
                Paste weak resume bullets. AI rewrites them with strong action verbs, metrics, and impact.
              </p>
            </button>
          </div>
        )}

        {mode === "upload" && !loading && (
          <div className="card">
            <h2 className="section-header text-xl mb-4">Upload Your Resume</h2>
            <div className="border-2 border-dashed border-space-border rounded-lg p-8 text-center mb-4">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
                id="resume-upload"
              />
              <label htmlFor="resume-upload" className="cursor-pointer">
                <Upload className="mx-auto text-gray-500 mb-3" size={40} />
                <p className="text-gray-400">
                  {file ? file.name : "Click to select PDF (max 5MB)"}
                </p>
              </label>
            </div>
            <div className="flex gap-4">
              <button onClick={handleUpload} disabled={!file} className="btn-primary flex-1">
                Scan Resume
              </button>
              <button onClick={() => setMode(null)} className="btn-ghost">
                Back
              </button>
            </div>
          </div>
        )}

        {mode === "generate" && !loading && (
          <div className="card">
            <h2 className="section-header text-xl mb-6">Generate Resume with AI</h2>
            <div className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Full Name</label>
                  <input
                    className="input"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Email</label>
                  <input
                    className="input"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    placeholder="john@example.com"
                  />
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Phone</label>
                  <input
                    className="input"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Target Role</label>
                  <input
                    className="input"
                    value={form.target_role}
                    onChange={(e) => setForm({ ...form, target_role: e.target.value })}
                    placeholder="e.g. Software Engineer"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">
                  Skills (comma separated)
                </label>
                <input
                  className="input"
                  value={form.skills}
                  onChange={(e) => setForm({ ...form, skills: e.target.value })}
                  placeholder="Python, JavaScript, React, Node.js"
                />
              </div>

              {/* Experience Section */}
              <div>
                <p className="font-mono text-xs uppercase tracking-wider text-gray-400 mb-3">Experience</p>
                {form.experience.map((exp, i) => (
                  <div key={i} className="bg-space-void rounded-lg p-4 space-y-3 mb-3">
                    <p className="text-xs text-gray-500 font-mono">Experience {i + 1}</p>
                    <div className="grid sm:grid-cols-2 gap-3">
                      <input
                        className="input"
                        placeholder="Company"
                        value={exp.company}
                        onChange={(e) => {
                          const newExp = [...form.experience];
                          newExp[i].company = e.target.value;
                          setForm({ ...form, experience: newExp });
                        }}
                      />
                      <input
                        className="input"
                        placeholder="Role"
                        value={exp.role}
                        onChange={(e) => {
                          const newExp = [...form.experience];
                          newExp[i].role = e.target.value;
                          setForm({ ...form, experience: newExp });
                        }}
                      />
                    </div>
                    <input
                      className="input"
                      placeholder="Duration (e.g. Jan 2022 - Present)"
                      value={exp.duration}
                      onChange={(e) => {
                        const newExp = [...form.experience];
                        newExp[i].duration = e.target.value;
                        setForm({ ...form, experience: newExp });
                      }}
                    />
                    <textarea
                      className="input min-h-[80px]"
                      placeholder="Key achievements (one per line)&#10;- Led team of 5 engineers&#10;- Reduced load time by 40%"
                      value={exp.bullets}
                      onChange={(e) => {
                        const newExp = [...form.experience];
                        newExp[i].bullets = e.target.value;
                        setForm({ ...form, experience: newExp });
                      }}
                    />
                  </div>
                ))}
                <button
                  onClick={() =>
                    setForm({
                      ...form,
                      experience: [...form.experience, { company: "", role: "", duration: "", bullets: "" }],
                    })
                  }
                  className="text-sm text-cyber-green font-mono hover:underline"
                >
                  + Add Another Experience
                </button>
              </div>

              {/* Education Section */}
              <div>
                <p className="font-mono text-xs uppercase tracking-wider text-gray-400 mb-3">Education</p>
                {form.education.map((edu, i) => (
                  <div key={i} className="bg-space-void rounded-lg p-4 space-y-3 mb-3">
                    <p className="text-xs text-gray-500 font-mono">Education {i + 1}</p>
                    <div className="grid sm:grid-cols-3 gap-3">
                      <input
                        className="input"
                        placeholder="School / University"
                        value={edu.school}
                        onChange={(e) => {
                          const newEdu = [...form.education];
                          newEdu[i].school = e.target.value;
                          setForm({ ...form, education: newEdu });
                        }}
                      />
                      <input
                        className="input"
                        placeholder="Degree"
                        value={edu.degree}
                        onChange={(e) => {
                          const newEdu = [...form.education];
                          newEdu[i].degree = e.target.value;
                          setForm({ ...form, education: newEdu });
                        }}
                      />
                      <input
                        className="input"
                        placeholder="Year (e.g. 2020-2024)"
                        value={edu.year}
                        onChange={(e) => {
                          const newEdu = [...form.education];
                          newEdu[i].year = e.target.value;
                          setForm({ ...form, education: newEdu });
                        }}
                      />
                    </div>
                  </div>
                ))}
                <button
                  onClick={() =>
                    setForm({
                      ...form,
                      education: [...form.education, { school: "", degree: "", year: "" }],
                    })
                  }
                  className="text-sm text-cyber-green font-mono hover:underline"
                >
                  + Add Another Education
                </button>
              </div>

              <div className="flex gap-4 pt-4">
                <button onClick={handleGenerate} className="btn-primary flex-1">
                  Fabricate Resume
                </button>
                <button onClick={() => setMode(null)} className="btn-ghost">
                  Back
                </button>
              </div>
            </div>
          </div>
        )}

        {mode === "improve" && !improving && (
          <div className="card">
            <h2 className="section-header text-xl mb-1">Bullet Improver</h2>
            <p className="text-sm text-gray-400 mb-6">
              One bullet per line. Free tier allows 3 improvements per day — Pro is unlimited.
            </p>

            {bulletError && (
              <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-4 text-center font-mono text-sm">
                {bulletError}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Target Role (optional)</label>
                <input
                  className="input"
                  value={bulletRole}
                  onChange={(e) => setBulletRole(e.target.value)}
                  placeholder="e.g. Backend Engineer, SDE-2"
                />
              </div>
              <div>
                <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Your Bullets</label>
                <textarea
                  className="input min-h-[140px] font-mono text-sm"
                  value={bulletsInput}
                  onChange={(e) => setBulletsInput(e.target.value)}
                  placeholder={"- Worked on the backend\n- Helped with the API\n- Responsible for testing"}
                />
              </div>

              <div className="flex gap-4">
                <button onClick={handleImproveBullets} disabled={!bulletsInput.trim()} className="btn-primary flex-1">
                  <Wand2 size={16} className="inline mr-1.5 -mt-0.5" /> Improve Bullets
                </button>
                <button onClick={() => setMode(null)} className="btn-ghost">
                  Back
                </button>
              </div>

              {bulletResults.length > 0 && (
                <div className="pt-4 space-y-4">
                  <div className="flex items-center justify-between">
                    <p className="font-mono text-xs uppercase tracking-wider text-gray-400">Improvements</p>
                    <button
                      onClick={copyAllBullets}
                      className="text-xs text-cyber-green font-mono hover:underline flex items-center gap-1"
                    >
                      {copiedIndex === -1 ? <Check size={13} /> : <Copy size={13} />}
                      {copiedIndex === -1 ? "All copied" : "Copy all"}
                    </button>
                  </div>
                  {bulletResults.map((r, i) => (
                    <div key={i} className="bg-space-void rounded-lg p-4 space-y-3">
                      <div>
                        <p className="text-[10px] font-mono uppercase tracking-wider text-gray-500 mb-1">Before</p>
                        <p className="text-sm text-gray-400">{r.original}</p>
                      </div>
                      <div>
                        <p className="text-[10px] font-mono uppercase tracking-wider text-cyber-green mb-1">After</p>
                        <p className="text-sm text-gray-200 leading-relaxed">{r.improved}</p>
                      </div>
                      {(r.action_verbs?.length > 0 || r.metric_added?.length > 0) && (
                        <div className="flex flex-wrap gap-2 pt-1">
                          {(r.action_verbs || []).slice(0, 3).map((v, vi) => (
                            <span key={`v${vi}`} className="px-2 py-0.5 text-[11px] rounded bg-cyber-green/10 text-cyber-green">{v}</span>
                          ))}
                          {(r.metric_added || []).slice(0, 3).map((m, mi) => (
                            <span key={`m${mi}`} className="px-2 py-0.5 text-[11px] rounded bg-cyber-blue/10 text-cyber-blue">{m}</span>
                          ))}
                        </div>
                      )}
                      <button
                        onClick={() => copyBullet(r.improved, i)}
                        className="text-xs text-cyber-green font-mono hover:underline flex items-center gap-1"
                      >
                        {copiedIndex === i ? <Check size={13} /> : <Copy size={13} />}
                        {copiedIndex === i ? "Copied" : "Copy improved bullet"}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {loading && (
          <div className="card text-center py-12">
            <Spinner size="lg" />
            <p className="text-gray-400 mt-4 font-mono">
              {mode === "upload" ? "Analyzing hull integrity..." : "Fabricating resume..."}
            </p>
            <p className="text-sm text-gray-500 mt-1 font-mono">This usually takes 10-20 seconds</p>
          </div>
        )}
      </div>
    </div>
  );
}
