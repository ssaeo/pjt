<template>
  <v-footer
    class="bg-indigo-lighten-1 text-center d-flex flex-column"
  >
    <div>
      <v-btn
        v-for="icon in icons"
        :key="icon"
        :icon="icon"
        class="mx-4"
        variant="text"
        @click="goHome" 
      ></v-btn>
    </div>

    <div class="pt-0">
      Phasellus feugiat arcu sapien, et iaculis ipsum elementum sit amet. Mauris cursus commodo interdum. Praesent ut risus eget metus luctus accumsan id ultrices nunc. Sed at orci sed massa consectetur dignissim a sit amet dui. Duis commodo vitae velit et faucibus. Morbi vehicula lacinia malesuada. Nulla placerat augue vel ipsum ultrices, cursus iaculis dui sollicitudin. Vestibulum eu ipsum vel diam elementum tempor vel ut orci. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    </div>

    <v-divider></v-divider>

    <div>
      {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
    </div>
  </v-footer>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // useRouter 훅 가져오기

// 아이콘 목록을 정의합니다.
const icons = ref(['mdi-facebook', 'mdi-twitter', 'mdi-instagram'])

const router = useRouter() // 라우터 인스턴스 가져오기

const goHome = () => {
  router.push({ name: 'home' }) // Home 페이지로 이동
}
</script>

<style scoped>
.bg-indigo-lighten-1 {
  background-color: #26A69A !important; /* Vuetify의 indigo lighten-1 색상 */
}

.text-center {
  text-align: center;
}

.d-flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.mx-4 {
  margin-left: 16px;
  margin-right: 16px;
}

.pt-0 {
  padding-top: 0;
}
</style>