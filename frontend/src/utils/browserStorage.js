import { createAuthStorage } from './authStorage'

/**
 * 浏览器端的登录态存储实例（localStorage）。
 * 独立成模块，便于测试环境只引用纯函数版本。
 */
export const authStorage = createAuthStorage(window.localStorage)
