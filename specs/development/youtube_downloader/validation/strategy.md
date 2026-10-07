# 下载工具验收策略

Run: youtube_downloader-20261004-094351

## Levels chosen
acceptance_criteria、bdd_scenarios：用户窗口与命令行契约。unit_tests：链接及选项。system_tests：真实 Tk、下载核心、FFmpeg 与取消。security：外部输入、登录边界和本任务进程树。

## Per-level summary
分别见同目录各层文件。原生 Tk 没有浏览器/API，以真实事件循环的窗口测试替代浏览器测试。

## Cross-cutting concerns
YouTube 外部访问与本地 HTTP 下载分开记录；本地测试不证明 YouTube 成功。cookies 不自动读取，不用用户账号验收。分片续传取决于源服务器支持，不承诺任意源。

## How runtime validation will use this
三个工作单元：download_core、desktop_cli、launch_and_integration。真实下载集成生成小片、HTTP 提供媒体、调用实际 yt-dlp/FFmpeg，再以 ffprobe 核查。测试失败修复后重验，最后启动检查。平台集成、频道/播放列表不在本次实现与验证范围；用户明确选择独立窗口，无需扩大到平台。

## Promotion-preservation check
新项目没有 promoted.md。未执行再生成或删除原项目。

## Manual walkthrough
自动化通过后发出 validation.requires_manual_walkthrough。最终窗口布局、焦点及用户自己的 YouTube 链接仍需用户试用；不宣称自动化替代人工体验验收。
