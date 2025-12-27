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
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>线路流量分布</span>
                </div>
              </template>
              <ECharts :option="pieChartOption" height="350px" />
            </el-card>
          </el-col>

          <!-- 时段流量分析 (5点-23点) -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>时段流量分析 (5:00-23:00)</span>
                </div>
              </template>
              <ECharts :option="areaChartOption" height="350px" />
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="charts-row">
          <!-- 天气信息展示 -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>今日天气信息</span>
                  <el-tag type="info" size="small">实时数据</el-tag>
                </div>
              </template>
              <ECharts :option="weatherChartOption" height="300px" />
            </el-card>
          </el-col>

          <!-- 流量分类分析（通勤/居家/非居家） -->
          <el-col :xs="24" :lg="12">
            <el-card class="chart-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>流量分类分析</span>
                </div>
              </template>
              <ECharts :option="categoryChartOption" height="300px" />
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="charts-row">
          <!-- OD流量分析（起终点站） -->
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
              <span>地铁线路详情</span>
              <el-button type="primary" size="small" :icon="Refresh" @click="refreshData">
                刷新数据
              </el-button>
            </div>
          </template>
          <el-table
            :data="metroLines"
            stripe
            style="width: 100%"
            :default-sort="{ prop: 'flow', order: 'descending' }"
          >
            <el-table-column prop="line" label="线路" width="120">
              <template #default="{ row }">
                <el-tag :type="row.tagType" size="large">{{ row.line }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="线路名称" />
            <el-table-column prop="stations" label="站点数" width="100" align="center" />
            <el-table-column prop="flow" label="今日流量(万人次)" width="160" sortable align="right">
              <template #default="{ row }">
                <el-text type="primary" size="large">{{ row.flow.toFixed(1) }}</el-text>
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
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
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

const router = useRouter()
const username = ref(localStorage.getItem('username') || '管理员')
let updateTimer = null

// 统计数据
const statsData = ref([
  {
    icon: 'UserFilled',
    label: '今日客流总量',
    value: '1256.8万',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: 'TrendCharts',
    label: '实时在线',
    value: '45.2万',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    icon: 'Connection',
    label: '运营线路',
    value: '20条',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    icon: 'Guide',
    label: '运营站点',
    value: '508个',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  }
])

// 地铁线路数据
const metroLines = ref([
  { line: '1号线', name: '富锦路 - 莘庄', stations: 28, flow: 156.8, status: '正常', tagType: 'primary' },
  { line: '2号线', name: '徐泾东 - 浦东国际机场', stations: 30, flow: 189.2, status: '正常', tagType: 'success' },
  { line: '3号线', name: '江杨北路 - 上海南站', stations: 29, flow: 142.5, status: '正常', tagType: 'warning' },
  { line: '4号线', name: '环线', stations: 26, flow: 135.6, status: '正常', tagType: 'danger' },
  { line: '5号线', name: '莘庄 - 奉贤新城', stations: 19, flow: 98.3, status: '正常', tagType: 'info' },
  { line: '6号线', name: '港城路 - 东方体育中心', stations: 28, flow: 126.4, status: '正常', tagType: 'primary' },
  { line: '7号线', name: '美兰湖 - 花木路', stations: 33, flow: 145.7, status: '正常', tagType: 'success' },
  { line: '8号线', name: '市光路 - 沈杜公路', stations: 30, flow: 138.9, status: '正常', tagType: 'warning' },
  { line: '9号线', name: '松江南站 - 曹路', stations: 35, flow: 167.3, status: '正常', tagType: 'danger' },
  { line: '10号线', name: '虹桥火车站 - 基隆路', stations: 31, flow: 152.1, status: '正常', tagType: 'info' }
])

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
    name: '人次/小时'
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
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '流量(万人次)'
  },
  yAxis: {
    type: 'category',
    data: []
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

// 时段流量分析
const areaChartOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['工作日', '周末']
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
    data: ['5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', 
           '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
  },
  yAxis: {
    type: 'value',
    name: '流量(万人次)'
  },
  series: [
    {
      name: '工作日',
      type: 'line',
      stack: 'Total',
      smooth: true,
      areaStyle: {},
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '周末',
      type: 'line',
      stack: 'Total',
      smooth: true,
      areaStyle: {},
      data: [],
      itemStyle: { color: '#67C23A' }
    }
  ]
})

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
    right: '4%',
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

// 流量分类分析图表（通勤C/居家HB/非居家NHB）
const categoryChartOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['通勤流量(C)', '居家流量(HB)', '非居家流量(NHB)']
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
    name: '流量(万人次)'
  },
  series: [
    {
      name: '通勤流量(C)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '居家流量(HB)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      data: [],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '非居家流量(NHB)',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      data: [],
      itemStyle: { color: '#E6A23C' }
    }
  ]
})

