from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class LoanBase(BaseModel):
    name: str
    total_price: float = 0.0
    principal: float = 0.0  # 本金（首付款）
    annual_rate: float = 0.0  # 年利率(%)
    years: float = 0.0  # 贷款年限（年）
    repayment_method: str = "equal_installment"  # equal_installment / equal_principal
    start_date: Optional[date] = None
    note: Optional[str] = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    name: Optional[str] = None
    total_price: Optional[float] = None
    principal: Optional[float] = None
    annual_rate: Optional[float] = None
    years: Optional[float] = None
    repayment_method: Optional[str] = None
    start_date: Optional[date] = None
    note: Optional[str] = None


class LoanRead(LoanBase):
    id: int
    loan_amount: float = 0.0  # 贷款金额 = 总价 - 本金（服务端计算，只读）
    monthly_payment: float = 0.0  # 首月月供（等额本息即每期固定值）
    last_month_payment: float = 0.0  # 末月月供（等额本金低于首月）
    end_date: Optional[date] = None  # 最后一期还款日
    created_at: datetime

    model_config = {"from_attributes": True}
