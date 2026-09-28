import request from './request'

export const getSummary = () => request.get('/summary')

// 资金消耗进度与耗尽预测；months=统计窗口（月），horizon=消耗进度基准周期（月）
export const getFundRunway = (params) => request.get('/summary/fund-runway', { params })
