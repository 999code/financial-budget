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

    <el-card class="tip" shadow="never">
      <template #header>欢迎使用家庭财务管理系统</template>
      <p>从左侧菜单开始管理你的账户、收支、分类与预算。</p>
      <p>数据接口前缀为 <code>/api/v1</code>，后端文档见 <code>http://127.0.0.1:8000/docs</code>。</p>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { getSummary } from '@/api/summary'

const summary = reactive({
  total_balance: 0,
  total_income: 0,
  total_expense: 0,
  account_count: 0
})

onMounted(async () => {
  const data = await getSummary()
  Object.assign(summary, data)
})
</script>

<style scoped>
.tip {
  margin-top: 20px;
}
</style>
