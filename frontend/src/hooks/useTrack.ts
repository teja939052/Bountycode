import { useCallback } from "react";
import { metricsApi } from "../services/api/metrics.ts";

export default function useTrack() {
  const track = useCallback((feature: string, event: string, value?: any) => {
    metricsApi.track(feature, event, value).catch(() => {});
  }, []);

  return track;
}
