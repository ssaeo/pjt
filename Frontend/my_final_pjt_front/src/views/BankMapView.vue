<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="12">
        <v-card class="pa-5">
          <v-card-title>
            <h1>주변 은행 검색</h1>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-row class="d-flex align-center my-5">
              <v-col cols="12" md="3">
                <v-select
                  v-model="selectedCity"
                  :items="cities"
                  label="광역시 / 도"
                  dense
                  outlined
                  variant="outlined"
                  color="teal-lighten-1"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="selectedCityDetail"
                  :items="citiesDetail"
                  label="시/군/구"
                  dense
                  outlined
                  variant="outlined"
                  color="teal-lighten-1"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="selectedBank"
                  :items="banks"
                  label="은행"
                  dense
                  outlined
                  variant="outlined"
                  color="teal-lighten-1"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3" class="d-flex align-start"> <!-- align-start로 변경 -->
        <v-btn 
          @click="clickSearch"
          variant="flat"
          color="#26A69A"
          size="x-large"
          class="pr-7 ml-2 mb-6"
          block
        >
        <v-icon class="me-1 mt-1">mdi-magnify</v-icon>
          찾기
        </v-btn>
      </v-col>
            </v-row>
            <v-card class="map-container elevation-7 mb-15">
              <v-btn
                @click="clickCurrentSearch"
                class="current-search-btn"
                color="#26A69A"
                elevation="8"
                large
              >
                현 지도에서 해당 은행 검색
              </v-btn>
              <div id="map" :style="`width: 100%; height: 600px;`"></div>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// 지역 데이터
const regions = {
  강원도: ["강릉시","동해시","삼척시","속초시","원주시","춘천시","태백시","고성군","양구군","양양군","영월군","인제군","정선군","철원군","평창군","홍천군","화천군","횡성군"],
  경기도: ["고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"],
  경상남도: ["거제시", "김해시", "마산시", "밀양시", "사천시", "양산시", "진주시", "진해시", "창원시", "통영시", "거창군", "고성군", "남해군", "산청군", "의령군", "창녕군", "하동군", "함안군", "함양군", "합천군"],
  경상북도: ["경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"],
  광주광역시: ["광산구", "남구", "동구", "북구", "서구"],
  대구광역시: ["남구", "달서구", "동구", "북구", "서구", "수성구", "중구", "달성군"],
  대전광역시: ["대덕구", "동구", "서구", "유성구", "중구"],
  부산광역시: ["강서구","금정구","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구","기장군"],
  서울특별시: ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"],
  울산광역시: ["남구","동구","북구","중구","울주군"],
  인천광역시: ["계양구","남구","남동구","동구","부평구","서구","연수구","중구","강화군","옹진군"],
  전라남도: ["광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"],
  전라북도: ["군산시", "김제시", "남원시", "익산시", "전주시", "정읍시", "고창군", "무주군", "부안군", "순창군", "완주군", "임실군", "장수군", "진안군"],
  제주특별자치도: ["서귀포시","제주시","남제주군","북제주군"],
  충청북도: ["제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"],
  충청남도: ["계룡시", "공주시", "논산시", "당진시", "보령시", "서산시", "아산시", "천안시", "금산군", "부여군", "서천군", "연기군", "예산군", "청양군", "태안군", "홍성군"]
}

const selectedBank = ref('전체보기')
const banks = ref(['전체보기', '우리은행', 'SC제일은행', '대구은행', '부산은행', '광주은행', '제주은행', '전북은행', '경남은행', 'IBK기업은행', 'KDB산업은행', '국민은행', '신한은행', '농협은행', '하나은행', '수협은행'])

const selectedCity = ref()
const cities = ref(Object.keys(regions))
const selectedCityDetail = ref()
const citiesDetail = ref()

const keyword = ref('은행')

watch(selectedCity, () => {
  selectedCityDetail.value = null
  citiesDetail.value = regions[selectedCity.value] || []
})

watch([selectedCity, selectedCityDetail, selectedBank], () => {
  keyword.value = `${selectedCity.value || ''}${selectedCityDetail.value || ''}${selectedBank.value === '전체보기' ? '은행' : selectedBank.value}`
})

const MAP_API_KEY = import.meta.env.VITE_KAKAO_MAP_KEY

const center = ref([36.1071457, 128.4159099]) 
const level = ref(3)
const mapRef = ref()
const markers = ref([]) // 마커를 저장할 배열
const infowindow = ref(null) // 인포윈도우를 저장할 변수

onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap('init')
  } else {
    const script = document.createElement('script')

    script.onload = () => kakao.maps.load(() => initMap('init'))
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${MAP_API_KEY}&libraries=services`
    document.head.appendChild(script)
  }
})

const initMap = (state='current') => {
  infowindow.value = new kakao.maps.InfoWindow({zIndex:1})

  const mapContainer = document.getElementById('map')
  const mapOption = {
    center: new kakao.maps.LatLng(center.value[0], center.value[1]),
    level: level.value
  }

  if (state === 'init') {
    var map = new kakao.maps.Map(mapContainer, mapOption)
    map.setDraggable(true)
    mapRef.value = map

    // 지도 클릭 시 인포윈도우 닫기
    kakao.maps.event.addListener(map, 'click', function() {
      if (infowindow.value) {
        infowindow.value.close()
      }
    })
  } else {
    var map = mapRef.value
  }

  kakao.maps.event.addListener(map, 'center_changed', function() {
    const levelMap = map.getLevel()
    level.value = levelMap

    const latlng = map.getCenter()
    center.value = [latlng.getLat(), latlng.getLng()]
  })

  const ps = new kakao.maps.services.Places(map)

  const searchCallback = (data, status, pagination) => {
    if (status === kakao.maps.services.Status.OK) {
      clearMarkers()
      const bounds = new kakao.maps.LatLngBounds()

      for (var i=0; i<data.length; i++) {
        displayMarker(data[i])
        bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x))
      }

      map.setBounds(bounds)
    }
  }

  if (state !== 'search') {
    if (selectedBank.value === '전체보기' || selectedBank.value === '은행') {
      ps.categorySearch('BK9', searchCallback, {useMapBounds:true})
    } else {
      ps.keywordSearch(selectedBank.value, searchCallback, {useMapBounds:true})
    }
  } else {
    ps.keywordSearch(keyword.value, searchCallback)
  }

  function displayMarker(place) {
    const marker = new kakao.maps.Marker({
      map: map,
      position: new kakao.maps.LatLng(place.y, place.x)
    })
    markers.value.push(marker)

    kakao.maps.event.addListener(marker, 'click', function() {
      if (infowindow.value) {
        infowindow.value.close()
      }
      infowindow.value.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>')
      infowindow.value.open(map, marker)
    })
  }
}

const clearMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
  if (infowindow.value) {
    infowindow.value.close()
  }
}

const clickSearch = function () {
  clearMarkers() // 인포윈도우 닫기
  initMap('search')
}

const clickCurrentSearch = function () {
  clearMarkers() // 인포윈도우 닫기
  initMap()
}
</script>

<style scoped>
.map-container {
  position: relative;
  border-radius: 10px;
}

.current-search-btn {
  position: absolute;
  top: 10px;
  left: 50%;
  z-index: 100;
  transform: translateX(-50%);
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

#map {
  border-radius: 10px;
}



</style>