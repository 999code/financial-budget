import { config } from "@/config";

/**
 * 财务管家 App 请求层
 *
 * 说明：框架内置 request() 约定后端返回 { code: 1000, message, data }，
 * 且 Authorization 不带 Bearer 前缀，与本项目后端（FastAPI：直接返回业务数据、
 * 使用 Bearer Token）不兼容，因此这里实现一套轻量适配层。
 * 同时兼容 H5（走 vite 代理）、App 与小程序（直连 baseUrl）三端。
 */

// token 存储 key
const TOKEN_KEY = "fm_token";

// 用户信息存储 key
const USER_KEY = "fm_user";

/**
 * 获取本地 token
 */
export function getToken(): string {
	const v = uni.getStorageSync(TOKEN_KEY) as string | null;
	return v == null ? "" : v;
}

/**
 * 保存 token
 */
export function setToken(token: string) {
	uni.setStorageSync(TOKEN_KEY, token);
}

/**
 * 清除 token
 */
export function removeToken() {
	uni.removeStorageSync(TOKEN_KEY);
}

/**
 * 是否已登录
 */
export function isLogin(): boolean {
	return getToken() != "";
}

/**
 * 保存/获取用户信息
 */
export function setUser(user: any) {
	uni.setStorageSync(USER_KEY, user);
}

export function getUser(): any | null {
	return uni.getStorageSync(USER_KEY) as any | null;
}

export function removeUser() {
	uni.removeStorageSync(USER_KEY);
}

// 请求参数
export type RequestOptions = {
	url: string; // 接口地址，如 "/auth/login"
	method?: "GET" | "POST" | "PUT" | "DELETE"; // 请求方法
	data?: any; // 请求体
	params?: any; // URL 参数
	header?: any; // 自定义请求头
	timeout?: number; // 超时时间
};

// 请求错误
export type RequestError = {
	message: string;
	code?: number;
};

/**
 * 拼接 URL 参数
 */
function stringify(params: any): string {
	if (params == null) {
		return "";
	}

	const keys = Object.keys(params);
	const list: string[] = [];

	for (let i = 0; i < keys.length; i++) {
		const k = keys[i];
		const v = params[k];

		// 注意用 !== 严格比较：宽松比较下 0 == "" 为真，会把 months=0 这类合法参数丢掉
		if (v != null && v !== "") {
			list.push(`${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`);
		}
	}

	return list.join("&");
}

/**
 * 发起请求
 */
export function request<T = any>(options: RequestOptions): Promise<T> {
	const { url, method = "GET", data = {}, params = {}, header = {}, timeout = 30000 } = options;

	// 拼接完整地址
	let u = url.startsWith("http") ? url : config.baseUrl + url;

	// 拼接 query
	const qs = stringify(params);
	if (qs != "") {
		u += (u.indexOf("?") >= 0 ? "&" : "?") + qs;
	}

	// token
	const token = getToken();

	return new Promise<T>((resolve, reject) => {
		uni.request({
			url: u,
			method,
			data,
			header: {
				"Content-Type": "application/json",
				...(token != "" ? { Authorization: `Bearer ${token}` } : {}),
				...header
			},
			timeout,

			success(res) {
				const status = res.statusCode;

				// 2xx 正常
				if (status >= 200 && status < 300) {
					resolve((res.data ?? null) as T);
					return;
				}

				// 401 未授权/登录失效
				if (status == 401) {
					removeToken();
					removeUser();
					reject({ message: "登录已失效，请重新登录", code: 401 } as RequestError);
					return;
				}

				// 其他错误，尝试取后端 detail
				let message = `请求失败(${status})`;
				const d = res.data as any;

				if (d != null && typeof d == "object") {
					if (typeof d.detail == "string") {
						message = d.detail;
					} else if (d.detail != null) {
						message = JSON.stringify(d.detail);
					} else if (typeof d.message == "string") {
						message = d.message;
					}
				}

				reject({ message, code: status } as RequestError);
			},

			fail(err) {
				reject({ message: err.errMsg ?? "网络异常，请稍后重试" } as RequestError);
			}
		});
	});
}

export default request;
