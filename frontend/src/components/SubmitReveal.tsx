import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Emblem from './emblems/Emblem';
import ComplexityDisplay from './ComplexityDisplay';
import AlgorithmGraph from './AlgorithmGraph';
import { CheckCircle, XCircle, Zap, Trophy, ArrowRight, RotateCcw, Star } from 'lucide-react';

// Full-screen celebration overlay after submitting a problem
// Combines emblem animation, complexity display, graph, XP counter

interface SubmitRevealProps {
  result?: Record<string, any>;
  question?: any;
  onClose?: () => void;
  onTryAgain?: () => void;
  onNext?: () => void;
}

export default function SubmitReveal({
  result,
  question,
  onClose,
  onTryAgain,
  onNext,
}: SubmitRevealProps) {
  const [phase, setPhase] = useState(0);
  const [xpCount, setXpCount] = useState(0);

  const score = result?.score || 0;
  const passed = score >= 6;
  const xp = result?.xp_gained || 0;

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),    // emblem appears
      setTimeout(() => setPhase(2), 800),     // score reveal
      setTimeout(() => setPhase(3), 1400),    // complexity + graph
      setTimeout(() => setPhase(4), 2000),    // XP counter
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  // XP counter animation
  useEffect(() => {
    if (phase < 4 || xp === 0) return;
    let current = 0;
    const step = Math.max(1, Math.floor(xp / 20));
    const interval = setInterval(() => {
      current = Math.min(current + step, xp);
      setXpCount(current);
      if (current >= xp) clearInterval(interval);
    }, 50);
    return () => clearInterval(interval);
  }, [phase, xp]);

  if (!result) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-2 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0, y: 30 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }}
          onClick={e => e.stopPropagation()}
          className="w-full max-w-lg max-h-[90vh] overflow-y-auto"
        >
          {/* Score Header */}
          <div className={`text-center py-6 rounded-t-2xl ${
            passed
              ? 'bg-gradient-to-b from-green-500/10 to-transparent'
              : 'bg-gradient-to-b from-red-500/10 to-transparent'
          }`}>
            {/* Emblem */}
            {phase >= 1 && (
              <motion.div
                className="flex justify-center mb-4"
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ duration: 0.8, ease: [0.34, 1.56, 0.64, 1] }}
              >
                <Emblem
                  question={question}
                  difficulty={question?.difficulty}
                  size="xl"
                  animated={true}
                />
              </motion.div>
            )}

            {/* Score */}
            {phase >= 2 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                <div className="flex items-center justify-center gap-2 mb-2">
                  {passed ? (
                    <CheckCircle size={24} className="text-green-400" />
                  ) : (
                    <XCircle size={24} className="text-red-400" />
                  )}
                  <span className={`text-2xl font-display font-black ${passed ? 'text-green-400' : 'text-red-400'}`}>
                    {passed ? 'SOLVED' : 'KEEP PUSHING'}
                  </span>
                </div>

                {/* Score bar */}
                <div className="flex items-center justify-center gap-3 mb-2">
                  <div className="flex gap-1">
                    {Array.from({ length: 10 }).map((_, i) => (
                      <motion.div
                        key={i}
                        initial={{ scaleY: 0 }}
                        animate={{ scaleY: 1 }}
                        transition={{ delay: 0.1 + i * 0.05 }}
                        className={`w-2 h-6 rounded-sm ${
                          i < score
                            ? score >= 8 ? 'bg-green-400' : score >= 5 ? 'bg-yellow-400' : 'bg-red-400'
                            : 'bg-gray-700/30'
                        }`}
                        style={{ transformOrigin: 'bottom' }}
                      />
                    ))}
                  </div>
                  <span className="text-xl font-display font-black text-text-primary">{score}/10</span>
                </div>

                {/* Feedback */}
                {result.feedback && (
                  <p className="text-sm text-gray-300 font-mono px-6 mt-2">
                    {result.feedback}
                  </p>
                )}
              </motion.div>
            )}
          </div>

          {/* Body */}
          <div className="bg-gray-900/80 border border-gray-700/30 rounded-b-2xl p-4 space-y-4">
            {/* Strengths & Improvements */}
            {phase >= 2 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="grid grid-cols-2 gap-3"
              >
                {result.strengths?.length > 0 && (
                  <div className="bg-green-500/5 border border-green-500/15 rounded-lg p-3">
                    <div className="flex items-center gap-1 mb-1">
                      <Star size={10} className="text-green-400" />
                      <span className="text-[9px] font-mono text-green-400 uppercase">Strengths</span>
                    </div>
                    {result.strengths.map((s, i) => (
                      <p key={i} className="text-[10px] font-mono text-gray-400 mt-1">{s}</p>
                    ))}
                  </div>
                )}
                {result.improvements?.length > 0 && (
                  <div className="bg-yellow-500/5 border border-yellow-500/15 rounded-lg p-3">
                    <div className="flex items-center gap-1 mb-1">
                      <Zap size={10} className="text-yellow-400" />
                      <span className="text-[9px] font-mono text-yellow-400 uppercase">Improve</span>
                    </div>
                    {result.improvements.map((s, i) => (
                      <p key={i} className="text-[10px] font-mono text-gray-400 mt-1">{s}</p>
                    ))}
                  </div>
                )}
              </motion.div>
            )}

            {/* Complexity + Graph */}
            {phase >= 3 && (result.time_complexity || result.space_complexity) && (
              <ComplexityDisplay
                timeComplexity={result.time_complexity}
                spaceComplexity={result.space_complexity}
                algorithm={result.algorithm}
              />
            )}

            {phase >= 3 && result.graph_nodes?.length > 0 && (
              <AlgorithmGraph
                nodes={result.graph_nodes}
                edges={result.graph_edges}
              />
            )}

            {/* XP Counter */}
            {phase >= 4 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-3"
              >
                <div className="flex items-center justify-center gap-2">
                  <Trophy size={16} className="text-cyber-amber" />
                  <span className="text-2xl font-display font-black text-cyber-amber">
                    +{xpCount}
                  </span>
                  <span className="text-xs font-mono text-gray-500">XP</span>
                </div>
              </motion.div>
            )}

            {/* Better Approach */}
            {result.better_approach && phase >= 3 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="bg-cyber-blue/5 border border-cyber-blue/15 rounded-lg p-3"
              >
                <span className="text-[9px] font-mono text-cyber-blue uppercase">Better Approach</span>
                <p className="text-[10px] font-mono text-gray-400 mt-1">{result.better_approach}</p>
              </motion.div>
            )}

            {/* Actions */}
            {phase >= 4 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-3 pt-2"
              >
                <button onClick={onTryAgain} className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg border border-gray-700/40 text-gray-400 hover:text-text-primary hover:border-gray-600 transition-all text-xs font-mono">
                  <RotateCcw size={12} />
                  Try Again
                </button>
                {onNext && (
                  <button onClick={onNext} className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg bg-cyber-blue/15 border border-cyber-blue/30 text-cyber-blue hover:bg-cyber-blue/25 transition-all text-xs font-mono font-bold">
                    Next Problem
                    <ArrowRight size={12} />
                  </button>
                )}
              </motion.div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
