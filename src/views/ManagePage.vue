<template>
  <div class="manage-page">
    <el-card class="page-container">
      <div class="page-header">
        <div class="user-info">
          <h2 class="page-title">用户管理</h2>
          <div class="user-detail">
            <span class="username">{{ userStore.username }}</span>
            <span class="role">({{ userStore.role }})</span>
          </div>
        </div>
        <el-button
          type="danger"
          class="logout-btn"
          @click="handleLogout"
        >
          登出
        </el-button>
      </div>
      <UserTable/>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userStore as store } from '@/store/userStore'
import { userService } from '@/api/userService'
import type { UserResponse } from '@/api/types'
import UserTable from '@/components/UserTable.vue'

const router = useRouter()
const userStore = store()

const userList = ref<UserResponse[]>([])

const fetchUserList = async () => {
  try {
    const data = await userService.getUsers()
    userList.value = data
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'login' })
}

onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.manage-page {
  padding: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-detail {
  margin-top: 4px;
  color: #606266;
  font-size: 14px;
}

.username {
  font-weight: 500;
}

.role {
  margin-left: 8px;
  color: #909399;
}

.logout-btn {
  margin-bottom: 20px;
  float: right;
}
</style>