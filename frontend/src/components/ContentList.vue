<template>
  <dl
    class="content-list"
    :class="{ 'content-list--double': resolvedFields.length > 3 }"
  >
    <div
      v-for="item in resolvedFields"
      :key="item.field"
      class="content-list__item"
    >
      <dt class="content-list__label">
        <slot
          :name="`${item.field}-label`"
          :data="props.data"
          :field="item.field"
          :item="item"
          :label="item.label"
        >
          {{ item.label }}：
        </slot>
      </dt>
      <dd class="content-list__value">
        <slot
          :name="`${item.field}-value`"
          :data="props.data"
          :field="item.field"
          :item="item"
          :value="item.value"
        >
          {{ displayValue(item.value) }}
        </slot>
      </dd>
    </div>
  </dl>
</template>

<script setup>
import { computed } from 'vue';
import { get } from 'lodash-es';

defineOptions({
  name: 'ContentList',
});

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
  fields: {
    type: Array,
    default: () => [],
  },
  emptyText: {
    type: String,
    default: '-',
  },
});

const resolvedFields = computed(() => props.fields
  .filter(item => item && item.field)
  .map(item => ({
    ...item,
    value: get(props.data, item.field),
  })));

function displayValue(value) {
  return value === null || value === undefined || value === ''
    ? props.emptyText
    : value;
}
</script>

<style scoped>
.content-list {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  column-gap: 40px;
  margin: 0;
}

.content-list--double {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.content-list__item {
  display: grid;
  grid-template-columns: minmax(88px, 32%) minmax(0, 1fr);
  gap: 16px;
  align-items: start;
  min-width: 0;
  padding: 10px 0;
  /* border-bottom: 1px solid var(--el-border-color-lighter); */
}

.content-list__label,
.content-list__value {
  min-width: 0;
  margin: 0;
  font-size: 14px;
  line-height: 22px;
  overflow-wrap: anywhere;
}

.content-list__label {
  color: var(--el-text-color-secondary);
}

.content-list__value {
  color: var(--el-text-color-primary);
  font-weight: 500;
  text-align: right;
}

@media (max-width: 720px) {
  .content-list--double {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
