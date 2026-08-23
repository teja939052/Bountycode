import { useState } from 'react';
import { motion } from 'framer-motion';

// Power-up shop — buy and use power-ups with coins
const POWER_UP_LIST = [
  { id: 'extra_time', name: 'Extra Time', emoji: '⏰', description: '+5 min on timed test', rarity: 'common', cost: 10 },
  { id: 'hint_reveal', name: 'Hint Reveal', emoji: '💡', description: 'Show 1 hint free', rarity: 'common', cost: 15 },
  { id: 'retry', name: 'Retry', emoji: '🔄', description: 'Extra attempt', rarity: 'uncommon', cost: 25 },
  { id: 'double_xp', name: 'Double XP', emoji: '⚡', description: '2x XP for 1 hour', rarity: 'rare', cost: 50 },
  { id: 'skip_boss', name: 'Skip Boss', emoji: '🛡️', description: 'Skip a boss battle', rarity: 'rare', cost: 75 },
  { id: 'show_answer', name: 'Show Answer', emoji: '🎯', description: 'Reveal answer', rarity: 'legendary', cost: 100 },
];

const RARITY_COLORS = {
  common: 'border-gray-500/30 bg-gray-500/5',
  uncommon: 'border-green-500/30 bg-green-500/5',
  rare: 'border-blue-500/30 bg-blue-500/5',
  legendary: 'border-yellow-500/30 bg-yellow-500/5',
};

const RARITY_TEXT = {
  common: 'text-gray-400',
  uncommon: 'text-green-400',
  rare: 'text-blue-400',
  legendary: 'text-yellow-400',
};

export default function PowerUpShop({ coins = 0, owned = {}, onBuy, onUse }) {
  const [tab, setTab] = useState('shop');

  return (
    <div className="bg-gray-900/60 border border-gray-700/30 rounded-2xl overflow-hidden">
      {/* Tabs */}
      <div className="flex border-b border-gray-700/30">
        <button
          onClick={() => setTab('shop')}
          className={`flex-1 py-2.5 text-xs font-mono uppercase tracking-wider transition-colors ${
            tab === 'shop' ? 'text-cyber-blue border-b-2 border-cyber-blue bg-cyber-blue/5' : 'text-gray-500 hover:text-gray-300'
          }`}
        >
          Shop
        </button>
        <button
          onClick={() => setTab('inventory')}
          className={`flex-1 py-2.5 text-xs font-mono uppercase tracking-wider transition-colors ${
            tab === 'inventory' ? 'text-cyber-purple border-b-2 border-cyber-purple bg-cyber-purple/5' : 'text-gray-500 hover:text-gray-300'
          }`}
        >
          Inventory
        </button>
      </div>

      {/* Coins display */}
      <div className="px-4 py-3 flex items-center justify-between border-b border-gray-700/20">
        <span className="text-xs font-mono text-gray-500">Your Coins</span>
        <span className="text-sm font-display font-bold text-yellow-400">💰 {coins}</span>
      </div>

      {/* Content */}
      <div className="p-3 space-y-2 max-h-64 overflow-y-auto">
        {tab === 'shop' ? (
          POWER_UP_LIST.map((up) => {
            const canAfford = coins >= up.cost;
            return (
              <motion.div
                key={up.id}
                whileHover={{ scale: 1.01 }}
                className={`flex items-center gap-3 p-3 rounded-xl border ${RARITY_COLORS[up.rarity]} transition-all`}
              >
                <span className="text-2xl">{up.emoji}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-display font-bold text-text-primary">{up.name}</span>
                    <span className={`text-[8px] font-mono uppercase ${RARITY_TEXT[up.rarity]}`}>{up.rarity}</span>
                  </div>
                  <p className="text-[10px] font-mono text-gray-500">{up.description}</p>
                </div>
                <button
                  onClick={() => onBuy?.(up.id)}
                  disabled={!canAfford}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-mono font-bold transition-all ${
                    canAfford
                      ? 'bg-yellow-500/15 text-yellow-400 border border-yellow-500/30 hover:bg-yellow-500/25'
                      : 'bg-gray-700/20 text-gray-600 border border-gray-700/20 cursor-not-allowed'
                  }`}
                >
                  💰 {up.cost}
                </button>
              </motion.div>
            );
          })
        ) : (
          POWER_UP_LIST.map((up) => {
            const count = owned[up.id] || 0;
            if (count === 0) return null;
            return (
              <motion.div
                key={up.id}
                whileHover={{ scale: 1.01 }}
                className="flex items-center gap-3 p-3 rounded-xl border border-gray-700/20 bg-gray-800/30"
              >
                <span className="text-2xl">{up.emoji}</span>
                <div className="flex-1">
                  <span className="text-xs font-display font-bold text-text-primary">{up.name}</span>
                  <p className="text-[10px] font-mono text-gray-500">{up.description}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-gray-400">×{count}</span>
                  <button
                    onClick={() => onUse?.(up.id)}
                    className="px-3 py-1.5 rounded-lg text-[10px] font-mono font-bold bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30 hover:bg-cyber-blue/25 transition-all"
                  >
                    Use
                  </button>
                </div>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
}
