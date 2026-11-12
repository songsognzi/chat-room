<template>
  <div class="login-page">
    <form class="login-card" @submit.prevent="submit">
      <h1 class="login-title">后台管理系统</h1>
      <p class="login-subtitle">请使用分配给你的账号登录</p>

      <label class="field">
        <span class="field-label">用户名</span>
        <input v-model.trim="form.username" class="field-input" name="username" autocomplete="username" />
      </label>

      <label class="field">
        <span class="field-label">密码</span>
        <input
          v-model="form.password"
          class="field-input"
          name="password"
          type="password"
          autocomplete="current-password"
        />
      </label>

      <p v-if="error" class="login-error">{{ error }}</p>

      <button class="login-button" type="submit" :disabled="loading">
        {{ loading ? '登录中…' : '登录' }}
      </button>

      <p class="login-hint">演示账号：admin / admin123（两个菜单），analyst / analyst123（仅统计分析）</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { login } from '@/api/auth'
import { applyMenuRoutes } from '@/router'
import { saveSession } from '@/store/auth'
import { loadMenus, resetMenus } from '@/store/menus'

const route = useRoute()
const router = useRouter()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function submit() {
  if (!form.username || !form.password) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  error.value = ''
  try {
    const { token, user } = await login(form.username, form.password)
    saveSession(token, user)

    const menus = await loadMenus()
    applyMenuRoutes(menus)

    const redirect = route.query.redirect
    await router.replace(typeof redirect === 'string' && redirect ? redirect : '/')
  } catch (err) {
    resetMenus()
    error.value = err.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f2937 0%, #2563eb 100%);
  padding: 24px;
}

.login-card {
  width: 340px;
  background: #ffffff;
  border-radius: 12px;
  padding: 28px 24px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.25);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.login-title {
  margin: 0;
  font-size: 20px;
  color: #111827;
  text-align: center;
}

.login-subtitle {
  margin: 0 0 6px;
  font-size: 13px;
  color: #6b7280;
  text-align: center;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 13px;
  color: #374151;
}

.field-input {
  height: 36px;
  padding: 0 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}

.field-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.login-error {
  margin: 0;
  font-size: 13px;
  color: #dc2626;
}

.login-button {
  height: 38px;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
}

.login-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.login-hint {
  margin: 4px 0 0;
  font-size: 12px;
  line-height: 1.6;
  color: #9ca3af;
}
</style>
