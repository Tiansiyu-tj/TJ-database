// API 服务 - shanghai_metro 数据库交互
const API_BASE_URL = 'http://localhost:8000/api'

// ============ Station ============
/** 获取所有站点 */
export async function fetchStations() {
  const res = await fetch(`${API_BASE_URL}/metro/stations`)
  const json = await res.json()
  return json.data || []
}

/** 根据 ID 获取单个站点（若后端无单点查询则使用列表过滤） */
export async function fetchStationById(id) {
  try {
    const res = await fetch(`${API_BASE_URL}/metro/stations/${id}`)
    if (res.ok) {
      const json = await res.json()
      return json.data || null
    }
  } catch (e) {
    // ignore and fallback
  }
  const list = await fetchStations().catch(() => [])
  return list.find(s => String(s.id) === String(id) || String(s.stationID) === String(id)) || null
} 

/** 根据名称模糊查找站点 */
export async function searchStations(name) {
  const params = new URLSearchParams({ q: name })
  const res = await fetch(`${API_BASE_URL}/metro/stations/search?${params}`)
  const json = await res.json()
  return json.data || []
}

// ============ Neighbour (拓扑) ============
/** 获取某站点的邻居站点 */
export async function fetchNeighbours(stationId) {
  const res = await fetch(`${API_BASE_URL}/metro/stations/${stationId}/neighbours`)
  const json = await res.json()
  return json.data || []
}

// ============ DateInfo & TimeSegment ============
/** 获取某日期的 DateInfo */
export async function fetchDateInfo(recordDate) {
  const res = await fetch(`${API_BASE_URL}/time/dateInfo?recordDate=${encodeURIComponent(recordDate)}`)
  const json = await res.json()
  return json.data || null
}

/** 获取某日期的所有 TimeSegment（后端支持按 recordDate 过滤或前端在返回列中过滤） */
export async function fetchTimeSegmentsByDate(recordDate, limit = 1000) {
  const params = new URLSearchParams()
  if (recordDate) params.append('recordDate', recordDate)
  params.append('limit', String(limit))
  const res = await fetch(`${API_BASE_URL}/metro/timesegments?${params}`)
  const json = await res.json()
  let data = json.data || []
  // 若后端未按日期过滤，前端在此降级过滤
  if (recordDate) data = data.filter(d => String(d.recordDate) === String(recordDate))
  return data
} 

/** 创建时间段 */
export async function createTimeSegment(data) {
  const res = await fetch(`${API_BASE_URL}/time/segments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

/** 更新时间段 */
export async function updateTimeSegment(slot, data) {
  const res = await fetch(`${API_BASE_URL}/time/segments/${slot}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

/** 删除时间段 */
export async function deleteTimeSegment(slot) {
  const res = await fetch(`${API_BASE_URL}/time/segments/${slot}`, { method: 'DELETE' })
  return await res.json()
}

// ============ Weather ============
/** 获取指定日期/时间的天气记录（若后端支持按日期过滤则使用，前端也会降级过滤） */
export async function fetchWeather(recordDate = null, recordTime = null, limit = 100) {
  const params = new URLSearchParams()
  if (recordDate) params.append('recordDate', recordDate)
  if (recordTime) params.append('recordTime', recordTime)
  params.append('limit', String(limit))
  const res = await fetch(`${API_BASE_URL}/metro/weather?${params}`)
  const json = await res.json()
  let data = json.data || []
  if (recordDate) data = data.filter(d => String(d.recordDate) === String(recordDate))
  return data
} 

/** 创建/更新天气记录 */
export async function upsertWeather(data) {
  const res = await fetch(`${API_BASE_URL}/weather`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

// ============ Inflow / Outflow / ODFlow ============
/** 获取某 Slot 的进站汇总 */
export async function fetchInflowBySlot(slot) {
  const params = new URLSearchParams({ Slot: slot })
  const res = await fetch(`${API_BASE_URL}/metro/inflow?${params}`)
  const json = await res.json()
  return json.data || []
} 

/** 获取某 Slot 的出站汇总 */
export async function fetchOutflowBySlot(slot) {
  const params = new URLSearchParams({ Slot: slot })
  const res = await fetch(`${API_BASE_URL}/metro/outflow?${params}`)
  const json = await res.json()
  return json.data || []
} 

/** 获取某 Slot 的 OD 流量（分页或限制） */
export async function fetchODFlowBySlot(slot, { limit = 100, offset = 0 } = {}) {
  const params = new URLSearchParams({ slot, limit, offset })
  const res = await fetch(`${API_BASE_URL}/flow/od?${params}`)
  const json = await res.json()
  return json.data || []
}

/** 提交进站/出站/OD 数据（批量） */
export async function submitInflowBatch(records) {
  const res = await fetch(`${API_BASE_URL}/flow/inflow/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ records })
  })
  return await res.json()
}

export async function submitOutflowBatch(records) {
  const res = await fetch(`${API_BASE_URL}/flow/outflow/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ records })
  })
  return await res.json()
}

export async function submitODBatch(records) {
  const res = await fetch(`${API_BASE_URL}/flow/od/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ records })
  })
  return await res.json()
}

/** 获取某 Slot 下按站点汇总的进站量（演示聚合接口） */
export async function fetchInflowAggregate(slot) {
  const res = await fetch(`${API_BASE_URL}/flow/inflow/aggregate?slot=${encodeURIComponent(slot)}`)
  const json = await res.json()
  return json.data || []
}

/** 获取 Top N OD 对（后端目前只支持按 limit） */
export async function fetchTopOD(slot, n = 10) {
  const params = new URLSearchParams({ limit: n })
  // slot 参数若后端支持可加入 params，但目前后端按 limit 返回 top od
  const res = await fetch(`${API_BASE_URL}/metro/top-od?${params}`)
  const json = await res.json()
  return json.data || []
} 

// ============ 辅助/健康检查 ============
/** 简单健康检查，验证后端可用性 */
export async function healthCheck() {
  const res = await fetch(`${API_BASE_URL}/health`)
  const json = await res.json()
  return json
}

/** 导出为 CSV（示例调用后端导出任务） */
export async function exportODCsv(slot) {
  const res = await fetch(`${API_BASE_URL}/flow/od/export?slot=${encodeURIComponent(slot)}`)
  // 如果后端直接返回文件流，前端需要按需处理，这里返回接口响应信息
  return await res.json()
}
