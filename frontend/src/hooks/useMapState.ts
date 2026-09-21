import { useQuery } from "@tanstack/react-query";
import { mapApi, type MapState } from "../services/api/map.ts";

export function useMapState(worldId?: string) {
  return useQuery<MapState>({
    queryKey: ["map", "state", worldId ?? "active"],
    queryFn: () => mapApi.getState(worldId),
    staleTime: 30_000,
    retry: 1,
  });
}
