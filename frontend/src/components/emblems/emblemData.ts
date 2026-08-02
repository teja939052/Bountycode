// Emblem types mapped to topics, difficulties, and categories
// Each emblem is a sacred geometry symbol rendered in SVG

export const EMBLEM_TYPES = {
  triquetra: {
    name: 'Triquetra',
    meaning: 'Interconnected Knowledge',
    topics: ['Linked Lists', 'Graphs', 'Trees', 'Graph'],
  },
  mandala: {
    name: 'Mandala',
    meaning: 'Precision & Patterns',
    topics: ['Quantitative', 'Quant', 'Mathematics', 'Probability', 'Percentages'],
  },
  dharma: {
    name: 'Dharma Wheel',
    meaning: 'Career Path',
    topics: ['Behavioral', 'HR', 'Soft Skills', 'Communication'],
  },
  sriYantra: {
    name: 'Sri Yantra',
    meaning: 'Layers of Architecture',
    topics: ['System Design', 'HLD', 'LLD', 'Architecture'],
  },
  celticKnot: {
    name: 'Celtic Knot',
    meaning: 'Overlapping Subproblems',
    topics: ['Dynamic Programming', 'DP', 'Recursion', 'Backtracking'],
  },
  flowerOfLife: {
    name: 'Flower of Life',
    meaning: 'Fractal Patterns',
    topics: ['Recursion', 'Divide and Conquer', 'Divide & Conquer'],
  },
  hexagram: {
    name: 'Hexagram',
    meaning: 'Complementary Forces',
    topics: ['Strings', 'String', 'Pattern Matching', 'Pattern Matching'],
  },
  spiral: {
    name: 'Golden Spiral',
    meaning: 'Ordered Progression',
    topics: ['Sorting', 'Searching', 'Binary Search', 'Sorting Algorithms'],
  },
  yinYang: {
    name: 'Yin-Yang',
    meaning: 'Balance of Opposites',
    topics: ['Greedy', 'Two Pointers', 'Two Pointers', 'Sliding Window'],
  },
  eye: {
    name: 'Eye of Providence',
    meaning: 'Watchful Precision',
    topics: ['Arrays', 'Matrix', 'Matrix/2D', 'Bit Manipulation'],
  },
  shield: {
    name: 'Shield',
    meaning: 'Fortified Defense',
    topics: ['Stacks', 'Queues', 'Stack', 'Queue', 'Monotonic Stack'],
  },
  compass: {
    name: 'Compass',
    meaning: 'True North',
    topics: ['Navigation', 'BFS', 'DFS', 'Shortest Path'],
  },
};

// Map category (from question metadata) to emblem type
export const CATEGORY_EMBLEM_MAP = {
  'quantitative': 'mandala',
  'logical': 'compass',
  'verbal': 'dharma',
  'behavioral': 'dharma',
  'dsa': 'eye',
  'system_design': 'sriYantra',
  'hld': 'sriYantra',
  'lld': 'sriYantra',
  'aptitude': 'mandala',
  'reasoning': 'compass',
};

// Map difficulty to emblem style modifiers
export const DIFFICULTY_STYLES = {
  easy: { rings: 1, opacity: 0.7, glowIntensity: 0.3 },
  medium: { rings: 2, opacity: 0.85, glowIntensity: 0.6 },
  hard: { rings: 3, opacity: 1, glowIntensity: 1 },
};

// Color palettes per emblem type
export const EMBLEM_COLORS = {
  triquetra: { primary: '#4CC9F0', secondary: '#06b6d4', glow: 'rgba(76,201,240,0.4)' },
  mandala: { primary: '#F59E0B', secondary: '#fbbf24', glow: 'rgba(245,158,11,0.4)' },
  dharma: { primary: '#ec4899', secondary: '#f472b6', glow: 'rgba(236,72,153,0.4)' },
  sriYantra: { primary: '#818cf8', secondary: '#6366f1', glow: 'rgba(129,140,248,0.4)' },
  celticKnot: { primary: '#22c55e', secondary: '#4ade80', glow: 'rgba(34,197,94,0.4)' },
  flowerOfLife: { primary: '#a855f7', secondary: '#c084fc', glow: 'rgba(168,85,247,0.4)' },
  hexagram: { primary: '#f97316', secondary: '#fb923c', glow: 'rgba(249,115,22,0.4)' },
  spiral: { primary: '#14b8a6', secondary: '#2dd4bf', glow: 'rgba(20,184,166,0.4)' },
  yinYang: { primary: '#e879f9', secondary: '#f0abfc', glow: 'rgba(232,121,249,0.4)' },
  eye: { primary: '#4CC9F0', secondary: '#38bdf8', glow: 'rgba(76,201,240,0.4)' },
  shield: { primary: '#ef4444', secondary: '#f87171', glow: 'rgba(239,68,68,0.4)' },
  compass: { primary: '#84cc16', secondary: '#a3e635', glow: 'rgba(132,204,22,0.4)' },
};

// Determine emblem for a topic string
export function getEmblemForTopic(topic) {
  if (!topic) return 'eye';
  const t = topic.toLowerCase();
  for (const [type, config] of Object.entries(EMBLEM_TYPES)) {
    for (const mappedTopic of config.topics) {
      if (t.includes(mappedTopic.toLowerCase()) || mappedTopic.toLowerCase().includes(t)) {
        return type;
      }
    }
  }
  return 'eye'; // default
}

// Determine emblem for a question based on category + topic
export function getEmblemForQuestion(question) {
  const category = (question.category || question.type || '').toLowerCase();
  if (CATEGORY_EMBLEM_MAP[category]) return CATEGORY_EMBLEM_MAP[category];
  return getEmblemForTopic(question.topic || question.subject || '');
}

// Size presets
export const EMBLEM_SIZES = {
  xs: 24,
  sm: 32,
  md: 48,
  lg: 64,
  xl: 96,
  '2xl': 128,
};
