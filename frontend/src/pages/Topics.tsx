import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import { BookOpen, ChevronRight, CheckCircle, Target, Flame } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";

const TOPIC_ICONS = {
  "Arrays": "01",
  "Linked Lists": "02",
  "Stacks & Queues": "03",
  "Binary Trees": "04",
  "Graphs": "05",
  "Dynamic Programming": "06",
  "Greedy": "07",
  "Tries": "08",
  "Heaps": "09",
  "Sorting": "10",
  "Searching": "11",
  "Bit Manipulation": "12",
  "Math": "13",
  "String": "14",
};

const TOPIC_COLORS = {
  "Arrays": "from-blue-500 to-cyan-500",
  "Linked Lists": "from-purple-500 to-pink-500",
  "Stacks & Queues": "from-orange-500 to-red-500",
  "Binary Trees": "from-green-500 to-emerald-500",
  "Graphs": "from-indigo-500 to-blue-500",
  "Dynamic Programming": "from-yellow-500 to-orange-500",
  "Greedy": "from-pink-500 to-rose-500",
  "Tries": "from-teal-500 to-cyan-500",
  "Heaps": "from-violet-500 to-purple-500",
};

export default function Topics() {
  const [topics, setTopics] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [topicsData, progressData] = await Promise.all([
        api.getTopics(),
        api.getProblemProgress(),
      ]);
      setTopics(topicsData.topics || []);
      setProgress(progressData);
    } catch (err) {
      console.error("Failed to load topics:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="space-y-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-2" />
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <BookOpen size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-text-primary">DSA Practice</h1>
              <p className="text-gray-600 dark:text-gray-400">
                Striver's SDE Sheet — Master every topic
              </p>
            </div>
          </div>
        </motion.div>

        {/* Overall Progress */}
        {progress && (
          <AnimatedCard className="card mb-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Target size={20} className="text-primary-600" />
                <h2 className="text-lg font-bold dark:text-white">Overall Progress</h2>
              </div>
              <div className="flex items-center gap-2">
                <Flame size={16} className="text-orange-500" />
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {progress.total_solved}/{progress.total_problems} solved
                </span>
              </div>
            </div>
            <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden mb-3">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600"
                initial={{ width: 0 }}
                animate={{ width: `${progress.overall_percentage}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            </div>
            <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
              <span>{progress.overall_percentage}% complete</span>
              <span>{progress.total_problems - progress.total_solved} remaining</span>
            </div>
          </AnimatedCard>
        )}

        {/* Topics Grid */}
        <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map((topic) => {
            const topicProgress = progress?.topics?.find((t) => t.topic === topic.topic);
            const solved = topicProgress?.solved || 0;
            const percentage = topicProgress?.percentage || 0;
            const colorClass = TOPIC_COLORS[topic.topic] || "from-gray-500 to-gray-600";

            return (
              <StaggerItem key={topic.topic}>
                <Link to={`/problems/${encodeURIComponent(topic.topic)}`}>
                  <motion.div
                    whileHover={reduced ? {} : { y: -4, scale: 1.02 }}
                    className="card h-full cursor-pointer group"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClass} flex items-center justify-center text-white font-bold text-sm`}>
                        {TOPIC_ICONS[topic.topic] || "XX"}
                      </div>
                      <ChevronRight
                        size={20}
                        className="text-gray-400 group-hover:text-primary-600 transition-colors"
                      />
                    </div>
                    <h3 className="text-lg font-bold dark:text-white mb-1">{topic.topic}</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                      {topic.total} problems
                    </p>

                    {/* Difficulty badges */}
                    <div className="flex gap-2 mb-3">
                      {topic.easy > 0 && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                          {topic.easy} Easy
                        </span>
                      )}
                      {topic.medium > 0 && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400">
                          {topic.medium} Medium
                        </span>
                      )}
                      {topic.hard > 0 && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400">
                          {topic.hard} Hard
                        </span>
                      )}
                    </div>

                    {/* Progress bar */}
                    <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          percentage >= 100
                            ? "bg-green-500"
                            : percentage >= 50
                            ? "bg-primary-500"
                            : "bg-primary-400"
                        }`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <span>{solved}/{topic.total} solved</span>
                      {solved > 0 && (
                        <span className="flex items-center gap-1">
                          <CheckCircle size={12} className="text-green-500" />
                          {percentage}%
                        </span>
                      )}
                    </div>
                  </motion.div>
                </Link>
              </StaggerItem>
            );
          })}
        </StaggerContainer>

        {topics.length === 0 && !loading && (
          <div className="card text-center py-12">
            <BookOpen size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No topics available yet</p>
            <p className="text-sm text-gray-400 dark:text-gray-500">
              Run the seed script to add problems
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
