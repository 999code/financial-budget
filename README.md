# 家庭财务管理系统

一个用于管理家庭收支、账户、分类与预算的全栈示例项目。

- **前端**：Vue 3 + Vite + Element Plus（位于 `frontend/`）
- **后端**：FastAPI + SQLAlchemy + SQLite（位于 `backend/`）

## 模块设计
| 模块 | 说明 |
| --- | --- |
| 仪表盘 Dashboard | 净资产、累计收支、账户数概览 |
| 账户 Accounts | 现金 / 银行卡 / 信用卡 / 投资账户等 |
| 收支管理 IncomeExpense | 固定收支（按月/年周期、含按期明细、合计金额、当年金额）与临时收支（按收入/支出分类） |
| 贷款管理 Loans | 贷款记录（总价 / 首付 / 贷款金额 / 利率 / 年限），自动算月供（等额本息、等额本金可选）并同步成固定收支里的每月支出 |
| 用户中心 Auth | 登录 / 注册 / 个人信息 / 修改密码（前端路由守卫 + 个人接口令牌校验） |
| 用户管理 Users（管理员专属） | 成员账号列表，支持新增 / 编辑 / 删除（仅 `admin` 可见可用） |

> 早期设计中的「收支记录、分类管理、预算管理」页面已从前端移除，仅后端保留对应接口。

## 账号说明
- 通过登录页「注册」自行创建账号；注册 / 登录成功后返回令牌并自动登录。
- 系统内置初始账号：`admin`（昵称「管理员」）与 `user1`，默认密码均为 `123456`。
- **权限差异**：`用户管理` 菜单仅对 `admin` 账号显示；非管理员（如 `user1`）侧边栏无此入口，且直接访问 `/users` 会被前端路由守卫重定向，后端 `/api/v1/users` 接口也仅管理员令牌可访问（其余返回 403）。
- 登录后可在「个人信息 / 修改密码」中修改昵称、联系方式与密码；管理员可通过「用户管理」页面维护成员账号。

## 快速启动

### 1. 后端
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
接口文档：http://127.0.0.1:8000/docs

### 2. 前端
```bash
cd frontend
npm install
npm run dev
```
访问：http://localhost:5173 （`/api` 已代理到后端 8000）

## 后续可扩展
- 数据库迁移（Alembic）、切换到 PostgreSQL/MySQL
- 图表统计（ECharts）、收支趋势、预算执行率
- 收支 / 预算等业务接口接入鉴权（当前仅登录注册与个人接口强制校验令牌）
- 多成员权限、数据导入导出
