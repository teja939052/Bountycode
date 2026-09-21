import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import { requestWithRetry as request } from "../services/api/request";
import {
  ArrowLeft, CheckCircle, Circle, Clock, TrendingUp, Building2,
  Lightbulb, Code2, Terminal, BookOpen, Sparkles, Target, ChevronRight,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import PatternTracer from "../components/interactivity/PatternTracer";
import CodeFillInTheBlank from "../components/interactivity/CodeFillInTheBlank";
import ExplainAloud from "../components/interactivity/ExplainAloud";
import AlgorithmTracer from "../components/interactive/AlgorithmTracer";
import PatternQuiz from "../components/interactive/PatternQuiz";
import FillInBlank from "../components/interactive/FillInBlank";
import PredictOutput from "../components/interactive/PredictOutput";
import OrderSteps from "../components/interactive/OrderSteps";

type PatternProblem = {
  id: string;
  title: string;
  difficulty: string;
  type: string;
  topic: string;
  sub_topic: string;
  status: string;
  best_score: number | null;
  companies: string[];
  provenance: string;
  statement: string;
  approach: string;
  complexity: { time?: string; space?: string };
  common_mistakes: string[];
  tips: string[];
  testcase_count: number;
  external_url?: string;
  source_platform?: string;
  ladder_order?: number;
};

type PatternPageData = {
  pattern: string;
  verified_only: boolean;
  total: number;
  mastered: number;
  solved: number;
  attempted: number;
  remaining: number;
  mastery_percent: number;
  companies: { name: string; count: number }[];
  problems: PatternProblem[];
};

type PatternMeta = {
  subtitle: string;
  difficulty_range: string;
  estimated_days: number;
  focus?: boolean;
  checklist?: string[];
  overview: string;
  intuition: string[];
  templates: {
    python_fixed: string;
    python_variable: string;
    java_fixed: string;
    java_variable: string;
  };
  related: { name: string; slug: string; why: string }[];
};

const PATTERN_META: Record<string, PatternMeta> = {
  "sliding-window": {
    subtitle:
      "Expand and shrink a moving window over an array or string to turn O(n²) brute-force scans into O(n) streams.",
    difficulty_range: "Easy → Hard",
    estimated_days: 5,
    focus: true,
    checklist: [
      "Read the pattern overview and reason through the example",
      "Explain the core intuition in my own words",
      "Implemented the fixed-window template myself",
      "Implemented the variable-window template myself",
      "Solved 3+ problems independently before peeking at guidance",
      "Explained the time and space complexity trade-off aloud",
    ],
    overview:
      "Sliding Window is the technique of processing consecutive segments of an array or string by moving two boundaries (left and right) so that each element enters the window once and leaves it once. Instead of re-computing every sub-array from scratch — which costs O(n²) — you maintain a summary of the current window (a running sum, a frequency table, a satisfaction counter) and update it by only O(1) work when the right edge adds an element or the left edge removes one. The deciding question is whether you need a fixed-size window or a variable-size one. Fixed-window problems (maximum average of size k, maximum of every window) ask for something about every window of an exact width. Variable-window problems (shortest subarray with sum ≥ target, longest substring without repeats) grow the window until a constraint is satisfied and shrink it to keep the window optimal. The pattern dissolves whenever the content of old sub-arrays can be cheaply removed — which is almost every contiguous-subarray and substring question. Mastering both the fixed and variable variants unlocks a large family of interview problems from service companies to product companies.",
    intuition: [
      "A window is just two pointers left and right over an 'in / out' stream — every element is added once, removed once, so every pointer moves at most n times and the total work stays O(n).",
      "Fixed windows: the constraint is the width. Advance right every step, advance left every step, and read the window summary before advancing left.",
      "Variable windows: the constraint is a property (sum, distinct count, zero count). Grow right until the property is violated, then shrink left until it is satisfied again, tracking the best answer along the way.",
    ],
    templates: {
      python_fixed: `def fixed_window(arr, k: int):
    # summary holds the answer-relevant aggregate of the current window
    summary = 0
    result = []
    for right in range(len(arr)):
        summary += arr[right]                      # grow into the window
        if right >= k - 1:                         # window is full
            result.append(summary)                 # record window answer
            summary -= arr[left_of_window]         # evict the leftmost element
    return result`,
      python_variable: `def variable_window(arr, k_lim=None):
    left = 0
    summary = 0
    best = float("inf")                            # or -inf for longest
    for right in range(len(arr)):
        summary += arr[right]                      # grow
        while not valid(summary, left, right):     # constraint violated
            summary -= arr[left]                   # shrink
            left += 1
        best = min(best, right - left + 1)         # record if valid
    return best`,
      java_fixed: `public int[] fixedWindow(int[] arr, int k) {
    int[] res = new int[arr.length - k + 1];
    int sum = 0, out = 0;
    for (int r = 0; r < arr.length; r++) {
        sum += arr[r];                       // grow into the window
        if (r >= k - 1) {                    // window is full
            res[out++] = sum;                // record window answer
            sum -= arr[r - k + 1];           // evict the leftmost element
        }
    }
    return res;
}`,
      java_variable: `public int variableWindow(int[] arr, int target) {
    int left = 0, sum = 0, best = Integer.MAX_VALUE;
    for (int r = 0; r < arr.length; r++) {
        sum += arr[r];                        // grow
        while (sum >= target) {               // constraint satisfied: shrink
            best = Math.min(best, r - left + 1);
            sum -= arr[left];
            left++;
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}`,
    },
    related: [
      { name: "Two Pointers", slug: "two-pointers", why: "Sliding Window is a two-pointer pattern specialised to contiguous segments." },
      { name: "Prefix Sum", slug: "prefix-sum", why: "Static sub-array sums in O(1) — often an alternative to maintaining a running window." },
      { name: "Hashing / Hash Map", slug: "hashing", why: "Frequency tables power the constraint checks inside variable-length windows." },
    ],
  },
  "two-pointers": {
    subtitle:
      "Move one or two cursors toward each other (or along a sorted line) to turn nested-loop scans into tight O(n) sweeps.",
    difficulty_range: "Easy → Hard",
    estimated_days: 5,
    focus: true,
    checklist: [
      "Read the pattern overview and reason through the example",
      "Explain the core intuition in my own words",
      "Implemented the convergent two-pointer template myself",
      "Implemented a boundary-sweep / partition template myself",
      "Solved 3+ problems independently before peeking at guidance",
      "Explained the time and space complexity trade-off aloud",
    ],
    overview:
      "Two Pointers is the family of techniques where you walk one, two, or occasionally three indices over the data instead of restarting from scratch each time. The classic shape is convergent: a slow pointer at one end, a fast pointer at the other, and a greedy rule for which end to advance until they meet — that single rule powers sorted two-sum, container area, character reversal, and removing duplicates. The opposite shape is divergent: one runner stays put while a second scans ahead (linked-list cycle detection, or partition sweeps like the Dutch national flag where three regions are managed by two boundaries). The deciding question is whether the data is sorted or naturally ordered — sorted input is the invitation: ordering lets you know which direction to move when the current pairing is too small or too large. Because each pointer only ever moves one way and never needs to revisit, total work collapses from O(n²) enumeration to O(n) or O(n log n) for the sort that enables the sweep.",
    intuition: [
      "Sorted data gives you the shortcut: if the pair sums to too little, only the small side can fix it — advance it; if too much, move the large side inward.",
      "Convergent pointers trade breadth for certainty: at every step you can discard the side that can never appear in a better answer.",
      "Shift-right / boundary-sweep variants partition data in place with two boundary marks — the Dutch national flag is the classic three-way example.",
    ],
    templates: {
      python_fixed: `def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        if s < target:
            lo += 1                      # pair too small: only lo can grow it
        else:
            hi -= 1                      # pair too big: only hi can shrink it
    return [-1, -1]`,
      python_variable: `def reverse_pairs(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1
    return arr`,
      java_fixed: `public int[] twoSumSorted(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int s = nums[lo] + nums[hi];
        if (s == target) return new int[]{lo, hi};
        if (s < target) lo++; else hi--;      // move the decisive side
    }
    return new int[]{-1, -1};
}`,
      java_variable: `public int[] reversePairs(int[] arr) {
    int lo = 0, hi = arr.length - 1;
    while (lo < hi) { swap(arr, lo++, hi--); }
    return arr;
}`,
    },
    related: [
      { name: "Sliding Window", slug: "sliding-window", why: "A variable window is convergent pointers specialised to contiguous segments." },
      { name: "Binary Search", slug: "binary-search", why: "Binary search also collapses a search space by discarding halves on sorted data." },
      { name: "Sorting", slug: "sorting", why: "Almost every two-pointer sweep assumes data is sorted first." },
    ],
  },
  "binary-search": {
    subtitle:
      "Prune the search space in half at every step on sorted (or otherwise monotonic) data — from O(n) scans to O(log n) decisions.",
    difficulty_range: "Easy → Hard",
    estimated_days: 6,
    focus: true,
    checklist: [
      "Read the pattern overview and reason through the example",
      "Explain the loop invariant for a boundary search in my own words",
      "Implemented the exact-target binary search template myself",
      "Implemented the first-true / predicate boundary template myself",
      "Solved 3+ problems independently before peeking at guidance",
      "Explained the time and space complexity trade-off aloud",
    ],
    overview:
      "Binary Search is the extreme case of the divide-and-conquer mindset: on data where a predicate is monotone — 'everything left of here is yes, everything right is no' (or the reverse) — you can inspect the middle element and discard an entire half in one comparison. It is not only for finding a value in a sorted array: it powers integer square roots (the predicate 'x² ≤ n' is monotone), the first/last position of a repeated target, searching in rotated arrays, and even an O(log(min(m, n))) median of two merged lists. The two classic shades are 'find exact target' and 'find the boundary of a predicate' — the second is more powerful and answers most interview variants. The common failure mode is the off-by-one around the loop invariant: pick one convention (lo inclusive, hi inclusive; compare mid against the predicate, then set lo = mid + 1 or hi = mid), write it once, and never mix conventions. Because the search space halves at each step, logarithmic complexity is guaranteed — but only if each comparison genuinely discards half, which is why rotated-search and duplicate-heavy variants deserve careful hand-tests.",
    intuition: [
      "The loop invariant is the entire craft: keep lo pointing at a 'yes' answer and hi at the first 'no', then repeatedly cut the middle until they meet.",
      "Upper-bound / first-true searches use lo = mid + 1 on success and hi = mid on failure; value searches use lo = mid + 1 / hi = mid - 1.",
      "Rotated arrays: one half is always sorted — test which one, then search it if the target fits, otherwise switch halves.",
    ],
    templates: {
      python_fixed: `def bsearch(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1`,
      python_variable: `def first_ge(arr, target):
    lo, hi = 0, len(arr)          # hi is an exclusive 'no' bound
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            hi = mid              # mid qualifies as a candidate answer
        else:
            lo = mid + 1          # mid is below the predicate
    return lo`,
      java_fixed: `public int bsearch(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;      // avoid overflow
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}`,
      java_variable: `public int firstGe(int[] arr, int target) {
    int lo = 0, hi = arr.length;          // hi exclusive 'no' bound
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] >= target) hi = mid; else lo = mid + 1;
    }
    return lo;
}`,
    },
    related: [
      { name: "Two Pointers", slug: "two-pointers", why: "Both patterns exploit sorted data to shrink the search space decisively." },
      { name: "Sorting", slug: "sorting", why: "Binary search is meaningless without a monotone or sorted order." },
      { name: "Sliding Window", slug: "sliding-window", why: "Windows over sorted data sometimes allow log-time scans with binary search inside." },
    ],
  },
  "hashing": {
    subtitle:
      "Turn membership, complement, and frequency questions into one-pass O(1) lookups — the workhorse behind most 'find the missing / duplicate / pair' problems.",
    difficulty_range: "Easy → Hard",
    estimated_days: 5,
    focus: true,
    checklist: [
      "Read the pattern overview and reason through the example",
      "Explain when a hash map beats sorting in my own words",
      "Implemented the one-pass complement template myself",
      "Implemented the two-pass frequency template myself",
      "Solved 3+ problems independently before peeking at guidance",
      "Explained the time and space complexity trade-off aloud",
    ],
    overview:
      "A hash map (or set) is the universal tool for turning 'have we seen X before?' into an O(1) decision. The recurring shape is: while scanning a list, store the information you will need later keyed by the value you are looking at now, then on every step query the map for the value that would complete the current answer. Two-sum and other complement problems query the map for target - current; frequency problems first count everything in one pass, then scan again to ask something about the counts (the first value whose frequency is 1, the values with unique frequencies, the K most common); subarray-sum problems store running-prefix totals so that a later prefix minus an earlier one can answer 'does a subarray sum to K?' in O(1). The deciding question is whether the data is indexed by value (use a map) or only by position (use arrays and pointers). Every one of these maps one quadratic nested scan into one linear pass, at the price of memory — the classic time-for-space trade that interviewers expect you to name aloud.",
    intuition: [
      "Store what you will need later; query for the value that completes the current step — half the work happens in the lookup expression, not a loop.",
      "One pass is required when the answer depends on order (two-sum, subarray counts); two passes are cleaner when the data is static (frequencies, first unique).",
      "Language cues: 'complement', 'pair', 'frequency', 'occurrence', 'prefix sum' almost always point at a hash map.",
    ],
    templates: {
      python_fixed: `def two_sum(nums, target):
    seen = {}                          # complement -> first index
    for i, v in enumerate(nums):
        if target - v in seen:
            return [seen[target - v], i]
        seen[v] = i                    # store for later queries
    return []`,
      python_variable: `def first_unique(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1   # pass 1: count
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i                         # pass 2: query
    return -1`,
      java_fixed: `public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);          // store for later queries
    }
    return new int[0];
}`,
      java_variable: `public int firstUnique(String s) {
    Map<Character, Integer> counts = new HashMap<>();
    for (char c : s.toCharArray()) {
        counts.merge(c, 1, Integer::sum);    // pass 1: count
    }
    for (int i = 0; i < s.length(); i++) {
        if (counts.get(s.charAt(i)) == 1) {
            return i;                        // pass 2: query
        }
    }
    return -1;
}`,
    },
    related: [
      { name: "Strings", slug: "strings", why: "Anagram and frequency problems are hash-map problems wearing string clothes." },
      { name: "Two Pointers", slug: "two-pointers", why: "On sorted data, two pointers answer two-sum without memory — the hash map's easier sibling." },
      { name: "Sliding Window", slug: "sliding-window", why: "Window constraint checks are powered by the same running frequency tables." },
    ],
  },
  "strings": {
    subtitle:
      "Character-level reasoning over prefixes, anagrams, runs and encodings — the pattern of deciding whether order matters or only the multiset does.",
    difficulty_range: "Easy → Hard",
    estimated_days: 5,
    focus: true,
    checklist: [
      "Read the pattern overview and reason through the example",
      "Explain the multiset-vs-order decision in my own words",
      "Implemented the counting comparison template myself",
      "Implemented a run-simulation template myself",
      "Solved 3+ problems independently before peeking at guidance",
      "Explained the time and space complexity trade-off aloud",
    ],
    overview:
      "String problems split into two families, and choosing a side early is the whole game. The multiset family (anagrams, characters that appear once, frequency checks) ignores order: sort the string or count its characters into a map, then compare maps. The order family (prefixes, substrings, reversals, run-lengths) must respect sequence: longest-common-prefix shrinks a candidate from the front, reverse-vowels walks two pointers inward, run-length and count-and-say simulate stretches of equal neighbours by reading runs left to right. The most common recipe is two passes: one pass to count or build a structure, a second pass to answer a 'first / last / which' question about it (first unique character is the archetype). Almost every string question is a disguise — anagram is hash-map, reverse-vowels is two-pointers, substrings-with-constraints is sliding-window — so the skill is naming the hidden shape before reaching for a string-specific trick.",
    intuition: [
      "Ask first: does order matter? If not, collapse the string to a multiset (sort or count) and compare — anagrams are just equal multisets.",
      "Prefix questions build a candidate and shrink it; reversal and pairing questions converge two pointers; run questions simulate contiguous stretches.",
      "Two passes is the standard rhythm: build the counting structure, then scan again for the 'first / last / only' answer.",
    ],
    templates: {
      python_fixed: `def is_anagram(s, t):
    from collections import Counter
    return Counter(s) == Counter(t)      # multiset equality`,
      python_variable: `def run_length_encode(s):
    out, count = [], 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            out.append(s[i - 1] + str(count))
            count = 1
    if s:
        out.append(s[-1] + str(count))
    return "".join(out)`,
      java_fixed: `public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] counts = new int[26];
    for (int i = 0; i < s.length(); i++) {
        counts[s.charAt(i) - 'a']++;    // count s
        counts[t.charAt(i) - 'a']--;    // cancel with t
    }
    for (int c : counts) if (c != 0) return false;
    return true;
}`,
      java_variable: `public String runLengthEncode(String s) {
    StringBuilder sb = new StringBuilder();
    int count = 1;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) == s.charAt(i - 1)) count++;
        else {
            sb.append(s.charAt(i - 1)).append(count);
            count = 1;
        }
    }
    if (s.length() > 0) sb.append(s.charAt(s.length() - 1)).append(count);
    return sb.toString();
}`,
    },
    related: [
      { name: "Hashing", slug: "hashing", why: "Counting characters is a hash-map operation; many string problems are hashing in disguise." },
      { name: "Two Pointers", slug: "two-pointers", why: "Reversal, palindrome and vowel-swap questions converge pointer pairs." },
      { name: "Sliding Window", slug: "sliding-window", why: "Substring constraints shrink to window problems over characters." },
    ],
  },
};

const DEFAULT_META: PatternMeta = {
  subtitle:
    "Verified practice problems ordered Easy → Medium → Hard, with live per-question progress and pattern mastery.",
  difficulty_range: "Easy → Hard",
  estimated_days: 3,
  focus: false,
  overview: "",
  intuition: [],
  templates: {
    python_fixed: "",
    python_variable: "",
    java_fixed: "",
    java_variable: "",
  },
  related: [],
};

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
};

