import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import { CalendarCheck, Flame, CheckCircle2, XCircle, Zap, Trophy, ArrowRight, RotateCcw } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";
import CelebrationOverlay from "../components/CelebrationOverlay";

export default function DailyDrill() {
  const { user } = useAuthStore();
  const [drill, setDrill] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadDrill();
  }, []);

  const loadDrill = async () => {
    setLoading(true);
    setSubmitted(false);
    setResult(null);
    setAnswers({});
    try {
      const data = await api.getDailyDrill();
      setDrill(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionIndex, answer) => {
    setAnswers((prev) => ({ ...prev, [questionIndex]: answer }));
  };

  const handleSubmit = async () => {
    if (!drill) return;
    setSubmitting(true);
    try {
      const res = await api.submitDrill(drill.drill_id || drill.id, answers);
      setResult(res);
      setSubmitted(true);
      if (res.percentage >= 80) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 2500);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const allAnswered = drill?.questions && Object.keys(answers).length === drill.questions.length;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <CelebrationOverlay show={showCelebration} type="perfect" message="Perfect Score!" />

        <motion.div
          className="text-center mb-10"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="w-16 h-16 bg-orange-100 dark:bg-orange-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <CalendarCheck size={32} className="text-orange-600" />
          </div>
          <h1 className="text-3xl font-bold dark:text-white">Daily Drill</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">5 quick questions to keep your skills sharp</p>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[
            { icon: Flame, value: user?.streak || 0, label: "Day Streak", color: "text-orange-500" },
            { icon: Zap, value: user?.xp || 0, label: "Total XP", color: "text-yellow-500" },
            { icon: Trophy, value: user?.level || 1, label: "Level", color: "text-primary-500" },
          ].map((stat, i) => (
            <AnimatedCard key={stat.label} delay={i * 0.05} className="card text-center">
              <stat.icon size={24} className={`mx-auto ${stat.color} mb-2`} />
              <p className="text-2xl font-bold dark:text-white">{stat.value}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">{stat.label}</p>
            </AnimatedCard>
          ))}
        </div>

        {/* Questions */}
        {drill && !submitted && (
          <StaggerContainer className="space-y-6">
            {drill.questions?.map((q, i) => (
              <StaggerItem key={i}>
                <AnimatedCard className="card">
                  <div className="flex items-start gap-3 mb-4">
                    <span className="w-8 h-8 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full flex items-center justify-center font-bold text-sm shrink-0">
                      {i + 1}
                    </span>
                    <p className="font-semibold text-lg dark:text-white">{q.question}</p>
                  </div>
                  {q.options && (
                    <div className="space-y-2 ml-11">
                      {q.options.map((opt, j) => (
                        <motion.button
                          key={j}
                          onClick={() => handleAnswer(i, j)}
                          className={`w-full text-left p-3 rounded-lg border-2 transition-colors ${
                            answers[i] === j
                              ? "border-primary-500 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400"
                              : "border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 dark:text-gray-300"
                          }`}
                          whileTap={reduced ? {} : { scale: 0.98 }}
                        >
                          <span className="font-medium mr-2">{String.fromCharCode(65 + j)}.</span>
                          {opt}
                        </motion.button>
                      ))}
                    </div>
                  )}
                </AnimatedCard>
              </StaggerItem>
            ))}

            <motion.button
              onClick={handleSubmit}
              disabled={!allAnswered || submitting}
              className="w-full bg-primary-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              whileHover={reduced ? {} : { scale: 1.01 }}
              whileTap={reduced ? {} : { scale: 0.99 }}
            >
              {submitting ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
              ) : (
                <>
                  Submit Drill
                  <ArrowRight size={20} />
                </>
              )}
            </motion.button>
          </StaggerContainer>
        )}

        {/* Results */}
        <AnimatePresence>
          {submitted && result && (
            <motion.div
              initial={reduced ? {} : { opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", stiffness: 200, damping: 20 }}
            >
              <div className="card text-center py-10">
                <motion.div
                  className={`w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 ${
                    result.percentage >= 80 ? "bg-green-100 dark:bg-green-900/30" : result.percentage >= 50 ? "bg-yellow-100 dark:bg-yellow-900/30" : "bg-red-100 dark:bg-red-900/30"
                  }`}
                  initial={reduced ? {} : { rotate: -180, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15 }}
                >
                  {result.percentage >= 80 ? (
                    <Trophy size={40} className="text-green-600" />
                  ) : result.percentage >= 50 ? (
                    <CheckCircle2 size={40} className="text-yellow-600" />
                  ) : (
                    <XCircle size={40} className="text-red-600" />
                  )}
                </motion.div>
                <h2 className="text-3xl font-bold mb-2 dark:text-white">
                  {result.percentage >= 80 ? "Excellent!" : result.percentage >= 50 ? "Good effort!" : "Keep practicing!"}
                </h2>
                <p className="text-6xl font-bold text-primary-600 mb-4">{result.percentage || 0}%</p>
                <p className="text-gray-600 dark:text-gray-400 mb-2">
                  {result.correct || 0} out of {result.total || 5} correct
                </p>
                {result.xp_gained && (
                  <p className="text-lg font-semibold text-yellow-600 mb-6">+{result.xp_gained} XP earned!</p>
                )}
                <button
                  onClick={loadDrill}
                  className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
                >
                  <RotateCcw size={18} />
                  Try Another Drill
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {drill && !submitted && (
          <div className="mt-6 text-center text-sm text-gray-400 dark:text-gray-500">
            {Object.keys(answers).length} of {drill.questions?.length || 0} answered
          </div>
        )}
      </div>
    </div>
  );
}
