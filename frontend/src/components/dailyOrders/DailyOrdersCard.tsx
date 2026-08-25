import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  CalendarClock,
  CheckCircle2,
  Circle,
  Hourglass,
  ScrollText,
} from "lucide-react";
import { Button } from "../../design-system/Button";
import { MentorAvatar } from "../../design-system";
import { dailyOrdersApi } from "../../services/api/dailyOrders";
import type { TodayOrders } from "../../services/api/dailyOrders";

/**
 * DailyOrdersCard — "First Mate Orders" on Home.
 * Deadline-driven daily checklist; deterministic per date, server-backed.
 */
export default function DailyOrdersCard() {
  const [data, setData] = useState<TodayOrders | null>(null);
  const [showSetup, setShowSetup] = useState(false);
  const [company, setCompany] = useState("");
  const [driveDate, setDriveDate] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      const d = await dailyOrdersApi.today();
      setData(d);
      if (!d.deadline.company) setShowSetup(true);
    } catch {
      // card is optional chrome — stay silent on failure
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function saveDeadline() {
    if (!company.trim() || !driveDate) return;
    setSaving(true);
    setError("");
    try {
      await dailyOrdersApi.setDeadline(company.trim(), driveDate);
      setShowSetup(false);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save the deadline");
    } finally {
      setSaving(false);
    }
  }

  async function toggleOrder(id: string, completed: boolean) {
    if (completed) return;
    try {
      const res = await dailyOrdersApi.complete(id);
      setData(prev =>
        prev
          ? {
              ...prev,
              orders: prev.orders.map(o =>
                o.id === id ? { ...o, completed: true } : o,
              ),
              progress: {
                ...prev.progress,
                done: prev.progress.done + (res.already_done ? 0 : 1),
                earned_points:
                  prev.progress.earned_points +
                  (prev.orders.find(o => o.id === id)?.points ?? 0),
                all_done:
                  prev.progress.done + (res.already_done ? 0 : 1) ===
                  prev.progress.total,
              },
            }
          : prev,
      );
    } catch {
      // ignore
    }
  }

  if (!data) return null;

  const dl = data.deadline;

  return (
    <section className="bounty-card p-5">
      <header className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <MentorAvatar size={40} mood="briefing" />
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-widest text-text">
              First Mate Orders
            </h2>
            <p className="text-xs text-text-muted">
              {data.progress.done}/{data.progress.total} done ·{" "}
              {data.progress.earned_points}/{data.progress.total_points} pts
            </p>
          </div>
        </div>
        <button
          onClick={() => setShowSetup(s => !s)}
          aria-label="Edit deadline"
          className="flex h-8 w-8 items-center justify-center rounded-lg border border-line text-text-muted hover:text-text"
        >
          <CalendarClock size={15} />
        </button>
      </header>

      {/* deadline strip */}
      {dl.company && dl.drive_date && (
        <p
          className={`mb-3 rounded-lg border px-3 py-2 text-xs font-semibold ${
            typeof dl.days_left === "number" && dl.days_left <= 3
              ? "border-coral/40 bg-red-50 text-coral"
              : "border-sky/30 bg-sky-50 text-ocean"
          }`}
        >
          {dl.days_left !== null && dl.days_left >= 0
            ? `${dl.days_left} day${dl.days_left === 1 ? "" : "s"} to ${dl.company}`
            : `${dl.company} drive date passed`}
        </p>
      )}

      {showSetup ? (
        <div className="space-y-2.5">
          <input
            value={company}
            onChange={e => setCompany(e.target.value)}
            placeholder="Drive company (e.g., TCS NQT)"
            maxLength={80}
            className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
          />
          <input
            type="date"
            value={driveDate}
            min={new Date().toISOString().slice(0, 10)}
            onChange={e => setDriveDate(e.target.value)}
            className="w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text outline-none focus:border-primary"
          />
          {error && (
            <p className="rounded-lg bg-red-50 px-2.5 py-1.5 text-xs text-coral">{error}</p>
          )}
          <Button size="sm" loading={saving} onClick={saveDeadline}>
            Set course
          </Button>
        </div>
      ) : (
        <>
          <ul className="space-y-2">
            {data.orders.map(o => (
              <li key={o.id}>
                <div
                  className={`flex items-start gap-2.5 rounded-lg border px-3 py-2 ${
                    o.completed
                      ? "border-primary/25 bg-mint/30"
                      : "border-line bg-canvas"
                  }`}
                >
                  <button
                    onClick={() => toggleOrder(o.id, o.completed)}
                    aria-label={o.completed ? `${o.title} completed` : `Mark ${o.title} complete`}
                    className="mt-0.5 shrink-0"
                  >
                    {o.completed ? (
                      <CheckCircle2 size={18} className="text-primary" />
                    ) : (
                      <Circle size={18} className="text-text-muted hover:text-primary" />
                    )}
                  </button>
                  <div className="min-w-0 flex-1">
                    <Link
                      to={o.link}
                      className={`block truncate text-sm font-semibold hover:underline ${
                        o.completed ? "text-text-muted line-through" : "text-text"
                      }`}
                    >
                      {o.title}
                    </Link>
                    <p className="truncate text-xs text-text-muted">{o.detail}</p>
                  </div>
                  <span className="shrink-0 text-xs font-bold text-reward">
                    +{o.points}
                  </span>
                </div>
              </li>
            ))}
          </ul>

          {data.progress.all_done && (
            <p className="mt-3 flex items-center gap-2 rounded-lg border border-reward/40 bg-reward/10 px-3 py-2 text-xs font-bold text-reward">
              <Hourglass size={14} /> All orders complete — the crew eats tonight.
            </p>
          )}

          {!dl.company && (
            <p className="mt-3 flex items-center gap-1.5 text-xs text-text-muted">
              <ScrollText size={13} /> No deadline set — orders still post daily.
            </p>
          )}
        </>
      )}
    </section>
  );
}
