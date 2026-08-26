import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutDashboard, BookOpen, Code2, MessageSquare, Menu, Trophy, Briefcase, Castle, Brain, Calendar, type LucideIcon } from 'lucide-react';
import useAuthStore from '../store/authStore';
import { useGamification } from '../hooks/useGamification';

interface NavItem {
  to: string;
  icon: LucideIcon;
  label: string;
}

/* 5 core destinations + a "More" drawer (Material/Apple guideline).
   Resume/ATS/Cover Letter live under the Career tab (no duplication). */
const NAV_ITEMS: NavItem[] = [
  { to: '/hub', icon: LayoutDashboard, label: 'Home' },
  { to: '/prepare', icon: BookOpen, label: 'Prepare' },
  { to: '/practice', icon: Code2, label: 'Practice' },
  { to: '/compete', icon: Trophy, label: 'Compete' },
  { to: '/career', icon: Briefcase, label: 'Career' },
  { to: '#', icon: Menu, label: 'More' },
];

const MORE_GROUPS: { label: string; items: NavItem[] }[] = [
  {
    label: 'Your Journey',
    items: [
      { to: '/tower', icon: Castle, label: 'Tower' },
    ],
  },
  {
    label: 'Tools & Community',
    items: [
      { to: '/community', icon: MessageSquare, label: 'Community' },
      { to: '/ai-mentor', icon: Brain, label: 'AI Mentor' },
      { to: '/project-generator', icon: MessageSquare, label: 'Project Generator' },
      { to: '/concepts', icon: Lightbulb, label: 'Concepts' },
      { to: '/placement-calendar', icon: Calendar, label: 'Placement Calendar' },
      { to: '/settings', icon: Menu, label: 'Settings' },
    ],
  },
];

export default function BottomNav() {
  const location = useLocation();
  const { user } = useAuthStore();
  const [moreOpen, setMoreOpen] = useState(false);
  const { startup } = useGamification();

  const hideOn = ['/', '/login', '/register', '/playground'];
  if (hideOn.includes(location.pathname)) return null;
  if (!user) return null;

  const tier = startup?.tier;
  const showLeague = tier && startup?.of;

  return (
    <>
      {moreOpen && (
        <div className="fixed inset-0 z-40 flex flex-col justify-end bg-black/30" onClick={() => setMoreOpen(false)}>
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="rounded-t-3xl border-t border-border bg-white p-4 pb-2 safe-area-bottom"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-border" />
            <div className="text-sm font-display font-bold text-text">Browse everything</div>
            <div className="mt-2 max-h-[55vh] overflow-y-auto pb-4">
              {MORE_GROUPS.map((group) => (
                <div key={group.label}>
                  <div className="px-2 pb-1 pt-4 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">{group.label}</div>
                  <div className="grid grid-cols-1 gap-1">
                    {group.items.map((item) => (
                      <Link
                        key={item.to}
                        to={item.to}
                        onClick={() => setMoreOpen(false)}
                        className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-text transition-colors hover:bg-ocean-soft hover:text-ocean"
                      >
                        <item.icon size={14} className="text-ocean" />
                        {item.label}
                      </Link>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}

      <nav className="fixed bottom-0 left-0 right-0 z-50 md:hidden border-t border-border bg-white shadow-[0_-4px_20px_rgba(17,33,27,0.06)] safe-area-bottom">
        {showLeague && (
          <Link
            to="/rank"
            className="block border-b border-border"
            style={{ background: `${tier.color}10` }}
          >
            <div className="flex items-center justify-center gap-1.5 h-7 px-3 text-[10px] font-mono">
              <Trophy size={11} style={{ color: tier.color }} />
              <span className="font-bold" style={{ color: tier.color }}>{tier.name} League</span>
              <span className="text-text-muted">
                #{startup.rank} of {startup.of} · {startup.weekly_xp || 0} XP
              </span>
              {startup.promoted_next_week && <span className="text-primary-dark">&uarr; promoting</span>}
              {startup.relegated_next_week && <span className="text-coral">&darr; relegation</span>}
            </div>
          </Link>
        )}
        <div className="flex items-center justify-around h-16 px-1">
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => {
            const isActive = location.pathname === to || location.pathname.startsWith(to + '/');
            const isMore = label === 'More';
            return (
              <Link
                key={to}
                to={isMore ? '#' : to}
                onClick={(e) => {
                  if (isMore) {
                    e.preventDefault();
                    setMoreOpen(true);
                  }
                }}
                className="flex flex-col items-center justify-center gap-0.5 relative min-w-[56px] min-h-[44px] py-1"
                aria-label={label}
              >
                <div className="relative w-7 h-7 flex items-center justify-center">
                  <Icon size={18}
                    className={`transition-colors duration-200 ${isActive && !isMore ? 'text-primary-dark' : 'text-text-muted'}`}
                  />
                  {isActive && !isMore && (
                    <motion.div layoutId="bottomNavActive"
                      className="absolute -bottom-1 w-5 h-0.5 rounded-full bg-primary"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    />
                  )}
                </div>
                <span className={`text-[9px] tracking-wider mt-0.5 ${isActive && !isMore ? 'text-primary-dark font-bold' : 'text-text-muted'}`}>
                  {label}
                </span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
