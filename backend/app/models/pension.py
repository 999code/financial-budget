"""养老金模块：人员档案、参数配置、月度记录三张表 + 计算引擎。

计算口径依据附件《公务员事业单位与企业养老金对比》《养老金计发结构》：

- 职工类（企业职工 / 公务员事业单位）
  - 领取：基础养老金 + 个人账户养老金 + 过渡性养老金（"中人"），机关事业再加职业年金
  - 缴费：缴费基数 × 个人费率 8%（机关事业再加职业年金个人 4%）
- 城乡居民
  - 领取：财政定额基础养老金 + 个人账户养老金 + 长缴加发 + 高龄加发
  - 缴费：（年缴费档次 + 政府补贴）÷ 12

金额一律由服务端 ``calc_pension()`` 计算后落库，接口不接受客户端传值。
"""
import json
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.database import Base

# ---------------------------------------------------------------- 常量
ENTERPRISE = "enterprise"  # 企业职工
GOVERNMENT = "government"  # 公务员 / 事业单位
RESIDENT = "resident"  # 城乡居民
VALID_SCHEMES = (ENTERPRISE, GOVERNMENT, RESIDENT)
SCHEME_TEXT = {
    ENTERPRISE: "企业职工",
    GOVERNMENT: "公务员事业单位",
    RESIDENT: "城乡居民",
}

DIRECTION_INCOME = "income"  # 领取
DIRECTION_EXPENSE = "expense"  # 缴费
VALID_DIRECTIONS = (DIRECTION_INCOME, DIRECTION_EXPENSE)

# 计发月数表（键=退休年龄，值=计发月数）：60 岁 139、55 岁 170、50 岁 195，
# 延迟退休按"精确到月"核定，故 61~63 岁一并给出，中间值线性插值。
DEFAULT_DIVISOR_MAP = {
    "50": 195.0,
    "55": 170.0,
    "60": 139.0,
    "61": 132.0,
    "62": 125.0,
    "63": 117.0,
}
# 居民缴费档次（元/年）与政府补贴（元/年），各地不同，可在参数设置里改
DEFAULT_RESIDENT_LEVELS = [100.0, 300.0, 500.0, 1000.0, 2000.0, 3000.0, 5000.0]
DEFAULT_RESIDENT_SUBSIDY = {
    "100": 30.0,
    "300": 40.0,
    "500": 60.0,
    "1000": 120.0,
    "2000": 200.0,
    "3000": 280.0,
    "5000": 400.0,
}


