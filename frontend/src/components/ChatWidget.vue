<template>
  <div class="fixed bottom-3 right-3 md:bottom-5 md:right-5 z-[1050]">
    <Transition name="fade" mode="out-in">
      <ChatWindow v-if="isOpen" @close="toggleChat" />
      <ChatBubble v-else @click="toggleChat" :unread="unreadCount" />
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useChatStore } from '@/store/chat'
import ChatBubble from './chat/ChatBubble.vue'
import ChatWindow from './chat/ChatWindow.vue'

const chatStore = useChatStore()
const isOpen = ref(false)
const unreadCount = computed(() => chatStore.unreadCount)

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) chatStore.markAllAsRead()
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
