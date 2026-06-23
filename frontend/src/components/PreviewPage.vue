<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useReviewStore } from '../stores/reviewStore'
import { PLATFORMS, PLATFORM_LABEL_MAP } from '../constants/tags'
import { ArrowLeft, CopyDocument, Check, Share, Star } from '@element-plus/icons-vue'

const store = useReviewStore()

const displayedText = ref('')
const copied = ref(false)
const showSuccess = ref(false)
const isTyping = ref(true)
const showPublishGuide = ref(false)
const currentGuideStep = ref(0)
let typingTimer = null

const platformInfo = computed(() => {
  const platform = PLATFORMS.find((p) => p.id === store.state.selectedPlatform)
  if (platform?.id === 'xiaohongshu') {
    return {
      name: platform.name,
      icon: platform.icon,
      cardStyle: 'xiaohongshu',
    }
  }
  return {
    name: PLATFORM_LABEL_MAP[store.state.selectedPlatform] || 'Google',
    icon: '🔍',
    cardStyle: 'google',
  }
})

const fullText = computed(() => store.state.generatedReview)

const clearTypingTimer = () => {
  if (typingTimer) {
    clearInterval(typingTimer)
    typingTimer = null
  }
}

const typeText = () => {
  if (!fullText.value) return

  clearTypingTimer()
  displayedText.value = ''
  isTyping.value = true
  let index = 0

  typingTimer = setInterval(() => {
    if (index < fullText.value.length) {
      displayedText.value += fullText.value[index]
      index++
    } else {
      clearTypingTimer()
      isTyping.value = false
    }
  }, 30)
}

onMounted(() => {
  typeText()
})

onUnmounted(() => {
  clearTypingTimer()
})

watch(fullText, () => {
  typeText()
})

