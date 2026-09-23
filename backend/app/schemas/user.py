from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class UserRead(UserBase):
    id: int
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """管理员编辑成员信息；所有字段均可选，仅传需要修改的字段。"""
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    phone: Optional[str] = None
    email: Optional[str] = None


# ---- 登录 / 注册 ----
class RegisterPayload(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class LoginPayload(BaseModel):
    username: str
    password: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class ChangePasswordPayload(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=128)
