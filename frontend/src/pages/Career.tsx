import SectionPage from "../components/SectionPage";
import { UserCircle, FileText, Search, Mail, Briefcase, MapPin, Users, Calendar, BarChart3, Handshake } from "lucide-react";

export default function Career() {
  return (
    <SectionPage
      title="Career"
      subtitle="Everything for the job hunt — your profile, applications, and offers."
      icon={Briefcase}
      groups={[
        {
          label: "Build Your Profile",
          items: [
            { to: "/career-profile", label: "Career Profile", desc: "Skills, experience, portfolio", icon: UserCircle },
            { to: "/resume", label: "Resume Builder", desc: "Generate or upload a resume", icon: FileText },
            { to: "/ats", label: "ATS Optimizer", desc: "Match resume to job descriptions", icon: Search },
            { to: "/cover-letter", label: "Cover Letter", desc: "AI cover letter & LinkedIn", icon: Mail },
          ],
        },
        {
          label: "Opportunities",
          items: [
            { to: "/applications", label: "Applications", desc: "Track job applications", icon: Briefcase },
            { to: "/placement-drives", label: "Placement Drives", desc: "Upcoming campus drives", icon: MapPin },
            { to: "/alumni-experiences", label: "Alumni Experiences", desc: "Peer interview insights", icon: Users },
            { to: "/interview-booking", label: "Interview Booking", desc: "Schedule mock interviews", icon: Calendar },
          ],
        },
        {
          label: "Salary",
          items: [
            { to: "/salary-benchmark", label: "Salary Benchmark", desc: "Market rate data", icon: BarChart3 },
            { to: "/salary-negotiation", label: "Salary Negotiation", desc: "AI negotiation coaching", icon: Handshake },
          ],
        },
      ]}
    />
  );
}
