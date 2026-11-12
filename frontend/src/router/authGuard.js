export const LOGIN_PATH = '/login'

/**
 * 全局路由守卫（vue-router 4 返回式写法）：
 * 未登录只能停在登录页，已登录不再回登录页。
 */
export function createAuthGuard({ isAuthenticated, loginPath = LOGIN_PATH }) {
  return (to) => {
    const authed = isAuthenticated()

    if (to.path === loginPath) {
      return authed ? { path: '/' } : true
    }

    if (!authed) {
      return { path: loginPath, query: { redirect: to.fullPath } }
    }

    return true
  }
}
