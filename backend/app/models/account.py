"""账户模型：现金 / 银行卡 / 信用卡 / 投资账户等。

余额说明：账户余额不再手工维护，而是「期初余额 + 关联收支（收入 − 支出）」算出来的，
由 app.api.accounts 在读取时聚合填充到 balance 字段；initial_balance 才是唯一需要录入的值。
"""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="账户名称")
    card_number = Column(String(50), nullable=False, default="", comment="卡号（必填，同一用户下不重复）")
    type = Column(String(20), default="cash", comment="cash/bank/creditcard/investment")
    initial_balance = Column(Float, default=0.0, comment="期初余额（建账时的本金）")
    balance = Column(Float, default=0.0, comment="当前余额（期初 + 收入 − 支出，读取时计算回填）")
    currency = Column(String(10), default="CNY", comment="币种")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
