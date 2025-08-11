<template>
  <div>
    <h2>Settings</h2>
    <input v-model="whisperPath" placeholder="Whisper Path" />
    <input v-model="modelPath" placeholder="Model Path" />
    <input v-model="openvinoScriptPath" placeholder="OpenVINO Script Path" />
    <button @click="saveSettings">Save</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSettingsStore } from '../stores/settings';

const settingsStore = useSettingsStore();

// 使用 ref 来创建响应式数据
const whisperPath = ref(settingsStore.whisperPath);
const modelPath = ref(settingsStore.modelPath);
const openvinoScriptPath = ref(settingsStore.openvinoScriptPath);

const saveSettings = () => {
  settingsStore.setWhisperPath(whisperPath.value);
  settingsStore.setModelPath(modelPath.value);
  settingsStore.setOpenvinoScriptPath(openvinoScriptPath.value);
};
</script>

