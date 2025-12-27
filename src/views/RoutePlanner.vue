<template>
  <div class="route-planner-container">
    <el-container>
      <!-- 顶部工具栏 -->
      <el-header class="toolbar-header">
        <div class="toolbar-left">
          <el-icon class="header-icon" :size="30" color="#409EFF">
            <Location />
          </el-icon>
          <h2>地铁导航</h2>
        </div>
        <div class="toolbar-right">
          <el-button type="primary" :icon="Plus" @click="handleAddLine">
            添加线路
          </el-button>
          <el-button type="success" :icon="Position" @click="handleAddStation">
            添加站点
          </el-button>
          <el-input
            v-model="lineName"
            placeholder="请输入线路名称"
            style="width: 200px; margin: 0 10px"
            clearable
          >
            <template #append>
              <el-button :icon="Search" @click="handleViewLine">查看单线</el-button>
            </template>
          </el-input>
          <el-button :icon="Refresh" @click="handleRestore">复原</el-button>
          <el-button v-if="isAdmin" type="info" :icon="TrendCharts" @click="goDashboard">
            管理员页
          </el-button>
          <el-button type="warning" :icon="Guide" @click="goCommute">
            嘉定推荐
          </el-button>
          <el-button type="danger" :icon="SwitchButton" @click="handleLogout">
            退出登录
          </el-button>
        </div>
      </el-header>

      <el-container>
        <!-- 主内容区域：地图 -->
        <el-main class="map-main">
          <el-card class="map-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>上海地铁线路图</span>
                <el-tag type="info" size="small">实时导航</el-tag>
              </div>
            </template>
            <div ref="mapContainer" class="map-container">
              <div class="image-map">
                <img :src="metroImage" alt="上海轨道交通网络示意图" class="metro-img" />
              </div>
              <!-- 保留占位，若后续需要切回 ECharts，可开启 -->
              <ECharts v-if="false" :option="mapChartOption" :height="mapHeight" />
            </div>
          </el-card>
        </el-main>

        <!-- 右侧边栏：路线规划 -->
        <el-aside width="350px" class="route-sidebar">
          <el-card class="route-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>路线规划</span>
              </div>
            </template>

            <!-- 站点选择 -->
            <div class="station-selector">
              <div class="station-item">
                <el-icon class="station-icon start-icon"><User /></el-icon>
                <el-select
                  v-model="startStation"
                  placeholder="请选择起始站点"
                  filterable
                  style="width: 100%"
                  @change="handleStartStationChange"
                >
                  <el-option
                    v-for="station in uniqueStations"
                    :key="station.id"
                    :label="station.name"
                    :value="station.id"
                  >
                    <span>{{ station.name }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ station.lines.join('/') }}</span>
                  </el-option>
                </el-select>
              </div>

              <div class="station-swap">
                <el-button
                  :icon="Sort"
                  circle
                  size="small"
                  @click="swapStations"
                />
              </div>

              <div class="station-item">
                <el-icon class="station-icon end-icon"><User /></el-icon>
                <el-select
                  v-model="endStation"
                  placeholder="请选择终点站点"
                  filterable
                  style="width: 100%"
                  @change="handleEndStationChange"
                >
                  <el-option
                    v-for="station in uniqueStations"
                    :key="station.id"
                    :label="station.name"
                    :value="station.id"
                  >
                    <span>{{ station.name }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ station.lines.join('/') }}</span>
                  </el-option>
                </el-select>
              </div>
            </div>

            <!-- 换乘策略 -->
            <div class="transfer-strategy">
              <div class="strategy-title">换乘策略</div>
              <el-radio-group v-model="transferStrategy" style="width: 100%">
                <el-radio label="time">时间最短</el-radio>
                <el-radio label="transfer">换乘最少</el-radio>
              </el-radio-group>
              <el-button
                type="primary"
                :icon="Search"
                style="width: 100%; margin-top: 15px"
                @click="handleSearchRoute"
              >
                开始搜索
              </el-button>
            </div>

            <!-- 换乘方案 -->
            <div v-if="routeResult.length > 0" class="route-result">
              <div class="result-title">换乘方案</div>
              <div class="route-path">
                <div
                  v-for="(station, index) in routeResult"
                  :key="index"
                  class="route-station"
                  :class="{ 'transfer-station': station.isTransfer }"
                >
                  <div class="station-dot" :class="{ 'active-dot': index === 0 || index === routeResult.length - 1 }"></div>
                  <div class="station-info">
                    <div class="station-name">{{ station.name }}</div>
                    <div v-if="station.isTransfer" class="transfer-label">换乘</div>
                    <div v-else class="station-line">{{ station.lines ? station.lines.join('/') : '' }}</div>
                  </div>
                  <div v-if="index < routeResult.length - 1" class="route-line"></div>
                </div>
              </div>
              <div class="route-summary">
                <el-tag type="success" size="small">
                  共 {{ routeResult.length - 1 }} 站
                </el-tag>
                <el-tag type="info" size="small" style="margin-left: 10px">
                  预计 {{ estimatedTime }} 分钟
                </el-tag>
                <el-tag v-if="transferCount > 0" type="warning" size="small" style="margin-left: 10px">
                  {{ transferCount }} 次换乘
                </el-tag>
              </div>
            </div>

            <el-empty
              v-else
              description="请选择起始站点和终点站点"
              :image-size="100"
            />
          </el-card>
        </el-aside>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Location,
  User,
  Plus,
  Position,
  Search,
  Refresh,
  Sort,
  TrendCharts,
  Guide,
  SwitchButton
} from '@element-plus/icons-vue'
import ECharts from '@/components/ECharts.vue'
import { getCurrentUser, logout } from '@/api/authApi'

