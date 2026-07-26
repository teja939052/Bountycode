// Tower data helpers — levels, titles, outfits

export const TOWER_TITLES = {
  1: ['Hatchling', '🐣'], 5: ['Novice', '🌱'], 10: ['Apprentice', '🌿'],
  15: ['Student', '📚'], 20: ['Learner', '📖'], 25: ['Adept', '⚔️'],
  30: ['Problem Solver', '🧩'], 35: ['Code Knight', '🗡️'], 40: ['Code Warrior', '🚀'],
  45: ['Tactician', '🎯'], 50: ['Interview Pro', '🏆'], 55: ['Algorithm Adept', '🔬'],
  60: ['Data Structures Expert', '💡'], 65: ['Architect', '🏗️'],
  70: ['Algorithm Master', '🔥'], 75: ['System Sage', '🧙'],
  80: ['Code Sage', '⚡'], 85: ['Byte Lord', '🌐'],
  90: ['Legendary Programmer', '🏅'], 95: ['Code Overlord', '👁️'],
  100: ['God of Code', '👑'],
};

export const WIZARD_OUTFITS = [
  { minLevel: 1, name: 'Novice Robe', color: '#6b7280', effect: 'none' },
  { minLevel: 10, name: 'Apprentice Robe', color: '#22c55e', effect: 'glow' },
  { minLevel: 25, name: 'Mage Robe', color: '#3b82f6', effect: 'sparkle' },
  { minLevel: 50, name: 'Archmage Robe', color: '#a855f7', effect: 'fire_aura' },
  { minLevel: 75, name: 'Code Sage Robe', color: '#f59e0b', effect: 'lightning' },
  { minLevel: 100, name: 'God of Code', color: '#4CC9F0', effect: 'rainbow_wings' },
];

export function getTitleForLevel(level) {
  let title = 'Hatchling';
  let emoji = '🐣';
  for (const [threshold, [t, e]] of Object.entries(TOWER_TITLES)) {
    if (level >= Number(threshold)) {
      title = t;
      emoji = e;
    }
  }
  return [title, emoji];
}

export function getOutfitForLevel(level) {
  let outfit = WIZARD_OUTFITS[0];
  for (const o of WIZARD_OUTFITS) {
    if (level >= o.minLevel) outfit = o;
  }
  return outfit;
}

export function xpForLevel(level) {
  return ((level - 1) ** 2) * 50;
}

export function xpForNextLevel(level) {
  return (level ** 2) * 50;
}
