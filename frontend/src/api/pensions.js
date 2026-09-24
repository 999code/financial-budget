import request from './request'

// 月度记录
export const getPensions = (params) => request.get('/pensions', { params })
export const getPensionStats = (params) => request.get('/pensions/stats', { params })
export const previewPension = (data) => request.post('/pensions/preview', data)
export const getPension = (id) => request.get(`/pensions/${id}`)
export const createPension = (data) => request.post('/pensions', data)
export const updatePension = (id, data) => request.put(`/pensions/${id}`, data)
export const deletePension = (id) => request.delete(`/pensions/${id}`)
// 同步到收支管理的固定收支（幂等：重复同步走更新）
export const syncPension = (id, data) => request.post(`/pensions/${id}/sync`, data || {})

// 人员档案
export const getPensionPersons = (params) => request.get('/pension-persons', { params })
export const createPensionPerson = (data) => request.post('/pension-persons', data)
export const updatePensionPerson = (id, data) => request.put(`/pension-persons/${id}`, data)
export const deletePensionPerson = (id) => request.delete(`/pension-persons/${id}`)

// 参数配置
export const getPensionParams = () => request.get('/pension-params')
export const updatePensionParams = (data) => request.put('/pension-params', data)
