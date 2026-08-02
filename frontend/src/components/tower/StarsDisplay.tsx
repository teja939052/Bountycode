import { motion } from 'framer-motion';

// Star rating display — 1 to 3 stars with fill animation
export default function StarsDisplay({ stars = 0, maxStars = 3, size = 'md', animated = true }) {
  const sizeClass = {
    sm: 'text-base',
    md: 'text-xl',
    lg: 'text-3xl',
    xl: 'text-4xl',
  }[size] || 'text-xl';

  return (
    <div className="flex gap-0.5 items-center">
      {Array.from({ length: maxStars }, (_, i) => (
        <motion.span
          key={i}
          className={`${sizeClass}`}
          initial={animated ? { scale: 0, rotate: -180 } : undefined}
          animate={animated ? { scale: 1, rotate: 0 } : undefined}
          transition={animated ? {
            delay: i * 0.2,
            type: 'spring',
            stiffness: 260,
            damping: 12,
          } : undefined}
        >
          {i < stars ? '⭐' : '☆'}
        </motion.span>
      ))}
    </div>
  );
}
