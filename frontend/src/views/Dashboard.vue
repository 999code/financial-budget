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
          <span class="runway__title">资金消耗与耗尽预测</span>
          <el-select v-model="windowMonths" size="small" class="runway__win" @change="loadRunway">
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
        ※ 环形进度 = 按当前消耗速度，未来 {{ runway.horizon_months }} 个月将耗用的账户余额占比，越低越安全。
        消耗速度取「当前月度运行率」：固定收支按月计（年度固定 /12），临时收支在所选窗口内摊销，已终止的固定收支不计入。
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
import { getSummary, getFundRunway } from '@/api/summary'

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

onMounted(async () => {
  const data = await getSummary()
  Object.assign(summary, data)
  await loadRunway()
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
.tip {
  margin-top: 20px;
}
</style>
