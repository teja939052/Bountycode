import { motion } from "framer-motion";

export default function HoloPanel({
  title,
  subtitle,
  status = "online",
  statusLabel,
  glowColor = "blue",
  children,
  className = "",
  noPad = false,
}) {
  const glowMap = {
    blue: "border-cyber-blue/20 shadow-cyber-blue",
    purple: "border-cyber-purple/20 shadow-cyber-purple",
    green: "border-cyber-green/20 shadow-cyber-green",
  };

  const statusColors = {
    online: "status-online",
    processing: "status-processing",
    warning: "status-warning",
    offline: "w-2 h-2 rounded-full bg-gray-600",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`relative overflow-hidden rounded-xl bg-space-panel/80 border ${glowMap[glowColor] || glowMap.blue} ${className}`}
    >
      {/* Ambient grid background */}
      <div className="absolute inset-0 ambient-grid opacity-30 pointer-events-none" />

      {/* Scan line effect */}
      <div className="absolute inset-0 scan-line pointer-events-none" />

      {/* Header */}
      {(title || subtitle) && (
        <div className="relative z-10 flex justify-between items-center px-6 py-4 border-b border-space-border">
          <div>
            {subtitle && (
              <span className="text-[10px] font-mono text-cyber-blue/70 tracking-widest uppercase block">
                {subtitle}
              </span>
            )}
            {title && (
              <h3 className="text-lg font-display font-bold text-text-primary tracking-tight">
                {title}
              </h3>
            )}
          </div>
          {statusLabel && (
            <div className="flex items-center gap-2">
              <span className={statusColors[status] || statusColors.online} />
              <span className="text-[10px] font-mono uppercase tracking-wider text-gray-400">
                {statusLabel}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Content */}
      <div className={`relative z-10 ${noPad ? "" : "p-6"}`}>
        {children}
      </div>
    </motion.div>
  );
}
