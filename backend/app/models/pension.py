"""养老金模块：人员档案、参数配置、月度记录三张表 + 计算引擎。

计算口径依据国发〔2005〕38 号、《国务院关于机关事业单位工作人员养老保险制度改革的决定》
及后续各省公布的计发办法，并已按 2025—2026 年公开政策补齐以下能力：

- 职工类（企业职工 / 公务员事业单位）
  - 领取：基础养老金 + 个人账户养老金 + 过渡性养老金（"中人"），
          机关事业再加职业年金；企业可加企业年金；两类都可叠第三支柱个人养老金
  - 个人账户支持**按历年记账利率复利滚存推算**，不用再手工估一个数
  - 过渡性养老金支持「四川式 / 广东式」两种官方口径
  - 法定退休年龄支持按渐进式延迟退休政策自动推算（2025-01-01 起）
  - 缴费：单位职工按缴费基数 × 8%（机关事业再加职业年金 4%）；
          灵活就业人员按 20% 且全部由个人承担
- 城乡居民
  - 领取：财政定额基础养老金 + 个人账户养老金 + 长缴加发 + 高龄加发（可拉阶梯）
  - 缴费：（年缴费档次 + 政府补贴）÷ 12
  - 居民个人账户记账利率与职工不同，由各省另行公布

金额一律由服务端 ``calc_pension()`` 计算后落库，接口不接受客户端传值。
"""
import calendar
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

# ---------------------------------------------------------------- 真实政策常量
# 各省市 2025 年度养老金计发基数（元/月），来源：各省人社厅公布的年度文件。
# 省内分档的地区单独列出；未列入的地区请在参数设置里手工填写。
# 注意：计发基数每年重算公布，跨年后数值会变，使用时请确认年度。
REGION_BASE_NUMBERS: List[tuple] = [
    ("上海", 12434.0),
    ("西藏", 11777.0),
    ("广东（不含深圳）", 9493.0),
    ("青海", 9056.0),
    ("新疆", 8448.0),
    ("浙江", 8433.0),
    ("宁夏", 8366.0),
    ("辽宁·沈阳（企业）", 8390.0),
    ("辽宁·大连（企业）", 8956.0),
    ("辽宁（不含沈阳大连）", 7346.0),
    ("云南", 8265.0),
    ("海南", 8188.0),
    ("内蒙古", 8179.0),
    ("吉林（长春）", 7978.25),
    ("吉林（不含长春、农垦）", 7322.08),
    ("吉林（农垦企业）", 2223.42),
    ("福建", 7932.0),
    ("湖南", 7694.0),
    ("黑龙江", 7570.0),
    ("河北", 7410.0),
    ("贵州", 7324.5),
    ("江西", 7054.0),
    # —— 以下为 P0 整改补齐的主要省份（2025 年度，来源：各省人社厅正式文件）——
    ("北京", 12049.0),          # 京人社发〔2025〕13号：2025 计算基数 12049 元/月
    ("深圳（企业）", 11293.0),   # 粤人社：深圳企业退休计发基数 11293（不含深圳为 9493）
    ("天津", 9417.0),           # 津人社局 2025-11-13 通知：2025 计发基数 9417 元/月
    ("江苏", 8917.0),           # 苏人社：2025 全省企业职工养老计发基数 8917（离退休人数全国第一）
    ("四川", 8462.0),           # 川人社办发〔2025〕39号 口径：2025 计发基数 8462 元/月
    ("重庆", 8240.0),           # 渝人社：2025 计发基数 8240 元/月
    ("湖北（武汉/省直）", 9112.0),  # 湖北按地市分档，武汉/省直一档计发基数 9112（见暖心人社梳理）
    ("湖北（不含武汉）", 7300.0),   # 湖北二/三档地市计发基数约 7200–7400，取代表值 7300
    ("安徽", 7999.0),           # 皖人社秘〔2025〕153号：2025 计发基数 7999 元/月
    ("山东", 7831.0),           # 鲁人社字〔2025〕100号：2025 计发基数 7831（不含菏泽）
    ("陕西", 7881.0),           # 2025 全省计发基数约 7881（陕已逐步并轨，与缴费基数接近）
    ("广西", 6983.0),           # 桂人社发〔2025〕43号：2025 养老待遇计发基数 6983（注意≠缴费基数上下限 6905）
    ("甘肃", 7746.0),           # 甘人社：2025 计发基数约 7746 元/月
    ("山西", 7253.0),           # 晋人社：2025 计发基数约 7253 元/月
    ("河南", 6738.0),           # 豫人社：2025 计发基数约 6738 元/月（全国最低梯队）
]

