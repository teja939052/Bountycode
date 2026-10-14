// @ts-nocheck
import type { UiverseComponentMeta } from "./index";
import { REGISTERED_COMPONENTS } from "./registry";

export function getRegisteredComponents(): UiverseComponentMeta[] {
  return [...REGISTERED_COMPONENTS];
}