const STATUS_STYLES: Record<string, string> = {
  not_started: "bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400",
  attempted: "bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400",
  solved: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  mastered: "bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400",
};

const STATUS_LABELS: Record<string, string> = {
  not_started: "Not Started",
  attempted: "Attempted",
  solved: "Solved",
  mastered: "Mastered",
};

const PUBLISHED_PATTERN_SLUGS = new Set(["sliding-window", "two-pointers", "binary-search", "hashing", "strings"]);

const DEFAULT_CHECKLIST = [
  "Read the pattern overview and reason through the example",
  "Explain the core intuition in my own words",
  "Implemented the core template myself",
  "Solved 3+ problems independently before peeking at guidance",
  "Explained the time and space complexity trade-off aloud",
];

function CodeBlock({ code, label }: { code: string; label: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="relative rounded-xl overflow-hidden border border-border dark:border-gray-700 bg-gray-950">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-800">
        <span className="text-xs font-mono text-gray-400">{label}</span>
        <button
          onClick={() => {
            navigator.clipboard?.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 1200);
          }}
          className="text-xs text-gray-500 hover:text-white transition-colors"
        >
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="p-4 text-[13px] leading-relaxed text-cyan-300 font-mono overflow-x-auto">
        <code>{code}</code>
      </pre>
    </div>
  );
}

