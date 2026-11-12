<template>
  <div class="page">
    <h2 class="page-title">系统配置</h2>
    <p class="page-desc">管理个人资料与系统基础配置。昵称修改后会同步到侧边栏与聊天室。</p>

    <el-card class="panel" shadow="never">
      <template #header>
        <span class="panel-title">个人资料</span>
      </template>

      <el-form :model="form" label-width="88px" class="profile-form" @submit.prevent>
        <el-form-item label="登录账号">
          <el-input :model-value="username" disabled />
        </el-form-item>

        <el-form-item label="昵称">
          <el-input
            v-model="form.displayName"
            maxlength="32"
            show-word-limit
            placeholder="请输入昵称，1~32 个字符"
            @keydown.enter.prevent="save"
          />
        </el-form-item>

        <el-form-item v-if="error" label=" ">
          <span class="form-error">{{ error }}</span>
        </el-form-item>

        <el-form-item label=" ">
          <el-button type="primary" :loading="saving" @click="save">保存</el-button>
          <el-button text @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="card-grid">
      <div v-for="item in todos" :key="item.title" class="card">
        <h3 class="card-title">{{ item.title }}</h3>
        <p class="card-desc">{{ item.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { computed, reactive, ref } from 'vue'

import { updateProfile } from '@/api/auth'
import { authState, updateUser } from '@/store/auth'
import { normalizeNickname } from '@/utils/profile'

const username = computed(() => authState.user?.username || '')
const currentNickname = computed(() => authState.user?.displayName || '')

const form = reactive({ displayName: currentNickname.value })
const saving = ref(false)
const error = ref('')

const todos = [
  { title: '用户管理', desc: '维护后台账号与所属角色（待建设）。' },
  { title: '角色管理', desc: '配置角色可见的菜单与操作权限（待建设）。' },
]

function reset() {
  form.displayName = currentNickname.value
  error.value = ''
}

async function save() {
  const { value, error: message } = normalizeNickname(form.displayName)
  if (message) {
    error.value = message
    return
  }

  saving.value = true
  error.value = ''
  try {
    const user = await updateProfile(value)
    updateUser(user)
    form.displayName = user.displayName
    ElMessage.success('昵称已更新，聊天室会显示新昵称')
  } catch (err) {
    error.value = err.message || '保存失败'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.page-title {
  margin: 0 0 8px;
  font-size: 20px;
  color: #111827;
}

.page-desc {
  margin: 0 0 20px;
  color: #6b7280;
  font-size: 13px;
}

.panel {
  max-width: 560px;
  border-radius: 8px;
}

.panel-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.profile-form {
  padding-top: 4px;
}

.form-error {
  color: #dc2626;
  font-size: 13px;
}

.card-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  max-width: 720px;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}

.card-title {
  margin: 0 0 8px;
  font-size: 15px;
  color: #111827;
}

.card-desc {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: #6b7280;
}
</style>
