import { type PluginConfig } from "@/.cool";
import { router } from "@/.cool";
import { isLogin } from "@/api/request";

export default {
	install(app) {
		/**
		 * 路由跳转前的全局钩子
		 * 本项目为财务管理应用，除登录页外所有页面均需登录态。
		 * （框架默认的 user.isNull() 依赖 /app/user/info/person 接口，本项目后端无此接口，故改为校验本地 token）
		 */
		router.beforeEach((to, from, next) => {
			// 登录页直接放行，避免重定向死循环
			if (to.path == "/pages/user/login") {
				next();
				return;
			}

			// 未登录则跳转登录页
			if (!isLogin()) {
				router.login();
				return;
			}

			next();
		});
	}
} as PluginConfig;
