import request from './request'

// 登录注册与个人中心，对应后端 /api/v1/auth
export const login = (data) => request.post('/auth/login', data)
export const register = (data) => request.post('/auth/register', data)
export const getProfile = () => request.get('/auth/me')
export const updateProfile = (data) => request.put('/auth/me', data)
export const changePassword = (data) => request.post('/auth/change-password', data)
