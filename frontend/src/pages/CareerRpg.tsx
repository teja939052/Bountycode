import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Crown, Swords, ScrollText, Map, ShieldCheck, Trophy, Zap,
  Lock, CheckCircle2, ChevronRight, Target, Flame, Loader2, RefreshCw,
  Star, Gem, Crosshair, BookOpen, Brain, Code2, Mic, Briefcase,
  Award, CircleDot, Anchor,
} from "lucide-react";
import { rpgApi } from "../services/api/rpg";
import { bountyApi } from "../services/api/bounty";
import { useJuice } from "../juice/JuiceProvider";
import { useNavigate } from "react-router-dom";
import BountyCard from "../components/BountyCard";
import Skeleton from "../components/ui/Skeleton";

const TABS = [
  { key: "rank", label: "Rank", icon: Crown },
  { key: "bounty", label: "Bounty", icon: Anchor },
  { key: "skilltree", label: "Skill Tree", icon: Map },
  { key: "quests", label: "Quests", icon: ScrollText },
  { key: "bosses", label: "Bosses", icon: Swords },
  { key: "dungeons", label: "Dungeons", icon: ShieldCheck },
  { key: "collections", label: "Collection", icon: Trophy },
];

const RARITY_COLORS: Record<string, string> = {
  common: "#9CA3AF",
  uncommon: "#22C55E",
  rare: "#3B82F6",
  epic: "#A855F7",
  legendary: "#F59E0B",
};

function formatXp(n: number) {
  return Number(n || 0).toLocaleString();
}

