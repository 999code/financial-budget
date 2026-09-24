<template>
  <div class="income-expense">
    <el-tabs v-model="activeTab" class="ie-tabs">
      <el-tab-pane
        v-for="t in tabs"
        :key="t.name"
        :name="t.name"
        :label="t.label"
        lazy
      >
        <!-- 搜索：名称 / 分类 / 金额区间 / 时间区间 -->
        <el-card>
          <search-form
            :schema="searchSchemaOf(t.name)"
            :collapsed-count="3"
            @search="load(t.name)"
            @reset="onReset(t.name)"
          />
        </el-card>
        <el-card style="margin-top: 30px;">

          <div class="toolbar">
            <el-button type="primary" :icon="Plus" @click="openCreate(t.name)">
              新增{{ t.label }}
            </el-button>
            <el-tooltip content="刷新列表" placement="top">
              <el-button
                :icon="Refresh"
                :loading="state[t.name].loading"
                @click="load(t.name)"
              />
            </el-tooltip>
          </div>
          <!-- 列表：名称 / 分类 / 金额 / 周期 / 时间 / 操作 -->
          <sc-table :schema="tableSchemaOf(t.name)" v-loading="state[t.name].loading" />
        </el-card>

      </el-tab-pane>
    </el-tabs>

    <!-- 新增 / 编辑 弹窗（sc-form） -->
    <el-dialog
      v-model="editVisible"
      :title="editingId ? '编辑收支' : '新增收支'"
      width="480px"
      @closed="onDialogClosed"
    >
      <sc-form ref="dialogFormRef" :schema="dialogSchema" />
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 查看 弹窗 -->
    <el-dialog v-model="viewVisible" title="收支详情" width="760px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="名称">{{ viewRow.name }}</el-descriptions-item>
        <el-descriptions-item label="分类">
          <el-tag :type="viewRow.category === 'income' ? 'success' : 'danger'" size="small">
            {{ categoryText(viewRow.category) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="银行账户">
          {{ viewRow.account_name || '未指定' }}
        </el-descriptions-item>
        <el-descriptions-item label="金额">
          ¥{{ viewRow.amount != null ? Number(viewRow.amount).toFixed(2) : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="周期" v-if="viewRow.kind === 'fixed'">
          {{ periodText(viewRow.period) }}
        </el-descriptions-item>
        <el-descriptions-item label="终止时间" v-if="viewRow.kind === 'fixed'">
          {{ viewRow.end_date ? viewRow.end_date.slice(0, 10) : '持续中' }}
        </el-descriptions-item>
        <el-descriptions-item label="类型">
          {{ viewRow.kind === 'fixed' ? '固定收支' : '临时收支' }}
        </el-descriptions-item>
        <el-descriptions-item label="时间">{{ formatTime(viewRow.occurred_at) }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ viewRow.note || '-' }}</el-descriptions-item>
      </el-descriptions>

      <!-- 固定收支：按周期展开的明细列表（时间 / 金额 / 操作） -->
      <div v-if="viewRow.kind === 'fixed'" class="ie-details">
        <div class="ie-details__header">
          <span class="ie-details__title">收支明细</span>
          <span class="ie-details__sum" :style="detailSumStyle">
            合计 {{ viewRow.category === 'income' ? '+' : '-' }}¥{{ detailTotalText }}
          </span>
        </div>
        <el-table :data="details" v-loading="detailsLoading" size="small" border max-height="320">
          <el-table-column prop="period_date" label="时间" min-width="140" />
          <el-table-column prop="amount" label="金额" width="150" align="center">
            <template #default="{ row }">¥{{ Number(row.amount).toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="openDetailEdit(row)">
                编辑
              </el-button>
              <el-button link type="danger" size="small" @click="removeDetail(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
          <template #empty>暂无明细</template>
        </el-table>
      </div>
    </el-dialog>

    <!-- 明细编辑 弹窗（嵌套在详情弹窗之上） -->
    <el-dialog v-model="detailEditVisible" title="编辑明细" width="420px" append-to-body>
      <el-form :model="detailForm" label-width="70px">
        <el-form-item label="时间">
          <el-date-picker
            v-model="detailForm.period_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="请选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="金额">
          <el-input-number
            v-model="detailForm.amount"
            :min="0"
            :precision="2"
            :step="10"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="detailEditVisible = false">取消</el-button>
        <el-button type="primary" :loading="detailSaving" @click="saveDetail">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, h, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import SearchForm from '@/components/SearchForm.vue'
import { getAccounts } from '@/api/accounts'
import {
  createIncomeExpense,
  deleteIncomeExpense,
  deleteIncomeExpenseDetail,
  getIncomeExpenseDetails,
  getIncomeExpenses,
  updateIncomeExpense,
  updateIncomeExpenseDetail,
} from '@/api/incomeExpense'

defineOptions({ name: 'IncomeExpense' })

const route = useRoute()

const tabs = [
  { name: 'fixed', label: '固定收支' },
  { name: 'temp', label: '临时收支' },
]

// 银行账户（来自账户管理），用于筛选与表单选择；加载失败不阻塞页面
const accounts = ref([])
const accountOptions = computed(() =>
  accounts.value.map((a) => ({ label: a.name, value: a.id })),
)
async function loadAccounts() {
  try {
    accounts.value = await getAccounts()
  } catch {
    accounts.value = []
  }
}

// 单元格模板是拼出来的字符串，账户名是用户输入，需要做转义再拼接
function escapeHtml(text) {
  return String(text ?? '').replace(/[&<>"']/g, (ch) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]
  ))
}

// 收支分类：收入 / 支出（沿用项目内的展示约定：收入绿、支出红）
const CATEGORY_OPTIONS = [
  { label: '收入', value: 'income' },
  { label: '支出', value: 'expense' },
]
function categoryText(category) {
  return category === 'income' ? '收入' : '支出'
}
function categoryTagType(category) {
  return category === 'income' ? 'success' : 'danger'
}

// 固定收支的周期：每月 / 每年
const PERIOD_OPTIONS = [
  { label: '每月', value: 'monthly' },
  { label: '每年', value: 'yearly' },
]
function periodText(period) {
  if (period === 'yearly') return '每年'
  if (period === 'monthly') return '每月'
  return '-' // 历史数据还没有周期
}

// 每个 tab 独立的列表、查询条件与加载状态
const emptyQuery = () => ({
  name: '',
  category: '',
  account_id: '',
  amount_min: null,
  amount_max: null,
  date_range: null, // [开始日期, 结束日期]
})
const state = reactive({
  fixed: { list: [], loading: false, query: emptyQuery() },
  temp: { list: [], loading: false, query: emptyQuery() },
})

const activeTab = ref('fixed')

// 金额区间：[最小金额] 至 [最大金额]，合并为一个表单项
const amountRangeItem = () => ({
  label: '金额',
  items: [
    {
      type: 'input-number',
      field: 'amount_min',
      min: 0,
      precision: 2,
      step: 10,
      controlsPosition: 'right',
      placeholder: '最小金额',
      style: 'flex: 1 1 0; min-width: 0;',
    },
    { type: 'text', content: '至', style: 'flex: 0 0 auto; padding: 0 8px; color: #909399;' },
    {
      type: 'input-number',
      field: 'amount_max',
      min: 0,
      precision: 2,
      step: 10,
      controlsPosition: 'right',
      placeholder: '最大金额',
      style: 'flex: 1 1 0; min-width: 0;',
    },
  ],
})

// ---- 搜索表单 schema（SearchForm） ----
function buildSearchSchema(kind) {
  return {
    colSpan: 6,
    labelPosition: 'top',
    gutter: 18,
    model: state[kind].query,
    formItems: [
      { type: 'input.trim', label: '名称', field: 'name', placeholder: '请输入名称', clearable: true },
      {
        type: 'select',
        label: '分类',
        field: 'category',
        options: [{ label: '全部', value: '' }, ...CATEGORY_OPTIONS],
        placeholder: '全部分类',
        clearable: true,
        style: 'width: 100%',
      },
      {
        type: 'select',
        label: '银行账户',
        field: 'account_id',
        options: [{ label: '全部', value: '' }, ...accountOptions.value],
        placeholder: '全部账户',
        clearable: true,
        style: 'width: 100%',
      },
      amountRangeItem(),
      {
        type: 'date-picker',
        subtype: 'daterange', // el-date-picker type="daterange"
        label: '时间',
        field: 'date_range',
        valueFormat: 'YYYY-MM-DD',
        startPlaceholder: '开始日期',
        endPlaceholder: '结束日期',
        rangeSeparator: '至',
        unlinkPanels: true,
        style: 'width: 100%',
      },
    ],
  }
}
const searchSchemaFixed = computed(() => buildSearchSchema('fixed'))
const searchSchemaTemp = computed(() => buildSearchSchema('temp'))
function searchSchemaOf(kind) {
  return kind === 'fixed' ? searchSchemaFixed.value : searchSchemaTemp.value
}

// ---- 表格操作列所需的绑定方法（供 sc-table 运行时模板调用） ----
const schemaBind = {
  onView(row) {
    openView(row)
  },
  onEdit(row) {
    openEdit(row)
  },
  onDelete(row) {
    remove(row)
  },
  formatTime(ts) {
    return formatTime(ts)
  },
  periodText(period) {
    return periodText(period)
  },
  categoryTagType(category) {
    return categoryTagType(category)
  },
  escapeHtml(text) {
    return escapeHtml(text)
  },
  // 总金额 / 今年总金额：收入显示 +（红），支出显示 -（绿）
  totalAmountText(row) {
    return signedAmount(row, row.total_amount)
  },
  yearTotalAmountText(row) {
    return signedAmount(row, row.year_total_amount)
  },
}

// 带符号与配色的金额文本（沿用项目约定：收入 +红、支出 -绿）
function moneyText(value) {
  return '¥' + Number(value || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}
function signedAmount(row, value) {
  const sign = row.category === 'income' ? '+' : '-'
  const color = row.category === 'income' ? '#f56c6c' : '#67c23a'
  return (
    '<span style="font-weight:600;color:' + color + '">' + sign + moneyText(value) + '</span>'
  )
}

// ---- 合计行：总金额 / 今年总金额 按列汇总为净额（收入 − 支出，带符号） ----
function netAmount(data, field) {
  let income = 0
  let expense = 0
  for (const row of data || []) {
    const value = Number(row[field] || 0)
    if (row.category === 'income') income += value
    else expense += value
  }
  const net = income - expense
  const color = net >= 0 ? '#f56c6c' : '#67c23a'
  const sign = net >= 0 ? '+' : '-'
  return h(
    'span',
    { style: 'font-weight:600;color:' + color },
    sign + moneyText(Math.abs(net)),
  )
}

// fields 指定哪些列要出净额（固定收支：总金额 / 今年总金额；临时收支：金额）
function makeSummaryMethod(fields) {
  return ({ columns, data }) => {
    const fieldOfIndex = new Map(
      fields.map((field) => [columns.findIndex((column) => column.property === field), field]),
    )
    return columns.map((column, index) => {
      if (index === 0) return h('span', { style: 'font-weight:600' }, '合计')
      const field = fieldOfIndex.get(index)
      return field ? netAmount(data, field) : ''
    })
  }
}

const summaryFixed = makeSummaryMethod(['total_amount', 'year_total_amount'])
const summaryTemp = makeSummaryMethod(['amount'])

// ---- 表格 schema（sc-table） ----
// 列定义与列表数据无关，必须在 computed 之外只构建一次：
// 若每次 data 变化都重建 columns（连 template 函数都是新引用），el-table 会重新注册列
// 并重新计算列宽，布局中间态会让单元格内容换行、行高从 40.5 撑到 64，
// 表现为「刷新后表格抖动」。列定义保持稳定后，刷新只更新行数据，不再重排。
function buildColumns(kind) {
  const columns = [
    { prop: 'name', label: '名称', minWidth: '160', align: 'left' },
    {
      prop: 'category',
      label: '分类',
      width: '90',
      template(scope) {
        const type = schemaBind.categoryTagType(scope.row.category)
        const text = scope.row.category === 'income' ? '收入' : '支出'
        return '<el-tag type="' + type + '" size="small">' + text + '</el-tag>'
      },
    },
    {
      prop: 'account_name',
      label: '银行账户',
      width: '130',
      template(scope) {
        return scope.row.account_name
          ? '<span>' + schemaBind.escapeHtml(scope.row.account_name) + '</span>'
          : '<span style="color:#909399">未指定</span>'
      },
    },
    {
      prop: 'amount',
      label: '金额',
      width: '140',
      sortable: true,
      template(scope) {
        const v = scope.row.amount
        return '<span style="font-weight:600">¥' + (v != null ? Number(v).toFixed(2) : '-') + '</span>'
      },
    },
  ]

  // 固定收支多一列「周期」：每月 / 每年
  if (kind === 'fixed') {
    columns.push({
      prop: 'period',
      label: '周期',
      width: '100',
      template(scope) {
        return '<span>' + schemaBind.periodText(scope.row.period) + '</span>'
      },
    })
    // 终止时间：留空表示一直持续
    columns.push({
      prop: 'end_date',
      label: '终止时间',
      width: '130',
      template(scope) {
        return '<span>' + (scope.row.end_date ? scope.row.end_date.slice(0, 10) : '持续中') + '</span>'
      },
    })
    // 总金额 = 详情里各期明细的合计（后端聚合，收入/支出分别以 + / - 展示）
    columns.push({
      prop: 'total_amount',
      label: '总金额',
      width: '150',
      sortable: true,
      template(scope) {
        return schemaBind.totalAmountText(scope.row)
      },
    })
    // 今年总金额 = 只统计 period_date 在 1/1 ~ 今天 之间的期次
    columns.push({
      prop: 'year_total_amount',
      label: '今年总金额',
      width: '150',
      sortable: true,
      template(scope) {
        return schemaBind.yearTotalAmountText(scope.row)
      },
    })
  }

  columns.push(
    {
      prop: 'occurred_at',
      label: '创建时间',
      width: '180',
      template(scope) {
        return '<span>' + schemaBind.formatTime(scope.row.occurred_at) + '</span>'
      },
    },
    {
      prop: 'operate',
      label: '操作',
      width: '200',
      fixed: 'right',
      template(scope) {
        return `
          <el-button link type="primary" size="small" @click="bind.onView(scope.row)">查看</el-button>
          <el-button link type="primary" size="small" @click="bind.onEdit(scope.row)">编辑</el-button>
          <el-button link type="danger" size="small" @click="bind.onDelete(scope.row)">删除</el-button>
        `
      },
    },
  )

  return columns;
}

const columnsFixed = buildColumns('fixed')
const columnsTemp = buildColumns('temp')

function buildTableSchema(kind) {
  return {
    bind: schemaBind,
    data: state[kind].list,
    height: 'auto',
    columns: kind === 'fixed' ? columnsFixed : columnsTemp,
    // 合计行：固定收支汇总总金额与今年总金额，临时收支汇总金额（均为净额）
    showSummary: true,
    summaryMethod: kind === 'fixed' ? summaryFixed : summaryTemp,
  }
}
const tableSchemaFixed = computed(() => buildTableSchema('fixed'))
const tableSchemaTemp = computed(() => buildTableSchema('temp'))
function tableSchemaOf(kind) {
  return kind === 'fixed' ? tableSchemaFixed.value : tableSchemaTemp.value
}

// ---- 新增 / 编辑 弹窗 ----
const editVisible = ref(false)
const submitting = ref(false)
const editingId = ref(null)
const editingKind = ref('fixed')
const dialogFormRef = ref(null)
const form = reactive({
  name: '',
  category: 'expense',
  amount: undefined,
  period: 'monthly',
  occurred_at: '',
  end_date: '',
  account_id: null,
  note: '',
})

const dialogSchema = computed(() => ({
  model: form,
  colSpan: 24,
  labelPosition: 'top',
  formItems: [
    {
      type: 'input',
      label: '名称',
      field: 'name',
      placeholder: '请输入收支名称',
      rules: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    },
    {
      type: 'select',
      label: '分类',
      field: 'category',
      options: CATEGORY_OPTIONS,
      placeholder: '请选择分类',
      style: 'width: 100%',
      rules: [{ required: true, message: '请选择分类', trigger: 'change' }],
    },
    {
      type: 'input-number',
      label: '金额',
      field: 'amount',
      min: 0,
      precision: 2,
      step: 10,
      style: 'width: 100%',
      rules: [{ required: true, message: '请输入金额', trigger: 'change' }],
    },
    // 周期仅在「固定收支」下出现，临时收支不展示
    {
      type: 'select',
      label: '银行账户',
      field: 'account_id',
      options: accountOptions.value,
      placeholder: '留空表示未指定',
      clearable: true,
      style: 'width: 100%',
    },
    {
      type: 'select',
      label: '周期',
      field: 'period',
      options: PERIOD_OPTIONS,
      placeholder: '请选择周期',
      style: 'width: 100%',
      show: editingKind.value === 'fixed',
      rules: [{ required: true, message: '请选择周期', trigger: 'change' }],
    },
    // 终止时间仅在「固定收支」下出现：留空表示一直持续
    {
      type: 'date-picker',
      label: '终止时间',
      field: 'end_date',
      valueFormat: 'YYYY-MM-DD',
      placeholder: '留空表示一直持续',
      style: 'width: 100%',
      show: editingKind.value === 'fixed',
    },
    {
      type: 'date-picker',
      label: '时间',
      field: 'occurred_at',
      valueFormat: 'YYYY-MM-DD',
      placeholder: '请选择时间',
      rules: [{ required: true, message: '请选择时间', trigger: 'change' }],
    },
  ],
}))

function todayStr() {
  const d = new Date()
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
}

function openCreate(kind) {
  editingId.value = null
  editingKind.value = kind
  Object.assign(form, {
    name: '',
    category: 'expense',
    amount: undefined,
    period: 'monthly',
    occurred_at: todayStr(),
    end_date: '',
    account_id: null,
    note: '',
  })
  editVisible.value = true
}

function openEdit(row) {
  editingId.value = row.id
  editingKind.value = row.kind
  Object.assign(form, {
    name: row.name,
    category: row.category || 'expense',
    amount: row.amount,
    period: row.period || 'monthly',
    occurred_at: (row.occurred_at || '').slice(0, 10),
    end_date: (row.end_date || '').slice(0, 10),
    account_id: row.account_id ?? null,
    note: row.note || '',
  })
  editVisible.value = true
}

function onDialogClosed() {
  dialogFormRef.value?.elForm?.clearValidate?.()
}

// sc-form 暴露的 elForm 可能是实例也可能是 computed ref，这里兼容两种
async function validateForm() {
  const ef = dialogFormRef.value?.elForm
  if (!ef) return true
  const inst = typeof ef.validate === 'function' ? ef : ef.value
  if (!inst || typeof inst.validate !== 'function') return true
  try {
    await inst.validate()
    return true
  } catch {
    return false
  }
}

async function submit() {
  const ok = await validateForm()
  if (!ok) return
  const payload = {
    name: form.name,
    amount: Number(form.amount),
    kind: editingKind.value,
    category: form.category,
    period: editingKind.value === 'fixed' ? form.period : null,
    end_date: editingKind.value === 'fixed' && form.end_date ? `${form.end_date} 00:00:00` : null,
    occurred_at: form.occurred_at ? `${form.occurred_at} 00:00:00` : null,
    account_id: form.account_id ?? null, // 选填：null 表示未指定账户
    note: form.note || null,
  }
  submitting.value = true
  try {
    if (editingId.value) {
      await updateIncomeExpense(editingId.value, payload)
      ElMessage.success('已更新')
    } else {
      await createIncomeExpense(payload)
      ElMessage.success('已添加')
    }
    editVisible.value = false
    load(editingKind.value)
  } finally {
    submitting.value = false
  }
}

// ---- 查看 弹窗 ----
const viewVisible = ref(false)
const viewRow = reactive({ id: null, name: '', amount: null, kind: '', occurred_at: '', note: '', account_name: '' })

// 固定收支的按期明细：后端按周期从创建时间自动展开，编辑/删除直接入库
const details = ref([])
const detailsLoading = ref(false)
const detailTotalText = computed(() =>
  details.value
    .reduce((sum, row) => sum + Number(row.amount || 0), 0)
    .toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
)
const detailSumStyle = computed(() => ({
  color: viewRow.category === 'income' ? '#f56c6c' : '#67c23a',
}))
async function loadDetails(recordId) {
  if (!recordId) return
  detailsLoading.value = true
  try {
    details.value = await getIncomeExpenseDetails(recordId)
  } finally {
    detailsLoading.value = false
  }
}

function openView(row) {
  Object.assign(viewRow, row)
  viewVisible.value = true
  details.value = []
  if (row.kind === 'fixed') loadDetails(row.id)
}

// 明细编辑 / 删除
const detailEditVisible = ref(false)
const detailSaving = ref(false)
const detailForm = reactive({ id: null, period_date: '', amount: 0 })

function openDetailEdit(row) {
  Object.assign(detailForm, { id: row.id, period_date: row.period_date, amount: Number(row.amount) })
  detailEditVisible.value = true
}

async function saveDetail() {
  if (!detailForm.period_date) {
    ElMessage.warning('请选择时间')
    return
  }
  detailSaving.value = true
  try {
    await updateIncomeExpenseDetail(detailForm.id, {
      period_date: detailForm.period_date,
      amount: Number(detailForm.amount),
    })
    ElMessage.success('已更新')
    detailEditVisible.value = false
    await loadDetails(viewRow.id)
  } finally {
    detailSaving.value = false
  }
}

async function removeDetail(row) {
  await ElMessageBox.confirm(`确认删除 ${row.period_date} 这一期？`, '提示', { type: 'warning' })
  await deleteIncomeExpenseDetail(row.id)
  ElMessage.success('已删除')
  await loadDetails(viewRow.id)
}

// ---- 删除 ----
async function remove(row) {
  await ElMessageBox.confirm(`确认删除「${row.name}」？`, '提示', { type: 'warning' })
  await deleteIncomeExpense(row.id)
  ElMessage.success('已删除')
  load(row.kind)
}

// ---- 加载 / 搜索 / 重置 ----
async function load(kind) {
  state[kind].loading = true
  try {
    const q = state[kind].query
    const params = { kind }
    if (q.name) params.name = q.name
    if (q.category) params.category = q.category
    if (q.account_id !== '' && q.account_id != null) params.account_id = q.account_id
    if (q.amount_min != null && q.amount_min !== '') params.amount_min = q.amount_min
    if (q.amount_max != null && q.amount_max !== '') params.amount_max = q.amount_max
    const [startDate, endDate] = Array.isArray(q.date_range) ? q.date_range : []
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate
    state[kind].list = await getIncomeExpenses(params)
  } finally {
    state[kind].loading = false
  }
}

function onReset(kind) {
  Object.assign(state[kind].query, emptyQuery())
  load(kind)
}

function formatTime(ts) {
  if (!ts) return '-'
  return String(ts).replace('T', ' ').slice(0, 16)
}

// 从账户管理页「查看」跳转过来时带上 ?account=<id>，两个 tab 都按该账户筛选
function applyAccountFromRoute(value) {
  if (value === undefined || value === null || value === '') return
  const id = Number(value)
  if (!id) return
  state.fixed.query.account_id = id
  state.temp.query.account_id = id
}

onMounted(() => {
  loadAccounts()
  applyAccountFromRoute(route.query.account)
  load('fixed')
  load('temp')
})

// 已在收支页时再次从账户页跳转（路由参数变化），同样应用筛选
watch(
  () => route.query.account,
  (value) => {
    applyAccountFromRoute(value)
    load('fixed')
    load('temp')
  },
)
</script>

<style scoped>
.ie-tabs :deep(.el-tabs__content) {
  padding-top: 16px;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 16px 0 12px;
}
.ie-details {
  margin-top: 18px;
}
.ie-details__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.ie-details__title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}
.ie-details__sum {
  font-size: 13px;
  font-weight: 600;
}
</style>
