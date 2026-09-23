"""收支分类模型。"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="分类名称")
    type = Column(String(10), nullable=False, comment="income(收入)/expense(支出)")
    icon = Column(String(50), nullable=True, comment="图标")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
