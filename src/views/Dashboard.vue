<template>
  <div class="dashboard-container">
    <el-container>
      <!-- 头部导航 -->
      <el-header class="dashboard-header">
        <div class="header-left">
          <el-icon class="header-icon" :size="30" color="#409EFF">
            <Location />
          </el-icon>
          <h2>上海地铁交通系统</h2>
        </div>
        <div class="header-right">
          <el-text class="username-text">
            <el-icon><User /></el-icon>
            {{ username }}
          </el-text>
          <el-button type="primary" :icon="Location" @click="goToRoutePlanner" style="margin-right: 10px">
            地铁导航
          </el-button>
          <el-button type="success" :icon="Guide" @click="goToCommute">
            嘉定推荐
          </el-button>
          <el-button type="danger" :icon="SwitchButton" @click="handleLogout">
            退出登录
          </el-button>
        </div>
      </el-header>

      <!-- 主要内容区域 -->
      <el-main class="dashboard-main">
        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stats-row">
          <el-col :xs="24" :sm="12" :md="6" v-for="(stat, index) in statsData" :key="index">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-icon" :style="{ background: stat.color }">
                  <el-icon :size="28">
                    <component :is="stat.icon" />
                  </el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图表区域 -->
        <el-row :gutter="20" class="charts-row">
          <!-- 实时流量趋势 -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>实时流量趋势</span>
                  <el-tag type="success" size="small">实时更新</el-tag>
                </div>
              </template>
              <ECharts :option="lineChartOption" height="300px" />
            </el-card>
          </el-col>

          <!-- 站点流量排名 -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>站点流量排名 TOP 10</span>
                </div>
              </template>
              <ECharts :option="barChartOption" height="300px" />
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="charts-row">
          <!-- 线路流量分布 -->
          <el-col :xs="24" :lg="12" class="equal-height-col">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>线路流量分布</span>
                </div>
              </template>
              <ECharts :option="pieChartOption" height="350px" />
            </el-card>
          </el-col>

          <!-- 天气信息展示 -->
          <el-col :xs="24" :lg="12" class="equal-height-col">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>今日天气信息</span>
                  <el-tag type="success" size="small">实时数据</el-tag>
                </div>
              </template>

            <div v-if="!todayWeather" class="weather-empty">暂无天气数据</div>
            <div class="echarts-wrapper" v-else>
              <ECharts :option="weatherChartOption" height="300px" />
            </div>
            </el-card>
        </el-col>
        </el-row>

        <!-- OD流量分析（起终点站） -->
        <el-row :gutter="20" class="charts-row">
          <el-col :xs="24" :lg="24">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>OD流量分析 - 热门起终点站</span>
                </div>
              </template>
              <ECharts :option="odChartOption" height="400px" />
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="charts-row">
          <!-- 进站流量分类（总流量/通勤/居家/非居家） -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>进站流量分类统计</span>
                </div>
              </template>
              <ECharts :option="inflowCategoryOption" height="350px" />
            </el-card>
          </el-col>

          <!-- 出站流量分类（总流量/通勤/居家/非居家） -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>出站流量分类统计</span>
                </div>
              </template>
              <ECharts :option="outflowCategoryOption" height="350px" />
            </el-card>
          </el-col>
        </el-row>

        <!-- 地铁线路列表 -->
        <el-card class="table-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>地铁站点详情</span>
            </div>
          </template>
          <el-table
            :data="paginatedStations"
            stripe
            style="width: 100%"
            :default-sort="{ prop: 'flow', order: 'descending' }"
          >
            <el-table-column prop="id" label="站点ID" width="120">
              <template #default="{ row }">
                <el-tag :type="row.tagType" size="large">{{ row.id }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="站点名称" />
            <el-table-column prop="longitude" label="经度(°)" width="120" align="center" />
            <el-table-column prop="latitude" label="纬度(°)" width="120" align="center" />
            <el-table-column prop="flow" label="今日流量(人次)" width="160" sortable align="right">
              <template #default="{ row }">
                <el-text type="primary" size="large">{{ row.flow }}</el-text>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="运行状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === '正常' ? 'success' : 'warning'">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <el-button type="primary" link :icon="View" @click="viewDetails(row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            background
            layout="prev, pager, next"
            :total="allStationsData.length"
            :page-size="pageSize"
            :current-page="currentPage"
            @current-change="handlePageChange"
            style="margin-top: 16px; text-align: center;"
          />
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ECharts from '@/components/ECharts.vue'
import {
  Location,
  User,
  SwitchButton,
  Refresh,
  View,
  UserFilled,
  TrendCharts,
  Connection,
  Guide,
  Sunny,
  Cloudy
} from '@element-plus/icons-vue'

// 从 shanghaiMetroApi 获取动态数据
import {
  fetchStations,
  fetchTimeSegmentsByDate,
  fetchInflowBySlot,
  fetchOutflowBySlot,
  fetchODFlowBySlot,
  fetchWeather,
  fetchInflowAggregate,
  fetchTopOD
} from '@/api/shanghaiMetroApi'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '管理员')

