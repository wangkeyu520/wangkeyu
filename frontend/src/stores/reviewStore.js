import { reactive, computed } from 'vue'
import axios from 'axios'
import { getTagLabels, STORE_INFO } from '../constants/tags'

const state = reactive({
  currentPage: 'home',
  selectedTags: [],
  selectedPlatform: '',
  generatedReview: '',
  isLoading: false,
  error: null,
  history: [],
})

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

let toastHandler = null

function parseApiError(error) {
  const detail = error.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item).join('；')
  }
  if (error.code === 'ECONNABORTED') return '请求超时，请稍后重试'
  if (!error.response) return '网络连接失败，请检查网络后重试'
  return error.message || '生成评价失败，请重试'
}

const getters = {
  canProceed: computed(() => {
    if (state.currentPage === 'select') {
      if (state.selectedTags.length === 0) return false
      if (state.selectedPlatform === '') return false
    }
    return true
  }),

  tagCount: computed(() => state.selectedTags.length),

  hasReview: computed(() => state.generatedReview.length > 0),
}

const actions = {
  registerToast(handler) {
    toastHandler = handler
  },

  showToast(message, type = 'success') {
    if (toastHandler) {
      toastHandler(message, type)
    }
  },

  navigateTo(page) {
    state.currentPage = page
  },

  selectTag(tagId) {
    const index = state.selectedTags.indexOf(tagId)
    if (index > -1) {
      state.selectedTags.splice(index, 1)
    } else {
      if (state.selectedTags.length >= 2) {
        throw new Error('最多选择2个感受标签')
      }
      state.selectedTags.push(tagId)
    }
  },

  selectPlatform(platformId) {
    state.selectedPlatform = platformId
  },

  async generateReview() {
    if (state.selectedTags.length === 0) {
      throw new Error('请先选择至少一个感受标签')
    }
    if (!state.selectedPlatform) {
      throw new Error('请选择发布平台')
    }

    state.isLoading = true
    state.error = null

    try {
      const response = await apiClient.post('/generate-review', {
        feeling_tags: getTagLabels(state.selectedTags),
        platform: state.selectedPlatform,
        store_info: STORE_INFO,
      })

      if (response.data.success) {
        state.generatedReview = response.data.review.content

        state.history.unshift({
          id: Date.now(),
          content: response.data.review.content,
          platform: state.selectedPlatform,
          tags: [...state.selectedTags],
          timestamp: new Date().toLocaleString('zh-CN'),
        })

        if (state.history.length > 10) {
          state.history.pop()
        }

        state.currentPage = 'preview'
      } else {
        throw new Error('生成评价失败，请重试')
      }
    } catch (error) {
      const message = parseApiError(error)
      state.error = message
      actions.showToast(message, 'error')
      throw new Error(message)
    } finally {
      state.isLoading = false
    }
  },

  resetAll() {
    state.selectedTags = []
    state.selectedPlatform = ''
    state.generatedReview = ''
    state.error = null
    state.currentPage = 'home'
  },

  clearError() {
    state.error = null
  },
}

const reviewStore = {
  state,
  ...getters,
  ...actions,
  apiClient,
}

export function useReviewStore() {
  return reviewStore
}

export { reviewStore }
