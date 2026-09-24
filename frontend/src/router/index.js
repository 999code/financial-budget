import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import { useAuthStore } from '@/store/auth'

const routes = [
  // 登录注册：独立页面，不带侧边栏
  { path: '/login', name: 'login', component: () => import('@/views/Login.vue'), meta: { title: '登录', public: true } },
  { path: '/register', name: 'register', component: () => import('@/views/Register.vue'), meta: { title: '注册', public: true } },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '仪表盘' } },
      { path: 'accounts', name: 'accounts', component: () => import('@/views/Accounts.vue'), meta: { title: '账户管理' } },
      { path: 'users', name: 'users', component: () => import('@/views/Users.vue'), meta: { title: '用户管理', admin: true } },
      { path: 'income-expense', name: 'income-expense', component: () => import('@/views/IncomeExpense.vue'), meta: { title: '收支管理' } },
      { path: 'loans', name: 'loans', component: () => import('@/views/Loans.vue'), meta: { title: '贷款管理' } },
      { path: 'pensions', name: 'pensions', component: () => import('@/views/Pensions.vue'), meta: { title: '养老金管理' } },
      { path: 'profile', name: 'profile', component: () => import('@/views/Profile.vue'), meta: { title: '个人信息' } },
      { path: 'change-password', name: 'change-password', component: () => import('@/views/ChangePassword.vue'), meta: { title: '修改密码' } },
      { path: 'example', name: 'example', component: () => import('@/views/Example.vue'), meta: { title: '示例' } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 前端登录守卫：未登录访问站内页面一律跳登录页，并带上回跳地址
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isLogin) {
    return { path: '/login', query: to.fullPath === '/' ? {} : { redirect: to.fullPath } }
  }
  // 已登录时不再进入登录/注册页
  if (to.meta.public && auth.isLogin && to.path !== '/register') {
    return { path: '/dashboard' }
  }
  // 管理员专属页面：用户信息缺失时先补齐，再判断是否为管理员
  if (to.meta.admin) {
    if (!auth.user) {
      try { await auth.fetchProfile() } catch { /* 令牌失效等，交由上面的未登录逻辑 */ }
    }
    if (!auth.isAdmin) {
      return { path: '/dashboard' }
    }
  }
  return true
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - 家庭财务` : '家庭财务管理系统'
})

export default router
