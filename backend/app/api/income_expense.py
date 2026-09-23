from datetime import date

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import IncomeExpense, IncomeExpenseDetail, User
from app.models.income_expense_detail import period_dates, to_date

router = APIRouter(prefix="/income-expense", tags=["收支管理"])


VALID_PERIODS = ("monthly", "yearly")  # monthly=每月 / yearly=每年
VALID_CATEGORIES = ("income", "expense")  # income=收入 / expense=支出


def _normalize_category(category: Optional[str]) -> str:
    """收支分类：收入 / 支出，缺省按支出。"""
    if not category:
        return "expense"
    if category not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail="分类必须为 income(收入) 或 expense(支出)")
    return category


def _normalize_period(kind: str, period: Optional[str]) -> Optional[str]:
    """固定收支需要有周期（默认每月），临时收支不带周期。"""
    if kind != "fixed":
        return None
    if not period:
        return "monthly"
    if period not in VALID_PERIODS:
        raise HTTPException(status_code=400, detail="周期必须为 monthly(每月) 或 yearly(每年)")
    return period


def _get_owned_detail(db: Session, detail_id: int, user_id: int) -> IncomeExpenseDetail:
    """明细本身没有 owner_id，需经它所属的收支记录判断归属。"""
    detail = db.get(IncomeExpenseDetail, detail_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="明细不存在")
    record = db.get(IncomeExpense, detail.record_id)
    if record is None or record.owner_id != user_id:
        raise HTTPException(status_code=404, detail="明细不存在")
    return detail


def ensure_details(record: IncomeExpense, db: Session) -> None:
    """按周期把固定收支从创建时间展开到「今天或终止时间（取较早者）」，缺失的期自动补一条。

    幂等：只补「还没有对应期次」的记录；被软删除的期也会占位，不会被重新生成。
    若设置了终止时间，超出终止时间的明细（含用户手动改到未来的期次）会被移除。
    """
    if record.kind != "fixed":
        return
    start = to_date(record.occurred_at)
    if start is None:
        return
    end_date = to_date(record.end_date)
    today = date.today()
    # 生成截止点：未设终止时间则到今天；设了则取「今天」与「终止时间」的较早者
    until = min(today, end_date) if end_date else today

    existed = {
        row[0]
        for row in db.query(IncomeExpenseDetail.period_date).filter(
            IncomeExpenseDetail.record_id == record.id
        )
    }
    created = False
    for period_date in period_dates(start, record.period or "monthly", until):
        if period_date in existed:
            continue
        db.add(
            IncomeExpenseDetail(
                record_id=record.id,
                period_date=period_date,
                amount=record.amount,
            )
        )
        created = True

    # 仅当设置了终止时间时，清理超出终止时间的明细（终止之后不再产生任何期次）
    if end_date:
        db.query(IncomeExpenseDetail).filter(
            IncomeExpenseDetail.record_id == record.id,
            IncomeExpenseDetail.period_date > end_date,
        ).delete()

    if created or end_date:
        db.commit()


