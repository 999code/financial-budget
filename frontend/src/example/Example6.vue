<template>
  <div class="example6">
    <h4>1. 基础用法：data + columns（属性与 Element Plus 一一对应）</h4>

    <sc-table :schema="schema1"></sc-table>

    <p class="tips">
      schema 中除 <code>columns</code>、<code>bind</code>、<code>on</code> 之外的属性都会透传给 el-table；
      columns 中除 <code>template</code> 之外的属性都会透传给 el-table-column，API 完全同官方文档。
      这里用 <code>height: 'auto'</code> 覆盖了组件默认的 <code>height: '100%'</code>。
    </p>

    <h4>2. template 的 3 种写法：模板字符串 / 组件对象 / 具名插槽</h4>

    <sc-table :schema="schema2">
      <template #nameSlot="scope">
        <div class="user-cell">
          <el-avatar :size="24">{{ scope.row.name?.charAt(0) }}</el-avatar>
          <span>{{ scope.row.name }}</span>
        </div>
      </template>
    </sc-table>

    <p class="tips">
      ① 函数返回模板字符串（状态列，模板中可直接访问 <code>scope</code> 与 <code>bind</code>）；<br />
      ② 函数返回 Vue 组件对象（操作列，用 <code>methods</code> 绑定当前组件的方法）；<br />
      ③ template 写成字符串（姓名列），对应外部同名插槽，适合结构特别复杂的单元格。<br />
      注意：el-table-column 会用空行对象（<code>row = {}</code>）预渲染一次列内容，
      因此 template / 插槽中对行数据取值时要做好兜底，避免调用 <code>charAt</code>、解构等方法时报错。
    </p>

    <h4>3. 多选、单行高亮与实例方法 getSelection / getTable</h4>

    <sc-table ref="table3" :schema="schema3"></sc-table>

    <div class="btn-group">
      <el-button size="small" type="primary" @click="onGetSelection">获取选中行</el-button>
      <el-button size="small" @click="onClearSelection">清空选中</el-button>
      <el-button size="small" @click="onToggleRow">选中第 2 行</el-button>
      <el-button size="small" @click="onSetCurrent">高亮第 3 行</el-button>
    </div>
    <p>已选：{{ selectionNames.join('、') || '（空）' }}</p>

    <h4>4. 表格事件：schema.on（函数中的 this 指向 schema.bind）</h4>

    <sc-table :schema="schema4"></sc-table>

    <ul class="event-logs">
      <li v-for="(log, i) of logs" :key="i">{{ log }}</li>
    </ul>

    <h4>5. 常用列配置与动态列：sortable / formatter / fixed / tooltip</h4>

    <el-checkbox-group v-model="visibleColumns" size="small">
      <el-checkbox v-for="col of columnOptions" :key="col.value" :value="col.value">
        {{ col.label }}
      </el-checkbox>
    </el-checkbox-group>

    <sc-table :schema="schema5"></sc-table>

    <p class="tips">
      columns 是响应式数组，直接增删即可实现动态列；<code>sortable</code> 排序、<code>formatter</code> 格式化、
      <code>fixed</code> 固定列、<code>showOverflowTooltip</code> 溢出提示均为 el-table-column 原生属性。
    </p>

    <h4>6. setting 覆盖组件默认配置（无边框 / 斑马纹 / 左对齐 / 固定高度滚动）</h4>

    <div class="table-box">
      <sc-table :schema="schema6" :setting="setting6"></sc-table>
    </div>

    <p class="tips">
      setting 包含 <code>table</code> 与 <code>column</code> 两部分默认值，schema 中的同名配置优先级更高，
      适合在项目里统一全局配置后再按需覆盖。
    </p>

    <h4>7. 合并单元格 spanMethod 与树形数据 treeProps</h4>

    <sc-table :schema="schema7"></sc-table>

    <sc-table :schema="schema8"></sc-table>

    <p class="tips">
      spanMethod 可直接通过闭包访问 setup 中的响应式状态；树形数据需要 <code>rowKey</code> 与 <code>treeProps</code>，
      组件默认开启了 <code>defaultExpandAll</code>，传 <code>false</code> 可关闭。
    </p>

    <h4>8. 综合示例：sc-form 查询 + loading + 分页</h4>

    <sc-form :schema="schemaQuery"></sc-form>

    <sc-table v-loading="loading" :schema="schema9"></sc-table>

    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="resultList.length"
      layout="total, prev, pager, next"
      @current-change="onPageChange"
    ></el-pagination>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus';
