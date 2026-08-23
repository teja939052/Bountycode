import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useSearchParams } from "react-router-dom";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  Clock,
  Code2,
  Compass,
  Lightbulb,
  Search,
  Sparkles,
  X,
  XCircle,
} from "lucide-react";
import { studyApi } from "../services/api/study.ts";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";

const LEVEL_STYLES = {
  beginner: "text-brand-primary border-brand-primary/20 bg-brand-primary/10",
  intermediate: "text-brand-gold border-amber-500/30 bg-amber-500/10",
  advanced: "text-rose-400 border-rose-500/30 bg-rose-500/10",
};

const CATEGORY_COLORS = {
  "html-css": "text-[#E34F26] border-[#E34F26]/30 bg-[#E34F26]/10",
  javascript: "text-[#F7DF1E] border-[#F7DF1E]/30 bg-[#F7DF1E]/10",
  typescript: "text-[#3178C6] border-[#3178C6]/30 bg-[#3178C6]/10",
  react: "text-[#61DAFB] border-[#61DAFB]/30 bg-[#61DAFB]/10",
  node: "text-[#339933] border-[#339933]/30 bg-[#339933]/10",
  sql: "text-[#4479A1] border-[#4479A1]/30 bg-[#4479A1]/10",
  "full-stack": "text-[#8B5CF6] border-[#8B5CF6]/30 bg-[#8B5CF6]/10",
};

function CategoryPill({ categoryId, name, icon, color, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 rounded-xl border px-3 py-2 text-sm font-mono transition-all ${
        active
          ? "border-white/40 bg-white border-border/10 text-text-primary"
          : "border-brand-primary/10 bg-white/[0.03] text-text-light hover:border-white/25 hover:bg-white/[0.06]"
      }`}
    >
      <span className="text-base leading-none">{icon}</span>
      {name}
      <span className="ml-1 h-1.5 w-1.5 rounded-full" style={{ background: color }} />
    </button>
  );
}

function ArticleCard({ article, onOpen }) {
  const cat = article.category;
  return (
    <motion.div whileHover={{ y: -4 }} className="group">
      <button onClick={() => onOpen(article.id)} className="block h-full w-full text-left">
        <div className="arena-card flex h-full flex-col p-5">
          <div className="flex items-center justify-between gap-2">
            <span className={`rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider ${CATEGORY_COLORS[cat] || "border-white/20 bg-white border-border shadow-card text-text-light"}`}>
              {cat.replace("-", " & ")}
            </span>
            <span className="flex items-center gap-1 text-[10px] font-mono text-text-light">
              <Clock size={10} /> {article.read_time_min} min
            </span>
          </div>

          <h3 className="mt-3 font-display font-bold text-text-primary group-hover:text-white transition-colors">
            {article.title}
          </h3>
          <p className="mt-2 text-sm leading-6 text-text-muted line-clamp-3">{article.summary}</p>

          <div className="mt-auto pt-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase ${LEVEL_STYLES[article.level] || LEVEL_STYLES.beginner}`}>
                {article.level}
              </span>
              <div className="flex flex-wrap gap-1.5">
                {article.related_topics.slice(0, 3).map(topic => (
                  <span key={topic} className="text-[10px] font-mono text-text-light">
                    #{topic}
                  </span>
                ))}
              </div>
            </div>
            <span className="mt-3 inline-flex items-center gap-1 text-xs font-mono text-cyber-blue">
              Read study article <ChevronRight size={12} className="transition-transform group-hover:translate-x-1" />
            </span>
          </div>
        </div>
      </button>
    </motion.div>
  );
}

