import { motion } from "framer-motion";
import { Gift, CheckCircle, Flame } from "lucide-react";
import { useToast } from "../components/Toast";

const DAYS = 30;

export default function DailyBonusCalendar({ dailyBonus, claiming, onClaim }) {
  const toast = useToast();
  const today = new Date().toISOString().slice(0, 10);
  const streak = dailyBonus.login_streak || 0;
  const lastClaimed = dailyBonus.last_claimed;
  const claimedToday = lastClaimed === today;

  const cells = [];
  for (let i = DAYS - 1; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    cells.push(d.toISOString().slice(0, 10));
  }

  const cellFor = (date) => dailyBonus.history?.find((h) => h.date === date);

  const streakTierLabel = (n) => {
    if (n <= 1) return "10 XP";
    if (n <= 3) return "25 XP";
    if (n <= 5) return "50 XP";
    return "100 XP";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-4"
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Gift size={16} className="text-brand-gold" />
          <span className="font-display font-bold text-sm text-brand-primary">Daily Bonus</span>
          {streak > 0 && (
            <span className="inline-flex items-center gap-1 text-xs text-brand-emerald bg-brand-emerald/10 px-2 py-0.5 rounded-full">
              <Flame size={12} /> {streak}-day streak
            </span>
          )}
        </div>
        {claimedToday ? (
          <span className="text-xs text-text-secondary">Claimed today</span>
        ) : (
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            disabled={claiming}
            onClick={onClaim}
            className="text-xs font-medium text-brand-gold hover:text-brand-primary bg-brand-gold/10 hover:bg-brand-gold/20 border border-brand-gold/30 rounded-lg px-3 py-1.5 transition"
          >
            {claiming ? "Claiming…" : `Claim (${streakTierLabel(streak + 1)})`}
          </motion.button>
        )}
      </div>

      <div className="grid grid-cols-7 gap-[3px] text-[10px] text-text-secondary">
        {["M", "T", "W", "T", "F", "S", "S"].map((d, i) => (
          <div key={i} className="text-center opacity-50">{d}</div>
        ))}
        {cells.map((date) => {
          const entry = cellFor(date);
          const intensity = entry ? Math.min(1, (entry.xp || 0) / 25) : 0;
          let bg = "bg-gray-800";
          if (intensity > 0.75) bg = "bg-brand-emerald";
          else if (intensity > 0.5) bg = "bg-emerald-600";
          else if (intensity > 0.25) bg = "bg-emerald-800";
          else if (intensity > 0) bg = "bg-emerald-900";
          return (
            <motion.div
              key={date}
              whileHover={entry ? { scale: 1.15 } : {}}
              className={`aspect-square w-full rounded ${bg} flex items-center justify-center`}
              title={entry ? `${date}: +${entry.xp} XP` : `${date}: no bonus`}
            >
              {entry && entry.xp > 0 && (
                <CheckCircle size={8} className="text-text-primary" />
              )}
            </motion.div>
          );
        })}
      </div>
      <div className="mt-2 text-[10px] text-text-secondary">
        Log in daily to build a streak. Longer streaks unlock bigger rewards and
        bonus coins at streak milestones (7 / 30 / 60 / 100 days).
      </div>
    </motion.div>
  );
}
