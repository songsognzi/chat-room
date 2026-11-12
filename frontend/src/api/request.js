import axios from 'axios'

import { authStorage } from '@/utils/browserStorage'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

let unauthorizedHandler = null

export function onUnauthorized(handler) {
  unauthorizedHandler = handler
}

request.interceptors.request.use((config) => {
  const token = authStorage.getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

function wrapError(message, { status, code } = {}) {
  const wrapped = new Error(message)
  wrapped.status = status
  wrapped.code = code
  return wrapped
}

request.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && body.code !== 0) {
      return Promise.reject(
        wrapError(body.message || '请求失败', { status: response.status, code: body.code }),
      )
    }
    return body
  },
  (error) => {
    const status = error.response && error.response.status
    const body = error.response && error.response.data

    if (status === 401 && unauthorizedHandler) {
      unauthorizedHandler()
    }

    return Promise.reject(
      wrapError((body && body.message) || error.message || '网络异常', {
        status,
        code: body && body.code,
      }),
    )
  },
)

export default request