# ---------------------------------------------------------------- 模型
class PensionPerson(Base):
    """养老金人员档案：工资、缴费年限、账户储存额等相对固定的参保信息。"""

    __tablename__ = "pension_persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="姓名")
    scheme = Column(
        String(20),
        nullable=False,
        server_default=ENTERPRISE,
        comment="enterprise(企业职工)/government(公务员事业单位)/resident(城乡居民)",
    )
    salary = Column(Float, default=0.0, comment="职工=月工资；居民=年缴费档次")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    retire_date = Column(Date, nullable=True, comment="退休日期（用于判定缴费/领取与计发月数）")
    contribution_years = Column(Float, default=0.0, comment="缴费年限（年）")
    personal_account_balance = Column(Float, default=0.0, comment="个人账户储存额")
    deemed_years = Column(Float, default=0.0, comment="视同缴费年限（年，仅职工）")
    deemed_index = Column(Float, nullable=True, comment="视同缴费指数（留空取参数默认值）")
    annuity_balance = Column(Float, default=0.0, comment="职业年金账户储存额（仅机关事业）")
    resident_base = Column(Float, nullable=True, comment="居民基础养老金（留空取参数默认值）")
    note = Column(String(200), nullable=True, comment="备注")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class PensionParams(Base):
    """养老金计算参数（每个用户一份，缺省时用模块默认值播种）。"""

    __tablename__ = "pension_params"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户")

    base_number = Column(Float, default=8000.0, comment="计发基数（各省公布，元/月）")
    avg_index = Column(Float, default=1.0, comment="本人平均缴费工资指数")
    base_floor = Column(Float, default=0.6, comment="缴费基数下限比例（社平的 60%）")
    base_cap = Column(Float, default=3.0, comment="缴费基数上限比例（社平的 300%）")
    personal_rate = Column(Float, default=8.0, comment="养老个人缴费费率(%)")
    annuity_personal_rate = Column(Float, default=4.0, comment="职业年金个人缴费费率(%)（机关事业）")
    company_rate = Column(Float, default=16.0, comment="单位缴费费率(%)（默认不计入收支）")
    include_company = Column(Boolean, default=False, comment="是否把单位缴费计入收支金额")
    deemed_index = Column(Float, default=1.0, comment="视同缴费指数默认值")
    transition_coef = Column(Float, default=1.3, comment="过渡系数(%)（各省 1.2~1.4）")
    retire_age = Column(Float, default=60.0, comment="缺省退休年龄（用于查计发月数）")
    resident_base = Column(Float, default=163.0, comment="居民基础养老金（元/月，2026 全国最低 163）")
    resident_divisor = Column(Float, default=139.0, comment="居民个人账户计发月数（不分年龄，139）")
    long_pay_threshold = Column(Float, default=15.0, comment="长缴加发起算年限（年）")
    long_pay_bonus = Column(Float, default=2.0, comment="长缴加发（元/月·每多缴 1 年）")
    elderly_age = Column(Float, default=65.0, comment="高龄加发起始年龄")
    elderly_bonus = Column(Float, default=0.0, comment="高龄加发（元/月）")

    divisor_map = Column(Text, nullable=True, comment='JSON：{"60":139,...} 退休年龄→计发月数')
    resident_levels = Column(Text, nullable=True, comment="JSON：[100,300,...] 居民年缴费档次")
    resident_subsidy_map = Column(Text, nullable=True, comment='JSON：{"500":60,...} 档次→政府补贴(元/年)')

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class Pension(Base):
    """养老金月度记录：金额由服务端按规则算出，接口不接受客户端传值。"""

    __tablename__ = "pensions"
    __table_args__ = (
        UniqueConstraint(
            "owner_id", "person_id", "period_month", "direction", name="uq_pension_person_month"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("pension_persons.id"), nullable=False, index=True, comment="关联人员")
    person_name = Column(String(50), nullable=False, comment="人员姓名（快照）")
    scheme = Column(String(20), nullable=False, comment="人员分类（快照）")
    direction = Column(String(10), nullable=False, comment="income(领取)/expense(缴费)")
    period_month = Column(String(7), nullable=False, index=True, comment="所属月份 YYYY-MM")
    occurred_on = Column(Date, nullable=True, comment="发生日期（列表展示用）")
    salary = Column(Float, default=0.0, comment="工资快照（职工=月工资，居民=年缴费档次）")
    amount = Column(Float, default=0.0, comment="金额（服务端按规则计算，只读）")
    params = Column(Text, nullable=True, comment="JSON：本次计算使用的参数快照")
    overrides = Column(Text, nullable=True, comment="JSON：记录级覆盖值（留空则取人员档案值）")
    breakdown = Column(Text, nullable=True, comment="JSON：计算明细（基础养老金/个人账户/过渡性/职业年金…）")
    note = Column(String(200), nullable=True, comment="备注")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="所属用户（数据隔离）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")


# ---------------------------------------------------------------- 计算引擎
@dataclass
class CalcResult:
    """计算结果：金额 + 明细 + 所用参数。"""

    amount: float = 0.0
    direction: str = DIRECTION_EXPENSE
    scheme: str = ENTERPRISE
    breakdown: Dict[str, float] = field(default_factory=dict)
    params: Dict[str, object] = field(default_factory=dict)


