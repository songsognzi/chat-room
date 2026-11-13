<template>
  <section class="chat-panel">
    <aside class="members">
      <header class="members-header">
        <span class="members-title">在线成员</span>
        <el-tag size="small" type="info" disable-transitions>{{ online.length }}</el-tag>
      </header>

      <el-scrollbar class="members-body">
        <ul class="member-list">
          <li
            v-for="user in online"
            :key="user.username"
            class="member"
            :class="{ 'is-me': user.username === myUsername }"
          >
            <el-avatar :size="30" class="member-avatar">{{ initial(user.displayName) }}</el-avatar>
            <span class="member-name">{{ user.displayName }}</span>
            <span v-if="user.username === myUsername" class="member-badge">我</span>
          </li>
        </ul>
        <p v-if="online.length === 0" class="empty-tip">暂无人在线</p>
      </el-scrollbar>

      <footer class="members-footer">
        <span class="self-name">{{ myName }}</span>
        <el-tag size="small" :type="connected ? 'success' : 'warning'" disable-transitions>
          {{ connected ? '已连接' : '连接中…' }}
        </el-tag>
      </footer>
    </aside>

    <div class="room">
      <header class="room-header">
        <span class="room-title">公共聊天室</span>
        <span class="room-sub">仅显示在线成员的实时消息 · 最多 200 条</span>
      </header>

      <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" class="room-alert" />

      <el-scrollbar ref="scroller" class="messages">
        <div class="messages-inner">
          <div
            v-for="message in messages"
            :key="message.id"
            class="message"
            :class="{ 'is-mine': message.username === myUsername }"
          >
            <el-avatar :size="30" class="message-avatar">{{ initial(message.displayName) }}</el-avatar>
            <div class="message-body">
              <div class="message-meta">{{ message.displayName }} · {{ message.createdAt }}</div>
              <div class="message-bubble">{{ message.content }}</div>
            </div>
          </div>

          <p v-if="messages.length === 0" class="empty-tip">
            还没有人说话，发一条试试
          </p>
        </div>
      </el-scrollbar>

      <footer class="composer">
        <div class="composer-toolbar">
          <el-popover placement="top-start" :width="360" trigger="click" popper-class="chat-emoji-popper">
            <template #reference>
              <el-button class="emoji-trigger" size="small" text>😊 表情</el-button>
            </template>

            <div class="chat-emoji-panel">
              <p class="chat-emoji-title">常用表情</p>
              <div class="chat-emoji-grid">
                <button
                  v-for="emoji in EMOJIS"
                  :key="emoji"
                  type="button"
                  class="chat-emoji-item"
                  :title="emoji"
                  @click="pickEmoji(emoji)"
                >
                  {{ emoji }}
                </button>
              </div>

              <p class="chat-emoji-title">颜文字</p>
              <div class="chat-kaomoji-grid">
                <button
                  v-for="face in KAOMOJI"
                  :key="face"
                  type="button"
                  class="chat-kaomoji-item"
                  @click="pickEmoji(face)"
                >
                  {{ face }}
                </button>
              </div>
            </div>
          </el-popover>
        </div>

        <el-input
          ref="inputRef"
          v-model="draft"
          type="textarea"
          :rows="3"
          resize="none"
          maxlength="500"
          show-word-limit
          placeholder="输入消息，Enter 发送，Shift + Enter 换行"
          @keydown.enter.exact.prevent="send"
        />
        <div class="composer-actions">
          <span class="composer-hint">以 {{ myName }} 的身份发送</span>
          <el-button type="primary" :disabled="!draft.trim()" @click="send">发送</el-button>
        </div>
      </footer>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'

import { sendChatMessage } from '@/api/chat'
import { authState } from '@/store/auth'
import { insertEmoji, mergeMessages } from '@/utils/chat'
import { createChatSocket } from '@/utils/chatSocket'

const MAX_MESSAGES = 200
const EMOJIS = [
  '😀', '😁', '😂', '😊', '😍', '😘', '😎', '🤔',
  '😅', '😭', '😡', '🥳', '😴', '🤝', '👍', '👎',
  '👏', '🙏', '💪', '🎉', '🔥', '❤️', '💔', '⭐',
  '✅', '❌', '🚀', '☕', '🌙', '🍀', '🎯', '💡',
]
const KAOMOJI = [
  '(＾▽＾)', '(≧▽≦)', '(￣▽￣)', '(╯°□°)╯', 'Orz', '(｡•́︿•̀｡)',
]

const myUsername = computed(() => authState.user?.username || '')
const myName = computed(() => authState.user?.displayName || authState.user?.username || '')

const messages = ref([])
const online = ref([])
const draft = ref('')
const error = ref('')
const connected = ref(false)
const scroller = ref(null)
const inputRef = ref(null)

let socket = null

function initial(name) {
  return (name || '?').trim().charAt(0).toUpperCase()
}

