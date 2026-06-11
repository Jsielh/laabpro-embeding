export interface Message {
  id: number
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
  isVoice?: boolean
  isFile?: boolean
  fileName?: string
  fileType?: string
}

export interface UploadResponse {
  answer: string
  filename: string
  extracted_text: string
}

export interface User {
  id?: string
  name?: string
  email?: string
  sessionId: string
}

export interface ChatResponse {
  message: string
  timestamp?: string
  language?: string
}

export interface VoiceResponse {
  transcription: string
  reply: string
}

export interface WidgetConfig {
  api: { baseUrl: string; timeout: number }
  ui: { width: number; height: number }
  voice: { enabled: boolean; maxDuration: number }
}
