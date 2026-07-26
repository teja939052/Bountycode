import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import ProblemDetail from "../components/ProblemDetail";
import Compiler from "../pages/Compiler";
import useReducedMotion from "../hooks/useReducedMotion";

export default function SolveProblem() {
  const { id } = useParams();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getQuestionFull(id);
        setProblem(data);
      } catch {
        setProblem(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (loading) {
    return (
      <div className="h-[calc(100vh-64px)] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="h-[calc(100vh-64px)] flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-400 mb-2">Problem not found</p>
          <a href="/question-bank" className="text-cyber-blue hover:underline text-sm">Back to Question Bank</a>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col">
      <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
        {/* Left Panel: Problem Description */}
        <motion.div
          className="w-full md:w-1/2 overflow-y-auto border-b md:border-b-0 md:border-r border-space-border"
          initial={reduced ? {} : { opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <ProblemDetail problemId={id} problem={problem} />
        </motion.div>

        {/* Right Panel: Compiler */}
        <motion.div
          className="w-full md:w-1/2 flex flex-col"
          initial={reduced ? {} : { opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <Compiler problemId={id} problem={problem} />
        </motion.div>
      </div>
    </div>
  );
}
