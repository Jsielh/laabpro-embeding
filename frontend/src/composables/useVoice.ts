import { ref, Ref } from 'vue'

export function useVoice() {
  const isRecording = ref(false)
  const mediaRecorder: Ref<MediaRecorder | null> = ref(null)
  const audioChunks: Ref<Blob[]> = ref([])

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []

    mediaRecorder.value.ondataavailable = (e: BlobEvent) => {
      if (e.data.size > 0) audioChunks.value.push(e.data)
    }

    mediaRecorder.value.start()
    isRecording.value = true
  }

  const stopRecording = (): Promise<Blob | null> => {
    return new Promise((resolve) => {
      if (!mediaRecorder.value || !isRecording.value) return resolve(null)

      mediaRecorder.value.onstop = () => {
        const blob = new Blob(audioChunks.value, { type: 'audio/webm' })
        mediaRecorder.value?.stream.getTracks().forEach(t => t.stop())
        isRecording.value = false
        audioChunks.value = []
        resolve(blob)
      }

      mediaRecorder.value.stop()
    })
  }

  return { isRecording, startRecording, stopRecording }
}
