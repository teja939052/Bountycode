import { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import gsap from "gsap";
import type { MapNode, MapState } from "../../services/api/map.ts";
import { analyticsApi } from "../../services/api/analytics.ts";
import { isMuted, setMuted, sfx, startAmbient, themeForWorld } from "../../utils/soundsea.ts";

interface Props {
  map: MapState | null;
  onAdvance: (node: MapNode) => void;
  onCampfire?: () => void;
  compact?: boolean;
}

const W = 340;
const H = 620;
const SAIL_MS = 650;

let sessionId: string | null = null;
function getSessionId(): string {
  if (!sessionId) {
    sessionId = typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `s-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
  }
  return sessionId;
}

function pirateThemeColor(worldId?: string | null): string {
  if (/pirate|cove|shore|treasure/i.test(worldId ?? "")) return "#b87333";
  return "#e8b64a";
}

function prefersReducedMotion(): boolean {
  return typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/** Winding sea-route through node positions (matches backend serpentine). */
function pathD(nodes: MapNode[]): string {
  if (nodes.length === 0) return "";
  if (nodes.length === 1) return `M${nodes[0].position.x},${nodes[0].position.y}`;
  let d = `M${nodes[0].position.x},${nodes[0].position.y}`;
  for (let i = 1; i < nodes.length; i++) {
    const p0 = nodes[i - 1].position;
    const p1 = nodes[i].position;
    const mx = (p0.x + p1.x) / 2;
    d += ` C${mx},${p0.y} ${mx},${p1.y} ${p1.x},${p1.y}`;
  }
  return d;
}

function Stars({ n }: { n: number }) {
  if (!n) return null;
  return (
    <motion.span
      key={n}
      initial={{ scale: 0.4, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 400, damping: 18 }}
      aria-label={`${n} stars`}
      className="ml-1 inline-block text-[11px] tracking-tight text-amber-300"
    >
      {"★".repeat(n)}{"☆".repeat(Math.max(0, 3 - n))}
    </motion.span>
  );
}

export default function VoyagePath({ map, onAdvance, onCampfire }: Props) {
  const allNodes = map?.nodes ?? [];
  const nodes = useMemo(() => allNodes.filter((n) => n.visible), [allNodes]);
  const foggedCount = map?.fogged_count ?? 0;
  const campfire = nodes.find((n) => n.kind === "srs_campfire") ?? null;
  const currentIdx = map?.character?.node_index ?? 0;
  const [sailing, setSailing] = useState(false);
  const [sailFrac, setSailFrac] = useState<number | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [burstAt, setBurstAt] = useState<{ x: number; y: number; k: number } | null>(null);
  const [muted, setMutedState] = useState(() => isMuted());
  const pathRef = useRef<SVGPathElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const [ship, setShip] = useState<{ x: number; y: number; a: number } | null>(null);
  const viewTracked = useRef(false);
  const sailTween = useRef<gsap.core.Tween | null>(null);

  const d = useMemo(() => pathD(nodes), [nodes]);
  const reducedMotion = useMemo(() => prefersReducedMotion(), []);

  // map_view instrumentation (once per mount; analytics never throws).
  useEffect(() => {
    if (!map || viewTracked.current) return;
    viewTracked.current = true;
    void analyticsApi.track("map_view", {
      session_id: getSessionId(),
      world_id: map.world?.id,
      node_index: map.character?.node_index,
      total: map.total,
      campfire_due: map.campfire?.due_count ?? 0,
    });
  }, [map]);

  // GSAP stagger reveal for island badges on first paint.
  useEffect(() => {
    if (reducedMotion || !svgRef.current || nodes.length === 0) return;
    const ctx = gsap.context(() => {
      gsap.from(svgRef.current!.querySelectorAll(".island-badge"), {
        scale: 0,
        opacity: 0,
        transformOrigin: "center",
        duration: 0.45,
        ease: "back.out(2)",
        stagger: { each: 0.06, from: "start" },
      });
    }, svgRef);
    return () => ctx.revert();
  }, [d, reducedMotion]); // eslint-disable-line react-hooks/exhaustive-deps

  // Campfire ember pulse (GSAP yoyo glow).
  useEffect(() => {
    if (reducedMotion || !campfire || !svgRef.current) return;
    const ctx = gsap.context(() => {
      gsap.to(svgRef.current!.querySelectorAll(".campfire-glow"), {
        opacity: 0.15,
        scale: 1.25,
        transformOrigin: "center",
        duration: 1.1,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1,
      });
    }, svgRef);
    return () => ctx.revert();
  }, [campfire?.node_id, reducedMotion]); // eslint-disable-line react-hooks/exhaustive-deps

  const fracFor = (idx: number) => (nodes.length <= 1 ? 0 : Math.min(1, Math.max(0, idx) / (nodes.length - 1)));

  const pointAt = (f: number) => {
    const el = pathRef.current;
    if (!el) {
      const n = nodes[Math.round(f * (nodes.length - 1))] ?? nodes[0];
      return n ? { x: n.position.x, y: n.position.y, a: 0 } : null;
    }
    try {
      const len = el.getTotalLength();
      const p = el.getPointAtLength(f * len);
      const p1 = el.getPointAtLength(Math.max(0, f * len - 2));
      const p2 = el.getPointAtLength(Math.min(len, f * len + 2));
      const a = (Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180) / Math.PI + 90;
      return { x: p.x, y: p.y, a };
    } catch {
      return null;
    }
  };

  // Place ship on current node. Geometry is in SVG user units (viewBox), so
  // it is invariant under responsive scaling — no ResizeObserver needed for
  // positioning; mobile Safari and Chrome resolve the same coordinates.
  useEffect(() => {
    if (sailFrac !== null) return;
    if (nodes.length === 0) return;
    const pt = pointAt(fracFor(currentIdx));
    if (pt) setShip(pt);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [d, nodes, currentIdx, sailFrac]);

  // Idle bob so the scene never feels static (skipped for reduced motion).
  const [bob, setBob] = useState(0);
  useEffect(() => {
    if (reducedMotion) return;
    let raf = 0;
    const t0 = performance.now();
    const loop = (t: number) => {
      setBob(Math.sin((t - t0) / 550) * 2.2);
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [reducedMotion]);

  // Kill any in-flight sail tween on unmount.
  useEffect(() => () => { sailTween.current?.kill(); }, []);

  const current = nodes[Math.min(currentIdx, Math.max(0, nodes.length - 1))];
  const bossAhead = useMemo(() => {
    if (!current) return null;
    const idx = nodes.indexOf(current);
    const boss = nodes.slice(idx + 1).find((n) => n.is_boss);
    if (!boss) return null;
    return { steps: nodes.indexOf(boss) - idx, title: boss.title };
  }, [nodes, current]);

  const xpPct = useMemo(() => {
    const s = map?.stats;
    if (!s) return 0;
    return Math.min(96, Math.max(6, (s.diamonds % 100) + 12));
  }, [map]);

  const repair = nodes.find((n) => n.kind === "repair" && n.visible) ?? null;
  const repairParent = repair?.branch_from
    ? nodes.find((n) => n.node_id === repair.branch_from) ?? null
    : null;

  const openRepair = () => {
    if (!repair || !repairParent) return;
    startAmbient(themeForWorld(map?.world?.id));
    void analyticsApi.track("map_repair_open", {
      session_id: getSessionId(),
      world_id: map?.world?.id,
      node_id: repair.node_id,
      branch_from: repair.branch_from,
    });
    sfx("pop");
    setToast(repair.title);
    window.setTimeout(() => setToast(null), 1600);
    // Merge-back is structural: the repair IS a guided re-attempt of the
    // parent through the canonical LevelPlayer flow. Clearing the parent
    // dissolves the branch on next fetch — no branch state exists anywhere.
    onAdvance(repairParent);
  };

  const worldTheme = (map?.world?.theme ?? {}) as { bgm?: string; color?: string };
  const bgm: "meadow" | "plains" | "embers" | "pirate" = (worldTheme.bgm as "meadow" | "plains" | "embers" | "pirate") ?? themeForWorld(map?.world?.id);
  const themeColor = worldTheme.color ?? pirateThemeColor(map?.world?.id);

  const toggleMute = () => {
    const next = !muted;
    setMuted(next);
    setMutedState(next);
    if (!next) {
      startAmbient(bgm);
      sfx("pop");
    }
  };

  const shakeBoss = (title: string) => {
    if (reducedMotion || !svgRef.current) return;
    const ctx = gsap.context(() => {
      gsap.fromTo(
        svgRef.current!.querySelectorAll(".boss-node"),
        { x: 0 },
        { x: 5, duration: 0.06, repeat: 5, yoyo: true, ease: "none", clearProps: "x" },
      );
    }, svgRef);
    window.setTimeout(() => ctx.revert(), 700);
    sfx("boss");
    setToast(`${title} stirs… come back stronger.`);
    window.setTimeout(() => setToast(null), 1600);
  };

  const sail = () => {
    if (!current || sailing) return;
    startAmbient(bgm);
    void analyticsApi.track("map_sail", {
      session_id: getSessionId(),
      world_id: map?.world?.id,
      node_id: current.node_id,
      node_index: currentIdx,
    });
    if (reducedMotion) {
      onAdvance(current);
      return;
    }
    setSailing(true);
    sfx("sail");
    const fromF = fracFor(currentIdx);
    // Sail toward the next visible node so the ship travels with weight
    // (GSAP back.out arrival) instead of teleporting.
    const toF = fracFor(Math.min(nodes.length - 1, currentIdx + 1));
    const proxy = { f: fromF };
    sailTween.current?.kill();
    sailTween.current = gsap.to(proxy, {
      f: toF,
      duration: SAIL_MS / 1000,
      ease: "back.out(1.4)",
      onUpdate: () => {
        setSailFrac(proxy.f);
        const pt = pointAt(proxy.f);
        if (pt) setShip(pt);
      },
      onComplete: () => {
        setBurstAt({ x: current.position.x, y: current.position.y, k: Date.now() });
        sfx("chime");
        setToast(`Set sail — ${current.title}`);
        window.setTimeout(() => {
          setSailFrac(null);
          setSailing(false);
          setToast(null);
          onAdvance(current);
        }, 350);
      },
    });
  };

  if (!map || nodes.length === 0) return null;

  return (
    <div>
      {/* Diamonds momentum bar (backend-owned numbers only) */}
      <div className="mb-3 flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3">
        <span aria-label="streak">🔥 <b>{map.stats?.streak ?? 0}</b></span>
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
          <motion.div
            className="h-full rounded-full bg-lime-500"
            animate={{ width: `${xpPct}%` }}
            transition={{ type: "spring", stiffness: 120, damping: 20 }}
          />
        </div>
        <span>🪙 <b>{map.stats?.coins ?? 0}</b></span>
        <span>Lv <b>{map.stats?.level ?? 1}</b></span>
        <button
          onClick={toggleMute}
          aria-label={muted ? "Unmute voyage sounds" : "Mute voyage sounds"}
          className="rounded-lg border border-white/10 bg-white/[0.06] px-2 py-1 text-sm"
        >
          {muted ? "🔇" : "🔊"}
        </button>
      </div>

      <h2 className="flex items-center gap-2 text-lg font-bold">
        <span aria-hidden className="inline-block h-4 w-1.5 rounded-full" style={{ background: themeColor }} />
        {map.world?.adventure_name ?? "Your voyage"}
      </h2>
      <p className="mb-2 text-xs opacity-60">Tap set sail — clear the pulsing node. Character walks on mastery, not clicks.</p>

      {bossAhead && (
        <div className="mb-2 rounded-xl border border-amber-300/30 bg-amber-300/10 px-3 py-2 text-xs font-semibold text-amber-200">
          🏴‍☠️ {bossAhead.title} awaits {bossAhead.steps === 1 ? "at the next island" : `${bossAhead.steps} islands ahead`} — fog promises, not just hides.
        </div>
      )}

      {campfire && (
        <button
          onClick={() => { sfx("pop"); onCampfire?.(); }}
          className="mb-2 flex w-full items-center gap-2 rounded-xl border border-orange-300/40 bg-orange-400/10 px-3 py-2 text-left text-xs font-semibold text-orange-200"
        >
          <span aria-hidden>🔥</span>
          Campfire Rest — {campfire.due_count ?? map.campfire?.due_count ?? 0} review{((campfire.due_count ?? 0) === 1) ? "" : "s"} due before the guardian. Rest, don&apos;t grind.
        </button>
      )}

      {repair && repairParent && (
        <button
          onClick={openRepair}
          className="mb-2 flex w-full items-center gap-2 rounded-xl border border-teal-300/40 bg-teal-400/10 px-3 py-2 text-left text-xs font-semibold text-teal-200"
        >
          <span aria-hidden>🛠️</span>
          {repair.title} — a short detour off {repairParent.title}, then straight back. Struggle is data.
        </button>
      )}

      <div
        className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-b from-emerald-900 via-[#082e21] to-[#041a12]"
        style={{ boxShadow: `inset 0 0 120px ${themeColor}22` }}
      >
        <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} className="block h-auto w-full" role="img" aria-label="Adventure voyage path">
          <path id="voyagePath" ref={pathRef} d={d} stroke="#e8b64a" strokeWidth={2.5}
            strokeDasharray="1 11" strokeLinecap="round" fill="none" opacity={0.85} />
          {repair && repairParent && (
            <path
              d={`M${repairParent.position.x},${repairParent.position.y} Q${(repairParent.position.x + repair.position.x) / 2 + 24},${(repairParent.position.y + repair.position.y) / 2 - 18} ${repair.position.x},${repair.position.y}`}
              stroke="#5eead4"
              strokeWidth={2}
              strokeDasharray="5 5"
              fill="none"
              opacity={0.8}
            />
          )}
          {nodes.map((n, i) => {
            const done = n.status === "completed";
            const cur = i === Math.min(currentIdx, nodes.length - 1);
            const isCamp = n.kind === "srs_campfire";
            const isRepair = n.kind === "repair";
            const fill = isRepair ? "#14b8a6" : isCamp ? "#f97316" : done ? "#e8b64a" : cur ? "#58cc02" : "rgba(255,253,247,0.12)";
            const stroke = isRepair ? "#5eead4" : isCamp ? "#fdba74" : done ? "#f6d98a" : cur ? "#89e219" : "rgba(255,253,247,0.25)";
            return (
              <g key={n.node_id} className={`island-badge${n.is_boss ? " boss-node" : ""}`} transform={`translate(${n.position.x},${n.position.y})`}>
                {cur && !isCamp && (
                  <circle r={20} fill="rgba(88,204,2,0.35)">
                    <animate attributeName="r" values="18;30" dur="1.8s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.55;0" dur="1.8s" repeatCount="indefinite" />
                  </circle>
                )}
                {isCamp && <circle className="campfire-glow" r={22} fill="rgba(249,115,22,0.35)" />}
                <circle r={isCamp ? 17 : 15} fill={fill} stroke={stroke} strokeWidth={3} opacity={n.fogged ? 0.35 : 1} />
                {isRepair ? (
                  <text y={6} textAnchor="middle" fontSize={15}>🛠️</text>
                ) : isCamp ? (
                  <text y={6} textAnchor="middle" fontSize={16}>🔥</text>
                ) : done ? (
                  <path d="M-5,0 L-1.5,4 L5,-4" stroke="#241a04" strokeWidth={2.4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
                ) : cur ? (
                  <circle r={3.5} fill="#0c1f18" />
                ) : n.is_boss ? (
                  <text y={5} textAnchor="middle" fontSize={13}>🏴‍☠️</text>
                ) : (
                  <g opacity={0.8}>
                    <rect x={-4} y={-1.5} width={8} height={6} rx={1} fill="rgba(255,253,247,0.55)" />
                  </g>
                )}
                {n.fogged && <circle r={15} fill="rgba(4,26,18,0.45)" />}
                {n.recovered && (
                  <circle r={18.5} fill="none" stroke="#7dd3fc" strokeWidth={1.5} strokeDasharray="3 3" opacity={0.9}>
                    <title>Recovered after a tough fight</title>
                  </circle>
                )}
                {/* Thumb-sized tap targets on live nodes (visuals stay small). */}
                {cur && !isCamp && (
                  <circle
                    r={26}
                    fill="transparent"
                    style={{ cursor: "pointer" }}
                    onClick={sail}
                    aria-label={`Sail to ${n.title}`}
                  />
                )}
                {isCamp && (
                  <circle
                    r={28}
                    fill="transparent"
                    style={{ cursor: "pointer" }}
                    onClick={() => { sfx("pop"); onCampfire?.(); }}
                    aria-label={`Rest at campfire, ${n.due_count ?? 0} reviews due`}
                  />
                )}
                {isRepair && (
                  <circle
                    r={28}
                    fill="transparent"
                    style={{ cursor: "pointer" }}
                    onClick={openRepair}
                    aria-label={`${n.title} — guided re-attempt, merges back`}
                  />
                )}
                {n.is_boss && !done && (
                  <circle
                    r={26}
                    fill="transparent"
                    style={{ cursor: "pointer" }}
                    onClick={() => shakeBoss(n.title)}
                    aria-label={`${n.title} (locked until path cleared)`}
                  />
                )}
              </g>
            );
          })}
          {burstAt && (
            <g transform={`translate(${burstAt.x},${burstAt.y})`}>
              {Array.from({ length: 14 }).map((_, i) => (
                <motion.circle key={`${burstAt.k}-${i}`} r={3} fill={i % 2 ? "#e8b64a" : "#58cc02"}
                  initial={{ x: 0, y: 0, opacity: 1 }}
                  animate={{ x: Math.cos((i / 14) * Math.PI * 2) * 46, y: Math.sin((i / 14) * Math.PI * 2) * 46 - 20, opacity: 0 }}
                  transition={{ duration: 0.7, ease: "easeOut" }} />
              ))}
            </g>
          )}
          {ship && (
            <g transform={`translate(${ship.x},${ship.y + bob}) rotate(${ship.a})`}>
              <ellipse cx={0} cy={13} rx={17} ry={4} fill="rgba(0,0,0,0.25)" />
              <path d="M-14,4 L14,4 L10,13 L-10,13 Z" fill="#caa26a" />
              <rect x={-1.4} y={-22} width={2.8} height={26} fill="#7a5230" />
              <path d="M1.4,-22 L18,-13 L1.4,-6 Z" fill="#fffdf7" />
              <path d="M1.4,-22 L1.4,-26 L11,-24 Z" fill="#ff4b4b" />
            </g>
          )}
        </svg>

        <AnimatePresence>
          {toast && (
            <motion.div initial={{ y: -48, opacity: 0 }} animate={{ y: 12, opacity: 1 }} exit={{ y: -48, opacity: 0 }}
              className="absolute left-1/2 top-2 -translate-x-1/2 whitespace-nowrap rounded-full bg-amber-300 px-4 py-2 text-sm font-bold text-amber-950">
              ⛵ {toast}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Readable legend — accessibility + real node names, fog-aware */}
      <div className="mt-3 flex flex-col gap-2">
        {nodes.slice(0, 6).map((n) => (
          <div key={n.node_id}
            className={`flex items-center gap-3 rounded-xl border px-3 py-2 text-sm ${n.is_current ? "border-lime-500/40 bg-lime-500/10" : n.kind === "srs_campfire" ? "border-orange-300/40 bg-orange-400/10" : "border-white/10 bg-white/[0.04]"}`}>
            <span className={`h-2.5 w-2.5 rounded-full ${n.status === "completed" ? "bg-amber-300" : n.is_current ? "bg-lime-500" : n.kind === "srs_campfire" ? "bg-orange-400" : n.kind === "repair" ? "bg-teal-300" : "bg-white/25"}`} />
            <div>
              <span className="font-semibold">{n.kind === "srs_campfire" ? "🔥 " : n.kind === "repair" ? "🛠️ " : ""}{n.title}</span>
              <Stars n={n.stars} />
              {n.recovered && <span className="ml-1 text-[11px] font-semibold text-sky-300">· fought back</span>}
              <div className="text-xs opacity-50">
                {n.kind === "srs_campfire"
                  ? `rest stop · ${n.due_count ?? 0} due`
                  : n.kind === "repair"
                    ? `detour · merges back · ${n.status}`
                    : n.is_boss ? "Boss Island" : n.kind.replace(/_/g, " ")} · {n.status}
                {n.attempts > 1 ? ` · ${n.attempts} attempts` : ""}
                {n.hints_used > 0 ? ` · ${n.hints_used} hint${n.hints_used === 1 ? "" : "s"}` : ""}
              </div>
            </div>
          </div>
        ))}
        {repair && !nodes.slice(0, 6).some((n) => n.node_id === repair.node_id) && (
          <button
            onClick={openRepair}
            className="flex items-center gap-3 rounded-xl border border-teal-300/40 bg-teal-400/10 px-3 py-2 text-left text-sm"
          >
            <span className="h-2.5 w-2.5 rounded-full bg-teal-300" />
            <div>
              <span className="font-semibold">🛠️ {repair.title}</span>
              <div className="text-xs opacity-50">detour · merges back · unlocked</div>
            </div>
          </button>
        )}
        {foggedCount > 0 && (
          <div className="rounded-xl border border-dashed border-white/15 px-3 py-2 text-center text-xs opacity-50">
            🌫️ {foggedCount} more node{foggedCount === 1 ? "" : "s"} shrouded — clear the path to reveal them.
          </div>
        )}
        {foggedCount === 0 && nodes.length > 0 && (
          <div className="rounded-xl border border-white/10 px-3 py-2 text-center text-xs opacity-50">
            🗺️ Charted waters end here — new regions unlock as verified content ships.
          </div>
        )}
      </div>

      <button onClick={sail} disabled={sailing || !current}
        className="mt-4 min-h-[52px] w-full rounded-xl bg-lime-500 py-3.5 font-bold text-emerald-950 shadow-[0_4px_0_#3f9401] active:translate-y-[3px] disabled:opacity-60">
        {sailing ? "Sailing…" : current ? `⛵ Set sail — ${current.title}` : "Voyage complete"}
      </button>
    </div>
  );
}
