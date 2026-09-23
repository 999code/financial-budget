import request from './request'

export const getAccounts = () => request.get('/accounts')
export const createAccount = (data) => request.post('/accounts', data)
export const updateAccount = (id, data) => request.put(`/accounts/${id}`, data)
export const deleteAccount = (id) => request.delete(`/accounts/${id}`)
