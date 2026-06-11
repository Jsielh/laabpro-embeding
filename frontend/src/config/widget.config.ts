import type { WidgetConfig } from '@/types'

interface EmbedConfig {
  apiUrl?: string
  locale?: string
  companyName?: string
  position?: 'bottom-right' | 'bottom-left'
  timeout?: number
  width?: number
  height?: number
  voiceEnabled?: boolean
  maxDuration?: number
  userEmail?: string
}

const runtimeConfig: EmbedConfig = (typeof window !== 'undefined' && (window as any).LAABPRO_CONFIG) || {}

export const WIDGET_CONFIG: WidgetConfig = {
  api: {
    baseUrl: runtimeConfig.apiUrl || import.meta.env.VITE_API_URL || 'https://laabpro-api.onrender.com',
    timeout: runtimeConfig.timeout ?? 30000
  },
  ui: {
    width: runtimeConfig.width ?? 380,
    height: runtimeConfig.height ?? 600
  },
  voice: {
    enabled: runtimeConfig.voiceEnabled ?? true,
    maxDuration: runtimeConfig.maxDuration ?? 60000
  }
}

export const USER_CONFIG = {
  email: runtimeConfig.userEmail || 'user@example.com',
  name: runtimeConfig.companyName || 'Usuario Demo'
}
