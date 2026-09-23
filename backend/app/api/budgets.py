from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import Budget, Category, User

router = APIRouter(prefix="/budgets", tags=["预算"])


def _ensure_owned_category(db: Session, category_id: int, user_id: int) -> Category:
    """预算必须挂在自己的分类下。"""
    category = db.get(Category, category_id)
    if category is None or category.owner_id != user_id:
        raise HTTPException(status_code=400, detail="分类不存在或不属于当前用户")
    return category


@router.get("", response_model=list[schemas.BudgetRead])
def list_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """只返回当前登录用户自己的预算。"""
    return (
        db.query(Budget)
        .filter(Budget.owner_id == current_user.id)
        .order_by(Budget.id)
        .all()
    )


@router.post("", response_model=schemas.BudgetRead, status_code=201)
def create_budget(
    payload: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="预算金额必须大于 0")
    _ensure_owned_category(db, payload.category_id, current_user.id)
    data = payload.model_dump()
    data["owner_id"] = current_user.id
    budget = Budget(**data)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/{budget_id}", response_model=schemas.BudgetRead)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_or_404(db, Budget, budget_id, current_user.id)


@router.put("/{budget_id}", response_model=schemas.BudgetRead)
def update_budget(
    budget_id: int,
    payload: schemas.BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = get_owned_or_404(db, Budget, budget_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    if "category_id" in updates and updates["category_id"] is not None:
        _ensure_owned_category(db, updates["category_id"], current_user.id)
    for key, value in updates.items():
        if key == "owner_id":
            continue
        setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = get_owned_or_404(db, Budget, budget_id, current_user.id)
    db.delete(budget)
    db.commit()
