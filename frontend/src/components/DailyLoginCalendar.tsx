import { motion } from "framer-motion";

const REWARD_ICONS: Record<string, string> = {
  hint_reveal: "💡",
  speed_boost: "🚀",
  double_xp: "⚡",
  skip_boss: "🛡️",
};

export default function DailyLoginCalendar({ calendar = [], streak = 0, onClaim }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-gray-200 flex items-center gap-2">
            📅 Daily Login Rewards
          </h3>
          <p className="text-xs text-gray-500 mt-0.5">{streak} day{streak !== 1 ? 's' : ''} claimed</p>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-2">
        {calendar.map((day, i) => {
          const icon = REWARD_ICONS[day.power_up as string] || "🎁";
          return (
            <motion.div
              key={day.day}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }}
              className={`relative rounded-xl p-2 text-center border ${
                day.claimed
                  ? "bg-green-500/10 border-green-500/30"
                  : "bg-white/[0.03] border-white/5"
              }`}
            >
              <div className="text-[10px] font-mono text-gray-500 mb-1">{day.label}</div>
              <div className="text-xl mb-1">{icon}</div>
              <div className="text-[10px] font-bold text-gray-300">+{day.diamonds} Diamonds</div>
              <div className="text-[10px] text-yellow-400">+{day.coins} 🪙</div>
              {day.claimed && (
                <div className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-green-500 flex items-center justify-center text-[10px] text-white">
                  ✓
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {onClaim && (
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onClaim}
          className="mt-4 w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-sm hover:from-indigo-500 hover:to-purple-500 transition-colors"
        >
          Claim Today&apos;s Reward
        </motion.button>
      )}
    </div>
  );
}
