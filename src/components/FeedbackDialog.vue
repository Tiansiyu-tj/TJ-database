<template>
  <el-dialog
    v-model="visible"
    title="拥挤度反馈"
    width="380px"
    @close="handleClose"
  >
    <div class="feedback-content">
      <p class="feedback-tip">请根据您的实际体验，反馈当前时段的拥挤程度：</p>
      
      <div class="line-info">
        <el-tag :type="lineId === '11' ? 'danger' : 'success'">
          {{ lineId }}号线
        </el-tag>
        <span class="hour-label">{{ hour }}:00 - {{ hour + 1 }}:00</span>
      </div>
      
      <div class="level-options">
        <div
          v-for="level in levels"
          :key="level.value"
          class="level-item"
          :class="{ active: selectedLevel === level.value }"
          @click="selectedLevel = level.value"
        >
          <span class="level-icon">{{ level.icon }}</span>
          <span class="level-text">{{ level.label }}</span>
        </div>
      </div>
    </div>
    
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">
        提交反馈
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { submitCongestionFeedback } from '@/api/commuteApi'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  lineId: String,
  hour: Number
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const loading = ref(false)
const selectedLevel = ref('normal')

const levels = [
  { value: 'empty', label: '空闲', icon: '😊' },
  { value: 'normal', label: '正常', icon: '🙂' },
  { value: 'crowded', label: '拥挤', icon: '😓' },
  { value: 'packed', label: '爆满', icon: '😰' }
]

function handleClose() {
  visible.value = false
  selectedLevel.value = 'normal'
}

async function handleSubmit() {
  loading.value = true
  try {
    await submitCongestionFeedback(props.lineId, props.hour, selectedLevel.value)
    ElMessage.success('感谢您的反馈！')
    emit('success')
    handleClose()
  } catch (e) {
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.feedback-content {
  padding: 10px 0;
}

.feedback-tip {
  color: #606266;
  margin-bottom: 16px;
}

.line-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.hour-label {
  color: #303133;
  font-weight: 600;
}

.level-options {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.level-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  border: 2px solid #e4e7ed;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.level-item:hover {
  border-color: #409eff;
}

.level-item.active {
  border-color: #409eff;
  background: #ecf5ff;
}

.level-icon {
  font-size: 28px;
  margin-bottom: 6px;
}

.level-text {
  font-size: 12px;
  color: #606266;
}
</style>
