import axios from 'axios'
import { WIDGET_CONFIG } from '@/config/widget.config'
import { HEADERS, STORAGE_KEYS } from '@/constants'

const api = axios.create({
  baseURL: WIDGET_CONFIG.api.baseUrl,
  timeout: WIDGET_CONFIG.api.timeout,
  headers: { 
    [HEADERS.CONTENT_TYPE]: HEADERS.APPLICATION_JSON 
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
  if (token) {
    config.headers.Authorization = `${HEADERS.BEARER_PREFIX}${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject({ 
    message: error.response?.data?.detail || error.response?.data?.message || error.message 
  })
)

export default api
