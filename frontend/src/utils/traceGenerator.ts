/* ─────────────────────────────────────────────────────────────
 * Client-side algorithm trace generator.
 *
 * Produces step-by-step execution traces compatible with the
 * AlgorithmVisualizer component contract:
 *   - sorting steps:  sorting_data, comparing, sorted_indices
 *   - array steps:    array_data, pointers, active_indices
 *   - graph steps:    graph {nodes,edges}, visited_nodes,
 *                     current_node, active_edges
 *   - stack steps:    stack, active_index
 *   - queue steps:    queue, active_index
 * Every step may also carry: line, action, explanation, variables.
 * ------------------------------------------------------------ */

export interface GraphNode {
  id: string;
  label?: string;
}

export interface GraphEdge {
  from: string;
  to: string;
  weight?: number;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface TraceStep {
  line?: number;
  action?: string;
  explanation?: string;
  variables?: Record<string, unknown>;
  pointers?: Record<string, number>;
  active_indices?: number[];
  comparing?: number[];
  sorted_indices?: number[];
  sorting_data?: number[];
  array_data?: number[];
  graph?: GraphData;
  visited_nodes?: string[];
  current_node?: string;
  active_edges?: [string, string][];
  stack?: (number | string)[];
  queue?: (number | string)[];
  active_index?: number | null;
}

export interface GeneratedTrace {
  steps: TraceStep[];
  algorithm?: string;
  time_complexity?: string;
  space_complexity?: string;
  visualization_type?: string;
  code?: string;
  language?: string;
  source?: string;
}

export interface TemplateStep {
  [key: string]: unknown;
  step?: number;
  action?: string;
  explanation?: string;
  array?: number[];
  compare?: number[];
  sorted?: number[];
  scan?: number[];
  visited?: number[] | string[];
  queue?: number[] | string[];
  stack?: number[] | string[];
  current?: number | string;
  pivot?: number;
  low?: number;
  high?: number;
  mid?: number;
  index?: number;
  distances?: Record<string, unknown>;
  result?: unknown;
}

export interface TemplateData {
  type?: string;
  category?: string;
  description?: string;
  example_input?: unknown;
  steps?: TemplateStep[];
}

/* ── helpers ───────────────────────────────────────────────── */

function clone<T>(value: T): T {
  return Array.isArray(value) ? (value.slice() as unknown as T) : value;
}

function randomArray(size: number, min = 10, max = 99): number[] {
  return Array.from({ length: size }, () => Math.floor(Math.random() * (max - min + 1)) + min);
}

function randomOps(size: number, max = 50): number[] {
  return Array.from({ length: size }, () => Math.floor(Math.random() * max) + 1);
}

function randomGraph(nodeCount = 6, weighted = false): GraphData {
  const nodes: GraphNode[] = Array.from({ length: nodeCount }, (_, i) => ({ id: String(i) }));
  const edges: GraphEdge[] = [];
  const seen = new Set<string>();
  for (let i = 1; i < nodeCount; i++) {
    const from = String(Math.floor(Math.random() * i));
    const to = String(i);
    const key = `${from}-${to}`;
    if (!seen.has(key)) {
      seen.add(key);
      edges.push({ from, to, ...(weighted ? { weight: Math.floor(Math.random() * 6) + 1 } : {}) });
    }
  }
  for (let i = 0; i < nodeCount; i++) {
    const a = String(Math.floor(Math.random() * nodeCount));
    const b = String(Math.floor(Math.random() * nodeCount));
    if (a === b) continue;
    const key = `${a}-${b}`;
    if (!seen.has(key)) {
      seen.add(key);
      edges.push({ from: a, to: b, ...(weighted ? { weight: Math.floor(Math.random() * 6) + 1 } : {}) });
    }
  }
  return { nodes, edges };
}

function adjacencyFromGraph(graph: GraphData): Record<string, string[]> {
  const adj: Record<string, string[]> = {};
  graph.nodes.forEach((n) => { adj[n.id] = []; });
  graph.edges.forEach((e) => {
    if (adj[e.from]) adj[e.from].push(e.to);
    if (adj[e.to]) adj[e.to].push(e.from);
  });
  return adj;
}

function weightedAdjacencyFromGraph(graph: GraphData): Record<string, [string, number][]> {
  const adj: Record<string, [string, number][]> = {};
  graph.nodes.forEach((n) => { adj[n.id] = []; });
  graph.edges.forEach((e) => {
    if (adj[e.from]) adj[e.from].push([e.to, e.weight ?? 1]);
    if (adj[e.to]) adj[e.to].push([e.from, e.weight ?? 1]);
  });
  return adj;
}

/* ── sorting ────────────────────────────────────────────────── */

const BUBBLE_CODE = [
  "def bubble_sort(arr):",
  "    n = len(arr)",
  "    for i in range(n - 1):",
  "        swapped = False",
  "        for j in range(n - 1 - i):",
  "            if arr[j] > arr[j + 1]:",
  "                arr[j], arr[j + 1] = arr[j + 1], arr[j]",
  "                swapped = True",
  "        if not swapped:",
  "            break",
  "    return arr",
].join("\n");

function bubbleSortTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const steps: TraceStep[] = [];
  const n = arr.length;
  steps.push({ line: 1, action: "Initialize", explanation: `Bubble sort on ${n} elements.`, sorting_data: clone(arr), variables: { n, swapped: false }, active_indices: [] });
  for (let i = 0; i < n - 1; i++) {
    let swapped = false;
    for (let j = 0; j < n - 1 - i; j++) {
      steps.push({
        line: 6, action: `Compare arr[${j}]=${arr[j]} and arr[${j + 1}]=${arr[j + 1]}`,
        explanation: `Check if adjacent elements are out of order.`,
        sorting_data: clone(arr), comparing: [j, j + 1], sorted_indices: sortedTail(n, i), variables: { i, j, swapped },
      });
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        swapped = true;
        steps.push({
          line: 7, action: `Swap: ${arr[j + 1]} and ${arr[j]} changed places`,
          explanation: `${arr[j]} > ${arr[j + 1]}, so they swap.`,
          sorting_data: clone(arr), comparing: [j, j + 1], sorted_indices: sortedTail(n, i), variables: { i, j, swapped },
        });
      }
    }
    steps.push({
      line: 9, action: `Pass ${i + 1} complete`,
      explanation: swapped ? `Largest unsorted value bubbled to position ${n - 1 - i}.` : "No swaps this pass — array is already sorted.",
      sorting_data: clone(arr), sorted_indices: sortedTail(n, i + 1), variables: { i, swapped },
    });
    if (!swapped) break;
  }
  steps.push({ line: 11, action: "Done", explanation: "Array is sorted.", sorting_data: clone(arr), sorted_indices: arr.map((_, i) => i), variables: { result: clone(arr) } });
  return { steps, algorithm: "Bubble Sort", time_complexity: "O(n²)", space_complexity: "O(1)", visualization_type: "sorting", code: BUBBLE_CODE };
}

