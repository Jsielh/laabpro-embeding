import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { storage } from '@/utils/storage'

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({
    sessionId: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  })

  const setUser = (data: Partial<User>) => {
    user.value = { ...user.value, ...data }
    storage.set('user', user.value)
  }

  const stored = storage.get<User>('user')
  if (stored) user.value = stored

  return { user, setUser }
})
