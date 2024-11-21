<template>
  <div class="bankmap-container">
    <!-- 검색 영역 -->
    <div class="search-area">
      <input
        v-model="bankSearchQuery"
        placeholder="은행 이름을 입력하세요 (예: 국민은행, 농협은행)"
        class="search-input"
      />
      <button @click="searchBank" class="search-btn">검색</button>
    </div>

    <!-- 지점 정보 표시 -->
    <div v-if="selectedBranch" class="branch-info">
      <h3>{{ selectedBranch.place_name }}</h3>
      <p>주소: {{ selectedBranch.address_name }}</p>
      <p>전화번호: {{ selectedBranch.phone || '정보 없음' }}</p>
      <p>
        현재 위치에서 거리: {{ (selectedBranch.distance / 1000)?.toFixed(2) || '계산 중...' }}km
      </p>
      <p><a :href="navigationLink" target="_blank" rel="noopener">길찾기</a></p>
    </div>

    <!-- 지도 -->
    <div id="map" class="map-container"></div>

    <!-- 검색 결과 목록 -->
    <div v-if="searchResults.length" class="search-results">
      <h4>검색 결과</h4>
      <div class="results-list">
        <div
          v-for="(result, index) in searchResults"
          :key="index"
          @click="focusOnPlace(result)"
          class="result-item"
        >
          <strong>{{ result.place_name }}</strong>
          <p>주소: {{ result.address_name }}</p>
          <p>전화번호: {{ result.phone || '정보 없음' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const map = ref(null)
const ps = ref(null)
const markers = ref([])
const searchResults = ref([])
const selectedBranch = ref(null)
const navigationLink = ref('')
const bankSearchQuery = ref('')
const searchRadius = ref(1000)

const defaultPosition = {
  lat: 36.1071457, // 기본 위치 (싸피 401호)
  lng: 128.4159099,
}

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new window.kakao.maps.LatLng(defaultPosition.lat, defaultPosition.lng),
    level: 3,
  }

  map.value = new window.kakao.maps.Map(container, options)
  const zoomControl = new window.kakao.maps.ZoomControl()
  map.value.addControl(zoomControl, window.kakao.maps.ControlPosition.RIGHT)

  ps.value = new window.kakao.maps.services.Places()

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(handleGeolocationSuccess, handleGeolocationError)
  } else {
    searchNearbyBranches(defaultPosition.lat, defaultPosition.lng)
  }
}

const handleGeolocationSuccess = (position) => {
  const lat = position.coords.latitude
  const lng = position.coords.longitude
  map.value.setCenter(new window.kakao.maps.LatLng(lat, lng))
  searchNearbyBranches(lat, lng)
}

const handleGeolocationError = () => {
  alert('현재 위치를 가져올 수 없어 기본 위치로 설정합니다.')
  searchNearbyBranches(defaultPosition.lat, defaultPosition.lng)
}

const searchBank = () => {
  if (!bankSearchQuery.value.trim()) {
    alert('검색어를 입력해주세요.')
    return
  }

  const center = map.value.getCenter()
  const options = {
    location: new window.kakao.maps.LatLng(center.getLat(), center.getLng()),
    radius: 5000,
  }

  ps.value.keywordSearch(bankSearchQuery.value, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      clearMarkers()
      searchResults.value = data

      data.forEach((place) => {
        addPlaceMarker(place)
      })

      if (data.length > 0) {
        selectBranch(data[0])
        map.value.setCenter(new window.kakao.maps.LatLng(data[0].y, data[0].x))
      }
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 없습니다.')
      searchResults.value = []
    } else {
      alert('검색 중 오류가 발생했습니다.')
    }
  }, options)
}

const selectBranch = (place) => {
  selectedBranch.value = place
  navigationLink.value = `https://map.kakao.com/link/to/${encodeURIComponent(
    place.place_name
  )},${place.y},${place.x}`
}

const addPlaceMarker = (place) => {
  const position = new window.kakao.maps.LatLng(place.y, place.x)
  const marker = new window.kakao.maps.Marker({
    position: position,
    map: map.value,
  })

  window.kakao.maps.event.addListener(marker, 'click', () => {
    selectBranch(place)
  })

  markers.value.push(marker)
}

const focusOnPlace = (place) => {
  map.value.setCenter(new window.kakao.maps.LatLng(place.y, place.x))
  selectBranch(place)
}

const clearMarkers = () => {
  markers.value.forEach((marker) => marker.setMap(null))
  markers.value = []
}

const searchNearbyBranches = (lat, lng) => {
  store.searchNearbyBranches(lat, lng, searchRadius.value)
    .then((branches) => {
      clearMarkers()
      branches.forEach(branch => {
        const position = new window.kakao.maps.LatLng(branch.latitude, branch.longitude)
        const marker = new window.kakao.maps.Marker({
          position,
          map: map.value
        })
        markers.value.push(marker)
      })
    })
}

onMounted(() => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`

  script.onload = () => {
    window.kakao.maps.load(initMap)
  }

  script.onerror = () => {
    alert('카카오맵 스크립트 로드에 실패했습니다. API 키를 확인하세요.')
  }

  document.head.appendChild(script)
})
</script>

<style scoped>
.bankmap-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-area {
  margin-bottom: 10px;
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #45a049;
}

.branch-info {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
}

.branch-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.branch-info p {
  margin: 5px 0;
  color: #666;
}

.branch-info a {
  color: #4CAF50;
  text-decoration: none;
}

.branch-info a:hover {
  text-decoration: underline;
}

.map-container {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}
.search-results {
margin-top: 20px;
padding: 15px;
border-top: 1px solid #ddd;
}
.search-results h4 {
margin: 0 0 15px 0;
color: #333;
}
.results-list {
display: flex;
flex-direction: column;
gap: 10px;
}
.result-item {
padding: 15px;
border: 1px solid #ddd;
border-radius: 4px;
cursor: pointer;
background-color: #f9f9f9;
transition: background-color 0.3s;
}
.result-item:hover {
background-color: #f0f0f0;
}
.result-item strong {
display: block;
margin-bottom: 8px;
color: #333;
}
.result-item p {
margin: 5px 0;
color: #666;
font-size: 14px;
}
.radius-input {
padding: 8px;
width: 150px;
border: 1px solid #ddd;
border-radius: 4px;
margin-right: 10px;
}
.selected {
background-color: #e3f2fd;
border-color: #2196F3;
}
@media (max-width: 768px) {
.bankmap-container {
padding: 10px;
}
.search-area {
flex-direction: column;
}
.map-container {
height: 400px;
}
.search-input {
width: 100%;
}
}
</style>