import { useState } from "react";
import api from "../services/api";

export default function LoopsVertical() {
  const [step, setStep] = useState<"learn" | "trace" | "practice" | "test" | "result">("learn");
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [report, setReport] = useState<any>(null);
  const startTest = async () => {
    const r = await api.exam.start({ topic: "loops", count: 5, duration_minutes: 10 });
    setAttemptId(r.attempt_id);
    setQuestions(r.questions);
    setStep("test");
  };
  const submit = async () => {
    if (!attemptId) return;
    for (const q of questions) {
      if (answers[q.id]) {
        await api.exam.answer({ attempt_id: attemptId, question_id: q.id, answer: answers[q.id] });
      }
    }
    const r = await api.exam.complete(attemptId);
    setReport(r);
    setStep("result");
  };
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Loops — Vertical Slice</h1>
      {step === "learn" && (
        <div className="space-y-4">
          <p>A <code>for</code> loop repeats a block while a condition holds.</p>
          <pre className="bg-gray-900 text-green-300 p-3 rounded">for (let i = 0; i &lt; 3; i++) console.log(i);</pre>
          <button className="btn-primary" onClick={() => setStep("trace")}>Next: Trace</button>
        </div>
      )}
      {step === "trace" && (
        <div className="space-y-4">
          <p>Predict: what prints?</p>
          <pre className="bg-gray-900 text-green-300 p-3 rounded">for (let i = 1; i &lt;= 3; i++) console.log(i);</pre>
          <button className="btn-primary" onClick={() => setStep("practice")}>Next: Practice</button>
        </div>
      )}
      {step === "practice" && (
        <div className="space-y-4">
          <p>Practice: nested loops count iterations.</p>
          <button className="btn-primary" onClick={startTest}>Start Test</button>
        </div>
      )}
      {step === "test" && (
        <div className="space-y-4">
          {questions.map((q) => (
            <div key={q.id} className="border p-3 rounded">
              <p>{q.question}</p>
              {Object.entries(q.options || {}).map(([k, v]) => (
                <label key={k} className="block">
                  <input type="radio" name={q.id} value={k}
                    checked={answers[q.id] === k}
                    onChange={() => setAnswers({ ...answers, [q.id]: k })} /> {k}. {String(v)}
                </label>
              ))}
            </div>
          ))}
          <button className="btn-primary" onClick={submit}>Submit</button>
        </div>
      )}
      {step === "result" && report && (
        <div className="space-y-4">
          <p>Score: {report.score}% ({report.correct}/{report.total})</p>
          <button className="btn-primary" onClick={() => setStep("learn")}>Restart</button>
        </div>
      )}
    </div>
  );
}
