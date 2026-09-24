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
 *
 * 这里用普通函数而非箭头函数：Vue 在初始化 options computed 时会把 getter
 * bind 到组件实例，普通函数里的 this 才是当前实例（箭头函数会锁死模块作用域）。
 */
function toComputed(keys) {
    const result = {};

    keys.forEach((key) => {
        result[key] = function () {
            const source = this.tplData || {};
            return source[key];
        };
    });

    return result;
}

// 仅在 data 的键集合发生变化时才需要重建组件（值变化走 computed 即可）
function toKey(source) {
    return Object.keys(source || {}).sort().join('|');
}

/**
 * 组件定义缓存：同一份模板 + 同一套 data 键集合只创建一次组件。
 *
 * 之前每次渲染都 defineComponent 出一个新组件对象，Vue patch 时发现 vnode.type
 * 不同（哪怕 key 相同）就会 unmount + mount，单元格内容被整体销毁重建，
 * 内部 el-tag / el-button 等带过渡的组件会同时出现 leave 与 enter 两份节点，
 * 300ms 内把单元格撑成两行（实测 cell 23 → 47、行高 40.5 → 64），
 * 表格高度随之跳变，表现就是「刷新后表格抖动」。
 * 缓存后模板不变的行只更新数据，不再重建，也就不会闪过渡动画。
 */
const componentCache = new Map();

function getCachedComponent(template, source, extraOptions) {
    const keys = Object.keys(source || {}).sort();
    const cacheKey = `${keys.join('|')}||${template}`;

    if (componentCache.size > 500) componentCache.clear();

    if (!componentCache.has(cacheKey)) {
        componentCache.set(
            cacheKey,
            defineComponent({
                ...(extraOptions || {}),
                props: {
                    tplData: {
                        type: Object,
                        default: () => ({}),
                    },
                },
                template,
                computed: toComputed(keys),
            }),
        );
    }

    return componentCache.get(cacheKey);
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
            getCachedComponent(props.content, props.data),
            {
                tplData: props.data,
                key: toKey(props.data),
            },
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
        getCachedComponent(template, data, options),
        {
            tplData: data,
            key: toKey(data),
        },
    );
}
</script>
