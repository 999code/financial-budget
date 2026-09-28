"""仪表盘派生统计模型（由账户与收支数据实时算出，不落库）。"""
from pydantic import BaseModel, Field


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
