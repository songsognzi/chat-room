import { describe, expect, it } from 'vitest'

import { insertEmoji, mergeMessages } from '../src/utils/chat.js'

function msg(id, createdAt, content = `m${id}`) {
  return { id, username: 'admin', displayName: '系统管理员', content, createdAt }
}

describe('mergeMessages', () => {
  it('把新消息追加到历史消息之后', () => {
    const merged = mergeMessages([msg(1, '2026-11-12 10:00:00')], [msg(2, '2026-11-12 10:00:05')])

    expect(merged.map((m) => m.id)).toEqual([1, 2])
  })

  it('同一个 id 不会重复出现（历史与实时回显去重）', () => {
    const merged = mergeMessages([msg(1, '2026-11-12 10:00:00')], [msg(1, '2026-11-12 10:00:00')])

    expect(merged).toHaveLength(1)
  })

  it('乱序到达时按 createdAt 升序排列', () => {
    const merged = mergeMessages(
      [msg(2, '2026-11-12 10:00:05')],
      [msg(1, '2026-11-12 10:00:00'), msg(3, '2026-11-12 10:00:09')],
    )

    expect(merged.map((m) => m.id)).toEqual([1, 2, 3])
  })

  it('超过上限时只保留最新的 limit 条', () => {
    const merged = mergeMessages(
      [msg(1, '2026-11-12 10:00:00'), msg(2, '2026-11-12 10:00:01')],
      [msg(3, '2026-11-12 10:00:02')],
      { limit: 2 },
    )

    expect(merged.map((m) => m.id)).toEqual([2, 3])
  })

  it('历史为空时直接返回新消息', () => {
    const merged = mergeMessages([], [msg(7, '2026-11-12 10:00:00')])

    expect(merged.map((m) => m.id)).toEqual([7])
  })
})

describe('insertEmoji', () => {
  it('在光标位置插入表情', () => {
    const result = insertEmoji('你好世界', '😀', 2)

    expect(result.text).toBe('你好😀世界')
    expect(result.cursor).toBe(4)
  })

  it('有选中内容时用表情替换选区', () => {
    const result = insertEmoji('你好世界', '😀', 2, 4)

    expect(result.text).toBe('你好😀')
    expect(result.cursor).toBe(4)
  })

  it('光标越界时追加到末尾', () => {
    const result = insertEmoji('你好', '😀', 99)

    expect(result.text).toBe('你好😀')
    expect(result.cursor).toBe(4)
  })

  it('光标为负数时按开头处理', () => {
    const result = insertEmoji('你好', '😀', -5)

    expect(result.text).toBe('😀你好')
    expect(result.cursor).toBe(2)
  })

  it('空文本也能插入表情', () => {
    const result = insertEmoji('', '😀', 0)

    expect(result.text).toBe('😀')
    expect(result.cursor).toBe(2)
  })
})
