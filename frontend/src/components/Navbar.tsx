import { Link, useNavigate } from "react-router-dom";
import { useState, type ReactNode } from "react";
import type { LucideIcon } from "lucide-react";
import useAuthStore from "../store/authStore";
import {
  LogOut,
  Menu,
  X,
  Settings,
  Trophy,
  Flame,
  ChevronDown,
  Zap,
  BookOpen,
  Shield,
  Compass,
  Code2,
  Sparkles,
  Layers,
  GraduationCap,
  Calendar,
  BarChart3,
  MessageSquare,
  Share2,
  Video,
  Swords,
  Award,
  Wand2,
} from "lucide-react";

const PRIMARY_LINKS: NavItem[] = [
  { to: "/hub", label: "Hub" },
  { to: "/learn", label: "Learn", icon: BookOpen },
  { to: "/modules", label: "Modules", icon: GraduationCap },
  { to: "/problems", label: "Practice", icon: Code2 },
  { to: "/interview-booking", label: "Book Interview", icon: Calendar },
  { to: "/interview", label: "Interview" },
  { to: "/daily-drill", label: "Drill", icon: Flame },
  { to: "/daily-challenge", label: "30 Days", icon: Flame },
  { to: "/challenge-packs", label: "Packs", icon: Sparkles },
  { to: "/journeys", label: "Journeys", icon: Compass },
  { to: "/dsa-visualizer", label: "DSA Viz", icon: BarChart3 },
  { to: "/visualize/compare", label: "Compare", icon: Share2 },
  { to: "/playground", label: "Playground", icon: Code2 },
  { to: "/ai-mentor", label: "AI Mentor", icon: MessageSquare },
  { to: "/community", label: "Community", icon: MessageSquare },
  { to: "/scrims", label: "Scrims", icon: Video },
  { to: "/battles", label: "Battles", icon: Swords },
  { to: "/rank", label: "Rank", icon: Award },
  { to: "/project-generator", label: "AI Build", icon: Wand2 },
];

