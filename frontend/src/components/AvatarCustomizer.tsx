import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Check, ChevronLeft, ChevronRight } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const BG_COLORS = [
  { name: "indigo", class: "from-indigo-500 to-indigo-600" },
  { name: "emerald", class: "from-emerald-500 to-emerald-600" },
  { name: "amber", class: "from-amber-500 to-amber-600" },
  { name: "rose", class: "from-rose-500 to-rose-600" },
  { name: "cyan", class: "from-cyan-500 to-cyan-600" },
  { name: "violet", class: "from-violet-500 to-violet-600" },
  { name: "teal", class: "from-teal-500 to-teal-600" },
  { name: "orange", class: "from-orange-500 to-orange-600" },
  { name: "pink", class: "from-pink-500 to-pink-600" },
  { name: "blue", class: "from-blue-500 to-blue-600" },
  { name: "purple", class: "from-purple-500 to-purple-600" },
  { name: "slate", class: "from-slate-500 to-slate-600" },
];

const BORDER_STYLES = [
  { name: "None", class: "border-0" },
  { name: "Glow", class: "border-2 border-indigo-400 shadow-[0_0_12px_rgba(99,102,241,0.5)]" },
  { name: "Pixel", class: "border-2 border-white rounded-none" },
  { name: "Gradient", class: "border-2 border-transparent bg-gradient-to-br from-indigo-400 to-amber-400 bg-clip-padding p-[2px]" },
];

const AVATAR_EMOJIS = [
  "💻", "🚀", "⚡", "🎯", "🔥", "💡", "🎮", "🏆", "🛡️", "⚔️",
  "📚", "🧠", "🎨", "🔧", "⭐", "🌟", "💎", "🧩", "🎪", "🎭",
  "🎲", "🎸", "🎹", "🎧", "🎤", "🏅", "📈", "📊", "🗺️", "🔬",
  "🤖", "👾", "🦄", "🌈", "🍀", "🌊",
];

const SHAPE_STYLES = [
  { name: "Circle", class: "rounded-full" },
  { name: "Square", class: "rounded-xl" },
  { name: "Rounded", class: "rounded-2xl" },
];

const INITIAL_COLORS = ["#6366f1", "#10b981", "#f59e0b", "#f43f5e", "#06b6d4", "#8b5cf6"];

const PREVIEW_SIZES = [
  { label: "Navbar", size: "w-8 h-8", textSize: "text-xs", fontSize: 14 },
  { label: "Profile", size: "w-14 h-14", textSize: "text-lg", fontSize: 24 },
  { label: "Feed", size: "w-24 h-24", textSize: "text-3xl", fontSize: 40 },
];

function PixelGrid({ value, onChange }) {
  const grid = value || Array.from({ length: 8 }, () => Array(8).fill(false));

  const toggle = (row, col) => {
    const next = grid.map((r, ri) =>
      r.map((c, ci) => (ri === row && ci === col ? !c : c))
    );
    onChange(next);
  };

  return (
    <div className="flex flex-col items-center gap-1">
      <p className="text-xs text-gray-400 mb-1">Click to toggle pixels (8x8)</p>
      <div className="bg-gray-800 p-2 rounded-xl inline-block">
        {grid.map((row, ri) => (
          <div key={ri} className="flex gap-0.5">
            {row.map((col, ci) => (
              <button
                key={ci}
                type="button"
                className={`w-5 h-5 border transition-colors ${
                  col
                    ? "bg-indigo-400 border-indigo-500 shadow-[0_0_4px_rgba(99,102,241,0.5)]"
                    : "bg-gray-700/50 border-gray-600/30 hover:bg-gray-600/50"
                }`}
                onClick={() => toggle(ri, ci)}
                aria-label={`Pixel ${ri},${ci}`}
              />
            ))}
          </div>
        ))}
      </div>
      <button
        type="button"
        className="text-xs text-gray-400 hover:text-white mt-1 transition-colors"
        onClick={() => onChange(Array.from({ length: 8 }, () => Array(8).fill(false)))}
      >
        Clear
      </button>
    </div>
  );
}

function drawPixelAvatar(grid, size) {
  if (!grid || grid.length === 0) return null;
  const pixelSize = Math.floor(size / 8);
  const canvas = [];
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if (grid[r]?.[c]) {
        canvas.push(
          <div
            key={`${r}-${c}`}
            className="absolute bg-indigo-400"
            style={{
              width: pixelSize,
              height: pixelSize,
              left: c * pixelSize,
              top: r * pixelSize,
            }}
          />
        );
      }
    }
  }
  return canvas;
}

