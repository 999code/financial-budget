<template>
  <nav class="example-menu" aria-label="示例页面">
    <p class="example-menu__title">组件示例</p>
    <router-link
      v-for="item in items"
      :key="item.path"
      :to="item.path"
      class="example-menu__link"
    >
      <span>{{ item.meta.title }}</span>
      <span v-if="item.meta.example" class="example-menu__number">{{ item.meta.example }}</span>
    </router-link>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.example-menu {
  padding: 24px 12px;
}

.example-menu__title {
  margin: 0 12px 24px;
  font-size: 16px;
  font-weight: 600;
}

.example-menu__link {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 4px 12px;
  min-height: 44px;
  box-sizing: border-box;
  margin-bottom: 4px;
  padding: 12px;
  border-radius: var(--el-border-radius-base);
  color: var(--el-text-color-regular);
  font-size: 14px;
  line-height: 20px;
  text-decoration: none;
}

.example-menu__link:hover {
  background: var(--el-fill-color-light);
}

.example-menu__link.router-link-exact-active {
  color: var(--el-color-primary-dark-2);
  background: var(--el-color-primary-light-9);
  font-weight: 600;
}

.example-menu__link:focus-visible {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

.example-menu__number {
  font-size: 12px;
}
</style>
