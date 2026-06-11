import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Message } from '@/types'
import { storage } from '@/utils/storage'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const isTyping = ref(false)
  const unreadCount = ref(0)

  const addMessage = (message: Message) => {
    messages.value.push(message)
    storage.set('messages', messages.value.slice(-50))
  }

  const setTyping = (typing: boolean) => {
    isTyping.value = typing
  }

  const clearMessages = () => {
    messages.value = []
    storage.remove('messages')
  }

  const markAllAsRead = () => {
    unreadCount.value = 0
  }

 
  const stored = storage.get<Message[]>('messages')
  if (stored) messages.value = stored.map((m: any) => ({ ...m, timestamp: new Date(m.timestamp) }))

  return { messages, isTyping, unreadCount, addMessage, setTyping, clearMessages, markAllAsRead }
})
