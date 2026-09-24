"""养老金管理接口。

- 金额由服务端 ``calc_for_person()`` 算出后落库，请求体里**没有** amount 字段；
- 人员档案与参数配置各自独立维护，记录保存时会把用到的值快照下来；
- 所有数据按 ``owner_id`` 隔离，越权一律 404。
"""
import json
from collections import defaultdict
from datetime import date, datetime
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas
from app.api.auth import get_current_user, get_owned_or_404
from app.api.income_expense import ensure_details, sync_detail_amounts
from app.database import get_db
from app.models import Account, IncomeExpense, Pension, PensionParams, PensionPerson, User
from app.models.pension import (
    DIRECTION_EXPENSE,
    DIRECTION_INCOME,
    ENTERPRISE,
    SCHEME_TEXT,
    VALID_DIRECTIONS,
    VALID_SCHEMES,
    calc_for_person,
    json_loads,
    months_between,
)

router = APIRouter(prefix="/pensions", tags=["养老金管理"])
persons_router = APIRouter(prefix="/pension-persons", tags=["养老金人员档案"])
params_router = APIRouter(prefix="/pension-params", tags=["养老金参数"])

DIRECTION_TEXT = {"income": "领取", "expense": "缴费"}


# ---------------------------------------------------------------- 工具
def _get_params(db: Session, user_id: int) -> PensionParams:
    """取当前用户的参数配置，没有则按默认值播种一份。"""
    params = db.query(PensionParams).filter(PensionParams.owner_id == user_id).first()
    if params is None:
        params = PensionParams(owner_id=user_id)
        db.add(params)
        db.commit()
        db.refresh(params)
    return params


def _month_of(value: Optional[str]) -> Optional[str]:
    """把 YYYY-MM-DD 归一化成 YYYY-MM，方便与 period_month 比较。"""
    return value[:7] if value else None


def _overrides_of(source) -> Dict:
    """从请求体里挑出记录级覆盖字段（只保留显式传了的）。"""
    keys = (
        "salary",
        "contribution_years",
        "personal_account_balance",
        "deemed_years",
        "deemed_index",
        "annuity_balance",
        "resident_base",
    )
    data = source.model_dump(exclude_unset=True) if hasattr(source, "model_dump") else {}
    return {k: data[k] for k in keys if k in data}


def _person_read(person: PensionPerson) -> schemas.PensionPersonRead:
    data = schemas.PensionPersonRead.model_validate(person, from_attributes=True)
    months = months_between(person.birth_date, person.retire_date)
    data.scheme_text = SCHEME_TEXT.get(person.scheme, person.scheme or "")
    data.retire_age = round(months / 12.0, 1) if months is not None else None
    return data


JSON_PENSION_FIELDS = ("breakdown", "params", "overrides")
DERIVED_PENSION_FIELDS = ("scheme_text", "direction_text", "signed_amount")


def _pension_read(record: Pension) -> schemas.PensionRead:
    payload = {
        name: getattr(record, name)
        for name in schemas.PensionRead.model_fields
        if name not in JSON_PENSION_FIELDS + DERIVED_PENSION_FIELDS
    }
    payload["breakdown"] = json_loads(record.breakdown, {}) or {}
    payload["params"] = json_loads(record.params, {}) or {}
    payload["overrides"] = json_loads(record.overrides, {}) or {}
    data = schemas.PensionRead(**payload)
    data.scheme_text = SCHEME_TEXT.get(record.scheme, record.scheme or "")
    data.direction_text = DIRECTION_TEXT.get(record.direction, record.direction or "")
    data.signed_amount = (
        float(record.amount or 0) if record.direction == DIRECTION_INCOME else -float(record.amount or 0)
    )
    return data


def _preview_result(
    person: PensionPerson,
    result,
    period_month: str,
) -> schemas.PensionPreviewResult:
    return schemas.PensionPreviewResult(
        amount=result.amount,
        signed_amount=result.amount if result.direction == DIRECTION_INCOME else -result.amount,
        direction=result.direction,
        direction_text=DIRECTION_TEXT.get(result.direction, result.direction),
        scheme=result.scheme,
        scheme_text=SCHEME_TEXT.get(result.scheme, result.scheme),
        period_month=period_month,
        breakdown=result.breakdown,
        params=result.params,
    )


