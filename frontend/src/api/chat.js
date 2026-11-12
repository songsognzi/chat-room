import request from './request'

export async function fetchChatMessages() {
  const body = await request.get('/chat/messages')
  return body.data || []
}

export async function sendChatMessage(content) {
  const body = await request.post('/chat/messages', { content })
  return body.data
}
