const STATUS_META = {
  success: { label: '成功', type: 'success' },
  failed: { label: '失败', type: 'danger' },
}

/**
 * 登录状态 → Element Plus 标签文案与配色。
 */
export function statusMeta(status) {
  if (!status) {
    return { label: '未知', type: 'info' }
  }
  return STATUS_META[status] || { label: status, type: 'info' }
}
