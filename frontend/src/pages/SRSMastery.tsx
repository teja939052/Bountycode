import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import { Brain, Clock, CheckCircle, XCircle, AlertTriangle, Sparkles, Zap, BookOpen, TrendingUp, Target } from "lucide-react";

const MASTERY_COLORS = {
  new: "text-text-muted bg-surface-card border-nature-leaf/20",
  learning: "text-cyber-blue bg-cyber-blue/10 border-cyber-blue/20",
  young: "text-cyber-yellow bg-cyber-yellow/10 border-cyber-yellow/20",
  maturing: "text-cyber-green bg-cyber-green/10 border-cyber-green/20",
  mature: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20",
  mastered: "text-cyber-purple bg-cyber-purple/10 border-cyber-purple/20",
};

const MASTERY_LABELS = {
  new: "New",
  learning: "Learning",
  young: "Young",
  maturing: "Maturing",
  mature: "Mature",
  mastered: "Mastered",
};

const GRADE_BUTTONS = [
  { grade: 0, label: "Again", desc: "Complete blackout", color: "bg-red-500/10 border-red-500/20 text-red-400 hover:bg-red-500/20", icon: XCircle },
  { grade: 1, label: "Hard", desc: "Struggled but got it", color: "bg-orange-500/10 border-orange-500/20 text-orange-400 hover:bg-orange-500/20", icon: AlertTriangle },
  { grade: 2, label: "Good", desc: "Correct with effort", color: "bg-cyber-blue/10 border-cyber-blue/20 text-cyber-blue hover:bg-cyber-blue/20", icon: CheckCircle },
  { grade: 3, label: "Easy", desc: "Instant recall", color: "bg-cyber-green/10 border-cyber-green/20 text-cyber-green hover:bg-cyber-green/20", icon: Sparkles },
];

const TOPIC_ICONS = {
  "Arrays & Strings": "📊",
  "Linked Lists": "🔗",
  "Stacks & Queues": "📚",
  "Trees & BST": "🌳",
  "Graphs": "🕸️",
  "Dynamic Programming": "⚡",
  "Heaps & Priority Queues": "🏔️",
  "Tries": "🌲",
  "Backtracking": "🔄",
  "Bit Manipulation": "🔢",
  "Math & Geometry": "📐",
};

