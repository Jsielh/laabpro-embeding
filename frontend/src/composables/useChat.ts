import { ref, computed } from 'vue'
import { useChatStore } from '@/store/chat'
import { useUserStore } from '@/store/user'
import { chatService } from '@/services/chatService'
import { useI18n } from 'vue-i18n'
import { ERROR_MESSAGES } from '@/constants'
import type { Message, UploadResponse } from '@/types'

export function useChat() {
  const chatStore = useChatStore()
  const userStore = useUserStore()
  const { locale } = useI18n()
  const isSending = ref(false)

  const sendMessage = async (text: string) => {
    if (!text || isSending.value) return

    isSending.value = true
    chatStore.addMessage({ 
      id: Date.now(), 
      text, 
      sender: 'user', 
      timestamp: new Date() 
    })
    
    const botMessageId = Date.now() + 1
    chatStore.addMessage({ 
      id: botMessageId, 
      text: '', 
      sender: 'bot', 
      timestamp: new Date() 
    })
    chatStore.setTyping(true)

    try {
      await chatService.sendMessageStream(
        text,
        userStore.user.sessionId,
        locale.value,
        (chunk: string) => {
          const messages = chatStore.messages
          const botMessage = messages.find(m => m.id === botMessageId)
          if (botMessage) {
            botMessage.text += chunk
          }
        },
        (fullMessage: string, timestamp: string) => {
          chatStore.setTyping(false)
          isSending.value = false
        },
        (error: string) => {
          const messages = chatStore.messages
          const botMessage = messages.find(m => m.id === botMessageId)
          if (botMessage) {
            botMessage.text = ERROR_MESSAGES.CHAT.SEND_FAILED
          }
          chatStore.setTyping(false)
          isSending.value = false
        }
      )
    } catch (error) {
      const messages = chatStore.messages
      const botMessage = messages.find(m => m.id === botMessageId)
      if (botMessage) {
        botMessage.text = ERROR_MESSAGES.CHAT.SEND_FAILED
      }
      chatStore.setTyping(false)
      isSending.value = false
    }
  }

  const sendFileMessage = async (file: File, text = '') => {
    if (isSending.value) return

    isSending.value = true
    chatStore.addMessage({
      id: Date.now(),
      text: text || file.name,
      sender: 'user',
      timestamp: new Date(),
      isFile: true,
      fileName: file.name,
      fileType: file.type,
    })

    try {
      chatStore.setTyping(true)
      const response = await chatService.sendFile(file, text, userStore.user.sessionId, locale.value)
      chatStore.addMessage({
        id: Date.now() + 1,
        text: response.data.answer,
        sender: 'bot',
        timestamp: new Date(),
      })
    } catch (error) {
      chatStore.addMessage({
        id: Date.now() + 1,
        text: ERROR_MESSAGES.CHAT.SEND_FAILED,
        sender: 'bot',
        timestamp: new Date(),
      })
    } finally {
      chatStore.setTyping(false)
      isSending.value = false
    }
  }

  const sendVoiceMessage = async (audioBlob: Blob) => {
    if (!audioBlob || isSending.value) return

    isSending.value = true
    chatStore.setTyping(true)

    try {
      const response = await chatService.sendVoice(audioBlob)
      chatStore.addMessage({ 
        id: Date.now(), 
        text: response.transcription, 
        sender: 'user', 
        timestamp: new Date(), 
        isVoice: true 
      })
      chatStore.addMessage({ 
        id: Date.now() + 1, 
        text: response.reply, 
        sender: 'bot', 
        timestamp: new Date() 
      })
    } catch (error) {
      chatStore.addMessage({ 
        id: Date.now() + 2, 
        text: ERROR_MESSAGES.CHAT.VOICE_PROCESSING, 
        sender: 'bot', 
        timestamp: new Date() 
      })
    } finally {
      chatStore.setTyping(false)
      isSending.value = false
    }
  }

  return {
    messages: computed(() => chatStore.messages),
    isTyping: computed(() => chatStore.isTyping),
    isSending,
    sendMessage,
    sendFileMessage,
    sendVoiceMessage,
    clearChat: () => chatStore.clearMessages()
  }
}
