import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import { Bot, FileText, Code, Brain, Layers, Calendar, BarChart3, ExternalLink } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";

const TABS = [
  { id: "interviews", label: "Interviews", icon: Bot, color: "blue" },
  { id: "resumes", label: "Resumes", icon: FileText, color: "green" },
  { id: "aptitude", label: "Aptitude", icon: Brain, color: "purple" },
  { id: "coding", label: "Coding", icon: Code, color: "emerald" },
  { id: "system_design", label: "System Design", icon: Layers, color: "indigo" },
];

export default function History() {
  const [activeTab, setActiveTab] = useState("interviews");
  const [data, setData] = useState({ interviews: [], resumes: [], tests: [], challenges: [], sessions: [] });
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const loadHistory = async () => {
      setLoading(true);
      try {
        const [interviews, resumes, aptitude, coding, systemDesign] = await Promise.all([
          api.get("/api/v1/interview/history").catch(() => ({ interviews: [] })),
          api.get("/api/v1/resume/history").catch(() => ({ resumes: [] })),
          api.get("/api/v1/aptitude/history").catch(() => ({ tests: [] })),
          api.get("/api/v1/coding/history").catch(() => ({ challenges: [] })),
          api.get("/api/v1/system-design/history").catch(() => ({ sessions: [] })),
        ]);
        setData({
          interviews: interviews.interviews || [],
          resumes: resumes.resumes || [],
          tests: aptitude.tests || [],
          challenges: coding.challenges || [],
          sessions: systemDesign.sessions || [],
        });
      } catch {} finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, []);

  const formatDate = (d) => new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyber-blue" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-3xl font-display font-black text-text-primary">Flight Log</h1>
            <p className="text-gray-500 font-mono text-sm mt-1">Track your progress across all practice sessions</p>
          </motion.div>
          <div className="flex items-center gap-2 text-sm text-gray-400 font-mono">
            <BarChart3 size={16} />
            {Object.values(data).flat().length} total sessions
          </div>
        </div>

        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {TABS.map((tab) => {
            const count = tab.id === "interviews" ? data.interviews.length
              : tab.id === "resumes" ? data.resumes.length
              : tab.id === "aptitude" ? data.tests.length
              : tab.id === "coding" ? data.challenges.length
              : data.sessions.length;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? "bg-cyber-blue text-space-void"
                    : "bg-space-panel border border-space-border text-gray-500 hover:bg-space-panel/80"
                }`}
              >
                <tab.icon size={16} />
                {tab.label}
                <span className={`text-xs px-1.5 py-0.5 rounded-full ${activeTab === tab.id ? "bg-cyber-blue/70" : "bg-space-panel"}`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {activeTab === "interviews" && (
          <StaggerContainer className="space-y-3">
            {data.interviews.length === 0 ? (
              <EmptyState icon={Bot} title="No interviews yet" link="/interview" linkText="Start your first interview" />
            ) : (
              data.interviews.map((item) => (
                <StaggerItem key={item._id || item.interview_id}>
                  <div className="card flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-cyber-blue/10 rounded-lg flex items-center justify-center">
                        <Bot size={20} className="text-cyber-blue" />
                      </div>
                      <div>
                        <p className="font-display font-bold text-text-primary">{item.job_role}</p>
                        <p className="text-gray-500 font-mono text-xs flex items-center gap-1">
                          <Calendar size={12} /> {formatDate(item.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <p className="text-text-primary font-display font-bold text-lg">{item.overall_score || "—"}/10</p>
                        <p className="text-xs text-gray-500">{item.questions_answered || 0} questions</p>
                      </div>
                      <Link to={`/interview/${item._id || item.interview_id}`} className="text-cyber-blue hover:text-cyber-blue/80">
                        <ExternalLink size={18} />
                      </Link>
                    </div>
                  </div>
                </StaggerItem>
              ))
            )}
          </StaggerContainer>
        )}

        {activeTab === "resumes" && (
          <StaggerContainer className="space-y-3">
            {data.resumes.length === 0 ? (
              <EmptyState icon={FileText} title="No resumes yet" link="/resume" linkText="Build your first resume" />
            ) : (
              data.resumes.map((item) => (
                <StaggerItem key={item._id || item.resume_id}>
                  <div className="card flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-cyber-green/10 rounded-lg flex items-center justify-center">
                        <FileText size={20} className="text-cyber-green" />
                      </div>
                      <div>
                        <p className="font-display font-bold text-text-primary">{item.target_role || "Resume"}</p>
                        <p className="text-gray-500 font-mono text-xs flex items-center gap-1">
                          <Calendar size={12} /> {formatDate(item.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      {item.ats_score && (
                        <div className="text-right">
                          <p className="font-bold text-lg text-text-primary">{item.ats_score}%</p>
                          <p className="text-xs text-gray-500">ATS Score</p>
                        </div>
                      )}
                      <Link to="/resume" className="text-cyber-blue hover:text-cyber-blue/80">
                        <ExternalLink size={18} />
                      </Link>
                    </div>
                  </div>
                </StaggerItem>
              ))
            )}
          </StaggerContainer>
        )}

        {activeTab === "aptitude" && (
          <StaggerContainer className="space-y-3">
            {data.tests.length === 0 ? (
              <EmptyState icon={Brain} title="No aptitude tests yet" link="/aptitude" linkText="Take your first test" />
            ) : (
              data.tests.map((item) => (
                <StaggerItem key={item._id || item.test_id}>
                  <div className="card flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-cyber-purple/10 rounded-lg flex items-center justify-center">
                        <Brain size={20} className="text-cyber-purple" />
                      </div>
                      <div>
                        <p className="font-display font-bold capitalize text-text-primary">{item.category} — {item.difficulty}</p>
                        <p className="text-gray-500 font-mono text-xs flex items-center gap-1">
                          <Calendar size={12} /> {formatDate(item.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-text-primary font-display font-bold text-lg">{item.percentage || item.score || "—"}%</p>
                      <p className="text-xs text-gray-500">{item.correct || 0}/{item.total || 10} correct</p>
                    </div>
                  </div>
                </StaggerItem>
              ))
            )}
          </StaggerContainer>
        )}

        {activeTab === "coding" && (
          <StaggerContainer className="space-y-3">
            {data.challenges.length === 0 ? (
              <EmptyState icon={Code} title="No coding challenges yet" link="/coding" linkText="Solve your first challenge" />
            ) : (
              data.challenges.map((item) => (
                <StaggerItem key={item._id || item.challenge_id}>
                  <div className="card flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-cyber-orange/10 rounded-lg flex items-center justify-center">
                        <Code size={20} className="text-cyber-orange" />
                      </div>
                      <div>
                        <p className="font-display font-bold text-text-primary">{item.title || "Coding Challenge"}</p>
                        <p className="text-gray-500 font-mono text-xs flex items-center gap-1">
                          <Calendar size={12} /> {formatDate(item.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                        item.status === "solved"
                          ? "bg-cyber-green/10 text-cyber-green border border-cyber-green/20"
                          : "bg-cyber-yellow/10 text-cyber-yellow border border-cyber-yellow/20"
                      }`}>
                        {item.status || "attempted"}
                      </span>
                      <Link to="/coding" className="text-cyber-blue hover:text-cyber-blue/80">
                        <ExternalLink size={18} />
                      </Link>
                    </div>
                  </div>
                </StaggerItem>
              ))
            )}
          </StaggerContainer>
        )}

        {activeTab === "system_design" && (
          <StaggerContainer className="space-y-3">
            {data.sessions.length === 0 ? (
              <EmptyState icon={Layers} title="No system design sessions yet" link="/system-design" linkText="Start designing" />
            ) : (
              data.sessions.map((item) => (
                <StaggerItem key={item._id || item.session_id}>
                  <div className="card flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-cyber-yellow/10 rounded-lg flex items-center justify-center">
                        <Layers size={20} className="text-cyber-yellow" />
                      </div>
                      <div>
                        <p className="font-display font-bold text-text-primary">{item.topic || "System Design"}</p>
                        <p className="text-gray-500 font-mono text-xs flex items-center gap-1">
                          <Calendar size={12} /> {formatDate(item.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-text-primary font-display font-bold text-lg">{item.overall_score || "—"}/10</p>
                    </div>
                  </div>
                </StaggerItem>
              ))
            )}
          </StaggerContainer>
        )}
      </div>
    </div>
  );
}

function EmptyState({ icon: Icon, title, link, linkText }) {
  return (
    <div className="card text-center py-12">
      <Icon size={48} className="mx-auto text-gray-600 mb-4" />
      <p className="text-gray-500 font-mono mb-4">{title}</p>
      <Link to={link} className="text-cyber-blue font-semibold hover:text-cyber-blue/80">
        {linkText} →
      </Link>
    </div>
  );
}
