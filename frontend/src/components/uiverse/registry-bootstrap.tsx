// @ts-nocheck
import { UIVERSE_CATEGORIES, type UiverseComponentMeta, registerUiverseComponent } from "./index";

const BASE_URL =
  "https://raw.githubusercontent.com/uiverse-io/galaxy/main";

async function fetchJson(url: string) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
  return res.json();
}

async function listCategoryComponents(category: string): Promise<string[]> {
  const url = `${BASE_URL}/${encodeURIComponent(category)}`;
  const data = await fetchJson(url);
  if (Array.isArray(data)) return data as string[];
  return [];
}

function parseComponentName(filename: string) {
  const raw = filename.replace(/\.html$/i, "");
  const parts = raw.split("_");
  const author = parts[0] || "unknown";
  const name = parts.slice(1).join("_").replace(/-/g, " ") || raw;
  return { author, name: name.trim() || raw };
}

async function bootstrapUiverseRegistry(): Promise<UiverseComponentMeta[]> {
  const items: UiverseComponentMeta[] = [];
  for (const category of UIVERSE_CATEGORIES) {
    try {
      const files = await listCategoryComponents(category);
      for (const file of files) {
        const { author, name } = parseComponentName(file);
        const id = `${category}/${file}`;
        items.push({
          id,
          name,
          category: category as UiverseComponentMeta["category"],
          tags: [category.toLowerCase(), author],
          source: "uiverse",
          description: `${name} by ${author}`,
        });
      }
    } catch (err) {
      console.error(`Failed to bootstrap ${category}:`, err);
    }
  }

  for (const item of items) {
    registerUiverseComponent(item);
  }
  return items;
}

export { bootstrapUiverseRegistry };
