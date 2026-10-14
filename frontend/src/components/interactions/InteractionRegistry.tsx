// @ts-nocheck
import React from "react";
import { learningEventsApi } from "../../services/api/learningEvents.ts";
import StateManipulation from "./StateManipulation";
import Slider from "./Slider";
import Toggle from "./Toggle";
import FreezePredict from "./FreezePredict";
import TimeTravel from "./TimeTravel";
import MemoryBoard from "./MemoryBoard";
import CodeBlocks from "./CodeBlocks";
import FillMissing from "./FillMissing";
import BugSurgery from "./BugSurgery";
import FirstWrongMoment from "./FirstWrongMoment";
import CompareWorlds from "./CompareWorlds";
import CounterexampleBuilder from "./CounterexampleBuilder";
import ReverseEngineer from "./ReverseEngineer";
import ExplainToUnlock from "./ExplainToUnlock";
import SameConceptNewWorld from "./SameConceptNewWorld";

type InteractionRegistryProps = {
  interaction: {
    type: string;
    params?: Record<string, any>;
    onComplete?: (result: any) => void;
    onAction?: (action: string, data: any) => void;
  };
  context?: {
    atom_id?: string;
    session_id?: string;
    user_id?: string;
    misconception_codes?: string[];
  };
};

const COMPONENT_MAP: Record<string, React.ComponentType<any>> = {
  state_manipulation: StateManipulation,
  slider: Slider,
  toggle: Toggle,
  freeze_predict: FreezePredict,
  time_travel: TimeTravel,
  memory_board: MemoryBoard,
  code_blocks: CodeBlocks,
  fill_missing: FillMissing,
  bug_surgery: BugSurgery,
  first_wrong_moment: FirstWrongMoment,
  compare_worlds: CompareWorlds,
  counterexample_builder: CounterexampleBuilder,
  reverse_engineer: ReverseEngineer,
  explain_to_unlock: ExplainToUnlock,
  same_concept_new_world: SameConceptNewWorld,
};

export default function InteractionRegistry({ interaction, context }: InteractionRegistryProps) {
  const { type, params = {}, onComplete, onAction } = interaction;
  const Component = COMPONENT_MAP[type];

  if (!Component) {
    return (
      <div className="text-sm text-gray-400">
        Missing interaction: {type}
      </div>
    );
  }

  const wrappedOnAction = async (action: string, data: any) => {
    onAction?.(action, data);
    
    if (context?.atom_id && context?.session_id) {
      try {
        await learningEventsApi.logInteractionAction({
          atom_id: context.atom_id,
          session_id: context.session_id,
          interaction_type: type,
          action,
          data,
          misconception_codes: context.misconception_codes,
        });
      } catch (e) {
        // Non-blocking
      }
    }
  };

  return <Component {...params} onComplete={onComplete || (() => {})} onAction={wrappedOnAction} />;
}
