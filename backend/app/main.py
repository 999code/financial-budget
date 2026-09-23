"""FastAPI 应用入口。

启动方式：
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, ensure_columns, get_db
import app.models  # noqa: F401  确保模型已注册到 Base.metadata
from app.api import accounts, budgets, categories, transactions, users, income_expense, loans, auth
from app.api.auth import get_current_user
from app.models import Account, Transaction, User

# 自动建表（仅初始化阶段使用，生产建议用 Alembic 迁移）
Base.metadata.create_all(bind=engine)
# SQLite 轻量迁移：为已存在的表补上后续新增的列（如 income_expenses.period）
ensure_columns(Base)

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
    total_balance = (
        db.query(func.coalesce(func.sum(Account.balance), 0.0))
        .filter(Account.owner_id == current_user.id)
        .scalar()
    )
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
    account_count = (
        db.query(func.count(Account.id))
        .filter(Account.owner_id == current_user.id)
        .scalar()
    )
    return {
        "total_balance": float(total_balance),
        "total_income": float(income),
        "total_expense": float(expense),
        "account_count": account_count,
    }


app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(accounts.router, prefix=settings.API_V1_PREFIX)
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(transactions.router, prefix=settings.API_V1_PREFIX)
app.include_router(budgets.router, prefix=settings.API_V1_PREFIX)
app.include_router(income_expense.router, prefix=settings.API_V1_PREFIX)
app.include_router(loans.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
