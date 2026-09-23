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
