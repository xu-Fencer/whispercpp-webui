import { defineStore } from 'pinia';
import { api } from '../api/client';

interface Settings {
  whisper_path: string;
  model_path: string;
  openvino_script_path: string;
  openvino_enabled: boolean;
  openvino_shell: string;
}

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    whisperPath: '',
    modelPath: '',
    openvinoScriptPath: '',
    openvinoEnabled: false,
    openvinoShell: 'auto',
    lastProbe: null as null | Record<string, unknown>,
  }),

  actions: {
    async fetchSettings() {
      try {
        const settings: Settings = await api.getSettings();
        this.whisperPath = settings.whisper_path;
        this.modelPath = settings.model_path;
        this.openvinoScriptPath = settings.openvino_script_path;
        this.openvinoEnabled = settings.openvino_enabled;
        this.openvinoShell = settings.openvino_shell;
      } catch (e) {
        console.error('Failed to fetch settings', e);
      }
    },
  },
});
