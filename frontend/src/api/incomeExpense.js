import request from './request'

// 收支管理（固定/临时）接口，对应后端 /api/v1/income-expense
export const getIncomeExpenses = (params) => request.get('/income-expense', { params })
export const getIncomeExpense = (id) => request.get(`/income-expense/${id}`)
export const createIncomeExpense = (data) => request.post('/income-expense', data)
export const updateIncomeExpense = (id, data) => request.put(`/income-expense/${id}`, data)
export const deleteIncomeExpense = (id) => request.delete(`/income-expense/${id}`)

// 固定收支的按期明细（后端按周期自动展开，编辑/删除会入库）
export const getIncomeExpenseDetails = (id) => request.get(`/income-expense/${id}/details`)
export const updateIncomeExpenseDetail = (id, data) =>
  request.put(`/income-expense/details/${id}`, data)
export const deleteIncomeExpenseDetail = (id) => request.delete(`/income-expense/details/${id}`)
