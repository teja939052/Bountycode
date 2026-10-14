// @ts-nocheck
import { requestWithRetry } from "./request.ts";

export const accountApi = {
  getProfile: () => requestWithRetry("/api/v1/account/profile"),
  getFeatures: () => requestWithRetry("/api/v1/account/features"),
  getPlan: () => requestWithRetry("/api/v1/account/plan"),
};

export default accountApi;
