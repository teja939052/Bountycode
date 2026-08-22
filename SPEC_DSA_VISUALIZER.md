# DSA Visualizer Rebuild Specification

**Document ID:** `SPEC-DSA-VISUALIZER-001`
**Version:** 1.0
**Date:** 2026-08-18
**Priority:** HIGH
**Target:** PlacementPro Skill Tree Integration

---

## Executive Summary

We are rebuilding the DSA Visualizer into a **teaching-grade interactive algorithm execution engine**. The goal is not a pretty animation — it's an **active learning system** where students understand WHY algorithms work by watching, stepping through, predicting, and manipulating execution.

**Core Philosophy:** Build an execution engine, not an animation player.

---

## Primary Goal

A student must be able to:
1. **Watch** the algorithm execute with perfect code synchronization
2. **Step through** at their own pace (prev/next/play/pause/scrub/speed)
3. **Predict** the next state before it happens
4. **Modify** inputs and re-run
4. **Debug** intentionally buggy implementations
5. **Prove understanding** through assessment

---

## Architecture Requirements

### 1. Framework-Independent Execution Engine
```
Algorithm Definition
       ↓
Execution Engine (pure JS/TS, no React)
       ↓
State Timeline (immutable snapshots)
       ↓
Visualization Renderer (React, decoupled)
       ↓
Student Interaction
       ↓
Understanding Assessment
```

**The execution engine must be completely independent from the UI.** Every algorithm execution produces deterministic state snapshots.

### 2. State Model

```ts
type AlgorithmState = {
  step: number;
  variables: Record<string, unknown>;
  array?: number[];
  pointers?: Pointer[];
  comparisons: Comparison[];
  swaps: Swap[];
  activeLine?: number;
  explanation: string;
  question?: InteractiveQuestion;
};

type Pointer = { id: string; index: number; label?: string; color?: string };
type Comparison = { i: number; j: number; result: '<' | '>' | '==' | '<=' | '>=' };
type Swap = { i: number; j: number };
type InteractiveQuestion = {
  type: 'predict-next' | 'why-this-happened' | 'choose-action';
  prompt: string;
  options: { label: string; correct: boolean }[];
  explanation: string;
};
```

### 3. Event Model (Visualization DSL)

Algorithms emit structured events — the renderer knows how to visualize each:

| Event | Payload | Visualization |
|-------|---------|---------------|
| `COMPARE` | `{i, j, result}` | Highlight two elements, show comparison result |
| `SWAP` | `{i, j}` | Animate swap with arc/trail |
| `MOVE_POINTER` | `{id, index}` | Smooth pointer movement |
| `INSERT` | `{index, value}` | Element slides in |
| `DELETE` | `{index}` | Element fades out |
| `VISIT` | `{index}` | Pulse/highlight node |
| `ENQUEUE` / `DEQUEUE` | `{value}` | Queue animation |
| `PUSH` / `POP` | `{value}` | Stack animation |
| `CALL` / `RETURN` | `{function, args}` | Call stack visualization |
| `PARTITION` | `{pivot, left, right}` | Quicksort partition highlight |
| `MERGE` | `{left, right, result}` | Merge sort visualization |
| `RELAX` | `{from, to, oldDist, newDist}` | Dijkstra edge relaxation |
| `FOUND` / `NOT_FOUND` | `{index}` | Success/failure indicator |
| `COMPLETE` | `{result}` | Final state celebration |

---

## Visualizer UI Layout

```
┌──────────────────────┬───────────────────────┐
│                      │                       │
│      VISUALIZER      │        CODE           │
│                      │  01 for (...)         │
│   [5][2][8][1][9]    │  02   if (...)       │
│       ↑              │  03      swap()      │
│      i               │                       │
│                      │  ← highlighted line   │
├──────────────────────┴───────────────────────┤
│ ▶  Step 12/43        Explanation              │
└───────────────────────────────────────────────┘
```

**Key Requirements:**
- Code panel highlights current executing line in real-time
- Visualizer shows current state (arrays, pointers, trees, etc.)
- Variables panel shows live values
- Timeline scrubber at bottom (drag from step 4 → 31, state reconstructs)
- Explanation panel tied to current step
- Interactive questions appear at key moments

---

## Algorithm Families Required

### Arrays
- Linear Search
- Binary Search (with eliminated-half gray-out)
- Two Pointers (with sum/target reasoning)
- Sliding Window (animated window movement)
- Prefix Sum

### Sorting (Race Mode Capable)
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort (show merge steps)
- Quick Sort (partition visualization)
- Heap Sort

### Linked Lists
- Traversal
- Insert/Delete at position
- Reverse (show `prev`, `curr`, `next` changing)
- Fast/Slow Pointer (cycle detection)

### Stacks/Queues
- Push/Pop with call stack
- Enqueue/Dequeue with queue visualization
- Monotonic Stack (next greater element)

