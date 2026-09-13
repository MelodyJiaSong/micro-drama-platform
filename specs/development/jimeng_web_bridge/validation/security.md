---
worker_id: level-specialist-05-security
stage: 5
role: level-specialist
level: security
status: complete
blockers: []
confidence: medium
---

# Validation — security（jimeng_web_bridge）

依据：`final_specs/spec.md`（NFR 安全 / 账号风险、FR-1/2/4/7/8/10/13–16/18–20/24/26–28/30/34–36/38–44/51–55、§5.10）、`findings/angle-mcp-http-interface.md`（§2.3 DNS rebinding / CVE-2025-66416）、`findings/angle-platform-limits-risk.md` §2.5、`agent_refs/validation/{general,development}.md`（§7 / §11）。

> confidence = medium：检查项本身明确，但 §15 列出的 spec 缺口（尤其 G-1、G-2、G-4）需要 parent 回写 spec 后，部分检查的期望值才能最终写死。

---

## 0. 范围、威胁模型、判级、执行映射

**受保护资产**
- 已登录的即梦会话（`.data/chrome_profile`）；
- 付费积分；
- 仓库文件（`ai_videos/`、`.env`、`projects/`）；
- `JIMENG_BRIDGE_TOKEN`；
- 截图、DOM 快照、trace（可能含账号信息与 cookie）。

**威胁来源**
- **A1 浏览器上下文攻击者**：本机任意浏览器里的任意网页，包括自动化 Chrome 里打开的即梦页本身，以及 DNS rebinding。
- **A2 同机非浏览器进程**：
  - 最现实的是「过度热心的 agent」：被 403 后自己加 header 重试、改 config 绕过护栏；本仓库当前会话就运行在 bypass permissions 模式下；
  - 其次是恶意进程。
- **A3 局域网其他机器**。
- **A4 被篡改或写错的文本输入**：shot md、资产卡、`.link.json`、TOML config。
- **A5 供应链**。
- **A6 平台侧**（ToS 执法）：不可测，见 §16。

**信任边界声明**：同一 Windows 用户下的恶意进程能直接读 `.env` 与 profile。因此 bearer token 防的是 A1、A3、「未授权的自动化 / agent 误用」以及 SSRF 类请求，**不防恶意的 A2**。它残余的风险记入 §16 R-2。

**判级**
- 按 `general.md` 标准严重度表：任何 SEC-* 失败为 `critical`，立即 halt；未经用户明确批准不进入修订轮。
- 例外项逐条标 `warning` 并写理由：供应链公告、锁版本、localhost DoS-lite、dev-proxy 守护、子进程超时、日志注入。
- 标「待 spec 定案」的检查，期望值随 §15 缺口回写而最终确定；缺口未决时，stage-5 签字前按 `general.md` §6 处理。

**测试落点**：遵循 `development.md` §6（`tests/api/` 镜像 `apps/api/`，`tests/libs/**` 镜像 `libs/**`，`tests/ui/` 放前端）。对组装后的 app 或整个仓库做的跨切面扫描统一放 `tests/api/security/`。

**共用 fixtures**
- `SENTINEL-` 前缀的随机 token；
- fake 即梦站点，跑在 `127.0.0.1:<随机端口>`，会记录点击 / 输入 / 请求；
- fake `dreamina`：**原生 `.exe` 启动器**，把 argv 和 env 写成 JSON，与生产的启动路径同类；
- tmp 仓库副本（含真实 `ai_videos/` 片段）；
- directory junction（Windows 下无需管理员，必须真跑）。

**work_unit_kind → 本级检查**

| work_unit_kind | 运行的 SEC 组 |
|---|---|
| `boot_smoke` | N01, N08, N11, B05, S05, P03 |
| `backend_api`（routes + middleware） | N02–N14, C07, C08, F03, F06, F11, K03–K05, S06, S07, R01–R04 |
| `mcp_tools` | N12, C09, C10, S07, R01 |
| `domain` / `application` | C01–C06, C11–C13, F01, F04, F07, F10, K01, K02, K06, T03, T04 |
| `browser_backend` | B01–B06, F08, F09, S02, S03, T05–T07 |
| `cli_backend` | P01–P06, F09 |
| `frontend_component` | U01–U04, C14 |
| 全项目收尾 | S01, S04, S09, T01, T02, T08, D01–D04 |

---

## 1. `general.md` §7 / `development.md` §11：会改写 header 或路径的层

spec 只有单一运行模式：`make run` 单进程，没有 Vite dev proxy，也没有反向代理。但同一进程内仍有三层会改变闸门看到的请求：

| 层 | v1 是否存在 | 改写内容 | 必测形状 |
|---|---|---|---|
| Vite dev proxy（§11 三形状） | **不存在** | — | N/A；由 SEC-N13 守护，将来一旦新增 dev 模式，§11 三形状立即成为 blocker |
| 反向代理 / CDN | 不存在 | — | N/A |
| uvicorn `ProxyHeadersMiddleware` | **默认存在**：`proxy_headers=True`，且信任 `127.0.0.1` | 根据 `X-Forwarded-For` / `X-Forwarded-Proto` 改写 `scope.client` 与 `scheme`；本服务所有客户端都是 127.0.0.1，等于全信任 | pre-mutation（真实 uvicorn，带伪造转发头）+ post-mutation（直接 ASGI scope）→ SEC-N11 |
| Starlette `Mount("/mcp")` + MCP SDK 自带 `TransportSecuritySettings` | 存在（同进程路由） | 改写 `scope.path` / `root_path`；SDK 闸门看到的是挂载后的形状 | pre-mount（完整 app，外层闸门）+ post-mount（子应用单独调用，SDK 闸门）→ SEC-N12 |

结论：本项目不需要 §11 的 dev-proxy 三形状；但 §7 的原则适用于上表后两层，两种形状缺一即 `critical`。

---

## 2. 鉴权判定表（stage-5 对 NFR「同源 UI 通过 Origin 校验放行」的解释，见 Gap G-1）

浏览器对同源 GET 请求**不发 `Origin`**，所以只看 Origin 的判定对 GET 无定义，也挡不住「非浏览器客户端伪造 Origin」。本表改用浏览器强制附带、页面 JS 无法伪造的 fetch-metadata 头（`Sec-Fetch-*`，Chrome / Edge / Firefox 对 `http://127.0.0.1`、`http://localhost` 均会发送）。本表对所有路径生效：`/`、静态资源、`/api/*`、`/mcp`。

| 步 | 条件 | 结果 |
|---|---|---|
| G0 | socket 对端 `scope.client` ≠ `127.0.0.1` | 403 |
| G1 | `Host` 头不唯一，或 ∉ {`127.0.0.1:8790`, `localhost:8790`}（主机名大小写不敏感，端口精确） | 403 |
| G2 | 存在 `Origin`，且 ∉ {`http://127.0.0.1:8790`, `http://localhost:8790`}（`null` 也算非法） | 403，**token 不豁免** |
| G3 | `Sec-Fetch-Site` ∈ {`cross-site`, `same-site`} | 403，token 不豁免 |
| G4 | 存在 `Authorization` | 必须是 `Bearer <token>` 且常量时间相等，否则 403。分类为 `bearer`：HTTP 请求记 `confirmer=http_auto`，`/mcp` 请求记 `mcp`。即使同时带合法 Origin，也不算 UI |
| G5 | 无 `Authorization`，`Sec-Fetch-Site: same-origin`；非 GET/HEAD 时还要求 Origin 合法 | 分类为 `ui_browser`，记 `confirmer=ui_human`；该分类访问 `/mcp` 一律 403 |
| G6 | 无 `Authorization`，GET/HEAD，`Sec-Fetch-Mode: navigate`，`Sec-Fetch-Site` ∈ {`none`, `same-origin`}，路径是 UI 页面（不在 `/api`、`/mcp` 下） | 放行：地址栏直接打开、toast 点击 |
| G7 | 其余（无 `Authorization`，也没有浏览器 fetch-metadata） | 只放行 `GET /api/health`，其余 403 |

补充规则：
- `confirmer` **只能**由本表的分类推导，不接受请求体自报。
- 本表列出的 HTTP 判定无法区分「伪造了完整 fetch-metadata 的本机进程」与真实浏览器，这一点见 §16 R-2。

---

## 3. 网络暴露

**SEC-N01 绑定地址锁死** · critical · 自动 `tests/api/test_main__bind.py`
- 威胁：A3 局域网访问，等于把账号给他人使用（协议 3.5）并替他人花积分。
- 测试：
  - `server.host` 分别取 `0.0.0.0`、`::`、`192.168.1.10`、`""`、`127.0.0.2`、`localhost.evil.com`，分别经 `global.toml` 与 `PUT /api/config/global` 写入；
  - 静态断言 `main.py` / Makefile `run` 目标不接受 `--host` 覆盖；
  - boot smoke 后用 `psutil.net_connections()` 列出本进程的监听。
- 期望：
  - 非法值：启动前抛 `ConfigError` 退出（码 ≠ 0），未监听任何 socket；
  - PUT：422，文件不变（另见 SEC-P04）；
  - `localhost` 实际绑定到 `127.0.0.1`；
  - 监听集合恰为 {`127.0.0.1:8790`}。

