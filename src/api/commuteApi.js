// API 服务 - 与后端通信
const API_BASE_URL = 'http://localhost:8000/api'

/**
 * 获取校区出行时刻表
 * @param {string} campus - 校区，如 'jiading'
 * @param {string} routeKey - 路线标识，如 'dz1', 'beian', 'bus822', 'teacher'
 * @param {string} dayType - 日期类型 'weekday' | 'weekend'
 * @param {string} direction - 方向 'campusToStation' | 'stationToCampus'
 */
export async function fetchSchedules(campus, routeKey, dayType, direction) {
  const params = new URLSearchParams({ campus, routeKey, dayType, direction })
  const res = await fetch(`${API_BASE_URL}/commute/schedules?${params}`)
  const json = await res.json()
  return json.data
}

/**
 * 获取所有时刻表数据（批量）
 * @param {string} dayType - 日期类型
 */
export async function fetchAllSchedules(dayType) {
  const routes = ['dz1', 'beian', 'bus822', 'teacher']
  const directions = ['campusToStation', 'stationToCampus']

  const result = {}

  for (const routeKey of routes) {
    result[routeKey] = {
      name: getRouteName(routeKey),
      campusToStation: { [dayType]: [] },
      stationToCampus: { [dayType]: [] }
    }

    for (const direction of directions) {
      try {
        const data = await fetchSchedules('jiading', routeKey, dayType, direction)
        result[routeKey][direction][dayType] = data.times || []
      } catch (e) {
        console.error(`Failed to fetch ${routeKey} ${direction}:`, e)
        result[routeKey][direction][dayType] = []
      }
    }
  }

  return result
}

function getRouteName(routeKey) {
  const names = {
    dz1: 'DZ1 直达短驳',
    beian: '北安跨线',
    bus822: '822 路',
    teacher: '教职班车（嘉定⇄四平）'
  }
  return names[routeKey] || routeKey
}

/**
 * 获取地铁拥挤度曲线
 * @param {string} lines - 线路号，逗号分隔，如 '11,14'
 */
export async function fetchCongestionProfiles(lines = '11,14') {
  const res = await fetch(`${API_BASE_URL}/metro/congestion/profiles?lines=${lines}`)
  const json = await res.json()

  // 转换为前端格式 { line11: [...], line14: [...] }
  const result = {}
  for (const item of json.data || []) {
    result[`line${item.line}`] = item.congestion
  }
  return result
}

/**
 * 获取路径元数据
 */
export async function fetchRouteMeta() {
  const res = await fetch(`${API_BASE_URL}/commute/routeMeta`)
  const json = await res.json()

  // 转换为前端格式
  const result = {}
  for (const item of json.data || []) {
    result[item.lineKey] = {
      name: item.displayName,
      color: item.color,
      baseMetroMinutes: item.defaultMetroMinutes,
      walkSteps: item.walkSteps,
      shuttleKey: item.shuttleKey,
      description: item.descriptionTemplate?.replace('{{destination}}', '真如') || ''
    }
  }
  return result
}

/**
 * 获取终点站地铁时间
 */
export async function fetchDestinationTimes() {
  const res = await fetch(`${API_BASE_URL}/commute/destinationTimes`)
  const json = await res.json()

  // 转换为前端格式 { '真如': { line11: 38, line14: 30 }, ... }
  const result = {}
  for (const item of json.data || []) {
    result[item.station] = item.lineTimes
  }
  return result
}

/**
 * 获取地铁线路和站点信息
 */
export async function fetchLinesWithStations() {
  const res = await fetch(`${API_BASE_URL}/metro/lines-with-stations`)
  const json = await res.json()

  // 转换为前端格式
  const lineOptions = []
  const lineToStations = {}

  for (const line of json.data || []) {
    lineOptions.push({
      value: line.lineName,
      label: line.lineName
    })
    lineToStations[line.lineName] = line.stations.map(s => s.name)
  }

  return { lineOptions, lineToStations }
}


// ============ 时刻表 CRUD ============

/**
 * 获取时刻表列表（带ID，用于管理）
 */
export async function fetchScheduleList(routeKey = null, dayType = null) {
  const params = new URLSearchParams()
  if (routeKey) params.append('routeKey', routeKey)
  if (dayType) params.append('dayType', dayType)
  const res = await fetch(`${API_BASE_URL}/commute/schedules/list?${params}`)
  const json = await res.json()
  return json.data || []
}

/**
 * 添加班次
 */
export async function createSchedule(data) {
  const res = await fetch(`${API_BASE_URL}/commute/schedules`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

/**
 * 修改班次
 */
export async function updateSchedule(id, data) {
  const res = await fetch(`${API_BASE_URL}/commute/schedules/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

/**
 * 删除班次
 */
export async function deleteSchedule(id) {
  const res = await fetch(`${API_BASE_URL}/commute/schedules/${id}`, {
    method: 'DELETE'
  })
  return await res.json()
}


// ============ 收藏功能 ============

/**
 * 获取收藏列表
 */
export async function fetchFavorites(userId = 'default') {
  const res = await fetch(`${API_BASE_URL}/favorites?userId=${userId}`)
  const json = await res.json()
  return json.data || []
}

/**
 * 添加收藏
 */
export async function addFavorite(stationName, lineKey = null) {
  const res = await fetch(`${API_BASE_URL}/favorites`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stationName, lineKey, userId: 'default' })
  })
  return await res.json()
}

/**
 * 取消收藏
 */
export async function removeFavorite(stationName) {
  const res = await fetch(`${API_BASE_URL}/favorites/station/${encodeURIComponent(stationName)}?userId=default`, {
    method: 'DELETE'
  })
  return await res.json()
}


// ============ 拥挤度反馈 ============

/**
 * 提交拥挤度反馈
 */
export async function submitCongestionFeedback(lineId, hour, reportedLevel) {
  const res = await fetch(`${API_BASE_URL}/feedback/congestion`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lineId, hour, reportedLevel })
  })
  return await res.json()
}

/**
 * 获取拥挤度反馈统计
 */
export async function fetchCongestionStats(lineId) {
  const res = await fetch(`${API_BASE_URL}/feedback/congestion/stats?lineId=${lineId}`)
  const json = await res.json()
  return json.data
}

