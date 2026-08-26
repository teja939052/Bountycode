export default function ForestJourney({ forest, level }: { forest: any; level: number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 mt-6">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-3">Forest Journey</h3>
      <p className="text-xs text-gray-400">Your forest grows as you level up. Current level: {level}</p>
    </div>
  );
}
