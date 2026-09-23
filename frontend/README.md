# 家庭财务管理系统 · 前端

基于 **Vue 3 + Vite + Element Plus** 的单页应用。

## 技术栈
- Vue 3（`<script setup>` 组合式 API）
- Vite 5：构建与开发服务器
- Element Plus：UI 组件库
- Pinia：状态管理
- Vue Router 4：路由
- Axios：HTTP 请求

## 目录结构
```
frontend/
├── index.html
├── vite.config.js        # 含 /api 代理到后端 8000
├── src/
│   ├── main.js           # 应用入口（Element Plus 中文语言包）
│   ├── App.vue
│   ├── router/           # 路由（含登录守卫 beforeEach）
│   ├── store/            # Pinia 状态：app / auth
│   ├── api/              # 接口封装（axios）：request/accounts/auth/incomeExpense/...
│   ├── layout/           # 整体布局（侧边栏 + 顶栏 + 用户菜单）
│   ├── views/            # 页面：Dashboard/Accounts/IncomeExpense/Login/Register/Profile/ChangePassword/Example
│   └── styles/
```

## 快速开始
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（默认 5173，/api 自动代理到后端 8000）
npm run dev

# 生产构建
npm run build
```

启动后访问：http://localhost:5173

> 注意：开发时需后端在 `http://127.0.0.1:8000` 运行，或由 vite proxy 转发 `/api`。

## 登录与鉴权
- 路由守卫（`router/index.js` 的 `beforeEach`）：未登录访问站内页面自动跳转到 `/login`，并带上回跳地址；已登录不会再进入登录/注册页。
- `store/auth.js`：以 Pinia 维护 `token` 与 `user`，持久化到 `localStorage`。
- 请求拦截器（`api/request.js`）：自动为请求附加 `Authorization: Bearer <token>`；收到 `401` 自动清除登录态并跳登录页。
- 顶栏用户菜单（MainLayout）：可进入「个人信息 / 修改密码」或退出登录。

## 页面说明
| 页面 | 路由 | 说明 |
| --- | --- | --- |
| 仪表盘 | `/dashboard` | 净资产、累计收支、账户数概览 |
| 账户管理 | `/accounts` | 现金/银行卡/信用卡/投资等账户 |
| 收支管理 | `/income-expense` | 固定收支（周期、合计金额、当年金额、按期明细）+ 临时收支（收入/支出分类），列表含净额合计行 |
| 个人信息 | `/profile` | 查看与修改昵称、手机号、邮箱 |
| 修改密码 | `/change-password` | 校验原密码后设置新密码 |
| 登录 / 注册 | `/login` `/register` | 独立页面，不带侧边栏 |
