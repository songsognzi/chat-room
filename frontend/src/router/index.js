import { createRouter, createWebHistory } from 'vue-router'

import BasicLayout from '@/layout/BasicLayout.vue'
import NotFound from '@/views/error/NotFound.vue'
import { isAuthenticated } from '@/store/auth'
import { menuState } from '@/store/menus'

import { createMenuRouteApplier } from './applyMenuRoutes'
import { createAuthGuard } from './authGuard'
import { views } from './views'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login/index.vue'),
  },
  {
    path: '/',
    name: 'layout',
    component: BasicLayout,
    redirect: () => (menuState.list[0] ? menuState.list[0].path : '/login'),
    children: [],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export const applyMenuRoutes = createMenuRouteApplier(router, { views, fallback: NotFound })

router.beforeEach(createAuthGuard({ isAuthenticated }))

export default router
