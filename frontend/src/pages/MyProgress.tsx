import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import { BarChart3, TrendingUp, Target, AlertCircle, CheckCircle, XCircle, ArrowRight } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import AnimatedNumber from "../components/motion/AnimatedNumber";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";

export default function MyProgress() {
  const [stats, setStats] = useState(null);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsData, recentData] = await Promise.all([
        api.questions.getStats().catch(() => null),
        api.getRecentAnswers(10).catch(() => ({ answers: [] })),
      ]);
      setStats(statsData);
      setRecent(recentData.answers || []);
    } catch {} finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  const totalAttempted = stats?.total_attempted || 0;
  const weakAreas = stats?.weak_areas || [];
  const strongAreas = stats?.strong_areas || [];
  const topicStats = stats?.topic_stats || [];
  const companyStats = stats?.company_stats || [];

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          className="mb-8"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center">
              <BarChart3 size={24} className="text-indigo-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold dark:text-white">My Progress</h1>
              <p className="text-brand-secondary dark:text-gray-400">Track your question bank performance</p>
            </div>
          </div>
        </motion.div>

        {/* Overview Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { value: totalAttempted, label: "Questions Done", color: "text-primary-600" },
            { value: strongAreas.length, label: "Strong Topics", color: "text-green-600" },
            { value: weakAreas.length, label: "Weak Topics", color: "text-orange-600" },
            { value: companyStats.length, label: "Companies", color: "text-blue-600" },
          ].map((s, i) => (
            <AnimatedCard key={s.label} delay={i * 0.05} className="card text-center">
              <p className={`text-3xl font-bold ${s.color}`}>
                <AnimatedNumber value={s.value} />
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{s.label}</p>
            </AnimatedCard>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Strong Areas */}
          <AnimatedCard className="card">
            <h3 className="font-bold mb-4 flex items-center gap-2 dark:text-white">
              <CheckCircle size={20} className="text-green-500" />
              Strong Areas
            </h3>
            {strongAreas.length === 0 ? (
              <p className="text-gray-400 dark:text-gray-500 text-sm">Answer more questions to see your strengths</p>
            ) : (
              <div className="space-y-3">
                {strongAreas.map((area) => (
                  <div key={area.topic}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-brand-primary dark:text-brand-secondary">{area.topic}</span>
                      <span className="font-medium text-green-600">{area.avg_score}/10</span>
                    </div>
                    <div className="w-full bg-surface-card/50 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${area.avg_score * 10}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-400 mt-0.5">{area.count} questions · {area.accuracy}% accuracy</p>
                  </div>
                ))}
              </div>
            )}
          </AnimatedCard>

          {/* Weak Areas */}
          <AnimatedCard className="card">
            <h3 className="font-bold mb-4 flex items-center gap-2 dark:text-white">
              <AlertCircle size={20} className="text-orange-500" />
              Areas to Improve
            </h3>
            {weakAreas.length === 0 ? (
              <p className="text-gray-400 dark:text-gray-500 text-sm">No weak areas identified yet</p>
            ) : (
              <div className="space-y-3">
                {weakAreas.map((area) => (
                  <div key={area.topic}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-brand-primary dark:text-brand-secondary">{area.topic}</span>
                      <span className="font-medium text-orange-600">{area.avg_score}/10</span>
                    </div>
                    <div className="w-full bg-surface-card/50 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full"
                        style={{ width: `${area.avg_score * 10}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-400 mt-0.5">{area.count} questions · {area.accuracy}% accuracy</p>
                  </div>
                ))}
              </div>
            )}
          </AnimatedCard>
        </div>

        {/* Company Stats */}
        {companyStats.length > 0 && (
          <AnimatedCard className="card mb-8">
            <h3 className="font-bold mb-4 flex items-center gap-2 dark:text-white">
              <Target size={20} className="text-blue-500" />
              Performance by Company
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {companyStats.map((cs) => (
                <div key={cs.company} className="bg-surface-base dark:bg-gray-700/50 rounded-lg p-3">
                  <p className="font-semibold text-sm dark:text-white">{cs.company}</p>
                  <p className="text-lg font-bold text-primary-600">{cs.avg_score}/10</p>
                  <p className="text-xs text-gray-400">{cs.count} questions</p>
                </div>
              ))}
            </div>
          </AnimatedCard>
        )}

        {/* Recent Answers */}
        {recent.length > 0 && (
          <AnimatedCard className="card mb-8">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold dark:text-white">Recent Answers</h3>
              <Link to="/question-bank" className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
                Practice more <ArrowRight size={14} />
              </Link>
            </div>
            <div className="space-y-2">
              {recent.map((a) => (
                <div key={a.id} className="flex items-center justify-between py-2 border-t border-gray-100 dark:border-gray-700 first:border-0">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium dark:text-white truncate">
                      {a.feedback?.substring(0, 60) || "Answer submitted"}
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(a.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className={`text-sm font-bold ${
                      a.score >= 7 ? "text-green-600" : a.score >= 4 ? "text-yellow-600" : "text-red-600"
                    }`}>
                      {a.score}/10
                    </span>
                    {a.is_correct ? (
                      <CheckCircle size={16} className="text-green-500" />
                    ) : (
                      <XCircle size={16} className="text-red-500" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </AnimatedCard>
        )}

        {/* CTA */}
        {totalAttempted === 0 && (
          <AnimatedCard className="card text-center py-12">
            <TrendingUp size={48} className="mx-auto text-brand-secondary dark:text-brand-secondary mb-4" />
            <h3 className="text-xl font-bold mb-2 dark:text-white">Start Practicing</h3>
            <p className="text-gray-500 dark:text-gray-400 mb-6">Answer questions from the question bank to see your progress here</p>
            <Link
              to="/question-bank"
              className="inline-flex items-center gap-2 bg-primary-600 text-text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Open Question Bank <ArrowRight size={18} />
            </Link>
          </AnimatedCard>
        )}
      </div>
    </div>
  );
}