async function scrollToBottom() {
  await nextTick()
  const wrap = scroller.value && scroller.value.$refs.wrapRef
  if (wrap) {
    wrap.scrollTop = wrap.scrollHeight
  }
}

function connect() {
  socket = createChatSocket(authState.token)

  socket.on('connect', () => {
    connected.value = true
    error.value = ''
  })
  socket.on('disconnect', () => {
    connected.value = false
  })
  socket.on('connect_error', (err) => {
    connected.value = false
    error.value = err.message || '聊天室连接失败'
  })
  socket.on('online_users', (users) => {
    online.value = users || []
  })
  socket.on('chat_message', (message) => {
    messages.value = mergeMessages(messages.value, [message], { limit: MAX_MESSAGES })
    scrollToBottom()
  })
}

function pickEmoji(emoji) {
  const textarea = inputRef.value && inputRef.value.textarea
  const start = textarea ? textarea.selectionStart : draft.value.length
  const end = textarea ? textarea.selectionEnd : draft.value.length

  const result = insertEmoji(draft.value, emoji, start, end)
  draft.value = result.text

  nextTick(() => {
    if (textarea) {
      textarea.focus()
      textarea.setSelectionRange(result.cursor, result.cursor)
    }
  })
}

async function send() {
  const content = draft.value.trim()
  if (!content) return

  draft.value = ''
  if (socket && socket.connected) {
    socket.emit('chat_message', { content })
    return
  }

  // socket 未连上时退回 HTTP 通道，后端同样会广播给在线用户
  try {
    const message = await sendChatMessage(content)
    messages.value = mergeMessages(messages.value, [message], { limit: MAX_MESSAGES })
    scrollToBottom()
  } catch (err) {
    error.value = err.message || '发送失败'
  }
}

onMounted(() => {
  connect()
})

onUnmounted(() => {
  if (socket) {
    socket.disconnect()
    socket = null
  }
})
</script>

<style scoped>
.chat-panel {
  display: flex;
  height: calc(100vh - 104px);
  min-height: 480px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.members {
  width: 220px;
  flex: 0 0 220px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e5e7eb;
  background: #f9fafb;
}

.members-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border-bottom: 1px solid #e5e7eb;
}

.members-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.members-body {
  flex: 1;
  min-height: 0;
}

.member-list {
  list-style: none;
  margin: 0;
  padding: 8px;
}

.member {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
  font-size: 13px;
  color: #374151;
}

.member.is-me {
  background: #eff6ff;
}

.member-avatar {
  flex: 0 0 auto;
  background: #2563eb;
  font-size: 13px;
}

.member-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.member-badge {
  font-size: 11px;
  color: #2563eb;
  border: 1px solid #bfdbfe;
  border-radius: 4px;
  padding: 0 4px;
}

.members-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid #e5e7eb;
  font-size: 12px;
  color: #6b7280;
}

.self-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.room-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.room-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.room-sub {
  font-size: 12px;
  color: #9ca3af;
}

.room-alert {
  margin: 10px 16px 0;
}

.messages {
  flex: 1;
  min-height: 0;
  background: #f3f4f6;
}

.messages-inner {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.message {
  display: flex;
  gap: 10px;
  max-width: 78%;
}

.message-avatar {
  flex: 0 0 auto;
  background: #6b7280;
  font-size: 13px;
}

.message-body {
  min-width: 0;
}

.message-meta {
  font-size: 12px;
  color: #9ca3af;
  margin-bottom: 4px;
}

.message-bubble {
  padding: 9px 12px;
  border-radius: 10px;
  background: #ffffff;
  color: #111827;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}

.message.is-mine {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.is-mine .message-avatar {
  background: #2563eb;
}

.message.is-mine .message-meta {
  text-align: right;
}

.message.is-mine .message-bubble {
  background: #2563eb;
  color: #ffffff;
}

.composer {
  border-top: 1px solid #e5e7eb;
  padding: 12px 16px 14px;
  background: #ffffff;
}

.composer-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.emoji-trigger {
  padding: 0 8px;
  font-size: 13px;
  color: #4b5563;
}

.composer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}

.composer-hint {
  font-size: 12px;
  color: #9ca3af;
}

.empty-tip {
  margin: 24px;
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
}
</style>

<style>
/* 弹层被 teleport 到 body，scoped 样式无法命中，这里用全局样式并限定类名前缀 */
.chat-emoji-panel {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-emoji-title {
  margin: 2px 0;
  font-size: 12px;
  color: #9ca3af;
}

.chat-emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
}

.chat-emoji-item {
  border: none;
  background: transparent;
  font-size: 20px;
  line-height: 1;
  padding: 6px 0;
  border-radius: 6px;
  cursor: pointer;
}

.chat-emoji-item:hover {
  background: #eff6ff;
}

.chat-kaomoji-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.chat-kaomoji-item {
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #374151;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 999px;
  cursor: pointer;
}

.chat-kaomoji-item:hover {
  border-color: #2563eb;
  color: #2563eb;
}
</style>
