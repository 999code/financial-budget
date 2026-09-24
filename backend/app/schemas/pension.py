"""养老金模块的接口数据模型。

约定：金额（amount）一律由后端按规则算出，Create / Update 里**不含** amount 字段。
"""
from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator

from app.models.pension import (
    DEFAULT_DIVISOR_MAP,
    DEFAULT_RESIDENT_LEVELS,
    DEFAULT_RESIDENT_SUBSIDY,
    DIRECTION_EXPENSE,
    ENTERPRISE,
    GOVERNMENT,
    RESIDENT,
    SCHEME_TEXT,
    VALID_DIRECTIONS,
    VALID_SCHEMES,
)

DIRECTION_TEXT = {"income": "领取", "expense": "缴费"}


def _check_scheme(value: str) -> str:
    if value not in VALID_SCHEMES:
        raise ValueError(f"人员分类必须为 {'/'.join(VALID_SCHEMES)}")
    return value


def _check_direction(value: Optional[str]) -> Optional[str]:
    if value is None or value == "":
        return None
    if value not in VALID_DIRECTIONS:
        raise ValueError("方向必须为 income(领取) 或 expense(缴费)")
    return value


def _check_month(value: str) -> str:
    text = (value or "").strip()
    if len(text) != 7 or text[4] != "-" or not text[:4].isdigit() or not text[5:].isdigit():
        raise ValueError("月份格式必须为 YYYY-MM")
    month = int(text[5:])
    if month < 1 or month > 12:
        raise ValueError("月份必须在 01~12 之间")
    return text


# ---------------------------------------------------------------- 人员档案
class PensionPersonBase(BaseModel):
    name: str
    scheme: str = ENTERPRISE
    salary: float = 0.0  # 职工=月工资；居民=年缴费档次
    birth_date: Optional[date] = None
    retire_date: Optional[date] = None
    contribution_years: float = 0.0
    personal_account_balance: float = 0.0
    deemed_years: float = 0.0
    deemed_index: Optional[float] = None
    annuity_balance: float = 0.0
    resident_base: Optional[float] = None
    note: Optional[str] = None

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        text = (v or "").strip()
        if not text:
            raise ValueError("请输入人员姓名")
        return text

    @field_validator("scheme")
    @classmethod
    def _scheme(cls, v: str) -> str:
        return _check_scheme(v)


class PensionPersonCreate(PensionPersonBase):
    pass


class PensionPersonUpdate(BaseModel):
    name: Optional[str] = None
    scheme: Optional[str] = None
    salary: Optional[float] = None
    birth_date: Optional[date] = None
    retire_date: Optional[date] = None
    contribution_years: Optional[float] = None
    personal_account_balance: Optional[float] = None
    deemed_years: Optional[float] = None
    deemed_index: Optional[float] = None
    annuity_balance: Optional[float] = None
    resident_base: Optional[float] = None
    note: Optional[str] = None

    @field_validator("name")
    @classmethod
    def _name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        text = v.strip()
        if not text:
            raise ValueError("请输入人员姓名")
        return text

    @field_validator("scheme")
    @classmethod
    def _scheme(cls, v: Optional[str]) -> Optional[str]:
        return None if v is None else _check_scheme(v)


class PensionPersonRead(PensionPersonBase):
    id: int
    scheme_text: str = ""
    retire_age: Optional[float] = None  # 退休时的年龄（岁，用于查计发月数）
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------- 参数配置
class PensionParamsBase(BaseModel):
    base_number: float = 8000.0
    avg_index: float = 1.0
    base_floor: float = 0.6
    base_cap: float = 3.0
    personal_rate: float = 8.0
    annuity_personal_rate: float = 4.0
    company_rate: float = 16.0
    include_company: bool = False
    deemed_index: float = 1.0
    transition_coef: float = 1.3
    retire_age: float = 60.0
    resident_base: float = 163.0
    resident_divisor: float = 139.0
    long_pay_threshold: float = 15.0
    long_pay_bonus: float = 2.0
    elderly_age: float = 65.0
    elderly_bonus: float = 0.0
    divisor_map: Dict[str, float] = dict(DEFAULT_DIVISOR_MAP)
    resident_levels: List[float] = list(DEFAULT_RESIDENT_LEVELS)
    resident_subsidy_map: Dict[str, float] = dict(DEFAULT_RESIDENT_SUBSIDY)


class PensionParamsUpdate(BaseModel):
    base_number: Optional[float] = None
    avg_index: Optional[float] = None
    base_floor: Optional[float] = None
    base_cap: Optional[float] = None
    personal_rate: Optional[float] = None
    annuity_personal_rate: Optional[float] = None
    company_rate: Optional[float] = None
    include_company: Optional[bool] = None
    deemed_index: Optional[float] = None
    transition_coef: Optional[float] = None
    retire_age: Optional[float] = None
    resident_base: Optional[float] = None
    resident_divisor: Optional[float] = None
    long_pay_threshold: Optional[float] = None
    long_pay_bonus: Optional[float] = None
    elderly_age: Optional[float] = None
    elderly_bonus: Optional[float] = None
    divisor_map: Optional[Dict[str, float]] = None
    resident_levels: Optional[List[float]] = None
    resident_subsidy_map: Optional[Dict[str, float]] = None


