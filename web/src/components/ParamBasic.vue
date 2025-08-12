<template>
  <div class="row">
    <div style="margin-right: 16px">
      <label class="label">语言</label>
      <md-outlined-select @change="onLang" :value="language">
        <md-select-option value="auto">auto</md-select-option>
        <md-select-option value="en">en</md-select-option>
        <md-select-option value="zh">zh</md-select-option>
        <md-select-option value="ja">ja</md-select-option>
        <md-select-option value="es">es</md-select-option>
      </md-outlined-select>
    </div>

    <div style="margin-right: 16px">
      <label class="label">翻译到英文</label>
      <md-switch :selected="translate" @change="onTranslate"></md-switch>
    </div>

    <div>
      <label class="label">输出格式</label>
      <md-outlined-select @change="onFmt" :value="outputFormat">
        <md-select-option value="srt">srt</md-select-option>
        <md-select-option value="vtt">vtt</md-select-option>
        <md-select-option value="json">json</md-select-option>
        <md-select-option value="txt">txt</md-select-option>
      </md-outlined-select>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  language: string,
  translate: boolean,
  outputFormat: string,
}>();
const emit = defineEmits(['update:language', 'update:translate', 'update:outputFormat']);

function onLang(e: Event) {
  const t = e.target as any;
  emit('update:language', t?.value ?? '');
}
function onTranslate(e: Event) {
  const t = e.target as any;
  emit('update:translate', !!t?.selected);
}
function onFmt(e: Event) {
  const t = e.target as any;
  emit('update:outputFormat', t?.value ?? 'srt');
}
</script>

<style scoped>
.row { display: flex; align-items: center; margin: 12px 0; gap: 16px; }
.label { display: block; margin-bottom: 6px; font-size: 12px; color: var(--md-sys-color-on-surface-variant); }
</style>
