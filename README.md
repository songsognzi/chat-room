# 后台管理系统（Flask + Vue2 骨架）

前后端分离的后台管理骨架：后端 Flask + SQLAlchemy 提供登录鉴权与「按用户权限返回菜单」的接口，前端 Vue2 工程化项目根据菜单动态生成路由与侧边栏。

```
myWeb/
├─ backend/    Flask + SQLAlchemy 后端
│  ├─ app/
│  │  ├─ __init__.py      create_app 工厂（建表 + 种子数据）
│  │  ├─ extensions.py    SQLAlchemy 实例
│  │  ├─ models.py        Menu / User / LoginLog 模型、默认账号/菜单/日志
│  │  ├─ auth.py          token 签发校验 + login_required
│  │  └─ api/
│  │     ├─ auth.py       POST /api/auth/login
│  │     ├─ menus.py      GET /api/menus（当前用户可见菜单）
│  │     └─ login_logs.py GET /api/login-logs（登录记录，需 login-log 菜单权限）
│  ├─ tests/              pytest 用例
│  ├─ run.py              开发入口（127.0.0.1:5000）
│  └─ requirements.txt
└─ frontend/   Vue3 + Vite + vue-router4 前端（组件统一 <script setup>）
   ├─ src/
   │  ├─ api/             请求封装（自动带 token、401 统一处理）
   │  ├─ router/          buildRoutes 菜单→路由、路由守卫、路由装配
   │  ├─ store/           auth（登录态）、menus（菜单）状态
   │  ├─ utils/           authStorage（登录态本地存储封装）
   │  ├─ layout/          侧边栏 + 头部 + 内容区布局
   │  └─ views/           登录页、系统配置、统计分析、登录信息(Element Plus 表格)、404
   ├─ tests/              vitest 用例
   └─ vite.config.js      dev server 8080 + /api 代理到 5000
```

## 启动

后端（首次先装依赖）：

```powershell
cd H:\myWeb\backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py            # http://127.0.0.1:5000
```

前端（需要 Node >= 18，推荐 20）：

```powershell
cd H:\myWeb\frontend
nvm use 20.19.4                              # 可选：本机 nvm 已装 20.19.4
npm install
npm run dev                                  # http://127.0.0.1:8080
```

打开 http://127.0.0.1:8080 ，未登录会被路由守卫送到 `/login`。

## 演示账号

| 账号 | 密码 | 可显示昵称 | 可见菜单 |
| --- | --- | --- | --- |
| admin | admin123 | 系统管理员 | 系统配置、统计分析、登录信息、聊天室 |
| analyst | analyst123 | 数据分析员 | 统计分析、聊天室 |
| zhouyuyan | 1314520 | 周雨嫣 | 统计分析、聊天室 |
| ssz | 1314520 | 宋宋子 | 统计分析、聊天室 |

账号与菜单授权在 `backend/app/models.py` 的 `DEFAULT_USERS` 中定义，首次启动写入数据库（幂等，已有账号不会覆盖）。

## 测试

```powershell
cd H:\myWeb\backend
.\.venv\Scripts\python.exe -m pytest -q

cd H:\myWeb\frontend
npm test
```

## 接口

### POST /api/auth/login

```json
{ "username": "admin", "password": "admin123" }
```

成功（200）：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "token": "eyJ1aWQiOjF9....",
    "user": { "id": 1, "username": "admin", "displayName": "系统管理员" }
  }
}
```

用户名或密码错误：401，`{"code": 1001, "message": "用户名或密码错误"}`。

### GET /api/login-logs

需要 `Authorization: Bearer <token>`，且当前用户必须拥有 `login-log` 菜单权限（否则 403）。返回最近 50 条登录记录，按时间倒序：

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "ip": "127.0.0.1",
      "userAgent": "Chrome 141 / Windows 11",
      "status": "success",
      "loginAt": "2026-11-11 16:48:05"
    }
  ]
}
```

每次登录成功会自动写入一条记录；首次启动若 `login_logs` 为空，会写入几条演示数据。

### GET /api/menus

需要请求头 `Authorization: Bearer <token>`，返回**当前登录用户**拥有的菜单：

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    { "id": 1, "code": "system",   "name": "系统配置", "path": "/system",   "component": "system/index",   "icon": "setting", "sort": 10 },
    { "id": 2, "code": "analysis", "name": "统计分析", "path": "/analysis", "component": "analysis/index", "icon": "chart",   "sort": 20 }
  ]
}
```

未登录、token 无效或过期：401，`{"code": 1002, "message": "未登录或登录已过期"}`。

token 为 itsdangerous 签名串，默认有效期 8 小时，密钥取环境变量 `ADMIN_SECRET_KEY`，未设置时使用开发默认值（生产必须覆盖）。

## 新增一个菜单（三步）

1. 后端在 `backend/app/models.py` 的 `DEFAULT_MENUS` 增加一条（`code` 唯一、`sort` 控制顺序），再把它的 `code` 加到对应账号的 `menu_codes`。
2. 前端在 `frontend/src/router/views.js` 增加 `component` 到页面组件的映射。
3. 在 `frontend/src/views/` 下新增对应页面组件。

未注册的 `component` 会自动落到 404 页，不会白屏。

## 实现说明

- 数据库默认 SQLite，文件在 `backend/instance/admin.db`，首次启动自动建表并写入默认菜单与账号。
- 前端 dev server 通过 Vite 代理 `/api` 到后端，因此无需额外配置 CORS。
- 登录态存 localStorage（`admin_token` / `admin_user`），请求拦截器自动加 `Authorization` 头；任意接口返回 401 会清会话并整页跳回登录页。
- 前端技术栈：Vue 3.5（Composition API + `<script setup>`）、vue-router 4、Vite 5、Vitest 2、**Element Plus 2.14**（Vue 3 对应 Element UI 的版本，Vue 2 的 element-ui 无法在当前栈使用）；入口用 `createApp`，状态用 `reactive` 模块 store，路由用 `createRouter` + `createWebHistory`。
- Element Plus 采用全量引入（`main.js` 中 `app.use(ElementPlus, { locale: zhCn })` + 引入 `element-plus/dist/index.css`），当前打包含 Element Plus 后主 chunk 约 1.1MB，后续可改按需引入（`unplugin-vue-components`）减肥。
- 依赖侧固定了 `overrides.rollup = 4.65.1` 并显式声明 `@rollup/rollup-win32-x64-msvc`：内网 npm 镜像没有 4.68.x 的原生二进制，不锁定会导致 `Cannot find module '@rollup/rollup-win32-x64-msvc'`。
- 菜单子路由由 `src/router/applyMenuRoutes.js` 统一注册：每次应用先 `removeRoute` 掉上一批菜单路由再 `addRoute`，所以切换账号是**同页内**完成，不会整页刷新，也不会残留上一个账号的路由。
- 路由守卫采用 vue-router 4 的返回式写法（返回 `true` 放行，返回 location 重定向）。
- 菜单目前是平铺结构；需要多级菜单时给 `Menu` 增加 `parent_id`，并在 `buildRoutes` 中生成 `children`。
