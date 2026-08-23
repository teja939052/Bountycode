import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Map, GitBranch, Lock, Unlock, Check, Trophy, Star, Zap, Flag,
  Sparkles, MapPin, ChevronRight, ChevronDown, Info, X, ArrowRight,
} from 'lucide-react';
import { worldApi } from '../services/api/world.ts';
import { useToast } from '../components/Toast';

/* ── Region positions on the SVG map (percentage-based) ── */
const REGION_NODES: Record<string, { x: number; y: number; terrain: string; color: string; glow: string }> = {
  village:        { x: 12, y: 75, terrain: 'grass',   color: '#4F8F57', glow: '#4F8F5740' },
  forest:         { x: 30, y: 55, terrain: 'forest',  color: '#2D6A3F', glow: '#2D6A3F40' },
  mountain:       { x: 50, y: 35, terrain: 'rock',    color: '#8B7355', glow: '#8B735540' },
  'cyber-city':   { x: 68, y: 50, terrain: 'neon',    color: '#7C3AED', glow: '#7C3AED40' },
  'silicon-valley':{ x: 82, y: 30, terrain: 'tech',   color: '#2563EB', glow: '#2563EB40' },
  'faang-castle': { x: 92, y: 12, terrain: 'castle',  color: '#DC2626', glow: '#DC262640' },
};

/* SVG path connecting regions (curved waypoints) */
const MAP_PATH = 'M 12 75 C 18 70, 24 60, 30 55 C 36 50, 42 40, 50 35 C 56 32, 60 42, 68 50 C 73 55, 76 40, 82 30 C 86 24, 88 18, 92 12';

/* Terrain SVG patterns */
function TerrainPattern({ id, terrain }: { id: string; terrain: string }) {
  if (terrain === 'forest') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#1a472a" />
      <circle cx="10" cy="8" r="5" fill="#2d6a3f" />
      <circle cx="5" cy="14" r="4" fill="#1f5c33" />
      <circle cx="15" cy="14" r="4" fill="#2d6a3f" />
    </pattern>
  );
  if (terrain === 'grass') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#4F8F57" />
      <line x1="5" y1="20" x2="5" y2="12" stroke="#6ab063" strokeWidth="1.5" />
      <line x1="12" y1="20" x2="12" y2="10" stroke="#5da055" strokeWidth="1" />
      <line x1="18" y1="20" x2="18" y2="14" stroke="#6ab063" strokeWidth="1" />
    </pattern>
  );
  if (terrain === 'rock') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#6b5b3e" />
      <polygon points="10,2 18,18 2,18" fill="#8b7355" opacity="0.6" />
      <polygon points="4,5 10,0 16,5 12,12" fill="#7a6848" opacity="0.4" />
    </pattern>
  );
  if (terrain === 'neon') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#1e1040" />
      <line x1="0" y1="10" x2="20" y2="10" stroke="#7C3AED" strokeWidth="0.5" opacity="0.5" />
      <line x1="10" y1="0" x2="10" y2="20" stroke="#a855f7" strokeWidth="0.5" opacity="0.3" />
      <circle cx="10" cy="10" r="2" fill="#c084fc" opacity="0.4" />
    </pattern>
  );
  if (terrain === 'tech') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#172554" />
      <rect x="3" y="3" width="6" height="6" fill="#2563EB" opacity="0.3" />
      <rect x="11" y="11" width="6" height="6" fill="#3b82f6" opacity="0.2" />
    </pattern>
  );
  if (terrain === 'castle') return (
    <pattern id={id} patternUnits="userSpaceOnUse" width="20" height="20">
      <rect width="20" height="20" fill="#450a0a" />
      <rect x="2" y="2" width="5" height="16" fill="#7f1d1d" opacity="0.5" />
      <rect x="9" y="6" width="5" height="12" fill="#991b1b" opacity="0.4" />
    </pattern>
  );
  return <pattern id={id}><rect width="20" height="20" fill="#333" /></pattern>;
}

