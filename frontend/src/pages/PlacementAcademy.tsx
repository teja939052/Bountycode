import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  BookOpen,
  Brain,
  Building2,
  CheckCircle2,
  Clock,
  Compass,
  GraduationCap,
  Search,
  ShieldCheck,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { useJourneyState } from "../hooks/useJourneyState";
import AcademyProfileSetup from "../components/academy/AcademyProfileSetup";
import AcademyDiagnostic from "../components/academy/AcademyDiagnostic";
import AcademyPersonalPlan from "../components/academy/AcademyPersonalPlan";

type Lesson = {
  id: string;
  slug: string;
  title: string;
  domain: string;
  difficulty: string;
  duration_min: number;
  step_count: number;
  learning_objectives?: string[];
  prerequisites?: string[];
  concept_count?: number;
  worked_example_count?: number;
  assessment_count?: number;
  company_count?: number;
  exercise_types?: string[];
};

type SkillEvidence = {
  score: number;
  mastery: string;
  mastery_label: string;
  accuracy: number;
  total_attempts: number;
  correct_count: number;
};

const LESSON_BY_TOPIC: Record<string, string> = {
  percentages: "successive_percentage_change",
  profit_loss: "profit_loss",
  ratio_proportion: "ratio_proportion",
  ratio: "ratio_proportion",
  averages: "averages",
  time_work: "time_work",
  time_distance: "time_distance",
  speed_time_distance: "time_distance",
  probability: "probability_basics",
  permutations: "permutations_combinations",
  permutation: "permutations_combinations",
  series: "number_series",
  number_series: "number_series",
  coding_decoding: "coding_decoding",
  blood_relation: "blood_relations",
  blood_relations: "blood_relations",
  reading_comprehension: "reading_comprehension",
  sentence_correction: "sentence_correction",
  grammar: "sentence_correction",
  para_jumbles: "para_jumbles",
  variable: "variables_basics",
  variables: "variables_basics",
  types: "variables_basics",
  data_types: "variables_basics",
  assignment: "variables_basics",
  assignments: "variables_basics",
  conditions: "conditions_basics",
  conditionals: "conditions_basics",
  if_else: "conditions_basics",
  conditional_logic: "conditions_basics",
  boolean_logic: "conditions_basics",
  branching: "conditions_basics",
  function: "functions_basics",
  functions: "functions_basics",
  parameters: "functions_basics",
  return_values: "functions_basics",
  arrays: "arrays_basics",
  strings: "strings_basics",
  loops: "loops_basics",
  recursion: "recursion_basics",
  sorting: "sorting_basics",
  searching: "searching_basics",
  hashing: "hashing_basics",
  hashmaps: "hashing_basics",
  joins: "sql_joins",
  sql: "sql_select_basics",
  oop: "oops_basics",
  normalization: "dbms_basics",
  os: "os_basics",
  operating_systems: "os_basics",
  networking: "computer_networks_basics",
  computer_networks: "computer_networks_basics",
  number_system: "number_systems",
  number_systems: "number_systems",
  hcf_lcm: "hcf_lcm",
  hcf: "hcf_lcm",
  lcm: "hcf_lcm",
  simple_interest: "simple_compound_interest",
  compound_interest: "simple_compound_interest",
  interest: "simple_compound_interest",
  mixture_alligation: "mixture_alligation",
  mixtures: "mixture_alligation",
  alligation: "mixture_alligation",
  syllogisms: "syllogisms",
  direction_sense: "direction_sense",
  directions: "direction_sense",
  puzzles: "logical_puzzles",
  arrangements: "logical_puzzles",
  seating_arrangement: "logical_puzzles",
  venn_diagrams: "logical_puzzles",
  clocks: "clocks_calendars",
  calendars: "clocks_calendars",
  linked_list: "linked_lists",
  linked_lists: "linked_lists",
  trees: "trees_basics",
  binary_trees: "trees_basics",
  bst: "trees_basics",
  stacks_queues: "stacks_queues",
  stack: "stacks_queues",
  queue: "stacks_queues",
  dynamic_programming: "dynamic_programming",
  dp: "dynamic_programming",
  basic_dp: "dynamic_programming",
  exception_handling: "exception_handling",
  exceptions: "exception_handling",
  file_io: "file_io",
  files: "file_io",
  time_complexity: "time_complexity",
  complexity_analysis: "time_complexity",
  big_o: "time_complexity",
  subqueries: "sql_subqueries",
  exists: "sql_subqueries",
  not_exists: "sql_subqueries",
  in: "sql_subqueries",
  any_all: "sql_subqueries",
  group_by: "sql_group_by",
  having: "sql_group_by",
  aggregation: "sql_group_by",
  matrix: "matrix_operations",
  matrices: "matrix_operations",
  matrix_operations: "matrix_operations",
  pipes_cisterns: "pipes_cisterns",
  number_analogies: "analogies_odd_one_out",
  odd_one_out: "analogies_odd_one_out",
  word_relationships: "analogies_odd_one_out",
  word_analogy: "analogies_odd_one_out",
  active_passive_voice: "grammar_transformations",
  direct_indirect_speech: "grammar_transformations",
  error_spotting: "error_spotting",
  cloze_test: "vocabulary_cloze",
  fill_in_blanks: "vocabulary_cloze",
  synonyms_antonyms: "vocabulary_cloze",
  vocabulary: "vocabulary_cloze",
  one_word_substitution: "vocabulary_cloze",
  java_python_basics: "programming_languages",
  c_java_python_basics: "programming_languages",
  collections: "collections_framework",
  pattern_printing: "pattern_printing",
  pattern_matching: "pattern_matching_basics",
  basic_pattern_matching: "pattern_matching_basics",
  pattern_recognition: "pattern_matching_basics",
  indexing: "sql_indexes_triggers",
  triggers: "sql_indexes_triggers",
  basic_algorithms: "algorithms_basics",
  mathematical: "algorithms_basics",
  math: "algorithms_basics",
  arithmetic: "arithmetic_algebra",
  algebra: "arithmetic_algebra",
  geometry: "geometry_basics",
  basic_ds: "data_structures_intro",
  technology_topics: "essay_writing",
  current_affairs: "essay_writing",
  opinion_essays: "essay_writing",
  technology: "essay_writing",
  business: "essay_writing",
  social_issues: "essay_writing",
  essay: "essay_writing",
  advanced_mixtures: "mixture_alligation",
  conditions: "loops_basics",
  reading: "reading_comprehension",
  sentence_rearrangement: "para_jumbles",
  advanced_probability: "advanced_probability",
  advanced_time_work: "advanced_time_work",
  simple_compound_interest: "simple_compound_interest",
  critical_reasoning: "logical_puzzles",
  dynamic_programming_basics: "dynamic_programming",

};

