import SectionPage from "../components/SectionPage";
import { Code2, ListChecks, Hash, Dumbbell, Package, FileCode, Video, Terminal, PlaySquare } from "lucide-react";

export default function Practice() {
  return (
    <SectionPage
      title="Practice"
      subtitle="Your core loop — solve, simulate, and ship real interview performance."
      icon={Code2}
      groups={[
        {
          label: "Simulations",
          items: [
            { to: "/mock-oa", label: "Mock OA", desc: "Timed online assessment simulator", icon: FileCode },
            { to: "/interview-booking", label: "Mock Interview", desc: "Live 1:1 mock interview", icon: Video },
            { to: "/company-mocks", label: "Company Mocks", desc: "Company-specific test series", icon: Package },
          ],
        },
        {
          label: "Practice",
          items: [
            { to: "/coding", label: "Coding", desc: "Timed coding challenges", icon: Code2 },
            { to: "/question-bank", label: "Question Bank", desc: "100+ curated problems", icon: ListChecks },
            { to: "/problems", label: "Topics", desc: "Practice by topic", icon: Hash },
            { to: "/daily-drill", label: "Daily Drill", desc: "Quick daily warm-up", icon: Dumbbell },
            { to: "/challenge-packs", label: "Challenge Packs", desc: "Curated problem packs", icon: Package },
          ],
        },
        {
          label: "Code",
          items: [
            { to: "/compiler", label: "Compiler", desc: "Run code in 15+ languages", icon: Terminal },
            { to: "/playground", label: "Playground", desc: "Experiment freely", icon: PlaySquare },
          ],
        },
      ]}
    />
  );
}
