import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Zap, Battery, BatteryLow, Clock } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function EnergyPage() {
  const [energy, setEnergy] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const e = await api.get("/api/v1/energy");
      setEnergy(e);
    } catch { }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const consume = async (amount: number = 1) => {
    try {
      const r = await api.post("/api/v1/energy/consume", { amount });
      setEnergy(r.energy || r);
    } catch { }
  };

  const dailyBonus = async () => {
    try {
      const r = await api.post("/api/v1/energy/daily-bonus");
      setEnergy(r.energy || r);
    } catch { }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  const current = energy?.current ?? 0;
  const max = energy?.max ?? 100;
  const pct = Math.round((current / max) * 100);

  return (
    <div className="min-h-screen px-4 py-8 max-w-2xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3">
          <Zap size={14} className="text-amber-400" />
          <span className="text-xs font-mono text-amber-400">ENERGY</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Energy System</h1>
      </motion.div>

      {/* Energy Ring */}
      <div className="glass rounded-2xl p-8 text-center mb-6">
        <div className="relative w-40 h-40 mx-auto mb-4">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="42" stroke="currentColor" strokeWidth="8" fill="none" className="text-text-primary/5" />
            <circle cx="50" cy="50" r="42" stroke="currentColor" strokeWidth="8" fill="none"
              className="text-amber-400" strokeDasharray={`${pct * 2.64} 264`} strokeLinecap="round" />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            {current > max * 0.3 ? <Battery size={24} className="text-amber-400 mb-1" /> : <BatteryLow size={24} className="text-red-400 mb-1" />}
            <span className="text-2xl font-display font-black text-text-primary">{current}</span>
            <span className="text-[10px] font-mono text-gray-500">/ {max}</span>
          </div>
        </div>
        {energy?.recharge_at && (
          <p className="text-xs font-mono text-gray-500 flex items-center justify-center gap-1">
            <Clock size={12} /> Recharges at {new Date(energy.recharge_at).toLocaleTimeString()}
          </p>
        )}
      </div>

      {/* Actions */}
      <div className="grid grid-cols-2 gap-4">
        <button onClick={() => consume(1)}
          className="glass rounded-xl p-4 text-center hover:border-amber-500/20 transition-all">
          <Zap size={20} className="text-amber-400 mx-auto mb-2" />
          <p className="text-sm font-mono text-text-primary">Use 1 Energy</p>
          <p className="text-[10px] font-mono text-gray-500">Quick practice</p>
        </button>
        <button onClick={dailyBonus}
          className="glass rounded-xl p-4 text-center hover:border-emerald-500/20 transition-all">
          <Battery size={20} className="text-emerald-400 mx-auto mb-2" />
          <p className="text-sm font-mono text-text-primary">Daily Bonus</p>
          <p className="text-[10px] font-mono text-gray-500">Free energy refill</p>
        </button>
      </div>
    </div>
  );
}
