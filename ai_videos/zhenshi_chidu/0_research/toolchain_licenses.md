# 调研 · 工具链与商用许可核对

> 2026-11-06 代理核对。用户要求「所有过程都可以商用」（立项对话 #3）。影片挂广告发 YouTube，属商用。
> 结论只对写明的版本有效；工具升级或换来源时重核。凡「未核实」的不许进入生产。

## 1. 总表

| 环节 | 工具 / 素材 | 版本 / 范围 | 许可（证据） | 结论 |
|---|---|---|---|---|
| 3D 软件与渲染 | Blender | 5.2.3 LTS（本机） | GPL：约束软件本身，渲出的画面归作者（Blender 官方 license FAQ） | ✅ |
| AI 遥控 Blender | `blender-mcp`（MCP for Blender） | 2.0.0（uvx 缓存 `blender_mcp-2.0.0.dist-info`，`License-Expression: MIT`） | MIT；Terms of Use（2026-08 版）只讲数据收集，不对产出主张权利 | ✅ 遥测保持关闭（`telemetry_consent=false`，2026-11-06 读回）；可另设 `DISABLE_TELEMETRY=true` 停发匿名使用记录（用户级配置，未改） |
| MCP 自带 3D 生成 | `generate_3d`（Tripo / Hunyuan3D / Hyper3D / Meshy / Premium） | — | 各家条款不同、多为收费 | ⛔ 不用（用户：不用 Hyper3D；全流程可商用） |
| 比例参照人 | MPFB（MakeHuman for Blender） | 2.x | 代码 GPLv3；自带素材 CC0；LICENSE.md §D：「no limitation on what you can do with this combined output」 | ✅ 只用自带素材；另下载的素材包逐个核 |
| 开放模型 | Poly Haven | — | CC0（站点与 MCP 返回均标 CC0） | ✅；但写实大型动物几乎没有（2026-11-06 搜 `animal` 只有老鼠与摆件） |
| 开放模型 | Sketchfab | 逐模型 | 逐模型许可字段 | ✅ 仅 CC0、CC-BY；⛔ NC / ND / SA / Standard / Editorial |
| 开放模型 | Poly Pizza | 逐模型 | CC0 或 CC-BY | ✅ CC-BY 需署名 |
| 开放模型 | Smithsonian 3D、NASA 3D Resources | 逐条 | Smithsonian 只收标注 CC0 的；NASA 媒体一般不受版权保护，但不得用 NASA 标志或暗示背书 | ✅ 逐条核 |
| 图生 3D 兜底 | TripoSR | main | 代码与模型 MIT（README）；依赖 torchmcubes MPL-2.0、rembg MIT、xatlas MIT、trimesh MIT、moderngl MIT、transformers Apache-2.0 | ✅ 兜底（ep01 30 只全用，follow-up 003）；产物卡上标 AI MODEL；2026-11-07 本机跑通 |
| 图生 3D 去背景 | rembg 模型 | rembg 2.0.87 | 代码 MIT；模型逐个不同：`isnet-general-use`（IS-Net/DIS，Apache-2.0）✅；默认 `bria-rmbg`（BRIA RMBG 2.0，HF 许可标 other：非商用，商用须另签协议）⛔ | ✅ 锁定 isnet-general-use（`tools/local_3d.py` 校验 sha256 `60920e99…964a`，缺文件报错、不自动下载）；2026-11-07 首跑时默认去下 bria，下载中断才没用上 |
| 图生 3D | TRELLIS | main | 本体 MIT，但 diffoctreerast 派生自 diff-gaussian-rasterization：「used non-commercially, i.e., for research」 | ⛔ |
| 图生 3D | TRELLIS.2 | main | 本体 MIT，但依赖 nvdiffrast（NVIDIA Source Code License 1-Way Commercial §3.3「only may be used … non-commercially」）与 nvdiffrec（同类条款） | ⛔ |
| 图生 3D | Stable Fast 3D | — | Stability Community License：年收入超 100 万美元需另购 | ⛔ 有条件，不选 |
| 图生 3D | Hunyuan3D | — | 许可排除欧盟、英国、韩国 | ⛔ 全球发布不适用 |
| 参考出图 | Codex 内置出图（`tools/codex_image.py`） | ChatGPT 订阅 | OpenAI 条款：输出归用户 | ✅ 第 1 版作 TripoSR 参考图；第 2 版（2.5D）直接作画面主体与 1.75 m 参照人（虚构人物）；照常先写请求日志 |
| 天空与光照 | Blender 内置 Sky Texture + 太阳光 | 5.2.3 | 软件内置程序纹理，渲出画面归作者 | ✅ ep01 第 1 版（3D） |
| 环境 HDRI、地面贴图、3D 草与石块 | Poly Haven：Mpumalanga Veld、Plains Sunset、Grass Ground、Grass Medium 01/02、Grass Bermuda 01、Moon Rock 02 | — | CC0（<https://polyhaven.com/license>，可商用、免署名；来源卡仍署名） | ✅ ep01 第 2 版（2.5D）起；文件与作者见 `_shared/SOURCES.md` |
| 抠像 | rembg `isnet-general-use` | 2.0.87 | 同上行 rembg：模型 Apache-2.0 | ✅ 2.5D 版主体与参照人抠像（`_tools/cutouts.py`，同样不许用默认的 bria 非商用模型） |
| 字体 | Inter、Noto Sans SC | — | SIL OFL 1.1（`projects/rank_scroll/assets/fonts/`） | ✅ |
| 国旗 | flagcdn | — | 国旗图案基本属公有领域（排行榜已用） | ✅ |
| 配乐 | 本机 Suno 服务 | Pro 档 | 订阅期内生成可商用；不用 Remix；不登记 Content ID（排行榜 bible §5） | ✅ 照常先写 `request_log.md` |
| 合成转码 | ffmpeg | N-125365（GPL build） | 约束软件本身，不约束输出 | ✅ |
| 数据 | 文献、机构数据 | — | 事实不受版权保护；只引数字并注出处，不照抄表述 | ✅ |
| 雕像 / 受版权保护建筑的造型 | 扫描模型、照片 | — | 全景自由（FoP）各国不同 | ⛔ 第一季不做；要做先单独调研 |

