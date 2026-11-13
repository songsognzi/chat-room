import request from './request'

export async function sendChatMessage(content) {
  const body = await request.post('/chat/messages', { content })
  return body.data
}
