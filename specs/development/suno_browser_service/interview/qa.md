# 需求澄清

类别：浏览器部署、生成授权、服务调用与恢复。

用户于 2026-10-22 确认：
- 本机后台浏览器，兼容 Browserless 接入。
- Suno 作为例外，自动生成并下载。

实现判断：HTTP+OpenAPI；本机单账号串行；SQLite 持久化；MP3 默认、WAV 可选；首次由用户在独立浏览器登录。重启后未知提交不重提，已知歌曲仅恢复下载。

Follow-up 002：用户要求尽量涵盖网页选项、上传参考与模式，并友好支持 Claude Code/Codex。自主选择共享请求 schema + JSON CLI + stdio MCP + 共用 skill，保留旧请求兼容。验证码暂停期间只做离线验证，新增界面功能不得标作真实账号验收通过。

Follow-up 003–005：补齐人/代理都可读的 API/MCP description 和调用示例；增加同源本机 UI；全流程所有新音频生成默认 Suno。用户无需再决定框架/布局：选择 React/TypeScript、light theme、schema 驱动选项、原 API 鉴权与稳定任务键。TTS/克隆等缺口明确保留，不自动换引擎；不修改既有媒体。