export default function SRSMastery() {
  const user = useAuthStore((s) => s.user);
  const [topics, setTopics] = useState([]);
  const [stats, setStats] = useState(null);
  const [dueCards, setDueCards] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedConcept, setSelectedConcept] = useState(null);
  const [reviewing, setReviewing] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [error, setError] = useState("");

  const loadAll = useCallback(async () => {
    setLoading(true);
    try {
      const [topicsRes, statsRes, dueRes, forecastRes] = await Promise.all([
        api.getSRSConcepts().catch(() => ({ topics: [] })),
        api.getSRSStats().catch(() => ({})),
        api.getDueSRSCards(20).catch(() => ({ cards: [] })),
        api.getSRSForecast(30).catch(() => ({ forecast: [] })),
      ]);
      setTopics(topicsRes.topics || []);
      setStats(statsRes);
      setDueCards(dueRes.cards || []);
      setForecast(forecastRes.forecast || []);
    } catch (e) {
      setError(e.message || "Failed to load SRS data");
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleInitialize = async () => {
    setLoading(true);
    try {
      await api.initializeSRS({});
      await loadAll();
    } catch (e) {
      setError(e.message || "Failed to initialize SRS");
    }
    setLoading(false);
  };

  const handleReview = async (conceptId, grade) => {
    setReviewing(true);
    try {
      const result = await api.reviewSRSConcept(conceptId, grade);
      if (result.new_interval >= 365) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 2000);
      }
      await loadAll();
    } catch (e) {
      setError(e.message || "Review failed");
    }
    setReviewing(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-base">
        <Spinner size="lg" />
      </div>
    );
  }

  const totalConcepts = topics.reduce((sum, t) => sum + t.subtopics.length, 0);
  const masteredCount = topics.reduce((sum, t) => sum + t.subtopics.filter(s => s.mastery === "mastered").length, 0);
  const learningCount = topics.reduce((sum, t) => sum + t.subtopics.filter(s => s.mastery === "learning").length, 0);
  const newCount = topics.reduce((sum, t) => sum + t.subtopics.filter(s => s.mastery === "new").length, 0);

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <CelebrationOverlay show={showCelebration} type="perfect" title="Concept Mastered!" onClose={() => setShowCelebration(false)} />
      
      <nav className="sticky top-0 z-50 border-b border-nature-leaf/20 bg-white/90">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="text-cyber-purple" size={24} />
              <div>
                <h1 className="font-display font-bold text-xl">DSA Mastery</h1>
                <p className="text-[10px] font-mono text-text-muted">Spaced Repetition Engine</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {stats?.due_now > 0 && (
                <span className="px-3 py-1 bg-cyber-red/10 border border-cyber-red/20 text-cyber-red text-xs font-mono rounded-full">
                  {stats.due_now} Due Now
                </span>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <motion.div className="mb-6 p-4 bg-cyber-red/10 border border-cyber-red/20 text-cyber-red rounded-xl" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
            {error}
          </motion.div>
        )}

        {/* Stats Overview */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard icon={Brain} label="Total Concepts" value={totalConcepts} color="text-cyber-purple" />
          <StatCard icon={CheckCircle} label="Mastered" value={masteredCount} color="text-cyber-green" />
          <StatCard icon={BookOpen} label="Learning" value={learningCount} color="text-cyber-blue" />
          <StatCard icon={Sparkles} label="New" value={newCount} color="text-cyber-yellow" />
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-[#EDEAE0]">
          {[
            { id: "overview", label: "Overview", icon: TrendingUp },
            { id: "due", label: `Due (${dueCards.length})`, icon: Clock },
            { id: "tree", label: "Concept Tree", icon: BookOpen },
            { id: "forecast", label: "30-Day Forecast", icon: Target },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 text-sm font-mono transition-colors flex items-center gap-2 ${
                activeTab === tab.id
                  ? "text-cyber-purple border-b-2 border-cyber-purple"
                  : "text-text-muted hover:text-text-secondary"
              }`}
            >
              <tab.icon size={14} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === "overview" && (
            <OverviewTab stats={stats} dueCards={dueCards} topics={topics} forecast={forecast} onReview={handleReview} reviewing={reviewing} />
          )}
          {activeTab === "due" && (
            <DueTab cards={dueCards} onReview={handleReview} reviewing={reviewing} />
          )}
          {activeTab === "tree" && (
            <TreeTab topics={topics} onReview={handleReview} reviewing={reviewing} />
          )}
          {activeTab === "forecast" && (
            <ForecastTab forecast={forecast} />
          )}
        </AnimatePresence>

        {/* Initialize button for new users */}
        {!topics.length && (
          <div className="text-center py-12">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card max-w-md mx-auto"
            >
              <Brain className="text-cyber-purple mx-auto mb-4" size={48} />
              <h3 className="font-display font-bold text-xl mb-2">Initialize Spaced Repetition</h3>
              <p className="text-text-muted text-sm mb-6">
                Set up your DSA mastery tracking with {get_all_concept_ids().length} concepts across 11 topics.
                The SM-2 algorithm will schedule optimal reviews for long-term retention.
              </p>
              <button onClick={handleInitialize} disabled={loading} className="btn-primary w-full">
                {loading ? <Spinner size="sm" className="text-space-void" /> : "Initialize My SRS"}
              </button>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }: {
  icon: any;
  label: string;
  value: string | number;
  color: string;
}) {
  return (
    <motion.div
      className="card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center gap-3 mb-2">
        <Icon className={`${color}`} size={24} />
        <span className="text-xs font-mono text-text-muted uppercase tracking-wider">{label}</span>
      </div>
      <div className="font-display font-bold text-3xl">{value}</div>
    </motion.div>
  );
}

function OverviewTab({ stats, dueCards, topics, forecast, onReview, reviewing }: {
  stats: any;
  dueCards: any[];
  topics: any[];
  forecast: any[];
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  if (!stats) return <div className="text-center py-12 text-text-muted">Loading stats...</div>;

  const retention = stats.retention_rate || 100;
  const avgEase = stats.avg_ease_factor || 2.5;

  return (
    <div className="space-y-6">
      {/* Retention & Ease */}
      <div className="grid sm:grid-cols-2 gap-4">
        <motion.div className="card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="text-cyber-green" size={24} />
            <span className="text-xs font-mono text-text-muted uppercase tracking-wider">Retention Rate</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-display font-bold text-4xl">{retention}%</span>
            <span className="text-xs font-mono text-text-muted">Target: {'>'}90%</span>
          </div>
          <div className="mt-2 h-2 bg-[#E5E0D3] rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-cyber-green to-cyber-blue rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${retention}%` }}
              transition={{ duration: 1 }}
            />
          </div>
        </motion.div>

        <motion.div className="card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <div className="flex items-center gap-3 mb-2">
            <Target className="text-cyber-blue" size={24} />
            <span className="text-xs font-mono text-text-muted uppercase tracking-wider">Avg Ease Factor</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-display font-bold text-4xl">{avgEase}</span>
            <span className="text-xs font-mono text-text-muted">Range: 1.3 - 3.0</span>
          </div>
          <div className="mt-2 h-2 bg-[#E5E0D3] rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-cyber-blue to-cyber-purple rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(100, (avgEase - 1.3) / 1.7 * 100)}%` }}
              transition={{ duration: 1 }}
            />
          </div>
        </motion.div>
      </div>

      {/* Topic Breakdown */}
      <motion.div className="card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h3 className="font-bold mb-4 flex items-center gap-2">
          <BookOpen size={20} className="text-cyber-purple" />
          Topic Breakdown
        </h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {Object.entries(stats.topic_breakdown || {}).map(([topic, data]: [string, any]) => (
            <div key={topic} className="p-4 bg-surface-base rounded-xl border border-nature-leaf/20">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-sm">{topic}</span>
                <span className="text-xs font-mono text-text-muted">{data.pct || 0}% mastered</span>
              </div>
              <div className="h-1.5 bg-[#E5E0D3] rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-cyber-purple to-cyber-blue rounded-full" style={{ width: `${data.pct || 0}%` }} />
              </div>
              <div className="flex justify-between text-[10px] font-mono text-text-muted mt-1">
                <span>🏆 {data.mastered || 0}</span>
                <span>📚 {data.learning || 0}</span>
                <span>✨ {data.new || 0}</span>
                <span>⏰ {data.due || 0} due</span>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Quick Actions */}
      <div className="grid sm:grid-cols-2 gap-4">
        <motion.button
          onClick={() => {}}
          className="card text-left hover:border-cyber-purple/30 transition-colors"
          whileHover={{ scale: 1.02 }}
        >
          <div className="flex items-center gap-3 mb-2">
            <Clock className="text-cyber-yellow" size={24} />
            <span className="text-xs font-mono text-text-muted uppercase tracking-wider">Due Now</span>
          </div>
          <div className="font-display font-bold text-3xl">{dueCards.length}</div>
          <p className="text-xs text-text-muted mt-1">concepts ready for review</p>
        </motion.button>

        <motion.button
          onClick={() => {}}
          className="card text-left hover:border-cyber-blue/30 transition-colors"
          whileHover={{ scale: 1.02 }}
        >
          <div className="flex items-center gap-3 mb-2">
            <Target className="text-cyber-blue" size={24} />
            <span className="text-xs font-mono text-text-muted uppercase tracking-wider">30-Day Forecast</span>
          </div>
          <div className="font-display font-bold text-3xl">{Array.from({length: 30}, (_, i) => i + 1).reduce((sum, d) => sum + (forecast.find(f => f.date === new Date(Date.now() + d * 86400000).toISOString().split('T')[0])?.reviews_due || 0), 0)}</div>
          <p className="text-xs text-text-muted mt-1">total reviews predicted</p>
        </motion.button>
      </div>
    </div>
  );
}

function DueTab({ cards, onReview, reviewing }: {
  cards: any[];
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  if (!cards.length) {
    return (
      <motion.div className="card text-center py-12" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <CheckCircle className="text-cyber-green mx-auto mb-4" size={48} />
        <h3 className="font-display font-bold text-xl mb-2">All Caught Up!</h3>
        <p className="text-text-muted">No concepts due for review right now. Check back later.</p>
      </motion.div>
    );
  }

  return (
    <div className="space-y-3">
      {cards.map((card, i) => (
        <DueCard key={card.concept_id} card={card} index={i} onReview={onReview} reviewing={reviewing} />
      ))}
    </div>
  );
}

function DueCard({ card, index, onReview, reviewing }: {
  card: any;
  index: number;
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  const overdue = card.overdue_days > 0;
  const masteryColor = MASTERY_COLORS[card.is_learning ? "learning" : "young"];

  return (
    <motion.div
      className={`card border-l-4 ${overdue ? "border-cyber-red/50" : "border-cyber-purple/30"}`}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-2">
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${masteryColor}`}>
              {MASTERY_LABELS[card.is_learning ? "learning" : "young"]}
            </span>
            <span className="text-[10px] font-mono text-text-muted">{card.topic}</span>
            {overdue && <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyber-red/10 text-cyber-red border border-cyber-red/20">{card.overdue_days}d overdue</span>}
          </div>
          <h4 className="font-display font-bold text-lg truncate">{card.subtopic}</h4>
          <div className="flex items-center gap-4 mt-2 text-[10px] font-mono text-text-muted">
            <span>Interval: {card.interval}d</span>
            <span>EF: {card.ease_factor}</span>
            <span>Reps: {card.repetitions}</span>
          </div>
        </div>
        <div className="flex gap-2 shrink-0">
          {GRADE_BUTTONS.map((g) => (
            <button
              key={g.grade}
              onClick={() => !reviewing && onReview(card.concept_id, g.grade)}
              disabled={reviewing}
              className={`px-3 py-2 rounded-lg text-xs font-mono transition-all flex items-center gap-1 ${g.color} disabled:opacity-50`}
              title={g.desc}
            >
              <g.icon size={12} />
              {g.label}
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function TreeTab({ topics, onReview, reviewing }: {
  topics: any[];
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  return (
    <div className="space-y-4">
      {topics.map((topic) => (
        <TopicAccordion key={topic.id} topic={topic} onReview={onReview} reviewing={reviewing} />
      ))}
    </div>
  );
}

function TopicAccordion({ topic, onReview, reviewing }: {
  topic: any;
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  const [open, setOpen] = useState(false);
  const icon = TOPIC_ICONS[topic.name] || "📁";
  const progress = topic.progress || { mastered: 0, learning: 0, new: 0, pct: 0 };

  return (
    <motion.div className="card" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-4 text-left"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <div>
            <h4 className="font-display font-bold">{topic.name}</h4>
            <p className="text-xs font-mono text-text-muted">{topic.subtopics.length} concepts • {progress.pct}% mastered</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="h-4 w-32 bg-[#E5E0D3] rounded-full overflow-hidden flex-1 max-w-xs">
            <div className="h-full bg-gradient-to-r from-cyber-purple to-cyber-blue rounded-full" style={{ width: `${progress.pct}%` }} />
          </div>
          <span className="text-sm font-mono font-bold text-cyber-purple">{progress.pct}%</span>
        </div>
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-[#EDEAE0] p-4"
          >
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {topic.subtopics.map((sub) => (
                <SubtopicCard key={sub.id} sub={sub} onReview={onReview} reviewing={reviewing} />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function SubtopicCard({ sub, onReview, reviewing }: {
  sub: any;
  onReview: (conceptId: string, grade: number) => void;
  reviewing: boolean;
}) {
  const masteryColor = MASTERY_COLORS[sub.mastery] || MASTERY_COLORS.new;

  return (
    <motion.div
      className={`card ${sub.is_due && !sub.is_learning ? "border-cyber-green/30" : ""}`}
      whileHover={{ scale: 1.01 }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono ${masteryColor}">
              {MASTERY_LABELS[sub.mastery] || sub.mastery}
            </span>
            {sub.is_due && !sub.is_learning && (
              <span className="px-1.5 py-0.5 rounded text-[9px] font-mono bg-cyber-green/10 text-cyber-green border border-cyber-green/20 animate-pulse">DUE</span>
            )}
          </div>
          <h5 className="font-medium text-sm truncate">{sub.name}</h5>
          <div className="flex items-center gap-3 mt-1 text-[10px] font-mono text-text-muted">
            <span>Interval: {sub.interval}d</span>
            <span>EF: {sub.ease_factor}</span>
            <span>Reps: {sub.repetitions}</span>
          </div>
        </div>
        <div className="flex gap-1 shrink-0">
          {GRADE_BUTTONS.map((g) => (
            <button
              key={g.grade}
              onClick={() => !reviewing && onReview(sub.id, g.grade)}
              disabled={reviewing}
              className={`px-2 py-1.5 rounded text-[10px] font-mono transition-all ${g.color} disabled:opacity-50`}
              title={g.desc}
            >
              <g.icon size={10} />
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function ForecastTab({ forecast }: { forecast: any[] }) {
  return (
    <div className="card">
      <h3 className="font-bold mb-4 flex items-center gap-2">
        <Target size={20} className="text-cyber-purple" />
        30-Day Review Forecast
      </h3>
      <div className="grid grid-cols-7 gap-1 text-center">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="text-[10px] font-mono text-text-muted py-2">{d}</div>
        ))}
        {Array.from({ length: 42 }, (_, i) => {
          const date = new Date();
          date.setDate(date.getDate() - date.getDay() + i);
          const dateStr = date.toISOString().split('T')[0];
          const dayForecast = forecast.find(f => f.date === dateStr);
          const count = dayForecast?.reviews_due || 0;
          const isPast = date < new Date();
          const isToday = dateStr === new Date().toISOString().split('T')[0];
          
          return (
            <motion.div
              key={dateStr}
              className={`aspect-square flex flex-col items-center justify-center rounded-xl text-xs font-mono transition-all ${
                isPast ? "text-text-muted bg-surface-card" : 
                count > 10 ? "bg-cyber-red/20 text-cyber-red" :
                count > 5 ? "bg-cyber-yellow/20 text-cyber-yellow" :
                count > 0 ? "bg-cyber-green/20 text-cyber-green" :
                "bg-surface-card text-text-muted"
              } ${isToday ? "ring-2 ring-cyber-purple" : ""}`}
              whileHover={{ scale: 1.1 }}
            >
              <span className="font-medium">{date.getDate()}</span>
              {count > 0 && <span className="text-[10px] font-mono">{count}</span>}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// Helper to get concept IDs (mirrors backend)
function get_all_concept_ids() {
  const DSA_CONCEPTS = {
    arrays: ["two-pointers", "sliding-window", "prefix-sum", "kadane", "dutch-flag", "binary-search-array", "rotate", "merge-intervals"],
    "linked-lists": ["reverse", "cycle-detection", "merge-two-lists", "palindrome", "intersection", "remove-nth-from-end", "copy-random-pointer"],
    "stacks-queues": ["valid-parentheses", "min-stack", "eval-rpn", "daily-temperatures", "largest-rectangle", "sliding-window-max", "queue-using-stacks"],
    trees: ["traversals", "max-depth", "validate-bst", "lowest-common-ancestor", "serialize-deserialize", "path-sum", "diameter", "bst-from-preorder"],
    graphs: ["bfs-dfs", "topological-sort", "dijkstra", "bellman-ford", "union-find", "mst-kruskal", "mst-prim", "strongly-connected", "bipartite", "cycle-detection", "shortest-path"],
    "dynamic-programming": ["fibonacci", "climbing-stairs", "coin-change", "knapsack-01", "lcs", "lis", "edit-distance", "house-robber", "max-subarray", "partition-equal-subset", "word-break", "dp-on-trees"],
    heaps: ["kth-largest", "merge-k-lists", "top-k-frequent", "median-stream", "task-scheduler", "reorganize-string"],
    tries: ["implement-trie", "word-search-ii", "autocomplete", "max-xor"],
    backtracking: ["subsets", "permutations", "combinations", "combination-sum", "palindrome-partition", "n-queens", "sudoku-solver"],
    "bit-manipulation": ["single-number", "hamming-weight", "counting-bits", "power-of-two", "missing-number", "single-number-ii", "bitwise-and-range"],
    "math-geometry": ["gcd-lcm", "modular-arithmetic", "sieve", "prime-factorization", "combinatorics", "probability", "coordinate-geometry"],
  };
  return Object.entries(DSA_CONCEPTS).flatMap(([topic, subs]) => subs.map(s => `${topic}:${s}`));
}
