<script setup>
import { ref, computed } from 'vue'
import { useReviewStore } from '../stores/reviewStore'
import { FEELING_TAGS, PLATFORMS, getTagLabels } from '../constants/tags'
import { ArrowLeft, ArrowRight, Check } from '@element-plus/icons-vue'

const store = useReviewStore()

const step = ref(1)

const feelingTags = FEELING_TAGS
const platforms = PLATFORMS

const isTagSelected = (tagId) => store.state.selectedTags.includes(tagId)

const selectedTagLabels = computed(() => getTagLabels(store.state.selectedTags))

const shakeTagId = ref(null)

const toggleTag = (tagId) => {
  try {
    store.selectTag(tagId)
  } catch (error) {
    store.showToast(error.message, 'warning')
    shakeTagId.value = tagId
    setTimeout(() => {
      shakeTagId.value = null
    }, 400)
  }
}

const togglePlatform = (platformId) => {
  store.selectPlatform(platformId)
}

const canProceed = computed(() => {
  if (step.value === 1) return store.state.selectedTags.length > 0
  return store.state.selectedPlatform !== ''
})

const nextStep = () => {
  if (step.value === 1 && store.state.selectedTags.length === 0) {
    store.showToast('请选择至少一个感受标签', 'warning')
    return
  }
  if (step.value === 2 && !store.state.selectedPlatform) {
    store.showToast('请选择发布平台', 'warning')
    return
  }
  if (step.value === 2) {
    store.navigateTo('generate')
  } else {
    step.value++
  }
}

const prevStep = () => {
  if (step.value > 1) {
    step.value--
  } else {
    store.navigateTo('home')
  }
}
</script>

<template>
  <div class="select-page">
    <el-container>
      <el-main>
        <div class="page-content">
          <div class="page-header">
            <el-button circle @click="prevStep" class="back-btn">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <div class="title-bar">评价生成</div>
            <div class="spacer"></div>
          </div>

          <div class="steps-wrapper">
            <el-steps :active="step - 1" align-center finish-status="success" class="custom-steps">
              <el-step title="感受选择" />
              <el-step title="平台选择" />
            </el-steps>
          </div>

          <div class="content-wrapper">
            <transition name="el-fade-in-linear" mode="out-in">
              <div v-if="step === 1" key="step1" class="step-content">
                <h2 class="section-title">您的消费感受</h2>
                <p class="section-desc">选择1-2个最符合您体验的标签</p>

                <div class="tags-grid">
                  <div
                    v-for="tag in feelingTags"
                    :key="tag.id"
                    class="tag-item"
                    :class="{
                      'tag-active': isTagSelected(tag.id),
                      'tag-limit': shakeTagId === tag.id
                    }"
                    @click="toggleTag(tag.id)">
                    <span class="tag-icon">{{ tag.icon }}</span>
                    <span class="tag-label">{{ tag.label }}</span>
                  </div>
                </div>

                <el-alert
                  :title="`已选择 ${store.state.selectedTags.length} 个标签 / 最多2个`"
                  :type="store.state.selectedTags.length >= 2 ? 'success' : 'info'"
                  :closable="false"
                  class="tags-alert" />
              </div>

              <div v-else key="step2" class="step-content">
                <h2 class="section-title">选择发布平台</h2>
                <p class="section-desc">AI将根据平台风格生成评价</p>

                <div v-if="selectedTagLabels.length" class="selected-summary">
                  <span class="summary-label">已选感受</span>
                  <div class="summary-tags">
                    <span
                      v-for="label in selectedTagLabels"
                      :key="label"
                      class="summary-chip">{{ label }}</span>
                  </div>
                </div>

                <div class="platforms-list">
                  <div
                    v-for="platform in platforms"
                    :key="platform.id"
                    class="platform-item"
                    :class="{ 'platform-active': store.state.selectedPlatform === platform.id }"
                    @click="togglePlatform(platform.id)">
                    <div
                      class="platform-icon"
                      :style="{ background: platform.gradient }">
                      {{ platform.icon }}
                    </div>
                    <div class="platform-info">
                      <h3 class="platform-name">{{ platform.name }}</h3>
                      <p class="platform-desc">{{ platform.description }}</p>
                    </div>
                    <div class="platform-check" :class="{ 'check-active': store.state.selectedPlatform === platform.id }">
                      <el-icon v-if="store.state.selectedPlatform === platform.id"><Check /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <div class="action-wrapper">
            <el-button
              type="primary"
              size="large"
              class="next-btn"
              @click="nextStep"
              :disabled="!canProceed">
              {{ step === 1 ? '下一步' : '生成评价' }}
              <el-icon class="ml-2"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.select-page {
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

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.back-btn {
  flex-shrink: 0;
}

.title-bar {
  flex: 1;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: #775029;
}

.spacer {
  width: 40px;
  flex-shrink: 0;
}

.steps-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
  padding: 0 20px;
}

.custom-steps {
  width: 100%;
  max-width: 300px;
}

.content-wrapper {
  flex: 1;
  margin-bottom: 16px;
}

.step-content {
  padding: 0;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 8px 0;
  text-align: center;
}

.section-desc {
  color: #93632c;
  font-size: 14px;
  margin: 0 0 24px 0;
  text-align: center;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.tag-item {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border-radius: 12px;
  border: 2px solid #e8d0a0;
  background: white;
  transition: all 0.3s;
  cursor: pointer;
}

.tag-item:hover {
  border-color: #c9994b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(201, 153, 75, 0.2);
}

.tag-active {
  background: linear-gradient(135deg, #c9994b, #d97706);
  border-color: transparent;
  color: white;
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(201, 153, 75, 0.4);
}

.tag-item:active {
  transform: scale(0.98);
}

.tag-limit {
  animation: tag-shake 0.4s ease;
}

@keyframes tag-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.tag-icon {
  font-size: 24px;
}

.tag-label {
  font-size: 14px;
  font-weight: 500;
}

.tags-alert {
  margin-top: 16px;
}

.platforms-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.platform-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid #e8d0a0;
  background: white;
  transition: all 0.3s;
  cursor: pointer;
}

.platform-item:hover {
  border-color: #c9994b;
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(201, 153, 75, 0.2);
}

.platform-active {
  border-color: #c9994b;
  background: rgba(201, 153, 75, 0.05);
}

.platform-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.selected-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  margin-bottom: 16px;
  background: rgba(201, 153, 75, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(201, 153, 75, 0.15);
}

.summary-label {
  font-size: 12px;
  color: #93632c;
  font-weight: 500;
  flex-shrink: 0;
}

.summary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.summary-chip {
  padding: 2px 10px;
  background: white;
  border-radius: 10px;
  font-size: 12px;
  color: #c9994b;
  font-weight: 500;
}

.platform-info {
  flex: 1;
}

.platform-name {
  font-size: 16px;
  font-weight: 600;
  color: #775029;
  margin: 0 0 4px 0;
}

.platform-desc {
  font-size: 12px;
  color: #93632c;
  margin: 0;
}

.platform-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #e8d0a0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  transition: all 0.3s;
  flex-shrink: 0;
}

.check-active {
  background: #c9994b;
  border-color: #c9994b;
  color: white;
}

.action-wrapper {
  padding: 16px 0;
  margin-top: auto;
}

.next-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, #c9994b, #d97706);
  border: none;
}

.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(201, 153, 75, 0.4);
}

.next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.ml-2 {
  margin-left: 8px;
}
</style>