const SKILL_ID = "dsa.sliding_window";

function useEvidence() {
  const startTime = useRef(Date.now());
  const emit = useCallback(async (source: string, passed: boolean, score: number, extra?: Record<string, unknown>) => {
    try {
      await request("/api/v1/study/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "practice",
          skill_id: SKILL_ID,
          passed,
          score,
          time_spent: Math.round((Date.now() - startTime.current) / 1000),
          diagnosis_codes: [],
          source,
          metadata: { pattern: "sliding-window", ...extra },
        }),
      });
    } catch { /* fail-open */ }
  }, []);
  return emit;
}

const SW_ARRAY = [2, 1, 5, 1, 3, 2, 8, 4, 6, 3];
const SW_K = 3;

const SW_TRACE_STEPS = (() => {
  const steps: Array<{ step: number; description: string; array: number[]; pointers: Record<string, number>; highlight: number[]; window?: { start: number; end: number }; variables: Record<string, string | number>; codeLine?: number }> = [];
  let sum = 0;
  for (let right = 0; right < SW_ARRAY.length; right++) {
    sum += SW_ARRAY[right];
    const left = right >= SW_K - 1 ? right - SW_K + 1 : 0;
    if (right >= SW_K - 1) sum -= SW_ARRAY[left > 0 ? left - 1 : 0];
    steps.push({
      step: right + 1,
      description: right < SW_K - 1
        ? `Enter ${SW_ARRAY[right]}. Window filling (${right + 1}/${SW_K}).`
        : `Enter ${SW_ARRAY[right]}, leave ${SW_ARRAY[right - SW_K]}. Window [${SW_ARRAY.slice(right - SW_K + 1, right + 1).join(", ")}].`,
      array: SW_ARRAY,
      pointers: { left, right },
      highlight: Array.from({ length: Math.min(right + 1, SW_K) }, (_, i) => right - SW_K + 1 + i >= 0 ? right - SW_K + 1 + i : i).filter(i => i >= 0 && i <= right),
      window: { start: left, end: right },
      variables: { k: SW_K, sum: SW_ARRAY.slice(left, right + 1).reduce((a, b) => a + b, 0) },
      codeLine: right < SW_K - 1 ? 2 : 4,
    });
  }
  return steps;
})();

