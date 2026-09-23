<template>
  <div v-bind="$attrs" class="block-quote">
    <div class="quote-content">
      <slot></slot>
    </div>
  </div>
  <el-divider v-if="showLine"></el-divider>
</template>
<script setup>
defineProps({
  showLine: {
    type: Boolean,
    default: false
  }
});
</script>
<style scoped>
.block-quote {
  border-left: 4px solid #409eff;
  padding-left: 6px;
  margin-bottom: 24px;
}

.quote-content {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  font-size: 16px;
  color: #1a1a1a;
}
</style>