function normalizeTopic(value: string) {
  return value.toLowerCase().trim().replace(/[\s-]+/g, "_");
}

function nextTopicLesson(module: any, trackId: string) {
  const mastery = module.topic_mastery || {};
  for (const topic of module.topics || []) {
    const key = normalizeTopic(topic);
    if (mastery[key]?.mastered) continue;
    const slug = LESSON_BY_TOPIC[key];
    if (slug) {
      return `/learn/lesson/${slug}?track_id=${encodeURIComponent(trackId)}&module_id=${encodeURIComponent(module.id)}&topic_id=${encodeURIComponent(key)}`;
    }
  }
  return null;
}

function percent(value: unknown) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.max(0, Math.min(100, Math.round(n))) : 0;
}

function learningTrackForDomain(domain: string): string {
  const value = String(domain || "").toLowerCase();
  if (value.includes("sql") || value.includes("database")) return "SQL & Databases";
  if (value.includes("aptitude") || value.includes("quantitative") || value.includes("arithmetic") || value.includes("math")) return "Quantitative Aptitude";
  if (value.includes("reason") || value.includes("logical") || value.includes("puzzle")) return "Logical Reasoning";
  if (value.includes("verbal") || value.includes("grammar") || value.includes("vocabulary") || value.includes("english")) return "Verbal & Communication";
  if (value.includes("computer science") || value.includes("operating system") || value === "os" || value.includes("network") || value.includes("dbms") || value.includes("oop")) return "Core Computer Science";
  if (value.includes("dsa") || value.includes("data structure") || value.includes("algorithm") || value.includes("programming") || value.includes("coding") || value.includes("code")) return "Programming & DSA";
  return "General Foundations";
}

