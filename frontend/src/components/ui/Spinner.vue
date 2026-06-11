<template>
  <div class="flex flex-col items-center gap-2" :class="centered ? 'justify-center w-full p-8' : ''">
    <div class="border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin" :class="sizeClass"></div>
    <p v-if="text" class="text-sm text-gray-600">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: { type: String, default: 'md', validator: v => ['sm', 'md', 'lg'].includes(v) },
  text: { type: String, default: '' },
  centered: { type: Boolean, default: false }
})

const sizeClass = computed(() => ({
  sm: 'w-5 h-5',
  md: 'w-8 h-8',
  lg: 'w-12 h-12'
}[props.size]))
</script>
