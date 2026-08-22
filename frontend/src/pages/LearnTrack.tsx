import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  Code2,
  GraduationCap,
  Hammer,
  Sparkles,
} from "lucide-react";
import { useCurriculumIndex } from "../hooks/useLesson";
import Spinner from "../components/ui/Spinner";

const PROGRESS_KEY = "pp_curriculum_progress_v1";

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
  } catch {
    return {};
  }
}

export default function LearnTrack() {
  const { trackId } = useParams();
  const { index, loading } = useCurriculumIndex();
  const progress = readProgress();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base">
        <Spinner />
      </div>
    );
  }

  const track = index?.tracks?.find((t) => t.id === trackId);

  if (!track) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-surface-base px-6 text-center">
        <p className="text-lg font-semibold text-text-primary">Track not found</p>
        <Link to="/curriculum" className="text-sm font-semibold text-nature-blossom">
          Back to all tracks
        </Link>
      </div>
    );
  }

  const allLessons = track.sections.flatMap((s) => s.lessons);
  const completedCount = allLessons.filter((l) => progress[l.id]).length;
  const pct = allLessons.length ? Math.round((completedCount / allLessons.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="sticky top-0 z-20 border-b border-[#E5E7EB] bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-[900px] items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-3">
            <Link
              to="/curriculum"
              className="flex h-9 w-9 items-center justify-center rounded-full border border-[#E5E7EB] text-text-muted hover:bg-[#F3F4F6]"
              aria-label="Back to curriculum"
            >
              <ArrowLeft size={16} />
            </Link>
            <h1 className="font-display text-base font-bold">{track.title}</h1>
          </div>
          <span className="rounded-full border border-[#E5E7EB] bg-[#F9FAFB] px-3 py-1 text-xs font-semibold text-text-muted">
            {completedCount}/{allLessons.length} · {pct}%
          </span>
        </div>
        <div className="h-1 bg-[#EEF5E7]">
          <div className="h-1 bg-nature-leaf transition-all" style={{ width: `${pct}%` }} />
        </div>
      </div>

      <div className="mx-auto max-w-[900px] px-4 py-8">
        <p className="mb-8 text-sm leading-relaxed text-text-muted">{track.tagline}</p>

        <div className="space-y-10">
          {track.sections.map((section) => {
            const done = section.lessons.filter((l) => progress[l.id]).length;
            return (
              <section key={section.id}>
                <div className="mb-4 flex items-center justify-between">
                  <h2 className="flex items-center gap-2 font-display text-lg font-bold text-text-primary">
                    <GraduationCap size={18} className="text-nature-blossom" />
                    {section.title}
                  </h2>
                  <span className="text-xs font-semibold text-text-muted">
                    {done}/{section.lessons.length}
                  </span>
                </div>

                <div className="overflow-hidden rounded-3xl border border-[#E5E7EB] bg-white shadow-[0_1px_2px_rgba(31,41,55,0.04)]">
                  {section.lessons.map((lesson, idx) => {
                    const isDone = !!progress[lesson.id];
                    const firstIncomplete = section.lessons.findIndex(
                      (l) => !progress[l.id]
                    );
                    const locked = !isDone && firstIncomplete !== idx;
                    return (
                      <div
                        key={lesson.id}
                        className={`flex items-center gap-4 border-b border-[#F3F4F6] px-5 py-4 last:border-b-0 ${
                          locked ? "" : "transition-colors hover:bg-surface-base"
                        }`}
                      >
                        {isDone ? (
                          <CheckCircle2 size={20} className="shrink-0 text-nature-blossom" />
                        ) : locked ? (
                          <Circle size={20} className="shrink-0 text-[#D1D5DB]" />
                        ) : (
                          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#EEF5E7] text-[11px] font-bold text-nature-blossom">
                            {idx + 1}
                          </span>
                        )}

                        {locked ? (
                          <div className="min-w-0 flex-1">
                            <p className="truncate text-sm font-semibold text-text-muted">
                              {lesson.title}
                            </p>
                            <p className="flex items-center gap-2 text-xs text-[#B8BFC9]">
                              {lesson.type === "project" ? <Hammer size={12} /> : <Code2 size={12} />}
                              {lesson.type === "project" ? "Project" : "Lesson"}
                              {lesson.xp ? ` · +${lesson.xp} XP` : ""}
                            </p>
                          </div>
                        ) : (
                          <Link
                            to={`/curriculum/${track.id}/${lesson.id}`}
                            className="min-w-0 flex-1"
                          >
                            <p className="truncate text-sm font-semibold text-text-primary hover:text-nature-blossom">
                              {lesson.title}
                            </p>
                            <p className="flex items-center gap-2 text-xs text-text-muted">
                              {lesson.type === "project" ? <Hammer size={12} /> : <Code2 size={12} />}
                              {lesson.type === "project" ? "Project" : "Lesson"}
                              {lesson.duration ? ` · ${lesson.duration}` : ""}
                              {lesson.xp ? ` · +${lesson.xp} XP` : ""}
                            </p>
                          </Link>
                        )}

                        {isDone && (
                          <span className="flex items-center gap-1 text-xs font-semibold text-nature-blossom">
                            <Sparkles size={13} /> +{lesson.xp || 0} XP
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
