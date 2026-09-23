<template>
  <div class="change-password">
    <el-card shadow="never">
      <template #header>
        <div class="change-password__header">
          <span>修改密码</span>
          <el-button link type="primary" @click="$router.push('/profile')">返回个人信息</el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="change-password__form"
      >
        <el-form-item label="原密码" prop="old_password">
          <el-input v-model="form.old_password" type="password" show-password placeholder="请输入当前密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="form.new_password" type="password" show-password placeholder="至少 6 位" />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submit">确认修改</el-button>
          <el-button @click="reset">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { changePassword } from '@/api/auth'

defineOptions({ name: 'ChangePassword' })

const formRef = ref(null)
const saving = ref(false)
const empty = () => ({ old_password: '', new_password: '', confirmPassword: '' })
const form = reactive(empty())

const rules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '新密码至少 6 位', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value && value === form.old_password) callback(new Error('新密码不能与原密码相同'))
        else callback()
      },
      trigger: 'blur',
    },
  ],
  confirmPassword: [
    {
      validator: (rule, value, callback) => {
        if (value !== form.new_password) callback(new Error('两次输入的新密码不一致'))
        else callback()
      },
      trigger: 'blur',
    },
  ],
}

function reset() {
  Object.assign(form, empty())
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
    await changePassword({ old_password: form.old_password, new_password: form.new_password })
    ElMessage.success('密码已修改，下次登录请使用新密码')
    reset()
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.change-password__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.change-password__form {
  max-width: 520px;
}
</style>
