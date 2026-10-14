// @ts-nocheck
import type { UiverseComponentMeta } from "./index";
import { REGISTERED_COMPONENTS } from "./registry-data";

export function getRegisteredComponents(): UiverseComponentMeta[] {
  return [...REGISTERED_COMPONENTS];
}
