"""仪表盘派生统计模型（由账户与收支数据实时算出，不落库）。"""
from pydantic import BaseModel, Field


class AbsoluteOutlookMonth(BaseModel):
    """绝对值口径下某一个月的收支与累计余额。"""

    month: str = Field("", description="月份 YYYY-MM")
    income: float = Field(0.0, description="该月收入合计")
    expense: float = Field(0.0, description="该月支出合计")
    net: float = Field(0.0, description="该月净额（收入 − 支出）")
    balance: float = Field(0.0, description="该月末账户预计余额")


class AbsoluteOutlookRead(BaseModel):
    """资金消耗与耗尽预测（绝对值口径）。

    与 FundRunwayRead 的区别：不把临时收支摊销成「月均运行率」，而是按
    收支管理里设置的真实金额逐月累加到所选时间点，得到该时点的累计收入、
    累计支出以及「支出 / 收入」比例，同时模拟账户余额找出转负的月份。
    """

    opening_balance: float = Field(0.0, description="当前账户余额合计（模拟起点）")
    account_count: int = Field(0, description="账户数量")
    months: int = Field(12, description="预测跨度（月）")
    from_month: str = Field("", description="起始月份 YYYY-MM（当前月的下一月）")
    target_month: str = Field("", description="目标月份 YYYY-MM")
    total_income: float = Field(0.0, description="截至目标月份的累计收入")
    total_expense: float = Field(0.0, description="截至目标月份的累计支出")
    net_amount: float = Field(0.0, description="累计净额（收入 − 支出）")
    expense_income_ratio: float | None = Field(
        None, description="支出占收入的比例（0~N，可超过 1；收入为 0 时为 null）"
    )
    expense_income_percent: float | None = Field(
        None, description="支出占收入的百分比（如 128.5；收入为 0 时为 null）"
    )
    net_asset: float = Field(0.0, description="净资产总额（账户余额合计，比例的基准）")
    expense_net_asset_ratio: float | None = Field(
        None, description="支出占净资产总额的比例（0~N，可超过 1；净资产为 0 时为 null）"
    )
    expense_net_asset_percent: float | None = Field(
        None, description="支出占净资产总额的百分比（如 16.4；净资产为 0 时为 null）"
    )
    projected_balance: float = Field(0.0, description="目标月末预计账户余额")
    depletion_month: str | None = Field(
        None, description="账户余额首次转负的月份 YYYY-MM；不会转负时为 null"
    )
    monthly: list[AbsoluteOutlookMonth] = Field(default_factory=list, description="逐月明细")
    status: str = Field(
        "nodata", description="healthy(支出<收入)/warning/danger(入不敷出或余额转负)/nodata"
    )
    message: str = Field("", description="结论文案，可直接展示给用户")


class FundRunwayRead(BaseModel):
    """账户资金消耗进度与耗尽预测。

    口径说明：
    - 余额 = 各账户「期初余额 + 关联收入 − 关联支出」实时汇总；
    - 消耗速度 = 固定收支的月度化金额（年度固定按 /12）+ 临时收支在统计窗口内摊销；
      用「当前月度运行率」而非历史均值，避免刚新增的固定收支被窗口稀释；
    - progress = 未来 horizon_months 个月将消耗掉的余额占比（0~100，封顶）。
    """

    balance: float = Field(0.0, description="账户实时余额合计")
    account_count: int = Field(0, description="账户数量")
    window_months: int = Field(6, description="统计窗口（月）")
    horizon_months: int = Field(12, description="消耗进度基准周期（月）")
    monthly_income: float = Field(0.0, description="月均收入")
    monthly_expense: float = Field(0.0, description="月均支出")
    monthly_net_outflow: float = Field(
        0.0, description="月均净流出（支出 − 收入，>0 表示资金在减少）"
    )
    runway_months: float | None = Field(
        None, description="按当前速度可支撑的月数；净流入或数据不足时为 null"
    )
    depletion_date: str | None = Field(
        None, description="预计耗尽日期 YYYY-MM-DD；不会耗尽时为 null"
    )
    consumption_ratio: float | None = Field(
        None, description="未来 horizon_months 个月消耗掉的余额比例（0~1，可超过 1）"
    )
    progress: float = Field(0.0, description="环形进度百分比（0~100）")
    status: str = Field(
        "nodata", description="surplus(净流入)/healthy/warning/danger/nodata(数据不足)"
    )
    message: str = Field("", description="结论文案，可直接展示给用户")
