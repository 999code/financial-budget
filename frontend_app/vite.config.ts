import { defineConfig } from "vite";
import { cool } from "@cool-vue/unix";
import { proxy } from "./config/proxy";
import tailwindcss from "tailwindcss";
import { join } from "node:path";
import uni from "@dcloudio/vite-plugin-uni";

const resolve = (dir: string) => join(__dirname, dir);

for (const i in proxy) {
	proxy[`/${i}/`] = proxy[i];
}

export default defineConfig({
	plugins: [
		uni(),
		cool({
			proxy
		})
	],

	server: {
		// 注意：原端口 9900 落在本机 Windows 保留端口段（netsh 显示 9829-9928 被 Hyper-V/Docker 占用），
		// 启动会报 EACCES，故改为 5176。
		host: "127.0.0.1",
		port: 5176,
		proxy
	},

	css: {
		postcss: {
			plugins: [tailwindcss({ config: resolve("./tailwind.config.ts") })]
		}
	}
});