const router = useRouter()
const metroImage = new URL('../../metroView.jpg', import.meta.url).href

// 用户角色检查
const isAdmin = computed(() => {
  const user = getCurrentUser()
  return user?.role === 'admin'
})

// 站点数据（包含邻接关系和坐标信息）
const stations = ref([
  // 9号线（从西到东）
  { id: 1, name: '七宝', lines: ['9号线'], x: 200, y: 100 },
  { id: 2, name: '星中路', lines: ['9号线'], x: 250, y: 100 },
  { id: 3, name: '合川路', lines: ['9号线'], x: 300, y: 100 },
  { id: 4, name: '漕河泾开发区', lines: ['9号线'], x: 350, y: 100 },
  { id: 5, name: '桂林路', lines: ['9号线'], x: 400, y: 100 },
  { id: 6, name: '宜山路', lines: ['3号线', '4号线', '9号线'], x: 450, y: 100, isTransfer: true },
  { id: 7, name: '徐家汇', lines: ['1号线', '9号线', '11号线'], x: 500, y: 100, isTransfer: true },
  { id: 8, name: '衡山路', lines: ['1号线'], x: 550, y: 100 },
  
  // 1号线（从西到东）
  { id: 9, name: '人民广场', lines: ['1号线', '2号线', '8号线'], x: 600, y: 150, isTransfer: true },
  
  // 2号线（从西到东）
  { id: 10, name: '虹桥火车站', lines: ['2号线', '10号线'], x: 150, y: 200, isTransfer: true },
  { id: 11, name: '静安寺', lines: ['2号线', '7号线'], x: 550, y: 200, isTransfer: true },
  { id: 12, name: '人民广场', lines: ['1号线', '2号线', '8号线'], x: 600, y: 150, isTransfer: true },
  { id: 13, name: '南京东路', lines: ['2号线', '10号线'], x: 650, y: 200, isTransfer: true },
  { id: 14, name: '陆家嘴', lines: ['2号线'], x: 700, y: 200 },
  
  // 10号线
  { id: 15, name: '三门路', lines: ['10号线'], x: 100, y: 250 },
  { id: 16, name: '虹桥火车站', lines: ['2号线', '10号线'], x: 150, y: 200, isTransfer: true },
  { id: 17, name: '世纪大道', lines: ['2号线', '4号线', '6号线', '9号线'], x: 650, y: 250, isTransfer: true },
  { id: 18, name: '南京东路', lines: ['2号线', '10号线'], x: 650, y: 200, isTransfer: true }
])

