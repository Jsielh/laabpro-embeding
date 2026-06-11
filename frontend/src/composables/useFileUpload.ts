import { ref, onUnmounted } from 'vue'
import { FILE_CONFIG } from '@/constants'

export function useFileUpload() {
  const selectedFile = ref<File | null>(null)
  const fileError = ref<string | null>(null)
  const previewUrl = ref<string | null>(null)
  let objectUrl: string | null = null

  function selectFile(file: File): boolean {
    fileError.value = null
    if (!FILE_CONFIG.allowedMime.includes(file.type as any)) {
      fileError.value = `Tipo de archivo no soportado. Formatos: ${FILE_CONFIG.supportedExtensions.join(', ')}`
      return false
    }
    if (file.size > FILE_CONFIG.maxSize) {
      fileError.value = 'El archivo supera el tamaño máximo de 10 MB'
      return false
    }
    revokeObjectUrl()
    selectedFile.value = file
    if (file.type.startsWith('image/')) {
      objectUrl = URL.createObjectURL(file)
      previewUrl.value = objectUrl
    }
    return true
  }

  function revokeObjectUrl() {
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl)
      objectUrl = null
    }
    previewUrl.value = null
  }

  function removeFile() {
    revokeObjectUrl()
    selectedFile.value = null
    fileError.value = null
  }

  function reset() {
    removeFile()
  }

  onUnmounted(() => {
    revokeObjectUrl()
  })

  return { selectedFile, previewUrl, fileError, selectFile, removeFile, reset }
}
