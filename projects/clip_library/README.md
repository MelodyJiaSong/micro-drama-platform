# 素材库（clip_library）

做「长采访提炼成 Short」用的素材地基：按授权搜 YouTube，批量下载视频和字幕并记录授权，在字幕里找原话，按授权截取 9:16 片段并加出处卡。第一期只做 YouTube，抖音和 TikTok 暂不做。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt pytest
```

需要 FFmpeg 在 PATH 中，出处卡用 Windows 自带的微软雅黑。

## 用法

```powershell
$cli = ".\.venv\Scripts\python.exe -m apps.cli.main"
# 搜索：默认只看 CC 授权；--duration long 表示 20 分钟以上，--order views 按播放量
& $cli search "jensen huang interview" --duration long --order views --limit 20
# 首次或登录过期时：弹出独立 Chrome，登录 YouTube 后关窗，登录状态导出到本机，之后自动使用
& $cli login
# 下载：可传链接、--file 链接清单或 --search 搜索结果
& $cli download --search "naval ravikant" --duration long --limit 10
& $cli download URL --license permission --note "作者 2026-11-14 邮件同意切片"
& $cli list
& $cli find "how hard could it be"
& $cli cut <视频ID> 12:03 12:11            # 默认 9:16，加 --horizontal 保留原比例
```

素材库默认在 `library/`（不进 git），可用 `--library` 或环境变量 `CLIP_LIBRARY_DIR` 改位置。

| 路径 | 内容 |
|---|---|
| `sources/{ID}/` | `video.mp4`、`video.{语言}.vtt`、`info.json`；`source.json` 是授权记录，也是下载完成的标记 |
| `clips/{片段ID}/` | `clip.mp4`、按语言出的 `clip.{语言}.srt`（时间从片段起点算）、`attribution.txt` |
| `clips.jsonl` | 每次截取的出处台账，发布时据此写来源 |

## 授权规则

| 授权 | 怎么判定 | 截取限制 |
|---|---|---|
| `cc_by` | 平台标了 Creative Commons 时自动记录；平台没标就不能手动记成 CC | 不限 |
| `permission` / `public_domain` | 手动指定，必须用 `--note` 写明依据 | 不限 |
| `quote` | 其余全部归为未授权，只能短引用 | 每段最多 10 秒（`QUOTE_MAX_SECONDS`） |

YouTube 的 CC 标签由上传者自己设置。如果是别人的内容被搬运后标成 CC，这个标签并不能带来授权，所以要优先用官方频道的视频。截取限制只是工具层面的护栏，不能当作合理使用的法律保证。

## 限制

- YouTube 会对视频详情页要求登录验证（搜索不受影响），所以下载前先跑 `login`。登录用的是独立的 Chrome 配置，不影响平时用的 Chrome，登录状态保存在 `%LOCALAPPDATA%\clip_library\cookies.txt`（不在仓库内）。也可以用 `--cookies` 指定其他文件。
- 默认下载英文和中文字幕。英文视频的中文字幕是 YouTube 自动翻译的，经常被限流（429），失败时只跳过字幕、不影响视频。实际拿到了哪些字幕，记录在 `source.json` 中。
- 批量下载时每条视频之间会随机等待 3 到 8 秒。已下载的视频自动跳过，中断后重跑同一命令即可接着下。

## 开发

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

规格见 `../../specs/development/clip_library/`。
