<template>
  <button
    @click="$emit('click')"
    class="w-14 h-14 md:w-[60px] md:h-[60px] rounded-full bg-blue-500 text-white shadow-lg hover:scale-110 active:scale-95 transition-transform flex items-center justify-center relative"
  >
    <svg class="w-6 h-6 md:w-8 md:h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
    </svg>
    <span v-if="unread > 0" class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">
      {{ unread }}
    </span>
  </button>
</template>

<script setup>
defineProps({ unread: { type: Number, default: 0 }})
defineEmits(['click'])
</script>