// 邻接关系（根据Neighbour表设计）
const stationConnections = ref([
  // 9号线连接
  { from: 1, to: 2, line: '9号线', time: 2 }, // 七宝 -> 星中路
  { from: 2, to: 3, line: '9号线', time: 2 }, // 星中路 -> 合川路
  { from: 3, to: 4, line: '9号线', time: 2 }, // 合川路 -> 漕河泾开发区
  { from: 4, to: 5, line: '9号线', time: 2 }, // 漕河泾开发区 -> 桂林路
  { from: 5, to: 6, line: '9号线', time: 2 }, // 桂林路 -> 宜山路
  { from: 6, to: 7, line: '9号线', time: 2 }, // 宜山路 -> 徐家汇
  { from: 7, to: 8, line: '1号线', time: 2 }, // 徐家汇 -> 衡山路 (1号线)
  { from: 8, to: 9, line: '1号线', time: 2 }, // 衡山路 -> 人民广场 (1号线)
  
  // 2号线连接
  { from: 10, to: 11, line: '2号线', time: 3 }, // 虹桥火车站 -> 静安寺
  { from: 11, to: 12, line: '2号线', time: 3 }, // 静安寺 -> 人民广场
  { from: 12, to: 13, line: '2号线', time: 2 }, // 人民广场 -> 南京东路
  { from: 13, to: 14, line: '2号线', time: 2 }, // 南京东路 -> 陆家嘴
  
  // 10号线连接
  { from: 15, to: 16, line: '10号线', time: 3 }, // 三门路 -> 虹桥火车站
  { from: 16, to: 18, line: '10号线', time: 5 }, // 虹桥火车站 -> 南京东路
  
  // 换乘站之间的连接（同一站点不同线路间的换乘）
  { from: 6, to: 6, line: '换乘', time: 5, isTransfer: true }, // 宜山路换乘
  { from: 7, to: 9, line: '换乘', time: 5, isTransfer: true }, // 徐家汇换乘到人民广场
  { from: 12, to: 12, line: '换乘', time: 5, isTransfer: true }, // 人民广场换乘
  { from: 13, to: 18, line: '换乘', time: 3, isTransfer: true }, // 南京东路换乘
])

// 构建邻接表
const adjacencyList = ref(new Map())

// 去重站点（相同名称的站点合并）
const uniqueStations = computed(() => {
  const stationMap = new Map()
  stations.value.forEach(station => {
    if (!stationMap.has(station.name)) {
      stationMap.set(station.name, station)
    } else {
      // 合并相同名称站点的线路信息
      const existing = stationMap.get(station.name)
      const allLines = [...new Set([...existing.lines, ...station.lines])]
      stationMap.set(station.name, {
        ...existing,
        lines: allLines,
        isTransfer: existing.isTransfer || station.isTransfer
      })
    }
  })
  return Array.from(stationMap.values())
})

const startStation = ref(null)
const endStation = ref(null)
const lineName = ref('')
const transferStrategy = ref('time')
const routeResult = ref([])
const mapHeight = ref('600px')
const mapContainer = ref(null)

// 地图图表配置
const mapChartOption = ref({
  backgroundColor: '#fff',
  title: {
    text: '上海地铁线路图',
    left: 'center',
    top: 10,
    textStyle: {
      fontSize: 18,
      fontWeight: 'bold'
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      if (params.dataType === 'node') {
        return `${params.data.name}<br/>${params.data.line || ''}`
      }
      if (params.dataType === 'edge') {
        return `${params.data.source} → ${params.data.target}`
      }
      return ''
    }
  },
  series: [
    {
      type: 'graph',
      layout: 'none',
      data: [],
      links: [],
      categories: [],
      roam: true,
      draggable: true,
      label: {
        show: true,
        position: 'right',
        formatter: '{b}',
        fontSize: 12
      },
      lineStyle: {
        color: '#409EFF',
        width: 2,
        curveness: 0.3
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 4
        },
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 2
      },
    }
  ]
})

// 计算属性
const transferCount = computed(() => {
  return routeResult.value.filter(station => station.isTransfer).length
})

const estimatedTime = computed(() => {
  // 每站2分钟，每次换乘额外5分钟
  return (routeResult.value.length - 1) * 2 + transferCount.value * 5
})

