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
      <p style="margin: 5px 0;">현재 위치에서 거리: {{ (selectedBranch.distance / 1000)?.toFixed(2) || '계산 중...' }}km</p>
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
export default {
  data() {
    return {
      map: null, // 카카오맵 객체
      ps: null, // 장소 검색 객체
      markers: [], // 지도에 표시된 마커들
      searchResults: [], // 검색 결과 목록
      selectedBranch: null, // 선택된 은행 지점 정보
      navigationLink: '', // 길찾기 링크
      bankSearchQuery: '', // 검색 입력 값
      defaultPosition: {
        lat: 36.1071457, // 기본 위치 (싸피 401호)
        lng: 128.4159099,
      },
    };
  },
  mounted() {
    this.loadKakaoMap();
  },
  methods: {
    // 카카오맵 로드
    loadKakaoMap() {
      if (!window.kakao || !window.kakao.maps) {
        const script = document.createElement('script');
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`;

        script.addEventListener('load', () => {
          window.kakao.maps.load(this.initMap);
        });

        script.addEventListener('error', () => {
          alert('카카오맵 스크립트 로드에 실패했습니다. API 키를 확인하세요.');
        });

        document.head.appendChild(script);
      } else {
        window.kakao.maps.load(this.initMap);
      }
    },

    // 지도 초기화
    initMap() {
      const container = document.getElementById('map');
      const options = {
        center: new window.kakao.maps.LatLng(
          this.defaultPosition.lat,
          this.defaultPosition.lng
        ),
        level: 3, // 초기 줌 레벨
      };

      this.map = new window.kakao.maps.Map(container, options);

      const zoomControl = new window.kakao.maps.ZoomControl();
      this.map.addControl(zoomControl, window.kakao.maps.ControlPosition.RIGHT);

      this.ps = new window.kakao.maps.services.Places();

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          this.handleGeolocationSuccess,
          this.handleGeolocationError
        );
      } else {
        this.searchNearbyBranches(this.defaultPosition.lat, this.defaultPosition.lng);
      }
    },

    // 현재 위치 가져오기 성공
    handleGeolocationSuccess(position) {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      this.map.setCenter(new window.kakao.maps.LatLng(lat, lng));
      this.searchNearbyBranches(lat, lng);
    },

    // 현재 위치 가져오기 실패
    handleGeolocationError() {
      alert('현재 위치를 가져올 수 없어 기본 위치로 설정합니다.');
      this.searchNearbyBranches(this.defaultPosition.lat, this.defaultPosition.lng);
    },

    // 은행 검색
    searchBank() {
      if (!this.bankSearchQuery.trim()) {
        alert('검색어를 입력해주세요.');
        return;
      }

      // 현재 지도 중심 가져오기
      const center = this.map.getCenter();

      // 현재 지도 중심 기준으로 검색
      const options = {
        location: new window.kakao.maps.LatLng(center.getLat(), center.getLng()), // 지도 중심 좌표
        radius: 5000, // 검색 반경 (5km)
      };

      this.ps.keywordSearch(this.bankSearchQuery, (data, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          this.clearMarkers();

          this.searchResults = data; // 검색 결과 저장

          data.forEach((place) => {
            this.addPlaceMarker(place);
          });

          // 첫 번째 검색 결과를 선택하여 표시
          if (data.length > 0) {
            this.selectBranch(data[0]);
            this.map.setCenter(new window.kakao.maps.LatLng(data[0].y, data[0].x));
          }
        } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
          alert('검색 결과가 없습니다.');
          this.searchResults = []; // 검색 결과 초기화
        } else {
          alert('검색 중 오류가 발생했습니다.');
        }
      }, options); // 검색 옵션 추가
    },

    // 선택된 지점 설정
    selectBranch(place) {
      this.selectedBranch = place;
      this.navigationLink = `https://map.kakao.com/link/to/${encodeURIComponent(
        place.place_name
      )},${place.y},${place.x}`;
    },

    // 마커 추가
    addPlaceMarker(place) {
      const position = new window.kakao.maps.LatLng(place.y, place.x);

      const marker = new window.kakao.maps.Marker({
        position: position,
        map: this.map,
      });

      window.kakao.maps.event.addListener(marker, 'click', () => {
        this.selectBranch(place);
      });

      this.markers.push(marker);
    },

    // 특정 장소로 지도 중심 이동
    focusOnPlace(place) {
      this.map.setCenter(new window.kakao.maps.LatLng(place.y, place.x));
      this.selectBranch(place);
    },

    // 기존 마커 삭제
    clearMarkers() {
      this.markers.forEach((marker) => marker.setMap(null));
      this.markers = [];
    },
  },
};
</script>
