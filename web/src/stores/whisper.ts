import { defineStore } from 'pinia';
import { api } from '../api/client';

export const useWhisperStore = defineStore('whisper', {
  state: () => ({
    cliArgs: null as null | Record<string, any>,
    isLoaded: false,
  }),

  actions: {
    async fetchCliArgs() {
      if (this.isLoaded) return;
      try {
        this.cliArgs = await api.getWhisperArgs();
        this.isLoaded = true;
      } catch (e) {
        console.error('Failed to fetch whisper cli args', e);
      }
    },
  },
});
