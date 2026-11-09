"use client";

import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  ArrowLeft,
  Flame,
  Zap,
  Crown,
  Play,
  RefreshCw,
  Settings,
} from "lucide-react";
import {
  StreakDisplay,
  XPLevelBar,
  HeartsDisplay,
  LessonCard,
  CelebrationModal,
  LessonToast,
  Button,
  Card,
  PageShell,
} from "../components/design-system";

// Mock curriculum data — in production this comes from /api/v1/curriculum
// For now, we simulate the structure from the backend curriculum module
const MOCK_CURRICULUM: Record<string, any> = {
  python: {
    id: "python",
    name: "Python",
    icon: "🐍",
    color: "#22C55E",
    description: "The most popular language for AI, web, and data science",
    total_lessons: 198,
    levels: {
      l01: {
        id: "l01",
        name: "First Steps",
        emoji: "🌱",
        color: "#22C55E",
        description: "Hello World & basic output",
        order: 1,
        difficulty: 1,
        total_xp: 85,
        lessons: [
          {
            title: "Hello World in Python",
            type: "practice",
            diamonds: 10,
            difficulty: 1,
            concept: "output",
            why: "Computers do nothing unless you tell them to — output is the first conversation between human and machine.",
            real_world: "Every CLI tool, web server, and mobile app starts by printing something to the screen.",
            interview: "Write a program that prints a formatted greeting with the user's name.",
            build: "A greeting card generator that takes user input and displays a personalized message.",
            problem_set: "Print numbers 1 to 100, each on a new line. Print them in reverse order too.",
            engineering: "stdout vs stderr, buffering, terminal encoding.",
            career: "Junior developer, QA engineer, technical support.",
          },
          {
            title: "print() Function",
            type: "theory",
            diamonds: 10,
            difficulty: 1,
            concept: "output",
            why: "print() is your first tool for talking to the computer.",
            real_world: "Debug output, logging, user-facing messages.",
            interview: "What's the difference between print() and return?",
            build: "A program that prints your name, age, and favorite language.",
            problem_set: "Print a multi-line poem using escape sequences.",
            engineering: "stdout buffering, end parameter, sep parameter.",
            career: "Every developer uses print for debugging.",
          },
          {
            title: "f-Strings & Formatting",
            type: "theory",
            diamonds: 10,
            difficulty: 1,
            concept: "output",
            why: "Clean string formatting makes output readable and professional.",
            real_world: "Formatted emails, reports, dashboard displays.",
            interview: "What's the advantage of f-strings over % formatting?",
            build: "A receipt formatter that shows item, qty, price, and total.",
            problem_set: "Format a user's full name, email, and phone into a contact card.",
            engineering: "String interpolation, locale-aware formatting.",
            career: "Backend (API responses), frontend (UI text), data (reports).",
          },
          {
            title: "Practice: Greeting Program",
            type: "practice",
            diamonds: 15,
            difficulty: 1,
            concept: "output",
            why: "Practice cements the concept — you learn by doing, not watching.",
            real_world: "User onboarding flows, welcome screens.",
            interview: "Write a program that asks for a name and prints a personalized greeting.",
            build: "A greeting card generator that takes user input and displays a personalized message.",
            problem_set: "Ask for two numbers and print their sum in a sentence.",
            engineering: "input() function, string concatenation vs interpolation.",
            career: "Frontend (form handling), backend (request parameters).",
          },
          {
            title: "Challenge: ASCII Banner",
            type: "challenge",
            diamonds: 25,
            difficulty: 2,
            concept: "output",
            why: "Challenges push you to apply concepts under constraints.",
            real_world: "CLI tools, terminal dashboards, ASCII art generators.",
            interview: "Print a box of asterisks with a message centered inside.",
            build: "A CLI banner program that prints a styled welcome message with borders.",
            problem_set: "Print a diamond pattern of asterisks.",
            engineering: "String multiplication, center alignment, loop-based output.",
            career: "DevOps (CLI tools), backend (scripting), QA (test output).",
          },
          {
            title: "Project: Welcome CLI",
            type: "project",
            diamonds: 60,
            difficulty: 3,
            concept: "output",
            why: "Projects combine everything you've learned into something real.",
            real_world: "Developer tools, onboarding scripts, welcome emails.",
            interview: "Walk me through a project you built from scratch.",
            build: "A CLI greeting card generator that takes user input and displays a personalized message.",
            problem_set: "Add a --name flag and --color option to your CLI.",
            engineering: "CLI argument parsing, modular code structure, error handling.",
            career: "Junior developer, QA engineer, technical support.",
          },
        ],
      },
      l02: {
        id: "l02",
        name: "Variables",
        emoji: "📦",
        color: "#3B82F6",
        description: "Data types, constants, declarations",
        order: 2,
        difficulty: 1,
        total_xp: 100,
        lessons: [
          {
            title: "Dynamic Typing",
            type: "theory",
            diamonds: 10,
            difficulty: 1,
            concept: "variables",
            why: "Variables give names to values so you can reuse and reason about them.",
            real_world: "User profiles, shopping carts, game scores — all named values in memory.",
            interview: "What's the difference between declaration, initialization, and assignment?",
            build: "A variable-driven mad-libs story generator.",
            problem_set: "Declare variables for length and width, compute area and perimeter.",
            engineering: "Stack vs heap allocation, variable lifetime, naming conventions.",
            career: "Frontend, backend, full-stack — every role uses variables.",
          },
        ],
      },
    },
  },
};

