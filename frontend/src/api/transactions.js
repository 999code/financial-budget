import request from './request'

export const getTransactions = () => request.get('/transactions')
export const createTransaction = (data) => request.post('/transactions', data)
export const updateTransaction = (id, data) => request.put(`/transactions/${id}`, data)
export const deleteTransaction = (id) => request.delete(`/transactions/${id}`)
