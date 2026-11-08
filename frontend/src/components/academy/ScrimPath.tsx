import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { BookOpen, ChevronRight, Sparkles, Target, Zap } from "lucide-react";

/** Coddy-style ordered scrim tracks (mirrors backend scrim_catalog.json). */
const SCRIM_TRACKS = [
  {
    id: "programming",
    name: "Programming",
    blurb: "Variables → control flow → code lab → arrays & strings",
    color: "#22c55e",
    scrims: [
      { slug: "variables_basics", title: "Variables and assignment" },
      { slug: "conditions_basics", title: "Conditions and branching" },
      { slug: "loops_basics", title: "Loops and repetition" },
      { slug: "loops_code_lab", title: "Code lab — sum with a loop" },
      { slug: "functions_basics", title: "Functions and parameters" },
      { slug: "arrays_basics", title: "Arrays and lists" },
      { slug: "strings_basics", title: "Strings basics" },
    ],
  },
  {
    id: "quant",
    name: "Quant",
    blurb: "NQT-heavy aptitude in short interactive missions",
    color: "#3b82f6",
    scrims: [
      { slug: "number_systems", title: "Number systems" },
      { slug: "percentages", title: "Percentages" },
      { slug: "successive_percentage_change", title: "Successive percentages" },
      { slug: "profit_loss", title: "Profit, loss & discount" },
      { slug: "ratio_proportion", title: "Ratio & proportion" },
      { slug: "averages", title: "Averages" },
      { slug: "time_work", title: "Time & work" },
      { slug: "time_distance", title: "Time & distance" },
      { slug: "hcf_lcm", title: "HCF & LCM" },
      { slug: "simple_compound_interest", title: "Simple & compound interest" },
      { slug: "pipes_cisterns", title: "Pipes & cisterns" },
      { slug: "mixture_alligation", title: "Mixtures & alligation" },
      { slug: "probability_basics", title: "Probability basics" },
    ],
  },
  {
    id: "reasoning",
    name: "Reasoning",
    blurb: "Series, puzzles, relations — rule then apply",
    color: "#a855f7",
    scrims: [
      { slug: "number_series", title: "Number series" },
      { slug: "coding_decoding", title: "Coding–decoding" },
      { slug: "blood_relations", title: "Blood relations" },
      { slug: "direction_sense", title: "Direction sense" },
      { slug: "syllogisms", title: "Syllogisms" },
      { slug: "seating_arrangement", title: "Seating arrangement" },
      { slug: "analogies_odd_one_out", title: "Analogies & odd one out" },
      { slug: "logical_puzzles", title: "Logical puzzles" },
      { slug: "clocks_calendars", title: "Clocks & calendars" },
    ],
  },
  {
    id: "verbal",
    name: "Verbal",
    blurb: "RC, grammar, cloze — passage-first discipline",
    color: "#f59e0b",
    scrims: [
      { slug: "reading_comprehension", title: "Reading comprehension" },
      { slug: "error_spotting", title: "Error spotting" },
      { slug: "vocabulary_cloze", title: "Vocabulary & cloze" },
      { slug: "grammar_transformations", title: "Grammar transformations" },
      { slug: "sentence_correction", title: "Sentence correction" },
      { slug: "para_jumbles", title: "Para jumbles" },
    ],
  },
  {
    id: "dsa",
    name: "DSA / OA",
    blurb: "Structures and patterns used in service coding rounds",
    color: "#ef4444",
    scrims: [
      { slug: "data_structures_intro", title: "Data structures intro" },
      { slug: "hashing_basics", title: "Hashing basics" },
      { slug: "algorithms_basics", title: "Algorithms basics" },
      { slug: "sorting_basics", title: "Sorting basics" },
      { slug: "searching_basics", title: "Searching basics" },
      { slug: "recursion_basics", title: "Recursion basics" },
    ],
  },
] as const;

export default function ScrimPath() {
  const [trackId, setTrackId] = useState<string>(SCRIM_TRACKS[0].id);
  const track = useMemo(
    () => SCRIM_TRACKS.find((t) => t.id === trackId) || SCRIM_TRACKS[0],
    [trackId],
  );

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.16em] text-emerald-700">
            <Sparkles size={14} /> Coddy-style scrim path
          </p>
          <h2 className="mt-1 text-xl font-black text-slate-900">Interactive missions by domain</h2>
          <p className="mt-1 max-w-2xl text-sm text-slate-600">
            Short explain → try → feedback loops. Hints help you learn; only server-graded
            assessments award mastery.
          </p>
        </div>
        <Link
          to="/skill-graph"
          className="inline-flex shrink-0 items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-white"
        >
          <Target size={14} /> Skill map
        </Link>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {SCRIM_TRACKS.map((t) => {
          const active = t.id === track.id;
          return (
            <button
              key={t.id}
              type="button"
              onClick={() => setTrackId(t.id)}
              className={`rounded-full px-3.5 py-1.5 text-xs font-bold transition ${
                active
                  ? "text-white shadow"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
              style={active ? { background: t.color } : undefined}
            >
              {t.name}
              <span className="ml-1 opacity-80">({t.scrims.length})</span>
            </button>
          );
        })}
      </div>

      <p className="mt-3 text-xs font-medium text-slate-500">{track.blurb}</p>

      <ol className="mt-4 space-y-2">
        {track.scrims.map((scrim, index) => (
          <li key={scrim.slug}>
            <Link
              to={`/learn/lesson/${scrim.slug}`}
              className="group flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50/80 px-3 py-3 transition hover:border-emerald-300 hover:bg-emerald-50/40"
            >
              <span
                className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-black text-white"
                style={{ background: track.color }}
              >
                {index + 1}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-bold text-slate-900">{scrim.title}</p>
                <p className="truncate text-[11px] text-slate-500">{scrim.slug.replace(/_/g, " ")}</p>
              </div>
              <span className="hidden items-center gap-1 text-[11px] font-semibold text-slate-500 sm:inline-flex">
                <BookOpen size={12} /> Scrim
              </span>
              <ChevronRight size={16} className="shrink-0 text-slate-400 transition group-hover:text-emerald-600" />
            </Link>
          </li>
        ))}
      </ol>

      <p className="mt-4 flex items-center gap-2 text-[11px] text-slate-500">
        <Zap size={12} className="text-amber-500" />
        Progress is evidence-based. Completing a scrim updates your skill map when the assessment passes.
      </p>
    </section>
  );
}
