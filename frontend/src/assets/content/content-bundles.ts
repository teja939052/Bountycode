/**
 * Content Bundles Manifest
 * 
 * Catalog of all structured learning content bundles available in BountyCode.
 * Each bundle contains lessons, practice questions, and timed topic test questions,
 * all human-reviewed (trust_status: "human_reviewed").
 *
 * Source files: backend/app/data/content/<subject>/<topic>.json
 * Loaded at backend startup via content_loader.py into question_store.
 */
export interface ContentBundle {
  subject: 'quantitative_aptitude' | 'logical_reasoning' | 'verbal_ability' | 'dsa' | 'programming';
  topic: string;
  pattern: string;
  title: string;
  description: string;
  lessonCount: number;
  practiceCount: number;
  questionCount: number;
  totalItems: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced' | 'mixed';
  companyTags: string[];
  estimatedMinutes: number;
  trustStatus: 'human_reviewed';
  source: 'bountycode_original';
  assets: {
    icon: string; // gamification icon key
  };
}

export const CONTENT_BUNDLES: ContentBundle[] = [
  {
    subject: 'quantitative_aptitude',
    topic: 'percentages',
    pattern: 'percentages',
    title: 'Percentages',
    description: 'Fractions, decimals, percent of a number, increase/decrease, successive change, reverse percentage, comparison, and real-world applications.',
    lessonCount: 8,
    practiceCount: 5,
    questionCount: 15,
    totalItems: 28,
    difficulty: 'mixed',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 45,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'score' },
  },
  {
    subject: 'quantitative_aptitude',
    topic: 'profit_loss',
    pattern: 'profit_loss',
    title: 'Profit & Loss',
    description: 'Profit/loss basics, SP & CP formulas, discount, successive discount, and real-world shopkeeper problems.',
    lessonCount: 4,
    practiceCount: 5,
    questionCount: 5,
    totalItems: 14,
    difficulty: 'mixed',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 35,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'score' },
  },
  {
    subject: 'quantitative_aptitude',
    topic: 'time_work',
    pattern: 'time_work',
    title: 'Time & Work',
    description: 'Time-work basics, combined work, work & wages, man-days, inverse proportion, and multi-worker problems.',
    lessonCount: 3,
    practiceCount: 5,
    questionCount: 5,
    totalItems: 13,
    difficulty: 'mixed',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 40,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'energy' },
  },
  {
    subject: 'quantitative_aptitude',
    topic: 'ratios',
    pattern: 'ratios',
    title: 'Ratios & Proportion',
    description: 'Ratio basics, proportion (product of means = product of extremes), comparison, and mixture problems.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 2,
    totalItems: 6,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys'],
    estimatedMinutes: 25,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'score' },
  },
  {
    subject: 'quantitative_aptitude',
    topic: 'averages',
    pattern: 'averages',
    title: 'Averages',
    description: 'Average basics, weighted average, combined average, and removal/addition problems.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 2,
    totalItems: 6,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 25,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'score' },
  },
  {
    subject: 'quantitative_aptitude',
    topic: 'time_speed_distance',
    pattern: 'time_speed_distance',
    title: 'Time, Speed & Distance',
    description: 'TSD basics, unit conversion (km/h ↔ m/s), relative speed, trains crossing bridges, and average speed.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 2,
    totalItems: 6,
    difficulty: 'mixed',
    companyTags: ['infosys', 'wipro'],
    estimatedMinutes: 30,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'energy' },
  },
  {
    subject: 'dsa',
    topic: 'arrays',
    pattern: 'Arrays',
    title: 'Arrays',
    description: 'Array basics, traversal, access vs search complexity, linear vs non-linear, and output-prediction MCQs.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 3,
    totalItems: 7,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 30,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'xp' },
  },
  {
    subject: 'dsa',
    topic: 'linked_lists',
    pattern: 'Linked Lists',
    title: 'Linked Lists',
    description: 'Linked list basics, LL vs array, LIFO/FIFO, stack/queue use cases, and insertion complexity.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 4,
    totalItems: 8,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 30,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'xp' },
  },
  {
    subject: 'dsa',
    topic: 'stacks_queues',
    pattern: 'Stacks & Queues',
    title: 'Stacks & Queues',
    description: 'Stack (LIFO) vs Queue (FIFO), push/pop/enqueue/dequeue, circular buffer, undo/back, BFS.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 3,
    totalItems: 7,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys'],
    estimatedMinutes: 30,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'energy' },
  },
  {
    subject: 'dsa',
    topic: 'trees',
    pattern: 'Trees',
    title: 'Trees',
    description: 'Tree basics, BST property, traversals (pre/in/post/level), AVL balance factor, BFS/DFS complexity.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 2,
    totalItems: 6,
    difficulty: 'intermediate',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 35,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'xp' },
  },
  {
    subject: 'dsa',
    topic: 'complexity',
    pattern: 'Complexity Analysis',
    title: 'Complexity Analysis',
    description: 'Big O notation, complexity reference table, merge sort vs quick sort, binary search requirements.',
    lessonCount: 2,
    practiceCount: 2,
    questionCount: 3,
    totalItems: 7,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys'],
    estimatedMinutes: 25,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'xp' },
  },
  {
    subject: 'logical_reasoning',
    topic: 'logical_reasoning',
    pattern: 'logical_reasoning',
    title: 'Logical Reasoning',
    description: 'Series completion, analogy, syllogism, odd-one-out, blood relations, and family tree puzzles.',
    lessonCount: 3,
    practiceCount: 2,
    questionCount: 3,
    totalItems: 8,
    difficulty: 'mixed',
    companyTags: ['tcs', 'infosys'],
    estimatedMinutes: 35,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'xp' },
  },
  {
    subject: 'verbal_ability',
    topic: 'verbal_ability',
    pattern: 'verbal_ability',
    title: 'Verbal Ability',
    description: 'Synonym & antonym, reading comprehension (True/False/Can\'t tell), sentence correction, spelling, grammar.',
    lessonCount: 3,
    practiceCount: 2,
    questionCount: 3,
    totalItems: 8,
    difficulty: 'beginner',
    companyTags: ['tcs', 'infosys', 'wipro'],
    estimatedMinutes: 30,
    trustStatus: 'human_reviewed',
    source: 'bountycode_original',
    assets: { icon: 'bugsy' },
  },
];

export const CONTENT_BUNDLE_BY_TOPIC: Record<string, ContentBundle> = Object.fromEntries(
  CONTENT_BUNDLES.map(b => [b.topic, b])
);

export const CONTENT_BY_SUBJECT: Record<string, ContentBundle[]> = CONTENT_BUNDLES.reduce(
  (acc, b) => {
    (acc[b.subject] = acc[b.subject] || []).push(b);
    return acc;
  },
  {} as Record<string, ContentBundle[]>
);

export const TOTAL_CONTENT_STATS = {
  totalBundles: CONTENT_BUNDLES.length,
  totalLessons: CONTENT_BUNDLES.reduce((s, b) => s + b.lessonCount, 0),
  totalPractice: CONTENT_BUNDLES.reduce((s, b) => s + b.practiceCount, 0),
  totalQuestions: CONTENT_BUNDLES.reduce((s, b) => s + b.questionCount, 0),
  totalEstimatedMinutes: CONTENT_BUNDLES.reduce((s, b) => s + b.estimatedMinutes, 0),
  allHumanReviewed: CONTENT_BUNDLES.every(b => b.trustStatus === 'human_reviewed'),
};