def json_loads(text_value: Optional[str], default):
    """把 JSON 文本列解析成对象，解析失败回退默认值。"""
    if not text_value:
        return default
    try:
        return json.loads(text_value)
    except (TypeError, ValueError):
        return default


def divisor_map_of(params: Optional[PensionParams]) -> Dict[str, float]:
    data = json_loads(getattr(params, "divisor_map", None), None)
    if isinstance(data, dict) and data:
        return {str(k): float(v) for k, v in data.items()}
    return dict(DEFAULT_DIVISOR_MAP)


def resident_levels_of(params: Optional[PensionParams]) -> List[float]:
    data = json_loads(getattr(params, "resident_levels", None), None)
    if isinstance(data, list) and data:
        return [float(v) for v in data]
    return list(DEFAULT_RESIDENT_LEVELS)


def subsidy_map_of(params: Optional[PensionParams]) -> Dict[str, float]:
    data = json_loads(getattr(params, "resident_subsidy_map", None), None)
    if isinstance(data, dict) and data:
        return {str(k): float(v) for k, v in data.items()}
    return dict(DEFAULT_RESIDENT_SUBSIDY)


def months_between(start: Optional[date], end: Optional[date]) -> Optional[int]:
    """两个日期相差的月数（按整月计，未到当月生日则减一个月）。"""
    if not start or not end:
        return None
    months = (end.year - start.year) * 12 + (end.month - start.month)
    return months - (1 if end.day < start.day else 0)


def divisor_for_age_months(months: Optional[float], divisor_map: Dict[str, float]) -> float:
    """按退休年龄（月）查计发月数，相邻档位线性插值。"""
    points = sorted((float(k) * 12.0, float(v)) for k, v in divisor_map.items())
    if not points:
        return 139.0
    value = float(months or 0)
    if value <= points[0][0]:
        return points[0][1]
    if value >= points[-1][0]:
        return points[-1][1]
    for (m1, v1), (m2, v2) in zip(points, points[1:]):
        if m1 <= value <= m2:
            if m2 == m1:
                return v1
            return round(v1 + (v2 - v1) * (value - m1) / (m2 - m1), 4)
    return points[-1][1]


def subsidy_for_level(level: float, subsidy_map: Dict[str, float]) -> float:
    """居民政府补贴：取不超过所选档次的最高档补贴。"""
    best_key = None
    best_threshold = None
    for key in subsidy_map:
        try:
            threshold = float(key)
        except (TypeError, ValueError):
            continue
        if level + 1e-9 >= threshold and (best_threshold is None or threshold > best_threshold):
            best_threshold = threshold
            best_key = key
    return float(subsidy_map[best_key]) if best_key else 0.0


def contribution_base(salary: float, params: Optional[PensionParams]) -> float:
    """职工缴费基数：工资在社平的 60%~300% 之间封顶。"""
    base_number = float(getattr(params, "base_number", 8000.0) or 0)
    floor = base_number * float(getattr(params, "base_floor", 0.6) or 0)
    cap = base_number * float(getattr(params, "base_cap", 3.0) or 0)
    salary = float(salary or 0)
    if salary <= 0:
        return 0.0
    return min(max(salary, floor), cap) if cap > 0 else max(salary, floor)


def resolve_direction(
    direction: Optional[str],
    period_month: str,
    retire_date: Optional[date],
) -> str:
    """方向：未指定时按退休日期自动判定（退休当月及之后为领取，之前为缴费）。"""
    if direction in VALID_DIRECTIONS:
        return direction
    if retire_date:
        try:
            year, month = int(period_month[:4]), int(period_month[5:7])
        except (TypeError, ValueError):
            return DIRECTION_EXPENSE
        return DIRECTION_INCOME if date(year, month, 1) >= date(retire_date.year, retire_date.month, 1) else DIRECTION_EXPENSE
    return DIRECTION_EXPENSE


