<template>
  <div class="examples-overview">
    <h1>示例页面</h1>
    <el-tabs v-model="activeExample" class="examples-overview__tabs">
      <el-tab-pane
        v-for="item in examplePages"
        :key="item.path"
        :name="item.meta.example"
        :label="`${item.meta.example} · ${item.meta.title}`"
        lazy
      >
        <component :is="item.component" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Example1 from './Example1.vue'
import Example2 from './Example2.vue'
import Example3 from './Example3.vue'
import Example4 from './Example4.vue'
import Example5 from './Example5.vue'
import Example6 from './Example6.vue'

const examplePages = [
  { path: '/example/1', meta: { example: 'example1', title: 'ScForm 基础' }, component: Example1 },
  { path: '/example/2', meta: { example: 'example2', title: 'ScForm 复用' }, component: Example2 },
  { path: '/example/3', meta: { example: 'example3', title: '多列布局/搜索' }, component: Example3 },
  { path: '/example/4', meta: { example: 'example4', title: '字段/验证/动态' }, component: Example4 },
  { path: '/example/5', meta: { example: 'example5', title: '通用组件' }, component: Example5 },
  { path: '/example/6', meta: { example: 'example6', title: 'ScTable 表格' }, component: Example6 }
]

const activeExample = ref(examplePages[0].meta.example)
</script>

<style scoped>
.examples-overview h1 {
  margin: 0 0 24px;
  font-size: 24px;
  font-weight: 600;
}

.examples-overview__tabs :deep(.el-tabs__content) {
  padding-top: 24px;
}
</style>
