import { motion } from "framer-motion";

interface HyperdriveStatusProps {
  status?: string;
  testResults?: Record<string, any>;
}

export default function HyperdriveStatus({ status = "idle", testResults = {} }: HyperdriveStatusProps) {
  const states = {
    idle: {
      label: "STANDBY",
      color: "text-gray-500",
      barColor: "bg-gray-600",
      glowColor: "",
      message: "Hyperdrive on standby. Submit code to initiate jump sequence.",
    },
    compiling: {
      label: "COMPILING",
      color: "text-cyber-amber",
      barColor: "bg-cyber-amber",
      glowColor: "shadow-[0_0_20px_rgba(245,158,11,0.3)]",
      message: "Compiling source code... Quantum processors engaged.",
    },
    running: {
      label: "EXECUTING",
      color: "text-cyber-blue",
      barColor: "bg-cyber-blue",
      glowColor: "shadow-cyber-blue",
      message: "Hyperdrive active. Running test cases through the matrix...",
    },
    success: {
      label: "ALL SYSTEMS CLEAR",
      color: "text-cyber-green",
      barColor: "bg-cyber-green",
      glowColor: "shadow-cyber-green",
      message: "All test cases passed. Thrusters nominal. Systems green across the board.",
    },
    partial: {
      label: "PARTIAL SUCCESS",
      color: "text-cyber-amber",
      barColor: "bg-cyber-amber",
      glowColor: "shadow-[0_0_20px_rgba(245,158,11,0.3)]",
      message: "Some test cases failed. Analyzing breach points...",
    },
    failed: {
      label: "HULL BREACH DETECTED",
      color: "text-cyber-red",
      barColor: "bg-cyber-red",
      glowColor: "shadow-[0_0_20px_rgba(239,68,68,0.3)]",
      message: "Test case failure detected. Systems stabilizing...",
    },
    error: {
      label: "COMPILATION ERROR",
      color: "text-cyber-red",
      barColor: "bg-cyber-red",
      glowColor: "shadow-[0_0_20px_rgba(239,68,68,0.3)]",
      message: "Code execution error. Diagnostic analysis required.",
    },
  };

  const s = states[status] || states.idle;
  const { passed = 0, failed = 0, total = 0 } = testResults;

  return (
    <div className={`rounded-xl bg-space-panel/80 border border-space-border overflow-hidden ${s.glowColor} transition-all duration-500`}>
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-space-border bg-space-void/50">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <span className={`w-3 h-3 rounded-full ${status === "success" ? "bg-cyber-green" : status === "failed" || status === "error" ? "bg-cyber-red animate-pulse" : "bg-gray-600"}`} />
            <span className={`w-3 h-3 rounded-full ${status === "running" || status === "compiling" ? "bg-cyber-blue animate-pulse" : "bg-gray-600"}`} />
            <span className="w-3 h-3 rounded-full bg-gray-600" />
          </div>
          <span className="text-[10px] font-mono uppercase tracking-widest text-gray-400">
            Quantum Hyperdrive
          </span>
        </div>
        <span className={`text-[10px] font-mono font-bold uppercase tracking-wider ${s.color}`}>
          {s.label}
        </span>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-space-void">
        <motion.div
          className={`h-full ${s.barColor}`}
          initial={{ width: "0%" }}
          animate={{
            width: status === "success" ? "100%" : status === "failed" ? "100%" : "60%",
          }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />
      </div>

      {/* Content */}
      <div className="p-4">
        <p className={`text-xs font-mono ${s.color} mb-3`}>{s.message}</p>

        {/* Test case results */}
        {total > 0 && (
          <div className="flex gap-4">
            <div className="flex items-center gap-2">
              <span className="status-online" />
              <span className="text-xs font-mono text-gray-400">
                <span className="text-cyber-green">{passed}</span> passed
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="status-dot bg-cyber-red" style={{ boxShadow: "0 0 6px rgba(239,68,68,0.6)" }} />
              <span className="text-xs font-mono text-gray-400">
                <span className="text-cyber-red">{failed}</span> failed
              </span>
            </div>
            <div className="text-xs font-mono text-gray-500">
              / {total} total
            </div>
          </div>
        )}

        {/* Thruster visualization */}
        {(status === "success" || status === "running") && (
          <div className="mt-3 flex gap-1">
            {Array.from({ length: 20 }).map((_, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0.2 }}
                animate={{ opacity: [0.2, 1, 0.2] }}
                transition={{ delay: i * 0.05, repeat: Infinity, duration: 1.5 }}
                className={`h-4 flex-1 rounded-sm ${
                  status === "success" ? "bg-cyber-green" : "bg-cyber-blue"
                }`}
                style={{ opacity: 0.3 + Math.random() * 0.7 }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