**SEC-N02 对端地址兜底** · critical · 自动 `tests/libs/infrastructure/middleware/test_host_origin__middleware.py`
- 威胁：绑定被意外放宽后（例如日后有人加 `--host`），闸门本身还要能拒绝非本机对端。
- 测试：ASGI scope `client=("192.168.1.5", 5000)`，其余 header 与 token 全部合法。
- 期望：403。对端地址取自 socket，不受转发头影响（SEC-N11）。

**SEC-N03 Host allowlist 覆盖所有路径** · critical · 自动 同上 + `tests/api/test_app_factory__security.py`
- 威胁：A1 DNS rebinding。`evil.com` 解析到 127.0.0.1 后，浏览器会把它当同源来读写 API。
- 测试：
  - 路径：`/`、`/assets/x.js`、`/api/health`、`/api/session`、`/api/artifacts/j/x.png`、`/mcp`；
  - 非法 Host：`evil.com:8790`、`127.0.0.1.nip.io:8790`、`localhost.evil.com:8790`、`127.0.0.1:8791`、`127.0.0.1`（无端口）、`[::1]:8790`、空值、两个 Host 头、`127.0.0.1:8790@evil.com`；
  - 合法对照：`127.0.0.1:8790`、`localhost:8790`、`LOCALHOST:8790`。
- 期望：非法一律 403（静态资源与 health 不例外）；合法进入下一闸门。

**SEC-N04 Origin allowlist（有 Origin 即校验）** · critical · 自动 同上
- 威胁：A1 跨站 simple request（form POST 或 `text/plain` fetch 不触发预检），来源包括即梦页 `https://jimeng.jianying.com`、fake site `http://127.0.0.1:9999`。
- 测试：`GUARDED_ROUTES` × 各类 Origin × {无 token, 有效 token}。
  - `GUARDED_ROUTES`：§5.10 全部 POST/PUT，加上 `/mcp` 的 POST/GET/DELETE；
  - Origin 取值：`https://jimeng.jianying.com`、`http://127.0.0.1:9999`、`null`、`http://127.0.0.1:8790.evil.com`、`http://127.0.0.1:8790/`、`https://127.0.0.1:8790`、`HTTP://127.0.0.1:8790`、两个 Origin 头。
- 期望：
  - 全部 403；handler spy 调用计数为 0；DB 与文件无变化；
  - 附加一条：JSON 端点对 `Content-Type: text/plain` 返回 415（纵深防御）。

**SEC-N05 fetch-metadata 跨站拒绝 + GET 无副作用** · critical · 自动 同上
- 威胁：A1 用 `<img>` / `<script>` 跨站嵌入发 GET（这类请求不带 Origin），探测截图是否存在，或触发 GET 上的副作用。
- 测试：
  - `GET /api/artifacts/…`、`/api/session`、`/api/jobs`，分别带 `Sec-Fetch-Site: cross-site` / `same-site`，有 token 与无 token 各一次；
  - 静态扫描路由表。
- 期望：请求一律 403；路由表中所有 GET 路由映射到 `*Query` 方法，没有任何 GET 映射到 `*Command`。

**SEC-N06 Bearer token 解析** · critical · 自动 `tests/libs/infrastructure/middleware/test_bearer_token__middleware.py`
- 威胁：A2 未授权脚本、SSRF 类请求（通常无法自定 header）。
- 测试：不带 fetch-metadata 的请求，`Authorization` 取以下值：
  - 缺失、`Bearer `（值为空）、`Bearer wrong`；
  - 正确 token 少 1 个字符、多 1 个字符；
  - `bearer <正确>`、`Basic <b64>`、`Bearer 令牌`（非 ASCII）；
  - 64 KB 超长值、两个 `Authorization` 头；
  - 另外把正确 token 放在 `?token=`、`?access_token=`、Cookie 里各试一次。
- 期望：
  - 只有 `Bearer <正确>` 通过。方案名大小写是否敏感在测试里写死一种；
  - 非 ASCII、超长值返回 403，不是 500；
  - query / cookie 里的 token 一律无效（避免进入日志和浏览器历史）。

**SEC-N07 常量时间比较** · critical · 自动（静态 + 单测）`tests/api/security/test_static_scan.py`
- 威胁：本机进程可以高频探测，逐字节比较存在时序侧信道。
- 测试：
  - AST 扫描 `apps/`、`libs/`：token 与 HMAC 签名只允许 `hmac.compare_digest(bytes, bytes)` 比较；
  - 名字含 `token|signature|digest|mac` 的变量上禁止 `==`、`!=`、`startswith`、`in`；
  - 单测：长度不等、含非 ASCII 的输入。
- 期望：扫描 0 命中；单测输入不抛 `TypeError`，返回 403。

**SEC-N08 token 未配置时 fail-closed** · critical · 自动 `tests/api/test_app_factory__security.py`（Gap G-3）
- 威胁：FR-1 把 `JIMENG_BRIDGE_TOKEN` 标为「可选」。如果实现成「未设置 = 不校验」，本机任意进程无需鉴权就能花积分。
- 测试：分别以 `.env` 无 token、token 为空串、token 长度 < 32 启动服务。
- 期望：
  - 服务照常启动，UI（G5/G6）可用；
  - 所有 `bearer` 路径（含 `/mcp`）返回 403，启动日志打 warning `token_not_configured`，日志不含任何 token 值；
  - 短 token 按「未配置」处理。

**SEC-N09 同源 UI 豁免不可被非浏览器客户端顺手冒充** · critical · 自动 + 手工（d）
- 威胁：A2 agent 或脚本被 403 后加 `Origin: http://127.0.0.1:8790` 重试。它借此绕过 token，被记为 `ui_human`，进而绕过 `allow_http_auto` 与预算。
- 测试：
  - (a) 只伪造 Origin，不带 `Sec-Fetch-*`，POST `/api/batches/{id}/confirm`；
  - (b) 伪造 Origin + `Bearer <正确>`；
  - (c) 伪造 Origin + 完整 fetch-metadata（`same-origin` / `cors` / `empty`）；
  - (d) 手工：真实 Chrome 打开构建后的 UI，点「确认并开始」。
- 期望：
  - (a) 403；
  - (b) 分类为 `bearer`，受 SEC-C07 约束；
  - (c) 通过，属残余风险，见 §16 R-2；
  - (d) 通过，库中 `confirmer=ui_human`。同时验证真实浏览器对 `http://127.0.0.1:8790` 确实发送 `Sec-Fetch-Site`；
  - 每次确认的审计记录包含 `auth_class`、`sec_fetch_site`、`user_agent`，不含 token。

**SEC-N10 不启用 CORS / Private Network Access** · critical · 自动
- 威胁：A1。只要有一个错误的 CORS 头，跨站页面就能读取会话状态、余额、截图。
- 测试：
  - `OPTIONS /api/batches`，带 `Origin: http://evil.com`、`Access-Control-Request-Method: POST`、`Access-Control-Request-Private-Network: true`；
  - 普通 GET 带任意 Origin；
  - 静态断言 app 没有注册 `CORSMiddleware`。
- 期望：任何响应都不含 `Access-Control-Allow-*`（包括 `-Private-Network`）；预检返回 403 或 405，绝不出现 200 + ACAO。

**SEC-N11 uvicorn 代理头不被信任（§1 表第 3 行）** · critical · 自动 `tests/api/test_main__bind.py`（Gap G-12）
- 测试：
  - pre-mutation 形状：用真实 uvicorn 起服务（不用 TestClient），发合法 Host 与 token，外加 `X-Forwarded-For: 192.168.1.5`、`X-Forwarded-Proto: https`、`X-Forwarded-Host: evil.com`、`Forwarded: for=1.2.3.4;host=evil.com`；
  - post-mutation 形状：直接构造 ASGI scope 调用 middleware；
  - 静态断言 `uvicorn.run(..., proxy_headers=False)`，Makefile 中没有 `--proxy-headers` / `--forwarded-allow-ips`。
- 期望：
  - 两种形状判定结果一致；
  - 应用看到的 `request.client.host` 仍为 `127.0.0.1`，`scheme` 仍为 `http`；
  - 转发头不参与 G0 / G1 / G2 的判定。

**SEC-N12 `/mcp` 挂载前后两形状 + DNS rebinding（CVE-2025-66416）** · critical · 自动 `tests/api/mcp_tools/test_mcp_transport_security.py`
- 测试：
  - pre-mount 形状：通过完整 app 访问 `/mcp`、`/mcp/`、`/MCP`、`/mcp/../mcp`、`//mcp`，分别发 `initialize` 与 `tools/call`，搭配非法 Host、非法 Origin、缺 token 三种情况；
  - post-mount 形状：绕过外层 middleware，直接实例化 MCP 子应用，发非法 Host 与非法 Origin；
  - 静态断言：代码显式传入 `TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=[…:8790], allowed_origins=[…:8790])`，不依赖 SDK 默认值。
- 期望：
  - pre-mount：全部 403（外层闸门）；
  - post-mount：子应用自己拒绝，状态码按 SDK 实测值写死；
  - 鉴权逐请求进行：只带 `Mcp-Session-Id`（如果 SDK 仍签发）、不带 token 的后续请求同样 403；
  - `ui_browser` 分类访问 `/mcp` 返回 403。

**SEC-N13 dev proxy 不存在的守护** · warning · 自动 `tests/api/security/test_static_scan.py`
- 理由：v1 只有一种模式，这是守护性检查，不是现存漏洞。
- 测试：
  - `apps/ui/vite.config.ts` 不含 `server.proxy`；
  - README / Makefile 不宣传 `vite dev` / `npm run dev` 运行模式。
