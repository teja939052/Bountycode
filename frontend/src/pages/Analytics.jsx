import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import {
  TrendingUp, Target, BarChart3, Zap, Briefcase, Award,
  AlertTriangle, CheckCircle, XCircle, ArrowUpRight
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

const STAGE_COLORS = {
  interested: "bg-gray-200 dark:bg-gray-700",
  applied: "bg-blue-500",
  oa_received: "bg-yellow-500",
  interview_scheduled: "bg-purple-500",
  interview_completed: "bg-indigo-500",
  offer_received: "bg-green-500",
  accepted: "bg-emerald-500",
  rejected: "bg-red-500",
  withdrawn: "bg-gray-400",
};

export default function Analytics() {
  const [overview, setOverview] = useState(null);
  const [funnel, setFunnel] = useState(null);
  const [skills, setSkills] = useState(null);
  const [companies, setCompanies] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [overviewData, funnelData, skillsData, companiesData, insightsData] = await Promise.all([
        api.getAnalyticsOverview().catch(() => null),
        api.getAnalyticsFunnel().catch(() => null),
        api.getAnalyticsSkills().catch(() => null),
        api.getAnalyticsCompanies().catch(() => null),
        api.getAnalyticsInsights().catch(() => null),
      ]);
      setOverview(overviewData);
      setFunnel(funnelData);
      setSkills(skillsData);
      setCompanies(companiesData);
      setInsights(insightsData);
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

  const maxFunnelCount = funnel?.funnel?.length ? Math.max(...funnel.funnel.map((s) => s.count)) : 1;

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-teal-100 dark:bg-teal-900/30 rounded-xl flex items-center justify-center">
              <BarChart3 size={24} className="text-teal-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold dark:text-white">Analytics</h1>
              <p className="text-gray-600 dark:text-gray-400">Track your job search performance</p>
            </div>
          </div>
        </motion.div>

        {/* Overview Cards */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              { label: "Applications", value: overview.total_applications, sub: `${overview.applications_30d} this month`, color: "text-blue-600", icon: Briefcase },
              { label: "Offers", value: overview.offers_received, sub: `${overview.offer_rate}% offer rate`, color: "text-green-600", icon: Award },
              { label: "XP", value: overview.xp, sub: `Level ${overview.level}`, color: "text-yellow-600", icon: Zap },
              { label: "Skill Score", value: overview.overall_skill_score, sub: `${overview.streak} day streak`, color: "text-teal-600", icon: TrendingUp },
            ].map((s, i) => (
              <AnimatedCard key={s.label} delay={i * 0.05} className="card">
                <div className="flex items-center gap-2 mb-2">
                  <s.icon size={18} className={`${s.color}`} />
                  <span className="text-xs text-gray-500">{s.label}</span>
                </div>
                <p className={`text-3xl font-bold ${s.color}`}>{s.value}</p>
                <p className="text-xs text-gray-400 mt-1">{s.sub}</p>
              </AnimatedCard>
            ))}
          </div>
        )}

        {/* Funnel */}
        {funnel && (
          <AnimatedCard className="card mb-8">
            <h3 className="font-bold mb-4 dark:text-white flex items-center gap-2">
              <Target size={20} className="text-primary-600" />
              Application Funnel
            </h3>
            <div className="space-y-3">
              {funnel.funnel.map((stage, i) => (
                <div key={stage.stage} className="flex items-center gap-3">
                  <span className="text-xs text-gray-500 w-32 capitalize">{stage.stage.replace(/_/g, " ")}</span>
                  <div className="flex-1 bg-gray-100 dark:bg-gray-700 rounded-full h-6 overflow-hidden">
                    <motion.div
                      className={`h-full rounded-full ${STAGE_COLORS[stage.stage] || "bg-gray-500"}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${(stage.count / maxFunnelCount) * 100}%` }}
                      transition={{ duration: 0.6, delay: i * 0.05 }}
                    />
                  </div>
                  <span className="text-xs font-mono text-gray-600 dark:text-gray-400 w-16 text-right">
                    {stage.count} ({stage.percentage}%)
                  </span>
                </div>
              ))}
            </div>
          </AnimatedCard>
        )}

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Skill Progression */}
          {skills && (
            <AnimatedCard className="card">
              <h3 className="font-bold mb-4 dark:text-white flex items-center gap-2">
                <TrendingUp size={20} className="text-green-500" />
                Skill Progression
              </h3>
              <div className="space-y-3">
                {Object.entries(skills.current?.categories || {}).map(([cat, data]) => (
                  <div key={cat}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="capitalize text-gray-600 dark:text-gray-400">{data.name}</span>
                      <span className="font-medium dark:text-white">{data.score}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <motion.div
                        className={`h-2 rounded-full ${data.score >= 70 ? "bg-green-500" : data.score >= 40 ? "bg-yellow-500" : "bg-red-500"}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${data.score}%` }}
                        transition={{ duration: 0.6 }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </AnimatedCard>
          )}

          {/* Insights */}
          {insights && (
            <AnimatedCard className="card">
              <h3 className="font-bold mb-4 dark:text-white flex items-center gap-2">
                <AlertTriangle size={20} className="text-orange-500" />
                Insights
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Average prediction</span>
                  <span className="text-sm font-bold dark:text-white">{insights.average_probability}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Best company</span>
                  <span className="text-sm font-bold text-green-600">{insights.best_company || "N/A"}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Predictions made</span>
                  <span className="text-sm font-bold dark:text-white">{insights.predictions_count}</span>
                </div>
                {insights.weak_areas?.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Weak areas to improve</p>
                    <div className="flex flex-wrap gap-1">
                      {insights.weak_areas.map((area, i) => (
                        <span key={i} className="text-xs px-2 py-1 rounded-full bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400">
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </AnimatedCard>
          )}
        </div>

        {/* Company Stats */}
        {companies?.companies?.length > 0 && (
          <AnimatedCard className="card mb-8">
            <h3 className="font-bold mb-4 dark:text-white flex items-center gap-2">
              <BarChart3 size={20} className="text-blue-500" />
              Company Performance
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500 border-b border-gray-200 dark:border-gray-700">
                    <th className="pb-2 font-medium">Company</th>
                    <th className="pb-2 font-medium">Applications</th>
                    <th className="pb-2 font-medium">Interviews</th>
                    <th className="pb-2 font-medium">Offers</th>
                    <th className="pb-2 font-medium">Interview Rate</th>
                    <th className="pb-2 font-medium">Offer Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {companies.companies.map((co, i) => (
                    <tr key={i} className="border-b border-gray-100 dark:border-gray-800">
                      <td className="py-2 font-medium dark:text-white">{co.company}</td>
                      <td className="py-2 text-gray-600 dark:text-gray-400">{co.total_applications}</td>
                      <td className="py-2 text-gray-600 dark:text-gray-400">{co.interviews}</td>
                      <td className="py-2 text-gray-600 dark:text-gray-400">{co.offers}</td>
                      <td className="py-2">
                        <span className={`font-medium ${co.interview_rate >= 50 ? "text-green-600" : co.interview_rate >= 25 ? "text-yellow-600" : "text-red-600"}`}>
                          {co.interview_rate}%
                        </span>
                      </td>
                      <td className="py-2">
                        <span className={`font-medium ${co.offer_rate >= 20 ? "text-green-600" : co.offer_rate >= 10 ? "text-yellow-600" : "text-red-600"}`}>
                          {co.offer_rate}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AnimatedCard>
        )}

        {/* Predictive Insights */}
        {insights && (
          <AnimatedCard className="card bg-gradient-to-r from-teal-50 to-emerald-50 dark:from-teal-900/20 dark:to-emerald-900/20 border border-teal-200 dark:border-teal-800">
            <h3 className="font-bold mb-2 dark:text-white flex items-center gap-2">
              <ArrowUpRight size={20} className="text-teal-600" />
              Predictive Insight
            </h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              {insights.best_company
                ? `Your highest probability is at ${insights.best_company} (${insights.average_probability}% average). Keep practicing to improve your chances.`
                : "Make more predictions to unlock personalized insights."}
            </p>
            {insights.weak_areas?.length > 0 && (
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                Focus on: <span className="font-medium">{insights.weak_areas.join(", ")}</span>
              </p>
            )}
          </AnimatedCard>
        )}
      </div>
    </div>
  );
}
