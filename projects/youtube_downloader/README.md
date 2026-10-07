# YouTube 本机下载工具

双击 `start.cmd` 启动窗口，粘贴单视频/Shorts 链接，选择目录和清晰度，点击「开始下载」。默认保存到用户的 `Downloads/YouTube`。

首次运行需 Python 3.11+，启动脚本会创建项目 `.venv` 并安装依赖。另需 FFmpeg（含 ffprobe）与 Deno 加入 PATH，本机已检测到。新机器可用 `winget install yt-dlp.FFmpeg` 和 `winget install DenoLand.Deno`，安装后重开终端。

视频保存 MP4，清晰度选项是**高度上限**；最佳可用保留较高画质，编码可能是 AV1/VP9，需要较新的播放器。选择「仅音频 MP3」可提取音频。下载和合并完成后日志显示文件路径。重复下载保护已有文件；取消保留分片，在同目录用相同选项重试可尝试续传。

默认不读取登录信息。只有选中浏览器时才使用其本机登录；Windows 浏览器锁文件或解密问题可能导致失败。登录不能保证受限制的视频可下载，也不支持纯播放列表、频道和已删除视频。

更新下载核心：

```powershell
.\.venv\Scripts\python.exe -m pip install -U "yt-dlp[default]"
```

调试入口（项目目录）：

```powershell
.\.venv\Scripts\python.exe -m apps.cli.main "https://www.youtube.com/watch?v=视频ID" --height 1080 -o "D:\Videos"
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -q
```

实现与验收范围见 `../../specs/development/youtube_downloader/`。下载过程受网络、视频权限与 YouTube 风控影响；失败会显示实际日志。