import { computed, reactive, ref } from 'vue';

// 状态字典，可抽离成公用的枚举文件
const STATUS_MAP = {
  1: { label: '在职', type: 'success' },
  2: { label: '试用', type: 'warning' },
  3: { label: '离职', type: 'info' },
};

// 表格列的候选配置，配合 checkbox 实现动态列
const COLUMN_MAP = {
  dept: { prop: 'dept', label: '部门', width: '120' },
  position: { prop: 'position', label: '岗位', minWidth: '160' },
  salary: {
    prop: 'salary',
    label: '月薪',
    width: '120',
    sortable: true,
    formatter: row => `¥${Number(row.salary).toLocaleString()}`,
  },
  entryDate: { prop: 'entryDate', label: '入职日期', width: '140', sortable: true },
  address: { prop: 'address', label: '地址', minWidth: '240', showOverflowTooltip: true },
};

defineOptions({
  name: 'Example6',
});

const employees = [{
  id: 1,
  name: '张三',
  dept: '技术部',
  position: '前端工程师',
  status: 1,
  salary: 18000,
  entryDate: '2021-03-01',
  address: '上海市浦东新区张江高科技园区博云路 2 号',
}, {
  id: 2,
  name: '李四',
  dept: '技术部',
  position: '后端工程师',
  status: 1,
  salary: 20000,
  entryDate: '2020-07-15',
  address: '上海市徐汇区漕河泾开发区宜山路 700 号',
}, {
  id: 3,
  name: '王五',
  dept: '产品部',
  position: '产品经理',
  status: 2,
  salary: 16000,
  entryDate: '2022-01-04',
  address: '北京市海淀区中关村软件园二期',
}, {
  id: 4,
  name: '赵六',
  dept: '产品部',
  position: '交互设计师',
  status: 3,
  salary: 12000,
  entryDate: '2019-05-20',
  address: '广州市天河区珠江新城华夏路 10 号',
}, {
  id: 5,
  name: '孙七',
  dept: '市场部',
  position: '市场专员',
  status: 2,
  salary: 9000,
  entryDate: '2023-09-01',
  address: '深圳市南山区科技园粤海街道',
}];
const statusOptions = [
  { label: '在职', value: 1 },
  { label: '试用', value: 2 },
  { label: '离职', value: 3 },
];
const visibleColumns = ref(['dept', 'position', 'salary', 'entryDate', 'address']);
const columnOptions = [
  { label: '部门', value: 'dept' },
  { label: '岗位', value: 'position' },
  { label: '月薪', value: 'salary' },
  { label: '入职日期', value: 'entryDate' },
  { label: '地址', value: 'address' },
];
const selectionNames = ref([]);
const logs = ref([]);
const setting6 = {
  table: {
    border: false,
    stripe: true,
    height: '100%', // 外层 .table-box 给定高度，表格内部滚动
  },
  column: {
    align: 'left',
  },
};
const treeData = [{
  id: 1,
  name: '技术部',
  leader: '张三',
  count: 12,
  children: [{
    id: 11,
    name: '前端组',
    leader: '张三',
    count: 5,
  }, {
    id: 12,
    name: '后端组',
    leader: '李四',
    count: 7,
  }],
}, {
  id: 2,
  name: '产品部',
  leader: '王五',
  count: 6,
  children: [{
    id: 21,
    name: '产品设计组',
    leader: '王五',
    count: 4,
  }, {
    id: 22,
    name: '交互设计组',
    leader: '赵六',
    count: 2,
  }],
}];
const query = reactive({
  name: '',
  status: '',
});
const loading = ref(false);
const resultList = ref([...employees]);
const currentPage = ref(1);
const pageSize = 4;
const table3 = ref(null);

function statusMeta(status) {
  return STATUS_MAP[status] || { label: '未知', type: 'info' };
}

function pushLog(log) {
  logs.value.unshift(new Date().toLocaleTimeString() + ' ' + log);
  logs.value = logs.value.slice(0, 5); // 只保留最近 5 条
}

function onEdit(row) {
  ElMessage.success('编辑：' + row.name);
}

function onDelete(row) {
  ElMessage.warning('删除：' + row.name);
}

const schemaBind = {
  statusMeta,
  pushLog,
  onEdit,
  onDelete,
};

function onGetSelection() {
  selectionNames.value = table3.value.getSelection().map(item => item.name);
}

function onClearSelection() {
  table3.value.getTable().clearSelection();
  selectionNames.value = [];
}

