<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="always">
      <template #header>
        <div class="auth-card__title">登录</div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="70px" size="large">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            autocomplete="current-password"
            @keyup.enter="submit"
          />
        </el-form-item>
      </el-form>

      <el-button type="primary" size="large" class="auth-card__submit" :loading="loading" @click="submit">
        登录
      </el-button>
      <div class="auth-card__footer">
        还没有账号？
        <el-button link type="primary" @click="$router.push('/register')">立即注册</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

defineOptions({ name: 'Login' })

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function submit() {
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    await auth.login({ username: form.username.trim(), password: form.password })
    ElMessage.success('登录成功')
    router.replace(route.query.redirect || '/dashboard')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (auth.isLogin) router.replace('/dashboard')
})
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f2f5fa;
}
.auth-card {
  width: 420px;
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
