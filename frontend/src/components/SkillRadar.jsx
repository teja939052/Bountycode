import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import { Target, AlertCircle } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

export default function SkillRadar() {
  const [skills, setSkills] = useState(null);
  const [weakAreas, setWeakAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const loadSkills = async () => {
      try {
        const [skillsData, weakData] = await Promise.all([
          api.getSkillGraph().catch(() => null),
          api.getWeakAreas(5).catch(() => []),
        ]);
        setSkills(skillsData);
        setWeakAreas(weakData);
      } catch (err) {
        console.error("Failed to load skills");
      }
      setLoading(false);
    };
    loadSkills();
  }, []);

  if (loading || !skills) return null;

  const categories = skills.categories || {};
  const categoryList = Object.entries(categories).map(([id, cat]) => ({
    id,
    name: cat.name,
    score: cat.score || 0,
  }));

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-600 bg-green-100 dark:bg-green-900/30";
    if (score >= 60) return "text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30";
    if (score >= 40) return "text-orange-600 bg-orange-100 dark:bg-orange-900/30";
    return "text-red-600 bg-red-100 dark:bg-red-900/30";
  };

  const getScoreBarColor = (score) => {
    if (score >= 80) return "bg-green-500";
    if (score >= 60) return "bg-yellow-500";
    if (score >= 40) return "bg-orange-500";
    return "bg-red-500";
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold flex items-center gap-2 dark:text-white">
          <Target size={20} className="text-indigo-600" />
          Skill Overview
        </h3>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          Overall: {skills.overall_score || 0}%
        </span>
      </div>

      {/* Category Scores with animated bars */}
      <div className="space-y-3 mb-6">
        {categoryList.map((cat, i) => (
          <div key={cat.id}>
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="text-gray-700 dark:text-gray-300">{cat.name}</span>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getScoreColor(cat.score)}`}>
                {cat.score}%
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
              <motion.div
                className={`h-2 rounded-full ${getScoreBarColor(cat.score)}`}
                initial={reduced ? { width: `${cat.score}%` } : { width: 0 }}
                whileInView={{ width: `${cat.score}%` }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: i * 0.1, ease: "easeOut" }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Weak Areas */}
      {weakAreas.length > 0 && (
        <div>
          <h4 className="font-semibold text-sm mb-2 flex items-center gap-2">
            <AlertCircle size={16} className="text-orange-500" />
            Areas to Improve
          </h4>
          <div className="space-y-2">
            {weakAreas.map((area, i) => (
              <motion.div
                key={i}
                className="flex items-center justify-between bg-orange-50 dark:bg-orange-900/20 rounded-lg px-3 py-2"
                initial={reduced ? {} : { opacity: 0, x: -10 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
              >
                <div>
                  <p className="text-sm font-medium text-gray-800 dark:text-gray-200 capitalize">
                    {area.skill.replace(/_/g, " ")}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{area.category_name}</p>
                </div>
                <span className="text-sm font-bold text-orange-600">{area.score}%</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
