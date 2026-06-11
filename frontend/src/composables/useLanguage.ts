import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { storage } from '@/utils/storage'

export function useLanguage() {
  const { locale, availableLocales } = useI18n()
  const currentLanguage = ref(locale.value)

  const detectLanguage = (): string => {
    const stored = storage.get<string>('language')
    if (stored && availableLocales.includes(stored)) return stored
    
    const browserLang = navigator.language.split('-')[0]
    return availableLocales.includes(browserLang) ? browserLang : 'es'
  }

  const setLanguage = (code: string) => {
    if (!availableLocales.includes(code)) return
    locale.value = code
    currentLanguage.value = code
    storage.set('language', code)
  }

  const initLanguage = () => setLanguage(detectLanguage())

  return { currentLanguage, setLanguage, initLanguage }
}
