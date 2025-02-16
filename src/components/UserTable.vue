<template>
  <el-table :data="users" style="width: 100%">
    <el-table-column prop="id" label="ID" width="100" />
    <el-table-column prop="username" label="用户名" />
    <el-table-column prop="role" label="角色" />
    <el-table-column prop="description" label="描述" />
    <el-table-column prop="createdAt" label="创建时间" width="180">
      <template #default="scope">
        {{ new Date(scope.row.createdAt).toLocaleString() }}
      </template>
    </el-table-column>
    <el-table-column prop="updatedAt" label="更新时间" width="180">
      <template #default="scope">
        {{ new Date(scope.row.updatedAt).toLocaleString() }}
      </template>
    </el-table-column>
    <el-table-column label="操作" width="150" v-if="isAdmin">
      <template #default="scope">
        <el-button type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <EditUserDialog ref="editDialogRef" mode="edit" />
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { userService } from '../api/userService';
import { userStore } from '../store/userStore';
import type { UserResponse } from '../api/types';
import EditUserDialog from './EditUserDialog.vue';

const store = userStore();
const users = ref<UserResponse[]>([]);
const isAdmin = store.isAdmin;

const fetchUsers = async () => {
  try {
    users.value = await userService.getUsers();
  } catch (error) {
    console.error('获取用户列表失败:', error);
  }
};

const editDialogRef = ref<InstanceType<typeof EditUserDialog>>();

const handleEdit = (user: UserResponse) => {
  editDialogRef.value?.open();
  editDialogRef.value?.$emit('confirm', () => {
    fetchUsers();
  });
};

const handleDelete = async (user: UserResponse) => {
  try {
    await userService.deleteUser(user.id);
    await fetchUsers();
  } catch (error) {
    console.error('删除用户失败:', error);
  }
};

onMounted(() => {
  fetchUsers();
});
</script>
