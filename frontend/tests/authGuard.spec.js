import { describe, expect, it } from 'vitest'

import { createAuthGuard } from '../src/router/authGuard.js'

function runGuard(guard, to) {
  return guard(to, { path: '/' })
}

describe('authGuard', () => {
  it('未登录访问受保护页面时跳转登录页并带上 redirect', () => {
    const guard = createAuthGuard({ isAuthenticated: () => false })

    const result = runGuard(guard, { path: '/system', fullPath: '/system' })

    expect(result).toEqual({ path: '/login', query: { redirect: '/system' } })
  })

  it('未登录访问登录页时直接放行', () => {
    const guard = createAuthGuard({ isAuthenticated: () => false })

    const result = runGuard(guard, { path: '/login', fullPath: '/login' })

    expect(result).toBe(true)
  })

  it('已登录访问登录页时跳回首页', () => {
    const guard = createAuthGuard({ isAuthenticated: () => true })

    const result = runGuard(guard, { path: '/login', fullPath: '/login' })

    expect(result).toEqual({ path: '/' })
  })

  it('已登录访问受保护页面时放行', () => {
    const guard = createAuthGuard({ isAuthenticated: () => true })

    const result = runGuard(guard, { path: '/analysis', fullPath: '/analysis' })

    expect(result).toBe(true)
  })
})
