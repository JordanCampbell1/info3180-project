<script setup>
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"

const route = useRoute()

// Header and footer hidden on login or register
const hideHeader = computed(() =>
  route.path === '/login' || route.path === '/register'
)
</script>

<template>
  <div :style="{ paddingTop: hideHeader ? '0' : '0' }">
    <AppHeader v-if="!hideHeader" />

    <main>
      <RouterView />
    </main>

    <AppFooter v-if="!hideHeader" />
  </div>
</template>

<style>
/* Removed body padding, now handled conditionally in template */
</style>
