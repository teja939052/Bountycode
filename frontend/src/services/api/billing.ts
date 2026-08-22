import { requestWithRetry as request } from "./request.ts";
import type {
  BillingStatus,
  CheckoutResponse,
  PlanInfo,
  CouponValidation,
} from "./types.ts";

export const billingApi = {
  createCheckout(
    country = "US",
    couponCode = "",
    seats = 1,
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode, seats }),
    });
  },

  createLifetimeCheckout(
    country = "US",
    couponCode = "",
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout/lifetime", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    });
  },

  createYearlyCheckout(
    country = "US",
    couponCode = "",
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout/yearly", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    });
  },

  createTeamCheckout(
    country = "US",
    seats = 5,
    couponCode = "",
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout/team", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    });
  },

  createEnterpriseCheckout(
    country = "US",
    seats = 10,
    couponCode = "",
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout/enterprise", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    });
  },

  createStripeCheckout(
    plan = "pro_monthly",
    country = "US",
    seats = 1,
    couponCode = "",
  ): Promise<CheckoutResponse> {
    return request("/api/v1/billing/checkout/stripe", {
      method: "POST",
      body: JSON.stringify({ plan, country, seats, coupon_code: couponCode }),
    });
  },

  captureOrder(
    orderId: string,
  ): Promise<{ captured?: boolean; status?: string }> {
    return request("/api/v1/billing/capture", {
      method: "POST",
      body: JSON.stringify({ order_id: orderId }),
    });
  },

  validateCoupon(code: string): Promise<CouponValidation> {
    return request("/api/v1/coupon/validate/" + code.toUpperCase());
  },

  applyCoupon(
    code: string,
    plan: string,
    amount: number,
    billingCycle: string,
  ): Promise<{ valid: boolean; discount: number; message?: string }> {
    return request("/api/v1/coupon/apply", {
      method: "POST",
      body: JSON.stringify({ code, plan, amount, billing_cycle: billingCycle }),
    });
  },

  getStatus(): Promise<BillingStatus> {
    return request("/api/v1/billing/status");
  },

  getPlans(): Promise<PlanInfo[]> {
    return request("/api/v1/billing/plans");
  },

  getRevenueMetrics(): Promise<Record<string, unknown>> {
    return request("/api/v1/revenue/metrics");
  },

  getMRR(): Promise<{ mrr: number; arra?: number; growth?: number }> {
    return request("/api/v1/revenue/mrr");
  },

  getRevenueAnalytics(days: number = 30): Promise<Record<string, unknown>> {
    return request(`/api/v1/revenue/analytics?days=${days || 30}`);
  },

  getReferralInfo(): Promise<Record<string, unknown>> {
    return request("/api/v1/referral/info");
  },

  createReferral(): Promise<{ referral_code: string; referral_link: string }> {
    return request("/api/v1/referral/create", { method: "POST" });
  },

  getReferralLeaderboard(limit = 10): Promise<Record<string, unknown>> {
    return request(`/api/v1/referral/leaderboard?limit=${limit}`);
  },

  claimReferralReward(
    referralNumber: string,
  ): Promise<{ claimed?: boolean; reward?: string }> {
    return request("/api/v1/referral/claim-reward", {
      method: "POST",
      body: JSON.stringify({ referral_number: referralNumber }),
    });
  },
};
