<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">后台管理系统</div>
      <nav class="menu">
        <router-link
          v-for="menu in menus"
          :key="menu.code"
          :to="menu.path"
          class="menu-item"
          active-class="is-active"
        >
          <span class="menu-icon">{{ iconOf(menu.icon) }}</span>
          <span class="menu-name">{{ menu.name }}</span>
        </router-link>
      </nav>
      <p v-if="error" class="menu-error">{{ error }}</p>
    </aside>

    <section class="main">
      <header class="header">
        <span class="header-title">{{ currentTitle }}</span>
        <div class="header-user">
          <span class="user-name">{{ userName }}</span>
          <button class="logout" type="button" @click="logout">退出登录</button>
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { authState, clearSession } from '@/store/auth'
import { menuState, resetMenus } from '@/store/menus'

const ICONS = {
  setting: '⚙️',
  chart: '📊',
  log: '🧾',
  chat: '💬',
}

const route = useRoute()
const router = useRouter()

const menus = computed(() => menuState.list)
const error = computed(() => menuState.error)
const userName = computed(() => {
  const user = authState.user
  return user ? user.displayName || user.username : ''
})
const currentTitle = computed(() => route.meta.title || '后台管理系统')

watch(
  currentTitle,
  (title) => {
    document.title = `${title} - 后台管理系统`
  },
  { immediate: true },
)

function iconOf(icon) {
  return ICONS[icon] || '📁'
}

function logout() {
  clearSession()
  resetMenus()
  router.replace('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  flex: 0 0 220px;
  background: #1f2937;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  padding: 16px 0;
  box-sizing: border-box;
}

.brand {
  font-size: 16px;
  font-weight: 600;
  padding: 8px 20px 20px;
  letter-spacing: 1px;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  color: #d1d5db;
  text-decoration: none;
  font-size: 14px;
}

.menu-item:hover {
  background: #374151;
  color: #ffffff;
}

.menu-item.is-active {
  background: #2563eb;
  color: #ffffff;
}

.menu-error {
  margin: 16px 20px 0;
  font-size: 12px;
  line-height: 1.6;
  color: #fca5a5;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f3f4f6;
}

.header {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: #374151;
}

.logout {
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  border-radius: 6px;
  padding: 5px 10px;
  font-size: 13px;
  cursor: pointer;
}

.logout:hover {
  border-color: #2563eb;
  color: #2563eb;
}

.content {
  padding: 24px;
}
</style>
