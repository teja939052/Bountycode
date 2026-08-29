import { ReactNode } from "react";
import { Link } from "react-router-dom";
import {
  Home,
  Code2,
  FileText,
  Target,
  GraduationCap,
  ListChecks,
  Terminal,
  BookOpen,
  Network,
  Trophy,
  Flame,
  Zap,
} from "lucide-react";

export const LC = {
  bg: "#0f0f0f",
  panel: "#171717",
  panel2: "#1f1f1f",
  border: "#2a2a2a",
  hover: "#242424",
  text: "#e9e9e9",
  muted: "#9a9a9a",
  faint: "#6b6b6b",
  brand: "#ffa116",
  easy: "#00b8a3",
  medium: "#ffc01e",
  hard: "#ff375f",
  green: "#2eb88a",
  blue: "#3b82f6",
};

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: Home },
  { to: "/interview", label: "Mock Interviews", icon: Code2 },
  { to: "/resume", label: "Resume Builder", icon: FileText },
  { to: "/ats", label: "ATS Optimizer", icon: Target },
  { to: "/aptitude", label: "Aptitude Tests", icon: GraduationCap },
  { to: "/company-prep", label: "Company Prep", icon: Network },
  { to: "/question-bank", label: "Problems", icon: ListChecks },
  { to: "/compiler", label: "Compiler", icon: Terminal },
  { to: "/learning", label: "Learning Hub", icon: BookOpen },
  { to: "/system-design", label: "System Design", icon: Network },
];

