// @ts-nocheck
import { Link, useNavigate } from "react-router-dom";
import { useState, type ReactNode } from "react";
import type { LucideIcon } from "lucide-react";
import { BountyCodeLogo } from "./brand/BountyCodeLogo";
import { useThemeStore } from "../store/themeStore";
import useAuthStore from "../store/authStore";
import {
  LogOut,
  Menu,
  X,
  Settings,
  ChevronDown,
  BookOpen,
  Code2,
  Sparkles,
  Lightbulb,
  Shield,
  Network,
  ClipboardList,
  Layers,
  Cpu,
  BookX,
  Gauge,
  User,
  Sun,
  Moon,
  CalendarDays,
  Trophy,
  Swords,
  GraduationCap,
  Compass,
  Target,
  FlaskConical,
  Briefcase,
  FileText,
  Building2,
} from "lucide-react";
import BackgroundSwitcher from "../components/background/BackgroundSwitcher";
import { useLocation } from "react-router-dom";

/* Unified navigation */
const PRIMARY_LINKS: NavItem[] = [
  { to: "/learning", label: "Learn", icon: BookOpen },
  { to: "/placement", label: "Command", icon: ClipboardList },
  { to: "/battlefield", label: "Battlefield", icon: Target },
  { to: "/interview", label: "Interview", icon: CalendarDays },
];

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const location = useLocation();
  const isLanding = location.pathname === "/";
  const { mode, setMode } = useThemeStore();

  const isAdmin = user?.is_admin || user?.role === "admin" || user?.plan === "pro" || user?.plan === "lifetime";

  const cycleTheme = () => {
    if (mode === "crystal-light") setMode("crystal-dark");
    else if (mode === "crystal-dark") setMode("crystal-light");
    else setMode("crystal-light");
  };

  const MORE_GROUPS: NavGroup[] = [
    {
      label: "Learn",
      items: [
        { to: "/learning", label: "Learning Hub", icon: BookOpen },
        { to: "/compiler", label: "Compiler", icon: Code2 },
      ],
    },
    {
      label: "Practice",
      items: [
        { to: "/question-bank", label: "Question Bank", icon: BookOpen },
        { to: "/aptitude", label: "Aptitude", icon: ClipboardList },
        { to: "/coding", label: "Coding Challenge", icon: Code2 },
        { to: "/mock-oa", label: "Mock OA", icon: ClipboardList },
      ],
    },
    {
      label: "Company Prep",
      items: [
        { to: "/battlefield", label: "Battlefield", icon: Target },
        { to: "/interview", label: "Mock Interview", icon: CalendarDays },
      ],
    },
    {
      label: "Career",
      items: [
        { to: "/resume", label: "Resume Builder", icon: FileText },
        { to: "/ats", label: "ATS Optimizer", icon: Sparkles },
        { to: "/daily-challenge", label: "Daily Challenge", icon: Trophy },
      ],
    },
    ...(isAdmin
      ? [
          {
            label: "Admin",
            items: [
              { to: "/admin", label: "Admin Dashboard", icon: Shield },
            ],
          } as NavGroup,
        ]
      : []),
  ];

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <nav className={`sticky top-0 z-50 border-b ${isLanding ? "bg-white/90 border-white/40 backdrop-blur-md" : "border-transparent bg-transparent"}`} role="navigation" aria-label="Main navigation">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-brand-primary focus:text-white focus:rounded-lg">Skip to main content</a>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between gap-4">
          <Link to="/" className="flex items-center gap-3 group shrink-0" aria-label="BountyCode home">
            <BountyCodeLogo variant="lockup" className="h-9" />
          </Link>

          <div className="hidden lg:flex items-center gap-1" role="menubar">
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
                    <div className="absolute right-0 mt-3 w-96 rounded-2xl border border-border/95 bg-surface-card p-3 shadow-lg z-20 backdrop-blur" role="menu" aria-label="More menu">
                      <div className="grid grid-cols-1 gap-4">
                        {MORE_GROUPS.map((group) => (
                          <div key={group.label}>
                            <div className="px-3 pb-1 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">{group.label}</div>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1">
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

                <Link to="/arena?random=true" className="ml-2 hidden xl:inline-flex items-center gap-2 rounded-full border border-brand-primary/30 bg-brand-primary/10 px-4 py-2 text-sm font-medium text-brand-primary transition-all hover:bg-brand-primary/20 hover:border-brand-primary/50" aria-label="Quick practice - random challenge">
                  <Sparkles size={14} aria-hidden="true" />
                  Quick Practice
                </Link>

                <div className="ml-3 flex items-center gap-3 rounded-full border border-border/80 bg-surface-card px-3 py-1.5 shadow-sm" aria-label="User menu">
                  <div className="hidden xl:flex flex-col text-right">
                    <span className="text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">Signed in as</span>
                    <span className="max-w-[140px] truncate text-sm font-medium text-text-primary">{user.name}</span>
                  </div>
                  <span className="rounded-full border border-brand-primary/30 bg-brand-primary/10 px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-primary" aria-label={`Plan: ${user.plan}`}>
                    {user.plan}
                  </span>
                  <Link to="/settings" className="text-text-muted transition-colors hover:text-brand-primary" aria-label="Settings">
                    <Settings size={17} />
                  </Link>
                  <button onClick={cycleTheme} className="text-text-muted transition-colors hover:text-brand-primary" aria-label="Toggle theme">
                    {mode === "crystal-dark" ? <Sun size={17} /> : <Moon size={17} />}
                  </button>
                  <BackgroundSwitcher />
                  <button onClick={handleLogout} className="text-text-muted transition-colors hover:text-error" aria-label="Logout">
                    <LogOut size={17} />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="px-3 py-2 text-sm font-medium text-text-muted transition-colors hover:text-text-primary" aria-label="Login">
                  Login
                </Link>
                <Link to="/start" className="rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-medium text-text-primary hover:bg-brand-primary/90 transition-colors" aria-label="Start free path">
                  Start Free
                </Link>
              </>
            )}
          </div>

          <button
            className="lg:hidden inline-flex items-center justify-center rounded-xl border border-border/80 bg-surface-card p-2 text-text-muted shadow-sm"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {mobileOpen && (
          <div className="lg:hidden pb-4">
            <div className="rounded-3xl border border-border/95 bg-surface-card p-3 shadow-lg backdrop-blur">
              {user ? (
                <>
                  <div className="mb-3 rounded-2xl bg-gradient-to-r from-brand-primary/10 via-brand-secondary/10 to-brand-tertiary/10 p-4">
                    <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-muted">Account</div>
                    <div className="mt-1 text-lg font-display font-bold text-text-primary">{user.name}</div>
                    <div className="mt-2 flex items-center gap-2">
                      <span className="rounded-full border border-brand-primary/30 bg-brand-primary/10 px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-primary">
                        {user.plan}
                      </span>
                    </div>
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
                  <MobileLink to="/start" onClick={() => setMobileOpen(false)} primary>
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
  const { pathname } = useLocation();
  const active = pathname === to || (to !== "/" && pathname.startsWith(to + "/"));
  return (
    <Link
      to={to}
      role={role}
      aria-current={active ? "page" : undefined}
      className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-all duration-200 ${
        active
          ? "bg-brand-primary/15 text-brand-primary"
          : "text-text-muted hover:bg-brand-primary/10 hover:text-brand-primary"
      }`}
    >
      {Icon ? <Icon size={14} /> : null}
      {children}
    </Link>
  );
}

function DropdownLink({ to, children, onClick, icon: Icon, role }: NavLinkProps) {
  const { pathname } = useLocation();
  const active = pathname === to;
  return (
    <Link
      to={to}
      onClick={onClick}
      role={role}
      aria-current={active ? "page" : undefined}
      className={`flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm transition-colors ${
        active
          ? "bg-brand-primary/15 text-brand-primary"
          : "text-text-secondary hover:bg-brand-primary/10 hover:text-brand-primary"
      }`}
    >
      {Icon ? <Icon size={14} className="text-brand-primary" /> : null}
      {children}
    </Link>
  );
}

function MobileLink({ to, children, onClick, primary, icon: Icon }: NavLinkProps & { primary?: boolean }) {
  const { pathname } = useLocation();
  const active = !primary && pathname === to;
  return (
    <Link
      to={to}
      onClick={onClick}
      aria-current={active ? "page" : undefined}
      className={`flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium transition-colors ${
        primary
          ? "rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-medium text-text-primary hover:bg-brand-primary/90 transition-colors"
          : active
            ? "border border-brand-primary/40 bg-brand-primary/10 text-brand-primary"
            : "border border-border/80 bg-surface-card text-text-secondary hover:border-brand-primary/40 hover:bg-brand-primary/10 hover:text-brand-primary"
      }`}
    >
      {Icon ? <Icon size={14} /> : null}
      {children}
    </Link>
  );
}