## 2. 证据来源（2026-11-06 读取）

- TRELLIS README License 节：<https://raw.githubusercontent.com/microsoft/TRELLIS/main/README.md>
- TRELLIS.2 README License 节：<https://raw.githubusercontent.com/microsoft/TRELLIS.2/main/README.md>
- diffoctreerast LICENSE：<https://raw.githubusercontent.com/JeffreyXiang/diffoctreerast/master/LICENSE>
- nvdiffrast LICENSE：<https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt>
- nvdiffrec LICENSE：<https://raw.githubusercontent.com/NVlabs/nvdiffrec/main/LICENSE.txt>
- FlexiCubes（Apache-2.0）：<https://raw.githubusercontent.com/nv-tlabs/FlexiCubes/main/LICENSE.txt>
- TripoSR README 与 requirements：<https://github.com/VAST-AI-Research/TripoSR>；torchmcubes（GitHub API spdx: MPL-2.0）
- rembg 模型清单与许可：rembg README 模型表；BRIA RMBG 2.0 许可：<https://huggingface.co/briaai/RMBG-2.0>（HF API `license:other`，非商用）；DIS 经 GitHub API 读回 `Apache-2.0`（2026-11-07）；IS-Net/DIS：<https://github.com/xuebinqin/DIS>（Apache-2.0）
- MPFB LICENSE.md：<https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.md>
- blender-mcp Terms：<https://raw.githubusercontent.com/ahujasid/blender-mcp/main/TERMS_AND_CONDITIONS.md>

## 3. 本机现状（2026-11-06）

| 项 | 状态 |
|---|---|
| Blender | 5.1、5.2 已装；运行中 5.2.3 LTS |
| MCP 插件 | 已更新（旧 1.5 备份为 `scripts/addons/blender_mcp.py.bak`），协议 15/15 一致 |
| MCP 素材库 | Poly Haven 开；Sketchfab、Poly Pizza 关（需 API key） |
| GPU | RTX 5000 Ada Laptop，16 GB |
| ffmpeg | N-125365，含 NVENC |
| MPFB | 2.0.18（Blender 官方扩展库，用户此前已装；2026-11-06 核对。离线另装的重复副本已卸载）；场景脚本用其男性基础人体烘焙成静态网格、缩放到 1.75 m |
| 本机 Blender 其他插件 | 用户 Blender 装有连 ComfyUI（127.0.0.1:8188）的 TRELLIS2 / PBR 插件，后台渲染时会尝试自动探测并失败；本系列不调用（TRELLIS 系非商用，见上表） |
| TripoSR | `.cache/venvs/triposr`（torch 2.11 + cu128，GPU 可用）；入口 `tools/local_3d.py`；权重 2026-11-06 由用户下载器取得，sha256 `429e2c6b…70ee` 已校验；去背景模型 `.cache/models/rembg/isnet-general-use.onnx`（md5 与 rembg 内置值一致）；单个 ~55 s（去背景在 CPU） |
