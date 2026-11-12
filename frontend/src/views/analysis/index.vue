<template>
  <div class="page">
    <h2 class="page-title">统计分析</h2>
    <p class="page-desc">按时间维度查看系统关键指标。当前为页面骨架，数据来源待接入。</p>

    <div class="card-grid">
      <div v-for="stat in stats" :key="stat.label" class="card">
        <p class="card-label">{{ stat.label }}</p>
        <p class="card-value">{{ stat.value }}</p>
        <p class="card-trend">{{ stat.trend }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const stats = [
  { label: '今日访问量', value: '1,286', trend: '较昨日 +12%' },
  { label: '活跃用户', value: '328', trend: '较昨日 +4%' },
  { label: '接口调用量', value: '9,451', trend: '较昨日 -2%' },
]
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

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
}

.card-label {
  margin: 0 0 10px;
  font-size: 13px;
  color: #6b7280;
}

.card-value {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.card-trend {
  margin: 8px 0 0;
  font-size: 12px;
  color: #10b981;
}
</style>
