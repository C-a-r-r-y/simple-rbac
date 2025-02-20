<template>
  <el-dialog v-model="dialogVisible" :title="props.mode === 'create' ? '创建用户' : '修改用户信息'">
    <el-form :model="editForm">
      <el-form-item v-if="props.mode === 'edit'" label="用户ID">
        <el-input v-model="editForm.id" disabled />
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="editForm.username" />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="editForm.role">
          <el-option label="系统管理员" value="system_admin" />
          <el-option label="管理员" value="admin" />
          <el-option label="普通用户" value="user" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="props.mode === 'create'" label="密码">
        <el-input v-model="editForm.password" type="password" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="editForm.description" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleConfirm">确认</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UserResponse, UserCreate } from '@/api/types'
import { userService } from '@/api/userService'

const props = defineProps<{
  mode: 'create' | 'edit',
  userId?: number
}>()

const dialogVisible = ref(false)
const options = ref<{ userId?: number, mode?: 'create' | 'edit', onConfirm?: () => void }>({})
const editForm = ref<UserResponse & { password?: string }>({
  id: 0,
  username: '',
  role: 'user',
  description: '',
  created_at: '',
  updated_at: '',
  password: ''
})

const emit = defineEmits(['confirm'])

const open = async (opts: { userId?: number, mode?: 'create' | 'edit', onConfirm?: () => void }) => {
  options.value = opts
  if (options.value.mode === 'edit' && options.value.userId) {
    const user = await userService.getUser(options.value.userId)
    editForm.value = { ...user }
  } else {
    editForm.value = {
    id: 0,
    username: '',
    role: 'user',
    description: '',
    created_at: '',
    updated_at: ''
    }
  }
  if (options.value.onConfirm) {
    emit('confirm', options.value.onConfirm)
  }
  dialogVisible.value = true
}

const handleConfirm = async () => {
  try {
    if (props.mode === 'create') {
      // 调用创建用户API
      const { id, created_at, updated_at, ...createData } = editForm.value
      if (!createData.password) {
        throw new Error('密码不能为空')
      }
      if (!/^\d{6,}$/.test(createData.password)) {
        throw new Error('密码必须为6位或以上的数字')
      }
      await userService.createUser({
        username: createData.username,
        password: createData.password,
        role: createData.role,
        description: createData.description
      } as UserCreate)
    } else {
      // 调用更新用户API
      const { id, created_at, updated_at, ...updateData } = editForm.value
      await userService.updateUser(id, updateData)
    }
    emit('confirm', editForm.value)
    if (options.value.onConfirm) {
      options.value.onConfirm()
    }
    ElMessage({
      type: 'success',
      message: props.mode === 'create' ? '用户创建成功' : '用户信息更新成功'
    })
    dialogVisible.value = false
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage({
      type: 'error',
      message: props.mode === 'create' ? '用户创建失败' : '用户信息更新失败'
    })
  }
}

defineExpose({
  open,
  handleConfirm
})
</script>