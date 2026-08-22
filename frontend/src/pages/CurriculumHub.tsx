import { Link } from "react-router-dom";
import { ArrowRight, Braces, CheckCircle2, Code2, Palette } from "lucide-react";
import { useCurriculumIndex } from "../hooks/useLesson";
import Spinner from "../components/ui/Spinner";

const ICONS = { Code2, Palette, Braces };

const PROGRESS_KEY = "pp_curriculum_progress_v1";

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
  } catch {
    return {};
  }
}

export default function CurriculumHub() {
  const { index, loading, error } = useCurriculumIndex();
  const progress = readProgress();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base">
        <Spinner />
      </div>
    );
  }

  if (error || !index) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-surface-base px-6 text-center">
        <p className="text-lg font-semibold text-text-primary">Curriculum unavailable</p>
        <p className="text-sm text-text-muted">{error || "Couldn't load the curriculum."}</p>
      </div>
    );
  }

  const totalLessons = index.tracks.reduce(
    (n, t) => n + t.sections.reduce((m, s) => m + s.lessons.length, 0),
    0
  );

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="mx-auto max-w-[1000px] px-4 py-12">
        <p className="mb-2 text-sm font-bold uppercase tracking-widest text-nature-blossom">
          Interactive Courses
        </p>
        <h1 className="font-display text-3xl font-black tracking-tight">
          Learn to code, one step at a time.
        </h1>
        <p className="mt-3 max-w-xl text-[15px] leading-relaxed text-text-muted">
          Hands-on lessons with a live preview, hints when you're stuck, and a quick quiz to lock it
          in. {totalLessons} lessons across {index.tracks.length} tracks so far — more on the way.
        </p>

        <div className="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {index.tracks.map((track) => {
            const Icon = ICONS[track.icon] || Code2;
            const lessons = track.sections.flatMap((s) => s.lessons);
            const done = lessons.filter((l) => progress[l.id]).length;
            const pct = lessons.length ? Math.round((done / lessons.length) * 100) : 0;
            const color = track.color || "#4F8F57";

            return (
              <Link
                key={track.id}
                to={`/curriculum/${track.id}`}
                className="group flex flex-col rounded-3xl border border-[#E5E7EB] bg-white p-6 shadow-[0_1px_2px_rgba(31,41,55,0.04)] transition-all hover:-translate-y-0.5 hover:shadow-lg"
              >
                <div
                  className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl text-white"
                  style={{ backgroundColor: color }}
                >
                  <Icon size={24} />
                </div>
                <h2 className="font-display text-xl font-bold">{track.title}</h2>
                <p className="mt-1 flex-1 text-sm leading-relaxed text-text-muted">
                  {track.tagline}
                </p>

                <div className="mt-5">
                  <div className="mb-1.5 flex items-center justify-between text-xs font-semibold">
                    <span className="text-text-muted">
                      {lessons.length} lessons · {done} done
                    </span>
                    <span className="flex items-center gap-1 text-nature-blossom">
                      <ArrowRight
                        size={14}
                        className="transition-transform group-hover:translate-x-0.5"
                      />
                    </span>
                  </div>
                  <div className="h-1.5 overflow-hidden rounded-full bg-[#F3F4F6]">
                    <div
                      className="h-1.5 rounded-full transition-all"
                      style={{ width: `${pct}%`, backgroundColor: color }}
                    />
                  </div>
                </div>

                {done === lessons.length && lessons.length > 0 && (
                  <p className="mt-3 flex items-center gap-1.5 text-xs font-semibold text-nature-blossom">
                    <CheckCircle2 size={13} /> Track complete — well done!
                  </p>
                )}
              </Link>
            );
          })}
        </div>

        <p className="mt-10 text-center text-xs text-text-muted">
          All 7 languages are here — more lessons and advanced tracks landing soon.
        </p>
      </div>
    </div>
  );
}
