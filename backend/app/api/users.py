from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.api.auth import require_admin
from app.models import User
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["家庭成员"])


@router.get("", response_model=list[schemas.UserRead])
def list_users(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()


@router.post("", response_model=schemas.UserRead, status_code=201)
def create_user(payload: schemas.UserCreate, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """新增家庭成员；若传了 username / password，同时生成登录账号。"""
    username = None
    if payload.username:
        username = payload.username.strip()
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="该用户名已被占用")
    user = User(
        name=payload.name,
        username=username,
        password_hash=hash_password(payload.password) if payload.password else None,
        phone=payload.phone,
        email=payload.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="成员不存在")
    return user


@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, payload: schemas.UserUpdate, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """编辑成员信息；可选重置登录密码。"""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="成员不存在")

    data = payload.model_dump(exclude_unset=True)
    if "username" in data and data["username"] is not None:
        username = data["username"].strip()
        if db.query(User).filter(User.username == username, User.id != user_id).first():
            raise HTTPException(status_code=400, detail="该用户名已被占用")
        data["username"] = username
    if "password" in data and data["password"]:
        data["password_hash"] = hash_password(data.pop("password"))

    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, _admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="成员不存在")
    db.delete(user)
    db.commit()
