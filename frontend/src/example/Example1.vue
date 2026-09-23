<template>
  <div>
    <h4>一个简单双向绑定表单</h4>
    <sc-form v-model="model" :schema="schema" />

    <h4>设置表单默认值</h4>
    <sc-form v-model="model2" :schema="schema2" />

    <h4>绑定多个model并验证表单某个字段</h4>
    <sc-form :schema="schema3" />
    <p>model: {{ JSON.stringify(model3) }}</p>
    <p>likes: {{ JSON.stringify(likes3) }}</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

defineOptions({
  name: 'Example1',
});

const model = ref({});
const schema = {
  inline: true,
  formItems: [
    {
      type: 'input',
      label: '名字',
      field: 'name',
      placeholder: '请输入名字'
    },
    {
      type: 'input',
      label: '密码',
      field: 'password',
      showPassword: true,
      placeholder: '请输入密码'
    },
    {
      type: 'button',
      content: '提交',
      on: {
        click() {
          console.log('submit!');
        }
      }
    }
  ]
};
const model2 = ref({
  name: 'kris',
});
const schema2 = {
  inline: true,
  formItems: [
    {
      type: 'input',
      label: '名字',
      field: 'name',
      placeholder: '请输入名字'
    },
    {
      type: 'input',
      label: '密码',
      field: 'password',
      showPassword: true,
      placeholder: '请输入密码'
    },
    {
      type: 'button',
      content: '提交',
      on: {
        click() {
          console.log('submit!');
        }
      }
    }
  ]
};
const model3 = ref({});
const likes3 = ref([]);
const schemaBind = {
  get likes3() {
    return likes3.value;
  },
  set likes3(value) {
    likes3.value = value;
  },
};

const schema3 = computed(() => ({
  bind: schemaBind, // 独立model通过绑定上下文更新
  inline: true,
  model: model3.value, // 整个表单的model
  formItems: [
    {
      type: 'input',
      label: '名字',
      field: 'name',
      placeholder: '请输入名字'
    },
    {
      type: 'input.number',
      label: '年龄',
      field: 'age',
      rules: [ // 字段验证规则，API 与 Element Plus Form 一致
        { required: true, message: '年龄不能为空' },
        { type: 'number', message: '年龄必须为数字值' }
      ]
    },
    {
      type: 'checkbox',
      label: '喜好',
      model: likes3.value, // 此字段独立绑定一个model
      field: 'likes3', // 此field名字跟model名字保持一致
      options: [{
        label: '足球',
        value: 1
      }, {
        label: '篮球',
        value: 2
      }, {
        label: '爬山',
        value: 3
      }, {
        label: '旅游',
        value: 4
      }]
    },
  ]
}));
</script>
