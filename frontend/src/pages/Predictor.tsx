import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import { TrendingUp, Target, Brain, ChevronDown, BarChart3, Zap, Building2, Flame } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import PredictorGauge from "../components/PredictorGauge";
import useReducedMotion from "../hooks/useReducedMotion";

export default function Predictor() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [role, setRole] = useState("SDE");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [companiesLoading, setCompaniesLoading] = useState(true);
  const [history, setHistory] = useState([]);
  const [practiceResult, setPracticeResult] = useState(null);
  const [practicing, setPracticing] = useState(false);
  const reduced = useReducedMotion();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getSupportedCompanies();
        setCompanies(data.companies || data || []);
      } catch {} finally {
        setCompaniesLoading(false);
      }
      try {
        const h = await api.getPredictionHistory();
        setHistory(h.predictions || h || []);
      } catch {}
    };
    load();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!selectedCompany) return;
    setLoading(true);
    try {
      const data = await api.predictOffer(selectedCompany, role);
      setPrediction(data);
    } catch {} finally {
      setLoading(false);
    }
  };

  const handlePracticeForRole = async () => {
    if (!selectedCompany) return;
    setPracticing(true);
    setPracticeResult(null);
    try {
      const data = await api.createPracticeSession({ company: selectedCompany, role });
      setPracticeResult(data);
    } catch {} finally {
      setPracticing(false);
    }
  };

  const probability = prediction?.probability || prediction?.placement_probability || 0;

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-10"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp size={32} className="text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold dark:text-white">Placement Predictor</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">Predict your offer based on skills and company tier</p>
        </motion.div>

        <AnimatedCard className="card mb-8">
          <form onSubmit={handlePredict}>
            <div className="grid md:grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company</label>
                <div className="relative">
                  <Building2 size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <select
                    value={selectedCompany}
                    onChange={(e) => setSelectedCompany(e.target.value)}
                    className="w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 appearance-none bg-white dark:bg-gray-800 dark:text-white"
                    required
                  >
                    <option value="">{companiesLoading ? "Loading..." : "Select company"}</option>
                    {companies.map((c) => (
                      <option key={c.name || c} value={c.name || c}>{c.name || c}</option>
                    ))}
                  </select>
                  <ChevronDown size={18} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <div className="relative">
                  <Target size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    placeholder="e.g., SDE, Data Scientist"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>
            </div>
            <button
              type="submit"
              disabled={loading || !selectedCompany}
              className="w-full bg-primary-600 text-white py-3 rounded-lg font-bold hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
              ) : (
                <>
                  <Zap size={18} />
                  Predict My Offer
                </>
              )}
            </button>
          </form>
        </AnimatedCard>

        {/* Results with Gauge */}
        <AnimatePresence>
          {prediction && (
            <motion.div
              className="space-y-6"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
               {/* Probability Gauge */}
               {probability > 0 && (
                <AnimatedCard className="card flex justify-center">
                  <PredictorGauge probability={probability} />
                </AnimatedCard>
              )}

              <div className="card bg-gradient-to-r from-primary-600 to-primary-700 text-white">
                <div className="text-center">
                  <p className="text-primary-100 mb-1">Predicted CTC</p>
                  <p className="text-5xl font-bold mb-2">
                    ₹{(prediction.predicted_ctc || prediction.salary || 0).toLocaleString("en-IN")}
                  </p>
                  <p className="text-primary-200 text-sm">
                    {prediction.range_min && prediction.range_max
                      ? `Range: ₹${prediction.range_min.toLocaleString("en-IN")} — ₹${prediction.range_max.toLocaleString("en-IN")}`
                      : "Based on your skills and company tier"}
                  </p>
                </div>
              </div>

              {prediction.skill_scores && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-4 flex items-center gap-2">
                    <Brain size={20} className="text-primary-600" />
                    Skill Assessment
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(prediction.skill_scores).map(([skill, score]: [string, any], i) => (
                      <div key={skill}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="capitalize text-gray-600 dark:text-gray-400">{skill.replace(/_/g, " ")}</span>
                          <span className="font-medium dark:text-white">{score}/10</span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                          <motion.div
                             className={`h-2 rounded-full ${Number(score) >= 8 ? "bg-green-500" : Number(score) >= 5 ? "bg-yellow-500" : "bg-red-500"}`}
                             initial={reduced ? { width: `${Number(score) * 10}%` } : { width: 0 }}
                             whileInView={{ width: `${Number(score) * 10}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: i * 0.1 }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </AnimatedCard>
              )}

              {!practiceResult && (
                <div className="text-center">
                  <button
                    onClick={handlePracticeForRole}
                    disabled={practicing || !selectedCompany}
                    className="btn-primary inline-flex items-center gap-2"
                  >
                    {practicing ? (
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                    ) : (
                      <><Flame size={18} /> Practice for This Role</>
                    )}
                  </button>
                </div>
              )}
              {practiceResult && (
                <AnimatedCard className="card bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 border border-emerald-200 dark:border-emerald-800">
                  <h3 className="font-bold mb-2 dark:text-white">Practice Session Ready</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    {practiceResult.company} · {practiceResult.role}
                  </p>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-700 dark:text-gray-300 mb-4">
                    <span>Coding: {practiceResult.coding?.length || 0}</span>
                    <span>Behavioral: {practiceResult.behavioral?.length || 0}</span>
                    <span>System Design: {practiceResult.system_design?.length || 0}</span>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Probability: {practiceResult.probability_before}% → {practiceResult.probability_after_target}%</span>
                  </div>
                </AnimatedCard>
              )}

              {prediction.tips && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-3">Tips to Improve</h3>
                  <ul className="space-y-2">
                    {(Array.isArray(prediction.tips) ? prediction.tips : [prediction.tips]).map((tip, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <span className="text-primary-600 mt-0.5">•</span>
                        {tip}
                      </li>
                    ))}
                  </ul>
                </AnimatedCard>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {history.length > 0 && (
          <div className="mt-8">
            <h3 className="font-bold mb-4 dark:text-white">Past Predictions</h3>
            <div className="space-y-2">
              {history.slice(0, 5).map((p, i) => (
                <AnimatedCard key={i} className="card flex items-center justify-between py-3">
                  <div>
                    <p className="font-semibold dark:text-white">{p.company}</p>
                    <p className="text-sm text-gray-500">{p.role}</p>
                  </div>
                  <p className="font-bold text-primary-600">₹{(p.predicted_ctc || p.salary || 0).toLocaleString("en-IN")}</p>
                </AnimatedCard>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
