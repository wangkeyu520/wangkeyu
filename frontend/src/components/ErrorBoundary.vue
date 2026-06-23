<template>
  <div v-if="error" class="error-boundary">
    <div class="error-content">
      <div class="error-icon">
        <el-icon :size="48"><Warning /></el-icon>
      </div>
      <h2 class="error-title">页面出错了</h2>
      <p class="error-message">{{ error.message || '未知错误' }}</p>
      <div class="error-actions">
        <el-button type="primary" @click="retry" :disabled="retryCount >= maxRetries">
          <el-icon><Refresh /></el-icon>
          重新加载
        </el-button>
        <el-button @click="goHome">
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
      </div>
      <p v-if="retryCount >= maxRetries" class="error-tip">
        重试次数已达上限，请稍后再试
      </p>
    </div>
  </div>
  <slot v-else />
</template>

<script>
import { ref, onErrorCaptured } from 'vue'
import { Warning, Refresh, HomeFilled } from '@element-plus/icons-vue'

export default {
  name: 'ErrorBoundary',
  components: {
    Warning,
    Refresh,
    HomeFilled
  },
  props: {
    maxRetries: {
      type: Number,
      default: 3
    }
  },
  emits: ['error'],
  setup(props, { emit }) {
    const error = ref(null)
    const retryCount = ref(0)

    const handleError = (err) => {
      error.value = err
      retryCount.value++
      emit('error', err)
      console.error('Error Boundary caught:', err)
      return false
    }

    const retry = () => {
      if (retryCount.value < props.maxRetries) {
        error.value = null
      }
    }

    const goHome = () => {
      window.location.reload()
    }

    onErrorCaptured(handleError)

    return {
      error,
      retryCount,
      retry,
      goHome
    }
  }
}
</script>

<style scoped>
.error-boundary {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fdfbf7 0%, #f9f2e6 100%);
}

.error-content {
  text-align: center;
  padding: 40px;
  max-width: 320px;
}

.error-icon {
  margin-bottom: 16px;
  color: #f59e0b;
}

.error-title {
  font-size: 20px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 8px 0;
}

.error-message {
  font-size: 14px;
  color: #93632c;
  margin: 0 0 20px 0;
}

.error-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.error-tip {
  margin-top: 16px;
  font-size: 12px;
  color: #dc2626;
}
</style>
