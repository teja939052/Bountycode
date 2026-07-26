import { useMemo } from 'react';
import { motion } from 'framer-motion';

// Graph data structure visualization of algorithm flow
// Renders nodes as a directed graph with animated traversal

const NODE_STYLES = {
  start: { fill: '#22c55e', stroke: '#16a34a', shape: 'rounded', label: 'Start' },
  process: { fill: '#3b82f6', stroke: '#2563eb', shape: 'rect', label: '' },
  decision: { fill: '#f59e0b', stroke: '#d97706', shape: 'diamond', label: '?' },
  end: { fill: '#ef4444', stroke: '#dc2626', shape: 'rounded', label: 'End' },
};

export default function AlgorithmGraph({ nodes = [], edges = [], animated = true, className = '' }) {
  // Compute layout positions
  const layout = useMemo(() => {
    if (!nodes || nodes.length === 0) return { nodes: [], edges: [] };

    const nodeMap = {};
    const positioned = nodes.map((n, i) => {
      // Use provided x,y or compute grid layout
      const x = n.x != null ? n.x : (i % 4) * 25 + 12;
      const y = n.y != null ? n.y : Math.floor(i / 4) * 30 + 15;
      const styled = { ...NODE_STYLES[n.type], ...NODE_STYLES.process };
      const nodeStyle = NODE_STYLES[n.type] || NODE_STYLES.process;
      nodeMap[n.id] = { x, y, ...nodeStyle, id: n.id, label: n.label || nodeStyle.label };
      return nodeMap[n.id];
    });

    const positionedEdges = (edges || []).map(e => ({
      from: nodeMap[e.from],
      to: nodeMap[e.to],
      label: e.label,
    })).filter(e => e.from && e.to);

    return { nodes: positioned, edges: positionedEdges };
  }, [nodes, edges]);

  if (!nodes || nodes.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className={`bg-gray-900/60 border border-gray-700/40 rounded-xl p-4 ${className}`}
    >
      <div className="text-center mb-3">
        <span className="text-[10px] font-mono uppercase tracking-widest text-gray-500">
          Algorithm Flow
        </span>
      </div>

      <div className="relative mx-auto" style={{ width: '100%', maxWidth: 400, height: 240 }}>
        <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="xMidYMid meet">
          {/* Edges */}
          {layout.edges.map((edge, i) => (
            <GraphEdge key={i} {...edge} animated={animated} index={i} />
          ))}

          {/* Nodes */}
          {layout.nodes.map((node, i) => (
            <GraphNode key={node.id || i} {...node} animated={animated} index={i} />
          ))}
        </svg>
      </div>
    </motion.div>
  );
}

function GraphNode({ x, y, fill, stroke, shape, label, id, animated, index }) {
  const cx = x;
  const cy = y;
  const w = 12;
  const h = 7;

  const nodeDelay = animated ? index * 0.15 : 0;

  if (shape === 'diamond') {
    const pts = `${cx},${cy - h} ${cx + w},${cy} ${cx},${cy + h} ${cx - w},${cy}`;
    return (
      <motion.g
        initial={animated ? { opacity: 0, scale: 0.3 } : undefined}
        animate={animated ? { opacity: 1, scale: 1 } : undefined}
        transition={{ delay: nodeDelay, duration: 0.4, ease: [0.34, 1.56, 0.64, 1] }}
      >
        <polygon points={pts} fill={fill} fillOpacity="0.15" stroke={stroke} strokeWidth="0.5" />
        <text x={cx} y={cy + 1} textAnchor="middle" fill={fill}
          fontSize="3.5" fontFamily="Orbitron" fontWeight="bold">
          {label || '?'}
        </text>
      </motion.g>
    );
  }

  if (shape === 'rounded') {
    return (
      <motion.g
        initial={animated ? { opacity: 0, scale: 0.3 } : undefined}
        animate={animated ? { opacity: 1, scale: 1 } : undefined}
        transition={{ delay: nodeDelay, duration: 0.4, ease: [0.34, 1.56, 0.64, 1] }}
      >
        <rect x={cx - w} y={cy - h} width={w * 2} height={h * 2} rx="3"
          fill={fill} fillOpacity="0.15" stroke={stroke} strokeWidth="0.5" />
        <text x={cx} y={cy + 1} textAnchor="middle" fill={fill}
          fontSize="3.5" fontFamily="Orbitron" fontWeight="bold">
          {label}
        </text>
      </motion.g>
    );
  }

  // Default: rect
  return (
    <motion.g
      initial={animated ? { opacity: 0, scale: 0.3 } : undefined}
      animate={animated ? { opacity: 1, scale: 1 } : undefined}
      transition={{ delay: nodeDelay, duration: 0.4, ease: [0.34, 1.56, 0.64, 1] }}
    >
      <rect x={cx - w} y={cy - h} width={w * 2} height={h * 2} rx="1"
        fill={fill} fillOpacity="0.1" stroke={stroke} strokeWidth="0.5" />
      <text x={cx} y={cy + 1} textAnchor="middle" fill={fill}
        fontSize="3" fontFamily="JetBrains Mono" fontWeight="500">
        {label}
      </text>
    </motion.g>
  );
}

function GraphEdge({ from, to, label, animated, index }) {
  if (!from || !to) return null;

  const edgeDelay = animated ? 0.5 + index * 0.1 : 0;

  // Calculate midpoint for label
  const mx = (from.x + to.x) / 2;
  const my = (from.y + to.y) / 2;

  // Calculate arrow angle
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const len = Math.sqrt(dx * dx + dy * dy);
  if (len < 0.1) return null;

  const nx = dx / len;
  const ny = dy / len;

  // Shorten line to avoid overlapping node
  const startX = from.x + nx * 8;
  const startY = from.y + ny * 5;
  const endX = to.x - nx * 8;
  const endY = to.y - ny * 5;

  return (
    <motion.g
      initial={animated ? { opacity: 0 } : undefined}
      animate={animated ? { opacity: 1 } : undefined}
      transition={{ delay: edgeDelay, duration: 0.3 }}
    >
      {/* Line */}
      <line x1={startX} y1={startY} x2={endX} y2={endY}
        stroke="#4b5563" strokeWidth="0.4" opacity="0.6" />

      {/* Arrow head */}
      <polygon
        points={`${endX},${endY} ${endX - nx * 2 + ny * 1},${endY - ny * 2 - nx * 1} ${endX - nx * 2 - ny * 1},${endY - ny * 2 + nx * 1}`}
        fill="#4b5563" opacity="0.6"
      />

      {/* Edge label */}
      {label && (
        <text x={mx} y={my - 1.5} textAnchor="middle" fill="#9ca3af"
          fontSize="2.5" fontFamily="JetBrains Mono">
          {label}
        </text>
      )}
    </motion.g>
  );
}
