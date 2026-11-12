<template>
  <el-card class="panel" shadow="never">
    <template #header>
      <div class="panel-header">
        <span class="panel-title">登录信息</span>
        <el-button size="small" :loading="loading" @click="load">刷新</el-button>
      </div>
    </template>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" class="alert" />

    <el-table
      v-loading="loading"
      :data="logs"
      border
      stripe
      size="default"
      empty-text="暂无登录记录"
      style="width: 100%"
    >
      <el-table-column prop="loginAt" label="登录时间" width="190" />
      <el-table-column prop="username" label="账号" width="140" />
      <el-table-column prop="ip" label="登录 IP" width="150" />
      <el-table-column prop="userAgent" label="终端 / 浏览器" min-width="220" show-overflow-tooltip />
      <el-table-column label="结果" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="statusMeta(row.status).type" effect="light" disable-transitions>
            {{ statusMeta(row.status).label }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <p class="panel-footer">共 {{ logs.length }} 条记录，最多展示最近 50 条。</p>
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'

import { fetchLoginLogs } from '@/api/loginLogs'
import { statusMeta } from '@/utils/loginLog'

const logs = ref([])
const loading = ref(false)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    logs.value = await fetchLoginLogs()
  } catch (err) {
    logs.value = []
    error.value = err.message || '加载登录信息失败'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.panel {
  border-radius: 8px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.alert {
  margin-bottom: 12px;
}

.panel-footer {
  margin: 12px 0 0;
  font-size: 12px;
  color: #9ca3af;
}
</style>
