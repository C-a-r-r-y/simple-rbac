<template>
  <div class="manage-page">
    <el-menu
      mode="horizontal"
      class="nav-bar"
    >
      <el-menu-item index="1" class="nav-title">欢迎</el-menu-item>
      <el-menu-item index="2" class="user-info">
        <div class="user-detail">
          <span class="username">{{ userStore.username }}</span>
          <span class="role">({{ userStore.role }})</span>
        </div>
      </el-menu-item>
      <el-menu-item index="3">
        <el-button
          type="danger"
          class="logout-btn"
          @click="handleLogout"
        >
          登出
        </el-button>
      </el-menu-item>
    </el-menu>
    <el-card class="page-container">
      <el-text class="system-title" type="primary" size="large" tag="h1">
        用户管理系统
      </el-text>
      <el-button
        type="primary"
        class="create-btn"
        @click="handleCreateUser"
        v-if="userStore.isAdmin"
      >
        创建用户
      </el-button>
      <UserTable/>
      <EditUserDialog ref="editUserDialog" mode="create" />
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
import EditUserDialog from '@/components/EditUserDialog.vue'

const router = useRouter()
const userStore = store()

const editUserDialog = ref<InstanceType<typeof EditUserDialog>>()
const userTableRef = ref<InstanceType<typeof UserTable>>()

const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'login' })
}

const handleCreateUser = () => {
  editUserDialog.value?.open({
    mode: 'create',
    onConfirm: () => {
      userTableRef.value?.fetchUsers()
      console.log('用户创建成功，刷新用户列表')
    }
  })
}

onMounted(() => {
  userTableRef.value?.fetchUsers()
})
</script>

<style scoped>
.manage-page {
  padding: 20px;
}

.nav-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-title {
  font-size: 18px;
  font-weight: bold;
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
  margin: 0;
}

.system-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 500;
  letter-spacing: 1px;
}
</style>