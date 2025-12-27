import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import Commute from '@/views/Commute.vue'
import RoutePlanner from '@/views/RoutePlanner.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/commute',
    name: 'Commute',
    component: Commute,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/route-planner',
    name: 'RoutePlanner',
    component: RoutePlanner,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  try {
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'

    if (to.meta.requiresAuth && !isAuthenticated) {
      next('/login')
    } else if (to.path === '/login' && isAuthenticated) {
      next('/commute')
    } else {
      next()
    }
  } catch (error) {
    console.error('路由守卫错误:', error)
    next('/login')
  }
})

export default router

