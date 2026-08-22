import { CROWS, TREES, BUSHES, GRASS, PEACOCKS, BUTTERFLIES, LOTUS, FIREFLIES, FLOCK } from "./landingData";

function Parrot({ x, y, flip = 1 }: { x: number; y: number; flip?: number }) {
  const s = flip < 0 ? -1 : 1;
  return (
    <g transform={`translate(${x},${y}) scale(${s},1)`} filter="url(#landShadow)">
      <path
        d="M-7 -9 C -3 -14, 1 -15, 5 -11 C 9 -7, 7 -1 1 2 C -7 1 -9 -3 -7 -2 C -11 -1 -13 3 -7 3 C -11 4 -13 8 -7 9 C -4 10 0 9 0 9"
        fill="url(#parrotG)"
      />
      <circle cx="7" cy="0" r="8" fill="url(#parrotG)" />
      <ellipse cx="15" cy="-3" rx="5" ry="7" fill="url(#parrotWing)" />
      <path d="M17 -11 C 20 -8, 24 -3, 17 -1 C 21 -2, 25 -4, 29 -2" fill="#EA8E3D" />
      <circle cx="31" cy="-7" r="2.8" fill="#EA8E3D" />
      <circle cx="32" cy="-8" r="1.1" fill="#7C2D12" />
      <circle cx="13" cy="-12" r="2.8" fill="#1E2937" />
      <circle cx="14" cy="-12" r="1.2" fill="#334155" />
    </g>
  );
}

function Crow({ x, y, flip = 1 }: { x: number; y: number; flip?: number }) {
  const s = flip < 0 ? -1 : 1;
  return (
    <g transform={`translate(${x},${y}) scale(${s},1)`} filter="url(#landShadow)">
      <path d="M-10 0 C -5 -8, 5 -9, 9 -3 C 9 -3, 5 -1, 0 2 C -9 2 -12 1 -10 0" fill="url(#crowG)" />
      <path d="M-3 0 C 2 -5, 9 -6, 10 -1 C 9 -1 5 -1 0 1 C -5 1 -8 0 -3 0" fill="url(#crowG)" />
      <circle cx="8" cy="-6" r="1.8" fill="#D1D5DB" opacity="0.85" />
      <path d="M-6 3 C -7 5, -4 6, -5 8" stroke="#111827" strokeWidth="1.6" strokeLinecap="round" />
    </g>
  );
}

function ChristmasTree({ x, y, scale = 1 }: { x: number; y: number; scale?: number }) {
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`}>
      <polygon points="0,-18 -8,-4 8,-4" fill="#1A6B3A" />
      <polygon points="0,-12 -10,6 10,6" fill="#2E6B35" />
      <polygon points="0,-6 -11,10 11,10" fill="#3F7A47" />
      <rect x="-1.5" y="10" width="3" height="7" fill="#B98A5E" />
      <circle cx="-7" cy="-8" r="2" fill="#FACC15" />
      <circle cx="6" cy="-10" r="2" fill="#FACC15" />
      <circle cx="0" cy="2" r="2" fill="#FACC15" />
      <circle cx="6" cy="4" r="1.6" fill="#EF4444" />
      <circle cx="-5" cy="5" r="1.6" fill="#EF4444" />
    </g>
  );
}

function GrassTuft({ x, y }: { x: number; y: number }) {
  return (
    <path
      d={`M${x} ${y} C ${x - 1.5} ${y - 8}, ${x + 1.5} ${y - 12}, ${x} ${y - 6} C ${x - 1} ${y - 7}, ${x + 1} ${y - 9}, ${x} ${y - 6}`}
      fill="#4F8F57"
      opacity="0.75"
    />
  );
}

function Peacock({ x, y, scale = 1 }: { x: number; y: number; scale?: number }) {
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`} filter="url(#landShadow)">
      <circle cx="0" cy="0" r="9" fill="url(#peacockG)" />
      <circle cx="-3" cy="-2" r="3.2" fill="#111827" />
      <path d="M4 -1 C 8 -3, 12 1, 10 4 C 12 5, 14 7, 12 9 C 10 11, 6 9 4 7 C 2 9 0 10 -2 9 C -6 11 -8 7 -6 6 C -8 5 -6 1 -4 0 C -4 -2 -1 -3 0 0" fill="url(#peacockG)" />
      <line x1="-10" y1="6" x2="-22" y2="-2" stroke="#155E75" strokeWidth="2.8" strokeLinecap="round" />
      <path
        d="M-18 -2 C -26 -10, -16 -16, -10 -8"
        fill="none"
        stroke="#38BDF8"
        strokeWidth="4"
        strokeLinecap="round"
      />
      <g transform="translate(-6,10)">
        <path d="M0 0 A 22 22 0 0 1 44 0 A 22 22 0 0 1 0 0" fill="#38BDF8" opacity="0.8" />
        <path d="M0 0 A 18 18 0 0 0 36 0 A 18 18 0 0 0 0 0" fill="#0EA5E9" />
      </g>
      <circle cx="6" cy="4" r="4" fill="url(#peacockEye)" />
      <circle cx="14" cy="6" r="2.6" fill="url(#peacockEye)" />
      <circle cx="4" cy="10" r="2.6" fill="url(#peacockEye)" />
      <circle cx="12" cy="10" r="2" fill="url(#peacockEye)" />
    </g>
  );
}

