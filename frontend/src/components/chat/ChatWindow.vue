<template>
  <div class="w-screen h-[100dvh] md:w-[380px] md:h-[600px] md:rounded-xl bg-white shadow-2xl flex flex-col overflow-hidden fixed md:relative inset-0 md:inset-auto">
    <ChatHeader @close="$emit('close')" />
    <ChatMessages />
    <ChatInput />
  </div>
</template>

<script setup>
import ChatHeader from './ChatHeader.vue'
import ChatMessages from './ChatMessages.vue'
import ChatInput from './ChatInput.vue'
defineEmits(['close'])
</script>