function onToggleRow() {
  table3.value.getTable().toggleRowSelection(employees[1]);
}

function onSetCurrent() {
  table3.value.getTable().setCurrentRow(employees[2]);
}

function onSearch() {
  loading.value = true;
  // 模拟接口请求
  setTimeout(() => {
    const { name, status } = query;
    resultList.value = employees.filter(item => {
      const matchName = !name || item.name.includes(name);
      const matchStatus = status === '' || status === undefined || item.status === status;
      return matchName && matchStatus;
    });
    currentPage.value = 1;
    loading.value = false;
  }, 500);
}

function onReset() {
  query.name = '';
  query.status = '';
  resultList.value = [...employees];
  currentPage.value = 1;
}

function onPageChange(page) {
  currentPage.value = page;
}

const schema1 = computed(() => ({
  data: employees,
  height: 'auto',
  columns: [{
    type: 'index',
    label: '#',
    width: '60',
  }, {
    prop: 'name',
    label: '姓名',
    width: '100',
  }, {
    prop: 'dept',
    label: '部门',
    width: '100',
  }, {
    prop: 'position',
    label: '岗位',
    minWidth: '160',
  }, {
    prop: 'salary',
    label: '月薪',
    width: '120',
    template(scope) {
      return '<span class="salary">¥' + Number(scope.row.salary || 0).toLocaleString() + '</span>';
    },
  }, {
    prop: 'entryDate',
    label: '入职日期',
    width: '140',
  }],
}));

const schema2 = computed(() => ({
  bind: schemaBind,
  data: employees,
  height: 'auto',
  columns: [{
    prop: 'name',
    label: '姓名（插槽）',
    width: '160',
    align: 'left',
    template: 'nameSlot',
  }, {
    prop: 'status',
    label: '状态（模板字符串）',
    width: '160',
    template() {
      return `<el-tag :type="bind.statusMeta(scope.row.status).type" size="small">
        {{ bind.statusMeta(scope.row.status).label }}
      </el-tag>`;
    },
  }, {
    prop: 'position',
    label: '岗位',
    minWidth: '160',
  }, {
    prop: 'operate',
    label: '操作（组件对象）',
    width: '160',
    fixed: 'right',
    template(scope) {
      return {
        data: {
          row: scope.row,
        },
        methods: {
          onEdit: () => this.onEdit(scope.row),
          onDelete: () => this.onDelete(scope.row),
        },
        template: `
          <el-button link type="primary" size="small" @click="onEdit()">编辑</el-button>
          <el-button link type="danger" size="small" :disabled="row.status === 3" @click="onDelete()">删除</el-button>
        `,
      };
    },
  }],
}));

const schema3 = computed(() => ({
  data: employees,
  height: 'auto',
  highlightCurrentRow: true,
  columns: [{
    type: 'selection',
    width: '55',
    reserveSelection: true,
  }, {
    prop: 'name',
    label: '姓名',
    width: '100',
  }, {
    prop: 'dept',
    label: '部门',
    minWidth: '120',
  }, {
    prop: 'position',
    label: '岗位',
    minWidth: '160',
  }],
}));

const schema4 = computed(() => ({
  bind: schemaBind,
  data: employees,
  height: 'auto',
  on: {
    'row-click'(row, column) {
      this.pushLog('row-click：' + row.name + '（列：' + (column?.label || '-') + '）');
    },
    'cell-click'(row, column) {
      this.pushLog('cell-click：' + column?.property + ' = ' + row[column?.property]);
    },
    'sort-change'({ column, order }) {
      this.pushLog('sort-change：' + (column ? column.label : '-') + ' ' + (order || '默认'));
    },
    'current-change'(currentRow) {
      this.pushLog('current-change：' + (currentRow ? currentRow.name : '无'));
    },
  },
  columns: [{
    prop: 'name',
    label: '姓名（点击行）',
    width: '140',
  }, {
    prop: 'salary',
    label: '月薪（排序）',
    width: '140',
    sortable: true,
  }, {
    prop: 'entryDate',
    label: '入职日期（排序）',
    minWidth: '160',
    sortable: true,
  }],
}));

const schema5 = computed(() => ({
  data: employees,
  height: 'auto',
  columns: [{
    prop: 'name',
    label: '姓名',
    width: '100',
    fixed: 'left',
  },
  ...visibleColumns.value.map(key => COLUMN_MAP[key]),
  {
    prop: 'operate',
    label: '操作',
    width: '120',
    fixed: 'right',
    template() {
      return '<el-button link type="primary" size="small">详情</el-button>';
    },
  }],
}));

