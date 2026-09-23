<template>
    <div>
        <BlockQuote showLine>
           标题组件
        </BlockQuote>
        <DetailCard title="详情卡片">
            <p>这是详情卡片的内容。</p>
        </DetailCard>
        <DetailCard title="详情卡片" :level="1">
            <p>这是详情卡片的内容。</p>
        </DetailCard>
        <DetailCard title="详情卡片" :level="2">
            <p>这是详情卡片的内容。</p>
        </DetailCard>
        <DetailCard title="内容列表">
            <ContentList :data="detailData" :fields="detailFields">
                <template #status-label>
                    当前状态
                </template>
                <template #status-value="{ value }">
                    <el-tag type="success" size="small">{{ value }}</el-tag>
                </template>
            </ContentList>
        </DetailCard>
    </div>
</template>

<script setup>
import BlockQuote from '../components/BlockQuote.vue';
import ContentList from '../components/ContentList.vue';
import DetailCard from '../components/DetailCard.vue';

const detailData = {
    orderNo: 'SO20260908001',
    customer: '千睿智汇',
    status: '已完成',
    owner: '张三',
};

const detailFields = [
    { field: 'orderNo', label: '订单编号' },
    { field: 'customer', label: '客户名称' },
    { field: 'status', label: '状态' },
    { field: 'owner', label: '负责人' },
];
</script>
