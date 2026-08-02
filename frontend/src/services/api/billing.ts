import { requestWithRetry as request } from "./request.ts";
export const billingApi = {
  createCheckout(country = "US", couponCode = "", seats = 1) {
    return request("/api/v1/billing/checkout", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode, seats }),
    });
  },

  createLifetimeCheckout(country = "US", couponCode = "") {
    return request("/api/v1/billing/checkout/lifetime", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    });
  },

  createYearlyCheckout(country = "US", couponCode = "") {
    return request("/api/v1/billing/checkout/yearly", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    });
  },

  createTeamCheckout(country = "US", seats = 5, couponCode = "") {
    return request("/api/v1/billing/checkout/team", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    });
  },

  createEnterpriseCheckout(country = "US", seats = 10, couponCode = "") {
    return request("/api/v1/billing/checkout/enterprise", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    });
  },

  createStripeCheckout(plan = "pro_monthly", country = "US", seats = 1, couponCode = "") {
    return request("/api/v1/billing/checkout/stripe", {
      method: "POST",
      body: JSON.stringify({ plan, country, seats, coupon_code: couponCode }),
    });
  },

  captureOrder(orderId) {
    return request("/api/v1/billing/capture", {
      method: "POST",
      body: JSON.stringify({ order_id: orderId }),
    });
  },

  validateCoupon(code) {
    return request("/api/v1/coupon/validate/" + code.toUpperCase());
  },

  applyCoupon(code, plan, amount, billingCycle) {
    return request("/api/v1/coupon/apply", {
      method: "POST",
      body: JSON.stringify({ code, plan, amount, billing_cycle: billingCycle }),
    });
  },

  getStatus() {
    return request("/api/v1/billing/status");
  },

  getRevenueMetrics() {
    return request("/api/v1/revenue/metrics");
  },

  getMRR() {
    return request("/api/v1/revenue/mrr");
  },

  getRevenueAnalytics(days) {
    return request(`/api/v1/revenue/analytics?days=${days || 30}`);
  },

  getReferralInfo() {
    return request("/api/v1/referral/info");
  },

  createReferral() {
    return request("/api/v1/referral/create", { method: "POST" });
  },

  getReferralLeaderboard(limit = 10) {
    return request(`/api/v1/referral/leaderboard?limit=${limit}`);
  },

  claimReferralReward(referralNumber) {
    return request("/api/v1/referral/claim-reward", {
      method: "POST",
      body: JSON.stringify({ referral_number: referralNumber }),
    });
  },
};