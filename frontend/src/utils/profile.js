export const NICKNAME_MAX_LENGTH = 32

/**
 * 规范化昵称：去首尾空格并给出校验提示。
 * 后端 PUT /api/auth/profile 使用相同的规则（1~32 字符）。
 */
export function normalizeNickname(input) {
  const value = typeof input === 'string' ? input.trim() : ''

  if (!value) {
    return { value, error: '昵称不能为空' }
  }

  if (value.length > NICKNAME_MAX_LENGTH) {
    return { value, error: `昵称最多 ${NICKNAME_MAX_LENGTH} 个字符` }
  }

  return { value, error: '' }
}