### Trees
- BST (insert, search, delete)
- DFS Traversals (pre/in/post-order with traversal sequence)
- BFS (queue visualization)
- Subtree highlighting

### Graphs
- BFS (queue + frontier + visited + parent + distance)
- DFS (call stack + visited + discovery/finish times)
- Dijkstra (distance table + edge relaxation animation)
- Topological Sort (Kahn's algorithm with queue)
- Union Find (union/find with path compression)

### Recursion
- factorial (call stack unwind visualization)
- fibonacci (tree recursion visualization)
- binary recursion
- backtracking (N-Queens, subsets)

---

## Interactive Modes

| Mode | Description |
|------|-------------|
| **LEARN** | Guided explanation with auto-play and pauses at key concepts |
| **EXPLORE** | Free step-through with full control |
| **PREDICT** | Pause before key steps — student predicts next state |
| **DEBUG** | Intentionally buggy implementation — student finds bug |
| **CHALLENGE** | Student completes missing steps |
| **RACE** | Compare algorithms on same input (race mode) |

---

## Required Interactions

### 1. Predict Next State
```
[2][5][8][9][1]
       ↑    ↑
       i    j

WHAT HAPPENS NEXT?
A → Swap
B → Move i
C → Move j
D → Nothing
```

### 2. Why Did This Happen?
```
Why did we move high?
○ Because sum > target
○ Because sum < target
○ Because left == right
```

### 3. Bug Detection
```python
# Buggy binary search
while low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        high = mid - 1  # BUG!
```

Student finds first incorrect state.

---

## Variables & Call Stack Panels

### Variables
```
VARIABLES
i        = 4
j        = 7
target   = 12
mid      = 6
low      = 0
high     = 9
```

### Call Stack (Recursion)
```
CALL STACK
fib(5)
 └─ fib(4)
     └─ fib(3)
         └─ fib(2)
```

---

## Complexity Visualization

At completion:
```
TIME
Best       Ω(n)
Average    Θ(n log n)
Worst      O(n²)

SPACE      O(log n)

OPERATIONS AT SCALE
n = 10       → 100 ops
n = 100      → 10,000 ops
n = 1,000    → 1,000,000 ops
n = 10,000   → 100,000,000 ops
```

---

## Performance Requirements

**CRITICAL:** Don't repeat the particle/cinematic performance mistake.

| Requirement | Implementation |
|-------------|----------------|
| No continuous React state updates for animation | Use `requestAnimationFrame` or CSS animations |
| Memoize stable components | `React.memo`, `useMemo` |
| Don't load Monaco until code editing needed | Lazy load |
| Avoid Framer Motion for every element | CSS transitions/animations |
| Pause when tab hidden | `document.hidden` + IntersectionObserver |
| Respect `prefers-reduced-motion` | Skip all animations |
| Large graphs | Canvas rendering, virtualization |
| State updates | Immutable snapshots, not 60fps React updates |

---

## Skill Tree Integration

**Do NOT create a second XP/skill system.**

```
Visualizer Completion
        ↓
Predict 8/10 states correctly
        ↓
Mastery +8% (existing Skill Mastery system)
        ↓
Binary Search skill
        ↓
Unlock Binary Search Quest (existing quest system)
```

---

## Migration Plan (Agent Must Produce Before Coding)

Before coding, the agent must inspect existing `DSAVisualizer.tsx`, `AlgorithmVisualizer.tsx`, and related components and report:

1. Current architecture
2. Reusable components
3. Broken functionality
4. Missing algorithms
5. Performance problems
6. Duplicate systems
7. Migration plan with milestones

**DO NOT IMPLEMENT until the plan is approved.**

---

## Signature Feature: "Predict the Algorithm"

This is the signature PlacementPro feature:

> Student sees a paused algorithm at a critical decision point. They predict what happens next. The algorithm executes. They get immediate feedback. This turns passive watching into active reasoning.

---

## Algorithms Priority (Phase 1)

1. Binary Search (with eliminated-half visualization)
2. Two Pointers (sum reasoning)
3. Sliding Window (animated window)
4. Bubble/Selection/Insertion Sort (race mode)
4. Merge Sort (merge animation)
5. Quick Sort (partition)
6. Binary Search Tree operations
6. BFS/DFS (queue/stack visualization)
7. Dijkstra (distance table + relaxation)
7. Recursion (factorial/fibonacci call stack)

---

## Technical Stack

- **Engine:** Pure TypeScript (no React, no DOM)
- **Renderer:** React + SVG/Canvas (selective)
- **State:** Immutable snapshots array
- **Timeline:** `requestAnimationFrame` or CSS animations
- **Code Editor:** Monaco (lazy-loaded, only for CHALLENGE/DEBUG modes)
- **No AI/API keys required** — fully deterministic, client-side execution

---

## Approval Required

**This spec must be reviewed and approved before any implementation begins.**

The agent must first:
1. Audit existing visualizer code
2. Produce migration plan
3. Get approval
4. Then implement in phases

---

*End of Specification*