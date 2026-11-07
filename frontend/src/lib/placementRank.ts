/** Placement ranks — evidence stage labels, not RPG titles. */
export type PlacementRank = {
  minLevel: number;
  title: string;
  blurb: string;
};

const BANDS: PlacementRank[] = [
  { minLevel: 1, title: "Beginner", blurb: "Building foundations" },
  { minLevel: 5, title: "Starter", blurb: "First skills under assessment" },
  { minLevel: 10, title: "Builder", blurb: "Core aptitude and coding habits" },
  { minLevel: 15, title: "Practitioner", blurb: "Consistent evidence across topics" },
  { minLevel: 25, title: "Contender", blurb: "Mock-ready for target companies" },
  { minLevel: 35, title: "Finalist", blurb: "Strong mock and interview signals" },
  { minLevel: 45, title: "Offer-Ready", blurb: "Readiness matches the hiring bar" },
  { minLevel: 60, title: "Mentor-Track", blurb: "Depth beyond the entry bar" },
  { minLevel: 80, title: "Placement Alumnus", blurb: "Sustained mastery record" },
  { minLevel: 100, title: "Campus Legend", blurb: "Top-tier evidence across domains" },
];

export function placementRank(level: number): PlacementRank {
  const n = Math.max(1, Math.floor(Number(level) || 1));
  let chosen = BANDS[0];
  for (const row of BANDS) {
    if (row.minLevel <= n) chosen = row;
    else break;
  }
  return chosen;
}