def _pick(override, default):
    """覆盖值优先：记录上的可选覆盖字段为空时取人员档案值。"""
    return default if override is None else override


def calc_pension(
    *,
    scheme: str,
    salary: float,
    contribution_years: float,
    personal_account_balance: float,
    deemed_years: float = 0.0,
    deemed_index: Optional[float] = None,
    annuity_balance: float = 0.0,
    resident_base: Optional[float] = None,
    retire_months: Optional[float] = None,
    direction: str = DIRECTION_EXPENSE,
    params: Optional[PensionParams] = None,
) -> CalcResult:
    """按人员分类与方向计算养老金金额，同时给出明细与所用参数。

    ``params`` 为空时使用模块内置的默认口径（便于单元测试直接调用）。
    """
    p = params
    base_number = float(getattr(p, "base_number", 8000.0) or 0)
    avg_index = float(getattr(p, "avg_index", 1.0) or 0)
    personal_rate = float(getattr(p, "personal_rate", 8.0) or 0)
    annuity_rate = float(getattr(p, "annuity_personal_rate", 4.0) or 0)
    company_rate = float(getattr(p, "company_rate", 16.0) or 0)
    include_company = bool(getattr(p, "include_company", False))
    default_deemed_index = float(getattr(p, "deemed_index", 1.0) or 0)
    transition_coef = float(getattr(p, "transition_coef", 1.3) or 0)
    resident_base_default = float(getattr(p, "resident_base", 163.0) or 0)
    resident_divisor = float(getattr(p, "resident_divisor", 139.0) or 139.0)
    long_pay_threshold = float(getattr(p, "long_pay_threshold", 15.0) or 0)
    long_pay_bonus = float(getattr(p, "long_pay_bonus", 2.0) or 0)
    elderly_age = float(getattr(p, "elderly_age", 65.0) or 0)
    elderly_bonus = float(getattr(p, "elderly_bonus", 0.0) or 0)
    retire_age = float(getattr(p, "retire_age", 60.0) or 60.0)

    divisor_map = divisor_map_of(p)
    subsidy_map = subsidy_map_of(p)
    years = float(contribution_years or 0)
    balance = float(personal_account_balance or 0)
    months = retire_months if retire_months else retire_age * 12.0
    divisor = divisor_for_age_months(months, divisor_map)

    breakdown: Dict[str, float] = {}
    used: Dict[str, object] = {}

    if direction == DIRECTION_EXPENSE:  # -------------------------------- 缴费
        if scheme == RESIDENT:
            level = float(salary or 0)
            subsidy = subsidy_for_level(level, subsidy_map)
            monthly = (level + subsidy) / 12.0
            breakdown["年缴费档次"] = round(level, 2)
            breakdown["政府补贴(年)"] = round(subsidy, 2)
            breakdown["月均缴费"] = round(monthly, 2)
            used.update({"档次": level, "政府补贴": subsidy})
            return CalcResult(
                amount=round(monthly, 2),
                direction=direction,
                scheme=scheme,
                breakdown=breakdown,
                params=used,
            )

        base = contribution_base(salary, p)
        personal = base * personal_rate / 100.0
        annuity = base * annuity_rate / 100.0 if scheme == GOVERNMENT else 0.0
        company = base * company_rate / 100.0
        breakdown["缴费基数"] = round(base, 2)
        breakdown[f"养老个人({personal_rate:g}%)"] = round(personal, 2)
        if scheme == GOVERNMENT:
            breakdown[f"职业年金个人({annuity_rate:g}%)"] = round(annuity, 2)
        if company_rate:
            breakdown[f"单位缴纳({company_rate:g}%，{'计入' if include_company else '不计入'})"] = round(company, 2)
        total = personal + annuity + (company if include_company else 0.0)
        used.update({"缴费基数": round(base, 2), "个人费率": personal_rate, "计发基数": base_number})
        return CalcResult(
            amount=round(total, 2),
            direction=direction,
            scheme=scheme,
            breakdown=breakdown,
            params=used,
        )

    # ------------------------------------------------------------------ 领取
    if scheme == RESIDENT:
        basic = float(resident_base) if resident_base is not None else resident_base_default
        account = balance / resident_divisor if resident_divisor else 0.0
        extra_years = max(years - long_pay_threshold, 0.0)
        long_pay = extra_years * long_pay_bonus
        elderly = elderly_bonus if months >= elderly_age * 12.0 else 0.0
        breakdown["基础养老金(财政定额)"] = round(basic, 2)
        breakdown[f"个人账户养老金(÷{resident_divisor:g})"] = round(account, 2)
        if long_pay:
            breakdown[f"长缴加发({extra_years:g}年)"] = round(long_pay, 2)
        if elderly:
            breakdown[f"高龄加发(≥{elderly_age:g}岁)"] = round(elderly, 2)
        used.update({
            "基础养老金": basic,
            "个人账户储存额": balance,
            "计发月数": resident_divisor,
            "缴费年限": years,
        })
        return CalcResult(
            amount=round(basic + account + long_pay + elderly, 2),
            direction=direction,
            scheme=scheme,
            breakdown=breakdown,
            params=used,
        )

    index = float(deemed_index) if deemed_index is not None else default_deemed_index
    indexed_wage = base_number * avg_index
    basic = (base_number + indexed_wage) / 2.0 * years * 0.01
    account = balance / divisor if divisor else 0.0
    transitional = base_number * index * float(deemed_years or 0) * transition_coef / 100.0
    annuity = float(annuity_balance or 0) / divisor if (scheme == GOVERNMENT and divisor) else 0.0

    breakdown["基础养老金"] = round(basic, 2)
    breakdown[f"个人账户养老金(÷{divisor:g})"] = round(account, 2)
    if deemed_years:
        breakdown["过渡性养老金"] = round(transitional, 2)
    if scheme == GOVERNMENT:
        breakdown[f"职业年金(÷{divisor:g})"] = round(annuity, 2)
    used.update({
        "计发基数": base_number,
        "平均缴费指数": avg_index,
        "缴费年限": years,
        "个人账户储存额": balance,
        "计发月数": divisor,
        "视同缴费年限": float(deemed_years or 0),
        "视同缴费指数": index,
        "过渡系数(%)": transition_coef,
    })
    total = basic + account + transitional + annuity
    return CalcResult(
        amount=round(total, 2),
        direction=direction,
        scheme=scheme,
        breakdown=breakdown,
        params=used,
    )


