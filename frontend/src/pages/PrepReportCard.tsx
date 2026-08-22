import { useState, useEffect, useCallback } from "react";
import { reportCardApi } from "../services/api/reportCard.ts";
import {
  FileText, Download, Loader2, Award, Zap, Flame, Trophy,
  MessageSquare, Share2, GitBranch, Briefcase, Star,
} from "lucide-react";

const SECTION_COLORS = [
  "from-brand-sky to-brand-lavender",
  "from-brand-coral to-amber-400",
  "from-emerald-400 to-brand-sky",
  "from-violet-400 to-brand-lavender",
  "from-amber-400 to-orange-400",
  "from-pink-400 to-brand-coral",
];

const GRADE_COLORS = {
  Excellent: "bg-green-100 text-green-700",
  Strong: "bg-emerald-100 text-emerald-700",
  Good: "bg-sky-100 text-sky-700",
  Developing: "bg-amber-100 text-amber-700",
  "Needs Work": "bg-orange-100 text-orange-700",
  "Just Started": "bg-gray-100 text-gray-700",
};

export default function PrepReportCard() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await reportCardApi.get();
      setReport(res);
    } catch (e) {
      setError(e.message || "Could not load report card");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const download = (fmt) => {
    window.open(reportCardApi.exportUrl(fmt), "_blank");
  };

  const sectionEntries = report ? Object.entries(report.sections || {}) : [];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
            <FileText className="text-brand-coral" size={32} />
            Prep Report Card
          </h1>
          <p className="text-text-light mt-1">Your placement readiness, at a glance — exportable anytime</p>
        </div>
        {report && (
          <div className="flex gap-2">
            <button onClick={() => download("docx")} className="px-4 py-2 rounded-xl bg-brand-sky text-white text-sm font-semibold flex items-center gap-2">
              <Download size={15} /> DOCX
            </button>
            <button onClick={() => download("pdf")} className="px-4 py-2 rounded-xl bg-brand-coral text-white text-sm font-semibold flex items-center gap-2">
              <Download size={15} /> PDF
            </button>
            <button onClick={() => download("txt")} className="px-4 py-2 rounded-xl border border-white/60 bg-white/80 text-text-primary text-sm font-semibold flex items-center gap-2">
              <FileText size={15} /> TXT
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      {loading ? (
        <div className="flex justify-center py-16"><Loader2 size={32} className="animate-spin text-brand-sky" /></div>
      ) : !report ? null : (
        <div className="space-y-6">
          {/* Overall */}
          <div className="p-6 rounded-2xl border border-white/60 bg-gradient-to-br from-[#101228] to-[#1d2150] text-white">
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-2xl font-display font-extrabold">{report.user.name}</div>
                <div className="text-xs text-white/60">{report.user.email} · {report.user.plan} plan</div>
              </div>
              <div className="text-center">
                <div className="text-5xl font-extrabold">{report.overall_score}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-white/60">Readiness / 100</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Award size={18} className="text-amber-300" />
              <span className={`px-2.5 py-1 rounded-lg text-sm font-bold ${GRADE_COLORS[report.grade] || "bg-white/20 text-white"}`}>
                {report.grade}
              </span>
              <span className="text-xs text-white/60 ml-1">generated {new Date(report.generated_at).toLocaleString()}</span>
            </div>
          </div>

          {/* Sections */}
          <div>
            <h2 className="text-lg font-bold text-text-primary mb-3">Sections</h2>
            <div className="space-y-3">
              {sectionEntries.map(([label, part], i) => (
                <div key={label} className="p-4 rounded-2xl border border-white/60 bg-white/80">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-text-primary">{label}</span>
                    <span className="text-sm text-text-light">{part.count} attempt{part.count === 1 ? "" : "s"} · <span className="font-bold text-text-primary">{part.score}/100</span></span>
                  </div>
                  <div className="h-3 rounded-full bg-white/60 border border-white/70 overflow-hidden">
                    <div className={`h-full rounded-full bg-gradient-to-r ${SECTION_COLORS[i % SECTION_COLORS.length]}`} style={{ width: `${part.score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Activity grid */}
          <div>
            <h2 className="text-lg font-bold text-text-primary mb-3">Activity</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Zap size={20} className="mx-auto text-brand-sky mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.solved_problems}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Problems Solved</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Flame size={20} className="mx-auto text-brand-coral mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.streak}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Day Streak</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Trophy size={20} className="mx-auto text-amber-400 mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">
                  {report.activity.battles.total}
                </div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">
                  Battles · {report.activity.battles.wins}W
                </div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Star size={20} className="mx-auto text-brand-lavender mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.level}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Level · {report.activity.xp} XP</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <MessageSquare size={20} className="mx-auto text-emerald-500 mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.reviews_given}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Peer Reviews</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Share2 size={20} className="mx-auto text-sky-500 mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.reviews_received}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Reviews Received</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <GitBranch size={20} className="mx-auto text-violet-500 mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">{report.activity.gd_ratings}</div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">GD Ratings</div>
              </div>
              <div className="p-4 rounded-2xl border border-white/60 bg-white/80 text-center">
                <Briefcase size={20} className="mx-auto text-indigo-500 mb-1" />
                <div className="text-2xl font-extrabold text-text-primary">
                  {report.activity.offers}<span className="text-sm text-text-light">/{report.activity.drives}</span>
                </div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-text-light">Offers / Drives</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
