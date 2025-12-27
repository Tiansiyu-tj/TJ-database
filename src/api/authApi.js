// 用户认证 API
const API_BASE_URL = 'http://localhost:8000/api'

/**
 * 用户注册
 */
export async function register(username, password, email) {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, email })
    })
    return await res.json()
}

/**
 * 用户登录
 */
export async function login(username, password) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    const json = await res.json()

    // 登录成功，保存用户信息到 localStorage
    if (json.code === 0 && json.data) {
        localStorage.setItem('user', JSON.stringify(json.data))
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('username', json.data.username)
    }

    return json
}

/**
 * 退出登录
 */
export function logout() {
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('username')
}

/**
 * 获取当前登录用户
 */
export function getCurrentUser() {
    const userStr = localStorage.getItem('user')
    if (userStr) {
        try {
            return JSON.parse(userStr)
        } catch {
            return null
        }
    }
    return null
}

/**
 * 检查是否已登录
 */
export function isLoggedIn() {
    return !!getCurrentUser()
}

/**
 * 获取用户信息
 */
export async function getUserInfo(userId) {
    const res = await fetch(`${API_BASE_URL}/auth/me?userId=${userId}`)
    return await res.json()
}
