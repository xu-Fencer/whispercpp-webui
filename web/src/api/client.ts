const base = '';

// Interfaces for API responses
export interface Settings {
  whisper_path: string;
  model_path: string;
  openvino_script_path: string;
  openvino_enabled: boolean;
  openvino_shell: string;
}

export interface WhisperCliArgs {
  [key: string]: {
    group: string;
    type: string;
    cli: string[];
    default: any;
    help: string;
  };
}

async function jsonGet<T>(url: string): Promise<T> {
  const res = await fetch(base + url, { method: 'GET' });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

async function jsonPost<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(base + url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

async function jsonPut<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(base + url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

async function formPost<T>(url: string, form: FormData): Promise<T> {
  const res = await fetch(base + url, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export const api = {
  getSettings: () => jsonGet<Settings>('/api/settings/'),
  saveSettings: (settings: any) => jsonPost('/api/settings/', settings),

  // 增加可选 exe 参数，前端可显式传递 whisper 可执行路径
  probeWhisper: (exe?: string) =>
    jsonGet(`/api/probe/whisper${exe ? `?exe=${encodeURIComponent(exe)}` : ''}`),

  probeFfmpeg: () => jsonGet('/api/probe/ffmpeg'),
  testOpenVINO: () => jsonPost('/api/settings/openvino/test', {}),

  createTask: (payload: any) => jsonPost('/api/tasks/', payload),
  getTask: (jobId: string) => jsonGet(`/api/tasks/${jobId}`),
  listFiles: (jobId: string) => jsonGet(`/api/files/${jobId}`),

  getWhisperArgs: () => jsonGet<WhisperCliArgs>('/api/whisper/whisper-args'),
  saveWhisperArgs: (args: any) => jsonPut('/api/whisper/whisper-args', args),
};