def _calc(
    db: Session,
    user_id: int,
    person_id: int,
    period_month: str,
    direction: Optional[str],
    overrides: Dict,
):
    """按人员档案 + 覆盖值计算（人员必须属于当前用户）。"""
    person = get_owned_or_404(db, PensionPerson, person_id, user_id)
    params = _get_params(db, user_id)
    ov = dict(overrides or {})
    ov["direction"] = ov.get("direction", direction)
    result = calc_for_person(person, params, period_month, direction=direction, overrides=ov)
    return person, result


def _ensure_no_duplicate(
    db: Session,
    user_id: int,
    person_id: int,
    period_month: str,
    direction: str,
    exclude_id: Optional[int] = None,
) -> None:
    q = db.query(Pension).filter(
        Pension.owner_id == user_id,
        Pension.person_id == person_id,
        Pension.period_month == period_month,
        Pension.direction == direction,
    )
    if exclude_id:
        q = q.filter(Pension.id != exclude_id)
    if q.first():
        raise HTTPException(
            status_code=409,
            detail=f"该人员在本月已有一条{DIRECTION_TEXT.get(direction, '')}记录，请直接修改或删除后再新增",
        )


def _occurred_on_of(period_month: str, explicit: Optional[date]) -> date:
    if explicit:
        return explicit
    return date(int(period_month[:4]), int(period_month[5:7]), 1)


def _sync_name(record: Pension) -> str:
    """同步到收支管理时的默认名称，如「张三·企业职工养老金领取」。"""
    scheme_text = SCHEME_TEXT.get(record.scheme, record.scheme or "")
    direction_text = DIRECTION_TEXT.get(record.direction, record.direction or "")
    return f"{record.person_name}·{scheme_text}养老金{direction_text}"


