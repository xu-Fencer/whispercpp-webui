<template>
  <section class="card">
    <h2>任务</h2>

    <div class="row">
      <md-outlined-text-field
        label="源文件服务器路径（暂用：后端可访问的绝对路径）"
        :value="serverFilePath"
        @input="onServerFilePath"
        style="width: 520px"
      />
    </div>

    <param-basic
      :language="language"
      :translate="translate"
      :outputFormat="outputFormat"
      @update:language="(v)=> language=v"
      @update:translate="(v)=> translate=v"
      @update:outputFormat="(v)=> outputFormat=v"
    />

    <param-advanced
      :threads="threads"
      :beamSize="beamSize"
      :bestOf="bestOf"
      @update:threads="(v)=> threads=v"
      @update:beamSize="(v)=> beamSize=v"
      @update:bestOf="(v)=> bestOf=v"
    />

    <div class="row">
      <md-filled-button @click="createTask">创建任务</md-filled-button>
      <md-filled-tonal-button style="margin-left: 8px" @click="refreshStatus" :disabled="!jobId">刷新状态</md-filled-tonal-button>
    </div>

    <div class="row" v-if="jobId"><strong>Job ID:</strong> {{ jobId }}</div>
    <div class="row" v-if="statusText"><strong>状态:</strong> {{ statusText }}</div>

    <log-console v-if="jobId" :jobId="jobId" />
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { api } from '../api/client';
import { useSettingsStore } from '../stores/settings';
import ParamBasic from '../components/ParamBasic.vue';
import ParamAdvanced from '../components/ParamAdvanced.vue';
import LogConsole from '../components/LogConsole.vue';

const store = useSettingsStore();

const serverFilePath = ref('');
const language = ref('auto');
const translate = ref(false);
const outputFormat = ref('srt');

const threads = ref(4);
const beamSize = ref(5);
const bestOf = ref(5);

const jobId = ref('');
const statusText = ref('');

function onServerFilePath(e: Event) {
  serverFilePath.value = (e.target as HTMLInputElement)?.value ?? '';
}

async function createTask() {
  try {
    if (!serverFilePath.value) throw new Error('请填写后端可访问的源文件绝对路径');
    if (!store.modelPath || !store.whisperPath) throw new Error('请先到“设置”页面填写可执行与模型路径');
    const payload = {
      input_file: serverFilePath.value,
      output_format: outputFormat.value,
      whisper_exe: store.whisperPath, // 显式传递可执行路径
      whisper_params: {
        model: store.modelPath,
        threads: threads.value,
        beam_size: beamSize.value,
        best_of: bestOf.value,
        language: language.value,
        translate: translate.value ? 'true' : 'false',
      },
    };
    const res = await api.createTask(payload);
    jobId.value = (res as any).job_id || '';
    statusText.value = '任务已创建';
  } catch (e: any) {
    statusText.value = '创建失败: ' + e.message;
  }
}

async function refreshStatus() {
  try {
    if (!jobId.value) return;
    const res = await api.getTask(jobId.value);
    statusText.value = JSON.stringify(res, null, 2);
  } catch (e: any) {
    statusText.value = '获取状态失败: ' + e.message;
  }
}
</script>

<style scoped>
.card { padding: 16px; border-radius: 12px; background: var(--md-sys-color-surface); color: var(--md-sys-color-on-surface); }
.row { margin: 12px 0; display: flex; align-items: center; }
</style>
