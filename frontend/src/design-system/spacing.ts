export const spacing = {
  base: 4, // 4px base unit
  scale: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    12: 48,
    16: 64,
    20: 80,
    24: 96,
  },
  get: (step: number) => `${step * 4}px`,
  rem: (step: number) => `${step * 0.25}rem`,
};