function sortedTail(n: number, i: number): number[] {
  const out: number[] = [];
  for (let k = n - 1; k >= n - i && k >= 0; k--) out.push(k);
  return out;
}

const SELECTION_CODE = [
  "def selection_sort(arr):",
  "    n = len(arr)",
  "    for i in range(n):",
  "        min_idx = i",
  "        for j in range(i + 1, n):",
  "            if arr[j] < arr[min_idx]:",
  "                min_idx = j",
  "        arr[i], arr[min_idx] = arr[min_idx], arr[i]",
  "    return arr",
].join("\n");

function selectionSortTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const steps: TraceStep[] = [];
  const n = arr.length;
  steps.push({ line: 1, action: "Initialize", explanation: `Selection sort on ${n} elements.`, sorting_data: clone(arr), variables: { n }, active_indices: [] });
  for (let i = 0; i < n; i++) {
    let minIdx = i;
    steps.push({ line: 4, action: `Start pass ${i}: assume minimum at index ${i}`, explanation: "Each pass finds the smallest element in the unsorted region.", sorting_data: clone(arr), active_indices: [i], sorted_indices: sortedHead(i), variables: { i, min_idx: minIdx } });
    for (let j = i + 1; j < n; j++) {
      steps.push({ line: 6, action: `Is arr[${j}]=${arr[j]} < arr[${minIdx}]=${arr[minIdx]}?`, explanation: `Compare candidate ${arr[j]} against current minimum ${arr[minIdx]}.`, sorting_data: clone(arr), active_indices: [minIdx, j], sorted_indices: sortedHead(i), variables: { i, j, min_idx: minIdx } });
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
        steps.push({ line: 7, action: `New minimum found at index ${j}`, explanation: `${arr[j]} is smaller, remember it as the new minimum.`, sorting_data: clone(arr), active_indices: [minIdx], sorted_indices: sortedHead(i), variables: { i, j, min_idx: minIdx } });
      }
    }
    if (minIdx !== i) {
      [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
    }
    steps.push({ line: 8, action: `Place minimum ${arr[i]} at position ${i}`, explanation: minIdx !== i ? `Swap arr[${i}] with arr[${minIdx}].` : "Already in place.", sorting_data: clone(arr), active_indices: [i], sorted_indices: sortedHead(i + 1), variables: { i, min_idx: minIdx } });
  }
  steps.push({ line: 9, action: "Done", explanation: "Array is sorted.", sorting_data: clone(arr), sorted_indices: arr.map((_, i) => i), variables: { result: clone(arr) } });
  return { steps, algorithm: "Selection Sort", time_complexity: "O(n²)", space_complexity: "O(1)", visualization_type: "sorting", code: SELECTION_CODE };
}

function sortedHead(i: number): number[] {
  return Array.from({ length: i }, (_, k) => k);
}

const INSERTION_CODE = [
  "def insertion_sort(arr):",
  "    for i in range(1, len(arr)):",
  "        key = arr[i]",
  "        j = i - 1",
  "        while j >= 0 and arr[j] > key:",
  "            arr[j + 1] = arr[j]",
  "            j -= 1",
  "        arr[j + 1] = key",
  "    return arr",
].join("\n");

function insertionSortTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const steps: TraceStep[] = [];
  steps.push({ line: 1, action: "Initialize", explanation: "Insertion sort — build the sorted region one element at a time.", sorting_data: clone(arr), sorted_indices: [0], variables: {} });
  for (let i = 1; i < arr.length; i++) {
    const key = arr[i];
    let j = i - 1;
    steps.push({ line: 3, action: `Take key = arr[${i}] = ${key}`, explanation: `Insert ${key} into the sorted region [0..${i - 1}].`, sorting_data: clone(arr), active_indices: [i], sorted_indices: sortedHead(i), variables: { i, key, j } });
    while (j >= 0 && arr[j] > key) {
      steps.push({ line: 5, action: `arr[${j}]=${arr[j]} > key=${key}, shift right`, explanation: `${arr[j]} is greater than ${key}, so it moves one position right to make room.`, sorting_data: clone(arr), active_indices: [j, j + 1], sorted_indices: sortedHead(i), variables: { i, key, j } });
      arr[j + 1] = arr[j];
      steps.push({ line: 6, action: `Shift ${arr[j + 1]} to index ${j + 1}`, explanation: "Element moved right.", sorting_data: clone(arr), active_indices: [j + 1], sorted_indices: sortedHead(i), variables: { i, key, j } });
      j -= 1;
    }
    arr[j + 1] = key;
    steps.push({ line: 8, action: `Insert key ${key} at index ${j + 1}`, explanation: `${key} is in its final sorted position within the sorted region.`, sorting_data: clone(arr), active_indices: [j + 1], sorted_indices: sortedHead(i + 1), variables: { i, key, j } });
  }
  steps.push({ line: 9, action: "Done", explanation: "Array is sorted.", sorting_data: clone(arr), sorted_indices: arr.map((_, i) => i), variables: { result: clone(arr) } });
  return { steps, algorithm: "Insertion Sort", time_complexity: "O(n²)", space_complexity: "O(1)", visualization_type: "sorting", code: INSERTION_CODE };
}