# 城镇职工基本养老保险个人账户记账利率（%）。
# 2016 年起由人社部、财政部统一公布；2015 及以前由各地确定，
# 此处采用地方社保经办机构公开口径，仅用于历史年度滚存推算。
BOOK_RATE_HISTORY: Dict[int, float] = {
    1986: 7.20, 1987: 7.20, 1988: 8.64, 1989: 10.08, 1990: 10.08,
    1991: 7.56, 1992: 7.65, 1993: 9.18, 1994: 10.98, 1995: 10.98,
    1996: 9.18, 1997: 7.47, 1998: 5.22, 1999: 3.78, 2000: 2.25,
    2001: 1.98, 2002: 1.98, 2003: 2.25, 2004: 2.25, 2005: 2.25,
    2006: 2.52, 2007: 3.21, 2008: 3.92, 2009: 2.25, 2010: 2.30,
    2011: 3.28, 2012: 3.24, 2013: 3.25, 2014: 2.97, 2015: 5.00,
    2016: 8.31, 2017: 7.12, 2018: 8.29, 2019: 7.61, 2020: 6.04,
    2021: 6.69, 2022: 6.12, 2023: 3.97, 2024: 2.62, 2025: 1.50,
}

# 过渡性养老金的两类官方口径
TRANSITION_SICHUAN = "sichuan"  # （计发基数 + 指数化月均缴费工资）÷2 × 视同年限 × 系数
TRANSITION_GUANGDONG = "guangdong"  # 计发基数 × 视同缴费指数 × 视同年限 × 系数
VALID_TRANSITION_FORMULAS = (TRANSITION_SICHUAN, TRANSITION_GUANGDONG)
TRANSITION_TEXT = {
    TRANSITION_SICHUAN: "四川等省（用平均缴费指数）",
    TRANSITION_GUANGDONG: "广东等省（用视同缴费指数）",
}

