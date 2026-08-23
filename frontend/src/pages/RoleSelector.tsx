import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Code2, Database, BarChart3, Bug, Server, Shield, Star, ArrowRight, MapPin } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";

type RoleTone = "primary" | "tech" | "rare" | "gold" | "ocean" | "coral";

interface RoleOption {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  icon: React.ReactNode;
  skills: string[];
  duration: string;
  assessments: number;
  tone: RoleTone;
}

const ROLES: RoleOption[] = [
  {
    id: "software-engineer",
    title: "Software Engineer",
    subtitle: "Build · Code · Systems · Scale",
    description:
      "Master the art of building scalable software systems. From algorithms to architecture, become a complete engineer.",
    icon: <Code2 size={28} />,
    skills: ["Data Structures & Algorithms", "System Design", "Databases", "APIs & Microservices"],
    duration: "26-week learning path",
    assessments: 120,
    tone: "primary",
  },
  {
    id: "data-analyst",
    title: "Data Analyst",
    subtitle: "Query · Visualize · Insight · Decide",
    description:
      "Transform raw data into actionable business insights. Master SQL, visualization, and statistical thinking.",
    icon: <Database size={28} />,
    skills: ["SQL & Databases", "Data Visualization", "Statistics & Probability", "Python for Data"],
    duration: "16-week learning path",
    assessments: 80,
    tone: "tech",
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    subtitle: "Model · Predict · Experiment · Deploy",
    description:
      "Build machine learning models that solve real problems. From experimentation to production ML systems.",
    icon: <BarChart3 size={28} />,
    skills: ["Machine Learning", "Deep Learning", "Statistics", "Model Deployment"],
    duration: "24-week learning path",
    assessments: 100,
    tone: "rare",
  },
  {
    id: "qa-engineer",
    title: "QA Engineer",
    subtitle: "Test · Automate · Quality · Ship",
    description:
      "Ensure software quality at scale. Master test automation, performance testing, and quality processes.",
    icon: <Bug size={28} />,
    skills: ["Test Automation", "API Testing", "Performance Testing", "Test Strategy"],
    duration: "14-week learning path",
    assessments: 70,
    tone: "gold",
  },
  {
    id: "devops-engineer",
    title: "DevOps Engineer",
    subtitle: "Infrastructure · Scale · Reliability · Automate",
    description:
      "Build and maintain the infrastructure that powers modern applications. Cloud, containers, and automation.",
    icon: <Server size={28} />,
    skills: ["Cloud Platforms", "Kubernetes", "CI/CD Pipelines", "Infrastructure as Code"],
    duration: "20-week learning path",
    assessments: 90,
    tone: "ocean",
  },
  {
    id: "security-engineer",
    title: "Security Engineer",
    subtitle: "Protect · Audit · Harden · Respond",
    description:
      "Secure applications and infrastructure. Application security, cloud security, and incident response.",
    icon: <Shield size={28} />,
    skills: ["Application Security", "Cloud Security", "Penetration Testing", "Incident Response"],
    duration: "18-week learning path",
    assessments: 85,
    tone: "coral",
  },
] as const;

const TONE_ICON_BG: Record<RoleTone, string> = {
  primary: "bg-primary-soft text-primary-dark",
  tech: "bg-tech-soft text-tech",
  rare: "bg-rare-soft text-rare",
  gold: "bg-reward-soft text-wood",
  ocean: "bg-ocean-soft text-ocean",
  coral: "bg-coral-soft text-coral",
};

const TONE_SKILL_CHIP: Record<RoleTone, string> = {
  primary: "bg-primary-soft text-primary-dark",
  tech: "bg-tech-soft text-tech",
  rare: "bg-rare-soft text-rare",
  gold: "bg-reward-soft text-wood",
  ocean: "bg-ocean-soft text-ocean",
  coral: "bg-coral-soft text-coral",
};

export default function RoleSelector() {
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const handleSelectRole = (roleId: string) => {
    // Store selected role and navigate to onboarding
    localStorage.setItem("selectedRole", roleId);
    navigate("/onboarding");
  };

  return (
    <PageShell theme="adventure">
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center"
        >
          <div className="mb-6 inline-flex items-center gap-1.5 rounded-full bg-surface px-4 py-1.5 shadow-card">
            <MapPin size={14} className="text-ocean" />
            <span className="text-xs font-bold uppercase tracking-wider text-text-muted">Choose your destination</span>
          </div>
          <h1 className="font-display mx-auto max-w-3xl text-3xl font-extrabold tracking-tight text-text sm:text-4xl lg:text-5xl">
            Which port are you sailing to?
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-text-muted sm:text-lg">
            We'll chart your preparation world around your target role. Every lesson, challenge,
            and assessment will be tailored to your route.
          </p>
        </motion.div>

        {/* Destination cards */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3"
        >
          {ROLES.map((role, index) => (
            <motion.div
              key={role.id}
              initial={reduced ? {} : { opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: reduced ? 0 : 0.15 + index * 0.08, duration: 0.4 }}
            >
              <Card interactive className="flex h-full flex-col">
                <div className="mb-4 flex items-center gap-4">
                  <div className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-xl ${TONE_ICON_BG[role.tone]}`}>
                    {role.icon}
                  </div>
                  <div className="min-w-0">
                    <h3 className="font-display truncate text-lg font-extrabold text-text">{role.title}</h3>
                    <p className="truncate text-xs font-semibold text-text-muted">{role.subtitle}</p>
                  </div>
                </div>

                <p className="mb-4 text-sm leading-relaxed text-text-muted">{role.description}</p>

                <div className="mb-4">
                  <h4 className="adventure-label mb-2">Route skills</h4>
                  <div className="flex flex-wrap gap-2">
                    {role.skills.slice(0, 3).map((skill) => (
                      <span
                        key={skill}
                        className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${TONE_SKILL_CHIP[role.tone]}`}
                      >
                        {skill}
                      </span>
                    ))}
                    <span className="rounded-full bg-surface-2 px-2.5 py-1 text-[11px] font-semibold text-text-muted">
                      +{role.skills.length - 3} more
                    </span>
                  </div>
                </div>

                <div className="surface-border mb-5 flex items-center justify-between border-t pt-4 text-xs text-text-muted">
                  <span className="font-bold">{role.duration}</span>
                  <span className="flex items-center gap-1.5">
                    <Star size={13} className="text-reward" />
                    <span>{role.assessments}+ bounties</span>
                  </span>
                </div>

                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  className="mt-auto"
                  onClick={() => handleSelectRole(role.id)}
                  rightIcon={<ArrowRight size={16} />}
                >
                  Set course
                </Button>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom note */}
        <motion.p
          initial={reduced ? {} : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          className="mt-12 text-center text-sm text-text-muted"
        >
          Not sure yet?{" "}
          <Link to="/career-explorer" className="ml-1 font-bold text-primary-dark hover:text-primary hover:underline">
            Explore all careers
          </Link>
        </motion.p>
      </div>
    </PageShell>
  );
}
