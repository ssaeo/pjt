<template>
  <div class="home">
    <h1>금융 서비스 플랫폼</h1>
    <p>금융 상품 조회, 환율 계산, 은행 지점 찾기 등 다양한 금융 서비스를 이용해보세요.</p>

    <!-- 원-달러 환율 -->
    <div class="exchange-rate">
      <h2>오늘의 환율</h2>
      <p>1 USD = {{ usdToKrwRate }} KRW</p>
      <button @click="navigateToCalculator" class="more-btn">자세히 보기</button>
    </div>

    <!-- 추천 금융 상품 -->
    <div class="recommended-products">
      <h2>추천 금융 상품</h2>
      <div class="carousel">
        <button class="carousel-btn prev" @click="prevSlide">‹</button>
        <div class="carousel-track-container">
          <ul class="carousel-track" ref="carouselTrack">
            <li class="carousel-slide" v-for="(product, index) in recommendedProducts" :key="index">
              <div class="card">
                <h3>{{ product.title }}</h3>
                <p>{{ product.description }}</p>
                <button @click="navigateToProductList" class="more-products-btn">더 많은 상품 보러가기</button>
              </div>
            </li>
          </ul>
        </div>
        <button class="carousel-btn next" @click="nextSlide">›</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import exchangeData from '@/assets/exchangeJSON.json'

// 추천 상품 데이터
const recommendedProducts = [
  { title: 'WON 플러스 적금', description: '최고 금리 3.5% 적금 상품' },
  { title: 'WON 플러스 예금', description: '안전하고 높은 금리의 예금' },
  { title: 'WON 청약 저축', description: '내 집 마련의 첫걸음, WON 청약' },
  { title: 'WON 적립식 펀드', description: '장기적인 자산 증식을 위한 펀드' }
]

// Carousel 상태 관리
const currentIndex = ref(0)
const carouselTrack = ref(null)

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
    scrollToSlide()
  }
}

const nextSlide = () => {
  if (currentIndex.value < recommendedProducts.length - 1) {
    currentIndex.value += 1
    scrollToSlide()
  }
}

const scrollToSlide = () => {
  const track = carouselTrack.value
  const slideWidth = track.querySelector('.carousel-slide').offsetWidth
  track.style.transform = `translateX(-${currentIndex.value * slideWidth}px)`
}

// 환율 데이터
const exchangeRates = exchangeData.find(rate => rate.cur_unit === 'USD')
const usdToKrwRate = parseFloat(exchangeRates.deal_bas_r) // USD to KRW 환율

// Router를 사용하여 환율 계산기 페이지로 이동
const router = useRouter()
const navigateToCalculator = () => {
  router.push({ name: 'ExchangeCalculatorView' }) // 계산기 페이지로 이동
}

// 금융 상품 리스트로 이동
const navigateToProductList = () => {
  router.push({ name: 'FinancialProducts' }) // FinancialProducts로 이동
}

</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

/* 원-달러 환율 */
.exchange-rate {
  background: #f8f9fa;
  padding: 1.5rem;
  margin: 2rem auto;
  border-radius: 8px;
  max-width: 400px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.exchange-rate h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.exchange-rate p {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.more-btn {
  background: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.more-btn:hover {
  background: #0056b3;
}

/* 추천 금융 상품 */
.recommended-products {
  margin-top: 2rem;
}

.carousel {
  position: relative;
  max-width: 600px;
  margin: 2rem auto;
  overflow: hidden;
}

.carousel-track-container {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.3s ease-in-out;
}

.carousel-slide {
  min-width: 100%;
  list-style: none;
}

.card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: #fff;
  border: none;
  font-size: 2rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.carousel-btn.prev {
  left: 10px;
}

.carousel-btn.next {
  right: 10px;
}

.carousel-btn:hover {
  background: #007bff;
  color: #fff;
}

/* 더 많은 상품 보러가기 버튼 */
.more-products-btn {
  margin-top: 1rem;
  background: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.more-products-btn:hover {
  background: #218838;
}

</style>
