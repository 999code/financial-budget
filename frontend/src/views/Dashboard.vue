<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="净资产总额" :value="summary.total_balance" :precision="2" prefix="¥">
            <template #prefix><span>¥</span></template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="累计收入" :value="summary.total_income" :precision="2" value-color="#f56c6c" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="累计支出" :value="summary.total_expense" :precision="2" value-color="#67c23a" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="账户数量" :value="summary.account_count" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 资金消耗进度与耗尽预测 -->
    <el-card class="runway" shadow="hover" v-loading="runwayLoading">
      <template #header>
        <div class="runway__hd">
          <span class="runway__title">资金消耗与耗尽预测（按照均值）</span>
          <el-select v-model="windowMonths" size="small" class="runway__win" @change="loadRunway">
            <el-option :value="0" label="全部历史" />
            <el-option :value="3" label="最近 3 个月" />
            <el-option :value="6" label="最近 6 个月" />
            <el-option :value="12" label="最近 12 个月" />
          </el-select>
        </div>
      </template>

      <div class="runway__body">
        <el-progress
          type="dashboard"
          :percentage="runway.progress"
          :color="ringColor"
          :width="168"
          :stroke-width="12"
        >
          <template #default="{ percentage }">
            <div class="ring">
              <span class="ring__val" :style="{ color: ringColor }">{{ percentage }}%</span>
              <span class="ring__cap">未来 {{ runway.horizon_months }} 个月消耗</span>
            </div>
          </template>
        </el-progress>

        <div class="runway__stats">
          <div class="stat">
            <span class="stat__lb">账户总余额</span>
            <span class="stat__vl">¥{{ fmt(runway.balance) }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">月均收入 / 支出</span>
            <span class="stat__vl">
              <span class="c-income">¥{{ fmt(runway.monthly_income) }}</span>
              <span class="stat__sep">/</span>
              <span class="c-expense">¥{{ fmt(runway.monthly_expense) }}</span>
            </span>
          </div>
          <div class="stat">
            <span class="stat__lb">月均净流出</span>
            <span class="stat__vl" :style="{ color: ringColor }">¥{{ fmt(runway.monthly_net_outflow) }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">可支撑</span>
            <span class="stat__vl">{{ runwayText }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">预计耗尽时间</span>
            <span class="stat__vl" :style="{ color: ringColor }">{{ depletionText }}</span>
          </div>
        </div>
      </div>

      <div class="runway__msg">
        <el-tag :type="tagType" size="small" effect="dark">{{ statusText }}</el-tag>
        <span class="runway__tx">{{ runway.message }}</span>
      </div>
      <p class="runway__note">
        ※ 环形进度 = 按{{ windowLabel }}消耗速度，未来 {{ runway.horizon_months }} 个月将耗用的账户余额占比，越低越安全。
        消耗速度取「当前月度运行率」：固定收支按月计（年度固定 /12），临时收支在所选窗口内摊销，已终止的固定收支不计入。
      </p>
    </el-card>

    <!-- 资金消耗与耗尽预测（绝对值口径） -->
    <el-card class="outlook" shadow="hover" v-loading="outlookLoading">
      <template #header>
        <div class="outlook__hd">
          <span class="outlook__title">资金消耗与耗尽预测（按照绝对值）</span>
          <div class="outlook__pick">
            <el-radio-group v-model="quickMonths" size="small" @change="onQuickChange">
              <el-radio-button v-for="m in quickOptions" :key="m" :value="m">{{ m }} 个月</el-radio-button>
            </el-radio-group>
            <el-date-picker
              v-model="customTarget"
              type="month"
              size="small"
              value-format="YYYY-MM"
              placeholder="指定目标月份"
              class="outlook__dp"
              @change="onTargetChange"
            />
          </div>
        </div>
      </template>

      <div class="outlook__body">
        <el-progress
          type="dashboard"
          :percentage="ratioRing"
          :color="outlookColor"
          :width="168"
          :stroke-width="12"
        >
          <template #default>
            <div class="ring">
              <span class="ring__val" :style="{ color: outlookColor }">{{ ratioText }}</span>
              <span class="ring__cap">支出 / 收入</span>
            </div>
          </template>
        </el-progress>

        <el-progress
          type="dashboard"
          :percentage="netAssetRing"
          :color="netAssetColor"
          :width="150"
          :stroke-width="12"
        >
          <template #default>
            <div class="ring">
              <span class="ring__val" :style="{ color: netAssetColor }">{{ netAssetText }}</span>
              <span class="ring__cap">支出 / 净资产</span>
            </div>
          </template>
        </el-progress>

        <div class="outlook__stats">
          <div class="stat">
            <span class="stat__lb">截至 {{ outlook.target_month }} 累计收入</span>
            <span class="stat__vl c-income">¥{{ fmt(outlook.total_income) }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">截至 {{ outlook.target_month }} 累计支出</span>
            <span class="stat__vl c-expense">¥{{ fmt(outlook.total_expense) }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">支出占收入比例</span>
            <span class="stat__vl" :style="{ color: outlookColor }">{{ ratioText }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">净资产总额</span>
            <span class="stat__vl">¥{{ fmt(outlook.net_asset) }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">支出占净资产比例</span>
            <span class="stat__vl" :style="{ color: netAssetColor }">{{ netAssetText }}</span>
          </div>
          <div class="stat">
            <span class="stat__lb">累计净额</span>
            <span class="stat__vl" :style="{ color: outlook.net_amount >= 0 ? '#f56c6c' : '#67c23c' }">
              {{ outlook.net_amount >= 0 ? '+' : '-' }}¥{{ fmt(Math.abs(outlook.net_amount)) }}
            </span>
          </div>
          <div class="stat">
            <span class="stat__lb">当前余额 / 期末预计余额</span>
            <span class="stat__vl">
              ¥{{ fmt(outlook.opening_balance) }}
              <span class="stat__sep">→</span>
              <span :style="{ color: outlook.projected_balance < 0 ? '#f56c6c' : '#303133' }">
                ¥{{ fmt(outlook.projected_balance) }}
              </span>
            </span>
          </div>
          <div class="stat">
            <span class="stat__lb">预计余额转负月份</span>
            <span class="stat__vl" :style="{ color: outlook.depletion_month ? '#f56c6c' : '#303133' }">
              {{ outlook.depletion_month || '不会转负' }}
            </span>
          </div>
        </div>
      </div>

      <div class="outlook__msg">
        <el-tag :type="outlookTagType" size="small" effect="dark">{{ outlookStatusText }}</el-tag>
        <span class="outlook__tx">{{ outlook.message }}</span>
      </div>

      <div class="outlook__detail">
        <el-button link type="primary" size="small" @click="showMonthly = !showMonthly">
          {{ showMonthly ? '收起逐月明细' : '展开逐月明细' }}
        </el-button>
        <el-table
          v-if="showMonthly"
          :data="outlook.monthly"
          size="small"
          max-height="280"
          class="outlook__tb"
        >
          <el-table-column prop="month" label="月份" width="100" />
          <el-table-column label="收入" align="right">
            <template #default="{ row }"><span class="c-income">¥{{ fmt(row.income) }}</span></template>
          </el-table-column>
          <el-table-column label="支出" align="right">
            <template #default="{ row }"><span class="c-expense">¥{{ fmt(row.expense) }}</span></template>
          </el-table-column>
          <el-table-column label="净额" align="right">
            <template #default="{ row }">
              <span :style="{ color: row.net >= 0 ? '#f56c6c' : '#67c23c' }">
                {{ row.net >= 0 ? '+' : '-' }}¥{{ fmt(Math.abs(row.net)) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="月末预计余额" align="right">
            <template #default="{ row }">
              <span :style="{ color: row.balance < 0 ? '#f56c6c' : '#303133' }">¥{{ fmt(row.balance) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <p class="outlook__note">
        ※ 绝对值口径：不做摊销、不取均值，按收支管理里设置的真实金额逐月累加到所选时间点——
        固定收支按月计（年度固定只在发生月份计一次），临时收支在其发生月份一次性计入，已终止的固定收支不再计入。
        左环为「累计支出 / 累计收入」，右环为「累计支出 / 净资产总额」（净资产 = 当前账户余额合计 ¥{{ fmt(outlook.net_asset) }}，反映这段时间会花掉多少家底）。
        起点为当前账户余额 ¥{{ fmt(outlook.opening_balance) }}，{{ outlook.from_month }} 起算至 {{ outlook.target_month }}。
      </p>
    </el-card>

    <el-card class="tip" shadow="never">
      <template #header>欢迎使用家庭财务管理系统</template>
      <p>从左侧菜单开始管理你的账户、收支、分类与预算。</p>
      <p>数据接口前缀为 <code>/api/v1</code>，后端文档见 <code>http://127.0.0.1:8000/docs</code>。</p>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { getSummary, getFundRunway, getAbsoluteOutlook } from '@/api/summary'

const summary = reactive({
  total_balance: 0,
  total_income: 0,
  total_expense: 0,
  account_count: 0
})

const windowMonths = ref(6)
const runwayLoading = ref(false)
const runway = reactive({
  balance: 0,
  account_count: 0,
  window_months: 6,
  horizon_months: 12,
  monthly_income: 0,
  monthly_expense: 0,
  monthly_net_outflow: 0,
  runway_months: null,
  depletion_date: null,
  consumption_ratio: null,
  progress: 0,
  status: 'nodata',
  message: ''
})

// 统计窗口文案：0 表示全部历史，后端会回显实际跨度
const windowLabel = computed(() =>
  windowMonths.value === 0 ? `全部历史（${runway.window_months} 个月）` : `最近 ${runway.window_months} 个月`
)

async function loadRunway() {
  runwayLoading.value = true
  try {
    const data = await getFundRunway({ months: windowMonths.value })
    Object.assign(runway, data)
  } catch {
    /* request 拦截器已统一提示错误 */
  } finally {
    runwayLoading.value = false
  }
}

/* ---------- 资金消耗与耗尽预测（绝对值口径） ---------- */
const quickOptions = [3, 6, 12, 24, 36, 60]
const quickMonths = ref(12)
const customTarget = ref('')
const outlookMonths = ref(12)
const showMonthly = ref(false)
const outlookLoading = ref(false)
const outlook = reactive({
  opening_balance: 0,
  account_count: 0,
  months: 12,
  from_month: '',
  target_month: '',
  total_income: 0,
  total_expense: 0,
  net_amount: 0,
  expense_income_ratio: null,
  expense_income_percent: null,
  net_asset: 0,
  expense_net_asset_ratio: null,
  expense_net_asset_percent: null,
  projected_balance: 0,
  depletion_month: null,
  monthly: [],
  status: 'nodata',
  message: ''
})

// 目标月份 → 跨度（月），从当前月的下一月起算
function monthsFromTarget(target) {
  if (!target) return null
  const [y, m] = target.split('-').map(Number)
  const now = new Date()
  const diff = (y - now.getFullYear()) * 12 + (m - (now.getMonth() + 1))
  if (!Number.isFinite(diff)) return null
  return Math.min(Math.max(diff, 1), 120)
}

function onQuickChange(value) {
  customTarget.value = ''
  outlookMonths.value = value
  loadOutlook()
}

function onTargetChange(value) {
  if (!value) {
    quickMonths.value = null
    return
  }
  const n = monthsFromTarget(value)
  if (n == null) return
  quickMonths.value = quickOptions.includes(n) ? n : null
  outlookMonths.value = n
  loadOutlook()
}

async function loadOutlook() {
  outlookLoading.value = true
  try {
    const data = await getAbsoluteOutlook({ months: outlookMonths.value })
    Object.assign(outlook, data)
  } catch {
    /* request 拦截器已统一提示错误 */
  } finally {
    outlookLoading.value = false
  }
}

onMounted(async () => {
  const data = await getSummary()
  Object.assign(summary, data)
  await loadRunway()
  await loadOutlook()
})

const ringColor = computed(
  () =>
    ({
      surplus: '#67c23a',
      healthy: '#67c23a',
      warning: '#e6a23c',
      danger: '#f56c6c',
      nodata: '#909399'
    }[runway.status] || '#909399')
)

const tagType = computed(
  () =>
    ({
      surplus: 'success',
      healthy: 'success',
      warning: 'warning',
      danger: 'danger',
      nodata: 'info'
    }[runway.status] || 'info')
)

const statusText = computed(
  () =>
    ({
      surplus: '资金净流入',
      healthy: '健康',
      warning: '需关注',
      danger: '紧张',
      nodata: '数据不足'
    }[runway.status] || '数据不足')
)

const runwayText = computed(() => {
  if (runway.status === 'nodata') return '—'
  if (runway.runway_months == null) return '不会耗尽'
  return `${runway.runway_months} 个月`
})

const depletionText = computed(() => {
  if (runway.status === 'nodata') return '—'
  return runway.depletion_date || '不会耗尽'
})

const ratioText = computed(() =>
  outlook.expense_income_percent == null ? '—' : `${outlook.expense_income_percent}%`
)

// 环形最大 100%，超出部分用文案与颜色表达
const ratioRing = computed(() =>
  Math.min(100, Math.max(0, Number(outlook.expense_income_percent || 0)))
)

const netAssetText = computed(() =>
  outlook.expense_net_asset_percent == null ? '—' : `${outlook.expense_net_asset_percent}%`
)

const netAssetRing = computed(() =>
  Math.min(100, Math.max(0, Number(outlook.expense_net_asset_percent || 0)))
)

// 净资产被消耗的程度：<50% 安全，<80% 需关注，≥80% 紧张
const netAssetColor = computed(() => {
  const pct = Number(outlook.expense_net_asset_percent || 0)
  if (outlook.expense_net_asset_percent == null) return '#909399'
  return pct >= 80 ? '#f56c6c' : pct >= 50 ? '#e6a23c' : '#67c23a'
})

const outlookColor = computed(
  () =>
    ({
      healthy: '#67c23a',
      warning: '#e6a23c',
      danger: '#f56c6c',
      nodata: '#909399'
    }[outlook.status] || '#909399')
)

const outlookTagType = computed(
  () =>
    ({
      healthy: 'success',
      warning: 'warning',
      danger: 'danger',
      nodata: 'info'
    }[outlook.status] || 'info')
)

const outlookStatusText = computed(
  () =>
    ({
      healthy: '健康',
      warning: '需关注',
      danger: '入不敷出',
      nodata: '数据不足'
    }[outlook.status] || '数据不足')
)

const fmt = (value) =>
  value == null
    ? '0.00'
    : Number(value).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
</script>

<style scoped>
.runway {
  margin-top: 20px;
}
.runway__hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.runway__title {
  font-size: 16px;
  font-weight: 600;
}
.runway__win {
  width: 130px;
}
.runway__body {
  display: flex;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
}
.ring {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.ring__val {
  font-size: 26px;
  font-weight: 600;
  line-height: 1.1;
}
.ring__cap {
  font-size: 12px;
  color: #909399;
}
.runway__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(200px, 1fr));
  gap: 14px 28px;
  flex: 1;
  min-width: 280px;
}
.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.stat__lb {
  font-size: 12px;
  color: #909399;
}
.stat__vl {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
.stat__sep {
  margin: 0 6px;
  color: #c0c4cc;
  font-weight: 400;
}
.c-income {
  color: #f56c6c;
}
.c-expense {
  color: #67c23a;
}
.runway__msg {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #ebeef5;
}
.runway__tx {
  font-size: 14px;
  color: #606266;
}
.runway__note {
  margin: 10px 0 0;
  font-size: 12px;
  color: #a8abb2;
  line-height: 1.6;
}
.outlook {
  margin-top: 20px;
}
.outlook__hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}
.outlook__title {
  font-size: 16px;
  font-weight: 600;
}
.outlook__pick {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.outlook__dp {
  width: 150px;
}
.outlook__body {
  display: flex;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
}
.outlook__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(180px, 1fr));
  gap: 14px 28px;
  flex: 1;
  min-width: 300px;
}
.outlook__msg {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #ebeef5;
}
.outlook__tx {
  font-size: 14px;
  color: #606266;
}
.outlook__detail {
  margin-top: 12px;
}
.outlook__tb {
  margin-top: 10px;
  width: 100%;
}
.outlook__note {
  margin: 10px 0 0;
  font-size: 12px;
  color: #a8abb2;
  line-height: 1.6;
}
.tip {
  margin-top: 20px;
}
</style>