interface LessonNodeProps {
  lesson: any;
  level: any;
  languageId: string;
  levelId: string;
  onLessonClick: (lesson: any) => void;
  completedLessons: Set<string>;
  currentLessonId?: string;
}

function LessonNode({
  lesson,
  level,
  languageId,
  levelId,
  onLessonClick,
  completedLessons,
  currentLessonId,
}: LessonNodeProps) {
  const isCompleted = completedLessons.has(lesson.title);
  const isCurrent = lesson.title === currentLessonId;
  const status: "locked" | "current" | "completed" = isCompleted
    ? "completed"
    : isCurrent
      ? "current"
      : "locked";

  const typeMap: Record<string, "theory" | "practice" | "challenge" | "project" | "boss" | "quiz"> = {
    theory: "theory",
    practice: "practice",
    challenge: "challenge",
    project: "project",
    boss: "boss",
    quiz: "quiz",
  };

  return (
    <LessonCard
      id={lesson.title}
      title={lesson.title}
      emoji={level.emoji || "📚"}
      description={lesson.why || lesson.interview}
      type={typeMap[lesson.type] || "theory"}
      diamonds={lesson.diamonds || 15}
      status={status}
      progress={isCompleted ? 100 : isCurrent ? 50 : 0}
      onClick={() => !status.includes("locked") && onLessonClick(lesson)}
      className="w-full"
    />
  );
}