const LEARNING_TRACK_ORDER = [
  "Programming & DSA",
  "Quantitative Aptitude",
  "Logical Reasoning",
  "Verbal & Communication",
  "SQL & Databases",
  "Core Computer Science",
  "General Foundations",
];

const LESSON_SEQUENCE_BY_TRACK: Record<string, string[]> = {
  "Programming & DSA": [
    "variables_basics", "conditions_basics", "functions_basics",
    "programming_languages", "loops_basics", "pattern_printing", "arrays_basics",
    "strings_basics", "data_structures_intro", "time_complexity", "searching_basics",
    "sorting_basics", "hashing_basics", "recursion_basics", "linked_lists",
    "stacks_queues", "trees_basics", "dynamic_programming", "sliding_window",
    "algorithms_basics", "collections_framework", "exception_handling", "file_io",
    "matrix_operations",
  ],
  "Quantitative Aptitude": [
    "number_systems", "hcf_lcm", "arithmetic_algebra", "successive_percentage_change",
    "profit_loss", "ratio_proportion", "averages", "time_work", "time_distance",
    "advanced_time_work", "simple_compound_interest", "mixture_alligation",
    "pipes_cisterns", "permutations_combinations", "probability_basics",
    "advanced_probability", "geometry_basics", "clocks_calendars",
  ],
  "Logical Reasoning": [
    "number_series", "coding_decoding", "blood_relations", "direction_sense",
    "syllogisms", "analogies_odd_one_out", "logical_puzzles", "flowchart_basics",
    "pattern_matching_basics",
  ],
  "Verbal & Communication": [
    "vocabulary_cloze", "sentence_correction", "grammar_transformations",
    "error_spotting", "para_jumbles", "reading_comprehension", "essay_writing",
  ],
  "SQL & Databases": [
    "dbms_basics", "sql_select_basics", "sql_joins", "sql_group_by",
    "sql_subqueries", "sql_indexes_triggers",
  ],
  "Core Computer Science": [
    "oops_basics", "os_basics", "computer_networks_basics",
  ],
};

function orderTrackLessons(track: string, lessons: Lesson[]): Lesson[] {
  const sequence = LESSON_SEQUENCE_BY_TRACK[track] || [];
  return [...lessons].sort((left, right) => {
    const leftIndex = sequence.indexOf(left.slug);
    const rightIndex = sequence.indexOf(right.slug);
    if (leftIndex < 0 && rightIndex < 0) return left.title.localeCompare(right.title);
    if (leftIndex < 0) return 1;
    if (rightIndex < 0) return -1;
    return leftIndex - rightIndex;
  });
}

