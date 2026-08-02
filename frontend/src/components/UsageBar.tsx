import { motion } from "framer-motion";
import { Zap } from "lucide-react";

export default function UsageBar({ used, limit, feature, upgradeUrl = "/pricing?selected=pro", showUpgrade = true }) {
  const isPro = limit === "unlimited" || limit === -1 || (typeof limit === "number" && limit < 0);
  const percentage = isPro ? 0 : Math.min((used / limit) * 100, 100);
  const isLow = !isPro && percentage >= 70;
  const isCritical = !isPro && percentage >= 90;

  if (isPro) {
    return (
      <div className="glass p-3 flex items-center justify-between">
        <span className="text-xs text-gray-400">{feature}</span>
        <span className="text-xs text-green-400 font-medium">Unlimited</span>
      </div>
    );
  }

  return (
    <div className="glass p-3 space-y-2">
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">{feature}</span>
        <span className={`font-mono ${isCritical ? "text-red-400" : isLow ? "text-orange-400" : "text-gray-300"}`}>
          {used} / {limit} used
        </span>
      </div>
      <div className="h-1.5 bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className={`h-full rounded-full ${
            isCritical ? "bg-red-500" : isLow ? "bg-orange-500" : "bg-cyber-blue"
          }`}
        />
      </div>
      {isLow && showUpgrade && (
        <button
          onClick={() => (window.location.href = upgradeUrl)}
          className="text-xs text-cyber-blue hover:text-cyber-blue/80 font-medium flex items-center gap-1"
        >
          <Zap size={12} /> Upgrade to Pro
        </button>
      )}
    </div>
  );
}