// OD流量分析图表（起终点站）
const odChartOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      return `${params.seriesName}<br/>${params.name}<br/>流量: ${params.value}万人次 (${params.percent}%)`
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
        formatter: '{b}: {c}万\n({d}%)'
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

// 进站流量分类统计
const inflowCategoryOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['总进站流量(Tot_IF)', '通勤进站(C_IF)', '居家进站(HB_IF)', '非居家进站(NHB_IF)']
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
    name: '流量(万人次)'
  },
  series: [
    {
      name: '总进站流量(Tot_IF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '通勤进站(C_IF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '居家进站(HB_IF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#E6A23C' }
    },
    {
      name: '非居家进站(NHB_IF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#F56C6C' }
    }
  ]
})

// 出站流量分类统计
const outflowCategoryOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['总出站流量(Tot_OF)', '通勤出站(C_OF)', '居家出站(HB_OF)', '非居家出站(NHB_OF)']
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
    name: '流量(万人次)'
  },
  series: [
    {
      name: '总出站流量(Tot_OF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '通勤出站(C_OF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '居家出站(HB_OF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#E6A23C' }
    },
    {
      name: '非居家出站(NHB_OF)',
      type: 'bar',
      data: [],
      itemStyle: { color: '#F56C6C' }
    }
  ]
})

// 初始化图表数据
const initChartData = () => {
  // 实时流量趋势 - 显示当日5:00-23:00的数据
  const hours = []
  const inFlow = []
  const outFlow = []
  const now = new Date()
  const currentHour = now.getHours()
  
  // 如果当前时间在5点之前，显示昨天5点-23点的数据
  // 如果当前时间在5点-23点之间，显示今天5点到当前时间的数据
  // 如果当前时间在23点之后，显示今天5点-23点的完整数据
  let startHour = 5
  let endHour = currentHour >= 23 ? 23 : (currentHour < 5 ? 23 : currentHour)
  
  for (let hour = startHour; hour <= endHour; hour++) {
    hours.push(`${hour}:00`)
    // 根据时段生成不同的流量数据
    let baseFlow = 80
    if (hour >= 7 && hour <= 9) {
      // 早高峰
      baseFlow = 140
    } else if (hour >= 17 && hour <= 19) {
      // 晚高峰
      baseFlow = 130
    } else if (hour >= 5 && hour <= 6) {
      // 早间
      baseFlow = 50
    } else if (hour >= 21 && hour <= 23) {
      // 晚间
      baseFlow = 60
    }
    inFlow.push(Math.floor(Math.random() * 30) + baseFlow)
    outFlow.push(Math.floor(Math.random() * 30) + baseFlow)
  }
  lineChartOption.value.xAxis.data = hours
  lineChartOption.value.series[0].data = inFlow
  lineChartOption.value.series[1].data = outFlow

  // 站点排名
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

  // 线路流量分布
  const topLines = metroLines.value.slice(0, 6).map(line => ({
    value: line.flow,
    name: line.line
  }))
  pieChartOption.value.series[0].data = topLines

  // 时段流量 (5点-23点，共19个时段)
  const workdayFlow = [12, 18, 45, 85, 120, 95, 80, 75, 70, 68, 72, 78, 95, 110, 98, 85, 65, 45, 30]
  const weekendFlow = [8, 12, 20, 35, 50, 65, 75, 85, 90, 88, 85, 90, 95, 100, 95, 85, 70, 50, 35]
  areaChartOption.value.series[0].data = workdayFlow
  areaChartOption.value.series[1].data = weekendFlow

  // 天气信息数据 (5点-23点，每小时)
  const weatherTimes = []
  const temperatures = []
  const rainfalls = []
  const windSpeeds = []
  for (let hour = 5; hour <= 23; hour++) {
    weatherTimes.push(`${hour}:00`)
    temperatures.push((Math.random() * 10 + 18).toFixed(1)) // 18-28°C
    rainfalls.push((Math.random() * 5).toFixed(1)) // 0-5mm/h
    windSpeeds.push((Math.random() * 20 + 10).toFixed(1)) // 10-30km/h
  }
  weatherChartOption.value.xAxis.data = weatherTimes
  weatherChartOption.value.series[0].data = temperatures
  weatherChartOption.value.series[1].data = rainfalls
  weatherChartOption.value.series[2].data = windSpeeds

  // 流量分类分析数据 (5点-23点)
  const categoryTimes = []
  const commuterFlow = [] // 通勤流量 C
  const homeFlow = [] // 居家流量 HB
  const nonHomeFlow = [] // 非居家流量 NHB
  for (let hour = 5; hour <= 23; hour++) {
    categoryTimes.push(`${hour}:00`)
    // 早高峰和晚高峰通勤流量高
    let commuter = 0
    if (hour >= 7 && hour <= 9) {
      commuter = Math.floor(Math.random() * 60 + 80) // 80-140
    } else if (hour >= 17 && hour <= 19) {
      commuter = Math.floor(Math.random() * 50 + 70) // 70-120
    } else {
      commuter = Math.floor(Math.random() * 30 + 20) // 20-50
    }
    commuterFlow.push(commuter)
    homeFlow.push(Math.floor(Math.random() * 40 + 30)) // 30-70
    nonHomeFlow.push(Math.floor(Math.random() * 35 + 25)) // 25-60
  }
  categoryChartOption.value.xAxis.data = categoryTimes
  categoryChartOption.value.series[0].data = commuterFlow
  categoryChartOption.value.series[1].data = homeFlow
  categoryChartOption.value.series[2].data = nonHomeFlow

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
  inflowCategoryOption.value.series[0].data = inflowTot
  inflowCategoryOption.value.series[1].data = inflowC
  inflowCategoryOption.value.series[2].data = inflowHB
  inflowCategoryOption.value.series[3].data = inflowNHB

  // 出站流量分类统计（TOP 10站点）
  const outflowTot = [] // 总出站流量
  const outflowC = [] // 通勤出站
  const outflowHB = [] // 居家出站
  const outflowNHB = [] // 非居家出站
  topStationsList.forEach(() => {
    const tot = Math.floor(Math.random() * 50 + 60) // 60-110
    outflowTot.push(tot)
    outflowC.push(Math.floor(tot * 0.45)) // 45%通勤
    outflowHB.push(Math.floor(tot * 0.30)) // 30%居家
    outflowNHB.push(Math.floor(tot * 0.25)) // 25%非居家
  })
  outflowCategoryOption.value.xAxis.data = topStationsList
  outflowCategoryOption.value.series[0].data = outflowTot
  outflowCategoryOption.value.series[1].data = outflowC
  outflowCategoryOption.value.series[2].data = outflowHB
  outflowCategoryOption.value.series[3].data = outflowNHB
}

