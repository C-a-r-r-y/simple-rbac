<template>
  <div class="login-container">
    <h2 class="login-title">用户登录</h2>
    <el-form :model="form" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { userStore } from '@/store/userStore'
import { ElMessage } from 'element-plus'

interface LoginForm {
  username: string
  password: string
}

const router = useRouter()
const store = userStore()

const form = ref<LoginForm>({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    const { username, password } = form.value
    if (!username || !password) {
      throw new Error('用户名和密码不能为空')
    }
    await store.login(username, password)
    router.push({ name: 'manage' })
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  font-size: 24px;
}

.el-form-item {
  margin-bottom: 24px;
}

.el-input {
  width: 100%;
}

.el-button {
  width: 100%;
  margin-top: 16px;
}

@media (max-width: 480px) {
  .login-container {
    margin: 50px 20px;
    padding: 30px;
  }
}
</style>