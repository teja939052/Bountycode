import SectionPage from "../components/SectionPage";
import {
  Code2, Database, Calculator, Brain, BookOpen, Server,
  Mic, Network, Bug,
} from "lucide-react";

// V3 §6 — Practice is unordered & always accessible. Same patterns the
// Journey orders; student picks any. All links reuse existing engines.
export default function Practice() {
  return (
    <SectionPage
      title="Practice by category"
      subtitle="Unordered. Pick any pattern — the Journey orders this for you when you're ready."
      icon={Code2}
      groups={[
        {
          label: "💻 Coding (40 patterns)",
          items: [
            { to: "/problems?topic=two-pointers", label: "Two Pointers", desc: "Paired scan from both ends", icon: Code2 },
            { to: "/problems?topic=sliding-window", label: "Sliding Window", desc: "Variable window over arrays/strings", icon: Code2 },
            { to: "/problems?topic=hashing", label: "Hash Lookup", desc: "O(1) membership & frequency", icon: Code2 },
            { to: "/problems?topic=binary-search", label: "Binary Search", desc: "Sorted-array divide & conquer", icon: Code2 },
            { to: "/question-bank", label: "All coding problems", desc: "100+ curated, TRUSTED only", icon: Code2 },
          ],
        },
        {
          label: "📊 Aptitude (20 patterns)",
          items: [
            { to: "/aptitude?topic=percentages", label: "Percentages", desc: "Successive change, ratios", icon: Calculator },
            { to: "/aptitude?topic=profit-loss", label: "Profit / Loss", desc: "Transformation drills", icon: Calculator },
            { to: "/aptitude", label: "All aptitude", desc: "Timed aptitude tests", icon: Calculator },
          ],
        },
        {
          label: "🧠 Reasoning (20 patterns)",
          items: [
            { to: "/aptitude?topic=reasoning", label: "Syllogism · Blood Relations", desc: "Set logic & relation graphs", icon: Brain },
            { to: "/aptitude?topic=coding-decoding", label: "Coding-Decoding", desc: "Transformation rules", icon: Brain },
          ],
        },
        {
          label: "📚 Verbal (15 patterns)",
          items: [
            { to: "/aptitude?topic=verbal", label: "Grammar · RC · Para Jumbles", desc: "Agreement, main idea, order", icon: BookOpen },
          ],
        },
        {
          label: "🗄 SQL (10 patterns)",
          items: [
            { to: "/problems?topic=sql", label: "SELECT → JOINs → GROUP BY", desc: "Subqueries, indexes", icon: Database },
          ],
        },
        {
          label: "🖥 CS Fundamentals (15 patterns)",
          items: [
            { to: "/concepts?topic=os", label: "OS · DBMS · Networks · OOP", desc: "Processes, normalization, OSI", icon: Server },
          ],
        },
        {
          label: "🎤 Interview (10 patterns)",
          items: [
            { to: "/interview", label: "AI Interview", desc: "Technical · Behavioral · HR", icon: Mic },
            { to: "/system-design", label: "System Design", desc: "Architecture & trade-offs", icon: Network },
          ],
        },
        {
          label: "🐞 Debugging",
          items: [
            { to: "/compiler", label: "Compiler / Playground", desc: "Run & break code freely", icon: Bug },
          ],
        },
      ]}
    />
  );
}
