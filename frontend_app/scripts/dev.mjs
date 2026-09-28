/**
 * 不依赖 HBuilder X 的 H5 开发、构建与产物预览入口。
 *
 * uni-app x CLI 默认把项目源码放在 src/，但本项目的 App.uvue、pages.json 等文件
 * 位于项目根目录，所以必须在加载编译器之前显式设置 UNI_INPUT_DIR。
 */

import { existsSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const require = createRequire(import.meta.url);
const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const supportedModes = new Set(["dev", "build", "preview"]);
const mode = supportedModes.has(args[0]) ? args.shift() : "dev";

function optionValue(name, fallback) {
	const index = args.indexOf(`--${name}`);

	if (index >= 0 && args[index + 1] && !args[index + 1].startsWith("--")) {
		return args[index + 1];
	}

	return fallback;
}

async function runPreview() {
	const outDir = resolve(projectRoot, optionValue("outDir", "dist/build/h5"));
	const indexFile = resolve(outDir, "index.html");

	if (!existsSync(indexFile)) {
		console.error(`未找到 H5 构建产物：${indexFile}`);
		console.error("请先执行 npm run build:h5");
		process.exit(1);
	}

	const { preview } = await import("vite");
	const port = Number(optionValue("port", process.env.PORT || 4176));
	const host = optionValue("host", process.env.HOST || "127.0.0.1");
	const server = await preview({
		configFile: false,
		root: projectRoot,
		build: { outDir },
		preview: { host, port, strictPort: false }
	});

	server.printUrls();
	console.log("\nH5 构建产物预览已启动。");
}

function runUniCli() {
	const uniCli = require.resolve("@dcloudio/vite-plugin-uni/bin/uni.js");
	const cliArgs = mode === "build" ? ["build", "-p", "h5", ...args] : ["-p", "h5", ...args];
	const child = spawn(process.execPath, [uniCli, ...cliArgs], {
		cwd: projectRoot,
		env: {
			...process.env,
			UNI_INPUT_DIR: process.env.UNI_INPUT_DIR || projectRoot
		},
		stdio: "inherit"
	});

	child.on("error", (error) => {
		console.error("H5 编译进程启动失败：", error);
		process.exit(1);
	});

	child.on("exit", (code, signal) => {
		if (signal) {
			process.kill(process.pid, signal);
			return;
		}

		process.exit(code ?? 1);
	});
}

if (mode === "preview") {
	await runPreview();
} else {
	runUniCli();
}
