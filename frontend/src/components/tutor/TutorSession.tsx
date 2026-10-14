// @ts-nocheck
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import api from "../../services/api";
import CalibratedQuestion from "./CalibratedQuestion";
import HintLadder from "./HintLadder";
import ReAnalogy from "./ReAnalogy";
import Decompose from "./Decompose";
import PickTheTruth from "./PickTheTruth";
import TeachBack from "./TeachBack";

type TutorSessionProps = {
  atomId: string;
  treeId: string;
  onComplete: () => void;
};

type Node = {
  move: string;
  say: string;
  to?: string;
  opts?: Array<{ t: string; to: string; code?: string }>;
  hints?: string[];
  steps?: string[];
  cards?: string[];
  correct_order?: number[];
  next?: string;
};

export default function TutorSession({ atomId, treeId, onComplete }: TutorSessionProps) {
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function init() {
      setLoading(true);
      setError("");
      try {
        const res = await api.tutor.startSession({ atom_id: atomId, tree_id: treeId });
        if (!cancelled) setSession(res.session);
      } catch (e) {
        if (!cancelled) setError("Failed to start tutor session");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    init();
    return () => { cancelled = true; };
  }, [atomId, treeId]);

  const handleAdvance = async (optionIndex: number) => {
    if (!session) return;
    try {
      const res = await api.tutor.advanceSession({ session_id: session.session_id, option_index: optionIndex });
      const updated = res.session;
      setSession(updated);

      const node = updated.current_node || {};
      if (node.move === "advance" || node.to === "done") {
        onComplete();
      }
    } catch (e) {
      setError("Failed to advance");
    }
  };

  const handleTeachBackComplete = async (_order: number[]) => {
    await handleAdvance(0);
  };

  if (loading) {
    return <div className="text-center text-gray-500 py-8">Starting tutor...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600 py-8">{error}</div>;
  }

  if (!session) {
    return <div className="text-center text-gray-500 py-8">No session.</div>;
  }

  const node: Node = session.current_node || {};
  if (node.move === "advance" || node.to === "done") {
    return (
      <div className="text-center py-8">
        <motion.div className="text-4xl mb-3" initial={{ scale: 0 }} animate={{ scale: 1 }}>🎉</motion.div>
        <p className="text-lg font-medium text-gray-800">Tutor session complete</p>
        <motion.button
          className="mt-4 bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          onClick={onComplete}
        >
          Continue
        </motion.button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xs font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{node.move}</span>
        <span className="text-xs text-gray-500">Tutor</span>
      </div>
      {node.move === "calibrated_question" && node.opts && (
        <CalibratedQuestion say={node.say} opts={node.opts} onChoose={handleAdvance} />
      )}
      {node.move === "hint_ladder" && node.hints && (
        <HintLadder say={node.say} hints={node.hints} onComplete={() => handleAdvance(0)} />
      )}
      {node.move === "re_analogy" && (
        <ReAnalogy
          say={node.say}
          physical_metaphor={undefined}
          primitive={undefined}
          opts={node.opts || []}
          onChoose={handleAdvance}
        />
      )}
      {node.move === "decompose" && node.steps && (
        <Decompose say={node.say} steps={node.steps} onComplete={() => handleAdvance(0)} />
      )}
      {node.move === "pick_the_truth" && node.opts && (
        <PickTheTruth say={node.say} opts={node.opts} onChoose={handleAdvance} />
      )}
      {node.move === "teach_back" && node.cards && (
        <TeachBack say={node.say} cards={node.cards} correct_order={node.correct_order || []} onComplete={handleTeachBackComplete} />
      )}
    </div>
  );
}