# 渐进式延迟退休：2025-01-01 起启动，用 15 年过渡到新法定退休年龄
GENDER_MALE = "male"
GENDER_FEMALE = "female"
POST_WORKER = "worker"  # 女工人岗（原 50 周岁退休）
POST_CADRE = "cadre"  # 女干部 / 技术岗（原 55 周岁退休）


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
    retire_date = Column(Date, nullable=True, comment="退休日期（空且填了性别时按渐进式延退政策推算）")
    gender = Column(String(10), nullable=True, comment="male(男)/female(女)，用于推算法定退休年龄")
    post_type = Column(
        String(10),
        nullable=True,
        comment="女性岗位：worker(工人岗，原50岁)/cadre(干部技术岗，原55岁)",
    )
    contribution_years = Column(Float, default=0.0, comment="缴费年限（年）")
    personal_account_balance = Column(Float, default=0.0, comment="个人账户储存额（手填值）")
    auto_balance = Column(
        Boolean, default=False, server_default="0",
        comment="是否按缴费基数+记账利率自动推算个人账户储存额",
    )
    deemed_years = Column(Float, default=0.0, comment="视同缴费年限（年，仅职工）")
    deemed_index = Column(Float, nullable=True, comment="视同缴费指数（留空取参数默认值）")
    annuity_balance = Column(Float, default=0.0, comment="职业年金账户储存额（仅机关事业）")
    enterprise_annuity_balance = Column(Float, default=0.0, comment="企业年金账户储存额（仅企业职工）")
    private_pension_balance = Column(Float, default=0.0, comment="第三支柱个人养老金账户储存额")
    flexible = Column(
        Boolean, default=False, server_default="0",
        comment="是否灵活就业人员（缴费按 20% 且全部个人承担）",
    )
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
    region = Column(String(50), nullable=True, comment="参保地区（选了会自动带出计发基数）")
    avg_index = Column(Float, default=0.6, comment="本人平均缴费工资指数（多数企业按下限缴，默认 0.6）")
    base_floor = Column(Float, default=0.6, comment="缴费基数下限比例（社平的 60%）")
    base_cap = Column(Float, default=3.0, comment="缴费基数上限比例（社平的 300%）")
    book_rate = Column(
        Float, default=1.5, server_default="1.5",
        comment="职工个人账户记账利率(%)，国家每年公布，2025 年为 1.5%",
    )
    resident_book_rate = Column(
        Float, default=3.6, server_default="3.6",
        comment="居民个人账户记账利率(%)，各省另行公布（皖3.67/闽3.84/鲁3.63）",
    )
    wage_growth = Column(
        Float, default=6.0, server_default="6.0",
        comment="缴费基数年增长率(%)，用于倒推历年缴费额推算账户储存额",
    )
    personal_rate = Column(Float, default=8.0, comment="养老个人缴费费率(%)")
    flexible_rate = Column(
        Float, default=20.0, server_default="20.0",
        comment="灵活就业人员缴费费率(%)，全部个人承担（其中 8% 入个人账户）",
    )
    annuity_personal_rate = Column(Float, default=4.0, comment="职业年金个人缴费费率(%)（机关事业）")
    company_rate = Column(Float, default=16.0, comment="单位缴费费率(%)（默认不计入收支）")
    include_company = Column(Boolean, default=False, comment="是否把单位缴费计入收支金额")
    deemed_index = Column(
        Float, nullable=True,
        comment="视同缴费指数，留空时回落到本人平均缴费指数（各省口径不同）",
    )
    transition_coef = Column(Float, default=1.3, comment="过渡系数(%)（各省 1.2~1.4）")
    transition_formula = Column(
        String(20), default=TRANSITION_SICHUAN, server_default=TRANSITION_SICHUAN,
        comment="过渡性养老金口径：sichuan/guangdong",
    )
    retire_age = Column(Float, default=60.0, comment="缺省退休年龄（无法推算时用于查计发月数）")
    adjust_rate = Column(
        Float, default=2.0, server_default="2.0",
        comment="退休后养老金年调整比例(%)，近年总体水平约 2%",
    )
    resident_base = Column(Float, default=163.0, comment="居民基础养老金（元/月，2026 全国最低 163）")
    resident_divisor = Column(Float, default=139.0, comment="居民个人账户计发月数（不分年龄，139）")
    long_pay_threshold = Column(Float, default=15.0, comment="长缴加发起算年限（年）")
    long_pay_bonus = Column(Float, default=2.0, comment="长缴加发（元/月·每多缴 1 年）")
    elderly_age = Column(Float, default=65.0, comment="高龄加发起始年龄")
    elderly_bonus = Column(Float, default=0.0, comment="高龄加发（元/月，未配阶梯时取此值）")
    elderly_tiers = Column(
        Text, nullable=True, comment='JSON：{"65":5,"70":10,"80":20} 高龄加发阶梯（元/月）'
    )

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
    synced_income_expense_id = Column(
        Integer,
        nullable=True,
        comment="已同步到的固定收支记录 id（幂等：重复同步走更新而非新建）",
    )
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


def _f(value, default: float) -> float:
    """读浮点参数：值为 None（历史行 ALTER 出来的列）时回落到默认值。"""
    return float(value) if value is not None else float(default)


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


# ---------------------------------------------------------------- 政策推算工具
def _months_since(birth: date, anchor_year: int, anchor_month: int) -> int:
    """出生月份相对某个基准年月的月数（早于基准返回负数）。"""
    return (birth.year - anchor_year) * 12 + (birth.month - anchor_month)


