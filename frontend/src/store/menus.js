import { reactive } from 'vue'

import { fetchMenus } from '@/api/menus'

export const menuState = reactive({
  list: [],
  error: '',
  errorStatus: null,
})

export async function loadMenus() {
  try {
    const menus = await fetchMenus()
    menuState.list = menus
    menuState.error = ''
    menuState.errorStatus = null
    return menus
  } catch (error) {
    console.error('加载菜单失败：', error)
    menuState.list = []
    menuState.error = error.message || '菜单加载失败'
    menuState.errorStatus = error.status || null
    return []
  }
}

export function resetMenus() {
  menuState.list = []
  menuState.error = ''
  menuState.errorStatus = null
}
