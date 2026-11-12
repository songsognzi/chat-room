import { buildRoutes } from './buildRoutes'

/**
 * 生成「按菜单注册子路由」的函数。
 * vue-router 4 支持 removeRoute，因此每次应用前先移除本函数上次注册的路由，
 * 保证切换账号后不会残留上一个账号的菜单权限。
 */
export function createMenuRouteApplier(router, { parentName = 'layout', views = {}, fallback } = {}) {
  let appliedNames = []

  return function applyMenuRoutes(menus = []) {
    appliedNames.forEach((name) => {
      if (router.hasRoute(name)) {
        router.removeRoute(name)
      }
    })
    appliedNames = []

    const menuRoutes = buildRoutes(menus, { views, fallback })
    menuRoutes.forEach((route) => {
      router.addRoute(parentName, route)
      appliedNames.push(route.name)
    })
    return menuRoutes
  }
}
