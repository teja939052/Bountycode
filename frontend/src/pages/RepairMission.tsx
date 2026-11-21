import { useState, useEffect } from "react";
import { useParams, Link, useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight, Rocket, RefreshCw, ShieldCheck, Target, Brain,
  AlertCircle, Play, Clock, ChevronRight, Sparkles,
} from "lucide-react";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { ReadinessRing } from "../design-system/Progress";
import api from "../services/api";
import { missionApi } from "../services/api/missions";

export default function RepairMission() {
  const { skill } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [mission, setMission] = useState<any>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [step, setStep] = useState<"mission" | "practice" | "retest" | "complete">("mission");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [repairResult, setRepairResult] = useState<any>(null);
  const [retestResult, setRetestResult] = useState<any>(null);

  useEffect(() => {
    if (!skill) return;
    loadRepairMission(skill);
  }, [skill]);

  const loadRepairMission = async (skillId: string) => {
    try {
      const [missionsResp, retestResp] = await Promise.all([
        missionApi.listRepairMissions(),
        missionApi.getRetest(skillId, 3),
      ]);

      const missions = missionsResp?.missions || missionsResp?.missions_data || [];
      const repairMission = missions.find(
        (m: any) => m.skill_id === skillId || m.skill === skillId || m.id === skillId
      ) || missions[0];

      setMission(repairMission);
      setQuestions(Array.isArray(retestResp?.questions) ? retestResp.questions : []);

      if (repairMission?.mission_id) {
        // Mark mission as started
        missionApi.completeRepairMission(repairMission.mission_id).catch(() => {});
      }
    } catch (err: any) {
      console.error("Failed to load repair mission", err);
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  const handleAnswer = (questionId: string, answer: any) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const isLastQuestion = currentQuestionIndex === questions.length - 1;

  const submitRepair = async () => {
    if (!mission) return;
    setSubmitting(true);
    try {
      const res: any = await missionApi.completeRepairMission(mission.mission_id);
      setRepairResult(res?.data || res);
      setStep("retest");
    } catch (err: any) {
      console.error("Repair submission failed", err);
      setSubmitting(false);
    }
  };

  const submitRetest = async () => {
    if (!mission) return;
    setSubmitting(true);
    try {
      const answersPayload = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: questionId,
        answer: answer,
      }));
      const res: any = await missionApi.submitRetest({
        mission_id: mission.mission_id,
        skill: skill,
        answers: answersPayload,
      });
      setRetestResult(res?.data || res);
      setSubmitting(false);
      setStep("complete");
    } catch (err: any) {
      console.error("Retest submission failed", err);
      setSubmitting(false);
    }
  };

  const improvement = retestResult?.improvement || retestResult?.improvement_pct;
  const passedRetest = retestResult?.passed ?? retestResult?.passed_retest;

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-sky mx-auto mb-3" />
          <p className="text-sm text-slate-500">Preparing your repair mission…</p>
        </div>
      </div>
    );
  }

  if (!mission) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto text-rose-500 mb-3" size={32} />
          <h2 className="text-lg font-bold text-slate-900">Repair mission not found</h2>
          <p className="text-sm text-slate-600">
            This repair mission could not be loaded. Please return to your dashboard and try again.
          </p>
          <Link to="/dashboard" className="mt-4 inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
            <ArrowLeft size={14} /> Back to dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-4 py-6 sm:py-10">
        {/* ===== HEADER ===== */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-700 flex items-center gap-2">
              <Rocket size={14} /> Repair mission
            </p>
            <h1 className="mt-1 text-xl font-black text-slate-900">
              Repair: {mission.skill_id || mission.skill || "Skill repair"}
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              {mission.description || "Fix the gap, then retest to confirm mastery."}
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 sm:items-end">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 rounded-md border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              <ArrowLeft size={14} /> Dashboard
            </Link>
          </div>
        </div>

        {/* ===== STEP: MISSION INFO ===== */}
        {step === "mission" && (
          <AnimatePresence>
            <motion.div key="mission" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
              <Card className="border border-green-100 bg-green-50 p-6 sm:p-8 shadow-sm">
                <div className="flex items-start gap-4">
                  <div className="rounded-xl bg-emerald-100 p-3 shrink-0">
                    <Rocket size={28} className="text-emerald-600" />
                  </div>
                  <div className="flex-1">
                    <h2 className="text-lg font-bold text-slate-900">{mission.title || "Repair this skill"}</h2>
                    <p className="mt-1 text-sm text-slate-600">
                      {mission.description || "This skill needs repair before you can retest and advance."}
                    </p>
                    <div className="mt-4 flex items-center gap-3">
                      <span className="rounded-full border border-emerald-200 bg-white px-2 py-1 text-xs font-bold text-emerald-700">
                        {mission.tier || "repair"}
                      </span>
                      <span className="ml-2 text-xs text-slate-500">
                        Estimated {mission.estimated_minutes ?? 10} min
                      </span>
                    </div>
                  </div>
                </div>
                <div className="mt-6 pt-6 border-t border-green-50">
                  <h3 className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">What you'll do</h3>
                  <ul className="mt-2 space-y-2">
                    {mission.steps?.map((s: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                        <span className="rounded-full bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 shrink-0">
                          {i + 1}
                        </span>
                        {s}
                      </li>
                    )) || (
                      <li className="flex items-start gap-2 text-sm text-slate-600">
                        <span className="rounded-full bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 shrink-0">
                          1
                        </span>
                        Read the explanation and understand the misconception
                      </li>
                    )}
                    <li className="flex items-start gap-2 text-sm text-slate-600">
                      <span className="rounded-full bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 shrink-0">
                        2
                      </span>
                      Practice targeted questions
                    </li>
                    <li className="flex items-start gap-2 text-sm text-slate-600">
                      <span className="rounded-full bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 shrink-0">
                        3
                      </span>
                      Retest to confirm mastery
                    </li>
                  </ul>
                </div>
                <div className="mt-6 flex gap-3">
                  <Button
                    variant="primary"
                    onClick={() => setStep("practice")}
                    className="w-full sm:w-auto px-6 py-3 text-lg font-bold"
                  >
                    Start repair practice <Rocket size={16} className="ml-2" />
                  </Button>
                  <Button variant="outline" asChild className="w-full sm:w-auto px-6 py-3">
                    <Link to="/dashboard" className="flex items-center gap-2">
                      Back to dashboard <ArrowRight size={14} />
                    </Link>
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </div>

        {/* ===== STEP: PRACTICE ===== */}
        {step === "practice" && questions.length > 0 && (
          <AnimatePresence>
            <motion.div key="practice" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <Card className="border border-blue-100 bg-blue-50 p-6 sm:p-8 shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[0.16em] text-blue-700 flex items-center gap-2">
                      <Target size={14} /> Repair practice
                    </p>
                    <h2 className="mt-1 text-xl font-bold text-slate-900">
                      {currentQuestion.title || currentQuestion.question || "Practice question"}
                    </h2>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-blue-100 px-2 py-1 text-xs font-bold text-blue-700">
                      {currentQuestionIndex + 1} / {questions.length}
                    </span>
                  </div>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-white/50">
                  <p className="text-lg font-medium text-slate-900 mb-4">
                    {currentQuestion.question || currentQuestion.title || "Practice question"}
                  </p>
                  {currentQuestion.options?.map((opt: string, i: number) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => handleAnswer(currentQuestion.id || i, i)}
                      className={`w-full text-left rounded-lg border px-4 py-3 text-sm transition-all ${
                        answers[currentQuestion.id || i] === i
                          ? "border-blue-600 bg-blue-50 text-blue-600 font-semibold"
                          : "border-white/5 bg-white/5 text-text-secondary hover:border-blue-200 hover:bg-white/5"
                      }`}
                    >
                      {String.fromCharCode(65 + i)}. {opt}
                    </button>
                  ))}
                </div>
                <div className="mt-6 flex justify-between">
                  <Button
                    variant="outline"
                    onClick={() => setCurrentQuestionIndex((i) => Math.max(0, i - 1))}
                    disabled={currentQuestionIndex === 0}
                    className="px-4 py-2"
                  >
                    Previous
                  </Button>
                  <Button
                    variant="primary"
                    onClick={() => {
                      if (answers[currentQuestion.id || currentQuestionIndex] == null) {
                        return;
                      }
                      if (isLastQuestion) {
                        setSubmitting(true);
                        submitRepair();
                      } else {
                        setCurrentQuestionIndex((i) => i + 1);
                      }
                    }}
                    className="w-full sm:w-auto px-6 py-3 font-bold"
                  >
                    {isLastQuestion ? "Submit repair mission" : "Next question <ArrowRight size={14} className=\"ml-2\""}
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </div>

        {/* ===== STEP: RETEST ===== */}
        {step === "retest" && (
          <AnimatePresence>
            <motion.div key="retest" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
              <Card className="border border-blue-100 bg-blue-50 p-6 sm:p-8 shadow-sm">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[0.16em] text-blue-700 flex items-center gap-2">
                      <Sparkles size={14} /> Retest
                    </p>
                    <h2 className="mt-1 text-xl font-bold text-slate-900">Confirm mastery</h2>
                    <p className="mt-1 text-sm text-slate-600">
                      You've repaired the skill. Now prove it with fresh questions.
                    </p>
                  </div>
                  <span className="rounded-full bg-blue-600 text-white px-3 py-1 text-[10px] font-bold">
                    {isLastQuestion ? "Final question" : `Question ${currentQuestionIndex + 1} of ${questions.length}`}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-white/50 mt-6">
                  <p className="text-lg font-medium text-slate-900 mb-4">
                    {currentQuestion.question || currentQuestion.title || "Practice question"}
                  </p>
                  {currentQuestion.options?.map((opt: string, i: number) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => handleAnswer(currentQuestion.id || i, i)}
                      className={`w-full text-left rounded-lg border px-4 py-3 text-sm transition-all ${
                        answers[currentQuestion.id || i] === i
                          ? "border-blue-600 bg-blue-50 text-blue-600 font-semibold"
                          : "border-white/5 bg-white/5 text-text-secondary hover:border-blue-200 hover:bg-white/5"
                      }`}
                    >
                      {String.fromCharCode(65 + i)}. {opt}
                    </button>
                  ))}
                </div>
                <div className="mt-6 flex justify-between">
                  <Button variant="outline" onClick={() => setStep("mission")} className="px-4 py-2">
                    Back to repair
                  </Button>
                  <Button
                    variant="primary"
                    onClick={() => {
                      if (answers[currentQuestion.id || currentQuestionIndex] == null) return;
                      setSubmitting(true);
                      submitRetest();
                    }}
                    className="w-full sm:w-auto px-6 py-3 font-bold"
                  >
                    {isLastQuestion ? "Submit retest" : "Next question <ArrowRight size={14} className=\"ml-2\""}
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </div>

        {/* ===== STEP: COMPLETE ===== */}
        {step === "complete" && (
          <AnimatePresence>
            <motion.div key="complete" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, y: -10 }}>
              <div className="text-center py-12">
                <div className="relative inline-flex items-center justify-center w-24 h-24 rounded-full bg-emerald-100 mb-6">
                  <div className="absolute inset-0 rounded-full border border-emerald-200 animate-ping"></div>
                  <ShieldCheck className="w-10 h-10 text-emerald-600" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Repair complete!</h2>
                <p className="mt-2 text-slate-600">
                  {passedRetest
                    ? "You've demonstrated mastery. Your readiness has improved."
                    : "You completed the repair mission. Keep practicing to improve your score."}
                </p>

                {improvement !== undefined && (
                  <div className="mt-8 flex items-center justify-center gap-4 text-sm font-semibold text-emerald-600">
                    <Sparkles size={16} className="animate-bounce" />
                    Improvement: <span className="font-bold text-emerald-700">+{improvement}%</span>
                  </div>
                )}

                <div className="mt-8 flex gap-3">
                  <Button
                    variant="primary"
                    onClick={() => {
                      navigate("/dashboard");
                    }}
                  >
                    Back to dashboard <ArrowRight size={14} />
                  </Button>
                  <Button variant="outline" onClick={() => navigate("/readiness")}>
                    View readiness report <ArrowRight size={14} />
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* ===== REPAIR COMPLETE MODAL ===== */}
        {step === "complete" && (
          <AnimatePresence>
            <motion.div key="complete-modal" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="absolute inset-0 z-50 flex items-center justify-center p-4">
                <div className="max-w-lg bg-white rounded-2xl shadow-2xl border border-white/20 p-6">
                  <h3 className="text-lg font-bold text-slate-900 mb-4">
                    {passedRetest ? "Mastery achieved!" : "Repair complete"}
                  </h3>
                  <p className="text-sm text-slate-600 mb-6">
                    {passedRetest
                      ? "You've demonstrated mastery of this skill. Your readiness has improved."
                      : "You completed the repair mission. Keep practicing to improve your score."}
                  </p>
                  <div className="flex gap-2">
                    <Button variant="primary" onClick={() => navigate("/dashboard")}>
                      Back to dashboard <ArrowRight size={14} />
                    </Button>
                    <Button variant="outline" onClick={() => navigate("/readiness")}>
                      View readiness report <ArrowRight size={14} />
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    );
  );
}
