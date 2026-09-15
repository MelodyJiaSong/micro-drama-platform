# 即梦网页桥接服务（jimeng_web_bridge）

> **状态：开发中（spec-driven stage 6）。** 规格见 `specs/development/jimeng_web_bridge/final_specs/spec.md`（v2），验证策略见同目录 `validation/strategy.md`。本 README 随功能落地逐步更新。

## ⚠️ 先读这条：账号与条款风险

- 即梦《用户服务协议》5.1 条明文禁止「使用任何自动化程序、软件或类似工具接入即梦AI」；《付费服务协议》6.5 / 8.2 条允许平台作废权益、冻结或永久封禁账号。**本服务驱动网页属于自动化，风险由使用者本人承担。**
- 本项目只面向**本人账号、本机、个人自用**。服务只绑定 `127.0.0.1`，不要把它开放给别人，那可能构成「许可他人使用账号」。
- 服务端强制执行的收敛措施：单账号、单浏览器 profile、固定提交间隔、并发上限、**提交零自动重试**、**只有人在本地网页里能确认花积分**、不做任何反检测（不装 stealth、不伪造请求、不解验证码）、图片走官方 `dreamina` CLI。
- 上传的素材按《用户服务协议》9.3 条授权平台用于优化模型。写实真人照片做参考图或主体可能被平台拒绝。

## 它做什么

一个本地常驻服务。视频走「驱动你已登录的即梦网页」，图片走「官方 `dreamina` CLI」，把 **上传参考 → 填 prompt → 设参数 → 提交 → 等待 → 下载落盘** 这条链路做成三种接口：

| 接口 | 给谁 | 能做什么 |
|---|---|---|
| 本地管理网页 `http://127.0.0.1:8790/` | 你 | 登录状态、每部剧的 config、**批次确认**、队列看板、历史与积分、主体对账、全局设置 |
| MCP `http://127.0.0.1:8790/mcp` | Claude | 预检一批 shot、查询和等待作业、取消 / 恢复、分步调试（到预演为止）、主体同步 / 对账 |
| HTTP `http://127.0.0.1:8790/api/*` | 脚本 | 与 MCP 相同 |

**Claude 和脚本都不能确认批次。** 它们只能拿到确认页链接，确认按钮只在本地网页上，由你亲自点击。请不要让 Claude 用浏览器自动化工具去点这个按钮。

## 前置条件

- Windows 11、已安装 Chrome、Python ≥ 3.11、Node.js（构建 UI 用）、`ffprobe`（校验下载文件用）。
- 官方 CLI `dreamina` 已安装并登录（`dreamina login`），默认路径 `~/bin/dreamina.exe`。

## 安装与启动

```powershell
cd projects/jimeng_web_bridge
make install      # 建 .venv、装依赖、装 UI 依赖
make init         # 在仓库根 .env 写入 JIMENG_BRIDGE_TOKEN（已存在则不动），创建 .data/ 与 HMAC 密钥
make ui-build     # 构建管理网页
make run          # 启动服务（API + MCP + UI，单进程）
```

首次启动会弹出一个**独立**的 Chrome 窗口（专用 profile，在 `.data/chrome_profile/`），请在里面手动扫码登录即梦一次，之后服务会复用这个登录状态。服务不会替你输入任何账号凭据。

## 接入 Claude Code（MCP）

在仓库根 `.mcp.json` 的 `mcpServers` 里加：

```json
"jimeng_bridge": {
  "type": "http",
  "url": "http://127.0.0.1:8790/mcp",
  "headers": { "Authorization": "Bearer ${JIMENG_BRIDGE_TOKEN}" },
  "timeout": 120000
}
```

## 数据放在哪

| 内容 | 位置 | 进 git |
|---|---|---|
| 全局 config | `projects/jimeng_web_bridge/config/global.toml` | 是 |
| 每部剧 config | `ai_videos/{剧}/jimeng_config.toml` | 是 |
| 视频产物 | `ai_videos/{剧}/…/shots/shotNN/renders/shotNN_{时间}.mp4` + `.jimeng.json` sidecar | 媒体走 R2，sidecar 进 git |
| 图片候选 | `ai_videos/{剧}/…/{主体目录}/_candidates/{路由键}/` | 同上 |
| 作业库、浏览器 profile、截图、日志、HMAC 密钥 | `projects/jimeng_web_bridge/.data/` | 否 |
| API token | 仓库根 `.env` 的 `JIMENG_BRIDGE_TOKEN` | 否 |

## 测试

```powershell
make test        # 单元 + 集成 + e2e，全部对离线假即梦站点和假 dreamina，不花积分
make test-perf   # 性能预算
make canary      # 人工触发：对真实站点做只读自检，不点生成
```

自动化测试在 `JWB_TEST_MODE=1` 下运行，有硬护栏：浏览器起始地址必须是 localhost、CLI 必须是假的，否则直接中止。
