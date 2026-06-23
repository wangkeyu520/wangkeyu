<script setup>
import { ref, onMounted, onErrorCaptured } from 'vue'
import { ElMessage } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import HomePage from './components/HomePage.vue'
import SelectPage from './components/SelectPage.vue'
import GeneratePage from './components/GeneratePage.vue'
import PreviewPage from './components/PreviewPage.vue'
import ErrorBoundary from './components/ErrorBoundary.vue'
import { useReviewStore } from './stores/reviewStore'

const store = useReviewStore()
const globalError = ref(null)

const showToast = (message, type = 'success') => {
  ElMessage({
    message,
    type,
    duration: 2500,
    showClose: true,
  })
}

onMounted(() => {
  store.registerToast(showToast)
})

const handleGlobalError = (error) => {
  globalError.value = error
  showToast(error.message || '发生未知错误', 'error')
}

onErrorCaptured((error) => {
  handleGlobalError(error)
  return false
})
</script>

<template>
  <el-config-provider :locale="zhCn">
    <ErrorBoundary @error="handleGlobalError">
      <div class="app-container">
        <transition name="page-transition" mode="out-in">
          <HomePage v-if="store.state.currentPage === 'home'" key="home" />
          <SelectPage v-else-if="store.state.currentPage === 'select'" key="select" />
          <GeneratePage v-else-if="store.state.currentPage === 'generate'" key="generate" />
          <PreviewPage v-else key="preview" />
        </transition>
      </div>
    </ErrorBoundary>
  </el-config-provider>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  min-height: 100dvh;
  background: linear-gradient(135deg, #fdfbf7 0%, #f9f2e6 50%, #fffbeb 100%);
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.page-transition-enter-active {
  transition: all 0.3s ease-out;
}

.page-transition-leave-active {
  transition: all 0.2s ease-in;
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>