import { Database, Workflow, Sparkles, Briefcase } from "lucide-react";

export const TOPIC_GROUPS: Record<string, string[]> = {
  data_structure: [
    "Arrays", "Linked Lists", "Stacks & Queues", "Hash Table", "Trees",
    "Heaps", "Tries", "Graphs", "Union Find", "Design",
  ],
  algorithm: [
    "Sorting", "Searching", "Dynamic Programming", "Greedy", "Math",
    "Bit Manipulation", "Strings",
  ],
  pattern: [
    "Two Pointers", "Sliding Window", "Binary Search", "Backtracking",
    "Intervals", "Prefix Sum", "Monotonic Stack",
  ],
  career: [
    "Aptitude", "Logical Reasoning", "Verbal Ability", "Coding Challenges",
  ],
};

export const GROUP_META: Record<string, { label: string; icon: any; color: string; tag: string; description: string }> = {
  data_structure: {
    label: "Data Structures",
    icon: Database,
    color: "from-blue-500 to-cyan-500",
    tag: "bg-blue-500/10 text-blue-400 border-blue-500/30",
    description: "The building blocks — arrays, trees, graphs, heaps and more.",
  },
  algorithm: {
    label: "Algorithms",
    icon: Workflow,
    color: "from-amber-500 to-orange-500",
    tag: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    description: "Systematic methods — sorting, searching, DP and greedy.",
  },
  pattern: {
    label: "Patterns",
    icon: Sparkles,
    color: "from-fuchsia-500 to-purple-500",
    tag: "bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/30",
    description: "Reusable techniques — two pointers, sliding window, backtracking.",
  },
  career: {
    label: "Career & Aptitude",
    icon: Briefcase,
    color: "from-green-500 to-emerald-500",
    tag: "bg-green-500/10 text-green-400 border-green-500/30",
    description: "Campus drive and screening-round practice.",
  },
};

export const GROUP_ORDER = ["data_structure", "algorithm", "pattern", "career"];

export const TOPIC_DESCRIPTIONS: Record<string, string> = {
  "Arrays": "Contiguous storage — the foundation of most problems.",
  "Linked Lists": "Sequential nodes with next pointers.",
  "Stacks & Queues": "LIFO and FIFO linear structures.",
  "Trees": "Hierarchical nodes (BST, traversal, LCA).",
  "Graphs": "Nodes and edges — BFS, DFS, shortest paths.",
  "Dynamic Programming": "Overlapping subproblems + memoization.",
  "Greedy": "Local optimum to reach global optimum.",
  "Tries": "Prefix trees for strings.",
  "Heaps": "Priority queues via complete binary trees.",
  "Sorting": "Order elements — comparison vs linear sorts.",
  "Searching": "Find elements efficiently.",
  "Bit Manipulation": "& | ^ << >> tricks.",
  "Math": "Number theory, combinatorics, geometry.",
  "Strings": "Text processing, matching, palindromes.",
  "Binary Search": "Halve the search space each step.",
  "Two Pointers": "Move two indices toward a solution.",
  "Sliding Window": "Expand and shrink a window over an array.",
  "Backtracking": "Try, recurse, undo.",
  "Intervals": "Merge / overlap range problems.",
  "Prefix Sum": "Precomputed cumulative sums for range queries.",
  "Monotonic Stack": "Next greater/smaller element pattern.",
  "Union Find": "Disjoint-set connectivity queries.",
  "Hash Table": "O(1) average lookups.",
  "Design": "Implement data structures and OOP systems.",
  "Aptitude": "Quantitative practice for campus drives.",
  "Logical Reasoning": "Pattern and deduction questions.",
  "Verbal Ability": "Grammar, vocabulary, comprehension.",
  "Coding Challenges": "Mixed general-purpose problems.",
};

export function topicGroup(topicName: string): string {
  for (const key of GROUP_ORDER) {
    if (TOPIC_GROUPS[key].includes(topicName)) return key;
  }
  return "pattern";
}
