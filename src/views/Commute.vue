<template>
  <div class="commute-page">
    <div class="commute-nav">
      <div class="nav-left">
        <el-icon class="nav-icon"><Location /></el-icon>
        <span class="nav-title">嘉定通勤推荐</span>
      </div>
      <div class="nav-right">
        <el-button v-if="isAdmin" :icon="TrendCharts" @click="goDashboard" type="primary">管理员页</el-button>
        <el-button :icon="Location" @click="goRoute" type="success">地铁线路图</el-button>
        <el-button :icon="SwitchButton" @click="handleLogout" type="danger">退出登录</el-button>
      </div>
    </div>

    <section class="hero-block">
      <div class="hero-left">
        <div class="eyebrow">
          <el-icon><Location /></el-icon>
          <span>嘉定校区 ↔ 轨交 14 号线封浜</span>
        </div>
        <h1>智能出行决策 · 校车/公交倒计时</h1>
        <p class="subtitle">
          按照你给的时刻表，把 11 号线安亭 vs 14 号线封浜的通勤体验做成可视化决策。
        </p>
        <div class="hero-controls">
          <el-select v-model="dayType" size="large" class="control-item" :teleported="false">
            <el-option label="工作日" value="weekday" />
            <el-option label="双休日/法定假日" value="weekend" />
          </el-select>
          <el-time-select
            v-model="virtualTime"
            :max-time="'23:00'"
            :start="'05:00'"
            :step="'00:10'"
            placeholder="出发时间"
            size="large"
            class="control-item"
          />
          <el-select
            v-model="selectedLine"
            placeholder="选择终点线路（如：11号线）"
            size="large"
            class="control-item"
            :teleported="false"
          >
            <el-option
              v-for="line in lineOptions"
              :key="line.value"
              :label="line.label"
              :value="line.value"
            />
          </el-select>
          <el-select
            v-model="selectedStation"
            :disabled="!selectedLine"
            placeholder="选择该线路上的站点"
            size="large"
            class="control-item"
            :teleported="false"
          >
            <el-option
              v-for="st in stationOptions"
              :key="st.value"
              :label="st.label"
              :value="st.value"
            />
          </el-select>
          <el-tag type="success" size="large" class="recommend-pill">
            <el-icon><StarFilled /></el-icon>
            推荐线路：{{ recommendedRoute.name }}
          </el-tag>
        </div>
        <div class="meta-row">
          <div class="meta-chip">
            <el-icon><TrendCharts /></el-icon>
            11 号线标红，14 号线标绿
          </div>
          <div class="meta-chip">
            <el-icon><Timer /></el-icon>
            校车/公交时间来自校内最新时刻表
          </div>
        </div>
      </div>
      <div class="hero-right">
        <div class="glass-card">
          <div class="card-title">
            <span>下一班车 · 封浜向</span>
            <el-tag size="small" type="success">实时更新</el-tag>
          </div>
          <div class="next-time">
            <div class="time-value">{{ nextForHero.time }}</div>
            <div class="time-desc">距离发车 {{ formatCountdown(nextForHero.diff) }}</div>
          </div>
          <div class="hero-tags">
            <span class="tag">{{ nextForHero.line }}</span>
            <span class="tag tag-soft">封浜 → 14 号线</span>
            <span class="tag tag-soft">乘车点：曹安公路绿苑路</span>
          </div>
          <div class="progress-row">
            <div class="progress-label">舒适度</div>
            <div class="progress-bar">
              <span :style="{ width: `${recommendedRoute.comfort}%`, background: recommendedRoute.color }"></span>
            </div>
            <div class="progress-num">{{ recommendedRoute.comfort }}%</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section-card decision-section">
      <div class="section-header">
        <div>
          <p class="section-eyebrow">The Decision Maker</p>
          <h3>11 号线 vs 14 号线 · 一键推荐</h3>
        </div>
        <el-button type="primary" link :icon="Guide">推荐逻辑：时刻表 + 拥挤度 + 等待时间</el-button>
      </div>
      <div class="decision-grid">
        <div
          v-for="option in routeOptions"
          :key="option.key"
          class="decision-card"
          :class="{ active: option.key === recommendedRoute.key }"
        >
          <div class="decision-header">
            <div class="title">
              <span class="dot" :style="{ background: option.color }"></span>
              {{ option.name }}
            </div>
            <el-tag v-if="option.key === recommendedRoute.key" type="success" size="small">
              推荐
            </el-tag>
          </div>
          <p class="desc">{{ option.description }}</p>
          <div class="metrics">
            <div class="metric">
              <div class="label">预计总耗时</div>
              <div class="value">{{ option.totalMinutes }} 分钟</div>
            </div>
            <div class="metric">
              <div class="label">等待接驳</div>
              <div class="value">{{ option.waitMinutes }} 分钟</div>
            </div>
            <div class="metric">
              <div class="label">拥挤度</div>
              <div class="value" :style="{ color: option.color }">{{ option.congestionText }}</div>
            </div>
          </div>
          <div class="chips">
            <span class="chip">{{ option.shuttleName }}</span>
            <span class="chip chip-soft">{{ option.walkSteps }} 步</span>
            <span class="chip chip-soft">地铁 {{ option.baseMetroMinutes }} 分钟</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section-card countdown-section">
      <div class="section-header">
        <div>
          <p class="section-eyebrow">The Live Scheduler</p>
          <h3>下一班车倒计时</h3>
        </div>
        <el-tag size="small" type="info">工作日 / 双休日一键切换</el-tag>
      </div>
      <div class="countdown-grid">
        <div v-for="item in countdownCards" :key="item.key" class="countdown-card">
          <div class="card-head">
            <span class="line-name">{{ item.name }}</span>
            <el-tag size="small" :type="item.tagType">{{ item.directionLabel }}</el-tag>
          </div>
          <div class="count-row">
            <div class="time">{{ item.nextDeparture.time }}</div>
            <div class="count">{{ formatCountdown(item.nextDeparture.diff) }}</div>
          </div>
          <div class="info-row">
            <span>返程：{{ item.returnDeparture.time }}</span>
            <span>返程剩余 {{ formatCountdown(item.returnDeparture.diff) }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section-card chart-section">
      <div class="section-header">
        <div>
          <p class="section-eyebrow">The Heatmap</p>
          <h3>11 / 14 号线拥挤度曲线</h3>
        </div>
        <el-button type="primary" :icon="ChatLineRound" @click="openFeedback">
          我要反馈
        </el-button>
      </div>
      <ECharts :option="congestionOption" height="360px" />
    </section>

    <section class="section-card timetable-section">
      <div class="section-header">
        <div>
          <p class="section-eyebrow">时刻表详情</p>
          <h3>嘉定校区出行时刻表（图片数字化）</h3>
        </div>
        <div class="header-actions">
          <el-select v-model="activeLineTab" size="small" style="width: 180px" :teleported="false">
            <el-option v-for="key in timetableKeys" :key="key" :label="busSchedules[key]?.name || key" :value="key" />
          </el-select>
          <el-button type="primary" size="small" :icon="Plus" @click="openAddSchedule">
            添加班次
          </el-button>
        </div>
      </div>
      <el-table :data="timetableRows" class="timetable" stripe>
        <el-table-column prop="direction" label="方向" width="180" />
        <el-table-column prop="time" label="时间">
          <template #default="{ row }">
            <span :class="row.isPast ? 'time-past' : 'time-future'">
              {{ row.time }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="hint" label="备注" width="200" />
      </el-table>
    </section>

    <!-- CRUD 弹窗 -->
    <ScheduleEditDialog
      v-model="showScheduleDialog"
      :edit-data="editingSchedule"
      @success="handleScheduleSuccess"
    />
    <FeedbackDialog
      v-model="showFeedbackDialog"
      :line-id="feedbackLineId"
      :hour="feedbackHour"
      @success="handleFeedbackSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import ECharts from '@/components/ECharts.vue'
import ScheduleEditDialog from '@/components/ScheduleEditDialog.vue'
import FeedbackDialog from '@/components/FeedbackDialog.vue'
import { Location, StarFilled, TrendCharts, Timer, Guide, ChatLineRound, Plus, SwitchButton } from '@element-plus/icons-vue'
import {
  fetchAllSchedules,
  fetchCongestionProfiles,
  fetchRouteMeta,
  fetchDestinationTimes,
  fetchLinesWithStations
} from '@/api/commuteApi'
import { getCurrentUser, logout } from '@/api/authApi'

const router = useRouter()
const dayType = ref('weekday')
const virtualTime = ref(getNowString())
const activeLineTab = ref('bus822')
const nowTick = ref(new Date())

// 用户角色检查
const isAdmin = computed(() => {
  const user = getCurrentUser()
  return user?.role === 'admin'
})

// ========== 从后端加载的数据 ==========
const busSchedules = ref({
  dz1: { name: 'DZ1 直达短驳', campusToStation: { weekday: [], weekend: [] }, stationToCampus: { weekday: [], weekend: [] } },
  beian: { name: '北安跨线', campusToStation: { weekday: [], weekend: [] }, stationToCampus: { weekday: [], weekend: [] } },
  bus822: { name: '822 路', campusToStation: { weekday: [], weekend: [] }, stationToCampus: { weekday: [], weekend: [] } },
  teacher: { name: '教职班车（嘉定⇄四平）', campusToStation: { weekday: [], weekend: [] }, stationToCampus: { weekday: [], weekend: [] } }
})

const congestionProfiles = ref({
  line11: Array(24).fill(0.5),
  line14: Array(24).fill(0.3)
})

const lineMeta = ref({
  line11: { name: '路径 A · 11号线安亭', color: '#ef4444', baseMetroMinutes: 38, walkSteps: 820, shuttleKey: 'beian', description: '嘉定校区 → 北安跨线 → 11号线安亭方向 → 真如' },
  line14: { name: '路径 B · 14号线封浜', color: '#22c55e', baseMetroMinutes: 30, walkSteps: 420, shuttleKey: 'bus822', description: '嘉定校区 → 822/DZ1 → 封浜 → 14号线 → 真如' }
})

const destinationTravelMinutes = ref({
  真如: { line11: 38, line14: 30 },
  江苏路: { line11: 42, line14: 34 },
  徐家汇: { line11: 48, line14: 40 }
})

// 终点线路与站点选项
const lineOptions = ref([
  { value: '11号线', label: '11号线' },
  { value: '14号线', label: '14号线' }
])

const lineToStations = ref({
  '11号线': ['真如', '江苏路', '徐家汇'],
  '14号线': ['真如', '嘉定新城', '封浜']
})

const isLoading = ref(true)

const selectedLine = ref('11号线')
const selectedStation = ref('真如')

const stationOptions = computed(() => {
  const list = lineToStations.value[selectedLine.value] || []
  return list.map(name => ({
    value: name,
    label: `${selectedLine.value} | ${name}`
  }))
})

const destination = computed(() => selectedStation.value || '真如')
let timer = null

const dayTypeKey = computed(() => (dayType.value === 'weekday' ? 'weekday' : 'weekend'))

const plannedDate = computed(() => {
  const date = new Date()
  const [hour, minute] = (virtualTime.value || '08:00').split(':').map(Number)
  date.setHours(hour || 0, minute || 0, 0, 0)
  return date
})

const parseToDate = (timeStr, baseDate = new Date()) => {
  const [hour, minute] = timeStr.split(':').map(Number)
  const d = new Date(baseDate)
  d.setHours(hour || 0, minute || 0, 0, 0)
  return d
}

const findNextTime = (list, baseDate) => {
  if (!list || list.length === 0) return { time: '--', diff: Infinity }
  const sorted = [...list].sort()
  const candidate = sorted.find(t => parseToDate(t, baseDate) >= baseDate)
  const targetTime = candidate || sorted[0]
  const targetDate = parseToDate(targetTime, baseDate)
  if (!candidate) {
    targetDate.setDate(targetDate.getDate() + 1)
  }
  const diffMinutes = Math.max(0, Math.round((targetDate - baseDate) / 60000))
  return { time: targetTime, diff: diffMinutes }
}

const getNextForLine = (lineKey, direction, baseDate) => {
  const schedule = busSchedules.value[lineKey]
  if (!schedule) return { time: '--', diff: Infinity }
  const list = schedule[direction]?.[dayTypeKey.value] || []
  return findNextTime(list, baseDate)
}

// 加载所有后端数据
async function loadAllData() {
  isLoading.value = true
  try {
    // 并行加载所有数据
    const [schedules, congestion, routeMeta, destTimes, linesData] = await Promise.all([
      fetchAllSchedules(dayTypeKey.value),
      fetchCongestionProfiles('11,14'),
      fetchRouteMeta(),
      fetchDestinationTimes(),
      fetchLinesWithStations()
    ])

    // 更新时刻表
    if (schedules) {
      Object.keys(schedules).forEach(key => {
        if (busSchedules.value[key]) {
          busSchedules.value[key] = schedules[key]
        }
      })
    }

    // 更新拥挤度
    if (congestion) {
      congestionProfiles.value = congestion
    }

    // 更新路径元数据
    if (routeMeta && Object.keys(routeMeta).length > 0) {
      lineMeta.value = routeMeta
    }

    // 更新终点站时间
    if (destTimes && Object.keys(destTimes).length > 0) {
      destinationTravelMinutes.value = destTimes
    }

    // 更新线路和站点选项
    if (linesData.lineOptions?.length > 0) {
      lineOptions.value = linesData.lineOptions
      lineToStations.value = linesData.lineToStations
      // 设置默认选中
      selectedLine.value = lineOptions.value[0]?.value || '11号线'
      selectedStation.value = lineToStations.value[selectedLine.value]?.[0] || '真如'
    }

    console.log('✅ 后端数据加载成功')
  } catch (error) {
    console.error('❌ 加载后端数据失败，使用默认数据:', error)
  } finally {
    isLoading.value = false
  }
}

// 监听日期类型变化，重新加载时刻表
watch(dayType, async () => {
  const schedules = await fetchAllSchedules(dayTypeKey.value)
  if (schedules) {
    Object.keys(schedules).forEach(key => {
      if (busSchedules.value[key]) {
        busSchedules.value[key] = schedules[key]
      }
    })
  }
})

// 不同终点对应的地铁乘坐时间（单位：分钟），用于让"预计总耗时"随终点变化


const routeOptions = computed(() => {
  const hour = plannedDate.value.getHours()
  const dest = destination.value?.trim() || '目的地'
  return Object.entries(lineMeta.value).map(([key, meta]) => {
    const congestion = congestionProfiles.value[key]?.[hour] ?? 0.5
    const shuttleName = busSchedules.value[meta.shuttleKey]?.name || '接驳班车'
    const next = getNextForLine(meta.shuttleKey, 'campusToStation', plannedDate.value)
    const waitMinutes = next.diff === Infinity ? 15 : next.diff
    const walkMinutes = Math.max(5, Math.round(meta.walkSteps / 80))
    const destMetro = destinationTravelMinutes.value[dest]?.[key] ?? meta.baseMetroMinutes
    const total = Math.round(destMetro + waitMinutes + walkMinutes + congestion * 25)
    const comfort = Math.max(10, Math.round((1 - congestion) * 100))
    const desc = (meta.description || '').replace('真如', dest)
    return {
      key,
      name: meta.name,
      description: desc,
      color: meta.color,
      shuttleName,
      walkSteps: meta.walkSteps,
      baseMetroMinutes: destMetro,
      totalMinutes: total,
      waitMinutes,
      comfort,
      congestionText: congestion >= 0.8 ? '拥挤' : congestion >= 0.5 ? '略挤' : '舒适'
    }
  })
})

const recommendedRoute = computed(() =>
  routeOptions.value.reduce((best, curr) => (curr.totalMinutes < best.totalMinutes ? curr : best), routeOptions.value[0] || {})
)

const countdownCards = computed(() => {
  const list = [
    { key: 'dz1', tagType: 'success', directionLabel: '封浜短驳' },
    { key: 'beian', tagType: 'warning', directionLabel: '北安跨线' },
    { key: 'bus822', tagType: 'info', directionLabel: '公交 822' },
    { key: 'teacher', tagType: 'primary', directionLabel: '教职班车' }
  ]
  return list.map(item => {
    const nextDeparture = getNextForLine(item.key, 'campusToStation', nowTick.value)
    const returnDeparture = getNextForLine(item.key, 'stationToCampus', nowTick.value)
    return {
      ...item,
      name: busSchedules.value[item.key]?.name || item.key,
      nextDeparture,
      returnDeparture
    }
  })
})

const nextForHero = computed(() => {
  const target = countdownCards.value.find(card => card.key === 'bus822') || countdownCards.value[0]
  return {
    line: target?.name || '—',
    time: target?.nextDeparture?.time || '--',
    diff: target?.nextDeparture?.diff ?? Infinity
  }
})

const congestionOption = computed(() => {
  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`)
  return {
    grid: { left: '3%', right: '4%', bottom: '5%', top: '12%', containLabel: true },
    tooltip: { trigger: 'axis' },
    legend: { data: ['11号线', '14号线'] },
    xAxis: { type: 'category', data: hours, boundaryGap: false },
    yAxis: { type: 'value', min: 0, max: 1, axisLabel: { formatter: value => (value * 100).toFixed(0) + '%' } },
    series: [
      {
        name: '11号线',
        type: 'line',
        smooth: true,
        areaStyle: { color: 'rgba(239,68,68,0.12)' },
        itemStyle: { color: '#ef4444' },
        data: congestionProfiles.value.line11
      },
      {
        name: '14号线',
        type: 'line',
        smooth: true,
        areaStyle: { color: 'rgba(34,197,94,0.12)' },
        itemStyle: { color: '#22c55e' },
        data: congestionProfiles.value.line14
      }
    ]
  }
})

const timetableKeys = ['bus822', 'dz1', 'beian', 'teacher']

const timetableRows = computed(() => {
  const currentKey = activeLineTab.value
  const schedule = busSchedules.value[currentKey]
  if (!schedule) return []

  const rows = []
  const typeKey = dayTypeKey.value
  const leaveList = schedule.campusToStation?.[typeKey] || []
  const backList = schedule.stationToCampus?.[typeKey] || []

  const now = nowTick.value
  const nowMinutes = now.getHours() * 60 + now.getMinutes()

  const parseMinutes = (t) => {
    const [h, m] = t.split(':').map(Number)
    return (h || 0) * 60 + (m || 0)
  }

  leaveList.forEach(time => {
    const mins = parseMinutes(time)
    rows.push({
      direction: '嘉定 → 站点',
      time,
      hint: '学校出发',
      isPast: mins < nowMinutes
    })
  })

  backList.forEach(time => {
    const mins = parseMinutes(time)
    rows.push({
      direction: '站点 → 嘉定',
      time,
      hint: '封浜/四平返回',
      isPast: mins < nowMinutes
    })
  })

  return rows
})

const formatCountdown = (minutes) => {
  if (minutes === Infinity) return '暂未排班'
  if (minutes <= 0) return '即将发车'
  if (minutes < 60) return `${minutes} 分钟`
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return `${h} 小时 ${m} 分`
}

const goDashboard = () => {
  router.push('/dashboard')
}

const goRoute = () => {
  router.push('/route-planner')
}

const handleLogout = () => {
  logout()
  router.push('/login')
}

onMounted(() => {
  // 加载后端数据
  loadAllData()
  
  // 定时刷新当前时间
  timer = setInterval(() => {
    nowTick.value = new Date()
  }, 1000 * 30)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function getNowString() {
  const now = new Date()
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  return `${h}:${m}`
}

// ============ CRUD 弹窗控制 ============

// 时刻表编辑弹窗
const showScheduleDialog = ref(false)
const editingSchedule = ref(null)

function openAddSchedule() {
  editingSchedule.value = {
    routeKey: activeLineTab.value,
    dayType: dayType.value,
    direction: 'campusToStation',
    departureTime: ''
  }
  showScheduleDialog.value = true
}

async function handleScheduleSuccess() {
  // 重新加载时刻表
  const schedules = await fetchAllSchedules(dayTypeKey.value)
  if (schedules) {
    Object.keys(schedules).forEach(key => {
      if (busSchedules.value[key]) {
        busSchedules.value[key] = schedules[key]
      }
    })
  }
}

// 拥挤度反馈弹窗
const showFeedbackDialog = ref(false)
const feedbackLineId = ref('11')
const feedbackHour = ref(8)

function openFeedback() {
  const now = new Date()
  feedbackHour.value = now.getHours()
  feedbackLineId.value = '11'  // 默认11号线
  showFeedbackDialog.value = true
}

function handleFeedbackSuccess() {
  // 可以刷新拥挤度数据或显示感谢
  console.log('反馈成功')
}
</script>

<style scoped>
.commute-page {
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(circle at 18% 12%, rgba(102, 126, 234, 0.14), transparent 26%),
    radial-gradient(circle at 86% 10%, rgba(118, 75, 162, 0.12), transparent 30%),
    linear-gradient(135deg, #f7f9ff 0%, #eef2ff 40%, #f9fbff 100%);
}

.commute-nav {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #eef0f6;
  border-radius: 14px;
  padding: 12px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 18px 40px rgba(31, 41, 55, 0.08);
  margin-bottom: 14px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #0f172a;
  font-weight: 700;
}

.nav-icon {
  color: #4f46e5;
}

.nav-title {
  font-size: 16px;
}

.nav-right {
  display: flex;
  gap: 10px;
}

.hero-block {
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 18px;
  margin-bottom: 18px;
}

.hero-left {
  background: linear-gradient(135deg, #ffffff, #f4f7ff);
  border: 1px solid #eef0f6;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 24px 50px rgba(99, 122, 179, 0.12);
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: #eef2ff;
  color: #4f46e5;
  font-weight: 600;
  font-size: 13px;
}

.hero-left h1 {
  margin: 14px 0 8px;
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
}

.subtitle {
  color: #64748b;
  margin-bottom: 16px;
}

.hero-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
}

.control-item {
  width: 180px;
}

.recommend-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(79, 70, 229, 0.06);
  color: #4338ca;
  font-size: 13px;
}

.hero-right .glass-card {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(12px);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
  height: 100%;
}

.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  color: #0f172a;
}

.next-time {
  margin: 14px 0;
}

.next-time .time-value {
  font-size: 36px;
  font-weight: 800;
  color: #4f46e5;
  line-height: 1.1;
}

.next-time .time-desc {
  color: #64748b;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 10px;
  background: #eef2ff;
  color: #4338ca;
  border-radius: 10px;
  font-size: 12px;
}

.tag-soft {
  background: #f5f7fb;
  color: #475569;
}

.progress-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 14px;
}

.progress-label {
  color: #475569;
}

.progress-bar {
  flex: 1;
  background: #e5e7eb;
  height: 8px;
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar span {
  display: block;
  height: 100%;
}

.progress-num {
  font-weight: 700;
  color: #0f172a;
}

.section-card {
  background: #fff;
  border: 1px solid #eef0f6;
  border-radius: 18px;
  padding: 18px;
  margin-bottom: 18px;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.section-eyebrow {
  color: #64748b;
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.5px;
}

.section-header h3 {
  margin: 2px 0 0;
  font-size: 20px;
  color: #0f172a;
}

.decision-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}

.decision-card {
  border: 1px solid #eef0f6;
  border-radius: 14px;
  padding: 14px;
  background: linear-gradient(145deg, #ffffff, #f6f7fb);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.decision-card.active {
  box-shadow: 0 20px 50px rgba(79, 70, 229, 0.15);
  border-color: rgba(79, 70, 229, 0.35);
  transform: translateY(-4px);
}

.decision-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.decision-header .title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
}

.decision-card .dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  display: inline-block;
}

.decision-card .desc {
  color: #64748b;
  margin: 0 0 10px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 10px;
}

.metric .label {
  color: #94a3b8;
  font-size: 12px;
}

.metric .value {
  font-weight: 700;
  color: #0f172a;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 6px 10px;
  background: rgba(79, 70, 229, 0.08);
  color: #4338ca;
  border-radius: 10px;
  font-size: 12px;
}

.chip-soft {
  background: #f5f7fb;
  color: #475569;
}

.countdown-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 12px;
}

.countdown-card {
  border: 1px solid #eef0f6;
  border-radius: 14px;
  padding: 12px;
  background: linear-gradient(145deg, #ffffff, #f8f9ff);
  box-shadow: 0 12px 30px rgba(31, 41, 55, 0.06);
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-weight: 700;
}

.count-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.count-row .time {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
}

.count-row .count {
  color: #4338ca;
  font-weight: 700;
}

.info-row {
  display: flex;
  justify-content: space-between;
  color: #64748b;
  font-size: 12px;
}

.chart-section {
  padding-bottom: 10px;
}

.timetable ::v-deep(.el-table__cell) {
  padding: 10px 8px;
}

.time-past {
  color: #ef4444;
  font-weight: 600;
}

.time-future {
  color: #16a34a;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .hero-block {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .commute-page {
    padding: 14px;
  }

  .commute-nav {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .hero-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  .control-item {
    width: 100%;
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>

