<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <el-icon class="metro-icon" :size="60" color="#409EFF">
          <Location />
        </el-icon>
        <h1>上海地铁交通系统</h1>
        <p>Shanghai Metro System</p>
      </div>
      
      <!-- 登录表单 -->
      <el-form
        v-if="!isRegister"
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 注册表单 -->
      <el-form
        v-else
        class="login-form"
        @submit.prevent="handleRegister"
      >
        <el-form-item>
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            size="large"
            prefix-icon="Message"
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="确认密码"
            size="large"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <el-button type="primary" link @click="toggleMode">
          {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
        </el-button>
        <el-text type="info" size="small" style="display: block; margin-top: 8px;">
          演示账号：admin / admin123
        </el-text>
      </div>
    </div>
    
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Location } from '@element-plus/icons-vue'
import { login, register } from '@/api/authApi'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)
const isRegister = ref(false)  // 切换登录/注册模式

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const res = await login(loginForm.username, loginForm.password)
        if (res.code === 0) {
          ElMessage.success('登录成功')
          router.push('/commute')
        } else {
          ElMessage.error(res.message || '登录失败')
        }
      } catch (e) {
        ElMessage.error('网络错误，请检查后端服务')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleRegister = async () => {
  const form = registerForm
  
  if (!form.username || !form.email || !form.password) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  if (form.password !== form.confirmPassword) {
    ElMessage.warning('两次密码不一致')
    return
  }
  
  loading.value = true
  try {
    const res = await register(form.username, form.password, form.email)
    if (res.code === 0) {
      ElMessage.success('注册成功，请登录')
      isRegister.value = false
      loginForm.username = form.username
    } else {
      ElMessage.error(res.message || '注册失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  } finally {
    loading.value = false
  }
}

const toggleMode = () => {
  isRegister.value = !isRegister.value
}
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  background:
    radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.28), transparent 35%),
    radial-gradient(circle at 80% 10%, rgba(118, 75, 162, 0.32), transparent 35%),
    linear-gradient(135deg, #0f172a 0%, #111827 40%, #0f172a 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.login-box {
  width: 440px;
  padding: 48px 42px;
  border-radius: 22px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(248, 249, 255, 0.92));
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px);
  z-index: 10;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.metro-icon {
  margin-bottom: 15px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.login-header h1 {
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
  letter-spacing: 1px;
}

.login-header p {
  font-size: 14px;
  color: #6b7280;
  letter-spacing: 2px;
}

.login-form {
  margin-top: 30px;
}

.login-button {
  width: 100%;
  height: 46px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 15px 30px rgba(64, 158, 255, 0.35);
}

.login-footer {
  text-align: center;
  margin-top: 18px;
}

.background-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  animation: pulse 5s ease-in-out infinite;
  filter: blur(1px);
}

.circle-1 {
  width: 340px;
  height: 340px;
  top: -120px;
  right: -120px;
  animation-delay: 0s;
}

.circle-2 {
  width: 220px;
  height: 220px;
  bottom: -40px;
  left: -60px;
  animation-delay: 1s;
}

.circle-3 {
  width: 180px;
  height: 180px;
  top: 55%;
  left: 12%;
  animation-delay: 2s;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.45;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

@media (max-width: 768px) {
  .login-box {
    width: 90%;
    padding: 40px 30px;
  }
}
</style>