// 指定测试日期（用于调试/验证，格式 YYYY-MM-DD）。设置为 null 表示使用当日或数据库中最新可用日期。
const TEST_METRO_DATE = '2017-06-10'
// 开发时自动登录（仅用于本地调试）。上线前请移除或置为 false
const DEV_AUTO_LOGIN = true

// 统计数据（通过 API 填充）
const stations = ref([])
const currentSlot = ref(null)

// 辅助：兼容 StartTime/EndTime 为 'HH:MM' 或 秒数（如 21600.0）或数值/字符串
const slotHour = (s) => {
  if (s == null) return null
  // s can be a slot object or a raw value
  const v = (typeof s === 'object') ? (s.StartTime ?? s.Start) : s
  if (v == null) return null
  const sv = String(v)
  if (sv.includes(':')) {
    const h = parseInt(sv.split(':')[0], 10)
    return Number.isFinite(h) ? h : null
  }
  const n = Number(sv)
  if (!isNaN(n)) {
    // if given in seconds (e.g., 21600), convert to hour
    if (n > 1000) return Math.floor(n / 3600)
    return Math.floor(n)
  }
  return null
}

const slotLabel = (s) => {
  const h = slotHour(s)
  return h != null ? `${h}:00` : '—'
}

// 将天气记录的 recordTime（秒或 HH:MM）转换为标签
const weatherLabel = (w) => {
  const t = (w && (w.recordTime ?? w.time)) ?? null
  if (t == null) return '—'
  const hh = slotHour({ StartTime: t })
  return hh != null ? `${hh}:00` : String(t)
}

const statsData = ref([
  {
    icon: UserFilled,
    label: '本时段客流',
    value: '—',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: TrendCharts,
    label: '活跃站点',
    value: '—',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    icon: Connection,
    label: '监测站点',
    value: '—',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    icon: Guide,
    label: '总站点数',
    value: '—',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  }
])

// 地铁线路数据（由站点/流量计算而来）
const allStationsData = ref([])  // 存储所有站点数据
const currentPage = ref(1)
const pageSize = ref(10)  // 每页显示10条数据

// 添加计算属性来获取当前页的数据
const paginatedStations = computed(() => {
  // 先对所有站点数据按流量降序排序
  const sortedStations = [...allStationsData.value].sort((a, b) => b.flow - a.flow)
  // 然后进行分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return sortedStations.slice(start, end)
})

const metroLines = computed(() => paginatedStations.value)

// 实时流量趋势图
const lineChartOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
  legend: {
    data: ['进站流量', '出站流量']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: []
  },
  yAxis: {
    type: 'value',
    name: '人次/小时',
    axisLabel: { formatter: (value) => Number(value).toLocaleString() }
  },
  series: [
    {
      name: '进站流量',
      type: 'line',
      smooth: true,
      data: [],
      itemStyle: { color: '#409EFF' },
      areaStyle: { color: 'rgba(64, 158, 255, 0.2)' }
    },
    {
      name: '出站流量',
      type: 'line',
      smooth: true,
      data: [],
      itemStyle: { color: '#67C23A' },
      areaStyle: { color: 'rgba(103, 194, 58, 0.2)' }
    }
  ]
})

// 站点流量排名
const barChartOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '8%',  // 增加右边距，为Y轴标签提供更多空间
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '人次',
    axisLabel: { formatter: (value) => Number(value).toLocaleString() }
  },
  yAxis: {
    type: 'category',
    data: [],
    axisLabel: {
      interval: 0,
      fontSize: 12  // 可选：调整字体大小以适应更多文字
    }
  },
  series: [
    {
      type: 'bar',
      data: [],
      itemStyle: {
        color: '#409EFF'
      }
    }
  ]
})

// 线路流量分布饼图
const pieChartOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    top: 'middle'
  },
  series: [
    {
      name: '流量分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '16',
          fontWeight: 'bold'
        }
      },
      data: []
    }
  ]
})