const SW_QUIZ_QUESTIONS = [
  { id: "sw-q1", problemStatement: "In a fixed-size sliding window of k=3 over [2,1,5,1,3], what is the maximum window sum?", options: ["8", "7", "9", "6"], correctIndex: 2, explanation: "Windows: [2,1,5]=8, [1,5,1]=7, [5,1,3]=9. Maximum is 9.", pattern: "sliding-window" },
  { id: "sw-q2", problemStatement: "What is the time complexity of computing max subarray sum with a fixed sliding window?", options: ["O(n)", "O(n log n)", "O(n*k)", "O(k)"], correctIndex: 0, explanation: "Each element enters and leaves the window once, so total work is O(n).", pattern: "sliding-window" },
  { id: "sw-q3", problemStatement: "For variable-size sliding window, when do you shrink the window from the left?", options: ["When window exceeds a constraint", "Always after k steps", "When sum is too large", "At each step"], correctIndex: 0, explanation: "Variable window shrinks when the current window violates the constraint (e.g., sum > target, no more than k distinct).", pattern: "sliding-window" },
];

const SW_FILL_BLANKS = [
  { id: "blank-1", placeholder: "window sum update", correctAnswer: "sum += arr[right]", hint: "Add the new element entering from the right", width: 200 },
  { id: "blank-2", placeholder: "shrink left", correctAnswer: "sum -= arr[left]", hint: "Remove the element leaving the window", width: 180 },
];

