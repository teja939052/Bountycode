import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";
import { PageShell } from "../design-system/PageShell";

const TRACKS = [
  { id: "python", label: "Python", color: "from-blue-500 to-cyan-500" },
  { id: "javascript", label: "JavaScript", color: "from-yellow-500 to-orange-500" },
  { id: "java", label: "Java", color: "from-red-500 to-orange-500" },
  { id: "cpp", label: "C++", color: "from-purple-500 to-blue-500" },
];

export default function LessonsPage() {
  const [lessons, setLessons] = useState<any[]>([]);
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTrack, setSelectedTrack] = useState("python");
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    loadLessons();
    loadProgress();
  }, [selectedTrack, searchQuery]);

  const loadLessons = async () => {
    try {
      if (searchQuery.trim()) {
        const data = await api.lessons.search(searchQuery, selectedTrack);
        setLessons(data.lessons || []);
      } else {
        const data = await api.lessons.list(selectedTrack);
        setLessons(data.lessons || []);
      }
    } catch {}
    setLoading(false);
  };

  const loadProgress = async () => {
    try {
      const data = await api.lessons.progress();
      setProgress(data);
    } catch {}
  };

  const trackLessons = lessons.filter((l) => l.track === selectedTrack);

  const lessonProgress = (lessonId: string) => {
    if (!progress) return 0;
    const lesson = trackLessons.find((l) => l.id === lessonId);
    if (!lesson) return 0;
    const done = lesson.steps.filter((s: any) =>
      progress.completed?.[`${lessonId}:${s.id}`]
    ).length;
    return Math.round((done / lesson.steps.length) * 100);
  };

  if (loading) {
    return (
      <PageShell theme="focus" className="max-w-4xl mx-auto py-20">
        <div className="flex items-center justify-center gap-2">
          <div className="w-6 h-6 animate-spin rounded-full border-2 border-brand-primary border-t-transparent" />
          <span className="text-text-muted">Loading lessons…</span>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell theme="adventure" className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h2 className="font-bold text-text text-2xl">Coding Academy</h2>
        <p className="text-text-muted mt-1">
          Step-by-step coding lessons with instant feedback. Write code, see output, level up.
        </p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <input
          placeholder="Search lessons (e.g., loops, variables, functions)..."
          value={searchQuery}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setSearchQuery(e.target.value)
          }
          className="w-full rounded-lg border border-[#2a2a2a] bg-[#0a0a0a] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none"
        />
      </div>

      {/* Track selector */}
      <div className="mb-6 flex gap-2">
        {TRACKS.map((t) => (
          <Button
            key={t.id}
            variant={selectedTrack === t.id ? "primary" : "outline"}
            size="sm"
            onClick={() => setSelectedTrack(t.id)}
            className="flex items-center gap-2"
          >
            <div
              className="w-3 h-3 rounded-full"
              style={t.color.includes("gradient")
                ? { background: t.color }
                : {}}
            ></div>
            <span>{t.label}</span>
          </Button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {trackLessons.length === 0 ? (
          <div className="col-span-full text-center py-12 text-text-muted">
            No lessons available for this track yet.
          </div>
        ) : (
          trackLessons.map((lesson) => {
            const pct = lessonProgress(lesson.id);
            const isComplete = pct === 100;
            return (
              <Card
                key={lesson.id}
                pad="md"
                tone={isComplete ? "sand" : "default"}
                interactive
                onClick={() => navigate(`/lessons/${lesson.id}`)}
                className="cursor-pointer group hover:border-brand-primary/50"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center mb-2" style={{ background: "#6366f1" }}>
                    <span className="text-xs font-bold text-[#0a0a0a]">{lesson.track.charAt(0).toUpperCase()}</span>
                  </div>
                  <span className="text-xs font-mono text-brand-muted">
                    {lesson.difficulty}
                  </span>
                </div>
                <h3 className="font-bold text-text mb-2">{lesson.title}</h3>
                <p className="text-sm text-brand-muted mb-3 line-clamp-2">
                  {lesson.description}
                </p>
                <div className="w-full bg-[#1a1a1a] rounded-full h-1.5 mb-3">
                  <div
                    className="bg-amber-500 h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${pct}%` }}
                  ></div>
                </div>
                <div className="flex items-center justify-between text-xs text-brand-muted">
                  <span>{pct}% complete</span>
                  <span>{lesson.xpReward} XP</span>
                </div>
              </Card>
            );
          })
        )}
      </div>
    </PageShell>
  );
}