// 时段流量分析 已移除（按需求）


// 天气信息图表
const weatherChartOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
  legend: {
    data: ['温度(°C)', '降雨量(mm/h)', '风速(km/h)']
  },
  grid: {
    left: '3%',
    right: '8%',  // 增加右边距，为Y轴标签提供更多空间
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: []
  },
  yAxis: [
    {
      type: 'value',
      name: '温度(°C)',
      position: 'left',
      axisLabel: {
        formatter: '{value} °C'
      }
    },
    {
      type: 'value',
      name: '降雨量/风速',
      position: 'right',
      axisLabel: {
        formatter: '{value}'
      }
    }
  ],
  series: [
    {
      name: '温度(°C)',
      type: 'line',
      smooth: true,
      data: [],
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '降雨量(mm/h)',
      type: 'bar',
      yAxisIndex: 1,
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '风速(km/h)',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      data: [],
      itemStyle: { color: '#67C23A' }
    }
  ]
})

// 当日天气概要（温度/降雨/风速）
const todayWeather = ref(null)

// 流量分类分析 已移除（按需求）


// OD流量分析图表（起终点站）
const odChartOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      return `${params.seriesName}<br/>${params.name}<br/>流量: ${Number(params.value).toLocaleString()} 人次 (${params.percent}%)`
    }
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    top: 'middle'
  },
  series: [
    {
      name: 'OD流量',
      type: 'pie',
      radius: ['30%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: function(params) { return `${params.name}: ${Number(params.value).toLocaleString()} 人次\n(${params.percent}%)` }
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '14',
          fontWeight: 'bold'
        }
      },
      data: []
    }
  ]
})

// 进站流量分类统计（仅三类：通勤/居家/非居家）
const inflowCategoryOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['通勤进站(C_IF)', '居家进站(HB_IF)', '非居家进站(NHB_IF)']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: []
  },
  yAxis: {
    type: 'value',
    name: '人次',
    axisLabel: { formatter: (value) => Number(value).toLocaleString() }
  },
  series: [
    {
      name: '通勤进站(C_IF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '居家进站(HB_IF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '非居家进站(NHB_IF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#E6A23C' }
    }
  ]
})

// 出站流量分类统计（仅三类：通勤/居家/非居家）
const outflowCategoryOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['通勤出站(C_OF)', '居家出站(HB_OF)', '非居家出站(NHB_OF)']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: []
  },
  yAxis: {
    type: 'value',
    name: '人次',
    axisLabel: { formatter: (value) => Number(value).toLocaleString() }
  },
  series: [
    {
      name: '通勤出站(C_OF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '居家出站(HB_OF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '非居家出站(NHB_OF)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      smooth: true,
      data: [],
      itemStyle: { color: '#E6A23C' }
    }
  ]
})

