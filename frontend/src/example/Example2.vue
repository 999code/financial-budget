<template>
  <div>
    <h4>同一份schema根据不同model生成独立表单</h4>
    <sc-form :schema="schema1" />
    <sc-form :schema="schema2" />
    <p>model1: {{ JSON.stringify(model1) }}</p>
    <p>model2: {{ JSON.stringify(model2) }}</p>

    <h4>绑定多个事件并使用title、slot等扩展功能</h4>
    <sc-form ref="form" :schema="schema3">
      <template #age-slot>
        <el-input v-model.number="model3.age" />
      </template>
    </sc-form>
    <p>model: {{ JSON.stringify(model3) }}</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { cloneDeep } from 'lodash-es';

// 表单schema，可以独立储存在其它地方作为公用
const schema = {
  formItems: [
    {
      type: 'input',
      label: '名字',
      field: 'name',
      placeholder: '请输入名字'
    },
    {
      type: 'input.number',
      label: "年龄",
      field: "age",
      rules: [
        { required: true, message: '年龄不能为空' },
        { type: 'number', message: '年龄必须为数字值' }
      ]
    }
  ]
};

defineOptions({
  name: 'Example2',
});

const model1 = ref({});
const model2 = ref({});
const model3 = ref({});
const form = ref(null);

const schema1 = computed(() => ({
  inline: true,
  model: model1.value, // 这里绑定表单model1
  ...cloneDeep(schema)
}));
const schema2 = computed(() => ({
  inline: true,
  model: model2.value, // 这里绑定表单model2
  ...cloneDeep(schema)
}));
const schema3 = computed(() => ({
  inline: true,
  model: model3.value, // 这里绑定表单model
  formItems: [
    {
      type: 'title', // 使用表单title
      content: '示例表单'
    },
    {
      type: 'input.trim', // trim去掉空格，同vue官方v-model.trim
      label: '名字',
      field: 'name',
      placeholder: '请输入名字',
      on: {
        'keyup.enter'() { // enter回车触发，同 Vue 3 官方 @keyup.enter
          console.log('keyup enter!');
        },
        change() { // change事件 同elment官方
          console.log('change!');
        }
      }
    },
    {
      type: 'slot', // 使用表单slot
      name: 'age-slot', // slot名字
      label: '年龄',
      field: 'age',
      rules: [
        { required: true, message: '年龄不能为空' },
        { type: 'number', message: '年龄必须为数字值' }
      ],
    },
    {
      type: 'button',
      content: '重置',
      on: {
        click() {
          form.value.elForm.resetFields(); // elForm属性获得el-form组件实例，并使用它的方法resetFields
        }
      }
    },
  ]
}));
</script>
