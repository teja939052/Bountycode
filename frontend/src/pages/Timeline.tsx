import { useState, useEffect, useCallback, useMemo } from "react";
import { motion } from "framer-motion";
import { timelineApi } from "../services/api/timeline.ts";

const EVENT_ICONS = {
  first_compile: "⚡",
  problem_solved: "🧩",
  guild_join: "🛡️",
  battle_win: "⚔️",
  dungeon_clear: "🏰",
  interview: "🎙️",
  offer: "💼",
  level_up: "🚀",
};

const EVENT_LABELS = {
  first_compile: "First Compile",
  problem_solved: "Problem Solved",
  guild_join: "Guild Joined",
  battle_win: "Battle Won",
  dungeon_clear: "Dungeon Cleared",
  interview: "Interview",
  offer: "Offer",
  level_up: "Level Up",
};

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const GRAPH_DAYS = 180;

function toDateString(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function cellClass(count) {
  if (count >= 6) return "bg-emerald-400";
  if (count >= 3) return "bg-emerald-600";
  if (count >= 1) return "bg-emerald-800";
  return "bg-slate-800";
}

function ContributionGraph({ activity }) {
  const { weeks, monthLabels } = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const start = new Date(today);
    start.setDate(start.getDate() - (GRAPH_DAYS - 1));

    const gridStart = new Date(start);
    gridStart.setDate(gridStart.getDate() - ((gridStart.getDay() + 6) % 7));

    const weeks = [];
    const monthLabels = [];
    let prevMonth = -1;
    let cursor = new Date(gridStart);
    while (cursor <= today) {
      const week = [];
      const weekFirst = new Date(cursor);
      for (let i = 0; i < 7; i++) {
        const dateKey = toDateString(cursor);
        week.push({
          key: dateKey,
          dateKey,
          count: activity[dateKey] || 0,
          isToday: dateKey === toDateString(today),
        });
        cursor.setDate(cursor.getDate() + 1);
      }
      const month = weekFirst.getMonth();
      if (month !== prevMonth) {
        monthLabels.push({ col: weeks.length, month });
        prevMonth = month;
      }
      weeks.push(week);
    }
    return { weeks, monthLabels };
  }, [activity]);

  const cells = weeks.flat();
  const cellSize = 12;
  const gap = 3;

  return (
    <div className="flex gap-2 overflow-x-auto pb-1">
      <div
        className="grid shrink-0"
        style={{ gridTemplateRows: `repeat(7, ${cellSize}px)`, gap: `${gap}px`, fontSize: "10px" }}
      >
        <div />
        <div className="flex items-center text-slate-500">Mon</div>
        <div />
        <div className="flex items-center text-slate-500">Wed</div>
        <div />
        <div className="flex items-center text-slate-500">Fri</div>
        <div />
      </div>
      <div className="flex flex-col">
        <div className="relative h-4 mb-1">
          {monthLabels.map(({ col, month }) => (
            <span
              key={`${col}-${month}`}
              className="absolute text-[10px] text-slate-400"
              style={{ left: col * (cellSize + gap) }}
            >
              {MONTHS[month]}
            </span>
          ))}
        </div>
        <div
          className="grid"
          style={{
            gridTemplateRows: `repeat(7, ${cellSize}px)`,
            gridAutoColumns: `${cellSize}px`,
            gridAutoFlow: "column",
            gap: `${gap}px`,
          }}
        >
          {cells.map((cell) => (
            <div
              key={cell.key}
              title={`${cell.dateKey}: ${cell.count} activity${cell.count === 1 ? "" : "s"}`}
              className={`w-full h-full rounded-[3px] ${cellClass(cell.count)} ${cell.isToday ? "ring-1 ring-slate-400" : ""}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

function formatDateStamp(iso) {
  const d = new Date(iso);
  const date = d.getDate();
  const suffix = ["th", "st", "nd", "rd"][(date % 100 > 10 && date % 100 < 14) ? 0 : ((date % 10) || 4) > 3 ? 0 : (date % 10) || 4];
  return `${date}${suffix} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
}

export default function Timeline() {
  const [timeline, setTimeline] = useState([]);
  const [activity, setActivity] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [tl, act] = await Promise.all([
        timelineApi.get(),
        timelineApi.activity(GRAPH_DAYS),
      ]);
      setTimeline(tl.timeline || []);
      setActivity(act.activity || {});
    } catch (e) {
      setError(e.message || "Failed to load timeline");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const stats = useMemo(() => {
    const days = new Set();
    let problems = 0;
    let offers = 0;
    let interviews = 0;
    for (const ev of timeline) {
      if (ev.created_at) days.add(toDateString(new Date(ev.created_at)));
      if (ev.event_type === "problem_solved") problems += 1;
      else if (ev.event_type === "offer") offers += 1;
      else if (ev.event_type === "interview") interviews += 1;
    }
    return { daysActive: days.size, problems, offers, interviews };
  }, [timeline]);

  const groups = useMemo(() => {
    const map = {};
    for (const ev of timeline) {
      if (!ev.created_at) continue;
      const d = new Date(ev.created_at);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
      if (!map[key]) map[key] = [];
      map[key].push(ev);
    }
    return Object.entries(map as Record<string, any[]>)
      .sort((a, b) => b[0].localeCompare(a[0]))
      .map(([month, events]: [string, any[]]) => ({
        month,
        events: [...events].sort((a: any, b: any) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()),
      }));
  }, [timeline]);

  const totalEvents = timeline.length;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <div className="max-w-4xl mx-auto px-4 py-10">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <p className="text-indigo-400 text-sm font-semibold tracking-widest uppercase">Placement Timeline</p>
          <h1 className="text-3xl md:text-4xl font-bold mt-2">This is your journey</h1>
          <p className="text-slate-400 mt-2 max-w-2xl">
            Every compile, solve, battle and offer — from Day 1 to your placement. Milestones
            are recorded automatically as you practice.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
          {[
            { label: "Days Active", value: stats.daysActive, icon: "📅" },
            { label: "Problems Solved", value: stats.problems, icon: "🧩" },
            { label: "Interviews", value: stats.interviews, icon: "🎙️" },
            { label: "Offers", value: stats.offers, icon: "💼" },
          ].map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.06 }}
              className="bg-slate-800/70 rounded-xl border border-slate-700/50 p-4"
            >
              <div className="text-2xl">{s.icon}</div>
              <div className="text-2xl font-bold mt-1">{s.value}</div>
              <div className="text-xs text-slate-400 mt-0.5">{s.label}</div>
            </motion.div>
          ))}
        </div>

        <div className="bg-slate-800/70 rounded-xl border border-slate-700/50 p-5 mt-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-lg">Contribution Graph</h2>
            <span className="text-xs text-slate-400">{totalEvents} milestones · last {GRAPH_DAYS} days</span>
          </div>
          {loading ? (
            <div className="h-40 flex items-center justify-center text-slate-500">Loading graph...</div>
          ) : (
            <ContributionGraph activity={activity} />
          )}
          <div className="flex items-center gap-1.5 mt-3 text-xs text-slate-400">
            <span>Less</span>
            <span className={`w-3 h-3 rounded-[3px] ${cellClass(0)}`} />
            <span className={`w-3 h-3 rounded-[3px] ${cellClass(1)}`} />
            <span className={`w-3 h-3 rounded-[3px] ${cellClass(3)}`} />
            <span className={`w-3 h-3 rounded-[3px] ${cellClass(6)}`} />
            <span>More</span>
          </div>
        </div>

        <div className="bg-slate-800/70 rounded-xl border border-slate-700/50 p-5 mt-6">
          <h2 className="font-semibold text-lg mb-4">Milestones</h2>
          {loading ? (
            <div className="h-32 flex items-center justify-center text-slate-500">Loading milestones...</div>
          ) : error ? (
            <div className="text-center py-8">
              <p className="text-red-400">{error}</p>
              <button
                onClick={load}
                className="mt-3 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm transition-colors"
              >
                Retry
              </button>
            </div>
          ) : totalEvents === 0 ? (
            <div className="text-center py-10">
              <div className="text-4xl mb-3">🚀</div>
              <p className="text-slate-300 font-medium">No milestones yet</p>
              <p className="text-slate-500 text-sm mt-1">Solve your first problem, compile your first program or record an offer to start your journey.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {groups.map((group) => (
                <div key={group.month}>
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="text-sm font-semibold text-indigo-300">
                      {MONTH_NAMES[Number(group.month.split("-")[1]) - 1]} {group.month.split("-")[0]}
                    </h3>
                    <div className="h-px flex-1 bg-slate-700/60" />
                  </div>
                  <div className="relative space-y-3 before:absolute before:left-[15px] before:top-1 before:bottom-1 before:w-px before:bg-slate-700/60">
                    {group.events.map((ev) => (
                      <div key={ev.id} className="relative flex items-start gap-3 pl-1">
                        <div className="w-8 h-8 shrink-0 rounded-full bg-slate-700/80 border border-slate-600/60 flex items-center justify-center text-sm z-10">
                          {EVENT_ICONS[ev.event_type] || "⭐"}
                        </div>
                        <div className="min-w-0 pt-0.5">
                          <p className="font-medium text-sm text-slate-100">{ev.title}</p>
                          <p className="text-xs text-slate-500 mt-0.5">
                            {EVENT_LABELS[ev.event_type] || ev.event_type} · {formatDateStamp(ev.created_at)}
                          </p>
                          {ev.meta && ev.meta.company && (
                            <span className="inline-block mt-1 px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 text-[11px]">
                              {ev.meta.company}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
