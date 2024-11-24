import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import HomeView from '@/views/HomeView.vue'
import ArticleList from '@/views/ArticleListView.vue'
import ArticleDetail from '@/views/ArticleDetailView.vue'
import ArticleCreate from '@/views/ArticleCreateView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import BankMapView from '@/views/BankMapView.vue'
import FinancialProductsView from '@/views/FinancialProductsView.vue'
// import ProductDetailView from '@/views/ProductDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ExchangeCalculatorView from '@/views/ExchangeCalculatorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // accounts
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
      beforeEnter: (to, from) => {
        const store = useCounterStore()
        if (store.isLogin) {
          alert('이미 로그인 되어 있습니다.')
          return false
        }
      }
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
      beforeEnter: (to, from) => {
        const store = useCounterStore()
        if (store.isLogin) {
          alert('이미 로그인 되어 있습니다.')
          return false
        }
      }
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView,
      props: true,
      beforeEnter: (to, from) => {
        const store = useCounterStore()
        if (!store.isLogin) {
          alert('로그인 후 이용 가능합니다.')
          return { name: 'LogInView'}
        }
      }
    },
    // articles
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
      component: ArticleCreate,
      beforeEnter: (to, from) => {
        const store = useCounterStore()
        if (!store.isLogin) {
          alert('로그인 후 이용 가능합니다.')
          return { name: 'LogInView'}
        }
      }
    },
    {
      path: '/articles/:id/edit',
      name: 'ArticleUpdate',
      component: ArticleUpdateView,
      beforeEnter: (to, from) => {
        const store = useCounterStore()
        if (!store.isLogin) {
          alert('로그인 후 이용 가능합니다.')
          return { name: 'LogInView'}
        }
      }
    },
    {
      path: '/bankmap',
      name: 'BankMap',
      component: BankMapView
    },
    {
      path: '/products', // 상품 목록 페이지 경로
      name: 'FinancialProductsView',
      component: FinancialProductsView
    },
    {
      path: '/financial-products',
      name: 'FinancialProducts',
      component: FinancialProductsView
    },
    // {
    //   path: '/product/:type/:id',
    //   name: 'ProductDetail',
    //   component: ProductDetailView,
    //   props: true
    // },
    {
      path: '/exchange-calculator',
      name: 'ExchangeCalculator',
      component: ExchangeCalculatorView
    },
    {
      path: '/calculator', // 실제 경로
      name: 'ExchangeCalculatorView', // 이 이름으로 라우팅됨
      component: ExchangeCalculatorView
    }
  ]
})


export default router