import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Map, GitBranch, Lock, Unlock, Check, Trophy, Star, Zap, Flag, Sparkles, MapPin, ChevronRight, Route } from 'lucide-react';
import { worldApi } from '../services/api/world.ts';
import { useToast } from '../components/Toast';

const lockState = {
  unlocked: { icon: Check, color: 'text-emerald-400', bg: 'border-emerald-500/40 bg-emerald-500/10', label: 'Unlocked' },
  current: { icon: MapPin, color: 'text-indigo-400', bg: 'border-indigo-500/50 bg-indigo-500/15', label: 'Current' },
  locked: { icon: Lock, color: 'text-slate-500', bg: 'border-white/10 bg-slate-900/60', label: 'Locked' },
};

export default function WorldMap() {
  const [activeTab, setActiveTab] = useState('map');
  const [mapData, setMapData] = useState(null);
  const [treeData, setTreeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [advancing, setAdvancing] = useState(false);
  const [unlockingId, setUnlockingId] = useState(null);
  const toast = useToast();

  const load = async () => {
    setLoading(true);
    try {
      const [mapRes, treeRes] = await Promise.all([
        worldApi.getMap().catch(() => null),
        worldApi.getTree().catch(() => null),
      ]);
      setMapData(mapRes);
      setTreeData(treeRes);
    } catch {}
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, []);

  const handleAdvance = async () => {
    if (!mapData?.next_region || mapData.total_xp < mapData.next_region.xp_required_to_unlock) return;
    setAdvancing(true);
    try {
      const res = await worldApi.advance();
      if (res.unlocked) {
        toast.success(`${res.unlocked_region.emoji} ${res.unlocked_region.name} unlocked!`);
      } else {
        toast.success(res.message || 'All regions unlocked');
      }
      setMapData(res);
    } catch (err) {
      toast.error(err.message || 'Failed to advance');
    }
    setAdvancing(false);
  };

  const handleUnlock = async (node) => {
    setUnlockingId(node.id);
    try {
      const res = await worldApi.unlockNode(node.id);
      if (res.already_unlocked) {
        toast.info('Node already unlocked');
      } else {
        toast.success(`${node.icon} ${node.name} unlocked!`);
      }
      setTreeData(res);
    } catch (err) {
      toast.error(err.message || 'Failed to unlock node');
    }
    setUnlockingId(null);
  };

  const regions = mapData?.regions || [];
  const unlocked = new Set(mapData?.unlocked_regions || []);
  const currentId = mapData?.current_region?.id || 'village';
  const nextRegion = mapData?.next_region || null;
  const canAdvance = nextRegion && mapData.total_xp >= nextRegion.xp_required_to_unlock;

  const unlockedNodes = new Set(treeData?.unlocked_node_ids || []);
  const depthGroups = (treeData?.nodes || []).reduce((acc, node) => {
    if (!acc[node.depth]) acc[node.depth] = [];
    acc[node.depth].push(node);
    return acc;
  }, []);
  const maxDepth = depthGroups.length;
  const depths = Array.from({ length: maxDepth }, (_, i) => depthGroups[i] || []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="spinner-cyber" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        <div className="flex flex-col items-center mb-8">
          <h1 className="text-3xl font-bold font-display bg-gradient-to-r from-emerald-400 to-indigo-400 bg-clip-text text-transparent mb-2">
            World Map
          </h1>
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <span className="flex items-center gap-1">
              <Zap size={14} className="text-amber-400" />
              {mapData?.total_xp ?? 0} XP
            </span>
            <span className="text-slate-600">|</span>
            <span className="flex items-center gap-1">
              <Route size={14} className="text-indigo-400" />
              {unlocked.size}/{regions.length} regions
            </span>
          </div>
        </div>

        <div className="flex justify-center gap-2 mb-10">
          {[
            { id: 'map', label: 'World Map', icon: Map },
            { id: 'skill', label: 'Skill Tree', icon: GitBranch },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl border text-sm font-semibold transition-all ${
                activeTab === tab.id
                  ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300 shadow-[0_0_20px_rgba(16,185,129,0.15)]'
                  : 'border-white/10 bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:border-white/20'
              }`}
            >
              <tab.icon size={16} />
              {tab.label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'map' ? (
            <motion.div
              key="map"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {nextRegion && (
                <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 mb-8">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono uppercase tracking-wider text-slate-500">
                      Progress to {nextRegion.name}
                    </span>
                    <span className="text-xs font-mono text-slate-400">
                      {mapData.total_xp.toLocaleString()} / {nextRegion.xp_required_to_unlock.toLocaleString()} XP
                    </span>
                  </div>
                  <div className="h-3 rounded-full bg-slate-800 overflow-hidden border border-white/10">
                    <motion.div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-indigo-500"
                      initial={{ width: 0 }}
                      animate={{ width: `${mapData.progress_percent}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                    />
                  </div>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-xs text-slate-500 font-mono">
                      {mapData.progress_percent}% complete
                    </span>
                    <button
                      onClick={handleAdvance}
                      disabled={!canAdvance || advancing}
                      className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                        canAdvance
                          ? 'bg-gradient-to-r from-emerald-500 to-indigo-500 text-white hover:opacity-90 shadow-[0_0_20px_rgba(16,185,129,0.3)]'
                          : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-white/10'
                      }`}
                    >
                      {advancing ? (
                        <span className="spinner-border spinner-border-sm" />
                      ) : (
                        <>
                          <Flag size={15} />
                          {canAdvance ? `Advance to ${nextRegion.name}` : `Need ${nextRegion.xp_required_to_unlock - mapData.total_xp} more XP`}
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}

              <div className="flex flex-col items-center">
                {regions.map((region, index) => {
                  const isUnlocked = unlocked.has(region.id);
                  const isCurrent = currentId === region.id;
                  const state = isCurrent ? lockState.current : isUnlocked ? lockState.unlocked : lockState.locked;
                  const StateIcon = state.icon;
                  return (
                    <div key={region.id} className="flex flex-col items-center w-full max-w-xl">
                      <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1, duration: 0.4 }}
                        className={`w-full rounded-2xl border p-5 transition-all ${state.bg} ${
                          isCurrent ? 'shadow-[0_0_30px_rgba(99,102,241,0.15)]' : ''
                        }`}
                      >
                        <div className="flex items-center gap-4">
                          <div className={`text-4xl ${isUnlocked ? '' : 'opacity-40 grayscale'}`}>
                            {region.emoji}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <h3 className={`font-semibold text-lg ${isUnlocked ? 'text-slate-100' : 'text-slate-500'}`}>
                                {region.name}
                              </h3>
                              <span className={`flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider ${state.color}`}>
                                <StateIcon size={12} />
                                {state.label}
                              </span>
                            </div>
                            <p className={`text-xs leading-relaxed mt-1 ${isUnlocked ? 'text-slate-400' : 'text-slate-600'}`}>
                              {region.description}
                            </p>
                            <div className="flex items-center gap-3 mt-2 text-[11px] font-mono">
                              <span className={`flex items-center gap-1 ${isUnlocked ? 'text-amber-400/80' : 'text-slate-600'}`}>
                                <Trophy size={11} />
                                {region.reward_badge}
                              </span>
                              <span className={`flex items-center gap-1 ${isUnlocked ? 'text-emerald-400/80' : 'text-slate-600'}`}>
                                <Star size={11} />
                                {region.order}. Region
                              </span>
                              {!isUnlocked && (
                                <span className="text-slate-600">
                                  {region.xp_required_to_unlock.toLocaleString()} XP
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </motion.div>
                      {index < regions.length - 1 && (
                        <div className="w-px h-10 bg-gradient-to-b from-emerald-500/50 to-indigo-500/50" />
                      )}
                    </div>
                  );
                })}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="skill"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 mb-8 flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-slate-100">Skill Tree</h3>
                  <p className="text-xs text-slate-500 mt-1">
                    {unlockedNodes.size}/{treeData?.nodes?.length || 0} skills unlocked
                  </p>
                </div>
                <div className="flex items-center gap-1 text-xs font-mono text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg px-3 py-1.5">
                  <Zap size={12} />
                  {mapData?.total_xp ?? 0} XP available
                </div>
              </div>

              <div className="overflow-x-auto pb-4">
                <div className="flex gap-4 min-w-max">
                  {depths.map((nodes, depth) => (
                    <div key={depth} className="flex flex-col gap-4">
                      <div className="text-center text-[10px] font-mono uppercase tracking-widest text-slate-600">
                        Depth {depth + 1}
                      </div>
                      {nodes.map((node) => {
                        const isUnlocked = unlockedNodes.has(node.id);
                        const parentUnlocked = !node.parent_id || unlockedNodes.has(node.parent_id);
                        const affordable = (mapData?.total_xp ?? 0) >= node.xp_cost;
                        const canUnlock = parentUnlocked && !isUnlocked && affordable;
                        const isUnlocking = unlockingId === node.id;
                        return (
                          <motion.div
                            key={node.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: depth * 0.1 }}
                            className={`w-56 rounded-xl border p-4 transition-all ${
                              isUnlocked
                                ? 'border-emerald-500/40 bg-emerald-500/10'
                                : parentUnlocked
                                ? 'border-indigo-500/40 bg-indigo-500/10'
                                : 'border-white/10 bg-slate-900/60'
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <div className={`text-2xl ${isUnlocked || parentUnlocked ? '' : 'opacity-40 grayscale'}`}>
                                {node.icon}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between gap-1">
                                  <h4 className={`text-sm font-semibold truncate ${isUnlocked || parentUnlocked ? 'text-slate-100' : 'text-slate-500'}`}>
                                    {node.name}
                                  </h4>
                                  {isUnlocked ? (
                                    <Check size={14} className="text-emerald-400 shrink-0" />
                                  ) : (
                                    <Lock size={14} className="text-slate-500 shrink-0" />
                                  )}
                                </div>
                                <p className={`text-[11px] mt-1 leading-snug ${isUnlocked || parentUnlocked ? 'text-slate-400' : 'text-slate-600'}`}>
                                  {node.perk}
                                </p>
                                <div className="flex items-center justify-between mt-3">
                                  <span className={`flex items-center gap-1 text-[10px] font-mono ${isUnlocked ? 'text-emerald-400' : affordable ? 'text-amber-400' : 'text-slate-500'}`}>
                                    <Sparkles size={10} />
                                    {node.xp_cost} XP
                                  </span>
                                  {isUnlocked ? (
                                    <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
                                      <Unlock size={10} />
                                      Learned
                                    </span>
                                  ) : parentUnlocked ? (
                                    <button
                                      onClick={() => handleUnlock(node)}
                                      disabled={!affordable || isUnlocking}
                                      className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-[10px] font-semibold transition-all ${
                                        affordable
                                          ? 'bg-gradient-to-r from-emerald-500 to-indigo-500 text-white hover:opacity-90'
                                          : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                                      }`}
                                    >
                                      {isUnlocking ? '...' : (
                                        <>
                                          <Unlock size={10} />
                                          Unlock
                                        </>
                                      )}
                                    </button>
                                  ) : (
                                    <span className="text-[10px] font-mono text-slate-600 flex items-center gap-1">
                                      <ChevronRight size={10} />
                                      Parent first
                                    </span>
                                  )}
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
