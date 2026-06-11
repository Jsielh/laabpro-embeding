<template>
  <div class="flex items-center gap-0.5">
    <span v-for="i in 4" :key="i" class="w-1 h-4 bg-current rounded-full animate-pulse" :style="{ animationDelay: `${i * 0.1}s` }"></span>
  </div>
</template>
