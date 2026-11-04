import { useState } from 'react';
import { Link } from 'react-router-dom';
import { CONTENT_BUNDLES, CONTENT_BY_SUBJECT } from '../assets/content/content-bundles';
import { GAMIFICATION_ICONS } from '../assets/gamification/index';
import { BRAND } from '../assets/brand/index';

const SUBJECT_LABELS: Record<string, { label: string; color: string }> = {
  quantitative_aptitude: { label: 'Aptitude & Reasoning', color: 'text-streak-500' },
  logical_reasoning: { label: 'Logical Reasoning', color: 'text-streak-500' },
  verbal_ability: { label: 'Verbal Ability', color: 'text-bugsy-500' },
  dsa: { label: 'Data Structures & Algorithms', color: 'text-coddy-500' },
  programming: { label: 'Programming', color: 'text-coddy-500' },
};

export default function ContentBundles() {
  const [filter, setFilter] = useState<string>('all');
  const bundles = filter === 'all' ? CONTENT_BUNDLES : CONTENT_BUNDLES.filter(b => b.subject === filter);

  const subjects = Object.keys(CONTENT_BY_SUBJECT);

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-ink dark:text-white">Content Bundles</h1>
          <p className="text-slate-500 dark:text-slate-400">
            {CONTENT_BUNDLES.length} learning bundles · {CONTENT_BUNDLES.reduce((s, b) => s + b.totalItems, 0)} lessons & practice items · All human-reviewed
          </p>
        </div>
        <Link to="/percentages-academy" className="flex items-center gap-2 px-4 py-2 bg-coddy-500 text-white rounded-xl hover:bg-coddy-button transition font-medium">
          Start Learning
        </Link>
      </div>

      {/* Stats bar */}
      <div className="grid gap-4 md:grid-cols-4">
        {[ 
          { label: 'Bundles', value: CONTENT_BUNDLES.length, icon: <GAMIFICATION_ICONS.xp className="w-5 h-5" /> },
          { label: 'Lessons', value: CONTENT_BUNDLES.reduce((s, b) => s + b.lessonCount, 0), icon: <GAMIFICATION_ICONS.journey_done className="w-5 h-5" /> },
          { label: 'Practice Qs', value: CONTENT_BUNDLES.reduce((s, b) => s + b.practiceCount + b.questionCount, 0), icon: <GAMIFICATION_ICONS.xp className="w-5 h-5" /> },
          { label: 'Est. Minutes', value: CONTENT_BUNDLES.reduce((s, b) => s + b.estimatedMinutes, 0), icon: <GAMIFICATION_ICONS.energy className="w-5 h-5" /> },
        ].map((stat, i) => (
          <div key={i} className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-xl p-4 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-coddy-50 dark:bg-coddy-900/30 flex items-center justify-center text-coddy-500">
                {stat.icon}
              </div>
              <div>
                <p className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">{stat.label}</p>
                <p className="text-2xl font-bold text-ink dark:text-white">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Subject filter */}
      <div className="flex gap-2 overflow-x-auto pb-4">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-xl font-medium transition ${filter === 'all' ? 'bg-coddy-500 text-white' : 'bg-white dark:bg-slate-800/50 text-slate-500 border border-white/20 dark:border-white/10'}`}
        >
          All Bundles
        </button>
        {subjects.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-4 py-2 rounded-xl font-medium transition ${filter === s ? 'bg-coddy-500 text-white' : 'bg-white dark:bg-slate-800/50 text-slate-500 border border-white/20 dark:border-white/10'}`}
          >
            {SUBJECT_LABELS[s]?.label || s}
          </button>
        ))}
      </div>

      {/* Bundle grid */}
      <div className="grid gap-6 md:grid-cols-3 lg:grid-cols-4">
        {bundles.length === 0 ? (
          <div className="col-span-full text-center py-20">
            <p className="text-slate-500 dark:text-slate-400">No bundles found for this subject.</p>
          </div>
        ) : (
          bundles.map((b) => {
            const subj = SUBJECT_LABELS[b.subject];
            const Icon = GAMIFICATION_ICONS[b.assets.icon as keyof typeof GAMIFICATION_ICONS] || GAMIFICATION_ICONS.xp;
            return (
              <article key={b.topic} className="group bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{
                    backgroundColor: subj.color.replace('text-', 'bg-') + '50',
                    color: subj.color,
                  }}>
                    <Icon />
                  </div>
                  <span className="text-[10px] px-2 py-[1px] rounded border font-bold text-xs" style={{
                    backgroundColor: `${subj.color.replace('text-', '')}15`,
                    color: subj.color.replace('text-', ''),
                    border: `1px solid ${subj.color.replace('text-', '')}40`,
                  }}>
                    {b.difficulty.toUpperCase()}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-ink dark:text-white mb-1">{b.title}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4 line-clamp-2">{b.description}</p>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400">
                    <span>{b.lessonCount} lessons</span>
                    <span>·</span>
                    <span>{b.practiceCount + b.questionCount} questions</span>
                  </div>
                  <span className="text-[10px] font-mono text-coddy-500">{b.estimatedMinutes} min</span>
                </div>
                <div className="flex gap-2">
                  <Link to={`/percentages-academy?topic=${b.topic}`} className="flex-1 px-3 py-2 bg-ink dark:bg-slate-800 text-white text-xs font-bold rounded-lg text-center hover:bg-indigo-800 dark:hover:bg-slate-700 transition">
                    Start
                  </Link>
                  <Link to={`/blog/dsa-basics-what-is-dsa`} className="px-2 py-2 bg-white dark:bg-slate-800 text-slate-500 border border-white/20 dark:border-white/10 rounded-lg text-xs hover:bg-slate-50 dark:hover:bg-slate-700/50 transition" title="Related blog">
                    <GAMIFICATION_ICONS.bugsy className="w-4 h-4" />
                  </Link>
                </div>
              </article>
            );
          })
        )}
      </div>
    </div>
  );
}
