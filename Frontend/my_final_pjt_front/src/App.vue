<template>
  <div id="app">
    <nav>
      <ul>
        <li><RouterLink to="/">Home</RouterLink></li>
        <li><RouterLink to="/calculator">Exchange Calculator</RouterLink></li>
        <li><RouterLink to="/bank-map">Bank Map</RouterLink></li>
        <li><RouterLink to="/products">Products</RouterLink></li> <!-- Products 링크 추가 -->
      </ul>
    </nav>
    <RouterView />
  </div>
</template>

<script>
import { RouterView, RouterLink } from 'vue-router';

export default {
  name: 'App',
  components: {
    RouterView,
    RouterLink,
  },
};
</script>

<style>
nav {
  background-color: #f8f9fa;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 15px; /* 메뉴 간격 */
}
li {
  display: inline;
}
a {
  text-decoration: none;
  color: #007bff;
}
a:hover {
  text-decoration: underline;
}
</style>
