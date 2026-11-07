import { Link } from "react-router-dom";
import { Flame, Trophy, Target, CheckCircle2 } from "lucide-react";
import { Card } from "../../design-system/Card";
import type { PlacementRank } from "../../lib/placementRank";

type Props = {
  streak: number;
  rank: PlacementRank;
  readiness: number | null;
};

export function DashboardSupportPanel({ streak, rank, readiness }: Props) {
  return (
    <Card className="border border-slate-200 bg-white p-5 sm:p-6">
      <div className="flex items-center gap-2 mb-4">
        <Trophy size={18} className="text-amber-500" />
        <h3 className="font-bold">Progress support</h3>
      </div>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-orange-50 text-orange-600">
              <Flame size={18} />
            </div>
            <div>
              <p className="text-sm font-medium">Habit streak</p>
              <p className="text-xs text-slate-500">Consistency, not perfection</p>
            </div>
          </div>
          <span className="text-lg font-black">{streak}</span>
        </div>
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
              <Target size={18} />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium">Placement rank</p>
              <p className="text-xs text-slate-500 truncate">{rank.blurb}</p>
            </div>
          </div>
          <span className="text-sm font-black shrink-0">{rank.title}</span>
        </div>
        {readiness != null && (
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
                <CheckCircle2 size={18} />
              </div>
              <div>
                <p className="text-sm font-medium">Readiness</p>
                <p className="text-xs text-slate-500">Evidence-based</p>
              </div>
            </div>
            <span className="text-lg font-black">{Math.round(Number(readiness))}%</span>
          </div>
        )}
      </div>
      <div className="mt-5 grid grid-cols-2 gap-2">
        <Link to="/academy" className="rounded-xl border border-slate-200 px-3 py-2 text-center text-xs font-semibold">Academy</Link>
        <Link to="/practice" className="rounded-xl border border-slate-200 px-3 py-2 text-center text-xs font-semibold">Practice</Link>
        <Link to="/quiz" className="rounded-xl border border-slate-200 px-3 py-2 text-center text-xs font-semibold">Mock quiz</Link>
        <Link to="/target" className="rounded-xl border border-slate-200 px-3 py-2 text-center text-xs font-semibold">Targets</Link>
      </div>
    </Card>
  );
}
