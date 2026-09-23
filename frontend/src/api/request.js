import axios from 'axios'
import { ElMessage } from 'element-plus'

const TOKEN_KEY = 'finance_token'

// 开发环境通过 vite proxy 转发 /api 到后端 8000
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

// 请求拦截：带上登录令牌（直接读 localStorage，避免与 store 形成循环依赖）
request.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// 响应拦截：统一解包并做错误提示
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const msg = error.response?.data?.detail || error.message || '请求失败'
    // 令牌失效：清掉本地令牌并跳登录页
    // （登录/注册失败返回的是 400，不会误触发这里）
    if (status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      if (!window.location.pathname.startsWith('/login')) {
        window.location.replace('/login')
        return Promise.reject(error)
      }
    }
    ElMessage.error(typeof msg === 'string' ? msg : JSON.stringify(msg))
    return Promise.reject(error)
  }
)

export default request
