<template>
    <div class="detail-card" :style="{ paddingLeft: `${props.level * 15}px` }">
        <BlockQuote>{{ title }}</BlockQuote>
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup>

import BlockQuote from './BlockQuote.vue';
const props = defineProps({
    title: {
        type: String,
        default: ''
    },
    level: {
        type: Number,
        default: 0
    }
});

</script>
