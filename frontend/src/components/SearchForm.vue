<template>
  <div :id="fieldsId" class="search-form">
    <ScForm ref="formRef" class="search-form__inner" :schema="visibleSchema" />
  </div>
</template>

<script setup>
import ScForm from '@/components/ScForm.vue'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'
import { computed, getCurrentInstance, ref } from 'vue'

defineOptions({ name: 'SearchForm' })

const GRID_COLUMN_COUNT = 24

const props = defineProps({
  schema: {
    type: Object,
    required: true
  },
  collapsedCount: {
    type: Number,
    default: 3,
    validator: (value) => Number.isInteger(value) && value > 0
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['search', 'reset'])
const formRef = ref(null)
const expanded = ref(false)
const fieldsId = `search-form-fields-${getCurrentInstance().uid}`

const availableItems = computed(() => (
  Array.isArray(props.schema.formItems)
    ? props.schema.formItems.filter((item) => item.show !== false)
    : []
))
const hasMoreItems = computed(() => availableItems.value.length > props.collapsedCount)
const visibleItemCount = computed(() => (
  expanded.value
    ? availableItems.value.length
    : Math.min(availableItems.value.length, props.collapsedCount)
))
const formItemSpan = computed(() => Number(props.schema.colSpan) || 6)
const actionsOffset = computed(() => {
  const itemsPerRow = GRID_COLUMN_COUNT / formItemSpan.value
  const occupiedItems = visibleItemCount.value % itemsPerRow
  return (itemsPerRow - occupiedItems - 1) * formItemSpan.value
})

const visibleSchema = computed(() => {
  let visibleIndex = 0
  const formItems = (props.schema.formItems || []).map((item) => {
    if (item.show === false) return item
    const show = expanded.value || visibleIndex < props.collapsedCount
    visibleIndex += 1
    return { ...item, show }
  })

  return {
    labelPosition: 'top',
    ...props.schema,
    inline: false,
    colSpan: formItemSpan.value,
    formItems: [
      ...formItems,
      {
        class: 'search-form-actions',
        offset: actionsOffset.value,
        items: [
          {
            type: 'button',
            content: '搜索',
            subtype: 'primary',
            loading: props.loading,
            on: { click: () => emit('search') }
          },
          {
            type: 'button',
            content: '重置',
            plain: true,
            disabled: props.loading,
            on: { click: () => emit('reset') }
          },
          ...(hasMoreItems.value ? [{
            type: 'button',
            content: expanded.value ? '收起' : '展开',
            subtype: 'primary',
            link: true,
            rightIcon: expanded.value ? ArrowUp : ArrowDown,
            'aria-expanded': expanded.value,
            'aria-controls': fieldsId,
            on: { click: () => { expanded.value = !expanded.value } }
          }] : [])
        ]
      }
    ]
  }
})

const elForm = computed(() => formRef.value?.elForm)

defineExpose({
  elForm,
  expanded,
  reset: () => formRef.value?.reset(),
  clearValidate: () => formRef.value?.elForm?.clearValidate()
})
</script>

<style lang="scss" scoped>
.search-form {
  min-width: 0;
}

.search-form__inner :deep(.el-form-item) {
  width: 100%;
  margin-right: 0;
  margin-bottom: 16px;
}

.search-form__inner :deep(.el-form-item__label) {
  height: auto;
  padding: 0 0 6px;
  color: var(--el-text-color-regular, #606266);
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
}

.search-form__inner :deep(.el-input),
.search-form__inner :deep(.el-date-editor) {
  width: 100%;
}


.search-form__inner :deep(.search-form-actions) {
  display: flex;
  height: 100%;
  align-items: flex-end;
}

.search-form__inner :deep(.search-form-actions .el-form-item__content) {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-end;
  padding-bottom: 18px;
  white-space: nowrap;
}


.search-form__inner :deep(.search-form-actions .el-button--text) {
  min-width: 64px;
}

@media (max-width: 760px) {
  .search-form__inner :deep(.el-col) {
    display: block;
    width: 100%;
    max-width: 100%;
    flex: 0 0 100%;
    margin-left: 0 !important;
  }

  .search-form__inner :deep(.el-input__inner),
  .search-form__inner :deep(.el-range-input) {
    font-size: 16px;
  }

  .search-form__inner :deep(.search-form-actions .el-form-item__content) {
    padding-bottom: 0;
  }
}
</style>
