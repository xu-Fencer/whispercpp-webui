# WebUI for whisper.cpp

本项目为 **whisper.cpp** 提供一个跨平台、开箱即用的本地 Web UI。
目标是让非技术用户通过浏览器即可调用 whisper.cpp 进行语音转文字 / 翻译，并实时预览外挂字幕。

---

## 1. 主要特性

1. 全量参数覆盖
   • Web 表单一一映射 whisper.cpp CLI 全部参数（基础 / 进阶 / 高级三折叠面板）。
2. 本地模型与可执行文件管理
   • 仅使用本地模型（\*.bin / \*.gguf），无需联网下载。
   • 手动选择并校验 whisper 可执行文件路径。
3. 自动转码与字幕预览
   • 自动调用 ffmpeg 将任意音视频转 16 kHz / 单声道 WAV。
   • 同时生成 SRT & VTT，浏览器内 `<audio>/<video> + <track>` 直接预览。
4. OpenVINO 支持
   • 可配置「初始化 .bat/.sh」脚本；每次任务前自动调用并合并环境变量。
5. 任务管理
   • 并发队列 / 取消任务 / WebSocket 实时日志与进度。
6. 安全本地运行
   • 无登陆、多用户或在线上传；所有文件均在本机白名单目录内处理。

---

## 2. 技术栈

### 后端

* Python 3.10+
* FastAPI + Uvicorn
* subprocess + asyncio 队列（任务调度）
* ffmpeg / ffprobe（系统级依赖）
* whisper.cpp CLI（二进制由用户自行编译或下载）

### 前端

* Vue 3 + Vite + TypeScript
* Pinia（状态管理） / Vue-Router
* Material Design 3
  • 默认采用 `@material/web` 原生 Web Components
  • 若需完整 Vue 组件语法，可切换 Vuetify 3 + M3 主题

### 目录结构

```
project-root
├─ app/          # FastAPI 后端
│  ├─ api/       # 路由 & Pydantic schemas
│  ├─ core/      # 任务队列 / 进程 & FFmpeg / OpenVINO 工具
│  ├─ whisper/   # 参数映射、命令生成、输出解析
│  ├─ preview/   # SRT↔VTT 转换工具
│  └─ static/    # 生成的字幕 / 临时转码文件
└─ web/          # Vue 3 前端
   ├─ src/
   │  ├─ components/
   │  ├─ pages/          # Task / Preview / Settings
   │  ├─ stores/
   │  ├─ router/
   │  └─ styles/
   └─ index.html
```

---

## 3. 运行流程

1. 前端收集用户输入
   • 上传或选择音/视频 → 选模型 → 设定参数 → 点击「开始」。
2. 后端执行

   1. 检测 & 调用 OpenVINO 初始化脚本（可选）。
   2. ffprobe 检测源文件；若非 16 k/mono WAV → ffmpeg 转码。
   3. 组装 whisper CLI 命令并启动子进程。
   4. 持续捕获 stdout / stderr，通过 WebSocket 推送进度。
   5. 任务完成后写出 SRT / 选配输出，并同步转 VTT。
3. 页面预览
   • 自动加载生成的 VTT → `<track>` 字幕轨道 → 实时播放预览。

---

## 4. REST / WebSocket API

| 方法   | 路径                             | 说明                                                                |
| ---- | ------------------------------ | ----------------------------------------------------------------- |
| GET  | /api/settings                  | 获取全局设置（模型 / 执行文件 / OpenVINO 脚本路径…）                                |
| PUT  | /api/settings                  | 保存全局设置                                                            |
| POST | /api/test/openvino             | `{ "script_path": "C:\\openvino\\vars.bat" }`<br>执行脚本并返回新增环境变量或错误 |
| POST | /api/task                      | 新建转写任务（表单或 JSON + 文件路径）→ 返回 `task_id`                             |
| GET  | /api/task/{id}/status          | 查询任务状态 / 结果文件列表                                                   |
| GET  | /api/task/{id}/download/{type} | 下载结果（srt / vtt / txt / json …）                                    |
| WS   | /ws/task/{id}/log              | 推送实时 stdout / 进度百分比                                               |
| GET  | /api/env/validate              | 校验 whisper 可执行 / ffmpeg / 模型文件等（query 参数 `type`+`path`）           |

---

## 5. 参数映射（示例）

后端统一采用 “只允许白名单参数” 策略，防止命令注入。

| 前端字段      | whisper flag          | 类型 / 默认    |
| --------- | --------------------- | ---------- |
| 线程数       | `-t` / `--threads`    | number / 4 |
| 处理器数      | `-p` / `--processors` | number / 1 |
| 翻译到英文     | `-tr` / `--translate` | boolean    |
| beam size | `-bs` / `--beam-size` | number / 5 |
| ……        | ……                    | ……         |



---

## 6. 安装与使用

### 6.1 先决条件

* Python 3.10+，pip
* Node 18+（前端构建）
* whisper.cpp 可执行文件（自行编译或下载）
* ffmpeg 6+
  Windows 推荐 [Gyan.dev build](https://www.gyan.dev/ffmpeg/)
* （可选）Intel OpenVINO Runtime + 初始化脚本

### 6.2 后端

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6.3 前端

```bash
cd web
npm i
npm run dev      # 开发
npm run build    # 生成静态文件，复制到 app/static/front/
```

---

## 7. OpenVINO 初始化脚本

在「设置」页填入脚本绝对路径，例如：

```
C:\Program Files (x86)\Intel\openvino\setupvars.bat
```

勾选「每次任务前执行」。
后端执行顺序：

```
cmd /s /c call "setupvars.bat" && set
```

抓取输出的 `KEY=VALUE`，合并到当前环境后再启动 whisper 进程。
错误或超时将阻止任务开始，并返回错误信息到前端。

---

## 8. 安全注意事项

1. 建议 **不要** 以管理员 / root 运行后端进程。
2. 文件操作限定在配置的工作目录；禁止任意系统路径。
3. 上传体积 / 转码时长有限制，防止拒绝服务。
4. 后端仅拼接白名单参数，不接受任何自由文本注入。

---
