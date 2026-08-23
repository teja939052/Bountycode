import React, { useState, useEffect } from "react";

const algorithmColors = {
  array: ["#3b82f6", "#1d4ed8", "#60a5fa"],
  arrayHighlight: ["#f87171", "#ef4444", "#f87171"],
  current: ["#fbbf24", "#f59e0b", "#eab308"],
  sorted: ["#22c55e", "#16a34a", "#84cc16"],
  pivot: ["#a855f7", "#9333ea", "#c084fc"],
};

const sortingAlgorithms = {
  bubbleSort: {
    name: "Bubble Sort",
    description: "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
    timeComplexity: "O(n²) average/worst, O(n) best",
    spaceComplexity: "O(1)",
    stable: true,
  },
  selectionSort: {
    name: "Selection Sort",
    description: "Divides the input list into two parts: the sublist of items already sorted, which is built up from left to right at the front (left) of the list, and the sublist of remaining items.",
    timeComplexity: "O(n²) in all cases",
    spaceComplexity: "O(1)",
    stable: false,
  },
  insertionSort: {
    name: "Insertion Sort",
    description: "Builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.",
    timeComplexity: "O(n²) average/worst, O(n) best",
    spaceComplexity: "O(1)",
    stable: true,
  },
  mergeSort: {
    name: "Merge Sort",
    description: "Divide and conquer algorithm that divides the input array into two halves, recursively sorts them, and then merges the sorted halves.",
    timeComplexity: "O(n log n) in all cases",
    spaceComplexity: "O(n)",
    stable: true,
  },
  quickSort: {
    name: "Quick Sort",
    description: "Divide and conquer algorithm that picks a 'pivot' element and partitions the array around the pivot, recursively sorting the sub-arrays.",
    timeComplexity: "O(n log n) average, O(n²) worst",
    spaceComplexity: "O(log n)",
    stable: false,
  },
  heapSort: {
    name: "Heap Sort",
    description: "Uses a binary heap data structure to sort elements. First builds a max heap, then repeatedly extracts the maximum element and rebuilds the heap.",
    timeComplexity: "O(n log n) in all cases",
    spaceComplexity: "O(1)",
    stable: false,
  },
};

const graphTraversalAlgorithms = {
  dfs: {
    name: "Depth-First Search",
    description: "Traverses a graph by exploring as far as possible along each branch before backtracking. Uses a stack (implicitly via recursion).",
    timeComplexity: "O(V + E)",
    spaceComplexity: "O(V)",
  },
  bfs: {
    name: "Breadth-First Search",
    description: "Traverses a graph level by level. Starts at the root node and explores all neighboring nodes at the present depth prior to moving on to nodes at the next depth level. Uses a queue.",
    timeComplexity: "O(V + E)",
    spaceComplexity: "O(V)",
  },
  dijkstra: {
    name: "Dijkstra's Algorithm",
    description: "Finds the shortest path from a source node to all other nodes in a weighted graph. Works by maintaining a set of unvisited nodes and calculating tentative distances.",
    timeComplexity: "O((V + E) log V) with binary heap",
    spaceComplexity: "O(V)",
  },
};

const arrayData = {
  reverse: [9, 8, 7, 6, 5, 4, 3, 2, 1],
  random: [5, 2, 8, 1, 9, 3, 7, 4, 6],
  sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9],
};

const sortingSteps = {
  bubbleSortSteps: [
    { phase: "1st pass", array: [8, 7, 5, 4, 2, 6, 3, 9, 1], comparisons: ["9>8✓", "8>7✓", "7>5✓", "5>4✓", "4>2✓", "2>6✗", "6>3✓", "3>9✗"], swaps: ["9>8→8,9"], moved: [] },
    { phase: "2nd pass", array: [7, 5, 4, 2, 6, 3, 8, 9, 1], comparisons: ["7>5✓", "5>4✓", "4>2✓", "2>6✗", "6>3✓", "3>8✗", "8>9✗"], swaps: ["6>3→3,6"], moved: [] },
    { phase: "3rd pass", array: [5, 4, 2, 3, 6, 7, 8, 9, 1], comparisons: ["5>4✓", "4>2✓", "2>3✓", "3>6✗", "6>7✗", "7>8✗", "8>9✗"], swaps: [], moved: [] },
  ],
  mergeSortSteps: [
    { phase: "Divide", array: [5, 2, 8, 1, 9, 3, 7, 4, 6], left: [5, 2, 8, 1, 9], right: [3, 7, 4, 6] },
    { phase: "Merge left", array: [1, 2, 5, 8, 9, 3, 7, 4, 6], left: [1, 2, 5, 8, 9], right: [3, 7, 4, 6] },
    { phase: "Merge right", array: [1, 2, 3, 4, 5, 6, 7, 8, 9], left: [1, 2, 3, 4, 5], right: [6, 7, 8, 9] },
    { phase: "Complete", array: [1, 2, 3, 4, 5, 6, 7, 8, 9], left: [1, 2, 3, 4, 5], right: [6, 7, 8, 9] },
  ],
};

