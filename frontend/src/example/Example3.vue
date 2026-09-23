<template>
  <div>
    <h4>多列布局col、span、gutter</h4>
    <sc-form ref="formRef" :schema="schema" />
    <p>model: {{ JSON.stringify(model) }}</p>
    <search-form  
      :schema="querySchema"
      @search="loadEvents"
      @reset="resetQuery"
      ></search-form>
  </div>
</template>

<script setup>
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue';
import { computed, ref } from 'vue';
import SearchForm from '@/components/SearchForm.vue';
const formRef = ref(null);
const loadEvents = () => {
  console.log('loadEvents', model.value);
};
const resetQuery = () => {
  console.log('resetQuery', model.value);
};
defineOptions({
  name: 'Example3',
});

const model = ref({});
const GRID_COLUMN_COUNT = 24;
const FORM_ITEM_SPAN = 6;
const COLLAPSED_ITEM_COUNT = 3;
const expanded = ref(false);
const formItems = [
  {
    type: 'input.trim',
    label: '名字',
    field: 'name',
    placeholder: '请输入名字',
  },
  {
    type: 'input.number',
    label: '年龄',
    field: 'age',
    placeholder: '请输入年龄',
  },
  {
    type: 'select',
    label: '性别',
    field: 'sex',
    options: [{
      label: '男',
      value: '1',
    }, {
      label: '女',
      value: '2',
    }]
  },
  {
    type: 'input.number',
    label: '电话',
    field: 'phone',
    placeholder: '请输入电话',
  },
  // {
  //   type: 'input',
  //   label: '地址',
  //   field: 'addr',
  //   placeholder: '请输入地址',
  // },
  // {
  //   type: 'checkbox',
  //   label: '爱好',
  //   field: 'likes',
  //   options: [{
  //     label: '草莓',
  //     value: '1',
  //   }, {
  //     label: '车厘子',
  //     value: '2',
  //   }, {
  //     label: '香蕉',
  //     value: '3',
  //   }]
  // },
];
const hasMoreItems = formItems.length > COLLAPSED_ITEM_COUNT;
const visibleItemCount = computed(() => (
  expanded.value ? formItems.length : Math.min(formItems.length, COLLAPSED_ITEM_COUNT)
));
const optionsOffset = computed(() => {
  const itemsPerRow = GRID_COLUMN_COUNT / FORM_ITEM_SPAN;
  const occupiedItems = visibleItemCount.value % itemsPerRow;

  return (itemsPerRow - occupiedItems - 1) * FORM_ITEM_SPAN;
});

const schema = computed(() => ({
        model: model.value, // 这里绑定表单model
        labelPosition: 'top',
        labelWidth: '50px',
        colSpan: FORM_ITEM_SPAN, // col 布局，同 Element Plus，默认 24
        gutter: 20, // 栅格 col 间隔，同 Element Plus，单位 px，默认 0
        formItems: [
          ...formItems.map((formItem, index) => ({
            ...formItem,
            show: expanded.value || index < COLLAPSED_ITEM_COUNT,
          })),
          {
            class: 'options-btns',
            offset: optionsOffset.value,
            items:[
              {
                type: 'button',
                content: '搜索',
                subtype: 'primary',
                on: {
                    click: $event => {
                      console.log('onSearch', $event,model.value);
                    }
                  }
                },
                {
                  type: 'button',
                  content: '重置',
                  plain: true,
                  on: {
                    click: $event => {
                      // formRef.value.reset();
                      formRef.value.elForm.resetFields();
                      console.log('onReset', $event);
                    }
                  }
                },
                ...(hasMoreItems ? [{
                  type: 'button',
                  content: expanded.value ? '收起' : '展开',
                  subtype: 'primary',
                  link: true,
                  rightIcon: expanded.value ? ArrowUp : ArrowDown,
                  'aria-expanded': expanded.value,
                  on: {
                    click: () => {
                      expanded.value = !expanded.value;
                    }
                  }
                }] : [])
            ]
          }
        ]
      }));

const querySchema = computed(() => ({
  colSpan: 6,
  labelPosition: 'top',
  gutter: 18,
  model: model.value,
   formItems
}))


</script>
<style scoped>
:deep(.options-btns) {
  display: flex;
  align-items: flex-end;
  height: 100%;
  .el-form-item__content{
    display: flex;
    justify-content: flex-end;
    padding-bottom: 18px;
  }
}
</style>
