[跳至内容](https://chat.sharedchat.top/c/689669df-ef0c-8325-9bd1-95755897f03c#main)

## 历史聊天记录







##### 您说：

我想让你给whisper.cpp开发一个webui，后端使用python，需要通过命令行调用whisper，需要能调整whisper.cpp可设置的所有参数，支持选择模型（选择文件），支持选择whisper的可执行程序的目录，支持在页面中直接预览生成好的字幕（视频/音频外挂srt），但我不知道是否需要使用ffmpeg（如果需要，你查找资料后加入这个功能），使用Material Design 3。先写一份项目开发思路，给我检查之后我再让你写代码。你可以参考以下帮助来看每个参数的含义和如何设置：

```
bash
./build/bin/whisper-cli -h

usage: ./build/bin/whisper-cli [options] file0 file1 ...
supported audio formats: flac, mp3, ogg, wav

options:
  -h,        --help              [default] show this help message and exit
  -t N,      --threads N         [4      ] number of threads to use during computation
  -p N,      --processors N      [1      ] number of processors to use during computation
  -ot N,     --offset-t N        [0      ] time offset in milliseconds
  -on N,     --offset-n N        [0      ] segment index offset
  -d  N,     --duration N        [0      ] duration of audio to process in milliseconds
  -mc N,     --max-context N     [-1     ] maximum number of text context tokens to store
  -ml N,     --max-len N         [0      ] maximum segment length in characters
  -sow,      --split-on-word     [false  ] split on word rather than on token
  -bo N,     --best-of N         [5      ] number of best candidates to keep
  -bs N,     --beam-size N       [5      ] beam size for beam search
  -ac N,     --audio-ctx N       [0      ] audio context size (0 - all)
  -wt N,     --word-thold N      [0.01   ] word timestamp probability threshold
  -et N,     --entropy-thold N   [2.40   ] entropy threshold for decoder fail
  -lpt N,    --logprob-thold N   [-1.00  ] log probability threshold for decoder fail
  -nth N,    --no-speech-thold N [0.60   ] no speech threshold
  -tp,       --temperature N     [0.00   ] The sampling temperature, between 0 and 1
  -tpi,      --temperature-inc N [0.20   ] The increment of temperature, between 0 and 1
  -debug,    --debug-mode        [false  ] enable debug mode (eg. dump log_mel)
  -tr,       --translate         [false  ] translate from source language to english
  -di,       --diarize           [false  ] stereo audio diarization
  -tdrz,     --tinydiarize       [false  ] enable tinydiarize (requires a tdrz model)
  -nf,       --no-fallback       [false  ] do not use temperature fallback while decoding
  -otxt,     --output-txt        [false  ] output result in a text file
  -ovtt,     --output-vtt        [false  ] output result in a vtt file
  -osrt,     --output-srt        [false  ] output result in a srt file
  -olrc,     --output-lrc        [false  ] output result in a lrc file
  -owts,     --output-words      [false  ] output script for generating karaoke video
  -fp,       --font-path         [/System/Library/Fonts/Supplemental/Courier New Bold.ttf] path to a monospace font for karaoke video
  -ocsv,     --output-csv        [false  ] output result in a CSV file
  -oj,       --output-json       [false  ] output result in a JSON file
  -ojf,      --output-json-full  [false  ] include more information in the JSON file
  -of FNAME, --output-file FNAME [       ] output file path (without file extension)
  -np,       --no-prints         [false  ] do not print anything other than the results
  -ps,       --print-special     [false  ] print special tokens
  -pc,       --print-colors      [false  ] print colors
  -pp,       --print-progress    [false  ] print progress
  -nt,       --no-timestamps     [false  ] do not print timestamps
  -l LANG,   --language LANG     [en     ] spoken language ('auto' for auto-detect)
  -dl,       --detect-language   [false  ] exit after automatically detecting language
             --prompt PROMPT     [       ] initial prompt (max n_text_ctx/2 tokens)
  -m FNAME,  --model FNAME       [models/ggml-base.en.bin] model path
  -f FNAME,  --file FNAME        [       ] input audio file path
  -oved D,   --ov-e-device DNAME [CPU    ] the OpenVINO device used for encode inference
  -dtw MODEL --dtw MODEL         [       ] compute token-level timestamps
  -ls,       --log-score         [false  ] log best decoder scores of tokens
  -ng,       --no-gpu            [false  ] disable GPU
  -fa,       --flash-attn        [false  ] flash attention
  -sns,      --suppress-nst      [false  ] suppress non-speech tokens
  --suppress-regex REGEX         [       ] regular expression matching tokens to suppress
  --grammar GRAMMAR              [       ] GBNF grammar to guide decoding
  --grammar-rule RULE            [       ] top-level GBNF grammar rule name
  --grammar-penalty N            [100.0  ] scales down logits of nongrammar tokens
```

以及这是whisper-server的手册，你觉得webui用哪个好就选哪个：

```
`markdown
# whisper.cpp/examples/server

Simple http server. WAV Files are passed to the inference model via http requests.

https://github.com/ggerganov/whisper.cpp/assets/1991296/e983ee53-8741-4eb5-9048-afe5e4594b8f

## Usage
```

./build/bin/whisper-server -h usage: ./build/bin/whisper-server [options] options:  -h,        --help              [default] show this help message and exit  -t N,      --threads N         [4      ] number of threads to use during computation  -p N,      --processors N      [1      ] number of processors to use during computation  -ot N,     --offset-t N        [0      ] time offset in milliseconds  -on N,     --offset-n N        [0      ] segment index offset  -d  N,     --duration N        [0      ] duration of audio to process in milliseconds  -mc N,     --max-context N     [-1     ] maximum number of text context tokens to store  -ml N,     --max-len N         [0      ] maximum segment length in characters  -sow,      --split-on-word     [false  ] split on word rather than on token  -bo N,     --best-of N         [2      ] number of best candidates to keep  -bs N,     --beam-size N       [-1     ] beam size for beam search  -ac N,     --audio-ctx N       [0      ] audio context size (0 - all)  -wt N,     --word-thold N      [0.01   ] word timestamp probability threshold  -et N,     --entropy-thold N   [2.40   ] entropy threshold for decoder fail  -lpt N,    --logprob-thold N   [-1.00  ] log probability threshold for decoder fail  -debug,    --debug-mode        [false  ] enable debug mode (eg. dump log_mel)  -tr,       --translate         [false  ] translate from source language to english  -di,       --diarize           [false  ] stereo audio diarization  -tdrz,     --tinydiarize       [false  ] enable tinydiarize (requires a tdrz model)  -nf,       --no-fallback       [false  ] do not use temperature fallback while decoding  -ps,       --print-special     [false  ] print special tokens  -pc,       --print-colors      [false  ] print colors  -pr,       --print-realtime    [false  ] print output in realtime  -pp,       --print-progress    [false  ] print progress  -nt,       --no-timestamps     [false  ] do not print timestamps  -l LANG,   --language LANG     [en     ] spoken language ('auto' for auto-detect)  -dl,       --detect-language   [false  ] exit after automatically detecting language             --prompt PROMPT     [       ] initial prompt  -m FNAME,  --model FNAME       [models/ggml-base.en.bin] model path  -oved D,   --ov-e-device DNAME [CPU    ] the OpenVINO device used for encode inference  -dtw MODEL --dtw MODEL         [       ] compute token-level timestamps  --host HOST,                   [127.0.0.1] Hostname/ip-adress for the server  --port PORT,                   [8080   ] Port number for the server  --public PATH,                 [examples/server/public] Path to the public folder  --request-path PATH,           [       ] Request path for all requests  --inference-path PATH,         [/inference] Inference path for all requests  --convert,                     [false  ] Convert audio to WAV, requires ffmpeg on the server  -sns,      --suppress-nst      [false  ] suppress non-speech tokens  -nth N,    --no-speech-thold N [0.60   ] no speech threshold  -nc,       --no-context        [false  ] do not use previous audio context  -ng,       --no-gpu            [false  ] do not use gpu  -fa,       --flash-attn        [false  ] flash attention Voice Activity Detection (VAD) options:             --vad                           [false  ] enable Voice Activity Detection (VAD)  -vm FNAME, --vad-model FNAME               [       ] VAD model path  -vt N,     --vad-threshold N               [0.50   ] VAD threshold for speech recognition  -vspd N,   --vad-min-speech-duration-ms  N [250    ] VAD min speech duration (0.0-1.0)  -vsd N,    --vad-min-silence-duration-ms N [100    ] VAD min silence duration (to split segments)  -vmsd N,   --vad-max-speech-duration-s   N [FLT_MAX] VAD max speech duration (auto-split longer)  -vp N,     --vad-speech-pad-ms           N [30     ] VAD speech padding (extend segments)  -vo N,     --vad-samples-overlap         N [0.10   ] VAD samples overlap (seconds between segments)

```
> [!WARNING]
> **Do not run the server example with administrative privileges and ensure it's operated in a sandbox environment, especially since it involves risky operations like accepting user file uploads and using ffmpeg for format conversions. Always validate and sanitize inputs to guard against potential security threats.**

## request examples

**/inference**
```

curl 127.0.0.1:8080/inference \ -H "Content-Type: multipart/form-data" \ -F file="@<file-path>" \ -F temperature="0.0" \ -F temperature_inc="0.2" \ -F response_format="json"

```
**/load**
```

curl 127.0.0.1:8080/load \ -H "Content-Type: multipart/form-data" \ -F model="<path-to-model-file>"

```
## Load testing with k6

> **Note:** Install [k6](https://k6.io/docs/get-started/installation/) before running the benchmark script.

You can benchmark the Whisper server using the provided bench.js script with [k6](https://k6.io/). This script sends concurrent multipart requests to the /inference endpoint and is fully configurable via environment variables.

**Example usage:**
```

k6 run bench.js \  --env FILE_PATH=/absolute/path/to/samples/jfk.wav \  --env BASE_URL=http://127.0.0.1:8080 \  --env ENDPOINT=/inference \  --env CONCURRENCY=4 \  --env TEMPERATURE=0.0 \  --env TEMPERATURE_INC=0.2 \  --env RESPONSE_FORMAT=json

```
**Environment variables:**
- `FILE_PATH`: Path to the audio file to send (must be absolute or relative to the k6 working directory)
- `BASE_URL`: Server base URL (default: `http://127.0.0.1:8080`)
- `ENDPOINT`: API endpoint (default: `/inference`)
- `CONCURRENCY`: Number of concurrent requests (default: 4)
- `TEMPERATURE`: Decoding temperature (default: 0.0)
- `TEMPERATURE_INC`: Temperature increment (default: 0.2)
- `RESPONSE_FORMAT`: Response format (default: `json`)

**Note:**
- The server must be running and accessible at the specified `BASE_URL` and `ENDPOINT`.
- The script is located in the same directory as this README: `bench.js`.
```

``

###### ChatGPT 说：

好的！下面是我给 **whisper.cpp Web UI** 做的一份「先设计、后落地」的**项目开发思路**。我会明确为什么需要 ffmpeg、选 CLI 还是 server、整体架构、参数映射、页面交互、以及安全与部署要点。看你确认后，我再开写代码。

------

# 1. 总体目标与关键选择

- **目标**：做一个跨平台的本地 WebUI（Material Design 3 风格），后端用 Python，通过命令行调用 whisper.cpp，**可完整覆盖 whisper.cpp 的所有可调参数**；支持选择 **模型文件**、**whisper 可执行程序路径**；支持上传/选择 **音视频文件**；能在页面**直接预览字幕**（外挂 SRT / VTT，含音频或视频预览）。
- **关于 ffmpeg**：
  - whisper.cpp 官方 README 明确：示例 `whisper-cli` **默认只吃 16-bit WAV**，建议用 `ffmpeg` 先转码（除非用 Linux 开启 `WHISPER_FFMPEG` 支持更多格式）。因此为了稳妥处理 **mp3/ogg/opus/aac/视频容器** 等输入，**必须集成 ffmpeg**（或检测到可用时自动使用）。[GitHub](https://github.com/ggml-org/whisper.cpp)
  - server 例子本身也提供 `--convert`，明确**需要 ffmpeg** 才能在服务器端转 WAV。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)
  - 浏览器 `<video>/<audio>` 的 `<track>` **原生只支持 WebVTT ( `.vtt`)**，不支持 SRT。为了在页面内预览，我们会把 SRT 同步生成 VTT（轻量文本转换即可）。[MDN Web Docs+1MDN Web Docs+1](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/track?utm_source=chatgpt.com)
- **CLI vs. server 的路线选择**：
  - **默认方案：CLI 路线**。满足你“后端 Python、通过命令行调用”的要求，并且 CLI 侧有完整输出开关（txt/vtt/srt/json 等）更利于产物落地；我们用 Python 构建参数→命令行的映射层。
  - **可选增强：Server 路线（增值项）**。如果需要内置 **VAD**、HTTP 推理入口或“类 API”集成，可在后台由 Python 管理/拉起 `whisper-server`，并代理其 `/inference`、`/load` 等端点（且可用 `--convert` 结合 ffmpeg）。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)
  - 结论：**先做 CLI 全量参数 WebUI**，再加“Server 模式（可选）”。

------

# 2. 技术栈与项目结构

- **后端**：Python 3.10+、FastAPI + Uvicorn

  - 任务执行：`subprocess` + 线程/队列（后续如需分布式可接 Celery/RQ）
  - 文件服务：本地文件目录白名单 + 断点续传（可选，初版先直传）
  - 实时日志：WebSocket 推送 whisper 进程 stdout/stderr（配合 `--print-progress`）

- **前端**：React + TypeScript + **Material Design 3**

  - 组件库：官方 **Material Web (Material 3)** 组件（`@material/web`），或 MUI 兼容 M3 的主题；优先官方 M3 规范一致性。[Material Design](https://m3.material.io/develop/web?utm_source=chatgpt.com)[GitHub](https://github.com/material-components/material-web?utm_source=chatgpt.com)

- **转码/封装**：系统级 `ffmpeg/ffprobe`（自动检测与版本显示）

- **目录结构（建议）**

  ```
  
  ```

```


```

- ```
  /app
    /api        # FastAPI 路由、schemas、依赖注入
    /core       # 任务队列、进程管理、ffmpeg/cli 能力检测
    /whisper    # 参数映射、命令生成、输出解析
    /preview    # srt<->vtt、HTML5 预览逻辑
    /static     # 静态文件（生成的字幕、波形图等）
  /web
    /src        # React 源码（Material 3）
  ```

------

# 3. 系统能力与工作流

## 3.1 启动与能力检测

- 启动时检测：
  - **whisper 可执行文件**（用户可在设置中填路径，如 `whisper-cli` / `whisper-cpp` / `main.exe` 等；一键“验证”跑 `-h`）。
  - **ffmpeg / ffprobe**（用于音视频探测与转码，和预览/封装）。
  - CLI 是否带 `WHISPER_FFMPEG` 支持（可尝试喂一个非 WAV 文件进行探测；或读取 README 提示+系统平台推断）。[GitHub](https://github.com/ggml-org/whisper.cpp)
- 显示环境信息（CPU/GPU/CUDA/Vulkan/OpenVINO 是否可用——仅做展示，不强绑定）。[GitHub](https://github.com/ggml-org/whisper.cpp)

## 3.2 任务流（CLI 模式）

1. **选择模型文件**（本地路径选择/扫描；也支持一键从 Hugging Face 镜像下载官方 ggml/gguf 模型目录到本地模型库）。[GitHub](https://github.com/ggml-org/whisper.cpp)
2. **选择可执行文件**（手填+“浏览服务器目录”（白名单根路径）+验证按钮）。
3. **上传音视频**或选择服务器现有文件。
4. **自动探测并决定是否转码**：
   - 如果文件非 16-bit 16k 单声道 WAV，或 CLI 不支持该容器/编码，后台走 `ffmpeg` → WAV（`-ar 16000 -ac 1 -c:a pcm_s16le`）。[GitHub](https://github.com/ggml-org/whisper.cpp)
   - server 模式可用 `--convert` 省去前置转码。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)
5. **参数面板 → 命令行**：把 UI 中每个参数转成 CLI flag，生成命令，启动子进程。
6. **输出落地**：根据勾选输出类型（txt/vtt/srt/json/json-full/lrc/csv/words）落盘；若只出 srt，为了浏览器预览，会**自动生成 .vtt** 一份（轻量文本转换）。[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/track?utm_source=chatgpt.com)
7. **页面预览**：
   - **音频**：`<audio>` + `<track src="*.vtt">`
   - **视频**：`<video>` + `<track src="*.vtt">`（若上传的视频源文件）。
   - （可选）一键“内封/硬字幕”：mp4 里软字幕需要 `-c:s mov_text`；mkv 可直接封装 srt。预览仍推荐外挂 vtt。[Super User](https://superuser.com/questions/1482965/adding-subtitles-via-command-line-in-ffmpeg?utm_source=chatgpt.com)[Stack Overflow](https://stackoverflow.com/questions/8672809/use-ffmpeg-to-add-text-subtitles?utm_source=chatgpt.com)

## 3.3 任务流（Server 模式，可选）

- 后端管理 `whisper-server` 进程（端口/路径/模型），转发 `/inference`、`/load`；如需兼容多格式，启用 `--convert`（需要 ffmpeg）。可选打开 **VAD**。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)

------

# 4. 参数覆盖与 UI 设计

> 目标：**把 whisper.cpp 可调项全部做成 UI**（含高级开关）。以下分组对应 CLI/server 常用参数（你提供的帮助文本为准），每个控件旁给出 flag 映射与默认值提示。

- **性能**
  - 线程、处理器：`--threads -t`、`--processors -p`
  - GPU / Flash-Attn：`--no-gpu -ng`（反向勾选）、`--flash-attn -fa`
  - OpenVINO 编码设备：`--ov-e-device`
  - 音频上下文：`--audio-ctx`
- **时域**
  - 偏移 / 时长：`--offset-t`、`--offset-n`、`--duration`
- **解码与搜索**
  - 温度 / 递增：`--temperature`、`--temperature-inc`
  - Beam/Best-of：`--beam-size -bs`、`--best-of -bo`
  - Fallback：`--no-fallback -nf`
  - 阈值：`--word-thold`、`--entropy-thold`、`--logprob-thold`、`--no-speech-thold`
- **文本片段控制**
  - 最大上下文：`--max-context`
  - 最大段长：`--max-len -ml`（含“按词切分” `--split-on-word -sow`；注意 `-ml 1` 可得到更细时间戳）[GitHub](https://github.com/ggml-org/whisper.cpp)
- **语言与任务**
  - 语言/自动检测：`--language -l` / `--detect-language -dl`
  - 翻译到英文：`--translate -tr`
  - 初始 Prompt：`--prompt`
- **说话人/对齐**
  - 立体声分离：`--diarize -di`
  - TinyDiarize：`--tinydiarize -tdrz`（需要 **tdrz 模型**，例如 small.en-tdrz）[Hugging Face](https://huggingface.co/akashmjn/tinydiarize-whisper.cpp?utm_source=chatgpt.com)
  - Token 级时间对齐：`--dtw MODEL`（D-T-W 模型路径）
- **输出**
  - 控制台输出开关：`--no-prints -np`、`--print-progress -pp`、`--print-colors -pc`、`--print-special -ps`、`--no-timestamps -nt`
  - 文件输出：`--output-txt/-vtt/-srt/-lrc/-csv/-json/-json-full`、`--output-words -owts`、`--font-path`、`--output-file -of`
- **抑制与语法引导**
  - 抑制非语音 token：`--suppress-nst -sns`
  - 正则抑制：`--suppress-regex`
  - GBNF 语法/规则/惩罚：`--grammar`、`--grammar-rule`、`--grammar-penalty`
- **Server 专属（可选页签）**
  - host/port/public 路径、`--request-path`、`--inference-path`
  - `--convert`（依赖 ffmpeg）
  - **VAD 开关与参数**：`--vad`、`--vad-model`、`--vad-threshold`、`--vad-min-speech-duration-ms`、`--vad-min-silence-duration-ms`、`--vad-max-speech-duration-s`、`--vad-speech-pad-ms`、`--vad-samples-overlap`（参数名以 README 为准）[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)

**交互建议（Material 3）**：将参数按“基础 / 进阶 / 高级”三折叠面板呈现；常用项（模型、语言、翻译、输出格式）默认展开；所有参数旁放置气泡说明（hover/点击），说明与默认值。M3 规范与组件参考：官方 M3 文档与 Material Web 组件库。[Material Design](https://m3.material.io/develop/web?utm_source=chatgpt.com)[GitHub](https://github.com/material-components/material-web?utm_source=chatgpt.com)

------

# 5. 字幕预览与封装策略

- **内页预览**：
  - 原生 `<audio>/<video> + <track>` 仅支持 **VTT**，故在生成 SRT 的同时自动生成 VTT；无需引入额外播放器即可跨浏览器预览。[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/track?utm_source=chatgpt.com)
- **外挂 vs. 内封**：
  - 预览默认**外挂**（最稳）。
  - 如需**封装**：
    - **MP4 软字幕** → 需要 `-c:s mov_text`。[Super User](https://superuser.com/questions/1482965/adding-subtitles-via-command-line-in-ffmpeg?utm_source=chatgpt.com)
    - **MKV 软字幕** → 可直接封装 SRT。
    - **硬字幕**（烧制） → ffmpeg `subtitles`/`ass` 滤镜（仅用于导出，不用于网页预览）。[bannerbear.com](https://www.bannerbear.com/blog/how-to-add-subtitles-to-a-video-file-using-ffmpeg/?utm_source=chatgpt.com)

------

# 6. 文件与模型管理

- **模型库**：允许配置模型目录，扫描列出 `.bin`（ggml/gguf）文件，显示大小；支持直接跳转到官方模型页（Hugging Face `ggerganov/whisper.cpp`）下载到库中。[GitHub](https://github.com/ggml-org/whisper.cpp)
- **可执行文件**：允许设置并校验 whisper 可执行路径（跨平台：`whisper-cli`/`whisper-cpp`/`main.exe` 等）。
- **结果目录**：每个任务独立子目录（含：原文件、转码 WAV、SRT、VTT、JSON 等）。

------

# 7. 后端实现要点

- **命令生成器**：将 UI 值严格映射到 flag；对布尔开关、数值范围、字符串进行校验与转义（防注入）。
- **进程与并发**：
  - 控制“最大并发任务数”，避免线程数与系统核数的过度叠加。
  - 提供**取消**按钮（终止子进程）。
- **日志与进度**：抓取 `stdout` 分析 `--print-progress`；WebSocket 推送到前端。
- **自动转码**：`ffprobe` 探测 → 不满足 16k/单声道/WAV 时，走 `ffmpeg` 统一到 `pcm_s16le`。[GitHub](https://github.com/ggml-org/whisper.cpp)
- **SRT → VTT**：后端同步生成（行首加 `WEBVTT`，去掉 SRT 编号、保持时间戳 `-->`；或用轻量库实现）。
- **Server 模式（可选）**：Python 负责拉起/守护 `whisper-server`，做健康检查与热加载模型 `/load`。`--convert` 需要 ffmpeg。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)

------

# 8. 安全、沙箱与权限

- **不要以管理员/root 权限运行** server 示例；处理用户上传（含 ffmpeg 转码）务必沙箱与白名单路径；严格校验扩展名与 MIME；限制最大文件体积与转码时长。[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)
- 命令行参数**严格转义**；仅允许我们映射的 flag 列表，拒绝任意拼接。
- 可选：把转码与推理放到受限的工作目录 / 容器中。

------

# 9. 部署与打包

- **本地安装**：Python + Node（前端打包产物内嵌）。
- **可选 Docker**：官方镜像包含 `ffmpeg`（官方也提供带 ffmpeg 的镜像）；我们可以基于其镜像扩展 Python 后端与前端。[GitHub](https://github.com/ggml-org/whisper.cpp)
- **Windows/macOS**：检测系统可执行名差异与路径分隔符；Homebrew 安装 `whisper-cpp`/`ffmpeg` 作为参考路径（非强依赖）。

------

# 10. 测试清单

- 各主流输入：wav/mp3/ogg/flac/mp4/mkv（视频只抽音频转码）→ CLI 推理 → srt/vtt 生成 → 页面播放/预览。
- 参数回归：核对每个 flag 的值覆盖到命令行（含默认值回退）。
- 大文件与并发、取消任务、失败重试。
- 无 ffmpeg / 无支持非 wav 的 CLI 时的降级策略。

------

# 11. 后续增强（可选）

- **参数预设**：保存/加载常用配置（如“极速草稿 / 高精度 / 翻译英语 / 逐词时间戳”等）。
- **模型下载器**：内置按型号/量化拉取官方模型清单。[GitHub](https://github.com/ggml-org/whisper.cpp)
- **多语言 UI** 与热键。
- **波形与逐词高亮**：用 `--output-json(-full)` 或 `-ml 1` 结果在前端高亮光标随时间滚动（实验性 word-level）。[GitHub](https://github.com/ggml-org/whisper.cpp)

------

# 12. 结论（是否需要 ffmpeg？）

- **需要，且强烈建议内置**：
  1. 统一各种**音视频格式**到 16k/mono WAV，使 CLI 稳定可用（或 Linux 开启 `WHISPER_FFMPEG` 也仍建议备选）；[GitHub](https://github.com/ggml-org/whisper.cpp)
  2. server 的 `--convert` 就是依赖 ffmpeg；[https://cnb.cool](https://cnb.cool/aigc/whisper.cpp/-/blob/3853d83d737efe0b6b9d8cfceefdc5fdd8ba3753/examples/server/README.md)
  3. **网页内预览**必须用 VTT（对 SRT 需转换），以及可选的容器内封/硬字幕处理，都离不开 ffmpeg/文本转换。[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/track?utm_source=chatgpt.com)[Super User](https://superuser.com/questions/1482965/adding-subtitles-via-command-line-in-ffmpeg?utm_source=chatgpt.com)

------

# 13. 需要你拍板的点

1. **是否按“CLI 为主 + Server 作为可选增强”** 的路线推进？
2. 前端组件库是用**官方 Material Web 3** 还是 **MUI（M3 主题）**？（我建议官方 M3 更贴合规范）[Material Design](https://m3.material.io/develop/web?utm_source=chatgpt.com)[GitHub](https://github.com/material-components/material-web?utm_source=chatgpt.com)
3. 是否要内置 **模型下载器**（指向官方 Hugging Face 存储）？[GitHub](https://github.com/ggml-org/whisper.cpp)
4. 是否需要 **字幕内封/烧制** 导出（预览仍走外挂）？
5. 初版是否只支持**单机本地**，后续再做多用户/权限？

你看看这份思路有没有要改的；你拍板后，我就开始搭骨架（FastAPI + React + M3），先把参数映射与任务流跑通，再补完预览与高级项。

##### 您说：

我不想使用React，我想使用vue3。无需字幕内封，无需多用户，无需链接HF下载模型，只使用本地模型，那么你会有一个怎样的新的开发计划（没改的地方不用说）。另外还有一个需要注意的地方，openvino每次运行前需要执行一个bat文件来设置一些环境变量，这个功能也要加上。Material 3 的实现哪个方便就用哪个。

###### ChatGPT 说：

好的，按你的新要求，我把**只需变更的部分**单独列出来（没改的就不重复了）：

# 变更版开发计划（仅列改动）

## 前端：改为 Vue 3 + Material 3

- **技术栈**：Vue 3 + Vite + TypeScript + Pinia（状态）+ Vue Router（路由）。

- **Material 3 实现**：优先用 **Material Web（@material/web）** 的 Web Components（原生 M3，和 Vue 3 兼容性好、无框架绑定）。

  - 在 Vue 里直接使用 `<md-filled-button> / <md-outlined-select> / <md-slider>` 等标签；用 `v-model` 场景会写一层极薄的绑定封装（把 `value`/自定义事件桥接为 `modelValue`/`update:modelValue`）。
  - 如果你更想用类库，备选是 **Vuetify 3**（有 M3 主题支持，工程化更“Vue 味”），但视觉与 M3 官方细节可能略有差异。默认我走 **@material/web**，你一句话就能切 Vuetify。

- **前端目录**：`/web` 改为 Vue 结构

  ```
  
  ```

```


```

- ```
  /web
    /src
      /components     # M3 控件封装（少量）
      /pages          # 任务页 / 预览页 / 设置页
      /stores         # Pinia
      /router
      /styles
      main.ts
  ```

## 字幕：仅外挂预览（不做内封/烧制）

- 去掉“内封/烧制/导出到 mp4/mkv”的功能与按钮。
- 保留 **SRT + 自动转 VTT**，网页内仍用 `<audio>/<video> + <track>` 进行预览。

## 模型：仅本地

- 去掉“模型下载/在线清单”。
- **模型面板**只保留“选择本地模型目录/文件（.bin/.gguf）”与最近使用的路径记录；做最基本的存在性/可读性校验。

## OpenVINO：运行前执行 .bat 初始化（Windows）

- **新设置项**（设置页）：
  - 「OpenVINO 初始化脚本（.bat）路径」
  - 「每次运行前执行」复选框
  - 「测试脚本」按钮（执行后显示新增/变更的环境变量）
- **执行策略**：
  - 在**每次启动 whisper 进程前**，后台先运行：
     `cmd /s /c call "<你的.bat>" && set`
     解析输出里的 `KEY=VALUE`，合并到当前进程的 `env`，再用该 `env` 启动 whisper（确保变量在同一子进程环境中生效）。
  - 失败时中止任务并把 stderr/返回码回传给前端（显眼提示“请以普通权限运行，确认 .bat 路径和 OpenVINO 安装完整”）。
  - （可选兼容）如将来在 Linux/Mac 可配置 `.sh`，保持同一机制；目前默认只做 Windows `.bat`。
- **安全**：仅允许执行**你在设置里明确指定**的脚本路径；脚本执行超时与日志截断保护。

## 用户/权限：单机本地

- 去掉多用户/登录相关；仅本机使用。
- 仍保留基本**文件白名单目录**与上传大小限制。

## 项目结构微调

- 后端基本不变；仅前端由 React→Vue。

- 根目录结构示意：

  ```
  
  ```

```


```

- ```
  /app      # FastAPI 后端（原结构不变）
  /web      # Vue 3 + Vite 前端
  ```

## 时间线（更新）

1. **D1-D2**：前端脚手架（Vue 3 + Vite + @material/web），主题/配色、基础布局；参数面板壳。
2. **D3-D4**：后端增加 **OpenVINO .bat 环境装载**能力与「测试脚本」API；命令生成器适配。
3. **D5**：任务跑通（含 ffmpeg 转码与 SRT/VTT 落盘）；进度与日志 WebSocket。
4. **D6**：预览页（音/视频 + VTT 轨道）；可取消/失败重试。
5. **D7**：设置页与模型/可执行文件选择；路径校验与持久化。
6. **D8**：稳定性与跨平台（Windows 优先）测试。

## 测试要点（新增/调整）

- **.bat 环境**：
  - 脚本缺失/报错/权限不足/路径含空格；多次调用是否正确覆盖 PATH/LD 路径。
  - 执行超时与回滚策略（不中断 UI，但任务不启动）。
- **仅本地模型**：不可读/损坏模型文件提示；切换模型后任务正确使用新路径。
- **字幕**：仅外挂 VTT 预览；SRT→VTT 转换在极端时间戳（重叠/负数/越界）下的健壮性。

------

### 待你拍板

1. **Material 3 实现**：默认走 **@material/web**（纯 M3），还是你要 **Vuetify 3**？
2. **OpenVINO 脚本**：仅做 Windows `.bat` 就好，还是要顺手把 Linux/Mac `.sh` 也兼容一下？

你确认后我就按这个新计划开工。

##### 您说：

使用@material/web；顺手把 Linux/Mac .sh 也兼容一下。我已确认，记得告诉我项目的目录，有什么文件，文件放哪里，运行什么之类的，相信你能做好的

###### ChatGPT 说：

太好了，咱就按 **Vue 3 + @material/web + FastAPI（Python）+ CLI 调用 whisper.cpp + ffmpeg + OpenVINO init 脚本** 来落地。我把你要的**项目目录、关键文件放置、怎么运行**都写清楚了（之前没改的设计不再重复）。

------

# 项目总览（实现要点）

- 前端：**Vue 3 + Vite + TypeScript + @material/web**（原生 Material 3 Web Components）
- 后端：**FastAPI + Uvicorn**（Python 3.10+）
- 调用链：浏览器 → FastAPI → （必要时 ffmpeg 转 WAV）→ 调用 **whisper CLI** → 生成 **SRT/VTT/JSON** → 浏览器 `<audio>/<video> + <track>` 预览
- OpenVINO：**推理前可选执行初始化脚本**（Windows `.bat`、Linux/macOS `.sh`），把脚本导出的环境变量合并进同一子进程环境后再启动 whisper
- 仅本地模型、本地可执行文件，不做内封字幕、不做多用户

------

# 目录结构（你关心的“文件放哪儿”）

```



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

------

# 关键点落地说明

## 1) OpenVINO 初始化脚本（Windows `.bat` + Linux/Mac `.sh`）

- **设置页字段**：
  - 脚本路径：`openvino.init_script_path`
  - 每次运行前执行：`openvino.enabled`（bool）
  - Shell 类型（可自动判断，也可手选）：`openvino.shell` = `auto | cmd | bash`
  - “测试脚本”按钮：后端执行脚本 → 把**新增/变更的环境变量 diff** 回显（只展示白名单 key，如 `PATH`, `LD_LIBRARY_PATH`, `INTEL_OPENVINO_DIR` 等）
- **执行方式（后端 `core/openvino_env.py`）**：
  - **Windows**：`cmd /s /c call "<script>.bat" && set`
  - **Linux/macOS**：`bash -lc 'source "<script>.sh" && env'`
  - 解析输出为 `KEY=VALUE`，与当前进程 `os.environ` 合并，**仅对本次 whisper 子进程生效**（不污染全局）。
  - 超时/非零退出码 → 中止任务，返回可读错误信息。
- **安全**：脚本路径需在白名单目录或用户显式确认，禁止任意上传执行。

## 2) ffmpeg/whisper 探测与转码

- `GET /api/probe`：返回 `ffmpeg`, `ffprobe`, `whisper` 是否可用及版本号；可执行路径是否有效。
- 上传/选择源文件后，`ffprobe` 检测是否需要转码（目标：**16k/mono/pcm_s16le WAV**）；需要则在任务目录内生成 `input.wav` 再喂给 whisper。

## 3) 任务与输出

- `POST /api/tasks`（multipart 或 JSON）：
  - 允许传**上传文件**或**服务器现有路径**（白名单内）
  - 允许传 whisper **全部参数**（UI 里勾选/输入的值）
  - 返回 `jobId`
- `GET /api/tasks/{jobId}`：状态；产物清单（`.srt`, `.vtt`, `.json`, `.txt`…）
- `DELETE /api/tasks/{jobId}`：取消（终止子进程）
- `WS /ws/tasks/{jobId}/logs`：实时日志/进度
- **自动生成 VTT**：如果只勾了 SRT，后端也会顺手产出 `.vtt` 用于网页 `<track>` 预览

------

# 安装 & 运行（Dev / Prod）

## 前置要求

- **Python 3.10+**
- **Node 18+**
- **ffmpeg / ffprobe**（系统可执行 PATH 中，或在 Settings 指定绝对路径）
- **whisper.cpp 可执行文件**（比如 `whisper-cli` / `main.exe`），**模型文件**（`.bin`/`.gguf`）
- Windows 场景如需 OpenVINO：准备好你的 `.bat`；Linux/macOS：准备 `.sh`

## 开发模式（前后端分离，Vite 代理）

```



# 1) 后端
cd whisper-webui/app
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2) 前端
cd ../web
npm i
npm run dev    # 默认 http://localhost:5173，已代理 /api 和 /ws 到 8000
```

打开浏览器 → **Settings** 页面先设置：

- Whisper 可执行路径
- 模型文件/目录
- （可选）OpenVINO 脚本路径并勾选“每次运行前执行”，点击“测试脚本”
   然后到 **Tasks** 页面上传/选择文件，设置参数，一键开始。

## 生产模式（后端托管静态资源）

```



# 构建前端
cd whisper-webui/web
npm ci
npm run build   # 输出到 web/dist

# 拷贝到后端静态目录（脚本会在项目里提供）
cp -r dist/* ../app/static/

# 启动后端（生产）
cd ../app
uvicorn main:app --host 0.0.0.0 --port 8000
# 或者用 gunicorn + uvicorn workers
```

然后访问 `http://<服务器>:8000/`（后端会把 `/` 映射到 `app/static/index.html`）。

------

# 依赖清单（摘）

`app/requirements.txt`（示例）

```



fastapi
uvicorn[standard]
pydantic
python-multipart
websockets
starlette
```

> 注：SRT→VTT 我们用自实现文本转换，**不额外引第三方库**；如你偏好库，也可加 `webvtt-py`（非必须）。

`web/package.json`（关键）

- `vite`, `vue`, `pinia`, `vue-router`, `typescript`
- `@material/web`（M3 组件）
- 开发时 `vite.config.ts` 里把 `/api`、`/ws` 代理到 `http://localhost:8000`

------

# 路由/接口一览（给你心里有数）

- **设置**
  - `GET /api/settings` / `POST /api/settings`
  - `POST /api/openvino/test`（执行脚本，返回 env diff）
  - `GET /api/probe`
- **任务**
  - `POST /api/tasks`（创建）
  - `GET /api/tasks/{jobId}`（查询状态/产物）
  - `DELETE /api/tasks/{jobId}`（取消）
  - `WS  /ws/tasks/{jobId}/logs`（实时日志）
- **文件**
  - `GET /api/files/{jobId}`（列出）
  - `GET /api/files/{jobId}/{name}`（下载）

------

# 使用小贴士

- **路径含空格**（尤其 Windows）没问题：后端执行前会统一做 **quoting/escape**。
- **白名单目录**：上传与“服务器现有文件选择”都限制在配置的根目录；避免越权访问。
- **性能**：不要把 `--threads` 开太离谱（一般与物理核数一致或略低）；队列里可以限制并发任务数量。
- **进度**：勾 `--print-progress` 时，日志里会有更细的阶段信息，WS 会推给前端。

------

# 下一步

如果目录/流程 OK，我就按这个结构开工：先提交一个**能跑的骨架**（接口打通、基础参数→命令映射、OpenVINO 脚本兼容、SRT→VTT + 预览），然后我们再一起把**全参数面板**填满。你也可以先把：

- Whisper 可执行文件路径
- 模型文件路径
- OpenVINO 脚本路径（如果需要）
   准备好，等我第一版提交就能直接跑起来了。

##### 您说：

我想知道这个开发能否在linux里运行（最终我想在windows里使用，这个webui的开发过程在别的平台应该没关系吧

###### ChatGPT 说：

已推理，持续 几秒

###### ChatGPT 说：

是的，整个 Web UI 的开发过程**在 Linux 上进行是完全可以的**，你可以在 Linux 开发和调试这个 Web UI，然后将其部署到 Windows 上使用。让我们逐步来看一下为什么可以：

### 1. **后端（FastAPI）**

- **兼容性**：FastAPI 和 Python 是跨平台的，理论上在 Windows 和 Linux 上是一样的。开发过程中，Linux 环境完全可以用于后端 API 和任务调度，甚至你可以在 Linux 上直接调试 Whisper 和 FFmpeg 的调用。
- **OpenVINO**：你提到 OpenVINO 脚本需要执行，但因为你最终会在 Windows 上运行，所以在 Linux 上只需要确保 OpenVINO 环境变量的设置部分没有问题。
  - 对于 Windows 和 Linux，我们会在脚本中处理 `.bat`（Windows）和 `.sh`（Linux/macOS），在 Linux 中测试 OpenVINO 脚本的执行也是一个常见的开发步骤，**不影响最终在 Windows 上的使用**。

### 2. **前端（Vue 3 + Vite + Material 3）**

- **兼容性**：Vite 和 Vue 3 都是跨平台的，可以在 Linux 环境下开发和打包。在 Linux 上的开发和调试与 Windows 上的运行没有任何冲突。你可以使用 Linux 开发 UI，构建并查看界面，所有的前端功能和交互是跨平台的。
- **@material/web**：Material 3 的 Web Components 完全支持跨平台，基于浏览器实现，与操作系统无关。**在 Linux 上开发时，你不会遇到与平台相关的问题**。

### 3. **Whisper 和 FFmpeg**

- **Whisper**：whisper.cpp 本身是 C++ 实现的，只要你确保 C++ 环境与编译器兼容，在 Linux 上的开发也不会妨碍最终在 Windows 上的运行。Linux 上调试、运行 whisper-cli 完全没问题，且对于跨平台调试非常重要。
- **FFmpeg**：FFmpeg 同样是跨平台的，它在 Linux 和 Windows 上的用法一致。在开发过程中，你可以使用 FFmpeg 在 Linux 上完成音频格式转码等工作，完全兼容 Windows 环境。

### 4. **部署到 Windows**

- **部署过程**：一旦前端和后端在 Linux 上都开发完成，你可以将整个应用迁移到 Windows。Linux 和 Windows 都支持 Python 和 Node.js 环境，所以将项目移植到 Windows 上非常简单。
  - 只需要安装相关的依赖项（Python, Node.js 和 FFmpeg 等），然后通过修改配置文件来适应 Windows 路径和环境变量即可。
  - 对于 OpenVINO 这部分，你只需要在 Windows 上确保 `.bat` 脚本可以正确运行即可。Windows 上的 OpenVINO 环境变量配置也应该与 Linux 上的 `.sh` 环境变量配置类似（只是路径和脚本不同）。

### 5. **平台差异**

- **文件路径与环境变量**：主要的差异可能在于文件路径的分隔符（Linux 使用 `/`，Windows 使用 `\`），以及在环境变量配置方面。你可以在配置文件里保持对不同操作系统路径格式的适配。
- **`.bat` 和 `.sh` 脚本**：Linux 上会使用 `.sh` 脚本，Windows 上使用 `.bat`，但这只是脚本和环境配置的差异，核心功能不会受到影响。

------

### 总结：

- **开发阶段**：你可以完全在 Linux 环境下开发、调试、构建 Web UI 和后端 API。只要你确保在配置文件中能够支持跨平台的路径和环境变量，Linux 上的开发不会影响最终在 Windows 上的使用。
- **部署到 Windows**：开发完成后，将整个项目部署到 Windows 上只需要适配文件路径（`/` → `\`）和 OpenVINO 环境变量（Windows `.bat` 配置），其他功能不会有问题。

简而言之，这个 Web UI 的开发过程完全可以在 Linux 上进行，**最终的 Windows 部署不会受到影响**。

##### 您说：

前端构建好后，如果我想开源到github上给别人用别人还需要bom build吗，我想减轻别人使用的工作量

###### ChatGPT 说：

完全可以做到**别人不用再 build 前端**。

# 最简单的开源分发方案（推荐）

把前端打包好的产物直接放进后端的 `app/static/`，提交到仓库里。这样别人：

1. 不需要装 Node，也不需要 `npm build`；
2. 只要有 Python（和 ffmpeg、whisper.cpp 可执行以及本地模型），就能跑。

典型使用流程就是：

```



git clone <repo>
cd whisper-webui/app
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
# 浏览器打开 http://localhost:8000
```

> 你刚才说的 “bom build” 我理解成 “npm build”。按上面做，**别人完全不需要 npm build**。

# 为用户减负还能再做这些（可选但很香）

- **提供一键启动脚本**
  - `run.bat`（Windows）/`run.sh`（Linux/Mac）：自动建 venv、装后端依赖、启动 Uvicorn，并自动打开浏览器。
  - 再加 `openvino_example.bat/.sh` 模板，用户只需把 OpenVINO 安装路径写进去，在设置页勾选“每次运行前执行”即可。
- **Release 压缩包**
  - 在 GitHub Releases 里发布 `whisper-webui-win64.zip` / `whisper-webui-linux-x64.tar.gz`：包含已经打好的 `app/static/`、后端源码、`run.*` 脚本。用户下载解压→双击运行脚本即可。
- **CI 自动打包（避免忘了手动拷 dist）**
  - 用 GitHub Actions：在打 tag 时自动执行 `npm ci && npm run build`（在 `/web`）、把产物复制到 `app/static/`，打包并上传到 Release。这样仓库主分支也可保持“源码整洁”，同时发布页永远有“可直接跑”的包。

# 仓库里要注意的两点

- **版本对齐**：给前端构建产物做个版本标记（例如把 git commit hash 写入 `index.html` 的注释或 `window.__APP_VERSION__`），避免后端与前端不匹配时不好排查。
- **忽略/保留策略**：如果你选择把 `app/static/` 一直提交到主分支，记得把 `/web/dist/` 忽略掉（只把 dist 拷到 `app/static/`）；或者走 CI 只在 Release 产物里携带静态文件。

# 一句话总结

- 你**先在本机把前端 build**，把 `web/dist` 拷到 **`app/static/` 并提交**；
- 给仓库加上 `run.bat` / `run.sh`；
- 用户只需 Python 环境 + ffmpeg + whisper.cpp + 本地模型，**无需 Node、无需再 build**，开箱即用。

ChatGPT 也可能会犯错。OpenAI 不会使用您的工作空间数据来训练其模型。