export default function PlacementAcademy() {
  const navigate = useNavigate();
  const { data: journey, isLoading: journeyLoading } = useJourneyState();
  const [lessonQuery, setLessonQuery] = useState("");
  const [domainFilter, setDomainFilter] = useState("all");

  const { data: tracksResult, isLoading: tracksLoading } = useQuery({
    queryKey: ["company-tracks", "list"],
    queryFn: () => api.companyTracks.listCompanies(),
    staleTime: 60_000,
  });

  const enrolledTracks = tracksResult?.tracks?.filter((track: any) => track.enrolled) || [];
  const activeTrackId =
    journey?.company?.company_track ||
    enrolledTracks[0]?.id ||
    "";

  const { data: trackDetail, isLoading: trackLoading } = useQuery({
    queryKey: ["company-tracks", "detail", activeTrackId],
    queryFn: () => api.companyTracks.getTrack(activeTrackId),
    enabled: Boolean(activeTrackId),
    staleTime: 30_000,
  });

  const { data: dailyResult, isLoading: dailyLoading } = useQuery({
    // Journey and Academy now consume the same authoritative Study Engine plan.
    queryKey: ["study", "today"],
    queryFn: () => api.journey.getToday(),
    staleTime: 30_000,
    retry: 1,
  });

  const { data: skillResult, isLoading: skillsLoading } = useQuery({
    queryKey: ["adaptive", "skills"],
    queryFn: () => api.adaptive.getSkillAssessment(),
    staleTime: 60_000,
    retry: 1,
  });

  const { data: lessonResult, isLoading: lessonsLoading } = useQuery({
    queryKey: ["company-lessons", "catalog"],
    queryFn: () => api.companyLessons.listLessons(),
    staleTime: 300_000,
  });

  const daily = (dailyResult as any)?.data ?? dailyResult ?? {};
  // The Study Engine publishes company work as company_mission. Prefer that
  // canonical target-aware mission over generic daily tasks.
  const mission = daily?.company_mission || daily?.company_focus || daily?.tasks?.[0] || null;
  const skillData = (skillResult as any)?.data ?? skillResult ?? {};
  const skills = (skillData.skills ?? skillData.assessment?.skills ?? {}) as Record<string, SkillEvidence>;
  const skillRows = useMemo(
    () => Object.entries(skills)
      .map(([id, value]) => ({ id, ...value }))
      .filter((skill) => skill.total_attempts > 0)
      .sort((a, b) => a.score - b.score)
      .slice(0, 5),
    [skills],
  );

  const allLessons = ((lessonResult as any)?.data ?? []) as Lesson[];
  const domains = useMemo(
    () => [
      "all",
      ...Array.from(new Set(allLessons.map((lesson) => learningTrackForDomain(lesson.domain))))
        .sort((a, b) => LEARNING_TRACK_ORDER.indexOf(a) - LEARNING_TRACK_ORDER.indexOf(b)),
    ],
    [allLessons],
  );
  const lessons = useMemo(() => {
    const q = lessonQuery.trim().toLowerCase();
    return allLessons.filter((lesson) => {
      const matchesQuery =
        !q ||
        lesson.title.toLowerCase().includes(q) ||
        lesson.domain.toLowerCase().includes(q) ||
        lesson.slug.toLowerCase().includes(q);
      const matchesDomain = domainFilter === "all" || learningTrackForDomain(lesson.domain) === domainFilter;
      return matchesQuery && matchesDomain;
    });
  }, [allLessons, lessonQuery, domainFilter]);

  const modules = (trackDetail as any)?.sections?.flatMap((section: any) => section.modules || []) || [];
  const missionModule = modules.find((module: any) => module.id === mission?.module_id);
  const missionLessonUrl = missionModule && activeTrackId
    ? nextTopicLesson(missionModule, activeTrackId)
    : null;
  const prioritizedModules = missionModule
    ? [missionModule, ...modules.filter((module: any) => module.id !== missionModule.id)]
    : modules;
  const completedModules = modules.filter((module: any) => module.completed).length;
  const topicTotal = modules.reduce((sum: number, module: any) => sum + (module.topics?.length || 0), 0);
  const masteredTopicTotal = modules.reduce((sum: number, module: any) => sum + (module.mastered_topic_count || 0), 0);
  const trackProgress = modules.length ? percent(completedModules / modules.length * 100) : 0;

  if (journeyLoading || tracksLoading) {
    return <div className="flex min-h-[50vh] items-center justify-center"><Spinner /></div>;
  }

  return (
    <div className="space-y-6 pb-12">
      <header className="rounded-3xl border border-[#e7e2d8] bg-gradient-to-br from-white via-[#fbfaf6] to-[#f0f5ed] p-5 shadow-sm sm:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-700">
              <GraduationCap size={15} /> Bountycode Placement Academy
            </p>
            <h1 className="mt-3 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Learn it. Practise it. Prove you know it.
            </h1>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              A guided route from fundamentals to company assessments. Your next lesson,
              practice and mastery check should follow your evidence—not a random checklist.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link to="/journey" className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700">
              <Compass size={15} /> Journey
            </Link>
            <Link to="/quiz" className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-4 text-sm font-semibold text-emerald-800">
              <BookOpen size={15} /> Practice quiz
            </Link>
            <Link to="/target" className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-slate-900 px-4 text-sm font-semibold text-white">
              <Target size={15} /> Change target
            </Link>
          </div>
        </div>
      </header>

      <section aria-label="Your personalized learning setup" className="space-y-4">
        <div className="flex items-end justify-between gap-3">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-emerald-700">Your learning system</p>
            <h2 className="mt-1 text-xl font-black text-slate-900">Start with your goal. Then follow your plan.</h2>
            <p className="mt-1 text-sm text-slate-600">Three connected steps turn your placement goal into a practical daily routine.</p>
          </div>
        </div>
        <div className="grid gap-2 sm:grid-cols-3">
          {[
            { number: "01", title: "Set your direction", detail: "Role, companies and available time" },
            { number: "02", title: "Find your starting point", detail: "A server-graded skill diagnostic" },
            { number: "03", title: "Follow your next action", detail: "A plan based on your evidence" },
          ].map((step) => (
            <div key={step.number} className="rounded-xl border border-slate-200 bg-white p-3">
              <p className="text-[10px] font-black tracking-widest text-emerald-700">STEP {step.number}</p>
              <p className="mt-1 text-sm font-bold text-slate-900">{step.title}</p>
              <p className="mt-1 text-xs text-slate-500">{step.detail}</p>
            </div>
          ))}
        </div>
        <div id="academy-profile"><AcademyProfileSetup /></div>
        <AcademyDiagnostic />
        <AcademyPersonalPlan />
      </section>

      {!activeTrackId ? (
        <section className="rounded-2xl border border-dashed border-emerald-300 bg-emerald-50/60 p-6">
          <div className="flex items-start gap-3">
            <Building2 className="mt-1 text-emerald-700" size={22} />
            <div className="flex-1">
              <h2 className="text-lg font-bold text-slate-900">Choose your placement target</h2>
              <p className="mt-1 text-sm text-slate-600">Choose a service-company assessment track to personalize your modules and daily plan.</p>
              <Link to="/target" className="mt-4 inline-flex min-h-10 items-center gap-2 rounded-xl bg-emerald-700 px-4 text-sm font-semibold text-white">
                Browse company tracks <ArrowRight size={15} />
              </Link>
            </div>
          </div>
        </section>
      ) : (
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-2xl">{(trackDetail as any)?.icon || "🏢"}</div>
            <div className="min-w-0 flex-1">
              <p className="text-[10px] font-bold uppercase tracking-wider text-emerald-700">Active placement target</p>
              <h2 className="mt-1 text-xl font-bold text-slate-900">{(trackDetail as any)?.name || activeTrackId}</h2>
              <p className="mt-1 text-xs text-slate-500">{(trackDetail as any)?.description || "Your company-specific preparation track."}</p>
            </div>

          </div>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-2xl font-black text-slate-900">{completedModules}/{modules.length}</p>
              <p className="text-xs text-slate-500">Modules mastered</p>
            </div>
            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-2xl font-black text-slate-900">{masteredTopicTotal}/{topicTotal}</p>
              <p className="text-xs text-slate-500">Topic skills mastered</p>
            </div>
            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-2xl font-black text-slate-900">{trackProgress}%</p>
              <p className="text-xs text-slate-500">Module completion</p>
            </div>
          </div>
          <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
            <div className="h-full rounded-full bg-emerald-600 transition-all" style={{ width: `${trackProgress}%` }} />
          </div>
          {trackLoading && <p className="mt-3 text-xs text-slate-500">Loading your company syllabus…</p>}
        </section>
      )}

      <section className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5">
          <div className="flex items-center gap-2 text-emerald-800">
            <Zap size={17} /> <p className="text-[10px] font-bold uppercase tracking-widest">Your next adaptive mission</p>
          </div>
          {dailyLoading ? (
            <div className="py-7"><Spinner /></div>
          ) : mission ? (
            <>
              <h2 className="mt-3 text-xl font-bold text-slate-900">{mission.title || "Continue your learning path"}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">{mission.description || "Continue the next skill in your learning plan."}</p>
              <div className="mt-4 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                {mission.estimated_minutes && <span className="inline-flex items-center gap-1 rounded-full bg-white px-3 py-1"><Clock size={12} /> {mission.estimated_minutes} min</span>}
                {mission.difficulty && <span className="rounded-full bg-white px-3 py-1 capitalize">{mission.difficulty}</span>}
                {mission.domain_id && <span className="rounded-full bg-white px-3 py-1">{String(mission.domain_id).replace(/_/g, " ")}</span>}
              </div>
              <button
                type="button"
                onClick={() => navigate(missionLessonUrl || mission.action_url || (mission.track_id ? `/company-tracks?track=${encodeURIComponent(mission.track_id)}` : "/learn"))}
                className="mt-5 inline-flex min-h-11 items-center gap-2 rounded-xl bg-emerald-800 px-4 text-sm font-bold text-white"
              >
                {missionLessonUrl ? "Start next lesson" : "Open company module"} <ArrowRight size={15} />
              </button>
            </>
          ) : (
            <p className="mt-3 text-sm text-slate-600">Complete a skill assessment or choose a company track to generate your next mission.</p>
          )}
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5">
          <div className="flex items-center gap-2">
            <Brain size={17} className="text-violet-700" />
            <h2 className="font-bold text-slate-900">Your current skill evidence</h2>
          </div>
          {skillsLoading ? <div className="py-6"><Spinner /></div> : skillRows.length ? (
            <div className="mt-4 space-y-3">
              {skillRows.map((skill) => (
                <div key={skill.id}>
                  <div className="mb-1 flex items-center justify-between gap-2 text-xs">
                    <span className="font-medium capitalize text-slate-700">{skill.id.replace(/_/g, " ")}</span>
                    <span className="text-slate-500">{percent(skill.score)}% · {skill.total_attempts} attempts</span>
                  </div>
                  <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-violet-600" style={{ width: `${percent(skill.score)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-sm text-slate-500">No quiz or coding evidence yet. Your first lesson will start building a skill profile.</p>
          )}
          <Link to="/skills" className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-violet-700">
            View skill map <ArrowRight size={13} />
          </Link>
        </div>
      </section>

      {activeTrackId && modules.length > 0 && (
        <section className="space-y-3">
          <div className="flex items-end justify-between gap-3">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Your employer syllabus</p>
              <h2 className="mt-1 text-xl font-bold text-slate-900">Continue by topic</h2>
            </div>
            <span className="text-xs text-slate-500">Full syllabus</span>
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {prioritizedModules.map((module: any) => {
              const nextUrl = nextTopicLesson(module, activeTrackId);
              const done = Boolean(module.completed);
              const mastered = module.mastered_topic_count || 0;
              const total = module.required_topic_count || module.topics?.length || 0;
              return (
                <article key={module.id} className="rounded-2xl border border-slate-200 bg-white p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold text-slate-900">{module.title}</h3>
                      <p className="mt-1 text-xs text-slate-500">{module.description}</p>
                    </div>
                    {done && <CheckCircle2 className="shrink-0 text-emerald-600" size={19} />}
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {(module.topics || []).map((topic: string) => {
                      const key = normalizeTopic(topic);
                      const isMastered = Boolean(module.topic_mastery?.[key]?.mastered);
                      return <span key={topic} className={`rounded-full px-2 py-1 text-[10px] ${isMastered ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"}`}>{isMastered ? "✓ " : ""}{topic.replace(/_/g, " ")}</span>;
                    })}
                  </div>
                  <p className="mt-3 text-[11px] text-slate-500">{mastered}/{total} topic skills mastered</p>
                  <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-emerald-600" style={{ width: `${total ? percent(mastered / total * 100) : done ? 100 : 0}%` }} />
                  </div>
                  {nextUrl ? (
                    <Link to={nextUrl} className="mt-4 inline-flex min-h-10 items-center gap-2 rounded-lg bg-slate-900 px-3 text-xs font-semibold text-white">
                      Learn next topic <ArrowRight size={13} />
                    </Link>
                  ) : (
                    <Link to={`/company-tracks?track=${encodeURIComponent(activeTrackId)}`} className="mt-4 inline-flex min-h-10 items-center gap-2 rounded-lg border border-slate-200 px-3 text-xs font-semibold text-slate-700">
                      Open module practice <ArrowRight size={13} />
                    </Link>
                  )}
                </article>
              );
            })}
          </div>
        </section>
      )}

      <section className="space-y-3">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Guided lesson library</p>
            <h2 className="mt-1 text-xl font-bold text-slate-900">Choose a skill to learn</h2>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row">
            <label className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input value={lessonQuery} onChange={(event) => setLessonQuery(event.target.value)} placeholder="Search topics…" className="min-h-10 w-full rounded-xl border border-slate-200 bg-white pl-9 pr-3 text-sm outline-none focus:border-emerald-500 sm:w-56" />
            </label>
            <select value={domainFilter} onChange={(event) => setDomainFilter(event.target.value)} className="min-h-10 rounded-xl border border-slate-200 bg-white px-3 text-sm">
              {domains.map((domain) => <option key={domain} value={domain}>{domain === "all" ? "All subjects" : domain}</option>)}
            </select>
          </div>
        </div>
        {lessonsLoading ? <div className="py-8"><Spinner /></div> : lessons.length ? (
          <div className="space-y-7">
            {LEARNING_TRACK_ORDER
              .map((track) => ({
                track,
                items: orderTrackLessons(track, lessons.filter((lesson) => learningTrackForDomain(lesson.domain) === track)),
              }))
              .filter((group) => group.items.length > 0)
              .map((group) => (
                <section key={group.track} aria-label={group.track} className="space-y-3">
                  <div className="flex flex-wrap items-end justify-between gap-2 border-b border-slate-200 pb-2">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-emerald-700">Learning pathway</p>
                      <h3 className="mt-1 text-lg font-bold text-slate-900">{group.track}</h3>
                    </div>
                    <span className="text-xs text-slate-500">{group.items.length} lessons · suggested progression</span>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                    {group.items.map((lesson, index) => (
                      <Link key={lesson.slug} to={`/learn/lesson/${lesson.slug}`} className="group rounded-2xl border border-slate-200 bg-white p-4 transition hover:-translate-y-0.5 hover:border-emerald-300 hover:shadow-sm">
                        <div className="flex items-start justify-between gap-2">
                          <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-semibold text-slate-600">{lesson.domain}</span>
                          <BookOpen size={16} className="text-emerald-700" />
                        </div>
                        <h4 className="mt-3 font-semibold text-slate-900 group-hover:text-emerald-700">{lesson.title}</h4>
                        <p className="mt-1 text-xs text-slate-500">{lesson.step_count} guided steps · {lesson.duration_min} min · {lesson.difficulty}</p>
                        {lesson.learning_objectives?.length ? (
                          <ul className="mt-3 space-y-1">
                            {lesson.learning_objectives.slice(0, 2).map((objective) => (
                              <li key={objective} className="line-clamp-1 text-xs text-slate-600">• {objective}</li>
                            ))}
                          </ul>
                        ) : null}
                        {lesson.prerequisites?.length ? (
                          <p className="mt-2 text-[11px] leading-5 text-slate-500">
                            Recommended first: {lesson.prerequisites.slice(0, 2).map((item) => item.replaceAll("_", " ")).join(", ")}
                          </p>
                        ) : null}
                        <div className="mt-3 flex flex-wrap gap-1.5">
                          {typeof lesson.concept_count === "number" && <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] text-slate-600">{lesson.concept_count} concepts</span>}
                          {typeof lesson.worked_example_count === "number" && <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] text-slate-600">{lesson.worked_example_count} examples</span>}
                          {typeof lesson.assessment_count === "number" && <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] text-slate-600">{lesson.assessment_count} assessment questions</span>}
                          {typeof lesson.company_count === "number" && lesson.company_count > 0 && <span className="rounded-full bg-emerald-50 px-2 py-1 text-[10px] text-emerald-700">{lesson.company_count} company contexts</span>}
                          {lesson.exercise_types?.length ? <span className="rounded-full bg-blue-50 px-2 py-1 text-[10px] text-blue-700">{lesson.exercise_types.length} exercise formats</span> : null}
                        </div>
                        <span className="mt-3 inline-flex items-center gap-1 text-xs font-semibold text-emerald-700">Start lesson <ArrowRight size={13} /></span>
                      </Link>
                    ))}
                  </div>
                </section>
              ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-300 p-6 text-center text-sm text-slate-500">No lessons match this filter.</div>
        )}
      </section>

      <footer className="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-slate-900 p-5 text-white">
        <div className="flex items-center gap-3">
          <ShieldCheck size={22} className="text-emerald-300" />
          <div>
            <h2 className="font-semibold">Mastery comes from evidence</h2>
            <p className="mt-1 text-xs text-slate-300">A topic is recorded only after a server-graded assessment; a mixed module needs every required skill.</p>
          </div>
        </div>
        <Link to="/mock-oa" className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-white px-4 text-xs font-bold text-slate-900">Take a timed mock <TrendingUp size={14} /></Link>
      </footer>
    </div>
  );
}
