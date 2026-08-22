import { useState, useEffect, useParams, useNavigate } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { BookOpen, Flag, Zap, Star, Target, Shield, Check, X, Clock, Code2, Palette, Globe, MapPin, Users, Calendar, } from "lucide-react";
import { useToast } from "../components/Toast";
import api from "../services/api";
import { useGamificationData } from "../hooks/useGamificationData";
import PracticeConsole from "../components/learning/PracticeConsole";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import useAuthStore from "../store/authStore";

const LANGUAGES = [
  { id: "c", name: "C", icon: "🔷", color: "#737373", description: "Systems programming, embedded, OS development" },
  { id: "python", name: "Python", icon: "🐍", color: "#3776AB", description: "Web, Data Science, AI/ML, Automation" },
  { id: "javascript", name: "JavaScript", icon: "🟨", color: "#F7DF1E", description: "Web frontend, Node.js, Mobile" },
  { id: "java", name: "Java", icon: "☕", color: "#D779A5", description: "Enterprise, Android, Web backend" },
  { id: "go", name: "Go", icon: "🟢", color: "#00ADD8", description: "Cloud, backend, microservices" },
  { id: "rust", name: "Rust", icon: "🦀", color: "#DEA584", description: "Systems, WebAssembly, performance-critical" },
  { id: "cpp", name: "C++", icon: "⚡", color: "#FF6B6B", description: "Systems, game dev, high performance" },
];

const LEVELS = [
  { id: "1", name: "Level 1: Foundations", emoji: "1️⃣", color: "#3B82F6", xp: 100 },
  { id: "2", name: "Level 2: Basics", emoji: "2️⃣", color: "#10B981", xp: 120 },
  { id: "3", name: "Level 3: Intermediate", emoji: "3️⃣", color: "#F59E0B", xp: 150 },
  { id: "4", name: "Level 4: Advanced", emoji: "4️⃣", color: "#EF4444", xp: 180 },
  { id: "5", name: "Level 5: Mastery", emoji: "5️⃣", color: "#EC4899", xp: 200 },
];

// C language boilerplates indexed by lesson number
const C_BOILERPLATES: Record<string, string> = {
  "1": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
  "2": "// Fibonacci sequence in C\n#include <stdio.h>\n\nint main() {\n    int n, a = 0, b = 1, next;\n    printf(\"Enter number of terms: \");\n    scanf(\"%d\", &n);\n    for (int i = 0; i < n; i++) {\n        printf(\"%d \", a);\n        next = a + b;\n        a = b;\n        b = next;\n    }\n    return 0;\n}",
  "3": "// Even or odd checker in C\n#include <stdio.h>\n\nint main() {\n    int n;\n    printf(\"Enter a number: \");\n    scanf(\"%d\", &n);\n    if (n % 2 == 0)\n        printf(\"Even\\n\");\n    else\n        printf(\"Odd\\n\");\n    return 0;\n}",
  "4": "// Simple calculator in C\n#include <stdio.h>\n\nint main() {\n    int a, b;\n    char op;\n    printf(\"Enter expression (e.g. 5 + 3): \");\n    scanf(\"%d %c %d\", &a, &op, &b);\n    switch (op) {\n        case '+': printf(\"%d + %d = %d\\n\", a, b, a + b); break;\n        case '-': printf(\"%d - %d = %d\\n\", a, b, a - b); break;\n        case '*': printf(\"%d * %d = %d\\n\", a, b, a * b); break;\n        case '/': if (b != 0) printf(\"%d / %d = %.2f\\n\", a, b, (double)a / b); else printf(\"Error: Division by zero\\n\"); break;\n    }\n    return 0;\n}",
  "5": "// Prime number checker in C\n#include <stdio.h>\n#include <math.h>\n\nint main() {\n    int n, i, isPrime = 1;\n    printf(\"Enter a number: \");\n    scanf(\"%d\", &n);\n    if (n <= 1) isPrime = 0;\n    for (i = 2; i <= sqrt(n); i++)\n        if (n % i == 0) isPrime = 0;\n    isPrime ? printf(\"Prime\\n\") : printf(\"Not prime\\n\");\n    return 0;\n}",
};

