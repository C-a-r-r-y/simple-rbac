<template>
  <div class="login-container">
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
    await store.login(username, password)
    router.push({ name: 'manage' })
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
}
</style>