- 期望：0 命中。命中时失败信息写明「新增 dev 模式须同时补 development.md §11 三形状」。

**SEC-N14 guarded 路由 × `serve_static=True` 全量扫描** · critical · 自动 `tests/api/test_app_factory__security.py`
- 依据：`development.md` §1。静态挂载 `/`（`html=True`）会吞掉被遮蔽的路由，返回 405。
- 测试：
  - `GUARDED_ROUTES` 从 app 路由表**自动收集**（全部非 GET 路由 + `/mcp`），禁止手写清单；
  - 与 `serve_static=True`、{无鉴权, 非法 Origin, 合法 bearer, 合法 UI 形状} 组合。
- 期望：无鉴权与非法组合返回 403（不是 405 / 404）；合法组合不返回 405。

---

## 4. 积分花费授权（按安全级处理）

**SEC-C01 确认 token 伪造 / 篡改** · critical · 自动 `tests/libs/domain/value_objects/test_confirmation_token__valueobject.py`
- 测试：
  - 在合法 token 上分别改动 `batch_id`、内容摘要、合计预计积分、`exp`、签名中的任一字节；
  - 用另一把 HMAC key 签名；
  - 空串、非 base64、截断、8 KB 超长、附加字段、签名段置空（`alg=none` 类）。
- 期望：一律 `token_invalid`；batch 仍为 `awaiting_confirm`；无 job 入队；无 500。

**SEC-C02 单次有效（并发 + 重启）** · critical · 自动 `tests/libs/application/commands/test_batch__command__confirm_security.py`
- 测试：
  - 同一 token 顺序确认两次；
  - `asyncio.gather` 并发发起 20 次确认；
  - 确认成功后重启服务（新容器、同一个 DB），再用同一 token 确认。
- 期望：
  - 恰好 1 次成功。`awaiting_confirm → confirmed` 用 DB 条件更新保证原子性；
  - 其余返回 409 `token_already_used`；
  - job 只入队一份；重启后仍然拒绝。

**SEC-C03 跨 batch 复用** · critical · 自动 同上
- 测试：把 batch A 的 token 用在 batch B 上，B 分别取内容相同、内容不同两种。
- 期望：拒绝；B 保持 `awaiting_confirm`。

**SEC-C04 过期** · critical · 自动（注入 Clock）
- 测试：
  - 分别在到期前 1 s、恰好 30 min、到期后 1 s 确认；
  - 系统时钟回拨 1 h 后，再用已过期的 token。
- 期望：
  - 到期即拒（恰好 30 min 也算过期）；
  - 服务端同时比较 token 签入的 `exp` 与 batch 入库的 `expires_at`，时钟回拨不能让 token 复活。

**SEC-C05 内容冻结与 TOCTOU** · critical · 自动 同上 + fake site e2e（Gap G-5）
- 威胁：precheck 与提交之间盘上内容被改，service 替用户花积分生成了他没看过的内容。
- 测试：
  - (a) precheck 后把 shot md 的 prompt 改一个字，再 confirm；
  - (b) confirm 后、upload 前，替换一张参考图的字节；
  - (c) confirm 后改 `jimeng_config.toml` 的 `references.overrides` 或 `video.model`；
  - (d) 把参考文件替换成指向沙箱外的 junction。
- 期望：
  - (a) confirm 返回 `digest_mismatch`；
  - (b) upload 前重算 sha256，与确认时不一致 → job 失败（`reference_changed`）或暂停，fake site「生成」点击计数为 0；
  - (c) 执行只使用确认时持久化的冻结 `GenerationRequest`，不重新解析 config；
  - (d) 沙箱拒绝。

**SEC-C06 页面预计积分超出已确认估算** · critical · 自动 fake site（待 spec 定案，Gap G-6）
- 测试：fake site 让页面预计积分 = 静态估算 × 3。
- 期望：偏差超过 `estimate_deviation_warn_pct` 的 job 不提交，转入需人工处理（或该 batch 重新确认）；点击计数为 0。

**SEC-C07 `allow_http_auto=false` 时 HTTP 客户端无法自行确认** · critical · 自动 `tests/api/routes/test_batch__route__security.py`
- 威胁：precheck 响应会把 `confirmation_token` 返回给调用方。bearer 脚本拿到后直接 `POST /confirm`，就等于自动确认；如果开关只检查 `auto_confirm=true` 字段，这条路就被绕过了。
- 测试：`allow_http_auto=false` 下，由 bearer 客户端发起：
  - (a) `POST /api/batches` 带 `auto_confirm=true`；
  - (b) 用 precheck 返回的 token 调 `POST /api/batches/{id}/confirm`；
  - (c) 请求体自报 `confirmer: "ui_human"`；
  - (d) `POST /api/jobs/{id}/steps/submit`。
- 期望：
  - (a)(b)(d) 返回 403 `auto_confirm_disabled` 或 409 `batch_not_confirmed`，batch 状态不变；
  - (c) 返回 422，或忽略该字段且库中记录为 `http_auto`（二选一写死）。

**SEC-C08 每日预算：拆批 / 并发 / 日界** · critical · 自动（注入 Clock + 时区，Gap G-7）
- 测试：`allow_http_auto=true`、`budget=2000`：
  - (a) 单批 2001；
  - (b) 1500 + 600 两批；
  - (c) 10 个 300 的批并发确认；
  - (d) 23:59:59 确认 1900，00:00:00 再确认 1900；
  - (e) 运行中把系统时区从 UTC+8 改为 UTC−8；
  - (f) 取消一个已确认的 batch；
  - (g) bearer 客户端先调高 budget（SEC-K03）。
- 期望：
  - (a)(b) 整批拒绝，不部分放行；
  - (c) 累计通过额 ≤ 2000（锁或事务内累加）；
  - (d) 按 G-7 定的时区换日，两批都通过；
  - (e) 不重置当日累计；
  - (f) 默认不回补额度；
  - (g) 403；
  - 计入额的口径（确认时的预计积分）在测试中写死。

**SEC-C09 MCP 不能传 auto_confirm、不能自报确认人** · critical · 自动 `tests/api/mcp_tools/test_batch__tool__security.py`
- 测试：
  - `tools/list` 读取 `precheck_batch` / `confirm_batch` 的 input schema；
  - 调用时附加 `auto_confirm: true`、`confirmer: "ui_human"`、`allow_http_auto: true`。
- 期望：
  - schema 中没有这些字段，且 `additionalProperties: false`；
  - 带这些附加字段调用返回 `isError`，batch 不变；
  - `confirm_batch` 成功时库中记录 `confirmer=mcp`。

**SEC-C10 MCP 确认的服务端上限** · critical · 自动（待 spec 定案，Gap G-2）
- 威胁：FR-15 对 `confirm_batch` 的人工批准完全依赖 Claude Code 客户端的权限询问。一旦把它加入 allow 列表、或运行在 bypass permissions 模式，就能 precheck→confirm 无限花积分，服务端零约束。
- 测试（按 G-2 定案）：`confirmer=mcp` 的确认计入每日预算（或独立的 MCP 预算），然后超额确认。
- 期望：超额返回 `isError`，附「在 UI 确认页确认：{url}」；UI 确认不受此限制。

**SEC-C11 未确认 job 从任何入口都进不了 `submitting`（FR-16）** · critical · 自动（domain 单测 + fake site e2e）
- 测试：
  - 对 `awaiting_confirm` batch 的 job，从 HTTP `steps/submit`、MCP `browser_step(op=submit)`、`resume_job`、`resume_queue`、调度器 tick、重启恢复逐一尝试；
  - 对 `cancelled` / `failed` 的 job 执行 submit；
  - 伪造 `job_id`。
- 期望：
  - 实体方法抛领域错误，HTTP 返回 409，MCP 返回 `isError`；
  - fake site「生成」点击计数恒为 0；无 `→ submitting` 转移记录。

**SEC-C12 `reroll` / 幂等不能绕过确认** · critical · 自动
- 测试：
  - 已 `done` 的请求带 `reroll: true` 重新 precheck；
  - 同一 `idempotency_key` 配不同内容；
  - 首批仍在 `awaiting_confirm` 时，同 key 同内容再 precheck，然后直接 submit。
- 期望：
  - reroll 生成新 batch，需要单独确认，并计入预算；
  - 同 key 不同内容返回 409；
  - 幂等返回原 batch，其确认状态不变；submit 被拒。

**SEC-C13 `resume` 不引发重提** · critical · 自动 fake site
- 测试：分别对 `paused_needs_human(restart_during_submit)` 与 `insufficient_credit` 的 job 执行 resume。
- 期望：只做历史对账或恢复轮询，点击计数不增加（与 SEC-T05 同源）。

**SEC-C14 确认页展示 = 签名内容** · critical · 自动 `tests/ui/` + 手工
- 测试：
  - 自动：确认页 DOM 显示的合计积分、`GET /api/batches/{id}` 返回的合计、token 签入值，三者比对；
  - 手工：拿一个 3 条的 batch，核对缩略图、参数、单条积分。
- 期望：三者一致；手工核对无出入。

---

## 5. 文件系统沙箱

**SEC-F01 统一沙箱解析器（表驱动）** · critical · 自动 `tests/libs/common/test_paths__sandbox.py`

