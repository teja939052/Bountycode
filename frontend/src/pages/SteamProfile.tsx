import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import api from "../services/api";

const LEVEL_XP_BASE = 500;

function xpProgress(xp) {
  const remainder = (xp || 0) % LEVEL_XP_BASE;
  return { pct: Math.min(100, Math.round((remainder / LEVEL_XP_BASE) * 100)), current: remainder };
}

function badgeLabel(badge) {
  if (typeof badge === "string") return badge;
  return badge?.name || badge?.id || "Badge";
}

function Card({ children, className = "" }) {
  return (
    <div className={`bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-sm ${className}`}>
      {children}
    </div>
  );
}

function SectionTitle({ children }) {
  return (
    <h2 className="text-sm font-semibold uppercase tracking-widest text-nature-blossom mb-4">
      {children}
    </h2>
  );
}

function StatPill({ label, value, accent = "text-gray-400" }: any) {
  return (
    <div className="bg-surface-card rounded-xl p-4 text-center">
      <div className={`text-2xl font-bold ${accent || "text-emerald-400"}`}>{value}</div>
      <div className="text-xs text-text-muted uppercase tracking-wide mt-1">{label}</div>
    </div>
  );
}

function Empty({ children }) {
  return <div className="text-text-muted text-sm py-4 text-center">{children}</div>;
}