// 构建邻接表
const buildAdjacencyList = () => {
  adjacencyList.value.clear()
  
  // 初始化所有站点的邻接列表
  stations.value.forEach(station => {
    adjacencyList.value.set(station.id, [])
  })
  
  // 添加连接关系
  stationConnections.value.forEach(conn => {
    if (conn.from !== conn.to) { // 排除换乘站的自环
      const neighbors = adjacencyList.value.get(conn.from) || []
      neighbors.push({
        to: conn.to,
        line: conn.line,
        time: conn.time,
        isTransfer: conn.isTransfer || false
      })
      adjacencyList.value.set(conn.from, neighbors)
      
      // 双向连接
      const reverseNeighbors = adjacencyList.value.get(conn.to) || []
      reverseNeighbors.push({
        to: conn.from,
        line: conn.line,
        time: conn.time,
        isTransfer: conn.isTransfer || false
      })
      adjacencyList.value.set(conn.to, reverseNeighbors)
    }
  })
}

// 初始化地图
const initMap = () => {
  // 构建邻接表
  buildAdjacencyList()
  
  // 生成站点节点数据，使用固定坐标（基于uniqueStations）
  const nodes = uniqueStations.value.map((station, index) => {
    return {
      id: station.id,
      name: station.name,
      lines: station.lines || [],
      x: station.x || (100 + (index % 8) * 100),
      y: station.y || (100 + Math.floor(index / 8) * 80),
      symbolSize: station.isTransfer ? 40 : 30,
      itemStyle: {
        color: station.isTransfer ? '#E6A23C' : '#409EFF',
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        position: (station.x && station.x > 600) ? 'left' : 'right',
        fontSize: 12,
        fontWeight: station.isTransfer ? 'bold' : 'normal'
      },
      category: station.isTransfer ? 1 : 0
    }
  })

  // 生成连接线（基于邻接关系）
  const links = []
  const addedLinks = new Set() // 避免重复连接
  
  stationConnections.value.forEach(conn => {
    if (conn.from !== conn.to) {
      const linkKey = `${Math.min(conn.from, conn.to)}-${Math.max(conn.from, conn.to)}`
      if (!addedLinks.has(linkKey)) {
        addedLinks.add(linkKey)
        
        // 根据线路设置不同颜色
        let lineColor = '#409EFF'
        if (conn.line.includes('1号线')) lineColor = '#E4002B'
        else if (conn.line.includes('2号线')) lineColor = '#6FB44B'
        else if (conn.line.includes('3号线')) lineColor = '#FDB913'
        else if (conn.line.includes('4号线')) lineColor = '#5F259F'
        else if (conn.line.includes('9号线')) lineColor = '#71C5E8'
        else if (conn.line.includes('10号线')) lineColor = '#C1A7E2'
        
        links.push({
          source: conn.from,
          target: conn.to,
          line: conn.line,
          lineStyle: {
            color: lineColor,
            width: conn.isTransfer ? 3 : 2,
            type: conn.isTransfer ? 'dashed' : 'solid'
          },
          label: {
            show: false
          }
        })
      }
    }
  })

  // 重置系列数据
  mapChartOption.value.series[0].data = nodes
  mapChartOption.value.series[0].links = links
}

const highlightRoute = (routeStations) => {
  if (routeStations.length === 0) return

  const nodeIds = routeStations.map(s => s.id)
  
  // 创建高亮的连接线
  const highlightedLinks = []
  for (let i = 0; i < routeStations.length - 1; i++) {
    highlightedLinks.push({
      source: routeStations[i].id,
      target: routeStations[i + 1].id,
      lineStyle: {
        color: '#F56C6C',
        width: 5
      }
    })
  }

  // 更新节点颜色和样式
  const allNodes = mapChartOption.value.series[0].data.map(node => {
    if (nodeIds.includes(node.id)) {
      return {
        ...node,
        symbolSize: 40,
        itemStyle: {
          color: '#F56C6C',
          borderColor: '#fff',
          borderWidth: 4
        },
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      }
    }
    return {
      ...node,
      symbolSize: 30,
      itemStyle: {
        color: '#409EFF',
        borderColor: '#fff',
        borderWidth: 2
      }
    }
  })

  // 创建新的系列来显示高亮路线
  const baseSeries = {
    ...mapChartOption.value.series[0],
    data: allNodes,
    lineStyle: {
      color: '#409EFF',
      width: 2
    }
  }

  // 高亮系列
  const highlightSeries = {
    type: 'graph',
    layout: 'none',
    data: allNodes.filter(node => nodeIds.includes(node.id)),
    links: highlightedLinks,
    roam: true,
    draggable: false,
    lineStyle: {
      color: '#F56C6C',
      width: 5
    },
    label: {
      show: true,
      fontSize: 14,
      fontWeight: 'bold'
    },
    itemStyle: {
      color: '#F56C6C',
      borderColor: '#fff',
      borderWidth: 4
    },
    emphasis: {
      focus: 'adjacency'
    },
  }

  mapChartOption.value.series = [baseSeries, highlightSeries]
}

