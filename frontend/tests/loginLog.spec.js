import { describe, expect, it } from 'vitest'

import { statusMeta } from '../src/utils/loginLog.js'

describe('statusMeta', () => {
  it('把 success 映射为成功标签', () => {
    expect(statusMeta('success')).toEqual({ label: '成功', type: 'success' })
  })

  it('把 failed 映射为失败标签', () => {
    expect(statusMeta('failed')).toEqual({ label: '失败', type: 'danger' })
  })

  it('遇到未知状态时原样展示且不报错', () => {
    expect(statusMeta('unknown')).toEqual({ label: 'unknown', type: 'info' })
  })

  it('状态为空时兜底为未知', () => {
    expect(statusMeta('')).toEqual({ label: '未知', type: 'info' })
  })
})