export default function LearningHub() {
  const { languageId } = useParams<{ languageId: string }>();
  const navigate = useNavigate();
  const [language, setLanguage] = useState<any>(null);
  const [levels, setLevels] = useState<any[]>([]);
  const [currentLevelIndex, setCurrentLevelIndex] = useState(0);
  const [completedLessons, setCompletedLessons] = useState<Set<string>>(new Set());
  const [currentLesson, setCurrentLesson] = useState<any>(null);
  const [showLessonView, setShowLessonView] = useState(false);
  const [celebration, setCelebration] = useState<{
    title: string;
    subtitle?: string;
    emoji?: string;
    xpGained?: number;
    streakGained?: number;
  } | null>(null);
  const [toast, setToast] = useState<{
    isOpen: boolean;
    title: string;
    xpGained?: number;
    streak?: number;
  } | null>(null);
  const [streak, setStreak] = useState(5);
  const [xp, setXp] = useState(1240);
  const [levelNum, setLevelNum] = useState(7);
  const [hearts, setHearts] = useState(3);
  const [streakFreeze, setStreakFreeze] = useState(2);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!languageId) return;
    const lang = MOCK_CURRICULUM[languageId as keyof typeof MOCK_CURRICULUM];
    if (lang) {
      setLanguage(lang);
      const levelArray = Object.values(lang.levels).sort(
        (a: any, b: any) => a.order - b.order
      );
      setLevels(levelArray);
      const firstIncomplete = levelArray.findIndex(
        (l: any) =>
          l.lessons.some(
            (lesson: any) => !completedLessons.has(lesson.title)
          )
      );
      setCurrentLevelIndex(firstIncomplete === -1 ? levelArray.length - 1 : firstIncomplete);
    }
    setIsLoading(false);
  }, [languageId]);

  const handleLessonClick = (lesson: any) => {
    setCurrentLesson(lesson);
    setShowLessonView(true);
  };

  const handleLessonComplete = (xpGained: number = 15) => {
    if (currentLesson) {
      setCompletedLessons((prev) => new Set([...prev, currentLesson.title]));
    }
    setXp((prev) => prev + xpGained);
    setStreak((prev) => prev + 1);
    setToast({
      isOpen: true,
      title: "Lesson complete!",
      xpGained,
      streak: streak + 1,
    });

    if ((xp + xpGained) >= levelNum * 100) {
      setCelebration({
        title: "Level Up!",
        subtitle: `You've reached level ${levelNum + 1}`,
        emoji: "👑",
        xpGained,
        streakGained: 1,
      });
      setLevelNum((prev) => prev + 1);
    } else {
      setCelebration({
        title: "Great job!",
        subtitle: "You're making excellent progress",
        emoji: "✅",
        xpGained,
        streakGained: 1,
      });
    }
  };

  const handleCelebrationClose = () => {
    setCelebration(null);
  };

  const handleToastClose = () => {
    setToast(null);
  };

  const handleBackToPath = () => {
    setShowLessonView(false);
    setCurrentLesson(null);
  };

  if (isLoading || !language) {
    return (
      <PageShell theme="focus" className="max-w-4xl mx-auto py-20">
        <div className="flex items-center justify-center gap-2">
          <RefreshCw size={20} className="animate-spin" />
          <span className="text-text-muted">Loading your path…</span>
        </div>
      </PageShell>
    );
  }

  const currentLevel = levels[currentLevelIndex];
  const nextLockedLesson = currentLevel?.lessons.find(
    (l: any) => !completedLessons.has(l.title)
  );

  const completedCount = currentLevel.lessons.filter((l: any) =>
    completedLessons.has(l.title)
  ).length;
  const progressPercent = Math.round((completedCount / currentLevel.lessons.length) * 100);

  return (
    <PageShell theme="focus" className="max-w-5xl mx-auto">
      {/* Top Bar — Gamification */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Link to="/">
            <ArrowLeft size={20} className="text-text-muted" />
          </Link>
          <div className="flex flex-col">
            <h1 className="font-bold text-text-primary text-xl">{language.name}</h1>
            <p className="text-xs text-text-muted">{language.description}</p>
          </div>
        </div>

        <div className="flex items-center gap-4 flex-wrap">
          <StreakDisplay streak={streak} streakFreezeCount={streakFreeze} />
          <XPLevelBar xp={xp} level={levelNum} xpToNext={100} />
          <HeartsDisplay hearts={hearts} />
          <Button variant="outline" size="sm" onClick={() => navigate("/profile")}>
            <Settings size={16} className="mr-2" /> Profile
          </Button>
        </div>
      </div>

      {/* Celebration Modal */}
      <CelebrationModal
        isOpen={!!celebration}
        onClose={handleCelebrationClose}
        title={celebration?.title || ""}
        subtitle={celebration?.subtitle}
        emoji={celebration?.emoji}
        xpGained={celebration?.xpGained}
        streakGained={celebration?.streakGained}
      />

      {/* Lesson Toast */}
      <LessonToast
        isOpen={!!toast}
        onClose={handleToastClose}
        title={toast?.title || ""}
        xpGained={toast?.xpGained}
        streak={toast?.streak}
      />

      {/* Lesson View */}
      {showLessonView && currentLesson && (
        <div className="mt-6">
          <div className="flex items-center gap-3 mb-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleBackToPath}
              className="text-text-muted"
            >
              <ArrowLeft size={16} /> Back to path
            </Button>
            <h2 className="font-bold text-text-primary">{currentLesson.title}</h2>
            <span className="px-2 py-1 rounded bg-blue-50 text-blue-600 text-xs font-bold">
              {currentLevel.emoji} {currentLevel.name}
            </span>
          </div>

          <Card variant="dark" padding="lg" radius="lg" className="shadow-card-hover">
            <div className="space-y-6">
              <h3 className="font-bold text-text-primary text-lg">{currentLesson.title}</h3>

              <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
                <h4 className="font-bold text-blue-800 text-sm mb-2 flex items-center gap-2">
                  <Flame size={14} /> Why this matters
                </h4>
                <p className="text-blue-700 text-sm">{currentLesson.why}</p>
              </div>

              <div className="bg-green-50 border border-green-100 rounded-lg p-4">
                <h4 className="font-bold text-green-800 text-sm mb-2 flex items-center gap-2">
                  <Zap size={14} /> Real world
                </h4>
                <p className="text-green-700 text-sm">{currentLesson.real_world}</p>
              </div>

              <div className="bg-purple-50 border border-purple-100 rounded-lg p-4">
                <h4 className="font-bold text-purple-800 text-sm mb-2 flex items-center gap-2">
                  <Crown size={14} /> Interview prep
                </h4>
                <p className="text-purple-700 text-sm">{currentLesson.interview}</p>
              </div>

              <div className="bg-orange-50 border border-orange-100 rounded-lg p-4">
                <h4 className="font-bold text-orange-800 text-sm mb-2 flex items-center gap-2">
                  <Play size={14} /> Build project
                </h4>
                <p className="text-orange-700 text-sm">{currentLesson.build}</p>
              </div>

              <div className="pt-4">
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={() => handleLessonComplete()}
                >
                  Mark Complete +{currentLesson.diamonds || 15} XP
                  <Play size={18} className="ml-2" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {!showLessonView && (
        <>
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-bold text-text-primary text-xl">
                {currentLevel.emoji} {currentLevel.name}
              </h2>
              <span className="px-2 py-1 rounded bg-gray-100 text-gray-600 text-xs font-bold">
                Level {currentLevel.order} of 40
              </span>
            </div>
            <p className="text-text-muted">{currentLevel.description}</p>

            <div className="mt-6 flex items-center justify-center">
              <div className="progress-ring">
                <svg viewBox="0 0 88 88">
                  <circle className="progress-ring-circle" cx="44" cy="44" r="40" />
                  <circle
                    className="progress-ring-fill"
                    cx="44"
                    cy="44"
                    r="40"
                    style={{
                      strokeDasharray: "251.2",
                      strokeDashoffset: 251.2 - (251.2 * (progressPercent / 100)),
                    }}
                  />
                </svg>
                <div className="progress-ring-text">
                  <div className="progress-ring-value">{progressPercent}%</div>
                  <div className="progress-ring-label">Level complete</div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            {currentLevel.lessons.map((lesson: any) => {
              const isCompleted = completedLessons.has(lesson.title);
              const isCurrent = lesson === nextLockedLesson;
              const status: "locked" | "current" | "completed" = isCompleted
                ? "completed"
                : isCurrent
                  ? "current"
                  : "locked";

              return (
                <LessonCard
                  key={lesson.title}
                  id={lesson.title}
                  title={lesson.title}
                  emoji={currentLevel.emoji || "📚"}
                  description={lesson.why}
                  type={
                    {
                      theory: "theory",
                      practice: "practice",
                      challenge: "challenge",
                      project: "project",
                      boss: "boss",
                      quiz: "quiz",
                    }[lesson.type] || "theory"
                  }
                  diamonds={lesson.diamonds || 15}
                  status={status}
                  progress={isCompleted ? 100 : isCurrent ? 30 : 0}
                  onClick={() => handleLessonClick(lesson)}
                />
              );
            })}
          </div>

          {levels[currentLevelIndex + 1] && (
            <Card variant="outlined" padding="md" radius="lg" className="mt-8 border-blue-100 bg-blue-50">
              <div className="flex items-center gap-3">
                <Flame size={18} className="text-blue-500" />
                <span className="font-bold text-text-primary">Next level:</span>
                <span className="text-text-muted">{levels[currentLevelIndex + 1].name}</span>
              </div>
              <p className="text-xs text-text-muted mt-1">
                Keep going to unlock {levels[currentLevelIndex + 1].description}
              </p>
            </Card>
          )}
        </>
      )}
    </PageShell>
  );
}
