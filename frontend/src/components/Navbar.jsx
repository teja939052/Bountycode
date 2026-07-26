import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import { LogOut, Menu, X, Settings, Trophy, Flame, ChevronDown, Zap, Palette } from "lucide-react";
import { useState } from "react";
import { useTheme } from "../contexts/ThemeContext";

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [themeOpen, setThemeOpen] = useState(false);
  const { theme, setTheme, themes } = useTheme();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-space-border bg-space-void/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-9 h-9 bg-gradient-to-br from-cyber-blue to-cyber-purple rounded-lg flex items-center justify-center shadow-cyber-blue group-hover:shadow-cyber-blue-intense transition-shadow duration-300">
              <Zap size={18} className="text-white" />
            </div>
            <div>
              <span className="text-lg font-display font-bold text-white tracking-wider">
                PLACEMENT<span className="text-cyber-blue">PRO</span>
              </span>
              <span className="hidden sm:block text-[8px] font-mono text-gray-500 tracking-[0.2em] uppercase -mt-1">
                Command Deck
              </span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {user ? (
              <>
                <NavLink to="/dashboard">Dashboard</NavLink>
                <NavLink to="/problems">DSA Practice</NavLink>
                <NavLink to="/interview">Interview</NavLink>
                <NavLink to="/coding">Coding</NavLink>
                <NavLink to="/aptitude">Aptitude</NavLink>
                <NavLink to="/daily-drill">
                  <Flame size={14} className="text-cyber-amber" />
                  Drill
                </NavLink>
                <NavLink to="/problems?random=true">
                  <Sparkles size={14} className="text-cyber-green" />
                  Quick Practice
                </NavLink>
                <NavLink to="/leaderboard">
                  <Trophy size={14} className="text-cyber-purple" />
                  Ranks
                </NavLink>
                <NavLink to="/contests">
                  🏆 Contests
                </NavLink>

                {/* Tools dropdown */}
                <div className="relative">
                  <button
                    onClick={() => setToolsOpen(!toolsOpen)}
                    className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-400 hover:text-cyber-blue rounded-lg hover:bg-cyber-blue/5 transition-all duration-200"
                  >
                    Systems
                    <ChevronDown size={14} className={`transition-transform duration-200 ${toolsOpen ? "rotate-180" : ""}`} />
                  </button>
                  {toolsOpen && (
                    <>
                      <div className="fixed inset-0 z-10" onClick={() => setToolsOpen(false)} />
                      <div className="absolute right-0 mt-2 w-60 bg-space-panel/95 backdrop-blur-xl rounded-xl shadow-cyber-blue border border-space-border py-2 z-20">
                        <DropdownLink to="/resume" onClick={() => setToolsOpen(false)}>Hull Builder</DropdownLink>
                        <DropdownLink to="/ats" onClick={() => setToolsOpen(false)}>Hull Scanner</DropdownLink>
                        <DropdownLink to="/cover-letter" onClick={() => setToolsOpen(false)}>Cover Letter & LinkedIn</DropdownLink>
                        <DropdownLink to="/system-design" onClick={() => setToolsOpen(false)}>System Design</DropdownLink>
                        <DropdownLink to="/company-prep" onClick={() => setToolsOpen(false)}>Company Intel</DropdownLink>
                        <DropdownLink to="/indian-placement" onClick={() => setToolsOpen(false)}>🇮🇳 Indian Placement</DropdownLink>
                        <DropdownLink to="/salary-benchmark" onClick={() => setToolsOpen(false)}>Salary Benchmark</DropdownLink>
                        <DropdownLink to="/salary-negotiation" onClick={() => setToolsOpen(false)}>Negotiation Coach</DropdownLink>
                        <DropdownLink to="/predictor" onClick={() => setToolsOpen(false)}>Placement Predictor</DropdownLink>
                        <DropdownLink to="/fingerprint" onClick={() => setToolsOpen(false)}>DSA Fingerprint</DropdownLink>
                        <DropdownLink to="/tower" onClick={() => setToolsOpen(false)}>Placement Tower</DropdownLink>
                        <div className="border-t border-space-border my-1" />
                        <DropdownLink to="/history" onClick={() => setToolsOpen(false)}>Mission Log</DropdownLink>
                        <DropdownLink to="/study-groups" onClick={() => setToolsOpen(false)}>Study Groups</DropdownLink>
                        <DropdownLink to="/contests" onClick={() => setToolsOpen(false)}>Monthly Contests</DropdownLink>
                        <DropdownLink to="/settings" onClick={() => setToolsOpen(false)}>Settings</DropdownLink>
                      </div>
                    </>
                  )}
                </div>

                <div className="flex items-center gap-2 ml-3 pl-3 border-l border-space-border">
                  <div className="relative">
                    <button
                      onClick={() => setThemeOpen(!themeOpen)}
                      className="text-gray-500 hover:text-cyber-blue transition-colors"
                    >
                      <Palette size={18} />
                    </button>
                    {themeOpen && (
                      <>
                        <div className="fixed inset-0 z-10" onClick={() => setThemeOpen(false)} />
                        <div className="absolute right-0 mt-2 w-40 bg-space-panel/95 backdrop-blur-xl rounded-xl shadow-cyber-blue border border-space-border py-2 z-20">
                          {themes.map((t) => (
                            <button
                              key={t.id}
                              onClick={() => { setTheme(t.id); setThemeOpen(false); }}
                              className={`w-full text-left px-4 py-2 text-sm hover:bg-cyber-blue/5 transition-colors ${
                                theme === t.id ? "text-cyber-blue font-medium" : "text-gray-300"
                              }`}
                            >
                              <span className={`inline-block w-3 h-3 rounded-full bg-gradient-to-r ${t.accent} mr-2`} />
                              {t.label}
                            </button>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                  <Link to="/settings" className="text-gray-500 hover:text-cyber-blue transition-colors">
                    <Settings size={18} />
                  </Link>
                  <span className="text-sm text-gray-400 max-w-[100px] truncate font-mono">{user.name}</span>
                  <span className="text-[10px] px-2 py-0.5 bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30 rounded-full font-mono uppercase tracking-wider">
                    {user.plan}
                  </span>
                  <button onClick={handleLogout} className="text-gray-500 hover:text-cyber-red transition-colors">
                    <LogOut size={18} />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-400 hover:text-white font-medium px-3 py-2 transition-colors">
                  Login
                </Link>
                <Link to="/register" className="btn-primary text-sm py-2 px-4">
                  Get Started Free
                </Link>
              </>
            )}
          </div>

          <button className="md:hidden text-gray-400 hover:text-white" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Nav */}
        {mobileOpen && (
          <div className="md:hidden pb-4 space-y-1 border-t border-space-border pt-4">
            {user ? (
              <>
                <MobileLink to="/dashboard" onClick={() => setMobileOpen(false)}>Dashboard</MobileLink>
                <MobileLink to="/problems" onClick={() => setMobileOpen(false)}>DSA Practice</MobileLink>
                <MobileLink to="/interview" onClick={() => setMobileOpen(false)}>Interview</MobileLink>
                <MobileLink to="/coding" onClick={() => setMobileOpen(false)}>Coding</MobileLink>
                <MobileLink to="/aptitude" onClick={() => setMobileOpen(false)}>Aptitude</MobileLink>
                <MobileLink to="/daily-drill" onClick={() => setMobileOpen(false)}>Daily Drill</MobileLink>
                <MobileLink to="/problems?random=true" onClick={() => setMobileOpen(false)}>Quick Practice</MobileLink>
                <MobileLink to="/leaderboard" onClick={() => setMobileOpen(false)}>Leaderboard</MobileLink>
                <MobileLink to="/contests" onClick={() => setMobileOpen(false)}>Contests</MobileLink>
                <div className="border-t border-space-border my-2" />
                <MobileLink to="/resume" onClick={() => setMobileOpen(false)}>Resume Builder</MobileLink>
                <MobileLink to="/ats" onClick={() => setMobileOpen(false)}>ATS Scanner</MobileLink>
                <MobileLink to="/cover-letter" onClick={() => setMobileOpen(false)}>Cover Letter</MobileLink>
                <MobileLink to="/system-design" onClick={() => setMobileOpen(false)}>System Design</MobileLink>
                <MobileLink to="/company-prep" onClick={() => setMobileOpen(false)}>Company Intel</MobileLink>
                <MobileLink to="/indian-placement" onClick={() => setMobileOpen(false)}>🇮🇳 Indian Placement</MobileLink>
                <MobileLink to="/salary-benchmark" onClick={() => setMobileOpen(false)}>Salary Benchmark</MobileLink>
                <MobileLink to="/predictor" onClick={() => setMobileOpen(false)}>Predictor</MobileLink>
                <MobileLink to="/fingerprint" onClick={() => setMobileOpen(false)}>DSA Fingerprint</MobileLink>
                <MobileLink to="/tower" onClick={() => setMobileOpen(false)}>Placement Tower</MobileLink>
                <MobileLink to="/study-groups" onClick={() => setMobileOpen(false)}>Study Groups</MobileLink>
                <MobileLink to="/history" onClick={() => setMobileOpen(false)}>Mission Log</MobileLink>
                <MobileLink to="/settings" onClick={() => setMobileOpen(false)}>Settings</MobileLink>
                <div className="border-t border-space-border my-2" />
                <button onClick={handleLogout} className="block w-full text-left py-2 px-4 text-cyber-red font-medium">Logout</button>
              </>
            ) : (
              <>
                <MobileLink to="/login" onClick={() => setMobileOpen(false)}>Login</MobileLink>
                <MobileLink to="/register" onClick={() => setMobileOpen(false)} primary>Get Started Free</MobileLink>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

function NavLink({ to, children }) {
  return (
    <Link
      to={to}
      className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-400 hover:text-cyber-blue rounded-lg hover:bg-cyber-blue/5 transition-all duration-200"
    >
      {children}
    </Link>
  );
}

function DropdownLink({ to, children, onClick }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className="block px-4 py-2 text-sm text-gray-300 hover:bg-cyber-blue/5 hover:text-cyber-blue transition-colors"
    >
      {children}
    </Link>
  );
}

function MobileLink({ to, children, onClick, primary }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={`block py-2 px-4 font-medium rounded-lg transition-colors ${
        primary ? "text-cyber-blue" : "text-gray-400 hover:text-white hover:bg-cyber-blue/5"
      }`}
    >
      {children}
    </Link>
  );
}
