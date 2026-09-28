import request from './request'

export const getSummary = () => request.get('/summary')

// 资金消耗进度与耗尽预测；months=统计窗口（月），horizon=消耗进度基准周期（月）
export const getFundRunway = (params) => request.get('/summary/fund-runway', { params })

// 资金消耗与耗尽预测（绝对值口径）；months=预测跨度（月），从当前月的下一月起算
export const getAbsoluteOutlook = (params) => request.get('/summary/absolute-outlook', { params })
