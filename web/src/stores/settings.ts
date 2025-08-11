import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    whisperPath: '',
    modelPath: '',
    openvinoScriptPath: '',
    openvinoEnabled: false,
  }),
  actions: {
    setWhisperPath(path: string) {
      this.whisperPath = path;
    },
    setModelPath(path: string) {
      this.modelPath = path;
    },
    setOpenvinoScriptPath(path: string) {
      this.openvinoScriptPath = path;
    },
    toggleOpenvino(enabled: boolean) {
      this.openvinoEnabled = enabled;
    },
  },
});
