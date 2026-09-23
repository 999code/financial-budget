# sc-form


## 1. 简介

sc-form 是一个支持 JSON schema 配置式生成页面表单的组件（基于 Element Plus），可以认为它是 Element Plus 表单组件及其它组件的 JSON 配置版本。它的特性有：

- 纯JSON配置化构建整个表单
- 接近 0 自定义api字段，上手成本低
- 拥有 Element Plus 表单及表单控件的特性（支持其属性及事件）
- 支持绑定多个复杂model
- 支持字段标签、文本、自定义组件、插槽等
- 加强定制了某些内容，支持全局配置
- 为复杂的 UI 提供col span布局支持
- 拥有 Javascript 完全编程能力


## 2. 例子
- **一个简单双向绑定表单**

```
<template>
	<sc-form  
        v-model="model"
        :schema="schema"
    />
</template>

<script>
export default {
	data() {
    	return {
        	model: {},
        	schema: {
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
           }
       }
   }
}
</script>

```

![image](http://team.3dxtyun.com/uploads/picture/40/202401/f804688eb2df15c493dc6876a1b0dff4.png)

上面完成了一个简单的双向绑定例子，schema 中的 ```showPassword```、```placeholder``` 等和对应的 Element Plus 表单控件属性一一对应，其中可以省略模板中的 ```v-model="model"``` 定义，统一在 schema 中定义 model，例如：
```
<template>
    <sc-form :schema="schema" />
</template>

<script>
export default {
    data() {
        return {
            model: {} // 定义表单model
        }
    },
    computed: {
    	schema() {
			return {
            	inline: true,
                model: this.model, // 这里绑定表单model
                formItems: [
                	...
                ]
            }
        }
    }
}
</script>
```

上面2种写法实现了同样的效果，注意后面一种写法的 schema 需要在 computed 中定义，因为它依赖了组件中的```this.model```。

实际项目中建议 schema 全部在 computed 中定义，因为表单中的控件往往需要依赖后端的数据来渲染，例如 select options、cascader等。

- **设置表单默认值**

```
export default {
    data() {
        return {
            model: { // model中的属性一一对应schema中的field名字
            	name: 'kris', // 这里为name字段设置默认值kris
            }
        }
    },
    computed: {
        schema() {
            return {
                inline: true,
                model: this.model,
                formItems: [
                    {
                      type: 'input',
                      label: '名字',
                      field: 'name',
                      placeholder: '请输入名字'
                    },
                    ...
                ]
            }
        }
    }
}
```


![image](http://team.3dxtyun.com/uploads/picture/40/202401/87325d12436143ba695b2c42b894eb0f.png)

- **绑定多个model并验证表单某个字段**

```
<template>
  <div>
    <sc-form :schema="schema" />
    <p>model: {{ JSON.stringify(model) }}</p>
    <p>likes: {{ JSON.stringify(likes) }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      model: {},
      likes: [],
    }
  },
  computed: {
    schema() {
      return {
        bind: this, // 多个model需要绑定当前组件this
        inline: true,
        model: this.model, // 整个表单的model
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
            rules: [ // 字段验证规则，API 与 Element Plus Form 一致
              { required: true, message: '年龄不能为空' },
              { type: 'number', message: '年龄必须为数字值' }
            ]
          },
          {
            type: 'checkbox',
            label: '喜好',
            model: this.likes, // 此字段独立绑定一个model
            field: 'likes', // 此field名字跟model名字保持一致
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
      }
    }
  }
}
</script>
```


![image](http://team.3dxtyun.com/uploads/picture/40/202401/a9c4af7891967ffec63d4c56355b3c3d.jpg)

>  注意：当表单有设置rules验证时，除非输入值全是字符串（如上例），否则应该尽量设置model具体field的初始值而不是一个空对象，因为如果是空对象组件会赋值一个默认的值（例如空数组）可能会导致el-form触发了验证或导致验证不正确。

- **同一份schema根据不同model生成独立表单**


```
<template>
  <div>
    <sc-form :schema="schema1" />
    <sc-form :schema="schema2" />
    <p>model1: {{ JSON.stringify(model1) }}</p>
    <p>model2: {{ JSON.stringify(model2) }}</p>
  </div>
</template>

<script>
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

export default {
  data() {
    return {
      model1: {},
      model2: {},
    }
  },
  computed: {
    schema1() {
      return {
        inline: true,
        model: this.model1, // 这里绑定表单model1
        ...cloneDeep(schema)
      }
    },
    schema2() {
      return {
        inline: true,
        model: this.model2, // 这里绑定表单model2
        ...cloneDeep(schema)
      }
    }
  }
}
</script>
```

![image](http://team.3dxtyun.com/uploads/picture/40/202401/fdad64a813c3aaa51be7364ce47fd1ac.jpg)

注意：需要引入lodash库的cloneDeep方法来深度复制schema，如果只是简单assign复制或解构复制可能会影响另外的表单，除非schema仅供一个表单使用。

- **绑定多个事件并使用title、slot等扩展功能**


```
<template>
  <div>
    <sc-form ref="form" :schema="schema">
      <template #age-slot>
        <el-input v-model.number="model.age" />
      </template>
    </sc-form>
    <p>model: {{ JSON.stringify(model) }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      model: {},
    }
  },
  computed: {
    schema() {
      return {
        bind: this, // 绑定当前组件this以使事件中能访问组件的数据及方法
        inline: true,
        model: this.model, // 这里绑定表单model
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
            label: "年龄",
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
                this.$refs.form.elForm.resetFields(); // elForm属性获得el-form组件实例，并使用它的方法resetFields
              }
            }
          },
        ]
      }
    }
  }
}
</script>
```

![image](http://team.3dxtyun.com/uploads/picture/40/202401/b1484695ee2362a43fa9ad77234943ce.jpg)

- **多列布局col、span、gutter**


```
<template>
  <div>
    <sc-form :schema="schema" />
    <p>model: {{ JSON.stringify(model) }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      model: {},
    }
  },
  computed: {
    schema() {
      return {
        model: this.model, // 这里绑定表单model
        labelPosition: 'left',
        labelWidth: '50px',
        colSpan: 8, // col 布局，同 Element Plus，默认 24
        gutter: 20, // 栅格 col 间隔，同 Element Plus，单位 px，默认 0
        formItems: [
          {
            type: 'title', // 使用表单title
            content: '示例表单'
          },
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
          {
            type: 'input',
            label: '地址',
            field: 'addr',
            placeholder: '请输入地址',
          },
        ]
      }
    }
  }
}
</script>
```

![image](http://team.3dxtyun.com/uploads/picture/40/202401/986c81da338c1d62ce81936c05468454.jpg)


更多demo示例下载 >>> [sc-form example](https://github.com/koen301/schema-creator/tree/master/element-ui/example)


## 3. Form Attributes

参数 | 说明 | 类型
---|---|---
schema | 表单 schema 配置 | object
v-model | 表单双向绑定的model，注意如果在 schema 中也配置了 model，schema 优先 | object
setting | 表单的默认配置，包含el-form及el-input，el-select等表单控件配置，可全局覆盖 | object

## 4. schema 配置

schema 对象最顶层的配置对应 el-form 表单配置，支持 Element Plus el-form 的属性及事件配置（注意需要驼峰写法，例如 ```label-position``` 需要写成 ```labelPosition```），额外提供了下面属性：

参数 | 说明 | 类型 | 默认值
---|---|---|---
bind | 表单需要绑定的上下文对象，一般为当前组件```this```，其作用有：<br/>1. 绑定表单事件中上下文```this```指向当前组件，这样在事件中可以方便的访问组件的属性及方法；<br/>2. 在formItems中自定义model时需要绑定```this```，否则不生效；<br/>如果没有使用上述功能，可以省略此设置 | Vue组件实例 | -
model | 表单双向绑定的对象数据，作用与```v-model```一致 | object | -
on | 定义el-form表单事件（事件同样需要驼峰式写法） | object | -
formItems | 定义el-form表单中的具体控件，详细看"formItems 表单项配置" | array | -
colSpan | 表单 Layout 布局中栅格占据的列数，具体参考 Element Plus Layout 布局（表单 inline 为 true 时此设置无效） | number | 24
gutter | 栅格 col 间隔，具体参考 Element Plus Layout 布局 | number | 0

## 5. formItems 表单项配置

```formItems``` 对应 el-form-item 数组，为了更简单地配置表单项，form-item 和 Element Plus 表单控件（例如 input、select 等）默认合并配置。

例如```label```实际上是配置 form-item 的```label```属性，类似还有```class，style，rules```，除了这4项，其它所有配置均是 form控件配置。

如果想独立 form-item 和 form控件配置，需要加一个```items```属性来区分配置 form-item 及 form控件，见下示例。

除了支持 Element Plus form-item 和表单控件属性，额外提供了下面属性：

参数 | 说明 | 类型 | 默认值
---|---|---|---
type | type 表单控件的类型，支持 Element Plus 表单控件，例如 el-input、el-select、el-cascader、el-upload 等<br>另外常用的 el-button、el-dropdown 非表单控件也提供了支持，注意名称需要去掉前缀 `el-`，例如 el-date-picker 的 type 为 ```'date-picker'```<br>另外提供了 type 为 ```text、html、slot、title、component``` 的支持，方便生成更多自定义内容，具体配置见“form 控件配置”<br>同时支持类似 Vue 原生 v-model 指令的修饰符：```.lazy```、```.number```、```.trim```，例如声明 ```type: 'input.number'``` 则会将输入值转换为数字类型 | string | -
field | 双向绑定的字段名称，对应上面 model 对象的字段（注意与 form-item 组件属性 prop 的区别，独立配置需要 prop 与组件的 field 字段同时赋值，这样才能使它的校验生效；合并配置则可以省略 prop，因为程序会把 form 控件的 field 值同时赋值给 form-item 的 prop 属性，以使配置更简洁）<br>支持响应`field：'items[0].name'`这种复杂结构 model 写法，但建议构建简单 model。 | string | -
model | 需要独立双向绑定的一个数据(不同于表单配置的model对象)，可以定义这个，同时 field 字段名称需要改成一致，例如绑定`this.otherFormData`，field 则是```'otherFormData'``` | string / number / boolean / object / array | -
subtype | 如果控件自身也有 type 属性，可以配置此项表示 Element Plus 控件的原生 type 属性，例如配置 el-button 控件的 ```type: 'primary'``` | string | -
on | 定义控件的事件，支持 Element Plus 官方所有事件，具体查看官方表单控件 API。<br>另外支持 el-input 控件的 ```keyup``` 及 ```keyup.enter``` 事件，配置为 ```{'keyup.enter'() { ...code }}``` | object | -
items | 独立控件配置，可以是对象也可以是数组（数组即内联inline生成多个表单控件）具体配置同上 | object / array | -
    
## 6. Form 控件配置

> schema 配置的 form 控件支持 Element Plus 属性及事件，下面列出额外支持或有别于官方的属性、方法和控件。

- select

参数 | 说明 | 类型 | 默认值
---|---|---|---
options | 可选项数据源，键名可通过 Props 属性配置，支持子项配置 disabled 禁用某一项 | array | -
props | 配置选项，主要有 label，value 分别配置选项标签及选项值对应的数据键名 | object | {label: 'label', value: 'value'}

- radio

参数 | 说明 | 类型 | 默认值
---|---|---|---
button | 是否按钮样式的单选组合，相当于选项是 el-radio-button | boolean | false
options | 可选项数据源，子项键名 label，value 分别配置选项标签及选项值 | array | -

- checkbox

参数 | 说明 | 类型 | 默认值
---|---|---|---
button | 是否按钮样式的多选组合，相当于选项是 el-checkbox-button | boolean | false
options | 可选项数据源，子项键名 label，value 分别配置选项标签及选项值 | array | -

- text

参数 | 说明 | 类型 | 默认值
---|---|---|---
content | 文本内容 | string | -

- html

参数 | 说明 | 类型 | 默认值
---|---|---|---
content | html内容 | string | -

- slot

参数 | 说明 | 类型 | 默认值
---|---|---|---
name | 插槽名字 | string | -

- title

参数 | 说明 | 类型 | 默认值
---|---|---|---
content | 标题内容 | string | -

- component

> 注意 component 实际是 Vue 内置的 component 组件，支持官方提供的所有属性例如```is```, ```keep-alive```等，当然也支持其绑定的任意事件（is属性指定的组件）

参数 | 说明 | 类型 | 默认值
---|---|---|---
content | 组件包裹的内容 | string | -
        
## 7. Form Methods

方法名 | 说明 | 参数
---|---|---
getForm | 获取 el-form 实例，方便访问 el-form 的方法/属性<br>也可以直接通用 pl-table 实例的```elForm```属性访问  | -
getField | 获取对应 field 的表单控件实例，方便访问表单控件的方法/属性<br>也可以通过注入组件对象的 ```this.$fields``` 获得 sc-form 定义的所有 field 控件，再具体 field 名称访问其控件实例，例如```this.$fields.inputName.focus()```访问 el-input 的 focus 方法 | string (Field名)
reset | 重置 form 表单，与 el-form 方法 resetFields 类似，区别在于 reset 方法能兼容表单控件 model 都为无定义的状态，而官方 resetFields 在某些情况下则会异常，例如 checkbox-group 原始值无定义<br>不过为了保持一致性，尽量还是用官方 resetFields 方法 | -

- items 合并/独立控件配置示例


```
// form item及控件合并配置
...
formItems: [{
	type: 'input',
    label: '名字',
    field: 'name',
    placeholder: '请输入',
}],
...

// form item及控件独立配置，items可以是对象
...
formItems: [{
    label: '名字',
    items: {
    	type: 'input',
    	field: 'name',
    	placeholder: '请输入',
    }
}],
...

// form item及控件独立配置，items是数组，这样可以配置多个表单控件
...
formItems: [{
    label: '名字',
    items: [{
    	type: 'input',
    	field: 'name',
    	placeholder: '请输入',
    }]
}],
...
```



