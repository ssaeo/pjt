import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import exchangeData from '@/assets/exchangeJSON.json'

export const useCounterStore = defineStore('counter', () => {
  // state
  const token = ref(localStorage.getItem('token'))
  const user = ref(null)
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  // bank
  // const bankBranches = ref([])
  // const selectedBranch = ref(null)
  // products
  const products = ref({
    deposits: [],
    savings: []
  })
  const selectedProduct = ref(null)
  const selectedBank = ref(null)
  // 환율계산기
  const exchangeRates = ref([])  

  // getters
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  // actions
  // 회원가입
  const signUp = function (payload) {
    const { username, password, email, name, age, address, wealth, salary } = payload
    
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username: username,
        password: password,
        email: email,
        name: name,
        age: age,
        address: address,
        wealth: wealth,
        salary: salary
      }
    })
      .then((res) => {
        console.log('회원가입 성공:', res.data)
        logIn({ username, password })
      })
      .catch((err) => {
        console.log('회원가입 실패:', err.response.data)
      })
  }

  // 로그인
  const logIn = function (payload) {
    const { username, password } = payload
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username: username,
        password: password
      }
    })
      .then((res) => {
        console.log('로그인 성공:', res.data)
        token.value = res.data.token
        user.value = res.data.user  // 서버에서 받은 사용자 정보 저장
        router.push({ 
          name: 'ProfileView', 
          params: { username: res.data.user.username }  // username 파라미터 추가
        })
      })
      .catch((err) => {
        console.error('로그인 실패:', err.response?.data)
        alert(err.response?.data?.error || '로그인에 실패했습니다.')
      })
  }

