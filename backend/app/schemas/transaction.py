from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionBase(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    type: str  # income / expense
    amount: float
    note: Optional[str] = None
    occurred_at: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    type: Optional[str] = None
    amount: Optional[float] = None
    note: Optional[str] = None
    occurred_at: Optional[datetime] = None


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
