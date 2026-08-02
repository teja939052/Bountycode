import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import api from "../services/api";
import {
  Play, Pause, SkipBack, SkipForward, RotateCcw, Copy, Check,
  Heart, Clock, ChevronLeft, Maximize2, Minimize2, Hash,
  ChevronDown, ChevronUp, GitFork, Pencil, Save, Loader, Lock,
} from "lucide-react";

const SPEEDS = [0.5, 1, 1.5];

const LANGUAGE_MAP = {
  python: "python",
  javascript: "javascript",
  java: "java",
  cpp: "cpp",
  sql: "sql",
};

const DIFFICULTY_COLORS = {
  beginner: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
  intermediate: "border-amber-500/30 bg-amber-500/10 text-amber-400",
  advanced: "border-rose-500/30 bg-rose-500/10 text-rose-400",
};

function formatTime(ms) {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function ScrimPlayer({ scrim, onBack, onLike }) {
  const originalSnapshots = scrim.snapshots || [];
  const [timeline, setTimeline] = useState(originalSnapshots);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [progress, setProgress] = useState(0);
  const [copied, setCopied] = useState(false);
  const [liked, setLiked] = useState(false);
  const [editorCode, setEditorCode] = useState("");
  const [userEdited, setUserEdited] = useState(false);
  const [showInfo, setShowInfo] = useState(true);
  const [fullscreen, setFullscreen] = useState(false);
  const [compact, setCompact] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedFork, setSavedFork] = useState(null);
  const editorRef = useRef(null);
  const playerRef = useRef(null);
  const timerRef = useRef(null);
  const progressRef = useRef(null);

  const isForked = timeline.some(
    (snap, i) => (originalSnapshots[i] || {}).code !== snap.code
  );
  const monacoLanguage = LANGUAGE_MAP[scrim.language] || "python";
  const currentSnapshot = timeline[currentIndex] || timeline[0];
  const lastIdx = timeline.length - 1;

  useEffect(() => {
    setTimeline(scrim.snapshots || []);
    setCurrentIndex(0);
    setPlaying(false);
    setProgress(0);
    setEditorCode((scrim.snapshots || [])[0]?.code || "");
    setUserEdited(false);
    setSavedFork(null);
  }, [scrim.id]);

  useEffect(() => {
    if (currentSnapshot) {
      setEditorCode(currentSnapshot.code);
      setUserEdited(false);
    }
  }, [currentIndex]);

  useEffect(() => {
    if (playing && timeline.length > 0) {
      const start = timeline[currentIndex]?.timestamp_ms || 0;
      const next = timeline[currentIndex + 1];
      const end = next ? next.timestamp_ms : (scrim.duration_seconds || 60) * 1000;
      const duration = end - start;
      const interval = 50;

      let elapsed = 0;
      timerRef.current = setInterval(() => {
        elapsed += interval * speed;
        const pct = Math.min(100, (elapsed / duration) * 100);
        setProgress(((start + elapsed) / ((scrim.duration_seconds || 60) * 1000)) * 100);

        if (pct >= 100) {
          if (currentIndex < timeline.length - 1) {
            setCurrentIndex(prev => prev + 1);
          } else {
            setPlaying(false);
            setProgress(100);
          }
        }
      }, interval);

      return () => clearInterval(timerRef.current);
    }
  }, [playing, currentIndex, speed, timeline, scrim.duration_seconds]);

  const togglePlay = useCallback(() => {
    if (currentIndex >= lastIdx && !playing) {
      setCurrentIndex(0);
      setProgress(0);
    }
    setPlaying(prev => !prev);
  }, [currentIndex, lastIdx, playing]);

  const goToStep = useCallback((idx) => {
    const target = Math.max(0, Math.min(idx, timeline.length - 1));
    setCurrentIndex(target);
    setProgress((timeline[target]?.timestamp_ms || 0) / ((scrim.duration_seconds || 60) * 1000) * 100);
    setPlaying(false);
  }, [timeline, scrim.duration_seconds]);

  const stepForward = useCallback(() => {
    goToStep(currentIndex + 1);
  }, [currentIndex, goToStep]);

  const stepBackward = useCallback(() => {
    goToStep(currentIndex - 1);
  }, [currentIndex, goToStep]);

  const resetToSnapshot = useCallback(() => {
    const orig = originalSnapshots[currentIndex];
    if (orig) {
      setEditorCode(orig.code);
      setTimeline(prev => prev.map((s, i) => (i === currentIndex ? orig : s)));
      setUserEdited(false);
    }
  }, [originalSnapshots, currentIndex]);

  const handleEditorChange = useCallback((val) => {
    const code = val || "";
    setEditorCode(code);
    setUserEdited(true);
    setTimeline(prev =>
      prev.map((s, i) => (i === currentIndex ? { ...s, code } : s))
    );
  }, [currentIndex]);

  const enterEditMode = useCallback(() => {
    setPlaying(false);
    setTimeout(() => editorRef.current?.focus(), 50);
  }, []);

  const handleContinue = useCallback(() => {
    setPlaying(true);
  }, []);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(editorCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleEditorMount = (editor) => {
    editorRef.current = editor;
    editor.focus();
  };

  const handleProgressClick = (e) => {
    const rect = progressRef.current?.getBoundingClientRect();
    if (!rect) return;
    const pct = (e.clientX - rect.left) / rect.width;
    const targetMs = pct * (scrim.duration_seconds || 60) * 1000;
    let idx = 0;
    for (let i = timeline.length - 1; i >= 0; i--) {
      if (timeline[i].timestamp_ms <= targetMs) { idx = i; break; }
    }
    goToStep(idx);
  };

  const handleForkSave = async () => {
    if (saving || savedFork || timeline.length < 2) return;
    setSaving(true);
    try {
      const payload = {
        title: `${scrim.title} (edited)`,
        description: scrim.description || `Forked from "${scrim.title}"`,
        topic: scrim.topic,
        difficulty: scrim.difficulty,
        language: scrim.language,
        snapshots: timeline.map(s => ({ code: s.code, timestamp_ms: s.timestamp_ms, line: s.line })),
        final_code: timeline[lastIdx]?.code || editorCode,
        tags: scrim.tags || [],
      };
      const data = await api.createScrim(payload);
      setSavedFork(data.id || "saved");
    } catch (e) {
      console.error("Failed to save fork:", e);
    } finally {
      setSaving(false);
    }
  };

  const totalMs = (scrim.duration_seconds || 60) * 1000;
  const currentMs = currentSnapshot?.timestamp_ms || 0;

  return (
    <div ref={playerRef} className={`min-h-screen bg-slate-950 ${fullscreen ? "fixed inset-0 z-50" : ""}`}>
      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-3 sm:py-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3 min-w-0">
            <button onClick={onBack} className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-700 bg-slate-800/60 text-xs text-slate-400 hover:text-slate-200 hover:border-indigo-500/40 transition-all">
              <ChevronLeft className="w-3.5 h-3.5" /> Back
            </button>
            <div className="min-w-0">
              <h2 className="text-base sm:text-lg font-semibold text-slate-100 truncate">{scrim.title}</h2>
              <p className="text-xs text-slate-500 truncate flex items-center gap-1.5">
                {scrim.author_name} · {scrim.topic} · {scrim.language}
                {isForked && (
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[10px] font-mono border border-indigo-500/30 bg-indigo-500/10 text-indigo-400">
                    <GitFork className="w-2.5 h-2.5" /> forked
                  </span>
                )}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setFullscreen(!fullscreen)}
              className="p-2 rounded-xl border border-slate-700 bg-slate-800/60 text-slate-400 hover:text-slate-200 hover:border-indigo-500/40 transition-all"
            >
              {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 space-y-3">
            <div className="relative rounded-2xl overflow-hidden border border-slate-700/60 bg-slate-900">
              <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700/60 bg-slate-800/40">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-slate-500">
                    <Hash className="w-3 h-3 inline mr-1" />
                    Line {currentSnapshot?.line || 1}
                  </span>
                  <span className="text-xs font-mono text-slate-600">·</span>
                  <span className="text-xs font-mono text-slate-500">
                    Snapshot {currentIndex + 1} of {timeline.length}
                  </span>
                  <span className="text-xs font-mono text-slate-600">·</span>
                  {playing ? (
                    <span className="flex items-center gap-1 text-xs font-mono text-slate-500">
                      <Lock className="w-3 h-3" /> playing
                    </span>
                  ) : userEdited ? (
                    <span className="flex items-center gap-1 text-xs font-mono text-indigo-400">
                      <Pencil className="w-3 h-3" /> editing
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-xs font-mono text-slate-500">
                      <Pencil className="w-3 h-3" /> paused
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={enterEditMode}
                    className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs transition-all ${
                      !playing
                        ? "text-indigo-400 border border-indigo-500/30 bg-indigo-500/10"
                        : "text-slate-400 hover:text-indigo-400 border border-transparent hover:bg-slate-700/50"
                    }`}
                  >
                    <Pencil className="w-3 h-3" /> {playing ? "Pause & Edit" : "Editing"}
                  </button>
                  <button onClick={resetToSnapshot} disabled={!userEdited} className="flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs text-slate-400 hover:text-indigo-400 disabled:opacity-30 hover:bg-slate-700/50 transition-all">
                    <RotateCcw className="w-3 h-3" /> Reset
                  </button>
                  <button onClick={handleCopy} className="flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs text-slate-400 hover:text-indigo-400 hover:bg-slate-700/50 transition-all">
                    {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    {copied ? "Copied" : "Copy"}
                  </button>
                </div>
              </div>

              <Editor
                height={compact ? "300px" : "480px"}
                language={monacoLanguage}
                value={editorCode}
                onChange={handleEditorChange}
                onMount={handleEditorMount}
                theme="vs-dark"
                options={{
                  fontSize: 13,
                  fontFamily: "JetBrains Mono, Fira Code, monospace",
                  minimap: { enabled: !compact },
                  scrollBeyondLastLine: false,
                  lineNumbers: "on",
                  renderWhitespace: "selection",
                  bracketPairColorization: { enabled: true },
                  padding: { top: 12 },
                  automaticLayout: true,
                  readOnly: playing,
                }}
              />
            </div>

            <AnimatePresence>
              {!playing && userEdited && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  className="rounded-2xl border border-indigo-500/30 bg-indigo-500/10 p-3 flex flex-wrap items-center justify-between gap-3"
                >
                  <div className="flex items-center gap-2 text-xs text-indigo-300 min-w-0">
                    <GitFork className="w-4 h-4 shrink-0" />
                    <span className="truncate">Edit mode — your changes fork this scrim's timeline.</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleContinue}
                      className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-500/30 text-xs font-medium transition-all"
                    >
                      <Play className="w-3.5 h-3.5" /> Continue
                    </button>
                    <button
                      onClick={handleForkSave}
                      disabled={saving || savedFork || timeline.length < 2}
                      className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 disabled:opacity-40 text-xs font-medium transition-all"
                    >
                      {saving ? <Loader className="w-3.5 h-3.5 animate-spin" /> : savedFork ? <Check className="w-3.5 h-3.5" /> : <Save className="w-3.5 h-3.5" />}
                      {savedFork ? "Fork Saved" : saving ? "Saving..." : "Fork & Save"}
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="rounded-2xl border border-slate-700/60 bg-slate-800/40 p-4">
              <div
                ref={progressRef}
                onClick={handleProgressClick}
                className="relative h-2 bg-slate-700/60 rounded-full cursor-pointer mb-4 group"
              >
                <div
                  className="absolute left-0 top-0 h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all duration-150"
                  style={{ width: `${Math.min(100, progress)}%` }}
                />
                <div
                  className="absolute top-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-white border-2 border-indigo-500 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ left: `calc(${Math.min(100, progress)}% - 8px)` }}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1">
                  <button onClick={stepBackward} disabled={currentIndex <= 0} className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 disabled:opacity-30 transition-all">
                    <SkipBack className="w-4 h-4" />
                  </button>
                  <button onClick={togglePlay} className="p-3 rounded-xl bg-indigo-500/20 text-indigo-400 hover:bg-indigo-500/30 transition-all">
                    {playing ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  </button>
                  <button onClick={stepForward} disabled={currentIndex >= lastIdx} className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 disabled:opacity-30 transition-all">
                    <SkipForward className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex items-center gap-4">
                  <span className="text-xs font-mono text-slate-500">
                    {formatTime(currentMs)} / {formatTime(totalMs)}
                  </span>

                  <div className="flex items-center gap-1">
                    {SPEEDS.map(s => (
                      <button
                        key={s}
                        onClick={() => setSpeed(s)}
                        className={`px-2 py-1 rounded-lg text-[11px] font-mono font-medium transition-all ${
                          speed === s
                            ? "bg-indigo-500/20 text-indigo-400 border border-indigo-500/30"
                            : "text-slate-500 hover:text-slate-300 border border-transparent"
                        }`}
                      >
                        {s}x
                      </button>
                    ))}
                  </div>

                  <button onClick={() => setShowInfo(!showInfo)} className="lg:hidden p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 transition-all">
                    {showInfo ? <ChevronDown className="w-4 h-4" /> : <ChevronUp className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <AnimatePresence>
            {(showInfo || window.innerWidth >= 1024) && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="space-y-4"
              >
                <div className="rounded-2xl border border-slate-700/60 bg-slate-800/40 p-4">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-7 h-7 rounded-lg bg-indigo-500/20 flex items-center justify-center">
                      <Hash className="w-3.5 h-3.5 text-indigo-400" />
                    </div>
                    <span className="text-xs font-mono font-medium text-slate-400">
                      STEP {currentIndex + 1} / {timeline.length}
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    {currentSnapshot?.description || "No description for this step."}
                  </p>
                  <div className="flex flex-wrap gap-2 mt-4">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border ${DIFFICULTY_COLORS[scrim.difficulty] || "border-slate-600 text-slate-400"}`}>
                      {scrim.difficulty}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-sky-500/30 bg-sky-500/10 text-sky-400">
                      {scrim.language}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-violet-500/30 bg-violet-500/10 text-violet-400">
                      {scrim.topic}
                    </span>
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-700/60 bg-slate-800/40 p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-xs font-mono uppercase tracking-wider text-slate-500">Timeline</h4>
                    {isForked && (
                      <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[10px] font-mono border border-indigo-500/30 bg-indigo-500/10 text-indigo-400">
                        <GitFork className="w-2.5 h-2.5" /> forked
                      </span>
                    )}
                  </div>
                  <div className="space-y-1.5 max-h-64 overflow-y-auto scrollbar-thin">
                    {timeline.map((snap, idx) => {
                      const stepEdited = snap.code !== (originalSnapshots[idx] || {}).code;
                      return (
                        <button
                          key={idx}
                          onClick={() => goToStep(idx)}
                          className={`w-full text-left flex items-center gap-3 px-3 py-2 rounded-xl text-xs transition-all ${
                            idx === currentIndex
                              ? "bg-indigo-500/15 text-indigo-300 border border-indigo-500/20"
                              : "text-slate-500 hover:text-slate-300 hover:bg-slate-700/30 border border-transparent"
                          }`}
                        >
                          <div className={`shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono ${
                            idx === currentIndex ? "bg-indigo-500/30 text-indigo-300" : "bg-slate-700/60 text-slate-500"
                          }`}>
                            {stepEdited ? <GitFork className="w-3 h-3" /> : idx + 1}
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="truncate font-medium flex items-center gap-1.5">
                              {snap.description || `Step ${idx + 1}`}
                              {stepEdited && <span className="text-[9px] px-1 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-mono shrink-0">edited</span>}
                            </div>
                            <div className="text-[10px] text-slate-600 font-mono">{formatTime(snap.timestamp_ms)}</div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-700/60 bg-slate-800/40 p-4">
                  <div className="flex items-center gap-4 text-xs text-slate-500 mb-4">
                    <span className="flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" /> {formatTime(totalMs)}</span>
                    <span className="flex items-center gap-1.5"><Hash className="w-3.5 h-3.5" /> {timeline.length} steps</span>
                    <span>{scrim.views || 0} views</span>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={onLike}
                      className="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-slate-700 text-xs text-slate-400 hover:text-rose-400 hover:border-rose-500/30 transition-all"
                    >
                      <Heart className={`w-3.5 h-3.5 ${liked ? "fill-rose-400 text-rose-400" : ""}`} />
                      {liked ? "Liked" : "Like"} ({scrim.likes || 0})
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
