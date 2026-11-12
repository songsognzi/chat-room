import { reactive } from 'vue'

import { authStorage } from '@/utils/browserStorage'

export const authState = reactive({
  token: authStorage.getToken(),
  user: authStorage.getUser(),
})

export function isAuthenticated() {
  return Boolean(authState.token)
}

export function saveSession(token, user) {
  authStorage.save(token, user)
  authState.token = token
  authState.user = user
}

export function updateUser(user) {
  authStorage.save(authState.token, user)
  authState.user = user
}

export function clearSession() {
  authStorage.clear()
  authState.token = ''
  authState.user = null
}
