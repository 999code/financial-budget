from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import Account, User

router = APIRouter(prefix="/accounts", tags=["账户"])


@router.get("", response_model=list[schemas.AccountRead])
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """只返回当前登录用户自己的账户。"""
    return (
        db.query(Account)
        .filter(Account.owner_id == current_user.id)
        .order_by(Account.id)
        .all()
    )


@router.post("", response_model=schemas.AccountRead, status_code=201)
def create_account(
    payload: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump()
    data["owner_id"] = current_user.id  # 强制归属当前用户，忽略客户端传值
    account = Account(**data)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=schemas.AccountRead)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_or_404(db, Account, account_id, current_user.id)


@router.put("/{account_id}", response_model=schemas.AccountRead)
def update_account(
    account_id: int,
    payload: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "owner_id":  # 不允许通过编辑把数据转移给别人
            continue
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    db.delete(account)
    db.commit()