function Butterfly({ x, y, scale = 1, color = "#0EA5E9", className = "" }: { x: number; y: number; scale?: number; color?: string; className?: string }) {
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`} className={className} filter="url(#landShadow)">
      <path d="M0 0 C -8 -9, -17 -7, -11 -1 C -17 5, -7 7, 0 0" fill={color} opacity="0.9" />
      <path d="M0 0 C 8 -9, 17 -7, 11 -1 C 17 5, 7 7, 0 0" fill={color} opacity="0.9" />
      <ellipse cx="0" cy="0" rx="2.8" ry="1.3" fill="#111827" />
      <ellipse cx="-2" cy="-2" rx="0.9" ry="0.4" fill="#fff" opacity="0.7" />
    </g>
  );
}

function Lotus({ x, y, scale = 1 }: { x: number; y: number; scale?: number }) {
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`} filter="url(#landShadow)">
      <path d="M0 0 C -4 -3, -7 2, -2 5 C 0 6, 3 2, 0 0" fill="url(#lotusG)" />
      <path d="M0 0 C 4 -3, 7 2, 2 5 C 0 6, -3 2, 0 0" fill="url(#lotusG)" />
      <path d="M0 0 C -4 3, -7 8, -2 10 C 0 11, 3 7, 0 0" fill="url(#lotusG)" />
      <path d="M0 0 C 5 -1, 9 4, 4 8 C 2 9, -1 8, 0 0" fill="url(#lotusG)" />
      <circle cx="0" cy="0" r="3" fill="#FBBF24" />
      <circle cx="0" cy="0" r="1.6" fill="#F2F0EA" />
    </g>
  );
}

