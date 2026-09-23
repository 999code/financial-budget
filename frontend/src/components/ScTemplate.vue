<template>
    <RenderContent />
</template>

<script setup>
import { defineComponent, h, resolveDynamicComponent } from 'vue';

defineOptions({
    name: 'ScTemplate',
});

const props = defineProps({
    content: {
        type: [String, Object],
        required: true,
    },
    data: {
        type: Object,
        default: () => ({}),
    },
});

function toHandlerKey(eventName) {
    return `on${eventName.charAt(0).toUpperCase()}${eventName.slice(1)}`;
}

/**
 * 把外部传入的 data 转成 computed，而不是一次性快照。
 *
 * 原先写成 `data: () => props.data`——data() 只在组件实例创建时执行一次，
 * 之后列表刷新（行对象换成新对象）时组件实例被复用，内部拿到的仍是旧对象，
 * 表现为「改完金额保存后再点编辑，弹窗里还是旧值」。改用 computed 后每次
 * 都读取最新的 props.data，行数据变化即可同步。
 */
function toComputed(getSource) {
    const source = getSource() || {};
    const result = {};

    Object.keys(source).forEach((key) => {
        result[key] = () => (getSource() || {})[key];
    });
    return result;
}

// 仅在 data 的键集合发生变化时才需要重建组件（值变化走 computed 即可）
function toKey(source) {
    return Object.keys(source || {}).sort().join('|');
}

function normalizeVNodeProps(options) {
    const {
        attrs = {},
        props = {},
        on = {},
        nativeOn = {},
        ...rest
    } = options;
    const listeners = {};

    Object.entries({ ...on, ...nativeOn }).forEach(([eventName, handler]) => {
        listeners[toHandlerKey(eventName)] = handler;
    });

    return {
        ...rest,
        ...attrs,
        ...props,
        ...listeners,
    };
}

function RenderContent() {
    if (typeof props.content === 'string') {
        return h(
            defineComponent({
                template: props.content,
                computed: toComputed(() => props.data),
            }),
            { key: toKey(props.data) },
        );
    }

    const {
        tag,
        content,
        template,
        data,
        ...options
    } = props.content;

    if (tag) {
        return h(
            resolveDynamicComponent(tag),
            normalizeVNodeProps(options),
            content,
        );
    }

    return h(
        defineComponent({
            ...options,
            template,
            computed: toComputed(() => props.content?.data),
        }),
        { key: toKey(props.content?.data) },
    );
}
</script>