const copyReview = async () => {
  try {
    await navigator.clipboard.writeText(fullText.value)
    copied.value = true
    store.showToast('已复制到剪贴板！', 'success')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch {
    store.showToast('复制失败，请手动复制', 'error')
  }
}

const handlePublish = () => {
  showPublishGuide.value = true
  currentGuideStep.value = 0
}

const nextGuideStep = () => {
  if (currentGuideStep.value < 2) {
    currentGuideStep.value++
  } else {
    showPublishGuide.value = false
    showSuccess.value = true
  }
}

const closeSuccess = () => {
  showSuccess.value = false
  store.resetAll()
}

const closeGuide = () => {
  showPublishGuide.value = false
}
</script>

<template>
  <div class="preview-page">
    <div class="page-content">
      <div class="page-header">
        <el-button circle @click="store.navigateTo('select')" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <div class="header-center">
          <h2 class="header-title">评价预览</h2>
          <p class="header-subtitle">{{ platformInfo.name }}风格</p>
        </div>
        <div class="spacer"></div>
      </div>

      <div 
        class="review-card-wrapper"
        :class="platformInfo.cardStyle">
        <div v-if="platformInfo.cardStyle === 'xiaohongshu'" class="xiaohongshu-card">
          <div class="xh-card-header">
            <div class="xh-avatar">S</div>
            <div class="xh-user-info">
              <span class="xh-username">Sunny Tea House</span>
              <span class="xh-location">📍 San Jose</span>
            </div>
            <div class="xh-more">···</div>
          </div>
          
          <div class="xh-card-body">
            <div class="xh-images">
              <div class="xh-image-item">🥤</div>
              <div class="xh-image-item">✨</div>
              <div class="xh-image-item">☕</div>
            </div>
            
            <div class="xh-text-content">
              <p class="xh-text">{{ displayedText }}</p>
              <span v-if="isTyping" class="typing-cursor">|</span>
            </div>
            
            <div class="xh-tags">
              <span class="xh-tag">#奶茶推荐</span>
              <span class="xh-tag">#探店</span>
              <span class="xh-tag">#SunnyTea</span>
            </div>
          </div>
          
          <div class="xh-card-footer">
            <div class="xh-action">
              <span class="xh-icon">❤️</span>
              <span>2.3k</span>
            </div>
            <div class="xh-action">
              <span class="xh-icon">💬</span>
              <span>156</span>
            </div>
            <div class="xh-action">
              <span class="xh-icon">⬆️</span>
              <span>分享</span>
            </div>
          </div>
        </div>

        <div v-else class="google-card">
          <div class="google-header">
            <div class="google-rating">
              <el-icon v-for="i in 5" :key="i" class="star-icon"><Star /></el-icon>
              <span class="rating-value">5.0</span>
            </div>
            <span class="google-date">2024</span>
          </div>
          
          <div class="google-body">
            <h3 class="google-title">{{ store.state.generatedReview.split('\n')[0] || 'Great Experience!' }}</h3>
            <p class="google-text">{{ displayedText }}</p>
            <span v-if="isTyping" class="typing-cursor">|</span>
          </div>
          
          <div class="google-footer">
            <div class="google-reply">
              <el-icon><Share /></el-icon>
              <span>Helpful</span>
            </div>
          </div>
        </div>
      </div>

      <div class="action-bar">
        <el-button 
          circle 
          @click="copyReview"
          class="action-btn"
          :class="{ 'btn-active': copied }">
          <el-icon><Check v-if="copied" /><CopyDocument v-else /></el-icon>
        </el-button>
        <span class="action-label">{{ copied ? '已复制' : '复制评价' }}</span>
      </div>

      <div class="guide-section">
        <h3 class="guide-title">发布指引</h3>
        <div class="guide-steps">
          <div 
            v-for="(step, index) in [
              { icon: '📋', title: '复制内容', desc: '点击复制按钮' },
              { icon: '📱', title: '打开平台', desc: '打开' + platformInfo.name },
              { icon: '🚀', title: '发布评价', desc: '粘贴并发布' }
            ]"
            :key="index"
            class="guide-step"
            :class="{ 'step-active': index === 0 }">
            <div class="step-icon-wrapper">
              <span class="step-icon">{{ step.icon }}</span>
            </div>
            <div class="step-content">
              <span class="step-title">{{ step.title }}</span>
              <span class="step-desc">{{ step.desc }}</span>
            </div>
            <div v-if="index < 2" class="step-arrow">→</div>
          </div>
        </div>
      </div>

      <div class="bottom-buttons">
        <el-button 
          size="large" 
          @click="store.resetAll"
          class="reset-btn">
          重新生成
        </el-button>
        <el-button 
          type="primary" 
          size="large"
          @click="handlePublish"
          class="publish-btn">
          <el-icon><Share /></el-icon>
          发布评价
        </el-button>
      </div>
    </div>

    <transition name="fade-scale">
      <div v-if="showPublishGuide" class="guide-modal" @click.self="closeGuide">
        <div class="guide-modal-content">
          <div class="guide-modal-header">
            <h3 class="guide-modal-title">发布步骤</h3>
            <el-button circle @click="closeGuide" class="close-btn">
              <el-icon><Check /></el-icon>
            </el-button>
          </div>
          
          <div class="guide-modal-body">
            <transition name="slide" mode="out-in">
              <div v-if="currentGuideStep === 0" key="step0" class="guide-step-content">
                <div class="step-icon-big">📋</div>
                <h4>复制评价内容</h4>
                <p>评价内容已生成完毕，请点击复制按钮或手动复制上方内容</p>
              </div>
              <div v-else-if="currentGuideStep === 1" key="step1" class="guide-step-content">
                <div class="step-icon-big">📱</div>
                <h4>打开{{ platformInfo.name }}</h4>
                <p>打开{{ platformInfo.name }}App，搜索 Sunny Tea House 店铺页面</p>
              </div>
              <div v-else key="step2" class="guide-step-content">
                <div class="step-icon-big">🚀</div>
                <h4>粘贴并发布</h4>
                <p>在评价输入框中粘贴内容，配上美美的照片，点击发布！</p>
              </div>
            </transition>
            
            <div class="guide-progress">
              <span 
                v-for="i in 3" 
                :key="i" 
                class="progress-dot"
                :class="{ 'dot-active': i <= currentGuideStep + 1 }">
              </span>
            </div>
          </div>
          
          <div class="guide-modal-footer">
            <el-button 
              v-if="currentGuideStep > 0"
              @click="currentGuideStep--"
              class="prev-btn">
              上一步
            </el-button>
            <el-button 
              type="primary"
              @click="nextGuideStep"
              class="next-btn">
              {{ currentGuideStep === 2 ? '完成发布' : '下一步' }}
            </el-button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade-scale">
      <div v-if="showSuccess" class="success-modal">
        <div class="success-content">
          <div class="success-icon">🎉</div>
          <h2 class="success-title">发布成功！</h2>
          <p class="success-desc">感谢您的评价，期待下次光临</p>
          <div class="success-stars">
            <span v-for="i in 5" :key="i" class="star">⭐</span>
          </div>
          <el-button type="primary" @click="closeSuccess" class="success-btn">
            返回首页
          </el-button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.preview-page {
  min-height: 100vh;
  max-width: 480px;
  margin: 0 auto;
  background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
}

