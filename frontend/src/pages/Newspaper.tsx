import { useState, useEffect, useCallback } from "react";
import { newspaperApi } from "../services/api/newspaper.ts";

const SECTION_TITLES = {
  battles: "Battle Reports",
  guilds: "Guild Chronicle",
  campus: "Campus Wars",
  achievements: "Hall of Achievements",
  boss: "Daily Boss",
  merchant: "Market Square",
};

export default function Newspaper() {
  const [paper, setPaper] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await newspaperApi.today();
      setPaper(data);
    } catch (e) {
      setPaper(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const refresh = async () => {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  };

  const sectionCard = (key, content) => (
    <div className="bg-white border border-nature-leaf/20 rounded-xl p-5">
      <h3 className="text-sm font-bold text-amber-400 uppercase tracking-widest mb-3">
        {SECTION_TITLES[key] || key}
      </h3>
      {content}
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center">
        <div className="text-text-muted animate-pulse">Printing today's edition...</div>
      </div>
    );
  }

  if (!paper) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary flex items-center justify-center flex-col gap-4">
        <p className="text-text-muted">The press is silent today.</p>
        <button onClick={load} className="px-4 py-2 bg-emerald-600 text-text-primary rounded-lg">Retry</button>
      </div>
    );
  }

  const s = paper.sections || {};

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-2">
          <div className="text-xs text-text-muted uppercase tracking-widest">The Daily Chronicle of the Realm</div>
          <div className="text-xs text-text-muted">Edition {paper.edition}</div>
        </div>

        <div className="text-center border-y-4 border-double border-amber-700/60 py-6 mb-8">
          <h1 className="text-4xl md:text-5xl font-serif font-black tracking-tight">PLACEMENT TIMES</h1>
          <div className="text-text-muted text-sm mt-2">{paper.date}</div>
        </div>

        <div className="bg-white border border-nature-leaf/20 rounded-2xl p-6 mb-6">
          <div className="text-xs text-nature-blossom uppercase tracking-widest mb-2">Headline</div>
          <h2 className="text-2xl md:text-3xl font-bold">{paper.headline.title}</h2>
          <p className="text-text-muted mt-2">{paper.headline.subtitle}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {s.battles?.present && (
            sectionCard("battles", (
              <div className="space-y-2">
                {s.battles.items.map((b) => (
                  <div key={b.id} className="flex items-center justify-between text-sm">
                    <div className="text-text-secondary">
                      <span className="font-semibold">{b.player1}</span>
                      <span className="text-text-muted mx-2">{b.score1 ?? 0} - {b.score2 ?? 0}</span>
                      <span className="font-semibold">{b.player2}</span>
                    </div>
                    <div className="text-nature-blossom text-xs">{b.winner ? `${b.winner} wins` : "draw"}</div>
                  </div>
                ))}
              </div>
            ))
          )}

          {s.guilds?.present && (
            sectionCard("guilds", (
              <div className="space-y-2">
                {s.guilds.top.map((g) => (
                  <div key={g.name} className="flex items-center justify-between text-sm">
                    <span className="font-semibold">{g.name}</span>
                    <span className="text-text-muted">{g.members} members · {g.xp.toLocaleString()} XP</span>
                  </div>
                ))}
                {s.guilds.war && (
                  <div className="mt-3 bg-amber-900/30 rounded-lg p-3 text-sm">
                    <span className="font-bold text-amber-700">{s.guilds.war.headline}</span>
                  </div>
                )}
              </div>
            ))
          )}

          {s.campus?.present && (
            sectionCard("campus", (
              <div className="space-y-2">
                {s.campus.items.map((c) => (
                  <div key={c.college} className="flex items-center justify-between text-sm">
                    <span className="font-semibold">
                      <span className="text-text-muted mr-2">#{c.rank}</span>{c.college}
                    </span>
                    <span className="text-nature-blossom">{c.points.toLocaleString()} pts</span>
                  </div>
                ))}
              </div>
            ))
          )}

          {s.achievements?.present && (
            sectionCard("achievements", (
              <div className="space-y-2">
                {s.achievements.items.map((a, i) => (
                  <div key={i} className="flex items-center justify-between text-sm">
                    <span className="font-semibold">{a.name}</span>
                    <span className="text-amber-600">{a.badge}</span>
                  </div>
                ))}
              </div>
            ))
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {s.boss?.present && (
            sectionCard("boss", (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold">{s.boss.name}</span>
                  <span className={`text-xs px-2 py-1 rounded ${s.boss.defeated ? "bg-nature-bark text-nature-blossom" : "bg-[#FCE8E8] text-red-700"}`}>
                    {s.boss.defeated ? "DEFEATED" : `${s.boss.percent}% remaining`}
                  </span>
                </div>
                <div className="h-2 bg-[#E5E0D3] rounded-full overflow-hidden">
                  <div
                    className={`h-full ${s.boss.defeated ? "bg-emerald-500" : "bg-red-500"}`}
                    style={{ width: `${s.boss.defeated ? 100 : 100 - s.boss.percent}%` }}
                  />
                </div>
                {s.boss.top_dealers.length > 0 && (
                  <div className="mt-3 text-xs text-text-muted">
                    Top: {s.boss.top_dealers.map((d) => `${d.name} (${d.damage.toLocaleString()})`).join(", ")}
                  </div>
                )}
              </div>
            ))
          )}

          {s.merchant?.present && (
            sectionCard("merchant", (
              <div>
                <p className="text-sm text-text-secondary">The Mystery Merchant has arrived.</p>
                <p className="text-xs text-text-muted mt-1">{s.merchant.trades} trades happened today</p>
              </div>
            ))
          )}
        </div>

        {paper.archive.length > 0 && (
          <div className="mt-8">
            <div className="text-xs text-text-muted uppercase tracking-widest mb-3">Past Editions</div>
            <div className="flex gap-3 overflow-x-auto pb-2">
              {paper.archive.map((e) => (
                <div key={e.date} className="bg-white border border-nature-leaf/20 rounded-lg px-4 py-3 min-w-[180px]">
                  <div className="text-xs text-text-muted">{e.date}</div>
                  <div className="text-sm font-semibold text-text-secondary line-clamp-2">{e.headline}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-8 text-center">
          <button
            onClick={refresh}
            disabled={refreshing}
            className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-text-primary rounded-lg text-sm font-semibold transition"
          >
            {refreshing ? "Printing..." : "Reprint Today's Edition"}
          </button>
        </div>
      </div>
    </div>
  );
}
