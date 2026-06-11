import api from './api'

export const voiceService = {
  async speechToText(audioBlob: Blob, language = 'auto'): Promise<{ text: string }> {
    const formData = new FormData()
    formData.append('audio', audioBlob)
    formData.append('language', language)
    return api.post('/voice/speech-to-text', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
  },

  async textToSpeech(text: string, language = 'es'): Promise<Blob> {
    const response = await api.post('/voice/text-to-speech', { text, language }, { responseType: 'blob' })
    return response as unknown as Blob
  }
}
