<template>
  <div class="flex gap-2" :class="isUser ? 'flex-row-reverse' : ''">
    <div v-if="!isUser" class="w-6 h-6 md:w-8 md:h-8 bg-blue-100 rounded-full flex items-center justify-center text-xs md:text-sm flex-shrink-0"></div>
    <div class="max-w-[80%] md:max-w-[75%]">
      <div class="px-3 py-2 md:px-4 md:py-2 rounded-lg" :class="isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800 shadow-sm'">
        <p class="text-xs md:text-sm break-words" v-html="formattedText"></p>
        <span class="text-[10px] md:text-xs opacity-70 block mt-1">{{ formattedTime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatDate } from '@/utils/date'

const props = defineProps({ message: { type: Object, required: true }})
const isUser = computed(() => props.message.sender === 'user')
const formattedText = computed(() =>
  props.message.text
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
)
const formattedTime = computed(() => formatDate(props.message.timestamp))
</script>
