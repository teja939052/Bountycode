import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../../services/api';
import { Snowflake, ShoppingCart, AlertTriangle } from 'lucide-react';
import { useToast } from '../Toast';

export default function StreakFreeze({ streakFreezes: initialFreezes, coins: initialCoins }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [buying, setBuying] = useState(false);
  const [freezes, setFreezes] = useState(initialFreezes || 0);
  const [coins, setCoins] = useState(initialCoins || 0);
  const toast = useToast();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getStreakFreezeStatus();
        setStatus(data);
        setFreezes(data.streak_freezes);
      } catch {}
      setLoading(false);
    };
    load();
  }, []);

  useEffect(() => {
    setFreezes(initialFreezes || 0);
    setCoins(initialCoins || 0);
  }, [initialFreezes, initialCoins]);

  const handleBuy = async () => {
    if (buying) return;
    setBuying(true);
    try {
      const res = await api.buyStreakFreeze();
      if (res.success) {
        setFreezes(f => f + 1);
        setCoins(res.coins_remaining);
        toast.success('Streak freeze purchased!');
      } else {
        toast.warning(res.message || 'Not enough coins');
      }
    } catch {
      toast.error('Failed to buy streak freeze');
    }
    setBuying(false);
  };

  if (loading) return null;

  const inDanger = status?.streak_in_danger;
  const canFreeze = status?.can_freeze;

  return (
    <div className={`glass p-4 rounded-xl ${inDanger ? 'border border-red-500/30' : ''}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Snowflake size={18} className={`${freezes > 0 ? 'text-blue-400' : 'text-gray-500'}`} />
          <span className="font-display font-bold text-sm text-white uppercase tracking-wider">
            Streak Freeze
          </span>
        </div>
        <span className="font-mono text-xs text-gray-400">
          {freezes} remaining
        </span>
      </div>

      {inDanger && canFreeze && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 mb-3"
        >
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle size={14} className="text-red-400" />
            <span className="text-xs font-mono text-red-400">Streak at risk!</span>
          </div>
          <p className="text-xs text-gray-400">
            You missed yesterday. Use a streak freeze to protect your {status?.streak}-day streak.
          </p>
        </motion.div>
      )}

      <div className="flex items-center justify-between">
        <div className="flex gap-1">
          {Array.from({ length: Math.min(freezes, 5) }).map((_, i) => (
            <Snowflake key={i} size={12} className="text-blue-400" />
          ))}
          {freezes === 0 && (
            <span className="text-xs font-mono text-gray-500">No freezes left</span>
          )}
        </div>

        <button
          onClick={handleBuy}
          disabled={buying || coins < (status?.cost || 50)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono
                     bg-blue-500/10 text-blue-400 border border-blue-500/20
                     hover:bg-blue-500/20 transition-all
                     disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <ShoppingCart size={12} />
          Buy ({status?.cost || 50} coins)
        </button>
      </div>
    </div>
  );
}
