import request from './request'

export async function fetchLoginLogs() {
  const body = await request.get('/login-logs')
  return body.data || []
}