/* ── SVG Skill Tree ── */
function SkillTreeSVG({ nodes, unlockedNodes, totalXp, onUnlock, unlockingId }: {
  nodes: any[];
  unlockedNodes: Set<string>;
  totalXp: number;
  onUnlock: (node: any) => void;
  unlockingId: string | null;
}) {
  /* Layout: depth → column, children centered under parents */
  const depthGroups: Record<number, any[]> = {};
  nodes.forEach(n => { (depthGroups[n.depth] ??= []).push(n); });
  const maxDepth = Math.max(...Object.keys(depthGroups).map(Number), 0);

  const TREE_W = 900;
  const TREE_H = 120 + maxDepth * 140;
  const COL_W = TREE_W / (maxDepth + 1);

  /* Compute positions */
  const pos: Record<string, { x: number; y: number }> = {};
  Object.entries(depthGroups).forEach(([d, group]) => {
    const depth = Number(d);
    const spacing = COL_W / (group.length + 1);
    group.forEach((node, i) => {
      pos[node.id] = {
        x: depth * COL_W + spacing * (i + 1),
        y: 70 + depth * 140,
      };
    });
  });

  return (
    <svg viewBox={`0 0 ${TREE_W} ${TREE_H}`} className="w-full h-auto" style={{ minHeight: 400 }}>
      <defs>
        <filter id="glow-green">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <filter id="glow-amber">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <linearGradient id="path-grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#4F8F57" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#7BB661" stopOpacity="0.3" />
        </linearGradient>
        <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#4F8F57" opacity="0.5" />
        </marker>
      </defs>

      {/* Connection lines */}
      {nodes.map(node => {
        if (!node.parent_id || !pos[node.parent_id] || !pos[node.id]) return null;
        const from = pos[node.parent_id];
        const to = pos[node.id];
        const bothUnlocked = unlockedNodes.has(node.id) && unlockedNodes.has(node.parent_id);
        const midX = (from.x + to.x) / 2;
        const midY = (from.y + to.y) / 2 - 20;
        return (
          <path
            key={`edge-${node.id}`}
            d={`M ${from.x} ${from.y} Q ${midX} ${midY} ${to.x} ${to.y}`}
            fill="none"
            stroke={bothUnlocked ? '#4F8F57' : '#d1d5db'}
            strokeWidth={bothUnlocked ? 3 : 2}
            strokeDasharray={bothUnlocked ? 'none' : '8 4'}
            opacity={bothUnlocked ? 0.8 : 0.4}
          />
        );
      })}

      {/* Nodes */}
      {nodes.map(node => {
        const p = pos[node.id];
        if (!p) return null;
        const isUnlocked = unlockedNodes.has(node.id);
        const parentOk = !node.parent_id || unlockedNodes.has(node.parent_id);
        const affordable = totalXp >= node.xp_cost;
        const canBuy = parentOk && !isUnlocked && affordable;
        const isUnlocking = unlockingId === node.id;

        return (
          <g key={node.id} style={{ cursor: canBuy ? 'pointer' : 'default' }}
             onClick={() => canBuy && onUnlock(node)}>
            {/* Background circle */}
            <circle
              cx={p.x} cy={p.y} r={32}
              fill={isUnlocked ? '#D9EFCF' : parentOk ? '#F0FDF4' : '#f3f4f6'}
              stroke={isUnlocked ? '#4F8F57' : canBuy ? '#B8D9A8' : '#E5E0D3'}
              strokeWidth={isUnlocked ? 3 : 2}
              filter={isUnlocked ? 'url(#glow-green)' : undefined}
            />
            {/* Icon */}
            <text x={p.x} y={p.y + 6} textAnchor="middle" fontSize="24" dominantBaseline="middle">
              {node.icon}
            </text>
            {/* Name */}
            <text x={p.x} y={p.y + 50} textAnchor="middle" fontSize="11" fontWeight="600"
                  fill={isUnlocked || parentOk ? '#1F2937' : '#9CA3AF'} fontFamily="system-ui">
              {node.name}
            </text>
            {/* Perk */}
            <text x={p.x} y={p.y + 65} textAnchor="middle" fontSize="9" fill="#6B7280" fontFamily="monospace">
              {node.perk}
            </text>
            {/* XP cost badge */}
            <g transform={`translate(${p.x - 28}, ${p.y + 72})`}>
              <rect x="0" y="0" width="56" height="18" rx="9"
                    fill={isUnlocked ? '#D9EFCF' : affordable ? '#FEF3C7' : '#f3f4f6'}
                    stroke={isUnlocked ? '#4F8F57' : affordable ? '#F59E0B' : '#E5E0D3'}
                    strokeWidth="1" />
              <text x="28" y="13" textAnchor="middle" fontSize="9" fontWeight="600" fontFamily="monospace"
                    fill={isUnlocked ? '#4F8F57' : affordable ? '#D97706' : '#9CA3AF'}>
                {isUnlocked ? '✓ Learned' : `${node.xp_cost} XP`}
              </text>
            </g>
            {/* Buy button ring */}
            {canBuy && (
              <circle cx={p.x} cy={p.y} r={36} fill="none" stroke="#4F8F57" strokeWidth="2"
                      strokeDasharray="6 3" opacity="0.5">
                <animateTransform attributeName="transform" type="rotate"
                                  from={`0 ${p.x} ${p.y}`} to={`360 ${p.x} ${p.y}`}
                                  dur="8s" repeatCount="indefinite" />
              </circle>
            )}
            {/* Unlocking spinner */}
            {isUnlocking && (
              <circle cx={p.x} cy={p.y} r={34} fill="none" stroke="#4F8F57" strokeWidth="3"
                      strokeDasharray="30 170" opacity="0.8">
                <animateTransform attributeName="transform" type="rotate"
                                  from={`0 ${p.x} ${p.y}`} to={`360 ${p.x} ${p.y}`}
                                  dur="1s" repeatCount="indefinite" />
              </circle>
            )}
          </g>
        );
      })}
    </svg>
  );
}

