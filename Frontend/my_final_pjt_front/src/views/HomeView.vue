<template>
  <div class="home">
    <!-- 상단 텍스트와 이미지 캐러셀 -->
    <div class="carousel-wrapper">
      <div class="carousel">
        <button class="carousel-btn prev" @click="prevCarouselImage">‹</button>
        <div class="carousel-track-container">
          <ul class="carousel-track" ref="carouselTrack">
            <li
              class="carousel-slide"
              v-for="(image, index) in carouselImages"
              :key="index"
            >
              <img
                :src="image.src"
                :alt="image.alt"
                class="carousel-image"
                @click="navigateToPage(image.link)"
              />
            </li>
          </ul>
        </div>
        <button class="carousel-btn next" @click="nextCarouselImage">›</button>
      </div>
      
      <div class="carousel-text">
        <h1>금융 서비스 플랫폼</h1>
        <p>금융 상품 조회, 환율 계산, 은행 지점 찾기 등 다양한 금융 서비스를 이용해보세요.</p>
      </div>
    </div>

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
  </div>
</template>


<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Chart from "chart.js/auto";
import exchangeData from "@/assets/exchangeData.json"; // 환율 JSON 데이터
import Chatbot from "@/components/Chatbot.vue"

// Chatbot 상태 관리
const showChatbot = ref(false);
const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value;
}

// 캐러셀 이미지 데이터
const carouselImages = ref([
  { src: new URL("@/assets/저축2.png", import.meta.url).href},
  { src: new URL("@/assets/환율2.png", import.meta.url).href, alt: "환율 계산기", link: "/exchange-calculator" },
  { src: new URL("@/assets/저축3.png", import.meta.url).href, alt: "추천 금융 상품", link: "/financial-products" },
  { src: new URL("@/assets/길1.png", import.meta.url).href, alt: "은행 찾기", link: "/bankmap" },
])


const currentImageIndex = ref(0)
const carouselTrack = ref(null)

// 이전 슬라이드로 이동
const prevCarouselImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value -= 1
    updateCarouselPosition()
  }
}

// 다음 슬라이드로 이동
const nextCarouselImage = () => {
  if (currentImageIndex.value < carouselImages.value.length - 1) {
    currentImageIndex.value += 1
    updateCarouselPosition()
  }
}

// 캐러셀 이동 업데이트
const updateCarouselPosition = () => {
  const track = carouselTrack.value
  const slideWidth = track.querySelector(".carousel-slide").offsetWidth
  track.style.transform = `translateX(-${currentImageIndex.value * slideWidth}px)`
}

// 페이지 이동
const navigateToPage = (link) => {
  router.push(link)
}

onMounted(() => {
  updateCarouselPosition() // 초기 위치 설정
})

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
  description: "최대 3.5% 금리를 제공하는 적금 상품입니다. 매달 일정 금액을 저축하여 안정적인 자산 증식을 도와드립니다. 단기 목표는 물론 장기적인 재정 관리를 원하는 분들에게 적합한 상품입니다. 다양한 금리 옵션과 유연한 가입 조건으로, 개인의 재정 상황에 맞는 최적의 적금 플랜을 제공하며, 신뢰와 안정성을 동시에 느낄 수 있습니다.",
},
{
  title: "WON 플러스 예금",
  description: "안정성과 높은 금리를 동시에 누릴 수 있는 예금 상품입니다. 1년 만기 기준으로 설정된 금리 조건은 최적의 재테크 환경을 제공합니다. 장기적으로 안전한 자산 관리를 추구하는 고객들에게 추천되며, 원금 보장은 물론 만기 시 높은 이자 수익을 기대할 수 있습니다. 예금 기간 동안 불필요한 리스크 없이 계획적인 재정 관리를 가능하게 해줍니다.",
},
{
  title: "WON 청약 저축",
  description: "내 집 마련의 첫걸음을 시작하는 분들을 위한 WON 청약 저축 상품입니다. 매월 소액부터 저축이 가능하며, 주택 청약에 필요한 기본 요건을 충족시킬 수 있습니다. 높은 경쟁률의 청약 조건에서도 우위를 점할 수 있도록 최적화된 상품으로, 장기적인 주택 구매 계획에 안정성과 신뢰를 더합니다. 다양한 주택 유형에 맞춘 유연한 플랜과 맞춤형 저축 전략을 제공합니다.",
},
{
  title: "WON 적립식 펀드",
  description: "장기적인 자산 증식에 최적화된 펀드 상품입니다. 매월 일정 금액을 적립하여 부담 없이 참여할 수 있으며 전문가의 조언과 맞춤형 투자 전략을 지원합니다. 글로벌 및 국내 시장의 트렌드를 반영한 투자 옵션으로 수익성을 극대화할 수 있는 상품입니다. 초보 투자자도 쉽게 이해하고 시작할 수 있도록 체계적인 교육과 지원 서비스를 제공하며, 장기적인 재정 목표를 달성하는 데 도움을 줍니다.",
},

]