export default function SteamProfile() {
  const [searchParams] = useSearchParams();
  const queryUser = searchParams.get("user") || "";
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    const load = async () => {
      try {
        const data = queryUser
          ? await api.steam.getPublic(queryUser)
          : await api.steam.get();
        if (active) setProfile(data);
      } catch (e) {
        if (active) setError(e.message || "Could not load this profile");
      } finally {
        if (active) setLoading(false);
      }
    };
    load();
    return () => {
      active = false;
    };
  }, [queryUser]);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center">
        <div className="text-text-muted animate-pulse">Loading profile...</div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center">
        <div className="text-center">
          <div className="text-3xl mb-3">🎮</div>
          <div className="text-text-secondary mb-2">{error || "Profile not found"}</div>
          <Link to="/profile/steam" className="text-nature-blossom hover:underline">
            Back to my profile
          </Link>
        </div>
      </div>
    );
  }

  const { user, gamification, stats, guild, showcase, recent_activity: recentActivity, collection } = profile;
  const { pct, current } = xpProgress(gamification.xp);
  const maxActivity = Math.max(1, ...recentActivity.map((d) => d.count));
  const badges = Array.isArray(gamification.badges) ? gamification.badges : [];

  return (
    <div className="min-h-screen bg-surface-base text-text-primary pb-16">
      <div className="max-w-3xl mx-auto px-4 py-8 space-y-5">
        {queryUser && (
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-muted">Viewing public profile</span>
            <Link to="/profile/steam" className="text-sm text-nature-blossom hover:underline">
              Back to my profile
            </Link>
          </div>
        )}

        {/* Header — Steam-style card */}
        <Card className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-[#EDF5E6] via-transparent to-[#F3F0E8] pointer-events-none" />
          <div className="relative flex items-center gap-4">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-[#4F8F57] to-[#7BB661] flex items-center justify-center text-4xl font-black text-white shadow-lg">
              {user.name ? user.name[0].toUpperCase() : "?"}
            </div>
            <div className="flex-1 min-w-0">
              <h1 className="text-2xl md:text-3xl font-extrabold truncate">{user.name || "Player"}</h1>
              <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-sm text-text-muted">
                {user.college && <span>🏛️ {user.college}</span>}
                <span className="inline-flex items-center gap-1 text-amber-500 font-bold">
                  Lv {gamification.level}
                </span>
                {gamification.titles && gamification.titles.length > 0 && (
                  <span className="text-nature-blossom">{gamification.titles[0]}</span>
                )}
              </div>
              {user.created_at && (
                <div className="text-xs text-text-muted mt-1">Joined {user.created_at}</div>
              )}
            </div>
          </div>
        </Card>

        {/* Level & XP bar */}
        <Card>
          <SectionTitle>Level & XP</SectionTitle>
          <div className="flex items-center justify-between text-sm mb-2">
            <span className="text-text-secondary font-semibold">Level {gamification.level}</span>
            <span className="text-nature-blossom font-semibold">{gamification.xp.toLocaleString()} XP</span>
          </div>
          <div className="h-3 bg-[#E5E0D3] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661] transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="text-xs text-text-muted mt-1">
            {current}/{LEVEL_XP_BASE} XP to next level
          </div>
        </Card>

        {/* Streak */}
        <Card>
          <SectionTitle>Streak</SectionTitle>
          <div className="flex items-center gap-3">
            <span className="text-3xl">🔥</span>
            <span className="text-2xl font-bold text-nature-blossom">{gamification.streak}</span>
            <span className="text-sm text-text-muted">day{gamification.streak === 1 ? "" : "s"} in a row</span>
          </div>
        </Card>

        {/* Trophies / Badges */}
        <Card>
          <SectionTitle>Trophies & Badges</SectionTitle>
          {badges.length === 0 ? (
            <Empty>No badges earned yet — keep practicing!</Empty>
          ) : (
            <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
              {badges.slice(0, 15).map((b, i) => (
                <div
                  key={i}
                  title={badgeLabel(b)}
                  className="flex flex-col items-center gap-1 bg-surface-card rounded-xl py-3 px-2"
                >
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-amber-400 to-yellow-600 flex items-center justify-center text-lg shadow">
                    🏆
                  </div>
                  <div className="text-[10px] text-text-secondary text-center leading-tight line-clamp-2">
                    {badgeLabel(b)}
                  </div>
                </div>
              ))}
              {badges.length > 15 && (
                <div className="flex items-center justify-center text-xs text-text-muted">
                  +{badges.length - 15} more
                </div>
              )}
            </div>
          )}
        </Card>

        {/* Collections & Inventory */}
        <Card>
          <SectionTitle>Collections & Inventory</SectionTitle>
          <div className="grid grid-cols-2 gap-4">
            <StatPill label="Items Owned" value={collection.count} />
            <StatPill label="Titles Unlocked" value={gamification.titles ? gamification.titles.length : 0} />
          </div>
        </Card>

        {/* Guild */}
        <Card>
          <SectionTitle>Guild</SectionTitle>
          {!guild ? (
            <Empty>Not in a guild yet</Empty>
          ) : (
            <div className="flex items-center justify-between">
              <div>
                <div className="text-lg font-bold">{guild.name}</div>
                <div className="text-sm text-text-muted mt-1">
                  {guild.title} · {guild.member_count} members · {guild.my_role}
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-nature-blossom">{guild.level}</div>
                <div className="text-xs text-text-muted uppercase">Lv</div>
              </div>
            </div>
          )}
        </Card>

        {/* Journey stats */}
        <Card>
          <SectionTitle>Journey Stats</SectionTitle>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <StatPill label="Problems" value={stats.problems} accent="text-sky-400" />
            <StatPill label="Interviews" value={stats.interviews} accent="text-violet-400" />
            <StatPill label="Battles" value={stats.battles} accent="text-rose-400" />
            <StatPill label="Offers" value={stats.offers} accent="text-amber-400" />
          </div>
        </Card>

        {/* Showcase */}
        <Card>
          <SectionTitle>Showcase Projects</SectionTitle>
          {showcase.length === 0 ? (
            <Empty>No showcased projects</Empty>
          ) : (
            <div className="space-y-3">
              {showcase.map((p) => (
                <Link
                  key={p.id}
                  to={`/showcase/${p.id}`}
                  className="flex items-center justify-between bg-surface-card rounded-xl px-4 py-3 hover:bg-[#EDEAE0] transition-colors"
                >
                  <div>
                    <div className="font-semibold">{p.title}</div>
                    <div className="text-xs text-text-muted mt-0.5">{p.language}</div>
                  </div>
                  <div className="text-right text-xs text-text-muted">
                    <div>❤️ {p.likes}</div>
                    <div>👁️ {p.views}</div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </Card>

        {/* Recent activity bar chart */}
        <Card>
          <SectionTitle>Recent Activity</SectionTitle>
          {recentActivity.length === 0 ? (
            <Empty>No activity yet this week</Empty>
          ) : (
            <>
              <div className="flex items-end gap-2 h-24">
                {recentActivity.map((d, i) => (
                  <div key={d.date} className="flex-1 flex flex-col items-center gap-1">
                    <div className="w-full flex items-end" style={{ height: "72px" }}>
                      <div
                        className="w-full bg-gradient-to-t from-[#3F7A47] to-[#7BB661] rounded-t-md"
                        style={{
                          height: `${d.count === 0 ? 4 : Math.max(10, (d.count / maxActivity) * 100)}%`,
                        }}
                      />
                    </div>
                    <div className="text-[10px] text-text-muted">
                      {new Date(d.date + "T00:00:00").toLocaleDateString(undefined, { weekday: "narrow" })}
                    </div>
                    <div className="text-[10px] text-text-muted">{d.count}</div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between text-[10px] text-text-muted mt-1">
                <span>{recentActivity[0]?.date}</span>
                <span>{recentActivity[recentActivity.length - 1]?.date}</span>
              </div>
            </>
          )}
        </Card>
      </div>
    </div>
  );
}
