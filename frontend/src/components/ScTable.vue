<template>
    <el-table 
        ref="table"
        v-bind="useProp(schema, 'table')"
        v-on="useEvent(schema)"
        @selection-change="onSelectionChange"
        @header-dragend="onHeaderDragend"     
    >
        <el-table-column
            v-for="(item, index) of schema.columns"
            v-bind="useProp(item, 'column')"
            :key="item.prop || `${item.type || 'column'}-${index}`"
        >
            <template v-if="typeof item.template === 'function'" #default="scope">
                <sc-template
                    :content="item.template.call(schema.bind, scope)"
                    :data="{ scope, bind: schema.bind }"
                />
            </template>
            <template v-else-if="typeof item.template === 'string'" #default="scope">
                <slot :name="item.template" v-bind="scope" />
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup>
import { computed, ref, toRefs } from 'vue';

defineOptions({
    name: 'ScTable',
});

const props = defineProps({
    schema: {
        type: Object,
        required: true,
    },
    setting: {
        type: Object,
        default: () => ({
            table: {
                border: true,
                defaultExpandAll: true,
                tooltipEffect: 'light',
                height: '100%',
                rowKey: row => row.id,
            },
            column: {
                align: 'center',
            },
        }),
    },
});
const { schema, setting } = toRefs(props);
const table = ref(null);
const selection = ref([]);
const tableInstance = computed(() => table.value);

/**
 * 归一化表格高度。
 *
 * el-table 只要 height 有值（哪怕是非数字的字符串）就会进入「固定高度」布局：
 * 内部用 ResizeObserver + doLayout() 把 body 高度写成「scrollHeight − 表头 − 合计行」的
 * 计算值。当父容器是自适应高度时，这个计算会在刷新时算错（曾实测 body 被撑高 164.5px，
 * 表现为刷新后表格抖一下）。因此 'auto' / 空值一律按「不设置 height」处理，
 * 让表格按内容自然撑开。
 */
function normalizeHeight(height) {
    if (height === 'auto' || height === '' || height === undefined || height === null) {
        return undefined;
    }
    return height;
}

function useProp(prop, type) {
    const componentProps = { ...prop };
    // 设置具体各项值/默认值
    switch (type) {
        case 'table':
            // 删除多余prop
            delete componentProps.bind;
            delete componentProps.on;
            delete componentProps.columns;
            return {
                ...setting.value.table,
                ...componentProps,
                height: normalizeHeight(componentProps.height ?? setting.value.table?.height),
            };
        case 'column':
            delete componentProps.template;
            return {
                ...setting.value.column,
                ...componentProps,
            };
        default:
            return componentProps;
    }
}

function useEvent({ on = {} }) {
    const listeners = {};
    Object.entries(on).forEach(([eventName, handler]) => {
        if (typeof handler === 'function') {
            const normalizedName = eventName.replace(/\.native$/, '');
            listeners[normalizedName] = schema.value.bind
                ? handler.bind(schema.value.bind)
                : handler;
        }
    });
    return listeners;
}

function onSelectionChange(value) {
    selection.value = value || [];
}

function onHeaderDragend() {
    tableInstance.value.doLayout();
}

function getTable() {
    return tableInstance.value;
}

function getSelection() {
    return selection.value;
}

defineExpose({
    elTable: tableInstance,
    selection,
    getTable,
    getSelection,
});
</script>