const currentExchangeIndex = ref(0);
const exchangeCarouselTrack = ref(null);

const prevExchangeSlide = () => {
  console.log("이전 버튼 클릭");
  if (currentExchangeIndex.value > 0) {
    currentExchangeIndex.value -= 1;
    scrollToExchangeSlide();
  }
};
const nextExchangeSlide = () => {
  console.log("다음 버튼 클릭");
  if (currentExchangeIndex.value < 1) {
    currentExchangeIndex.value += 1;
    scrollToExchangeSlide();
  }
}

const scrollToExchangeSlide = () => {
  const track = exchangeCarouselTrack.value;
  const slideWidth = track.querySelector(".carousel-slide").offsetWidth;
  track.style.transform = `translateX(-${currentExchangeIndex.value * slideWidth}px)`;
}

// Router를 사용하여 페이지 이동
const router = useRouter()
const navigateToCalculator = () => router.push({ name: "ExchangeCalculatorView" })
const navigateToProductList = () => router.push({ name: "FinancialProducts" })

// 캐러셀 상태 관리: 상품 추천
const currentProductIndex = ref(0);
const productCarouselTrack = ref(null);

const prevProductSlide = () => {
  if (currentProductIndex.value > 0) {
    currentProductIndex.value -= 1;
    scrollToProductSlide();
  }
};
const nextProductSlide = () => {
  if (currentProductIndex.value < recommendedProducts.length - 1) {
    currentProductIndex.value += 1;
    scrollToProductSlide();
  }
};
const scrollToProductSlide = () => {
  const track = productCarouselTrack.value;
  const slideWidth = track.querySelector(".carousel-slide").offsetWidth;
  track.style.transform = `translateX(-${currentProductIndex.value * slideWidth}px)`;
};

