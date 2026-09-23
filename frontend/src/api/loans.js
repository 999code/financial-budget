import request from './request'

export const getLoans = (params) => request.get('/loans', { params })
export const getLoan = (id) => request.get(`/loans/${id}`)
export const createLoan = (data) => request.post('/loans', data)
export const updateLoan = (id, data) => request.put(`/loans/${id}`, data)
export const deleteLoan = (id) => request.delete(`/loans/${id}`)
