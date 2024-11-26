<template>
  <v-app>
    <v-main class="no-margin-padding">
      <!-- 상단 텍스트와 이미지 캐러셀 -->
      <v-container fluid class="no-margin-padding">
        <v-carousel
          height="600"
          show-arrows="hover"
          cycle
          hide-delimiter-background
        >
          <v-carousel-item
            v-for="(image, index) in carouselImages"
            :key="index"
          >
            <v-img
              :src="image.src"
              :alt="image.alt"
              class="carousel-image"
              @click="navigateToPage(image.link)"
              cover
            />
          </v-carousel-item>
        </v-carousel>
      </v-container>

      <button class="chat-icon" @click="toggleChatbot">💬</button>
      <Chatbot v-if="showChatbot" @closeChatbot="toggleChatbot" />

      <!-- 카드 컨테이너 -->
      <div class="card-container">
        <!-- 첫 번째 카드: 환율 계산기 및 그래프 -->
        <div class="card">
          <h2>환율 정보</h2>
          <div class="carousel-container">
            <button class="carousel-btn prev" @click="prevExchangeSlide">‹</button>
            <div class="carousel-track-container">
              <ul class="carousel-track" ref="exchangeCarouselTrack">
                <li class="carousel-slide">
                  <div class="carousel-content">
                    <h3>현재 주요 환율</h3>
                    <div class="rate-list">
                      <p><strong>1 USD</strong>: {{ usdToKrwRate }} KRW</p>
                      <p><strong>1 EUR</strong>: 1467.65 KRW</p>
                      <p><strong>1 JPY</strong>: 9.11 KRW</p>
                      <p><strong>1 CNY</strong>: 193.3 KRW</p>
                    </div>
                    <button @click="navigateToCalculator" class="more-btn">환율 계산기 열기</button>
                  </div>
                </li>
                <li class="carousel-slide">
                  <div class="carousel-content">
                    <h3>최근 1년간 원-달러 환율</h3>
                    <canvas id="exchangeRateChart"></canvas>
                  </div>
                </li>
              </ul>
            </div>
            <button class="carousel-btn next" @click="nextExchangeSlide">›</button>
          </div>
        </div>

        <!-- 두 번째 카드: 추천 금융 상품 -->
        <div class="card">
          <h2>추천 금융 상품</h2>
          <div class="carousel-container">
            <button class="carousel-btn prev" @click="prevProductSlide">‹</button>
            <div class="carousel-track-container">
              <ul class="carousel-track" ref="productCarouselTrack">
                <li
                  class="carousel-slide"
                  v-for="(product, index) in recommendedProducts"
                  :key="index"
                >
                  <div class="carousel-content">
                    <h3>{{ product.title }}</h3>
                    <p>{{ product.description }}</p>
                    <button @click="navigateToProductList" class="more-products-btn">자세히 보기</button>
                  </div>
                </li>
              </ul>
            </div>
            <button class="carousel-btn next" @click="nextProductSlide">›</button>
          </div>
        </div>

        <!-- 세 번째 카드: 현재 위치 기반 카카오맵 -->
        <div class="card">
          <h2>내 주변 은행 찾기</h2>
          <div id="map" style="width: 100%; height: 400px; margin-top: 1rem; border-radius: 10px;"></div>
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Chart from "chart.js/auto";
import exchangeData from "@/assets/exchangeData.json"; // 환율 JSON 데이터
import Chatbot from "@/components/Chatbot.vue";

// Chatbot 상태 관리
const showChatbot = ref(false);
const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value;
};

// 캐러셀 이미지 데이터
const carouselImages = ref([
  { src: new URL("@/assets/슬라이드(커뮤니티).png", import.meta.url).href, alt: "환율 계산기", link: "/articles" },
  { src: new URL("@/assets/슬라이드(환율계산기).png", import.meta.url).href, alt: "환율 계산기", link: "/exchange-calculator" },
  { src: new URL("@/assets/슬라이드(예적금).png", import.meta.url).href, alt: "추천 금융 상품", link: "/financial-products" },
  { src: new URL("@/assets/슬라이드(은행찾기).png", import.meta.url).href, alt: "은행 찾기", link: "/bankmap" },
]);

// 페이지 이동
const router = useRouter();
const navigateToPage = (link) => {
  router.push(link);
};

// 환율 데이터 로드
const exchangeRates = exchangeData
  .map((rate) => ({
    date: rate.date,
    value: parseFloat(rate.rate),
  }))
  .filter((rate) => !isNaN(rate.value) && rate.value >= 900 && rate.value <= 1500);

