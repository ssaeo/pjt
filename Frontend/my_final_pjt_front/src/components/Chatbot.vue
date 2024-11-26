<template>
  <div class="chatbot">
    <div class="chatbot-header">
      <h3>AI 금융 상담사</h3>
      <button @click="$emit('closeChatbot')" class="close-btn">X</button>
    </div>
    <div class="chatbot-body">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <p>
          <strong>{{ message.role === 'user' ? '질문' : 'AI 답변' }}:</strong>
          {{ message.content }}
        </p>
      </div>
      <div v-if="loading" class="loading-message">AI가 답변을 작성 중입니다...</div>
    </div>
    <div class="chatbot-footer">
      <input
        v-model="userMessage"
        placeholder="예: 케이뱅크 상품 추천해줘"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  setup(_, { emit }) {
    // 사용자에게 표시될 메시지
    const messages = ref([
      {
        role: 'assistant',
        content: '안녕하세요! 무엇을 도와드릴까요? 금융 상품에 대해 질문해 주세요.'
      }
    ])

    // 시스템 메시지 (API 요청용, 사용자에게는 보이지 않음)
    const systemMessage = {
      role: 'system',
      content: `
        당신은 금융 상담 전문가입니다. 
        사용자의 질문에 대해 간결하고 유용한 답변만 작성하세요.
        필요하면 관련 금융 상품을 추천하거나 참고할 정보를 제공하세요.
        답변은 너무 길지않고 요점만 말하도록 하고 **는 빼고 답변하세요.
      `
    }

    const userMessage = ref('')
    const loading = ref(false)

    const sendMessage = () => {
      if (!userMessage.value.trim()) return

      const userInput = userMessage.value
      messages.value.push({ role: 'user', content: userInput })
      userMessage.value = ''
      loading.value = true

      // 시스템 메시지 포함한 API 요청용 메시지 배열
      const apiMessages = [systemMessage, ...messages.value]

      axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-4o-mini',
          messages: apiMessages,
          max_tokens: 200,
          temperature: 0.7,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
          },
        }
      )
        .then(response => {
          const aiResponse = response.data.choices[0].message.content
          messages.value.push({ role: 'assistant', content: aiResponse })
        })
        .catch(error => {
          console.error('AI 응답 실패:', error.response ? error.response.data : error)
          messages.value.push({
            role: 'assistant',
            content: '죄송합니다. 답변을 생성하는 데 문제가 발생했습니다. 다시 시도해 주세요.',
          })
        })
        .finally(() => {
          loading.value = false
        })
    }

    return {
      messages,
      userMessage,
      sendMessage,
      loading,
    }
  },
}
</script>

<style scoped>
.chatbot {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 300px;
  height: 400px; /* 높이 조정 */
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 헤더 스타일 */
.chatbot-header {
  background-color: #26A69A;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 본문 스타일 */
.chatbot-body {
  padding: 10px;
  flex: 1;
  overflow-y: auto;
  background-color: #f9f9f9;
}

/* 푸터 스타일 */
.chatbot-footer {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.chatbot-footer input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.chatbot-footer button {
  margin-left: 10px;
  padding: 8px 12px;
  background-color: #26A69A;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chatbot-footer button:hover {
  background-color: #26A69A;
}

/* 로딩 메시지 */
.loading-message {
  text-align: center;
  color: #555;
  margin-top: 10px;
  font-size: 14px;
}
</style>
