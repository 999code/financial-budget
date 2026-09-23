<template>
  <div class="schema-demo">
    <h4>每个字段绑定不同model表单</h4>

    <sc-form :schema="schema1"></sc-form>
    <p>{{ name }} {{ age }}</p>


    <h4>绑定一个model，且初始化model值</h4>

    <sc-form :schema="schema2" v-model="model2"></sc-form>
    <p>{{ JSON.stringify(model2) }}</p>

    <h4>复制一份schema生成表单，绑定独立model，并支持重置默认值 (注意与el-form官方resetFields重置的区别)</h4>
    <sc-form ref="model3Form" :schema="schema3" v-model="model3"></sc-form>
    <p>{{ JSON.stringify(model3) }}</p>
    <el-button @click="model3Form.reset()">sc-form 重置</el-button>
    <el-button @click="model3Form.elForm.resetFields()">el-form 重置</el-button>
    <p class="tips">Tips：官方el-checkbox-group的v-model绑定值必须定义且为数组否则重置可能异常，大部分情况建议用官方resetFields方法来重置表单，这样可以跟官方API保持一致。</p>

    <h4>复制一份schema生成表单绑定独立model，且定制了schema某些部分</h4>

    <sc-form :schema="schema4" v-model="model4"></sc-form>
    <p>{{ JSON.stringify(model4) }}</p>

    <h4>组合不同schema生成表单，且复用上面model</h4>

    <sc-form :schema="schemaGroup" v-model="model4"></sc-form>
    <p>{{ JSON.stringify(model4) }}</p>

    <h4>在一个 formItem 中组合搜索和重置按钮</h4>

    <sc-form ref="queryForm" :schema="schemaButtonGroup" v-model="queryModel"></sc-form>
    <p>{{ JSON.stringify(queryModel) }}</p>

    <h4>表单验证，与 Element Plus API 相同</h4>

    <sc-form :schema="schemaValidate" v-model="model5"></sc-form>
    <p>{{ JSON.stringify(model5) }}</p>

    <h4>动态增减表单项，并响应复杂结构的model</h4>

    <sc-form :schema="schemaDynamic" v-model="model6"></sc-form>
    <p>{{ JSON.stringify(model6) }}</p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { cloneDeep, set } from 'lodash-es';

// 表单schema，可以独立储存在其它地方作为公用
const schema = {
  formItems: [
    {
      type: 'input',
      label: '名字',
      placeholder: '请输入名字',
      field: 'name'
    },
    {
      type: 'select',
      label: '年龄',
      field: 'age',
      options: [{
        label: '十八',
        value: 18
      }, {
        label: '二十',
        value: 20
      }]
    },
    {
      type: 'radio',
      label: '意见',
      field: 'agree',
      options: [{
        label: '同意',
        value: 1
      }, {
        label: '不同意',
        value: 2
      }]
    },
    {
      type: 'checkbox',
      label: '喜欢',
      field: 'like',
      options: [{
        label: '草莓',
        value: 1
      }, {
        label: '苹果',
        value: 2
      }, {
        label: '西瓜',
        value: 3
      }, {
        label: '芒果',
        value: 4
      }]
    }
  ]
}
// 按钮schema
const btnSchema = {
  inline: true,
  formItems: [
    {
      type: 'button',
      content: '搜索',
      size: 'small',
      subtype: 'primary',
      on: {
        click: $event => {
          console.log('onSearch', $event);
        }
      }
    }, {
      type: 'button',
      content: '重置',
      size: 'small',
      plain: true,
      on: {
        click: $event => {
          console.log('onReset', $event);
        }
      }
    }
  ]
};

defineOptions({
  name: 'Example4',
});