// 构建静态图叠加层路径
const buildOverlay = () => {
  if (!routeResult.value || routeResult.value.length === 0) {
    overlayPath.value = []
    overlayDots.value = []
    return
  }

  const points = []
  const dots = []

  routeResult.value.forEach((station, idx) => {
    const coord = getCoord(station.name) || getCoord(`${station.name}-${station.lines?.[0] || ''}`)
    if (!coord) return

    points.push({ x: coord.x, y: coord.y })
    dots.push({
      x: coord.x,
      y: coord.y,
      name: station.name,
      isStart: idx === 0,
      isEnd: idx === routeResult.value.length - 1,
      isTransfer: station.isTransfer,
      color: station.isTransfer ? '#f59e0b' : '#2563eb'
    })
  })

  overlayPath.value = points
  overlayDots.value = dots
}

// 搜索路线
const handleSearchRoute = () => {
  if (!startStation.value || !endStation.value) {
    ElMessage.warning('请选择起始站点和终点站点')
    return
  }

  if (startStation.value === endStation.value) {
    ElMessage.warning('起始站点和终点站点不能相同')
    overlayPath.value = []
    overlayDots.value = []
    return
  }

  // 路线搜索算法（实际应调用后端API）
  const start = uniqueStations.value.find(s => s.id === startStation.value)
  const end = uniqueStations.value.find(s => s.id === endStation.value)
  
  if (!start || !end) {
    ElMessage.error('站点信息错误')
    return
  }

  // 简单的路径查找（实际应该使用图算法如Dijkstra）
  const route = findRoute(start, end)
  routeResult.value = route

  // 高亮显示路线
  highlightRoute(route)

  ElMessage.success('路线规划完成')
}

// Dijkstra算法查找最短路径
const dijkstra = (startId, endId, prioritizeTransfers = false) => {
  const distances = new Map()
  const previous = new Map()
  const visited = new Set()
  const queue = []
  
  // 初始化距离
  stations.value.forEach(station => {
    distances.set(station.id, station.id === startId ? 0 : Infinity)
    previous.set(station.id, null)
    queue.push(station.id)
  })
  
  // 主循环
  while (queue.length > 0) {
    // 找到距离最小的未访问节点
    let minId = queue[0]
    let minDist = distances.get(minId)
    
    for (const id of queue) {
      const dist = distances.get(id)
      if (dist < minDist) {
        minDist = dist
        minId = id
      }
    }
    
    // 移除已访问节点
    queue.splice(queue.indexOf(minId), 1)
    visited.add(minId)
    
    // 如果到达终点，构建路径
    if (minId === endId) {
      const path = []
      let current = endId
      
      while (current !== null) {
        const station = stations.value.find(s => s.id === current)
        if (station) {
          path.unshift({
            id: station.id,
            name: station.name,
            lines: station.lines,
            isTransfer: station.isTransfer || false
          })
        }
        current = previous.get(current)
      }
      
      // 标记换乘站
      for (let i = 1; i < path.length - 1; i++) {
        const prevStation = stations.value.find(s => s.id === path[i - 1].id)
        const currStation = stations.value.find(s => s.id === path[i].id)
        
        // 如果前后站点不在同一线路，当前站点是换乘站
        const prevLines = new Set(prevStation?.lines || [])
        const currLines = new Set(currStation?.lines || [])
        const commonLines = [...prevLines].filter(line => currLines.has(line))
        
        if (commonLines.length === 0 && currStation?.isTransfer) {
          path[i].isTransfer = true
        }
      }
      
      return path
    }
    
    // 更新邻接节点的距离
    const neighbors = adjacencyList.value.get(minId) || []
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor.to)) {
        // 计算新的距离（考虑换乘时间）
        let newDist = distances.get(minId) + neighbor.time
        if (prioritizeTransfers && neighbor.isTransfer) {
          newDist += 3 // 换乘惩罚
        }
        
        if (newDist < distances.get(neighbor.to)) {
          distances.set(neighbor.to, newDist)
          previous.set(neighbor.to, minId)
        }
      }
    }
  }
  
  return [] // 未找到路径
}

