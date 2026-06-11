<template>
  <div id="app">
    <ChatWidget />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import ChatWidget from './components/ChatWidget.vue'
import { useLanguage } from './composables/useLanguage'
import { useNotifications } from './composables/useNotifications'
import { useUserStore } from './store/user'
import { USER_CONFIG } from './config/widget.config'

const { initLanguage } = useLanguage()
const { requestPermission } = useNotifications()
const userStore = useUserStore()

onMounted(() => {

  initLanguage()
  
  requestPermission()

  if (!userStore.user.email) {
    userStore.setUser(USER_CONFIG)
  }
})
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>