const MERGE_CODE = [
  "def merge_sort(arr):",
  "    n = len(arr)",
  "    width = 1",
  "    while width < n:",
  "        for left in range(0, n, 2 * width):",
  "            mid = min(left + width, n)",
  "            right = min(left + 2 * width, n)",
  "            merge(arr, left, mid, right)",
  "        width *= 2",
  "    return arr",
  "",
  "def merge(arr, left, mid, right):",
  "    merged = []",
  "    i, j = left, mid",
  "    while i < mid and j < right:",
  "        if arr[i] <= arr[j]:",
  "            merged.append(arr[i]); i += 1",
  "        else:",
  "            merged.append(arr[j]); j += 1",
  "    merged += arr[i:mid] + arr[j:right]",
  "    arr[left:right] = merged",
].join("\n");

function mergeSortTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const steps: TraceStep[] = [];
  const n = arr.length;
  steps.push({ line: 1, action: "Initialize", explanation: `Merge sort on ${n} elements — divide into runs, merge pairwise.`, sorting_data: clone(arr), variables: { n, width: 1 } });
  let width = 1;
  while (width < n) {
    steps.push({ line: 4, action: `Run width = ${width}`, explanation: width === 1 ? "Treat each element as a sorted run of size 1." : `Merge adjacent runs of size ${width}.`, sorting_data: clone(arr), variables: { n, width } });
    for (let left = 0; left < n; left += 2 * width) {
      const mid = Math.min(left + width, n);
      const right = Math.min(left + 2 * width, n);
      if (mid >= right) continue;
      steps.push({ line: 8, action: `Merge runs [${left}..${mid - 1}] and [${mid}..${right - 1}]`, explanation: `Combines two sorted runs into one sorted run [${left}..${right - 1}].`, sorting_data: clone(arr), active_indices: range(left, right), variables: { left, mid, right } });
      const merged: number[] = [];
      let i = left;
      let j = mid;
      while (i < mid && j < right) {
        const cmp: [number, number] = [i, j];
        steps.push({ line: 15, action: `Compare arr[${i}]=${arr[i]} vs arr[${j}]=${arr[j]}`, explanation: "Take the smaller of the two run heads into the merged output.", sorting_data: clone(arr), comparing: [i, j], active_indices: range(left, right), variables: { i, j, left, mid, right } });
        if (arr[i] <= arr[j]) { merged.push(arr[i]); i++; }
        else { merged.push(arr[j]); j++; }
      }
      while (i < mid) { merged.push(arr[i]); i++; }
      while (j < right) { merged.push(arr[j]); j++; }
      const before = clone(arr);
      for (let k = 0; k < merged.length; k++) arr[left + k] = merged[k];
      steps.push({ line: 20, action: `Write merged run back`, explanation: `Result: [${merged.join(", ")}] is now sorted.`, sorting_data: clone(arr), sorted_indices: range(left, right), variables: { merged: clone(merged), left, right } });
      if (JSON.stringify(before) === JSON.stringify(arr)) {
        // no change — still push a descriptive step is enough
      }
    }
    width *= 2;
  }
  steps.push({ line: 10, action: "Done", explanation: "Array is sorted.", sorting_data: clone(arr), sorted_indices: arr.map((_, i) => i), variables: { result: clone(arr) } });
  return { steps, algorithm: "Merge Sort", time_complexity: "O(n log n)", space_complexity: "O(n)", visualization_type: "sorting", code: MERGE_CODE };
}

function range(a: number, b: number): number[] {
  const out: number[] = [];
  for (let i = a; i < b; i++) out.push(i);
  return out;
}

const QUICK_CODE = [
  "def quick_sort(arr):",
  "    stack = [(0, len(arr) - 1)]",
  "    while stack:",
  "        lo, hi = stack.pop()",
  "        if lo >= hi:",
  "            continue",
  "        p = partition(arr, lo, hi)",
  "        stack.append((lo, p - 1))",
  "        stack.append((p + 1, hi))",
  "    return arr",
  "",
  "def partition(arr, lo, hi):",
  "    pivot = arr[hi]",
  "    i = lo - 1",
  "    for j in range(lo, hi):",
  "        if arr[j] < pivot:",
  "            i += 1",
  "            arr[i], arr[j] = arr[j], arr[i]",
  "    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]",
  "    return i + 1",
].join("\n");

function quickSortTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const steps: TraceStep[] = [];
  const stack: [number, number][] = [[0, arr.length - 1]];
  steps.push({ line: 1, action: "Initialize", explanation: "Quick sort — partition around a pivot, recurse on both sides.", sorting_data: clone(arr), variables: { stack: "[(0, n-1)]" } });
  while (stack.length) {
    const [lo, hi] = stack.pop() as [number, number];
    if (lo >= hi) {
      steps.push({ line: 5, action: `Range [${lo}..${hi}] has ≤1 element`, explanation: "A single-element range is trivially sorted.", sorting_data: clone(arr), sorted_indices: [lo], variables: { lo, hi } });
      continue;
    }
    const pivot = arr[hi];
    let i = lo - 1;
    steps.push({ line: 12, action: `Pivot = arr[${hi}] = ${pivot}`, explanation: "The last element of the range is chosen as the pivot.", sorting_data: clone(arr), active_indices: [hi], variables: { lo, hi, pivot } });
    for (let j = lo; j < hi; j++) {
      steps.push({ line: 15, action: `Is arr[${j}]=${arr[j]} < pivot=${pivot}?`, explanation: "Elements smaller than the pivot move to the left partition.", sorting_data: clone(arr), active_indices: [j, hi], variables: { lo, hi, pivot, i, j } });
      if (arr[j] < pivot) {
        i += 1;
        if (i !== j) {
          [arr[i], arr[j]] = [arr[j], arr[i]];
          steps.push({ line: 17, action: `Swap arr[${i}] ↔ arr[${j}]`, explanation: `Move ${arr[i]} into the left partition.`, sorting_data: clone(arr), comparing: [i, j], variables: { lo, hi, pivot, i, j } });
        }
      }
    }
    const p = i + 1;
    if (p !== hi) {
      [arr[p], arr[hi]] = [arr[hi], arr[p]];
    }
    steps.push({ line: 18, action: `Place pivot ${pivot} at index ${p}`, explanation: `Pivot is now in its final sorted position.`, sorting_data: clone(arr), active_indices: [p], sorted_indices: [p], variables: { lo, hi, p } });
    stack.push([lo, p - 1]);
    stack.push([p + 1, hi]);
    steps.push({ line: 8, action: `Recurse on [${lo}..${p - 1}] and [${p + 1}..${hi}]`, explanation: "Sort both sides of the pivot.", sorting_data: clone(arr), sorted_indices: [p], variables: { stack: JSON.stringify(stack) } });
  }
  steps.push({ line: 10, action: "Done", explanation: "Array is sorted.", sorting_data: clone(arr), sorted_indices: arr.map((_, i) => i), variables: { result: clone(arr) } });
  return { steps, algorithm: "Quick Sort", time_complexity: "O(n log n)", space_complexity: "O(log n)", visualization_type: "sorting", code: QUICK_CODE };
}

/* ── searching ──────────────────────────────────────────────── */

const LINEAR_CODE = [
  "def linear_search(arr, target):",
  "    for i in range(len(arr)):",
  "        if arr[i] == target:",
  "            return i",
  "    return -1",
].join("\n");

function linearSearchTrace(input: number[]): GeneratedTrace {
  const arr = clone(input);
  const target = arr.length > 1 ? arr[Math.floor(arr.length / 2)] : arr[0];
  const steps: TraceStep[] = [];
  steps.push({ line: 1, action: "Initialize", explanation: `Linear search for ${target} — scan from left to right.`, array_data: clone(arr), pointers: { i: 0 }, variables: { target } });
  for (let i = 0; i < arr.length; i++) {
    steps.push({ line: 3, action: `Check arr[${i}]=${arr[i]} vs target ${target}`, explanation: arr[i] === target ? "Match found!" : `${arr[i]} ≠ ${target}, keep scanning.`, array_data: clone(arr), active_indices: [i], pointers: { i }, variables: { target, i } });
    if (arr[i] === target) {
      steps.push({ line: 4, action: `Found ${target} at index ${i}`, explanation: "Return the index immediately.", array_data: clone(arr), active_indices: [i], variables: { result: i } });
      return { steps, algorithm: "Linear Search", time_complexity: "O(n)", space_complexity: "O(1)", visualization_type: "array", code: LINEAR_CODE };
    }
  }
  steps.push({ line: 5, action: "Target not found", explanation: `Return -1 — ${target} is not in the array.`, array_data: clone(arr), variables: { result: -1 } });
  return { steps, algorithm: "Linear Search", time_complexity: "O(n)", space_complexity: "O(1)", visualization_type: "array", code: LINEAR_CODE };
}

const BINARY_CODE = [
  "def binary_search(arr, target):",
  "    low, high = 0, len(arr) - 1",
  "    while low <= high:",
  "        mid = (low + high) // 2",
  "        if arr[mid] == target:",
  "            return mid",
  "        elif arr[mid] < target:",
  "            low = mid + 1",
  "        else:",
  "            high = mid - 1",
  "    return -1",
].join("\n");

function binarySearchTrace(input: number[]): GeneratedTrace {
  const arr = clone(input).sort((a, b) => a - b);
  const target = arr.length > 1 ? arr[Math.floor(arr.length / 2)] : arr[0];
  const steps: TraceStep[] = [];
  let low = 0;
  let high = arr.length - 1;
  steps.push({ line: 2, action: "Initialize", explanation: `Binary search for ${target} on a sorted array.`, array_data: clone(arr), pointers: { low, high }, variables: { target, low, high } });
  while (low <= high) {
    const mid = Math.floor((low + high) / 2);
    steps.push({ line: 4, action: `mid = (${low} + ${high}) / 2 = ${mid}`, explanation: "Halve the search space around the middle.", array_data: clone(arr), active_indices: [mid], pointers: { low, high, mid }, variables: { target, low, high, mid } });
    if (arr[mid] === target) {
      steps.push({ line: 6, action: `Found ${target} at index ${mid}`, explanation: "arr[mid] equals the target — return the index.", array_data: clone(arr), active_indices: [mid], variables: { result: mid } });
      return { steps, algorithm: "Binary Search", time_complexity: "O(log n)", space_complexity: "O(1)", visualization_type: "array", code: BINARY_CODE };
    }
    if (arr[mid] < target) {
      low = mid + 1;
      steps.push({ line: 8, action: `arr[${mid}] < target → low = ${low}`, explanation: "Target must be in the right half.", array_data: clone(arr), active_indices: [mid], pointers: { low, high }, variables: { target, low, high } });
    } else {
      high = mid - 1;
      steps.push({ line: 10, action: `arr[${mid}] > target → high = ${high}`, explanation: "Target must be in the left half.", array_data: clone(arr), active_indices: [mid], pointers: { low, high }, variables: { target, low, high } });
    }
  }
  steps.push({ line: 11, action: "Target not found", explanation: `Search space exhausted — return -1.`, array_data: clone(arr), variables: { result: -1 } });
  return { steps, algorithm: "Binary Search", time_complexity: "O(log n)", space_complexity: "O(1)", visualization_type: "array", code: BINARY_CODE };
}

/* ── graph ──────────────────────────────────────────────────── */

