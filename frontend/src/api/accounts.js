import request from './request'

export const getAccounts = () => request.get('/accounts')
export const createAccount = (data) => request.post('/accounts', data)
export const updateAccount = (id, data) => request.put(`/accounts/${id}`, data)
export const deleteAccount = (id) => request.delete(`/accounts/${id}`)
// 账户关联的收支流水（含「期初 + 收入 − 支出 = 余额」的推算）
export const getAccountIncomeExpenses = (id) => request.get(`/accounts/${id}/income-expenses`)
