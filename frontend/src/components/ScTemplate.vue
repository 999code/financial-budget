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
        return h(defineComponent({
            template: props.content,
            data: () => props.data,
        }));
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

    return h(defineComponent({
        ...options,
        template,
        data: () => data || {},
    }));
}
</script>
