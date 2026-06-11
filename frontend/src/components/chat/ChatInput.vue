<template>
  <div class="p-3 md:p-4 bg-white border-t">
    <div v-if="fileError" class="mb-2 px-3 py-1.5 bg-red-50 rounded-lg text-sm text-red-600">
      {{ fileError }}
    </div>
    <div v-if="selectedFile" class="flex items-center gap-2 mb-2 px-3 py-1.5 bg-blue-50 rounded-lg text-sm">
      <svg class="w-4 h-4 text-blue-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span class="flex-1 truncate text-gray-700">{{ selectedFile.name }}</span>
      <button @click="removeFile" class="text-gray-400 hover:text-red-500 transition flex-shrink-0">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <div class="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2">
      <button @click="openFilePicker" class="text-gray-400 hover:text-blue-500 transition active:scale-95 flex-shrink-0" title="Adjuntar archivo">
        <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
        </svg>
      </button>
      <input
        ref="fileInput"
        @change="handleFileSelect"
        type="file"
        :accept="FILE_CONFIG.supportedExtensions.map(e => '.' + e).join(',')"
        class="hidden"
      />
      <input
        v-model="message"
        @keydown.enter="handleSend"
        type="text"
        placeholder="Escribe un mensaje..."
        class="flex-1 bg-transparent outline-none text-sm md:text-base"
        :disabled="isDisabled"
      />
      <VoiceRecorder v-if="showVoice" @audio="handleAudio" />
      <button @click="handleSend" :disabled="!canSend" class="text-blue-500 disabled:opacity-30 active:scale-95 transition">
        <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useChat } from '@/composables/useChat'
import { useFileUpload } from '@/composables/useFileUpload'
import { FILE_CONFIG } from '@/constants'
import VoiceRecorder from '../voice/VoiceRecorder.vue'

const { sendMessage, sendVoiceMessage, sendFileMessage } = useChat()
const message = ref('')
const fileInput = ref(null)
const { selectedFile, fileError, selectFile, removeFile } = useFileUpload()

const props = defineProps({
  showVoice: { type: Boolean, default: true },
  isDisabled: { type: Boolean, default: false }
})

const canSend = computed(() => (message.value.trim().length > 0 || selectedFile.value) && !props.isDisabled)

const openFilePicker = () => fileInput.value?.click()

const handleFileSelect = (e) => {
  const file = e.target.files?.[0]
  if (file) selectFile(file)
  e.target.value = ''
}

const handleSend = () => {
  if (!canSend.value) return
  if (selectedFile.value) {
    sendFileMessage(selectedFile.value, message.value.trim())
    removeFile()
  } else {
    sendMessage(message.value.trim())
  }
  message.value = ''
}

const handleAudio = async (blob) => await sendVoiceMessage(blob)
</script>
