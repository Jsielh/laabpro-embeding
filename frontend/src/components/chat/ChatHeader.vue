<template>
  <div class="flex items-center justify-between px-3 py-3 md:p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white">
    <div class="flex items-center gap-2 md:gap-3">
      <div class="w-8 h-8 md:w-10 md:h-10 bg-white rounded-full flex items-center justify-center text-blue-500 font-bold text-lg md:text-xl"></div>
      <div>
        <h3 class="font-semibold text-sm md:text-base">{{ title }}</h3>
        <p class="text-xs md:text-sm opacity-90">En línea</p>
      </div>
    </div>
    <button @click="$emit('close')" class="w-8 h-8 hover:bg-white/20 rounded-lg flex items-center justify-center transition active:scale-95">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const title = computed(() => t('chat.title'))
defineEmits(['close'])
</script>
