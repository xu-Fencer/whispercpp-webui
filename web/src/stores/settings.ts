import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    whisperPath: '',
    modelPath: '',
    openvinoScriptPath: '',
    openvinoEnabled: false,
    openvinoShell: 'auto',
    lastProbe: null as null | Record<string, unknown>,
  }),
});
