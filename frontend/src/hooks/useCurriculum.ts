// @ts-nocheck
import { useQuery } from "@tanstack/react-query";
import api from "../services/api";
import type { FlagshipMission } from "../services/api/curriculum";

const FLAGSHIP_MISSIONS_KEY = ["curriculum", "missions"] as const;
const FLAGSHIP_MISSION_KEY = (missionId: string) => ["curriculum", "mission", missionId] as const;

export function useFlagshipMissions() {
  return useQuery({
    queryKey: FLAGSHIP_MISSIONS_KEY,
    queryFn: () => api.curriculum.listFlagshipMissions(),
    staleTime: 1000 * 60 * 60,
  });
}

export function useFlagshipMission(missionId: string | null) {
  return useQuery({
    queryKey: FLAGSHIP_MISSION_KEY(missionId || ""),
    queryFn: () => api.curriculum.getFlagshipMission(missionId!),
    enabled: Boolean(missionId),
    staleTime: 1000 * 60 * 30,
  });
}

export function useCurriculumMeta() {
  return useQuery({
    queryKey: ["curriculum", "meta"],
    queryFn: () => api.curriculum.getMeta(),
    staleTime: 1000 * 60 * 60,
  });
}

export function useCurriculumStats() {
  return useQuery({
    queryKey: ["curriculum", "stats"],
    queryFn: () => api.curriculum.getStats(),
    staleTime: 1000 * 60 * 60,
  });
}

export function useCurriculumPhases() {
  return useQuery({
    queryKey: ["curriculum", "phases"],
    queryFn: () => api.curriculum.listPhases(),
    staleTime: 1000 * 60 * 60,
  });
}

export function useCurriculumRoles() {
  return useQuery({
    queryKey: ["curriculum", "roles"],
    queryFn: () => api.curriculum.listRoles(),
    staleTime: 1000 * 60 * 30,
  });
}

export function useRoleDetail(roleId) {
  return useQuery({
    queryKey: ["curriculum", "role", roleId],
    queryFn: () => api.curriculum.getRoleDetail(roleId),
    enabled: !!roleId,
    staleTime: 1000 * 60 * 30,
  });
}

export function useRolePhase(roleId, phaseId) {
  return useQuery({
    queryKey: ["curriculum", "role", roleId, "phase", phaseId],
    queryFn: () => api.curriculum.getRolePhase(roleId, phaseId),
    enabled: !!roleId && !!phaseId,
    staleTime: 1000 * 60 * 30,
  });
}

export function useCurriculumModules(filters = {}) {
  return useQuery({
    queryKey: ["curriculum", "modules", filters],
    queryFn: () => api.curriculum.listModules(filters),
    staleTime: 1000 * 60 * 30,
  });
}

export function useModuleDetail(moduleId) {
  return useQuery({
    queryKey: ["curriculum", "module", moduleId],
    queryFn: () => api.curriculum.getModuleDetail(moduleId),
    enabled: !!moduleId,
    staleTime: 1000 * 60 * 15,
  });
}

export function useCurriculumCompanies() {
  return useQuery({
    queryKey: ["curriculum", "companies"],
    queryFn: () => api.curriculum.listCompanies(),
    staleTime: 1000 * 60 * 60,
  });
}

export function useCompanyDetail(companyId) {
  return useQuery({
    queryKey: ["curriculum", "company", companyId],
    queryFn: () => api.curriculum.getCompanyDetail(companyId),
    enabled: !!companyId,
    staleTime: 1000 * 60 * 30,
  });
}

export function useCurriculumPath(roleId, company = null) {
  return useQuery({
    queryKey: ["curriculum", "path", roleId, company],
    queryFn: () => api.curriculum.getCurriculumPath(roleId, company),
    enabled: !!roleId,
    staleTime: 1000 * 60 * 15,
  });
}
