import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Rocket, ChevronRight, CheckCircle2, Lock } from 'lucide-react';

const api = {
  worlds: () => fetch('/api/v1/curriculum/worlds', { credentials: 'include' }).then(r => r.json()),
  world: (id: string) => fetch(`/api/v1/curriculum/world/${id}`, { credentials: 'include' }).then(r => r.json()),
  progress: () => fetch('/api/v1/curriculum/progress', { credentials: 'include' }).then(r => r.json()),
  daily: () => fetch('/api/v1/curriculum/daily', { credentials: 'include' }).then(r => r.json()),
};

interface World { id: string; title: string; icon: string; description: string; order: number; competencies: number; unlocked: boolean; }
interface Competency { id: string; title: string; skills_taught: string[]; scenario: string; goal: string; step_count: number; completed: boolean; score: number; }
interface DailyPlan { day: string; type: string; icon: string; label: string; description: string; recommendation: { world_id: string; competency_id: string; title: string; scenario: string } | null; }

export default function CapabilityWorlds() {
  const [worlds, setWorlds] = useState<World[]>([]);
  const [selectedWorld, setSelectedWorld] = useState<string | null>(null);
  const [competencies, setCompetencies] = useState<Competency[]>([]);
  const [daily, setDaily] = useState<DailyPlan | null>(null);
  const [progress, setProgress] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.worlds(), api.progress(), api.daily()]).then(([w, p, d]) => {
      setWorlds(w.worlds || []);
      setProgress(p);
      setDaily(d);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (selectedWorld) {
      setLoading(true);
      api.world(selectedWorld).then(r => {
        setCompetencies(r.competencies || []);
        setLoading(false);
      });
    }
  }, [selectedWorld]);

  if (loading && !selectedWorld) {
    return <div className="min-h-screen bg-[#0a0e17] flex items-center justify-center"><div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" /></div>;
  }

  if (selectedWorld) {
    return <WorldDetailView worldId={selectedWorld} competencies={competencies} loading={loading} onBack={() => { setSelectedWorld(null); setCompetencies([]); }} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0d1525] to-[#0f172a] text-white">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-400 text-sm mb-4">
            <Rocket className="w-4 h-4" /> Capability Curriculum
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">
            Train the <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-amber-400 bg-clip-text text-transparent">capabilities</span> the job requires.
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Not topics. Not videos. Simulations that make you actually do the work.
          </p>
        </motion.div>

        {daily && daily.recommendation && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            className="mb-8 p-5 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 rounded-2xl">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-cyan-400 mb-1">{daily.icon} Today's Mission — {daily.label}</div>
                <div className="text-lg font-semibold">{daily.recommendation.title}</div>
                <div className="text-sm text-gray-400 mt-1">{daily.recommendation.scenario}</div>
              </div>
              <button onClick={() => { setSelectedWorld(daily.recommendation!.world_id); }}
                className="px-5 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg text-cyan-300 text-sm font-medium transition-colors flex items-center gap-2">
                Start <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}

        <div className="space-y-4">
          {worlds.map((world, i) => (
            <motion.button key={world.id}
              initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
              whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }}
              onClick={() => setSelectedWorld(world.id)}
              className={`w-full p-5 rounded-2xl border text-left transition-all flex items-center gap-5 ${
                world.unlocked ? 'bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/[0.07]' : 'bg-white/[0.02] border-white/5 opacity-50 cursor-not-allowed'
              }`}>
              <div className="text-4xl">{world.icon}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <span className="font-bold text-lg">{world.title}</span>
                  {!world.unlocked && <Lock className="w-4 h-4 text-gray-500" />}
                </div>
                <div className="text-sm text-gray-400">{world.description}</div>
                <div className="text-xs text-gray-500 mt-2">{world.competencies} competencies</div>
              </div>
              <ChevronRight className="w-5 h-5 text-gray-500 flex-shrink-0" />
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  );
}

function WorldDetailView({ worldId, competencies, loading, onBack }: { worldId: string; competencies: Competency[]; loading: boolean; onBack: () => void }) {
  if (loading) {
    return <div className="min-h-screen bg-[#0a0e17] flex items-center justify-center"><div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" /></div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0d1525] to-[#0f172a] text-white">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <button onClick={onBack} className="mb-6 px-4 py-2 text-gray-400 hover:text-white text-sm transition-colors">&larr; Back to Worlds</button>

        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">{competencies[0] ? '' : ''}{worldId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h2>
          <p className="text-gray-400">Complete all competencies to master this world.</p>
        </div>

        <div className="space-y-4">
          {competencies.map((comp, i) => (
            <motion.a key={comp.id}
              href={`/capability-mission/${worldId}/${comp.id}`}
              initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
              className="block p-5 rounded-2xl border bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/[0.07] transition-all group">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-sm font-bold ${
                  comp.completed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/10 text-gray-400'
                }`}>
                  {comp.completed ? <CheckCircle2 className="w-6 h-6" /> : <span>{i + 1}</span>}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-lg mb-1">{comp.title}</div>
                  <div className="text-sm text-gray-400 line-clamp-2">{comp.scenario}</div>
                  <div className="flex gap-2 mt-2 flex-wrap">
                    {comp.skills_taught.map(skill => (
                      <span key={skill} className="px-2 py-0.5 bg-white/5 rounded text-xs text-gray-400">{skill.replace(/_/g, ' ')}</span>
                    ))}
                  </div>
                </div>
                <div className="text-right flex-shrink-0">
                  <div className="text-sm text-gray-400">{comp.step_count} steps</div>
                  {comp.completed && <div className="text-sm text-emerald-400 mt-1">{comp.score}%</div>}
                </div>
                <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-white transition-colors flex-shrink-0" />
              </div>
            </motion.a>
          ))}
        </div>
      </div>
    </div>
  );
}
