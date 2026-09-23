from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import Category, User

router = APIRouter(prefix="/categories", tags=["分类"])


@router.get("", response_model=list[schemas.CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """只返回当前登录用户自己的分类。"""
    return (
        db.query(Category)
        .filter(Category.owner_id == current_user.id)
        .order_by(Category.type, Category.id)
        .all()
    )


@router.post("", response_model=schemas.CategoryRead, status_code=201)
def create_category(
    payload: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.type not in ("income", "expense"):
        raise HTTPException(status_code=400, detail="type 必须为 income 或 expense")
    data = payload.model_dump()
    data["owner_id"] = current_user.id
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_or_404(db, Category, category_id, current_user.id)


@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    payload: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_owned_or_404(db, Category, category_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "owner_id":
            continue
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_owned_or_404(db, Category, category_id, current_user.id)
    db.delete(category)
    db.commit()
