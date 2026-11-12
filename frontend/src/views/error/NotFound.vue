<template>
  <div class="not-found">
    <h2>404</h2>
    <p>页面不存在，或你的账号没有该菜单的权限。</p>
    <router-link class="back" to="/">返回首页</router-link>
  </div>
</template>

<style scoped>
.not-found {
  padding: 48px;
  text-align: center;
  color: #374151;
}

.not-found h2 {
  margin: 0 0 8px;
  font-size: 32px;
}

.not-found p {
  margin: 0 0 16px;
  color: #6b7280;
  font-size: 14px;
}

.back {
  color: #2563eb;
  font-size: 14px;
  text-decoration: none;
}
</style>