function GlowBar({ pct, color }: { pct: number; color: string }) {
  return (
    <div className="h-2.5 rounded-full bg-black/20 border border-white/10 overflow-hidden">
      <motion.div
        className="h-full rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        style={{ background: `linear-gradient(90deg, ${color}, ${color}cc)` }}
      />
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }: any) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 flex items-center gap-3">
      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${color}22`, border: `1px solid ${color}44` }}>
        <Icon className="w-5 h-5" style={{ color }} />
      </div>
      <div>
        <p className="text-lg font-bold text-white">{value}</p>
        <p className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{label}</p>
      </div>
    </div>
  );
}

/* ─── Rank Tab ─── */
function RankTab({ data }: any) {
  if (!data) return null;
  const { rank, level, xp, xp_to_next, readiness } = data;
  const pct = xp_to_next > 0 ? Math.min(100, Math.round((xp / (xp + xp_to_next)) * 100)) : 100;
  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}
        className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-transparent p-6 sm:p-8 overflow-hidden relative">
        <div className="absolute inset-x-0 top-0 h-1" style={{ background: rank.color }} />
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5 mb-6">
          <div className="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl border"
            style={{ borderColor: `${rank.color}66`, background: `${rank.color}14` }}>
            {rank.icon}
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="text-2xl sm:text-3xl font-display font-bold text-white">{rank.title}</h2>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold text-white border"
                style={{ borderColor: `${rank.color}66`, background: `${rank.color}33` }}>
                LEVEL {level}
              </span>
            </div>
            <p className="text-gray-400 mt-2 text-sm">{rank.description}</p>
          </div>
        </div>
        <div className="mb-2 flex items-center justify-between text-xs font-mono">
          <span className="text-gray-400">Progress to next rank</span>
          <span style={{ color: rank.color }}>{pct}%</span>
        </div>
        <GlowBar pct={pct} color={rank.color} />
        {xp_to_next > 0 && (
          <p className="mt-2 text-xs text-gray-500 font-mono">{formatXp(xp_to_next)} XP to next level</p>
        )}
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard icon={Zap} label="Total XP" value={formatXp(xp)} color="#F59E0B" />
        <StatCard icon={Target} label="Readiness" value={`${Math.round(readiness)}%`} color="#22C55E" />
        <StatCard icon={Trophy} label="Badges" value={data.total_badges} color="#A855F7" />
        <StatCard icon={Swords} label="Bosses Slain" value={data.bosses_defeated_count} color="#EF4444" />
      </div>
    </div>
  );
}

/* ─── Skill Tree Tab ─── */
function SkillTreeTab({ data }: any) {
  if (!data) return null;
  const { nodes, unlocked_count, total_nodes } = data;
  const pct = total_nodes > 0 ? Math.round((unlocked_count / total_nodes) * 100) : 0;
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-mono text-gray-400">Skill Tree</h3>
        <span className="text-xs font-mono text-green-400">{unlocked_count}/{total_nodes} unlocked ({pct}%)</span>
      </div>
      <GlowBar pct={pct} color="#22C55E" />
      <div className="relative overflow-x-auto pb-4">
        <svg width="800" height="650" viewBox="0 0 800 650" className="w-full max-w-3xl mx-auto">
          {nodes.map((node: any) =>
            node.prerequisites.map((pid: string) => {
              const parent = nodes.find((n: any) => n.id === pid);
              if (!parent) return null;
              return (
                <line key={`${pid}-${node.id}`} x1={parent.x} y1={parent.y} x2={node.x} y2={node.y}
                  stroke={node.unlocked ? "#22C55E66" : "#ffffff11"} strokeWidth={2} />
              );
            })
          )}
          {nodes.map((node: any) => {
            const bg = node.unlocked ? "#22C55E22" : "#ffffff08";
            const border = node.unlocked ? "#22C55E66" : "#ffffff15";
            const textColor = node.unlocked ? "#ffffff" : "#666";
            return (
              <g key={node.id}>
                <rect x={node.x - 50} y={node.y - 22} width={100} height={44} rx={12}
                  fill={bg} stroke={border} strokeWidth={1.5} />
                <text x={node.x} y={node.y + 1} textAnchor="middle" dominantBaseline="middle"
                  fill={textColor} fontSize={11} fontFamily="monospace" fontWeight={600}>
                  {node.icon} {node.name}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}

/* ─── Quests Tab ─── */
function QuestsTab({ data, onCompleteStep }: any) {
  if (!data) return null;
  return (
    <div className="space-y-4">
      {data.map((chain: any) => (
        <motion.div key={chain.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className={`rounded-2xl border p-5 transition-all ${chain.unlocked
            ? "border-white/10 bg-white/5 hover:border-green-500/30"
            : "border-white/5 bg-white/[0.02] opacity-60"
          }`}>
          <div className="flex items-start gap-4 mb-4">
            <div className="text-3xl">{chain.icon}</div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-bold text-white">{chain.title}</h4>
                {!chain.unlocked && <Lock className="w-3.5 h-3.5 text-gray-500" />}
                {chain.is_complete && <CheckCircle2 className="w-4 h-4 text-green-400" />}
              </div>
              <p className="text-xs text-gray-400 mt-0.5">{chain.description}</p>
              <div className="flex items-center gap-3 mt-2 text-[10px] font-mono text-gray-500">
                <span>{chain.completed_steps}/{chain.total_steps} steps</span>
                <span>{chain.progress_pct}%</span>
                <span>{formatXp(chain.reward_xp)} XP reward</span>
              </div>
              <GlowBar pct={chain.progress_pct} color={chain.is_complete ? "#22C55E" : "#3B82F6"} />
            </div>
          </div>
          {chain.unlocked && (
            <div className="space-y-2">
              {chain.steps.map((step: any) => {
                const stepKey = `${chain.id}_${step.id}`;
                const done = chain.completed_steps > 0 && false;
                return (
                  <div key={step.id} className="flex items-center gap-3 px-3 py-2 rounded-xl bg-black/20 border border-white/5">
                    <CircleDot className="w-4 h-4 text-gray-500 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-white font-medium truncate">{step.title}</p>
                      <p className="text-[10px] text-gray-500">{step.description}</p>
                    </div>
                    {!chain.is_complete && chain.unlocked && (
                      <button onClick={() => onCompleteStep(chain.id, step.id)}
                        className="text-[10px] font-mono text-green-400 hover:text-green-300 px-2 py-1 rounded-lg bg-green-500/10 border border-green-500/20 transition-all shrink-0">
                        Complete
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
}

/* ─── Bosses Tab ─── */
function BossesTab({ data }: any) {
  const navigate = useNavigate();
  if (!data) return null;
  return (
    <div className="space-y-4">
      {data.map((boss: any) => (
        <motion.div key={boss.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className={`rounded-2xl border p-5 transition-all ${boss.unlocked
            ? "border-white/10 bg-white/5 hover:border-red-500/30 cursor-pointer"
            : "border-white/5 bg-white/[0.02] opacity-60"
          }`}
          onClick={() => boss.unlocked && navigate(`/boss/${boss.id}`)}>
          <div className="flex items-center gap-4">
            <div className="text-3xl">{boss.icon}</div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-bold text-white">{boss.name}</h4>
                {boss.defeated && <CheckCircle2 className="w-4 h-4 text-green-400" />}
                {!boss.unlocked && <Lock className="w-3.5 h-3.5 text-gray-500" />}
              </div>
              <div className="flex items-center gap-3 mt-1 text-[10px] font-mono text-gray-500">
                <span>Pass: {boss.pass_score}%</span>
                <span>{boss.challenges?.length || 0} challenges</span>
                <span>{formatXp(boss.reward_xp)} XP</span>
              </div>
            </div>
            {boss.unlocked && !boss.defeated && (
              <ChevronRight className="w-5 h-5 text-gray-500" />
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
}

/* ─── Dungeons Tab ─── */
function DungeonsTab({ data }: any) {
  const navigate = useNavigate();
  if (!data) return null;
  return (
    <div className="space-y-4">
      {data.map((d: any) => (
        <motion.div key={d.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className={`rounded-2xl border p-5 transition-all ${d.unlocked
            ? "border-white/10 bg-white/5 hover:border-amber-500/30 cursor-pointer"
            : "border-white/5 bg-white/[0.02] opacity-60"
          }`}
          onClick={() => d.unlocked && navigate(`/dungeon/${d.id}`)}>
          <div className="flex items-center gap-4">
            <div className="text-3xl">{d.icon}</div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-bold text-white">{d.name}</h4>
                {d.cleared && <CheckCircle2 className="w-4 h-4 text-green-400" />}
                {!d.unlocked && <Lock className="w-3.5 h-3.5 text-gray-500" />}
              </div>
              <p className="text-[10px] text-gray-500 mt-0.5">
                {d.gates?.length || 0} gates + final boss
                {d.unlocked && !d.cleared && ` · Readiness needed: ${d.min_readiness}%`}
                {!d.unlocked && ` · Need ${Math.round(d.readiness_gap)}% more readiness`}
              </p>
            </div>
            {d.unlocked && !d.cleared && (
              <ChevronRight className="w-5 h-5 text-gray-500" />
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
}

/* ─── Collections Tab ─── */
function CollectionsTab({ data }: any) {
  if (!data) return null;
  return (
    <div className="space-y-6">
      {data.map((coll: any) => (
        <div key={coll.id}>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-lg">{coll.icon}</span>
              <h4 className="text-sm font-bold text-white">{coll.name}</h4>
            </div>
            <span className="text-[10px] font-mono text-gray-500">{coll.earned_count}/{coll.total_count}</span>
          </div>
          <GlowBar pct={coll.progress_pct} color="#A855F7" />
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 mt-3">
            {coll.items.map((item: any) => (
              <div key={item.id}
                className={`rounded-xl border p-3 text-center transition-all ${item.earned
                  ? "border-white/15 bg-white/5"
                  : "border-white/5 bg-white/[0.02] opacity-40"
                }`}>
                <div className="text-2xl mb-1">{item.icon}</div>
                <p className="text-[10px] font-bold text-white truncate">{item.name}</p>
                <span className="inline-block mt-1 px-2 py-0.5 rounded-full text-[8px] font-mono font-bold uppercase"
                  style={{ color: RARITY_COLORS[item.rarity] || "#999", background: `${RARITY_COLORS[item.rarity] || "#999"}22` }}>
                  {item.rarity}
                </span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── Bounty Tab ─── */
function BountyTab({ data }: { data: any }) {
  if (!data) return null;
  return (
    <div className="space-y-6">
      <div className="flex justify-center">
        <BountyCard user={data} size="large" showStats={true} />
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard icon={Zap} label="Total XP" value={formatXp(data.xp)} color="#F59E0B" />
        <StatCard icon={Target} label="Readiness" value={`${Math.round(data.readiness || 0)}%`} color="#22C55E" />
        <StatCard icon={Swords} label="Bosses Slain" value={data.bosses_defeated || 0} color="#EF4444" />
        <StatCard icon={ShieldCheck} label="Dungeons Cleared" value={data.dungeons_cleared || 0} color="#3B82F6" />
      </div>
    </div>
  );
}

/* ─── Main CareerRpg ─── */
export default function CareerRpg() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("rank");
  const [subData, setSubData] = useState<any>(null);
  const [subLoading, setSubLoading] = useState(false);
  const { showXP, play } = useJuice();

  const loadProfile = useCallback(async () => {
    setLoading(true);
    try {
      const d = await rpgApi.profile();
      setData(d);
    } catch (e: any) {
      setError(e.message || "Failed to load RPG profile");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadTab = useCallback(async (t: string) => {
    setSubLoading(true);
    try {
      let d;
      switch (t) {
        case "bounty": d = await bountyApi.myCard(); break;
        case "skilltree": d = await rpgApi.skillTree(); break;
        case "quests": d = await rpgApi.quests(); break;
        case "bosses": d = await rpgApi.bosses(); break;
        case "dungeons": d = await rpgApi.dungeons(); break;
        case "collections": d = await rpgApi.collections(); break;
        default: d = null;
      }
      setSubData(d);
    } catch {
      setSubData(null);
    } finally {
      setSubLoading(false);
    }
  }, []);

  useEffect(() => { loadProfile(); }, [loadProfile]);
  useEffect(() => { if (tab !== "rank") loadTab(tab); }, [tab, loadTab]);

  const handleCompleteStep = async (questId: string, stepId: string) => {
    try {
      const res = await rpgApi.completeQuestStep(questId, stepId);
      showXP(res.xp_earned, window.innerWidth / 2, window.innerHeight / 2);
      play(res.chain_complete ? "levelUp" : "xpCollect");
      loadTab("quests");
      loadProfile();
    } catch { /* ignore */ }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-5xl mx-auto">
        <Skeleton className="h-10 w-64 mb-3 bg-white/5" />
        <Skeleton className="h-5 w-96 mb-8 bg-white/5" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-20 rounded-2xl bg-white/5" />)}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
          {error || "Could not load RPG profile."}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black px-4 py-6 sm:py-10 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-display font-black text-white flex items-center gap-3">
            <Crown className="w-8 h-8 text-amber-400" />
            Career RPG
          </h1>
          <p className="text-gray-400 mt-1 text-sm">Level up. Defeat bosses. Claim your placement.</p>
        </div>
        <button onClick={() => { loadProfile(); loadTab(tab); }}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm font-medium hover:bg-white/10 transition-all">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 overflow-x-auto pb-2 scrollbar-hide">
        {TABS.map((t) => {
          const Icon = t.icon;
          return (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-mono font-medium whitespace-nowrap transition-all ${
                tab === t.key
                  ? "bg-white/10 text-white border border-white/15"
                  : "text-gray-500 hover:text-gray-300 border border-transparent"
              }`}>
              <Icon className="w-4 h-4" />
              {t.label}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        <motion.div key={tab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
          {tab === "rank" && <RankTab data={data} />}
          {tab === "bounty" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading bounty...</div> : <BountyTab data={subData} />)}
          {tab === "skilltree" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading...</div> : <SkillTreeTab data={subData} />)}
          {tab === "quests" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading...</div> : <QuestsTab data={subData} onCompleteStep={handleCompleteStep} />)}
          {tab === "bosses" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading...</div> : <BossesTab data={subData} />)}
          {tab === "dungeons" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading...</div> : <DungeonsTab data={subData} />)}
          {tab === "collections" && (subLoading ? <div className="text-center text-gray-500 py-10">Loading...</div> : <CollectionsTab data={subData} />)}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
