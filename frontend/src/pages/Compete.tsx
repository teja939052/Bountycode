import SectionPage from "../components/SectionPage";
import { Swords, Trophy, Award, Castle, ListOrdered, CalendarCheck, TrendingUp, Package } from "lucide-react";

export default function Compete() {
  return (
    <SectionPage
      title="Compete"
      subtitle="Test yourself against others — battles, contests, and leaderboards."
      icon={Trophy}
      groups={[
        {
          label: "Compete",
          items: [
            { to: "/battles", label: "1v1 Battles", desc: "Real-time coding duels", icon: Swords },
            { to: "/contests", label: "Contests", desc: "Monthly competitive contests", icon: Trophy },
            { to: "/tournaments", label: "Tournaments", desc: "Bracketed competitions", icon: Award },
            { to: "/campus-wars", label: "Campus Wars", desc: "College vs college", icon: Castle },
          ],
        },
        {
          label: "Leaderboards & Challenges",
          items: [
            { to: "/leaderboard", label: "Leaderboard", desc: "Global rankings", icon: ListOrdered },
            { to: "/daily-challenge", label: "Daily Challenge", desc: "Adaptive daily mission", icon: CalendarCheck },
            { to: "/trending", label: "Trending", desc: "Hot challenges right now", icon: TrendingUp },
            { to: "/challenge-packs", label: "Challenge Packs", desc: "Themed pack leaderboards", icon: Package },
          ],
        },
      ]}
    />
  );
}
