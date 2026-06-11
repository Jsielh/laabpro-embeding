import { createApp, type App } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import ChatWidget from './components/ChatWidget.vue'
import es from './i18n/locales/es.json'
import en from './i18n/locales/en.json'
import pt from './i18n/locales/pt.json'
import cssVariables from './assets/styles/variables.css?inline'
import cssMain from './assets/styles/main.css?inline'
import cssAnimations from './assets/styles/animations.css?inline'

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

type Position = 'bottom-right' | 'bottom-left'

declare global {
  interface Window {
    LAABPRO_CONFIG?: EmbedConfig
  }
}

const CONTAINER_ID = 'laabpro-agent-widget'

function buildStyles(): string {
  let css = cssVariables + '\n' + cssMain + '\n' + cssAnimations
  css = css.replace(/:root/g, ':host')
  css = css.replace(/body\s*\{[^}]*\}/g, '')
  css = css.replace(/html\s*\{[^}]*\}/g, '')
  return css
}

function getPositionStyles(position: Position, width: number, height: number): string {
  const right = position === 'bottom-right' ? '20px' : 'auto'
  const left = position === 'bottom-left' ? '20px' : 'auto'
  return `
    :host {
      all: initial;
      display: block;
      position: fixed;
      ${right ? `right: ${right};` : ''}
      ${left ? `left: ${left};` : ''}
      bottom: 20px;
      z-index: 2147483647;
      width: ${width}px;
      height: ${height}px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    :host([hidden]) { display: none; }
  `
}

function createShadowContainer(position: Position, width: number, height: number): ShadowRoot {
  const existing = document.getElementById(CONTAINER_ID)
  if (existing) existing.remove()

  const host = document.createElement('div')
  host.id = CONTAINER_ID
  document.body.appendChild(host)

  const shadow = host.attachShadow({ mode: 'closed' })

  const positionStyle = document.createElement('style')
  positionStyle.textContent = getPositionStyles(position, width, height)
  shadow.appendChild(positionStyle)

  const appStyle = document.createElement('style')
  appStyle.textContent = buildStyles()
  shadow.appendChild(appStyle)

  const mount = document.createElement('div')
  mount.id = 'app'
  shadow.appendChild(mount)

  return shadow
}

function initApp(shadow: ShadowRoot, config: EmbedConfig): App<Element> {
  const i18n = createI18n({
    legacy: false,
    locale: config.locale || 'es',
    fallbackLocale: 'es',
    messages: { es, en, pt }
  })

  const pinia = createPinia()

  const app = createApp(ChatWidget)
  app.use(pinia)
  app.use(i18n)

  const mountPoint = shadow.getElementById('app')
  if (!mountPoint) throw new Error('Mount point not found')

  app.mount(mountPoint)
  return app
}

function initWidget(config?: EmbedConfig): void {
  try {
    const resolvedConfig: EmbedConfig = config || window.LAABPRO_CONFIG || {}
    const position = resolvedConfig.position || 'bottom-right'
    const width = resolvedConfig.width || 380
    const height = resolvedConfig.height || 600

    const shadow = createShadowContainer(position, width, height)
    initApp(shadow, resolvedConfig)
  } catch (err) {
    console.error('[LaabPro Widget] Failed to initialize:', err)
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => initWidget())
} else {
  initWidget()
}

export { initWidget }
