import { createI18n } from 'vue-i18n'
import es from './locales/es.json'
import en from './locales/en.json'
import pt from './locales/pt.json'

export const i18n = createI18n({
  legacy: false,
  locale: 'es',
  fallbackLocale: 'es',
  messages: { es, en, pt }
})
