import { describe, expect, it } from 'vitest'

import { createAuthStorage } from '../src/utils/authStorage.js'

function createMemoryStorage() {
  const data = new Map()
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
  }
}

describe('createAuthStorage', () => {
  it('保存后能读回 token 与用户信息', () => {
    const storage = createAuthStorage(createMemoryStorage())

    storage.save('token-123', { username: 'admin', displayName: '系统管理员' })

    expect(storage.getToken()).toBe('token-123')
    expect(storage.getUser()).toEqual({ username: 'admin', displayName: '系统管理员' })
  })

  it('没有登录过时 token 为空字符串、用户为 null', () => {
    const storage = createAuthStorage(createMemoryStorage())

    expect(storage.getToken()).toBe('')
    expect(storage.getUser()).toBeNull()
  })

  it('clear 后清空 token 与用户信息', () => {
    const storage = createAuthStorage(createMemoryStorage())
    storage.save('token-123', { username: 'admin' })

    storage.clear()

    expect(storage.getToken()).toBe('')
    expect(storage.getUser()).toBeNull()
  })

  it('用户信息损坏时返回 null 而不是抛异常', () => {
    const memory = createMemoryStorage()
    memory.setItem('admin_user', '{not-json')
    const storage = createAuthStorage(memory)

    expect(storage.getUser()).toBeNull()
  })
})
