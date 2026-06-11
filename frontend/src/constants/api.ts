export const API_ENDPOINTS = {
  CHAT: {
    MESSAGE: '/ask',
    STREAM: '/ask',
    HISTORY: '/chat/history',
    VOICE: '/chat/voice',
    UPLOAD: '/chat/upload',
  },
  HEALTH: '/health',
} as const

export const API_CONFIG = {
  TIMEOUT: 30000,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
} as const

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const

export const HEADERS = {
  CONTENT_TYPE: 'Content-Type',
  AUTHORIZATION: 'Authorization',
  APPLICATION_JSON: 'application/json',
  MULTIPART_FORM_DATA: 'multipart/form-data',
  BEARER_PREFIX: 'Bearer ',
} as const
