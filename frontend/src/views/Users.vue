<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" :icon="Plus" @click="openCreate">新增用户</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column label="用户名" min-width="120">
        <template #default="{ row }">{{ row.username || '-' }}</template>
      </el-table-column>
      <el-table-column prop="name" label="姓名" min-width="120" />
      <el-table-column label="手机号" min-width="140">
        <template #default="{ row }">{{ row.phone || '-' }}</template>
      </el-table-column>
      <el-table-column label="邮箱" min-width="180">
        <template #default="{ row }">{{ row.email || '-' }}</template>
      </el-table-column>
      <el-table-column label="创建时间" min-width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" :disabled="row.id === currentUserId" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="visible" :title="editingId ? '编辑用户' : '新增用户'" width="460px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="如：张三" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="登录用户名，留空则该成员不可登录" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            :placeholder="editingId ? '留空表示不修改密码' : '登录密码，至少 6 位'"
          />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="选填" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="选填" />
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
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { createUser, deleteUser, getUsers, updateUser } from '@/api/users'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const currentUserId = computed(() => auth.user?.id)

const list = ref([])
const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const formRef = ref()

const emptyForm = { name: '', username: '', password: '', phone: '', email: '' }
const form = reactive({ ...emptyForm })

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [
    {
      validator: (rule, value, cb) => {
        if (value && value.length < 6) cb(new Error('密码至少 6 位'))
        else cb()
      },
      trigger: 'blur',
    },
  ],
}

function formatTime(v) {
  if (!v) return '-'
  return v.replace('T', ' ').slice(0, 19)
}

async function load() {
  loading.value = true
  try {
    list.value = await getUsers()
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
    username: row.username || '',
    password: '',
    phone: row.phone || '',
    email: row.email || '',
  })
  visible.value = true
}

async function submit() {
  await formRef.value.validate()
  // 仅在填写了密码时才提交密码字段
  const payload = { ...form }
  if (!payload.password) delete payload.password

  if (editingId.value) {
    await updateUser(editingId.value, payload)
    ElMessage.success('已更新')
  } else {
    await createUser(payload)
    ElMessage.success('已创建')
  }
  visible.value = false
  load()
}

async function remove(row) {
  if (row.id === currentUserId.value) {
    ElMessage.warning('不能删除当前登录的账号')
    return
  }
  await ElMessageBox.confirm(`确认删除用户「${row.name}」？该操作不可恢复。`, '提示', { type: 'warning' })
  await deleteUser(row.id)
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
