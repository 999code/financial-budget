from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str
    type: str = "cash"
    balance: float = 0.0
    currency: str = "CNY"
    owner_id: Optional[int] = None


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    balance: Optional[float] = None
    currency: Optional[str] = None
    owner_id: Optional[int] = None


class AccountRead(AccountBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
