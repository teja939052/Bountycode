import { requestWithRetry as request } from "./request.ts";
import type { ThemeMode } from "../../store/themeStore";

export type { ThemeInfo } from "../../store/themeStore";

export const themesApi = {
  current(): Promise<{ theme: string }> {
    return request("/api/v1/themes/current");
  },

  list(): Promise<{
    is_pro: boolean;
    unlocked: string[];
    current: string;
  }> {
    return request("/api/v1/themes/");
  },

  select(themeId: ThemeMode): Promise<{ success: boolean; theme: string }> {
    return request("/api/v1/themes/select", {
      method: "POST",
      body: JSON.stringify({ theme_id: themeId }),
    });
  },
};
