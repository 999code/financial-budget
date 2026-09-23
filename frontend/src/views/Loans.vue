<template>
  <div class="loans">
    <!-- 搜索：名称 / 时间 / 金额范围 -->
    <search-form :schema="searchSchema" @search="load" @reset="onReset" />

    <div class="toolbar">
      <el-button type="primary" :icon="Plus" @click="openCreate">新增贷款</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border stripe>
      <el-table-column prop="name" label="名称" min-width="120" show-overflow-tooltip />
      <el-table-column label="总价" width="130" align="right">
        <template #default="{ row }">¥ {{ money(row.total_price) }}</template>
      </el-table-column>
      <el-table-column label="本金" width="130" align="right">
        <template #default="{ row }">¥ {{ money(row.principal) }}</template>
      </el-table-column>
      <el-table-column label="贷款金额" width="130" align="right">
        <template #default="{ row }">¥ {{ money(row.loan_amount) }}</template>
      </el-table-column>
      <el-table-column label="利率" width="90" align="right">
        <template #default="{ row }">{{ row.annual_rate }}%</template>
      </el-table-column>
      <el-table-column label="贷款年限" width="100" align="right">
        <template #default="{ row }">{{ row.years }} 年</template>
      </el-table-column>
      <el-table-column label="时间" width="120">
        <template #default="{ row }">{{ row.start_date || '-' }}</template>
      </el-table-column>
      <el-table-column label="月供" width="180" align="right">
        <template #default="{ row }">
          <span v-if="row.repayment_method === 'equal_principal'" class="loan-monthly">
            ¥ {{ money(row.monthly_payment) }} → ¥ {{ money(row.last_month_payment) }}
          </span>
          <span v-else>¥ {{ money(row.monthly_payment) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openView(row)">查看</el-button>
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
      <template #empty>
        <span class="empty-text">暂无贷款，点击「新增贷款」添加</span>
      </template>
    </el-table>

    <!-- 新增 / 编辑 -->
    <el-dialog v-model="visible" :title="editingId ? '编辑贷款' : '新增贷款'" width="520px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="110px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="如：住房贷款" />
        </el-form-item>
        <el-form-item label="总价">
          <el-input-number v-model="form.total_price" :min="0" :precision="2" :step="10000" style="width: 100%" />
        </el-form-item>
        <el-form-item label="本金（首付）">
          <el-input-number v-model="form.principal" :min="0" :precision="2" :step="10000" style="width: 100%" />
        </el-form-item>
        <el-form-item label="贷款金额" :error="loanAmountError">
          <el-input-number
            :model-value="loanAmount"
            :min="0"
            :precision="2"
            disabled
            style="width: 100%"
          />
          <div class="hint">自动计算：总价 − 本金（首付）</div>
        </el-form-item>
        <el-form-item label="年利率(%)">
          <el-input-number v-model="form.annual_rate" :min="0" :precision="2" :step="0.05" style="width: 100%" />
        </el-form-item>
        <el-form-item label="贷款年限(年)" prop="years">
          <el-input-number v-model="form.years" :min="1" :max="40" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="还款方式">
          <el-select v-model="form.repayment_method" style="width: 100%">
            <el-option label="等额本息（每月固定）" value="equal_installment" />
            <el-option label="等额本金（逐月递减）" value="equal_principal" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间">
          <el-date-picker
            v-model="form.start_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择贷款起始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.note" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>
        <el-form-item label="预计月供">
          <div class="preview">
            <template v-if="form.repayment_method === 'equal_principal'">
              首月 ¥ {{ money(preview.first) }} → 末月 ¥ {{ money(preview.last) }}
            </template>
            <template v-else>每月 ¥ {{ money(preview.first) }}</template>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 查看 -->
    <el-dialog v-model="viewVisible" title="贷款详情" width="560px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="名称">{{ viewRow.name }}</el-descriptions-item>
        <el-descriptions-item label="总价">¥ {{ money(viewRow.total_price) }}</el-descriptions-item>
        <el-descriptions-item label="本金（首付）">¥ {{ money(viewRow.principal) }}</el-descriptions-item>
        <el-descriptions-item label="贷款金额">¥ {{ money(viewRow.loan_amount) }}</el-descriptions-item>
        <el-descriptions-item label="年利率">{{ viewRow.annual_rate }}%</el-descriptions-item>
        <el-descriptions-item label="贷款年限">{{ viewRow.years }} 年（{{ months(viewRow.years) }} 期）</el-descriptions-item>
        <el-descriptions-item label="还款方式">{{ methodText(viewRow.repayment_method) }}</el-descriptions-item>
        <el-descriptions-item label="时间">{{ viewRow.start_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="月供">
          <template v-if="viewRow.repayment_method === 'equal_principal'">
            首月 ¥ {{ money(viewRow.monthly_payment) }} → 末月 ¥ {{ money(viewRow.last_month_payment) }}
          </template>
          <template v-else>¥ {{ money(viewRow.monthly_payment) }}</template>
        </el-descriptions-item>
        <el-descriptions-item label="最后一期还款日">{{ viewRow.end_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ viewRow.note || '-' }}</el-descriptions-item>
      </el-descriptions>
      <div class="sync-tip">
        月供已自动同步为固定收支中的一条支出（名称「{{ viewRow.name }}-月供」），随本条贷款联动更新。
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import SearchForm from '@/components/SearchForm.vue'
import { createLoan, deleteLoan, getLoans, updateLoan } from '@/api/loans'

const METHOD_TEXT = {
  equal_installment: '等额本息',
  equal_principal: '等额本金',
}

function money(v) {
  return Number(v || 0).toFixed(2)
}

/** 与后端一致的月供计算：年利率(%) → 月利率，年限(年) → 期数 */
function calcPayments(loanAmount, annualRate, years, method) {
  const months = Math.round(Number(years || 0) * 12)
  const amount = Number(loanAmount || 0)
  if (months <= 0 || amount <= 0) return { first: 0, last: 0 }
  const r = Number(annualRate || 0) / 100 / 12
  if (r <= 0) {
    const per = amount / months
    return { first: per, last: per }
  }
  if (method === 'equal_principal') {
    const perPrincipal = amount / months
    return {
      first: perPrincipal + amount * r,
      last: perPrincipal + (amount - perPrincipal * (months - 1)) * r,
    }
  }
  const factor = Math.pow(1 + r, months)
  const monthly = (amount * r * factor) / (factor - 1)
  return { first: monthly, last: monthly }
}

const list = ref([])
const loading = ref(false)
const visible = ref(false)
const viewVisible = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref()
const viewRow = ref({})

const emptyQuery = () => ({ name: '', date_range: null, amount_min: null, amount_max: null })
const query = reactive(emptyQuery())

const searchSchema = computed(() => ({
  colSpan: 6,
  labelPosition: 'top',
  gutter: 18,
  model: query,
  formItems: [
    { type: 'input.trim', label: '名称', field: 'name', placeholder: '请输入名称', clearable: true },
    {
      type: 'date-picker',
      subtype: 'daterange',
      label: '时间',
      field: 'date_range',
      valueFormat: 'YYYY-MM-DD',
      startPlaceholder: '开始日期',
      endPlaceholder: '结束日期',
      rangeSeparator: '至',
      unlinkPanels: true,
      style: 'width: 100%',
    },
    {
      label: '金额范围',
      items: [
        {
          type: 'input-number',
          field: 'amount_min',
          min: 0,
          precision: 2,
          step: 10000,
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
          step: 10000,
          controlsPosition: 'right',
          placeholder: '最大金额',
          style: 'flex: 1 1 0; min-width: 0;',
        },
      ],
    },
  ],
}))

const emptyForm = () => ({
  name: '',
  total_price: 0,
  principal: 0,
  annual_rate: 0,
  years: 30,
  repayment_method: 'equal_installment',
  start_date: '',
  note: '',
})
const form = reactive(emptyForm())

// 贷款金额 = 总价 - 本金（首付），派生值，不进表单模型（无法被编辑或写入）
const loanAmount = computed(() => {
  const diff = Number(form.total_price || 0) - Number(form.principal || 0)
  return diff > 0 ? Number(diff.toFixed(2)) : 0
})
// 提交过一次后才提示，贷款金额一大于 0 提示自动消失
const amountChecked = ref(false)
const loanAmountError = computed(() =>
  amountChecked.value && loanAmount.value <= 0
    ? '贷款金额必须大于 0，请检查总价与本金（首付）'
    : ''
)

const preview = computed(() =>
  calcPayments(loanAmount.value, form.annual_rate, form.years, form.repayment_method)
)

const rules = {
  name: [{ required: true, message: '请输入贷款名称', trigger: 'blur' }],
  years: [{ required: true, message: '请输入贷款年限', trigger: 'blur' }],
}

function months(years) {
  return Math.round(Number(years || 0) * 12)
}

function methodText(method) {
  return METHOD_TEXT[method] || method || '-'
}

function buildParams() {
  const params = {}
  if (query.name) params.name = query.name
  if (query.amount_min != null) params.amount_min = query.amount_min
  if (query.amount_max != null) params.amount_max = query.amount_max
  if (Array.isArray(query.date_range) && query.date_range.length === 2) {
    params.start_date = query.date_range[0]
    params.end_date = query.date_range[1]
  }
  return params
}

async function load() {
  loading.value = true
  try {
    list.value = await getLoans(buildParams())
  } finally {
    loading.value = false
  }
}

function onReset() {
  Object.assign(query, emptyQuery())
  load()
}

function openCreate() {
  editingId.value = null
  Object.assign(form, emptyForm())
  amountChecked.value = false
  visible.value = true
}

function openEdit(row) {
  editingId.value = row.id
  Object.assign(form, {
    name: row.name,
    total_price: row.total_price,
    principal: row.principal,
    annual_rate: row.annual_rate,
    years: row.years,
    repayment_method: row.repayment_method,
    start_date: row.start_date || '',
    note: row.note || '',
  })
  amountChecked.value = false
  visible.value = true
}

function openView(row) {
  viewRow.value = { ...row }
  viewVisible.value = true
}

async function submit() {
  await formRef.value.validate()
  const payload = {
    name: form.name,
    total_price: Number(form.total_price || 0),
    principal: Number(form.principal || 0),
    annual_rate: Number(form.annual_rate || 0),
    years: Number(form.years || 0),
    repayment_method: form.repayment_method,
    start_date: form.start_date || null,
    note: form.note || null,
  }
  if (loanAmount.value <= 0) {
    amountChecked.value = true
    return
  }
  amountChecked.value = false
  submitting.value = true
  try {
    if (editingId.value) {
      await updateLoan(editingId.value, payload)
      ElMessage.success('已更新，月供已同步')
    } else {
      await createLoan(payload)
      ElMessage.success('已创建，月供已同步到固定收支')
    }
    visible.value = false
    load()
  } finally {
    submitting.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(
    `确认删除贷款「${row.name}」？同步生成的月供收支也会一并删除。`,
    '提示',
    { type: 'warning' }
  )
  await deleteLoan(row.id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}

.hint {
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
  line-height: 1.4;
}

.preview {
  width: 100%;
  color: #409eff;
  font-weight: 600;
}

.empty-text {
  color: #909399;
}

.loan-monthly {
  color: #e6a23c;
}

.sync-tip {
  margin-top: 12px;
  padding: 10px 12px;
  background: #f4f4f5;
  border-radius: 4px;
  color: #606266;
  font-size: 12px;
  line-height: 1.6;
}
</style>
