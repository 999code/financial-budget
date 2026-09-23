"""交易（收支）记录模型。"""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, comment="关联账户")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, comment="关联分类")
    type = Column(String(10), nullable=False, comment="income(收入)/expense(支出)")
    amount = Column(Float, nullable=False, comment="金额")
    note = Column(String(200), nullable=True, comment="备注")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), comment="发生时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
