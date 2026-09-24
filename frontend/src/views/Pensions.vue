<template>
  <div class="pensions">
    <!-- 搜索：人员 / 时间 / 人员分类 -->
     <el-card>
       <search-form :schema="searchSchema" @search="load" @reset="onReset" />
     </el-card>

    <!-- 汇总卡片 -->
     <el-card style="margin: 16px 0;">
       <div class="stats">
         <div class="stat-card">
           <div class="stat-card__label">领取合计</div>
           <div class="stat-card__value income">¥ {{ money(stats.income_total) }}</div>
         </div>
         <div class="stat-card">
           <div class="stat-card__label">缴费合计</div>
           <div class="stat-card__value expense">¥ {{ money(stats.expense_total) }}</div>
         </div>
         <div class="stat-card">
           <div class="stat-card__label">净额</div>
           <div class="stat-card__value" :class="stats.net >= 0 ? 'income' : 'expense'">
             ¥ {{ money(stats.net) }}
           </div>
         </div>
         <div class="stat-card">
           <div class="stat-card__label">记录数</div>
           <div class="stat-card__value">{{ stats.count }}</div>
         </div>
       </div>
     </el-card>
    <el-card>
      <div class="toolbar">
        <div class="toolbar__left">
          <el-button type="primary" :icon="Plus" @click="openCreate">新增记录</el-button>
          <el-button :icon="User" @click="openPersons">人员档案</el-button>
          <el-button :icon="Setting" @click="openParams">参数设置</el-button>
        </div>
        <el-tooltip content="刷新列表" placement="top">
          <el-button :icon="Refresh" :loading="loading" @click="load" />
        </el-tooltip>
      </div>
  
      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="person_name" label="人员" min-width="110" show-overflow-tooltip />
        <el-table-column label="时间" width="120">
          <template #default="{ row }">{{ row.occurred_on || row.period_month }}</template>
        </el-table-column>
        <el-table-column label="分类" width="140">
          <template #default="{ row }">
            <el-tag :type="schemeTagType(row.scheme)" size="small">{{ row.scheme_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="方向" width="90">
          <template #default="{ row }">
            <el-tag
              :type="row.direction === 'income' ? 'danger' : 'success'"
              size="small"
              effect="plain"
            >
              {{ row.direction_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="收支金额" width="140" align="right">
          <template #default="{ row }">
            <span :class="row.direction === 'income' ? 'income' : 'expense'">
              {{ row.direction === 'income' ? '+' : '-' }} ¥ {{ money(row.amount) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" min-width="120" show-overflow-tooltip>
          <template #default="{ row }">{{ row.note || '-' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openView(row)">查看</el-button>
            <el-button link type="primary" @click="openEdit(row)">修改</el-button>
            <el-button link type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <span class="empty-text">暂无记录，请先维护人员档案后再点击「新增记录」</span>
        </template>
      </el-table>
  
      <el-collapse class="collapse-block">
        <el-collapse-item title="按月统计" name="month">
          <el-table :data="stats.month_stats" size="small" border>
            <el-table-column prop="month" label="月份" width="120" />
            <el-table-column label="领取" align="right">
              <template #default="{ row }">
                <span class="income">¥ {{ money(row.income) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="缴费" align="right">
              <template #default="{ row }">
                <span class="expense">¥ {{ money(row.expense) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="净额" align="right">
              <template #default="{ row }">
                <span :class="row.net >= 0 ? 'income' : 'expense'">¥ {{ money(row.net) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="条数" width="90" align="right" />
          </el-table>
          <el-table :data="stats.scheme_stats" size="small" border class="scheme-table">
            <el-table-column label="人员分类" width="140">
              <template #default="{ row }">
                <el-tag :type="schemeTagType(row.scheme)" size="small">{{ row.scheme_text }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="领取" align="right">
              <template #default="{ row }">
                <span class="income">¥ {{ money(row.income) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="缴费" align="right">
              <template #default="{ row }">
                <span class="expense">¥ {{ money(row.expense) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="净额" align="right">
              <template #default="{ row }">
                <span :class="row.net >= 0 ? 'income' : 'expense'">¥ {{ money(row.net) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="条数" width="90" align="right" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="三类养老制度口径说明" name="rules">
          <div class="rules">
            <p>
              <b>企业职工 / 公务员事业单位：</b>月基本养老金 ＝ 基础养老金（（计发基数＋指数化月平均缴费工资）÷2×缴费年限×1%）
              ＋ 个人账户养老金（储存额 ÷ 计发月数，60 岁为 139）＋ 过渡性养老金（计发基数 × 视同缴费指数 × 视同缴费年限 × 过渡系数）；
              机关事业另加<b>职业年金</b>。缴费按个人 8%，机关事业再加职业年金个人 4%。
            </p>
            <p>
              <b>城乡居民：</b>月待遇 ＝ 基础养老金（财政定额，2026 年全国最低 163 元/月）＋ 个人账户养老金（（个人缴费＋政府补贴＋利息）÷ 139）
              ＋ 长缴加发 ＋ 高龄加发；缴费按年选档，政府按档补贴。
            </p>
            <p class="rules__tip">※ 金额由上述规则结合「参数设置」中的计发基数等参数自动算出，不可手工填写；实际发放以当地社保经办核定为准。</p>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 新增 / 编辑 -->
    <el-dialog v-model="visible" :title="editingId ? '编辑养老金记录' : '新增养老金记录'" width="620px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="130px">
        <el-form-item label="人员" prop="person_id">
          <el-select
            v-model="form.person_id"
            placeholder="请选择人员"
            filterable
            style="width: 100%"
            @change="onPersonChange"
          >
            <el-option v-for="p in persons" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
          <div v-if="!persons.length" class="hint">
            还没有人员档案，请先点击列表上方的「人员档案」添加
          </div>
        </el-form-item>
        <el-form-item label="人员分类">
          <el-input :model-value="schemeText" disabled />
        </el-form-item>
        <el-form-item label="方向">
          <el-radio-group v-model="form.direction">
            <el-radio-button v-for="d in DIRECTION_OPTIONS" :key="d.value" :value="d.value">
              {{ d.label }}
            </el-radio-button>
          </el-radio-group>
          <div class="hint">
            {{
              form.direction
                ? DIRECTION_TEXT[form.direction]
                : '留空时按人员档案的退休日期自动判定（退休当月及之后为领取）'
            }}
          </div>
        </el-form-item>
        <el-form-item :label="salaryLabel" prop="salary">
          <el-input-number
            v-model="form.salary"
            :min="0"
            :precision="2"
            :step="salaryStep"
            style="width: 100%"
          />
          <div class="hint">{{ salaryHint }}</div>
        </el-form-item>
        <el-form-item label="发生月份" prop="period_month">
          <el-date-picker
            v-model="form.period_month"
            type="month"
            value-format="YYYY-MM"
            placeholder="选择月份"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="收支金额（自动计算）">
          <div class="amount-box">
            <span v-if="preview" :class="preview.direction === 'income' ? 'income' : 'expense'">
              {{ preview.direction === 'income' ? '+' : '-' }} ¥ {{ money(preview.amount) }}
            </span>
            <span v-else class="hint">请选择人员与月份后自动计算</span>
            <el-tag v-if="preview" size="small" effect="plain" class="amount-box__tag">
              {{ preview.direction_text }}
            </el-tag>
          </div>
        </el-form-item>
        <el-form-item v-if="breakdownRows.length" label="计算明细">
          <el-table :data="breakdownRows" size="small" border>
            <el-table-column prop="name" label="项目" min-width="180" />
            <el-table-column label="金额" width="140" align="right">
              <template #default="{ row }">¥ {{ money(row.value) }}</template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.note" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>
        <el-collapse class="collapse-block">
          <el-collapse-item title="覆盖本次计算参数（选填）" name="override">
            <el-form-item v-if="isStaff" label="缴费年限(年)">
              <el-input-number v-model="form.contribution_years" :min="0" :precision="1" :step="1" style="width: 100%" />
            </el-form-item>
            <el-form-item label="个人账户储存额">
              <el-input-number
                v-model="form.personal_account_balance"
                :min="0"
                :precision="2"
                :step="1000"
                style="width: 100%"
              />
            </el-form-item>
            <template v-if="isStaff">
              <el-form-item label="视同缴费年限(年)">
                <el-input-number v-model="form.deemed_years" :min="0" :precision="1" :step="1" style="width: 100%" />
              </el-form-item>
              <el-form-item label="视同缴费指数">
                <el-input-number v-model="form.deemed_index" :min="0" :precision="2" :step="0.1" style="width: 100%" />
              </el-form-item>
              <el-form-item v-if="form.scheme === 'government'" label="职业年金储存额">
                <el-input-number
                  v-model="form.annuity_balance"
                  :min="0"
                  :precision="2"
                  :step="1000"
                  style="width: 100%"
                />
              </el-form-item>
            </template>
            <el-form-item v-else label="基础养老金(元/月)">
              <el-input-number
                v-model="form.resident_base"
                :min="0"
                :precision="2"
                :step="10"
                style="width: 100%"
              />
            </el-form-item>
            <div class="hint">留空则使用人员档案中的值；填写后仅影响本条记录。</div>
          </el-collapse-item>
        </el-collapse>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 查看 -->
    <el-dialog v-model="viewVisible" title="养老金记录详情" width="620px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="人员">{{ viewRow.person_name }}</el-descriptions-item>
        <el-descriptions-item label="时间">{{ viewRow.occurred_on || viewRow.period_month }}</el-descriptions-item>
        <el-descriptions-item label="人员分类">{{ viewRow.scheme_text }}</el-descriptions-item>
        <el-descriptions-item label="方向">{{ viewRow.direction_text }}</el-descriptions-item>
        <el-descriptions-item label="工资">
          ¥ {{ money(viewRow.salary) }}（{{ viewRow.scheme === 'resident' ? '元/年' : '元/月' }}）
        </el-descriptions-item>
        <el-descriptions-item label="收支金额">
          <span :class="viewRow.direction === 'income' ? 'income' : 'expense'">
            {{ viewRow.direction === 'income' ? '+' : '-' }} ¥ {{ money(viewRow.amount) }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="备注">{{ viewRow.note || '-' }}</el-descriptions-item>
      </el-descriptions>
      <el-table
        v-if="viewBreakdown.length"
        :data="viewBreakdown"
        size="small"
        border
        class="view-table"
      >
        <el-table-column prop="name" label="计算明细" min-width="200" />
        <el-table-column label="金额" width="140" align="right">
          <template #default="{ row }">¥ {{ money(row.value) }}</template>
        </el-table-column>
      </el-table>
      <el-table
        v-if="viewParams.length"
        :data="viewParams"
        size="small"
        border
        class="view-table"
      >
        <el-table-column prop="name" label="本次使用的参数" min-width="200" />
        <el-table-column prop="value" label="取值" width="160" />
      </el-table>
    </el-dialog>

    <!-- 人员档案 -->
    <el-dialog v-model="personsVisible" title="人员档案" width="860px">
      <div class="toolbar">
        <el-button type="primary" :icon="Plus" @click="openPersonCreate">新增人员</el-button>
      </div>
      <el-table :data="persons" v-loading="personsLoading" border stripe size="small">
        <el-table-column prop="name" label="姓名" width="110" />
        <el-table-column label="分类" width="140">
          <template #default="{ row }">
            <el-tag :type="schemeTagType(row.scheme)" size="small">{{ row.scheme_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="工资" width="130" align="right">
          <template #default="{ row }">
            ¥ {{ money(row.salary) }}{{ row.scheme === 'resident' ? '/年' : '/月' }}
          </template>
        </el-table-column>
        <el-table-column label="缴费年限" width="100" align="right">
          <template #default="{ row }">{{ row.contribution_years }} 年</template>
        </el-table-column>
        <el-table-column label="个人账户" width="130" align="right">
          <template #default="{ row }">¥ {{ money(row.personal_account_balance) }}</template>
        </el-table-column>
        <el-table-column label="退休日期" width="120">
          <template #default="{ row }">{{ row.retire_date || '-' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openPersonEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="removePerson(row)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty><span class="empty-text">暂无人员档案</span></template>
      </el-table>
    </el-dialog>

    <!-- 人员新增 / 编辑 -->
    <el-dialog v-model="personVisible" :title="personId ? '编辑人员' : '新增人员'" width="560px" append-to-body>
      <el-form ref="personFormRef" :model="personForm" :rules="personRules" label-width="140px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="personForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="人员分类" prop="scheme">
          <el-select v-model="personForm.scheme" style="width: 100%">
            <el-option v-for="s in SCHEME_OPTIONS" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item :label="personForm.scheme === 'resident' ? '年缴费档次(元)' : '月工资(元)'">
          <el-input-number
            v-model="personForm.salary"
            :min="0"
            :precision="2"
            :step="personForm.scheme === 'resident' ? 100 : 500"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="出生日期">
          <el-date-picker
            v-model="personForm.birth_date"
            type="date"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="退休日期">
          <el-date-picker
            v-model="personForm.retire_date"
            type="date"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
          <div class="hint">用于自动判定缴费 / 领取，并结合出生日期查计发月数</div>
        </el-form-item>
        <el-form-item label="缴费年限(年)">
          <el-input-number v-model="personForm.contribution_years" :min="0" :precision="1" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="个人账户储存额">
          <el-input-number
            v-model="personForm.personal_account_balance"
            :min="0"
            :precision="2"
            :step="1000"
            style="width: 100%"
          />
        </el-form-item>
        <template v-if="personForm.scheme !== 'resident'">
          <el-form-item label="视同缴费年限(年)">
            <el-input-number v-model="personForm.deemed_years" :min="0" :precision="1" :step="1" style="width: 100%" />
          </el-form-item>
          <el-form-item label="视同缴费指数">
            <el-input-number v-model="personForm.deemed_index" :min="0" :precision="2" :step="0.1" style="width: 100%" />
            <div class="hint">留空取参数设置中的默认值</div>
          </el-form-item>
          <el-form-item v-if="personForm.scheme === 'government'" label="职业年金储存额">
            <el-input-number
              v-model="personForm.annuity_balance"
              :min="0"
              :precision="2"
              :step="1000"
              style="width: 100%"
            />
          </el-form-item>
        </template>
        <el-form-item v-else label="基础养老金(元/月)">
          <el-input-number v-model="personForm.resident_base" :min="0" :precision="2" :step="10" style="width: 100%" />
          <div class="hint">留空取参数设置中的居民基础养老金</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="personForm.note" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="personVisible = false">取消</el-button>
        <el-button type="primary" :loading="personSubmitting" @click="submitPerson">保存</el-button>
      </template>
    </el-dialog>

    <!-- 参数设置 -->
    <el-dialog v-model="paramsVisible" title="养老金计算参数" width="620px">
      <el-form :model="paramsForm" label-width="170px">
        <el-form-item label="计发基数(元/月)">
          <el-input-number v-model="paramsForm.base_number" :min="0" :precision="2" :step="100" style="width: 100%" />
          <div class="hint">各省每年公布的社会平均工资口径</div>
        </el-form-item>
        <el-form-item label="平均缴费工资指数">
          <el-input-number v-model="paramsForm.avg_index" :min="0" :precision="2" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="缴费基数下限(%)">
          <el-input-number v-model="paramsForm.base_floor_pct" :min="0" :max="100" :precision="1" :step="5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="缴费基数上限(%)">
          <el-input-number v-model="paramsForm.base_cap_pct" :min="0" :max="1000" :precision="1" :step="10" style="width: 100%" />
        </el-form-item>
        <el-form-item label="养老个人费率(%)">
          <el-input-number v-model="paramsForm.personal_rate" :min="0" :precision="2" :step="0.5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="职业年金个人费率(%)">
          <el-input-number v-model="paramsForm.annuity_personal_rate" :min="0" :precision="2" :step="0.5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="单位费率(%)">
          <el-input-number v-model="paramsForm.company_rate" :min="0" :precision="2" :step="0.5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="单位缴费计入金额">
          <el-switch v-model="paramsForm.include_company" />
          <div class="hint">默认只统计个人缴费部分</div>
        </el-form-item>
        <el-form-item label="视同缴费指数">
          <el-input-number v-model="paramsForm.deemed_index" :min="0" :precision="2" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="过渡系数(%)">
          <el-input-number v-model="paramsForm.transition_coef" :min="0" :precision="2" :step="0.1" style="width: 100%" />
          <div class="hint">各省 1.2% ~ 1.4%</div>
        </el-form-item>
        <el-form-item label="默认退休年龄">
          <el-input-number v-model="paramsForm.retire_age" :min="40" :max="75" :precision="0" :step="1" style="width: 100%" />
          <div class="hint">人员未填出生/退休日期时用于查计发月数</div>
        </el-form-item>
        <el-form-item label="居民基础养老金(元/月)">
          <el-input-number v-model="paramsForm.resident_base" :min="0" :precision="2" :step="10" style="width: 100%" />
        </el-form-item>
        <el-form-item label="居民计发月数">
          <el-input-number v-model="paramsForm.resident_divisor" :min="1" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="长缴加发起算年限">
          <el-input-number v-model="paramsForm.long_pay_threshold" :min="0" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="长缴加发(元/年)">
          <el-input-number v-model="paramsForm.long_pay_bonus" :min="0" :precision="2" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="高龄加发起始年龄">
          <el-input-number v-model="paramsForm.elderly_age" :min="50" :max="100" :precision="0" :step="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="高龄加发(元/月)">
          <el-input-number v-model="paramsForm.elderly_bonus" :min="0" :precision="2" :step="5" style="width: 100%" />
        </el-form-item>
        <el-collapse class="collapse-block">
          <el-collapse-item title="高级：计发月数表与居民补贴（JSON）" name="json">
            <el-form-item label="退休年龄→计发月数">
              <el-input v-model="paramsForm.divisor_map_text" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="居民年缴费档次">
              <el-input v-model="paramsForm.resident_levels_text" type="textarea" :rows="2" />
            </el-form-item>
            <el-form-item label="档次→政府补贴(元/年)">
              <el-input v-model="paramsForm.resident_subsidy_text" type="textarea" :rows="3" />
            </el-form-item>
          </el-collapse-item>
        </el-collapse>
      </el-form>
      <template #footer>
        <el-button @click="paramsVisible = false">取消</el-button>
        <el-button type="primary" :loading="paramsSubmitting" @click="submitParams">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Setting, User } from '@element-plus/icons-vue'
import SearchForm from '@/components/SearchForm.vue'
import {
  createPension,
  createPensionPerson,
  deletePension,
  deletePensionPerson,
  getPensionParams,
  getPensionPersons,
  getPensionStats,
  getPensions,
  previewPension,
  updatePension,
  updatePensionParams,
  updatePensionPerson,
} from '@/api/pensions'

const SCHEME_OPTIONS = [
  { label: '企业职工', value: 'enterprise' },
  { label: '公务员事业单位', value: 'government' },
  { label: '城乡居民', value: 'resident' },
]
const SCHEME_TEXT = {
  enterprise: '企业职工',
  government: '公务员事业单位',
  resident: '城乡居民',
}
const DIRECTION_OPTIONS = [
  { label: '自动', value: '' },
  { label: '缴费', value: 'expense' },
  { label: '领取', value: 'income' },
]
const DIRECTION_TEXT = { income: '领取', expense: '缴费' }

function money(v) {
  return Number(v || 0).toFixed(2)
}

function schemeTagType(scheme) {
  return { enterprise: 'primary', government: 'warning', resident: 'success' }[scheme] || 'info'
}

function currentMonth() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

const list = ref([])
const loading = ref(false)
const stats = ref({ income_total: 0, expense_total: 0, net: 0, count: 0, month_stats: [], scheme_stats: [] })
const persons = ref([])
const personsLoading = ref(false)

const emptyQuery = () => ({ person: '', date_range: null, scheme: '' })
const query = reactive(emptyQuery())

const searchSchema = computed(() => ({
  colSpan: 6,
  labelPosition: 'top',
  gutter: 18,
  model: query,
  formItems: [
    { type: 'input.trim', label: '人员', field: 'person', placeholder: '请输入人员姓名', clearable: true },
    {
      type: 'date-picker',
      subtype: 'daterange',
      label: '时间',
      field: 'date_range',
      valueFormat: 'YYYY-MM-DD',
      startPlaceholder: '开始日期',
      endPlaceholder: '结束日期',
      rangeSeparator: '至',
      unlinkPanels: true,
      style: 'width: 100%',
    },
    {
      type: 'select',
      label: '人员分类',
      field: 'scheme',
      placeholder: '全部分类',
      clearable: true,
      options: SCHEME_OPTIONS,
    },
  ],
}))

function buildParams() {
  const params = {}
  if (query.person) params.person = query.person
  if (query.scheme) params.scheme = query.scheme
  if (Array.isArray(query.date_range) && query.date_range.length === 2) {
    params.start_date = query.date_range[0]
    params.end_date = query.date_range[1]
  }
  return params
}

async function load() {
  loading.value = true
  try {
    const params = buildParams()
    const [rows, summary] = await Promise.all([getPensions(params), getPensionStats(params)])
    list.value = rows
    stats.value = summary
  } finally {
    loading.value = false
  }
}

async function loadPersons() {
  personsLoading.value = true
  try {
    persons.value = await getPensionPersons()
  } finally {
    personsLoading.value = false
  }
}

function onReset() {
  Object.assign(query, emptyQuery())
  load()
}

// ---------------------------------------------------------------- 记录表单
const visible = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref()
const preview = ref(null)
const previewing = ref(false)
let previewTimer = null

const emptyForm = () => ({
  person_id: null,
  period_month: currentMonth(),
  direction: '',
  salary: null,
  note: '',
  contribution_years: null,
  personal_account_balance: null,
  deemed_years: null,
  deemed_index: null,
  annuity_balance: null,
  resident_base: null,
})
const form = reactive(emptyForm())

const rules = {
  person_id: [{ required: true, message: '请选择人员', trigger: 'change' }],
  period_month: [{ required: true, message: '请选择发生月份', trigger: 'change' }],
  salary: [{ required: true, message: '请输入工资', trigger: 'blur' }],
}

const currentPerson = computed(() => persons.value.find((p) => p.id === form.person_id) || null)
const formScheme = computed(() => currentPerson.value?.scheme || 'enterprise')
const isStaff = computed(() => formScheme.value !== 'resident')
const schemeText = computed(() => SCHEME_TEXT[formScheme.value] || '-')
const salaryLabel = computed(() => (formScheme.value === 'resident' ? '年缴费档次(元)' : '月工资(元)'))
const salaryStep = computed(() => (formScheme.value === 'resident' ? 100 : 500))
const salaryHint = computed(() =>
  formScheme.value === 'resident'
    ? '居民按年选档缴费，政府按档给予补贴（参数设置中可维护）'
    : '职工缴费基数按社平的 60%~300% 封顶'
)
const breakdownRows = computed(() =>
  Object.entries(preview.value?.breakdown || {}).map(([name, value]) => ({ name, value }))
)

function onPersonChange() {
  const person = currentPerson.value
  if (person) {
    if (form.salary === null || editingId.value === null) form.salary = person.salary
  }
  runPreview()
}

watch(
  () => [
    form.person_id,
    form.period_month,
    form.direction,
    form.salary,
    form.contribution_years,
    form.personal_account_balance,
    form.deemed_years,
    form.deemed_index,
    form.annuity_balance,
    form.resident_base,
  ],
  () => {
    clearTimeout(previewTimer)
    previewTimer = setTimeout(runPreview, 300)
  }
)

function previewPayload() {
  return {
    person_id: form.person_id,
    period_month: form.period_month,
    direction: form.direction || null,
    salary: form.salary,
    contribution_years: form.contribution_years,
    personal_account_balance: form.personal_account_balance,
    deemed_years: form.deemed_years,
    deemed_index: form.deemed_index,
    annuity_balance: form.annuity_balance,
    resident_base: form.resident_base,
  }
}

async function runPreview() {
  if (!form.person_id || !form.period_month) {
    preview.value = null
    return
  }
  previewing.value = true
  try {
    preview.value = await previewPension(previewPayload())
  } catch {
    preview.value = null
  } finally {
    previewing.value = false
  }
}

function openCreate() {
  editingId.value = null
  Object.assign(form, emptyForm())
  preview.value = null
  visible.value = true
  if (!persons.value.length) loadPersons()
}

function openEdit(row) {
  editingId.value = row.id
  const ov = row.overrides || {}
  Object.assign(form, {
    person_id: row.person_id,
    period_month: row.period_month,
    direction: row.direction,
    salary: row.salary,
    note: row.note || '',
    contribution_years: ov.contribution_years ?? null,
    personal_account_balance: ov.personal_account_balance ?? null,
    deemed_years: ov.deemed_years ?? null,
    deemed_index: ov.deemed_index ?? null,
    annuity_balance: ov.annuity_balance ?? null,
    resident_base: ov.resident_base ?? null,
  })
  visible.value = true
  runPreview()
}

async function submit() {
  await formRef.value.validate()
  const payload = previewPayload()
  payload.occurred_on = null
  payload.note = form.note || null
  submitting.value = true
  try {
    if (editingId.value) {
      await updatePension(editingId.value, payload)
      ElMessage.success('已更新，金额已按规则重算')
    } else {
      await createPension(payload)
      ElMessage.success('已新增，金额按规则自动算出')
    }
    visible.value = false
    load()
  } finally {
    submitting.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除「${row.person_name}」${row.period_month} 的记录？`, '提示', {
    type: 'warning',
  })
  await deletePension(row.id)
  ElMessage.success('已删除')
  load()
}

// ---------------------------------------------------------------- 查看
const viewVisible = ref(false)
const viewRow = ref({})
const viewBreakdown = computed(() =>
  Object.entries(viewRow.value.breakdown || {}).map(([name, value]) => ({ name, value }))
)
const viewParams = computed(() =>
  Object.entries(viewRow.value.params || {}).map(([name, value]) => ({ name, value }))
)

function openView(row) {
  viewRow.value = { ...row }
  viewVisible.value = true
}

// ---------------------------------------------------------------- 人员档案
const personsVisible = ref(false)
const personVisible = ref(false)
const personId = ref(null)
const personSubmitting = ref(false)
const personFormRef = ref()

const emptyPersonForm = () => ({
  name: '',
  scheme: 'enterprise',
  salary: 0,
  birth_date: '',
  retire_date: '',
  contribution_years: 0,
  personal_account_balance: 0,
  deemed_years: 0,
  deemed_index: null,
  annuity_balance: 0,
  resident_base: null,
  note: '',
})
const personForm = reactive(emptyPersonForm())
const personRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  scheme: [{ required: true, message: '请选择人员分类', trigger: 'change' }],
}

function openPersons() {
  personsVisible.value = true
  loadPersons()
}

function openPersonCreate() {
  personId.value = null
  Object.assign(personForm, emptyPersonForm())
  personVisible.value = true
}

function openPersonEdit(row) {
  personId.value = row.id
  Object.assign(personForm, {
    name: row.name,
    scheme: row.scheme,
    salary: row.salary,
    birth_date: row.birth_date || '',
    retire_date: row.retire_date || '',
    contribution_years: row.contribution_years,
    personal_account_balance: row.personal_account_balance,
    deemed_years: row.deemed_years,
    deemed_index: row.deemed_index ?? null,
    annuity_balance: row.annuity_balance,
    resident_base: row.resident_base ?? null,
    note: row.note || '',
  })
  personVisible.value = true
}

async function submitPerson() {
  await personFormRef.value.validate()
  const payload = { ...personForm }
  // 日期控件清空后是空串，后端按日期解析会报 422，统一转成 null
  for (const key of ['birth_date', 'retire_date']) {
    if (!payload[key]) payload[key] = null
  }
  for (const key of ['deemed_index', 'resident_base']) {
    if (payload[key] === '' || payload[key] === undefined) payload[key] = null
  }
  personSubmitting.value = true
  try {
    if (personId.value) {
      await updatePensionPerson(personId.value, payload)
      ElMessage.success('人员已更新')
    } else {
      await createPensionPerson(payload)
      ElMessage.success('人员已新增')
    }
    personVisible.value = false
    await loadPersons()
    load()
  } finally {
    personSubmitting.value = false
  }
}

async function removePerson(row) {
  await ElMessageBox.confirm(`确认删除人员「${row.name}」？其名下的养老金记录会一并删除。`, '提示', {
    type: 'warning',
  })
  await deletePensionPerson(row.id)
  ElMessage.success('已删除')
  await loadPersons()
  load()
}

// ---------------------------------------------------------------- 参数设置
const paramsVisible = ref(false)
const paramsSubmitting = ref(false)
const paramsForm = reactive({
  base_number: 8000,
  avg_index: 1,
  base_floor_pct: 60,
  base_cap_pct: 300,
  personal_rate: 8,
  annuity_personal_rate: 4,
  company_rate: 16,
  include_company: false,
  deemed_index: 1,
  transition_coef: 1.3,
  retire_age: 60,
  resident_base: 163,
  resident_divisor: 139,
  long_pay_threshold: 15,
  long_pay_bonus: 2,
  elderly_age: 65,
  elderly_bonus: 0,
  divisor_map_text: '',
  resident_levels_text: '',
  resident_subsidy_text: '',
})

async function openParams() {
  const data = await getPensionParams()
  Object.assign(paramsForm, {
    base_number: data.base_number,
    avg_index: data.avg_index,
    base_floor_pct: Number((data.base_floor * 100).toFixed(2)),
    base_cap_pct: Number((data.base_cap * 100).toFixed(2)),
    personal_rate: data.personal_rate,
    annuity_personal_rate: data.annuity_personal_rate,
    company_rate: data.company_rate,
    include_company: data.include_company,
    deemed_index: data.deemed_index,
    transition_coef: data.transition_coef,
    retire_age: data.retire_age,
    resident_base: data.resident_base,
    resident_divisor: data.resident_divisor,
    long_pay_threshold: data.long_pay_threshold,
    long_pay_bonus: data.long_pay_bonus,
    elderly_age: data.elderly_age,
    elderly_bonus: data.elderly_bonus,
    divisor_map_text: JSON.stringify(data.divisor_map),
    resident_levels_text: JSON.stringify(data.resident_levels),
    resident_subsidy_text: JSON.stringify(data.resident_subsidy_map),
  })
  paramsVisible.value = true
}

async function submitParams() {
  const payload = {
    base_number: paramsForm.base_number,
    avg_index: paramsForm.avg_index,
    base_floor: Number((paramsForm.base_floor_pct / 100).toFixed(4)),
    base_cap: Number((paramsForm.base_cap_pct / 100).toFixed(4)),
    personal_rate: paramsForm.personal_rate,
    annuity_personal_rate: paramsForm.annuity_personal_rate,
    company_rate: paramsForm.company_rate,
    include_company: paramsForm.include_company,
    deemed_index: paramsForm.deemed_index,
    transition_coef: paramsForm.transition_coef,
    retire_age: paramsForm.retire_age,
    resident_base: paramsForm.resident_base,
    resident_divisor: paramsForm.resident_divisor,
    long_pay_threshold: paramsForm.long_pay_threshold,
    long_pay_bonus: paramsForm.long_pay_bonus,
    elderly_age: paramsForm.elderly_age,
    elderly_bonus: paramsForm.elderly_bonus,
  }
  try {
    payload.divisor_map = JSON.parse(paramsForm.divisor_map_text)
    payload.resident_levels = JSON.parse(paramsForm.resident_levels_text)
    payload.resident_subsidy_map = JSON.parse(paramsForm.resident_subsidy_text)
  } catch {
    ElMessage.error('计发月数表 / 居民补贴配置不是合法 JSON，请检查')
    return
  }
  paramsSubmitting.value = true
  try {
    await updatePensionParams(payload)
    ElMessage.success('参数已保存，后续新增/编辑的记录将按新参数计算')
    paramsVisible.value = false
    runPreview()
  } finally {
    paramsSubmitting.value = false
  }
}

onMounted(() => {
  load()
  loadPersons()
})
</script>

<style scoped>
.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.stat-card {
  flex: 1 1 180px;
  min-width: 160px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid var(--el-border-color-lighter, #ebeef5);
  border-radius: 8px;
}

.stat-card__label {
  color: #909399;
  font-size: 12px;
}

.stat-card__value {
  margin-top: 6px;
  font-size: 20px;
  font-weight: 600;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.toolbar__left {
  display: flex;
  gap: 8px;
}

.income {
  color: #f56c6c;
}

.expense {
  color: #67c23a;
}

.hint {
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
  line-height: 1.4;
}

.empty-text {
  color: #909399;
}

.amount-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.amount-box__tag {
  font-weight: 400;
}

.collapse-block {
  margin-top: 16px;
}

.scheme-table {
  margin-top: 12px;
}

.view-table {
  margin-top: 12px;
}

.rules {
  color: #606266;
  font-size: 13px;
  line-height: 1.8;
}

.rules p {
  margin: 0 0 8px;
}

.rules__tip {
  color: #909399;
  font-size: 12px;
}
</style>
