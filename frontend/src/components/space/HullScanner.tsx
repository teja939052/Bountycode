import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function HullScanner({ atsScore = 0, issues = [], keywords = [] }) {
  const [scanning, setScanning] = useState(false);

  const getScoreColor = (s) => {
    if (s >= 80) return { text: "text-cyber-green", glow: "glow-green", ring: "from-cyber-green to-emerald-400" };
    if (s >= 60) return { text: "text-cyber-blue", glow: "glow-blue", ring: "from-cyber-blue to-cyan-400" };
    if (s >= 40) return { text: "text-cyber-amber", glow: "", ring: "from-cyber-amber to-yellow-400" };
    return { text: "text-cyber-red", glow: "", ring: "from-cyber-red to-red-400" };
  };

  const sc = getScoreColor(atsScore);

  return (
    <div className="relative rounded-xl bg-space-panel/80 border border-space-border overflow-hidden">
      {/* Ambient grid */}
      <div className="absolute inset-0 ambient-grid opacity-20 pointer-events-none" />

      {/* Header */}
      <div className="relative z-10 flex justify-between items-center px-6 py-4 border-b border-space-border">
        <div>
          <span className="text-[10px] font-mono text-cyber-blue/70 tracking-widest uppercase block">
            Hull Structural Diagnostic
          </span>
          <h3 className="text-lg font-display font-bold text-text-primary tracking-tight">
            ATS Compatibility Scan
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span className={scanning ? "status-processing" : atsScore >= 70 ? "status-online" : "status-warning"} />
          <span className="text-[10px] font-mono uppercase tracking-wider text-gray-400">
            {scanning ? "Scanning" : "Complete"}
          </span>
        </div>
      </div>

      <div className="relative z-10 p-6">
        {/* Score Display */}
        <div className="flex items-center gap-8 mb-6">
          {/* Circular score with scan animation */}
          <div className="relative">
            <div className={`w-28 h-28 rounded-full border-4 border-space-border flex items-center justify-center bg-space-void/50`}>
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0.5, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className={`text-3xl font-display font-black ${sc.text} ${sc.glow}`}
                >
                  {atsScore}
                </motion.div>
                <div className="text-[8px] font-mono uppercase tracking-widest text-gray-500">
                  ATS Score
                </div>
              </div>
            </div>

            {/* Scan line overlay */}
            {scanning && (
              <motion.div
                initial={{ top: 0 }}
                animate={{ top: "100%" }}
                transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-cyber-blue to-transparent"
                style={{ boxShadow: "0 0 10px rgba(76,201,240,0.5)" }}
              />
            )}
          </div>

          {/* Issues summary */}
          <div className="flex-1 space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="font-mono text-gray-400">Critical Issues</span>
              <span className="font-mono text-cyber-red">{issues.filter(i => i.severity === "critical").length}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="font-mono text-gray-400">Warnings</span>
              <span className="font-mono text-cyber-amber">{issues.filter(i => i.severity === "warning").length}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="font-mono text-gray-400">Keywords Found</span>
              <span className="font-mono text-cyber-green">{keywords.length}</span>
            </div>
          </div>
        </div>

        {/* Issues list */}
        <AnimatePresence>
          {issues.length > 0 && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              className="space-y-2 mb-4"
            >
              {issues.map((issue, i) => (
                <motion.div
                  key={i}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: i * 0.1 }}
                  className={`flex items-start gap-3 p-3 rounded-lg border ${
                    issue.severity === "critical"
                      ? "bg-cyber-red/5 border-cyber-red/20"
                      : "bg-cyber-amber/5 border-cyber-amber/20"
                  }`}
                >
                  <span className={`status-dot mt-1 ${
                    issue.severity === "critical" ? "bg-cyber-red" : "bg-cyber-amber"
                  }`} />
                  <div>
                    <p className={`text-sm font-medium ${
                      issue.severity === "critical" ? "text-cyber-red" : "text-cyber-amber"
                    }`}>
                      {issue.severity === "critical" ? "Structural Scramble" : "System Warning"}
                    </p>
                    <p className="text-xs text-gray-400 mt-0.5">{issue.message}</p>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Keywords found */}
        {keywords.length > 0 && (
          <div>
            <span className="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-2 block">
              Detected Keywords
            </span>
            <div className="flex flex-wrap gap-1.5">
              {keywords.map((kw, i) => (
                <motion.span
                  key={kw}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: i * 0.05 }}
                  className="px-2 py-0.5 rounded bg-cyber-green/10 text-cyber-green border border-cyber-green/20 text-[11px] font-mono"
                >
                  {kw}
                </motion.span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
