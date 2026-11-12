import { describe, expect, it } from 'vitest'

import { buildRoutes } from '../src/router/buildRoutes.js'

const MENUS = [
  { code: 'system', name: '系统配置', path: '/system', component: 'system/index', icon: 'setting', sort: 10 },
  { code: 'analysis', name: '统计分析', path: '/analysis', component: 'analysis/index', icon: 'chart', sort: 20 },
]

describe('buildRoutes', () => {
  it('把后端菜单转换为带 path、name 和 meta.title 的路由记录', () => {
    const routes = buildRoutes(MENUS, { views: {} })

    expect(routes.map((route) => route.path)).toEqual(['/system', '/analysis'])
    expect(routes.map((route) => route.name)).toEqual(['system', 'analysis'])
    expect(routes.map((route) => route.meta.title)).toEqual(['系统配置', '统计分析'])
  })

  it('使用 views 中注册的组件渲染菜单页面', () => {
    const System = { name: 'SystemView' }
    const Analysis = { name: 'AnalysisView' }

    const routes = buildRoutes(MENUS, {
      views: { 'system/index': System, 'analysis/index': Analysis },
    })

    expect(routes[0].component).toBe(System)
    expect(routes[1].component).toBe(Analysis)
  })

  it('菜单组件未注册时回退到 fallback 组件', () => {
    const Fallback = { name: 'FallbackView' }

    const routes = buildRoutes([MENUS[0]], { views: {}, fallback: Fallback })

    expect(routes[0].component).toBe(Fallback)
  })
})
