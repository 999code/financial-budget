<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" :icon="Plus" @click="openCreate">新增账户</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="账户名称" />
      <el-table-column label="类型" width="120">
        <template #default="{ row }">{{ typeLabel[row.type] || row.type }}</template>
      </el-table-column>
      <el-table-column label="余额" width="140">
        <template #default="{ row }">¥ {{ row.balance?.toFixed(2) }}</template>
      </el-table-column>
      <el-table-column prop="currency" label="币种" width="90" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
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
        <el-form-item label="余额" prop="balance">
          <el-input-number v-model="form.balance" :min="0" :precision="2" :step="100" style="width: 100%" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { createAccount, deleteAccount, getAccounts, updateAccount } from '@/api/accounts'

const typeLabel = { cash: '现金', bank: '银行卡', creditcard: '信用卡', investment: '投资账户' }

const list = ref([])
const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const formRef = ref()

const emptyForm = { name: '', type: 'cash', balance: 0, currency: 'CNY' }
const form = reactive({ ...emptyForm })
const rules = {
  name: [{ required: true, message: '请输入账户名称', trigger: 'blur' }]
}

async function load() {
  loading.value = true
  try {
    list.value = await getAccounts()
  } finally {
    loading.value = false
  }
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
    balance: row.balance,
    currency: row.currency
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
  await ElMessageBox.confirm(`确认删除账户「${row.name}」？`, '提示', { type: 'warning' })
  await deleteAccount(row.id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
</style>
