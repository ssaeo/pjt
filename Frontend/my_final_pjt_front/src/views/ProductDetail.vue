<template>
  <div>
    <div v-if="loading">로딩 중...</div> <!-- 로딩 메시지 -->
    <div v-else-if="product">
      <h1>{{ product.fin_prdt_nm }}</h1>
      <p><strong>은행명:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>상품 설명:</strong> {{ product.etc_note || '설명이 없습니다.' }}</p>
      <p><strong>가입 방법:</strong> {{ product.join_way || '정보 없음' }}</p>
      <p><strong>가입 대상:</strong> {{ product.join_member || '정보 없음' }}</p>

      <h2>옵션 정보</h2>
      <div v-if="options.length > 0">
        <div v-for="option in options" :key="option.id">
          <p><strong>저축 기간:</strong> {{ option.save_trm }}개월</p>
          <p><strong>기본 금리:</strong> {{ option.intr_rate }}%</p>
          <p><strong>최대 금리:</strong> {{ option.intr_rate2 }}%</p>
        </div>
      </div>
      <p v-else>옵션 정보가 없습니다.</p>
    </div>
    <div v-else>
      <p>상품 정보를 불러오는 데 실패했습니다.</p>
    </div>
    <button @click="$router.go(-1)">뒤로 가기</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      product: null, // 상품 데이터
      options: [], // 옵션 데이터
      loading: true, // 로딩 상태
    };
  },
  mounted() {
    const { productType, id } = this.$route.params;

    // API 호출
    axios
      .get(`http://localhost:8000/finlife/products/${productType}/${id}/`)
      .then((response) => {
        this.product = response.data.product; // 상품 데이터 저장
        this.options = response.data.options; // 옵션 데이터 저장
        this.loading = false; // 로딩 종료
      })
      .catch((error) => {
        console.error("상품 정보를 불러오는 중 오류:", error);
        this.loading = false; // 로딩 종료
      });
  },
};
</script>
