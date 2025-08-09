# WebUI for whisper.cpp

目录结构：

```python
whisper-webui/
├─ app/                          # 后端（FastAPI）
│  ├─ main.py                    # 入口：挂路由、静态文件、CORS、WS
│  ├─ requirements.txt           # Python 依赖
│  ├─ config.py                  # 配置模型（读取 settings.json / 环境变量）
│  ├─ settings.json              # 持久化设置（可执行路径、模型目录、OpenVINO 脚本路径等）
│  ├─ api/
│  │  ├─ routes_settings.py      # GET/POST /api/settings（可执行/模型/脚本路径、开关）
│  │  ├─ routes_tasks.py         # 任务：创建/查询/取消，文件上传
│  │  ├─ routes_probe.py         # 探测：ffmpeg/ffprobe/whisper 可用性
│  │  ├─ routes_files.py         # 下载/列出生成文件（srt/vtt/json）
│  │  └─ ws_logs.py              # WebSocket：实时日志/进度推送
│  ├─ core/
│  │  ├─ task_manager.py         # 任务状态机、并发/队列、取消
│  │  ├─ process_runner.py       # 子进程启动 & stdout/stderr 捕获
│  │  ├─ path_guard.py           # 路径白名单、大小限制、MIME 校验
│  │  └─ openvino_env.py         # **执行 .bat/.sh，解析并合并 env**（重点）
│  ├─ whisper/
│  │  ├─ cli_args.py             # UI 参数 → whisper-cli 参数映射与校验
│  │  ├─ command_builder.py      # 生成命令行（含 quoting/escape）
│  │  ├─ ffmpeg.py               # ffprobe 探测、必要的转码（16k/mono/pcm_s16le）
│  │  ├─ outputs.py              # 输出落地（txt/vtt/srt/json…）
│  │  └─ srt_to_vtt.py           # SRT→VTT 转换（用于浏览器预览）
│  ├─ static/                    # 生产环境前端打包产物（build 后复制到这）
│  └─ runs/
│     └─ <job-id>/               # 每个任务自己的目录：源文件、转码 wav、字幕/JSON 等
│
├─ web/                          # 前端（Vue 3 + @material/web）
│  ├─ index.html                 # Vite 入口
│  ├─ vite.config.ts             # dev 代理到后端；build 输出目录配置
│  ├─ package.json
│  └─ src/
│     ├─ main.ts                 # 注册路由、Pinia、全局样式
│     ├─ app.vue
│     ├─ router/
│     │  └─ index.ts             # /tasks /preview /settings
│     ├─ stores/
│     │  └─ settings.ts          # 前端状态（路径、开关、最近使用）
│     ├─ pages/
│     │  ├─ TasksPage.vue        # 任务面板：选择文件/模型/可执行、参数、执行、进度
│     │  ├─ PreviewPage.vue      # 预览：<audio>/<video> + <track src="*.vtt">
│     │  └─ SettingsPage.vue     # 设置：whisper 路径、模型目录、OpenVINO 脚本等
│     ├─ components/
│     │  ├─ ParamBasic.vue       # 常用参数（语言/翻译/输出格式）
│     │  ├─ ParamAdvanced.vue    # 高级参数（beam/best-of/阈值等）
│     │  ├─ FilePicker.vue       # 选择/上传文件
│     │  ├─ ModelPicker.vue      # 本地模型选择（扫描目录）
│     │  ├─ ExecPicker.vue       # 可执行选择与 -h 验证
│     │  └─ LogConsole.vue       # 实时日志（WebSocket）
│     ├─ material/               # @material/web 薄封装（方便 v-model）
│     │  ├─ mw-input.ts          # 例：桥接 value / change 事件
│     │  └─ theme.css            # Material 3 主题 token（CSS 变量）
│     └─ styles/
│        └─ global.css           # 重置 & 布局
│
├─ .gitignore
├─ README.md                     # 快速上手说明
└─ LICENSE

```