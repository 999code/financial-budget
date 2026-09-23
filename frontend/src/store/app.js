import { defineStore } from 'pinia'

// 轻量级全局状态示例（可扩展为登录用户、主题等）
export const useAppStore = defineStore('app', {
  state: () => ({
    title: '家庭财务管理系统',
    sidebarCollapsed: false
  }),
  actions: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
})