export default function WorldMap() {
  const [activeTab, setActiveTab] = useState('map');
  const [mapData, setMapData] = useState<any>(null);
  const [treeData, setTreeData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [advancing, setAdvancing] = useState(false);
  const [unlockingId, setUnlockingId] = useState<string | null>(null);
  const [selectedRegion, setSelectedRegion] = useState<any>(null);
  const [hoverRegion, setHoverRegion] = useState<string | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
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

  useEffect(() => { load(); }, []);

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
    } catch (err: any) {
      toast.error(err.message || 'Failed to advance');
    }
    setAdvancing(false);
  };

  const handleUnlock = async (node: any) => {
    setUnlockingId(node.id);
    try {
      const res = await worldApi.unlockNode(node.id);
      if (res.already_unlocked) {
        toast.info('Node already unlocked');
      } else {
        toast.success(`${node.icon} ${node.name} unlocked!`);
      }
      setTreeData(res);
    } catch (err: any) {
      toast.error(err.message || 'Failed to unlock node');
    }
    setUnlockingId(null);
  };

  const regions = mapData?.regions || [];
  const unlockedSet = new Set(mapData?.unlocked_regions || []);
  const currentId = mapData?.current_region?.id || 'village';
  const nextRegion = mapData?.next_region || null;
  const canAdvance = nextRegion && mapData?.total_xp >= nextRegion.xp_required_to_unlock;
  const unlockedNodes = new Set(treeData?.unlocked_node_ids || []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-3 border-[#4F8F57] border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0f0d] text-text-primary py-6 px-4">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="flex flex-col items-center mb-6">
          <h1 className="text-3xl font-bold font-display bg-gradient-to-r from-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent mb-2">
            World Map
          </h1>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400">
              <Zap size={12} />
              {mapData?.total_xp?.toLocaleString() ?? 0} XP
            </span>
            <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#4F8F57]/10 border border-[#4F8F57]/30 text-[#7BB661]">
              <MapPin size={12} />
              {unlockedSet.size}/{regions.length} regions
            </span>
            {nextRegion && (
              <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border-border shadow-card border border-white/10 text-gray-400">
                <Flag size={12} />
                Next: {nextRegion.name}
              </span>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex justify-center gap-2 mb-8">
          {[
            { id: 'map', label: 'World Map', icon: Map },
            { id: 'skill', label: 'Skill Tree', icon: GitBranch },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl border text-sm font-semibold transition-all ${
                activeTab === tab.id
                  ? 'border-[#4F8F57]/60 bg-[#4F8F57]/15 text-[#7BB661] shadow-[0_0_20px_rgba(79,143,87,0.2)]'
                  : 'border-white/10 bg-white border-border shadow-card text-gray-400 hover:text-white hover:border-white/20'
              }`}
            >
              <tab.icon size={16} />
              {tab.label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'map' ? (
            <motion.div key="map" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              {/* Progress bar */}
              {nextRegion && (
                <div className="rounded-2xl border border-white/10 bg-white border-border shadow-card backdrop-blur p-5 mb-8">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono uppercase tracking-wider text-gray-500">
                      Progress to {nextRegion.emoji} {nextRegion.name}
                    </span>
                    <span className="text-xs font-mono text-gray-400">
                      {mapData.total_xp.toLocaleString()} / {nextRegion.xp_required_to_unlock.toLocaleString()} XP
                    </span>
                  </div>
                  <div className="h-3 rounded-full bg-white border-border shadow-card overflow-hidden">
                    <motion.div
                      className="h-full rounded-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661]"
                      initial={{ width: 0 }}
                      animate={{ width: `${mapData.progress_percent}%` }}
                      transition={{ duration: 1, ease: 'easeOut' }}
                    />
                  </div>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-xs text-gray-500 font-mono">{mapData.progress_percent}%</span>
                    <button
                      onClick={handleAdvance}
                      disabled={!canAdvance || advancing}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                        canAdvance
                          ? 'bg-gradient-to-r from-[#4F8F57] to-[#7BB661] text-text-primary hover:opacity-90 shadow-[0_0_24px_rgba(79,143,87,0.35)]'
                          : 'bg-white border-border shadow-card text-gray-500 cursor-not-allowed border border-white/10'
                      }`}
                    >
                      {advancing ? (
                        <div className="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
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

              {/* ── Interactive SVG World Map ── */}
              <div className="relative rounded-2xl border border-white/10 bg-gradient-to-br from-[#0a1a10] via-[#0d1f14] to-[#081208] overflow-hidden p-2">
                {/* Background stars */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                  {Array.from({ length: 40 }).map((_, i) => (
                    <div key={i} className="absolute w-px h-px bg-white rounded-full"
                         style={{
                           left: `${(i * 37 + 13) % 100}%`,
                           top: `${(i * 23 + 7) % 100}%`,
                           opacity: 0.15 + (i % 5) * 0.08,
                           animationDelay: `${i * 0.3}s`,
                         }} />
                  ))}
                </div>

                <svg ref={svgRef} viewBox="0 0 100 90" className="w-full h-auto relative z-10" style={{ minHeight: 320 }}>
                  <defs>
                    {/* Glow filter for current node */}
                    <filter id="current-glow">
                      <feGaussianBlur stdDeviation="2" result="blur" />
                      <feMerge>
                        <feMergeNode in="blur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                    <filter id="node-shadow">
                      <feDropShadow dx="0" dy="1" stdDeviation="1" floodOpacity="0.3" />
                    </filter>
                    {/* Path gradient */}
                    <linearGradient id="mainPathGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#4F8F57" stopOpacity="0.8" />
                      <stop offset="50%" stopColor="#7BB661" stopOpacity="0.5" />
                      <stop offset="100%" stopColor="#DC2626" stopOpacity="0.3" />
                    </linearGradient>
                  </defs>

                  {/* Background terrain regions */}
                  <ellipse cx="12" cy="78" rx="14" ry="10" fill="#1a3a20" opacity="0.3" />
                  <ellipse cx="30" cy="58" rx="16" ry="12" fill="#142a1a" opacity="0.3" />
                  <ellipse cx="50" cy="38" rx="15" ry="14" fill="#2a2418" opacity="0.3" />
                  <ellipse cx="68" cy="53" rx="14" ry="12" fill="#1a1040" opacity="0.3" />
                  <ellipse cx="82" cy="33" rx="14" ry="12" fill="#0f1a3a" opacity="0.3" />
                  <ellipse cx="92" cy="15" rx="12" ry="12" fill="#2a0a0a" opacity="0.3" />

                  {/* Main winding path — unlocked segments */}
                  <path d={MAP_PATH} fill="none" stroke="url(#mainPathGrad)" strokeWidth="0.6"
                        strokeLinecap="round" opacity="0.6" />

                  {/* Particle trail along path */}
                  <circle r="0.8" fill="#7BB661" opacity="0.7">
                    <animateMotion dur="6s" repeatCount="indefinite" path={MAP_PATH} />
                  </circle>
                  <circle r="0.5" fill="#4F8F57" opacity="0.5">
                    <animateMotion dur="6s" repeatCount="indefinite" path={MAP_PATH} begin="2s" />
                  </circle>

                  {/* Region nodes */}
                  {regions.map((region) => {
                    const nodeInfo = REGION_NODES[region.id];
                    if (!nodeInfo) return null;
                    const isUnlocked = unlockedSet.has(region.id);
                    const isCurrent = currentId === region.id;
                    const isHovered = hoverRegion === region.id;
                    const x = nodeInfo.x;
                    const y = nodeInfo.y;

                    return (
                      <g key={region.id}
                         style={{ cursor: 'pointer' }}
                         onClick={() => setSelectedRegion(region)}
                         onMouseEnter={() => setHoverRegion(region.id)}
                         onMouseLeave={() => setHoverRegion(null)}>
                        {/* Glow ring for current */}
                        {isCurrent && (
                          <circle cx={x} cy={y} r={isHovered ? 7.5 : 6.5} fill="none"
                                  stroke={nodeInfo.color} strokeWidth="0.5" opacity="0.4">
                            <animate attributeName="r" values="5.5;7.5;5.5" dur="2s" repeatCount="indefinite" />
                            <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2s" repeatCount="indefinite" />
                          </circle>
                        )}

                        {/* Outer ring — unlocked glow */}
                        {isUnlocked && (
                          <circle cx={x} cy={y} r={isHovered ? 5.5 : 4.5} fill="none"
                                  stroke={nodeInfo.color} strokeWidth="0.4" opacity="0.5" />
                        )}

                        {/* Main circle */}
                        <circle cx={x} cy={y} r={isHovered ? 4.8 : 4}
                                fill={isUnlocked ? nodeInfo.color : isCurrent ? nodeInfo.color : '#2a2a2a'}
                                stroke={isUnlocked ? nodeInfo.color : '#555'}
                                strokeWidth={isCurrent ? 0.8 : 0.4}
                                opacity={isUnlocked || isCurrent ? 1 : 0.5}
                                filter={isCurrent ? 'url(#current-glow)' : undefined} />

                        {/* Emoji */}
                        <text x={x} y={y + 0.2} textAnchor="middle" dominantBaseline="central"
                              fontSize={isHovered ? 4.2 : 3.8} style={{ pointerEvents: 'none' }}>
                          {region.emoji}
                        </text>

                        {/* Region name label */}
                        <text x={x} y={y + (y > 50 ? 7 : -6)} textAnchor="middle" fontSize="2.4"
                              fontWeight="700" fontFamily="system-ui"
                              fill={isUnlocked || isCurrent ? '#e5e7eb' : '#6b7280'}
                              opacity={isHovered || isCurrent ? 1 : 0.7}
                              style={{ pointerEvents: 'none' }}>
                          {region.name}
                        </text>

                        {/* Status badge */}
                        {isCurrent && (
                          <g transform={`translate(${x - 3.5}, ${y + (y > 50 ? 8.5 : -10)})`}>
                            <rect x="0" y="0" width="7" height="2.5" rx="1.25"
                                  fill={nodeInfo.color} opacity="0.9" />
                            <text x="3.5" y="1.7" textAnchor="middle" fontSize="1.6" fontWeight="700"
                                  fill="white" fontFamily="monospace" style={{ pointerEvents: 'none' }}>
                              HERE
                            </text>
                          </g>
                        )}

                        {/* Lock icon for locked regions */}
                        {!isUnlocked && !isCurrent && (
                          <g transform={`translate(${x + 2.5}, ${y - 4})`}>
                            <circle cx="0" cy="0" r="1.8" fill="#1a1a1a" stroke="#555" strokeWidth="0.3" />
                            <text x="0" y="0.5" textAnchor="middle" fontSize="2" fill="#999"
                                  style={{ pointerEvents: 'none' }}>🔒</text>
                          </g>
                        )}
                      </g>
                    );
                  })}
                </svg>
              </div>

              {/* ── Region Detail Panel ── */}
              <AnimatePresence>
                {selectedRegion && (
                  <motion.div
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 20, scale: 0.95 }}
                    className="mt-6 rounded-2xl border border-white/10 bg-white border-border shadow-card backdrop-blur p-6"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <div className="text-5xl">{selectedRegion.emoji}</div>
                        <div>
                          <h3 className="text-xl font-bold text-text-primary">{selectedRegion.name}</h3>
                          <p className="text-sm text-gray-400 mt-1 max-w-md">{selectedRegion.description}</p>
                        </div>
                      </div>
                      <button onClick={() => setSelectedRegion(null)}
                              className="p-2 rounded-lg text-gray-500 hover:text-white hover:bg-white border-border/10 transition-all">
                        <X size={18} />
                      </button>
                    </div>
                    <div className="flex items-center gap-4 text-xs font-mono">
                      <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400">
                        <Trophy size={12} />
                        Badge: {selectedRegion.reward_badge}
                      </span>
                      <span className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full ${
                        unlockedSet.has(selectedRegion.id)
                          ? 'bg-[#4F8F57]/10 border border-[#4F8F57]/30 text-[#7BB661]'
                          : 'bg-white border-border shadow-card border border-white/10 text-gray-400'
                      }`}>
                        {unlockedSet.has(selectedRegion.id) ? <Unlock size={12} /> : <Lock size={12} />}
                        {unlockedSet.has(selectedRegion.id) ? 'Unlocked' : `${selectedRegion.xp_required_to_unlock.toLocaleString()} XP needed`}
                      </span>
                      <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border-border shadow-card border border-white/10 text-gray-400">
                        <Star size={12} />
                        Region {selectedRegion.order}
                      </span>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* ── Region list below map ── */}
              <div className="mt-8 grid grid-cols-2 md:grid-cols-3 gap-3">
                {regions.map((region: any) => {
                  const isUnlocked = unlockedSet.has(region.id);
                  const isCurrent = currentId === region.id;
                  const nodeInfo = REGION_NODES[region.id];
                  return (
                    <button key={region.id} onClick={() => setSelectedRegion(region)}
                      className={`text-left rounded-xl border p-4 transition-all ${
                        isCurrent
                          ? 'border-[#4F8F57]/40 bg-[#4F8F57]/10'
                          : isUnlocked
                          ? 'border-white/10 bg-white border-border shadow-card hover:bg-white border-border/10'
                          : 'border-white/5 bg-white/[0.02] opacity-60'
                      }`}>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xl">{region.emoji}</span>
                        <span className="text-sm font-semibold text-text-primary">{region.name}</span>
                        {isCurrent && <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#4F8F57]/20 text-[#7BB661]">HERE</span>}
                      </div>
                      <p className="text-xs text-gray-500 line-clamp-2">{region.description}</p>
                    </button>
                  );
                })}
              </div>
            </motion.div>
          ) : (
            /* ── Skill Tree Tab ── */
            <motion.div key="skill" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <div className="rounded-2xl border border-white/10 bg-white border-border shadow-card backdrop-blur p-5 mb-6 flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-text-primary">Skill Tree</h3>
                  <p className="text-xs text-gray-500 mt-1 font-mono">
                    {unlockedNodes.size}/{treeData?.nodes?.length || 0} skills learned
                  </p>
                </div>
                <div className="flex items-center gap-1.5 text-xs font-mono text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg px-3 py-1.5">
                  <Zap size={12} />
                  {mapData?.total_xp ?? 0} XP available
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white border-border shadow-card backdrop-blur p-4 overflow-x-auto">
                <SkillTreeSVG
                  nodes={treeData?.nodes || []}
                  unlockedNodes={unlockedNodes}
                  totalXp={mapData?.total_xp ?? 0}
                  onUnlock={handleUnlock}
                  unlockingId={unlockingId}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
