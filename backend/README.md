# 家庭财务管理系统 · 后端

基于 **FastAPI + SQLAlchemy** 的家庭财务管理后端服务。

## 技术栈
- FastAPI：Web 框架
- SQLAlchemy 2.x：ORM
- SQLite：默认数据库（零配置，可直接运行）
- Pydantic / pydantic-settings：数据校验与配置

## 目录结构
```
backend/
├── app/
│   ├── main.py          # 应用入口（含 CORS、路由、概览接口）
│   ├── config.py        # 配置（环境变量）
│   ├── database.py      # 引擎 / 会话 / Base / SQLite 轻量迁移(ensure_columns)
│   ├── security.py      # 密码哈希(pbkdf2) 与 HMAC 令牌签发/校验
│   ├── models/          # ORM 模型：User/Account/Category/Transaction/Budget/IncomeExpense/IncomeExpenseDetail
│   ├── schemas/         # Pydantic 模型
│   └── api/             # 路由：auth/users/accounts/categories/transactions/budgets/income_expense
└── requirements.txt
```

## 快速开始
```bash
cd backend

# 1. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务（自动建表）
uvicorn app.main:app --reload --port 8000
```

启动后访问：
- API 文档：http://127.0.0.1:8000/docs
- 概览接口：http://127.0.0.1:8000/api/v1/summary

## 接口一览（`/api/v1` 前缀）
| 资源 | 方法 | 鉴权 |
| --- | --- | --- |
| `/auth/register` | POST（注册并返回令牌） | 开放 |
| `/auth/login` | POST（登录并返回令牌） | 开放 |
| `/auth/me` | GET / PUT（个人信息） | 需 Bearer 令牌 |
| `/auth/change-password` | POST（修改密码） | 需 Bearer 令牌 |
| `/users` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 仅管理员（username=`admin`）令牌可访问，否则 403；未带令牌 401 |
| `/accounts` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 需 Bearer 令牌（仅本人数据） |
| `/income-expense` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 需 Bearer 令牌（仅本人数据） |
| `/income-expense/{id}/details` | GET / POST（按期明细） | 需 Bearer 令牌（仅本人数据） |
| `/income-expense/{id}/details/{detail_id}` | PUT / DELETE（明细编辑/软删除） | 需 Bearer 令牌（仅本人数据） |
| `/categories` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 需 Bearer 令牌（仅本人数据） |
| `/transactions` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 需 Bearer 令牌（仅本人数据） |
| `/budgets` | GET / POST / GET{id} / PUT{id} / DELETE{id} | 需 Bearer 令牌（仅本人数据） |
| `/summary` | GET（仪表盘概览） | 需 Bearer 令牌（仅本人数据） |

> 收支明细说明：固定收支按周期（每月/每年）自动补齐 `income_expense_details` 明细并记录金额，删除采用软删除（`is_deleted`）以避免自动补齐时复活。列表接口聚合返回 `total_amount`（总金额）与 `year_total_amount`（当年截至今天金额）。
>
> 终止时间（`end_date`）：仅对固定收支（`kind=fixed`）生效，留空表示一直持续。设置后，按期明细只生成到「今天」与「终止时间」中的**较早者**；把终止时间往前调整时，超出部分的明细会被自动清理，聚合金额随之回缩。未设置终止时间时不会清理任何未来期次（避免误删手动调整过的明细）。

> 修改金额时的明细同步：改动固定收支主记录的 `amount` 后，已展开的各期明细会同步为新金额，但**金额被单独调整过的期次保持不动**（判定依据是该期金额是否仍等于旧金额，用 0.005 容差比较浮点）。这样「整体调价」与「某月房租上涨」两种场景可以共存，总金额随之正确汇总。

## 数据隔离（多账号）
- 业务表（accounts / categories / transactions / budgets / income_expenses）均带 `owner_id`（外键 `users.id`），所有业务接口只返回、且只允许操作**当前登录用户自己**的数据。
- 列表按 `owner_id` 过滤；按 id 的单条读/改/删会校验归属，不属于自己的一律返回 **404**（刻意不区分 403 与 404，避免接口被用来越权探测他人数据是否存在）。
- 创建时由服务端强制写入 `owner_id = 当前用户`，客户端传入的 `owner_id` 会被忽略；编辑时也不允许变更归属。
- 交易、预算所引用的账户与分类必须属于自己，否则 400。
- 管理员 `admin` 同样只看得到自己的账目；「用户管理」是账号维护权限，与数据可见性无关。
- 新用户注册后自动播种一套默认分类（餐饮/交通/购物/住房/医疗/娱乐/教育/其他支出，以及工资/奖金/投资/其他收入），开箱即可记账与设置预算。
- 历史数据迁移：启用隔离时，库中已存在的历史数据统一归属到 `admin`，其余账号从零开始；迁移前会自动备份为 `finance.db.bak.<时间戳>`。

## 认证说明
- 已实现基础认证：密码使用 `pbkdf2` 哈希存储；登录/注册成功后返回 HMAC 令牌（`Authorization: Bearer <token>`）。
- 前端路由守卫 + 后端「个人信息 / 修改密码」接口强制校验令牌；收支等业务接口当前保持开放。
- 系统内置初始账号：`admin`（昵称「管理员」）与 `user1`，默认密码均为 `123456`；新账号通过 `/auth/register` 创建，管理员可在「用户管理」页维护。

## 说明
- 当前使用 SQLite，初始化时自动建表；并通过 `ensure_columns()` 为已存在的表幂等补列（`ALTER TABLE ADD COLUMN`，支持 NOT NULL DEFAULT）。
- 生产环境建议改用 PostgreSQL/MySQL 并通过 Alembic 做迁移。