const TOOL_LINKS: NavItem[] = [
  { to: "/resume-ats", label: "Resume & ATS", icon: Layers },
  { to: "/system-design", label: "System Design", icon: Compass },
  { to: "/company-prep", label: "Company Intel", icon: Shield },
  { to: "/aptitude", label: "Aptitude", icon: GraduationCap },
  { to: "/salary-benchmark", label: "Salary Benchmark", icon: Trophy },
  { to: "/predictor", label: "Placement Predictor", icon: Sparkles },
  { to: "/tower", label: "Placement Tower", icon: Trophy },
];

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
<nav className="sticky top-0 z-50 border-b border-white/60 bg-white/75 backdrop-blur-2xl shadow-sm" role="navigation" aria-label="Main navigation">
       <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-brand-sky/70 to-transparent" />
       <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-brand-sky focus:text-white focus:rounded-lg">Skip to main content</a>
       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
         <div className="flex h-16 items-center justify-between gap-4">
           <Link to="/" className="flex items-center gap-3 group shrink-0" aria-label="PlacementPro home">
             <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-brand-sky via-brand-lavender to-brand-coral flex items-center justify-center shadow-soft-md transition-transform duration-300 group-hover:scale-105" aria-hidden="true">
               <Zap size={18} className="text-white" />
             </div>
             <div className="leading-tight">
               <div className="text-lg font-display font-extrabold tracking-tight text-text-primary">
                 Placement<span className="text-brand-sky">Pro</span>
               </div>
               <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">
                 Gameified Career Arena
               </div>
             </div>
           </Link>

           <div className="hidden lg:flex items-center gap-1" role="menubar">
             {user ? (
               <>
                 {PRIMARY_LINKS.map((item) => (
                   <NavLink key={item.to} to={item.to} icon={item.icon} role="menuitem">
                     {item.label}
                   </NavLink>
                 ))}

                 <div className="relative ml-1" role="none">
                   <button
                     onClick={() => setToolsOpen((prev) => !prev)}
                     aria-haspopup="true"
                     aria-expanded={toolsOpen}
                     className="quest-chip hover:border-brand-sky/40 hover:text-brand-sky transition-all"
                   >
                     Systems
                     <ChevronDown size={12} className={`transition-transform ${toolsOpen ? "rotate-180" : ""}`} aria-hidden="true" />
                   </button>

                   {toolsOpen && (
                     <>
                       <div className="fixed inset-0 z-10" onClick={() => setToolsOpen(false)} aria-hidden="true" />
                       <div className="absolute right-0 mt-3 w-72 rounded-2xl border border-white/70 bg-white/95 p-2 shadow-soft-lg z-20" role="menu" aria-label="Tools menu">
                         {TOOL_LINKS.map((item) => (
                           <DropdownLink key={item.to} to={item.to} onClick={() => setToolsOpen(false)} icon={item.icon} role="menuitem">
                             {item.label}
                           </DropdownLink>
                         ))}
                         <div className="my-2 h-px bg-gray-100" role="separator" />
                         <DropdownLink to="/history" onClick={() => setToolsOpen(false)} role="menuitem">Mission Log</DropdownLink>
                         <DropdownLink to="/settings" onClick={() => setToolsOpen(false)} role="menuitem">Settings</DropdownLink>
                       </div>
                     </>
                   )}
                 </div>

                 <Link to="/problems?random=true" className="ml-2 inline-flex items-center gap-2 rounded-full border border-brand-sky/20 bg-brand-sky/10 px-4 py-2 text-sm font-medium text-brand-sky transition-all hover:bg-brand-sky/20 hover:border-brand-sky/30" aria-label="Quick practice - random question">
                   <Sparkles size={14} aria-hidden="true" />
                   Quick Practice
                 </Link>

                 <div className="ml-3 flex items-center gap-3 rounded-full border border-gray-200 bg-white px-3 py-1.5 shadow-sm" aria-label="User menu">
                   <div className="hidden xl:flex flex-col text-right">
                     <span className="text-[10px] font-mono uppercase tracking-[0.22em] text-text-light">Signed in as</span>
                     <span className="max-w-[140px] truncate text-sm font-medium text-text-secondary">{user.name}</span>
                   </div>
                   <span className="rounded-full border border-brand-coral/20 bg-brand-coral-pale px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-coral" aria-label={`Plan: ${user.plan}`}>
                     {user.plan}
                   </span>
                   <Link to="/settings" className="text-text-light transition-colors hover:text-brand-coral" aria-label="Settings">
                     <Settings size={17} />
                   </Link>
                   <button onClick={handleLogout} className="text-text-light transition-colors hover:text-error" aria-label="Logout">
                     <LogOut size={17} />
                   </button>
                 </div>
               </>
             ) : (
               <>
                 <Link to="/login" className="px-3 py-2 text-sm font-medium text-text-light transition-colors hover:text-text-primary" aria-label="Login">
                   Login
                 </Link>
                 <Link to="/register" className="btn-primary px-5 py-2.5 text-sm" aria-label="Start free trial">
                   Start Free
                 </Link>
               </>
             )}
           </div>

          <button
            className="lg:hidden inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white/80 p-2 text-text-secondary shadow-sm"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {mobileOpen && (
          <div className="lg:hidden pb-4">
            <div className="rounded-3xl border border-white/70 bg-white/95 p-3 shadow-soft-lg">
              {user ? (
                <>
                  <div className="mb-3 rounded-2xl bg-gradient-to-r from-brand-sky/10 via-brand-lavender/10 to-brand-coral/10 p-4">
                    <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Command Deck</div>
                    <div className="mt-1 text-lg font-display font-bold text-text-primary">{user.name}</div>
                    <div className="mt-2 flex items-center gap-2">
                      <span className="rounded-full border border-brand-coral/20 bg-brand-coral-pale px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-coral">
                        {user.plan}
                      </span>
                      <span className="rounded-full border border-brand-sky/20 bg-brand-sky/10 px-2.5 py-1 text-[10px] font-mono uppercase tracking-[0.2em] text-brand-sky">
                        Quick Practice
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

                  <div className="my-3 h-px bg-gray-100" />

                  <div className="grid grid-cols-1 gap-2">
                    {TOOL_LINKS.map((item) => (
                      <MobileLink key={item.to} to={item.to} onClick={() => setMobileOpen(false)} icon={item.icon}>
                        {item.label}
                      </MobileLink>
                    ))}
                    <MobileLink to="/history" onClick={() => setMobileOpen(false)}>Mission Log</MobileLink>
                    <MobileLink to="/settings" onClick={() => setMobileOpen(false)}>Settings</MobileLink>
                  </div>

                  <div className="mt-3 flex gap-2">
                    <button onClick={handleLogout} className="flex-1 rounded-xl border border-red-200 bg-red-50 px-4 py-2.5 text-sm font-medium text-error">
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

function NavLink({ to, children, icon: Icon, role }: NavLinkProps) {
  return (
    <Link
      to={to}
      role={role}
      className="flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-text-light transition-all hover:bg-brand-sky/10 hover:text-brand-sky"
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
      className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-text-secondary transition-colors hover:bg-brand-sky/10 hover:text-brand-sky"
    >
      {Icon ? <Icon size={14} className="text-brand-sky" /> : null}
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
          ? "bg-brand-sky text-white shadow-soft-md"
          : "border border-gray-200 bg-white text-text-secondary hover:border-brand-sky/30 hover:bg-brand-sky/10 hover:text-brand-sky"
      }`}
    >
      {Icon ? <Icon size={14} /> : null}
      {children}
    </Link>
  );
}
