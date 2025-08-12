<template>
  <div class="row">
    <div class="col">
      <label class="label">线程数 (--threads)</label>
      <md-outlined-text-field
        type="number"
        :value="threads"
        @input="onThreads"
      />
    </div>
    <div class="col">
      <label class="label">Beam Size (--beam-size)</label>
      <md-outlined-text-field
        type="number"
        :value="beamSize"
        @input="onBeamSize"
      />
    </div>
    <div class="col">
      <label class="label">Best Of (--best-of)</label>
      <md-outlined-text-field
        type="number"
        :value="bestOf"
        @input="onBestOf"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ threads: number; beamSize: number; bestOf: number }>();
const emit = defineEmits(['update:threads','update:beamSize','update:bestOf']);

function onThreads(e: Event) {
  const v = parseInt((e.target as HTMLInputElement)?.value || '0', 10);
  emit('update:threads', Number.isFinite(v) ? v : 0);
}
function onBeamSize(e: Event) {
  const v = parseInt((e.target as HTMLInputElement)?.value || '0', 10);
  emit('update:beamSize', Number.isFinite(v) ? v : 0);
}
function onBestOf(e: Event) {
  const v = parseInt((e.target as HTMLInputElement)?.value || '0', 10);
  emit('update:bestOf', Number.isFinite(v) ? v : 0);
}
</script>

<style scoped>
.row { display: flex; gap: 16px; margin: 12px 0; }
.col { display: flex; flex-direction: column; gap: 6px; width: 180px; }
.label { font-size: 12px; color: var(--md-sys-color-on-surface-variant); }
</style>