// 初始化图表数据
const initChartData = async () => {
  try {
    // 通过 API 获取当日时段与站点流量
    const today = new Date().toISOString().slice(0, 10) // YYYY-MM-DD

    // 站点列表
    stations.value = await fetchStations().catch(() => [])
    statsData.value[3].value = `${stations.value.length}个`

    // 获取当日时间段并筛选 5:00-23:00 槽
    // 若设置了 TEST_METRO_DATE，则优先使用该日期
    let usedDate = TEST_METRO_DATE || today
    let segments = await fetchTimeSegmentsByDate(usedDate).catch(() => [])
    let slots = (segments || []).filter(s => {
      const hour = slotHour(s)
      if (hour == null) return false
      return hour >= 6 && hour <= 23  // 修改：从6点开始到23点结束
    }).sort((a, b) => (slotHour(a) || 0) - (slotHour(b) || 0))

    // 如果没有 segments（例如当天或 TEST_METRO_DATE 无数据），不再自动回退到其他日期（已移除 fallback 模式）
    if (!slots.length) {
      console.warn('initChartData: no slots for', usedDate)
      ElMessage.warning('当天无可用时段数据；请检查所选日期或稍后重试')
      // 清空主要图表数据并返回
      lineChartOption.value.xAxis.data = []
      lineChartOption.value.series[0].data = []
      lineChartOption.value.series[1].data = []

      barChartOption.value.yAxis.data = []
      barChartOption.value.series[0].data = []

      pieChartOption.value.series[0].data = []



      weatherChartOption.value.xAxis.data = []
      weatherChartOption.value.series[0].data = []
      weatherChartOption.value.series[1].data = []
      weatherChartOption.value.series[2].data = []

      odChartOption.value.series[0].data = []

      inflowCategoryOption.value.series[0].data = []
      inflowCategoryOption.value.series[1].data = []
      inflowCategoryOption.value.series[2].data = []

      outflowCategoryOption.value.series[0].data = []
      outflowCategoryOption.value.series[1].data = []
      outflowCategoryOption.value.series[2].data = []

      statsData.value.forEach(stat => {
        stat.value = '—'
      })

      metroLines.value = []
      todayWeather.value = null
      return
    }

    // 仍然没有时段则回退到随机生成（保持原体验）
    if (!slots.length) {
      fallbackInitData()
      return
    }

    // 并行获取每个 slot 的进出站数据（仅取一定数量以免请求过多）
    const now = new Date()
    const currentSlotIdx = slots.findIndex(s => {
      const sh = slotHour(s)
      let eh = slotHour({ StartTime: s.EndTime })
      if (eh == null && sh != null) eh = sh + 1
      const ch = now.getHours()
      return sh != null && eh != null && ch >= sh && ch < eh
    })

    // 修改：不再以当前时间为限制，而是使用全部6:00-23:00的slots
    // 原代码：
    // const useSlots = currentSlotIdx >= 0 ? slots.slice(0, currentSlotIdx + 1) : slots
    const useSlots = slots // 使用所有符合条件的slots（6:00-23:00）

    const inflowPromises = useSlots.map(s => fetchInflowBySlot(s.Slot).then(data => ({ slot: s, data })).catch(() => ({ slot: s, data: [] })))
    const outflowPromises = useSlots.map(s => fetchOutflowBySlot(s.Slot).then(data => ({ slot: s, data })).catch(() => ({ slot: s, data: [] })))

    const inflowResults = await Promise.all(inflowPromises)
    const outflowResults = await Promise.all(outflowPromises)

    // 构造时间序列与系列数据
    const hours = useSlots.map(s => slotLabel(s))
    const inFlowSeries = inflowResults.map(r => r.data.reduce((sum, it) => sum + (it.Tot_IF || it.tot_if || 0), 0))
    const outFlowSeries = outflowResults.map(r => r.data.reduce((sum, it) => sum + (it.Tot_OF || it.tot_of || 0), 0))

    lineChartOption.value.xAxis.data = hours
    lineChartOption.value.series[0].data = inFlowSeries
    lineChartOption.value.series[1].data = outFlowSeries

    // 当前 slot（最后一个）统计
    const lastInTotal = inFlowSeries.length ? inFlowSeries[inFlowSeries.length - 1] : 0
    const activeStations = inflowResults.length ? inflowResults[inflowResults.length - 1].data.filter(s => (s.Tot_IF || s.tot_if || 0) > 0).length : 0
    statsData.value[0].value = lastInTotal >= 10000 ? `${(lastInTotal / 10000).toFixed(1)}万` : `${lastInTotal}`
    statsData.value[1].value = `${activeStations}个`
    statsData.value[2].value = `${stations.value.length ? Math.max(1, Math.round(stations.value.length / 10)) : '—'}条` // 简单近似线路数

    // 站点排名（基于当前 slot 的进站）
    // 修改：改为基于所有时间段的总进站流量进行排名
    // 原代码：
    // const currInflow = inflowResults.length ? inflowResults[inflowResults.length - 1].data : []
    // 使用站点ID获取对应站点名称
    // const topStations = (currInflow || []).map(s => {
    //   // 尝试获取站点名称，如果不存在则使用ID
    //   const station = stations.value.find(st => st.stationID === s.stationID || st.id === s.stationID)
    //   const name = station ? (station.name || station.stationName || station.stationID) : (s.stationName || s.stationID || '未知')
    //   return { 
    //     name: name.trim(), 
    //     flow: (s.Tot_IF || s.tot_if || 0),
    //     stationID: s.stationID
    //   }
    // }).sort((a, b) => b.flow - a.flow).slice(0, 10)
    
    // 计算所有时间段的站点总流量
    const totalInflowByStationForTopStations = new Map()
    for (const result of inflowResults) {
      for (const item of result.data) {
        const stationID = item.stationID
        const flow = (item.Tot_IF || item.tot_if || 0)
        if (totalInflowByStationForTopStations.has(stationID)) {
          totalInflowByStationForTopStations.set(stationID, totalInflowByStationForTopStations.get(stationID) + flow)
        } else {
          totalInflowByStationForTopStations.set(stationID, flow)
        }
      }
    }
    
    // 转换为数组并排序，获取TOP 10，用于站点排名图表
    const allStationsTotal = Array.from(totalInflowByStationForTopStations.entries()).map(([stationID, flow]) => {
      const station = stations.value.find(st => st.stationID === stationID || st.id === stationID)
      const name = station ? (station.name || station.stationName || station.stationID) : `站点${stationID}`
      return { 
        name: name.trim(), 
        flow: flow,
        stationID: stationID
      }
    }).sort((a, b) => b.flow - a.flow)
    
    // 更新站点排名图表数据（取TOP 10）
    if (allStationsTotal.length) {
      barChartOption.value.yAxis.data = allStationsTotal.slice(0, 10).map(s => s.name).reverse()
      barChartOption.value.series[0].data = allStationsTotal.slice(0, 10).map(s => s.flow).reverse()
    }

    // 线路流量分布 - 以站点聚合近似展示（取 Top 6 站点占比）
    const topLines = allStationsTotal.slice(0, 6).map(s => ({ value: s.flow, name: s.name }))
    pieChartOption.value.series[0].data = topLines

    // 时段流量（工作日/周末）及分类统计（基于所有已拉取的 slots）
    const workdayFlow = []
    const weekendFlow = []


    // 进站流量分类统计和出站流量分类统计数据
    const inflowCategoryTimes = []
    const inflowCommuter = []
    const inflowHome = []
    const inflowNonHome = []
    
    const outflowCommuter = []
    const outflowHome = []
    const outflowNonHome = []

    for (let i = 0; i < useSlots.length; i++) {
      const s = useSlots[i]
      const inflows = inflowResults[i].data
      const outflows = outflowResults[i].data
      const cSum = inflows.reduce((sum, it) => sum + (it.C_IF || it.c_if || 0), 0)
      const hbSum = inflows.reduce((sum, it) => sum + (it.HB_IF || it.hb_if || 0), 0)
      const nhbSum = inflows.reduce((sum, it) => sum + (it.NHB_IF || it.nhb_if || 0), 0)

      // 计算总进站流量用于工作日/周末判断
      const totalIn = inflows.reduce((sum, it) => sum + (it.Tot_IF || it.tot_if || 0), 0)

      // 进站分类数据
      inflowCategoryTimes.push(slotLabel(s))
      inflowCommuter.push(cSum)
      inflowHome.push(hbSum)
      inflowNonHome.push(nhbSum)

      // 出站分类数据
      const cSumOut = outflows.reduce((sum, it) => sum + (it.C_OF || it.c_of || 0), 0)
      const hbSumOut = outflows.reduce((sum, it) => sum + (it.HB_OF || it.hb_of || 0), 0)
      const nhbSumOut = outflows.reduce((sum, it) => sum + (it.NHB_OF || it.nhb_of || 0), 0)
      
      outflowCommuter.push(cSumOut)
      outflowHome.push(hbSumOut)
      outflowNonHome.push(nhbSumOut)

      // 简易区分 weekday/weekend（依赖于 DateInfo 在后端）
      // 若后端没有 weekday 标记，这里将数据都放到工作日系列（作为降级方案）
      workdayFlow.push(totalIn)
      weekendFlow.push(0)
    }



    // 进站流量分类统计图表数据（仅三类）
    inflowCategoryOption.value.xAxis.data = inflowCategoryTimes
    inflowCategoryOption.value.series[0].data = inflowCommuter
    inflowCategoryOption.value.series[1].data = inflowHome
    inflowCategoryOption.value.series[2].data = inflowNonHome

    // 出站流量分类统计图表数据（仅三类，使用相同的时间轴）
    outflowCategoryOption.value.xAxis.data = inflowCategoryTimes
    outflowCategoryOption.value.series[0].data = outflowCommuter
    outflowCategoryOption.value.series[1].data = outflowHome
    outflowCategoryOption.value.series[2].data = outflowNonHome

    // 天气（尝试拉取用于展示的日期天气，可能是当天或最近可用日期）
    let weatherData = await fetchWeather(usedDate).catch(() => [])
    console.info('initChartData: fetched weather for', usedDate, 'count=', weatherData ? weatherData.length : 0)
    if (!weatherData || !weatherData.length) {
      // 尝试回退到最近可用的天气记录（不带日期参数）
      const fallbackWeather = await fetchWeather(null, null, 100).catch(() => [])
      if (fallbackWeather && fallbackWeather.length) {
        console.info('initChartData: no weather for', usedDate, 'falling back to latest available, count=', fallbackWeather.length)
        weatherData = fallbackWeather
        // 标记来源日期以便在 UI 中提示
        var weatherSourceDate = (weatherData && weatherData.length && weatherData[0].recordDate) ? weatherData[0].recordDate : null
      }
    }

    if (weatherData && weatherData.length) {
      // 按时间排序，确保从0点开始的完整时间序列
      const sortedWeatherData = [...weatherData].sort((a, b) => {
        const timeA = Number(a.recordTime || 0)
        const timeB = Number(b.recordTime || 0)
        return timeA - timeB
      })
      
      const weatherTimes = sortedWeatherData.map(w => weatherLabel(w))
      weatherChartOption.value.xAxis.data = weatherTimes
      weatherChartOption.value.series[0].data = sortedWeatherData.map(w => Number(w.temperature_2m || 0))
      weatherChartOption.value.series[1].data = sortedWeatherData.map(w => Number(w.rain || 0))
      weatherChartOption.value.series[2].data = sortedWeatherData.map(w => Number(w.wind_speed_10m || 0))

      // 使用最新时间的天气记录作为今日概要（若 recordTime 为秒数也可处理）
      const latest = sortedWeatherData.reduce((a, b) => (Number(a.recordTime || 0) >= Number(b.recordTime || 0) ? a : b))
      todayWeather.value = {
        temp: Number(latest.temperature_2m || latest.temperature || null),
        rain: Number(latest.rain || 0),
        wind: Number(latest.wind_speed_10m || latest.wind_speed || 0),
        timeLabel: weatherLabel(latest),
        sourceDate: weatherSourceDate || (latest.recordDate || null)
      }
    } else {
      todayWeather.value = null
    }

    // OD 流量 Top（使用最近 slot）
    if (useSlots.length) {
      const lastSlotId = useSlots[useSlots.length - 1].Slot
      const topOD = await fetchTopOD(lastSlotId, 10).catch(() => [])
      if (topOD && topOD.length) {
        odChartOption.value.series[0].data = topOD.map(item => {
          // 获取起始站点和终点站的名称
          const originStation = stations.value.find(st => st.id === item.O_Station)
          const destStation = stations.value.find(st => st.id === item.D_Station)

          const originName = String(originStation?.name || item.O_Station || '未知').trim()
          const destName = String(destStation?.name || item.D_Station || '未知').trim()
          
          return { 
            name: `${originName} → ${destName}`, 
            value: item.Tot_F || item.tot_f || 0 
          }
        })
      }
    }

    // Metro lines 表格 - 使用与站点排名相同的计算逻辑，确保数据一致性
    const newMetroLines = stations.value.map(station => {
      const stationFlow = totalInflowByStationForTopStations.get(station.id || station.stationID) || 0
      const stationName = station.name || `站点 ${station.id || station.stationID}`
      return {
        id: station.id || station.stationID,
        name: stationName,
        longitude: station.lon,  // 添加经度数据
        latitude: station.lat,   // 添加纬度数据
        stations: 1,
        flow: stationFlow,  // 使用计算的流量而不是原始数据
        status: stationFlow && stationFlow > 0 ? '正常' : '待检测',
        tagType: stationFlow > 0 ? 'primary' : 'info'
      }
    })
    
    allStationsData.value = newMetroLines  // 存储所有站点数据
    currentPage.value = 1  // 重置为第一页

  } catch (err) {
    console.error('initChartData: API 获取失败', err)
    ElMessage.error('数据加载失败，请检查网络连接或稍后重试')
    
    // 清空所有图表数据
    lineChartOption.value.xAxis.data = []
    lineChartOption.value.series[0].data = []
    lineChartOption.value.series[1].data = []
    
    barChartOption.value.yAxis.data = []
    barChartOption.value.series[0].data = []
    
    pieChartOption.value.series[0].data = []
    

    
    weatherChartOption.value.xAxis.data = []
    weatherChartOption.value.series[0].data = []
    weatherChartOption.value.series[1].data = []
    weatherChartOption.value.series[2].data = []
    
    odChartOption.value.series[0].data = []
    
    inflowCategoryOption.value.series[0].data = []
    inflowCategoryOption.value.series[1].data = []
    inflowCategoryOption.value.series[2].data = []
    
    outflowCategoryOption.value.series[0].data = []
    outflowCategoryOption.value.series[1].data = []
    outflowCategoryOption.value.series[2].data = []
    
    statsData.value.forEach(stat => {
      stat.value = '—'
    })
    
    metroLines.value = []
    todayWeather.value = null
  }
}