def calc_for_person(
    person: PensionPerson,
    params: Optional[PensionParams],
    period_month: str,
    direction: Optional[str] = None,
    overrides: Optional[dict] = None,
) -> CalcResult:
    """按人员档案 + 记录级覆盖值计算，返回 CalcResult（含最终方向）。"""
    ov = overrides or {}
    scheme = ov.get("scheme") or person.scheme or ENTERPRISE
    resolved = resolve_direction(ov.get("direction", direction), period_month, person.retire_date)
    retire_months = months_between(person.birth_date, person.retire_date)
    return calc_pension(
        scheme=scheme,
        salary=float(_pick(ov.get("salary"), person.salary) or 0),
        contribution_years=float(_pick(ov.get("contribution_years"), person.contribution_years) or 0),
        personal_account_balance=float(
            _pick(ov.get("personal_account_balance"), person.personal_account_balance) or 0
        ),
        deemed_years=float(_pick(ov.get("deemed_years"), person.deemed_years) or 0),
        deemed_index=_pick(ov.get("deemed_index"), person.deemed_index),
        annuity_balance=float(_pick(ov.get("annuity_balance"), person.annuity_balance) or 0),
        resident_base=_pick(ov.get("resident_base"), person.resident_base),
        retire_months=retire_months,
        direction=resolved,
        params=params,
    )
