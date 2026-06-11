import { createApp } from 'vue'
import App from './App.vue'
import { pinia } from './store'
import { i18n } from './i18n'
import './assets/styles/variables.css'
import './assets/styles/main.css'
import './assets/styles/animations.css'

createApp(App).use(pinia).use(i18n).mount('#app')
