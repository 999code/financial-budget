from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

CARD_NUMBER_MAX_LENGTH = 50


def normalize_card_number(value):
    """卡号去空白后必须非空（必填）；None 表示「本次不修改」。"""
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        raise ValueError("卡号不能为空")
    if len(value) > CARD_NUMBER_MAX_LENGTH:
        raise ValueError(f"卡号长度不能超过 {CARD_NUMBER_MAX_LENGTH} 个字符")
    return value


class AccountBase(BaseModel):
    name: str
    card_number: str  # 卡号：必填，同一用户下不重复
    type: str = "cash"
    initial_balance: float = 0.0  # 期初余额：唯一需要录入的金额
    currency: str = "CNY"
    owner_id: Optional[int] = None

    @field_validator("card_number")
    @classmethod
    def _normalize_card(cls, v):
        return normalize_card_number(v)


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    card_number: Optional[str] = None
    type: Optional[str] = None
    initial_balance: Optional[float] = None  # 余额由收支汇总算出，不接受直接改 balance
    currency: Optional[str] = None
    owner_id: Optional[int] = None

    @field_validator("card_number")
    @classmethod
    def _normalize_card(cls, v):
        return normalize_card_number(v)


class AccountRead(AccountBase):
    """读取账户：balance 是「期初 + 收入 − 支出」算出来的，不是存储值。"""

    id: int
    balance: float = 0.0
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- 账户关联的收支流水 ----
class AccountIncomeExpenseItem(BaseModel):
    """账户流水：临时收支一条；固定收支按已展开的期次每条一条。"""

    id: str  # temp-<记录id> / fixed-<明细id>，前端展开列表用
    record_id: int
    detail_id: Optional[int] = None
    name: str
    kind: str  # fixed / temp
    category: str  # income(收入) / expense(支出)
    amount: float  # 原始金额（正数）
    signed_amount: float  # 收入为正、支出为负
    date: str  # YYYY-MM-DD
    period: Optional[str] = None  # 固定收支的周期


class AccountIncomeExpenseSummary(BaseModel):
    """账户流水汇总，用于解释余额是怎么来的。"""

    account_id: int
    initial_balance: float = 0.0
    income_total: float = 0.0
    expense_total: float = 0.0
    net_total: float = 0.0  # 收入 − 支出
    balance: float = 0.0  # 期初 + 净额
    items: list[AccountIncomeExpenseItem] = []
