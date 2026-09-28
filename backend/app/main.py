"""FastAPI 应用入口。

启动方式：
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
import calendar
from datetime import date, timedelta

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas
from app.config import settings
from app.database import Base, backfill_nulls, engine, ensure_columns, get_db
import app.models  # noqa: F401  确保模型已注册到 Base.metadata
from app.api import accounts, budgets, categories, transactions, users, income_expense, loans, auth, pensions
from app.api.accounts import fill_balances
from app.api.auth import get_current_user
from app.models import Account, IncomeExpense, Transaction, User
from app.models.income_expense_detail import add_months, to_date

# 自动建表（仅初始化阶段使用，生产建议用 Alembic 迁移）
Base.metadata.create_all(bind=engine)
# SQLite 轻量迁移：为已存在的表补上后续新增的列（如 income_expenses.period）
ensure_columns(Base)
# 补列时老行会留 NULL，这里按模型默认值回填，避免读取时类型校验失败
backfill_nulls(Base)

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "docs": "/docs", "api_prefix": settings.API_V1_PREFIX}


@app.get("/api/v1/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """仪表盘概览数据（只统计当前登录用户自己的数据）。"""
    accounts = (
        db.query(Account)
        .filter(Account.owner_id == current_user.id)
        .order_by(Account.id)
        .all()
    )
    # 余额口径与账户管理页一致：期初余额 + 关联收入 − 关联支出。
    # Account.balance 是历史遗留的冗余列，可能已过期，这里统一实时算。
    fill_balances(db, accounts, current_user.id)
    total_balance = sum(float(account.balance or 0.0) for account in accounts)
    income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
        .filter(Transaction.type == "income", Transaction.owner_id == current_user.id)
        .scalar()
    )
    expense = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
        .filter(Transaction.type == "expense", Transaction.owner_id == current_user.id)
        .scalar()
    )
    account_count = len(accounts)
    return {
        "total_balance": float(total_balance),
        "total_income": float(income),
        "total_expense": float(expense),
        "account_count": account_count,
    }


def _monthly_rate(record) -> float:
    """固定收支的月度化金额：年度固定按 /12 摊到每月。"""
    amount = float(record.amount or 0.0)
    return amount / 12.0 if (record.period or "monthly") == "yearly" else amount


def _is_active_today(record, today: date) -> bool:
    """固定收支今天是否仍在生效（未开始或已终止的不计入当前运行率）。"""
    start = to_date(record.occurred_at)
    if start and start > today:
        return False
    end = to_date(record.end_date)
    return not (end and end < today)


def _depletion_date(base: date, months: float) -> date:
    """把「可支撑 x 个月」换算成具体日期（小数部分按当月天数折算）。"""
    whole = int(months)
    anchor = add_months(base, whole)
    days = calendar.monthrange(anchor.year, anchor.month)[1]
    return anchor + timedelta(days=round((months - whole) * days))


@app.get("/api/v1/summary/fund-runway", response_model=schemas.FundRunwayRead)
def fund_runway(
    months: int = Query(6, ge=0, le=60, description="统计窗口（月），临时收支在该窗口内摊销；0 = 全部历史"),
    horizon: int = Query(12, ge=1, le=60, description="消耗进度基准周期（月）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """账户资金消耗进度与耗尽预测（账户实时余额 + 收支管理的当前月度运行率）。

    消耗速度取「当前月度运行率」而非历史均值：固定收支按周期月度化（年度 /12），
    临时收支在统计窗口内摊销。这样刚新增的固定收支不会被统计窗口稀释。
    """
    accounts = (
        db.query(Account)
        .filter(Account.owner_id == current_user.id)
        .order_by(Account.id)
        .all()
    )
    # 余额口径与账户管理一致：期初余额 + 关联收入 − 关联支出
    fill_balances(db, accounts, current_user.id)
    balance = sum(float(account.balance or 0.0) for account in accounts)

    today = date.today()

    records = (
        db.query(IncomeExpense).filter(IncomeExpense.owner_id == current_user.id).all()
    )

    if months > 0:
        window_start = add_months(today, -months)
        span = months
    else:
        # 全部：从最早一条记录起算，跨度不足 1 个月时按 1 个月摊销，避免除以 0
        dates = [
            d
            for d in (to_date(r.occurred_at) or to_date(r.created_at) for r in records)
            if d
        ]
        start = min(dates) if dates else add_months(today, -1)
        span = max(1, (today.year - start.year) * 12 + today.month - start.month)
        window_start = start
        months = span  # 回显实际跨度，便于前端展示「近 N 个月」

    recurring_income = recurring_expense = 0.0
    temp_income = temp_expense = 0.0
    for record in records:
        category = record.category or "expense"
        if record.kind == "fixed":
            if not _is_active_today(record, today):
                continue
            rate = _monthly_rate(record)
            if category == "income":
                recurring_income += rate
            else:
                recurring_expense += rate
        else:
            occurred = to_date(record.occurred_at) or to_date(record.created_at)
            if not occurred or not (window_start <= occurred <= today):
                continue
            amount = float(record.amount or 0.0)
            if category == "income":
                temp_income += amount
            else:
                temp_expense += amount

    monthly_income = recurring_income + temp_income / span
    monthly_expense = recurring_expense + temp_expense / span
    monthly_net_outflow = monthly_expense - monthly_income

    base = dict(
        balance=round(balance, 2),
        account_count=len(accounts),
        window_months=months,
        horizon_months=horizon,
        monthly_income=round(monthly_income, 2),
        monthly_expense=round(monthly_expense, 2),
        monthly_net_outflow=round(monthly_net_outflow, 2),
    )

    if not accounts:
        return schemas.FundRunwayRead(**base, status="nodata", message="暂无账户数据")
    if balance <= 0:
        return schemas.FundRunwayRead(
            **base,
            runway_months=0.0,
            depletion_date=today.isoformat(),
            progress=100.0,
            status="danger",
            message="账户余额已耗尽",
        )
    if monthly_income == 0 and monthly_expense == 0:
        return schemas.FundRunwayRead(**base, status="nodata", message="暂无收支数据，无法预测")
    if monthly_net_outflow <= 0:
        return schemas.FundRunwayRead(
            **base,
            status="surplus",
            message=f"资金净流入（月均 +{abs(monthly_net_outflow):,.2f} 元），不会耗尽",
        )

    runway = balance / monthly_net_outflow
    ratio = monthly_net_outflow * horizon / balance
    progress = min(100.0, ratio * 100.0)
    status = "healthy" if progress < 50 else ("warning" if progress < 80 else "danger")
    return schemas.FundRunwayRead(
        **base,
        runway_months=round(runway, 1),
        depletion_date=_depletion_date(today, runway).isoformat(),
        consumption_ratio=round(ratio, 4),
        progress=round(progress, 1),
        status=status,
        message=f"按当前速度约 {runway:.1f} 个月后耗尽",
    )


def _month_start(d: date) -> date:
    """取某月 1 号，作为月份粒度比较的锚点。"""
    return date(d.year, d.month, 1)


def _mk(d: date) -> tuple:
    """月份序号（便于比较先后）。"""
    return (d.year, d.month)


@app.get("/api/v1/summary/absolute-outlook", response_model=schemas.AbsoluteOutlookRead)
def absolute_outlook(
    months: int = Query(12, ge=1, le=120, description="预测跨度（月），从当前月的下一月起算"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """资金消耗与耗尽预测（绝对值口径）。

    不摊销、不取均值：把收支管理里设置的真实金额按发生规则逐月累加到所选时间点，
    得到累计收入、累计支出与「支出 / 收入」比例，并从当前账户余额出发逐月模拟，
    找出余额首次转负的月份。

    - 固定收支：monthly 每月计一次全额；yearly 只在每年发生月份计一次全额；
      未到生效月或已过终止月不计入。
    - 临时收支：按发生月份一次性计入（仅计入未来区间内的）。
    """
    accounts = (
        db.query(Account)
        .filter(Account.owner_id == current_user.id)
        .order_by(Account.id)
        .all()
    )
    fill_balances(db, accounts, current_user.id)
    opening = sum(float(account.balance or 0.0) for account in accounts)

    today = date.today()
    start = _month_start(add_months(today, 1))  # 从下一月起算，当月已发生的不重复计
    month_list = [_month_start(add_months(start, i)) for i in range(months)]
    keys = [m.strftime("%Y-%m") for m in month_list]
    monthly = [
        schemas.AbsoluteOutlookMonth(month=key, income=0.0, expense=0.0, net=0.0, balance=0.0)
        for key in keys
    ]
    index = {key: i for i, key in enumerate(keys)}

    records = (
        db.query(IncomeExpense).filter(IncomeExpense.owner_id == current_user.id).all()
    )

    for record in records:
        occurred = to_date(record.occurred_at) or to_date(record.created_at)
        if not occurred:
            continue

        amount = float(record.amount or 0.0)
        field = "income" if (record.category or "expense") == "income" else "expense"

        if record.kind == "fixed":
            end = to_date(record.end_date)
            hits = []

            for m in month_list:
                if _mk(m) < _mk(occurred):  # 还没生效
                    continue
                if end and _mk(m) > _mk(end):  # 已终止
                    continue
                if (record.period or "monthly") == "yearly" and m.month != occurred.month:
                    continue  # 年度固定只在发生月份计入
                hits.append(m)

            for m in hits:
                item = monthly[index[m.strftime("%Y-%m")]]
                setattr(item, field, getattr(item, field) + amount)
        else:
            key = occurred.strftime("%Y-%m")
            if key in index:  # 临时收支只在其发生月份计入一次
                item = monthly[index[key]]
                setattr(item, field, getattr(item, field) + amount)

    running = opening
    depletion_month = None
    total_income = total_expense = 0.0

    for item in monthly:
        item.income = round(item.income, 2)
        item.expense = round(item.expense, 2)
        item.net = round(item.income - item.expense, 2)
        running += item.net
        item.balance = round(running, 2)

        total_income += item.income
        total_expense += item.expense

        if depletion_month is None and running < 0:
            depletion_month = item.month

    total_income = round(total_income, 2)
    total_expense = round(total_expense, 2)
    net_amount = round(total_income - total_expense, 2)
    projected = round(opening + net_amount, 2)
    ratio = (total_expense / total_income) if total_income > 0 else None

    net_asset = round(opening, 2)
    net_asset_ratio = (total_expense / net_asset) if net_asset > 0 else None
    net_asset_percent = None if net_asset_ratio is None else round(net_asset_ratio * 100, 1)

    base = dict(
        opening_balance=round(opening, 2),
        account_count=len(accounts),
        months=months,
        from_month=keys[0],
        target_month=keys[-1],
        total_income=total_income,
        total_expense=total_expense,
        net_amount=net_amount,
        net_asset=net_asset,
        expense_net_asset_ratio=None if net_asset_ratio is None else round(net_asset_ratio, 4),
        expense_net_asset_percent=net_asset_percent,
        projected_balance=projected,
        depletion_month=depletion_month,
        monthly=monthly,
    )

    if total_income == 0 and total_expense == 0:
        return schemas.AbsoluteOutlookRead(
            **base, status="nodata", message="所选区间内没有可预测的收支项，请先在收支管理中录入"
        )

    percent = None if ratio is None else round(ratio * 100, 1)

    if ratio is None:
        status = "danger" if depletion_month else "warning"
        message = (
            f"截至 {keys[-1]} 无收入记录，累计支出 ¥{total_expense:,.2f}"
            + (f"，预计 {depletion_month} 账户余额转负" if depletion_month else "")
        )
    elif depletion_month:
        status = "danger"
        message = (
            f"截至 {keys[-1]} 累计支出 ¥{total_expense:,.2f}，占收入 ¥{total_income:,.2f} 的 "
            f"{percent:.1f}%；预计 {depletion_month} 账户余额转负"
        )
    elif ratio >= 1:
        status = "danger"
        message = (
            f"截至 {keys[-1]} 累计支出 ¥{total_expense:,.2f} 已超过累计收入 ¥{total_income:,.2f}"
            f"（{percent:.1f}%），靠存量资金补足"
        )
    elif ratio >= 0.8:
        status = "warning"
        message = (
            f"截至 {keys[-1]} 累计支出 ¥{total_expense:,.2f}，占收入 ¥{total_income:,.2f} 的 "
            f"{percent:.1f}%，结余空间有限"
        )
    else:
        status = "healthy"
        message = (
            f"截至 {keys[-1]} 累计支出 ¥{total_expense:,.2f}，占收入 ¥{total_income:,.2f} 的 "
            f"{percent:.1f}%，累计结余 ¥{net_amount:,.2f}"
        )

    if net_asset_percent is not None:
        message += f"；相当于当前净资产 ¥{net_asset:,.2f} 的 {net_asset_percent:.1f}%"

    return schemas.AbsoluteOutlookRead(
        **base,
        expense_income_ratio=None if ratio is None else round(ratio, 4),
        expense_income_percent=percent,
        status=status,
        message=message,
    )


app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(accounts.router, prefix=settings.API_V1_PREFIX)
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(transactions.router, prefix=settings.API_V1_PREFIX)
app.include_router(budgets.router, prefix=settings.API_V1_PREFIX)
app.include_router(income_expense.router, prefix=settings.API_V1_PREFIX)
app.include_router(loans.router, prefix=settings.API_V1_PREFIX)
app.include_router(pensions.router, prefix=settings.API_V1_PREFIX)
app.include_router(pensions.persons_router, prefix=settings.API_V1_PREFIX)
app.include_router(pensions.params_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
