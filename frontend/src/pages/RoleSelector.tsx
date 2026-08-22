import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button, Card } from "../design-system/components";
import { Code2, Database, BarChart3, Bug, Server, Shield, Star, ArrowRight } from "lucide-react";

interface RoleOption {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  icon: React.ReactNode;
  skills: string[];
  duration: string;
  assessments: number;
  color: string;
  gradient: string;
}

const ROLES: RoleOption[] = [
  {
    id: "software-engineer",
    title: "Software Engineer",
    subtitle: "Build · Code · Systems · Scale",
    description: "Master the art of building scalable software systems. From algorithms to architecture, become a complete engineer.",
    icon: <Code2 size={32} />,
    skills: ["Data Structures & Algorithms", "System Design", "Databases", "APIs & Microservices", "Testing & DevOps", "Frontend & Backend"],
    duration: "26-week learning path",
    assessments: 120,
    color: "#16A34A",
    gradient: "from-emerald-500 to-teal-600",
  },
  {
    id: "data-analyst",
    title: "Data Analyst",
    subtitle: "Query · Visualize · Insight · Decide",
    description: "Transform raw data into actionable business insights. Master SQL, visualization, and statistical thinking.",
    icon: <Database size={32} />,
    skills: ["SQL & Databases", "Data Visualization", "Statistics & Probability", "Excel & Spreadsheets", "Python for Data", "Business Intelligence"],
    duration: "16-week learning path",
    assessments: 80,
    color: "#3B82F6",
    gradient: "from-blue-500 to-cyan-600",
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    subtitle: "Model · Predict · Experiment · Deploy",
    description: "Build machine learning models that solve real problems. From experimentation to production ML systems.",
    icon: <BarChart3 size={32} />,
    skills: ["Machine Learning", "Deep Learning", "Statistics", "MLOps", "Feature Engineering", "Model Deployment"],
    duration: "24-week learning path",
    assessments: 100,
    color: "#8B5CF6",
    gradient: "from-purple-500 to-indigo-600",
  },
  {
    id: "qa-engineer",
    title: "QA Engineer",
    subtitle: "Test · Automate · Quality · Ship",
    description: "Ensure software quality at scale. Master test automation, performance testing, and quality processes.",
    icon: <Bug size={32} />,
    skills: ["Test Automation", "API Testing", "Performance Testing", "CI/CD Integration", "Test Strategy", "Bug Advocacy"],
    duration: "14-week learning path",
    assessments: 70,
    color: "#F59E0B",
    gradient: "from-amber-500 to-orange-600",
  },
  {
    id: "devops-engineer",
    title: "DevOps Engineer",
    subtitle: "Infrastructure · Scale · Reliability · Automate",
    description: "Build and maintain the infrastructure that powers modern applications. Cloud, containers, and automation.",
    icon: <Server size={32} />,
    skills: ["Cloud Platforms", "Kubernetes", "CI/CD Pipelines", "Infrastructure as Code", "Monitoring", "Security"],
    duration: "20-week learning path",
    assessments: 90,
    color: "#EF6A5B",
    gradient: "from-red-500 to-rose-600",
  },
  {
    id: "security-engineer",
    title: "Security Engineer",
    subtitle: "Protect · Audit · Harden · Respond",
    description: "Secure applications and infrastructure. Application security, cloud security, and incident response.",
    icon: <Shield size={32} />,
    skills: ["Application Security", "Cloud Security", "Penetration Testing", "Compliance", "Incident Response", "Threat Modeling"],
    duration: "18-week learning path",
    assessments: 85,
    color: "#EC4899",
    gradient: "from-pink-500 to-rose-600",
  },
];

export default function RoleSelector() {
  const navigate = useNavigate();

  const handleSelectRole = (roleId: string) => {
    // Store selected role and navigate to onboarding
    localStorage.setItem("selectedRole", roleId);
    navigate("/onboarding");
  };

  return (
    <div className="min-h-screen bg-background-primary">
      {/* Subtle ambient background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-8 w-40 h-40 rounded-full bg-brand-mint/30 blur-3xl" />
        <div className="absolute bottom-20 right-8 w-32 h-32 rounded-full bg-brand-mint/20 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-mint/50 text-brand-primary text-sm font-mono uppercase tracking-wider mb-6">
            <span>Step 1 of 4</span>
          </div>
          <h1 className="font-display text-4xl font-extrabold tracking-tight text-text-primary sm:text-5xl lg:text-6xl mb-4">
            What career are you building?
          </h1>
          <p className="text-lg text-text-secondary max-w-2xl mx-auto leading-relaxed">
            We'll create your preparation world around your target role.
            Every lesson, challenge, and assessment will be tailored to your path.
          </p>
        </motion.div>

        {/* Role Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {ROLES.map((role, index) => (
            <motion.div
              key={role.id}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 + index * 0.08, duration: 0.4 }}
            >
              <Card
                variant="outlined"
                padding="lg"
                hover
                className="h-full flex flex-col"
                style={{
                  borderColor: `${role.color}40`,
                  background: `linear-gradient(135deg, ${role.color}08 0%, transparent 100%)`,
                }}
              >
                <div className="mb-4">
                  <div
                    className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4"
                    style={{ background: `linear-gradient(135deg, ${role.color}20 0%, ${role.color}10 100%)` }}
                  >
                    <span style={{ color: role.color }}>{role.icon}</span>
                  </div>
                  <div className="text-center">
                    <h3 className="font-display text-2xl font-bold text-text-primary mb-1">{role.title}</h3>
                    <p className="text-sm text-text-secondary font-medium">{role.subtitle}</p>
                  </div>
                </div>

                <p className="text-text-secondary text-sm mb-5 leading-relaxed text-center">
                  {role.description}
                </p>

                <div className="mb-5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-text-secondary mb-3">Core skills</h4>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {role.skills.slice(0, 4).map((skill, i) => (
                      <span
                        key={skill}
                        className="px-2.5 py-1 text-xs font-medium rounded-full"
                        style={{
                          background: `${role.color}15`,
                          color: role.color,
                        }}
                      >
                        {skill}
                      </span>
                    ))}
                    {role.skills.length > 4 && (
                      <span className="px-2.5 py-1 text-xs font-medium rounded-full bg-background-secondary text-text-secondary">
                        +{role.skills.length - 4} more
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-center gap-6 text-sm text-text-secondary mb-6 border-t border-border-primary pt-4">
                  <div className="flex items-center gap-1.5">
                    <span className="w-4 h-4 rounded-full" style={{ background: role.color }} />
                    <span className="font-mono">{role.duration}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Star size={14} className="text-xp" />
                    <span className="font-mono">{role.assessments}+ assessments</span>
                  </div>
                </div>

                <Button
                  size="lg"
                  fullWidth
                  className="mt-auto"
                  style={{
                    background: `linear-gradient(135deg, ${role.color} 0%, ${role.color}dd 100%)`,
                  }}
                  onClick={() => handleSelectRole(role.id)}
                  rightIcon={<ArrowRight size={16} />}
                >
                  Enter Journey →
                </Button>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom note */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          className="mt-12 text-center text-sm text-text-secondary"
        >
          Not sure yet? <Link to="/career-explorer" className="text-brand-primary font-semibold hover:underline ml-1">Explore all careers</Link>
        </motion.p>
      </div>
    </div>
  );
}