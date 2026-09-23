from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class IncomeExpenseBase(BaseModel):
    name: str
    amount: float
    kind: str  # fixed / temp
    category: str = "expense"  # income(收入) / expense(支出)
    period: Optional[str] = None  # monthly(每月) / yearly(每年)，仅固定收支使用
    end_date: Optional[date] = None  # 终止时间（仅 fixed 生效，留空表示不终止）
    occurred_at: Optional[datetime] = None
    note: Optional[str] = None


class IncomeExpenseCreate(IncomeExpenseBase):
    pass


class IncomeExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    kind: Optional[str] = None
    category: Optional[str] = None
    period: Optional[str] = None
    end_date: Optional[date] = None
    occurred_at: Optional[datetime] = None
    note: Optional[str] = None


class IncomeExpenseRead(IncomeExpenseBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class IncomeExpenseWithTotalRead(IncomeExpenseRead):
    """列表用：附带明细合计金额（临时收支恒为 0）。"""

    total_amount: float = 0.0  # 全部明细合计
    year_total_amount: float = 0.0  # 今年（1/1 至今天）明细合计


# ---- 固定收支的按期明细 ----
class IncomeExpenseDetailBase(BaseModel):
    record_id: int
    period_date: date
    amount: float
    note: Optional[str] = None


class IncomeExpenseDetailRead(IncomeExpenseDetailBase):
    id: int
    is_deleted: bool = False

    model_config = {"from_attributes": True}


class IncomeExpenseDetailUpdate(BaseModel):
    period_date: Optional[date] = None
    amount: Optional[float] = None
    note: Optional[str] = None
