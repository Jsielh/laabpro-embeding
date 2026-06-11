export const ERROR_MESSAGES = {
  CHAT: {
    SEND_FAILED: 'Error. Intenta de nuevo.',
    VOICE_PROCESSING: 'Error procesando voz.',
    NETWORK_ERROR: 'Error de conexión. Verifica tu internet.',
    TIMEOUT: 'La respuesta tardó demasiado. Intenta de nuevo.',
  },
  API: {
    GENERIC: 'Ha ocurrido un error. Intenta de nuevo.',
    NOT_FOUND: 'No se encontró el recurso solicitado.',
    UNAUTHORIZED: 'No tienes autorización para esta acción.',
    SERVER_ERROR: 'Error del servidor. Intenta más tarde.',
  },
  VALIDATION: {
    EMPTY_MESSAGE: 'El mensaje no puede estar vacío.',
    INVALID_EMAIL: 'Email inválido.',
  }
} as const

export const SUCCESS_MESSAGES = {
  CHAT: {
    SENT: 'Mensaje enviado',
    CLEARED: 'Chat limpiado',
  },
  VOICE: {
    RECORDED: 'Audio grabado exitosamente',
  }
} as const

export const INFO_MESSAGES = {
  CHAT: {
    TYPING: 'Escribiendo...',
    CONNECTING: 'Conectando...',
    PROCESSING: 'Procesando...',
  },
  VOICE: {
    RECORDING: 'Grabando...',
    LISTENING: 'Escuchando...',
  }
} as const

export const DEFAULT_MESSAGES = {
  USER: {
    EMAIL: 'guest@laabpro.com',
    NAME: 'Usuario Demo',
  },
  GREETING: '¡Hola! ¿En qué puedo ayudarte hoy?',
} as const
