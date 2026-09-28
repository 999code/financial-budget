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

// 资金消耗与耗尽预测（绝对值口径）逐月明细
export type AbsoluteOutlookMonth = {
	month: string;
	income: number;
	expense: number;
	net: number;
	balance: number;
};

// 资金消耗与耗尽预测（绝对值口径）
export type AbsoluteOutlook = {
	opening_balance: number;
	account_count: number;
	months: number;
	from_month: string;
	target_month: string;
	total_income: number;
	total_expense: number;
	net_amount: number;
	expense_income_ratio: number | null;
	expense_income_percent: number | null;
	net_asset: number;
	expense_net_asset_ratio: number | null;
	expense_net_asset_percent: number | null;
	projected_balance: number;
	depletion_month: string | null;
	monthly: AbsoluteOutlookMonth[];
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
	},

	/** 绝对值口径：months 为预测跨度（月），从当前月的下一月起算，1~120 */
	absoluteOutlook(params?: { months?: number }) {
		return request<AbsoluteOutlook>({
			url: "/summary/absolute-outlook",
			params
		});
	}
};

/**
 * 账户
 * type: cash(现金) / bank(储蓄卡) / creditcard(信用卡) / investment(投资)
 * 注意：balance 由收支实时算出，不能提交；只能录入 initial_balance(期初余额)
 * card_number 必填，且同一用户下不可重复
 */
export type AccountPayload = {
	name: string;
	card_number: string;
	type: string;
	initial_balance: number;
	currency: string;
};

/** 账户 */
export const accountApi = {
	list() {
		return request<any[]>({ url: "/accounts" });
	},

	detail(id: number) {
		return request<any>({ url: `/accounts/${id}` });
	},

	create(data: AccountPayload) {
		return request<any>({
			url: "/accounts",
			method: "POST",
			data
		});
	},

	update(id: number, data: Partial<AccountPayload>) {
		return request<any>({
			url: `/accounts/${id}`,
			method: "PUT",
			data
		});
	},

	remove(id: number) {
		return request<any>({
			url: `/accounts/${id}`,
			method: "DELETE"
		});
	}
};

/** 用户信息 */
export type UserPayload = {
	name?: string;
	username?: string;
	phone?: string;
	email?: string;
	password?: string;
};

export const userApi = {
	detail(id: number) {
		return request<any>({ url: `/users/${id}` });
	},

	update(id: number, data: UserPayload) {
		return request<any>({
			url: `/users/${id}`,
			method: "PUT",
			data
		});
	}
};

/**
 * 收支记录
 * category: income(收入) / expense(支出)
 * kind: fixed(固定) / temp(临时)
 * period: monthly(每月) / yearly(每年)，仅 kind=fixed 有效，临时传 null
 */
export type IncomeExpensePayload = {
	name: string;
	amount: number;
	kind: string;
	category: string;
	period?: string | null;
	end_date?: string | null;
	occurred_at?: string | null;
	note?: string | null;
	account_id?: number | null;
};

/**
 * 贷款
 * - loan_amount（贷款金额）由服务端按「总价 - 首付」算出，不能提交
 * - repayment_method: equal_installment(等额本息) / equal_principal(等额本金)
 * - 保存后后端会自动生成/更新一条「名称-月供」的固定支出
 */
export type LoanPayload = {
	name: string;
	total_price: number;
	principal: number;
	annual_rate: number;
	years: number;
	repayment_method: string;
	start_date?: string | null;
	note?: string | null;
};

/** 贷款管理 */
export const loanApi = {
	list(params?: any) {
		return request<any[]>({
			url: "/loans",
			params
		});
	},

	detail(id: number) {
		return request<any>({ url: `/loans/${id}` });
	},

	create(data: LoanPayload) {
		return request<any>({
			url: "/loans",
			method: "POST",
			data
		});
	},

	update(id: number, data: Partial<LoanPayload>) {
		return request<any>({
			url: `/loans/${id}`,
			method: "PUT",
			data
		});
	},

	remove(id: number) {
		return request<any>({
			url: `/loans/${id}`,
			method: "DELETE"
		});
	}
};

