import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { DollarSign, TrendingUp, CheckCircle, XCircle } from "lucide-react";

export default function SalaryNegotiation() {
  const [form, setForm] = useState({
    job_title: "",
    offered_salary: "",
    location: "",
    years_experience: 0,
    company_size: "",
    benefits: [],
  });
  const [tips, setTips] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const companySizes = ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1000+)"];

  const handleSubmit = async () => {
    if (!form.job_title || !form.offered_salary || !form.location) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.getSalaryNegotiationTips(
        form.job_title,
        form.offered_salary,
        form.location,
        form.years_experience,
        form.company_size,
        form.benefits
      );
      setTips(data);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-10"
        >
          <div className="w-16 h-16 bg-cyber-green/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <DollarSign className="text-cyber-green" size={32} />
          </div>
          <h1 className="section-header text-3xl mb-2">
            Salary <span className="text-cyber-green">Negotiation</span>
          </h1>
          <p className="text-gray-400 mt-2">
            Get AI-powered tips to negotiate the best possible offer
          </p>
        </motion.div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
            {error}
          </div>
        )}

        {!tips ? (
          <div className="card">
            <h2 className="text-xl font-bold mb-6">Enter Your Offer Details</h2>
            <div className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Job Title *</label>
                  <input
                    className="input"
                    placeholder="e.g. Software Engineer"
                    value={form.job_title}
                    onChange={(e) => setForm({ ...form, job_title: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Offered Salary *</label>
                  <input
                    className="input"
                    placeholder="e.g. $85,000 or ₹12,00,000"
                    value={form.offered_salary}
                    onChange={(e) => setForm({ ...form, offered_salary: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Location *</label>
                  <input
                    className="input"
                    placeholder="e.g. San Francisco, CA or Bangalore, India"
                    value={form.location}
                    onChange={(e) => setForm({ ...form, location: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Years of Experience</label>
                  <input
                    type="number"
                    className="input"
                    min="0"
                    max="30"
                    value={form.years_experience}
                    onChange={(e) => setForm({ ...form, years_experience: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Company Size</label>
                <div className="flex flex-wrap gap-2">
                  {companySizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => setForm({ ...form, company_size: size })}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        form.company_size === size
                          ? "bg-cyber-green text-space-void"
                          : "bg-space-panel border border-space-border text-gray-500"
                      }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={handleSubmit}
                disabled={!form.job_title || !form.offered_salary || !form.location || loading}
                className="w-full btn-primary"
              >
                {loading ? <Spinner size="sm" className="inline mr-2" /> : null}
                Analyze Offer
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {tips.market_research && (
              <div className="card border-cyber-blue/20 bg-cyber-blue/5">
                <h3 className="font-bold text-text-primary mb-2 flex items-center gap-2">
                  <TrendingUp size={20} /> Market Research
                </h3>
                <p className="text-gray-400">{tips.market_research}</p>
              </div>
            )}

            {tips.negotiation_points?.length > 0 && (
              <div className="card">
                <h3 className="font-bold mb-3">Key Negotiation Points</h3>
                <ul className="space-y-2">
                  {tips.negotiation_points.map((point, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-400 font-mono text-xs">
                      <span className="text-cyber-green mt-1">•</span> {point}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {tips.scripts && (
              <div className="card">
                <h3 className="font-bold mb-4">Negotiation Scripts</h3>
                <div className="space-y-4">
                      {Object.entries(tips.scripts).map(([key, script]: [string, any]) => (
                    <div key={key} className="bg-space-void border border-space-border rounded-lg p-4">
                      <p className="font-semibold text-sm text-gray-400 mb-2 capitalize">
                        {key.replace("_", " ")}:
                      </p>
                      <p className="font-mono text-xs italic text-gray-400">"{script}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="grid sm:grid-cols-2 gap-4">
              {tips.dos?.length > 0 && (
                <div className="card border-cyber-green/20 bg-cyber-green/5">
                  <h3 className="font-bold text-cyber-green mb-3 flex items-center gap-2">
                    <CheckCircle size={18} /> Do's
                  </h3>
                  <ul className="space-y-2">
                    {tips.dos.map((item, i) => (
                      <li key={i} className="text-cyber-green text-sm flex items-start gap-2">
                        <span>✓</span> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {tips.donts?.length > 0 && (
                <div className="card border-cyber-red/20 bg-cyber-red/5">
                  <h3 className="font-bold text-cyber-red mb-3 flex items-center gap-2">
                    <XCircle size={18} /> Don'ts
                  </h3>
                  <ul className="space-y-2">
                    {tips.donts.map((item, i) => (
                      <li key={i} className="text-cyber-red text-sm flex items-start gap-2">
                        <span>✗</span> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {tips.total_compensation_tips?.length > 0 && (
              <div className="card">
                <h3 className="font-bold mb-3">Total Compensation Tips</h3>
                <ul className="space-y-2">
                  {tips.total_compensation_tips.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-400 font-mono text-xs">
                      <span className="text-cyber-green mt-1">•</span> {tip}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex gap-4">
              <button onClick={() => setTips(null)} className="flex-1 btn-primary text-center">
                New Analysis
              </button>
              <Link to="/dashboard" className="flex-1 btn-secondary text-center">
                Command Deck
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
