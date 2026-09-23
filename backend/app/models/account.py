"""账户模型：现金 / 银行卡 / 信用卡 / 投资账户等。"""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="账户名称")
    type = Column(String(20), default="cash", comment="cash/bank/creditcard/investment")
    balance = Column(Float, default=0.0, comment="当前余额")
    currency = Column(String(10), default="CNY", comment="币种")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
