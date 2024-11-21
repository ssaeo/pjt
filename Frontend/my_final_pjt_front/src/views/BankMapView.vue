<template>
  <div class="bank-map">
    <h1>은행 찾기</h1>
    
    <div class="search-filters">
      <select v-model="selectedBank">
        <option value="">모든 은행</option>
        <option v-for="bank in banks" :key="bank.code" :value="bank.code">
          {{ bank.name }}
        </option>
      </select>

      <button @click="getCurrentLocation" class="location-btn">
        내 주변 은행 찾기
      </button>
    </div>

    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useCounterStore()
const { bankBranches } = storeToRefs(store)

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const selectedBank = ref('')

const banks = [
  { code: '004', name: '국민은행' },
  { code: '011', name: '농협은행' },
  { code: '020', name: '우리은행' },
  { code: '081', name: '하나은행' },
]

const initMap = () => {
  if (!window.kakao?.maps) {
    console.log('카카오맵 API가 로드되지 않았습니다.')
    return
  }

  const options = {
    center: new kakao.maps.LatLng(35.8714354, 128.601445),  // 대구 중심
    level: 3
  }
  map.value = new kakao.maps.Map(mapContainer.value, options)
}

const updateMarkers = (branches) => {
  // 기존 마커 제거
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  console.log('업데이트할 지점들:', branches)

  branches.forEach(branch => {
    console.log('지점 좌표:', branch.latitude, branch.longitude)

    const position = new kakao.maps.LatLng(
      parseFloat(branch.latitude), 
      parseFloat(branch.longitude)
    )

    const marker = new kakao.maps.Marker({ 
      position, 
      map: map.value,
      image: new kakao.maps.MarkerImage(
        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_blue.png',
        new kakao.maps.Size(44, 49),
        { offset: new kakao.maps.Point(15, 49) }
      )
    })

    const infowindow = new kakao.maps.InfoWindow({
      content: `
        <div style="padding:10px;min-width:200px;">
          <h3 style="margin:5px 0;color:#333;">${branch.brch_name}</h3>
          <p style="margin:5px 0;font-size:13px;color:#666;">
            <strong>${banks.find(b => b.code === branch.bank_code)?.name || '은행'}</strong>
          </p>
          <p style="margin:5px 0;font-size:13px;color:#666;">${branch.addr}</p>
          ${branch.brch_telno ? 
            `<p style="margin:5px 0;font-size:13px;color:#666;">
              📞 <a href="tel:${branch.brch_telno}" style="color:#1a73e8;text-decoration:none;">
                ${branch.brch_telno}
              </a>
            </p>` : 
            ''
          }
        </div>
      `
    })

    kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.open(map.value, marker)
    })

    markers.value.push(marker)
  })

  if (markers.value.length > 0) {
    const bounds = new kakao.maps.LatLngBounds()
    markers.value.forEach(marker => bounds.extend(marker.getPosition()))
    map.value.setBounds(bounds)
  }
}

const getCurrentLocation = () => {
  if (!store.token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  if (!navigator.geolocation) {
    alert('위치 정보를 사용할 수 없습니다.')
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      console.log('현재 위치:', latitude, longitude)

      const params = {
        lat: latitude,
        lng: longitude,
        radius: 1000,
        bank_code: selectedBank.value || undefined
      }

      console.log('요청 파라미터:', params)

      store.searchNearbyBranches(params)
        .then((branches) => {
          console.log('검색 결과:', branches)
          if (branches && branches.length > 0) {
            const currentPos = new kakao.maps.LatLng(latitude, longitude)
            map.value.setCenter(currentPos)
            
            // 현재 위치 마커 추가
            const currentMarker = new kakao.maps.Marker({
              position: currentPos,
              map: map.value,
              image: new kakao.maps.MarkerImage(
                'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
                new kakao.maps.Size(64, 69),
                { offset: new kakao.maps.Point(27, 69) }
              )
            })

            // 은행 지점 마커 업데이트
            updateMarkers(branches)
          } else {
            alert('주변에 은행 지점이 없습니다.')
          }
        })
        .catch((err) => {
          console.error('API 호출 에러:', err)
          if (err.response?.status === 401) {
            alert('로그인이 필요한 서비스입니다.')
            router.push('/login')
          } else {
            console.error('은행 검색 실패:', err)
            alert('은행 검색 중 오류가 발생했습니다.')
          }
        })
    },
    (err) => {
      console.error('위치 정보 조회 실패:', err)
      alert('위치 정보를 가져올 수 없습니다.')
    }
  )
}

// bankBranches 변경 감지
watch(bankBranches, (newBranches) => {
  console.log('bankBranches 변경됨:', newBranches)
  if (newBranches && newBranches.length > 0) {
    updateMarkers(newBranches)
  }
}, { deep: true })

// 컴포넌트 마운트 시 지도 초기화
onMounted(() => {
  console.log('컴포넌트 마운트됨')
  initMap()
})
</script>

<style scoped>
.bank-map {
  padding: 20px;
}

.search-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.location-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.location-btn:hover {
  background-color: #45a049;
}

.map-container {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>