.page-content {
  padding: 20px;
  padding-bottom: 32px;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  flex-shrink: 0;
}

.header-center {
  flex: 1;
  text-align: center;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 4px 0;
}

.header-subtitle {
  font-size: 12px;
  color: #93632c;
  margin: 0;
}

.spacer {
  width: 40px;
  flex-shrink: 0;
}

.review-card-wrapper {
  margin-bottom: 20px;
}

.xiaohongshu-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(239, 68, 68, 0.12);
  border: 1px solid #fecaca;
}

.xh-card-header {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.xh-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ef4444, #ec4899);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
}

.xh-user-info {
  flex: 1;
}

.xh-username {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 2px;
}

.xh-location {
  font-size: 12px;
  color: #6b7280;
}

.xh-more {
  color: #9ca3af;
  font-size: 18px;
}

.xh-card-body {
  padding: 0 16px;
}

.xh-images {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
}

.xh-image-item {
  width: calc((100% - 8px) / 3);
  aspect-ratio: 1;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
}

.xh-text-content {
  margin-bottom: 12px;
}

.xh-text {
  font-size: 15px;
  line-height: 1.6;
  color: #1f2937;
  white-space: pre-wrap;
  word-break: break-all;
}

.typing-cursor {
  animation: blink 0.8s infinite;
  color: #ef4444;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.xh-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 16px;
}

.xh-tag {
  padding: 4px 10px;
  background: rgba(239, 68, 68, 0.08);
  color: #ef4444;
  font-size: 12px;
  border-radius: 4px;
}

.xh-card-footer {
  display: flex;
  justify-content: space-around;
  padding: 16px;
  border-top: 1px solid #f3f4f6;
}

.xh-action {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #6b7280;
}

.xh-icon {
  font-size: 16px;
}

.google-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
  border: 1px solid #bfdbfe;
}

.google-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.google-rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.star-icon {
  color: #fbbf24;
  font-size: 16px;
}

.rating-value {
  font-size: 14px;
  font-weight: 600;
  color: #1d4ed8;
  margin-left: 4px;
}

.google-date {
  font-size: 12px;
  color: #6b7280;
}

.google-body {
  margin-bottom: 16px;
}

.google-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.google-text {
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  white-space: pre-wrap;
}

