import { useMemo } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, Compass, MapPin, Swords } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";
import { IslandNode, PathConnector } from "../design-system/JourneyMap";
import { MasteryBar } from "../design-system/Progress";
import { MentorAvatar } from "../design-system/Mentor";
import { getWorldProgress } from "../engine/progressStore";
import type { Mission } from "../engine/missionTypes";
import { WORLD_1 } from "../data/missions/world1";

/**
 * JourneyMapPage — the Bounty Map.
 * Vertical island chain: each island is a mission; boss node closes the world.
 * State comes from real persisted progress (progressStore), never invented.
 */

export default function JourneyMapPage() {
  // Single-world build: canonicalize to the world's real id regardless of URL,
  // so data lookups and progress keys can never split across aliases.
  const worldId = WORLD_1.id;
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const missions: Mission[] = useMemo(() => {
    return WORLD_1.missions || [];
  }, []);

  const progress = useMemo(() => getWorldProgress(worldId), [worldId]);

  const completedCount = missions.filter((m) => progress[m.id]).length;
  const worldMastery = missions.length
    ? Math.round(
        missions.reduce((sum, m) => sum + (progress[m.id]?.mastery ?? 0), 0) / missions.length
      )
    : 0;

  const nextMission = missions.find((m) => !progress[m.id]) || null;
  const allDone = completedCount === missions.length && missions.length > 0;

  // Deterministic mentor line by state
  const mentorLine = allDone
    ? "World cleared. The next horizon awaits — but rest, sailor. You've earned it."
    : nextMission
      ? `Your heading: "${nextMission.title}". Fair winds — I'll be watching from the crow's nest.`
      : "Chart your first island to begin the voyage.";

  return (
    <PageShell theme="adventure">
      <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
        {/* Header */}
        <div className="mb-8 flex items-center gap-3">
          <button
            onClick={() => navigate("/home")}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-border bg-surface text-text-muted shadow-card transition-colors hover:text-text"
            aria-label="Back to home"
          >
            <ArrowLeft size={16} />
          </button>
          <div className="min-w-0">
            <span className="adventure-label">Bounty Map</span>
            <h1 className="font-display mt-1 truncate text-2xl font-extrabold text-text">
              World 1 · Origin
            </h1>
          </div>
          <div className="ml-auto hidden shrink-0 rounded-xl border border-border bg-surface px-4 py-2 text-center shadow-card sm:block">
            <p className="font-display text-lg font-extrabold leading-none text-text">{completedCount}/{missions.length}</p>
            <p className="text-[10px] font-bold uppercase tracking-wider text-text-muted">islands</p>
          </div>
        </div>

        {/* World mastery summary */}
        <Card tone="bounty" pad="sm" className="mb-8">
          <div className="parchment-bg flex items-center gap-4 rounded-xl p-4">
            <Compass size={28} className="shrink-0 text-wood" />
            <div className="min-w-0 flex-1">
              <MasteryBar value={worldMastery} label="World mastery" tone="gold" />
            </div>
          </div>
        </Card>

        {/* Captain Byte guidance */}
        <div className="mb-10 flex items-center gap-3">
          <MentorAvatar size={48} mood={allDone ? "celebrating" : "briefing"} />
          <p className="rounded-xl border border-border bg-surface px-4 py-2.5 text-sm leading-snug text-text-muted shadow-card">
            <span className="font-bold text-text">Captain Byte:</span> {mentorLine}
          </p>
        </div>

        {/* The map — vertical island chain */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <ol className="relative mx-auto flex max-w-md flex-col items-center">
            {missions.map((m, i) => {
              const entry = progress[m.id];
              const isNext = nextMission?.id === m.id;

              return (
                <li key={m.id} className="flex w-full flex-col items-center">
                  <IslandNode
                    state={
                      entry
                        ? entry.mastery >= m.masteryThreshold
                          ? "completed"
                          : "in_progress"
                        : isNext
                          ? "available"
                          : "locked"
                    }
                    title={`${m.order}. ${m.title}`}
                    mastery={entry?.mastery ?? 0}
                    onClick={() => navigate(`/mission/${worldId}/${m.id}`)}
                  />

                  {/* Current destination marker */}
                  {isNext && (
                    <span className="-mt-14 mb-11 translate-x-24 rounded-full bg-ocean px-2.5 py-0.5 text-[10px] font-extrabold uppercase tracking-wider text-white shadow-card">
                      You are here
                    </span>
                  )}

                  {/* Connector to next island */}
                  {i < missions.length - 1 && (
                    <PathConnector progress={entry ? 100 : 0} />
                  )}
                </li>
              );
            })}

            {/* Boss node closes the chain */}
            <li className="mt-2 flex flex-col items-center">
              <IslandNode
                state={allDone ? "boss_cleared" : "boss"}
                title="World Boss"
                isBoss
                icon={<Swords size={26} className="text-coral" />}
                onClick={() => navigate(`/readiness`)}
              />
            </li>
          </ol>
        </motion.div>

        {/* Start/continue CTA */}
        <div className="mx-auto mt-12 max-w-sm">
          {allDone ? (
            <Link to="/learn" className="block">
              <Button variant="gold" size="xl" fullWidth>
                Sail to the Learning Isles
              </Button>
            </Link>
          ) : nextMission ? (
            <Button
              variant="primary"
              size="xl"
              fullWidth
              onClick={() => navigate(`/mission/${worldId}/${nextMission.id}`)}
            >
              {completedCount === 0 ? "Begin the Voyage" : "Continue Voyage"}
            </Button>
          ) : null}
          <p className="mt-3 flex items-center justify-center gap-1.5 text-xs text-text-muted">
            <MapPin size={12} />
            Progress is saved on this device
          </p>
        </div>
      </div>
    </PageShell>
  );
}
