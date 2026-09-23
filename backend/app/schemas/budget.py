from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BudgetBase(BaseModel):
    category_id: int
    amount: float
    period: str = "monthly"
    start_date: Optional[datetime] = None


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    period: Optional[str] = None
    start_date: Optional[datetime] = None


class BudgetRead(BudgetBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
