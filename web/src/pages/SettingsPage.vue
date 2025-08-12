<template>
  <section class="card">
    <h2>设置</h2>

    <div class="row">
      <md-outlined-text-field
        label="Whisper 可执行文件路径"
        :value="whisperPath"
        @input="onWhisperPath"
        style="width: 520px"
      />
    </div>

    <div class="row">
      <md-outlined-text-field
        label="模型文件路径（.bin/.gguf）"
        :value="modelPath"
        @input="onModelPath"
        style="width: 520px"
      />
    </div>

    <div class="row">
      <md-outlined-text-field
        label="OpenVINO 初始化脚本路径（.bat/.sh）"
        :value="openvinoScriptPath"
        @input="onOpenvinoScriptPath"
        style="width: 520px"
      />
    </div>

    <div class="row">
      <md-switch
        :selected="openvinoEnabled"
        @change="onOpenvinoEnabled"
      ></md-switch>
      <span style="margin-left:8px">每次运行前执行 OpenVINO 初始化脚本</span>
    </div>

    <div class="row">
      <md-filled-tonal-button @click="save">保存设置</md-filled-tonal-button>
      <md-filled-button style="margin-left: 8px" @click="testOpenVINO">测试 OpenVINO 脚本</md-filled-button>
      <md-filled-button style="margin-left: 8px" @click="probe">探测环境</md-filled-button>
    </div>

    <pre v-if="message" class="msg">{{ message }}</pre>
    <pre v-if="probeResult" class="msg">{{ probeResult }}</pre>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { api } from '../api/client';
import { useSettingsStore } from '../stores/settings';

const store = useSettingsStore();

const whisperPath = ref(store.whisperPath);
const modelPath = ref(store.modelPath);
const openvinoScriptPath = ref(store.openvinoScriptPath);
const openvinoEnabled = ref(store.openvinoEnabled);

const message = ref('');
const probeResult = ref('');

onMounted(async () => {
  try {
    const data = await api.getSettings();
    whisperPath.value = (data as any).whisper_path || '';
    modelPath.value = (data as any).model_path || '';
    openvinoScriptPath.value = (data as any).openvino_script_path || '';
    openvinoEnabled.value = !!(data as any).openvino_enabled;
  } catch (e: any) {
    message.value = '读取设置失败: ' + e.message;
  }
});

// 事件处理函数：避免在模板中写类型
function onWhisperPath(e: Event) {
  whisperPath.value = (e.target as HTMLInputElement)?.value ?? '';
}
function onModelPath(e: Event) {
  modelPath.value = (e.target as HTMLInputElement)?.value ?? '';
}
function onOpenvinoScriptPath(e: Event) {
  openvinoScriptPath.value = (e.target as HTMLInputElement)?.value ?? '';
}
function onOpenvinoEnabled(e: Event) {
  // md-switch 是 Web Component，selected 在 target 上
  const t = e.target as any;
  openvinoEnabled.value = !!t?.selected;
}

async function save() {
  try {
    await api.saveSettings({
      whisper_path: whisperPath.value,
      model_path: modelPath.value,
      openvino_script_path: openvinoScriptPath.value,
      openvino_enabled: openvinoEnabled.value,
      openvino_shell: 'auto',
    });
    store.whisperPath = whisperPath.value;
    store.modelPath = modelPath.value;
    store.openvinoScriptPath = openvinoScriptPath.value;
    store.openvinoEnabled = openvinoEnabled.value;
    message.value = '保存成功';
  } catch (e: any) {
    message.value = '保存失败: ' + e.message;
  }
}

async function testOpenVINO() {
  try {
    const res = await api.testOpenVINO();
    message.value = JSON.stringify(res, null, 2);
  } catch (e: any) {
    message.value = '测试失败: ' + e.message;
  }
}

async function probe() {
  try {
    const ff = await api.probeFfmpeg();
    // 显式将 whisper 可执行路径传给后端进行探测
    const wh = await api.probeWhisper(whisperPath.value || undefined);
    probeResult.value = 'ffmpeg: ' + JSON.stringify(ff, null, 2) + '\n\nwhisper: ' + JSON.stringify(wh, null, 2);
  } catch (e: any) {
    probeResult.value = '探测失败: ' + e.message;
  }
}
</script>

<style scoped>
.card { padding: 16px; border-radius: 12px; background: var(--md-sys-color-surface); color: var(--md-sys-color-on-surface); }
.row { margin: 12px 0; display: flex; align-items: center; }
.msg { background: #111; color: #eee; padding: 12px; border-radius: 8px; max-height: 280px; overflow: auto; }
</style>
