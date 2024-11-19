import { createRouter, createWebHistory } from 'vue-router';

// 컴포넌트 임포트
import HomeView from '../views/HomeView.vue';
import ExchangeCalculator from '../components/ExchangeCalculator.vue';
import BankMap from '../components/BankMap.vue';
import ProductList from '../views/ProductList.vue'; // 상품 목록 컴포넌트
import ProductDetail from '../views/ProductDetail.vue'; // 상품 상세 컴포넌트

// 라우트 설정
const routes = [
  { path: '/', name: 'Home', component: HomeView }, // 홈 페이지
  { path: '/calculator', name: 'Calculator', component: ExchangeCalculator }, // 환율 계산기
  { path: '/bank-map', name: 'BankMap', component: BankMap }, // 은행 지도
  { path: '/products', name: 'ProductList', component: ProductList }, // 상품 목록
  { 
    path: '/products/:productType/:id', 
    name: 'ProductDetail', 
    component: ProductDetail, 
    props: true // URL 파라미터를 컴포넌트로 전달
  }, // 상품 상세
];

// 라우터 생성
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
