import { createSSRApp } from "vue";
import App from "./App.uvue";

// #ifdef H5
// 独立 UTS 编译器会把 Vue <script setup> 生成的属性描述符包装为
// UTSJSONObject。该类型自带 get 方法，与 value 同时传给原生
// Object.defineProperty 时会被浏览器判定为非法描述符。HBuilder X 内置
// 运行环境会处理这一差异；独立 H5 运行时在这里将它还原成普通描述符。
const nativeDefineProperty = Object.defineProperty.bind(Object);

Object.defineProperty = ((
	target: object,
	propertyKey: PropertyKey,
	attributes: PropertyDescriptor
) => {
	if (attributes?.constructor?.name == "UTSJSONObject") {
		const descriptor: PropertyDescriptor = {};

		for (const key of ["configurable", "enumerable", "value", "writable", "get", "set"]) {
			if (Object.prototype.propertyIsEnumerable.call(attributes, key)) {
				(descriptor as any)[key] = (attributes as any)[key];
			}
		}

		return nativeDefineProperty(target, propertyKey, descriptor);
	}

	return nativeDefineProperty(target, propertyKey, attributes);
}) as typeof Object.defineProperty;
// #endif

export function createApp() {
	const app = createSSRApp(App);

	return {
		app
	};
}