// 回退用的随机初始化（保留原有随机逻辑，供 API 不可用时使用）
const fallbackInitData = () => {
  // 保留原脚本中生成随机数据的行为（仅截取与展示相关的核心段）
  const hours = []
  const inFlow = []
  const outFlow = []
  const now = new Date()
  const currentHour = now.getHours()
  let startHour = 5
  let endHour = currentHour >= 23 ? 23 : (currentHour < 5 ? 23 : currentHour)
  for (let hour = startHour; hour <= endHour; hour++) {
    hours.push(`${hour}:00`)
    let baseFlow = 80
    if (hour >= 7 && hour <= 9) baseFlow = 140
    else if (hour >= 17 && hour <= 19) baseFlow = 130
    else if (hour >= 5 && hour <= 6) baseFlow = 50
    else if (hour >= 21 && hour <= 23) baseFlow = 60
    inFlow.push(Math.floor(Math.random() * 30) + baseFlow)
    outFlow.push(Math.floor(Math.random() * 30) + baseFlow)
  }
  lineChartOption.value.xAxis.data = hours
  lineChartOption.value.series[0].data = inFlow
  lineChartOption.value.series[1].data = outFlow

  // 站点排名回退
  const topStations = [
    { name: '人民广场', flow: 89.5 },
    { name: '徐家汇', flow: 76.3 },
    { name: '陆家嘴', flow: 72.1 },
    { name: '静安寺', flow: 68.9 },
    { name: '南京东路', flow: 65.4 },
    { name: '世纪大道', flow: 61.2 },
    { name: '中山公园', flow: 58.7 },
    { name: '虹桥火车站', flow: 55.3 },
    { name: '上海南站', flow: 52.1 },
    { name: '上海火车站', flow: 48.9 }
  ]
  barChartOption.value.yAxis.data = topStations.map(s => s.name).reverse()
  barChartOption.value.series[0].data = topStations.map(s => s.flow).reverse()

  // 保持饼图和其他图的原随机数据逻辑
  const topLines = [
    { value: 156.8, name: '1号线' },
    { value: 189.2, name: '2号线' },
    { value: 142.5, name: '3号线' },
    { value: 135.6, name: '4号线' },
    { value: 98.3, name: '5号线' },
    { value: 126.4, name: '6号线' }
  ]
  pieChartOption.value.series[0].data = topLines

  // 进/出站、OD 与分类的回退逻辑将在下方统一生成（避免重复声明）

  // OD流量分析数据（热门起终点站）
  const topODPairs = [
    { name: '人民广场 → 陆家嘴', value: 45.2 },
    { name: '徐家汇 → 人民广场', value: 38.6 },
    { name: '虹桥火车站 → 人民广场', value: 35.4 },
    { name: '静安寺 → 南京东路', value: 32.1 },
    { name: '上海南站 → 人民广场', value: 28.9 },
    { name: '陆家嘴 → 世纪大道', value: 26.7 },
    { name: '南京东路 → 人民广场', value: 24.3 },
    { name: '中山公园 → 徐家汇', value: 22.1 },
    { name: '世纪大道 → 陆家嘴', value: 19.8 },
    { name: '其他', value: 156.9 }
  ]
  odChartOption.value.series[0].data = topODPairs

  odChartOption.value.series[0].data = topODPairs

  // 进站流量分类统计（TOP 10站点）
  const topStationsList = ['人民广场', '徐家汇', '陆家嘴', '静安寺', '南京东路', '世纪大道', '中山公园', '虹桥火车站', '上海南站', '上海火车站']
  const inflowTot = [] // 总进站流量
  const inflowC = [] // 通勤进站
  const inflowHB = [] // 居家进站
  const inflowNHB = [] // 非居家进站
  topStationsList.forEach(() => {
    const tot = Math.floor(Math.random() * 50 + 60) // 60-110
    inflowTot.push(tot)
    inflowC.push(Math.floor(tot * 0.45)) // 45%通勤
    inflowHB.push(Math.floor(tot * 0.30)) // 30%居家
    inflowNHB.push(Math.floor(tot * 0.25)) // 25%非居家
  })
  inflowCategoryOption.value.xAxis.data = topStationsList
  inflowCategoryOption.value.series[0].data = inflowC
  inflowCategoryOption.value.series[1].data = inflowHB
  inflowCategoryOption.value.series[2].data = inflowNHB

  // 出站流量分类统计（TOP 10站点）
  const outflowC = [] // 通勤出站
  const outflowHB = [] // 居家出站
  const outflowNHB = [] // 非居家出站
  topStationsList.forEach(() => {
    const tot = Math.floor(Math.random() * 50 + 60) // 60-110
    outflowC.push(Math.floor(tot * 0.45)) // 45%通勤
    outflowHB.push(Math.floor(tot * 0.30)) // 30%居家
    outflowNHB.push(Math.floor(tot * 0.25)) // 25%非居家
  })
  outflowCategoryOption.value.xAxis.data = topStationsList
  outflowCategoryOption.value.series[0].data = outflowC
  outflowCategoryOption.value.series[1].data = outflowHB
  outflowCategoryOption.value.series[2].data = outflowNHB
}

