# jimeng_web_bridge（项目已删除，本目录为历史记录）

`projects/jimeng_web_bridge`（即梦网页自动化桥接服务）已于 2026-10-11 删除。依据是 `ai_video_management` follow-up 239：用户决定删除旧的独立软件项目。本目录保留当时的需求、访谈、调研、规格与验证文档，不再维护。文中出现的 `projects/jimeng_web_bridge/…` 路径都已不存在。

- **删除原因**：项目的数据契约绑定旧流程，按旧 `shot*.md` 版式解析，资产目录用 `scenes/`，每部剧需要一份 `jimeng_config.toml`。它也没有登记为收费服务入口。项目自己的 README 写明网页自动化违反即梦《用户服务协议》5.1。现行出片改走官方 `dreamina` CLI，入口是 `tools/service_call.py` 与 `tools/shot_take.py`。
- **查看旧代码**：删除前的最后一版在提交 `c2f32612`，例如 `git show c2f32612:projects/jimeng_web_bridge/README.md`。
- **本地运行数据**：`.data/` 下有专用 Chrome profile（含即梦登录态）和 probe 记录，`.venv` 里是依赖。这些都随目录删除，没有备份。删除清单记在本机审计目录 `.audit/legacy_removal_20261011/followup239/`，该目录不入库。
