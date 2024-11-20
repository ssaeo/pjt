import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signup',
      name: 'SignUpView',
      component: () => import('@/views/SignUpView.vue')
    },
    {
      path: '/login',
      name: 'LogInView',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: () => import('@/views/ProfileView.vue')
    },
    {
      path: '/articles',
      name: 'ArticleList',
      component: () => import('@/views/ArticleListView.vue')
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetail',
      component: () => import('@/views/ArticleDetailView.vue')
    },
    {
      path: '/articles/create',
      name: 'ArticleCreate',
      component: () => import('@/views/ArticleCreateView.vue')
    }
  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  
  if (to.name === 'ProfileView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && store.isLogin) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'ProfileView' }
  }
})

export default router



