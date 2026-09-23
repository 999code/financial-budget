from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import Account, Category, Transaction, User

router = APIRouter(prefix="/transactions", tags=["交易记录"])


def _ensure_owned_account(db: Session, account_id: int, user_id: int) -> Account:
    """交易必须挂在自己的账户下，避免引用他人账户。"""
    account = db.get(Account, account_id)
    if account is None or account.owner_id != user_id:
        raise HTTPException(status_code=400, detail="账户不存在或不属于当前用户")
    return account


def _ensure_owned_category(db: Session, category_id: int, user_id: int) -> Category:
    """分类同理，必须是自己的。"""
    category = db.get(Category, category_id)
    if category is None or category.owner_id != user_id:
        raise HTTPException(status_code=400, detail="分类不存在或不属于当前用户")
    return category


@router.get("", response_model=list[schemas.TransactionRead])
def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """只返回当前登录用户自己的交易。"""
    return (
        db.query(Transaction)
        .filter(Transaction.owner_id == current_user.id)
        .order_by(Transaction.occurred_at.desc())
        .all()
    )


@router.post("", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(
    payload: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.type not in ("income", "expense"):
        raise HTTPException(status_code=400, detail="type 必须为 income 或 expense")
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于 0")
    _ensure_owned_account(db, payload.account_id, current_user.id)
    if payload.category_id is not None:
        _ensure_owned_category(db, payload.category_id, current_user.id)
    data = payload.model_dump()
    data["owner_id"] = current_user.id
    txn = Transaction(**data)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


@router.get("/{txn_id}", response_model=schemas.TransactionRead)
def get_transaction(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_or_404(db, Transaction, txn_id, current_user.id)


@router.put("/{txn_id}", response_model=schemas.TransactionRead)
def update_transaction(
    txn_id: int,
    payload: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    txn = get_owned_or_404(db, Transaction, txn_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    if "account_id" in updates and updates["account_id"] is not None:
        _ensure_owned_account(db, updates["account_id"], current_user.id)
    if "category_id" in updates and updates["category_id"] is not None:
        _ensure_owned_category(db, updates["category_id"], current_user.id)
    for key, value in updates.items():
        if key == "owner_id":
            continue
        setattr(txn, key, value)
    db.commit()
    db.refresh(txn)
    return txn


@router.delete("/{txn_id}", status_code=204)
def delete_transaction(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    txn = get_owned_or_404(db, Transaction, txn_id, current_user.id)
    db.delete(txn)
    db.commit()