export default function LanguageLearning() {
  const { languageId } = useParams();
  const [activeLanguage, setActiveLanguage] = useState(languageId || "c");
  const [currentLevel, setCurrentLevel] = useState("1");
  const [showCreatePath, setShowCreatePath] = useState(false);
  const [showLessonModal, setShowLessonModal] = useState(false);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [lessonContent, setLessonContent] = useState({ code: "", language: activeLanguage, title: "" });
  const [progress, setProgress] = useState({ completed: 0, total: 80, xp: 0, level: "1" });
  const [streak, setStreak] = useState({ days: 0, bonus: "0%" });
  const [dailyGoal, setDailyGoal] = useState({ target: 1, completed: 0 });
  const { user } = useAuthStore();
  const { xp, streak: gamestreak, coins } = useGamificationData();
  const toast = useToast();

  const language = LANGUAGES.find(l => l.id === activeLanguage) || LANGUAGES[0];
  const level = LEVELS.find(l => l.id === currentLevel) || LEVELS[0];

  useEffect(() => {
    api.get(`/api/v1/languages/${activeLanguage}`).then((d: any) => {
      setProgress({ completed: d.completed || 0, total: d.total || 80, xp: d.xp || 0, level: d.level || "1" });
    }).catch(() => setProgress({ completed: 0, total: 80, xp: 0, level: "1" }));
  }, [activeLanguage]);

  const handleCompleteLesson = async (lessonId: string) => {
    try {
      const res = await api.post(`/api/v1/languages/${activeLanguage}/modules/${lessonId}/complete`);
      setProgress(prev => ({
        completed: Math.min(prev.completed + 1, progress.total),
        total: progress.total,
        xp: prev.xp + (res?.xp_gained || 10),
        level: res?.level || prev.level,
      }));
      if (toast) toast.success(`+${res?.xp_gained || 10} XP — ${language.name} progress ${res?.new_level_unlocked ? "leveled up!" : "kept going"}`);
    } catch { toast.error("Failed to complete lesson"); }
  };

  const handleSetLanguage = (id: string) => {
    setActiveLanguage(id);
    setCurrentLevel("1");
    setProgress({ completed: 0, total: 80, xp: 0, level: "1" });
    setShowCreatePath(false);
    navigate(`/learn/${id}`);
  };

  const handleStartLevel = () => {
    // Load boilerplate for current language and level
    const boilerplate = C_BOILERPLATES[currentLevel] || "// Write your code here";
    setLessonContent({ code: boilerplate, language: activeLanguage, title: `Lesson ${currentLevel}` });
    setShowLessonModal(true);
  };

  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0a0f16] via-[#111827] to-[#1a233b] text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">

        {/* Language Selector Header */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
            <h1 className="text-2xl font-bold font-display bg-gradient-to-r from-[#737373] to-[#D4C1FF] bg-clip-text text-transparent">
              Language Learning Hub
            </h1>
            <div className="flex gap-2">
              {LANGUAGES.map((lang) => (
                <button
                  key={lang.id}
                  onClick={() => handleSetLanguage(lang.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-mono transition-all ${
                    activeLanguage === lang.id
                      ? 'bg-white/20 text-white border border-white/30'
                      : 'text-gray-400 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span className="text-xl">{lang.icon}</span>
                  <span className="font-medium">{lang.name}</span>
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Language Cards Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {LANGUAGES.map((lang) => (
            <motion.div
              key={lang.id}
              initial={{ opacity: 0, scale: 0.9, x: -10 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.9, x: -10 }}
              className={`rounded-2xl border transition-all ${
                activeLanguage === lang.id
                  ? 'border-white/20 text-white border border-white/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/10'
              }`}>
              <div className="p-4 text-center">
                <span className="text-3xl">{lang.icon}</span>
                <h3 className="mt-2 text-lg font-medium text-white">{lang.name}</h3>
                <p className="text-xs text-gray-400 mt-1 line-clamp-2">{lang.description}</p>
                <div className="mt-2">
                  <span className="text-xs text-gray-500">Levels</span>
                  <span className="text-sm font-medium text-white">{progress.total}/80</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Current Learning Area */}
        <div className="bg-white/5 backdrop-blur rounded-2xl p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold"> {language.name} — {level.emoji} {level.name}</h2>
              <p className="text-sm text-gray-400">Systems: {language.color === '#737373' ? 'Embedded/OS' : language.color === '#3776AB' ? 'AI/Data' : language.color === '#F7DF1E' ? 'Web' : 'Enterprise/Cloud'}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs text-gray-400">XP</span>
              <span className="font-mono font-bold text-[14px]">{progress.xp.toLocaleString()}</span>
              <span className="text-gray-400">/ {progress.xp + 500} </span>
            </div>
          </div>
          <div className="h-4 rounded-full bg-white/10 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-[color] to-[color2] rounded-full transition-all"
              style={{
                width: `${Math.min((progress.completed / progress.total) * 100, 100)}%`,
                background: language.color === '#737373' ? 'linear-gradient(90deg, #737373, #D4C1FF)' : language.color === '#3776AB' ? 'linear-gradient(90deg, #3776AB, #60A5FA)' : language.color === '#F7DF1E' ? 'linear-gradient(90deg, #F7DF1E, #FBBF24)' : language.color === '#D779A5' ? 'linear-gradient(90deg, #D779A5, #F97316)' : language.color === '#00ADD8' ? 'linear-gradient(90deg, #00ADD8, #67E8F9)' : language.color === '#DEA584' ? 'linear-gradient(90deg, #DEA584, #FCD34D)' : 'linear-gradient(90deg, #FF6B6B, #EDGE1C)',
              }}
            />
          </div>
          <div className="flex justify-between text-xs text-gray-400">
            <span>{progress.completed}/{progress.total} modules</span>
            <span>{progress.level}</span>
          </div>
        </div>

        {/* Practice Console with lesson */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-6">
          <ArcadeBackdrop className="h-48 rounded-t-xl">
            <div className="flex items-end justify-between p-4">
              <div>
                <h3 className="font-medium text-white">{lessonContent.title}</h3>
                <p className="text-xs text-gray-400">{language.name} — {level.name}</p>
              </div>
              <button onClick={() => setShowLessonModal(false)} className="p-2 rounded-lg text-gray-400 hover:text-white transition-all">
                <X size={18} />
              </button>
            </div>
          </ArcadeBackdrop>
          <PracticeConsole
            language={activeLanguage}
            initialCode={lessonContent.code}
            onCodeChange={(code: string) => setLessonContent(prev => ({ ...prev, code }))}
            onRun={() => toast.info("Running code...")}
            onExecute={(code: string) => {
              api.post('/api/compiler/execute', { code, language: activeLanguage }).then((d: any) => {
                setLessonContent(prev => ({ ...prev, code: d?.output || d?.error || code }));
              }).catch(() => setLessonContent(prev => ({ ...prev, code: "// Execution failed" })));
            }}
            onComplete={() => {
              handleCompleteLesson(currentLevel);
              setShowLessonModal(false);
              setShowLessonModal(true);
            }}
          />
        </motion.div>

        {/* Lesson Roadmap */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
          {["Variables & Types", "Control Flow", "Functions", "Pointers & Memory", "Structures & Files", "Projects"].map((topic, i) => (
            <motion.div
              key={topic}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-xl border p-3 text-center transition-all ${
                progress.completed > i ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-white/5 bg-white/0'
              }">
                <span className="text-xl mb-1">{i < 3 ? "1️⃣" : i < 6 ? "2️⃣" : "3️⃣"}</span>
                <p className="text-xs text-gray-400 line-clamp-1">{topic}</p>
                <span className="text-[10px] font-mono text-gray-500">{progress.completed > i ? "✓" : ""}</span>
              </motion.div>
            ))}
        </div>

        {/* Daily Goal & Streak */}
        <div className="grid grid-cols-2 gap-3 mb-8">
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-widest">Daily Goal</p>
            <div className="mt-2 h-2 rounded-full bg-white/10 overflow-hidden">
              <div className="h-full rounded-full bg-emerald-500 transition-all" style={{ width: `${dailyGoal.completed / dailyGoal.target * 100}%` }} />
            </div>
            <p className="text-xs text-white mt-1">{dailyGoal.completed}/{dailyGoal.target} lessons</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-widest">Streak</p>
            <div className="mt-2 flex items-center gap-2">
              <span className="text-xl">{streak.days}d</span>
              <span className="text-[8px] text-gray-400">{streak.bonus} bonus XP</span>
            </div>
          </div>
        </div>

        {/* C-Specific Section */}
        {activeLanguage === "c" && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-8 p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur">
            <h3 className="text-lg font-bold mb-3">🎯 C Programming — Free Trial</h3>
            <p className="text-gray-400 mb-4">
              Write your first C program and run it in under 30 seconds. No setup required.
            </p>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => {
                  setLessonContent({ code: C_BOILERPLATES["1"], language: "c", title: "Hello World" });
                  setShowLessonModal(true);
                }}
                className="rounded-lg bg-emerald-500/20 border border-emerald-500/30 px-4 py-3 text-sm font-mono text-emerald-400 hover:bg-emerald-500/30 transition-all"
              >
                Hello World Program
              </button>
              <button
                onClick={() => {
                  setLessonContent({ code: C_BOILERPLATES["2"], language: "c", title: "Fibonacci" });
                  setShowLessonModal(true);
                }}
                className="rounded-lg bg-emerald-500/20 border border-emerald-500/30 px-4 py-3 text-sm font-mono text-emerald-400 hover:bg-emerald-500/30 transition-all"
              >
                Fibonacci Sequence
              </button>
            </div>
          </motion.div>
        )}

        {/* Continue Learning CTA */}
        <motion.div className="mt-8 pt-8 border-t border-white/10">
          <div className="flex items-center gap-3">
            <Flag size={14} className="text-yellow-400" />
            <div>
              <p className="font-medium text-white">Keep Learning</p>
              <p className="text-xs text-gray-400">Maintain your streak for multiplier bonuses</p>
            </div>
          </div>
          <button
            onClick={() => navigate(`/learn/${activeLanguage}`)}
            className="mt-3 px-6 py-3 rounded-xl bg-emerald-600/20 text-emerald-400 font-mono text-sm hover:bg-emerald-600/30 transition-all"
          >
            Continue {language.name} Learning
          </button>
        </motion.div>
      </div>
    </div>
  );
}