<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" :icon="Plus" @click="openCreate">新增账户</el-button>
      <el-tooltip content="刷新列表" placement="top">
        <el-button :icon="Refresh" :loading="loading" @click="load" />
      </el-tooltip>
    </div>

    <el-table
      ref="tableRef"
      :data="list"
      v-loading="loading"
      border
      stripe
      row-key="id"
      @expand-change="onExpandChange"
    >
      <el-table-column type="expand">
        <template #default="{ row }">
          <div class="flow" v-loading="flowLoading[row.id]">
            <template v-if="flow[row.id]">
              <div class="flow__summary">
                <span>期初 ¥{{ money(flow[row.id].initial_balance) }}</span>
                <span class="flow__op">+</span>
                <span class="flow__income">收入 ¥{{ money(flow[row.id].income_total) }}</span>
                <span class="flow__op">−</span>
                <span class="flow__expense">支出 ¥{{ money(flow[row.id].expense_total) }}</span>
                <span class="flow__op">=</span>
                <span class="flow__balance">余额 ¥{{ money(flow[row.id].balance) }}</span>
              </div>
              <el-table :data="flow[row.id].items" size="small" border max-height="300">
                <el-table-column prop="date" label="时间" width="120" />
                <el-table-column prop="name" label="名称" min-width="140" />
                <el-table-column label="类型" width="90" align="center">
                  <template #default="{ row: item }">
                    {{ item.kind === 'fixed' ? '固定' : '临时' }}
                  </template>
                </el-table-column>
                <el-table-column label="分类" width="80" align="center">
                  <template #default="{ row: item }">
                    <el-tag
                      :type="item.category === 'income' ? 'success' : 'danger'"
                      size="small"
                    >
                      {{ item.category === 'income' ? '收入' : '支出' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="周期" width="80" align="center">
                  <template #default="{ row: item }">
                    {{ item.kind === 'fixed' ? periodText(item.period) : '-' }}
                  </template>
                </el-table-column>
                <el-table-column label="金额" width="130" align="center">
                  <template #default="{ row: item }">
                    <span :style="amountStyle(item)">
                      {{ item.signed_amount >= 0 ? '+' : '-' }}¥{{ money(Math.abs(item.signed_amount)) }}
                    </span>
                  </template>
                </el-table-column>
                <template #empty>该账户还没有关联收支</template>
              </el-table>
            </template>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="账户名称" />
      <el-table-column label="类型" width="120">
        <template #default="{ row }">{{ typeLabel[row.type] || row.type }}</template>
      </el-table-column>
      <el-table-column label="期初余额" width="130">
        <template #default="{ row }">¥ {{ money(row.initial_balance) }}</template>
      </el-table-column>
      <el-table-column label="余额" width="150">
        <template #default="{ row }">
          <el-tooltip content="期初余额 + 收入 − 支出（由收支管理自动汇总）" placement="top">
            <span class="balance">¥ {{ money(row.balance) }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="currency" label="币种" width="90" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="viewIncomeExpense(row)">查看</el-button>
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="visible" :title="editingId ? '编辑账户' : '新增账户'" width="460px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="如：招商银行卡" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" style="width: 100%">
            <el-option v-for="(v, k) in typeLabel" :key="k" :label="v" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="期初余额" prop="initial_balance">
          <el-input-number
            v-model="form.initial_balance"
            :min="0"
            :precision="2"
            :step="100"
            style="width: 100%"
          />
          <div class="hint">当前余额由「期初余额 + 收入 − 支出」自动算出，无需手工填写</div>
        </el-form-item>
        <el-form-item label="币种">
          <el-input v-model="form.currency" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import {
  createAccount,
  deleteAccount,
  getAccountIncomeExpenses,
  getAccounts,
  updateAccount,
} from '@/api/accounts'

const router = useRouter()
const typeLabel = { cash: '现金', bank: '银行卡', creditcard: '信用卡', investment: '投资账户' }
const periodMap = { monthly: '每月', yearly: '每年' }

const list = ref([])
const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const formRef = ref()

// 展开行：每个账户的收支流水按需加载
const flow = ref({})
const flowLoading = reactive({})
const expandedIds = new Set() // 记录哪些行处于展开态，刷新后重新取这几行

const emptyForm = { name: '', type: 'cash', initial_balance: 0, currency: 'CNY' }
const form = reactive({ ...emptyForm })
const rules = {
  name: [{ required: true, message: '请输入账户名称', trigger: 'blur' }],
}

function money(value) {
  return Number(value || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}
function periodText(period) {
  return periodMap[period] || '-'
}
// 沿用项目约定：收入红、支出绿
function amountStyle(item) {
  const color = item.signed_amount >= 0 ? '#f56c6c' : '#67c23a'
  return { fontWeight: 600, color }
}

async function load() {
  loading.value = true
  try {
    list.value = await getAccounts()
    flow.value = {} // 余额可能变了，已展开的流水需要重新取
    for (const id of expandedIds) await fetchFlow(id)
  } finally {
    loading.value = false
  }
}

async function fetchFlow(accountId) {
  flowLoading[accountId] = true
  try {
    const summary = await getAccountIncomeExpenses(accountId)
    flow.value = { ...flow.value, [accountId]: summary }
  } finally {
    flowLoading[accountId] = false
  }
}

async function onExpandChange(row, expandedRows) {
  const expanded = Array.isArray(expandedRows)
    ? expandedRows.some((r) => r.id === row.id)
    : true
  if (expanded) expandedIds.add(row.id)
  else expandedIds.delete(row.id)
  if (!expanded || flow.value[row.id]) return
  await fetchFlow(row.id)
}

function viewIncomeExpense(row) {
  router.push({ path: '/income-expense', query: { account: row.id } })
}

function openCreate() {
  editingId.value = null
  Object.assign(form, emptyForm)
  visible.value = true
}

function openEdit(row) {
  editingId.value = row.id
  Object.assign(form, {
    name: row.name,
    type: row.type,
    initial_balance: row.initial_balance ?? 0,
    currency: row.currency,
  })
  visible.value = true
}

async function submit() {
  await formRef.value.validate()
  if (editingId.value) {
    await updateAccount(editingId.value, { ...form })
    ElMessage.success('已更新')
  } else {
    await createAccount({ ...form })
    ElMessage.success('已创建')
  }
  visible.value = false
  load()
}

async function remove(row) {
  await ElMessageBox.confirm(
    `确认删除账户「${row.name}」？关联的收支会保留，但会变成「未指定」账户。`,
    '提示',
    { type: 'warning' },
  )
  await deleteAccount(row.id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.flow {
  padding: 12px 16px;
  min-height: 60px;
}
.flow__summary {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #606266;
}
.flow__op {
  color: #909399;
}
.flow__income {
  color: #f56c6c;
  font-weight: 600;
}
.flow__expense {
  color: #67c23a;
  font-weight: 600;
}
.flow__balance {
  font-weight: 600;
  color: #303133;
}
.balance {
  font-weight: 600;
}
.hint {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}
</style>