onMounted(() => {
  const MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_KEY; // 환경 변수에서 API Key 가져오기
  if (!window.kakao || !window.kakao.maps) {
    const script = document.createElement("script");
    script.onload = () => kakao.maps.load(() => initMap()); // 지도 초기화
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${MAP_API_KEY}&libraries=services`;
    document.head.appendChild(script);
  } else {
    kakao.maps.load(() => initMap()); // 이미 로드된 경우 바로 지도 초기화
  }
});

const searchNearbyBanks = (map) => {
  const placesService = new kakao.maps.services.Places();

  // 은행 카테고리 검색
  placesService.categorySearch(
    "BK9", // 은행 카테고리 코드
    (data, status) => {
      if (status === kakao.maps.services.Status.OK) {
        data.forEach((place) => {
          // 마커 생성
          const marker = new kakao.maps.Marker({
            position: new kakao.maps.LatLng(place.y, place.x),
            map: map,
          });

          // 인포윈도우 생성
          const infowindow = new kakao.maps.InfoWindow({
            content: `<div style="padding:5px;">${place.place_name}</div>`,
          });

          // 마커에 마우스 오버 이벤트 추가 (지도 중심 이동 비활성화)
          kakao.maps.event.addListener(marker, "mouseover", () => {
            infowindow.open(map, marker); // 마우스 오버 시 인포윈도우 열기
          });
          kakao.maps.event.addListener(marker, "mouseout", () => {
            infowindow.close(); // 마우스 아웃 시 인포윈도우 닫기
          });
          kakao.maps.event.addListener(marker, "click", () => {
            // 클릭 시 지도 중심 이동하지 않음, 단순히 콘솔 출력
            console.log(`클릭한 장소: ${place.place_name}`);
          });
        });
      } else {
        console.warn("주변 은행 정보를 가져오지 못했습니다.");
      }
    },
    { location: map.getCenter() } // 지도 중심 기준으로 검색
  );
};

const initMap = () => {
  const container = document.getElementById("map"); // 지도를 표시할 div
  const options = {
    center: new kakao.maps.LatLng(36.10714520, 128.4159571), // 기본 중심 좌표 (서울)
    level: 3, // 확대 레벨
  };
  const map = new kakao.maps.Map(container, options); // 지도 생성

  // 현재 위치로 지도 중심 이동
  moveToCurrentLocation(map);

  searchNearbyBanks(map);
};


const moveToCurrentLocation = (map) => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        const moveLatLon = new kakao.maps.LatLng(lat, lng);

        map.setCenter(moveLatLon); // 현재 위치로 지도 중심 이동
        console.log("현재 위치로 지도 이동:", lat, lng);
      },
      (error) => {
        console.warn("위치 정보를 가져올 수 없습니다. 기본 위치로 이동합니다.", error);
        // 기본 위치로 지도 이동 (예: 서울)
        const defaultLatLon = new kakao.maps.LatLng(36.10714520642778, 128.4159571529663);
        map.setCenter(defaultLatLon);
      }
    );
  } else {
    console.warn("Geolocation을 지원하지 않는 브라우저입니다.");
  }
};



// "환율 그래프" 렌더링
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
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          enabled: true,
          mode: "index",
          intersect: false,
          callbacks: {
            title: (tooltipItems) => `날짜: ${tooltipItems[0].label}`,
            label: (tooltipItem) =>
`환율: ${tooltipItem.raw} KRW`,
          },
          backgroundColor: "#333",
          titleColor: "#fff",
          bodyColor: "#fff",
          borderColor: "red",
          borderWidth: 2,
        },
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#666",
            autoSkip: true,
            maxTicksLimit: 10,
          },
        },
        y: {
          ticks: {
            color: "#666",
            stepSize: 100,
            callback: (value) => `${value} KRW`,
          },
          min: 1200,
          max: 1500,
        },
      },
    },
  });
});
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin: 0;
  padding: 0;
}

.carousel-wrapper {
  position: relative;
  width: 100vw; /* 전체 화면 가로 */
  height: 70vh; /* 화면 높이의 70% */
  overflow: hidden;
}

/* 카드 컨테이너 */
.card-container {
  display: flex;
  flex-wrap: nowrap; /* 가로로 배치 */
  justify-content: space-between;
  align-items: stretch;
  overflow-y: auto;
  gap: 10px; /* 카드 간격 */
  margin-top: 1rem; /* 캐러셀과 카드 컨테이너 간격 조정 */
  padding: 10px;
}

.card h2 {
  letter-spacing: 1.5px; /* 글자 간격 */
  margin-bottom: 10px; /* 제목과 내용 사이 간격 */
}

.card p {
  line-height: 1.6; /* 줄 간격 */
  letter-spacing: 0.5px; /* 글자 간격 */
  margin-top: 8px; /* 상단 간격 */
  margin-bottom: 12px; /* 하단 간격 */
}

/* 기본적으로 숨김 */
.card-container .carousel-btn {
  display: none; /* 기본적으로 숨김 */
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
  align-items: center;
  justify-content: center;
}

/* 마우스가 카드 컨테이너 위로 올라오면 버튼 표시 */
.card-container:hover .carousel-btn {
  display: flex;
}

/* 좌우 버튼 위치 */
.card-container .carousel-btn.prev {
  left: 10px;
}

.card-container .carousel-btn.next {
  right: 10px;
}

/* 버튼 hover 시 스타일 */
.card-container .carousel-btn:hover {
  background: #007bff;
  color: #fff;
}

.card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  flex: 1 1 auto; /* 카드 크기를 비율에 맞춰 조정 */
  width: 450px;
  height: 450px;
  text-align: center;
  margin: 10px;
  transition: transform 0.3s ease-in-out, width 0.3s ease-in-out, height 0.3s ease-in-out;
}

.card:hover {
  transform: scale(1.05); /* 호버 시 카드 확대 */
}

/* 반응형 카드 높이 줄이기 */
@media (max-height: 800px) {
  .card {
    height: 250px; /* 화면 높이가 줄어들면 카드 높이 조정 */
  }
}

@media (max-height: 600px) {
  .card {
    height: 200px; /* 더 작아지면 카드 높이 더 줄임 */
  }
}

@media (max-width: 768px) {
  .card-container {
    justify-content: start; /* 작은 화면에서 카드 왼쪽 정렬 */
  }

  .card {
    width: 250px; /* 작은 화면에서 기본 카드 너비 줄임 */
  }
}

.rate-list p {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%; /* 가로를 완전히 채우기 */
}

.carousel {
  position: relative;
  margin: 20px auto;
  overflow: hidden;
  width: 100%;
  height: 600px;
  border-radius: 10px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.carousel-text {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: white;
  z-index: 10;
}

.carousel-text h1 {
  font-size: 2.5rem;
  margin: 0;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.carousel-text p {
  font-size: 1.2rem;
  margin-top: 0.5rem;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.carousel-container {
  margin-top: 1rem;
  position: relative;
  overflow: hidden;
}

.carousel-track-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.3s ease-in-out;
}

.carousel-slide {
  min-width: 100%;
  height: 100%;
  list-style: none;
}

.carousel-content {
  padding: 1rem;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-btn.prev {
  left: 0px;
}

.carousel-btn.next {
  right: 0px;
}

.carousel-btn:hover {
  background: #007bff;
  color: #fff;
}

.more-btn,
.more-products-btn {
  background: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.more-btn:hover,
.more-products-btn:hover {
  background: #0056b3;
}

.chat-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* 아이콘이 항상 최상단에 표시되도록 설정 */
}

.chat-icon:hover {
  background-color: #0056b3;
}
</style>