const BFS_CODE = [
  "from collections import deque",
  "def bfs(graph, start):",
  "    visited = {start}",
  "    queue = deque([start])",
  "    order = []",
  "    while queue:",
  "        node = queue.popleft()",
  "        order.append(node)",
  "        for neighbor in graph[node]:",
  "            if neighbor not in visited:",
  "                visited.add(neighbor)",
  "                queue.append(neighbor)",
  "    return order",
].join("\n");

function bfsTrace(graph: GraphData): GeneratedTrace {
  const adj = adjacencyFromGraph(graph);
  const start = graph.nodes[0]?.id ?? "0";
  const visited = new Set<string>([start]);
  const queue: string[] = [start];
  const order: string[] = [];
  const steps: TraceStep[] = [];
  steps.push({ line: 2, action: "Initialize", explanation: `BFS from node ${start} — explore level by level.`, graph, visited_nodes: [start], current_node: start, queue, variables: { queue: clone(queue), visited: Array.from(visited) } });
  while (queue.length) {
    const node = queue.shift() as string;
    order.push(node);
    steps.push({ line: 7, action: `Dequeue ${node}`, explanation: "Process the front of the queue.", graph, visited_nodes: Array.from(visited), current_node: node, queue: clone(queue), variables: { node, queue: clone(queue), order: clone(order) } });
    for (const neighbor of adj[node] || []) {
      const edge: [string, string] = [node, neighbor];
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
        steps.push({ line: 10, action: `Visit ${neighbor} from ${node}`, explanation: `Discovered ${neighbor} for the first time, enqueue it.`, graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], queue: clone(queue), variables: { neighbor, queue: clone(queue), visited: Array.from(visited) } });
      } else {
        steps.push({ line: 10, action: `${neighbor} already visited`, explanation: `Skip ${neighbor} — already discovered.`, graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], queue: clone(queue), variables: { neighbor } });
      }
    }
  }
  steps.push({ line: 13, action: "Done", explanation: `BFS order: [${order.join(", ")}]`, graph, visited_nodes: Array.from(visited), variables: { order: clone(order) } });
  return { steps, algorithm: "BFS (Breadth-First Search)", time_complexity: "O(V+E)", space_complexity: "O(V)", visualization_type: "default", code: BFS_CODE };
}

const DFS_CODE = [
  "def dfs(graph, start):",
  "    visited = {start}",
  "    stack = [start]",
  "    order = []",
  "    while stack:",
  "        node = stack.pop()",
  "        order.append(node)",
  "        for neighbor in graph[node]:",
  "            if neighbor not in visited:",
  "                visited.add(neighbor)",
  "                stack.append(neighbor)",
  "    return order",
].join("\n");

function dfsTrace(graph: GraphData): GeneratedTrace {
  const adj = adjacencyFromGraph(graph);
  const start = graph.nodes[0]?.id ?? "0";
  const visited = new Set<string>([start]);
  const stack: string[] = [start];
  const order: string[] = [];
  const steps: TraceStep[] = [];
  steps.push({ line: 1, action: "Initialize", explanation: `DFS from node ${start} — go as deep as possible, then backtrack.`, graph, visited_nodes: [start], current_node: start, stack: clone(stack), variables: { stack: clone(stack), visited: Array.from(visited) } });
  while (stack.length) {
    const node = stack.pop() as string;
    order.push(node);
    steps.push({ line: 6, action: `Pop ${node}`, explanation: "Process the top of the stack.", graph, visited_nodes: Array.from(visited), current_node: node, stack: clone(stack), variables: { node, stack: clone(stack), order: clone(order) } });
    for (const neighbor of adj[node] || []) {
      const edge: [string, string] = [node, neighbor];
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        stack.push(neighbor);
        steps.push({ line: 9, action: `Discover ${neighbor} from ${node}`, explanation: `Mark ${neighbor} visited and push it onto the stack.`, graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], stack: clone(stack), variables: { neighbor, stack: clone(stack), visited: Array.from(visited) } });
      } else {
        steps.push({ line: 9, action: `${neighbor} already visited`, explanation: "Backtrack — all neighbors are already discovered.", graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], stack: clone(stack), variables: { neighbor } });
      }
    }
  }
  steps.push({ line: 12, action: "Done", explanation: `DFS order: [${order.join(", ")}]`, graph, visited_nodes: Array.from(visited), variables: { order: clone(order) } });
  return { steps, algorithm: "DFS (Depth-First Search)", time_complexity: "O(V+E)", space_complexity: "O(V)", visualization_type: "default", code: DFS_CODE };
}

const DIJKSTRA_CODE = [
  "import heapq",
  "def dijkstra(graph, start):",
  "    dist = {node: float('inf') for node in graph}",
  "    dist[start] = 0",
  "    pq = [(0, start)]",
  "    while pq:",
  "        d, node = heapq.heappop(pq)",
  "        if d > dist[node]: continue",
  "        for neighbor, w in graph[node]:",
  "            nd = d + w",
  "            if nd < dist[neighbor]:",
  "                dist[neighbor] = nd",
  "                heapq.heappush(pq, (nd, neighbor))",
  "    return dist",
].join("\n");