def add_months_to_date(source: date, months: int) -> date:
    """在日期上按月加减，日超出当月天数时取当月最后一天。"""
    total = source.year * 12 + (source.month - 1) + months
    year, month = divmod(total, 12)
    month += 1
    day = min(source.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def legal_retire_months(
    birth: Optional[date],
    gender: Optional[str],
    post_type: Optional[str] = None,
) -> Optional[float]:
    """按渐进式延迟退休政策推算法定退休年龄（返回总月数）。

    依据 2024-09-13 通过、2025-01-01 实施的延迟退休决定：
    - 男职工（原 60 周岁）：每 4 个月延迟 1 个月，逐步到 63 周岁
    - 女工人岗（原 50 周岁）：每 2 个月延迟 1 个月，逐步到 55 周岁
    - 女干部 / 技术岗（原 55 周岁）：每 4 个月延迟 1 个月，逐步到 58 周岁

    返回值仅供预算估算，实际以社保经办机构核定为准。
    """
    if not birth:
        return None
    if gender == GENDER_MALE:
        anchor, step, cap, base_months = (1965, 1), 4, 36, 60 * 12
    elif gender == GENDER_FEMALE:
        if post_type == POST_CADRE:
            anchor, step, cap, base_months = (1970, 1), 4, 36, 55 * 12
        else:  # 女工人岗，未指定岗位时按此处理
            anchor, step, cap, base_months = (1975, 1), 2, 60, 50 * 12
    else:
        return None
    elapsed = _months_since(birth, anchor[0], anchor[1])
    delay = 0 if elapsed < 0 else min(elapsed // step + 1, cap)
    return float(base_months + delay)


def legal_retire_date(
    birth: Optional[date],
    gender: Optional[str],
    post_type: Optional[str] = None,
) -> Optional[date]:
    """法定退休年月日（由法定退休年龄换算）。"""
    months = legal_retire_months(birth, gender, post_type)
    return None if months is None else add_months_to_date(birth, int(round(months)))


def estimate_account_balance(
    current_base: float,
    years: float,
    rate_pct: float,
    book_rate_pct: float,
    growth_pct: float,
    end_year: Optional[int] = None,
) -> float:
    """按「当前缴费基数 + 工资年增长率」倒推历年缴费，并按历年记账利率复利滚存。

    当年缴费按年中一次性投入（计半年息）近似，与国家公布的逐年计息口径接近。

    - ``current_base``：最近一个年度的月缴费基数
    - ``rate_pct``：入个人账户的缴费比例（职工 8%、灵活就业 8%）
    - ``book_rate_pct``：记账利率，缺历史年份数据时用它兜底
    """
    years_int = max(int(years or 0), 0)
    if years_int <= 0 or current_base <= 0:
        return 0.0
    end_year = end_year or (date.today().year - 1)  # 上一个完整缴费年度
    growth = float(growth_pct or 0) / 100.0
    rate = float(rate_pct or 0) / 100.0
    fallback = float(book_rate_pct or 0) / 100.0

    balance = 0.0
    # 先按「偏移」倒推各年缴费额，再按年份**升序**逐年滚存（复利必须顺着时间方向累加）
    schedule = []
    for offset in range(years_int):
        year = end_year - offset
        discount = ((1 + growth) ** offset) if growth else 1.0
        yearly_base = float(current_base) / discount
        schedule.append((year, yearly_base * 12.0 * rate))
    schedule.sort(key=lambda item: item[0])
    for year, pay in schedule:
        r = BOOK_RATE_HISTORY.get(year, fallback) / 100.0
        balance = balance * (1 + r) + pay * (1 + r / 2.0)
    return balance


def min_contribution_years(retire_year: Optional[int]) -> float:
    """最低缴费年限：2029 年底前仍为 15 年，2030 年起每年提高 6 个月，到 2040 年提至 20 年。"""
    if not retire_year or retire_year < 2030:
        return 15.0
    return min(15.0 + (retire_year - 2029) * 0.5, 20.0)


def elderly_bonus_of(
    age_years: float,
    elderly_age: float,
    elderly_bonus: float,
    tiers: Optional[Dict[str, float]] = None,
) -> float:
    """高龄加发：配了阶梯就按年龄取适用的最高档，否则走「起始年龄 + 固定金额」。"""
    if tiers:
        best = 0.0
        for key, value in tiers.items():
            try:
                threshold = float(key)
            except (TypeError, ValueError):
                continue
            if age_years + 1e-9 >= threshold:
                best = max(best, float(value or 0))
        return best
    return float(elderly_bonus or 0) if age_years >= float(elderly_age or 0) else 0.0


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
    # 以下为按 2025—2026 政策补齐的可选项
    auto_balance: bool = False,  # 是否按记账利率自动推算个人账户储存额
    age_years: Optional[float] = None,  # 实际年龄（居民高龄加发按实际年龄判定）
    flexible: bool = False,  # 灵活就业人员（20% 全部个人承担）
    enterprise_annuity_balance: float = 0.0,  # 企业年金储存额
    private_pension_balance: float = 0.0,  # 第三支柱个人养老金储存额
) -> CalcResult:
    """按人员分类与方向计算养老金金额，同时给出明细与所用参数。

    ``params`` 为空时使用模块内置的默认口径（便于单元测试直接调用）。
    """
    p = params
    base_number = _f(getattr(p, "base_number", None), 8000.0)
    avg_index = _f(getattr(p, "avg_index", None), 0.6)
    book_rate = _f(getattr(p, "book_rate", None), 1.5)
    resident_book_rate = _f(getattr(p, "resident_book_rate", None), 3.6)
    wage_growth = _f(getattr(p, "wage_growth", None), 6.0)
    personal_rate = _f(getattr(p, "personal_rate", None), 8.0)
    flexible_rate = _f(getattr(p, "flexible_rate", None), 20.0)
    annuity_rate = _f(getattr(p, "annuity_personal_rate", None), 4.0)
    company_rate = _f(getattr(p, "company_rate", None), 16.0)
    include_company = bool(getattr(p, "include_company", False))
    # 视同缴费指数缺省回落到本人平均缴费指数（各省口径不同，1.0 对低基数人群明显高估）
    fallback_index = getattr(p, "deemed_index", None)
    default_deemed_index = float(fallback_index) if fallback_index is not None else avg_index
    transition_coef = _f(getattr(p, "transition_coef", None), 1.3)
    transition_formula = str(getattr(p, "transition_formula", None) or TRANSITION_SICHUAN)
    resident_base_default = _f(getattr(p, "resident_base", None), 163.0)
    resident_divisor = _f(getattr(p, "resident_divisor", None), 139.0)
    long_pay_threshold = _f(getattr(p, "long_pay_threshold", None), 15.0)
    long_pay_bonus = _f(getattr(p, "long_pay_bonus", None), 2.0)
    elderly_age = _f(getattr(p, "elderly_age", None), 65.0)
    elderly_bonus = _f(getattr(p, "elderly_bonus", None), 0.0)
    elderly_tiers = json_loads(getattr(p, "elderly_tiers", None), None) or {}
    retire_age = _f(getattr(p, "retire_age", None), 60.0)

    divisor_map = divisor_map_of(p)
    subsidy_map = subsidy_map_of(p)
    years = float(contribution_years or 0)
    months = retire_months if retire_months else retire_age * 12.0
    divisor = divisor_for_age_months(months, divisor_map)

    # 个人账户储存额：开启了自动推算就按「缴费基数 + 记账利率」滚存，否则用手填值
    balance = float(personal_account_balance or 0)
    estimated = 0.0
    if auto_balance:
        if scheme == RESIDENT:
            level = float(salary or 0)
            subsidy = subsidy_for_level(level, subsidy_map)
            yearly = level + subsidy
            cb = yearly / 12.0
        else:
            cb = contribution_base(salary, p)
            yearly = cb * 12.0 * (personal_rate / 100.0)
        rate = resident_book_rate if scheme == RESIDENT else book_rate
        # 居民是把（档次+补贴）全额计入个人账户，故按 100% 折算成等效费率
        base_for_roll = cb if scheme != RESIDENT else yearly / 12.0
        estimated = estimate_account_balance(
            current_base=base_for_roll,
            years=years,
            rate_pct=100.0 if scheme == RESIDENT else personal_rate,
            book_rate_pct=rate,
            growth_pct=wage_growth,
        )
        balance = estimated

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
        if flexible:
            # 灵活就业：全部由个人承担（默认 20%，其中 8% 进个人账户，12% 进统筹）
            own = base * flexible_rate / 100.0
            breakdown["缴费基数"] = round(base, 2)
            breakdown[f"灵活就业个人缴({flexible_rate:g}%)"] = round(own, 2)
            total = own
        else:
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
        used.update({"缴费基数": round(base, 2), "计发基数": base_number})
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
        # 居民的高龄加发看的是实际年龄，不是「退休年龄」（居民统一 60 岁起领）
        age = age_years if age_years is not None else months / 12.0
        elderly = elderly_bonus_of(age, elderly_age, elderly_bonus, elderly_tiers)
        breakdown["基础养老金(财政定额)"] = round(basic, 2)
        breakdown[f"个人账户养老金(÷{resident_divisor:g})"] = round(account, 2)
        if long_pay:
            breakdown[f"长缴加发({extra_years:g}年)"] = round(long_pay, 2)
        if elderly:
            breakdown[f"高龄加发({age:.1f}岁)"] = round(elderly, 2)
        used.update({
            "基础养老金": basic,
            "个人账户储存额": balance,
            "计发月数": resident_divisor,
            "缴费年限": years,
        })
        if auto_balance:
            used.update({"居民记账利率(%)": resident_book_rate, "储存额为推算值": True})
        private = float(private_pension_balance or 0) / resident_divisor if resident_divisor else 0.0
        if private:
            breakdown[f"个人养老金(÷{resident_divisor:g})"] = round(private, 2)
        return CalcResult(
            amount=round(basic + account + long_pay + elderly + private, 2),
            direction=direction,
            scheme=scheme,
            breakdown=breakdown,
            params=used,
        )

    index = float(deemed_index) if deemed_index is not None else default_deemed_index
    indexed_wage = base_number * avg_index
    basic = (base_number + indexed_wage) / 2.0 * years * 0.01
    account = balance / divisor if divisor else 0.0
    # 过渡性养老金：四川等省用平均缴费指数，广东等省用单独的视同缴费指数
    deemed = float(deemed_years or 0)
    if not deemed:
        transitional = 0.0
    elif transition_formula == TRANSITION_GUANGDONG:
        transitional = base_number * index * deemed * transition_coef / 100.0
    else:
        transitional = (base_number + indexed_wage) / 2.0 * deemed * transition_coef / 100.0
    annuity = float(annuity_balance or 0) / divisor if (scheme == GOVERNMENT and divisor) else 0.0
    enterprise_annuity = (
        float(enterprise_annuity_balance or 0) / divisor
        if (scheme == ENTERPRISE and divisor)
        else 0.0
    )
    private = float(private_pension_balance or 0) / divisor if divisor else 0.0

    breakdown["基础养老金"] = round(basic, 2)
    breakdown[f"个人账户养老金(÷{divisor:g})"] = round(account, 2)
    if deemed:
        breakdown["过渡性养老金"] = round(transitional, 2)
    if scheme == GOVERNMENT:
        breakdown[f"职业年金(÷{divisor:g})"] = round(annuity, 2)
    if enterprise_annuity:
        breakdown[f"企业年金(÷{divisor:g})"] = round(enterprise_annuity, 2)
    if private:
        breakdown[f"个人养老金(÷{divisor:g})"] = round(private, 2)
    used.update({
        "计发基数": base_number,
        "平均缴费指数": avg_index,
        "缴费年限": years,
        "个人账户储存额": balance,
        "计发月数": divisor,
        "退休年龄(岁)": round(months / 12.0, 2),
        "视同缴费年限": deemed,
        "视同缴费指数": index,
        "过渡系数(%)": transition_coef,
        "过渡性口径": TRANSITION_TEXT.get(transition_formula, transition_formula),
        "退休后年调整(%)": _f(getattr(p, "adjust_rate", None), 2.0),
    })
    if auto_balance:
        used.update({
            "记账利率(%)": book_rate,
            "工资增长率(%)": wage_growth,
            "储存额为推算值": True,
        })
    total = basic + account + transitional + annuity + enterprise_annuity + private
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
    # 退休日期优先取档案值；没填但有出生日期和性别时，按渐进式延退政策推算
    effective_retire_date = person.retire_date
    legal_months = None
    if not effective_retire_date and person.birth_date and person.gender:
        legal_months = legal_retire_months(person.birth_date, person.gender, person.post_type)
        if legal_months is not None:
            effective_retire_date = legal_retire_date(
                person.birth_date, person.gender, person.post_type
            )
    resolved = resolve_direction(ov.get("direction", direction), period_month, effective_retire_date)
    retire_months = months_between(person.birth_date, effective_retire_date)
    if retire_months is None and legal_months is not None:
        retire_months = int(round(legal_months))
    # 实际年龄：按记录所属月份计算（居民高龄加发要用）
    age_years = None
    if person.birth_date:
        try:
            year, month = int(period_month[:4]), int(period_month[5:7])
            age_years = months_between(person.birth_date, date(year, month, 1)) / 12.0
        except (TypeError, ValueError):
            age_years = None
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
        auto_balance=bool(person.auto_balance),
        age_years=age_years,
        flexible=bool(person.flexible),
        enterprise_annuity_balance=float(person.enterprise_annuity_balance or 0),
        private_pension_balance=float(person.private_pension_balance or 0),
    )
