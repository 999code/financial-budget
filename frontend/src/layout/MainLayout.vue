<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <el-icon><Money /></el-icon>
        <span>家庭财务</span>
      </div>
      <el-menu
        ref="menuRef"
        :default-active="activeMenu"
        :default-openeds="defaultOpeneds"
        router
        background-color="#1f2d3d"
        text-color="#c0c4cc"
        active-text-color="#409eff"
        class="menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/accounts">
          <el-icon><Wallet /></el-icon>
          <span>账户管理</span>
        </el-menu-item>
        <el-menu-item index="/income-expense">
          <el-icon><RefreshRight /></el-icon>
          <span>收支管理</span>
        </el-menu-item>
        <el-menu-item index="/loans">
          <el-icon><CreditCard /></el-icon>
          <span>贷款管理</span>
        </el-menu-item>
        <!-- 设置分组：只作为父级展开用，其 index 不对应具体路由 -->
        <el-sub-menu index="/settings">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </template>
          <el-menu-item index="/profile">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </el-menu-item>
          <el-menu-item v-if="auth.isAdmin" index="/users">
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/example">
          <el-icon><Document /></el-icon>
          <span>示例</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <span class="header-title">{{ currentTitle }}</span>
        <el-dropdown class="header-user" @command="onCommand">
          <span class="header-user__trigger">
            <el-icon><UserFilled /></el-icon>
            <span>{{ auth.displayName || '未登录' }}</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="change-password">修改密码</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/store/auth'

// 「设置」是纯分组菜单，不对应具体路由；其下的页面路径
const SETTINGS_INDEX = '/settings'
const SETTINGS_PATHS = ['/profile', '/users']

const menuRef = ref()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || '家庭财务管理系统')
// el-menu 的 default-openeds 只在初始化时读取一次，用它保证「刷新后停在子页面」时父级是展开的
const defaultOpeneds = computed(() =>
  SETTINGS_PATHS.includes(route.path) ? [SETTINGS_INDEX] : []
)
// 运行时切换（含从右上角下拉跳进来）：直接调 el-menu 的 open/close，父级不会自动展开
watch(
  () => route.path,
  (path) => {
    nextTick(() => {
      if (!menuRef.value) return
      if (SETTINGS_PATHS.includes(path)) menuRef.value.open(SETTINGS_INDEX)
      else menuRef.value.close(SETTINGS_INDEX)
    })
  },
  { immediate: true }
)

// 刷新后 user 信息会丢失，这里按令牌补一次
onMounted(() => {
  if (auth.isLogin && !auth.user) {
    auth.fetchProfile().catch(() => auth.logout())
  }
})

async function onCommand(command) {
  if (command === 'logout') {
    await ElMessageBox.confirm('确认退出登录？', '提示', { type: 'warning' })
    auth.logout()
    router.replace('/login')
    return
  }
  router.push(`/${command}`)
}
</script>

<style scoped>
.layout {
  height: 100%;
}
.aside {
  background: #1f2d3d;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  padding: 0 20px;
}
.menu {
  border-right: none;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}
.header-title {
  font-size: 16px;
  font-weight: 600;
}
.header-user__trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  outline: none;
}
.main {
  padding: 20px;
}
</style>
