## 1. 简介

- sc-table 是一个支持 JSON schema 配置式生成页面表格的组件（基于 Element Plus 的 el-table），可以认为它是 el-table 的 JSON 配置版本。
- sc-table 拥有 Element Plus el-table 的特性，并根据项目加强定制了某些内容，这样在项目中使用表格特别是处理复杂表格生成将变得异常简单。

## 2. 例子

- 基本例子

```
<template>
	<sc-table :schema="tableSchema"></sc-table>
</template>
<script>
export default {
	data() {
    	return {
        	// 表格列表数据
        	tableList: [{
            	index: 1,
                name: 'a1',
                lifecycleStatus: 1,
            }, {
            	index: 2,
                name: 'a2',
                lifecycleStatus: 3,
            }]
        }
    }
	computed: {
    	// 表格列表Schema
    	tableSchema() {
          return {
            // 绑定表格数据
            data: this.tableList,
            // 定义表格column
            columns: [{
              type: "selection",
              width: "55",
              align: "center",
              reserveSelection: true,
            }, {
              prop: "index",
              label: "序号",
              width: "120",
              align: "center",
            }, {
              prop: "name",
              label: "名称",
              minWidth: "350",
              align: "center",
              // 对应column中的template插槽
              template(scope) {
                return `<div class="white-space: pre-wrap;">${scope.row.name}</div>`;
              }
            }, {
              prop: "lifecycleStatus",
              label: "文档状态",
              width: "100",
              align: "center",
              template({row}) {
                let { lifecycleStatus } = row;
                lifecycleStatus = lifecycleStatus >=3 && lifecycleStatus < 5 ? 3 : lifecycleStatus;
                const statusMap = {
                  1: '创建编辑中',
                  2: '变更编辑中',
                  3: '审核中',
                  5: '恢复审核中',
                  6: '失效审核中',
                  7: '预淘汰',
                  8: '有效',
                  9: '失效',
                };
                return `<span>${statusMap[lifecycleStatus]}</span>`;
              }
            }]
          }
    	},
    }
}
</script>
```

> 上面 schema 中的 column 项属性和 el-table 官方属性一一对应（除了 ```template```），相关 API 查看 Element Plus 官方文档。

> ```template```属性是 sc-table 自定义属性方法，代表 column 中的 template 插槽，参数 scope 与官方插槽中的 scope 保持一致。```template```方法必须返回一个字符串代表渲染的模版，字符串模板可以使用自定义组件或任何其它标签，与Vue官方模版使用一致。

- 复杂例子

```
<template>
	<sc-table :schema="tableSchema"></sc-table>
</template>
<script>
export default {
	data() {
    	return {
        	// 表格列表数据
        	tableList: [{
            	index: 1,
                name: 'a1',
                lifecycleStatus: 1,
            }, {
            	index: 2,
                name: 'a2',
                lifecycleStatus: 3,
            }]
        }
    }
	computed: {
    	// 表格列表Schema
    	tableSchema() {
          return {
            // 绑定this组件
            bind: this,
            // 绑定表格数据
            data: this.tableList,
            // 定义表格column
            columns: [{
              type: "selection",
              width: "55",
              align: "center",
              reserveSelection: true,
            }, {
              prop: "index",
              label: "序号",
              width: "120",
              align: "center",
            }, {
              prop: "name",
              label: "名称",
              minWidth: "350",
              align: "center",
              // 对应column中的template插槽
              template(scope) {
                return `<div class="white-space: pre-wrap;">${scope.row.name}</div>`;
              }
            }, {
              prop: "operate",
              label: "操作",
              width: "180",
              fixed: "right",
              template(scope){
                //定义操作按钮
                const operationConfig = [{
                  name: '详情',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:DETAIL',
                }, {
                  name: '修改',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:MODIFY',
                  show: scope.row.lifecycleStatus === 1 || scope.row.lifecycleStatus === 2,
                }, {
                  name: '变更',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:CHANGE',
                  show: scope.row.lifecycleStatus === 8,
                  disabled: scope.row.lifecycleStatus === 8 && scope.row.changeFlag === 0,
                }, {
                  name: '关联关系',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:RELATION',
                }, {
                  name: '文件管理',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:FILE_MANAGEMENT',
                  show: scope.row.lifecycleStatus === 1 || scope.row.lifecycleStatus === 2,
                }, {
                  name: '签收',
                  click: () => this.handlerFn(scope.row),
                  hasPermission: 'WEB_PLM_PDM_ROOT_Document_DocumentList:SIGN',
                  show: scope.row.lifecycleStatus === 8,
                }];

                return {
                  data: {scope, operationConfig},
                  template: `
                    <div v-if="scope.row.status === 1">
                      <OperationButtons :data="operationConfig" />
                    </div>
                  `,
                }
              },
            }]
          }
    	},
    }
}
</script>
```

>  这里的 schema 绑定了当前组件 this 是为了方便 template 方法中访问当前组件的数据和方法，本例中直接访问了组件的```this.handlerFn```方法。

> 这里的 template 返回了一个对象，事实上它是一个简单版本的 Vue 组件对象，Vue 组件对象有 data 属性和 template 属性分别代表数据和模版，这里给此组件传递了```scope, operationConfig```2个数据，因此在它的模版中可以直接访问```scope```及```operationConfig```。

完整例子请参考项目文件 ```\src\components\page\series\doc\PlmDocMain.vue```

## 3. Table Attributes


> 注意：sc-table 继承 el-table 的所有属性和方法，下面为 sc-table 自定义的属性或方法。

参数 | 说明 | 类型
---|---|---
schema | 表格 schema | object
setting | 表格的默认配置，包含el-table及el-table-column配置，可全局覆盖 | object

## 4. Table Methods
方法名 | 说明 | 参数
---|---|---
getTable | 获取 el-table 实例，方便访问 el-table 的方法。也可以直接通用 sc-table 实例的```elTable```属性访问  | -
getSelection | 获取选中的数据行，也可以直接通用 sc-table 实例的```selection```属性访问 | -

## 5. Table Slot
name | 说明 | 参数
---|---|---
变量 | schema 中的 template 定义的名字对应的模板 | scope

#### 关于 schema 中的```template ```

schema 中的```template ```有3种生成方式：
1.  函数返回模版字符串(示例1)
2.  函数返回Vue组件对象(示例2)
3.  template名字

例如定义```template: 'nameTemplate'```，则代表它的template是在它的slot中，名字为'nameTemplate'的模版，这样就可以不影响schema情况下构建任意复杂的template内容。

- 例子：

```
<template>
	<sc-table :schema="tableSchema">
    	<template #nameTemplate="scope">
        	<div class="white-space: pre-wrap;">{{scope.row.name}}</div>
        </template>
    </sc-table>
</template>
<script>
export default {
	data() {
    	return {
        	// 表格列表数据
        	tableList: [{
            	index: 1,
                name: 'a1',
            }, {
            	index: 2,
                name: 'a2',
            }]
        }
    }
	computed: {
    	// 表格列表Schema
    	tableSchema() {
          return {
            // 绑定表格数据
            data: this.tableList,
            // 定义表格column
            columns: [{
              prop: "index",
              label: "序号",
              width: "120",
              align: "center",
            }, {
              prop: "name",
              label: "名称",
              minWidth: "350",
              align: "center",
              // 对应column中的template插槽
              template: 'nameTemplate',
            }]
          }
    	},
    }
}
</script>
```


