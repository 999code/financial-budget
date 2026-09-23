"""登录、注册、个人信息与修改密码。

说明：按约定，本模块的「个人信息 / 修改密码」需要登录令牌，
收支等业务接口仍保持开放，不强制鉴权。
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import Category, User
from app.security import create_token, decode_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["登录注册"])

bearer = HTTPBearer(auto_error=False)

# 新用户注册后自动播种的常用分类，保证其开箱即可记账与设置预算
DEFAULT_CATEGORIES = [
    ("expense", "餐饮"),
    ("expense", "交通"),
    ("expense", "购物"),
    ("expense", "住房"),
    ("expense", "医疗"),
    ("expense", "娱乐"),
    ("expense", "教育"),
    ("expense", "其他支出"),
    ("income", "工资"),
    ("income", "奖金"),
    ("income", "投资"),
    ("income", "其他收入"),
]


def seed_default_categories(db: Session, user: User) -> None:
    """给新用户播种一套默认收支分类（已存在则跳过，可安全重复调用）。"""
    for type_, name in DEFAULT_CATEGORIES:
        exists = (
            db.query(Category)
            .filter(
                Category.owner_id == user.id,
                Category.name == name,
                Category.type == type_,
            )
            .first()
        )
        if exists:
            continue
        db.add(Category(name=name, type=type_, owner_id=user.id))
    db.commit()


def get_current_user(
    credential: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    """解析 Authorization: Bearer <token>，拿到当前登录用户。"""
    if credential is None or not credential.credentials:
        raise HTTPException(status_code=401, detail="未登录或登录已失效")
    user_id = decode_token(credential.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="未登录或登录已失效")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """仅管理员（username == 'admin'）可访问，否则 403。"""
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="仅管理员可访问")
    return current_user


def get_owned_or_404(db: Session, model, obj_id: int, user_id: int):
    """取「属于自己的」记录：不存在、或不属于当前用户，一律 404。

    刻意不区分 403 与 404，避免接口被用来越权探测他人数据是否存在。
    """
    obj = db.get(model, obj_id)
    if obj is None or getattr(obj, "owner_id", None) != user_id:
        raise HTTPException(status_code=404, detail="记录不存在")
    return obj


def _ensure_username_available(db: Session, username: str, exclude_id: int | None = None):
    query = db.query(User).filter(User.username == username)
    if exclude_id is not None:
        query = query.filter(User.id != exclude_id)
    if query.first():
        raise HTTPException(status_code=400, detail="该用户名已被占用")


@router.post("/register", response_model=schemas.TokenRead, status_code=201)
def register(payload: schemas.RegisterPayload, db: Session = Depends(get_db)):
    """注册后直接返回登录令牌，省去再登录一次。"""
    username = payload.username.strip()
    _ensure_username_available(db, username)
    user = User(
        name=(payload.name or username).strip(),
        username=username,
        password_hash=hash_password(payload.password),
        phone=payload.phone,
        email=payload.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    seed_default_categories(db, user)  # 新账号自带一套常用分类，开箱即可记账
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": user}


@router.post("/login", response_model=schemas.TokenRead)
def login(payload: schemas.LoginPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username.strip()).first()
    # 用户不存在与口令错误返回同样的提示，避免暴露账号是否存在
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码不正确")
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": user}


@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserRead)
def update_me(
    payload: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password", status_code=200)
def change_password(
    payload: schemas.ChangePasswordPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="原密码不正确")
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "密码已修改"}
