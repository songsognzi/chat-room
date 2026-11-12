import { io } from 'socket.io-client'

/**
 * 建立聊天室 socket 连接：token 放在 auth 里，后端 connect 时校验 token 与菜单权限。
 * 走 Vite 的 /socket.io 代理（ws: true），因此同源、无需额外配置 CORS。
 */
export function createChatSocket(token) {
  return io('/', {
    path: '/socket.io',
    auth: { token },
    // 后端用 threading 模式（Werkzeug 无原生 WebSocket），长轮询即可实时推送；
    // 换成 eventlet/gevent 后可改为 ['websocket', 'polling']。
    transports: ['polling'],
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
  })
}
