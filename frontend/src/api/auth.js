import request from './request'

export async function login(username, password) {
  const body = await request.post('/auth/login', { username, password })
  return body.data
}

export async function updateProfile(displayName) {
  const body = await request.put('/auth/profile', { displayName })
  return body.data.user
}
