const TOKEN_KEY = 'admin_token'
const USER_KEY = 'admin_user'

/**
 * 基于任意 Storage（localStorage/sessionStorage/内存对象）的登录态读写封装。
 */
export function createAuthStorage(storage) {
  return {
    getToken() {
      return storage.getItem(TOKEN_KEY) || ''
    },
    getUser() {
      try {
        return JSON.parse(storage.getItem(USER_KEY))
      } catch (error) {
        return null
      }
    },
    save(token, user) {
      storage.setItem(TOKEN_KEY, token)
      storage.setItem(USER_KEY, JSON.stringify(user || null))
    },
    clear() {
      storage.removeItem(TOKEN_KEY)
      storage.removeItem(USER_KEY)
    },
  }
}