@router.get("", response_model=list[schemas.IncomeExpenseWithTotalRead])
def list_items(
    kind: Optional[str] = Query(None, description="fixed(固定收支)/temp(临时收支)"),
    name: Optional[str] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    period: Optional[str] = Query(None, description="monthly(每月)/yearly(每年)，仅固定收支"),
    category: Optional[str] = Query(None, description="income(收入)/expense(支出)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """收支列表，支持按 kind、分类、名称、金额范围、时间范围筛选（仅当前用户的数据）。"""
    q = db.query(IncomeExpense).filter(IncomeExpense.owner_id == current_user.id)
    if kind:
        q = q.filter(IncomeExpense.kind == kind)
    if category:
        q = q.filter(IncomeExpense.category == category)
    if period:
        q = q.filter(IncomeExpense.period == period)
    if name:
        q = q.filter(IncomeExpense.name.ilike(f"%{name}%"))
    if amount_min is not None:
        q = q.filter(IncomeExpense.amount >= amount_min)
    if amount_max is not None:
        q = q.filter(IncomeExpense.amount <= amount_max)
    if start_date:
        q = q.filter(func.date(IncomeExpense.occurred_at) >= start_date)
    if end_date:
        q = q.filter(func.date(IncomeExpense.occurred_at) <= end_date)
    rows = q.order_by(IncomeExpense.occurred_at.desc()).all()

    # 固定收支：先按周期补齐明细，再分别求「总金额」与「今年总金额」
    today = date.today()
    year_start = date(today.year, 1, 1)
    fixed_ids = [row.id for row in rows if row.kind == "fixed"]
    if fixed_ids:
        for record_id in fixed_ids:
            record = db.get(IncomeExpense, record_id)
            if record:
                ensure_details(record, db)
        sums = dict(
            db.query(
                IncomeExpenseDetail.record_id,
                func.coalesce(func.sum(IncomeExpenseDetail.amount), 0.0),
            )
            .filter(
                IncomeExpenseDetail.record_id.in_(fixed_ids),
                IncomeExpenseDetail.is_deleted.is_(False),
            )
            .group_by(IncomeExpenseDetail.record_id)
            .all()
        )
        # 今年：只统计 period_date 落在 1/1 ~ 今天 之间的期次（明细日期可被手改成未来，需过滤）
        year_sums = dict(
            db.query(
                IncomeExpenseDetail.record_id,
                func.coalesce(func.sum(IncomeExpenseDetail.amount), 0.0),
            )
            .filter(
                IncomeExpenseDetail.record_id.in_(fixed_ids),
                IncomeExpenseDetail.is_deleted.is_(False),
                IncomeExpenseDetail.period_date >= year_start,
                IncomeExpenseDetail.period_date <= today,
            )
            .group_by(IncomeExpenseDetail.record_id)
            .all()
        )
    else:
        sums = {}
        year_sums = {}
    for row in rows:
        row.total_amount = float(sums.get(row.id, 0.0) or 0.0)
        row.year_total_amount = float(year_sums.get(row.id, 0.0) or 0.0)
    return rows


@router.post("", response_model=schemas.IncomeExpenseRead, status_code=201)
def create_item(
    payload: schemas.IncomeExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.kind not in ("fixed", "temp"):
        raise HTTPException(status_code=400, detail="kind 必须为 fixed 或 temp")
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于 0")
    data = payload.model_dump()
    data["category"] = _normalize_category(data.get("category"))
    data["period"] = _normalize_period(data.get("kind"), data.get("period"))
    data["owner_id"] = current_user.id
    item = IncomeExpense(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    ensure_details(item, db)  # 固定收支入库即按周期展开明细
    return item


def sync_detail_amounts(db: Session, record: IncomeExpense, old_amount: Optional[float]) -> None:
    """金额变化后同步已展开的期次。

    只改「金额仍等于旧值」的期次；用户单独调过金额的期次（如某月房租上涨）保持不动。
    用容差比较避免浮点误差导致漏同步。
    """
    if old_amount is None or record.amount == old_amount:
        return
    db.query(IncomeExpenseDetail).filter(
        IncomeExpenseDetail.record_id == record.id,
        IncomeExpenseDetail.is_deleted.is_(False),
        func.abs(IncomeExpenseDetail.amount - old_amount) < 0.005,
    ).update(
        {IncomeExpenseDetail.amount: record.amount},
        synchronize_session=False,
    )
    db.commit()


@router.get("/{item_id}", response_model=schemas.IncomeExpenseRead)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_or_404(db, IncomeExpense, item_id, current_user.id)


@router.put("/{item_id}", response_model=schemas.IncomeExpenseRead)
def update_item(
    item_id: int,
    payload: schemas.IncomeExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = get_owned_or_404(db, IncomeExpense, item_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    if "category" in updates:
        updates["category"] = _normalize_category(updates.get("category"))
    if "kind" in updates or "period" in updates:
        updates["period"] = _normalize_period(
            updates.get("kind", item.kind),
            updates.get("period", item.period),
        )
    old_amount = item.amount
    for key, value in updates.items():
        if key == "owner_id":
            continue
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    sync_detail_amounts(db, item, old_amount)
    ensure_details(item, db)  # 改了金额/周期/时间后补齐新产生的期次
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = get_owned_or_404(db, IncomeExpense, item_id, current_user.id)
    # SQLite 未开启外键级联，明细需手动清理
    db.query(IncomeExpenseDetail).filter(IncomeExpenseDetail.record_id == item_id).delete()
    db.delete(item)
    db.commit()


# ---- 固定收支的按期明细 ----
@router.get(
    "/{item_id}/details",
    response_model=list[schemas.IncomeExpenseDetailRead],
    summary="收支明细（固定收支按周期自动展开）",
)
def list_details(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_owned_or_404(db, IncomeExpense, item_id, current_user.id)
    ensure_details(record, db)
    return (
        db.query(IncomeExpenseDetail)
        .filter(
            IncomeExpenseDetail.record_id == item_id,
            IncomeExpenseDetail.is_deleted.is_(False),
        )
        .order_by(IncomeExpenseDetail.period_date)
        .all()
    )


@router.put("/details/{detail_id}", response_model=schemas.IncomeExpenseDetailRead)
def update_detail(
    detail_id: int,
    payload: schemas.IncomeExpenseDetailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = _get_owned_detail(db, detail_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    if "amount" in updates and updates["amount"] is None:
        raise HTTPException(status_code=400, detail="金额不能为空")
    for key, value in updates.items():
        setattr(detail, key, value)
    db.commit()
    db.refresh(detail)
    return detail


@router.delete("/details/{detail_id}", status_code=204)
def delete_detail(
    detail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """软删除：删掉后不会再被自动展开重建。"""
    detail = _get_owned_detail(db, detail_id, current_user.id)
    detail.is_deleted = True
    db.commit()
