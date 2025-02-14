import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/userStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue')
    },
    {
      path: '/manage',
      name: 'manage',
      component: () => import('@/views/ManagePage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/',
      redirect: '/manage'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router