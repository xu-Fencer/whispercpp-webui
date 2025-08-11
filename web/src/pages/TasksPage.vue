<template>
  <div>
    <h2>Task Management</h2>
    <file-picker />
    <param-basic />
    <button @click="createTask">Create Task</button>
    <div v-if="taskStatus">Status: {{ taskStatus }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSettingsStore } from '../stores/settings';
import ParamBasic from '../components/ParamBasic.vue';
import FilePicker from '../components/FilePicker.vue';

const taskStatus = ref('');
const settingsStore = useSettingsStore();

const createTask = () => {
  // 任务创建逻辑
  taskStatus.value = 'Task Created';
};
</script>
