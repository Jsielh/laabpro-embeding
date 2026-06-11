<template>
  <button @click="toggleRecording" :disabled="isDisabled" class="text-gray-600 hover:text-blue-500 disabled:opacity-30 transition active:scale-95">
    <svg v-if="!isRecording" class="w-5 h-5 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
    </svg>
    <AudioWave v-else />
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { useVoice } from '@/composables/useVoice'
import AudioWave from './AudioWave.vue'

const props = defineProps({ isDisabled: { type: Boolean, default: false }})
const emit = defineEmits(['audio', 'error'])
const { startRecording, stopRecording, isRecording } = useVoice()

const toggleRecording = async () => {
  try {
    if (isRecording.value) {
      const blob = await stopRecording()
      emit('audio', blob)
    } else {
      await startRecording()
    }
  } catch (error) {
    emit('error', error)
  }
}
</script>