export function LNav() {
  return (
    <aside className="hidden lg:flex w-56 shrink-0 sticky top-0 h-screen flex-col border-r border-[#2a2a2a] bg-[#121212] py-5 px-3">
      <div className="flex items-center gap-2 px-2 mb-6">
        <div className="h-7 w-7 rounded-md bg-[#ffa116] flex items-center justify-center text-black font-black text-sm">
          P
        </div>
        <span className="text-sm font-bold text-[#e9e9e9] tracking-tight">
          PlacementPro
        </span>
      </div>
      <nav className="flex-1 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.to}
              to={item.to}
              className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-[#9a9a9a] hover:bg-[#242424] hover:text-[#e9e9e9] transition-colors"
            >
              <Icon size={16} className="shrink-0" />
              <span className="truncate">{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="mt-4 px-3 text-[11px] text-[#6b6b6b] leading-relaxed">
        Practice daily. Climb the leaderboard. Land the offer.
      </div>
    </aside>
  );
}

export function LCard({
  children,
  className = "",
  padded = true,
}: {
  children: ReactNode;
  className?: string;
  padded?: boolean;
}) {
  return (
    <div
      className={`rounded-xl border border-[#2a2a2a] bg-[#171717] ${
        padded ? "p-5" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}

export function LSectionTitle({
  title,
  icon,
  action,
}: {
  title: string;
  icon?: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2 text-[#e9e9e9] font-semibold text-[15px]">
        {icon}
        {title}
      </div>
      {action}
    </div>
  );
}

export function LStat({
  label,
  value,
  accent,
  sub,
}: {
  label: string;
  value: ReactNode;
  accent?: string;
  sub?: string;
}) {
  return (
    <LCard className="p-4">
      <div className="text-[11px] text-[#9a9a9a] uppercase tracking-wide">
        {label}
      </div>
      <div
        className="mt-1.5 text-2xl font-bold leading-none"
        style={{ color: accent || LC.text }}
      >
        {value}
      </div>
      {sub && <div className="text-[11px] text-[#6b6b6b] mt-1.5">{sub}</div>}
    </LCard>
  );
}

export function DifficultyBadge({ level }: { level?: string }) {
  const map: Record<string, { color: string; label: string }> = {
    easy: { color: LC.easy, label: "Easy" },
    medium: { color: LC.medium, label: "Medium" },
    hard: { color: LC.hard, label: "Hard" },
  };
  const key = (level || "").toLowerCase();
  const d = map[key] || map.medium;
  return (
    <span
      style={{ color: d.color }}
      className="text-[13px] font-medium whitespace-nowrap"
    >
      {d.label}
    </span>
  );
}

export function ProgressRing({
  value,
  size = 132,
  stroke = 11,
  color = LC.brand,
  label,
  sublabel,
}: {
  value: number;
  size?: number;
  stroke?: number;
  color?: string;
  label?: ReactNode;
  sublabel?: string;
}) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - Math.min(100, Math.max(0, value)) / 100);
  return (
    <div
      className="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke="#2a2a2a"
          strokeWidth={stroke}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={color}
          strokeWidth={stroke}
          fill="none"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <div className="text-2xl font-bold text-[#e9e9e9]">
          {label ?? `${Math.round(value)}%`}
        </div>
        {sublabel && (
          <div className="text-[10px] text-[#9a9a9a] mt-0.5">{sublabel}</div>
        )}
      </div>
    </div>
  );
}

export function Pill({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: "neutral" | "brand" | "green" | "red";
}) {
  const tones: Record<string, string> = {
    neutral: "bg-[#242424] text-[#9a9a9a]",
    brand: "bg-[#ffa1161a] text-[#ffa116]",
    green: "bg-[#2eb88a1a] text-[#2eb88a]",
    red: "bg-[#ff375f1a] text-[#ff375f]",
  };
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[11px] font-medium ${tones[tone]}`}
    >
      {children}
    </span>
  );
}

const HEAT_COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"];

export function Heatmap({
  weeks = 16,
  data,
}: {
  weeks?: number;
  data?: number[];
}) {
  const cells =
    data && data.length === weeks * 7
      ? data
      : Array.from({ length: weeks * 7 }, () =>
          Math.floor(Math.random() * 5)
        );
  const columns: number[][] = [];
  for (let w = 0; w < weeks; w++) {
    columns.push(cells.slice(w * 7, w * 7 + 7));
  }
  return (
    <div className="overflow-x-auto">
      <div className="flex gap-[3px]">
        {columns.map((col, i) => (
          <div key={i} className="flex flex-col gap-[3px]">
            {col.map((v, j) => (
              <div
                key={j}
                title={`${v} sessions`}
                className="h-[11px] w-[11px] rounded-[2px]"
                style={{ backgroundColor: HEAT_COLORS[v] }}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="flex items-center gap-1.5 mt-2 text-[10px] text-[#6b6b6b]">
        <span>Less</span>
        {HEAT_COLORS.map((c) => (
          <span
            key={c}
            className="h-[10px] w-[10px] rounded-[2px]"
            style={{ backgroundColor: c }}
          />
        ))}
        <span>More</span>
      </div>
    </div>
  );
}

export function SkillRadar({
  skills,
  size = 208,
}: {
  skills: { label: string; value: number }[];
  size?: number;
}) {
  const cx = size / 2;
  const cy = size / 2;
  const R = size / 2 - 28;
  const n = skills.length;
  const angleAt = (i: number) => (Math.PI * 2 * i) / n - Math.PI / 2;
  const pointAt = (i: number, r: number) => [
    cx + Math.cos(angleAt(i)) * R * (r / 100),
    cy + Math.sin(angleAt(i)) * R * (r / 100),
  ];
  const gridLevels = [25, 50, 75, 100];
  const dataPoly = skills
    .map((s, i) => pointAt(i, s.value).join(","))
    .join(" ");

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="max-w-full">
        {gridLevels.map((lvl) => (
          <polygon
            key={lvl}
            points={skills
              .map((_, i) => pointAt(i, lvl).join(","))
              .join(" ")}
            fill="none"
            stroke="#2a2a2a"
            strokeWidth={1}
          />
        ))}
        {skills.map((_, i) => {
          const [x, y] = pointAt(i, 100);
          return (
            <line
              key={i}
              x1={cx}
              y1={cy}
              x2={x}
              y2={y}
              stroke="#2a2a2a"
              strokeWidth={1}
            />
          );
        })}
        <polygon
          points={dataPoly}
          fill="rgba(255,161,22,0.22)"
          stroke="#ffa116"
          strokeWidth={2}
        />
        {skills.map((s, i) => {
          const [x, y] = pointAt(i, s.value);
          return <circle key={i} cx={x} cy={y} r={3} fill="#ffa116" />;
        })}
        {skills.map((s, i) => {
          const [x, y] = pointAt(i, 118);
          return (
            <text
              key={i}
              x={x}
              y={y}
              fill="#9a9a9a"
              fontSize={10}
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {s.label}
            </text>
          );
        })}
      </svg>
    </div>
  );
}

export function Chip({
  icon,
  children,
  tone = "neutral",
}: {
  icon?: ReactNode;
  children: ReactNode;
  tone?: "neutral" | "brand" | "green" | "red";
}) {
  const tones: Record<string, string> = {
    neutral: "border-[#2a2a2a] text-[#9a9a9a]",
    brand: "border-[#ffa11655] text-[#ffa116]",
    green: "border-[#2eb88a55] text-[#2eb88a]",
    red: "border-[#ff375f55] text-[#ff375f]",
  };
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium ${tones[tone]}`}
    >
      {icon}
      {children}
    </span>
  );
}

export const LIcon = { Trophy, Flame, Zap };