// BFS算法查找最少换乘路径
const bfsMinTransfers = (startId, endId) => {
  const queue = [[startId]]
  const visited = new Set([startId])
  
  while (queue.length > 0) {
    const path = queue.shift()
    const currentId = path[path.length - 1]
    
    if (currentId === endId) {
      // 构建完整路径
      return path.map(id => {
        const station = stations.value.find(s => s.id === id)
        return {
          id: station.id,
          name: station.name,
          lines: station.lines,
          isTransfer: station.isTransfer || false
        }
      })
    }
    
    const neighbors = adjacencyList.value.get(currentId) || []
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor.to)) {
        visited.add(neighbor.to)
        queue.push([...path, neighbor.to])
      }
    }
  }
  
  return []
}

// 路线查找（根据策略选择算法）
const findRoute = (start, end) => {
  if (start.id === end.id) {
    return [start]
  }
  
  buildAdjacencyList() // 确保邻接表已构建
  
  if (transferStrategy.value === 'time') {
    // 时间最短：使用Dijkstra算法
    return dijkstra(start.id, end.id, false)
  } else {
    // 换乘最少：使用BFS算法
    const route = bfsMinTransfers(start.id, end.id)
    // 对路径进行优化，合并同线路的连续站点
    return optimizeRoute(route)
  }
}

// 优化路线，标记换乘站点
const optimizeRoute = (route) => {
  if (route.length <= 2) return route
  
  const optimized = [route[0]]
  
  for (let i = 1; i < route.length - 1; i++) {
    const prev = stations.value.find(s => s.id === route[i - 1].id)
    const curr = stations.value.find(s => s.id === route[i].id)
    const next = stations.value.find(s => s.id === route[i + 1].id)
    
    // 检查是否换乘
    const prevLines = new Set(prev?.lines || [])
    const currLines = new Set(curr?.lines || [])
    const nextLines = new Set(next?.lines || [])
    
    const prevCommon = [...prevLines].filter(l => currLines.has(l))
    const nextCommon = [...currLines].filter(l => nextLines.has(l))
    const allCommon = prevCommon.filter(l => nextCommon.has(l))
    
    // 如果前后共同线路为空，说明需要换乘
    if (allCommon.length === 0 && curr?.isTransfer) {
      optimized.push({
        ...route[i],
        isTransfer: true
      })
    } else {
      optimized.push(route[i])
    }
  }
  
  optimized.push(route[route.length - 1])
  return optimized
}

// 交换起始和终点
const swapStations = () => {
  const temp = startStation.value
  startStation.value = endStation.value
  endStation.value = temp
  if (routeResult.value.length > 0) {
    routeResult.value = routeResult.value.reverse()
    highlightRoute(routeResult.value)
  }
}

// 站点变化处理
const handleStartStationChange = () => {
  if (routeResult.value.length > 0) {
    routeResult.value = []
    initMap() // 重置地图
  }
}

const handleEndStationChange = () => {
  if (routeResult.value.length > 0) {
    routeResult.value = []
    initMap() // 重置地图
  }
}

// 工具按钮处理
const handleAddLine = () => {
  ElMessage.info('添加线路功能开发中')
}

const handleAddStation = () => {
  ElMessage.info('添加站点功能开发中')
}