function Firefly({ x, y, scale = 1 }: { x: number; y: number; scale?: number }) {
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`} className="meadow-animate-float">
      <circle cx="0" cy="0" r="2.4" fill="#FBBF24" opacity="0.85" />
      <circle cx="0" cy="0" r="6" fill="#FBBF24" opacity="0.25" />
    </g>
  );
}

function Rainbow({ x = 830, y = 120, scale = 1 }: { x?: number; y?: number; scale?: number }) {
  const stops = [
    { c: "#EF4444", r: 110 },
    { c: "#F97316", r: 100 },
    { c: "#FACC15", r: 90 },
    { c: "#10B981", r: 80 },
    { c: "#0EA5E9", r: 70 },
    { c: "#8B5CF6", r: 60 },
    { c: "#EC4899", r: 50 },
  ];
  return (
    <g transform={`translate(${x},${y}) scale(${scale})`} opacity="0.85">
      {stops.map((s) => (
        <path
          key={s.c}
          d={`M${-s.r} 0 A ${s.r} ${s.r} 0 0 1 ${s.r} 0`}
          fill="none"
          stroke={s.c}
          strokeWidth="7"
          strokeLinecap="round"
          opacity="0.85"
        />
      ))}
      <path d="M-108 0 L-120 0" stroke="#CBD5E1" strokeWidth="2" />
      <path d="M108 0 L120 0" stroke="#CBD5E1" strokeWidth="2" />
    </g>
  );
}

function Bush({ y, scale = 1, colors }: { y: number; scale?: number; colors: string[] }) {
  return (
    <g transform={`translate(28,${y}) scale(${scale})`}>
      <circle cx="0" cy="0" r="9" fill={colors[0]} opacity="0.9" />
      <circle cx="-7" cy="4" r="7" fill={colors[1]} />
      <circle cx="7" cy="5" r="8" fill={colors[2]} opacity="0.85" />
    </g>
  );
}

export default function ValleyScene() {
  return (
    <svg
      viewBox="0 0 1200 460"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
      className="block h-52 w-full sm:h-auto"
      role="img"
    >
      <defs>
        <linearGradient id="vsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#FDFBF2" />
          <stop offset="100%" stopColor="#F4F1E4" />
        </linearGradient>
        <linearGradient id="vsea" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#B9DBE6" />
          <stop offset="100%" stopColor="#87C4D6" />
        </linearGradient>
        <linearGradient id="parrotG" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#2E9559" />
          <stop offset="100%" stopColor="#125E3B" />
        </linearGradient>
        <linearGradient id="parrotWing" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38B2AC" />
          <stop offset="100%" stopColor="#0D7A66" />
        </linearGradient>
        <linearGradient id="peacockG" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#155E75" />
        </linearGradient>
        <linearGradient id="peacockEye" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#EAB318" />
          <stop offset="40%" stopColor="#FACC15" />
          <stop offset="100%" stopColor="#7C2D12" />
        </linearGradient>
        <radialGradient id="crowG" cx="0.4" cy="0.35" r="1">
          <stop offset="0%" stopColor="#D1D5DB" />
          <stop offset="100%" stopColor="#111827" />
        </radialGradient>
        <radialGradient id="lotusG" cx="0.4" cy="0.3" r="1">
          <stop offset="0%" stopColor="#F8FAFC" />
          <stop offset="100%" stopColor="#87C4D6" />
        </radialGradient>
        <filter id="landShadow" x="-60%" y="-60%" width="220%" height="280%">
          <feDropShadow dx="0" dy="3" stdDeviation="3" floodOpacity="0.25" />
        </filter>
      </defs>

      <rect width="1200" height="460" fill="url(#vsky)" />

      <circle cx="1015" cy="96" r="72" fill="#F7E6A8" opacity="0.35" />
      <circle cx="1015" cy="96" r="46" fill="#F5E2A2" />

      <g className="meadow-animate-drift" style={{ animationDuration: "26s" }}>
        <ellipse cx="160" cy="84" rx="52" ry="17" fill="#FFFFFF" opacity="0.95" />
        <ellipse cx="200" cy="76" rx="34" ry="13" fill="#FFFFFF" opacity="0.9" />
        <ellipse cx="128" cy="79" rx="30" ry="12" fill="#FFFFFF" opacity="0.9" />
      </g>
      <g className="meadow-animate-drift" style={{ animationDuration: "38s" }}>
        <ellipse cx="560" cy="60" rx="44" ry="14" fill="#FFFFFF" opacity="0.8" />
        <ellipse cx="596" cy="54" rx="30" ry="11" fill="#FFFFFF" opacity="0.75" />
      </g>

      <Rainbow x={820} y={120} />

      {CROWS.map((c) => (
        <Crow key={c.x} x={c.x} y={c.y} flip={c.flip} />
      ))}

      <path
        d="M780 215 C 830 195, 900 205, 970 175 C 1040 145, 1120 165, 1200 145 L1200 190 A60 60 0 0 1 1150 195 C 1080 185, 1000 200, 920 185 C 850 170, 790 195, 780 205 Z"
        fill="url(#vsea)"
        opacity="0.92"
      />

      {FLOCK.map((x) => (
        <Crow key={x} x={x} y={64} flip={x % 2 === 0 ? 1 : -1} />
      ))}

      {PEACOCKS.map((p) => (
        <Peacock key={p.x} x={p.x} y={p.y} scale={p.s} />
      ))}

      {LOTUS.map((l) => (
        <Lotus key={l.x} x={l.x} y={l.y} scale={l.s} />
      ))}

      {BUTTERFLIES.map((b) => (
        <Butterfly key={b.x} x={b.x} y={b.y} scale={b.s} color={b.c} className="meadow-animate-float" />
      ))}

      {FIREFLIES.map((x, i) => (
        <Firefly key={x} x={x} y={280 + (i % 3) * 24} scale={0.7 + (i % 3) * 0.2} />
      ))}

      <path
        d="M0 300 C 180 250, 300 255, 420 285 C 560 320, 700 300, 840 320 C 960 336, 1080 316, 1200 330 L1200 460 L0 460 Z"
        fill="#DCEED2"
      />

      <path
        d="M980 210 C 930 280, 1010 330, 960 460"
        fill="none"
        stroke="#B9DBE6"
        strokeWidth="30"
        strokeLinecap="round"
      />
      <path
        d="M980 210 C 930 280, 1010 330, 960 460"
        fill="none"
        stroke="#D2E8F0"
        strokeWidth="14"
        strokeLinecap="round"
      />

      <path
        d="M0 380 C 220 330, 420 350, 620 372 C 820 394, 1020 368, 1200 390 L1200 460 L0 460 Z"
        fill="#C6E1B6"
      />

      {TREES.map((t) => (
        <ChristmasTree key={t.x} x={t.x} y={t.y} scale={t.s} />
      ))}

      {GRASS.map((x) => (
        <GrassTuft key={x} x={x} y={378} />
      ))}

      {BUSHES.map((b) => (
        <Bush key={b.x} y={b.y} scale={b.s} colors={b.c} />
      ))}

      <g transform="translate(620,250)">
        <rect x="4" y="20" width="9" height="22" rx="2" fill="#B98A5E" />
        <circle cx="9" cy="10" r="20" fill="#7BB661" />
        <circle cx="0" cy="17" r="13" fill="#4F8F57" />
        <circle cx="18" cy="15" r="14" fill="#92C276" />
      </g>
      <g transform="translate(720,268)">
        <rect x="4" y="16" width="8" height="18" rx="2" fill="#B98A5E" />
        <circle cx="8" cy="9" r="16" fill="#5B9A62" />
        <circle cx="-2" cy="14" r="10" fill="#7BB661" />
      </g>

      <path
        d="M150 320 C 240 340, 320 308, 430 348 C 540 388, 600 360, 740 402"
        fill="none"
        stroke="#EFE7D3"
        strokeWidth="26"
        strokeLinecap="round"
      />
      <path
        d="M150 320 C 240 340, 320 308, 430 348 C 540 388, 600 360, 740 402"
        fill="none"
        stroke="#E0D3B6"
        strokeWidth="3"
        strokeDasharray="10 14"
        strokeLinecap="round"
        opacity="0.9"
      />

      <g>
        <rect x="118" y="252" width="40" height="30" rx="3" fill="#FFF9E9" stroke="#E4D6B4" strokeWidth="1.5" />
        <polygon points="112,252 138,234 164,252" fill="#E9C78F" />
        <rect x="128" y="262" width="6" height="8" rx="1" fill="#A97D5B" />
        <rect x="142" y="262" width="6" height="8" rx="1" fill="#A97D5B" />

        <rect x="252" y="246" width="36" height="34" rx="3" fill="#FFF9E9" stroke="#E4D6B4" strokeWidth="1.5" />
        <polygon points="246,246 270,226 294,246" fill="#F2D9A6" />
        <rect x="262" y="258" width="7" height="9" rx="1" fill="#A97D5B" />
        <rect x="272" y="258" width="7" height="9" rx="1" fill="#A97D5B" />

        <rect x="192" y="262" width="32" height="26" rx="3" fill="#FDF6E3" stroke="#E4D6B4" strokeWidth="1.5" />
        <polygon points="188,262 208,246 228,262" fill="#E9C78F" />
        <rect x="204" y="270" width="7" height="9" rx="1" fill="#A97D5B" />
      </g>

      <path d="M158 118 Q 170 108 182 118 Q 194 108 206 118" fill="none" stroke="#8A9B7E" strokeWidth="2.5" strokeLinecap="round" />
      <path d="M220 98 Q 229 90 238 98 Q 247 90 256 98" fill="none" stroke="#8A9B7E" strokeWidth="2" strokeLinecap="round" opacity="0.85" />

      <g className="meadow-animate-swing" style={{ animationDuration: "18s" }}>
        <path
          d="M210 170 C 255 145, 300 140, 345 150 C 390 160, 430 188, 460 218"
          fill="none"
          stroke="#B98A5E"
          strokeWidth="5"
          strokeLinecap="round"
        />
        <path
          d="M212 170 C 255 145, 300 140, 345 150 C 390 160, 430 188, 460 218"
          fill="none"
          stroke="#A67C4A"
          strokeWidth="2.2"
          strokeLinecap="round"
        />
      </g>
      <g className="meadow-animate-swing" style={{ animationDuration: "18s", animationDelay: "1s" }}>
        <Parrot x={335} y={150} flip={-1} />
      </g>
      <g className="meadow-animate-swing" style={{ animationDuration: "18s", animationDelay: "2s" }}>
        <Parrot x={390} y={178} flip={1} />
      </g>

      <g className="meadow-animate-float" style={{ animationDuration: "9s" }}>
        <ellipse cx="860" cy="300" rx="5" ry="9" fill="#5B9A62" transform="rotate(28 860 300)" opacity="0.8" />
      </g>
      <g className="meadow-animate-float" style={{ animationDuration: "11s" }}>
        <ellipse cx="300" cy="180" rx="4" ry="8" fill="#7BB661" transform="rotate(-20 300 180)" opacity="0.75" />
      </g>
      <g className="meadow-animate-float" style={{ animationDuration: "13s" }}>
        <ellipse cx="690" cy="150" rx="4" ry="8" fill="#92C276" transform="rotate(40 690 150)" opacity="0.7" />
      </g>

      <circle cx="340" cy="332" r="4" fill="#F2B8C6" />
      <circle cx="368" cy="344" r="3" fill="#F5D48A" />
      <circle cx="508" cy="372" r="4" fill="#F2B8C6" />
      <circle cx="470" cy="368" r="3" fill="#FFFFFF" opacity="0.9" />
      <circle cx="640" cy="398" r="4" fill="#F5D48A" />
      <circle cx="820" cy="396" r="3.5" fill="#F2B8C6" />
    </svg>
  );
}