export default function AvatarCustomizer({ open, onClose, onSave, currentAvatar }) {
  const reduced = useReducedMotion();
  const [tab, setTab] = useState("style");
  const [shape, setShape] = useState(currentAvatar?.shape || 0);
  const [border, setBorder] = useState(currentAvatar?.border || 0);
  const [bgColor, setBgColor] = useState(currentAvatar?.bgColor || 0);
  const [mode, setMode] = useState(currentAvatar?.mode || "initials");
  const [initialsColor, setInitialsColor] = useState(currentAvatar?.initialsColor || 0);
  const [emoji, setEmoji] = useState(currentAvatar?.emoji || 0);
  const [pixelGrid, setPixelGrid] = useState(currentAvatar?.pixelGrid || null);
  const [initials, setInitials] = useState(currentAvatar?.initials || "U");

  const handleSave = useCallback(() => {
    const avatar = { shape, border, bgColor, mode, initialsColor, emoji, pixelGrid, initials };
    onSave?.(avatar);
    onClose?.();
  }, [shape, border, bgColor, mode, initialsColor, emoji, pixelGrid, initials, onSave, onClose]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === "Escape") onClose?.();
  }, [onClose]);

  useEffect(() => {
    if (open) window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, handleKeyDown]);

  if (!open) return null;

  const renderAvatar = (sizeClass, textSizeClass, fontSize) => {
    const bg = BG_COLORS[bgColor] || BG_COLORS[0];
    const borderStyle = BORDER_STYLES[border] || BORDER_STYLES[0];
    const shapeClass = SHAPE_STYLES[shape]?.class || SHAPE_STYLES[0].class;

    if (mode === "pixel" && pixelGrid) {
      const hasPixels = pixelGrid.some(row => row.some(c => c));
      if (hasPixels) {
        const sizeNum = fontSize * 2;
        return (
          <div className={`relative ${sizeClass}`}>
            <div className={`w-full h-full ${shapeClass} bg-gray-800 overflow-hidden relative`} style={{ minWidth: sizeNum, minHeight: sizeNum }}>
              {drawPixelAvatar(pixelGrid, sizeNum)}
            </div>
          </div>
        );
      }
    }

    return (
      <div
        className={`${sizeClass} ${shapeClass} bg-gradient-to-br ${bg.class} ${borderStyle.class} flex items-center justify-center text-white font-bold ${textSizeClass}`}
      >
        {mode === "initials" && (
          <span className="select-none">{initials.slice(0, 2).toUpperCase()}</span>
        )}
        {mode === "emoji" && (
          <span className="select-none">{AVATAR_EMOJIS[emoji] || "💻"}</span>
        )}
        {mode === "pixel" && (!pixelGrid || !pixelGrid.some(row => row.some(c => c))) && (
          <span className="select-none text-2xl">🎮</span>
        )}
      </div>
    );
  };

  const tabs = [
    { id: "style", label: "Style" },
    { id: "avatar", label: "Avatar" },
    { id: "color", label: "Colors" },
    { id: "preview", label: "Preview" },
  ];

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />

          <motion.div
            className="relative w-full max-w-lg bg-gray-900 border border-gray-700/50 rounded-2xl shadow-2xl overflow-hidden"
            initial={reduced ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={reduced ? { opacity: 0 } : { opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700/50">
              <h2 className="text-lg font-bold text-white pixel-font tracking-wider">
                ⚔️ Avatar Customization
              </h2>
              <button
                onClick={onClose}
                className="w-8 h-8 rounded-lg bg-gray-800 hover:bg-gray-700 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Current avatar preview */}
            <div className="flex justify-center py-6 bg-gray-800/50">
              {renderAvatar("w-20 h-20", "text-2xl", 40)}
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-700/50 px-2">
              {tabs.map(t => (
                <button
                  key={t.id}
                  type="button"
                  className={`px-4 py-3 text-xs font-medium tracking-wider uppercase transition-colors ${
                    tab === t.id
                      ? "text-indigo-400 border-b-2 border-indigo-400"
                      : "text-gray-500 hover:text-gray-300"
                  }`}
                  onClick={() => setTab(t.id)}
                >
                  {t.label}
                </button>
              ))}
            </div>

            {/* Tab content */}
            <div className="p-6 max-h-[50vh] overflow-y-auto">
              {tab === "style" && (
                <div className="space-y-5">
                  <div>
                    <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Shape</p>
                    <div className="flex gap-2">
                      {SHAPE_STYLES.map((s, i) => (
                        <button
                          key={s.name}
                          type="button"
                          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                            shape === i
                              ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                              : "bg-gray-800 text-gray-400 border border-gray-700/50 hover:border-gray-600"
                          }`}
                          onClick={() => setShape(i)}
                        >
                          {s.name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Border</p>
                    <div className="flex gap-2 flex-wrap">
                      {BORDER_STYLES.map((b, i) => (
                        <button
                          key={b.name}
                          type="button"
                          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                            border === i
                              ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                              : "bg-gray-800 text-gray-400 border border-gray-700/50 hover:border-gray-600"
                          }`}
                          onClick={() => setBorder(i)}
                        >
                          {b.name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Avatar Mode</p>
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        { id: "initials", label: "Initials", icon: "Aa" },
                        { id: "emoji", label: "Emoji", icon: "😀" },
                        { id: "pixel", label: "Pixel Art", icon: "🎮" },
                      ].map((m) => (
                        <button
                          key={m.id}
                          type="button"
                          className={`px-4 py-3 rounded-lg text-xs font-medium transition-all flex flex-col items-center gap-1 ${
                            mode === m.id
                              ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                              : "bg-gray-800 text-gray-400 border border-gray-700/50 hover:border-gray-600"
                          }`}
                          onClick={() => setMode(m.id)}
                        >
                          <span className="text-lg">{m.icon}</span>
                          {m.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {tab === "avatar" && (
                <div className="space-y-5">
                  {mode === "initials" && (
                    <div>
                      <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Initials</p>
                      <input
                        type="text"
                        maxLength={2}
                        value={initials}
                        onChange={(e) => setInitials(e.target.value.toUpperCase())}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700/50 rounded-lg text-white text-center text-xl font-bold tracking-widest focus:outline-none focus:border-indigo-500/50"
                        placeholder="U"
                      />
                    </div>
                  )}

                  {mode === "emoji" && (
                    <div>
                      <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Choose Emoji</p>
                      <div className="grid grid-cols-6 gap-1">
                        {AVATAR_EMOJIS.map((e, i) => (
                          <button
                            key={i}
                            type="button"
                            className={`w-10 h-10 flex items-center justify-center text-lg rounded-lg transition-all ${
                              emoji === i
                                ? "bg-indigo-500/30 ring-2 ring-indigo-400 scale-110"
                                : "bg-gray-800 hover:bg-gray-700"
                            }`}
                            onClick={() => setEmoji(i)}
                          >
                            {e}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {mode === "pixel" && (
                    <PixelGrid value={pixelGrid} onChange={setPixelGrid} />
                  )}
                </div>
              )}

              {tab === "color" && (
                <div className="space-y-5">
                  <div>
                    <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Background Color</p>
                    <div className="grid grid-cols-6 gap-2">
                      {BG_COLORS.map((c, i) => (
                        <button
                          key={c.name}
                          type="button"
                          className={`w-10 h-10 rounded-lg bg-gradient-to-br ${c.class} transition-all ${
                            bgColor === i ? "ring-2 ring-white ring-offset-2 ring-offset-gray-900 scale-110" : ""
                          }`}
                          onClick={() => setBgColor(i)}
                          title={c.name}
                        />
                      ))}
                    </div>
                  </div>

                  {mode === "initials" && (
                    <div>
                      <p className="text-xs text-gray-400 mb-2 uppercase tracking-wider">Initials Color</p>
                      <div className="grid grid-cols-6 gap-2">
                        {INITIAL_COLORS.map((c, i) => (
                          <button
                            key={i}
                            type="button"
                            className={`w-10 h-10 rounded-lg transition-all ${
                              initialsColor === i ? "ring-2 ring-white ring-offset-2 ring-offset-gray-900 scale-110" : ""
                            }`}
                            style={{ backgroundColor: c }}
                            onClick={() => setInitialsColor(i)}
                          />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {tab === "preview" && (
                <div>
                  <p className="text-xs text-gray-400 mb-4 uppercase tracking-wider">How it looks</p>
                  <div className="space-y-4">
                    {PREVIEW_SIZES.map((p) => (
                      <div key={p.label} className="flex items-center gap-4 bg-gray-800/50 rounded-xl p-4">
                        {renderAvatar(p.size, p.textSize, p.fontSize)}
                        <span className="text-sm text-gray-300">{p.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-700/50">
              <button
                type="button"
                onClick={onClose}
                className="px-5 py-2 rounded-lg text-sm font-medium text-gray-400 bg-gray-800 hover:bg-gray-700 transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSave}
                className="px-5 py-2 rounded-lg text-sm font-medium text-white bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-400 hover:to-purple-400 transition-all flex items-center gap-2"
              >
                <Check size={14} />
                Save Avatar
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export { AVATAR_EMOJIS, BG_COLORS };
