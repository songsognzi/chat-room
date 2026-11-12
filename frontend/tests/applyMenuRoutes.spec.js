import { describe, expect, it } from 'vitest'

import { createMenuRouteApplier } from '../src/router/applyMenuRoutes.js'

const ADMIN_MENUS = [
  { code: 'system', name: '系统配置', path: '/system', component: 'system/index', icon: 'setting', sort: 10 },
  { code: 'analysis', name: '统计分析', path: '/analysis', component: 'analysis/index', icon: 'chart', sort: 20 },
]

const ANALYST_MENUS = [ADMIN_MENUS[1]]

function createFakeRouter() {
  const routes = new Map()
  return {
    routes,
    addRoute(parentOrRoute, route) {
      const record = route || parentOrRoute
      routes.set(record.name, record)
    },
    hasRoute(name) {
      return routes.has(name)
    },
    removeRoute(name) {
      routes.delete(name)
    },
    names() {
      return Array.from(routes.keys())
    },
  }
}

describe('createMenuRouteApplier', () => {
  it('把菜单路由注册到 layout 父路由下', () => {
    const router = createFakeRouter()
    const apply = createMenuRouteApplier(router, { views: {}, fallback: {} })

    apply(ADMIN_MENUS)

    expect(router.names()).toEqual(['system', 'analysis'])
  })

  it('切换账号后旧菜单路由被移除，只保留新账号的菜单', () => {
    const router = createFakeRouter()
    const apply = createMenuRouteApplier(router, { views: {}, fallback: {} })

    apply(ADMIN_MENUS)
    apply(ANALYST_MENUS)

    expect(router.names()).toEqual(['analysis'])
  })

  it('重复应用同一批菜单不会产生重复路由', () => {
    const router = createFakeRouter()
    const apply = createMenuRouteApplier(router, { views: {}, fallback: {} })

    apply(ADMIN_MENUS)
    apply(ADMIN_MENUS)

    expect(router.names()).toEqual(['system', 'analysis'])
  })
})