// 로그아웃
const logOut = function () {
  axios({
    method: 'post',
    url: `${API_URL}/accounts/logout/`,
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
    .then(() => {
      token.value = null
      user.value = null
      router.push({ name: 'LogInView' })
    })
    .catch((err) => {
      console.log(err)
    })
}

  // 프로필 조회
  const getProfile = function (username) {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${username}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        user.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 프로필 수정
  const updateProfile = function (username, userData) {
    const config = {
      method: 'put',
      url: `${API_URL}/accounts/profile/${username}/`,
      headers: {
        Authorization: `Token ${token.value}`,
        // FormData를 사용할 경우 자동으로 multipart/form-data로 설정됨
      },
      data: userData
    }
  
    return axios(config)
      .then((res) => {
        user.value = res.data
        return res.data
      })
      .catch((err) => {
        console.error('프로필 업데이트 실패:', err)
        throw err
      })
  }

  // 회원 탈퇴
  const deleteAccount = function (username) {
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/profile/${username}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        token.value = null
        user.value = null
        router.push({ name: 'SignUpView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }


  // 게시글 관련 actions
  const getArticles = function (page = 1) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/`,
      params: { page }
    })
      .then((res) => {
        articles.value = res.data.results
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getArticleDetail = function (articleId) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/`
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const createArticle = function (articleData) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/`,
      data: articleData,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const updateArticle = function (articleId, articleData) {
    return axios({
      method: 'put',
      url: `${API_URL}/articles/${articleId}/`,
      data: articleData,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const deleteArticle = function (articleId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        router.push({ name: 'ArticleList' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 댓글 관련 actions
  const getComments = function (articleId) {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/comments/`
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const createComment = function (articleId, content) {
    return axios({
      method: 'post',
      url: `${API_URL}/articles/${articleId}/comments/`,
      data: { content },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 댓글 수정 함수 추가
  const updateComment = (articleId, commentId, newContent) => {
    return axios({
      method: 'put',
      url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
      data: { content: newContent },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        return res.data
      })
      .catch((err) => {
        console.error('댓글 수정 실패:', err)
        throw err
      })
  }

  const deleteComment = function (articleId, commentId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        console.log('댓글이 삭제되었습니다.')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 은행(BankMap)
  // 은행 검색 관련 actions
  // const searchNearbyBranches = (params) => {
  //   if (!token.value) {
  //     return Promise.reject('로그인이 필요합니다.')
  //   }
  
  //   console.log('검색 파라미터:', params)
  
  //   return axios.get(`${API_URL}/bank-branches/nearby/`, { 
  //     params,
  //     headers: {
  //       'Authorization': `Token ${token.value}`
  //     }
  //   })
  //     .then((res) => {
  //       console.log('서버 응답:', res.data)
  //       bankBranches.value = res.data.results
  //       return res.data.results
  //     })
  //     .catch((err) => {
  //       console.error('주변 은행 검색 실패:', err.response?.data || err)
  //       throw err
  //     })
  // }

  // 금융상품 관련 actions
const fetchProducts = function () {
  return axios({
    method: 'get',
    url: `${API_URL}/finlife/products/`  // URL 수정
  })
    .then((res) => {
      products.value = res.data
    })
    .catch((err) => {
      console.error('상품 목록 조회 실패:', err)
    })
}

const fetchProductDetail = function (type, id) {
  return axios({
    method: 'get',
    url: `${API_URL}/finlife/products/${type}/${id}/`  // URL 수정
  })
    .then((res) => {
      selectedProduct.value = res.data
      return res.data
    })
    .catch((err) => {
      console.error('상품 상세 조회 실패:', err)
    })
}

const joinFinancialProduct = function (productType, productId) {
  // 디버깅을 위한 로그 추가
  console.log('joinFinancialProduct 호출됨:', { productType, productId })

  if (!productType || !productId) {
    console.error('상품 타입 또는 ID가 없습니다')
    return Promise.reject(new Error('상품 정보가 올바르지 않습니다.'))
  }

  return axios({
    method: 'post',
    url: `${API_URL}/finlife/products/join/`,
    data: {
      product_type: productType,
      product_id: productId
    },
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
    .then((res) => {
      console.log('가입 성공 응답:', res.data)
      return res.data
    })
    .catch((err) => {
      console.error('가입 실패 응답:', err.response?.data)
      throw err
    })
}

// 금융상품 해지
const terminateProduct = function (productType, productId) {
  if (!productType || !productId) {
    console.error('상품 타입 또는 ID가 없습니다');
    return Promise.reject(new Error('상품 정보가 올바르지 않습니다.'))
  }

  return axios({
    method: 'post',
    url: `${API_URL}/finlife/products/cancel/`,
    data: {
      product_type: productType,
      product_id: productId
    },
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
    .then((res) => {
      console.log('해지 성공 응답:', res.data)
      return res.data;
    })
    .catch((err) => {
      console.error('해지 실패 응답:', err.response?.data)
      throw err;
    })
}

const getMyFinancialProducts = function () {
  return axios({
    method: 'get',
    url: `${API_URL}/finlife/products/user/`,  // URL 수정
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
    .then((res) => {
      return res.data.products
    })
    .catch((err) => {
      console.error('가입 상품 조회 실패:', err)
      return []
    })
}
// 환율계산기
const loadExchangeRates = () => {
  exchangeRates.value = exchangeData
}





  return { 
    token,
    user,
    articles,
    API_URL,
    isLogin,
    signUp,
    logIn,
    logOut,
    getProfile,
    updateProfile,
    deleteAccount,
    getArticles,
    getArticleDetail,
    createArticle,
    updateArticle,
    deleteArticle,
    // 댓글 관련 actions
    getComments,
    createComment,
    updateComment,
    deleteComment,
    // BankMap
    // bankBranches,
    // searchNearbyBranches,
    // searchBranches,
    // selectedBranch,
    // searchNearbyBranches,
    // setSelectedBranch,
    // Products
    products,
    selectedBank,
    selectedProduct,
    fetchProducts,
    fetchProductDetail,
    joinFinancialProduct,
    getMyFinancialProducts,
    terminateProduct,
    // 환율계산기
    exchangeRates,
    loadExchangeRates,
  }
}, { persist: true })