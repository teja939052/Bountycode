import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../../services/api';
import { Target, CheckCircle2 } from 'lucide-react';

export default function DailyGoal() {
  const [goal, setGoal] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getDailyGoal();
        setGoal(data);
      } catch {}
      setLoading(false);
    };
    load();
  }, []);

  if (loading || !goal) return null;

  const pct = Math.min(100, (goal.count / goal.target) * 100);
  const isComplete = goal.completed;

  return (
    <div className="glass p-4 rounded-xl">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {isComplete ? (
            <CheckCircle2 size={18} className="text-green-400" />
          ) : (
            <Target size={18} className="text-cyber-blue" />
          )}
          <span className="font-display font-bold text-sm text-white uppercase tracking-wider">
            Daily Goal
          </span>
        </div>
        <span className="font-mono text-xs text-gray-400">
          {goal.count}/{goal.target} solved
        </span>
      </div>

      {/* Progress bar */}
      <div className="relative w-full h-3 bg-space-void rounded-full overflow-hidden mb-2">
        <motion.div
          className={`h-full rounded-full ${isComplete ? 'bg-gradient-to-r from-green-500 to-emerald-400' : 'bg-gradient-to-r from-cyber-blue to-cyan-400'}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        />
        {isComplete && (
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
            initial={{ x: '-100%' }}
            animate={{ x: '200%' }}
            transition={{ duration: 1.5, repeat: Infinity, repeatDelay: 2 }}
          />
        )}
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs font-mono ${isComplete ? 'text-green-400' : 'text-gray-500'}`}>
          {isComplete ? 'Goal complete! +15 XP bonus' : `${goal.target - goal.count} more to go`}
        </span>
        {isComplete && (
          <span className="text-xs font-mono text-green-400">+15 XP</span>
        )}
      </div>
    </div>
  );
}
