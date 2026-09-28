import { request } from "./request";

/**
 * 接口定义（baseUrl 已含 /api/v1，见 config/proxy.ts）
 */

// 登录返回
export type LoginResult = {
	access_token: string;
	token_type?: string;
	user?: any;
};

// 总览
export type Summary = {
	total_balance: number;
	total_income: number;
	total_expense: number;
	account_count: number;
};

// 资金消耗与耗尽预测
export type FundRunway = {
	balance: number;
	account_count: number;
	window_months: number;
	horizon_months: number;
	monthly_income: number;
	monthly_expense: number;
	monthly_net_outflow: number;
	runway_months: number | null;
	depletion_date: string | null;
	consumption_ratio: number;
	progress: number;
	status: string;
	message: string;
};

/** 登录注册 */
export const authApi = {
	login(data: { username: string; password: string }) {
		return request<LoginResult>({
			url: "/auth/login",
			method: "POST",
			data
		});
	}
};

/** 总览 */
export const summaryApi = {
	get() {
		return request<Summary>({ url: "/summary" });
	},

	fundRunway(params?: { months?: number; horizon?: number }) {
		return request<FundRunway>({
			url: "/summary/fund-runway",
			params
		});
	}
};

/** 账户 */
export const accountApi = {
	list() {
		return request<any[]>({ url: "/accounts" });
	}
};

/** 收支管理 */
export const incomeExpenseApi = {
	list(params?: any) {
		return request<any[]>({
			url: "/income-expense",
			params
		});
	}
};
