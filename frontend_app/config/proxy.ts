export const proxy = {
	// 开发环境配置
	dev: {
		// 本地后端地址（FastAPI，端口 8000，接口前缀 /api/v1）
		target: "http://127.0.0.1:8000/api/v1",
		// 真机/局域网调试时，把上面的 127.0.0.1 换成电脑的局域网 IP，例如：
		// target: "http://192.168.1.100:8000/api/v1",
		changeOrigin: true,
		rewrite: (path: string) => path.replace("/dev", "")
	},

	// 生产环境配置
	prod: {
		// 生产后端域名（部署后改成真实域名）
		target: "http://127.0.0.1:8000",
		changeOrigin: true,
		rewrite: (path: string) => path.replace("/prod", "/api/v1")
	}
};

export const value = "dev";
