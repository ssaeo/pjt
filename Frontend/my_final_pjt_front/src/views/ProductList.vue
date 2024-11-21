<template>
  <div>
    <h1>상품 목록</h1>

    <!-- 은행 검색 -->
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="은행명을 입력하세요"
      />
      <button @click="applyFilter">검색하기</button>
    </div>

    <!-- 상품 테이블 -->
    <table>
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th>
            6개월
            <button @click="sortByRate('6', 'desc')">▲</button>
            <button @click="sortByRate('6', 'asc')">▼</button>
          </th>
          <th>
            12개월
            <button @click="sortByRate('12', 'desc')">▲</button>
            <button @click="sortByRate('12', 'asc')">▼</button>
          </th>
          <th>
            24개월
            <button @click="sortByRate('24', 'desc')">▲</button>
            <button @click="sortByRate('24', 'asc')">▼</button>
          </th>
          <th>
            36개월
            <button @click="sortByRate('36', 'desc')">▲</button>
            <button @click="sortByRate('36', 'asc')">▼</button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="product in sortedFilteredProducts"
          :key="`${product.type}-${product.id}`"
        >
          <td>{{ product.kor_co_nm }}</td>
          <td>
            <router-link :to="`/products/${product.type}/${product.id}`">
              {{ product.fin_prdt_nm }}
            </router-link>
          </td>
          <td>{{ product.interest_rates['6'] || '-' }}%</td>
          <td>{{ product.interest_rates['12'] || '-' }}%</td>
          <td>{{ product.interest_rates['24'] || '-' }}%</td>
          <td>{{ product.interest_rates['36'] || '-' }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const products = ref([]);
    const searchQuery = ref("");
    const sortColumn = ref(null);
    const sortOrder = ref(null);

    // 상품 목록 가져오기
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/finlife/products/");
        const { deposits, savings } = response.data;

        // 데이터 통합 및 type 필드 추가
        const updatedDeposits = deposits.map((item) => ({
          ...item,
          type: "deposit",
        }));
        const updatedSavings = savings.map((item) => ({
          ...item,
          type: "saving",
        }));

        products.value = [...updatedDeposits, ...updatedSavings]
      } catch (error) {
        console.error("상품 목록을 불러오는 중 오류:", error)
      }
    };

    onMounted(fetchProducts);

    // 검색 및 정렬을 적용한 상품 목록
    const sortedFilteredProducts = computed(() => {
      let filtered = products.value;

      // 검색어 필터
      if (searchQuery.value.trim()) {
        const query = searchQuery.value.trim().toLowerCase();
        filtered = filtered.filter((product) =>
          product.kor_co_nm.toLowerCase().includes(query)
        );
      }

      // 정렬
      if (sortColumn.value) {
        filtered.sort((a, b) => {
          const rateA = parseFloat(a.interest_rates[sortColumn.value] || 0)
          const rateB = parseFloat(b.interest_rates[sortColumn.value] || 0)

          // -%인 항목을 0으로 간주하고 하단에 배치
          const valueA = isNaN(rateA) || rateA === -1 ? -Infinity : rateA;
          const valueB = isNaN(rateB) || rateB === -1 ? -Infinity : rateB;

          return sortOrder.value === "asc" ? valueA - valueB : valueB - valueA;
        });
      }

      return filtered;
    });

    // 검색 버튼 클릭 시 호출
    const applyFilter = () => {
      searchQuery.value = searchQuery.value.trim();
    };

    // 정렬 기준 및 방향 설정
    const sortByRate = (term, order) => {
      sortColumn.value = term;
      sortOrder.value = order;
    };

    return {
      products,
      searchQuery,
      sortColumn,
      sortOrder,
      sortedFilteredProducts,
      applyFilter,
      sortByRate,
    };
  },
};
</script>

<style scoped>
.search-container {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.search-container input {
  padding: 8px;
  font-size: 14px;
  width: 100%;
  max-width: 300px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-container button {
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

.search-container button:hover {
  background-color: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 16px;
  text-align: center;
}

th,
td {
  padding: 12px;
  border: 1px solid #ccc;
}

th {
  background-color: #f4f4f4;
  position: relative;
}

button {
  margin-left: 5px;
  padding: 2px 5px;
  font-size: 12px;
  cursor: pointer;
  border: 1px solid #ccc;
  background-color: #fff;
}

button:hover {
  background-color: #ddd;
}
</style>
