# Cool Unix 组件库使用说明

> 本文档整理自 [Cool Unix](https://unix.cool-js.com/) 官方文档站（版本 8.1.0）。
> Cool Unix 是 cool-team-official 开源的 uni-app-x / 鸿蒙 uvue 组件库，支持多端（uni-app-x、鸿蒙、App、H5、小程序）、多语言、深色模式、tailwindcss 与 AI 编码。GitHub 仓库：<https://github.com/cool-team-official/cool-unix>。

## 特性概览

- **开源免费**：基于 MIT 协议，开箱即用。
- **多端一致**：基于 uni-app-x / uvue 语法，一套代码多端运行。
- **TypeScript 友好**：完整类型定义，组件 ref 调用带类型提示。
- **主题定制**：基于 tailwindcss，支持 CSS 变量与 PassThrough 样式穿透。
- **国际化**：内置多语言，支持 `unix-i18n create` 扩展。
- **图标体系**：内置图标库，支持自定义图标。
- **组件覆盖**：基础、表单、布局、数据、状态、反馈、其他共 7 大类 66 个组件。



## 目录

- [项目简介与快速开始](#项目简介与快速开始)
- [Cool Unix 框架简介](#cool-unix-框架简介)
- [快速开始指南](#快速开始指南)
- [组件库引入指南](#组件库引入指南)
- [主题与样式系统](#主题与样式系统)
- [国际化多语言](#国际化多语言)
- [图标配置指南](#图标配置指南)
- [组件开发指南](#组件开发指南)
- [PassThrough (pt) 属性](#passthrough-pt-属性)
- [版本更新 📚](#版本更新)
- [一、基础组件](#一基础组件)
- [二、表单组件](#二表单组件)
- [三、布局组件](#三布局组件)
- [四、数据组件](#四数据组件)
- [五、状态组件](#五状态组件)
- [六、反馈组件](#六反馈组件)
- [七、其他组件](#七其他组件)

---



## 项目简介与快速开始

## Cool Unix 框架简介

在移动互联网快速发展的今天，跨端应用开发已成为企业数字化转型的重要需求。Cool Unix 是一个现代化的跨端应用开发脚手架，基于 uni-app x 技术栈，为开发者提供了完整的解决方案，助力快速构建高质量、高性能的跨平台应用。

兼容平台：

| 平台 | 运行方式 | 预览效果 |
| --- | --- | --- |
| 🌐 **Web** | 点击运行到浏览器 | 实时热重载 |
| 📱 **App** | 连接真机调试 | 原生性能体验 |
| 💬 **微信小程序** | 微信开发者工具 | 小程序预览 |
| 🦋 **鸿蒙** | HarmonyOS 模拟器 | 系统级集成 |

### 开源共建

在 uni-app x 生态中，虽然存在众多收费的 UI 框架，但我们选择将 Cool Unix `完全开源`。我们相信，开源共享不仅能让更多开发者受益，也能吸引优秀的贡献者共同完善框架，推动 uni-app x 生态的繁荣发展。我们期待与社区一起，打造一个更加开放、活跃的跨端开发生态系统。

仓库地址：

| 平台 | 仓库地址 |
| --- | --- |
| **GitHub** | [cool-team-official/cool-unix](https://github.com/cool-team-official/cool-unix) |
| **Gitee** | [cool-team-official/cool-unix](https://gitee.com/cool-team-official/cool-unix) |

加入我们：

### 🛠️ 核心技术栈

采用业界领先的技术组合，确保项目的稳定性和可扩展性：

- [uni-app x](https://doc.dcloud.net.cn/uni-app-x/) - 新一代跨端开发框架，支持编译到多个平台
- [Vite](https://vite.dev/) - 极速构建工具，提供闪电般的开发体验

#### 🔧 服务能力

- Service 服务 - 统一的 API 请求管理和 Entity 类型

#### 🎨 UI 组件与样式

- uvue 组件库 - 原生级别的组件性能
- Tailwind CSS - 实用优先的 CSS 框架
- 多主题支持 - 自由切换主题色彩
- 深色模式 - 适配用户偏好设置

#### 🌐 国际化与图标

- 多语言切换 - 国际化应用必备
- 图标自动导入 - 支持 Iconfont 和 Remixicon

#### 🔐 多样化登录方式

- 微信小程序登录 - 无缝对接微信生态
- APP 微信登录 - 第三方授权登录
- 一键登录 - 运营商快速登录
- 短信验证码 - 传统可靠的登录方式

### 💡 开始使用

准备好开启高效的跨端开发之旅了吗？

👉 [立即开始](./quick.html) 查看详细的安装和配置指南

## 快速开始指南

### 开发环境推荐

为了获得最佳的开发体验，我们推荐使用以下工具：

- 代码编辑器 ： Cursor - AI 驱动的智能编辑器，提供强大的代码提示和生成功能
- 运行调试工具 ： HBuilderX - 专为 uni-app 优化的集成开发环境

### 获取项目代码

您可以通过以下任一方式克隆项目仓库：

#### GitHub

```bash
git clone https://github.com/cool-team-official/cool-unix.git
```

#### Gitee

```bash
git clone https://gitee.com/cool-team-official/cool-unix.git
```

### 安装与运行

#### 1. 安装依赖

进入项目根目录，安装项目依赖：

```bash
# 推荐使用 pnpm（更快，更节省空间）
pnpm i

# 或者使用其他包管理器
yarn
```

>
> **⚡ 性能提示**：推荐使用 `pnpm`，它具有以下优势：
>
>
> - 安装速度更快
> - 磁盘空间占用更少
> - 依赖管理更严格
>

#### 2. 启动项目

使用 [HBuilderX](https://www.dcloud.io/hbuilderx.html) 打开项目，即可运行到各个平台：

##### 支持的平台

- 🌐 H5 ：浏览器预览
- 📱 小程序 ：微信、支付宝、百度等各大小程序平台
- 📲 App ：Android、iOS 原生应用
- 🚀 鸿蒙 ：华为鸿蒙 App（ 查看详细文档 ）

##### 首次运行注意事项

>
> **📋 重要提示**：HBuilderX 首次运行时会自动安装必要的扩展插件，请注意查看控制台提示信息，确保所有插件安装完成。
>

#### 3. 开发模式

项目启动后，您可以：

- 实时预览代码修改效果
- 使用 HBuilderX 的调试功能
- 体验热重载带来的高效开发体验

### 下一步

恭喜！🎉 您已经成功启动了项目。接下来可以：

- 📖 阅读 组件文档 了解可用组件
- 🛠️ 查看 配置指南 自定义项目设置
- 🎨 学习 主题定制 打造独特风格
- 🔧 了解 兼容问题 避免开发陷阱
- 🔍 探索 Admin 对接指南 快速构建完整应用

## 组件库引入指南

如何在自己的项目中使用 cool-unix。

注意事项

- 独立组件库版本可能不包含部分功能，例如： canvas 绘制 、 震动 、 文件上传 等特性，请根据实际需求评估使用（项目版请移步 快速开始 ）。

### 配置文件

首先全局安装

```bash
npm install -g @cool-vue/unix-cli
```

或

```bash
pnpm add -g @cool-vue/unix-cli
```

然后在你的项目根目录下初始化配置

```bash
unix-init
```

执行完成后，所需的配置与依赖文件会被自动集成到你的项目中，无需手动操作。

如遇依赖未自动安装的情况，请手动执行以下命令

```bash
# 推荐使用 pnpm（更快，更节省空间）
pnpm i

# 或者使用其他包管理器
yarn
```

#### 2. 启动项目

使用 [HBuilderX](https://www.dcloud.io/hbuilderx.html) 打开项目，即可运行到各个平台

## 主题与样式系统

基于 [Tailwind CSS](https://tailwindcss.com/) 构建了完整的主题系统，提供灵活的样式定制能力和优雅的深色模式支持。

### 🎨 颜色系统

框架内置了完整的颜色体系，支持主题色和表面色的自由搭配：

主色 Primary

emerald、green、lime、orange、amber、yellow、teal、cyan、sky、blue、indigo、violet、purple、fuchsia、pink

表面色 Surface

slate、gray、zinc、neutral、stone、soho、viva、ocean

### ⚙️ 主题配置

通过 `tailwind.config.ts` 文件自定义主题配置：

```js
// tailwind.config.ts
export default {
	content: [resolve("./**/*.{uvue,vue}"), "!**/node_modules/**", "!**/dist/**"],
	darkMode: "class",
	theme: {
		extend: {
			colors: {
				...getPrimary("teal"), // 设置主色调
				...getSurface("zinc"), // 设置表面色调
			},
			// 自定义扩展配置
			fontSize: {
				md: ["1rem", "1.5rem"] // 自定义字体大小
			},
			scale: {
				"80": "0.8" // 自定义缩放比例
			},
		}
	},
	corePlugins: {
		preflight: false // 禁用默认样式重置
	}
} as Config;
```

#### 颜色配置说明

- 主色系 (Primary) : 用于品牌色彩、按钮、链接等主要交互元素
- 表面色系 (Surface) : 用于背景、边框、分割线等界面基础元素

### 📝 样式类使用指南

#### 布局与定位

```html
<!-- Flexbox 布局 -->
<view class="flex flex-col">纵向布局</view>
<view class="flex flex-row">横向布局</view>
<view class="flex flex-row items-center">垂直居中</view>
<view class="flex flex-row items-center justify-center">完全居中</view>
<view class="flex-1">弹性伸缩</view>
```

#### 尺寸设置

```html
<!-- 固定尺寸 -->
<view class="h-5 w-5">小尺寸</view>
<view class="h-full w-full">全尺寸</view>

<!-- 自定义尺寸 -->
<view class="h-[50rpx] w-[50rpx]">自定义 rpx</view>
<view class="h-[50px] w-[50px]">自定义 px</view>
<view class="h-80/100">百分比尺寸</view>
```

#### 间距与边距

```html
<!-- 内边距 -->
<view class="p-3">全方向内边距</view>
<view class="px-3">水平内边距</view>
<view class="py-3">垂直内边距</view>

<!-- 外边距 -->
<view class="m-3">全方向外边距</view>
<view class="mx-3">水平外边距</view>
<view class="my-3">垂直外边距</view>
```

#### 圆角与边框

```html
<!-- 圆角设置 -->
<view class="rounded-md">中等圆角</view>
<view class="rounded-lg">大圆角</view>
<view class="rounded-full">完全圆角</view>

<!-- 边框样式 -->
<view class="border border-solid border-surface-100">基础边框</view>
```

#### 文字样式

```html
<!-- 字体大小 -->
<view class="text-xs">超小字体</view>
<view class="text-md">中等字体</view>
<view class="text-lg">大字体</view>
<view class="text-xl">超大字体</view>

<!-- 文字颜色 -->
<view class="text-primary-50">主色文字</view>
<view class="text-surface-50">表面色文字</view>
<view class="text-center">居中对齐</view>

<!-- 自定义颜色 -->
<view class="text-[#ff0]">自定义颜色</view>
<view class="text-[30rpx]">自定义大小</view>
```

#### 强制样式 (!important)

```html
<!-- 使用 ! 前缀强制覆盖样式 -->
<view class="!text-surface-100">强制文字颜色</view>
<view class="!bg-white">强制背景色</view>
<view class="!border-surface-300">强制边框色</view>
```

### 🌙 深色模式

#### API 调用

```ts
import { isDark, toggleTheme, setIsAuto, setTheme } from "@/.cool";

// 状态检查
console.log(isDark.value); // 当前是否为深色模式

// 主题切换
toggleTheme(); // 切换深色/亮色模式

// 主题设置
setTheme("light"); // 设置为亮色模式
setTheme("dark"); // 设置为深色模式

// 自动模式（仅 APP 端有效）
setIsAuto(true); // 跟随系统主题
```

#### 样式适配

##### 方式一：使用 dark: 前缀

```html
<view class="bg-surface-100 dark:!bg-surface-900">
	<text class="text-surface-700 dark:!text-white">自适应文本</text>
</view>
```

>
> **💡 提示**: `dark:` 前缀后加 `!` 表示使用 `!important` 强制覆盖样式
>

##### 方式二：使用响应式变量

```html
<view class="bg-surface-100" :class="{ '!bg-surface-900': isDark }">
	<text class="text-surface-700" :class="{ '!text-white': isDark }">响应式文本</text>
</view>
```

#### 在 scss 中使用

```html
<style lang="scss" scoped>
	.custom-component {
		@apply text-md bg-primary-500;
		@apply h-10 w-10 fixed right-10 top-10;
	}
</style>
```

#### 在 script 中使用

```js
import { getColor } from "@/.cool";

getColor("primary-500"); // = text-primary-500
getColor("surface-500"); // = text-surface-500
```

### ⚠️ 重要注意事项

由于 uni-app x 的 [CSS 限制](https://doc.dcloud.net.cn/uni-app-x/css/)，在使用时需要注意以下几点：

📱 APP 端限制

**文字样式限制**: APP 中不能在 `view` 标签中使用字体相关的样式

```html
<!-- ❌ 错误用法 -->
<view class="text-md">文本内容</view>

<!-- ✅ 正确用法 -->
<text class="text-md">文本内容</text>
```

🔄 动态样式渲染

**父子样式联动**: APP 中动态修改父级样式时，子元素样式不会自动重新渲染

```html
<view class="box" :class="{ 'active': isActive }">
	<text class="text">文本</text>
</view>

<style lang="scss" scoped>
	.box {
		@apply bg-white;

		.text {
			@apply text-surface-700;
		}

		&.active {
			@apply bg-black; /* ✅ 生效 */

			.text {
				@apply text-white; /* ❌ 不生效 */
			}
		}
	}
</style>
```

**解决方案**: 为子元素单独添加响应式类名

```html
<view class="box" :class="{ 'active': isActive }">
	<text class="text" :class="{ 'active': isActive }">文本</text>
</view>

<style lang="scss" scoped>
	.box {
		@apply bg-white;

		.text {
			@apply text-surface-700;

			&.active {
				@apply text-white; /* ✅ 生效 */
			}
		}

		&.active {
			@apply bg-black;
		}
	}
</style>
```

### 🚀 最佳实践

1. 优先使用预设颜色 : 使用框架内置的 primary 和 surface 色系
2. 合理使用深色模式 : 为重要界面元素提供深色模式适配
3. 注意平台差异 : 了解不同平台的样式限制，编写兼容性代码
4. 保持一致性 : 在项目中统一使用 Tailwind CSS 类名，避免混用内联样式

### 📚 延伸阅读

- Tailwind CSS 官方文档
- uni-app x CSS 规范

## 国际化多语言

Cool Unix 内置强大的国际化插件，支持多语言切换和 AI 智能翻译，助力您的应用走向全球市场。

提示

框架自动扫描并加载所有 `locales` 目录下的语言资源文件。结合 AI 翻译工具，可实现多语言内容的快速生成，大大提升开发效率。

### 🌍 特性概览

- 🤖 AI 智能翻译 - 基于人工智能的自动翻译服务
- 🔄 动态语言切换 - 运行时无缝切换语言
- 📝 占位符支持 - 支持参数化翻译内容
- 🌐 广泛语言支持 - 内置 50+ 种语言配置

### ⚙️ 配置设置

#### 基础配置

在根目录的 `/plugins/locale.ts` 文件（不存在则手动创建）中配置需要支持的语言参数 `languages`

```js
import { initLocale, type PluginConfig } from "@/.cool";

export default {
	options: {
		// 支持的多语言代码列表，AI 将依据此列表生成对应的本地化文件
		languages: ["zh-cn", "zh-tw", "en", "es", "ja", "ko", "fr"]
	},

	install(app) {
		// 初始化多语言设置，"none" 表示优先跟随系统当前语言
		initLocale("zh-cn");
	}
} as PluginConfig;
```

重要说明

`languages` 参数的决定 AI 翻译时同时处理的语言数量。对于翻译不准确的内容，建议手动调整优化。

#### 不使用多语言

如果项目不需要多语言支持，直接删除 `/plugins/locale.ts` 文件即可，不会影响程序正常运行。

### 📝 使用指南

#### 基础用法

所有需要翻译的文本内容都需要使用 `t()` 或 `$t()` 函数包装：

```html
<!-- 模板中使用 -->
<text>{{ t('你好') }}</text>
<text>{{ $t('欢迎{name}', { name: '张三' }) }}</text>
```

#### 脚本中使用

```html
<script setup lang="ts">
	import { t, $t } from "/@/locale";

	// 基础翻译
	ui.showToast({
		message: t("操作成功")
	});

	// 参数化翻译
	ui.showToast({
		message: $t("欢迎回来，{name}", { name: "李四" })
	});
</script>
```

#### 函数说明

| 函数 | 语法 | 功能 | 使用场景 |
| --- | --- | --- | --- |
| `t()` | `t(text)` | 基础翻译 | 静态文本内容 |
| `$t()` | `$t(text, data)` | 参数化翻译 | 动态内容，支持占位符 |

为什么不使用可选参数 data? ，在 [帮助文档](/src/introduce/help.html) 中会说明。

### 🤖 AI 翻译工具

项目已默认集成相关工具依赖，只需在项目根目录下执行以下命令：

```bash
# 安装
pnpm add @cool-vue/unix-cli -g

# 创建/更新翻译文件
unix-i18n create

# 添加 uni_modules 下的语言
unix-i18n add uni_modules/[name]
```

#### 工作流程

1. 扫描源码 - 工具会自动扫描项目中的 t() 和 $t() 函数
2. 提取文本 - 收集所有需要翻译的中文文本
3. AI 翻译 - 调用 AI 服务翻译成目标语言
4. 生成文件 - 在相应目录下生成翻译文件

#### 输出结构

```text
locales/
    ├── zh-cn.json      # 简体中文
    ├── zh-tw.json      # 繁体中文
    ├── en.json         # 英语
    └── es.json         # 西班牙语
```

### 🌐 支持的语言

#### 主要语言

| 语言 | 代码 | 地区 |
| --- | --- | --- |
| 简体中文 | `zh-cn` ` | 中国大陆 |
| 繁体中文 | `zh-tw` | 中国台湾 |
| 英语 | `en` | 美国 |
| 日语 | `ja` | 日本 |
| 韩语 | `ko` | 韩国 |

#### 欧洲语言

| 语言 | 代码 | 语言 | 代码 |
| --- | --- | --- | --- |
| 德语 | `de` | 法语 | `fr` |
| 西班牙语 | `es` | 意大利语 | `it` |
| 葡萄牙语 | `pt` | 荷兰语 | `nl` |
| 俄语 | `ru` | 波兰语 | `pl` |
| 瑞典语 | `sv` | 丹麦语 | `da` |
| 挪威语 | `nb-NO` | 芬兰语 | `fi` |
| 希腊语 | `el` | 捷克语 | `cs` |
| 匈牙利语 | `hu` | 罗马尼亚语 | `ro` |

#### 其他地区语言

**点击查看完整语言列表**

| 语言 | 代码 | 语言 | 代码 |
| --- | --- | --- | --- |
| 阿拉伯语 | `ar` | 希伯来语 | `he` |
| 土耳其语 | `tr` | 波斯语 | `fa` |
| 泰语 | `th` | 越南语 | `vi` |
| 印度尼西亚语 | `id` | 马来语 | `ms` |
| 孟加拉语 | `bn` | 泰米尔语 | `ta` |
| 乌克兰语 | `uk` | 保加利亚语 | `bg` |
| 克罗地亚语 | `hr` | 塞尔维亚语 | `sr` |
| 斯洛伐克语 | `sk` | 斯洛文尼亚语 | `sl` |
| 立陶宛语 | `lt` | 拉脱维亚语 | `lv` |
| 爱沙尼亚语 | `et` | 加泰罗尼亚语 | `ca` |
| 巴斯克语 | `eu` | 世界语 | `eo` |
| 库尔德语 | `ku` / `ckb` | 亚美尼亚语 | `hy-am` |
| 阿塞拜疆语 | `az` | 哈萨克语 | `kk` |
| 吉尔吉斯语 | `ky` | 蒙古语 | `mn` |
| 土库曼语 | `tk` | 维吾尔语 | `ug-cn` |
| 高棉语 | `km` | 南非荷兰语 | `af` |
| 普什图语 | `pa` | 巴西葡萄牙语 | `pt-br` |

## 图标配置指南

本框架支持主流图标库：[iconfont](https://www.iconfont.cn/) 和 [remixicon](https://remixicon.com/) 等，您可以轻松集成自定义图标。

### 1. 选择图标

#### iconfont 图标库

在 iconfont 平台选择所需图标后，点击 `⬇️ 下载至本地` 按钮获取图标包。

#### remixicon 图标库

在 remixicon 平台选择图标后，点击 `⬇️ Fonts` 按钮下载。

### 2. 安装图标包

将下载的 `zip` 压缩包放置到项目根目录的 `/icons/` 文件夹下。

命名提示

命名 zip 文件，避免使用特殊符号（如 `+-=.\@`），建议格式：`icon-project.zip`

### 3. 构建图标

在项目根目录打开终端，执行以下命令：

```bash
# 安装
pnpm add @cool-vue/unix-cli -g

# 执行
pnpm unix-icons
```

执行成功后，图标将自动集成到项目 `/.cool/icons` 中，无需引入可直接使用。

### 4. 使用图标

图标的 `name` 属性与图标库中的名称一一对应，使用时请注意：

- 避免命名冲突 ：建议为自定义图标添加项目前缀
- 保持一致性 ：统一图标命名规范

#### 基础用法

```html
<cl-icon name="home-line"></cl-icon>
```

#### 自定义前缀示例

自定义前缀规则可以在各个图标库平台中配置。

```html
<!-- 推荐：使用项目前缀避免冲突 -->
<cl-icon name="project-custom-icon"></cl-icon>
```

## 组件开发指南

本文档详细介绍了组件开发的规范和注意事项，建议仔细阅读以确保开发质量。

### 开发规范

#### 基础规范

- 样式设置 ：不要在自定义组件上直接添加 class 属性，不同平台存在兼容性问题。推荐使用 pt 参数进行样式定制
- 标签闭合 ：所有组件都必须使用双闭合标签格式

```html
<!-- 正确写法 -->
<image></image>
<cl-image></cl-image>

<!-- 错误写法 -->
<image />
<cl-image />
```

### 调用组件方法

#### 使用方式

以 `cl-popup` 组件为例，演示如何通过 ref 调用组件内部方法：

```html
<cl-popup ref="popupRef"></cl-popup>

<!-- 在其他组件中使用 ref 的属性 -->
<cl-input :autofocus="popupRef!.isOpen"></cl-input>

<script lang="ts" setup>
  import { ref } from "vue";

  // 定义 ref，类型格式：组件名 + ComponentPublicInstance
  const popupRef = ref<ClPopupComponentPublicInstance | null>(null);

  // 调用组件方法（注意使用 ! 符号）
  function openPopup() {
    popupRef.value!.open();
  }
</script>
```

#### 注意事项

- 类型定义 ：必须严格按照 组件名 + ComponentPublicInstance 格式， null 联合类型不可省略
- 调用时机 ：避免在页面未完全加载时调用组件方法
- 安全调用 ：使用 ! 操作符确保调用时 ref 已被正确赋值

## PassThrough (pt) 属性

### 概念介绍

PassThrough 是一种用于访问组件内部 DOM 结构的 API，它允许开发者将任意属性和监听器直接应用于组件内部的 DOM 元素。这种设计的核心优势在于突破了组件主要 API 的限制，提供更灵活的定制能力。

#### 组件的局限

在传统的组件开发中，每个样式需求都需要单独的参数支持：

```html
<!-- 圆角样式 -->
<test rounded></test>

<!-- 圆角大小 -->
<test :rounded="10"></test>

<!-- 字体样式 -->
<test :font-size="14" font-color="#fff"></test>

<!-- 图标颜色 -->
<test icon-color="#fff"></test>

<!-- 外边距 -->
<test margin="10rpx"></test>

<!-- 复杂外边距 -->
<test :margin="[10, 0, 0, 10]"></test>
```

这种方式导致：

- 组件参数数量急剧增长
- 内部逻辑复杂度提升
- 维护成本居高不下
- 扩展性受限

#### 解决方案

使用 `pt` 参数，可以灵活定制组件样式：

##### 圆角设置

```html
<!-- 基础圆角 -->
<test :pt="{ className: 'rounded' }"></test>

<!-- 指定圆角大小 -->
<test :pt="{ className: 'rounded-md' }"></test>
<test :pt="{ className: 'rounded-[10rpx]' }"></test>
```

##### 文字样式

```html
<!-- 字体大小 -->
<test :pt="{ className: 'text-md' }"></test>
<test :pt="{ className: 'text-[28rpx]' }"></test>

<!-- 字体颜色 -->
<test :pt="{ className: 'text-white' }"></test>
<test :pt="{ className: 'text-[#fff]' }"></test>
```

##### 复合样式

```html
<!-- 图标和文字不同颜色 -->
<test
	:pt="{
		className: 'text-white',
		icon: { className: 'text-black' }
	}"
></test>
```

###### 间距设置

```html
<!-- 统一外边距 -->
<test :pt="{ className: 'm-2' }"></test>

<!-- 方向性外边距 -->
<test :pt="{ className: 'ml-2 mt-2 mb-2 mr-2' }"></test>
```

#### 优势总结

- 灵活性 ：支持任意 CSS 类名和样式，配合 tailwindcss 简直完美
- 可扩展性 ：无需修改组件即可实现新的样式需求
- 维护性 ：减少组件内部参数和逻辑复杂度
- 一致性 ：统一的样式定制方式

### 使用说明

#### PassThroughProps

```ts
type PassThroughProps = {
	className?: string;
};
```

#### 示例

每个组件的 `pt` 可选参数都有详细说明。以 `cl-button` 的 `PassThrough` 为例：

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| label | 文本标签样式 | [PassThroughProps](#passthroughprops) |
| icon | 图标元素样式 | [ClIconProps](/src/components/basic/icon.html#passthrough) |
| loading | 加载动画样式 | [ClLoadingProps](/src/components/basic/loading.html#passthrough) |

具体使用方式如下（在 VS Code 中点击类型链接可查看完整的参数说明和智能提示）：

```html
<cl-button
	:pt="{
		className: '!rounded-2xl',
		icon: {
			size: 50,
			className: 'mr-5'
		},
		label: {
			color: 'red',
			className: 'font-bold'
		},
		loading: {
			size: 50
		}
	}"
>
  点击
</cl-button>
```

`className` 支持字符串类型，如需动态样式可使用 `parseClass` 辅助函数：

```html
<cl-button
	:pt="{
		className: parseClass([
			[isDark, '!bg-white', '!bg-black'], // 条件判断：[条件, 真值样式, 假值样式]

			// 支持字符串和对象语法（与 :class 用法一致）
			'!rounded-2xl p-5',
			{
				'mr-2': isActive
			}
		])
	}"
>
  点击
</cl-button>
```

## 版本更新 📚

感谢您对 cool-unix 的关注与支持！我们致力于为开发者提供更好的开发体验，持续迭代优化产品功能。

如果本项目对您有所帮助，欢迎点击 ⭐ **Star** 支持我们，这将是我们前进路上最大的动力！

- [欢迎在 uniapp 插件市场为我们点赞支持](https://ext.dcloud.net.cn/plugin?id=24497#rating)
- [欢迎在 GitHub 上为我们点 Star](https://github.com/cool-team-official/cool-unix)

### v8.1.0 - 2026.1.18

- [功能] 新增“宽屏”支持，默认单位由 rpx 调整为 px ，提升显示适配性
- [功能] 增加插件机制 plugins ，支持自动加载，扩展更灵活
- [功能] 目录结构优化，将 /cool 调整为 /.cool
- [功能] 国际化目录更名，统一由 /locale 改为 /locales
- [功能] 核心代码优化，支持自动引入，无需手动导入
- [功能] 新增底部导航栏组件 cl-tabbar
- [功能] 优化并升级 unix-i18n 、 unix-ui-types 、 unix-icons 命令的使用体验和功能完善
- [优化] 解决 cl-cropper 在 APP 端首次加载图片时出现模糊的问题
- [优化] 修复 cl-text 在多端下的对齐异常
- [优化] 修复 cl-input 在 APP 端 placeholder 字体大小异常问题
- [优化] 修复 cl-icon 在多端下的对齐异常
- [优化] 修复 cl-button 在 IOS 端 light 按下样式异常问题
- [优化] 优化 cl-picker-view 在不同端的样式一致性
- [优化] 解决 tailwind 部分符号如 > | 渲染异常问题

### v8.0.31 - 2025.12.02

- [功能]更新 icon 脚本
- [优化]修复 cl-select 组件在异步获取 options 时不显示数据的问题，以及仅有单个选项时无法正确触发更新值的问题
- [优化]修复 cl-noticebar 在 鸿蒙 端动画无效问题
- [优化]修复 cl-tabs 在 鸿蒙 端下划线不显示问题
- [优化]修复 cl-popup 在拖动关闭位置错误问题
- [优化]修复 cl-textarea 在 鸿蒙 端不弹出键盘问题
- [优化]修复 cl-switch 在 IOS 端切换 disabled 被隐藏问题
- [优化]修复 cl-input-opt 光标动画重复创建问题
- [优化]修复 cl-input 在 鸿蒙 端不弹出键盘问题
- [优化]修复 cl-input 参数 clear 在 IOS 端失效问题
- [优化]修复 cl-input-opt 在 鸿蒙 端边框不显示问题
- [优化]修复 cl-float-view 禁用不生效问题
- [优化]修复 cl-float-view 拖动错位问题
- [优化]修复 cl-textarea 在 鸿蒙 端不弹出键盘问题
- [优化]修复 cl-calendar-select 在 mode=range 确认选择时错误提示的问题
- [优化]修复 cl-watermark 在 IOS 端不生效问题
- [优化]优化 cl-list-item 左右滑动
- [优化]修复 cl-topbar 层级过低问题
- [优化]修复 cl-picker-view 在 IOS 错位问题，默认 itemHeight=50
- [优化]修复 tailwindcss 隔离问题（更新依赖 @cool-vue/vite-plugin@8.2.19）

### v8.0.30 - 2025.11.10

- [功能]添加 cool-share 系统分享插件
- [优化]优化 router.query 取值
- [优化]修复 cl-banner 1处bug、优化手势操作、增加touch代理功能
- [优化]修复 cl-input-number 在特殊情况下输入框高度不一致问题
- [优化]修复 cl-select-date 初始值未显示问题
- [优化]修复 cl-text 设置超大号字体时导致的多行重叠和web端显示不全的问题
- [优化] cl-form-item 支持根据规则自动判断必填状态
- [优化] cl-input 添加数字输入精度控制功能
- [优化][脚本]支持读取 iconfont 图标前缀并生成对应ts文件

### v8.0.29 - 2025.10.28

- [功能]添加 商品详情 模板页面
- [优化]优化 router.query 取值
- [优化] cl-banner 添加 image-mode 参数
- [优化]修复 cl-tabs 底横线位置异常问题
- [优化] cl-calendar 添加颜色、大小等参数

### v8.0.28 - 2025.10.26

- [功能]添加 cl-watermark 水印组件
- [优化]解决打包后 cl-icon 颜色异常问题

### v8.0.27 - 2025.10.21

- [功能]添加帖子详情模板
- [优化] cl-list-item 组件添加 pt.wrapper 参数
- [优化] cl-topbar 组件添加 backable 控制返回按钮是否可用
- [优化] cl-select 组件添加空选项提示
- [优化] isPressing 修改为 ref<boolean>
- [优化] usePage() 添加 offScroll 方法
- [优化]修复 cl-timeline-item 时间线不显示问题
- [优化]解决 :deep 失效问题

### v8.0.26 - 2025.10.15

- [优化]修复 cl-popup 关闭按钮在小程序端的兼容问题
- [优化]修复了在 HBuilder 新版本中， cl-banner 组件第三张及之后的图片无法显示的问题
- [优化]修复 cool-vibrate 鸿蒙权限文件书写错误问题
- [优化]修复 easycom 解析异常的问题
- [优化]优化 cl-cascader 选择效果
- [优化] cl-calendar-select 添加提示
- [优化] cl-calendar 支持配置 start 、 end 可选日期
- [优化]修复 cl-select-date 组件在范围选择模式下首次渲染时内容未显示的问题
- [优化]优化 router ，支持 isAuth ，并添加示例
- [优化]解决 Illegal '/' in tags 异常

### v8.0.25 - 2025.09.18

- [功能]组件库现已独立发布，欢迎前往 插件市场 查看与体验
- [优化]解决 cl-read-more 动态内容不显示展开问题
- [优化]解决 cl-input-opt 在小程序兼容问题
- [优化]解决 router/index.ts 路径判断错误问题

### v8.0.24 - 2025.09.13

- [优化] locale 现已支持自定义语言配置，详情请见 文档
- [优化] cl-calendar 日历设置自定义语言
- [优化] cl-text 参数 lines 修改为仅在 ellipsis 时生效
- [功能] 添加 cl-marquee 跑马灯组件
- [功能] 添加 cl-read-more 查看更多组件
- [优化] cl-footer 添加 pt 参数，默认 overflow-visible

### v8.0.23 - 2025.09.11

- [优化]解决图标脚本命名不一致问题
- [优化]鸿蒙圆形进度条显示异常问题
- [优化] cl-countdown 添加 auto 参数
- [优化] cl-calendar 支持添加上下文案

### v8.0.22 - 2025.09.09

- [功能]添加 cl-calendar 组件
- [优化]添加 dayUts 方法
- [优化] cl-text 支持多行省略号

### v8.0.21 - 2025.09.08

- [功能]添加 animation 动画库，优化组件动画
- [优化] cl-text 组件的字体大小和颜色，在 pt 配置中无需添加 ! 符号
- [优化] cl-list-item 组件添加 image 参数，添加 slot

### v8.0.21 - 2025.09.08

- [功能]添加 animation 动画库，优化组件动画
- [优化] cl-text 组件的字体大小和颜色，在 pt 配置中无需添加 ! 符号
- [优化] cl-list-item 组件添加 image 参数，添加 slot

### v8.0.20 - 2025.09.05

- [功能]添加 cl-tree 树形组件，支持 multiple 多选
- [优化]解决 ios 端 cl-cropper 高和宽为 0 时不触发 load 事件
- [优化]解决 ios 端 cl-draggable 拖动异常问题
- [优化]解决 ios 端 cl-loading 旋转动画异常问题
- [优化]解决 ios 端底部自定义栏不显示问题
- [优化]解决 ios 端图标异常?问题
- [优化]解决鸿蒙 svg 渲染问题

### v8.0.19 - 2025.08.28

- [功能]添加 cl-slide-verify 滑动验证组件，支持图片转正

### v8.0.18 - 2025.08.27

- [优化]弃用 service 请求，重新设计了 request 请求方案
- [优化]用户信息绑定方式更改为 userInfo
- [优化]更新依赖 @cool-vue/vite-plugin 版本 8.2.9

### v8.0.17 - 2025.08.26

- [功能]新增 useWx() 方法，支持微信小程序登录等功能
- [功能]新增微信小程序登录模板，首次登录时提示基本信息的修改

### v8.0.16 - 2025.08.25

- [功能]添加 cl-svg 组件，支持 base64 、 本地文件 、 svg标签
- [优化]多语言方案已优化，成功解决 APP 端 Method too large 的问题， cool-ui 语言包现已独立分离
- [优化]更新依赖 @cool-vue/ai 版本 1.1.6
- [优化]更新依赖 @cool-vue/vite-plugin 版本 8.2.7

### v8.0.15 - 2025.08.22

- [功能]添加 cl-filter-item 筛选栏组件

### v8.0.14 - 2025.08.21

- [优化]修复 cl-picker-view 边界值溢出的问题
- [优化]修复 cl-select 和 cl-select-time 打开时未设置当前值的问题
- [优化]修复 cl-select 和 cl-select-time 中 text 显示异常的问题

### v8.0.13 - 2025.08.21

- [功能]添加 购物车 和 商品分类 模板页
- [优化]解决 cl-text 参数 size 未生效问题
- [优化]解决小程序上 cl-badge 字体样式失效问题
- [优化]解决 cl-input-number 首次触发 onChange 的问题
- [优化]解决 cl-input 事件丢失问题
- [优化]解决 cl-select-date 快捷按钮需点击两次的问题
- [优化]解决 cl-noticebar 等待时间过长显示的问题

### v8.0.10 - 2025.08.19

- [功能]添加 cl-canvas 组件，支持图片裁剪、文字多行省略、变形转换等功能
- [优化]解决 cl-topbar 的 pt 和 background-color 互斥问题

### v8.0.9 - 2025.08.15

- [功能] cl-form 支持动态表单验证，如 prop="contacts[0].phone"
- [功能] cl-form-item 支持配置 rules 参数

### v8.0.8 - 2025.08.13

- [功能]新增全局字号设置功能，支持动态调整文字大小，适用于 cl-text 和 cl-icon 组件

### v8.0.7 - 2025.08.12

- [功能]添加纯净版本， 文档
- [功能] cl-form 表单验证组件支持滚动到错误位置
- [功能] cl-form 表单内组件支持红框错误提示
- [功能]重新实现 usePage() ，支持监听页面滚动及跳转等事件
- [功能] cl-list-view 添加下拉刷新功能
- [功能]添加 usePager() 页面刷新操作
- [功能]添加 cl-back-top 回到顶部组件
- [优化]优化 cl-button cl-loading 组件颜色的控制
- [优化]优化 cl-select-date 组件的选择操作体验（不回到首个）

### v8.0.6 - 2025.08.06

- [功能]添加 cl-form 、 cl-form-item 表单验证组件
- [功能] cl-select-time 支持类型选择
- [修复] cl-select-date 文本无法清空问题
- [优化] useParent 方法支持 useParent<ClFormComponentPublicInstance>('cl-form') 类型定义和目标组件名
- [优化]补充多语言

### v8.0.5 - 2025.08.03

- [功能]添加 cl-cropper 图片裁剪组件
- [修复] cl-popup 内容区域去掉滑动事件
- [修复] locale-set 点击掉帧问题
- [修复] canvasToPng 参数优化，仅需一个 canvasRef
- [优化]登录页细节调整
- [优化]补充多语言
- [优化]画布高清处理

### v8.0.4 - 2025.07.29

- [功能] cl-slider 支持范围选择
- [功能]添加 cl-sign 签名组件
- [修复]优化导出图片方法
- [修复]解决多语言切换时部分组件文案不更新

### v8.0.3 - 2025.07.28

- [功能]添加 cl-draggable 拖拽排序组件

### v8.0.2 - 2025.07.26

- [修复] cl-popup 关闭按钮按下体验
- [功能]添加 cl-progress-circle 圆形进度条组件

### v8.0.1 - 2025.07.25

- [修复]切换多语言 tabbar 组件无法更新
- [修复] cl-confirm 组件深色字体不显示
- [修复]页面无法注释，更新依赖 @cool-vue/vite-plugin

### 🎉 v8.0.0 - 2025.07.21

#### 🚀 重大更新

本次版本带来了激动人心的全新特性：

- 🌍 多语言支持 - 让您的应用面向全球用户 → 查看详情
- 🌙 深色模式 - 提供舒适的夜间使用体验 → 查看详情

#### 📱 平台兼容性

- ✅ 鸿蒙系统 - 全面适配华为鸿蒙生态
- ✅ 微信小程序 - 完美支持小程序开发
- ✅ Android - 原生 Android 应用支持
- ✅ iOS - 完美适配苹果生态系统

---

>
> 💡 **提示**：如果您在使用过程中遇到任何问题，欢迎通过 [Issues](https://github.com/cool-team-official/cool-unix/issues) 反馈给我们！
>


## 一、基础组件

### Page 页面

cl-page 组件是一个基础的页面容器组件。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| backTop | 是否显示回到顶部 | boolean | - | true |

**示例：使用示例**

```html
// 显示确认弹窗
ui.showConfirm({
	title: "提示",
	message: "确定要提交吗？"
});

// 显示提示信息
ui.showTips("订单已结算成功", () => {
	router.back();
});

// 显示 Toast 消息
ui.showToast({
	message: "Hello"
});

// 显示 Loading
ui.showLoading("加载中");

// 隐藏 Loading
ui.hideLoading();
```

**示例：使用示例**

```html
<template>
	<cl-page @scroll="onScroll"></cl-page>
</template>

<script lang="ts" setup>
	const onScroll = (top: number) => {
		console.log(`页面滚动距离: ${top}px`);
	};
</script>
```

### Button 按钮

基于官方 button 组件封装的增强按钮组件，支持多种样式主题、尺寸规格和交互状态，提供更丰富的视觉效果和用户体验。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| size | 按钮尺寸 | string | "normal" \| "small" \| "large" | "normal" |
| type | 按钮主题类型 | string | "primary" \| "success" \| "error" \| "warn" \| "info" \| "light" \| "dark" | "primary" |
| text | 是否为纯文本按钮 | boolean |  | false |
| border | 是否显示边框 | boolean |  | false |
| rounded | 是否显示圆角 | boolean |  | false |
| loading | 是否显示加载状态 | boolean |  | false |
| disabled | 是否禁用按钮 | boolean |  | false |
| icon | 图标名称 | string |  |  |
| color | 自定义文字颜色 | string |  |  |
| fluid | 是否为 flex-1 布局 | boolean |  | false |

<!-- 更多参数查阅：https://doc.dcloud.net.cn/uni-app-x/component/button.html -->

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| label | 文本元素配置 | ClTextProps |
| icon | 图标元素配置 | ClIconProps |
| loading | 加载元素配置 | ClLoadingProps |

**示例：基础用法**

最简单的按钮用法，显示默认样式。

```html
<cl-button>普通按钮</cl-button>
```

**示例：主题类型**

通过 type 参数设置不同的按钮主题，适用于不同的场景。

```html
<cl-button type="primary">主要按钮</cl-button>
<cl-button type="success">成功按钮</cl-button>
<cl-button type="error">危险按钮</cl-button>
<cl-button type="warn">警告按钮</cl-button>
<cl-button type="info">信息按钮</cl-button>
<cl-button type="light">浅色按钮</cl-button>
<cl-button type="dark">深色按钮</cl-button>
```

**示例：按钮尺寸**

通过 size 参数控制按钮的大小。

```html
<cl-button size="small">小号按钮</cl-button>
<cl-button size="normal">常规按钮</cl-button>
<cl-button size="large">大号按钮</cl-button>
```

### Text 文本

cl-text 文本组件，支持多种文本类型展示，包括手机号、金额、内容超出省略等功能，并提供数据脱敏能力。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| value | 文本内容 | string |  |  |
| color | 字体颜色 | string | "primary" \| "success" \| "error" \| "warn" \| "info" |  |
| type | 文本类型 | string | "default" \| "phone" \| "name" \| "amount" \| "card" \| "email" | "default" |
| size | 字体大小(px) | number |  | 14 |
| mask | 是否开启脱敏处理 | boolean |  | false |
| currency | 金额货币符号 | string |  | "¥" |
| precision | 金额小数位数 | number |  | 2 |
| maskStart | 脱敏起始位置 | number |  | 3 |
| maskEnd | 脱敏结束位置 | number |  | 4 |
| maskChar | 脱敏替换字符 | string |  | "*" |
| ellipsis | 是否启用省略号显示 | boolean |  | false |
| lines | 最大行数，只在 ellipsis 启用有效 | number |  | 1 |
| selectable | 是否允许选择文本 | boolean |  | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

**示例：基础用法**

显示普通文本内容：

```html
<cl-text>云想衣裳花想容，春风拂槛露华浓。</cl-text>
```

**示例：设置文字颜色**

通过 color 参数设置不同的文字颜色：

```html
<cl-text color="primary">主色调文字</cl-text>
<cl-text color="success">成功状态文字</cl-text>
<cl-text color="error">错误状态文字</cl-text>
<cl-text color="warn">警告状态文字</cl-text>
<cl-text color="info">信息提示文字</cl-text>
```

**示例：手机号脱敏显示**

自动对手机号进行脱敏处理，保护用户隐私：

```html
<cl-text type="phone" mask value="13800138000"></cl-text>
```

### Icon 图标

cl-icon 是一个功能强大的图标组件，内置丰富的图标库，支持 iconfont 和 remixicon 两种图标字体的自动导入，为应用提供统一的视觉图标解决方案。 图标配置详情

**参数**

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| name | 图标名称 | string | 支持 iconfont 和 remixicon 图标名 |  |
| size | 图标尺寸(px) | number | 任意有效的尺寸值 | 16 |
| color | 图标颜色 | string | "primary" \| "success" \| "error" \| "warn" \| "info" |  |
| height | 图标高度(px) | number | 自定义高度，优先级高于 size |  |
| width | 图标宽度(px) | number | 自定义宽度，优先级高于 size |  |

**PassThrough 样式穿透**

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

**示例：基础用法**

最简单的图标使用方式，指定图标名称即可。

```html
<cl-icon name="heart-fill"></cl-icon>

<cl-icon name="heart-fill" :pt="{ className: 'ml-2' }"></cl-icon>
```

**示例：设置尺寸**

通过 size 属性控制图标大小，支持数字和字符串格式。

```html
<cl-icon name="heart-fill" :size="18"></cl-icon>

<cl-icon name="heart-fill" :size="20"></cl-icon>
```

**示例：设置颜色**

使用预设的主题色彩，让图标与应用主题保持一致。

```html
<cl-icon name="heart-fill" color="primary"></cl-icon>

<cl-icon name="close-line" color="error"></cl-icon>

<cl-icon name="check-line" color="success"></cl-icon>
```

### Image 图片

cl-image 组件是基于 uni-app 原生 image 组件封装的增强版图片组件

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| src | 图片资源地址 | string |  |  |
| mode | 图片裁剪、缩放模式 | string |  | "aspectFill" |
| preview | 是否启用预览功能 | boolean |  | false |
| preview-list | 预览图片列表 | string[] |  | [] |
| height | 图片高度 | string \| number |  | 60 |
| width | 图片宽度 | string \| number |  | 60 |
| showLoading | 是否显示加载状态 | boolean |  | false |
| lazyLoad | 是否启用懒加载 | boolean |  | false |
| fadeShow | 是否启用淡入动画 | boolean |  | false |
| webp | 是否解码 webp 格式 | boolean |  | false |
| showMenuByLongpress | 是否长按显示菜单 | boolean |  | false |

**PassThrough 样式穿透**

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| inner | 图片元素配置 | PassThroughProps |
| error | 错误状态配置 | PassThroughProps |
| loading | 加载状态配置 | PassThroughProps |

**示例：自定义插槽内容**

```html
<!-- 空数据占位 -->
<cl-image src="">
	<template #placeholder>
		<text>暂无图片</text>
	</template>
</cl-image>

<!-- 加载失败提示 -->
<cl-image src="invalid-url">
	<template #error>
		<text>图片加载失败</text>
	</template>
</cl-image>
```

**示例：自定义图片尺寸**

```html
<cl-image :height="100" :width="100"></cl-image> <cl-image height="50px" width="50px"></cl-image>
```

**示例：图片预览功能**

配置 previewList 属性，组件会自动将当前的 src 匹配为预览列表中的第一张图片。

```html
<cl-image :preview-list="previewList"></cl-image>
```

### Tag 标签

cl-tag 是一个轻量级的标签组件，常用于标记关键词、分类标识或状态展示等场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| type | 标签类型 | string | "primary" \| "success" \| "error" \| "warn" \| "info" | "primary" |
| icon | 左侧图标 | string | - | - |
| rounded | 是否圆角显示 | boolean | true \| false | false |
| closable | 是否显示关闭按钮 | boolean | true \| false | false |
| plain | 是否为镂空样式 | boolean | true \| false | false |

**PassThrough 样式穿透**

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| text | 文本元素配置 | PassThroughProps |

**示例：基础用法**

默认样式的标签。

```html
<cl-tag>默认标签</cl-tag>
```

**示例：不同类型**

通过 type 属性设置不同的标签类型，支持主要、成功、错误、警告、信息五种类型。

```html
<cl-tag type="primary">主要</cl-tag>
<cl-tag type="success">成功</cl-tag>
<cl-tag type="error">错误</cl-tag>
<cl-tag type="warn">警告</cl-tag>
<cl-tag type="info">信息</cl-tag>
```

**示例：镂空样式**

设置 plain 属性可以显示为镂空样式。

```html
<cl-tag type="primary" plain>主要</cl-tag>
<cl-tag type="success" plain>成功</cl-tag>
<cl-tag type="error" plain>错误</cl-tag>
<cl-tag type="warn" plain>警告</cl-tag>
<cl-tag type="info" plain>信息</cl-tag>
```

### Loading 加载中

加载动画用于在数据请求或操作处理中，为用户提供当前正在进行中的提示，提升用户体验。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| loading | 是否加载中 | boolean |  | true |
| size | 图标大小(px) | number |  | 24 |
| color | 图标颜色 | string |  |  |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 图标元素配置 | ClIconProps |

**示例：基础用法**

```html
<cl-loading></cl-loading>
```

## 二、表单组件

### Form 表单验证

表单组件用于数据录入与校验，支持多种校验规则、错误提示、禁用状态等功能。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | — | — |
| modelValue | 表单数据模型 | any | — | {} |
| rules | 表单规则 | Map<string, ClFormRule[]> | — | [] |
| labelPosition | 标签位置 | ClFormLabelPosition | 'top' \| 'left' \| 'right' | 'top' |
| labelWidth | 标签宽度(px) | number | — | '70px' |
| showAsterisk | 是否显示必填星号 | boolean | — | true |
| showMessage | 是否显示错误信息 | boolean | — | true |
| disabled | 是否禁用整个表单 | boolean | — | false |
| scrollToError | 滚动到第一个错误位置 | boolean | — | true |

**示例：示例**

当需要根据表单字段验证结果为 input 组件添加红色边框样式时：

```html
<template>
  <cl-form-item prop="name">
    <input :class="{ 'border-red-500': isError }"></input>
  </cl-form-item>
</template>

<script setup lang="ts">
import { useFormItem } from "@/uni_modules/cool-ui";

const { isError } = useFormItem();
</script>
```

**示例：简单用法**

```html
<template>
	<cl-form v-model="formData">
		<cl-form-item prop="avatarUrl">
			<cl-upload v-model="formData.avatarUrl" test></cl-upload>
		</cl-form-item>

		<cl-form-item label="用户名" prop="nickName">
			<cl-input v-model="formData.nickName" placeholder="请输入用户名" clearable></cl-input>
		</cl-form-item>
	</cl-form>
</template>

<script setup lang="ts">
import { ref, type Ref } from "vue";

// 自定义表单数据类型
type FormData = {
	avatarUrl: string;
	nickName: string;
};

// 表单数据
const formData = ref<FormData>({
	avatarUrl: "",
	nickName: "神仙都没用"
}) as Ref<FormData>;
</script>
```

**示例：添加验证规则**

```html
<template>
	<cl-form v-model="formData" :rules="rules">
		<cl-form-item prop="avatarUrl">
			<cl-upload v-model="formData.avatarUrl" test></cl-upload>
		</cl-form-item>

		<cl-form-item label="用户名" prop="nickName" required>
			<cl-input v-model="formData.nickName" placeholder="请输入用户名" clearable></cl-input>
		</cl-form-item>
	</cl-form>
</template>

<script setup lang="ts">
import { ref, type Ref } from "vue";
import { type ClFormRule } from "@/uni_modules/cool-ui";

// 自定义表单数据类型
type FormData = {
	avatarUrl: string;
	nickName: string;
};

// 表单数据
const formData = ref<FormData>({
	avatarUrl: "",
	nickName: "神仙都没用"
}) as Ref<FormData>;

// ------ 以下为新增内容 ------

// 表单验证规则
const rules = new Map<string, ClFormRule[]>([
	[
		"nickName",
		[
			{ required: true, message: t("用户名不能为空") },
			{ min: 3, max: 20, message: t("用户名长度在3-20个字符之间") }
		]
	]
]);
</script>
```

### Input 输入框

cl-input 组件基于 uni-app 的 input 组件，提供了丰富的输入功能和样式定制能力。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| modelValue | 绑定值 | string |  | "" |
| type | 输入框类型 | string | "text" \| "number" \| "idcard" \| "digit" \| "tel" \| "safe-password" \| "nickname" | "text" |
| prefixIcon | 前缀图标名称 | string |  |  |
| suffixIcon | 后缀图标名称 | string |  |  |
| password | 是否为密码类型 | boolean |  | false |
| autofocus | 是否自动聚焦 | boolean |  | false |
| placeholder | 输入框为空时的占位符文本 | string |  | "请输入" |
| placeholderClass | 占位符文本的样式类名 | string |  | "" |
| border | 是否显示边框 | boolean |  | false |
| disabled | 是否禁用输入框 | boolean |  | false |
| readonly | 是否为只读状态 | boolean |  | false |
| clearable | 是否可清空内容 | boolean |  | false |
| maxlength | 最大输入长度限制 | number |  | 140 |
| cursorSpacing | 指定光标与键盘的距离(px) | number |  | 5 |
| confirmHold | 点击键盘确认按钮时是否保持键盘不收起 | boolean |  | false |
| confirmType | 设置键盘右下角按钮的文字 | string | "done" \| "go" \| "next" \| "search" \| "send" | done |
| adjustPosition | 键盘弹起时，是否自动上推页面 | boolean |  | true |
| holdKeyboard | 是否保持键盘不收起 | boolean |  | false |
| precision | 保留精度 | number |  | 0 |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| inner | 输入框配置 | PassThroughProps |
| prefixIcon | 前缀图标配置 | ClIconProps |
| suffixIcon | 后缀图标配置 | ClIconProps |

**示例：基本用法**

最简单的输入框用法：

```html
<cl-input></cl-input>
```

**示例：数字输入**

通过设置 type 为 number 来限制只能输入数字：

```html
<cl-input type="number"></cl-input>
```

**示例：密码输入**

通过设置 password 属性来隐藏输入内容：

```html
<cl-input password></cl-input>
```

### Textarea 文本域

cl-textarea 组件基于 uni-app 的 textarea 组件，提供了丰富的多行文本输入功能和样式定制能力。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough |  |  |
| modelValue | 双向绑定的输入值 | string |  | "" |
| inputmode | 输入键盘类型 | string | "none" \| "text" \| "decimal" \| "numeric" \| "tel" \| "search" \| "email" \| "url" | "text" |
| autofocus | 是否自动获取焦点 | boolean |  | false |
| placeholder | 输入框为空时显示的占位符文本 | string |  | "请输入" |
| placeholderClass | 占位符文本的自定义样式类名 | string |  | "" |
| border | 是否显示输入框边框 | boolean |  | false |
| maxlength | 最大输入字符数限制 | number |  | 140 |
| disabled | 是否禁用输入框 | boolean |  | false |
| readonly | 是否设置为只读状态 | boolean |  | false |
| fixed | 如果 textarea 是在 position:fixed 的区域，需要显示指定属性 fixed 为 true | boolean |  | false |
| height | 文本域高度 | number |  | 70 |
| autoHeight | 是否自动调整高度 | boolean |  | false |
| showWordLimit | 是否显示字数统计 | boolean |  | true |
| clearable | 是否显示清空按钮 | boolean |  | false |
| cursorColor | 光标颜色 | string |  |  |
| cursorSpacing | 指定光标与键盘的距离（单位：px） | number |  | 5 |
| confirmHold | 点击键盘确认按钮时是否保持键盘不收起 | boolean |  | false |
| confirmType | 设置键盘右下角按钮的文字 | string | "done" \| "go" \| "next" \| "search" \| "send" | done |
| showConfirmBar | 是否显示键盘上方带有"完成"按钮那一栏 | boolean |  | true |
| holdKeyboard | 焦点时，点击页面的时候不收起键盘 | boolean |  | false |
| selectionStart | 光标起始位置，自动聚集时有效，需与 selection-end 搭配使用 | number |  | -1 |
| selectionEnd | 光标结束位置，自动聚集时有效，需与 selection-start 搭配使用 | number |  | -1 |
| adjustPosition | 键盘弹起时，是否自动上推页面 | boolean |  | true |
| adjustKeyboardTo | 键盘对齐位置 | string | "cursor" \| "bottom" | "cursor" |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| inner | 内部输入框配置 | PassThroughProps |

**示例：基本用法**

最简单的文本域用法：

```html
<cl-textarea></cl-textarea>
```

**示例：带边框**

添加边框样式：

```html
<cl-textarea border></cl-textarea>
```

**示例：自动调整高度**

根据内容自动调整文本域高度：

```html
<cl-textarea auto-height></cl-textarea>
```

### InputNumber 计数器

cl-input-number 是一个数字输入计数器组件，支持通过加减按钮或直接输入来调整数值，并可设置数值范围和步长。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | — | — |
| modelValue | 当前绑定的数值 | number | — | 0 |
| step | 每次点击加减按钮的步长 | number | — | 1 |
| max | 允许输入的最大数值 | number | — | 100 |
| min | 允许输入的最小数值 | number | — | 0 |
| inputable | 是否允许手动输入数值 | boolean | — | true |
| size | 加减按钮的尺寸大小（px） | number | — | 24 |
| disabled | 是否禁用组件 | boolean | — | false |
| inputType | 输入框的数值类型 | string | "digit" \| "number" | 'number' |
| placeholder | 输入框的占位提示文本 | string | — | — |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| value | 中间数值显示区配置 | ValuePassThrough |
| op | 左右加减按钮配置 | OpPassThrough |

**示例：基础用法**

最简单的计数器，默认值为 0，步长为 1：

```html
<cl-input-number></cl-input-number>
```

**示例：设置步长**

设置每次点击按钮时的数值变化量：

```html
<cl-input-number :step="5"></cl-input-number>
```

**示例：调整尺寸**

自定义加减按钮的大小：

```html
<cl-input-number :size="60"></cl-input-number>
```

### InputOtp 验证码输入

cl-input-otp 是一个验证码输入组件，用于输入一次性密码（OTP）或验证码，支持自定义位数、自动聚焦等功能，提供良好的用户输入体验。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | — | — |
| modelValue | 当前输入的验证码值 | string | — |  |
| autofocus | 是否自动聚焦 | boolean | — | false |
| length | 验证码位数 | number | — | 4 |
| disabled | 是否禁用组件 | boolean | — | false |
| inputType | 输入类型 | string | "number" | 'number' |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| list | 输入框列表容器配置 | PassThroughProps |
| item | 单个输入框配置 | PassThroughProps |
| cursor | 光标指示器配置 | PassThroughProps |
| value | 输入值显示配置 | PassThroughProps |

**示例：基础用法**

```html
<cl-input-otp></cl-input-otp>
```

**示例：自动聚焦**

设置 autofocus 属性，组件渲染后自动聚焦到第一个输入框：

```html
<cl-input-otp autofocus></cl-input-otp>
```

**示例：自定义位数**

通过 length 属性设置验证码位数，适用于不同长度的验证码场景：

```html
<cl-input-otp :length="6"></cl-input-otp>
```

### Keyboard 虚拟键盘

虚拟键盘组件提供安全的输入体验，支持多种键盘类型。默认需要点击确定按钮才会更新绑定值，启用 inputImmediate 参数后可实现实时输入绑定。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | — | — |
| modelValue | 当前输入的值 | string | — | — |
| type | 键盘输入类型 | string | "number" \| "digit" \| "idcard" | "number" |
| title | 弹窗标题 | string | — | "数字键盘" |
| placeholder | 输入框占位文本 | string | — | "安全键盘，请放心输入" |
| confirmText | 确认按钮文本 | string | — | "确定" |
| maxlength | 最大输入长度限制 | number | — | 8 |
| showValue | 是否显示当前输入值 | boolean | — | true |
| inputImmediate | 是否启用实时绑定 | boolean | — | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根容器样式类 | string |
| item | 键盘按键样式配置 | PassThroughProps |
| value | 输入值显示区域样式 | PassThroughProps |
| popup | 弹窗容器参数配置 | ClPopupProps |

**示例：示例**

```html
<cl-keyboard-number ref="keyboardNumberRef"> </cl-keyboard-number>

<script setup lang="ts">
	const keyboardNumberRef = ref<ClKeyboardNumberComponentPublicInstance | null>(null);

	function openKeyboardNumber() {
		keyboardNumberRef.value!.open();
	}
</script>
```

**示例：示例**

```html
<cl-keyboard-password ref="keyboardPasswordRef"> </cl-keyboard-password>

<script setup lang="ts">
	const keyboardPasswordRef = ref<ClKeyboardPasswordComponentPublicInstance | null>(null);

	function openKeyboardPassword() {
		keyboardPasswordRef.value!.open();
	}
</script>
```

**示例：示例**

```html
<cl-keyboard-car ref="keyboardCarRef" @change="handleCarNumberChange"> </cl-keyboard-car>

<script setup lang="ts">
	const keyboardCarRef = ref<ClKeyboardCarComponentPublicInstance | null>(null);

	function openKeyboardCar() {
		keyboardCarRef.value!.open();
	}
</script>
```

### Radio 单选框

Radio 单选框组件用于在一组选项中进行单一选择。支持自定义图标、样式穿透配置，以及灵活的事件处理。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 绑定值（双向绑定） | string \| number \| boolean | - | - |
| activeIcon | 选中状态的图标名称 | string | - | "checkbox-circle-line" |
| inactiveIcon | 未选中状态的图标名称 | string | - | "checkbox-blank-circle-line" |
| showIcon | 是否显示状态图标 | boolean | - | true |
| label | 单选框的标签文本 | string | - | - |
| value | 该单选框对应的唯一值 | string \| number \| boolean | - | - |
| disabled | 是否禁用该单选框 | boolean | - | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 图标元素配置 | ClIconProps |
| label | 标签文本元素配置 | ClTextProps |

**示例：基础用法**

最基本的单选框使用方式，通过 v-model 实现双向数据绑定。

```html
<template>
	<cl-radio v-model="selected" value="vue">Vue.js</cl-radio>
	<cl-radio v-model="selected" value="react">React</cl-radio>
	<cl-radio v-model="selected" value="angular">Angular</cl-radio>
	<cl-radio v-model="selected" value="svelte">Svelte</cl-radio>
</template>

<script setup>
	import { ref } from "vue";

	// 当前选中的框架
	const selected = ref("vue");
</script>
```

**示例：禁用状态**

使用 disabled 属性可以禁用特定的单选框选项。

```html
<template>
	<cl-radio v-model="selected" value="available">可用选项</cl-radio>
	<cl-radio v-model="selected" value="disabled" disabled>禁用选项</cl-radio>
	<cl-radio v-model="selected" value="normal">普通选项</cl-radio>
</template>

<script setup>
	import { ref } from "vue";

	const selected = ref("available");
</script>
```

**示例：纯文本样式**

通过设置 :show-icon="false" 隐藏图标，创建纯文本风格的单选框。

```html
<template>
	<cl-radio v-model="selected" value="option1" :show-icon="false"> 纯文本选项一 </cl-radio>
	<cl-radio v-model="selected" value="option2" :show-icon="false"> 纯文本选项二 </cl-radio>
</template>

<script setup>
	import { ref } from "vue";

	const selected = ref("option1");
</script>
```

### checkbox 多选框

checkbox 多选框组件用于在一组选项中进行单一选择。支持自定义图标、样式穿透配置，以及灵活的事件处理。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 绑定值（双向绑定） | any[] \| boolean | - | [] |
| activeIcon | 选中状态的图标名称 | string | - | "checkbox-line" |
| inactiveIcon | 未选中状态的图标名称 | string | - | "checkbox-blank-line" |
| showIcon | 是否显示状态图标 | boolean | - | true |
| label | 多选框的标签文本 | string | - | - |
| value | 该多选框对应的唯一值 | string \| number \| boolean | - | - |
| disabled | 是否禁用该多选框 | boolean | - | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 图标元素配置 | ClIconProps |
| label | 标签文本元素配置 | PassThroughProps |

**示例：基础用法**

最基本的多选框使用方式，通过 v-model 实现双向数据绑定。

```html
<template>
	<cl-checkbox v-model="selected" value="vue">Vue.js</cl-checkbox>
	<cl-checkbox v-model="selected" value="react">React</cl-checkbox>
	<cl-checkbox v-model="selected" value="angular">Angular</cl-checkbox>
	<cl-checkbox v-model="selected" value="svelte">Svelte</cl-checkbox>
</template>

<script setup>
	import { ref } from "vue";

	// 当前选中的框架
	const selected = ref(["vue"]);
</script>
```

**示例：禁用状态**

使用 disabled 属性可以禁用特定的多选框选项。

```html
<template>
	<cl-checkbox v-model="selected" value="available">可用选项</cl-checkbox>
	<cl-checkbox v-model="selected" value="disabled" disabled>禁用选项</cl-checkbox>
	<cl-checkbox v-model="selected" value="normal">普通选项</cl-checkbox>
</template>

<script setup>
	import { ref } from "vue";

	const selected = ref(["avaiable"]);
</script>
```

**示例：纯文本样式**

通过设置 :show-icon="false" 隐藏图标，创建纯文本风格的多选框。

```html
<template>
	<cl-checkbox v-model="selected" value="option1" :show-icon="false"> 纯文本选项一 </cl-checkbox>
	<cl-checkbox v-model="selected" value="option2" :show-icon="false"> 纯文本选项二 </cl-checkbox>
</template>

<script setup>
	import { ref } from "vue";

	const selected = ref(["option1"]);
</script>
```

### Switch 开关

用于在两个相互对立的状态间切换的组件。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 绑定值 | boolean | - | - |
| disabled | 是否禁用 | boolean | - | false |
| loading | 是否显示加载状态 | boolean | - | false |
| height | 开关高度(px) | number | - | 24 |
| width | 开关宽度(px) | number | - | 40 |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| track | 开关轨道元素配置 | PassThroughProps |
| thumb | 开关滑块元素配置 | PassThroughProps |
| loading | 加载图标元素配置 | ClLoadingProps |

**示例：基础用法**

最简单的用法，默认关闭状态。

```html
<cl-switch></cl-switch>
```

**示例：禁用状态**

设置 disabled 属性可以禁用开关。

```html
<cl-switch disabled></cl-switch>
```

**示例：加载状态**

设置 loading 属性显示加载状态。

```html
<cl-switch loading></cl-switch>
```

### Rate 评分

用于对事物进行评级操作的组件，支持星级评分、自定义图标、半星评分等功能。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 当前评分值 | number | - | 0 |
| max | 最大评分数（星级总数） | number | - | 5 |
| disabled | 是否禁用 | boolean | - | false |
| allowHalf | 是否允许半星评分 | boolean | - | false |
| showScore | 是否显示当前分数 | boolean | - | false |
| size | 单个星级的尺寸大小（px） | number | - | 40 |
| icon | 激活状态的图标名称 | string | - | "star-fill" |
| voidIcon | 未激活状态的图标名称 | string | - | "star-fill" |
| color | 激活状态的颜色 | string | - | "primary" |
| voidColor | 未激活状态的颜色 | string | - | "#dddddd" |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 星级项的配置 | PassThroughProps |
| score | 分数显示配置 | PassThroughProps |
| icon | 图标组件配置 | ClIconProps |

**示例：基本用法**

最简单的评分组件使用方式：

```html
<cl-rate v-model="score"></cl-rate>

<script lang="ts" setup>
  import { ref } from "vue";
  const score = ref<number>(2);
</script>
```

**示例：自定义尺寸**

通过 size 属性设置星级的大小：

```html
<cl-rate v-model="score" :size="50"></cl-rate>

<script lang="ts" setup>
  import { ref } from "vue";
  const score = ref<number>(2);
</script>
```

**示例：半星评分**

开启 allowHalf 属性支持半星评分，同时可以显示具体分数：

```html
<cl-rate v-model="score" allow-half show-score></cl-rate>

<script lang="ts" setup>
  import { ref } from "vue";
  const score = ref<number>(2.5);
</script>
```

### Slider 滑块

一个可交互的滑块组件，用于在指定范围内选择数值。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 绑定的当前值 | number | - | 0 |
| values | 绑定的范围值 | number[] | - | [] |
| max | 可选择的最大值 | number | - | 100 |
| min | 可选择的最小值 | number | - | 0 |
| step | 滑动步长 | number | - | 1 |
| disabled | 是否禁用滑块 | boolean | - | false |
| blockSize | 滑块手柄大小(px) | number | - | 20 |
| showValue | 是否显示当前值 | boolean | - | false |
| range | 是否启用范围选择 | boolean | - | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| track | 滑块轨道配置 | PassThroughProps |
| progress | 滑块进度条配置 | PassThroughProps |
| thumb | 滑块手柄配置 | PassThroughProps |
| value | 显示数值标签配置 | PassThroughProps |

**示例：基本用法**

最简单的滑块使用方式

```html
<cl-slider></cl-slider>
```

**示例：显示当前值**

在滑块上方显示当前选择的数值

```html
<cl-slider show-value></cl-slider>
```

**示例：设置步长**

设置滑块的移动步长为 10

```html
<cl-slider :step="10"></cl-slider>
```

### Select 选择器

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 绑定值 | string / number / boolean | - | - |
| title | 选择器标题 | string | - | '请选择' |
| placeholder | 选择器占位符 | string | - | '请选择' |
| options | 选项数据 | ClSelectOption[] | - | [] |
| showTrigger | 是否显示选择器触发器 | boolean | - | true |
| disabled | 是否禁用选择器 | boolean | - | false |
| columnCount | 列数 | number | - | 1 |
| splitor | 分隔符 | string | - | ' - ' |
| confirmText | 确认按钮文本 | string | - | '确定' |
| showConfirm | 是否显示确认按钮 | boolean | - | true |
| cancelText | 取消按钮文本 | string | - | '取消' |
| showCancel | 是否显示取消按钮 | boolean | - | true |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| trigger | 选择器样式配置 | ClSelectTriggerPassThrough |
| popup | 弹窗样式配置 | ClPopupPassThrough |

**示例：基础用法**

最简单的选择器用法，从预定义的选项中选择一个值。

```html
<template>
	<cl-select v-model="val" :options="options" placeholder="请选择技术栈"></cl-select>
</template>

<script setup lang="ts">
import { type ClSelectOption } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const val = ref(1);

const options = ref<ClSelectOption[]>([
	{
		label: "HTML",
		value: 1
	},
	{
		label: "CSS",
		value: 2
	},
	{
		label: "JavaScript",
		value: 3
	},
	{
		label: "Node.js",
		value: 4
	},
	{
		label: "Vue.js",
		value: 5
	},
	{
		label: "React",
		value: 6
	}
]);
</script>
```

**示例：手动控制弹窗**

通过调用组件的 open 方法手动打开选择弹窗，适用于自定义触发器的场景。

```html
<template>
	<view>
		<cl-button @click="openSelect">打开选择器</cl-button>
		<cl-select
			ref="selectRef"
			v-model="val"
			:options="options"
			:show-trigger="false"
		></cl-select>
	</view>
</template>

<script setup lang="ts">
import { type ClSelectOption } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const selectRef = ref();
const val = ref(1);

const options = ref<ClSelectOption[]>([
	{
		label: "HTML",
		value: 1
	},
	{
		label: "CSS",
		value: 2
	},
	{
		label: "JavaScript",
		value: 3
	},
	{
		label: "Node.js",
		value: 4
	},
	{
		label: "Vue.js",
		value: 5
	},
	{
		label: "React",
		value: 6
	}
]);

function openSelect() {
	selectRef.value!.open((value) => {
		console.log("选择的值:", value);
	});
}
</script>
```

**示例：多列级联选择**

通过配置 column-count 和 children 实现多列级联选择，常用于地区选择等场景。

```html
<template>
	<cl-select
		v-model="val"
		:options="options"
		:column-count="3"
		title="选择地区"
		placeholder="请选择省市区"
	></cl-select>
</template>

<script setup lang="ts">
import { type ClSelectOption } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const val = ref();

const options = ref<ClSelectOption[]>([
	{
		label: "福建省",
		value: "fujian",
		children: [
			{
				label: "福州市",
				value: "fuzhou",
				children: [
					{
						label: "鼓楼区",
						value: "gulou"
					},
					{
						label: "台江区",
						value: "taijiang"
					},
					{
						label: "仓山区",
						value: "cangshan"
					},
					{
						label: "马尾区",
						value: "mawei"
					}
				]
			},
			{
				label: "厦门市",
				value: "xiamen",
				children: [
					{
						label: "思明区",
						value: "siming"
					},
					{
						label: "湖里区",
						value: "huli"
					},
					{
						label: "集美区",
						value: "jimei"
					},
					{
						label: "海沧区",
						value: "haicang"
					}
				]
			},
			{
				label: "泉州市",
				value: "quanzhou",
				children: [
					{
						label: "鲤城区",
						value: "licheng"
					},
					{
						label: "丰泽区",
						value: "fengze"
					},
					{
						label: "洛江区",
						value: "luojiang"
					},
					{
						label: "泉港区",
						value: "quangang"
					}
				]
			}
		]
	},
	{
		label: "浙江省",
		value: "zhejiang",
		children: [
			{
				label: "杭州市",
				value: "hangzhou",
				children: [
					{
						label: "上城区",
						value: "shangcheng"
					},
					{
						label: "下城区",
						value: "xiacheng"
					},
					{
						label: "江干区",
						value: "jianggan"
					},
					{
						label: "拱墅区",
						value: "gongshu"
					}
				]
			},
			{
				label: "宁波市",
				value: "ningbo",
				children: [
					{
						label: "海曙区",
						value: "haishu"
					},
					{
						label: "江北区",
						value: "jiangbei"
					},
					{
						label: "北仑区",
						value: "beilun"
					}
				]
			}
		]
	},
	{
		label: "湖南省",
		value: "hunan",
		children: [
			{
				label: "长沙市",
				value: "changsha",
				children: [
					{
						label: "芙蓉区",
						value: "furong"
					},
					{
						label: "天心区",
						value: "tianxin"
					},
					{
						label: "岳麓区",
						value: "yuelu"
					}
				]
			},
			{
				label: "株洲市",
				value: "zhuzhou",
				children: [
					{
						label: "荷塘区",
						value: "hetang"
					},
					{
						label: "芦淞区",
						value: "lusong"
					}
				]
			}
		]
	},
	{
		label: "江西省",
		value: "jiangxi",
		children: [
			{
				label: "南昌市",
				value: "nanchang",
				children: [
					{
						label: "东湖区",
						value: "donghu"
					},
					{
						label: "西湖区",
						value: "xihu"
					},
					{
						label: "青云谱区",
						value: "qingyunpu"
					}
				]
			},
			{
				label: "九江市",
				value: "jiujiang",
				children: [
					{
						label: "浔阳区",
						value: "xunyang"
					},
					{
						label: "濂溪区",
						value: "lianxi"
					}
				]
			}
		]
	}
]);
</script>
```

### SelectDate 日期选择器

一个功能强大的日期时间选择器组件，支持多种粒度的日期时间选择，提供灵活的配置选项和自定义样式。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 双向绑定的日期值 | string | - | - |
| title | 选择器弹窗顶部标题 | string | - | "请选择" |
| placeholder | 输入框占位符文本 | string | - | "请选择" |
| headers | 选择器列表头部标题数组 | string[] | - | ['年', '月', '日', '时', '分', '秒'] |
| showTrigger | 是否显示默认的选择器触发元素 | boolean | true / false | true |
| disabled | 是否禁用选择器，禁用后无法操作 | boolean | true / false | false |
| type | 选择器类型，控制日期选择的精度 | string | "year" \| "month" \| "date" \| "hour" \| "minute" \| "second" | "second" |
| confirmText | 确认按钮显示文本 | string | "确定" |  |
| showConfirm | 是否显示确认按钮 | boolean | true |  |
| cancelText | 取消按钮显示文本 | string | "取消" |  |
| showCancel | 是否显示取消按钮 | boolean | true |  |
| labelFormat | 选中值在触发器中的显示格式 | string | "" |  |
| valueFormat | 输出值的格式化规则 | string | "" |  |
| start | 可选择的最早日期时间 | string | "1950-01-01 00:00:00" |  |
| end | 可选择的最晚日期时间 | string | "2050-12-31 23:59:59" |  |
| rangeable | 是否范围选择 | boolean |  | false |
| startPlaceholder | 开始日期占位符 | string |  | "开始日期" |
| endPlaceholder | 结束日期占位符 | string |  | "结束日期" |
| rangeSeparator | 范围分隔符 | string |  | "至" |
| showShortcuts | 是否显示快捷选项 | boolean |  | true |
| shortcuts | 快捷选项 | ClSelectDateShortcut[] |  | [] |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| trigger | 选择器触发元素样式配置 | ClSelectTriggerPassThrough |
| popup | 弹窗容器样式配置 | ClPopupPassThrough |

**示例：基础用法**

最简单的日期选择器，默认精确到秒级别。

```html
<template>
	<cl-select-date v-model="selectedDate"></cl-select-date>
</template>

<script setup>
	import { ref } from "vue";

	const selectedDate = ref("");
</script>
```

**示例：不同精度选择**

根据业务需求选择不同的时间精度。

```html
<cl-select-date
	v-model="dateTime"
	type="second"
	title="选择时间"
	placeholder="请选择日期时间"
></cl-select-date>
```

**示例：格式化显示**

自定义日期的显示和输出格式。

```html
<cl-select-date
	v-model="formattedDate"
	type="date"
	label-format="YYYY年MM月DD日"
	value-format="YYYY-MM-DD"
	title="选择日期"
></cl-select-date>
```

### SelectTime 时间选择器

用于选择时间的交互式组件，支持小时、分钟、秒的选择，提供友好的弹窗选择界面。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 双向绑定的时间值 | string | - | - |
| title | 选择器弹窗顶部标题 | string | - | "请选择" |
| placeholder | 输入框占位符文本 | string | - | "请选择" |
| headers | 选择器列表头部标题数组 | string[] | - | ['小时', '分钟', '秒数'] |
| showTrigger | 是否显示默认的选择器触发元素 | boolean | true/false | true |
| disabled | 是否禁用选择器，禁用后无法操作 | boolean | true/false | false |
| labelFormat | 时间标签格式化字符串 | string | - | "{H}:{m}:{s}" |
| type | 选择类型 | string | "hour" \| "minute" \| "second" | "second" |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| trigger | 选择器触发元素样式配置 | ClSelectTriggerPassThrough |
| popup | 弹窗容器样式配置 | ClPopupPassThrough |

**示例：基础用法**

最简单的时间选择器使用方式。

```html
<template>
  <cl-select-time v-model="selectedTime"></cl-select-time>
</template>

<script setup lang="ts">
  import { ref } from "vue";

  const selectedTime = ref("");
</script>
```

**示例：自定义展示格式**

通过 labelFormat 属性自定义时间的显示格式。

```html
<cl-select-time v-model="time1" label-format="{H}时{m}分{s}秒"></cl-select-time>
```

**示例：自定义触发器**

隐藏默认触发器，使用自定义的触发元素。

```html
<template>
  <cl-select-time
    ref="selectTimeRef"
    v-model="customTime"
    :show-trigger="false"
  ></cl-select-time>
</template>

<script setup lang="ts">
  import { ref } from "vue";

  const selectTimeRef = ref<ClSelectTimeComponentPublicInstance | null>(null);
  const customTime = ref("");

  function openTimePicker() {
    selectTimeRef.value!.open((value: string) => {
      console.log("选择的时间:", value);
    });
  }
</script>
```

### Cascader 级联选择器

用于从多级数据结构中进行选择，常用于省市区、分类等场景。用户可以逐级展开并选择目标项，支持自定义选项内容、分隔符、禁用状态等功能，适用于需要多层级联动选择的表单或数据录入场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 双向绑定的值 | string[] | - | - |
| title | 选择器弹窗顶部标题 | string | - | "请选择" |
| placeholder | 输入框占位符文本 | string | - | "请选择" |
| options | 选项数据源，支持树形结构 | ClCascaderOption[] |  | [] |
| showTrigger | 是否显示默认触发器 | boolean |  | true |
| disabled | 是否禁用选择器 | boolean |  | false |
| labelKey | 标签显示字段的键名 | string |  | "label" |
| valueKey | 值字段的键名 | string |  | "value" |
| textSeparator | 文本分隔符 | string |  | " - " |
| height | 列表高度 | string \| number |  | 400 |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| trigger | 选择器触发元素配置 | ClSelectTriggerPassThrough |
| popup | 弹窗容器配置 | ClPopupPassThrough |

**示例：基础用法**

使用级联选择器展示树形结构数据， options 需要定义为 ClCascaderOption[] 类型。

```html
<template>
	<cl-cascader v-model="val" :options="options"></cl-cascader>
</template>

<script setup>
	  import { ref } from "vue";
	  import { type ClCascaderOption } from "@/uni_modules/cool-ui";

	  const val = ref<string[]>([]);

	  const options = ref<ClCascaderOption[]>([{
			label: "电子产品",
			value: "1",
			children: [
				{
					label: "手机",
					value: "1-1",
					children: [
						{
							label: "苹果",
							value: "1-1-1",
						},
						{
							label: "华为",
							value: "1-1-2",
						},
						{
							label: "小米",
							value: "1-1-3"
						}
					]
				},
				{
					label: "电脑",
					value: "1-2",
					children: [
						{
							label: "笔记本",
							value: "1-2-1"
						},
						{
							label: "台式机",
							value: "1-2-2"
						}
					]
				},
			]
		},
		{
			label: "服装",
			value: "2",
			children: [
				{
					label: "男装",
					value: "2-1",
					children: [
						{
							label: "上衣",
							value: "2-1-1"
						},
						{
							label: "裤装",
							value: "2-1-2"
						},
					]
				},
				{
					label: "女装",
					value: "2-2",
					children: [
						{
							label: "裙装",
							value: "2-2-1"
						},
						{
							label: "上装",
							value: "2-2-2"
						}
					]
				}
			]
		}
	]);
</script>
```

**示例：地区选择示例**

当使用外部 JSON 数据（如地区数据）时，由于 import 导入的类型是 UTSJSONObject ，需要使用 useCascader() 进行类型转换后才能赋值给 options 。

```html
<template>
	<cl-cascader v-model="val" :options="options"></cl-cascader>
</template>

<script setup>
	import { ref } from "vue";
	import { useCascader } from "@/uni_modules/cool-ui";
	import pca from "@/data/pca.json";

	const val = ref<string[]>([]);

	const options = useCascader(pca)
</script>
```

### Upload 文件上传

一个功能完整的上传组件，已封装好 上传请求处理 。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 双向绑定的文件地址 | string \| string[] | - | - |
| icon | 上传按钮显示的图标 | string | - | "camera-fill" |
| text | 上传按钮显示的文字 | string | - | "上传/拍摄" |
| sizeType | 图片压缩方式 | string[] | "original" \| "compressed" | ["original", "compressed"] |
| sourceType | 图片选择来源 | string[] | "album" \| "camera" | ["album", "camera"] |
| height | 上传区域高度 | string \| number | - | 72 |
| width | 上传区域宽度 | string \| number | - | 72 |
| multiple | 是否支持多文件上传 | boolean | - | false |
| limit | 最大上传文件数量 | number | - | 9 |
| disabled | 是否禁用上传功能 | boolean | - | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 文件项容器配置 | PassThroughProps |
| add | 添加按钮配置 | PassThroughProps |
| image | 图片预览配置 | PassThroughProps |
| text | 按钮文本配置 | ClTextProps |
| icon | 图标配置 | ClIconProps |

**示例：基础用法**

最简单的使用方式，绑定一个字符串变量来接收上传后的文件地址。

```html
<cl-upload v-model="url"></cl-upload>
```

**示例：禁用状态**

通过 disabled 属性禁用上传功能，常用于表单只读状态。

```html
<cl-upload v-model="url" disabled></cl-upload>
```

**示例：自定义图标和文字**

通过 icon 和 text 属性自定义上传按钮的外观。

```html
<cl-upload v-model="url" icon="id-card-line" text="上传证件照"></cl-upload>
```

### Calendar 日历

日历组件用于选择日期，支持单选、多选和范围选择等多种模式，适用于表单、数据录入等场景。通过丰富的参数配置，可以自定义显示样式、日期范围、头部导航栏、星期显示等，满足不同业务需求。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 当前选中的日期值（单选模式） | string \| null | - | null |
| date | 选中的日期数组（多选/范围模式） | string[] | - | [] |
| mode | 日期选择模式 | "single" \| "multiple" \| "range" | - | "single" |
| dateConfig | 日期配置 | ClCalendarDateConfig[] |  | [] |
| year | 设置年份（首次定位） | number |  | 0 |
| month | 设置月份（首次定位） | number |  | 0 |
| showOtherMonth | 是否显示其他月份的日期 | boolean |  | true |
| showHeader | 是否显示头部导航栏 | boolean |  | true |
| showWeeks | 是否显示星期 | boolean |  | true |
| cellHeight | 单元格高度 | number |  | 66 |
| cellGap | 单元格间距 | number |  | 0 |
| color | 主色 | string |  | "" |
| textColor | 当前月份日期颜色 | string |  | "" |
| textOtherMonthColor | 其他月份日期颜色 | string |  | "" |
| textDisabledColor | 禁用日期颜色 | string |  | "" |
| textTodayColor | 今天日期颜色 | string |  | "#ff6b6b" |
| textSelectedColor | 选中日期颜色 | string |  | "#ffffff" |
| bgSelectedColor | 选中日期背景颜色 | string |  | "" |
| bgRangeColor | 范围选择背景颜色 | string |  | "" |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

**示例：日历面板**

```html
<template>
  <cl-calendar v-model="date"></cl-calendar>
</template>

<script lang="ts" setup>
const date = ref("2025-10-01");
</script>
```

**示例：使用选择器**

```html
<template>
  <cl-calendar-select
    v-model="date"
    ref="calendarSelectRef"
  ></cl-calendar-select>
</template>

<script lang="ts" setup>
const calendarSelectRef = ref<ClCalendarSelectComponentPublicInstance | null>(
  null
);

const date = ref("2025-10-01");
</script>
```

**示例：多个日期选择**

如需选择多个日期，请使用 v-model:date 进行绑定，并传入一个字符串数组。

```html
<template>
  <cl-calendar v-model:date="date"></cl-calendar>
</template>

<script lang="ts" setup>
const date = ref(["2025-10-01", "2025-10-02", "2025-10-03"]);
</script>
```


## 三、布局组件

### Flex 弹性布局

Flex 弹性布局组件的使用说明与参数配置。

**参数**

*cl-row*

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| gutter | 栅格间隔，单位 rpx | number |  | 0 |

*cl-col*

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| span | 栅格占据的列数 | number |  | 24 |
| offset | 栅格左侧的间隔格数 | number |  | 0 |
| push | 栅格向右移动格数 | number |  | 0 |
| pull | 栅格向左移动格数 | number |  | 0 |

**PassThrough 样式穿透**

*cl-row*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根容器样式 | string |

*cl-col*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

*基础用法*

```html
<cl-row :gutter="12">
  <cl-col :span="8"> 1 </cl-col>
  <cl-col :span="8"> 2 </cl-col>
  <cl-col :span="8"> 3 </cl-col>
</cl-row>
```

*基础用法*

```html
<cl-row :gutter="12">
  <cl-col :span="6"> 1 </cl-col>
  <cl-col :span="6"> 2 </cl-col>
  <cl-col :span="6"> 3 </cl-col>
  <cl-col :span="6" :pull="6"> 4 </cl-col>
</cl-row>
```

*基础用法*

```html
<cl-row
  :gutter="12"
  :pt="{
    className: 'mt-5 border border-solid border-surface-100 p-3',
  }"
>
  <cl-col :span="8"> 1 </cl-col>
  <cl-col :span="8"> 2 </cl-col>
  <cl-col :span="8"> 3 </cl-col>
</cl-row>
```

### Tabs 标签页

用于在不同内容区域之间进行切换的标签页组件，支持横向滚动、填充布局等多种展示方式。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 当前选中标签的值 | number \| string | - | - |
| height | 标签容器高度(px) | number | - | 40 |
| list | 标签数据列表 | ClTabsItem[] | - | [] |
| fill | 是否横向填充标签 | boolean | - | true |
| gutter(px) | 标签之间的间距 | number | - | 14 |
| color | 选中状态的文字颜色 | string | - | - |
| unColor | 未选中状态文字颜色 | string | - | - |
| showLine | 是否显示底部下划线 | boolean | - | true |
| showSlider | 是否显示滑块背景 | boolean | - | false |
| disabled | 是否禁用整个组件 | boolean | - | false |

**PassThrough 样式穿透**

*事件*

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 标签切换时触发事件 | value: string \| number |

*事件*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| text | 标签文本配置 | PassThroughProps |
| item | 单个标签配置 | PassThroughProps |
| line | 底部下划线配置 | PassThroughProps |
| slider | 滑块背景配置 | PassThroughProps |

*基础用法*

```html
<cl-tabs v-model="val" :list="list"></cl-tabs>

<script lang="ts" setup>
import type { ClTabsItem } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const val = ref("1");

const list = ref<ClTabsItem[]>([
	{
		label: "Vue",
		value: "1"
	},
	{
		label: "React",
		value: "2"
	},
	{
		label: "Angular",
		value: "3"
	},
	{
		label: "Svelte",
		value: "4"
	},
	{
		label: "Jquery",
		value: "5"
	},
	{
		label: "Vuex",
		value: "6"
	},
	{
		label: "Vue Router",
		value: "7"
	},
	{
		label: "Pinia",
		value: "8"
	}
]);
</script>
```

*基础用法*

```html
<view class="flex flex-row justify-center">
    <cl-tabs v-model="val" :list="list" color="red" un-color="#ccc"></cl-tabs>
</view>

<script lang="ts" setup>
import type { ClTabsItem } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const val = ref("1");

const list = ref<ClTabsItem[]>([
	{
		label: "Vue",
		value: "1"
	},
	{
		label: "React",
		value: "2"
	},
	{
		label: "Angular",
		value: "3"
	},
	{
		label: "Svelte",
		value: "4"
	}
]);
</script>
```

*基础用法*

```html
<cl-tabs
	v-model="val"
	:list="list"
	show-slider
	:pt="{
		className: '!p-2'
	}"
></cl-tabs>

<script lang="ts" setup>
import type { ClTabsItem } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const val = ref("1");

const list = ref<ClTabsItem[]>([
	{
		label: "Vue",
		value: "1"
	},
	{
		label: "React",
		value: "2"
	},
	{
		label: "Angular",
		value: "3"
	},
	{
		label: "Svelte",
		value: "4"
	}
]);
</script>
```

### Collapse 折叠面板

折叠面板组件用于展示和隐藏内容区域，支持平滑的展开收起动画效果，常用于 FAQ、详情展示等场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件样式 | PassThrough | - | - |
| modelValue | 控制折叠面板的展开/收起状态 | boolean | - | false |

**PassThrough 样式穿透**

*方法*

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| show | 展开状态 | - |
| hide | 收起状态 | - |
| toggle | 切换展开/收起状态 | - |

*方法*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

*基础用法*

```html
<cl-button @click="toggle">{{ visible ? '收起' : '展开' }}</cl-button>

<cl-collapse v-model="visible">
	<cl-text> 云想衣裳花想容，春风拂槛露华浓，若非群玉山头见，会向瑶台月下逢。 </cl-text>
</cl-collapse>

<script lang="ts" setup>
	import { ref } from "vue";

	const visible = ref(false);

	function toggle() {
		visible.value = !visible.value;
	}
</script>
```

*基础用法*

```html
<cl-button @click="toggle">切换状态</cl-button>

<cl-collapse ref="collapseRef">
	<cl-text> 云想衣裳花想容，春风拂槛露华浓，若非群玉山头见，会向瑶台月下逢。 </cl-text>
</cl-collapse>

<script lang="ts" setup>
	import { ref } from "vue";

	// 注意：类型必须为 ClCollapseComponentPublicInstance | null，默认值不能省略
	const collapseRef = ref<ClCollapseComponentPublicInstance | null>(null);

	function toggle() {
		collapseRef.value!.toggle();
	}
</script>
```

### Sticky 吸顶

Sticky 组件用于将元素固定在页面顶部，当页面滚动时，被包裹的内容会始终保持在可视区域的顶部。常用于导航栏、标题栏等需要始终可见的内容。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| offsetTop | 距离顶部的偏移量(px) | number | - | 0 |
| zIndex | 层级，控制显示优先级 | number | - | 100 |
| scrollTop | 页面当前滚动高度(px) | number | - | 0 |

*基础用法*

```html
<cl-sticky>
  <view
    class="bg-blue-500 p-3 h-[50px] flex flex-row items-center justify-center"
  >
    <text class="text-white font-bold">固定导航栏</text>
  </view>
</cl-sticky>
```

*基础用法*

```html
<!-- 第一个吸顶元素 -->
<cl-sticky>
  <view
    class="bg-red-500 p-3 h-[50px] flex flex-row items-center justify-center"
  >
    <text class="text-white font-bold">主导航栏</text>
  </view>
</cl-sticky>

<!-- 第二个吸顶元素，紧贴在第一个下方 -->
<cl-sticky :offset-top="50">
  <view
    class="bg-orange-500 p-3 h-[40px] flex flex-row items-center justify-center"
  >
    <text class="text-white">子导航栏</text>
  </view>
</cl-sticky>
```

*基础用法*

```html
<cl-sticky :z-index="200">
  <view
    class="bg-purple-500 p-3 h-[50px] flex flex-row items-center justify-center"
  >
    <text class="text-white font-bold">高优先级导航</text>
  </view>
</cl-sticky>
```

### Topbar 顶栏

顶部导航栏组件，支持自定义标题、返回按钮、颜色配置等功能，常用于页面顶部导航。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件样式 | PassThrough | - | - |
| title | 导航栏标题文本 | string | - | - |
| color | 文字颜色，优先级最高 | string | - | - |
| backgroundColor | 背景颜色，优先级最高 | string | - | - |
| showBack | 是否显示返回按钮 | boolean | - | true |
| backPath | 返回按钮点击后的跳转路径 | string | - | - |
| backIcon | 返回按钮使用的图标名称 | string | - | "back" |
| safeAreaTop | 是否启用安全区域顶部边距 | boolean | - | false |
| fixed | 是否固定在页面顶部 | boolean | - | false |
| height | 导航栏内容高度 | number \| string | - | 44px |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| title | 标题文本配置 | PassThroughProps |
| back | 返回按钮图标配置 | ClIconProps |

*基础用法*

```html
<cl-topbar title="页面标题"></cl-topbar>
```

*基础用法*

```html
<cl-topbar title="插槽示例">
    <template #prepend>
        <cl-icon name="home-2-line"></cl-icon>
    </template>

    <template #append>
        <cl-button text>保存</cl-button>
    </template>
</cl-topbar>
```

*基础用法*

```html
<cl-topbar title="选项卡导航">
    <cl-tabs v-model="type" :height="32" :list="typeList"></cl-tabs>
</cl-topbar>

<script lang="ts" setup>
import { ref } from "vue";
import type { ClTabsItem } from "@/uni_modules/cool-ui";

const type = ref("fans");
const typeList = ref<ClTabsItem[]>([
	{
		label: "我的粉丝",
		value: "fans"
	},
	{
		label: "我的关注",
		value: "follow"
	}
]);
</script>
```

### Footer 底部栏

固定在页面底部的布局组件，通常用于放置操作按钮，如提交、购买、确认等功能按钮。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件样式 | PassThrough | - | - |
| minHeight | 最小高度，低于此值时组件不显示 | number | - | 30 |
| vt | 监听值，用于触发组件重新计算 | number | - | 0 |
| height | 固定的内容高度 | number | - |  |
| backgroundColor | 背景颜色 | number | - |  |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| content | 内容区域配置 | PassThroughProps |

*基础用法*

```html
<cl-list>
	<cl-list-item :label="`列表项 ${i}`" v-for="i in 50" :key="i"></cl-list-item>
</cl-list>

<cl-footer>
	<cl-button type="primary" size="large" @tap="handleSubmit"> 提交 </cl-button>
</cl-footer>
```

*基础用法*

```html
<cl-list>
	<cl-list-item :label="`列表项 ${i}`" v-for="i in 50" :key="i"></cl-list-item>
</cl-list>

<cl-footer :vt="cache.key">
	<template v-if="status == 0">
		<view class="flex flex-row">
			<cl-button :pt="{ className: 'flex-1' }" text border size="large" @tap="cancel">
				取消订单
			</cl-button>

			<cl-button :pt="{ className: 'flex-1' }" type="primary" size="large" @tap="buy">
				立即购买
			</cl-button>
		</view>
	</template>

	<cl-button type="error" size="large" @tap="confirm" v-if="status == 1"> 确认收货 </cl-button>

	<cl-button type="success" size="large" @tap="comment" v-if="status == 2"> 评价 </cl-button>
</cl-footer>

<script lang="ts" setup>
	import { useCache } from "@/.cool";
	import { ref } from "vue";

	const status = ref(0);

	// useCache 可以监听多个值的变化
	const { cache } = useCache(() => [status.value]);

	function cancel() {
		status.value = 3;
	}

	function buy() {
		status.value = 1;
	}

	function confirm() {
		status.value = 2;
	}

	function comment() {
		status.value = 3;
	}
</script>
```

### FloatView 悬浮视图

FloatView 是一个可拖拽的悬浮视图组件，支持自动边缘吸附和自定义位置拖拽功能，常用于悬浮按钮、工具栏等场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| zIndex | 组件层级 | number | - | 500 |
| size | 组件尺寸（宽高相等） | number | - | 40 |
| left | 初始左边距（px） | number | - | 10 |
| bottom | 初始底部距离（px） | number | - | 10 |
| gap | 距离屏幕边缘的最小间距 | number | - | 10 |
| disabled | 是否禁用拖拽功能 | boolean | - | false |
| noSnapping | 是否禁用边缘自动吸附功能 | boolean | - | false |
| height | 自定义高度（px） | number | - | - |
| width | 自定义宽度（px） | number | - | - |

*基础用法*

```html
<cl-float-view :left="50" :bottom="50">
  <view
    class="w-[40px] h-[40px] bg-primary-500 flex flex-row items-center justify-center"
  >
    <cl-icon name="heart-fill" color="white"></cl-icon>
  </view>
</cl-float-view>
```

*基础用法*

```html
<cl-float-view :left="50" :bottom="50" disabled>
  <view
    class="w-[40px] h-[40px] bg-primary-500 flex flex-row items-center justify-center"
  >
    <cl-icon name="heart-fill" color="white"></cl-icon>
  </view>
</cl-float-view>
```

*基础用法*

```html
<cl-float-view :left="50" :bottom="50" :height="100" :width="200">
  <view
    class="h-[100px] w-[200px] bg-primary-500 flex flex-row items-center justify-center"
  >
    <cl-icon name="heart-fill" color="white"></cl-icon>
  </view>
</cl-float-view>
```

### Tabbar 标签栏

底部导航栏组件,用于在应用底部展示多个页面入口,支持图标和文字的组合显示,常用于应用的主导航。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 当前选中的导航项值 | string | - | "" |
| list | 导航项数据列表 | ClTabbarItem[] | - | [] |
| height | 导航栏高度(px) | number | - | 60 |
| backgroundColor | 背景颜色 | string | - | null |
| color | 未选中状态的文字颜色 | string | - | surface-400 |
| selectedColor | 选中状态的文字颜色 | string | - | primary-500 |
| iconSize | 图标尺寸(px) | number | - | 32 |
| textSize | 文字大小(px) | number | - | 12 |
| showIcon | 是否显示图标 | boolean | - | true |
| showText | 是否显示文字 | boolean | - | true |

**PassThrough 样式穿透**

*事件*

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| select | 导航项被点击时触发 | item: ClTabbarItem |

*事件*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 导航项配置 | PassThroughProps |
| icon | 图标配置 | ClImageProps |
| text | 文字配置 | ClTextProps |
| footer | 底部容器配置 | PassThroughProps |
| footerContent | 底部内容配置 | PassThroughProps |

*基础用法*

```html
<cl-tabbar v-model="current" :list="list" @select="handleSelect"></cl-tabbar>

<script lang="ts" setup>
import type { ClTabbarItem } from "@/uni_modules/cool-ui";
import { ref } from "vue";

const current = ref("home");

const list = ref<ClTabbarItem[]>([
	{
		text: "首页",
		value: "home",
		icon: "/static/icon/tabbar/home.png",
		selectedIcon: "/static/icon/tabbar/home-active.png"
	},
	{
		text: "分类",
		value: "category",
		icon: "/static/icon/tabbar/category.png",
		selectedIcon: "/static/icon/tabbar/category-active.png"
	},
	{
		text: "购物车",
		value: "cart",
		icon: "/static/icon/tabbar/cart.png",
		selectedIcon: "/static/icon/tabbar/cart-active.png"
	},
	{
		text: "我的",
		value: "my",
		icon: "/static/icon/tabbar/my.png",
		selectedIcon: "/static/icon/tabbar/my-active.png"
	}
]);

function handleSelect(item: ClTabbarItem) {
	// 可以在这里进行页面跳转等操作
}
</script>
```

*基础用法*

```html
<cl-tabbar
	v-model="current"
	:list="list"
	:pt="{
		className: 'border-t border-gray-200',
		item: {
			className: 'hover:bg-gray-50'
		},
		text: {
			size: 14,
			className: 'font-bold'
		},
		icon: {
			width: 36,
			height: 36
		}
	}"
></cl-tabbar>
```

*基础用法*

```html
interface ClTabbarItem {
	text?: string; // 导航项文字
	value: string; // 导航项唯一标识
	icon?: string; // 未选中状态图标
	selectedIcon?: string; // 选中状态图标
}
```

## 四、数据组件

### Avatar 头像

用于展示用户头像或替代图像的组件，支持图片显示和图标占位。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| src | 头像图片地址 | string | - | - |
| size | 头像尺寸大小(px) | number | - | 40 |
| rounded | 是否显示为圆形头像 | boolean | true/false | false |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 图标元素配置 | ClIconProps |

*基本用法*

```html
<!-- 使用图片地址显示头像 -->
<cl-avatar src="https://example.com/avatar.jpg"></cl-avatar>
```

*基本用法*

```html
<!-- 当没有图片时，使用图标作为占位符 -->
<cl-avatar
	:pt="{
    icon: {
        size: 30,
        name: 'user-line'
    }
}"
></cl-avatar>
```

*组合示例*

```html
<!-- 大尺寸圆形头像配合自定义图标 -->
<cl-avatar
	:size="150"
	rounded
	:pt="{
      className: 'custom-avatar',
      icon: {
          size: 60,
          name: 'account-circle-line'
      }
}"
></cl-avatar>
```

### ReadMore 展开阅读

用于内容超出指定高度时，显示“展开/收起”按钮，支持自定义展开/收起文案、图标及禁用状态。常用于长文本、详情介绍等场景，提升页面的简洁性和用户体验。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| modelValue | 是否展开 | boolean | - | false |
| height | 收起状态下的最大高度(px) | number | - | 40 |
| expandText | 展开时显示的文本 | string | - | "展开" |
| collapseText | 收起时显示的文本 | string | - | "收起" |
| expandIcon | 展开时显示的图标 | string | - | "arrow-down-s-line" |
| collapseIcon | 收起时显示的图标 | string | - | "arrow-up-s-line" |
| disabled | 是否禁用 | boolean | - | false |

**PassThrough 样式穿透**

*方法*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| toggle | 切换收起/展开 | (): void |

*方法*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根容器的样式类名 | string |
| wrapper | 内容包裹区域的配置 | PassThroughProps |
| content | 展示内容区域的配置 | PassThroughProps |
| mask | 内容底部遮罩的配置 | PassThroughProps |
| toggle | 展开/收起按钮的配置 | PassThroughProps |

*基础用法*

```html
<template>
	<cl-read-more>
		<cl-text>
			云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。
			一枝红艳露凝香，云雨巫山枉断肠。借问汉宫谁得似？可怜飞燕倚新妆。
			名花倾国两相欢，常得君王带笑看。解释春风无限恨，沉香亭北倚阑干。
		</cl-text>
	</cl-read-more>
</template>
```

*基础用法*

```html
<template>
	<cl-read-more :content="content" :show-toggle="content != ''" ref="readMoreRef">
		<view class="flex flex-row items-center justify-center h-14" v-if="content == ''">
			<cl-loading></cl-loading>
		</view>
	</cl-read-more>
</template>

<script lang="ts" setup>
const content = ref("");

function getContent() {
	setTimeout(() => {
		content.value =
			"云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。一枝红艳露凝香，云雨巫山枉断肠。借问汉宫谁得似？可怜飞燕倚新妆。名花倾国两相欢，常得君王带笑看。解释春风无限恨，沉香亭北倚阑干。";

		// 使用 slot 插入内容时，如果内容发生变化，需要重新获取高度
		// readMoreRef.value!.getContentHeight();
	}, 500);
}
</script>
```

*基础用法*

```html
<template>
	<cl-read-more
		v-model="visible"
		:disabled="disabled"
		:expand-text="disabled ? '付费解锁' : '展开'"
		:expand-icon="disabled ? 'lock-line' : 'arrow-down-s-line'"
		@toggle="toggle"
	>
		<cl-text>
			云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。
			一枝红艳露凝香，云雨巫山枉断肠。借问汉宫谁得似？可怜飞燕倚新妆。
			名花倾国两相欢，常得君王带笑看。解释春风无限恨，沉香亭北倚阑干。
		</cl-text>
	</cl-read-more>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUi } from "@/uni_modules/cool-ui";

const ui = useUi();

const visible = ref(false);
const disabled = ref(true);

function toggle(isExpanded: boolean) {
	ui.showConfirm({
		title: "提示",
		message: "需支付100元才能解锁全部内容，是否继续？",
		callback(action) {
			if (action == "confirm") {
				ui.showToast({
					message: "支付成功"
				});

				disabled.value = false;
				visible.value = true;
			}
		}
	});
}
</script>
```

### List 列表

List 组件用于展示一系列的数据项，支持自定义样式、交互操作和数据渲染。
列表容器组件，用于展示多个列表项。

**参数**

*cl-list*

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置 | PassThrough | - | - |
| list | 列表数据源 | ClListItem[] | - | [] |
| title | 列表标题 | string | - | - |
| border | 是否显示边框 | boolean | - | false |

*cl-list-item*

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置 | PassThrough | - | - |
| icon | 左侧图标名称 | string | - | - |
| image | 左侧图片链接 | string | - | - |
| label | 标签文本 | string | - | - |
| justify | 内容对齐方式 | "start" \| "center" \| "end" | start / center / end | end |
| arrow | 是否显示右侧箭头 | boolean | true / false | false |
| swipeable | 是否支持滑动操作 | boolean | true / false | false |
| hoverable | 是否显示点击态 | boolean | true / false | false |
| disabled | 是否禁用状态 | boolean | true / false | false |
| collapse | 是否支持折叠展开 | boolean | true / false | false |

**PassThrough 样式穿透**

*cl-list*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| list | 列表容器配置 | PassThroughProps |
| item | 列表项配置 | ClListItemPassThrough |

*cl-list-item*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素的 CSS 类名 | string |
| inner | 内部容器样式配置 | PassThroughProps |
| label | 标签文本样式配置 | ClTextProps |
| content | 内容区域样式配置 | PassThroughProps |
| icon | 图标样式配置 | ClIconProps |
| image | 图片样式配置 | ClImageProps |
| collapse | 折叠内容样式配置 | PassThroughProps |

**插槽**

*插槽*

| 插槽名 | 说明 |
| --- | --- |
| icon | 图标内容 |
| image | 图片内容 |
| default | 默认内容 |

```html
type ClListItemPassThrough = {
	className?: string;
	inner?: PassThroughProps;
	label?: ClTextProps;
	content?: PassThroughProps;
	icon?: ClIconProps;
	collapse?: PassThroughProps;
};
```

*基础用法*

```html
<cl-list border title="功能">
	<cl-list-item label="我的订单" hoverable></cl-list-item>
	<cl-list-item label="我的收藏" hoverable></cl-list-item>
	<cl-list-item label="我的钱包" hoverable></cl-list-item>
</cl-list>
```

*基础用法*

```html
<cl-list border title="功能" :list="list"></cl-list>

<script lang="ts" setup>
	import { ref } from "vue";
	import { type ClListItem } from "@/uni_modules/cool-ui";

	const list = ref<ClListItem[]>([
		{
			label: "我的订单"
		},
		{
			label: "我的收藏"
		},
		{
			label: "我的钱包",
			content: "10,000.00"
		}
	]);
</script>
```

### ListView 长列表

采用虚拟列表技术实现高性能数据渲染，专为海量数据场景设计，支持无限滚动、分组显示和索引定位等功能。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| data | 列表数据源，支持分组数据结构 | ClListViewItem[] | - | [] |
| itemHeight(px) | 单个列表项的固定高度（虚拟渲染必需） | number | - | 50 |
| headerHeight(px) | 分组标题的固定高度 | number | - | 32 |
| topHeight(px) | 列表顶部预留空间高度，可用于放置搜索框等 | number | - | 0 |
| bottomHeight(px) | 列表底部预留空间高度，可用于放置加载更多按钮 | number | - | 0 |
| bufferSize | 缓冲区大小，控制可视区域外预渲染的项目数量 | number | - | 5 |
| virtual | 是否启用虚拟列表渲染，关闭后为普通列表 | boolean | - | true |
| scrollIntoView | 滚动到指定位置 | string | - | "" |
| scrollWithAnimation | 是否启用滚动动画 | boolean | - | false |
| showScrollbar | 是否显示滚动条 | boolean | - | false |
| refresherEnabled | 是否启用下拉刷新 | boolean | - | false |
| refresherThreshold | 下拉刷新触发距离，相当于下拉内容高度 | number | - | 50 |
| refresherBackground | 下拉刷新区域背景色 | string | - | "transparent" |
| refresherDefaultText | 下拉刷新默认文案 | string | - | "下拉刷新" |
| refresherPullingText | 释放刷新文案 | string | - | "释放立即刷新" |
| refresherRefreshingText | 正在刷新文案 | string | - | "加载中" |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| item-tap | 列表项点击时触发 | item: ClListViewVirtualItem |

*插槽*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根容器样式类名 | string |
| item | 列表项容器的样式配置 | PassThroughProps |
| itemHover | 列表项容器按下的样式配置 | PassThroughProps |
| list | 列表容器的样式配置 | PassThroughProps |
| scroller | 滚动容器的样式配置 | PassThroughProps |
| refresher | 下拉刷新容器的样式配置 | PassThroughProps |
| indexBar | 右侧索引栏容器的样式配置 | PassThroughProps |

**插槽**

*插槽*

| 插槽名 | 说明 | 参数 | 使用场景 |
| --- | --- | --- | --- |
| top | 顶部内容插槽 | - | 搜索框、筛选器等 |
| header | 分组标题插槽 | { index: string } | 自定义分组标题样式 |
| item | 列表项内容插槽 | { data: ClListViewItem; item: ClListViewVirtualItem } | 自定义列表项布局和内容 |
| bottom | 底部内容插槽 | - | 加载更多、底部提示信息等 |
| index | 右侧索引栏项目插槽 | { index: string } | 自定义索引栏字母或图标样式 |
| refresher | 下拉刷新插槽 | { status: ClListViewRefresherStatus; text: string } | 下拉刷新自定义文字和图标 |

```html
type ClListViewItem = {
	label?: string;
	value?: any;
	index?: string;
	children?: ClListViewItem[];
};

type ClListViewGroup = {
	index: string;
	children: ClListViewItem[];
};

type ClListViewVirtualItem = {
	key: string;
	type: "header" | "item";
	index: number;
	top: number;
	height: number;
	data: ClListViewItem;
};

type ClListViewRefresherStatus = "default" | "pulling" | "refreshing";
```

*基础用法*

```html
<cl-list-view :data="data"> </cl-list-view>

<script lang="ts" setup>
	import { request } from "@/.cool";
	import { ref } from "vue";

	const data = ref<ClListViewItem[]>([]);

	onReady(() => {
		// 根据实际情况调整数据的类型
		request<UTSJSONObject[]>({
			url: "https://cool-service.oss-cn-shanghai.aliyuncs.com/app%2Fbase%2Fb1957e07f1254de99f44b5a711f277d2_pca_flat.json"
		})
			.then((res) => {
				data.value = useListView(res);
			})
			.catch((err) => {
				console.error(err);
			});
	});
</script>
```

*基础用法*

```html
<cl-list-view
	:pt="{
    indexBar: {
      className: '!fixed',
    },
  }"
>
</cl-list-view>
```

### ListViewRefresh 下拉刷新

cl-list-view 组件结合 usePager() 钩子函数提供了完整的列表刷新解决方案，主要解决以下痛点：
virtual 属性用于控制是否启用虚拟列表渲染。启用时需要注意:
pt.refresher 提供下拉刷新区域的自定义样式能力
refresher-enabled 设置为 true 开启下拉刷新功能
@pull 下拉刷新事件,触发时会重置页码为 1,实现列表数据重新加载
@bottom 监听列表滚动到底部事件,用于触发加载更多数据
#item 建议将列表项封装为独立组件(如 goods-item.uvue):
#bottom 用于自定义底部加载更多区域,通常配合 cl-loadmore 组件使用
usePager 分页钩子函数
usePager(cb) 的参数是一个方法，用于调用获取列表的接口

**参数**

（本站未列出参数表，详见官方文档。）

*示例*

```html
type PagerCallback = (params: UTSJSONObject, ctx: Pager) => void | Promise<void>;

type usePager(cb: PagerCallback): Pager
```

*示例*

```html
<template>
	<cl-page>
		<cl-list-view
			ref="listViewRef"
			:data="listView"
			:virtual="false"
			:pt="{
				refresher: {
					className: 'pt-3'
				}
			}"
			:refresher-enabled="true"
			@pull="onPull"
			@bottom="loadMore"
		>
			<template #item="{ value }">
				<goods-item :value="value"></goods-item>
			</template>

			<template #bottom>
				<view class="py-3">
					<cl-loadmore :loading="loading" v-if="list.length > 0"></cl-loadmore>
				</view>
			</template>
		</cl-list-view>
	</cl-page>
</template>

<script lang="ts" setup>
import { useUi } from "@/uni_modules/cool-ui";
import { ref } from "vue";
import { usePager } from "@/.cool";
import GoodsItem from "../components/goods-item.uvue";
import { t } from "@/locale";

const ui = useUi();

const listViewRef = ref<ClListViewComponentPublicInstance | null>(null);

let id = 0;

const { refresh, list, listView, loading, loadMore } = usePager((params, { render }) => {
	// 模拟请求
	setTimeout(() => {
		render({
			list: [
				{
					id: id++,
					title: "春日樱花盛开时节，粉色花瓣如诗如画般飘洒",
					image: "https://unix.cool-js.com/images/demo/1.jpg"
				},
				{
					id: id++,
					title: "夕阳西下的海滩边，金色阳光温柔地洒在波光粼粼的海面上，构成令人心旷神怡的日落美景",
					image: "https://unix.cool-js.com/images/demo/2.jpg"
				},
				{
					id: id++,
					title: "寒冬腊月时分，洁白雪花纷纷扬扬地覆盖着整个世界，感受冬日的宁静与美好",
					image: "https://unix.cool-js.com/images/demo/3.jpg"
				}
			],
			pagination: {
				page: params["page"],
				size: params["size"],
				total: 100
			}
		});

		ui.hideLoading();
	}, 1000);
});

async function onPull() {
	await refresh({ page: 1 });
	listViewRef.value!.stopRefresh();
}

onReady(() => {
	ui.showLoading(t("加载中"));
	// 默认请求
	refresh({});
});
</script>
```

*示例*

```html
<template>
	<view class="p-3 pb-0">
		<view class="w-full p-3 bg-white rounded-xl dark:bg-surface-800">
			<cl-image :src="item?.image" mode="aspectFill" width="100%" height="280rpx"></cl-image>
			<cl-text :pt="{ className: 'mt-2' }">{{ item?.title }}</cl-text>
		</view>
	</view>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import { parse } from "@/.cool";

defineOptions({
	name: "goods-item"
});

type GoodsItem = {
	id: number;
	title: string;
	image: string;
};

const props = defineProps({
	value: {
		type: Object,
		default: () => ({})
	}
});

const item = computed(() => parse<GoodsItem>(props.value));
</script>
```

### Waterfall 瀑布流

瀑布流组件是一个响应式的多列布局组件，能够自动计算每个项目的位置，实现高度不等的网格布局效果。特别适用于图片展示、卡片列表等场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置 | PassThrough | - | - |
| column | 瀑布流列数 | number | - | 2 |
| gutter | 列间距(px) | number | - | 8 |
| nodeKey | 数据项的唯一标识字段名 | string | - | "id" |

**PassThrough 样式穿透**

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

*基本用法*

```html
<!-- 两列布局 -->
<cl-waterfall :column="2"></cl-waterfall>

<!-- 三列布局 -->
<cl-waterfall :column="3"></cl-waterfall>
```

*完整示例*

```html
<template>
	<cl-page back-top>
		<view class="py-2">
			<cl-waterfall ref="waterfallRef" :column="2">
				<template #item="{ item, index }">
					<view class="bg-white mb-3 rounded-xl dark:!bg-gray-800 relative">
						<!-- 图片展示 -->
						<image :src="item.image" mode="widthFix" class="w-full rounded-xl"></image>

						<!-- 广告标识 -->
						<template v-if="item.isAd">
							<cl-tag :pt="{ className: 'absolute left-1 top-1 scale-75' }">
								广告
							</cl-tag>
							<cl-icon
								color="white"
								name="close-line"
								:pt="{ className: 'absolute right-2 top-2' }"
								@tap="del(item.id as number)"
							></cl-icon>
						</template>

						<!-- 内容区域 -->
						<view class="p-3" v-else>
							<cl-text>{{ item.title }}</cl-text>

							<!-- 点赞区域 -->
							<cl-row class="mt-2" :pt="{ className: 'justify-end items-center' }">
								<cl-icon name="heart-line"></cl-icon>
								<cl-text :pt="{ className: '!text-sm ml-1' }">
									{{ item.likeCount }}
								</cl-text>
							</cl-row>
						</view>
					</view>
				</template>
			</cl-waterfall>

			<!-- 加载更多指示器 -->
			<cl-loadmore :loading="loading"></cl-loadmore>
		</view>
	</cl-page>
</template>

<script lang="ts" setup>
	import { random } from "@/.cool";
	import { onMounted, ref } from "vue";

	const waterfallRef = ref<ClWaterfallComponentPublicInstance | null>(null);
	const loading = ref(false);

	let id = 0;

	// 生成模拟数据
	function generateMockData() {
		return [
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "春日樱花盛开时节，粉色花瓣如诗如画般飘洒",
				image: "/static/demo/1.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "夕阳西下的海滩边，金色阳光温柔地洒在波光粼粼的海面上，构成令人心旷神怡的日落美景",
				image: "/static/demo/2.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "寒冬腊月时分，洁白雪花纷纷扬扬地覆盖着整个世界，感受冬日的宁静与美好",
				image: "/static/demo/3.jpg"
			},
			{
				id: id++,
				image: "/static/demo/4.jpg",
				isAd: true
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "都市夜景霓虹闪烁，五彩斑斓光芒照亮城市营造梦幻般景象",
				image: "/static/demo/5.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "云雾缭绕的山间风光如诗如画让人心旷神怡，微风轻抚树梢带来阵阵清香，鸟儿在林间自由歌唱",
				image: "/static/demo/6.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "古老建筑与现代摩天大楼交相辉映，传统与现代完美融合创造独特城市景观",
				image: "/static/demo/7.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "广袤田野绿意盎然风光无限，金黄麦浪在微风中轻柔摇曳，农家炊烟袅袅升起",
				image: "/static/demo/8.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "璀璨星空下银河横跨天际，繁星闪烁神秘光芒营造浪漫夜空美景",
				image: "/static/demo/9.jpg"
			},
			{
				id: id++,
				likeCount: random(100, 1000),
				title: "雄伟瀑布从高耸悬崖飞流直下激起千层浪花，彩虹在水雾中若隐若现如梦如幻",
				image: "/static/demo/10.jpg"
			}
		];
	}

	// 刷新数据
	function refresh() {
		const items = generateMockData();
		waterfallRef.value!.append(items);
	}

	// 删除指定项目
	function del(id: number) {
		waterfallRef.value!.remove(id);
	}

	// 触底加载更多
	onReachBottom(() => {
		if (loading.value) return;

		loading.value = true;

		setTimeout(() => {
			refresh();
			loading.value = false;
		}, 1000);
	});

	// 初始化数据
	onMounted(() => {
		refresh();
	});
</script>
```

*完整示例*

```html
interface ClWaterfallComponentPublicInstance {
	append(items: any[]): void;
	update(id: any, data: Partial<any>): void;
	remove(id: any): void;
	clear(): void;
}
```

### Banner 轮播

轮播图组件，支持自动播放、手势滑动、自定义样式等功能。适用于图片展示、广告位、产品推荐等场景。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置 | PassThrough | - | - |
| list | 轮播项列表（图片链接） | string[] | - | [] |
| previousMargin | 前一个轮播项的左边距 | number | - | 0 |
| nextMargin | 后一个轮播项的右边距 | number | - | 0 |
| autoplay | 是否自动轮播 | boolean | - | true |
| interval | 自动轮播间隔时间（毫秒） | number | - | 5000 |
| showDots | 是否显示指示器圆点 | boolean | - | true |
| disableTouch | 是否禁用手势滑动 | boolean | - | false |
| height | 轮播容器高度 | number \| string | - | 160 |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 轮播项切换时触发 | (value: number) |
| item-tap | 点击轮播项时触发 | (index: number) |

*事件*

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 轮播项容器的配置 | PassThroughProps |
| itemActive | 当前激活轮播项的配置 | PassThroughProps |
| image | 轮播图片的配置 | PassThroughProps |
| dots | 指示器容器的配置 | PassThroughProps |
| dot | 指示器圆点的配置 | PassThroughProps |
| dotActive | 激活指示器圆点的配置 | PassThroughProps |

*基础用法*

```html
<cl-banner :list="list"></cl-banner>

<script lang="ts" setup>
	import { ref } from "vue";

	const list = ref<string[]>([
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg2.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg3.png"
	]);
</script>
```

*基础用法*

```html
<cl-banner
	:list="list"
	:pt="{
    dots: {
      className: parseClass(['!bottom-[10px]']),
    },
    dot: {
      className: parseClass(['!w-[8px] !h-[8px] !bg-white/50']),
    },
    dotActive: {
      className: parseClass(['!w-[16px] !bg-white !rounded-[4px]']),
    },
  }"
></cl-banner>

<script lang="ts" setup>
	import { ref } from "vue";
	import { parseClass } from "@/.cool";

	const list = ref<string[]>([
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg2.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg3.png"
	]);
</script>
```

*基础用法*

```html
<cl-banner
	:list="list"
	:pt="{
    className: 'mx-[-6px]',
    item: {
      className: parseClass(['px-[6px]']),
    },
  }"
	:next-margin="40"
></cl-banner>

<script lang="ts" setup>
	import { ref } from "vue";
	import { parseClass } from "@/.cool";

	const list = ref<string[]>([
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg2.png",
		"https://uni-docs.cool-js.com/demo/pages/demo/static/bg3.png"
	]);
</script>
```

### Marquee 跑马灯

Marquee 跑马灯组件用于展示图片或内容的循环滚动效果，支持横向和纵向两种滚动方向。通过配置参数可以自定义滚动速度、间距、单项尺寸等，适用于广告轮播、信息公告等场景。组件还支持方法调用控制动画的开始、暂停、重置等操作，并提供插槽和样式透传能力，方便进行深度定制。

**参数**

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| list | 图片列表 | string[] | - | [] |
| direction | 滚动方向 | "horizontal" \| "vertical" | - | "horizontal" |
| duration | 一次滚动的持续时间 | number | - | 5000 |
| itemHeight(px) | 图片高度 | number \| string | - | 100 |
| itemWidth(px) | 图片宽度（仅横向滚动时生效，纵向为 100%） | number \| string | - | 150 |
| gap(px) | 间距 | number \| string | - | 10 |

**PassThrough 样式穿透**

*方法*

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| start | 开始滚动动画 | - |
| stop | 停止滚动动画 | - |
| reset | 重置滚动动画 | - |
| pause | 暂停滚动动画 | - |
| play | 播放滚动动画 | - |

*方法*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根容器的样式类名 | string |
| list | 列表区域的配置 | PassThroughProps |
| item | 单个项的配置 | PassThroughProps |
| image | 图片的配置 | PassThroughProps |

**插槽**

*插槽*

| 插槽名 | 说明 | 参数 | 使用场景 |
| --- | --- | --- | --- |
| item | 每个项内容 | { item: MarqueeItem; index: number } | 搜索框、筛选器等 |

```html
type MarqueeItem = {
	url: string;
	originalIndex: number;
};
```

*示例*

```html
<template>
	<cl-marquee
		:list="list"
		direction="vertical"
		:item-height="100"
		:pt="{
			className: 'h-[100px] rounded-xl'
		}"
	></cl-marquee>
</template>

<script setup lang="ts">
const list = ref<string[]>([
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png",
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg2.png",
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg3.png"
]);
</script>
```

*示例*

```html
<template>
	<cl-marquee
		ref="marqueeRef"
		:list="list"
		direction="vertical"
		:item-height="130"
		:pt="{
			className: 'h-[250px] rounded-xl'
		}"
	></cl-marquee>
</template>

<script setup lang="ts">
import { ref } from "vue";

const list = ref<string[]>([
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png",
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg2.png",
	"https://uni-docs.cool-js.com/demo/pages/demo/static/bg3.png"
]);

const marqueeRef = ref<ClMarqueeComponentPublicInstance | null>(null);

function play() {
	marqueeRef.value!.play();
}

function pause() {
	marqueeRef.value!.pause();
}
</script>
```

### Pagination 分页

分页组件用于处理大量数据的分页显示，提供页码切换和导航功能，支持自定义样式和文本内容。

**参数**

*基础属性*

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| modelValue | 当前页码（双向绑定） | number | - | 1 |
| total | 数据总条数 | number | - | 0 |
| size | 每页显示的数据条数 | number | - | 10 |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 当页码发生变化时触发 | (value: number) |

*事件*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 页码项元素配置 | PassThroughProps |
| prev | "上一页"按钮配置 | PassThroughProps |
| next | "下一页"按钮配置 | PassThroughProps |

*基础用法*

```html
<cl-pagination v-model="page" :total="24"></cl-pagination>
```

*基础用法*

```html
<cl-pagination
  v-model="page"
  :total="100"
  :pt="{
    item: {
      className: '!rounded-none !mx-[2rpx]',
    },
  }"
></cl-pagination>
```

*基础用法*

```html
<cl-pagination
  v-model="page4"
  :total="24"
  :pt="{
    prev: {
      className: '!w-auto px-3',
    },
    next: {
      className: '!w-auto px-3',
    },
  }"
>
  <template #prev>
    <cl-text class="!text-sm">上一页</cl-text>
  </template>

  <template #next>
    <cl-text class="!text-sm">下一页</cl-text>
  </template>
</cl-pagination>
```

### Timeline 时间线

Timeline 时间轴组件用于展示时间流信息，通常用于显示历史记录、步骤流程或事件序列。

**参数**

*基础属性*

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| title | 时间轴项目标题 | string | - | - |
| icon | 时间轴项目图标 | string | - | - |
| content | 时间轴项目内容描述 | string | - | - |
| date | 时间轴项目日期 | string | - | - |
| hideLine | 是否隐藏连接线 | boolean | - | false |

**PassThrough 样式穿透**

*基础属性*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 图标元素配置 | PassThroughProps |
| title | 标题元素配置 | PassThroughProps |
| content | 内容元素配置 | PassThroughProps |
| date | 日期元素配置 | PassThroughProps |

*基础用法*

```html
<cl-timeline-item
  title="开通账号"
  date="2025-01-01"
  content="恭喜您成功开通账号，赠送新用户专属福利500元"
>
</cl-timeline-item>
```

*基础用法*

```html
<cl-timeline-item icon="account-box-line" title="推荐产品" date="2025-01-01">
  <view class="flex flex-row mb-3 mt-1">
    <cl-image
      src="https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png"
      class="w-20 h-20 rounded-lg"
    ></cl-image>

    <view class="flex-1 px-3">
      <cl-text class="font-medium">{{ "优选灵活配置混合A基金" }}</cl-text>

      <cl-text class="mr-5 mt-1 !text-sm text-gray-500">
        {{ "投资门槛：1000元起投" }}
      </cl-text>

      <view class="flex flex-row mt-2 items-center">
        <cl-button size="small" type="light"> {{ "立即购买" }} </cl-button>
      </view>
    </view>
  </view>
</cl-timeline-item>
```

*基础用法*

```html
<cl-timeline-item
  title="最后一项"
  date="2025-01-03"
  content="这是时间轴的最后一项，不显示连接线"
  :hideLine="true"
>
</cl-timeline-item>
```

### Draggable 拖拽

一个功能强大的拖拽排序组件，支持单列、多列布局，可自定义拖拽动画和样式。

**参数**

*基础属性*

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| modelValue | 数据数组 | UTSJSONObject[] | - | [] |
| disabled | 是否禁用拖拽功能 | boolean | - | false |
| animation | 拖拽动画持续时间（毫秒） | number | - | 150 |
| columns | 列数：1 为单列纵向布局 | number | - | 1 |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 数据顺序发生变化时触发 | (list: UTSJSONObject[]) |
| start | 开始拖拽时触发 | (index: number) |
| end | 结束拖拽时触发 | (index: number) |

*插槽*

| 插槽名 | 说明 | 参数 |
| --- | --- | --- |
| item | 子元素 | {item: UTSJSONObject; index: numbe; dragging: boolean; dragIndex: number; insertIndex: number} |

*插槽*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| ghost | 拖拽选中时元素配置 | PassThroughProps |

*基础用法*

```html
<cl-draggable v-model="list">
  <template #item="{ item, index }">
    <view
      class="flex flex-row items-center p-3 bg-surface-100 rounded-lg mb-2 dark:!bg-surface-700"
      :class="{
        'opacity-50': item['disabled']
      }"
    >
      <cl-text>{{ (item as UTSJSONObject).label }}</cl-text>
    </view>
  </template>
</cl-draggable>
```

*结合列表使用*

```html
<cl-draggable v-model="list3" :columns="4">
  <template #item="{ item, index }">
    <view
      class="flex flex-row items-center justify-center p-3 bg-surface-100 rounded-lg m-1 dark:!bg-surface-700"
      :class="{
        'opacity-50': item['disabled']
      }"
    >
      <cl-text>{{ item['label'] }}</cl-text>
    </view>
  </template>
</cl-draggable>
```

*结合图片使用*

```html
<cl-draggable v-model="list4" :columns="4">
  <template #item="{ item, index }">
    <view class="p-[2px]">
      <cl-image
        :src="(item as UTSJSONObject).url"
        mode="widthFix"
        :pt="{
          className: '!w-full'
        }"
        preview
      ></cl-image>
    </view>
  </template>
</cl-draggable>
```

### FilterBar 筛选栏

FilterBar 筛选栏组件用于在列表、商品页等场景中快速筛选和切换数据，支持多种筛选类型，灵活组合，满足多样化业务需求。

**参数**

*基础属性*

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| label | 筛选项标签 | string | - | "" |
| value | 当前值 | any | - |  |
| type | 筛选类型 | ClFilterItemType | "switch" \| "select" \| "sort" | "switch" |
| options | 下拉类型的选项数据 | [ClSelectOption] | - | [] |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 切换时触发 | (value: number) |

*事件*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| label | 标签元素样式配置 | PassThroughProps |

*使用示例*

```html
<cl-filter-bar>
  <cl-filter-item
    label="综合排序"
    type="select"
    :value="1"
    :options="coreOptions"
    @change="onOptionsChange"
  ></cl-filter-item>
</cl-filter-bar>
```

*使用示例*

```html
<cl-filter-bar>
  <cl-filter-item
    label="国补"
    type="switch"
    :value="false"
    @change="onSwitchChange"
  ></cl-filter-item>
</cl-filter-bar>
```

*使用示例*

```html
<cl-filter-bar>
  <!-- 下拉框 -->
  <cl-filter-item
    label="综合排序"
    type="select"
    :value="1"
    :options="coreOptions"
    :pt="{
        className: 'w-[220rpx] !flex-none'
    }"
    @change="onOptionsChange"
  ></cl-filter-item>

  <!-- 排序 -->
  <cl-filter-item
    label="销量"
    type="sort"
    value="desc"
    @change="onSortChange"
  ></cl-filter-item>

  <!-- 开关 -->
  <cl-filter-item
    label="国补"
    type="switch"
    :value="false"
    @change="onSwitchChange"
  ></cl-filter-item>

  <!-- 自定义 -->
  <view
    class="flex flex-row items-center justify-center flex-1"
    @tap="openFilter"
  >
    <cl-text>筛选</cl-text>
    <cl-icon name="filter-line"></cl-icon>
  </view>
</cl-filter-bar>

<script lang="ts" setup>
  // 下拉框的必须定义类型 ClSelectOption[]
  const coreOptions = ref<ClSelectOption[]>([
    {
      label: "综合排序",
      value: 1,
    },
    {
      label: "价格从高到底",
      value: 2,
    },
    {
      label: "价格从低到高",
      value: 3,
    },
  ]);
</script>
```

### Tree 树形控件

树形组件用于以层级结构展示数据，支持节点的展开、收起、选择等操作。常用于组织结构、分类管理、权限分配等场景，能够清晰地表达数据之间的父子关系，并支持多种交互方式（如多选、懒加载、节点自定义等）。

**参数**

*基础属性*

| 属性名 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| modelValue | 当前页码（双向绑定） | array \| string \| number | - | null |
| icon | 节点图标 | string | - | "arrow-right-s-fill" |
| expandIcon | 展开图标 | string | - | "arrow-down-s-fill" |
| checkStrictly | 是否严格的遵循父子不互相关联 | boolean | - | false |
| checkable | 是否可以选择节点 | boolean | - | false |
| multiple | 是否允许多选 | boolean | - | false |

**PassThrough 样式穿透**

*事件*

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| clearChecked | 清除所有已选中的节点 | () => void |
| setChecked | 设置指定节点的选中状态 | (key: string \| number, flag: boolean) => void |
| setCheckedKeys | 批量设置选中节点 | (keys: (string \| number)[]) => void |
| getCheckedKeys | 获取所有已选中节点的 key | () => (string \| number)[] |
| getHalfCheckedKeys | 获取所有半选节点的 key | () => (string \| number)[] |
| setExpanded | 设置指定节点的展开状态 | (key: string \| number, flag: boolean) => void |
| setExpandedKeys | 批量设置展开节点 | (keys: (string \| number)[]) => void |
| getExpandedKeys | 获取所有已展开节点的 key | () => (string \| number)[] |
| expandAll | 展开所有节点 | () => void |
| collapseAll | 收起所有节点 | () => void |

*事件*

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 单项元素配置 | PassThroughProps |
| itemChecked | 选中状态配置 | PassThroughProps |
| itemWrapper | 外层包裹配置 | PassThroughProps |
| expand | 展开区域配置 | PassThroughProps |
| expandIcon | 展开图标配置 | PassThroughProps |
| checkbox | 复选框区域配置 | PassThroughProps |
| checkedIcon | 选中图标配置 | ClIconProps |
| halfCheckedIcon | 半选图标配置 | ClIconProps |
| uncheckedIcon | 未选中图标配置 | ClIconProps |
| label | 标签配置 | PassThroughProps |

*基础用法*

```html
<template>
  <cl-tree v-model="checkedKeys" ref="treeRef" :list="list"></cl-tree>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useTree, useUi, type ClTreeItem } from "@/uni_modules/cool-ui";

const checkedKeys = ref<string[]>(["1-1-1-1", "2-1-1", "2-1-2"]);

const ui = useUi();

const list = ref<ClTreeItem[]>([]);

function refresh() {
  ui.showLoading();

  setTimeout(() => {
    list.value = useTree([
      {
        id: "1",
        label: "华为",
        children: [
          {
            id: "1-1",
            label: "手机",
            children: [
              {
                id: "1-1-1",
                label: "Mate系列",
                children: [
                  {
                    id: "1-1-1-1",
                    label: "Mate 50",
                  },
                  {
                    id: "1-1-1-2",
                    disabled: true,
                    label: "Mate 40",
                  },
                  {
                    id: "1-1-1-3",
                    label: "Mate 30",
                  },
                ],
              },
              {
                id: "1-1-2",
                label: "P系列",
                children: [
                  {
                    id: "1-1-2-1",
                    disabled: true,
                    label: "P60",
                  },
                  {
                    id: "1-1-2-2",
                    label: "P50",
                  },
                  {
                    id: "1-1-2-3",
                    label: "P40",
                  },
                ],
              },
            ],
          },
          {
            id: "1-2",
            label: "笔记本",
            children: [
              {
                id: "1-2-1",
                label: "MateBook X",
                children: [
                  {
                    id: "1-2-1-1",
                    label: "MateBook X Pro",
                  },
                  {
                    id: "1-2-1-2",
                    label: "MateBook X 2022",
                  },
                ],
              },
              {
                id: "1-2-2",
                label: "MateBook D",
                children: [
                  {
                    id: "1-2-2-1",
                    label: "MateBook D 14",
                  },
                  {
                    id: "1-2-2-2",
                    label: "MateBook D 15",
                  },
                ],
              },
              {
                id: "1-2-3",
                label: "MateBook 13",
              },
            ],
          },
        ],
      },
      {
        id: "2",
        label: "小米",
        isExpand: true,
        children: [
          {
            id: "2-1",
            label: "手机",
            children: [
              {
                id: "2-1-1",
                label: "小米数字系列",
              },
              {
                id: "2-1-2",
                label: "Redmi系列",
              },
            ],
          },
          {
            id: "2-2",
            label: "家电",
            children: [
              {
                id: "2-2-1",
                label: "电视",
              },
              {
                id: "2-2-2",
                label: "空调",
              },
            ],
          },
        ],
      },
      {
        id: "3",
        label: "苹果",
        children: [
          {
            id: "3-1",
            label: "手机",
            children: [
              {
                id: "3-1-1",
                label: "iPhone 14",
              },
              {
                id: "3-1-2",
                label: "iPhone 13",
              },
            ],
          },
          {
            id: "3-2",
            label: "平板",
            children: [
              {
                id: "3-2-1",
                label: "iPad Pro",
              },
              {
                id: "3-2-2",
                label: "iPad Air",
              },
            ],
          },
        ],
      },
      {
        id: "4",
        label: "OPPO",
        children: [
          {
            id: "4-1",
            label: "手机",
            children: [
              {
                id: "4-1-1",
                label: "Find系列",
              },
              {
                id: "4-1-2",
                label: "Reno系列",
              },
            ],
          },
          {
            id: "4-2",
            label: "配件",
            children: [
              {
                id: "4-2-1",
                label: "耳机",
              },
              {
                id: "4-2-2",
                label: "手环",
              },
            ],
          },
        ],
      },
      {
        id: "5",
        label: "vivo",
        children: [
          {
            id: "5-1",
            label: "手机",
            children: [
              {
                id: "5-1-1",
                label: "X系列",
              },
              {
                id: "5-1-2",
                label: "S系列",
              },
            ],
          },
          {
            id: "5-2",
            label: "智能设备",
            children: [
              {
                id: "5-2-1",
                label: "手表",
              },
              {
                id: "5-2-2",
                label: "耳机",
              },
            ],
          },
        ],
      },
    ]);

    ui.hideLoading();
  }, 500);
}
</script>
```

*使用 useTree()*

```html
<script lang="ts" setup>
const list = ref<ClTreeItem[]>(
  useTree([
    {
      id: "1",
      label: "A",
      children: [
        {
          id: "1-1",
          label: "A-1",
          children: [
            {
              id: "1-1-1",
              label: "A-1-1",
            },
          ],
        },
      ],
    },
    {
      id: "2",
      label: "B",
    },
  ])
);
</script>
```

*使用 useTree()*

```html
<template>
  <cl-tree ref="treeRef"></cl-tree>
</template>

<script lang="ts" setup>
const treeRef = ref<ClTreeComponentPublicInstance | null>(null);

function expand() {
  treeRef.value!.setExpandedKeys(["4", "5"]);
}

function getExpanded() {
  expandedKeys.value = treeRef.value!.getExpandedKeys();
}

function expandAll() {
  treeRef.value!.expandAll();
  expandedKeys.value = treeRef.value!.getExpandedKeys();
}

function collapseAll() {
  treeRef.value!.collapseAll();
}
</script>
```


## 五、状态组件

### Badge 角标

Badge 角标是一个用于显示数字、文本或者小圆点的状态指示器组件，常用于消息提醒、通知计数等场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| type | 角标主题类型，影响背景颜色 | "primary" \| "success" \| "warn" \| "error" \| "info" | primary/success/warn/error/info | 'error' |
| dot | 是否显示为小圆点样式，开启后忽略 value 参数 | boolean | true/false | false |
| value | 角标显示的内容，可以是数字或文字 | string \| number | - | 0 |
| position | 是否开启绝对定位模式，通常用于相对父元素进行位置调整 | boolean | true/false | false |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |

```html
<cl-badge type="primary" value="1" class="mr-2"></cl-badge>
<cl-badge type="success" value="12" class="mr-2"></cl-badge>
<cl-badge type="warn" value="31" class="mr-2"></cl-badge>
<cl-badge type="error" value="24" class="mr-2"></cl-badge>
<cl-badge type="info" value="17" class="mr-2"></cl-badge>
<cl-badge type="primary" value="41" class="mr-2"></cl-badge>
<cl-badge type="success" value="56" class="mr-2"></cl-badge>
```

```html
<!-- 数字角标 -->
<cl-button>
  购买
  <template #content>
    <cl-badge type="error" value="1" position> </cl-badge>
  </template>
</cl-button>

<!-- 圆点角标 -->
<cl-button>
  消息
  <template #content>
    <cl-badge type="error" dot position> </cl-badge>
  </template>
</cl-button>
```

```html
<view class="flex flex-row overflow-visible">
  <cl-image
    :pt="{
      className: 'overflow-visible'
    }"
    src="https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png"
  >
    <cl-badge type="error" value="+9" position> </cl-badge>
  </cl-image>
</view>
```


### Noticebar 通知栏

通知栏组件用于展示系统通知、公告信息等重要内容，支持水平滚动和垂直轮播两种展示方式，适用于各种信息展示场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| text | 公告文本内容，支持字符串或字符串数组 | string \| string[] | - | - |
| direction | 滚动方向 | string | "horizontal" \| "vertical" | "horizontal" |
| duration | 垂直滚动时的切换间隔时间 | number | - | 3000 |
| speed | 水平滚动时的滚动速度 | number | - | 100 |
| height | 通知栏的高度 | string \| number | - | 40 |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| text | 文本元素配置 | PassThroughProps |

```html
<cl-noticebar
  text="云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。"
></cl-noticebar>
```

```html
<view class="flex flex-row items-center">
  <cl-icon name="notification-4-line" class="mr-2"></cl-icon>
  <cl-noticebar
    text="云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。"
  ></cl-noticebar>
</view>
```

```html
<cl-noticebar
  :speed="40"
  text="云想衣裳花想容，春风拂槛露华浓。若非群玉山头见，会向瑶台月下逢。"
></cl-noticebar>
```


### Countdown 倒计时

倒计时组件用于展示剩余时间，支持多种时间格式和自定义样式，常用于活动倒计时、验证码倒计时等场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| format | 时间格式化模板，支持 {d}天 {h}时 {m}分 {s}秒 | string | - | "{h}:{m}:{s}" |
| hideZero | 是否隐藏值为 0 的时间单位 | boolean | - | false |
| day | 指定倒计时天数 | number | - | 0 |
| hour | 指定倒计时小时数 | number | - | 0 |
| minute | 指定倒计时分钟数 | number | - | 0 |
| second | 指定倒计时秒数 | number | - | 0 |
| datetime | 目标结束时间，可以是 Date 对象或日期字符串 | string \| Date | - | - |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| text | 数字文本元素配置 | PassThroughProps |
| splitor | 分隔符元素配置 | PassThroughProps |

```html
<cl-countdown :datetime="datetime"></cl-countdown>

<script lang="ts" setup>
	import { ref } from "vue";
	import { dayUts } from "@/.cool";

	// 设置倒计时目标时间为 1 分钟后
	const datetime = ref(dayUts().add(1, "minute").toDate());
</script>
```

```html
<cl-countdown :minute="60" hide-zero></cl-countdown>
```

```html
<cl-countdown :day="2" format="{d}天{h}:{m}:{s}"></cl-countdown>
```


### Progress 进度条

一个轻量级的进度条组件，用于展示操作进度或任务完成状态。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| value | 当前进度值（0-100） | number | 0-100 | 0 |
| strokeWidth | 进度条线条宽度(px) | number | - | 12 |
| showText | 是否显示进度百分比文本 | boolean |  | true |
| color | 进度条颜色 | string |  | - |
| unColor | 进度条背景色 | string |  | - |

#### PassThrough 样式穿透

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| outer | 外层进度条元素配置 | PassThroughProps |
| inner | 内层进度条元素配置 | PassThroughProps |
| text | 文本元素配置 | PassThroughProps |

```html
<cl-progress :value="50"></cl-progress>
```

```html
<cl-progress :value="50" :show-text="false"></cl-progress>
```

```html
<!-- 红色主题 -->
<cl-progress :value="30" color="red" un-color="#f7bfbf"></cl-progress>

<!-- 绿色主题 -->
<cl-progress :value="80" color="#52c41a" un-color="#f6ffed"></cl-progress>
```


### ProgressCircle 圆形进度条

一个轻量级的圆形进度条组件，用于展示操作进度或任务完成状态。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式透传配置对象 | PassThrough | - | - |
| value | 当前进度值（0-100） | number | 0-100 | 0 |
| strokeWidth | 进度条线条宽度(px) | number | - | 8 |
| size | 进度条大小(px) | number |  | 120 |
| showText | 是否显示进度百分比文本 | boolean |  | true |
| unit | 单位 | string |  | "%" |
| color | 进度条颜色 | string |  | - |
| unColor | 进度条背景色 | string |  | - |
| startAngle | 起始角度 (弧度) | number |  | -Math.PI / 2 |
| clockwise | 是否顺时针 | boolean |  | true |
| duration | 动画时长 | string |  | 500 |

#### PassThrough 样式穿透

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| text | 文本元素配置 | PassThroughProps |

```html
<cl-progress-circle :value="50"></cl-progress-circle>
```

```html
<cl-progress-circle :value="50" :show-text="false"></cl-progress-circle>
```

```html
<!-- 红色主题 -->
<cl-progress-circle :value="30" color="red" un-color="#f7bfbf"></cl-progress-circle>

<!-- 绿色主题 -->
<cl-progress-circle :value="80" color="#52c41a" un-color="#f6ffed"></cl-progress-circle>
```


### Skeleton 骨架图

骨架图组件用于在数据加载过程中显示页面的基本结构，避免页面的突然变化，为用户提供更好的视觉体验。组件支持多种预设类型，也可以通过组合使用来构建复杂的骨架结构。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| loading | 是否显示骨架图 | boolean | true / false | true |
| type | 骨架图类型 | string | "text" \| "image" \| "circle" \| "button" | "text" |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| loading | 加载状态下配置 | PassThroughProps |

```html
<!-- 显示骨架图 -->
<cl-skeleton loading>
	<cl-text>云想衣裳花想容，春风拂槛露华浓。</cl-text>
</cl-skeleton>

<!-- 隐藏骨架图，显示真实内容 -->
<cl-skeleton :loading="false">
	<cl-text>云想衣裳花想容，春风拂槛露华浓。</cl-text>
</cl-skeleton>
```

```html
<view class="flex flex-row">
	<cl-skeleton type="button" loading>
		<cl-button>立即购买</cl-button>
	</cl-skeleton>

	<cl-skeleton type="button" loading class="ml-3">
		<cl-button type="plain">加入购物车</cl-button>
	</cl-skeleton>
</view>
```

```html
<cl-skeleton type="image" loading>
	<cl-image src="https://uni-docs.cool-js.com/demo/pages/demo/static/bg1.png"></cl-image>
</cl-skeleton>
```


### Loadmore 加载更多

用于列表底部的加载状态提示组件，支持加载中和加载完成两种状态的显示。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| loading | 是否正在加载中 | boolean | - | false |
| loadingText | 加载中状态的显示文本 | string | - | "加载中" |
| finish | 是否已加载完成（无更多数据） | boolean | - | false |
| finishText | 加载完成状态的显示文本 | string | - | "没有更多了" |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| icon | 加载图标配置 | PassThroughProps |
| text | 文本内容配置 | PassThroughProps |

```html
<cl-loadmore loading></cl-loadmore>
```

```html
<cl-loadmore :loading="loading" :finish="finish"></cl-loadmore>

<script lang="ts" setup>
  import { ref } from "vue";

  const loading = ref(true);
  const finish = ref(false);

  setTimeout(() => {
    loading.value = false;
    finish.value = true;
  }, 3000);
</script>
```


### RollingNumber 数字滚动

一个具有平滑动画效果的数字滚动组件，支持从一个数值平滑过渡到另一个数值，常用于数据展示、计数器等场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| value | 目标数字值，组件将从当前值滚动到此数值 | number | - | 0 |
| duration | 动画持续时间，单位为毫秒 | number | - | 1000 |
| decimals | 小数位数，控制数字显示的精度 | number | - | 0 |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| color | 数字颜色 | string |

```html
<cl-rolling-number :value="1000"></cl-rolling-number>
```

```html
<cl-rolling-number :value="1000" :duration="300"></cl-rolling-number>
```

```html
<!-- 显示两位小数 -->
<cl-rolling-number :value="1000.58" :decimals="2"></cl-rolling-number>
```


## 六、反馈组件

### ActionSheet 操作菜单

用于从底部弹出的操作菜单，为用户提供多个操作选项的选择界面。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| item | 菜单项配置 | PassThroughProps |

```html
type ClActionSheetItem = {
	label: string; // 标签内容
	icon?: string; // 图标
	disabled?: boolean; // 是否禁用
	color?: string; // 字体、图标颜色
	callback?: () => void; // 点击回掉
};

type ClActionSheetOptions = {
	list: ClActionSheetItem[]; // 菜单列表
	title?: string; // 标题
	description?: string; // 描述
	cancelText?: string; // 取消文案，默认取消
	showCancel?: boolean; // 是否显示取消按钮，默认true
	maskClosable?: boolean; // 点击遮罩是否关闭，默认true
};
```

```html
<template>
	<cl-button @tap="open">打开操作菜单</cl-button>
	<cl-action-sheet ref="actionSheetRef" />
</template>

<script lang="ts" setup>
import { ref } from "vue";
import type { ClActionSheetOptions } from "@/uni_modules/cool-ui";

const actionSheetRef = ref<ClActionSheetComponentPublicInstance | null>(null);

function open() {
	actionSheetRef.value!.open({
		list: [
			{
				label: "反馈"
			}
		]
	} as ClActionSheetOptions);
}
</script>
```

```html
<template>
	<cl-button @tap="open">打开带图标的菜单</cl-button>
	<cl-action-sheet ref="actionSheetRef" />
</template>

<script lang="ts" setup>
import { ref } from "vue";
import type { ClActionSheetOptions } from "@/uni_modules/cool-ui";

const actionSheetRef = ref<ClActionSheetComponentPublicInstance | null>(null);

function open() {
	actionSheetRef.value!.open({
		list: [
			{
				label: "反馈",
				icon: "feedback-line"
			},
			{
				label: "设置",
				icon: "settings-line"
			}
		]
	} as ClActionSheetOptions);
}
</script>
```


### Popup 弹出框

一个功能丰富的弹出框组件，支持多方向弹出、拖拽关闭、自定义样式等特性。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置，用于自定义组件内部元素样式 | PassThrough | - | - |
| modelValue | 控制弹窗显示隐藏状态 | boolean | - | false |
| title | 弹窗标题文本 | string | - |  |
| direction | 弹出方向 | "top" \| "right" \| "bottom" \| "center" \| "left" | - | "bottom" |
| size | 弹出框尺寸（根据方向决定宽度或高度） | string \| number | - |  |
| showHeader | 是否显示头部区域 | boolean | - | true |
| showClose | 是否显示关闭按钮 | boolean | - | true |
| showMask | 是否显示遮罩层 | boolean | - | true |
| maskClosable | 点击遮罩层是否关闭弹窗 | boolean | - | true |
| swipeClose | 是否启用拖拽关闭功能 | boolean | - | true |
| swipeCloseThreshold | 拖拽关闭触发距离（单位：px） | number | - | 150 |
| pointerEvents | 触摸事件响应方式 | "auto" \| "none" | - | "auto" |
| keepAlive | 是否启用内容缓存 | boolean | - | false |
| enablePortal | 是否插入到最外层 | boolean | - | true |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| inner | 弹窗主体容器配置 | PassThroughProps |
| header | 头部区域配置 | PassThroughProps |
| container | 内容区域配置 | PassThroughProps |
| mask | 遮罩层配置 | PassThroughProps |
| draw | 拖拽指示器配置 | PassThroughProps |

```html
<cl-button @tap="open">打开弹窗</cl-button>

<cl-popup v-model="visible" title="诗词欣赏">
  <view class="p-4">
    <cl-text>
      春江花月夜，花草复青青。<br />
      江水流不尽，月光照无情。<br />
      夜来风雨急，愁思满心头。<br />
      何时再相见，共赏月明楼。
    </cl-text>
  </view>
</cl-popup>

<script lang="ts" setup>
  import { ref } from "vue";

  const visible = ref(false);

  function open() {
    visible.value = true;
  }
</script>
```

```html
<cl-button @tap="open">无头部弹窗</cl-button>

<cl-popup v-model="visible" :show-header="false">
  <view class="p-4">
    <cl-text> 这是一个没有头部的弹窗， 所有内容都可以自由定制。 </cl-text>
  </view>
</cl-popup>

<script lang="ts" setup>
  import { ref } from "vue";

  const visible = ref(false);

  function open() {
    visible.value = true;
  }
</script>
```

```html
<cl-button @tap="open()">打开</cl-button>

<cl-popup v-model="visible" direction="bottom" title="弹出方向">
  <view class="p-4">
    <cl-text>
      春江花月夜，花草复青青。 江水流不尽，月光照无情。 夜来风雨急，愁思满心头。
      何时再相见，共赏月明楼。
    </cl-text>
  </view>
</cl-popup>

<script lang="ts" setup>
  import { ref } from "vue";

  const visible = ref(false);

  function open() {
    visible.value = true;
  }
</script>
```


### Confirm 确认框

用于重要操作的二次确认，避免用户误操作。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| title | 标题 | string | - | - |
| message | 消息内容 | string | - | - |
| confirmText | 确认按钮文案 | string | - | "确认" |
| showConfirm | 显示确认按钮 | boolean | - | true |
| cancelText | 取消按钮文案 | string | - | "取消" |
| showCancel | 显示取消按钮 | boolean | - | true |
| duration | 自动关闭时长 | number | - | 0 |
| callback | 关闭回调 | (action: ClConfirmAction) => void | - | - |
| beforeClose | 关闭前钩子 | (action: ClConfirmAction, event: ClConfirmBeforeCloseEvent) => void | - | - |

```html
type ClConfirmAction = "confirm" | "cancel" | "close";

type ClConfirmBeforeCloseEvent = {
  close: () => void;
  showLoading: () => void;
  hideLoading: () => void;
};

type ClConfirmOptions = {
  title: string;
  message: string;
  confirmText?: string;
  showConfirm?: boolean;
  cancelText?: string;
  showCancel?: boolean;
  duration?: number;
  callback?: (action: ClConfirmAction) => void;
  beforeClose?: (
    action: ClConfirmAction,
    event: ClConfirmBeforeCloseEvent
  ) => void;
};
```

```html
import { useUi } from "@/uni_modules/cool-ui";

const ui = useUi();

ui.showConfirm({
  title: "删除确认",
  message: "确定要删除这条记录吗？删除后不可恢复。",
  callback(action) {
    if (action === "confirm") {
      console.log("用户确认删除");
      // 执行删除操作
    } else {
      console.log("用户取消操作");
    }
  },
});
```

```html
import { useUi } from "@/uni_modules/cool-ui";

const ui = useUi();

function showCustomText() {
  ui.showConfirm({
    title: "退出确认",
    message: "确定要退出当前账户吗？",
    confirmText: "退出",
    cancelText: "留下",
    callback(action) {
      if (action === "confirm") {
        // 执行退出登录
      }
    },
  });
}
```


### Toast 提示框

Toast 组件用于向用户显示简短的消息反馈，支持多种类型和位置配置。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| type | 提示类型 | string | success \| warn \| error \| question \| disabled \| stop | - |
| icon | 自定义图标 | string | - | - |
| image | 自定义图片 | string | - | - |
| message | 提示内容 | string | - | - |
| position | 显示位置 | string | top \| center \| bottom | center |
| duration | 自动关闭时长 | number | - | 3000(ms) |
| clear | 清除其他提示 | boolean | - | false |

```html
type ClToastPosition = "top" | "center" | "bottom";

type ClToastType =
  | "success"
  | "warn"
  | "error"
  | "question"
  | "disabled"
  | "stop";

type ClToastOptions = {
  type?: ClToastType;
  icon?: string;
  image?: string;
  message: string;
  position?: ClToastPosition;
  duration?: number;
  clear?: boolean;
};
```

```html
import { useUi } from "@/uni_modules/cool-ui";

const ui = useUi();

ui.showToast({
  message: "保存成功",
});
```

```html
import { useUi } from "@/uni_modules/cool-ui";

const ui = useUi();

// 顶部显示
ui.showToast({
  message: "操作成功",
  position: "top",
});

// 中间显示（默认）
ui.showToast({
  message: "操作成功",
  position: "center",
});

// 底部显示
ui.showToast({
  message: "操作成功",
  position: "bottom",
});
```


## 七、其他组件

### Qrcode 二维码

二维码组件，支持自定义样式、LOGO 嵌入和图片导出功能。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| width | 二维码宽度 | string | - | 200px |
| height | 二维码高度 | string | - | 200px |
| foreground | 二维码前景色 | string | - | #131313 |
| background | 二维码背景色 | string | - | #ffffff |
| pdColor | 定位点颜色，不填写时与前景色一致 | string | - | - |
| pdRadius | 定位图案圆角半径 | number | - | 10 |
| text | 二维码内容 | string | - | " https://cool-js.com/ " |
| logo | logo 图片地址，支持网络、本地路径 | string | - | - |
| logoSize | logo 大小 | string | - | 50px |
| padding | 二维码边距 | number | - | 20 |
| mode | 二维码样式 | string | "rect" \| "circular" \| "line" \| "rectSmall" | "rect" |

```html
<cl-qrcode text="https://cool-js.com/"></cl-qrcode>
```

```html
<cl-qrcode
  text="https://cool-js.com/"
  logo="/static/logo2.png"
  logo-size="60px"
>
</cl-qrcode>
```

```html
<cl-qrcode text="https://cool-js.com/" :pd-radius="50"> </cl-qrcode>
```


### Sign 签名

签名组件，提供手写签名功能，支持毛笔效果、自定义样式和图片导出。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| width | 画布宽度 | number | - | windowWidth |
| height | 画布高度 | number | - | 200 |
| strokeColor | 线条颜色 | string | - | #000000 |
| strokeWidth | 线条宽度 | number | - | 3 |
| backgroundColor | 背景颜色 | string | - | #ffffff |
| enableBrush | 是否启用毛笔效果 | boolean | - | true |
| minStrokeWidth | 最小线条宽度 | number | - | 1 |
| maxStrokeWidth | 最大线条宽度 | number | - | 6 |
| velocitySensitivity | 速度敏感度 | number | - | 0.7 |

```html
<cl-sign></cl-sign>
```

```html
<cl-sign enable-brush></cl-sign>
```

```html
<template>
  <cl-sign :width="width" :height="height"></cl-sign>
</template>

<script setup lang="ts">
const height = ref(0);
const width = ref(0);

onReady(() => {
  const { windowWidth, windowHeight } = uni.getWindowInfo();

  height.value = windowHeight;
  width.value = windowWidth;
});
</script>
```


### Watermark 水印

水印组件，用于在页面或内容上添加水印效果，支持文字水印、自定义样式和深色模式适配。通过 Canvas 绘制实现高性能的水印渲染，支持自定义文字、颜色、大小、旋转角度、间距等参数，可灵活应用于版权保护、内容标识等场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| text | 水印文本 | string | - | "Watermark" |
| fontSize | 水印字体大小 | number | - | 16 |
| color | 水印文字颜色（浅色模式） | string | - | "rgba(0, 0, 0, 0.15)" |
| darkColor | 水印文字颜色（深色模式） | string | - | "rgba(255, 255, 255, 0.15)" |
| opacity | 水印透明度 | number | - | 1 |
| rotate | 水印旋转角度 | number | - | -22 |
| width | 水印宽度 | number | - | 120 |
| height | 水印高度 | number | - | 64 |
| gapX | 水印之间的水平间距 | number | - | 100 |
| gapY | 水印之间的垂直间距 | number | - | 100 |
| zIndex | 水印层级 | number | - | 9 |
| fontWeight | 字体粗细 | string | - | "normal" |
| fontFamily | 字体样式 | string | - | "sans-serif" |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素的样式配置 | string |
| container | 内容容器元素的样式配置 | PassThroughProps |

```html
<cl-watermark>
  <view class="p-4 bg-gray-100 h-40">
    <text>这里是需要添加水印的内容</text>
  </view>
</cl-watermark>
```

```html
<cl-watermark text="版权所有">
  <view class="p-4 bg-gray-100 h-40">
    <text>这里是需要添加水印的内容</text>
  </view>
</cl-watermark>
```

```html
<cl-watermark
  text="CONFIDENTIAL"
  :font-size="20"
  color="rgba(255, 0, 0, 0.3)"
  :rotate="-45"
  :opacity="0.8"
  font-weight="bold"
>
  <view class="p-4 bg-gray-100 h-40">
    <text>机密文档内容</text>
  </view>
</cl-watermark>
```


### Cropper 图片裁剪

图片裁剪组件，支持自定义裁剪框大小、形状，并提供图片旋转、缩放等功能。可用于头像裁剪、图片编辑等场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| cropWidth | 裁剪宽度 | number | - | 300 |
| cropHeight | 裁剪高度 | number | - | 300 |
| maxScale | 图片最大缩放倍数 | number | - | 3 |
| resizable | 是否可以自定义裁剪框大小 | boolean | - | false |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素样式 | string |
| image | 图片元素配置 | PassThroughProps |
| op | 操作栏元素配置 | PassThroughProps |
| opItem | 操作项按钮元素配置 | PassThroughProps |
| mask | 遮罩层元素配置 | PassThroughProps |
| cropBox | 裁剪框元素配置 | PassThroughProps |

```html
<template>
  <cl-button @tap="chooseImage">{{ t("选择图片") }}</cl-button>
  <cl-cropper ref="cropperRef" @crop="onCrop" @load="onImageLoad"></cl-cropper>
</template>

<script lang="ts" setup>
const cropperRef = ref<ClCropperComponentPublicInstance | null>(null);

function chooseImage() {
  // 方法一，调用 open 方法打开
  uni.chooseImage({
    count: 1,
    sizeType: ["original", "compressed"],
    sourceType: ["album", "camera"],
    success: (res) => {
      if (res.tempFilePaths.length > 0) {
        cropperRef.value!.open(res.tempFilePaths[0]);
      }
    },
  });

  // 方法二，调用选择图片方法打开裁剪
  cropperRef.value!.chooseImage();
}

function onCrop(url: string) {
  uni.previewImage({
    urls: [url],
  });
}

function onImageLoad(e: UniImageLoadEvent) {
  console.log("onImageLoad", e);
}
</script>
```

<!-- 更多参数查阅：https://doc.dcloud.net.cn/uni-app-x/component/image.html#uniimageloadevent -->


### Canvas 画布

cl-canvas 组件是一个基于 canvas 封装的画布组件，支持图片裁剪、文字多行省略、变形转换等丰富功能，适用于生成海报、图片处理、签名等多种场景。你可以通过配置参数和调用方法，灵活实现自定义绘制、图片导出等操作。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| canvasId | 画布 ID | string | - | - |
| height | 画布宽度 | number | - | 300 |
| width | 画布高度 | number | - | 300 |

```html
type TextRenderOptions = {
  x: number; // 文字起始横坐标
  y: number; // 文字起始纵坐标
  height?: number; // 文字区域高度（可选）
  width?: number; // 文字区域宽度（可选）
  content: string; // 文字内容
  color?: string; // 文字颜色（可选）
  fontSize?: number; // 字体大小（可选）
  fontFamily?: string; // 字体（可选）
  fontWeight?: "normal" | "bold" | "bolder" | "lighter" | number; // 字重（可选）
  textAlign?: "left" | "right" | "center"; // 对齐方式（可选）
  overflow?: "ellipsis"; // 超出省略（可选，支持省略号）
  lineClamp?: number; // 最大显示行数（可选）
  letterSpace?: number; // 字符间距（可选）
  lineHeight?: number; // 行高（可选）
  opacity?: number; // 透明度（可选）
  scale?: number; // 缩放比例（可选，整体缩放）
  scaleX?: number; // 横向缩放（可选）
  scaleY?: number; // 纵向缩放（可选）
  rotate?: number; // 旋转角度（可选，单位：度）
  translateX?: number; // 横向平移（可选）
  translateY?: number; // 纵向平移（可选）
};
```

```html
<template>
  <cl-page>
    <cl-canvas
      ref="canvasRef"
      canvas-id="test"
      :height="300"
      :width="300"
      @load="onCanvasLoad"
    ></cl-canvas>
  </cl-page>
</template>

<script lang="ts" setup>
import { ClCanvas } from "@/uni_modules/cool-canvas";

function onCanvasLoad(canvas: ClCanvas) {
  canvas
    .text({
      x: 10,
      y: 10,
      content: "神仙都没用",
      color: "#666666",
    })
    .draw();
}
</script>
```

```html
type DivRenderOptions = {
  x: number; // 横坐标
  y: number; // 纵坐标
  height?: number; // 高度（可选）
  width?: number; // 宽度（可选）
  radius?: number; // 圆角半径（可选）
  backgroundColor?: string; // 背景颜色（可选）
  borderWidth?: number; // 边框宽度（可选）
  borderColor?: string; // 边框颜色（可选）
  opacity?: number; // 透明度（可选）
  scale?: number; // 缩放比例（可选，整体缩放）
  scaleX?: number; // 横向缩放（可选）
  scaleY?: number; // 纵向缩放（可选）
  rotate?: number; // 旋转角度（可选，单位：度）
  translateX?: number; // 横向平移（可选）
  translateY?: number; // 纵向平移（可选）
};
```


### Svg 图标

适用于图标、装饰性元素等多种场景，推荐结合 Tailwind CSS 的 w- 、 h- 类控制尺寸。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| src | 数据源 | string | - | "" |
| color | 图标颜色 | string | - | "" |

```html
<cl-svg src="/static/demo/svg/category.svg" class="h-6 w-6"></cl-svg>
<cl-svg src="/static/demo/svg/shopping-cart.svg" class="h-6 w-6 ml-3"></cl-svg>
<cl-svg src="/static/demo/svg/points.svg" class="h-6 w-6 ml-3"></cl-svg>
```

```html
<cl-svg src="/static/demo/svg/points.svg" class="h-10 w-10"></cl-svg>
<cl-svg src="/static/demo/svg/points.svg" class="h-8 w-8 ml-3"></cl-svg>
<cl-svg src="/static/demo/svg/points.svg" class="h-6 w-6 ml-3"></cl-svg>
```

```html
<cl-svg :src="svg" class="h-6 w-6"></cl-svg>

<script lang="ts" setup>
  const svg = ref(
    `<svg t="1756119341770" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7779" width="64" height="64"><path d="M783.1 899.3H242.9c-97.7 0-177.3-79.5-177.3-177.3V302.6c0-97.7 79.5-177.3 177.3-177.3H783c97.7 0 177.3 79.5 177.3 177.3V722c0.1 97.7-79.5 177.3-177.2 177.3zM242.9 214.8c-48.4 0-87.8 39.4-87.8 87.8V722c0 48.4 39.4 87.8 87.8 87.8H783c48.4 0 87.8-39.4 87.8-87.8V302.6c0-48.4-39.4-87.8-87.8-87.8H242.9z" fill="#333333" p-id="7780"></path><path d="M513 600.5c-24.9 0-49.9-7.3-71.6-21.8l-2.9-2.1-214.9-170.1c-19.4-15.3-22.7-43.5-7.3-62.8 15.3-19.4 43.5-22.6 62.8-7.3l213.2 168.8c12.7 7.8 28.7 7.8 41.5 0L747 336.4c19.3-15.3 47.5-12.1 62.8 7.3 15.3 19.4 12.1 47.5-7.3 62.8L584.6 578.7c-21.7 14.5-46.7 21.8-71.6 21.8z" fill="#333333" p-id="7781"></path></svg>`
  );
</script>
```


### SlideVerify 滑动验证

滑动验证组件，支持滑块模式和图片拼图模式，常用于登录、注册等场景下的人机验证。通过拖动滑块或拼图，验证用户的操作行为，有效防止恶意请求和机器人攻击。组件支持多种自定义参数，可灵活配置样式、验证模式、提示信息等，满足不同业务需求。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| pt | 样式穿透配置 | PassThrough | - | - |
| modelValue | 是否验证成功 | boolean | - | false |
| mode | 验证模式 | string | "slide" \| "image" | "slide" |
| size(px) | 滑块大小 | number | - | 40 |
| disabled | 是否禁用 | boolean | - | false |
| imageUrl | 图片 URL（图片模式使用） | string | - | "" |
| imageSize | 图片大小（图片模式使用）） | number \| string | - | 300 |
| angleThreshold | 角度容错范围 | number | - | 10 |
| showFail | 是否错误提示 | boolean | - | true |
| failText | 错误提示文字 | string | - | "验证失败" |

#### PassThrough 样式穿透

| 参数 | 说明 | 类型 |
| --- | --- | --- |
| className | 组件根元素的样式配置 | string |
| track | 滑道轨迹元素的元素配置 | PassThroughProps |
| image | 图片元素的元素配置 | PassThroughProps |
| progress | 进度条元素的元素配置 | PassThroughProps |
| slider | 滑块元素的元素配置 | PassThroughProps |
| icon | 图标元素的元素配置 | PassThroughProps |
| text | 提示文字的元素配置 | PassThroughProps |
| label | 标签元素的元素配置 | PassThroughProps |

```html
<cl-slide-verify v-model="status" @success="onSuccess" @fail="onFail"></cl-slide-verify>
```

```html
<cl-slide-verify :show-fail="false"></cl-slide-verify>
```

```html
<cl-slide-verify
	mode="image"
	image-url="https://unix.cool-js.com/images/demo/avatar.jpg"
></cl-slide-verify>
```


### Animation 动画

动画（Animation）用于为元素添加动态效果，提升界面交互的流畅性和视觉吸引力。通过 AnimationEngine，你可以方便地为任意元素实现淡入淡出、滑动、缩放、旋转、弹跳等多种常见动画效果，并支持动画的播放、暂停、恢复、重置等操作。动画支持链式调用和异步控制，适用于页面过渡、弹窗、提示等多种场景。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| duration | 动画持续时间（毫秒） | number |  | 300 |
| loop | 循环次数，-1 为无限循环 | number |  | 1 |
| alternate | 是否往返播放 | boolean |  | false |
| sequential | 是否按属性顺序依次执行动画 | boolean |  | false |
| timingFunction | 缓动函数名称 | string |  | 'linear' |
| bezier | 自定义贝塞尔曲线参数 | number[] |  | undefined |
| complete | 动画完成回调 | () => void |  | undefined |
| start | 动画开始回调 | () => void |  | undefined |
| frame | 每帧回调，参数为进度（0~1） | (progress: number) => void |  | undefined |

```html
<template>
  <view ref="viewRef" class="h-10 w-10 bg-primary-500 rounded-lg"></view>
</template>

<script lang="ts" setup>
onReady(() => {
  createAnimation(viewRef.value, {
    duration: 1000,
  })
    .rotate("0deg", "360deg")
    .play();
});
</script>
```

```html
<template>
  <view ref="viewRef" class="h-10 w-10 bg-primary-500 rounded-lg"></view>
</template>

<script lang="ts" setup>
onReady(() => {
  createAnimation(viewRef.value, {
    duration: 1000,
    loop: -1,
  })
    .rotate("0deg", "360deg")
    .play();
});
</script>
```

```html
<template>
  <view ref="viewRef" class="h-10 w-10 bg-primary-500 rounded-lg"></view>
</template>

<script lang="ts" setup>
onReady(() => {
  createAnimation(viewRef.value, {
    duration: 1000,
    loop: -1,
    alternate: true,
  })
    .rotate("0deg", "360deg")
    .play();
});
</script>
```


### SelectSeat 座位选择

座位选择组件，支持缩放、拖动、自定义样式和图片渲染，适用于电影院、剧院等场景的座位选择。

「参数」

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| v-model | 已选座位数组 | ClSelectSeatValue[] | - | [] |
| rows | 行数 | number | - | 0 |
| cols | 列数 | number | - | 0 |
| width | 组件宽度(px) | number | - | 0 |
| height | 组件高度(px) | number | - | 0 |
| seats | 座位数据，不传则自动生成 | ClSelectSeatItem[] | - | [] |
| seatGap | 座位间距 | number | - | 8 |
| borderRadius | 座位圆角 | number | - | 8 |
| borderWidth | 边框宽度 | number | - | 1 |
| minScale | 最小缩放比例 | number | - | 1 |
| maxScale | 最大缩放比例 | number | - | 3 |
| color | 座位图标颜色 | string | surface-300 |  |
| darkColor | 暗色模式座位图标颜色 | string | surface-500 |  |
| bgColor | 座位背景色 | string | #ffffff |  |
| darkBgColor | 暗色模式座位背景色 | string | surface-800 |  |
| borderColor | 边框颜色 | string | surface-200 |  |
| darkBorderColor | 暗色模式边框颜色 | string | surface-600 |  |
| selectedBgColor | 选中背景色 | string | primary-500 |  |
| selectedColor | 选中图标颜色 | string | #ffffff |  |
| image | 座位图片 | string | - |  |
| selectedImage | 选中座位图片 | string | - |  |
| selectedIcon | 选中图标 | string | check-line |  |

```html
// 选中值类型
interface ClSelectSeatValue {
	row: number;
	col: number;
}

// 座位项类型
interface ClSelectSeatItem {
	row: number;
	col: number;
	disabled?: boolean; // 是否禁用
	empty?: boolean; // 是否为空位（不渲染）
	bgColor?: string; // 自定义背景色
	borderColor?: string; // 自定义边框色
	selectedBgColor?: string; // 自定义选中背景色
	selectedColor?: string; // 自定义选中图标色
	selectedIcon?: string; // 自定义选中图标
	selectedImage?: string; // 自定义选中图片
	icon?: string; // 自定义图标
	image?: string; // 自定义图片
	color?: string; // 自定义图标颜色
}
```

```html
<template>
	<cl-select-seat
		v-model="selectedSeats"
		:rows="10"
		:cols="12"
		:width="350"
		:height="400"
	></cl-select-seat>
</template>

<script lang="ts" setup>
	import type { ClSelectSeatValue } from "@/uni_modules/cool-ui/types";

	const selectedSeats = ref<ClSelectSeatValue[]>([]);
</script>
```

```html
<template>
	<cl-select-seat
		v-model="selectedSeats"
		:rows="5"
		:cols="8"
		:width="350"
		:height="250"
		:seats="seats"
	></cl-select-seat>
</template>

<script lang="ts" setup>
	import type { ClSelectSeatItem, ClSelectSeatValue } from "@/uni_modules/cool-ui/types";

	const selectedSeats = ref<ClSelectSeatValue[]>([]);

	const seats = ref<ClSelectSeatItem[]>([]);

	// 初始化座位
	for (let row = 0; row < 5; row++) {
		for (let col = 0; col < 8; col++) {
			const seat: ClSelectSeatItem = { row, col };

			// 设置部分座位为已售（禁用）
			if ((row === 2 && col === 3) || (row === 2 && col === 4)) {
				seat.disabled = true;
				seat.bgColor = "#ef4444";
			}

			// 设置走廊（空位）
			if (col === 4 && row < 2) {
				seat.empty = true;
			}

			seats.value.push(seat);
		}
	}
</script>
```
