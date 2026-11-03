import { useState } from "react";

export default function CodingAcademy() {
  const [step, setStep] = useState<"learn" | "trace" | "predict" | "practice">("learn");
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Coding Academy</h1>
      {step === "learn" && (
        <div className="space-y-4">
          <p>Loops repeat a block while a condition holds.</p>
          <pre className="bg-gray-900 text-green-300 p-3 rounded">for (let i = 0; i < 3; i++) console.log(i);</pre>
          <button className="btn-primary" onClick={() => setStep("trace")}>Next: Trace</button>
        </div>
      )}
      {step === "trace" && (
        <div className="space-y-4">
          <p>Predict the output:</p>
          <pre className="bg-gray-900 text-green-300 p-3 rounded">for (let i = 1; i <= 3; i++) console.log(i);</pre>
          <button className="btn-primary" onClick={() => setStep("predict")}>Next: Predict</button>
        </div>
      )}
      {step === "predict" && (
        <div className="space-y-4">
          <p>Output prediction MCQ:</p>
          <button className="btn-primary" onClick={() => setStep("practice")}>Next: Practice</button>
        </div>
      )}
      {step === "practice" && (
        <div className="space-y-4">
          <p>Write a loop that sums 1 to n.</p>
          <button className="btn-primary">Submit</button>
        </div>
      )}
    </div>
  );
}
