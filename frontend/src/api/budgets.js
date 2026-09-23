import request from './request'

export const getBudgets = () => request.get('/budgets')
export const createBudget = (data) => request.post('/budgets', data)
export const updateBudget = (id, data) => request.put(`/budgets/${id}`, data)
export const deleteBudget = (id) => request.delete(`/budgets/${id}`)