function dijkstraTrace(graph: GraphData): GeneratedTrace {
  const adj = weightedAdjacencyFromGraph(graph);
  const start = graph.nodes[0]?.id ?? "0";
  const dist: Record<string, number> = {};
  graph.nodes.forEach((n) => { dist[n.id] = Infinity; });
  dist[start] = 0;
  const visited = new Set<string>();
  const pq: [number, string][] = [[0, start]];
  const steps: TraceStep[] = [];
  steps.push({ line: 2, action: "Initialize", explanation: `Dijkstra from node ${start} — all distances start at ∞ except the source.`, graph, visited_nodes: [], current_node: start, variables: { dist: distLabel(dist) } });
  while (pq.length) {
    pq.sort((a, b) => a[0] - b[0]);
    const [d, node] = pq.shift() as [number, string];
    if (d > dist[node]) continue;
    visited.add(node);
    steps.push({ line: 7, action: `Extract ${node} (shortest distance ${d})`, explanation: `Node ${node} now has its final shortest distance.`, graph, visited_nodes: Array.from(visited), current_node: node, variables: { node, d, dist: distLabel(dist) } });
    for (const [neighbor, w] of adj[node] || []) {
      const nd = d + w;
      const edge: [string, string] = [node, neighbor];
      if (nd < dist[neighbor]) {
        const before = dist[neighbor];
        dist[neighbor] = nd;
        pq.push([nd, neighbor]);
        steps.push({ line: 11, action: `Relax edge ${node}→${neighbor}: ${before === Infinity ? "∞" : before} → ${nd}`, explanation: `A shorter path to ${neighbor} was found via ${node} (weight ${w}).`, graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], variables: { neighbor, w, old: before === Infinity ? "∞" : before, new: nd, dist: distLabel(dist) } });
      } else {
        steps.push({ line: 10, action: `Edge ${node}→${neighbor} (${w}) not an improvement`, explanation: `Current distance ${dist[neighbor] === Infinity ? "∞" : dist[neighbor]} ≤ ${nd}, skip.`, graph, visited_nodes: Array.from(visited), current_node: node, active_edges: [edge], variables: { neighbor, w, dist: distLabel(dist) } });
      }
    }
  }
  steps.push({ line: 14, action: "Done", explanation: `Shortest distances from ${start}: ${Object.entries(dist).map(([k, v]) => `${k}=${v}`).join(", ")}`, graph, visited_nodes: Array.from(visited), variables: { dist: distLabel(dist) } });
  return { steps, algorithm: "Dijkstra Shortest Path", time_complexity: "O((V+E) log V)", space_complexity: "O(V)", visualization_type: "default", code: DIJKSTRA_CODE };
}

function distLabel(dist: Record<string, number>): Record<string, string> {
  const out: Record<string, string> = {};
  Object.entries(dist).forEach(([k, v]) => { out[k] = v === Infinity ? "∞" : String(v); });
  return out;
}

/* ── data structures ────────────────────────────────────────── */

const STACK_CODE = [
  "stack = []",
  "def push(x):",
  "    stack.append(x)",
  "def pop():",
  "    return stack.pop()",
  "def peek():",
  "    return stack[-1] if stack else None",
].join("\n");

function stackOpsTrace(values: number[]): GeneratedTrace {
  const stack: number[] = [];
  const steps: TraceStep[] = [];
  steps.push({ line: 1, action: "Initialize", explanation: "Stack — LIFO. push adds to the top, pop removes from the top.", stack: [], active_index: null, variables: {} });
  values.forEach((v, k) => {
    const op = k % 3 === 2 && stack.length ? "pop" : "push";
    if (op === "push") {
      stack.push(v);
      steps.push({ line: 2, action: `push(${v})`, explanation: `${v} is placed on top of the stack.`, stack: clone(stack), active_index: stack.length - 1, variables: { op: "push", x: v, top: v } });
    } else {
      const popped = stack.pop();
      steps.push({ line: 4, action: `pop() → ${popped}`, explanation: `${popped} is removed from the top (LIFO).`, stack: clone(stack), active_index: stack.length - 1, variables: { op: "pop", popped } });
    }
  });
  steps.push({ line: 6, action: "Complete", explanation: `Final stack: [${stack.join(", ")}]`, stack: clone(stack), active_index: stack.length - 1, variables: { stack: clone(stack) } });
  return { steps, algorithm: "Stack Operations", time_complexity: "O(1)", space_complexity: "O(n)", visualization_type: "default", code: STACK_CODE };
}

const QUEUE_CODE = [
  "from collections import deque",
  "queue = deque()",
  "def enqueue(x):",
  "    queue.append(x)",
  "def dequeue():",
  "    return queue.popleft()",
].join("\n");

function queueOpsTrace(values: number[]): GeneratedTrace {
  const queue: number[] = [];
  const steps: TraceStep[] = [];
  steps.push({ line: 2, action: "Initialize", explanation: "Queue — FIFO. enqueue adds to the back, dequeue removes from the front.", queue: [], active_index: null, variables: {} });
  values.forEach((v, k) => {
    const op = k % 3 === 2 && queue.length ? "dequeue" : "enqueue";
    if (op === "enqueue") {
      queue.push(v);
      steps.push({ line: 3, action: `enqueue(${v})`, explanation: `${v} joins at the back of the queue.`, queue: clone(queue), active_index: 0, variables: { op: "enqueue", x: v } });
    } else {
      const dequeued = queue.shift();
      steps.push({ line: 5, action: `dequeue() → ${dequeued}`, explanation: `${dequeued} leaves from the front (FIFO).`, queue: clone(queue), active_index: 0, variables: { op: "dequeue", dequeued } });
    }
  });
  steps.push({ line: 6, action: "Complete", explanation: `Final queue: [${queue.join(", ")}]`, queue: clone(queue), active_index: 0, variables: { queue: clone(queue) } });
  return { steps, algorithm: "Queue Operations", time_complexity: "O(1)", space_complexity: "O(n)", visualization_type: "default", code: QUEUE_CODE };
}

const HEAP_CODE = [
  "def heap_push(heap, x):",
  "    heap.append(x)",
  "    i = len(heap) - 1",
  "    while i > 0:",
  "        parent = (i - 1) // 2",
  "        if heap[i] < heap[parent]:",
  "            heap[i], heap[parent] = heap[parent], heap[i]",
  "            i = parent",
  "        else:",
  "            break",
  "",
  "def heap_pop(heap):",
  "    root = heap[0]",
  "    last = heap.pop()",
  "    if heap:",
  "        heap[0] = last",
  "        i, n = 0, len(heap)",
  "        while i < n:",
  "            l, r = 2*i+1, 2*i+2",
  "            smallest = i",
  "            if l < n and heap[l] < heap[smallest]: smallest = l",
  "            if r < n and heap[r] < heap[smallest]: smallest = r",
  "            if smallest == i: break",
  "            heap[i], heap[smallest] = heap[smallest], heap[i]",
  "            i = smallest",
  "    return root",
].join("\n");

