<template>
  <div class="flex gap-2">
    <div class="w-6 h-6 md:w-8 md:h-8 bg-blue-100 rounded-full flex items-center justify-center text-xs md:text-sm flex-shrink-0"></div>
    <div class="bg-white px-3 py-2 md:px-4 md:py-3 rounded-lg shadow-sm flex gap-1">
      <span v-for="i in 3" :key="i" class="w-1.5 h-1.5 md:w-2 md:h-2 bg-gray-400 rounded-full typing-dot"></span>
    </div>
  </div>
</template>