const goToRoutePlanner = () => {
  router.push('/route-planner')
}

const goToCommute = () => {
  router.push('/commute')
}

const handleLogout = () => {
  localStorage.removeItem('isAuthenticated')
  localStorage.removeItem('username')
  ElMessage.success('已退出登录')
  router.push('/login')
}

const refreshData = async () => {
  try {
    await initChartData()
    ElMessage.success('数据已刷新')
  } catch (err) {
    console.error('刷新失败:', err)
    ElMessage.error('数据刷新失败，请检查网络连接或稍后重试')
  }
}

const viewDetails = (row) => {
  ElMessage.info(`查看 ${row.name} 的详细信息`)
}

const handlePageChange = (page) => {
  currentPage.value = page
}

onMounted(() => {
  try {
    // 开发自动登录（仅本地调试）
    if (DEV_AUTO_LOGIN) {
      try {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('username', '开发测试')
        username.value = '开发测试'
        console.info('DEV_AUTO_LOGIN active: auto-authenticated as 开发测试')
      } catch (e) {
        // ignore localStorage errors in non-browser env
      }
    }

    // 初始化并开始周期性更新
    initChartData()
  } catch (error) {
    console.error('Dashboard 初始化失败:', error)
    ElMessage.error('页面初始化失败，请检查网络连接或稍后重试')
  }
})

