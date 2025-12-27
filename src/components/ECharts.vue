<template>
  <div ref="chartRef" :style="{ width: width, height: height }"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  option: {
    type: Object,
    required: true
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '400px'
  },
  autoresize: {
    type: Boolean,
    default: true
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (chartRef.value && !chartInstance && props.option) {
    try {
      chartInstance = echarts.init(chartRef.value)
      if (props.option && Object.keys(props.option).length > 0) {
        chartInstance.setOption(props.option)
      }
    } catch (error) {
      console.error('ECharts 初始化失败:', error)
    }
  }
}

const updateChart = () => {
  if (chartInstance && props.option && Object.keys(props.option).length > 0) {
    try {
      chartInstance.setOption(props.option, true)
    } catch (error) {
      console.error('ECharts 更新失败:', error)
    }
  }
}

const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  initChart()
  if (props.autoresize) {
    window.addEventListener('resize', resizeChart)
  }
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (props.autoresize) {
    window.removeEventListener('resize', resizeChart)
  }
})

watch(() => props.option, updateChart, { deep: true })
</script>

