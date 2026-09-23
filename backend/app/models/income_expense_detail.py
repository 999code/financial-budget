"""固定收支的按期明细。

一条固定收支（kind=fixed）按周期（每月/每年）从创建时间自动展开成多条明细，
每条记录该期的日期与金额。明细支持改金额与删除：

- 删除走软删除（is_deleted），因为展开逻辑是「补齐缺失的期」，
  若物理删除，下一次打开详情时该期又会被自动重建，删除就白做了。
"""
import calendar
from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class IncomeExpenseDetail(Base):
    __tablename__ = "income_expense_details"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(
        Integer,
        ForeignKey("income_expenses.id"),
        nullable=False,
        index=True,
        comment="所属收支记录",
    )
    period_date = Column(Date, nullable=False, comment="该期的日期")
    amount = Column(Float, nullable=False, comment="该期金额")
    note = Column(String(200), nullable=True, comment="备注")
    is_deleted = Column(Boolean, nullable=False, default=False, comment="软删除，删除后不再自动重建")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


def add_months(source: date, months: int) -> date:
    """按月加减，日超出当月天数时取当月最后一天（如 1/31 + 1 月 = 2/28）。"""
    total = source.year * 12 + (source.month - 1) + months
    year, month = divmod(total, 12)
    month += 1
    day = min(source.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def period_dates(start: date, period: str, until: date) -> list[date]:
    """从 start 起按周期列出所有不晚于 until 的期次日期（含 start 当期）。"""
    dates = []
    index = 0
    while True:
        current = add_months(start, index * 12) if period == "yearly" else add_months(start, index)
        if current > until:
            break
        dates.append(current)
        index += 1
        if index > 1000:  # 防御：避免异常数据导致死循环
            break
    return dates


def to_date(value) -> date | None:
    """兼容 datetime / date / 'YYYY-MM-DD' 字符串。"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None
