import { defineStore } from 'pinia'
import { getProfile, login, register } from '@/api/auth'

const TOKEN_KEY = 'finance_token'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: null,
    loaded: false,
  }),
  getters: {
    isLogin: (state) => Boolean(state.token),
    displayName: (state) => state.user?.name || state.user?.username || '',
    isAdmin: (state) => state.user?.username === 'admin',
  },
  actions: {
    setToken(token) {
      this.token = token || ''
      if (token) localStorage.setItem(TOKEN_KEY, token)
      else localStorage.removeItem(TOKEN_KEY)
    },
    async login(payload) {
      const data = await login(payload)
      this.setToken(data.access_token)
      this.user = data.user
      this.loaded = true
    },
    async register(payload) {
      const data = await register(payload)
      this.setToken(data.access_token)
      this.user = data.user
      this.loaded = true
    },
    async fetchProfile(force = false) {
      if (!this.token) return null
      if (this.user && !force) return this.user
      this.user = await getProfile()
      this.loaded = true
      return this.user
    },
    updateUser(patch) {
      this.user = { ...(this.user || {}), ...patch }
    },
    logout() {
      this.setToken('')
      this.user = null
      this.loaded = false
    },
  },
})
