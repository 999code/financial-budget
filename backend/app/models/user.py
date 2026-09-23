"""家庭成员（用户）模型。

在原有「成员姓名」基础上增加登录所需字段：
- username：登录用户名（唯一，唯一性由接口层保证，SQLite 不支持 ALTER TABLE 加唯一约束）
- password_hash：PBKDF2 口令摘要（见 app/security.py）
- phone / email：个人信息页可维护的联系方式
"""
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="成员姓名")
    username = Column(String(50), nullable=True, index=True, comment="登录用户名")
    password_hash = Column(String(255), nullable=True, comment="登录口令摘要")
    phone = Column(String(20), nullable=True, comment="手机号")
    email = Column(String(100), nullable=True, comment="邮箱")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
