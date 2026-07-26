import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import {
  ArrowLeft, CheckCircle, Lock, ChevronRight, ArrowRight,
  Code, Clock, Building2
} from "lucide-react";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";
import useAuthStore from "../store/authStore";

const DIFFICULTY_COLORS = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
};

export default function TopicProblems() {
  const { topic } = useParams();
  const { user } = useAuthStore();
  const [problems, setProblems] = useState([]);
  const [topicData, setTopicData] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();
  const isPro = user?.plan === "pro" || user?.plan === "lifetime";

  useEffect(() => {
    loadProblems();
  }, [topic]);

  const loadProblems = async () => {
    setLoading(true);
    try {
      const data = await api.getTopicProblems(topic);
      setProblems(data.problems || []);
      setTopicData(data);
    } catch (err) {
      console.error("Failed to load problems:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSolve = (problemId) => {
    window.location.href = `/solve/${problemId}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="space-y-3">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-2" />
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Back link */}
        <Link
          to="/problems"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 mb-6 transition-colors"
        >
          <ArrowLeft size={16} />
          All Topics
        </Link>

        {/* Header */}
        <motion.div
          className="mb-8"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold dark:text-white mb-1">{topic}</h1>
              <p className="text-gray-600 dark:text-gray-400">
                {topicData?.total || 0} problems · {topicData?.solved_count || 0} solved
              </p>
            </div>
            {topicData && topicData.total > 0 && (
              <div className="text-right">
                <div className="text-2xl font-bold text-primary-600">
                  {Math.round(((topicData.solved_count || 0) / topicData.total) * 100)}%
                </div>
                <div className="text-xs text-gray-500">Complete</div>
              </div>
            )}
          </div>
          {topicData && topicData.total > 0 && (
            <div className="mt-4 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600"
                initial={{ width: 0 }}
                animate={{
                  width: `${((topicData.solved_count || 0) / topicData.total) * 100}%`,
                }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
          )}
        </motion.div>

        {/* Problem List */}
        {problems.length > 0 ? (
          <StaggerContainer className="space-y-3">
            {problems.map((problem, index) => (
              <StaggerItem key={problem.id}>
                <motion.div
                  whileHover={reduced ? {} : { x: 4 }}
                  className="card flex items-center gap-4 cursor-pointer group"
                  onClick={() => handleSolve(problem.id)}
                >
                  {/* Number */}
                  <div className="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-sm font-bold text-gray-500 dark:text-gray-400 shrink-0">
                    {index + 1}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold dark:text-white truncate group-hover:text-primary-600 transition-colors">
                        {problem.question_title || problem.question}
                      </h3>
                      {problem.solved && (
                        <CheckCircle size={16} className="text-green-500 shrink-0" />
                      )}
                    </div>
                    <div className="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400">
                      <span className={`px-2 py-0.5 rounded-full ${DIFFICULTY_COLORS[problem.difficulty] || ""}`}>
                        {problem.difficulty}
                      </span>
                      {problem.company?.slice(0, 2).map((c) => (
                        <span key={c} className="flex items-center gap-1">
                          <Building2 size={10} />
                          {c}
                        </span>
                      ))}
                      {problem.topics?.slice(0, 2).map((t) => (
                        <span key={t} className="flex items-center gap-1">
                          <Code size={10} />
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Status */}
                  <div className="shrink-0">
                    {problem.solved ? (
                      <span className="px-3 py-1.5 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-medium">
                        Solved
                      </span>
                    ) : (
                      <span className="px-3 py-1.5 rounded-lg bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-sm font-medium flex items-center gap-1 group-hover:bg-primary-600 group-hover:text-white transition-colors">
                        Solve <ArrowRight size={14} />
                      </span>
                    )}
                  </div>
                </motion.div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        ) : (
          <div className="card text-center py-12">
            <Code size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No problems in this topic yet</p>
          </div>
        )}
      </div>
    </div>
  );
}