// 오늘의 환율 값
const usdToKrwRate =
  exchangeRates.length > 0 ? exchangeRates.at(-1).value.toFixed(2) : "N/A";

// 추천 금융 상품 데이터
const recommendedProducts = [
  {
    title: "WON 플러스 적금",
    description: "최대 3.5% 금리를 제공하는 적금 상품입니다. 매달 일정 금액을 저축하여 안정적인 자산 증식을 도와드립니다.",
  },
  {
    title: "WON 플러스 예금",
    description: "안정성과 높은 금리를 동시에 누릴 수 있는 예금 상품입니다. 1년 만기 기준으로 설정된 금리 조건은 최적의 재테크 환경을 제공합니다.",
  },
  {
    title: "WON 청약 저축",
    description: "내 집 마련의 첫걸음을 시작하는 분들을 위한 청약 상품입니다.",
  },
  {
    title: "WON 적립식 펀드",
    description: "장기적인 자산 증식에 최적화된 펀드 상품입니다.",
  },
];

// 캐러셀 상태 관리
const currentExchangeIndex = ref(0);
const exchangeCarouselTrack = ref(null);
const prevExchangeSlide = () => {
  currentExchangeIndex.value = (currentExchangeIndex.value - 1 + 2) % 2;
  scrollToExchangeSlide();
};
const nextExchangeSlide = () => {
  currentExchangeIndex.value = (currentExchangeIndex.value + 1) % 2;
  scrollToExchangeSlide();
};
const scrollToExchangeSlide = () => {
  const track = exchangeCarouselTrack.value;
  const slideWidth = track.querySelector(".carousel-slide").offsetWidth;
  track.style.transform = `translateX(-${currentExchangeIndex.value * slideWidth}px)`;
};

// 상품 캐러셀 상태 관리
const currentProductIndex = ref(0);
const productCarouselTrack = ref(null);
const prevProductSlide = () => {
  currentProductIndex.value = (currentProductIndex.value - 1 + recommendedProducts.length) % recommendedProducts.length;
  scrollToProductSlide();
};
const nextProductSlide = () => {
  currentProductIndex.value = (currentProductIndex.value + 1) % recommendedProducts.length;
  scrollToProductSlide();
};
const scrollToProductSlide = () => {
  const track = productCarouselTrack.value;
  const slideWidth = track.querySelector(".carousel-slide").offsetWidth;
  track.style.transform = `translateX(-${currentProductIndex.value * slideWidth}px)`;
};

// 카카오맵 초기화
onMounted(() => {
  const MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_KEY;
  if (!window.kakao || !window.kakao.maps) {
    const script = document.createElement("script");
    script.onload = () => kakao.maps.load(() => initMap());
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${MAP_API_KEY}&libraries=services`;
    document.head.appendChild(script);
  } else {
    kakao.maps.load(() => initMap());
  }
});

const initMap = () => {
  const container = document.getElementById("map");
  const options = {
    center: new kakao.maps.LatLng(36.10714520, 128.4159571),
    level: 3,
  };
  const map = new kakao.maps.Map(container, options);
};

// 환율 그래프 생성
onMounted(() => {
  const ctx = document.getElementById("exchangeRateChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: exchangeRates.map((item) => item.date),
      datasets: [
        {
          label: "원/달러 환율",
          data: exchangeRates.map((item) => item.value),
          borderColor: "red",
          borderWidth: 2,
          fill: false,
        },
      ],
    },
  });
});
</script>

<style scoped>
.v-main.no-margin-padding,
.v-container.no-margin-padding {
  margin: 0;
  padding: 0;
}

.carousel-image {
  width: 100vw;
  height: 600px;
  object-fit: cover;
  object-position: top; /* 상단이 잘리지 않도록 설정 */
}

.card-container {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;
}

.card {
  flex: 1;
  background: #ffffff; /* 흰색 배경 */
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 올라오는 효과 */
}

.card h2 {
  color: #26A69A; /* h2 태그의 텍스트 색상 */
  font-size: 1.5rem;
  margin-bottom: 15px;
  font-weight: bold;
}

.card p {
  color: #555;
  line-height: 1.6;
  margin-top: 8px;
  margin-bottom: 12px;
}

.chat-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #26A69A;
  color: white;
  border-radius: 50%;
  width: 60px;
  height: 60px;
}
</style>