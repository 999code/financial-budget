"""贷款模型：房贷 / 车贷等，支持等额本息与等额本金两种还款方式。"""
import calendar
from datetime import date
from typing import Optional, Tuple

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base

EQUAL_INSTALLMENT = "equal_installment"  # 等额本息：每月还款额固定
EQUAL_PRINCIPAL = "equal_principal"  # 等额本金：每月本金固定，利息递减
VALID_METHODS = (EQUAL_INSTALLMENT, EQUAL_PRINCIPAL)


def add_months(d: date, months: int) -> date:
    """按月加减日期，自动处理月末（如 1/31 加 1 个月 → 2/28）。"""
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def total_months(years: Optional[float]) -> int:
    """贷款年限（年）换算成期数（月）。"""
    return int(round(float(years or 0) * 12))


def calc_monthly_payments(
    loan_amount: Optional[float],
    annual_rate: Optional[float],
    years: Optional[float],
    method: str = EQUAL_INSTALLMENT,
) -> Tuple[float, float]:
    """计算月供，返回 (首月月供, 末月月供)。

    等额本息：每月还款额相同，首月 == 末月。
    等额本金：每月归还本金相同、利息递减，首月最高、末月最低。
    """
    months = total_months(years)
    amount = float(loan_amount or 0)
    if months <= 0 or amount <= 0:
        return 0.0, 0.0

    monthly_rate = float(annual_rate or 0) / 100.0 / 12.0
    if monthly_rate <= 0:  # 免息：直接按本金摊到每期
        per = amount / months
        return per, per

    if method == EQUAL_PRINCIPAL:
        per_principal = amount / months
        first = per_principal + amount * monthly_rate
        last = per_principal + (amount - per_principal * (months - 1)) * monthly_rate
        return first, max(last, 0.0)

    factor = (1 + monthly_rate) ** months
    monthly = amount * monthly_rate * factor / (factor - 1)
    return monthly, monthly


def due_date(start: Optional[date], years: Optional[float]) -> Optional[date]:
    """最后一期还款日 = 起始日 + (期数 - 1) 个月。"""
    if not start:
        return None
    months = total_months(years)
    if months <= 0:
        return start
    return add_months(start, months - 1)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="贷款名称")
    total_price = Column(Float, default=0.0, comment="总价")
    principal = Column(Float, default=0.0, comment="本金（首付款）")
    loan_amount = Column(Float, default=0.0, comment="贷款金额（= 总价 - 本金）")
    annual_rate = Column(Float, default=0.0, comment="年利率(%)")
    years = Column(Float, default=0.0, comment="贷款年限（年）")
    repayment_method = Column(String(20), default=EQUAL_INSTALLMENT, comment="equal_installment/equal_principal")
    start_date = Column(Date, nullable=True, comment="贷款起始（首次还款）日期")
    note = Column(String(200), nullable=True, comment="备注")
    income_expense_id = Column(
        Integer, ForeignKey("income_expenses.id"), nullable=True, comment="联动的固定收支（月供）"
    )
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