class PensionParamsRead(PensionParamsBase):
    id: int
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------- 月度记录
class PensionCreate(BaseModel):
    person_id: int
    period_month: str
    direction: Optional[str] = None  # 留空=按退休日期自动判定
    salary: Optional[float] = None  # 留空=取人员档案工资
    occurred_on: Optional[date] = None
    note: Optional[str] = None
    # 记录级覆盖（留空=取人员档案值）
    contribution_years: Optional[float] = None
    personal_account_balance: Optional[float] = None
    deemed_years: Optional[float] = None
    deemed_index: Optional[float] = None
    annuity_balance: Optional[float] = None
    resident_base: Optional[float] = None

    @field_validator("period_month")
    @classmethod
    def _month(cls, v: str) -> str:
        return _check_month(v)

    @field_validator("direction")
    @classmethod
    def _direction(cls, v: Optional[str]) -> Optional[str]:
        return _check_direction(v)


class PensionUpdate(BaseModel):
    person_id: Optional[int] = None
    period_month: Optional[str] = None
    direction: Optional[str] = None
    salary: Optional[float] = None
    occurred_on: Optional[date] = None
    note: Optional[str] = None
    contribution_years: Optional[float] = None
    personal_account_balance: Optional[float] = None
    deemed_years: Optional[float] = None
    deemed_index: Optional[float] = None
    annuity_balance: Optional[float] = None
    resident_base: Optional[float] = None

    @field_validator("period_month")
    @classmethod
    def _month(cls, v: Optional[str]) -> Optional[str]:
        return None if v is None else _check_month(v)

    @field_validator("direction")
    @classmethod
    def _direction(cls, v: Optional[str]) -> Optional[str]:
        return _check_direction(v)


class PensionRead(BaseModel):
    id: int
    person_id: int
    person_name: str
    scheme: str
    scheme_text: str = ""
    direction: str
    direction_text: str = ""
    period_month: str
    occurred_on: Optional[date] = None
    salary: float = 0.0
    amount: float = 0.0  # 服务端计算，只读
    signed_amount: float = 0.0  # 领取为正、缴费为负
    breakdown: Dict[str, float] = {}
    params: Dict[str, object] = {}
    overrides: Dict[str, object] = {}
    note: Optional[str] = None
    synced_income_expense_id: Optional[int] = None  # 已同步到的固定收支 id，None=未同步
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------- 同步到收支管理
class PensionSyncRequest(BaseModel):
    """把某条养老金记录同步成「固定收支」。"""

    account_id: Optional[int] = None  # 关联账户（选填，留空=未指定）
    name: Optional[str] = None  # 留空=按「人员·分类养老金方向」自动生成


class PensionSyncResult(BaseModel):
    action: str  # created(新建) / updated(更新)
    income_expense_id: int
    name: str
    amount: float
    category: str  # income(收入)/expense(支出)
    period: str  # monthly
    link_broken: bool = False  # 原关联收支已被删除，本次改为新建


# ---------------------------------------------------------------- 试算
class PensionPreviewRequest(BaseModel):
    person_id: int
    period_month: str
    direction: Optional[str] = None
    salary: Optional[float] = None
    contribution_years: Optional[float] = None
    personal_account_balance: Optional[float] = None
    deemed_years: Optional[float] = None
    deemed_index: Optional[float] = None
    annuity_balance: Optional[float] = None
    resident_base: Optional[float] = None

    @field_validator("period_month")
    @classmethod
    def _month(cls, v: str) -> str:
        return _check_month(v)

    @field_validator("direction")
    @classmethod
    def _direction(cls, v: Optional[str]) -> Optional[str]:
        return _check_direction(v)


class PensionPreviewResult(BaseModel):
    amount: float = 0.0
    signed_amount: float = 0.0
    direction: str = DIRECTION_EXPENSE
    direction_text: str = ""
    scheme: str = ENTERPRISE
    scheme_text: str = ""
    period_month: str = ""
    breakdown: Dict[str, float] = {}
    params: Dict[str, object] = {}


# ---------------------------------------------------------------- 统计
class PensionMonthStat(BaseModel):
    month: str
    income: float = 0.0
    expense: float = 0.0
    net: float = 0.0
    count: int = 0


class PensionSchemeStat(BaseModel):
    scheme: str
    scheme_text: str = ""
    income: float = 0.0
    expense: float = 0.0
    net: float = 0.0
    count: int = 0


class PensionStats(BaseModel):
    income_total: float = 0.0
    expense_total: float = 0.0
    net: float = 0.0
    count: int = 0
    month_stats: List[PensionMonthStat] = []
    scheme_stats: List[PensionSchemeStat] = []


__all__ = [
    "PensionPersonBase",
    "PensionPersonCreate",
    "PensionPersonUpdate",
    "PensionPersonRead",
    "PensionParamsBase",
    "PensionParamsUpdate",
    "PensionParamsRead",
    "PensionCreate",
    "PensionUpdate",
    "PensionRead",
    "PensionPreviewRequest",
    "PensionPreviewResult",
    "PensionMonthStat",
    "PensionSchemeStat",
    "PensionStats",
    "DIRECTION_TEXT",
    "SCHEME_TEXT",
    "RESIDENT",
    "GOVERNMENT",
    "ENTERPRISE",
]
