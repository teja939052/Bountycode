import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Code, Sword, Target, User, Route, Flame, Trophy, Sparkles, Bot, Gamepad2, MessageSquare, Video, Swords, Award, type LucideIcon } from 'lucide-react';
import useAuthStore from '../store/authStore';

interface ProgressRingProps {
  value: number;
  max?: number;
  size?: number;
  strokeWidth?: number;
  color?: string;
}

function ProgressRing({ value, max = 100, size = 24, strokeWidth = 2, color = '#6366f1' }: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.min(1, Math.max(0, value / max));
  const offset = circumference * (1 - pct);
  return (
    <svg width={size} height={size} className="absolute -top-0.5 -right-0.5">
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={strokeWidth} />
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round"
        strokeDasharray={circumference} strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: 'stroke-dashoffset 0.6s ease' }}
      />
    </svg>
  );
}

interface NavItem {
  to: string;
  icon: LucideIcon;
  label: string;
  ringColor?: string;
}

const NAV_ITEMS: NavItem[] = [
  { to: '/hub', icon: Home, label: 'Hub' },
  { to: '/learn', icon: Code, label: 'Learn' },
  { to: '/daily-drill', icon: Flame, label: 'Drill', ringColor: '#f97316' },
  { to: '/tower', icon: Trophy, label: 'Tower', ringColor: '#a855f7' },
  { to: '/community', icon: MessageSquare, label: 'Community' },
  { to: '/battles', icon: Swords, label: 'Battles' },
  { to: '/rank', icon: Award, label: 'Rank' },
];

export default function BottomNav() {
  const location = useLocation();
  const { user } = useAuthStore();

  const hideOn = ['/', '/login', '/register', '/playground'];
  if (hideOn.includes(location.pathname)) return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 md:hidden border-t border-slate-800/80 bg-slate-950/95 backdrop-blur-xl safe-area-bottom"
      style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
      <div className="flex items-center justify-around h-16 px-1">
        {NAV_ITEMS.map(({ to, icon: Icon, label, ringColor }) => {
          const isActive = location.pathname === to || location.pathname.startsWith(to + '/');
          return (
            <Link key={to} to={to}
              className="flex flex-col items-center justify-center gap-0.5 relative min-w-[56px] min-h-[44px] py-1"
            >
              <div className="relative w-7 h-7 flex items-center justify-center">
                <Icon size={18}
                  className={`transition-colors duration-200 ${isActive ? 'text-indigo-400' : 'text-slate-500'}`}
                />
                {isActive && (
                  <motion.div layoutId="bottomNavActive"
                    className="absolute -bottom-1 w-5 h-0.5 rounded-full bg-indigo-500"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
              </div>
              <span className={`text-[9px] font-mono tracking-wider mt-0.5 ${isActive ? 'text-indigo-300 font-semibold' : 'text-slate-600'}`}>
                {label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
