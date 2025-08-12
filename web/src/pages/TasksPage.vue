<template>
  <div>
    <div class="page-layout">
      <section class="card params-section">
        <h2>创建任务</h2>

        <div class="row">
          <md-outlined-text-field
            label="源文件服务器路径"
            v-model="serverFilePath"
            style="width: 100%"
          />
        </div>

        <div class="actions">
            <md-filled-button @click="createTask">创建任务</md-filled-button>
        </div>

        <div class="presets">
          <md-outlined-text-field label="预设名称" v-model="presetName" />
          <md-filled-button @click="savePreset">保存预设</md-filled-button>
          <md-outlined-select label="选择预设" v-model="selectedPreset">
            <md-select-option v-for="name in presetNames" :key="name" :value="name">{{ name }}</md-select-option>
          </md-outlined-select>
          <md-filled-tonal-button @click="loadPreset">加载预设</md-filled-tonal-button>
          <md-filled-tonal-button @click="deletePreset">删除预设</md-filled-tonal-button>
        </div>

        <div class="param-groups">
          <details v-for="(group, groupName) in groupedArgs" :key="groupName" open>
            <summary>{{ groupName }}</summary>
            <div class="param-grid">
              <div v-for="(arg, key) in group" :key="key" class="param-item">
                <label :title="arg.help">{{ arg.label || key }}</label>
                <div class="param-input">
                  <md-outlined-text-field
                    v-if="arg.type === 'string' || arg.type === 'integer' || arg.type === 'float'"
                    :type="arg.type === 'string' ? 'text' : 'number'"
                    v-model="taskParams[key]"
                    :label="key"
                  />
                  <input
                    v-if="arg.type === 'integer' && arg.min !== undefined && arg.max !== undefined"
                    type="range"
                    :min="arg.min"
                    :max="arg.max"
                    v-model="taskParams[key]"
                    class="slider"
                  />
                </div>
                <md-switch
                  v-if="arg.type === 'boolean'"
                  :selected="taskParams[key]"
                  @change="taskParams[key] = $event.target.selected"
                />
              </div>
            </div>
          </details>
        </div>
      </section>

      <section class="card results-section">
        <h2>运行结果</h2>
        <div v-if="jobId" class="status">
            <strong>Job ID:</strong> {{ jobId }}
        </div>
        <log-console :jobId="jobId" />
      </section>
    </div>

    <div v-if="statusText" class="toast" :class="{ show: statusText }">{{ statusText }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import { api } from '../api/client';
import { useSettingsStore } from '../stores/settings';
import { useWhisperStore } from '../stores/whisper';
import LogConsole from '../components/LogConsole.vue';

const settingsStore = useSettingsStore();
const whisperStore = useWhisperStore();

const serverFilePath = ref('');
const jobId = ref('');
const statusText = ref('');
let toastTimer: number | undefined;

const taskParams = reactive<Record<string, any>>({});
const presets = ref<Record<string, any>>({});
const presetName = ref('');
const selectedPreset = ref('');

onMounted(async () => {
  await whisperStore.fetchCliArgs();
  if (whisperStore.cliArgs) {
    for (const key in whisperStore.cliArgs) {
      taskParams[key] = whisperStore.cliArgs[key].default;
    }
  }
  loadPresetsFromStorage();
});

const presetNames = computed(() => Object.keys(presets.value));

const groupedArgs = computed(() => {
  if (!whisperStore.cliArgs) return {};
  const groups: Record<string, any> = {};
  for (const key in whisperStore.cliArgs) {
    const arg = whisperStore.cliArgs[key];
    if (!groups[arg.group]) {
      groups[arg.group] = {};
    }
    groups[arg.group][key] = arg;
  }
  return groups;
});

function loadPresetsFromStorage() {
  const saved = localStorage.getItem('whisper_presets');
  if (saved) {
    presets.value = JSON.parse(saved);
  }
}

function savePreset() {
  if (!presetName.value) {
    showToast('请输入预设名称', 'error');
    return;
  }
  presets.value[presetName.value] = JSON.parse(JSON.stringify(taskParams));
  localStorage.setItem('whisper_presets', JSON.stringify(presets.value));
  showToast(`预设 "${presetName.value}" 已保存`);
}

function loadPreset() {
  if (!selectedPreset.value) {
    showToast('请选择要加载的预设', 'error');
    return;
  }
  Object.assign(taskParams, presets.value[selectedPreset.value]);
  showToast(`预设 "${selectedPreset.value}" 已加载`);
}

function deletePreset() {
  if (!selectedPreset.value) {
    showToast('请选择要删除的预设', 'error');
    return;
  }
  delete presets.value[selectedPreset.value];
  localStorage.setItem('whisper_presets', JSON.stringify(presets.value));
  showToast(`预设 "${selectedPreset.value}" 已删除`);
  selectedPreset.value = '';
}

function showToast(message: string, type: 'info' | 'error' = 'info') {
  statusText.value = message;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    statusText.value = '';
  }, 2700); // 3000ms total, 300ms for fade-out
}

async function createTask() {
  try {
    if (!serverFilePath.value) throw new Error('请填写源文件路径');
    if (!settingsStore.modelPath || !settingsStore.whisperPath) throw new Error('请先到“设置”页面填写可执行文件与模型路径');
    
    const payload = {
      input_file: serverFilePath.value,
      output_format: 'srt', // Or make this a parameter
      whisper_params: taskParams,
    };

    const res = await api.createTask(payload);
    jobId.value = (res as any).job_id || '';
    showToast('任务已创建');
  } catch (e: any) {
    showToast('创建失败: ' + e.message, 'error');
  }
}

</script>

<style scoped>
.page-layout { display: flex; gap: 16px; }
.params-section { flex: 1; }
.results-section { flex: 1; }
.card { padding: 16px; border-radius: 12px; background: var(--md-sys-color-surface); color: var(--md-sys-color-on-surface); }
.row { margin: 12px 0; display: flex; align-items: center; }
.actions { margin: 16px 0; display: flex; gap: 8px; }
.presets { display: flex; gap: 8px; align-items: center; margin-bottom: 16px; }
.param-groups { margin-top: 16px; }
.param-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; padding: 16px; }
.param-item { display: flex; flex-direction: column; gap: 4px; }
.param-input { display: flex; align-items: center; gap: 8px; }
.slider {
  width: 100%;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: var(--md-sys-color-surface-variant);
  outline: none;
  opacity: 0.7;
  transition: opacity .2s;
}
.slider:hover { opacity: 1; }
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: var(--md-sys-color-primary);
  cursor: pointer;
  border-radius: 50%;
}
.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: var(--md-sys-color-primary);
  cursor: pointer;
  border-radius: 50%;
}
summary { font-weight: bold; cursor: pointer; padding: 8px; background-color: var(--md-sys-color-surface-variant); border-radius: 4px; }
.status { margin-top: 16px; }
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 24px;
  background-color: var(--md-sys-color-inverse-surface);
  color: var(--md-sys-color-inverse-on-surface);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.toast.show {
  opacity: 1;
}
</style>
