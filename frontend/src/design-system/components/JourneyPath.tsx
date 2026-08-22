import { ReactNode } from "react";
import { colors, radii, shadows, motion, spacing } from "..";

interface JourneyNode {
  id: string;
  label: string;
  description?: string;
  status: "completed" | "current" | "locked" | "upcoming";
  type?: "lesson" | "challenge" | "boss" | "milestone";
  position: { x: number; y: number };
  to?: string;
  xp?: number;
  icon?: ReactNode;
}

interface JourneyPathProps {
  nodes: JourneyNode[];
  connections?: { from: string; to: string }[];
  orientation?: "vertical" | "horizontal";
  className?: string;
  onNodeClick?: (node: JourneyNode) => void;
}

const nodeSize = 48;
const nodeRadius = nodeSize / 2;

function getNodeColor(status: JourneyNode["status"], type?: JourneyNode["type"]) {
  switch (status) {
    case "completed":
      return colors.semantic.success;
    case "current":
      return colors.brand.primary;
    case "locked":
      return colors.semantic.locked;
    case "upcoming":
      return colors.text.dim;
    default:
      return colors.text.muted;
  }
}

function getNodeBorder(status: JourneyNode["status"]) {
  switch (status) {
    case "completed":
      return colors.semantic.success;
    case "current":
      return colors.brand.primary;
    case "locked":
      return colors.semantic.locked;
    case "upcoming":
      return colors.border.primary;
    default:
      return colors.border.primary;
  }
}

function getNodeIcon(status: JourneyNode["status"], type?: JourneyNode["type"]) {
  switch (status) {
    case "completed":
      return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="20 6 9 17 4 12" />
        </svg>
      );
    case "current":
      return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="8" />
        </svg>
      );
    case "locked":
      return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
      );
    default:
      return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="8" />
        </svg>
      );
  }
}

export function JourneyPath({
  nodes,
  connections = [],
  orientation = "vertical",
  className = "",
  onNodeClick,
}: JourneyPathProps) {
  const sortedNodes = [...nodes].sort((a, b) => {
    if (orientation === "vertical") {
      return a.position.y - b.position.y;
    }
    return a.position.x - b.position.x;
  });

  const containerWidth = orientation === "vertical" ? 200 : nodes.length * 200;
  const containerHeight = orientation === "vertical" ? nodes.length * 160 : 200;

  return (
    <div className={`relative ${className}`} style={{ width: containerWidth, height: containerHeight }}>
      <svg
        className="absolute inset-0 pointer-events-none"
        width={containerWidth}
        height={containerHeight}
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth={10}
            markerHeight={7}
            refX={9}
            refY={3.5}
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill={colors.border.primary} />
          </marker>
        </defs>
        {connections.map((conn, idx) => {
          const fromNode = nodes.find((n) => n.id === conn.from);
          const toNode = nodes.find((n) => n.id === conn.to);
          if (!fromNode || !toNode) return null;

          const fromX = fromNode.position.x + nodeRadius;
          const fromY = fromNode.position.y + nodeRadius;
          const toX = toNode.position.x + nodeRadius;
          const toY = toNode.position.y + nodeRadius;

          const midX = (fromX + toX) / 2;
          const midY = (fromY + toY) / 2;

          if (orientation === "vertical") {
            return (
              <path
                key={idx}
                d={`M ${fromX} ${fromY} Q ${midX} ${midY} ${toX} ${toY}`}
                stroke={colors.border.primary}
                strokeWidth={2}
                fill="none"
                strokeLinecap="round"
                markerEnd="url(#arrowhead)"
                style={{
                  strokeDasharray: "8 4",
                  opacity: 0.6,
                }}
              />
            );
          }

          return (
            <path
              key={idx}
              d={`M ${fromX} ${fromY} Q ${midX} ${midY} ${toX} ${toY}`}
              stroke={colors.border.primary}
              strokeWidth={2}
              fill="none"
              strokeLinecap="round"
              markerEnd="url(#arrowhead)"
              style={{
                strokeDasharray: "8 4",
                opacity: 0.6,
              }}
            />
          );
        })}
      </svg>

      <div className="relative" style={{ width: containerWidth, height: containerHeight }}>
        {sortedNodes.map((node, idx) => (
          <div
            key={node.id}
            className="absolute transition-all duration-300 ease-out"
            style={{
              left: orientation === "vertical" ? "50%" : node.position.x,
              top: orientation === "vertical" ? node.position.y : "50%",
              transform: orientation === "vertical" ? "translateX(-50%)" : "translateY(-50%)",
              zIndex: 10,
            }}
            onClick={() => onNodeClick?.(node)}
          >
            <div
              className={`
                relative flex items-center justify-center transition-all duration-300 ease-out
                ${node.status === "current" ? "animate-pulse" : ""}
              `}
              style={{
                width: nodeSize,
                height: nodeSize,
                borderRadius: radii.full,
                backgroundColor:
                  node.status === "completed"
                    ? colors.semantic.success
                    : node.status === "current"
                    ? colors.brand.primary
                    : "transparent",
                border: `2px solid ${getNodeBorder(node.status)}`,
                boxShadow:
                  node.status === "current"
                    ? shadows.glow
                    : node.status === "completed"
                    ? shadows.glow
                    : "none",
              }}
            >
              {node.icon || getNodeIcon(node.status, node.type)}
            </div>

            <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-40 text-center">
              <p className={`
                text-xs font-medium truncate transition-colors
                ${node.status === "completed" ? "text-text-primary" : ""}
                ${node.status === "current" ? "text-brand-primary font-semibold" : ""}
                ${node.status === "locked" ? "text-text-dim" : "text-text-secondary"}
              `}>
                {node.label}
              </p>
              {node.xp && (
                <p className="text-[10px] font-mono text-xp/80 mt-0.5">
                  +{node.xp} XP
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function SkillNode({
  skill,
  mastery,
  onClick,
  className = "",
}: {
  skill: string;
  mastery: number;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <div
      className={`
        group relative rounded-${radii.card} border border-border-primary
        bg-background-surface p-4 transition-all duration-300
        hover:border-brand-primary hover:shadow-glow cursor-pointer
        ${className}
      `}
      onClick={onClick}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="font-semibold text-text-primary">{skill}</span>
        <span className="text-sm font-mono text-brand-primary">
          {mastery}%
        </span>
      </div>
      <ProgressBar value={mastery} size="sm" color="primary" />
      <div className="mt-2 text-xs text-text-secondary">
        {mastery >= 80 ? "Mastered" : mastery >= 50 ? "Proficient" : "Learning"}
      </div>
    </div>
  );
}