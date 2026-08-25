import { requestWithRetry as request } from "./request.ts";

export interface DailyOrder {
  id: string;
  type: string;
  title: string;
  detail: string;
  link: string;
  points: number;
  completed: boolean;
}

export interface TodayOrders {
  date: string;
  deadline: {
    company: string | null;
    drive_date: string | null;
    days_left: number | null;
  };
  orders: DailyOrder[];
  progress: {
    done: number;
    total: number;
    earned_points: number;
    total_points: number;
    all_done: boolean;
  };
}

export const dailyOrdersApi = {
  today(): Promise<TodayOrders> {
    return request("/api/v1/orders/today");
  },

  setDeadline(company: string, driveDate: string): Promise<{
    company: string;
    drive_date: string;
    days_left: number;
    message: string;
  }> {
    return request("/api/v1/orders/deadline", {
      method: "PUT",
      body: JSON.stringify({ company, drive_date: driveDate }),
    });
  },

  clearDeadline(): Promise<{ cleared: boolean }> {
    return request("/api/v1/orders/deadline", { method: "DELETE" });
  },

  complete(orderId: string): Promise<{
    order_id: string;
    already_done: boolean;
    xp_gained: number;
  }> {
    return request(`/api/v1/orders/${orderId}/complete`, { method: "POST" });
  },
};
