import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { Mail, Copy, Check } from "lucide-react";

export default function CoverLetter() {
  const [resumeId, setResumeId] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [coverLetter, setCoverLetter] = useState("");
  const [linkedinAbout, setLinkedinAbout] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState("cover-letter");

  const handleUploadResume = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.uploadResume(file);
      setResumeId(data.resume_id);
      setResumeText(data.text);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleGenerateCoverLetter = async () => {
    if (!resumeId || !jobDescription.trim()) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.generateCoverLetter(resumeId, jobDescription, companyName);
      setCoverLetter(data.cover_letter);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleGenerateLinkedIn = async () => {
    if (!resumeId) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.generateLinkedInAbout(resumeId, companyName);
      setLinkedinAbout(data.linkedin_about);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <div className="w-16 h-16 bg-cyber-blue/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Mail className="text-cyber-blue" size={32} />
          </div>
          <span className="section-subheader mb-3 block">Communication Relay</span>
          <h1 className="section-header text-3xl mb-2">
            Cover <span className="text-cyber-blue">Letter</span> & LinkedIn
          </h1>
          <p className="text-gray-400 mt-2">
            Generate tailored cover letters and LinkedIn content with AI
          </p>
        </motion.div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
            {error}
          </div>
        )}

        {!resumeId ? (
          <div className="card">
            <h2 className="text-xl font-display font-bold text-text-primary mb-4">Upload Your Resume</h2>
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center">
              <input
                type="file"
                accept=".pdf"
                onChange={handleUploadResume}
                className="hidden"
                id="cl-upload"
              />
              <label htmlFor="cl-upload" className="cursor-pointer">
                <Mail className="mx-auto text-gray-400 mb-3" size={40} />
                <p className="text-gray-400">Click to upload PDF resume</p>
                <p className="text-sm text-gray-500 mt-1">Max 5MB</p>
              </label>
            </div>
          </div>
        ) : (
          <>
            <div className="flex gap-4 mb-6">
              <button
                onClick={() => setActiveTab("cover-letter")}
                className={`flex-1 py-3 rounded-lg font-semibold transition-colors ${
                  activeTab === "cover-letter" ? "bg-cyber-blue text-space-void" : "bg-space-panel border border-gray-200 text-gray-500"
                }`}
              >
                Cover Letter
              </button>
              <button
                onClick={() => setActiveTab("linkedin")}
                className={`flex-1 py-3 rounded-lg font-semibold transition-colors ${
                  activeTab === "linkedin" ? "bg-cyber-blue text-space-void" : "bg-space-panel border border-gray-200 text-gray-500"
                }`}
              >
                LinkedIn About
              </button>
            </div>

            {activeTab === "cover-letter" && !coverLetter && (
              <div className="card">
                <h2 className="text-xl font-display font-bold text-text-primary mb-4">Generate Cover Letter</h2>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-4">
                  <p className="text-xs font-mono text-gray-400">
                    Resume uploaded: <span className="text-text-primary">{resumeText.substring(0, 80)}...</span>
                  </p>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Company Name (optional)</label>
                    <input
                      className="input"
                      placeholder="e.g. Google, Microsoft, Amazon"
                      value={companyName}
                      onChange={(e) => setCompanyName(e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Job Description *</label>
                    <textarea
                      className="input min-h-[150px] resize-y"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                    />
                  </div>
                  <button
                    onClick={handleGenerateCoverLetter}
                    disabled={!jobDescription.trim() || loading}
                    className="w-full btn-primary"
                  >
                    {loading ? <Spinner size="sm" className="inline mr-2" /> : null}
                    Transmit Cover Letter
                  </button>
                </div>
              </div>
            )}

            {activeTab === "cover-letter" && coverLetter && (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-display font-bold text-text-primary">Your Cover Letter</h2>
                  <button
                    onClick={() => copyToClipboard(coverLetter)}
                    className="flex items-center gap-2 text-sm text-cyber-blue hover:text-cyber-blue/80"
                  >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                    {copied ? "Copied!" : "Copy"}
                  </button>
                </div>
                <pre className="whitespace-pre-wrap text-xs font-mono text-gray-700 bg-gray-50 border border-gray-200 p-4 rounded-lg max-h-[500px] overflow-y-auto">
                  {coverLetter}
                </pre>
                <div className="flex gap-4 mt-4">
                  <button onClick={() => setCoverLetter("")} className="btn-ghost">
                    New Transmission
                  </button>
                  <Link to="/dashboard" className="btn-ghost">
                    Command Deck
                  </Link>
                </div>
              </div>
            )}

            {activeTab === "linkedin" && !linkedinAbout && (
              <div className="card">
                <h2 className="text-xl font-display font-bold text-text-primary mb-4">Generate LinkedIn About Section</h2>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-4">
                  <p className="text-xs font-mono text-gray-400">
                    Resume uploaded: <span className="text-text-primary">{resumeText.substring(0, 80)}...</span>
                  </p>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Target Role (optional)</label>
                    <input
                      className="input"
                      placeholder="e.g. Senior Software Engineer"
                      value={companyName}
                      onChange={(e) => setCompanyName(e.target.value)}
                    />
                  </div>
                  <button
                    onClick={handleGenerateLinkedIn}
                    disabled={loading}
                    className="w-full btn-primary"
                  >
                    {loading ? <Spinner size="sm" className="inline mr-2" /> : null}
                    Transmit LinkedIn About
                  </button>
                </div>
              </div>
            )}

            {activeTab === "linkedin" && linkedinAbout && (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-display font-bold text-text-primary">Your LinkedIn About Section</h2>
                  <button
                    onClick={() => copyToClipboard(linkedinAbout)}
                    className="flex items-center gap-2 text-sm text-cyber-blue hover:text-cyber-blue/80"
                  >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                    {copied ? "Copied!" : "Copy"}
                  </button>
                </div>
                <pre className="whitespace-pre-wrap text-xs font-mono text-gray-700 bg-gray-50 border border-gray-200 p-4 rounded-lg max-h-[300px] overflow-y-auto">
                  {linkedinAbout}
                </pre>
                <div className="flex gap-4 mt-4">
                  <button onClick={() => setLinkedinAbout("")} className="btn-ghost">
                    New Transmission
                  </button>
                  <Link to="/dashboard" className="btn-ghost">
                    Command Deck
                  </Link>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
