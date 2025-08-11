const base = '';

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

async function formPost<T>(url: string, form: FormData): Promise<T> {
  const res = await fetch(base + url, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export const api = {
  getSettings: () => jsonGet('/api/settings/'),
  saveSettings: (settings: any) => jsonPost('/api/settings/', settings),
  testOpenVINO: () => jsonPost('/api/settings/openvino/test', {}),
  probeFfmpeg: () => jsonGet('/api/probe/ffmpeg'),
  probeWhisper: () => jsonGet('/api/probe/whisper'),
  createTask: (payload: any) => jsonPost('/api/tasks/', payload),
  getTask: (jobId: string) => jsonGet(`/api/tasks/${jobId}`),
  listFiles: (jobId: string) => jsonGet(`/api/files/${jobId}`),
};