const name = ref('kris');
const age = ref(18);
const model2 = ref({
  name: 'kris',
  age: 18,
  agree: 1,
  like: [1, 2]
});
const model3 = ref({ name: 'kkk1' });
const model4 = ref({});
const model5 = ref({});
const model6 = ref({ addresses: [{ value: '' }] }); // 支持复杂model
const queryModel = ref({ name: '' });
const schema2 = cloneDeep(schema); // 需要cloneDeep复制一份独立schema
const schema3 = cloneDeep(schema);
const model3Form = ref(null);
const queryForm = ref(null);
const schemaBind = {
  get name() {
    return name.value;
  },
  set name(value) {
    name.value = value;
  },
  get age() {
    return age.value;
  },
  set age(value) {
    age.value = value;
  },
};

const schema1 = computed(() => ({
  bind: schemaBind,
  formItems: [{
    label: '名字',
    items: [{
      type: 'input',
      field: 'name',
      model: name.value,
      placeholder: '请选择输入名字',
      on: {
        change() {
          console.log('change');
        },
        input() {
          console.log('input');
        }
      }
    }]
  }, {
    label: '年龄',
    type: 'input-number',
    field: 'age',
    model: age.value,
    placeholder: '请选择年龄',
    options: [{
      label: '十八',
      value: 18
    }, {
      label: '二十',
      value: 20
    }],
    props: {
      label: 'label',
      value: 'value'
    },
  }]
}));

const schema4 = computed(() => {
  // 先复制
  const mySchema = cloneDeep(schema);
  // 编辑schema
  set(mySchema, 'formItems[0].placeholder', '请输入你的大名');
  set(mySchema, 'formItems[0].on', {
    focus() {
      console.log('focus!');
    }
  });
  // 也可以用Object.assign编辑
  Object.assign(mySchema.formItems[0].on, {
    input(value) {
      console.log(value);
    }
  });
  // 插入一个form item
  mySchema.formItems.splice(1, 0, {
    type: 'input',
    label: '小名',
    field: 'nickName',
    placeholder: '输入你的小名',
  });

  return mySchema;
});

const schemaGroup = computed(() => {
  const { formItems } = cloneDeep(schema);
  const { formItems: btnItems } = cloneDeep(btnSchema);
  console.log(formItems, 'btnItems', btnItems);

  // 组合schema/btnSchema生成新schema
  return {
    inline: true,
    formItems: [
      formItems[0],
      formItems[1],
      ...btnItems,
    ]
  };
});

const schemaButtonGroup = computed(() => ({
  inline: true,
  formItems: [
    {
      type: 'input',
      label: '名字',
      field: 'name',
      placeholder: '请输入名字',
    },
    {
      items: [
        {
          type: 'button',
          content: '搜索',
          size: 'small',
          subtype: 'primary',
          on: {
            click() {
              console.log('onSearch', queryModel.value);
            }
          }
        },
        {
          type: 'button',
          content: '重置',
          size: 'small',
          plain: true,
          on: {
            click() {
              queryForm.value.reset();
            }
          }
        }
      ]
    }
  ]
}));

const schemaValidate = computed(() => {
  const { formItems: btnItems } = cloneDeep(btnSchema);
  return {
    inline: true,
    formItems: [
      {
        label: '年龄',
        type: 'input.number',
        field: 'age',
        rules: [
          { required: true, message: '年龄不能为空' },
          { type: 'number', message: '年龄必须为数字值' }
        ],
      },
      ...btnItems,
    ]
  };
});

const dynamicItems = computed(() => model6.value.addresses.map((item, i) => ({
  label: `地址${i}`,
  prop: `addresses[${i}].value`,
  items: [
    {
      type: 'input',
      field: `addresses[${i}].value`,
    }, {
      type: 'button',
      content: '删除',
      style: 'marginLeft: 10px',
      on: {
        click() {
          model6.value.addresses.splice(i, 1);
        }
      }
    }
  ],
})));

const schemaDynamic = computed(() => ({
  formItems: [
    ...dynamicItems.value,
    {
      type: 'button',
      subtype: 'primary',
      content: '新增',
      on: {
        click() {
          model6.value.addresses.push({ value: '' });
        }
      }
    }
  ]
}));
</script>
<style>
.schema-demo .el-form-item__content>.el-input {
  width: 216px;
}
.tips {
  font-size: 12px;
  color: #999;
  margin: 20px 0;
}
</style>