function heapOpsTrace(values: number[]): GeneratedTrace {
  const heap: number[] = [];
  const steps: TraceStep[] = [];
  steps.push({ line: 1, action: "Initialize", explanation: "Min-heap — parent is always ≤ its children. Array layout: node i → children 2i+1, 2i+2.", array_data: [], active_indices: [], variables: { heap: [] } });
  values.forEach((v, k) => {
    if (k % 4 === 3 && heap.length > 1) {
      const root = heap[0];
      const last = heap.pop() as number;
      steps.push({ line: 12, action: `extract-min() → ${root}`, explanation: `The root ${root} is the minimum; ${last} moves to the root and sifts down.`, array_data: clone(heap), active_indices: [0], variables: { root, last, heap: clone(heap) } });
      if (heap.length) {
        heap[0] = last;
        let i = 0;
        const n = heap.length;
        steps.push({ line: 17, action: `Sift down ${last}`, explanation: "Restore the heap property by bubbling down.", array_data: clone(heap), active_indices: [i], variables: { i, heap: clone(heap) } });
        while (i < n) {
          const l = 2 * i + 1;
          const r = 2 * i + 2;
          let smallest = i;
          if (l < n && heap[l] < heap[smallest]) smallest = l;
          if (r < n && heap[r] < heap[smallest]) smallest = r;
          if (smallest === i) break;
          [heap[i], heap[smallest]] = [heap[smallest], heap[i]];
          steps.push({ line: 25, action: `Swap ${heap[i]} ↔ ${heap[smallest]}`, explanation: "Child is smaller — swap to maintain min-heap.", array_data: clone(heap), active_indices: [i, smallest], variables: { i, smallest, heap: clone(heap) } });
          i = smallest;
        }
      }
    } else {
      heap.push(v);
      let i = heap.length - 1;
      steps.push({ line: 2, action: `insert(${v})`, explanation: `${v} is added as a leaf, then sifts up.`, array_data: clone(heap), active_indices: [i], variables: { x: v, heap: clone(heap) } });
      while (i > 0) {
        const parent = Math.floor((i - 1) / 2);
        if (heap[i] < heap[parent]) {
          [heap[i], heap[parent]] = [heap[parent], heap[i]];
          steps.push({ line: 7, action: `Sift up: swap with parent ${heap[i]}`, explanation: `${heap[i]} < ${heap[parent]} — swap to restore heap property.`, array_data: clone(heap), active_indices: [i, parent], variables: { i, parent, heap: clone(heap) } });
          i = parent;
        } else {
          steps.push({ line: 9, action: `${heap[i]} ≥ parent, stop`, explanation: "Heap property satisfied.", array_data: clone(heap), active_indices: [i], variables: { i, parent, heap: clone(heap) } });
          break;
        }
      }
    }
  });
  steps.push({ line: 27, action: "Complete", explanation: `Final heap (array view): [${heap.join(", ")}]`, array_data: clone(heap), active_indices: [], variables: { heap: clone(heap) } });
  return { steps, algorithm: "Binary Heap Operations", time_complexity: "O(log n)", space_complexity: "O(n)", visualization_type: "array", code: HEAP_CODE };
}

/* ── dispatcher ─────────────────────────────────────────────── */

const DEFAULT_GRAPH: GraphData = {
  nodes: [{ id: "0" }, { id: "1" }, { id: "2" }, { id: "3" }, { id: "4" }, { id: "5" }],
  edges: [
    { from: "0", to: "1" },
    { from: "0", to: "2" },
    { from: "1", to: "3" },
    { from: "2", to: "3" },
    { from: "3", to: "4" },
    { from: "4", to: "5" },
  ],
};

const DEFAULT_WEIGHTED_GRAPH: GraphData = {
  nodes: [{ id: "0" }, { id: "1" }, { id: "2" }, { id: "3" }, { id: "4" }],
  edges: [
    { from: "0", to: "1", weight: 4 },
    { from: "0", to: "2", weight: 1 },
    { from: "1", to: "3", weight: 1 },
    { from: "2", to: "1", weight: 2 },
    { from: "2", to: "3", weight: 5 },
    { from: "3", to: "4", weight: 3 },
  ],
};

export interface TraceInput {
  array?: number[];
  graph?: GraphData;
  values?: number[];
}

export function generateTrace(algoId: string, input: TraceInput = {}): GeneratedTrace {
  switch (algoId) {
    case "bubble":
      return bubbleSortTrace(input.array ?? randomArray(10));
    case "selection":
      return selectionSortTrace(input.array ?? randomArray(10));
    case "insertion":
      return insertionSortTrace(input.array ?? randomArray(10));
    case "merge":
      return mergeSortTrace(input.array ?? randomArray(10));
    case "quick":
      return quickSortTrace(input.array ?? randomArray(10));
    case "linear":
      return linearSearchTrace(input.array ?? randomArray(9));
    case "binary":
      return binarySearchTrace(input.array ?? randomArray(9));
    case "bfs":
      return bfsTrace(input.graph ?? DEFAULT_GRAPH);
    case "dfs":
      return dfsTrace(input.graph ?? DEFAULT_GRAPH);
    case "dijkstra":
      return dijkstraTrace(input.graph ?? DEFAULT_WEIGHTED_GRAPH);
    case "stack":
      return stackOpsTrace(input.values ?? randomOps(10));
    case "queue":
      return queueOpsTrace(input.values ?? randomOps(10));
    case "heap":
      return heapOpsTrace(input.values ?? randomOps(10));
    default:
      return { steps: [], algorithm: algoId, visualization_type: "default", code: "" };
  }
}