读根为 `ai_videos/`；写根为 `ai_videos/` 下的目标目录与 `projects/jimeng_web_bridge/.data/`。每个输入分别用 `/`、`\`、混合分隔符喂入：

- **相对逃逸**：`..`、`../../projects/x`、`a/../../x`、`a\..\..\x`、`.\..\`
- **编码**：`..%2f`、`..%5c`、`%2e%2e%2f`、`%252e%252e%252f`（双重编码）、`..%c0%af`、`%00`
- **绝对路径**：`C:\Windows\win.ini`、`C:/Windows`、`\Windows`（当前盘根）、`C:foo`（盘符相对）、`/etc/passwd`
- **UNC 与设备路径**：`\\server\share\a.png`、`//server/share`、`\\?\C:\x`、`\\?\UNC\server\share`、`\\.\pipe\x`、`\\.\PhysicalDrive0`、`\??\C:\x`
- **保留名**（出现在任一路径段）：`CON`、`nul.png`、`COM1.txt`、`LPT9`、`AUX.md`、`CONIN$`
- **NTFS ADS**：`shot02.md:evil`、`a.png::$DATA`、`renders:$I30:$INDEX_ALLOCATION`
- **尾随点 / 空格**：`shot02.md.`、`shot02.md `、`renders.\x`、`hy3 \x`
- **前缀兄弟目录**（专抓字符串 `startswith` 漏洞）：`ai_videos_backup/x`、`ai_videos2/x`
- **大小写与短名**：`AI_VIDEOS/x`（应接受）、`AI_VID~1/x`（按解析后真实路径判断）
- **控制字符与超长**：`\n`、`\t`、超过 260 字符的路径

期望：
- 逃逸、UNC、设备路径、ADS、保留名、尾随点空格全部抛 `SandboxViolation`（HTTP 400/403，MCP `isError`；错误信息只含仓库相对路径）；
- 判定方式：先 `resolve()`，再与沙箱根做**逐路径段、大小写不敏感**的比较，不用字符串前缀；
- 合法的中文路径（`characters/c1_砌炉的老人`）能通过。

**SEC-F02 symlink / junction / hardlink** · critical · 自动（symlink 用例 `skipif` 无权限；junction 与 hardlink 不需要管理员，必须真跑）
- 测试：在 tmp `ai_videos/` 中分别建立：
  - 指向沙箱外目录的 junction；
  - 指向 `.env` 的 symlink；
  - 指向 `.data/chrome_profile` 的 junction。

  再让它们分别充当参考图目录、`renders/`、`_candidates/`、`_deleted/`、剧目录本身。
- 期望：
  - 路径中任一段是 reparse point，读写都拒绝（不只检查最后一段）；
  - 产物绝不会落到沙箱外；
  - hardlink 无法靠路径识别，记入 §16 R-5，但相关流程不能崩溃。

**SEC-F03 `{drama}` URL 参数** · critical · 自动 `tests/api/routes/test_drama_config__route__security.py`
- 测试：`GET/PUT /api/dramas/{drama}/config` 与 `POST …/propose`，`{drama}` 取：
  - `..%2F..%2Fprojects`、`huangye_shenghuo%2F..%2F..`、`%2e%2e`；
  - `_deleted`、`huangye_shenghuo%2F_series`；
  - `C%3A%5CWindows`、`%5C%5Cserver%5Cshare`、`hy3%00`；
  - 4 段深路径、系列目录本身 `huangye_shenghuo`、不存在的剧。
- 期望：
  - 不是剧根：404 `drama_not_found`（只走 `libs/common/drama_ref.py` 的 `series.json` 规则）；
  - 逃逸：403；
  - PUT 的实际写入路径只能是 `ai_videos/{drama_root}/jimeng_config.toml`（断言 basename 与父目录）。

**SEC-F04 原始入口 `output_dir` 与参考路径（FR-7）** · critical · 自动 `tests/libs/application/commands/test_batch__command__sandbox.py`
- 测试：
  - 把 F01 的输入集分别当作 `output_dir` 与参考路径；
  - 参考路径指向 `ai_videos/` 内的 `jimeng_config.toml`、`*.jimeng.json`、指向 `.env` 的 junction；
  - `output_dir` 取 `ai_videos/_deleted/`、剧根本身、`.data/`。
- 期望：
  - 逃逸：预检 error，不进 batch；
  - 参考文件只接受媒体扩展名（image / video / audio）；
  - `output_dir` 不能落在 `search_exclude` 保留目录内，`.data/` 也不是合法产物目录。

**SEC-F05 `.link.json` 目标（FR-10）** · critical · 自动 `tests/libs/infrastructure/readers/test_drama_tree__reader__link_json.py`
- 测试：`target` 取 F01 输入集，另加：
  - 指向另一个 `.link.json`、自指、互指循环；
  - 指向 junction、目录、`.env`、`projects/`；
  - 畸形内容：JSON 非对象、`target` 非字符串、超长值、带额外字段。
- 期望：
  - 逃逸或 reparse point：拒绝，并给出可操作的提示；
  - 链只解析一跳，循环不会挂死；
  - 畸形 JSON：预检 error，不产生 500。

**SEC-F06 `/api/artifacts/{job_id}/{name}` 与 MCP `get_screenshot`** · critical · 自动 `tests/api/routes/test_artifact__route.py`、`tests/api/mcp_tools/test_artifact__tool.py`
- 测试：
  - `name` 取 `..%2F..%2Fbridge.db`、`..%5Cchrome_profile%5CDefault%5CCookies`、`..%2Flogs%2Fa.jsonl`、`trace.zip`、`dom.html`、盘上存在但未登记的文件名、另一个 job 的截图名；
  - `job_id` 取非法格式与 SQL 片段。
- 期望：
  - 只按 DB 中**该 job 登记的** artifact 名查找，从不把 `name` 拼成路径；
  - 未登记：404；
  - 解析结果必须位于 `.data/artifacts/{job_id}/` 内；
  - 响应类型受 SEC-S06 约束。

**SEC-F07 promote / archive（FR-43）** · critical · 自动 `tests/libs/application/commands/test_candidate__command__sandbox.py`
- 测试：
  - candidate 取：其他主体 `_candidates` 下的文件、`_candidates/../c1-1.png`、沙箱外绝对路径、junction 下的文件；
  - `key` 含 `/`、`\`、`..`、`:`、保留名，或不符合 4b-A 路由键形态；
  - 源文件为 junction 时计算 archive 目标；
  - 目标 `{key}.png` 已存在且为只读文件，或已存在同名目录。
- 期望：
  - candidate 必须位于 `{subject_dir}/_candidates/{key}/` 内，且 key 与块路由键一致；
  - archive 目标解析后仍在 `ai_videos/_deleted/` 内；
  - 任何失败都不留半移动状态（先复制、再归档、最后落位；出错可恢复）。

**SEC-F08 上传前临时改名（FR-30）** · critical · 自动 `tests/libs/infrastructure/clients/test_jimeng_browser__client__upload_name.py`
- 威胁：`{name}{ext}` 里的 `name` 来自 shot md 的 `参考:` 行，是人或 Claude 写的自由文本。
- 测试：`name` 取 `../../x`、`a\b`、`CON`、`x:stream`、`x.`、`x `、含 `\n * ? " < |` 的字符串、250 个中文字符、空串。
- 期望：
  - 预检阶段即报 error，并提示应填的 config 键；
  - 即使绕过预检，临时文件解析后也必须在本 job 独占的临时子目录内，结束后清理。

**SEC-F09 下载 / CLI 输出文件名不由平台决定** · critical · 自动
- 测试：
  - fake site 下载的 `suggested_filename = "..\\..\\evil.mp4"`；
  - fake dreamina 在 `--download_dir` 中写入 `../escape.png`、symlink、500 个文件、非图片文件。
- 期望：
  - 只从本次独占的临时目录挑选文件；最终文件名完全由 FR-42/43 模板生成；
  - 逃逸出去的文件不会被移动；
  - 类型或数量异常时 job 失败。

**SEC-F10 config 中的路径模板写不出沙箱** · critical · 自动 `tests/libs/domain/value_objects/test_drama_config__valueobject__paths.py`
- 测试：
  - `outputs.video_name` 取 `../../{shot}.mp4`、`C:\x\{shot}.mp4`、`{shot}/../../x.mp4`、`CON.mp4`；
  - `outputs.image_candidates_dir` 与 `entities.source_images` glob 取 `{card_dir}/../../**/*.png`、`**/../..`；
  - `references.overrides` 的值取沙箱外路径、`ENTITY:` 大小写混淆；
  - `references.search_exclude` 删成空列表。
- 期望：
  - schema 返回 422 并指出字段路径；
  - 运行期渲染出的路径再过一次 F01；
  - `_deleted`、`_candidates`、`renders` 永不参与参考解析（硬编码底线，config 只能在此基础上追加）。

**SEC-F11 静态文件服务不外泄** · critical · 自动
- 测试：
  - 请求 `/..%2F.data%2Fbridge.db`、`/assets/..%2F..%2F..%2Fconfig%2Fglobal.toml`、`/%5C..%5C.env`、`/.env`、`/.data/chrome_profile/Default/Cookies`；
  - 在 static 目录内放一个指向沙箱外的 junction。
