import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Cinematic emblem reveal shown after login — GoT/BB intro style
// Shows the user's emblem assembling piece by piece with dramatic lighting

export default function LoginReveal({ user, streak = 0, level = 1, onComplete }) {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 300),
      setTimeout(() => setPhase(2), 1200),
      setTimeout(() => setPhase(3), 2400),
      setTimeout(() => setPhase(4), 3800),
      setTimeout(() => onComplete?.(), 4200),
    ];
    return () => timers.forEach(clearTimeout);
  }, [onComplete]);

  const pieceCount = Math.min(12, 4 + level);
  const pieces = Array.from({ length: pieceCount }, (_, i) => ({
    angle: (360 / pieceCount) * i,
    delay: i * 0.08,
    size: 8 + Math.random() * 16,
    type: i % 3,
  }));

  return (
    <AnimatePresence>
      {phase < 4 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.6 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black"
          onClick={() => onComplete?.()}
        >
          {phase >= 1 && (
            <div className="absolute inset-0 overflow-hidden">
              {Array.from({ length: 20 }).map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-1 h-1 rounded-full bg-cyber-blue/40"
                  initial={{
                    x: Math.random() * 1200,
                    y: Math.random() * 800,
                    opacity: 0,
                  }}
                  animate={{
                    y: [null, Math.random() * -200],
                    opacity: [0, 0.6, 0],
                    scale: [0, 1.5, 0],
                  }}
                  transition={{
                    duration: 2 + Math.random() * 2,
                    delay: Math.random() * 2,
                    repeat: Infinity,
                    ease: 'easeOut',
                  }}
                />
              ))}
            </div>
          )}

          {phase >= 1 && (
            <motion.div
              className="absolute left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyber-blue/60 to-transparent"
              initial={{ top: '100%' }}
              animate={{ top: '0%' }}
              transition={{ duration: 1.5, ease: 'linear' }}
            />
          )}

          <div className="relative">
            {phase >= 1 && (
              <motion.div
                className="absolute rounded-full"
                initial={{ scale: 0.3, opacity: 0 }}
                animate={{ scale: [0.3, 1.2, 1], opacity: [0, 0.4, 0.2] }}
                transition={{ duration: 1.5, ease: 'easeOut' }}
                style={{
                  width: 200, height: 200, top: -24, left: -24,
                  background: 'radial-gradient(circle, rgba(245,158,11,0.3) 0%, rgba(239,68,68,0.1) 50%, transparent 70%)',
                }}
              />
            )}

            <svg viewBox="-60 -60 120 120" width="160" height="160" className="relative z-10">
              {phase >= 2 && pieces.map((piece, i) => (
                <motion.g
                  key={i}
                  initial={{
                    x: (Math.random() - 0.5) * 200,
                    y: (Math.random() - 0.5) * 200,
                    opacity: 0, scale: 0,
                  }}
                  animate={{
                    x: Math.cos((piece.angle * Math.PI) / 180) * 36,
                    y: Math.sin((piece.angle * Math.PI) / 180) * 36,
                    opacity: 1, scale: 1,
                    rotate: [180, 0],
                  }}
                  transition={{
                    duration: 0.8,
                    delay: piece.delay,
                    ease: [0.34, 1.56, 0.64, 1],
                  }}
                >
                  {piece.type === 0 && (
                    <circle cx="0" cy="0" r={piece.size / 3} fill="none"
                      stroke="#4CC9F0" strokeWidth="1" opacity="0.8" />
                  )}
                  {piece.type === 1 && (
                    <polygon
                      points={`0,${-piece.size / 2.5} ${piece.size / 3},${piece.size / 4} ${-piece.size / 3},${piece.size / 4}`}
                      fill="none" stroke="#7209B7" strokeWidth="1" opacity="0.8"
                    />
                  )}
                  {piece.type === 2 && (
                    <line x1={-piece.size / 3} y1="0" x2={piece.size / 3} y2="0"
                      stroke="#4BB543" strokeWidth="1.5" opacity="0.8" />
                  )}
                </motion.g>
              ))}

              {phase >= 2 && (
                <motion.g
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.8, duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
                >
                  <circle cx="0" cy="0" r="18" fill="#111318" stroke="#4CC9F0" strokeWidth="1.5" opacity="0.9" />
                  <circle cx="0" cy="0" r="12" fill="none" stroke="#7209B7" strokeWidth="0.8" opacity="0.5" />
                  <text x="0" y="4" textAnchor="middle" fill="#4CC9F0"
                    fontSize="12" fontFamily="Orbitron" fontWeight="bold">
                    {level}
                  </text>
                </motion.g>
              )}
            </svg>

            {phase >= 3 && (
              <motion.div
                className="absolute -bottom-16 left-1/2 -translate-x-1/2 text-center whitespace-nowrap"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <h2 className="text-xl font-display font-black text-white tracking-wider">
                  {user?.name || 'Commander'}
                </h2>
                <div className="flex items-center justify-center gap-3 mt-2">
                  {streak > 0 && (
                    <motion.span
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
                      className="text-xs font-mono px-2 py-1 rounded bg-cyber-amber/15 text-cyber-amber border border-cyber-amber/30"
                    >
                      {streak} day streak
                    </motion.span>
                  )}
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
                    className="text-xs font-mono px-2 py-1 rounded bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30"
                  >
                    LVL {level}
                  </motion.span>
                </div>
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.5 }}
                  transition={{ delay: 0.6 }}
                  className="text-[10px] font-mono text-gray-500 mt-3"
                >
                  tap anywhere to continue
                </motion.p>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
