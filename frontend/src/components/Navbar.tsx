import { Link, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState, type ReactNode } from "react";
import type { LucideIcon } from "lucide-react";
import type { AuthState } from "../store/authStore";
import useAuthStore from "../store/authStore";
import { GamificationWidget } from "../components/gamification";
import {
  LogOut,
  Menu,
  X,
  Settings,
  ChevronDown,
  BookOpen,
  Code2,
  Sparkles,
  LayoutDashboard,
  Home,
  MessageSquare,
  Calendar,
  Trophy,
  Briefcase,
  Castle,
  Brain,
  List,
  Lightbulb,
  User,
} from "lucide-react";

/* Primary IA — exactly 5 top-level destinations (Material/Apple guideline).
   Dashboard is the student's home base; Career lives in "More → Your Journey".
   Everything else lives in the "More" menu so users build a fast mental map.
   Resume/ATS/Cover Letter appear ONLY under Career (no duplication). */
const PRIMARY_LINKS: NavItem[] = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/hub", label: "Home", icon: Home },
  { to: "/prepare", label: "Prepare", icon: BookOpen },
  { to: "/practice", label: "Practice", icon: Code2 },
  { to: "/compete", label: "Compete", icon: Trophy },
];

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.plan === "pro" || user?.plan === "lifetime";

  const MORE_GROUPS: NavGroup[] = [
    {
      label: "Your Journey",
      items: [
        { to: "/tower", label: "Tower", icon: Castle },
        { to: "/gamification", label: "Gamification", icon: Trophy },
        { to: "/profile", label: "Profile", icon: User },
        { to: "/history", label: "History", icon: List },
      ],
    },
    {
      label: "Practice",
      items: [
        { to: "/question-bank", label: "Question Bank", icon: List },
        { to: "/solve/:id", label: "Solve Problem", icon: Code2 },
        { to: "/coding", label: "Coding Challenge", icon: Code2 },
        { to: "/compiler", label: "Compiler", icon: Code2 },
        { to: "/daily-drill", label: "Daily Drill", icon: Calendar },
        { to: "/daily-challenge", label: "Daily Challenge", icon: Trophy },
        { to: "/challenge-packs", label: "Challenge Packs", icon: List },
        { to: "/dsa-visualizer", label: "DSA Visualizer", icon: Brain },
      ],
    },
    {
      label: "Assessments",
      items: [
        { to: "/aptitude", label: "Aptitude Test", icon: Brain },
        { to: "/mock-oa", label: "Mock OA", icon: Castle },
        { to: "/system-design", label: "System Design", icon: LayoutDashboard },
        { to: "/predictor", label: "Interview Predictor", icon: Lightbulb },
      ],
    },
    {
      label: "Career Tools",
      items: [
        { to: "/resume", label: "Resume Builder", icon: LayoutDashboard },
        { to: "/resume-studio", label: "Resume Studio", icon: LayoutDashboard },
        { to: "/ats", label: "ATS Optimizer", icon: Lightbulb },
        { to: "/interview", label: "Mock Interview", icon: MessageSquare },
        { to: "/ai-mentor", label: "AI Mentor", icon: Brain },
      ],
    },
    {
      label: "Learning",
      items: [
        { to: "/learn", label: "Learning Hub", icon: BookOpen },
        { to: "/languages", label: "Language Paths", icon: Code2 },
        { to: "/lessons", label: "Lessons", icon: LayoutDashboard },
        { to: "/content", label: "Content Bundles", icon: List },
        { to: "/concepts", label: "Concepts", icon: Lightbulb },
      ],
    },
    {
      label: "Community & Placements",
      items: [
        { to: "/community", label: "Community", icon: MessageSquare },
        { to: "/indian-placement", label: "Indian Placement", icon: Briefcase },
        { to: "/placement-calendar", label: "Placement Calendar", icon: Calendar },
        { to: "/placement-drives", label: "Placement Drives", icon: Calendar },
        { to: "/alumni-experiences", label: "Alumni Experiences", icon: User },
        { to: "/leaderboard", label: "Leaderboard", icon: Trophy },
        { to: "/contests", label: "Contests", icon: Trophy },
      ],
    },
    {
      label: "Settings",
      items: [
        { to: "/settings", label: "Settings", icon: Settings },
      ],
    },
  ];

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-transparent bg-transparent" role="navigation" aria-label="Main navigation">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-brand-primary focus:text-white focus:rounded-lg">Skip to main content</a>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between gap-4">
          <Link to="/" className="flex items-center gap-3 group shrink-0" aria-label="BountyCode home">
            <div className="relative">
              <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-nature-leaf/40 to-nature-blossom/40 blur-md opacity-70 group-hover:opacity-100 transition-opacity" aria-hidden="true" />
              <div className="relative h-10 w-10 rounded-2xl bg-gradient-to-br from-nature-leaf via-nature-moss to-nature-blossom flex items-center justify-center shadow-[0_8px_20px_-8px_rgba(45,130,110,0.4)] transition-transform duration-300 group-hover:scale-105 overflow-hidden">
                <img src="/assets/logo/bountycode-icon.svg" alt="BountyCode" className="h-7 w-7" />
              </div>
            </div>
            <div className="leading-tight">
              <div className="text-lg font-display font-extrabold tracking-tight text-text-primary">
                BountyCode
              </div>
              <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-muted">
                Placement Prep Platform
              </div>
            </div>
          </Link>

          <div className="relative hidden lg:flex items-center gap-1" role="menubar">
            {user ? (
              <>
                {PRIMARY_LINKS.map((item) => (
                  <NavLink key={item.to} to={item.to} icon={item.icon} role="menuitem">
                    {item.label}
                  </NavLink>
                ))}

                 <button
                     onClick={() => setToolsOpen((prev) => !prev)}
                     aria-haspopup="true"
                     aria-expanded={toolsOpen}
                     className="rounded-full border border-brand-primary/30 bg-brand-primary/10 px-4 py-2 text-sm font-medium text-brand-primary transition-all hover:bg-brand-primary/20 hover:border-brand-primary/50"
                   >
                     More
                     <ChevronDown size={12} className={`transition-transform ${toolsOpen ? "rotate-180" : ""}`} aria-hidden="true" />
                   </button>

                   {toolsOpen && (
                      <>
                        <div className="fixed inset-0 z-10" onClick={() => setToolsOpen(false)} aria-hidden="true" />
                        <div className="absolute right-0 mt-8 w-[420px] rounded-2xl border border-gray-200 bg-white border-border/95 p-4 shadow-xl z-20 backdrop-blur" role="menu" aria-label="More menu">
                        <div className="grid grid-cols-1 gap-6">
                          {MORE_GROUPS.map((group) => (
                            <div key={group.label}>
                              <div className="px-2 pb-1 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted border-b border-gray-100 pb-2">{group.label}</div>
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                {group.items.map((item) => (
                                  <DropdownLink key={item.to} to={item.to} onClick={() => setToolsOpen(false)} icon={item.icon} role="menuitem">
                                    {item.label}
                                  </DropdownLink>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                        </div>
                       </>
                    )}

                <Link to="/problems?random=true" className="ml-2 inline-flex items-center gap-2 rounded-full border border-brand-primary/30 bg-brand-primary/10 px-4 py-2 text-sm font-medium text-brand-primary transition-all hover:bg-brand-primary/20 hover:border-brand-primary/50" aria-label="Quick practice - random question">
                  <Sparkles size={14} aria-hidden="true" />
                  Quick Practice
                </Link>

                <UserMenu user={user} onLogout={handleLogout} />
              </>
             ) : (
              <>
                <Link to="/login" className="px-3 py-2 text-sm font-medium text-text-muted transition-colors hover:text-text-primary" aria-label="Login">
                  Login
                </Link>
                <Link to="/register" className="rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-medium text-text-primary hover:bg-brand-primary/90 transition-colors" aria-label="Start free trial">
                  Start Free
                </Link>
              </>
            )}
          </div>


<button
            className="lg:hidden inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white border-border/80 p-2 text-text-muted shadow-sm"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {mobileOpen && (
          <div className="lg:hidden pb-4">
            <div className="rounded-3xl border border-gray-200 bg-white border-border/95 p-3 shadow-lg backdrop-blur">
              {user ? (
                <>
                  <div className="mb-3 rounded-2xl border border-border bg-white p-3">
                    <button
                      type="button"
                      onClick={() => setAccountOpen((open) => !open)}
                      aria-expanded={accountOpen}
                      aria-controls="mobile-account-details"
                      className="flex w-full items-center justify-between gap-3 text-left"
                    >
                      <span className="truncate text-sm font-semibold text-text-primary">{user.name || "Account"}</span>
                      <ChevronDown size={16} className={`shrink-0 transition-transform ${accountOpen ? "rotate-180" : ""}`} />
                    </button>
                    {accountOpen && (
                      <div id="mobile-account-details" className="mt-3 border-t border-border pt-3">
                        <span className="inline-flex rounded-full border border-brand-primary/25 bg-brand-primary/10 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-brand-primary">
                          {user.plan || "Free"} plan
                        </span>
                        <div className="my-3 rounded-xl bg-brand-primary/5 p-3">
                          <GamificationWidget xp={user.xp ?? 0} level={user.level ?? 1} streak={user.streak ?? 0} league={(user as any).leagueRank ?? 5} badges={(user as any).badgesCount ?? 0} />
                        </div>
                        <Link to="/settings" onClick={() => { setMobileOpen(false); setAccountOpen(false); }} className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-text-secondary hover:bg-brand-primary/10 hover:text-brand-primary">
                          <Settings size={16} /> Account settings
                        </Link>
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    {PRIMARY_LINKS.map((item) => (
                      <MobileLink key={item.to} to={item.to} onClick={() => setMobileOpen(false)} icon={item.icon}>
                        {item.label}
                      </MobileLink>
                    ))}
                  </div>

                  {MORE_GROUPS.map((group) => (
                    <div key={group.label}>
                      <div className="px-1 pb-1 pt-4 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">{group.label}</div>
                      <div className="grid grid-cols-1 gap-2">
                        {group.items.map((item) => (
                          <MobileLink key={item.to} to={item.to} onClick={() => setMobileOpen(false)} icon={item.icon}>
                            {item.label}
                          </MobileLink>
                        ))}
                      </div>
                    </div>
                  ))}

                  <div className="mt-3 flex gap-2">
                    <button onClick={handleLogout} className="flex-1 rounded-xl border border-error/20 bg-error/10 px-4 py-2.5 text-sm font-medium text-error">
                      Logout
                    </button>
                  </div>
                </>
              ) : (
                <div className="grid gap-2">
                  <MobileLink to="/login" onClick={() => setMobileOpen(false)}>Login</MobileLink>
                  <MobileLink to="/register" onClick={() => setMobileOpen(false)} primary>
                    Start Free
                  </MobileLink>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

interface NavLinkProps {
  to: string;
  children: ReactNode;
  icon?: LucideIcon;
  role?: string;
  onClick?: () => void;
}

interface NavItem {
  to: string;
  label: string;
  icon?: LucideIcon;
}

interface NavGroup {
  label: string;
  items: NavItem[];
}

function NavLink({ to, children, icon: Icon, role }: NavLinkProps) {
  return (
    <Link
      to={to}
      role={role}
      className="flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-text-muted transition-all duration-200 hover:bg-brand-primary/10 hover:text-brand-primary"
    >
      {Icon ? <Icon size={14} /> : null}
      {children}
    </Link>
  );
}

function DropdownLink({ to, children, onClick, icon: Icon, role }: NavLinkProps) {
  return (
    <Link
      to={to}
      onClick={onClick}
      role={role}
      className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-text-secondary transition-colors hover:bg-brand-primary/10 hover:text-brand-primary"
    >
      {Icon ? <Icon size={14} className="text-brand-primary" /> : null}
      {children}
    </Link>
  );
}

function MobileLink({ to, children, onClick, primary, icon: Icon }: NavLinkProps & { primary?: boolean }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={`flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium transition-colors ${
        primary
          ? "rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-medium text-text-primary hover:bg-brand-primary/90 transition-colors"
          : "border border-gray-200 bg-white border-border/80 text-text-secondary hover:border-brand-primary/40 hover:bg-brand-primary/10 hover:text-brand-primary"
      }`}
    >
      {Icon ? <Icon size={14} /> : null}
      {children}
    </Link>
  );
}

function UserMenu({ user, onLogout }: { user: NonNullable<AuthState["user"]>; onLogout: () => void }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDocClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onDocClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDocClick);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  return (
    <div ref={ref} className="relative ml-3">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="User menu"
        className="flex items-center gap-2 rounded-full border border-gray-200 bg-white border-border/80 px-3 py-1.5 text-sm font-medium text-text-primary shadow-sm transition-colors hover:border-brand-primary/40 hover:bg-brand-primary/5"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-brand-primary/10 text-brand-primary">
          <User size={15} aria-hidden="true" />
        </span>
        <span className="max-w-[140px] truncate">{user.name}</span>
        <ChevronDown size={14} className={`text-text-muted transition-transform ${open ? "rotate-180" : ""}`} aria-hidden="true" />
      </button>

      {open && (
        <div
          role="menu"
          aria-label="Account menu"
          className="absolute right-0 mt-2 w-72 rounded-2xl border border-gray-200 bg-white border-border/95 p-3 shadow-lg z-20"
        >
          <div className="px-2 pb-2">
            <div className="text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">Signed in as</div>
            <div className="mt-0.5 truncate text-sm font-medium text-text-primary">{user.name}</div>
            <div className="mt-2 flex items-center gap-2">
              <span className="rounded-full border border-brand-primary/30 bg-brand-primary/10 px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-primary" aria-label={`Plan: ${user.plan}`}>
                {user.plan}
              </span>
            </div>
          </div>
          <div className="border-t border-border/60 pt-2">
            <GamificationWidget xp={user.xp ?? 0} level={user.level ?? 1} streak={user.streak ?? 0} league={(user as any).leagueRank ?? 5} badges={(user as any).badgesCount ?? 0} />
          </div>
          <div className="mt-2 grid gap-1 border-t border-border/60 pt-2">
            <Link to="/settings" onClick={() => setOpen(false)} role="menuitem" className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-text-secondary transition-colors hover:bg-brand-primary/10 hover:text-brand-primary">
              <Settings size={15} aria-hidden="true" /> Settings
            </Link>
            <Link to="/profile" onClick={() => setOpen(false)} role="menuitem" className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-text-secondary transition-colors hover:bg-brand-primary/10 hover:text-brand-primary">
              <User size={15} aria-hidden="true" /> Profile
            </Link>
            <button onClick={() => { setOpen(false); onLogout(); }} role="menuitem" className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-left text-sm text-error transition-colors hover:bg-error/10">
              <LogOut size={15} aria-hidden="true" /> Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