- 期望：
  - 一律 404；
  - StaticFiles 根固定为 `apps/api/static/`，`follow_symlink=False`；
  - SPA fallback 只返回 `index.html`。

**SEC-F12 参考图缩略图端点（若新增）** · critical · 自动（Gap G-10）
- 测试：确认页取缩略图用的端点，使用 F01 输入集 + 非图片文件（`.toml`、`.md`、`.env`）。
- 期望：只读 `ai_videos/` 下的图片 / 视频类型；其余一律 404 或 403；响应头同 SEC-S06。

---

## 6. 子进程（dreamina CLI）

本机实测：`~/bin/dreamina.exe` 是 PE32+ 原生可执行文件（Go / cobra 风格 flag）。`text2image` 只有 `--prompt string` 参数，**没有从文件读取 prompt 的途径**，因此 argv 是唯一通道。

**SEC-P01 argv 列表、不经 shell** · critical · 自动（静态 + 单测）`tests/libs/infrastructure/clients/test_dreamina_cli__client__argv.py`
- 测试：
  - 静态扫描 `apps/`、`libs/`，禁止 `shell=True`、`os.system`、`os.popen`、以字符串形式传给 `subprocess`、`asyncio.create_subprocess_shell`、`cmd /c`、`powershell -Command`；
  - 单测断言 client 调用的是 `create_subprocess_exec(path, *args)`。
- 期望：0 命中。

