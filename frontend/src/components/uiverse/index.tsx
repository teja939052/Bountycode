// @ts-nocheck
export const UIVERSE_CATEGORIES = [
  "Buttons",
  "Cards",
  "Loaders",
  "Toggle-switches",
  "Inputs",
  "Forms",
  "Checkboxes",
  "Patterns",
  "Radio-buttons",
  "Tooltips",
  "Notifications",
] as const;

export type UiverseCategory = (typeof UIVERSE_CATEGORIES)[number];

export interface UiverseComponentMeta {
  id: string;
  name: string;
  category: UiverseCategory;
  tags: string[];
  source: "uiverse" | "custom";
  description?: string;
}

export const UIVERSE_REGISTRY: UiverseComponentMeta[] = [];

export function registerUiverseComponent(meta: UiverseComponentMeta) {
  UIVERSE_REGISTRY.push(meta);
}

export function getUiverseComponentsByCategory(
  category: UiverseCategory
): UiverseComponentMeta[] {
  return UIVERSE_REGISTRY.filter((item) => item.category === category);
}

export function searchUiverseComponents(query: string): UiverseComponentMeta[] {
  const lower = query.toLowerCase();
  return UIVERSE_REGISTRY.filter(
    (item) =>
      item.name.toLowerCase().includes(lower) ||
      item.tags.some((tag) => tag.toLowerCase().includes(lower)) ||
      item.category.toLowerCase().includes(lower)
  );
}
