// @ts-nocheck
import React from "react";

const PRIMITIVE_MAP: Record<string, React.ComponentType<any>> = {
  VariableBox: React.lazy(() => import("./VariableBox")),
  QueueLine: React.lazy(() => import("./QueueLine")),
  PointerHand: React.lazy(() => import("./PointerHand")),
  LoopCounter: React.lazy(() => import("./LoopCounter")),
  StackPlates: React.lazy(() => import("./StackPlates")),
  Speaker: React.lazy(() => import("./Speaker")),
  RecipeCard: React.lazy(() => import("./RecipeCard")),
  Funnel: React.lazy(() => import("./Funnel")),
  ConveyorBelt: React.lazy(() => import("./ConveyorBelt")),
  Camera: React.lazy(() => import("./Camera")),
  Blueprint: React.lazy(() => import("./Blueprint")),
  LockedBox: React.lazy(() => import("./LockedBox")),
  RussianDoll: React.lazy(() => import("./RussianDoll")),
  FunctionMachine: React.lazy(() => import("./FunctionMachine")),
  LockerRow: React.lazy(() => import("./LockerRow")),
  Crossroads: React.lazy(() => import("./Crossroads")),
  PhoneBook: React.lazy(() => import("./PhoneBook")),
};

type PrimitiveRegistryProps = {
  primitive: string;
  [key: string]: any;
};

export default function PrimitiveRegistry({ primitive, ...props }: PrimitiveRegistryProps) {
  const Component = PRIMITIVE_MAP[primitive];
  if (!Component) {
    return (
      <div className="text-sm text-gray-400">
        Missing primitive: {primitive}
      </div>
    );
  }
  return <Component {...props} />;
}
