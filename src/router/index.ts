import { createRouter, createWebHistory } from 'vue-router'
import { userStore } from '@/store/userStore'

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
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})


router.beforeEach((to, from, next) => {
  //const userStore = useUserStore()
  
  // 如果路由需要认证但用户未登录
  if (to.meta.requiresAuth && !userStore().isLoggedIn) {
    next({ name: 'login' })
  }
  // 如果用户已登录但访问登录页
  else if (to.name === 'login' && userStore().isLoggedIn) {
    next({ name: 'manage' })
  }
  // 其他情况正常导航
  else {
    next()
  }
})

export default router