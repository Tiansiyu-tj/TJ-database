<template>
  <el-dialog
    v-model="visible"
    :title="isEdit ? '编辑班次' : '添加班次'"
    width="420px"
    @close="handleClose"
  >
    <el-form :model="form" label-width="80px">
      <el-form-item label="线路">
        <el-select v-model="form.routeKey" :disabled="isEdit" style="width: 100%">
          <el-option label="DZ1 直达短驳" value="dz1" />
          <el-option label="北安跨线" value="beian" />
          <el-option label="822 路" value="bus822" />
          <el-option label="教职班车" value="teacher" />
        </el-select>
      </el-form-item>
      <el-form-item label="日期类型">
        <el-select v-model="form.dayType" :disabled="isEdit" style="width: 100%">
          <el-option label="工作日" value="weekday" />
          <el-option label="周末" value="weekend" />
        </el-select>
      </el-form-item>
      <el-form-item label="方向">
        <el-select v-model="form.direction" :disabled="isEdit" style="width: 100%">
          <el-option label="校区 → 地铁站" value="campusToStation" />
          <el-option label="地铁站 → 校区" value="stationToCampus" />
        </el-select>
      </el-form-item>
      <el-form-item label="发车时间">
        <el-time-select
          v-model="form.departureTime"
          start="05:00"
          step="00:05"
          end="23:55"
          placeholder="选择时间"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">
        {{ isEdit ? '保存' : '添加' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { createSchedule, updateSchedule } from '@/api/commuteApi'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  editData: Object
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isEdit = computed(() => !!props.editData?.id)
const loading = ref(false)

const form = ref({
  routeKey: 'bus822',
  dayType: 'weekday',
  direction: 'campusToStation',
  departureTime: '08:00'
})

watch(() => props.editData, (data) => {
  if (data) {
    form.value = {
      routeKey: data.routeKey || 'bus822',
      dayType: data.dayType || 'weekday',
      direction: data.direction || 'campusToStation',
      departureTime: data.departureTime || '08:00'
    }
  }
}, { immediate: true })

function handleClose() {
  visible.value = false
}

async function handleSubmit() {
  if (!form.value.departureTime) {
    ElMessage.warning('请选择发车时间')
    return
  }
  
  loading.value = true
  try {
    if (isEdit.value) {
      await updateSchedule(props.editData.id, {
        departureTime: form.value.departureTime
      })
      ElMessage.success('修改成功')
    } else {
      await createSchedule(form.value)
      ElMessage.success('添加成功')
    }
    emit('success')
    handleClose()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}
</script>