// 更新实时数据
const updateRealtimeData = () => {
  const now = new Date()
  const currentHour = now.getHours()
  const currentHourStr = `${currentHour}:00`
  
  // 只更新5:00-23:00运营时段内的数据
  if (currentHour >= 5 && currentHour <= 23) {
    if (lineChartOption.value.xAxis.data) {
      const lastIndex = lineChartOption.value.xAxis.data.length - 1
      const lastHourStr = lineChartOption.value.xAxis.data[lastIndex]
      
      if (lastHourStr !== currentHourStr) {
        // 如果是新时段，添加新数据点（只要不超过23点）
        if (currentHour > parseInt(lastHourStr.split(':')[0])) {
          lineChartOption.value.xAxis.data.push(currentHourStr)
          
          // 根据时段生成流量数据
          let baseFlow = 80
          if (currentHour >= 7 && currentHour <= 9) {
            baseFlow = 140
          } else if (currentHour >= 17 && currentHour <= 19) {
            baseFlow = 130
          } else if (currentHour >= 5 && currentHour <= 6) {
            baseFlow = 50
          } else if (currentHour >= 21 && currentHour <= 23) {
            baseFlow = 60
          }
          
          lineChartOption.value.series[0].data.push(Math.floor(Math.random() * 30) + baseFlow)
          lineChartOption.value.series[1].data.push(Math.floor(Math.random() * 30) + baseFlow)
        }
      } else {
        // 更新当前时段的数据
        let baseFlow = 80
        if (currentHour >= 7 && currentHour <= 9) {
          baseFlow = 140
        } else if (currentHour >= 17 && currentHour <= 19) {
          baseFlow = 130
        } else if (currentHour >= 5 && currentHour <= 6) {
          baseFlow = 50
        } else if (currentHour >= 21 && currentHour <= 23) {
          baseFlow = 60
        }
        
        lineChartOption.value.series[0].data[lastIndex] = Math.floor(Math.random() * 30) + baseFlow
        lineChartOption.value.series[1].data[lastIndex] = Math.floor(Math.random() * 30) + baseFlow
      }
    }
  }

  // 更新统计数据
  statsData.value[0].value = (1256.8 + Math.random() * 10).toFixed(1) + '万'
  statsData.value[1].value = (45.2 + Math.random() * 2).toFixed(1) + '万'
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

const refreshData = () => {
  initChartData()
  ElMessage.success('数据已刷新')
}

const viewDetails = (row) => {
  ElMessage.info(`查看 ${row.line} 的详细信息`)
}

onMounted(() => {
  try {
    initChartData()
    // 每30秒更新一次实时数据
    updateTimer = setInterval(updateRealtimeData, 30000)
  } catch (error) {
    console.error('Dashboard 初始化失败:', error)
  }
})

onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
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

.table-card {
  border-radius: 16px;
  border: 1px solid #eef0f6;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
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

