import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useCounterStore = defineStore('counter', () => {
  // state
  const token = ref(localStorage.getItem('token'))
  const user = ref(null)
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'

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
    const { username, password } = payload
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username: username,
        password: password
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
      user.value = { username: res.data.username }  // user 정보 저장
      router.push({ 
        name: 'ProfileView', 
        params: { username: res.data.username } 
      })
    })
    .catch((err) => {
      console.log('로그인 실패:', err.response?.data)
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
    axios({
      method: 'put',
      url: `${API_URL}/accounts/profile/${username}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: userData
    })
      .then((res) => {
        user.value = res.data
      })
      .catch((err) => {
        console.log(err)
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
  const getArticles = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/articles/`
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
    deleteComment,
  }
}, { persist: true })