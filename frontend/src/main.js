import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn' // Element Plus 中文语言包
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import ScForm from './components/ScForm.vue'
import ScTable from './components/ScTable.vue'
import ScTemplate from './components/ScTemplate.vue'
import './styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
// 传入 locale 才会把组件内置文案（确认弹窗按钮、日期面板、分页、表格空数据等）切为中文
app.use(ElementPlus, { locale: zhCn })

// 全局注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局注册项目内置的 schema 组件库（示例页与业务页均通过 <sc-form> / <sc-table> 直接使用）
app.component('ScForm', ScForm)
app.component('ScTable', ScTable)
// ScForm / ScTable 内部通过 <sc-template> 渲染字符串模板，必须一并注册
app.component('ScTemplate', ScTemplate)

app.mount('#app')
