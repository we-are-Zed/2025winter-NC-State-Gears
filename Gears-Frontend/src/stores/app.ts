// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    username: '',
    sid: '',
    isLogin: false,
    token: '',
  }),
})