const SW_PREDICT_QUESTIONS = [
  { id: "sw-p1", code: "arr = [2, 1, 5, 1, 3]\nk = 3\nwindow_sum = sum(arr[:k])\nfor right in range(k, len(arr)):\n    window_sum += arr[right] - arr[right - k]\nprint(max_sum)", options: ["9", "8", "7", "6"], correctIndex: 0, explanation: "Fixed window max sum is [5,1,3] = 9.", language: "python" },
];

const SW_ORDER_STEPS = [
  { id: "s1", text: "Initialize window sum with first k elements", order: 1 },
  { id: "s2", text: "Slide window: add new element, remove old", order: 2 },
  { id: "s3", text: "Track maximum sum seen so far", order: 3 },
  { id: "s4", text: "Return maximum after processing all windows", order: 4 },
];

export default function PatternPage() {
  const { patternId = "sliding-window" } = useParams();
  const reduced = useReducedMotion();
  const meta: PatternMeta = PATTERN_META[patternId] || DEFAULT_META;
  const checklist = meta.checklist || DEFAULT_CHECKLIST;

  const [data, setData] = useState<PatternPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [checked, setChecked] = useState<boolean[]>(() => checklist.map(() => false));
  const [checklistLoaded, setChecklistLoaded] = useState(false);
  const useEvidenceRef = useRef(useEvidence());

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    setChecked(checklist.map(() => false));
    setChecklistLoaded(false);
    Promise.all([
      api.questions.getPatternPage(patternId),
      api.questions.getPatternChecklist(patternId),
    ]).then(([res, checklistState]) => {
      if (active) {
        setData(res);
        if (checklistState && Array.isArray(checklistState.checked)) {
          setChecked(checklistState.checked);
        }
        setChecklistLoaded(true);
      }
    }).catch(() => {
      if (active) {
        setError("Could not load this pattern page. It may not exist yet.");
        setChecklistLoaded(true);
      }
    }).finally(() => {
      if (active) setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [patternId]);

  const toggleCheck = async (idx: number) => {
    const next = checked.slice();
    next[idx] = !next[idx];
    setChecked(next);
    try {
      await api.questions.savePatternChecklist({
        pattern_id: patternId,
        checked: next,
        checklist,
      });
    } catch (err) {
      console.error("Failed to save checklist state:", err);
    }
  };

  const [tab, setTab] = useState<"python" | "java">("python");
  const [template, setTemplate] = useState<"fixed" | "variable">("fixed");

  const mastered = data ? data.mastered : 0;
  const checklistDone = checked.filter(Boolean).length;
  const hasEditorial = meta.focus;

  if (loading) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-4xl mx-auto space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 animate-pulse" />
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-2" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <Link
          to="/problems"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 mb-6 transition-colors"
        >
          <ArrowLeft size={16} />
          All Topics
        </Link>

        {/* Header */}
        <motion.div
          className="mb-8"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex flex-wrap items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold dark:text-white">
              {data?.pattern || "Pattern"}
            </h1>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800">
              <Sparkles size={12} />
              Pattern
            </span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 max-w-3xl">{meta.subtitle}</p>

          <div className="mt-4 flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
              <TrendingUp size={14} /> {meta.difficulty_range}
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
              <Clock size={14} /> ~{meta.estimated_days} day{meta.estimated_days > 1 ? "s" : ""} to master
            </span>
            {data && data.companies.length > 0 && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
                <Building2 size={14} />
                {data.companies.slice(0, 4).map((c) => c.name).join(", ")}
                <span className="text-xs text-gray-400">(pattern relevance)</span>
              </span>
            )}
          </div>

          {/* Mastery */}
          {data && (
            <div className="mt-6 grid grid-cols-2 sm:grid-cols-5 gap-3">
              <div className="card p-4">
                <div className="text-2xl font-bold text-primary-600">{data.mastery_percent}%</div>
                <div className="text-xs text-gray-500">Pattern Mastery</div>
                <div className="mt-2 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${data.mastery_percent}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                  />
                </div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-green-500">{data.solved}</div>
                <div className="text-xs text-gray-500">Solved</div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-indigo-500">{data.mastered}</div>
                <div className="text-xs text-gray-500">Mastered (8.0+)</div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-amber-500">{data.attempted}</div>
                <div className="text-xs text-gray-500">Attempted</div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-gray-400">{data.remaining}</div>
                <div className="text-xs text-gray-500">Remaining</div>
              </div>
            </div>
          )}
        </motion.div>

        {error ? (
          <div className="card text-center py-12 text-gray-500 dark:text-gray-400">{error}</div>
        ) : (
          <div className="space-y-8">
            {/* Overview */}
            {hasEditorial && meta.overview && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-3">
                  <BookOpen size={18} className="text-primary-500" /> Pattern Overview
                </h2>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{meta.overview}</p>
              </motion.section>
            )}

            {/* Core Intuition */}
            {hasEditorial && meta.intuition.length > 0 && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-3">
                  <Lightbulb size={18} className="text-amber-500" /> Core Intuition
                </h2>
                <ul className="space-y-2">
                  {meta.intuition.map((item, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                      <Target size={15} className="mt-1 shrink-0 text-amber-500" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </motion.section>
            )}

            {/* Template Code */}
            {hasEditorial && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-3">
                  <Code2 size={18} className="text-cyan-500" /> Template Code
                </h2>
                <div className="flex gap-2 mb-4">
                  <button
                    onClick={() => setTemplate("fixed")}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                      template === "fixed"
                        ? "bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400"
                        : "bg-gray-100 dark:bg-gray-800 text-gray-500"
                    }`}
                  >
                    Fixed Window
                  </button>
                  <button
                    onClick={() => setTemplate("variable")}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                      template === "variable"
                        ? "bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400"
                        : "bg-gray-100 dark:bg-gray-800 text-gray-500"
                    }`}
                  >
                    Variable Window
                  </button>
                  <div className="flex-1" />
                  <div className="flex gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
                    {(["python", "java"] as const).map((lang) => (
                      <button
                        key={lang}
                        onClick={() => setTab(lang)}
                        className={`px-3 py-1 rounded-md text-xs font-semibold uppercase tracking-wide transition-colors ${
                          tab === lang
                            ? "bg-white dark:bg-gray-700 text-primary-600 shadow"
                            : "text-gray-500"
                        }`}
                      >
                        {lang}
                      </button>
                    ))}
                  </div>
                </div>
                <CodeBlock
                  code={meta.templates[`${tab}_${template}`]}
                  label={`${tab === "python" ? "Python" : "Java"} · ${template === "fixed" ? "Fixed window" : "Variable window"}`}
                />
              </motion.section>
            )}

            {/* Active Recall — manipulate, predict, explain (evidence via /study/activity) */}
            {hasEditorial && patternId === "sliding-window" && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-1">
                  <Target size={18} className="text-emerald-500" /> Active Recall
                </h2>
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">
                  Manipulate the window, predict the shrink step, then explain why it stays O(n).
                  Each interaction records evidence to the existing study pipeline (skill dsa.sliding_window).
                </p>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-3 mb-3">
                  <PatternTracer />
                  <CodeFillInTheBlank />
                  <ExplainAloud />
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mb-3">
                  <AlgorithmTracer
                    steps={SW_TRACE_STEPS}
                    title="Fixed Window Max Sum"
                    questionMode
                    questionStep={4}
                    questionText="What is the window sum at this step?"
                    correctAnswer={String(SW_ARRAY.slice(1, 4).reduce((a, b) => a + b, 0))}
                    onComplete={(c) => {
                      const emit = useEvidenceRef.current;
                      emit?.("algorithm_tracer", c, c ? 100 : 0, { component: "algorithm_tracer" });
                    }}
                  />
                  <PatternQuiz
                    questions={SW_QUIZ_QUESTIONS}
                    onComplete={(score, total) => {
                      const emit = useEvidenceRef.current;
                      emit?.("pattern_quiz", score === total, (score / total) * 100, { component: "pattern_quiz", score, total });
                    }}
                  />
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                  <FillInBlank
                    codeTemplate={`def max_subarray_sum(arr, k):\n    window_sum = sum(arr[:k])\n    # ${"{blank-1}}"}\n    for right in range(k, len(arr)):\n        window_sum += arr[right] - arr[right - k]\n    return max_sum`}
                    blanks={SW_FILL_BLANKS}
                    onComplete={(correct, attempts) => {
                      const emit = useEvidenceRef.current;
                      emit?.("fill_in_blank", correct, correct ? 100 : 0, { component: "fill_in_blank", attempts });
                    }}
                  />
                  <PredictOutput
                    questions={SW_PREDICT_QUESTIONS}
                    onComplete={(score, total) => {
                      const emit = useEvidenceRef.current;
                      emit?.("predict_output", score === total, (score / total) * 100, { component: "predict_output", score, total });
                    }}
                  />
                </div>
                <div className="mt-3">
                  <OrderSteps
                    steps={SW_ORDER_STEPS}
                    title="Sliding Window Algorithm Steps"
                    onComplete={(correct, attempts) => {
                      const emit = useEvidenceRef.current;
                      emit?.("order_steps", correct, correct ? 100 : 0, { component: "order_steps", attempts });
                    }}
                  />
                </div>
              </motion.section>
            )}

            {/* Progressive Problem List */}
            <motion.section
              className="card p-6"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white">
                  <Terminal size={18} className="text-primary-500" /> Progressive Practice
                </h2>
                <span className="text-xs text-gray-500">
                  {data?.verified_only ? `${data?.total ?? 0} verified problems · Easy → Hard` : ""}
                </span>
              </div>

              {data && data.problems.length > 0 ? (
                <div className="space-y-3">
                  {data.problems.map((problem, index) => {
                    const href = problem.external_url || `/solve/${problem.id}`;
                    const isExternal = Boolean(problem.external_url);
                    const platformLabel = problem.source_platform || (isExternal ? "External" : "Practice");
                    return (
                      <div
                        key={problem.id}
                        className="flex flex-col sm:flex-row sm:items-center gap-3 p-4 rounded-xl border border-border dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 transition-colors"
                      >
                        <div className="flex items-center gap-3 sm:w-64 shrink-0">
                          <div className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-sm font-bold text-gray-500 dark:text-gray-400 shrink-0">
                            {problem.ladder_order && problem.ladder_order < 999 ? problem.ladder_order : index + 1}
                          </div>
                          <Link
                            to={href}
                            target={isExternal ? "_blank" : undefined}
                            rel={isExternal ? "noopener noreferrer" : undefined}
                            className="font-semibold text-sm dark:text-white hover:text-primary-600 transition-colors underline-offset-2 hover:underline"
                          >
                            {problem.title}
                          </Link>
                        </div>
                        <div className="flex items-center gap-2 flex-wrap sm:flex-1">
                          <span className={`px-2 py-0.5 rounded-full text-xs ${DIFFICULTY_COLORS[problem.difficulty] || ""}`}>
                            {problem.difficulty}
                          </span>
                          <span className="text-[10px] font-mono uppercase tracking-wider text-gray-400 border border-gray-700 rounded-full px-2 py-0.5">
                            {platformLabel}
                          </span>
                          {problem.companies.slice(0, 2).map((c) => (
                            <span key={c} className="text-xs text-gray-400 flex items-center gap-1">
                              <Building2 size={10} /> {c}
                            </span>
                          ))}
                          <span className="text-xs text-gray-500 dark:text-gray-400 hidden lg:inline">
                            {problem.complexity?.time ? `O(${problem.complexity.time})` : ""}
                          </span>
                        </div>
                        <div className="flex items-center justify-between sm:w-40 shrink-0 gap-2">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${STATUS_STYLES[problem.status] || ""}`}>
                            {STATUS_LABELS[problem.status] || problem.status}
                          </span>
                          <Link
                            to={href}
                            target={isExternal ? "_blank" : undefined}
                            rel={isExternal ? "noopener noreferrer" : undefined}
                            className="text-primary-600 hover:text-primary-700 text-xs font-semibold inline-flex items-center gap-0.5"
                          >
                            {isExternal ? "Open" : (problem.status === "solved" || problem.status === "mastered" ? "Review" : "Solve")} <ChevronRight size={14} />
                          </Link>
                        </div>
                        {problem.approach && (
                          <div className="sm:w-full text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-900/50 rounded-lg p-2.5">
                            <span className="font-semibold text-gray-600 dark:text-gray-300">Why this problem: </span>
                            {problem.approach}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-10 text-gray-500 dark:text-gray-400">
                  No verified problems in this pattern yet.
                </div>
              )}
            </motion.section>

            {/* Mastery Checklist */}
            <motion.section
              className="card p-6"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center justify-between mb-3">
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white">
                  <CheckCircle size={18} className="text-green-500" /> Mastery Checklist
                </h2>
                <span className="text-xs text-gray-500">{checklistDone}/{checklist.length} done</span>
              </div>
              <ul className="space-y-2">
                {checklist.map((item, i) => (
                  <li key={i}>
                    <label className="flex items-start gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={checked[i]}
                        onChange={() => toggleCheck(i)}
                        className="mt-0.5 w-4 h-4 accent-emerald-500"
                      />
                      <span className={`text-sm ${checked[i] ? "text-gray-400 line-through" : "text-gray-600 dark:text-gray-400"}`}>
                        {item}
                      </span>
                    </label>
                  </li>
                ))}
              </ul>
            </motion.section>

            {/* Related Patterns */}
            {meta.related.length > 0 && (
              <motion.section
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-3">
                  <Sparkles size={18} className="text-primary-500" /> Related Patterns
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {meta.related.map((r) => {
                      const published = PUBLISHED_PATTERN_SLUGS.has(r.slug);
                      const body = (
                        <>
                          <h3 className="font-bold text-sm dark:text-white group-hover:text-primary-600 transition-colors mb-1">
                            {r.name}
                            {!published && (
                              <span className="ml-2 text-[10px] font-mono uppercase tracking-wide text-gray-400">coming soon</span>
                            )}
                          </h3>
                          <p className="text-xs text-gray-500 dark:text-gray-400">{r.why}</p>
                          {published ? (
                            <span className="inline-flex items-center gap-1 text-xs text-primary-600 mt-2">
                              Open pattern <ChevronRight size={12} />
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 text-xs text-gray-400 mt-2">
                              More verified problems coming
                            </span>
                          )}
                        </>
                      );
                      return published ? (
                        <Link
                          key={r.slug}
                          to={`/pattern/${r.slug}`}
                          className="card p-4 group hover:border-primary-300 dark:hover:border-primary-700 transition-colors"
                        >
                          {body}
                        </Link>
                      ) : (
                        <div key={r.slug} className="card p-4 group opacity-70">
                          {body}
                        </div>
                      );
                    })}
                </div>
              </motion.section>
            )}
          </div>
        )}

        <div className="mt-8 text-center">
          <Link
            to="/problems"
            className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 transition-colors"
          >
            <ArrowLeft size={14} /> Back to all topics
          </Link>
        </div>
      </div>
    </div>
  );
}