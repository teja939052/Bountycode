import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function SkillTrees() {
  const { showXP, play } = useJuice();
  const [trees, setTrees] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [treesData, progressData] = await Promise.all([
        api.skillTrees?.getAll?.() || { trees: [] },
        api.skillTrees?.getProgress?.() || {},
      ]);
      setTrees(treesData.trees || []);
      setProgress(progressData);
    } catch {
      setTrees([]);
      setProgress(null);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteLevel = async (treeKey, branchName, levelId, xp) => {
    try {
      const data = await api.skillTrees?.updateProgress?.({
        tree_key: treeKey,
        branch_name: branchName,
        level_id: levelId,
        xp,
      }) || {};

      setMessage(`+${data.total_xp || xp} XP! ${data.branch_complete ? "🌿 Branch Complete!" : ""}`);
      play(data.branch_complete ? "levelUp" : "xpCollect");
      showXP(data.total_xp || xp, window.innerWidth / 2, window.innerHeight / 2);
      setTimeout(() => setMessage(""), 3000);
      await loadData();
    } catch {
      setMessage("Failed to update progress");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading skill trees...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">🌳 Skill Trees</h1>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      <div className="bg-white border border-gray-200 rounded-xl p-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-600">Total Skill XP</span>
          <span className="text-2xl font-bold text-indigo-600">{progress?.total_xp || 0}</span>
        </div>
      </div>

      <div className="space-y-8">
        {trees.map((tree) => (
          <div key={tree.key} className="bg-white border border-gray-200 rounded-xl overflow-hidden">
            <div className="p-5 border-b border-gray-100">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{tree.emoji}</span>
                <div className="flex-1">
                  <h2 className="text-xl font-bold">{tree.name}</h2>
                  <p className="text-sm text-gray-500">{tree.description}</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-indigo-600">{tree.progress?.percentage || 0}%</div>
                  <div className="text-xs text-gray-500">{tree.progress?.completed || 0}/{tree.progress?.total || 0} levels</div>
                </div>
              </div>
              <div className="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-600 rounded-full transition-all"
                  style={{ width: `${tree.progress?.percentage || 0}%` }}
                />
              </div>
            </div>
            <div className="p-5 space-y-6">
              {tree.branches.map((branch) => (
                <div key={branch.name}>
                  <h3 className="text-lg font-semibold mb-3">
                    <span className="mr-2">{branch.icon}</span>
                    {branch.name}
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {branch.levels.map((level) => {
                      const isCompleted = progress?.progress?.[tree.key]?.[branch.name]?.[level.id]?.completed;
                      return (
                        <div
                          key={level.id}
                          className={`p-3 rounded-lg border ${isCompleted ? "border-green-300 bg-green-50" : "border-gray-200 bg-gray-50"}`}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-medium text-sm">{level.name}</span>
                            <span className="text-xs font-semibold text-indigo-600">+{level.xp} XP</span>
                          </div>
                          {isCompleted ? (
                            <span className="text-xs text-green-600">✓ Completed</span>
                          ) : (
                            <button
                              onClick={() => handleCompleteLevel(tree.key, branch.name, level.id, level.xp)}
                              className="mt-1 px-2 py-0.5 bg-indigo-600 text-white rounded text-xs font-medium hover:bg-indigo-700"
                            >
                              Complete
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}