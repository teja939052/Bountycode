import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Compass, Code2, ClipboardList, User, Building2, Trophy, Flame, type LucideIcon } from 'lucide-react';
import useAuthStore from '../store/authStore';
import { useGamificationState } from '../hooks/useGamificationState';

interface NavItem {
  to: string;
  icon: LucideIcon;
  label: string;
}

const NAV_ITEMS: NavItem[] = [
  { to: '/journey', icon: Compass, label: 'Journey' },
  { to: '/practice', icon: Code2, label: 'Practice' },
  { to: '/mock-oa', icon: ClipboardList, label: 'Mock OA' },
  { to: '/interview', icon: User, label: 'AI Interview' },
  { to: '/company-tracks', icon: Building2, label: 'Companies' },
  { to: '/career-profile', icon: User, label: 'Profile' },
];

export default function BottomNav() {
  const location = useLocation();
  const { user } = useAuthStore();
  const { profile, startup } = useGamificationState();

  const hideOn = ['/', '/login', '/register', '/playground'];
  if (hideOn.includes(location.pathname)) return null;
  if (!user) return null;

  const league = (startup as any)?.league;
  const tier = league?.tier;
  const showLeague = tier && league?.of;
  const level = profile?.level ?? 1;
  const streak = profile?.streak ?? 0;

  return (
    <>
      <nav className="fixed bottom-0 left-0 right-0 z-50 md:hidden border-t border-white/10 bg-gray-900/90 backdrop-blur-xl safe-area-bottom">
        {showLeague && (
          <Link
            to="/leaderboard"
            className="block border-b border-white/10"
            style={{ background: `${tier.color}15` }}
          >
            <div className="flex items-center justify-center gap-1.5 h-7 px-3 text-[10px] font-mono">
              <Trophy size={11} style={{ color: tier.color }} />
              <span className="font-bold" style={{ color: tier.color }}>{tier.name} League</span>
              <span className="text-gray-400">
                #{league.rank} of {league.of} · {league.weekly_xp || 0} Diamonds
              </span>
              {league.promoted_next_week && <span className="text-emerald-400">&uarr; promoting</span>}
              {league.relegated_next_week && <span className="text-red-400">&darr; relegation</span>}
            </div>
          </Link>
        )}
        {streak > 0 && (
          <div className="flex items-center justify-center gap-1.5 h-6 text-[10px] font-mono text-orange-400 border-b border-white/5 bg-orange-500/5">
            <Flame size={10} className="fill-orange-500 text-orange-500" />
            <span className="font-bold">{streak} day streak</span>
          </div>
        )}
        <div className="flex items-center justify-around h-16 px-1">
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => {
            const isActive = location.pathname === to || location.pathname.startsWith(to + '/');
            return (
              <Link
                key={to}
                to={to}
                className="flex flex-col items-center justify-center gap-0.5 relative min-w-[56px] min-h-[44px] py-1"
                aria-label={label}
              >
                <div className="relative w-7 h-7 flex items-center justify-center">
                  <Icon size={18}
                    className={`transition-colors duration-200 ${isActive ? 'text-indigo-400' : 'text-gray-500'}`}
                  />
                  {isActive && (
                    <motion.div layoutId="bottomNavActive"
                      className="absolute -bottom-1 w-5 h-0.5 rounded-full bg-indigo-400"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    />
                  )}
                  {isActive && label === 'Levels' && (
                    <span className="absolute -top-1.5 -right-2 text-[8px] font-black bg-indigo-500 text-white rounded-full w-4 h-4 flex items-center justify-center">
                      {level}
                    </span>
                  )}
                </div>
                <span className={`text-[9px] tracking-wider mt-0.5 ${isActive ? 'text-indigo-400 font-bold' : 'text-gray-500'}`}>
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
