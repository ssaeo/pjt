import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import HomeView from '@/views/HomeView.vue'
import ArticleList from '@/views/ArticleListView.vue'
import ArticleDetail from '@/views/ArticleDetailView.vue'
import ArticleCreate from '@/views/ArticleCreateView.vue'
import BankMapView from '@/views/BankMapView.vue'
import FinancialProductsView from '@/views/FinancialProductsView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView,
      props: true
    },
    {
      path: '/articles',
      name: 'ArticleList',
      component: ArticleList
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetail',
      component: ArticleDetail
    },
    {
      path: '/articles/create',
      name: 'ArticleCreate',
      component: ArticleCreate
    },
    {
      path: '/bankmap',
      name: 'BankMap',
      component: BankMapView
    },
    {
      path: '/financial-products',
      name: 'FinancialProducts',
      component: FinancialProductsView
    },
    {
      path: '/product/:type/:id',
      name: 'ProductDetail',
      component: ProductDetailView,
      props: true
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