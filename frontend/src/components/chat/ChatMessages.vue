<template>
  <div ref="messagesContainer" class="flex-1 overflow-y-auto p-3 md:p-4 space-y-3 bg-gray-50">
    <ChatMessage v-for="msg in messages" :key="msg.id" :message="msg" />
    <ChatTyping v-if="isTyping" />
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '@/store/chat'
import ChatMessage from './ChatMessage.vue'
import ChatTyping from './ChatTyping.vue'

const chatStore = useChatStore()
const container = ref(null)
const messages = computed(() => chatStore.messages)
const isTyping = computed(() => chatStore.isTyping)

const scrollToBottom = () => nextTick(() => container.value?.scrollTo({ top: container.value.scrollHeight, behavior: 'smooth' }))

watch([() => messages.value.length, isTyping], scrollToBottom)
</script>