function QuizBlock({ quiz }) {
  const [revealed, setRevealed] = useState({});
  const [picked, setPicked] = useState({});

  if (!quiz || quiz.length === 0) return null;

  return (
    <div className="mt-8 space-y-5">
      <h3 className="flex items-center gap-2 text-sm font-display font-bold text-cyber-purple">
        <CheckCircle2 size={15} /> Quick check — do you remember?
      </h3>
      {quiz.map((q, qi) => {
        const isPicked = picked[qi] !== undefined;
        const isCorrect = isPicked && picked[qi] === q.answer;
        return (
          <div key={qi} className="rounded-2xl border border-cyber-purple/20 bg-surface-card/10 p-5">
            <p className="text-sm font-medium text-text-primary">{qi + 1}. {q.question}</p>
            <div className="mt-3 grid gap-2">
              {q.options.map((opt, oi) => {
                const isAnswer = oi === q.answer;
                const isChosen = picked[qi] === oi;
                let cls = "border-brand-primary/10 bg-surface-card/10 text-text-secondary hover:border-cyber-purple/40 hover:bg-white/[0.05]";
                if (revealed[qi] || isPicked) {
                  if (isAnswer) cls = "border-brand-primary/30 bg-brand-primary/10 text-brand-primary";
                  else if (isChosen) cls = "border-rose-400/40 bg-rose-500/10 text-rose-300";
                  else cls = "border-white/5 bg-white/[0.01] text-text-muted";
                }
                return (
                  <button
                    key={oi}
                    disabled={isPicked}
                    onClick={() => setPicked(p => ({ ...p, [qi]: oi }))}
                    className={`rounded-xl border px-3 py-2 text-left text-xs leading-6 transition-all disabled:cursor-default ${cls}`}
                  >
                    <span className="mr-2 font-mono text-text-light">{String.fromCharCode(65 + oi)}.</span>
                    {opt}
                    {revealed[qi] && isAnswer && <CheckCircle2 size={12} className="ml-2 inline text-brand-primary" />}
                    {revealed[qi] && isChosen && !isAnswer && <XCircle size={12} className="ml-2 inline text-rose-400" />}
                  </button>
                );
              })}
            </div>
            <div className="mt-3 flex items-center gap-2">
              {!revealed[qi] && (
                <button
                  onClick={() => setRevealed(r => ({ ...r, [qi]: true }))}
                  className="btn-primary px-3 py-1.5 text-xs"
                >
                  {isPicked ? "Check answer" : "Show answer"}
                </button>
              )}
              {revealed[qi] && (
                <span className={`text-xs font-mono ${isCorrect ? "text-brand-primary" : "text-brand-gold"}`}>
                  {isCorrect ? "Correct — well done!" : `Answer: ${q.options[q.answer]}`}
                </span>
              )}
            </div>
            {revealed[qi] && q.explanation && (
              <p className="mt-3 rounded-xl border border-white/5 bg-surface-2 p-3 text-xs leading-6 text-text-secondary">
                <Lightbulb size={12} className="mr-1 inline text-brand-gold" />
                {q.explanation}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}

function ExerciseBlock({ exercise }) {
  const [tab, setTab] = useState("task");

  if (!exercise) return null;
  const tabs = [
    { id: "task", label: "Task", node: <p className="text-sm leading-7 text-text-secondary">{exercise.task}</p> },
    { id: "starter", label: "Starter", node: <pre className="overflow-x-auto rounded-xl border border-brand-primary/10 bg-surface-card/50 p-4 text-xs leading-6 text-brand-primary"><code>{exercise.starter}</code></pre> },
    { id: "solution", label: "Solution", node: <pre className="overflow-x-auto rounded-xl border border-emerald-400/20 bg-surface-card/50 p-4 text-xs leading-6 text-brand-primary"><code>{exercise.solution}</code></pre> },
    ...(exercise.hint ? [{ id: "hint", label: "Hint", node: <p className="text-sm leading-7 text-brand-gold-pale">{exercise.hint}</p> }] : []),
  ];

  return (
    <div className="mt-8 rounded-2xl border border-brand-gold/25 bg-brand-gold/5 p-5">
      <h3 className="flex items-center gap-2 text-sm font-display font-bold text-brand-gold">
        <Code2 size={15} /> Coding exercise — {exercise.title}
      </h3>
      <div className="mt-3 flex flex-wrap gap-1.5">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`rounded-lg border px-3 py-1.5 text-xs font-mono transition-colors ${
              tab === t.id
                ? "border-brand-gold/40 bg-brand-gold/10 text-brand-gold"
                : "border-brand-primary/10 bg-surface-card/10 text-text-light hover:border-white/25"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className="mt-4">{tabs.find(t => t.id === tab)?.node}</div>
      {tab === "task" && (
        <p className="mt-3 text-[11px] font-mono text-text-light">
          Try it yourself first, then peek at the starter code and solution.
        </p>
      )}
    </div>
  );
}

function ArticleModal({ article, onClose }) {
  if (!article) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-surface-2 p-4 backdrop-blur-sm md:py-12"
        onClick={onClose}
      >
        <motion.div
          initial={{ y: 24, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 24, opacity: 0 }}
          onClick={e => e.stopPropagation()}
          className="arena-card relative my-auto w-full max-w-3xl p-6 md:p-8"
        >
          <button
            onClick={onClose}
            className="absolute right-4 top-4 rounded-lg border border-brand-primary/10 p-1.5 text-text-light transition-colors hover:border-white/30 hover:text-white"
            aria-label="Close article"
          >
            <X size={16} />
          </button>

          <div className="flex flex-wrap items-center gap-2 pr-8">
            <span className={`rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider ${CATEGORY_COLORS[article.category] || "border-white/20 bg-white border-border shadow-card text-text-light"}`}>
              {article.category.replace("-", " & ")}
            </span>
            <span className={`rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase ${LEVEL_STYLES[article.level] || LEVEL_STYLES.beginner}`}>
              {article.level}
            </span>
            <span className="flex items-center gap-1 text-[10px] font-mono text-text-light">
              <Clock size={10} /> {article.read_time_min} min read
            </span>
          </div>

          <h1 className="mt-4 text-2xl font-display font-black text-text-primary md:text-3xl">{article.title}</h1>
          <p className="mt-3 text-sm leading-7 text-text-muted md:text-base">{article.summary}</p>

          <div className="mt-6 space-y-6">
            {article.sections.map((section, i) => (
              <div key={i} className="rounded-2xl border border-white/5 bg-surface-card/10 p-5">
                <h2 className="flex items-center gap-2 font-display font-bold text-brand-sky">
                  <span className="text-xs font-mono text-text-light">{String(i + 1).padStart(2, "0")}</span>
                  {section.heading}
                </h2>
                <p className="mt-3 text-sm leading-7 text-text-secondary">{section.body}</p>

                {section.code && (
                  <pre className="mt-4 overflow-x-auto rounded-xl border border-brand-primary/10 bg-surface-card/50 p-4 text-xs leading-6 text-brand-primary">
                    <code>{section.code}</code>
                  </pre>
                )}

                {section.pro_tip && (
                  <div className="mt-4 flex items-start gap-2 rounded-xl border border-brand-gold/20 bg-brand-gold/5 p-3">
                    <Sparkles size={14} className="mt-0.5 shrink-0 text-brand-gold" />
                    <p className="text-xs leading-6 text-brand-gold-pale">{section.pro_tip}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-6 rounded-2xl border border-brand-teal/20 bg-brand-teal/5 p-5">
            <h3 className="flex items-center gap-2 text-sm font-display font-bold text-brand-teal">
              <BookOpen size={14} /> Key takeaways
            </h3>
            <ul className="mt-3 space-y-2">
              {article.key_takeaways.map((tip, i) => (
                <li key={i} className="flex items-start gap-2 text-sm leading-6 text-text-secondary">
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-teal" />
                  {tip}
                </li>
              ))}
            </ul>
          </div>

          <QuizBlock quiz={article.quiz} />
          <ExerciseBlock exercise={article.exercise} />
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default function StudyLibrary() {
  const [categories, setCategories] = useState([]);
  const [articles, setArticles] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [openArticle, setOpenArticle] = useState(null);
  const [articleDetail, setArticleDetail] = useState(null);
  const [searchParams] = useSearchParams();

  const loadArticles = useCallback((category, q) => {
    setLoading(true);
    studyApi
      .getArticles({ category, q })
      .then(d => setArticles(d.articles || []))
      .catch(() => setArticles([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    studyApi
      .getCategories()
      .then(d => setCategories(d.categories || []))
      .catch(() => {});
    loadArticles(null, "");

    const deepLinkId = searchParams.get("article");
    if (deepLinkId) openArticleDetail(deepLinkId);
  }, [loadArticles, searchParams]);

  const selectCategory = catId => {
    const next = activeCategory === catId ? null : catId;
    setActiveCategory(next);
    loadArticles(next, query);
  };

  const handleSearch = e => {
    const q = e.target.value;
    setQuery(q);
    loadArticles(activeCategory, q);
  };

  const openArticleDetail = id => {
    studyApi
      .getArticle(id)
      .then(d => {
        setArticleDetail(d.article);
        setOpenArticle(id);
      })
      .catch(() => {});
  };

  return (
    <div className="relative min-h-screen px-4 py-6 md:py-8">
      <ArcadeBackdrop variant="arcade" />
      <div className="relative z-10 mx-auto max-w-7xl space-y-6">
        <motion.section initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="hero-shell p-6 md:p-8 text-text-primary">
          <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <span className="section-kicker border-brand-primary/10 bg-white border-border/10 text-text-primary">
                <Compass size={12} />
                Study library
              </span>
              <h1 className="mt-4 text-3xl font-black tracking-tight text-text-primary md:text-5xl">
                In-depth guides that go beyond the tutorials
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-200 md:text-base">
                W3Schools-depth study articles for every track in the Learning Hub — theory, analogies,
                real code, common mistakes, and takeaways. Learn the why, not just the syntax.
              </p>
            </div>

            <div className="w-full max-w-sm">
              <div className="relative">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-light" />
                <input
                  value={query}
                  onChange={handleSearch}
                  placeholder="Search topics — 'closures', 'joins', 'grid'..."
                  className="w-full rounded-xl border border-white/15 bg-white border-border shadow-card py-3 pl-10 pr-4 text-sm text-text-primary placeholder:text-slate-400 focus:border-cyber-blue focus:outline-none"
                />
              </div>
            </div>
          </div>
        </motion.section>

        <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="mb-4 flex items-center gap-2">
            <BookOpen size={18} className="text-cyber-purple" />
            <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Categories</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            <CategoryPill
              categoryId={null}
              name="All"
              icon="🧺"
              color="#fff"
              active={!activeCategory}
              onClick={() => selectCategory(null)}
            />
            {categories.map(cat => (
              <CategoryPill
                key={cat.id}
                categoryId={cat.id}
                name={cat.name}
                icon={cat.icon}
                color={cat.color}
                active={activeCategory === cat.id}
                onClick={() => selectCategory(cat.id)}
              />
            ))}
          </div>
        </motion.section>

        <section>
          {loading ? (
            <div className="flex min-h-[240px] items-center justify-center">
              <Spinner />
            </div>
          ) : articles.length === 0 ? (
            <div className="arena-card flex min-h-[240px] flex-col items-center justify-center gap-3 p-6 text-center">
              <Search size={20} className="text-text-light" />
              <p className="text-sm text-text-muted">No articles found for this filter.</p>
              <button
                onClick={() => { setQuery(""); setActiveCategory(null); loadArticles(null, ""); }}
                className="btn-primary px-4 py-2 text-sm"
              >
                Clear filters
              </button>
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {articles.map((article, i) => (
                <motion.div
                  key={article.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.04 }}
                >
                  <ArticleCard article={article} onOpen={openArticleDetail} />
                </motion.div>
              ))}
            </div>
          )}
        </section>
      </div>

      <AnimatePresence>
        {openArticle && articleDetail && (
          <ArticleModal article={articleDetail} onClose={() => setOpenArticle(null)} />
        )}
      </AnimatePresence>

      <div className="mx-auto max-w-7xl px-4 pb-8">
        <Link to="/learn" className="inline-flex items-center gap-2 text-xs font-mono text-cyber-blue">
          <ArrowLeft size={12} /> Back to Learning Hub
        </Link>
      </div>
    </div>
  );
}
