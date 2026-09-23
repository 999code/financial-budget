"""贷款管理：贷款记录的增删改查，并把月供自动同步成一条固定支出。"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import IncomeExpense, IncomeExpenseDetail, Loan, User
from app.models.loan import (
    EQUAL_INSTALLMENT,
    EQUAL_PRINCIPAL,
    VALID_METHODS,
    calc_monthly_payments,
    due_date,
)
from app.api.income_expense import ensure_details, sync_detail_amounts

router = APIRouter(prefix="/loans", tags=["贷款管理"])


def _validate(data: dict) -> None:
    """校验贷款字段的取值。"""
    if data.get("repayment_method") not in VALID_METHODS:
        raise HTTPException(status_code=400, detail="还款方式必须为 equal_installment 或 equal_principal")
    if (data.get("loan_amount") or 0) <= 0:
        raise HTTPException(status_code=400, detail="贷款金额必须大于 0")
    if (data.get("years") or 0) <= 0:
        raise HTTPException(status_code=400, detail="贷款年限必须大于 0")
    if (data.get("annual_rate") or 0) < 0:
        raise HTTPException(status_code=400, detail="年利率不能为负数")
    if (data.get("total_price") or 0) < 0 or (data.get("principal") or 0) < 0:
        raise HTTPException(status_code=400, detail="总价与本金不能为负数")


def _to_read(loan: Loan) -> schemas.LoanRead:
    """ORM 对象转响应模型，补上计算得出的月供与到期日。"""
    first, last = calc_monthly_payments(
        loan.loan_amount, loan.annual_rate, loan.years, loan.repayment_method
    )
    data = schemas.LoanRead.model_validate(loan, from_attributes=True)
    data.monthly_payment = round(first, 2)
    data.last_month_payment = round(last, 2)
    data.end_date = due_date(loan.start_date, loan.years)
    return data


def _sync_income_expense(db: Session, loan: Loan, user_id: int) -> None:
    """把月供同步成一条固定支出（kind=fixed, period=monthly）。

    - 尚未关联则新建一条「贷款名-月供」的固定支出；
    - 已关联则更新名称/金额/起止时间，金额变化时同步已展开的明细；
    - 终止时间 = 最后一期还款日，明细不会超出贷款期限。
    """
    first, last = calc_monthly_payments(
        loan.loan_amount, loan.annual_rate, loan.years, loan.repayment_method
    )
    amount = round(first, 2)
    started = (
        datetime.combine(loan.start_date, datetime.min.time())
        if loan.start_date
        else datetime.now()
    )
    end = due_date(loan.start_date, loan.years)

    record = db.get(IncomeExpense, loan.income_expense_id) if loan.income_expense_id else None
    if record is not None and record.owner_id != user_id:
        record = None  # 归属异常时不复用，改为新建

    if loan.repayment_method == EQUAL_PRINCIPAL:
        note = f"贷款「{loan.name}」月供（等额本金：首月 {amount:.2f}，末月 {round(last, 2):.2f}，逐月递减）"
    else:
        note = f"贷款「{loan.name}」月供（等额本息：每月固定 {amount:.2f}）"

    if record is None:
        record = IncomeExpense(
            name=f"{loan.name}-月供",
            amount=amount,
            kind="fixed",
            category="expense",
            period="monthly",
            occurred_at=started,
            end_date=end,
            note=note,
            owner_id=user_id,
        )
        db.add(record)
        db.flush()  # 取到 id 回写到贷款
        loan.income_expense_id = record.id
        db.commit()
        db.refresh(loan)
        ensure_details(record, db)
        return

    old_amount = record.amount
    record.name = f"{loan.name}-月供"
    record.amount = amount
    record.occurred_at = started
    record.end_date = end
    record.note = note
    record.kind = "fixed"
    record.category = "expense"
    record.period = "monthly"
    db.commit()
    db.refresh(record)
    sync_detail_amounts(db, record, old_amount)  # 只同步未被手动调整的期次
    ensure_details(record, db)


@router.get("", response_model=list[schemas.LoanRead])
def list_loans(
    name: Optional[str] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD，贷款起始时间下限"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD，贷款起始时间上限"),
    repayment_method: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """贷款列表，支持按名称、贷款金额范围、起始时间范围筛选（仅当前用户的数据）。"""
    q = db.query(Loan).filter(Loan.owner_id == current_user.id)
    if name:
        q = q.filter(Loan.name.ilike(f"%{name}%"))
    if amount_min is not None:
        q = q.filter(Loan.loan_amount >= amount_min)
    if amount_max is not None:
        q = q.filter(Loan.loan_amount <= amount_max)
    if start_date:
        q = q.filter(Loan.start_date >= start_date)
    if end_date:
        q = q.filter(Loan.start_date <= end_date)
    if repayment_method:
        q = q.filter(Loan.repayment_method == repayment_method)
    rows = q.order_by(Loan.start_date.desc(), Loan.id.desc()).all()
    return [_to_read(row) for row in rows]


@router.post("", response_model=schemas.LoanRead, status_code=201)
def create_loan(
    payload: schemas.LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump()
    _validate(data)
    data["owner_id"] = current_user.id  # 强制归属当前用户，忽略客户端传值
    loan = Loan(**data)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    _sync_income_expense(db, loan, current_user.id)
    return _to_read(loan)


@router.get("/{loan_id}", response_model=schemas.LoanRead)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _to_read(get_owned_or_404(db, Loan, loan_id, current_user.id))


@router.put("/{loan_id}", response_model=schemas.LoanRead)
def update_loan(
    loan_id: int,
    payload: schemas.LoanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loan = get_owned_or_404(db, Loan, loan_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    merged = {
        "loan_amount": loan.loan_amount,
        "years": loan.years,
        "annual_rate": loan.annual_rate,
        "total_price": loan.total_price,
        "principal": loan.principal,
        "repayment_method": loan.repayment_method,
    }
    merged.update({k: v for k, v in updates.items() if k in merged})
    _validate(merged)
    for key, value in updates.items():
        if key == "owner_id":  # 不允许通过编辑把数据转移给别人
            continue
        setattr(loan, key, value)
    db.commit()
    db.refresh(loan)
    _sync_income_expense(db, loan, current_user.id)
    return _to_read(loan)


@router.delete("/{loan_id}", status_code=204)
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除贷款，同时清理由它生成的月供固定收支（含其按期明细）。"""
    loan = get_owned_or_404(db, Loan, loan_id, current_user.id)
    if loan.income_expense_id:
        record = db.get(IncomeExpense, loan.income_expense_id)
        if record is not None and record.owner_id == current_user.id:
            # SQLite 未开启外键级联，明细需手动清理
            db.query(IncomeExpenseDetail).filter(
                IncomeExpenseDetail.record_id == record.id
            ).delete()
            db.delete(record)
    db.delete(loan)
    db.commit()
