<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="always">
      <template #header>
        <div class="auth-card__title">注册</div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="70px" size="large">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="3-50 个字符，登录用" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="至少 6 位"
            autocomplete="new-password"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            show-password
            placeholder="请再次输入密码"
            autocomplete="new-password"
          />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="选填，默认与用户名相同" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="选填" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="选填" />
        </el-form-item>
      </el-form>

      <el-button type="primary" size="large" class="auth-card__submit" :loading="loading" @click="submit">
        注册并登录
      </el-button>
      <div class="auth-card__footer">
        已有账号？
        <el-button link type="primary" @click="$router.push('/login')">去登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

defineOptions({ name: 'Register' })

const router = useRouter()
const auth = useAuthStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  phone: '',
  email: '',
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '长度为 3-50 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) callback(new Error('两次输入的密码不一致'))
        else callback()
      },
      trigger: 'blur',
    },
  ],
  email: [{ type: 'email', message: '邮箱格式不正确', trigger: 'blur' }],
}

async function submit() {
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    await auth.register({
      username: form.username.trim(),
      password: form.password,
      name: form.name.trim() || undefined,
      phone: form.phone.trim() || undefined,
      email: form.email.trim() || undefined,
    })
    ElMessage.success('注册成功')
    router.replace('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  min-height: 100vh;
  padding: 40px 16px;
  background: #f2f5fa;
}
.auth-card {
  width: 460px;
}
.auth-card__title {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}
.auth-card__submit {
  width: 100%;
}
.auth-card__footer {
  margin-top: 14px;
  font-size: 13px;
  color: #909399;
  text-align: center;
}
</style>