const handleViewLine = () => {
  if (!lineName.value) {
    ElMessage.warning('请输入线路名称')
    return
  }
  ElMessage.success(`查看 ${lineName.value} 线路`)
}

const goDashboard = () => {
  router.push('/dashboard')
}

const goCommute = () => {
  router.push('/commute')
}

const handleLogout = () => {
  logout()
  router.push('/login')
}

// 地图缩放与平移
const handleRestore = () => {
  routeResult.value = []
  startStation.value = null
  endStation.value = null
  initMap()
  ElMessage.success('已复原')
}

onMounted(() => {
  // 设置地图高度
  mapHeight.value = `${window.innerHeight - 200}px`
  initMap()

  // 窗口大小变化时更新地图高度
  window.addEventListener('resize', () => {
    mapHeight.value = `${window.innerHeight - 200}px`
  })
})
</script>

<style scoped>
.route-planner-container {
  width: 100%;
  min-height: 100vh;
  background:
    radial-gradient(circle at 20% 15%, rgba(102, 126, 234, 0.14), transparent 28%),
    radial-gradient(circle at 85% 10%, rgba(118, 75, 162, 0.18), transparent 30%),
    linear-gradient(135deg, #f7f9ff 0%, #eef2ff 40%, #f9fbff 100%);
}

.toolbar-header {
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  box-shadow: 0 12px 32px rgba(31, 41, 55, 0.08);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 20;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toolbar-left h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.map-main {
  padding: 20px;
  background: transparent;
}

.map-card {
  height: calc(100vh - 100px);
  border-radius: 16px;
  border: 1px solid #eef0f6;
  box-shadow: 0 20px 45px rgba(31, 41, 55, 0.08);
  background: #ffffff;
}

.map-container {
  height: calc(100vh - 200px);
  min-height: 620px;
  width: 100%;
  overflow: hidden;
}

.image-map {
  position: relative;
  height: 100%;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #f8fafc;
  border: 1px solid #eef0f6;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.metro-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.route-sidebar {
  background: transparent;
  padding: 20px;
  overflow-y: auto;
}

.route-card {
  border-radius: 16px;
  border: 1px solid #eef0f6;
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

.station-selector {
  margin-bottom: 30px;
}

.station-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.station-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.start-icon {
  color: #22c55e;
}

.end-icon {
  color: #ef4444;
}

.station-swap {
  text-align: center;
  margin: 10px 0;
}

.transfer-strategy {
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(145deg, #ffffff, #f6f7fb);
  border-radius: 12px;
  border: 1px solid #eef0f6;
}

.strategy-title {
  font-weight: 700;
  margin-bottom: 15px;
  color: #0f172a;
}

.route-result {
  margin-top: 20px;
}

.result-title {
  font-weight: 700;
  margin-bottom: 20px;
  color: #0f172a;
}

.route-path {
  position: relative;
  padding-left: 30px;
}

.route-station {
  position: relative;
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.station-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #409EFF;
  border: 2px solid #fff;
  position: absolute;
  left: -24px;
  top: 6px;
  z-index: 2;
  box-shadow: 0 0 0 6px rgba(64, 158, 255, 0.12);
}

.active-dot {
  width: 16px;
  height: 16px;
  left: -26px;
  top: 4px;
}

.route-line {
  position: absolute;
  left: -18px;
  top: 18px;
  width: 2px;
  height: calc(100% + 10px);
  background: linear-gradient(180deg, #3b82f6 0%, #6366f1 100%);
  z-index: 1;
}

.route-station:last-child .route-line {
  display: none;
}

.station-info {
  flex: 1;
}

.station-name {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 5px;
}

.station-line {
  font-size: 12px;
  color: #6b7280;
}

.transfer-label {
  font-size: 12px;
  color: #eab308;
  font-weight: 700;
}

.transfer-station .station-dot {
  background: #eab308;
  box-shadow: 0 0 0 6px rgba(234, 179, 8, 0.12);
}

.route-summary {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .toolbar-header {
    flex-direction: column;
    height: auto;
    padding: 15px;
    gap: 15px;
  }

  .toolbar-right {
    flex-wrap: wrap;
    gap: 10px;
  }

  .route-sidebar {
    width: 100% !important;
  }
}
</style>