**SEC-P02 prompt 逐字节到达** · critical · 自动
- 测试：fake dreamina（`.exe` 启动器）接收下列 prompt：
  - 引号与反斜杠：`"`、`\"`、`\\"`、尾随 `a\`；
  - 换行：`\n`、`\r\n`；
  - shell 元字符：`& calc &`、`| whoami`、`; del x`、`%PATH%`、`!VAR!`、`^`、`$(id)`、`` `id` ``；
  - 像 flag 的值：`--download_dir=C:\Windows`、以 `-` 开头的文本；
  - 中文 + emoji、5000 字长文本。
- 期望：
  - fake 记录的 prompt 值与输入逐字节相等；
  - 注入 sentinel 文件不存在（说明没有命令被执行）；
  - 参数一律以 `--flag=value` 单元素形式传递（与 CLI 自带示例一致），以 `-` 开头的 prompt 不会被解析成别的 flag；
  - 含 NUL 的 prompt 在预检阶段即被拒。

**SEC-P03 `cli.path` 可执行体约束** · critical · 自动（Gap G-14）
- 威胁：Windows 上 `.bat` / `.cmd` 会经 cmd.exe 二次解析参数（BatBadBut 类问题），列表传参也挡不住 `& | %` 注入。
- 测试：`cli.path` / `DREAMINA_CLI_PATH` 分别取 `.cmd`、`.bat`、`.ps1`、`cmd.exe`、`powershell.exe`、`python.exe`、不存在的路径、目录、UNC 路径。
- 期望：
  - 启动时（FR-41 版本检查）拒绝，返回 `cli_path_unsafe`；
  - CLI 队列不可用，web 队列不受影响；
  - `dreamina version` 输出格式不符时同样拒绝。

**SEC-P04 执行路径类键不能经 API 修改** · critical · 自动 `tests/libs/application/commands/test_global_config__command__security.py`
- 判级理由：一个可以经 bearer 或 UI 修改的「可执行文件路径」，就是一个本机代码执行原语。它还会和 C07 / C08 叠加，变成积分护栏的旁路。
- 测试：通过 `PUT /api/config/global` 修改 `cli.path`、`cli.min_version`、`browser.profile_dir`、`browser.channel`、`server.host`、`server.port`，bearer 与 UI 两种分类各测一遍。
- 期望：
  - 返回 422 `field_not_writable_via_api`；UI 上这些字段只读展示，并提示「编辑 global.toml / .env 后重启」；
  - 文件不变；
  - 被拒的尝试写入审计日志（不含 token）。

**SEC-P05 子进程环境不带机密** · critical · 自动
- 测试：fake dreamina dump 自己收到的 `os.environ`。
- 期望：不含 `JIMENG_BRIDGE_TOKEN`，也不含 `.env` 加载的其他机密键；`PATH`、`USERPROFILE` 保留。

**SEC-P06 子进程超时与输出上限** · warning · 自动
- 理由：影响只限于本机可用性。
- 测试：fake dreamina 分别挂起不退出、输出 200 MB stdout、输出非 JSON。
- 期望：
  - 超时后终止整个进程树，映射为可暂停的原因；
  - stdout 读取有上限；
  - 非 JSON 输出记为 CLI 错误，不产生 500。

---

## 7. config 注入

**SEC-K01 schema 校验 + 纯 TOML，无代码执行** · critical · 自动 `tests/libs/infrastructure/writers/test_drama_config__writer__schema.py`
- 测试：
  - 未知键；类型错误；
  - 枚举外值：`negative_prompt = "merge"`、`image_on_existing = "overwrite"`、`routing.video = "api"`；
  - TOML 语法错误、重复键；
  - 原文视图里写入 `!!python/object`、`${ENV}`、`{{ }}`。
- 期望：
  - 返回 422 并指出字段路径；文件字节不变；
  - 解析只用 tomlkit / tomllib，全程无 eval、YAML、模板引擎；
  - `${ENV}` 按字面字符串保存，不被展开。

**SEC-K02 名称模板占位符白名单** · critical · 自动
- 威胁：`str.format` 支持 `{x.__class__}`、`{x[0]}` 这类属性与下标访问。
- 测试：`entities.name_template`、`outputs.video_name` 取 `{abbrev.__class__}`、`{abbrev[0]}`、`{0}`、`{abbrev!r}`、`{abbrev:>999999}`、`{unknown}`。
- 期望：
  - 只允许 FR-2 列出的具名占位符（`{abbrev}` `{character_name}` `{shot}` `{ts}` `{_i}` `{key}` `{card_dir}`）；
  - 其余 422；
  - 模板替换走白名单实现，不走 `str.format`。

**SEC-K03 护栏键只允许人工 UI 修改** · critical · 自动（Gap G-4）
- 威胁：bearer 客户端先把 `confirm.allow_http_auto` 改为 true、`budget.*` 改为 999999、`pacing.min_submit_interval_s` 改为 0、`concurrency.max_remote_rendering` 改为 50，然后自动确认。一次 PUT 就能拆掉花费护栏和 ToS 护栏。
- 测试：分别以 bearer 分类和 UI 分类修改 `confirm.*`、`budget.*`、`pacing.*`、`concurrency.*`。
- 期望：
  - bearer：403 `sensitive_key_requires_ui`；
  - UI：允许，但须经二次确认（FR-55），并写审计 `{key, before, after, auth_class, at}`；
  - schema 设上下限，越界返回 422：`min_submit_interval_s ≥ 15`（或 spec 定的下限）、`1 ≤ max_remote_rendering ≤ 3`、`budget ≥ 0`。

**SEC-K04 机密不可经 `/api/config/global` 读写** · critical · 自动
- 测试：
  - `.env` 中配置了 token 与 profile 覆盖时，调 `GET /api/config/global`；
  - `PUT` 带 `token`、`secrets`、`env`、`JIMENG_BRIDGE_TOKEN` 等键。
- 期望：
  - GET 不返回 token 值，只返回 `token_configured: bool`；被 env 覆盖的键只标 `overridden_by_env: true`；
  - PUT 返回 422；
  - 服务从不写 `.env`。

**SEC-K05 请求体与结构上限** · warning · 自动（Gap G-8）
- 理由：localhost 上的资源耗尽，影响只限于本机。
- 测试：
  - config PUT 1 MB；
  - `references.rules` 10 000 条；
  - 数组嵌套 1000 层；
  - 10 000 字符、含 500 个 `*` 的 `label_glob`；
  - 非法 UTF-8。
- 期望：
  - body 超过 256 KiB：413；
  - rules > 200、单个 glob > 256 字符：422；
  - 单次预检的 glob 匹配耗时 ≤ 5 s；
  - 非法 UTF-8：400。

**SEC-K06 每剧 config 不能携带全局护栏** · critical · 自动
- 威胁：`jimeng_config.toml` 放在 `ai_videos/` 下，会被 Claude 顺手编辑，是最容易被写进越权设置的文件。
- 测试：在每剧 config 中写入 `[confirm] allow_http_auto = true`、`[budget]`、`[pacing]`、`[concurrency]`、`[cli] path = …`、`[server]`。
- 期望：
  - 每剧 schema 不含这些段：保存时 422，读取时报预检 error；
  - 全局护栏只来自 `global.toml`。

---

## 8. 机密与隐私

**SEC-S01 token 哨兵全链路扫描** · critical · 自动 `tests/api/security/test_secret_canary.py`
- 测试：
  - 设置 `JIMENG_BRIDGE_TOKEN=SENTINEL-<48 位随机>`，错误 token 用另一个哨兵 `WRONG-SENTINEL-…`；
  - 跑完离线 e2e：成功路径、每种暂停与失败注入、401/403 路径、全部 MCP 工具，并注入一次 handler 未处理异常；
  - 然后扫描：`.data/logs/**`、`bridge.db`（`iterdump`）、`.data/artifacts/**`（trace zip 解压后的文本）、tmp 仓库中所有新增的 `*.jimeng.json` / `jimeng_config.toml`、全部 HTTP 响应头与响应体、MCP 的 `structuredContent` 与文本、uvicorn 访问日志、stderr、toast 调用参数。
- 期望：
  - 两个哨兵出现次数均为 0；
  - `Authorization` 头不出现在任何日志字段；
  - config / settings 对象的 `repr()` 不含 token。

**SEC-S02 sidecar 字段白名单与隐私（FR-44）** · critical · 自动 `tests/libs/infrastructure/writers/test_output__writer__sidecar_privacy.py`
- 威胁：sidecar 进 git，任何账号标识一旦写入就永久留在历史里。
- 测试：用 fake site 返回的历史响应走完下载与 sidecar 写入。响应里带有 `uid`、`sec_uid`、`sessionid`、`msToken`、`a_bogus`、昵称、头像 URL，以及带 `x-signature` / `x-expires` 的结果 URL。
- 期望：
  - sidecar 的键集合严格等于 FR-44 所列（多一个键即失败）；
  - 值中不出现上述任何字段值，不出现签名 URL，不出现 `C:\Users\` 这类绝对路径（`references[].path` 必须是仓库相对的 POSIX 路径）；
  - `platform_task_id` 允许出现。

**SEC-S03 截图 / DOM / trace 只落 `.data/`** · critical · 自动
- 威胁：`ai_videos/` 下的图片与视频会被 pre-commit 钩子自动上传 R2 并写入 `assets.json`（CLAUDE.md），截图落进剧目录就等于外泄到云端。
- 测试：e2e 前后，对 tmp 仓库副本执行 `git status --porcelain --ignored ai_videos/`，取差集。
- 期望：
  - `ai_videos/` 下的新增文件只可能是：`renders/*.mp4`、`_candidates/**/*.png`、`{key}.png`、`*.jimeng.json`、`jimeng_config.toml`、`_deleted/**`；
  - 截图、预演图、DOM 快照、trace 全部在 `.data/artifacts/` 下。

**SEC-S04 `.gitignore` 覆盖** · critical · 自动 `tests/api/security/test_gitignore_coverage.py`
- 测试：对仓库执行 `git check-ignore -v`。
  - **应忽略**：`projects/jimeng_web_bridge/.data/bridge.db`、`bridge.db-wal`、`.data/chrome_profile/Default/Cookies`、`.data/artifacts/j/x.png`、`.data/logs/a.jsonl`、`.data/tmp/x`、仓库根 `.env`、`apps/api/static/index.html`、`apps/ui/node_modules/x`；
  - **不应忽略**：`config/global.toml`、`ai_videos/**/jimeng_config.toml`、`**/*.jimeng.json`；
  - 另查 `git ls-files projects/jimeng_web_bridge/.data` 结果为空。
- 期望：全部符合。注意：根 `.gitignore` 目前**没有** `.data` 规则，完全依赖项目级 `.gitignore`，本测试必须证明项目级规则真实生效。

**SEC-S05 profile 目录位置守护** · critical · 自动
- 测试：`browser.profile_dir` / `JIMENG_BRIDGE_PROFILE_DIR` 取：仓库内未被忽略的路径、`%LOCALAPPDATA%\Google\Chrome\User Data`（日常 profile）、UNC 路径、仓库根。
- 期望：
  - 启动拒绝，返回 `profile_dir_unsafe`；
  - 合法位置只有：项目 `.data/chrome_profile`，或仓库外的用户目录；
  - profile 目录永远不在任何 HTTP 可服务的根之下。

**SEC-S06 artifact 只按图片类型服务** · critical · 自动（Gap G-11）
- 威胁：
  - DOM 快照若以 `text/html` 从本服务源返回，即梦页面脚本会在 `127.0.0.1:8790` 源内执行，从而按 UI 身份调用 API；
  - trace zip 里带 cookie 请求头。
- 测试：
  - 请求 DB 中登记的 `dom.html`、`trace.zip`、`.json`；
  - 把某张截图的内容换成 HTML 文本（测类型嗅探）。
- 期望：
  - 只服务 `.png`、`.jpg`、`.jpeg`、`.webp`；
  - 响应头为对应图片 `Content-Type` + `X-Content-Type-Options: nosniff` + `Content-Security-Policy: default-src 'none'` + `Cross-Origin-Resource-Policy: same-origin`；
  - 其他类型 404。DOM 快照与 trace 只供本机手工打开。

**SEC-S07 错误与 MCP 输出卫生** · critical · 自动
- 测试：各 HTTP 路由与 MCP 工具的业务错误、参数错误、内部异常。
- 期望：
  - 响应中不含 traceback、token、cookie、本机绝对路径（统一用仓库相对路径）；
  - `get_screenshot` 只返回相对路径 + 长边 ≤ 768 px 的缩略图。

**SEC-S08 日志注入与内容边界** · warning · 自动
- 理由：影响的是审计完整性，不直接泄密。
- 测试：prompt、参考名、页面弹窗文本中含 `\n{"level":"error"}`、ANSI 转义、10 万字符。
- 期望：
  - JSONL 每行仍是一个合法对象，行数不能被伪造；
  - 超长字段被截断；
  - 页面响应体不整段写入日志，只记录解析结果与计数。

**SEC-S09 README / `.mcp.json` 无明文 token** · critical · 自动
- 测试：扫描项目 README、仓库 `.mcp.json`、`config/`。
- 期望：
  - `Authorization` 的值只能是 `Bearer ${JIMENG_BRIDGE_TOKEN}`；
  - 高熵串检测（≥ 32 位 base64 / hex）0 命中。

---

## 9. 浏览器会话

**SEC-B01 service 不向页面输入凭据（FR-26）** · critical · 自动 fake site + 静态
- 测试：
  - fake site 登录页含手机号、密码、验证码输入框；service 检测到未登录后（fake clock）等待 60 s；
  - 静态检查 PageMap 与 config schema，不存在登录表单 selector，也不存在 `password`、`phone`、`sms_code` 键。
- 期望：
  - 这些字段上的 input / keydown 事件为 0；
  - 状态为 `login_required`，窗口置前，弹 toast。

**SEC-B02 页面 JS 无法触达 service** · critical · 自动（静态 + fake site）`tests/api/security/test_static_scan.py`
- 测试：
  - 静态禁用 `expose_binding`、`expose_function`、`add_init_script`；
  - `page.evaluate` 的参数中不得出现服务 URL、端口、`/api/`、`/mcp`、token；
  - fake site 页面脚本在被驱动期间尝试 `fetch("http://127.0.0.1:8790/api/session")`、`POST /api/batches/{id}/confirm`、`navigator.sendBeacon`、表单 POST。
- 期望：扫描 0 命中；页面发出的请求全部 403（其 Origin 是 fake site 源）；服务端状态不变。

**SEC-B03 响应监听只读** · critical · 自动 静态
- 测试：扫描 `apps/`、`libs/`（不含 `tests/` 与 fixtures）。
  - 禁用：`page.route`、`context.route`、`route_from_har`、`route.fulfill`、`route.continue_`、`route.abort`、`set_extra_http_headers`、`add_cookies`、`clear_cookies`、写出 `storage_state(path=…)`、`context.request` / `page.request`（APIRequestContext 会带着浏览器 cookie 主动发请求）、`new_cdp_session`；
  - 允许：`page.on("response")`、`context.on("response")`、`response.json()` / `response.body()`。
- 期望：0 命中。

**SEC-B04 不主动调用即梦内部接口** · critical · 自动（静态 + fake site）
- 测试：
  - 静态：`/mweb/v1/`、`/commerce/v1/`、`dreamina_subject`、`msToken`、`a_bogus`、`X-Bogus` 只允许出现在 `jimeng_response__reader.py` 的响应 URL 匹配器里；
  - 静态：`httpx`、`requests`、`aiohttp`、`urllib` 的目标主机不得为 `*.jianying.com`、`*.capcut*`、`*.bytedance*`；
  - fake site 记录所有入站请求，逐条断言都由页面自身 UI 行为发出（带页面脚本打的标记）。
- 期望：
  - 0 违规；
  - 若 FR-35 最终采用「结果 URL」下载方案，只允许对媒体 CDN 发**不带 cookie** 的 GET，并在测试中显式列入白名单。

**SEC-B05 不开放 CDP 远程调试端口** · critical · 自动（boot smoke）
- 威胁：`--remote-debugging-port` 让任意本机进程，以及 DNS rebinding 到 CDP 的网页，直接接管已登录会话并读取 cookie。
- 测试：
  - 检查启动参数 `args` 与 `ignore_default_args`；
  - boot smoke 后枚举 chrome 子进程的 TCP 监听。
- 期望：
  - 不出现 `--remote-debugging-port` / `--remote-debugging-address`；
  - chrome 进程没有 TCP 监听（Playwright 默认走 pipe）。

**SEC-B06 单 context、单 profile** · critical · 自动
- 测试：并发触发 canary、`browser_lost` 重建、resume。
- 期望：
  - 任一时刻活跃的 `launch_persistent_context` ≤ 1，重建前旧 context 已关闭；
  - config 里不存在多账号 / 多 profile 的键。

---

## 10. 账号风险 / ToS 护栏（可验证部分）

**SEC-T01 反检测 / 验证码求解依赖黑名单** · critical · 自动 `tests/api/security/test_dependency_denylist.py`
- 扫描对象：`requirements.txt`、`pyproject.toml`、`.venv` 的 `pip freeze`、`apps/ui/package.json` 与 `package-lock.json`（含传递依赖）。包名规范化匹配，大小写与 `-` / `_` 不敏感。
- 黑名单：
  - **Python**：`playwright-stealth`、`undetected-playwright`、`patchright`、`rebrowser-playwright`、`camoufox`、`botasaurus`、`undetected-chromedriver`、`selenium-stealth`、`nodriver`、`zendriver`、`browserforge`、`curl_cffi`、`tls-client`、`2captcha-python`、`anticaptchaofficial`、`capsolver`、`python-anticaptcha`、`ddddocr`；
  - **npm**：`puppeteer-extra*`、`playwright-extra`、`@extra/*`、`fingerprint-injector`、`fingerprint-generator`、`ghost-cursor`。
- 期望：0 命中。黑名单放 `tests/fixtures/security/denylist.txt`，可以追加。

**SEC-T02 反检测代码特征** · critical · 自动 静态
- 测试：扫描非测试代码中的：
  - `navigator.webdriver`、`AutomationControlled`、`--disable-blink-features`；
  - `ignore_default_args` 中出现 `--enable-automation`；
  - `Object.defineProperty(navigator`、覆盖 `user_agent=`、改写 WebGL / canvas；
  - click / pacing 路径上的 `random.*` 延时或鼠标轨迹；
  - 坐标点击 `mouse.click(` / `mouse.move(`（FR-28 禁止）。
- 期望：0 命中。提交间隔是固定值、不做随机化，这是 FR-1 的规定。

**SEC-T03 最小提交间隔由服务端强制** · critical · 自动 `tests/libs/application/commands/test_job__command__pacing.py`（随调度器实际落点调整）
- 测试（注入 fake clock）：
  - 10 个已确认 job 同时可提交；
  - 上次提交 1 s 后，从 HTTP `steps/submit` 与 MCP `browser_step(submit)` 强行提交；
  - 刚提交完就重启服务，立即再提交。
- 期望：
  - fake site 记录的任意相邻两次「生成」点击间隔 ≥ `pacing.min_submit_interval_s`；
  - 手动 submit 被延后或返回 409 `pacing`，不能绕过；
  - 上次提交时间已持久化，重启不清零。

**SEC-T04 远端并发上限由服务端强制** · critical · 自动
- 测试：
  - 已有 3 个 `generating` 时，从各入口提交第 4 个；
  - fake site 注入「并行任务已达上限」提示。
- 期望：
  - 第 4 个停在 `awaiting_submit_slot`，点击计数不增加；
  - 收到上限提示后回到等待、不计失败，下次点击仍遵守间隔。

**SEC-T05 零自动重提** · critical · 自动 fake site
- 测试：
  - `submitting` 状态下杀进程并重启；
  - 点击后提交响应丢失，且历史对账也失败；
  - 分别注入 `moderation_reject`、`fill_mismatch`、`page_contract_broken`；
  - 断网后恢复；
  - `resume_queue`。
- 期望：
  - 每个 job attempt 内「生成」点击 ≤ 1；
  - `reroll` 算新的 attempt，且需要重新确认；
  - 自动重试只发生在 set_params / upload / fill / download。

**SEC-T06 canary 只读** · critical · 自动 + 手工
- 测试：
  - 自动：在 fake site 上以定时、批前、恢复前三种方式触发 canary；
  - 手工：`make canary` 跑真实站点时开启 Playwright trace，事后查看 trace。
- 期望：
  - fake site 点击计数为 0；
  - 真实站点 trace 中没有点击生成、没有上传、没有表单提交。

**SEC-T07 验证码 / 风控弹窗零交互** · critical · 自动
- 测试：fake site 注入验证码或风控弹窗。
- 期望：
  - 队列暂停；
  - 对弹窗元素零点击、零输入，也不点关闭按钮；
  - 恢复前 canary 若仍能看到弹窗，保持暂停。

**SEC-T08 README 首屏风险声明** · critical · 自动 grep
- 理由：spec 里「风险由用户知情接受」这一前提，依赖这段声明确实存在。
- 测试：README 首屏（前 40 行）检查以下内容：用户协议 5.1、付费协议 6.5 / 8.2、9.3 素材授权、「本人账号 / 本机 / 自用」，以及「不要把 `confirm_batch` 加入 allow 列表」。
- 期望：全部存在。

---

## 11. UI 源内安全

**SEC-U01 前端不渲染原始 HTML** · critical · 自动 `tests/ui/`
- 威胁：本服务源内的 XSS，等于以 `ui_human` 身份确认、花积分。UI 上的 prompt、参考名、暂停原因（页面弹窗文本）、即梦主体名、TOML 原文都是外部文本。
- 测试：
  - 静态禁用 `dangerouslySetInnerHTML`、`innerHTML`、`outerHTML`、`insertAdjacentHTML`、`eval`、`new Function`，以及允许 raw HTML 的 markdown 渲染；
  - e2e：在 prompt、主体名、暂停原因里放 `<img src=x onerror="window.__xss=1">`，依次打开确认页、看板、主体页、config 原文视图。
- 期望：扫描 0 命中；`window.__xss` 保持 undefined；上述文本按字面显示。

**SEC-U02 安全响应头** · critical · 自动
- 测试：检查 `GET /` 与 `/api/*` 的响应头。
- 期望：
  - `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'`；
  - `img-src 'self' data: blob:`。即梦主体缩略图若要外链，须显式列出或经本服务代理，二选一写死；
  - `X-Frame-Options: DENY`、`X-Content-Type-Options: nosniff`、`Referrer-Policy: no-referrer`。
  - 仓库先例：`ai_video_management` 的 `SecurityHeadersMiddleware`。

**SEC-U03 确认页防点击劫持** · critical · 自动
- 威胁：iframe 内发出的请求是 frame 自身源的 same-origin 请求，G2 / G3 挡不住，只能靠响应头。
- 测试：Playwright 打开 `http://127.0.0.1:9999` 上的页面，用 iframe 嵌入确认页。
- 期望：iframe 不渲染。

**SEC-U04 花积分 / 写即梦的按钮都经二次确认（FR-55）** · critical · 手工
- 测试：walkthrough 覆盖以下按钮：确认并开始、提交后取消、恢复队列、创建主体、改护栏键（K03）、promote 覆盖已有 `{key}.png`。
- 期望：每个都有确认页或二次确认，文案写明花费或「不退积分」。

---

## 12. 依赖与供应链

**SEC-D01 MCP Python SDK 版本下限** · critical · 自动
- 测试：解析 `requirements.txt`、`pyproject.toml`，并读取实际安装版本。
- 期望：
  - `mcp >= 1.23.0`（CVE-2025-66416 / GHSA-9h52-p55h-vw2f 的修复版本）；
  - 若使用独立 FastMCP 包，其依赖的 `mcp` 同样满足；
  - SEC-N12 要求的显式 `TransportSecuritySettings` 仍须存在。

**SEC-D02 锁定版本** · warning · 自动
- 理由：关系到可复现性与供应链暴露面，本身不是可利用漏洞。
- 测试：
  - `requirements.txt` 每一项都用 `==` 固定；
  - `pyproject.toml` 与之同名同版本；
  - `apps/ui/package-lock.json` 已提交，Makefile 用 `npm ci`；
  - Makefile 不使用 `uv`（`development.md` §6）。
- 期望：全部满足。

**SEC-D03 漏洞审计（`make audit`，不进 `make test` 硬门）** · warning · 自动
- 测试：`pip-audit -r requirements.txt` 与 `npm audit --omit=dev --audit-level=high`；离线时 skip 并写明原因。
- 期望：
  - 无 high / critical 公告；有公告时发 `validation.issue.raised`（severity=warning），附包名与修复版本；
  - 暴露面上的包（`mcp`、`starlette`、`fastapi`、`uvicorn`、`python-multipart`、`playwright`、`tomlkit`）出现 high 及以上公告时，升级为 critical，由人工判断是否可利用。

**SEC-D04 无遥测 / 外发** · warning · 自动 静态
- 理由：属启发式扫描。真正外发由 SEC-S03 与 SEC-B04 兜住。
- 测试：
  - 依赖中不含 `sentry-sdk`、`posthog` 等遥测 SDK；
  - 运行期 HTTP 客户端调用只指向 `127.0.0.1` 或 SEC-B04 白名单里的主机。
- 期望：0 命中。

---

## 13. localhost DoS-lite

本节全部为 `warning`：影响仅限本机可用性，不越出信任边界。其中违反 MCP ≤ 90 s 契约的部分，同时由 acceptance 级按 blocker 处理。

**SEC-R01 `wait_jobs` / `POST /api/jobs/wait` 超时钳制** · warning · 自动
- 测试：
  - `timeout_s` 取 `1e9`、`-1`、`0`、`NaN`、`"90"`、`null`、`90.5`；
  - `job_ids` 取 10 000 个、含重复、含不存在的 id。
- 期望：
  - 超过 90 的值钳到 90（或返回 422，写死一种）；
  - 负数、NaN、非数字：422；
  - `job_ids` 超过上限（如 500）：422；
  - 实际返回时间 ≤ 91 s。

**SEC-R02 批大小与请求体** · warning · 自动
- 测试：`POST /api/batches` 与 MCP `precheck_batch`，分别提交 10 000 条 items、1 MB 的单条 prompt、1000 个参考项、20 MB 请求体。
- 期望：
  - body 超过 2 MiB：413；
  - items 超过 200：422；
  - 参考数量先于 sha256 计算检查，不会为超限请求去哈希大文件。

**SEC-R03 并发长连接** · warning · 自动
- 测试：200 个并发 `wait` 请求，同时发 1 个 `/api/health`。
- 期望：
  - health 在 500 ms 内返回，BrowserActor 不被阻塞；
  - 超过并发等待上限：429。

**SEC-R04 幂等键与缩略图资源** · warning · 自动
- 测试：
  - `idempotency_key` 取 1 MB 长度，以及 10 万个不同的 key；
  - 用 30000×30000 的 PNG（解压炸弹）生成缩略图。
- 期望：
  - key 超过长度上限（如 128）：422，过期 key 清理生效；
  - 缩略图生成有像素上限，超限显示占位，不崩溃。

---

## 14. 手工 walkthrough（发 `validation.requires_manual_walkthrough`）

1. SEC-N09 (d)：真实浏览器从 UI 完成确认，核对库中 `confirmer=ui_human`、审计里的 `sec_fetch_site`。
2. SEC-C14：确认页上 3 条的缩略图、参数、积分与 API 一致。
3. SEC-T06：带 trace 跑一次 `make canary`（真实站点），检查 trace 中无写操作。
4. SEC-U04：高危按钮逐个过二次确认。
5. 首次 `make run` 时 Windows 防火墙**没有**弹出「允许专用 / 公用网络访问」。弹出就说明绑定了非回环地址，立即 critical。
6. 用浏览器打开 `http://127.0.0.1:8790/api/artifacts/...` 与 `/api/config/global`，肉眼确认页面不含 token，也没有渲染任何 HTML 快照。

---

## 15. Spec gaps（请 parent 回写 spec 或确认后再签字）

| # | 缺口 | 影响检查 | 建议 |
|---|---|---|---|
| G-1 | NFR 只写「同源 UI 通过 Origin 校验放行」。同源 GET 不带 Origin，判定未定义；Origin 本身也可被非浏览器客户端伪造 | N04, N05, N09 | 采用 §2 判定表（fetch-metadata），写入 NFR 安全 |
| G-2 | `confirm_batch` 的人工批准只靠 Claude Code 客户端权限询问。allow 列表或 bypass permissions 模式下，服务端对 MCP 花费零约束，与 §1「未经确认不花一分积分」冲突（`general.md` §6，stage-5 critical） | C10 | `confirmer=mcp` 计入每日预算（或新增 `confirm.allow_mcp` + `budget.mcp_confirm_daily_credits`），超额引导去 UI 确认 |
| G-3 | FR-1 把 `JIMENG_BRIDGE_TOKEN` 标为「可选」，未配置时的行为没写 | N08 | 未配置或短于 32 字符时 fail-closed（bearer 路径全部 403），UI 照常可用 |
| G-4 | `PUT /api/config/global` 能改 `confirm.*`、`budget.*`、`pacing.*`、`concurrency.*`、`cli.*`、`server.*`、`browser.profile_dir`，没有写权限划分，也没有上下限 | K03, P04, C08 | 执行路径类键 API 只读；护栏键只允许 UI 分类修改并写审计；schema 设上下限 |
| G-5 | 确认后执行用冻结请求还是重读盘上文件没写；参考 sha256 在上传前是否复核也没写 | C05 | 执行只用确认时持久化的 `GenerationRequest`；upload 前复核 sha256，不一致则 job 失败 |
| G-6 | 浏览器预演在确认**之后**才发生；页面积分高于已确认估算时怎么处理没写（FR-12 只要求高亮） | C06 | 偏差超阈值不提交，转人工或重新确认 |
| G-7 | 「当日」预算的时区、计入口径、取消后是否回补都没写 | C08 | 固定时区（系统本地时区于 config 显式记录），按确认时预计积分计入，取消不回补 |
| G-8 | body、items、job_ids、rules、glob、idempotency key、并发 wait 等上限数值未写入 spec | K05, R01–R04 | 写入 §6 NFR 或 `global.toml` schema 常量 |
| G-9 | `confirmer` 三个取值与鉴权方式的映射没写死 | C07, C09, N09 | 由服务端按 §2 分类推导，不接受请求体自报 |
| G-10 | 确认页需要参考图缩略图，§5.10 却没有对应端点 | F12 | 新增只读缩略图端点，受 `ai_videos/` 沙箱与媒体类型约束 |
| G-11 | FR-36 保存 DOM 快照与 trace，但没说哪些 artifact 可以经 HTTP / MCP 获取 | S06, F06 | 只服务图片；DOM 快照与 trace 永不经 HTTP / MCP 暴露 |
| G-12 | uvicorn 默认信任 127.0.0.1 发来的代理头，spec 未要求关闭 | N11 | 在 NFR 安全中写明 `proxy_headers=False` |
| G-13 | `confirmation_token` 的 HMAC key 来源与生命周期未定义 | C01, C02 | 进程内随机生成（重启后未确认 batch 需重新预检），或存于 `.data/` 独立文件（gitignored）；不得放 `global.toml` 或 DB |
| G-14 | `cli.path` 可执行体类型没有约束；dreamina 没有从文件读 prompt 的参数，argv 是唯一通道 | P02, P03 | 只接受原生 `.exe`；参数统一用 `--flag=value` 形式 |
| G-15 | FR-2 列出了每剧 config 的结构，但没说禁止出现全局护栏段 | K06 | schema 分离，每剧 config 出现全局段即报错 |

---

## 16. Accepted risks（user-acknowledged，不可测或不在 v1 防护范围）

- **R-1 平台 ToS 执法。** 用户协议 5.1 明文禁止用自动化工具接入；付费协议 6.5 / 8.2 可以作废权益或封号。平台的检测手段与阈值未知。本级检查只能证明暴露面被压小（T01–T08），**不能证明不会封号**。
- **R-2 同用户本机进程完整冒充浏览器。** 伪造全部 fetch-metadata 头，或直接读 `.env` 的 token、Chrome profile 的 cookie（DPAPI 对同用户可解）。HTTP 层无法区分，因此 `ui_human` 分类对恶意本机进程不可信。缓解：审计记录分类依据；README 约束 agent 不得伪造 Origin 或 `Sec-Fetch-*`。
- **R-3 MCP 确认的人工批准在客户端侧。** 采用 G-2 方案后，残余风险是预算额度内的花费。
- **R-4 积分口径不透明。** 失败或审核拒绝是否退积分未知；预计与实扣存在偏差；预算按预计积分计入。
- **R-5 NTFS hardlink。** 无法靠路径检测（创建者本身须已能访问源文件）。
- **R-6 素材授权。** 上传素材按协议 9.3 授权平台用于优化模型；写实人像素材可能被拒。这属于平台侧隐私问题。
- **R-7 本机明文数据。** profile cookie、截图（可能含昵称、余额）、trace 以本机用户权限存放在 `.data/`；本机一旦被入侵，会话即泄露。
- **R-8 目录 ACL。** Windows 上 `C:\workspace` 下的目录默认可能对本机其他已认证用户可读，`.env` 与 `.data/` 随之暴露。v1 不做 ACL 加固，只在 README 建议。
- **R-9 dreamina CLI 自身。** 它的网络行为与本地凭据存放位置不在本服务控制范围内。
- **R-10 自动化 Chrome 里的第三方脚本。** 即梦页面在自动化 Chrome 中执行任意第三方脚本。本服务只保证不暴露触达自己的通道（B02 / B05），不防页面针对浏览器本身的攻击。

---

## 17. 覆盖索引（spec → SEC）

| spec 锚点 | SEC |
|---|---|
| NFR 安全：只绑 127.0.0.1、Host / Origin allowlist、403 | N01–N05, N10–N14 |
| NFR 安全：非同源客户端必须带 Bearer、同源 UI 放行 | N06–N09, §2 |
| NFR 安全：token 只在 `.env` | N08, S01, S09, K04, P05 |
| NFR 安全：文件沙箱、拒绝 symlink 与 `..` | F01–F12 |
| NFR 安全：CLI 参数用列表 | P01–P03 |
| NFR 账号风险 | T01–T08, B03–B06 |
| FR-1 / FR-4 / FR-5 config | K01–K06, P04, S05 |
| FR-7 / FR-8 / FR-10 输入解析 | F03–F05, F08, F10 |
| FR-13 / FR-14 / FR-15 / FR-16 确认闸门 | C01–C12, C14 |
| FR-18 / FR-19 / FR-20 / FR-23 调度与恢复 | T03–T05, C13 |
| FR-24 幂等 | C12, R04 |
| FR-26 / FR-27 / FR-28 / FR-34 浏览器 | B01–B06, T02, T06, T07 |
| FR-30 / FR-35 / FR-39 / FR-42 / FR-43 落盘 | F07–F09 |
| FR-36 失败现场 | S03, S06 |
| FR-38 / FR-41 CLI | P01–P06 |
| FR-44 / FR-45 sidecar | S02 |
| FR-51 / FR-52 / FR-53 MCP | N12, C09, C10, S07, S09, R01 |
| FR-54 / FR-55 UI | U01–U04, C14 |
| §9 AC-2（确认闸门） | C01–C04, C11 |
| §9 AC-11（安全） | N03, N04, N06, F01 |
