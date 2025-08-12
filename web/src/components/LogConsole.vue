<template>
  <section class="console">
    <div class="head">
      <div class="title">运行日志</div>
      <div class="status" :data-state="state">
        {{ stateText }}
      </div>
    </div>
    <pre ref="preRef" class="body">{{ logs }}</pre>
    <div v-if="err" class="err">日志连接失败：{{ err }}（可忽略或检查后端 WS 路径）</div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue';

const props = defineProps<{ jobId: string }>();

const logs = ref('');
const err = ref('');
const state = ref<'idle'|'connecting'|'open'|'closed'>('idle');
const preRef = ref<HTMLElement|null>(null);
let ws: WebSocket | null = null;

const stateText = computed(() => {
  switch (state.value) {
    case 'connecting': return '连接中';
    case 'open': return '已连接';
    case 'closed': return '已关闭';
    default: return '空闲';
  }
});

function connect() {
  cleanup();
  state.value = 'connecting';
  try {
    // 适配 dev/preview：以当前站点为基准拼出 ws/wss
    const wsUrl = `${location.origin.replace(/^http/, 'ws')}/ws/logs/${encodeURIComponent(props.jobId)}`;
    ws = new WebSocket(wsUrl);
    ws.onopen = () => { state.value = 'open'; };
    ws.onmessage = (ev) => {
      logs.value += (typeof ev.data === 'string' ? ev.data : '');
      // 自动滚动到底部
      requestAnimationFrame(() => {
        const el = preRef.value;
        if (el) el.scrollTop = el.scrollHeight;
      });
    };
    ws.onerror = () => {
      err.value = 'WebSocket 发生错误';
    };
    ws.onclose = () => {
      state.value = 'closed';
    };
  } catch (e: any) {
    err.value = e?.message || String(e);
    state.value = 'closed';
  }
}

function cleanup() {
  if (ws) {
    try { ws.close(); } catch {}
    ws = null;
  }
}

watch(() => props.jobId, (id) => {
  if (id) {
    logs.value = '';
    err.value = '';
    connect();
  } else {
    cleanup();
  }
}, { immediate: true });

onMounted(() => {
  if (props.jobId) connect();
});

onBeforeUnmount(() => cleanup());
</script>

<script lang="ts">
export default {};
</script>

<style scoped>
.console { margin-top: 16px; border: 1px solid color-mix(in srgb, var(--md-sys-color-on-surface) 12%, transparent); border-radius: 12px; overflow: hidden; }
.head { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; background: var(--md-sys-color-surface); }
.title { font-weight: 600; }
.status { font-size: 12px; opacity: 0.8; }
.body { background: #0b0b0b; color: #eaeaea; padding: 12px; margin: 0; max-height: 320px; overflow: auto; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.err { color: #ffb4ab; padding: 8px 12px; font-size: 12px; background: color-mix(in srgb, #ffb4ab 12%, transparent); }
</style>
