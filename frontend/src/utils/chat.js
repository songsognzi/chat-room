/**
 * 合并聊天消息：按 id 去重、按 createdAt 升序、超长时保留最新 limit 条。
 * 后端返回的 createdAt 形如 "2026-11-12 10:00:05"，可直接按字符串比较。
 */
export function mergeMessages(existing = [], incoming = [], { limit = 200 } = {}) {
  const byId = new Map()

  ;[...existing, ...incoming].forEach((message) => {
    if (message && message.id !== undefined && message.id !== null) {
      byId.set(message.id, message)
    }
  })

  const merged = Array.from(byId.values()).sort((a, b) => {
    if (a.createdAt === b.createdAt) {
      return a.id - b.id
    }
    return String(a.createdAt).localeCompare(String(b.createdAt))
  })

  return merged.length > limit ? merged.slice(-limit) : merged
}

/**
 * 在光标处插入表情：有选区则替换选区，越界则夹到文本范围内。
 * 返回新文本和插入后的光标位置，方便调用方把光标放到表情之后。
 */
export function insertEmoji(text = '', emoji = '', start = text.length, end = start) {
  const length = text.length
  const from = Math.min(Math.max(Number.isFinite(start) ? start : length, 0), length)
  const to = Math.min(Math.max(Number.isFinite(end) ? end : from, from), length)

  return {
    text: text.slice(0, from) + emoji + text.slice(to),
    cursor: from + emoji.length,
  }
}
