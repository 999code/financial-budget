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
    POST_CADRE,
    POST_WORKER,
    RESIDENT,
    SCHEME_TEXT,
    VALID_DIRECTIONS,
    VALID_SCHEMES,
    VALID_TRANSITION_FORMULAS,
)

DIRECTION_TEXT = {"income": "领取", "expense": "缴费"}
GENDER_TEXT = {"male": "男", "female": "女"}
POST_TEXT = {POST_WORKER: "工人岗（原50岁）", POST_CADRE: "干部/技术岗（原55岁）"}


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
    gender: Optional[str] = None  # male/female，用于推算法定退休年龄
    post_type: Optional[str] = None  # 女性岗位：worker/cadre
    contribution_years: float = 0.0
    personal_account_balance: float = 0.0
    auto_balance: bool = False  # 按记账利率自动推算个人账户储存额
    deemed_years: float = 0.0
    deemed_index: Optional[float] = None
    annuity_balance: float = 0.0
    enterprise_annuity_balance: float = 0.0  # 企业年金
    private_pension_balance: float = 0.0  # 第三支柱个人养老金
    flexible: bool = False  # 灵活就业（缴费 20% 全部个人承担）
    resident_base: Optional[float] = None
    note: Optional[str] = None

    @field_validator("gender")
    @classmethod
    def _gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        text = str(v).strip().lower()
        if text not in ("male", "female"):
            raise ValueError("性别必须为 male(男) 或 female(女)")
        return text

    @field_validator("post_type")
    @classmethod
    def _post(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        text = str(v).strip().lower()
        if text not in (POST_WORKER, POST_CADRE):
            raise ValueError("女性岗位必须为 worker 或 cadre")
        return text

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
    gender: Optional[str] = None
    post_type: Optional[str] = None
    contribution_years: Optional[float] = None
    personal_account_balance: Optional[float] = None
    auto_balance: Optional[bool] = None
    deemed_years: Optional[float] = None
    deemed_index: Optional[float] = None
    annuity_balance: Optional[float] = None
    enterprise_annuity_balance: Optional[float] = None
    private_pension_balance: Optional[float] = None
    flexible: Optional[bool] = None
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

    @field_validator("gender")
    @classmethod
    def _gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        text = str(v).strip().lower()
        if text not in ("male", "female"):
            raise ValueError("性别必须为 male(男) 或 female(女)")
        return text

    @field_validator("post_type")
    @classmethod
    def _post(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        text = str(v).strip().lower()
        if text not in (POST_WORKER, POST_CADRE):
            raise ValueError("女性岗位必须为 worker 或 cadre")
        return text


class PensionPersonRead(PensionPersonBase):
    id: int
    scheme_text: str = ""
    gender_text: str = ""
    post_text: str = ""
    retire_age: Optional[float] = None  # 退休时的年龄（岁，用于查计发月数）
    legal_retire_age: Optional[float] = None  # 按渐进式延退政策推算的法定退休年龄（岁）
    legal_retire_date: Optional[date] = None  # 推算的法定退休日期
    retire_source: str = ""  # manual(手填) / legal(政策推算)
    estimated_balance: float = 0.0  # 按记账利率推算的个人账户储存额（供参考）
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------- 参数配置
class PensionParamsBase(BaseModel):
    region: Optional[str] = None  # 参保地区（选择后自动带出计发基数）
    base_number: float = 8000.0
    avg_index: float = 0.6  # 多数企业按下限缴，默认取 0.6；实际以本人历年指数为准
    base_floor: float = 0.6
    base_cap: float = 3.0
    book_rate: float = 1.5  # 职工个人账户记账利率(%)，2025 年为 1.5%
    resident_book_rate: float = 3.6  # 居民记账利率(%)，各省另行公布
    wage_growth: float = 6.0  # 缴费基数年增长率(%)，用于推算账户储存额
    personal_rate: float = 8.0
    flexible_rate: float = 20.0  # 灵活就业人员缴费费率(%)
    annuity_personal_rate: float = 4.0
    company_rate: float = 16.0
    include_company: bool = False
    deemed_index: Optional[float] = None  # 留空时回落到本人平均缴费指数
    transition_coef: float = 1.3
    transition_formula: str = "sichuan"  # sichuan(用平均缴费指数)/guangdong(用视同缴费指数)
    retire_age: float = 60.0
    adjust_rate: float = 2.0  # 退休后养老金年调整比例(%)
    resident_base: float = 163.0
    resident_divisor: float = 139.0
    long_pay_threshold: float = 15.0
    long_pay_bonus: float = 2.0
    elderly_age: float = 65.0
    elderly_bonus: float = 0.0
    elderly_tiers: Dict[str, float] = {}  # {"65":5,"70":10} 高龄加发阶梯（元/月）
    divisor_map: Dict[str, float] = dict(DEFAULT_DIVISOR_MAP)
    resident_levels: List[float] = list(DEFAULT_RESIDENT_LEVELS)
    resident_subsidy_map: Dict[str, float] = dict(DEFAULT_RESIDENT_SUBSIDY)

    @field_validator("transition_formula")
    @classmethod
    def _formula(cls, v: str) -> str:
        text = str(v or "").strip().lower()
        if text not in VALID_TRANSITION_FORMULAS:
            raise ValueError("过渡性口径必须为 sichuan 或 guangdong")
        return text


class PensionParamsUpdate(BaseModel):
    region: Optional[str] = None
    base_number: Optional[float] = None
    avg_index: Optional[float] = None
    base_floor: Optional[float] = None
    base_cap: Optional[float] = None
    book_rate: Optional[float] = None
    resident_book_rate: Optional[float] = None
    wage_growth: Optional[float] = None
    personal_rate: Optional[float] = None
    flexible_rate: Optional[float] = None
    annuity_personal_rate: Optional[float] = None
    company_rate: Optional[float] = None
    include_company: Optional[bool] = None
    deemed_index: Optional[float] = None
    transition_coef: Optional[float] = None
    transition_formula: Optional[str] = None
    retire_age: Optional[float] = None
    adjust_rate: Optional[float] = None
    resident_base: Optional[float] = None
    resident_divisor: Optional[float] = None
    long_pay_threshold: Optional[float] = None
    long_pay_bonus: Optional[float] = None
    elderly_age: Optional[float] = None
    elderly_bonus: Optional[float] = None
    elderly_tiers: Optional[Dict[str, float]] = None
    divisor_map: Optional[Dict[str, float]] = None
    resident_levels: Optional[List[float]] = None
    resident_subsidy_map: Optional[Dict[str, float]] = None

    @field_validator("transition_formula")
    @classmethod
    def _formula(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        text = str(v).strip().lower()
        if text not in VALID_TRANSITION_FORMULAS:
            raise ValueError("过渡性口径必须为 sichuan 或 guangdong")
        return text


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


class PensionRegionItem(BaseModel):
    """可选择的参保地区及其计发基数。"""

    name: str
    base_number: float


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