.google-footer {
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.google-reply {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #1d4ed8;
  font-size: 14px;
  cursor: pointer;
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 20px;
}

.action-btn {
  width: 48px;
  height: 48px;
  background: white;
  border: 2px solid #e8d0a0;
  transition: all 0.3s;
}

.action-btn:hover {
  border-color: #c9994b;
}

.btn-active {
  background: linear-gradient(135deg, #c9994b, #d97706);
  border-color: transparent;
  color: white;
}

.action-label {
  font-size: 14px;
  color: #775029;
  font-weight: 500;
}

.guide-section {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(201, 153, 75, 0.1);
}

.guide-title {
  font-size: 16px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 16px 0;
}

.guide-steps {
  display: flex;
  align-items: center;
  gap: 8px;
}

.guide-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 8px;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.3s;
}

.step-active {
  background: linear-gradient(135deg, rgba(201, 153, 75, 0.1), rgba(245, 158, 11, 0.1));
  transform: scale(1.05);
}

.step-icon-wrapper {
  width: 36px;
  height: 36px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.step-content {
  text-align: center;
}

.step-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #775029;
}

.step-desc {
  font-size: 11px;
  color: #93632c;
}

.step-arrow {
  color: #e8d0a0;
  font-size: 16px;
  font-weight: 700;
}

.bottom-buttons {
  display: flex;
  gap: 12px;
}

.reset-btn {
  flex: 1;
  height: 52px;
  font-size: 16px;
  border-radius: 14px;
  border: 2px solid #e8d0a0;
  background: white;
  color: #c9994b;
  font-weight: 500;
  transition: all 0.3s;
}

.reset-btn:hover {
  border-color: #c9994b;
  background: #fafafa;
}

.publish-btn {
  flex: 2;
  height: 52px;
  font-size: 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, #c9994b 0%, #d97706 50%, #b45309 100%);
  border: none;
  font-weight: 600;
  box-shadow: 0 6px 20px rgba(201, 153, 75, 0.4);
  transition: all 0.3s;
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(201, 153, 75, 0.5);
}

.guide-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.guide-modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 340px;
  overflow: hidden;
  animation: modal-in 0.3s ease-out;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.guide-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.guide-modal-title {
  font-size: 18px;
  font-weight: 600;
  color: #775029;
  margin: 0;
}

.close-btn {
  background: #f3f4f6;
  color: #6b7280;
}

.guide-modal-body {
  padding: 32px 20px;
  text-align: center;
}

.guide-step-content {
  animation: slide-in 0.3s ease-out;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.step-icon-big {
  font-size: 64px;
  margin-bottom: 16px;
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.guide-step-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 8px 0;
}

.guide-step-content p {
  font-size: 14px;
  color: #93632c;
  margin: 0;
  line-height: 1.5;
}

.guide-progress {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
}

.progress-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e5e7eb;
  transition: all 0.3s;
}

.dot-active {
  background: linear-gradient(135deg, #c9994b, #d97706);
  transform: scale(1.2);
}

.guide-modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #f3f4f6;
}

.prev-btn {
  flex: 1;
  height: 48px;
  border-radius: 12px;
  border: 2px solid #e8d0a0;
  color: #c9994b;
}

.next-btn {
  flex: 1;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #c9994b, #d97706);
  border: none;
}

.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.success-content {
  background: white;
  border-radius: 24px;
  padding: 40px 20px;
  text-align: center;
  width: 100%;
  max-width: 320px;
  animation: modal-in 0.4s ease-out;
}

.success-icon {
  font-size: 80px;
  margin-bottom: 16px;
  animation: pop 0.5s ease-out;
}

@keyframes pop {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.success-title {
  font-size: 24px;
  font-weight: 700;
  color: #775029;
  margin: 0 0 8px 0;
}

.success-desc {
  font-size: 14px;
  color: #93632c;
  margin: 0 0 20px 0;
}

.success-stars {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 24px;
}

.success-stars .star {
  font-size: 24px;
  animation: star-pop 0.5s ease-out backwards;
}

.success-stars .star:nth-child(1) { animation-delay: 0.1s; }
.success-stars .star:nth-child(2) { animation-delay: 0.2s; }
.success-stars .star:nth-child(3) { animation-delay: 0.3s; }
.success-stars .star:nth-child(4) { animation-delay: 0.4s; }
.success-stars .star:nth-child(5) { animation-delay: 0.5s; }

@keyframes star-pop {
  0% { transform: scale(0) rotate(-30deg); }
  100% { transform: scale(1) rotate(0); }
}

.success-btn {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #c9994b, #d97706);
  border: none;
  font-size: 16px;
  font-weight: 600;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>