<template>
  <div>
    <label for="language">Language:</label>
    <select v-model="language" id="language">
      <option value="en">English</option>
      <option value="es">Spanish</option>
      <option value="auto">Auto</option>
    </select>

    <label for="translate">Translate:</label>
    <input type="checkbox" v-model="translate" id="translate" />

    <label for="outputFormat">Output Format:</label>
    <select v-model="outputFormat" id="outputFormat">
      <option value="srt">SRT</option>
      <option value="vtt">VTT</option>
    </select>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const language = ref('en');
const translate = ref(false);
const outputFormat = ref('srt');
</script>