const schema6 = computed(() => {
  const list = [];
  // 造多一点数据，方便看到固定高度下的内部滚动
  for (let i = 0; i < 3; i++) {
    employees.forEach(item => {
      list.push({
        ...item,
        id: i + '-' + item.id,
        name: item.name + (i + 1),
      });
    });
  }
  return {
    data: list,
    columns: [{
      type: 'index',
      label: '#',
      width: '60',
    }, {
      prop: 'name',
      label: '姓名',
      width: '120',
    }, {
      prop: 'dept',
      label: '部门',
      width: '120',
    }, {
      prop: 'position',
      label: '岗位',
      minWidth: '160',
    }, {
      prop: 'entryDate',
      label: '入职日期',
      minWidth: '160',
    }],
  };
});

const deptSpans = computed(() => {
  const spans = [];
  let pos = 0;
  employees.forEach((row, index) => {
    if (index === 0) {
      spans.push(1);
      pos = 0;
    } else if (row.dept === employees[index - 1].dept) {
      spans[pos] += 1;
      spans.push(0);
    } else {
      spans.push(1);
      pos = index;
    }
  });
  return spans;
});

const schema7 = computed(() => ({
  data: employees,
  height: 'auto',
  spanMethod: ({ columnIndex, rowIndex }) => {
    if (columnIndex === 0) {
      const rowspan = deptSpans.value[rowIndex];
      return {
        rowspan,
        colspan: rowspan > 0 ? 1 : 0,
      };
    }
    return undefined;
  },
  columns: [{
    prop: 'dept',
    label: '部门（合并）',
    width: '120',
  }, {
    prop: 'name',
    label: '姓名',
    width: '120',
  }, {
    prop: 'position',
    label: '岗位',
    minWidth: '160',
  }],
}));

const schema8 = computed(() => ({
  data: treeData,
  height: 'auto',
  rowKey: 'id',
  treeProps: { children: 'children' },
  defaultExpandAll: true,
  columns: [{
    prop: 'name',
    label: '组织',
    minWidth: '240',
    align: 'left',
  }, {
    prop: 'leader',
    label: '负责人',
    width: '120',
  }, {
    prop: 'count',
    label: '人数',
    width: '100',
  }],
}));

const schemaQuery = computed(() => ({
  inline: true,
  model: query,
  formItems: [{
    type: 'input',
    label: '姓名',
    field: 'name',
    placeholder: '请输入姓名',
  }, {
    type: 'select',
    label: '状态',
    field: 'status',
    clearable: true,
    placeholder: '全部',
    options: statusOptions,
  }, {
    type: 'button',
    content: '搜索',
    subtype: 'primary',
    on: {
      click: onSearch,
    },
  }, {
    type: 'button',
    content: '重置',
    plain: true,
    on: {
      click: onReset,
    },
  }],
}));

const pageList = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return resultList.value.slice(start, start + pageSize);
});

const schema9 = computed(() => ({
  data: pageList.value,
  height: 'auto',
  columns: [{
    prop: 'name',
    label: '姓名',
    width: '100',
  }, {
    prop: 'dept',
    label: '部门',
    width: '120',
  }, {
    prop: 'position',
    label: '岗位',
    minWidth: '160',
  }, {
    prop: 'status',
    label: '状态',
    width: '100',
    template(scope) {
      const { label, type } = STATUS_MAP[scope.row.status] || {};
      return '<el-tag type="' + (type || 'info') + '" size="small">' + (label || '-') + '</el-tag>';
    },
  }, {
    prop: 'entryDate',
    label: '入职日期',
    minWidth: '140',
  }],
}));
</script>

<style scoped>
.example6 {
  background-color: #fff;
  padding: 20px;
  margin: 0 20px;
  border-radius: 4px;
}
.tips {
  font-size: 12px;
  color: #909399;
  line-height: 22px;
  margin: 16px 0 40px;
}
.tips code {
  background-color: #f5f7fa;
  padding: 1px 4px;
  border-radius: 2px;
  color: #409eff;
}
.btn-group {
  margin-top: 16px;
}
.user-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.event-logs {
  margin: 16px 0 40px;
  padding: 10px 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
  line-height: 22px;
  min-height: 30px;
}
.table-box {
  height: 260px;
}
/* 运行时编译的 template 内容不带 scoped 标记，需要用 :deep 穿透 */
:deep(.salary) {
  color: #f56c6c;
  font-weight: 500;
}
.el-pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>