# ---------------------------------------------------------------- 月度记录
@router.get("", response_model=list[schemas.PensionRead])
def list_pensions(
    person: Optional[str] = None,
    scheme: Optional[str] = Query(None, description="enterprise/government/resident"),
    direction: Optional[str] = Query(None, description="income(领取)/expense(缴费)"),
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD，起始时间"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD，结束时间"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """养老金记录列表，支持按人员、分类、方向、时间范围筛选（仅当前用户的数据）。"""
    if scheme and scheme not in VALID_SCHEMES:
        raise HTTPException(status_code=400, detail="人员分类取值非法")
    if direction and direction not in VALID_DIRECTIONS:
        raise HTTPException(status_code=400, detail="方向必须为 income 或 expense")

    q = db.query(Pension).filter(Pension.owner_id == current_user.id)
    if person:
        q = q.filter(Pension.person_name.ilike(f"%{person}%"))
    if scheme:
        q = q.filter(Pension.scheme == scheme)
    if direction:
        q = q.filter(Pension.direction == direction)
    start_month, end_month = _month_of(start_date), _month_of(end_date)
    if start_month:
        q = q.filter(Pension.period_month >= start_month)
    if end_month:
        q = q.filter(Pension.period_month <= end_month)
    rows = q.order_by(Pension.period_month.desc(), Pension.id.desc()).all()
    return [_pension_read(row) for row in rows]


@router.get("/stats", response_model=schemas.PensionStats)
def pension_stats(
    person: Optional[str] = None,
    scheme: Optional[str] = None,
    direction: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """按月统计养老金的领取 / 缴费 / 净额，并按人员分类汇总。"""
    q = db.query(Pension).filter(Pension.owner_id == current_user.id)
    if person:
        q = q.filter(Pension.person_name.ilike(f"%{person}%"))
    if scheme:
        q = q.filter(Pension.scheme == scheme)
    if direction:
        q = q.filter(Pension.direction == direction)
    start_month, end_month = _month_of(start_date), _month_of(end_date)
    if start_month:
        q = q.filter(Pension.period_month >= start_month)
    if end_month:
        q = q.filter(Pension.period_month <= end_month)
    rows = q.all()

    month_income: Dict[str, float] = defaultdict(float)
    month_expense: Dict[str, float] = defaultdict(float)
    month_count: Dict[str, int] = defaultdict(int)
    scheme_income: Dict[str, float] = defaultdict(float)
    scheme_expense: Dict[str, float] = defaultdict(float)
    scheme_count: Dict[str, int] = defaultdict(int)

    income_total = expense_total = 0.0
    for row in rows:
        amount = float(row.amount or 0)
        if row.direction == DIRECTION_INCOME:
            income_total += amount
            month_income[row.period_month] += amount
            scheme_income[row.scheme] += amount
        else:
            expense_total += amount
            month_expense[row.period_month] += amount
            scheme_expense[row.scheme] += amount
        month_count[row.period_month] += 1
        scheme_count[row.scheme] += 1

    months = sorted(set(month_income) | set(month_expense) | set(month_count), reverse=True)
    schemes = sorted(set(scheme_income) | set(scheme_expense) | set(scheme_count))

    return schemas.PensionStats(
        income_total=round(income_total, 2),
        expense_total=round(expense_total, 2),
        net=round(income_total - expense_total, 2),
        count=len(rows),
        month_stats=[
            schemas.PensionMonthStat(
                month=m,
                income=round(month_income.get(m, 0.0), 2),
                expense=round(month_expense.get(m, 0.0), 2),
                net=round(month_income.get(m, 0.0) - month_expense.get(m, 0.0), 2),
                count=month_count.get(m, 0),
            )
            for m in months
        ],
        scheme_stats=[
            schemas.PensionSchemeStat(
                scheme=s,
                scheme_text=SCHEME_TEXT.get(s, s or ""),
                income=round(scheme_income.get(s, 0.0), 2),
                expense=round(scheme_expense.get(s, 0.0), 2),
                net=round(scheme_income.get(s, 0.0) - scheme_expense.get(s, 0.0), 2),
                count=scheme_count.get(s, 0),
            )
            for s in schemes
        ],
    )


@router.post("/preview", response_model=schemas.PensionPreviewResult)
def preview_pension(
    payload: schemas.PensionPreviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """试算：只返回金额与明细，不落库（供新增/编辑弹窗实时预览）。"""
    _person, result = _calc(
        db,
        current_user.id,
        payload.person_id,
        payload.period_month,
        payload.direction,
        _overrides_of(payload),
    )
    return _preview_result(_person, result, payload.period_month)


@router.post("", response_model=schemas.PensionRead, status_code=201)
def create_pension(
    payload: schemas.PensionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """新增一条月度记录，金额由服务端按规则计算。"""
    overrides = _overrides_of(payload)
    person, result = _calc(
        db,
        current_user.id,
        payload.person_id,
        payload.period_month,
        payload.direction,
        overrides,
    )
    _ensure_no_duplicate(db, current_user.id, person.id, payload.period_month, result.direction)
    record = Pension(
        person_id=person.id,
        person_name=person.name,
        scheme=result.scheme or person.scheme or ENTERPRISE,
        direction=result.direction,
        period_month=payload.period_month,
        occurred_on=_occurred_on_of(payload.period_month, payload.occurred_on),
        salary=float(payload.salary if payload.salary is not None else person.salary or 0),
        amount=result.amount,
        params=json.dumps(result.params, ensure_ascii=False),
        overrides=json.dumps(overrides, ensure_ascii=False),
        breakdown=json.dumps(result.breakdown, ensure_ascii=False),
        note=payload.note,
        owner_id=current_user.id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return _pension_read(record)


@router.get("/{pension_id}", response_model=schemas.PensionRead)
def get_pension(
    pension_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _pension_read(get_owned_or_404(db, Pension, pension_id, current_user.id))


@router.put("/{pension_id}", response_model=schemas.PensionRead)
def update_pension(
    pension_id: int,
    payload: schemas.PensionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """编辑记录：改动人员、月份、工资或覆盖值后，金额会重新计算。"""
    record = get_owned_or_404(db, Pension, pension_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    updates.pop("owner_id", None)

    person_id = updates.get("person_id", record.person_id)
    period_month = updates.get("period_month", record.period_month)
    direction = updates.get("direction", record.direction)

    # 覆盖值：旧值打底 + 本次显式传的值；显式传 null 表示"取消覆盖，改用档案值"
    merged = dict(json_loads(record.overrides, {}) or {})
    merged.update(_overrides_of(payload))
    overrides = {k: v for k, v in merged.items() if v is not None}

    person, result = _calc(db, current_user.id, person_id, period_month, direction, overrides)
    _ensure_no_duplicate(
        db, current_user.id, person.id, period_month, result.direction, exclude_id=record.id
    )

    for key, value in updates.items():
        setattr(record, key, value)
    record.person_id = person.id
    record.person_name = person.name
    record.scheme = result.scheme or person.scheme or ENTERPRISE
    record.direction = result.direction
    record.period_month = period_month
    record.occurred_on = _occurred_on_of(period_month, updates.get("occurred_on", record.occurred_on))
    record.salary = float(
        overrides.get("salary", updates.get("salary", person.salary)) or 0
    )
    record.amount = result.amount
    record.params = json.dumps(result.params, ensure_ascii=False)
    record.overrides = json.dumps(overrides, ensure_ascii=False)
    record.breakdown = json.dumps(result.breakdown, ensure_ascii=False)
    db.commit()
    db.refresh(record)
    return _pension_read(record)


@router.delete("/{pension_id}", status_code=204)
def delete_pension(
    pension_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_owned_or_404(db, Pension, pension_id, current_user.id)
    db.delete(record)
    db.commit()


def _sync_payload_of(record: Pension, name: Optional[str]) -> Dict:
    """构造同步到固定收支所需的字段。"""
    occurred_on = record.occurred_on or _occurred_on_of(record.period_month, None)
    return {
        "name": (name or "").strip() or _sync_name(record),
        "amount": float(record.amount or 0),
        "kind": "fixed",
        "category": record.direction,
        "period": "monthly",
        "end_date": None,  # 养老金按月发生，不设终止时间
        "occurred_at": datetime(occurred_on.year, occurred_on.month, occurred_on.day),
        "note": f"由养老金记录同步（{record.person_name} · {record.period_month}）",
    }


@router.post("/{pension_id}/sync", response_model=schemas.PensionSyncResult)
def sync_pension_to_income_expense(
    pension_id: int,
    payload: Optional[schemas.PensionSyncRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """把该条养老金记录同步成「收支管理」里的固定收支（每月、不终止）。

    幂等：同一条养老金重复同步时更新上次生成的那条收支，不会重复堆积；
    若那条收支已被手动删除或不属于当前用户，则重新创建一条。
    """
    record = get_owned_or_404(db, Pension, pension_id, current_user.id)
    body = payload or schemas.PensionSyncRequest()
    if float(record.amount or 0) <= 0:
        raise HTTPException(status_code=400, detail="金额为 0，无法同步到收支管理")

    account_id = body.account_id
    if account_id is not None:
        account = db.get(Account, account_id)
        if account is None or account.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="账户不存在")

    fields = _sync_payload_of(record, body.name)

    item = None
    link_broken = False
    if record.synced_income_expense_id:
        item = db.get(IncomeExpense, record.synced_income_expense_id)
        if item is not None and item.owner_id != current_user.id:
            item = None  # 越权：当作未关联处理，重新创建
        if item is None:
            link_broken = True  # 上次同步的那条已被删除

    if item is None:
        item = IncomeExpense(account_id=account_id, owner_id=current_user.id, **fields)
        db.add(item)
        db.commit()
        db.refresh(item)
        ensure_details(item, db)  # 入库即按月展开期次
        record.synced_income_expense_id = item.id
        db.commit()
        action = "created"
    else:
        old_amount = item.amount
        for key, value in fields.items():
            setattr(item, key, value)
        item.account_id = account_id
        db.commit()
        db.refresh(item)
        sync_detail_amounts(db, item, old_amount)  # 已展开期次按新金额同步
        ensure_details(item, db)
        action = "updated"

    return schemas.PensionSyncResult(
        action=action,
        income_expense_id=item.id,
        name=item.name,
        amount=item.amount,
        category=item.category,
        period=item.period or "monthly",
        link_broken=link_broken,
    )


# ---------------------------------------------------------------- 人员档案
@persons_router.get("", response_model=list[schemas.PensionPersonRead])
def list_persons(
    name: Optional[str] = None,
    scheme: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(PensionPerson).filter(PensionPerson.owner_id == current_user.id)
    if name:
        q = q.filter(PensionPerson.name.ilike(f"%{name}%"))
    if scheme:
        q = q.filter(PensionPerson.scheme == scheme)
    rows = q.order_by(PensionPerson.id.desc()).all()
    return [_person_read(row) for row in rows]


@persons_router.post("", response_model=schemas.PensionPersonRead, status_code=201)
def create_person(
    payload: schemas.PensionPersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump()
    data["owner_id"] = current_user.id
    person = PensionPerson(**data)
    db.add(person)
    db.commit()
    db.refresh(person)
    return _person_read(person)


@persons_router.put("/{person_id}", response_model=schemas.PensionPersonRead)
def update_person(
    person_id: int,
    payload: schemas.PensionPersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    person = get_owned_or_404(db, PensionPerson, person_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "owner_id":
            continue
        setattr(person, key, value)
    db.commit()
    db.refresh(person)
    return _person_read(person)


@persons_router.delete("/{person_id}", status_code=204)
def delete_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除人员档案，同时清理其名下的养老金记录。"""
    person = get_owned_or_404(db, PensionPerson, person_id, current_user.id)
    db.query(Pension).filter(Pension.person_id == person.id).delete()
    db.delete(person)
    db.commit()


# ---------------------------------------------------------------- 参数配置
JSON_PARAM_FIELDS = ("divisor_map", "resident_levels", "resident_subsidy_map")


def _params_read(params: PensionParams) -> schemas.PensionParamsRead:
    """把 ORM 对象（JSON 列为文本）转成响应模型。"""
    from app.models.pension import (
        DEFAULT_DIVISOR_MAP,
        DEFAULT_RESIDENT_LEVELS,
        DEFAULT_RESIDENT_SUBSIDY,
        json_loads as _loads,
    )

    payload = {
        name: getattr(params, name)
        for name in schemas.PensionParamsBase.model_fields
        if name not in JSON_PARAM_FIELDS
    }
    payload["divisor_map"] = _loads(params.divisor_map, dict(DEFAULT_DIVISOR_MAP)) or dict(DEFAULT_DIVISOR_MAP)
    payload["resident_levels"] = _loads(params.resident_levels, list(DEFAULT_RESIDENT_LEVELS)) or list(
        DEFAULT_RESIDENT_LEVELS
    )
    payload["resident_subsidy_map"] = _loads(
        params.resident_subsidy_map, dict(DEFAULT_RESIDENT_SUBSIDY)
    ) or dict(DEFAULT_RESIDENT_SUBSIDY)
    return schemas.PensionParamsRead(id=params.id, updated_at=params.updated_at, **payload)


@params_router.get("", response_model=schemas.PensionParamsRead)
def get_params(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _params_read(_get_params(db, current_user.id))


@params_router.put("", response_model=schemas.PensionParamsRead)
def update_params(
    payload: schemas.PensionParamsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    params = _get_params(db, current_user.id)
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if key in ("divisor_map", "resident_levels", "resident_subsidy_map"):
            setattr(params, key, json.dumps(value, ensure_ascii=False) if value is not None else None)
        elif key == "owner_id":
            continue
        else:
            setattr(params, key, value)
    db.commit()
    db.refresh(params)
    return _params_read(params)