export function generateInputFor(algoId: string): TraceInput {
  switch (algoId) {
    case "bfs":
    case "dfs":
      return { graph: randomGraph(6, false) };
    case "dijkstra":
      return { graph: randomGraph(5, true) };
    case "stack":
    case "queue":
    case "heap":
      return { values: randomOps(10) };
    default:
      return { array: randomArray(algoId === "linear" || algoId === "binary" ? 9 : 10) };
  }
}

/* ── normalize backend template steps (Compare Visualizer) ──── */

const SORTING_TEMPLATE_TYPES = new Set(["bars", "sorting", "dp_table"]);
const ARRAY_TEMPLATE_TYPES = new Set(["array", "matrix"]);
const GRAPH_TEMPLATE_TYPES = new Set(["graph"]);
const STACK_TEMPLATE_TYPES = new Set(["stack"]);
const QUEUE_TEMPLATE_TYPES = new Set(["queue"]);
const TREE_TEMPLATE_TYPES = new Set(["binary_tree", "recursion_tree"]);
const LINKED_LIST_TEMPLATE_TYPES = new Set(["linked_list"]);

export function normalizeTemplateTrace(template: TemplateData, fallbackVizType = "default"): GeneratedTrace {
  const rawSteps = Array.isArray(template.steps) ? template.steps : [];
  const type = template.type || "";
  let vizType = fallbackVizType;
  if (SORTING_TEMPLATE_TYPES.has(type)) vizType = "sorting";
  else if (ARRAY_TEMPLATE_TYPES.has(type)) vizType = "array";
  else if (GRAPH_TEMPLATE_TYPES.has(type)) vizType = "graph";
  else if (STACK_TEMPLATE_TYPES.has(type)) vizType = "stack";
  else if (QUEUE_TEMPLATE_TYPES.has(type)) vizType = "queue";
  else if (TREE_TEMPLATE_TYPES.has(type)) vizType = "tree";
  else if (LINKED_LIST_TEMPLATE_TYPES.has(type)) vizType = "linked_list";

  let graph: GraphData | undefined;
  const example = template.example_input;
  if (vizType === "graph") {
    graph = buildGraphFromExample(example);
  }

  const steps: TraceStep[] = rawSteps.map((s, idx) => {
    const base: TraceStep = {
      line: idx + 1,
      action: typeof s.action === "string" ? s.action : `Step ${s.step ?? "?"}`,
      explanation: typeof s.explanation === "string" ? s.explanation : (typeof s.action === "string" ? s.action : "Executing..."),
      variables: {},
    };

    const rest: TemplateStep = { ...s };
    delete rest.step;
    delete rest.action;
    delete rest.explanation;
    if (Array.isArray(rest.array)) base.variables = { ...rest };
    else {
      Object.entries(rest).forEach(([k, v]) => {
        if (v === undefined) return;
        base.variables![k] = v;
      });
    }

    if (vizType === "sorting") {
      base.sorting_data = Array.isArray(s.array) ? clone(s.array) : undefined;
      base.comparing = Array.isArray(s.compare) ? clone(s.compare) : [];
      base.sorted_indices = Array.isArray(s.sorted) ? clone(s.sorted) : [];
      base.active_indices = Array.isArray(s.scan) ? clone(s.scan) : [];
    } else if (vizType === "array") {
      base.array_data = Array.isArray(s.array) ? clone(s.array) : undefined;
      const pointers: Record<string, number> = {};
      if (typeof s.low === "number") pointers.low = s.low;
      if (typeof s.high === "number") pointers.high = s.high;
      if (typeof s.mid === "number") pointers.mid = s.mid;
      if (typeof s.index === "number") pointers.i = s.index;
      base.pointers = Object.keys(pointers).length ? pointers : undefined;
      if (typeof s.index === "number") base.active_indices = [s.index];
      if (typeof s.mid === "number") base.active_indices = [s.mid];
    } else if (vizType === "graph" && graph) {
      base.graph = graph;
      base.visited_nodes = Array.isArray(s.visited) ? s.visited.map(String) : [];
      base.current_node = s.current !== undefined ? String(s.current) : undefined;
      if (base.current_node) base.visited_nodes = base.visited_nodes.filter((v) => v !== base.current_node);
    } else if (vizType === "stack") {
      base.stack = Array.isArray(s.stack) ? clone(s.stack) : [];
      base.active_index = base.stack.length - 1;
    } else if (vizType === "queue") {
      base.queue = Array.isArray(s.queue) ? clone(s.queue) : [];
      base.active_index = 0;
    } else if (vizType === "tree") {
      base.array_data = Array.isArray(s.array) ? clone(s.array) : undefined;
    }

    return base;
  });

  return {
    steps,
    algorithm: template.category ? template.category.replace(/_/g, " ").toUpperCase() : undefined,
    visualization_type: vizType,
    time_complexity: undefined,
    space_complexity: undefined,
    code: rawSteps.map((s) => (typeof s.action === "string" ? s.action : `Step ${s.step ?? "?"}`)).join("\n"),
    language: "python",
  };
}

function buildGraphFromExample(example: unknown): GraphData | undefined {
  if (!example) return undefined;
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];
  if (Array.isArray(example)) {
    const ids = new Set<string>();
    example.forEach((edge) => {
      if (!Array.isArray(edge) || edge.length < 2) return;
      const [a, b] = edge;
      const from = String(a);
      const to = String(b);
      ids.add(from);
      ids.add(to);
      edges.push({ from, to, ...(typeof edge[2] === "number" ? { weight: edge[2] } : {}) });
    });
    ids.forEach((id) => nodes.push({ id }));
    return { nodes, edges };
  }
  if (typeof example === "object" && example !== null) {
    const ex = example as Record<string, unknown>;
    const exEdges = ex.edges;
    if (Array.isArray(exEdges)) return buildGraphFromExample(exEdges);
  }
  return undefined;
}
