import { ref } from 'vue'

export function useNotifications() {
  const hasPermission = ref(false)
  const audioCache: Record<string, HTMLAudioElement> = {}

  const requestPermission = async (): Promise<boolean> => {
    if (!('Notification' in window)) return false
    if (Notification.permission === 'granted') {
      hasPermission.value = true
      return true
    }
    const permission = await Notification.requestPermission()
    hasPermission.value = permission === 'granted'
    return hasPermission.value
  }

  const playNotification = async (type: 'send' | 'notification' = 'notification') => {
    try {
      const path = type === 'send' ? '/audio/send.mp3' : '/audio/notification.mp3'
      if (audioCache[type]) {
        audioCache[type].currentTime = 0
        await audioCache[type].play()
      } else {
        audioCache[type] = new Audio(path)
        await audioCache[type].play()
      }
    } catch (error) {
      console.error('Audio error:', error)
    }
  }

  return { hasPermission, requestPermission, playNotification }
}
