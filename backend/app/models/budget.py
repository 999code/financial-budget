"""预算模型。"""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, comment="关联分类")
    amount = Column(Float, nullable=False, comment="预算金额")
    period = Column(String(10), default="monthly", comment="monthly(月度)/yearly(年度)")
    start_date = Column(DateTime(timezone=True), server_default=func.now(), comment="预算起始")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