/**
 * 养老金月度记录
 * - amount 由服务端按人员档案 + 参数算出，请求体不含 amount
 * - direction: income(领取) / expense(缴费)，留空表示按退休日期自动判定
 * - period_month 格式 YYYY-MM
 */
export type PensionPayload = {
	person_id: number;
	period_month: string;
	direction?: string | null;
	salary?: number | null;
	occurred_on?: string | null;
	note?: string | null;
	contribution_years?: number | null;
	personal_account_balance?: number | null;
	deemed_years?: number | null;
	deemed_index?: number | null;
	annuity_balance?: number | null;
	resident_base?: number | null;
};

/** 养老金记录 */
export const pensionApi = {
	list(params?: any) {
		return request<any[]>({
			url: "/pensions",
			params
		});
	},

	stats(params?: any) {
		return request<any>({
			url: "/pensions/stats",
			params
		});
	},

	detail(id: number) {
		return request<any>({ url: `/pensions/${id}` });
	},

	/** 试算：不落库，返回金额与 breakdown 明细 */
	preview(data: PensionPayload) {
		return request<any>({
			url: "/pensions/preview",
			method: "POST",
			data
		});
	},

	create(data: PensionPayload) {
		return request<any>({
			url: "/pensions",
			method: "POST",
			data
		});
	},

	update(id: number, data: Partial<PensionPayload>) {
		return request<any>({
			url: `/pensions/${id}`,
			method: "PUT",
			data
		});
	},

	remove(id: number) {
		return request<any>({
			url: `/pensions/${id}`,
			method: "DELETE"
		});
	},

	/** 同步成收支管理里的固定收支（幂等） */
	sync(id: number, data?: { account_id?: number | null; name?: string | null }) {
		return request<any>({
			url: `/pensions/${id}/sync`,
			method: "POST",
			data: data ?? {}
		});
	}
};

/** 养老金人员档案 */
export type PensionPersonPayload = {
	name: string;
	scheme: string;
	salary: number;
	birth_date?: string | null;
	retire_date?: string | null;
	gender?: string | null;
	post_type?: string | null;
	contribution_years?: number;
	personal_account_balance?: number;
	auto_balance?: boolean;
	deemed_years?: number;
	deemed_index?: number | null;
	annuity_balance?: number;
	enterprise_annuity_balance?: number;
	private_pension_balance?: number;
	flexible?: boolean;
	resident_base?: number | null;
	note?: string | null;
};

/** 养老金人员档案 */
export const pensionPersonApi = {
	list(params?: any) {
		return request<any[]>({
			url: "/pension-persons",
			params
		});
	},

	create(data: PensionPersonPayload) {
		return request<any>({
			url: "/pension-persons",
			method: "POST",
			data
		});
	},

	update(id: number, data: Partial<PensionPersonPayload>) {
		return request<any>({
			url: `/pension-persons/${id}`,
			method: "PUT",
			data
		});
	},

	remove(id: number) {
		return request<any>({
			url: `/pension-persons/${id}`,
			method: "DELETE"
		});
	}
};

/** 养老金参数配置 */
export const pensionParamsApi = {
	get() {
		return request<any>({ url: "/pension-params" });
	},

	update(data: any) {
		return request<any>({
			url: "/pension-params",
			method: "PUT",
			data
		});
	},

	/** 参保地区及其计发基数 */
	regions() {
		return request<any[]>({ url: "/pension-params/regions" });
	},

	/** 恢复政策默认值 */
	reset() {
		return request<any>({
			url: "/pension-params/reset",
			method: "POST"
		});
	}
};

/** 收支管理 */
export const incomeExpenseApi = {
	list(params?: any) {
		return request<any[]>({
			url: "/income-expense",
			params
		});
	},

	detail(id: number) {
		return request<any>({ url: `/income-expense/${id}` });
	},

	create(data: IncomeExpensePayload) {
		return request<any>({
			url: "/income-expense",
			method: "POST",
			data
		});
	},

	update(id: number, data: Partial<IncomeExpensePayload>) {
		return request<any>({
			url: `/income-expense/${id}`,
			method: "PUT",
			data
		});
	},

	remove(id: number) {
		return request<any>({
			url: `/income-expense/${id}`,
			method: "DELETE"
		});
	}
};
