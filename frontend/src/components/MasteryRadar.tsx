import { useMemo } from "react";
import { motion } from "framer-motion";

interface Dimension {
  name: string;
  icon: string;
  score: number;
  attempts: number;
}

interface MasteryRadarProps {
  dimensions: Record<string, Dimension>;
  overall: number;
  size?: number;
  showLabels?: boolean;
}

const DIM_ORDER = ["understanding", "prediction", "coding", "debugging"];
const DIM_COLORS: Record<string, string> = {
  understanding: "#3B82F6",
  prediction: "#A855F7",
  coding: "#22C55E",
  debugging: "#EF4444",
};

export default function MasteryRadar({ dimensions, overall, size = 200, showLabels = true }: MasteryRadarProps) {
  const center = size / 2;
  const radius = size * 0.38;
  const angleStep = (Math.PI * 2) / DIM_ORDER.length;

  const points = useMemo(() => {
    return DIM_ORDER.map((key, i) => {
      const angle = angleStep * i - Math.PI / 2;
      const dim = dimensions[key];
      const score = dim?.score || 0;
      const r = (score / 100) * radius;
      return {
        key,
        label: dim?.name || key,
        icon: dim?.icon || "",
        score,
        attempts: dim?.attempts || 0,
        x: center + r * Math.cos(angle),
        y: center + r * Math.sin(angle),
        labelX: center + (radius + 24) * Math.cos(angle),
        labelY: center + (radius + 24) * Math.sin(angle),
        color: DIM_COLORS[key] || "#999",
      };
    });
  }, [dimensions, center, radius, angleStep]);

  const gridLevels = [25, 50, 75, 100];

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {gridLevels.map((level) => {
          const r = (level / 100) * radius;
          const pts = DIM_ORDER.map((_, i) => {
            const angle = angleStep * i - Math.PI / 2;
            return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
          }).join(" ");
          return (
            <polygon key={level} points={pts} fill="none" stroke="#ffffff11" strokeWidth={1} />
          );
        })}

        {DIM_ORDER.map((_, i) => {
          const angle = angleStep * i - Math.PI / 2;
          return (
            <line key={i} x1={center} y1={center}
              x2={center + radius * Math.cos(angle)} y2={center + radius * Math.sin(angle)}
              stroke="#ffffff08" strokeWidth={1} />
          );
        })}

        <motion.polygon
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          points={points.map((p) => `${p.x},${p.y}`).join(" ")}
          fill="#22C55E18" stroke="#22C55E66" strokeWidth={2}
        />

        {points.map((p) => (
          <motion.circle key={p.key} cx={p.x} cy={p.y} r={4}
            initial={{ scale: 0 }} animate={{ scale: 1 }}
            transition={{ delay: 0.3, duration: 0.3 }}
            fill={p.color} stroke="#000" strokeWidth={2} />
        ))}

        {showLabels && points.map((p) => (
          <text key={`label-${p.key}`} x={p.labelX} y={p.labelY}
            textAnchor="middle" dominantBaseline="middle"
            fill="#9CA3AF" fontSize={10} fontFamily="monospace">
            {p.icon} {Math.round(p.score)}
          </text>
        ))}
      </svg>

      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="text-center">
          <p className="text-2xl font-black text-white">{Math.round(overall)}%</p>
          <p className="text-[9px] font-mono text-gray-500 uppercase">Mastery</p>
        </div>
      </div>
    </div>
  );
}
