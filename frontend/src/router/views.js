/**
 * 后端菜单里的 component 字段与前端页面组件的映射表。
 * 新增页面时，在这里补一行映射即可。
 */
export const views = {
  'system/index': () => import('@/views/system/index.vue'),
  'analysis/index': () => import('@/views/analysis/index.vue'),
  'login-info/index': () => import('@/views/login-info/index.vue'),
  'chat/index': () => import('@/views/chat/index.vue'),
}
