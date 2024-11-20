<template>
  <div>
    <!-- 검색 영역 -->
    <div style="margin-bottom: 10px; display: flex; gap: 10px;">
      <input
        v-model="bankSearchQuery"
        placeholder="은행 이름을 입력하세요 (예: 국민은행, 농협은행)"
        style="width: 250px; padding: 8px;"
      />
      <button @click="searchBank" style="padding: 8px 15px;">검색</button>
    </div>

    <!-- 지도 상단에 지점 정보 표시 -->
    <div v-if="selectedBranch" style="border-bottom: 1px solid #ddd; padding: 10px;">
      <h3 style="margin: 0;">{{ selectedBranch.place_name }}</h3>
      <p style="margin: 5px 0;">주소: {{ selectedBranch.address_name }}</p>
      <p style="margin: 5px 0;">전화번호: {{ selectedBranch.phone || '정보 없음' }}</p>
      <p style="margin: 5px 0;">
        현재 위치에서 거리: {{ (selectedBranch.distance / 1000)?.toFixed(2) || '계산 중...' }}km
      </p>
      <p><a :href="navigationLink" target="_blank" rel="noopener">길찾기</a></p>
    </div>

    <!-- 지도 -->
    <div id="map" style="width: 100%; height: 500px;"></div>

    <!-- 검색 결과 목록 -->
    <div v-if="searchResults.length" style="margin-top: 10px; padding: 10px; border-top: 1px solid #ddd;">
      <h4>검색 결과</h4>
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <div
          v-for="(result, index) in searchResults"
          :key="index"
          @click="focusOnPlace(result)"
          style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; background-color: #f9f9f9;"
        >
          <strong>{{ result.place_name }}</strong>
          <p style="margin: 5px 0;">주소: {{ result.address_name }}</p>
          <p style="margin: 5px 0;">전화번호: {{ result.phone || '정보 없음' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const map = ref(null)
    const ps = ref(null)
    const markers = ref([])
    const searchResults = ref([])
    const selectedBranch = ref(null)
    const navigationLink = ref('')
    const bankSearchQuery = ref('')
    const defaultPosition = {
      lat: 36.1071457, // 기본 위치 (싸피 401호)
      lng: 128.4159099,
    }

    const loadKakaoMap = () => {
      if (!window.kakao || !window.kakao.maps) {
        const script = document.createElement('script')
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`

        script.addEventListener('load', () => {
          window.kakao.maps.load(initMap)
        })

        script.addEventListener('error', () => {
          alert('카카오맵 스크립트 로드에 실패했습니다. API 키를 확인하세요.')
        })

        document.head.appendChild(script)
      } else {
        window.kakao.maps.load(initMap)
      }
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

    onMounted(() => {
      loadKakaoMap()
    })

    return {
      map,
      ps,
      markers,
      searchResults,
      selectedBranch,
      navigationLink,
      bankSearchQuery,
      loadKakaoMap,
      searchBank,
      focusOnPlace,
    }
  },
}
</script>
