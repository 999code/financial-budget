from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth import get_current_user, get_owned_or_404
from app import schemas
from app.models import Account, IncomeExpense, IncomeExpenseDetail, User
from app.api.income_expense import ensure_details

router = APIRouter(prefix="/accounts", tags=["账户"])


def _as_float(value) -> float:
    """新增列前历史行的 initial_balance 可能为 NULL，统一按 0 处理。"""
    return float(value or 0.0)


def build_account_items(db: Session, account_id: int, user_id: int) -> list[schemas.AccountIncomeExpenseItem]:
    """汇总某个账户下的全部收支流水。

    - 临时收支：整条记录算一笔，日期取发生时间；
    - 固定收支：按已展开的期次逐条算（未到期的不算），日期取该期日期。
    """
    records = (
        db.query(IncomeExpense)
        .filter(
            IncomeExpense.owner_id == user_id,
            IncomeExpense.account_id == account_id,
        )
        .all()
    )
    items: list[schemas.AccountIncomeExpenseItem] = []
    for record in records:
        category = record.category or "expense"
        sign = 1.0 if category == "income" else -1.0
        if record.kind == "fixed":
            ensure_details(record, db)  # 先把该补的期次补齐，避免漏算
            details = (
                db.query(IncomeExpenseDetail)
                .filter(
                    IncomeExpenseDetail.record_id == record.id,
                    IncomeExpenseDetail.is_deleted.is_(False),
                )
                .order_by(IncomeExpenseDetail.period_date)
                .all()
            )
            for detail in details:
                amount = float(detail.amount or 0.0)
                items.append(
                    schemas.AccountIncomeExpenseItem(
                        id=f"fixed-{detail.id}",
                        record_id=record.id,
                        detail_id=detail.id,
                        name=record.name,
                        kind="fixed",
                        category=category,
                        amount=amount,
                        signed_amount=sign * amount,
                        date=detail.period_date.isoformat() if detail.period_date else "",
                        period=record.period,
                    )
                )
        else:
            amount = float(record.amount or 0.0)
            occurred = record.occurred_at or record.created_at
            items.append(
                schemas.AccountIncomeExpenseItem(
                    id=f"temp-{record.id}",
                    record_id=record.id,
                    name=record.name,
                    kind="temp",
                    category=category,
                    amount=amount,
                    signed_amount=sign * amount,
                    date=occurred.date().isoformat() if occurred else "",
                )
            )
    items.sort(key=lambda item: item.date)
    return items


def compute_balance(db: Session, account: Account, user_id: int) -> tuple[float, float, float]:
    """返回 (余额, 收入合计, 支出合计)：余额 = 期初余额 + 收入 − 支出。"""
    items = build_account_items(db, account.id, user_id)
    income = sum(item.amount for item in items if item.category == "income")
    expense = sum(item.amount for item in items if item.category == "expense")
    return _as_float(account.initial_balance) + income - expense, income, expense


def fill_balances(db: Session, accounts, user_id: int) -> None:
    """就地计算账户余额（列表接口用）。"""
    for account in accounts:
        account.initial_balance = _as_float(account.initial_balance)
        balance, _income, _expense = compute_balance(db, account, user_id)
        account.balance = balance


@router.get("", response_model=list[schemas.AccountRead])
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """只返回当前登录用户自己的账户，余额按关联收支实时算出。"""
    accounts = (
        db.query(Account)
        .filter(Account.owner_id == current_user.id)
        .order_by(Account.id)
        .all()
    )
    fill_balances(db, accounts, current_user.id)
    return accounts


@router.post("", response_model=schemas.AccountRead, status_code=201)
def create_account(
    payload: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump()
    data["owner_id"] = current_user.id  # 强制归属当前用户，忽略客户端传值
    data["initial_balance"] = _as_float(data.get("initial_balance"))
    data["balance"] = data["initial_balance"]  # 新建时尚无收支，余额就等于期初余额
    account = Account(**data)
    db.add(account)
    db.commit()
    db.refresh(account)
    account.balance = compute_balance(db, account, current_user.id)[0]
    return account


@router.get("/{account_id}", response_model=schemas.AccountRead)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    account.balance = compute_balance(db, account, current_user.id)[0]
    return account


@router.get(
    "/{account_id}/income-expenses",
    response_model=schemas.AccountIncomeExpenseSummary,
    summary="账户关联的收支流水与余额推算",
)
def list_account_income_expenses(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """账户管理页展开行用：流水明细 + 「期初 + 收入 − 支出 = 余额」的推算过程。"""
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    account.initial_balance = _as_float(account.initial_balance)
    items = build_account_items(db, account.id, current_user.id)
    income = sum(item.amount for item in items if item.category == "income")
    expense = sum(item.amount for item in items if item.category == "expense")
    net = income - expense
    balance = account.initial_balance + net
    account.balance = balance
    return schemas.AccountIncomeExpenseSummary(
        account_id=account.id,
        initial_balance=account.initial_balance,
        income_total=income,
        expense_total=expense,
        net_total=net,
        balance=balance,
        items=items,
    )


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
        if key == "initial_balance":
            value = _as_float(value)
        setattr(account, key, value)
    account.initial_balance = _as_float(account.initial_balance)
    account.balance = compute_balance(db, account, current_user.id)[0]
    db.commit()
    db.refresh(account)
    account.balance = compute_balance(db, account, current_user.id)[0]
    return account


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    # 账户没了，关联的收支保留但解除绑定（显示成「未指定」），不跟着一起删
    db.query(IncomeExpense).filter(IncomeExpense.account_id == account_id).update(
        {IncomeExpense.account_id: None}, synchronize_session=False
    )
    db.delete(account)
    db.commit()