onUnmounted(() => {
})
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  min-height: 100vh;
  background:
    radial-gradient(circle at 15% 10%, rgba(102, 126, 234, 0.14), transparent 28%),
    radial-gradient(circle at 85% 20%, rgba(118, 75, 162, 0.16), transparent 30%),
    linear-gradient(135deg, #f7f9ff 0%, #eef2ff 40%, #f9fbff 100%);
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 28px;
  box-shadow: 0 12px 32px rgba(31, 41, 55, 0.08);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 20;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  animation: rotate 18s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.header-left h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username-text {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(64, 158, 255, 0.08);
  border: 1px solid rgba(64, 158, 255, 0.16);
}

.dashboard-main {
  padding: 22px;
  overflow-y: auto;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  border-radius: 16px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
  border: 1px solid #eef0f6;
  background: linear-gradient(145deg, #ffffff, #f6f7fb);
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 28px 65px rgba(31, 41, 55, 0.12);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 16px;
  margin-bottom: 20px;
  border: 1px solid #eef0f6;
  background: #ffffff;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  font-size: 16px;
  color: #0f172a;
}

.today-weather-summary {
  padding: 12px 8px 4px 8px;
  border-bottom: 1px dashed #eef0f6;
  margin-bottom: 8px;
}
.weather-summary-row {
  align-items: center;
}
.weather-item {
  text-align: center;
}
.weather-value {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}
.weather-label {
  font-size: 12px;
  color: #6b7280;
}
.weather-time {
  margin-top: 6px;
  font-size: 12px;
  color: #8b8f98;
}
.weather-empty {
  padding: 24px;
  text-align: center;
  color: #9aa0a6;
  font-size: 14px;
}

.chart-card .el-card__body {
  display: flex;
  flex-direction: column;
}

.echarts-wrapper {
  margin-top: 8px;
  flex: 1 1 auto;
}

.table-card {
  border-radius: 16px;
  border: 1px solid #eef0f6;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
}

.equal-height-col {
  display: flex;
}

.equal-height-col .chart-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px; /* 设置最小高度确保统一 */
}

.equal-height-col .el-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    height: auto;
    padding: 15px;
    gap: 15px;
  }

  .header-left h2 {
    font-size: 20px;
  }

  .dashboard-main {
    padding: 15px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>