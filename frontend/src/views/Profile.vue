<template>
  <div class="profile">
    <el-card shadow="never">
      <template #header>
        <div class="profile__header">
          <span>个人信息</span>
          <el-button type="primary" plain size="small" @click="$router.push('/change-password')">
            修改密码
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        v-loading="loading"
        :model="form"
        :rules="rules"
        label-width="90px"
        class="profile__form"
      >
        <el-form-item label="用户名">
          <el-input :model-value="form.username" disabled />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" clearable />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" clearable />
        </el-form-item>
        <el-form-item label="注册时间">
          <span>{{ formatTime(form.created_at) }}</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submit">保存</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { getProfile, updateProfile } from '@/api/auth'

defineOptions({ name: 'Profile' })

const auth = useAuthStore()
const formRef = ref(null)
const loading = ref(false)
const saving = ref(false)
const form = reactive({ username: '', name: '', phone: '', email: '', created_at: '' })

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '邮箱格式不正确', trigger: 'blur' }],
}

function fill(user) {
  Object.assign(form, {
    username: user?.username || '',
    name: user?.name || '',
    phone: user?.phone || '',
    email: user?.email || '',
    created_at: user?.created_at || '',
  })
}

onMounted(async () => {
  loading.value = true
  try {
    fill(await getProfile())
  } finally {
    loading.value = false
  }
})

function reset() {
  fill(auth.user)
  formRef.value?.clearValidate()
}

async function submit() {
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  saving.value = true
  try {
    const user = await updateProfile({
      name: form.name.trim(),
      phone: form.phone.trim() || null,
      email: form.email.trim() || null,
    })
    fill(user)
    auth.updateUser(user)
    ElMessage.success('已保存')
  } finally {
    saving.value = false
  }
}

function formatTime(ts) {
  if (!ts) return '-'
  return String(ts).replace('T', ' ').slice(0, 16)
}
</script>

<style scoped>
.profile__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.profile__form {
  max-width: 520px;
}
</style>
