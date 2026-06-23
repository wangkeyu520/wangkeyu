<script setup>
import { ref, computed, onMounted } from 'vue'
import { useReviewStore } from '../stores/reviewStore'
import { getTagLabels, PLATFORM_LABEL_MAP, STORE_INFO } from '../constants/tags'
import { Refresh, ArrowLeft } from '@element-plus/icons-vue'

const store = useReviewStore()
const hasFailed = ref(false)

const displayTags = computed(() => getTagLabels(store.state.selectedTags))

const displayPlatform = computed(() => {
  return PLATFORM_LABEL_MAP[store.state.selectedPlatform] || store.state.selectedPlatform
})

const runGenerate = async () => {
  hasFailed.value = false
  store.clearError()

  try {
    await store.generateReview()
  } catch {
    hasFailed.value = true
  }
}

const handleRetry = () => {
  runGenerate()
}

const handleBack = () => {
  store.clearError()
  store.navigateTo('select')
}

onMounted(() => {
  setTimeout(runGenerate, 400)
})
</script>

<template>
  <div class="generate-page">
    <div class="page-content">
      <div v-if="!hasFailed" class="loading-container">
        <div class="avatar-section">
          <div class="robot-avatar">
            <span class="robot-emoji">🤖</span>
            <div class="robot-glow"></div>
          </div>
          <div class="online-dot"></div>
        </div>

        <h2 class="loading-title">AI 正在思考中...</h2>
        <p class="loading-desc">请稍候，正在为您生成专属评价</p>

        <div class="info-card">
          <div class="card-header">
            <div class="store-avatar">
              <span>☕</span>
            </div>
            <div class="store-info">
              <h3 class="store-name">{{ STORE_INFO.name }}</h3>
              <p class="store-location">{{ STORE_INFO.location }}</p>
            </div>
          </div>

          <div class="card-divider"></div>

          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">感受标签</span>
              <div class="info-tags">
                <span
                  v-for="tag in displayTags"
                  :key="tag"
                  class="tag-chip">{{ tag }}</span>
              </div>
            </div>
            <div class="info-item">
              <span class="info-label">发布平台</span>
              <span class="platform-chip">{{ displayPlatform }}</span>
            </div>
          </div>
        </div>

        <div class="loading-indicator">
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
          <div class="loading-dots">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>

        <p class="loading-tip">
          AI 正在分析您的选择，生成符合平台风格的评价内容...
        </p>
      </div>

      <div v-else class="error-container">
        <div class="error-icon">😔</div>
        <h2 class="error-title">生成失败了</h2>
        <p class="error-message">{{ store.state.error || '请稍后重试' }}</p>

        <div class="error-card">
          <div class="error-card-row">
            <span class="error-card-label">感受标签</span>
            <div class="info-tags">
              <span
                v-for="tag in displayTags"
                :key="tag"
                class="tag-chip">{{ tag }}</span>
            </div>
          </div>
          <div class="error-card-row">
            <span class="error-card-label">发布平台</span>
            <span class="platform-chip">{{ displayPlatform }}</span>
          </div>
        </div>

        <div class="error-actions">
          <el-button
            type="primary"
            size="large"
            class="retry-btn"
            :loading="store.state.isLoading"
            @click="handleRetry">
            <el-icon><Refresh /></el-icon>
            重新生成
          </el-button>
          <el-button
            size="large"
            class="back-btn"
            @click="handleBack">
            <el-icon><ArrowLeft /></el-icon>
            返回修改
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.generate-page {
  min-height: 100vh;
  max-width: 480px;
  margin: 0 auto;
  background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
}

.page-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
  flex: 1;
}

.avatar-section {
  position: relative;
  margin-bottom: 24px;
}

.robot-avatar {
  position: relative;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #e8d0a0, #c9994b);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(201, 153, 75, 0.3);
  animation: robot-float 3s ease-in-out infinite;
}

.robot-emoji {
  font-size: 50px;
}

.robot-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140px;
  height: 140px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse-glow 2s ease-in-out infinite;
}

.online-dot {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 16px;
  height: 16px;
  background: #10b981;
  border-radius: 50%;
  border: 3px solid white;
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes robot-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes pulse-glow {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
  50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.8; }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.loading-title {
  font-size: 24px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 8px 0;
}

.loading-desc {
  color: #93632c;
  font-size: 14px;
  margin: 0 0 32px 0;
}

.info-card,
.error-card {
  width: 100%;
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(201, 153, 75, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.store-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #e8d0a0, #c9994b);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.store-name {
  font-size: 16px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 4px 0;
}

.store-location {
  font-size: 12px;
  color: #93632c;
  margin: 0;
}

.card-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 153, 75, 0.2), transparent);
  margin: 16px 0;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 12px;
  color: #93632c;
  font-weight: 500;
}

.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-chip {
  padding: 4px 12px;
  background: rgba(201, 153, 75, 0.1);
  border-radius: 12px;
  font-size: 12px;
  color: #c9994b;
  font-weight: 500;
}

.platform-chip {
  padding: 4px 12px;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 12px;
  font-size: 12px;
  color: #d97706;
  font-weight: 600;
  align-self: flex-start;
}

.loading-indicator {
  width: 100%;
  margin-bottom: 24px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(201, 153, 75, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #c9994b, #f59e0b);
  border-radius: 3px;
  animation: progress-flow 2s ease-in-out infinite;
}

@keyframes progress-flow {
  0% { width: 0%; }
  50% { width: 70%; }
  100% { width: 100%; }
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background: #c9994b;
  border-radius: 50%;
  animation: dot-bounce 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.loading-tip {
  color: #93632c;
  font-size: 12px;
  text-align: center;
  margin: 0;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.error-title {
  font-size: 22px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 8px 0;
}

.error-message {
  font-size: 14px;
  color: #b45309;
  text-align: center;
  margin: 0 0 24px 0;
  line-height: 1.5;
  max-width: 280px;
}

.error-card {
  border-color: rgba(239, 68, 68, 0.15);
}

.error-card-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.error-card-row:last-child {
  margin-bottom: 0;
}

.error-card-label {
  font-size: 12px;
  color: #93632c;
  font-weight: 500;
}

.error-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: auto;
  padding-bottom: 24px;
}

.retry-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, #c9994b, #d97706);
  border: none;
}

.back-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  border-radius: 12px;
  border: 2px solid #e8d0a0;
  color: #c9994b;
}
</style>
