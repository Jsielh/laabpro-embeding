import api from './api'
import { WIDGET_CONFIG } from '@/config/widget.config'
import { API_ENDPOINTS, HEADERS } from '@/constants'
import type { AxiosResponse } from 'axios'
import type { ChatResponse, UploadResponse, VoiceResponse } from '@/types'

export const chatService = {
  async sendMessage(message: string, sessionId: string, language = 'es', userEmail?: string): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>(API_ENDPOINTS.CHAT.MESSAGE, {
      query: message,
      locale: language,
      session_id: sessionId
    })
    return response.data as ChatResponse
  },

  async sendMessageStream(
    message: string,
    sessionId: string,
    language = 'es',
    onChunk: (chunk: string) => void,
    onComplete: (fullMessage: string, timestamp: string) => void,
    onError: (error: string) => void
  ): Promise<void> {
    const url = `${WIDGET_CONFIG.api.baseUrl}${API_ENDPOINTS.CHAT.STREAM}`
    const body = JSON.stringify({
      query: message,
      locale: language,
      session_id: sessionId
    })

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { [HEADERS.CONTENT_TYPE]: HEADERS.APPLICATION_JSON },
        body
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      if (data.detail) {
        onError(data.detail)
        return
      }

      const answer = data.answer || ''
      const timestamp = new Date().toISOString()
      
      const chunks = answer.match(/.{1,50}/g) || [answer]
      for (let i = 0; i < chunks.length; i++) {
        onChunk(chunks[i])
        await new Promise(r => setTimeout(r, 30))
      }
      
      onComplete(answer, timestamp)
    } catch (error: any) {
      onError(error.message)
    }
  },

  async sendVoice(audioBlob: Blob): Promise<VoiceResponse> {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'voice.webm')
    return api.post(API_ENDPOINTS.CHAT.VOICE, formData, { 
      headers: { [HEADERS.CONTENT_TYPE]: HEADERS.MULTIPART_FORM_DATA } 
    })
  },

  async sendFile(file: File, query: string, sessionId: string, locale: string): Promise<AxiosResponse<UploadResponse>> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('query', query)
    formData.append('session_id', sessionId)
    formData.append('locale', locale)
    return api.post(API_ENDPOINTS.CHAT.UPLOAD, formData, {
      headers: { [HEADERS.CONTENT_TYPE]: HEADERS.MULTIPART_FORM_DATA }
    })
  },

  async getHistory(limit = 50) {
    return api.get(API_ENDPOINTS.CHAT.HISTORY, { params: { limit } })
  },

  async clearHistory() {
    return api.delete(API_ENDPOINTS.CHAT.HISTORY)
  }
}

