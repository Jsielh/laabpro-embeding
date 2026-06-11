export const APP_CONFIG = {
  NAME: 'LaabPro Agent',
  VERSION: '1.0.0',
  DEFAULT_LANGUAGE: 'es',
  SUPPORTED_LANGUAGES: ['es', 'en', 'pt'] as const,
} as const

export const CHAT_CONFIG = {
  MAX_MESSAGE_LENGTH: 1000,
  MIN_MESSAGE_LENGTH: 1,
  HISTORY_LIMIT: 50,
  AUTO_SCROLL_DELAY: 100,
} as const

export const VOICE_CONFIG = {
  MAX_DURATION: 60000,
  AUDIO_FORMAT: 'webm',
  MIME_TYPE: 'audio/webm',
} as const

export const FILE_CONFIG = {
  maxSize: 20 * 1024 * 1024,
  supportedExtensions: ['txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'] as const,
  imageExtensions: ['jpg', 'jpeg', 'png'] as const,
  allowedMime: [
    'text/plain',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
  ],
} as const

export const UI_CONFIG = {
  WIDGET: {
    WIDTH: 380,
    HEIGHT: 600,
    MIN_WIDTH: 320,
    MIN_HEIGHT: 400,
  },
  ANIMATION: {
    DURATION: 300,
    EASING: 'ease-in-out',
  },
  DEBOUNCE_DELAY: 300,
} as const

export const STORAGE_KEYS = {
  TOKEN: 'widget-token',
  USER: 'widget-user',
  LANGUAGE: 'widget-language',
  THEME: 'widget-theme',
  CHAT_HISTORY: 'widget-chat-history',
} as const
