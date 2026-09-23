<template>
  <div>
    <el-alert
      type="info"
      :closable="false"
      show-icon
      title="组件使用示例（example1 – example6）"
      description="本页通过 el-tabs 展示 src/example 下的 6 个组件使用示例：ScForm 表单、ScTable 表格，以及 BlockQuote / DetailCard / ContentList 等通用组件。"
    />

    <el-tabs v-model="active" class="example-tabs" style="margin-top: 16px">
      <el-tab-pane
        v-for="item in examples"
        :key="item.name"
        :name="item.name"
        :label="item.label"
        lazy
      >
        <component :is="item.component" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Example1 from '@/example/Example1.vue'
import Example2 from '@/example/Example2.vue'
import Example3 from '@/example/Example3.vue'
import Example4 from '@/example/Example4.vue'
import Example5 from '@/example/Example5.vue'
import Example6 from '@/example/Example6.vue'

const active = ref('example1')

const examples = [
  { name: 'example1', label: 'Example1 · ScForm 基础', component: Example1 },
  { name: 'example2', label: 'Example2 · ScForm 复用', component: Example2 },
  { name: 'example3', label: 'Example3 · 多列布局/搜索', component: Example3 },
  { name: 'example4', label: 'Example4 · 字段/验证/动态', component: Example4 },
  { name: 'example5', label: 'Example5 · 通用组件', component: Example5 },
  { name: 'example6', label: 'Example6 · ScTable 表格', component: Example6 }
]
</script>

<style scoped>
.example-tabs :deep(.el-tabs__content) {
  padding-top: 16px;
}
</style>