export default function DSAVisualizer() {
  const [showSorting, setShowSorting] = useState(false);
  const [showGraphs, setShowGraphs] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [arrayValues, setArrayValues] = useState([...arrayData.sorted]);
  const [steps, setSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(500);

  const handleSortAlgorithm = (algo) => {
    setSelectedAlgorithm(algo);
    setShowSorting(true);
    setCurrentStep(0);
    setIsPlaying(false);
    
    switch (algo) {
      case "bubbleSort":
        setSteps(sortingSteps.bubbleSortSteps);
        break;
      case "mergeSort":
        setSteps(sortingSteps.mergeSortSteps);
        break;
      default:
        setSteps([]);
    }
  };

  const handleGraphAlgorithm = (algo) => {
    setSelectedAlgorithm(algo);
    setShowGraphs(true);
  };

  const prevStep = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
    else setIsPlaying(false);
  };

  const togglePlay = () => {
    if (isPlaying) {
      setIsPlaying(false);
    } else {
      setIsPlaying(true);
    }
  };

  let displayedSteps = steps;

  if (showSorting && selectedAlgorithm && steps.length > 0) {
    if (isPlaying) {
      // Auto-advance
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        setIsPlaying(false);
        setCurrentStep(steps.length - 1);
      }
    }
    displayedSteps = steps.slice(0, currentStep + 1);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            DSA Visualizer — Algorithm Animations
          </h1>
          <p className="text-gray-600 mt-1">
            Interactive algorithm visualizations for PlacementPro SDE preparation
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-4">
        {/* Sorting Algorithms Section */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Sorting Algorithms
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Object.keys(sortingAlgorithms).map((key) => (
              <div
                key={key}
                className="group rounded-lg border p-4 hover:border-blue-500 transition-colors"
              >
                <h3 className="font-medium text-gray-700 mb-2">
                  {sortingAlgorithms[key].name}
                </h3>
                <p className="text-sm text-gray-500 line-clamp-2">
                  {sortingAlgorithms[key].description}
                </p>
                <div className="mt-2 text-xs text-gray-500">
                  <span>{sortingAlgorithms[key].timeComplexity}</span>
                  <span className="mx-2">|</span>
                  <span>{sortingAlgorithms[key].spaceComplexity}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Visualization */}
          {showSorting && selectedAlgorithm && steps.length > 0 && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow">
              <h3 className="font-medium text-gray-900 mb-4">
                {sortingAlgorithms[selectedAlgorithm].name} — Step-by-Step
              </h3>
              <div className="space-y-4">
                {displayedSteps.map((step, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-lg border transition-all duration-300"
                    style={{
                      background: currentStep >= idx ? "#f0fdf4" : "transparent",
                      borderColor: currentStep >= idx ? "#22c55e" : "transparent",
                    }}
                  >
                    <p className="font-medium text-gray-700 mb-2">
                      {step.phase || `Step ${idx + 1}`}
                    </p>
                    <div className="space-y-2">
                      {step.comparisons && step.comparisons.length > 0 && (
                        <div>
                          <p className="text-sm text-gray-500">
                            Comparisons:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {step.comparisons.map((comp, i) => (
                              <span
                                key={i}
                                className={`px-3 py-1 rounded text-xs ${
                                  comp.includes("✓") ? "bg-green-100 text-green-800" :
                                  comp.includes("✗") ? "bg-red-100 text-red-800" :
                                  "bg-gray-100 text-gray-800"
                                }`}
                              >
                                {comp}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {step.swaps && step.swaps.length > 0 && (
                        <div>
                          <p className="text-sm text-gray-500 mb-2">
                            Swaps:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {step.swaps.map((swap, i) => (
                              <span key={i} className="px-3 py-1 rounded text-xs bg-yellow-100 text-yellow-800">
                                {swap}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {step.moved && step.moved.length > 0 && (
                        <div>
                          <p className="text-sm text-gray-500 mb-2">
                            Moved:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {step.moved.map((m, i) => (
                              <span key={i} className="px-3 py-1 rounded text-xs bg-blue-100 text-blue-800">
                                {m}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Controls */}
          {showSorting && selectedAlgorithm && steps.length > 0 && (
            <div className="mt-6 pt-6 border-t">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-gray-600">
                  Step {currentStep + 1}/{steps.length}
                </span>
                <button
                  onClick={togglePlay}
                  className={`px-4 py-2 rounded text-sm font-medium transition-colors ${
                    isPlaying ? "bg-red-500 text-text-primary" : "bg-blue-500 text-text-primary"
                  }`}
                >
                  {isPlaying ? "Pause" : "Play Auto"}
                </button>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={prevStep} className="px-3 py-1 rounded bg-gray-200 text-sm">
                  ← Prev
                </button>
                <button onClick={nextStep} className="px-3 py-1 rounded bg-gray-200 text-sm">
                  Next →
                </button>
              </div>
            </div>
          )}
        </section>

        {/* Graph Algorithms Section */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Graph Traversal Algorithms
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Object.keys(graphTraversalAlgorithms).map((key) => (
              <div
                key={key}
                className="group rounded-lg border p-4 hover:border-blue-500 transition-colors cursor-pointer"
                onClick={() => handleGraphAlgorithm(key)}
              >
                <h3 className="font-medium text-gray-700 mb-2">
                  {graphTraversalAlgorithms[key].name}
                </h3>
                <p className="text-sm text-gray-500 line-clamp-2">
                  {graphTraversalAlgorithms[key].description}
                </p>
                <div className="text-xs text-gray-500">{graphTraversalAlgorithms[key].timeComplexity}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Array Controls */}
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Array Operations
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button
              onClick={() => setArrayValues([...arrayData.reverse])}
              className="flex-1 py-2 rounded bg-blue-500 text-text-primary text-sm hover:bg-blue-600 transition-colors"
            >
              Reverse
            </button>
            <button
              onClick={() => setArrayValues([...arrayData.random])}
              className="flex-1 py-2 rounded bg-green-500 text-text-primary text-sm hover:bg-green-600 transition-colors"
            >
              Random
            </button>
            <button
              onClick={() => setArrayValues([...arrayData.sorted])}
              className="flex-1 py-2 rounded bg-purple-500 text-text-primary text-sm hover:bg-purple-600 transition-colors"
            >
              Sorted
            </button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t pt-6 text-center text-sm text-gray-500">
        <p>DSA Visualizer — PlacementPro SDE Preparation</p>
      </footer>
    </div>
  );
}