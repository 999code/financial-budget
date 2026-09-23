"""收支（固定/临时）记录模型。

与 transactions 的区别：本表用于「收支管理」页面，记录项只关心
名称 / 金额 / 时间，并按 kind（fixed=固定收支, temp=临时收支）归类，
不强制关联账户与分类，适合家庭日常的固定开销与一次性的临时收支。
"""
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class IncomeExpense(Base):
    __tablename__ = "income_expenses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="收支名称")
    amount = Column(Float, nullable=False, comment="金额")
    kind = Column(String(10), nullable=False, comment="fixed(固定收支)/temp(临时收支)")
    category = Column(
        String(10),
        nullable=False,
        server_default="expense",
        comment="income(收入)/expense(支出)",
    )
    period = Column(String(10), nullable=True, comment="monthly(每月)/yearly(每年)，仅 fixed 生效")
    end_date = Column(Date, nullable=True, comment="终止时间（仅 fixed 生效，留空表示不终止）")
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), comment="发生时间")
    note = Column(String(200), nullable=True, comment="备注")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
