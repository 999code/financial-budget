import { type PluginConfig } from "@/.cool";

// #ifdef H5
import TouchEmulator from "hammer-touchemulator";
// #endif

export default {
	install(app) {
		// #ifdef H5
		// 模拟移动端调试的触摸事件
		TouchEmulator();
		// #endif
	}
} as PluginConfig;
