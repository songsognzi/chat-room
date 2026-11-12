import { describe, expect, it } from 'vitest'

import { normalizeNickname } from '../src/utils/profile.js'

describe('normalizeNickname', () => {
  it('去掉首尾空格后返回昵称', () => {
    const result = normalizeNickname('  管理员小明  ')

    expect(result).toEqual({ value: '管理员小明', error: '' })
  })

  it('空字符串提示昵称不能为空', () => {
    const result = normalizeNickname('')

    expect(result.value).toBe('')
    expect(result.error).toBe('昵称不能为空')
  })

  it('纯空格同样视为空', () => {
    const result = normalizeNickname('    ')

    expect(result.error).toBe('昵称不能为空')
  })

  it('超过 32 个字符时提示过长', () => {
    const result = normalizeNickname('昵'.repeat(33))

    expect(result.error).toBe('昵称最多 32 个字符')
  })

  it('正好 32 个字符是允许的', () => {
    const result = normalizeNickname('昵'.repeat(32))

    expect(result.error).toBe('')
    expect(result.value).toHaveLength(32)
  })
})
