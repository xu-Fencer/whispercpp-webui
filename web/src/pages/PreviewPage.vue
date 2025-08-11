<template>
  <section class="card">
    <h2>预览</h2>
    <div class="row">
      <md-outlined-text-field
        label="媒体文件 URL（由后端静态或文件接口提供）"
        :value="mediaUrl"
        @input="(e:any)=> mediaUrl = e.target.value"
        style="width: 520px"
      />
    </div>
    <div class="row">
      <md-outlined-text-field
        label="字幕 VTT URL"
        :value="vttUrl"
        @input="(e:any)=> vttUrl = e.target.value"
        style="width: 520px"
      />
    </div>

    <div class="player">
      <video v-if="isVideo" :src="mediaUrl" controls style="width: 100%; max-width: 800px">
        <track :src="vttUrl" kind="subtitles" srclang="en" label="Subtitles" default/>
      </video>
      <audio v-else :src="mediaUrl" controls style="width: 100%; max-width: 800px">
        <track :src="vttUrl" kind="subtitles" srclang="en" label="Subtitles" default/>
      </audio>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const mediaUrl = ref('');
const vttUrl = ref('');
const isVideo = computed(() => {
  return /\.(mp4|mkv|webm|mov)$/i.test(mediaUrl.value);
});
</script>

<style scoped>
.card { padding: 16px; border-radius: 12px; background: var(--md-sys-color-surface); color: var(--md-sys-color-on-surface); }
.row { margin: 12px 0; display: flex; align-items: center; }
.player { margin-top: 16px; }
</style>
