import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'

import App from './App.vue'
import { onUnauthorized } from './api/request'
import router, { applyMenuRoutes } from './router'
import { clearSession, isAuthenticated } from './store/auth'
import { loadMenus, menuState, resetMenus } from './store/menus'

/** 后端不可用时给出提示与重试入口，避免把用户误踢回登录页。 */
function renderBootFailure(message) {
  const container = document.getElementById('app')
  if (!container) return

  container.textContent = ''
  const box = document.createElement('div')
  box.style.cssText =
    'max-width:520px;margin:80px auto;padding:24px;border:1px solid #e5e7eb;border-radius:8px;text-align:center'

  const title = document.createElement('h2')
  title.textContent = '无法连接后端服务'
  title.style.cssText = 'margin:0 0 8px;font-size:18px;color:#111827'

  const desc = document.createElement('p')
  desc.textContent = message || '请确认后端已启动后重试'
  desc.style.cssText = 'margin:0 0 16px;font-size:13px;line-height:1.6;color:#6b7280'

  const button = document.createElement('button')
  button.textContent = '重新加载'
  button.style.cssText =
    'padding:8px 16px;border:none;border-radius:6px;background:#2563eb;color:#fff;font-size:14px;cursor:pointer'
  button.addEventListener('click', () => window.location.reload())

  box.append(title, desc, button)
  container.appendChild(box)
}

async function bootstrap() {
  // 登录态失效：清会话 + 移除旧菜单路由，再回到登录页（无需整页刷新）
  onUnauthorized(() => {
    const current = router.currentRoute.value
    if (current.path === '/login') return

    clearSession()
    resetMenus()
    applyMenuRoutes([])
    router.replace({ path: '/login', query: { redirect: current.fullPath } })
  })

  if (isAuthenticated()) {
    const menus = await loadMenus()

    if (menus.length > 0) {
      applyMenuRoutes(menus)
    } else if (menuState.errorStatus === 401) {
      clearSession()
    } else if (menuState.error) {
      // 网络抖动 / 后端未启动：保留登录态，提示重试，不要静默登出
      renderBootFailure(menuState.error)
      return
    } else {
      // 登录有效但账号没有任何菜单
      clearSession()
    }
  }

  const app = createApp(App)
  app.use(router)
  app.use(ElementPlus, { locale: zhCn })
  await router.isReady()
  app.mount('#app')
}

bootstrap()
