import { type PluginConfig } from "@/.cool";
import { vibrate } from "@/uni_modules/cool-vibrate";

export default {
	install(app: VueApp) {
		uni.$on("cool.vibrate", (duration: number | null) => {
			vibrate(duration ?? 1);
		});
	}
} as PluginConfig;
