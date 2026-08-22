import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutDashboard, BookOpen, Code2, MessageSquare, Menu, User, Trophy, Briefcase, Gamepad2, Castle, Users, Swords, Layers, Award, Globe, Coins, Library, Gift, Shield, Brain, Timer, Calendar, MessageCircle, Building2, Lightbulb, ScrollText, Target, Zap, UserPlus, type LucideIcon } from 'lucide-react';
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
      { to: '/journey', icon: Gamepad2, label: 'Journey' },
      { to: '/tower', icon: Castle, label: 'Tower' },
      { to: '/guilds', icon: Users, label: 'Guilds' },
      { to: '/dungeons', icon: Swords, label: 'Dungeons' },
      { to: '/collection', icon: Library, label: 'Collection' },
      { to: '/cards', icon: Layers, label: 'Cards' },
      { to: '/achievements', icon: Award, label: 'Achievements' },
      { to: '/world', icon: Globe, label: 'World' },
      { to: '/economy', icon: Coins, label: 'Economy' },
      { to: '/wheel', icon: Gift, label: 'Lucky Wheel' },
      { to: '/battle-pass', icon: Shield, label: 'Battle Pass' },
    ],
  },
  {
    label: 'Tools & Community',
    items: [
      { to: '/community', icon: MessageSquare, label: 'Community' },
      { to: '/discussions', icon: MessageCircle, label: 'Discussions' },
      { to: '/friends', icon: UserPlus, label: 'Friends' },
      { to: '/ai-mentor', icon: Brain, label: 'AI Mentor' },
      { to: '/project-generator', icon: MessageSquare, label: 'Project Generator' },
      { to: '/concepts', icon: Lightbulb, label: 'Concepts' },
      { to: '/behavioral-practice', icon: ScrollText, label: 'Behavioral Practice' },
      { to: '/company-directory', icon: Building2, label: 'Company Directory' },
      { to: '/study-timer', icon: Timer, label: 'Study Timer' },
      { to: '/placement-calendar', icon: Calendar, label: 'Placement Calendar' },
      { to: '/settings', icon: Menu, label: 'Settings' },
    ],
  },
  {
    label: 'Progress',
    items: [
      { to: '/quests', icon: ScrollText, label: 'Quests' },
      { to: '/goals', icon: Target, label: 'Goals' },
      { to: '/readiness', icon: Zap, label: 'Readiness Score' },
      { to: '/skill-mastery', icon: Lightbulb, label: 'Skill Mastery' },
      { to: '/energy', icon: Zap, label: 'Energy' },
      { to: '/mystery-box', icon: Gift, label: 'Mystery Box' },
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
            className="rounded-t-3xl border-t border-gray-200 bg-white/95 p-4 pb-2 safe-area-bottom"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-gray-300" />
            <div className="text-sm font-display font-bold text-text-primary">Browse everything</div>
            <div className="mt-2 max-h-[55vh] overflow-y-auto pb-4">
              {MORE_GROUPS.map((group) => (
                <div key={group.label}>
                  <div className="px-2 pb-1 pt-4 text-[10px] font-mono uppercase tracking-[0.22em] text-text-light">{group.label}</div>
                  <div className="grid grid-cols-1 gap-1">
                    {group.items.map((item) => (
                      <Link
                        key={item.to}
                        to={item.to}
                        onClick={() => setMoreOpen(false)}
                        className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-text-secondary transition-colors hover:bg-brand-sky/10 hover:text-brand-sky"
                      >
                        <item.icon size={14} className="text-brand-sky" />
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

      <nav className="fixed bottom-0 left-0 right-0 z-50 md:hidden border-t border-white/60 bg-white shadow-[0_-4px_20px_rgba(11,16,32,0.06)] safe-area-bottom">
        {showLeague && (
          <Link
            to="/rank"
            className="block border-b border-white/60"
            style={{ background: `linear-gradient(90deg, ${tier.color}14, ${tier.color}08)` }}
          >
            <div className="flex items-center justify-center gap-1.5 h-7 px-3 text-[10px] font-mono">
              <Trophy size={11} style={{ color: tier.color }} />
              <span className="font-bold" style={{ color: tier.color }}>{tier.icon} {tier.name} League</span>
              <span className="text-text-light">
                #{startup.rank} of {startup.of} · {startup.weekly_xp || 0} XP
              </span>
              {startup.promoted_next_week && <span className="text-brand-emerald">↑ promoting</span>}
              {startup.relegated_next_week && <span className="text-brand-coral">↓ relegation</span>}
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
                    className={`transition-colors duration-200 ${isActive && !isMore ? 'text-brand-sky' : 'text-text-light'}`}
                  />
                  {isActive && !isMore && (
                    <motion.div layoutId="bottomNavActive"
                      className="absolute -bottom-1 w-5 h-0.5 rounded-full bg-brand-sky"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    />
                  )}
                </div>
                <span className={`text-[9px] font-mono tracking-wider mt-0.5 ${isActive && !isMore ? 'text-brand-sky font-semibold' : 'text-text-light'}`}>
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
