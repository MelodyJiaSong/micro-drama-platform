# 排行榜系列 · 每期数据契约 v1.4（渲染器输入）

> 2026-11-03 代理定（用户授权自主决策）。渲染器 `projects/rank_scroll/` 只读本契约规定的文件；字段变化时同步改渲染器的校验。

## 目录

```
ai_videos/paihangbang/episodes/epNN_<slug>/
├── topic.md          # 选题卡（模板见 topics.md §4）
├── data.json         # 本契约
├── sources.md        # 每条主值的出处与交叉核对；许可核实记录
├── assets.json       # 图片版权账本（不在账本里的图不许渲染）
├── assets/img/       # 主图，文件名 NN_<slug>.jpg（NN = 名次两位）
├── render/           # 渲染输出（渲染器写）
├── qc.md             # 审片记录
└── publish.md        # 标题、描述（来源＋署名）、标签、封面说明
```

共用素材：`ai_videos/paihangbang/_assets/flags/{iso2小写}.png`（flagcdn，公有领域）。

## data.json

```json
{
  "episode": "ep02_highest_peak_by_country",
  "title": "Highest Mountain in Every Country",
  "kicker": "TOP 50",
  "metric_label": "Elevation",
  "unit": "m",
  "period_label": "Data as of Nov 2026",
  "source_line": "Sources: Wikidata (CC0), national surveys",
  "theme": "alpine",
  "tally": {"by": "continent", "title": "Peaks by continent"},
  "items": [
    {
      "rank": 1,
      "name": "Mount Everest",
      "subtitle": "Mahalangur Himal, Himalaya",
      "country_iso2": "CN",
      "country_name": "China",
      "continent": "Asia",
      "value": 8848.86,
      "value_display": "8,849 m",
      "secondary_display": "29,032 ft",
      "badge": "SHARED WITH NEPAL",
      "tags": [{"icon": "calendar", "text": "First ascent 1953"}],
      "image": "assets/img/01_mount_everest.jpg",
      "image_credit": "Author / CC BY-SA 4.0",
      "source": {"name": "...", "url": "...", "retrieved_at": "2026-11-03"},
      "cross_check": {"name": "...", "url": "...", "value": 8849, "diff_pct": 0.0},
      "notes": ""
    }
  ],
  "insights": [
    {"after_rank": 41, "text": "Short English fact, max 90 characters."}
  ]
}
```

（上例数值只示意字段。）

规则：

- `items` 按 rank 升序（1 = 冠军）；渲染器从 N 倒数到 1。rank 连续，同值同名次时 rank 可重复，但顺序须稳定。
- `value` 是排序用的原值（数字）；`value_display` 是屏上显示的字符串，由数据整理者按 bible §3.4 取整。
- `badge`：可选，≤ 22 字符，大写短语（NEW 2025、SHARED WITH NEPAL、UNDER DISPUTE 等）。
- `tags`：0–2 个；`icon` 只能取下面的名字；`text` ≤ 24 字符。
- `insights`：每 8–12 名一条，`after_rank` 指这张洞察卡出现在哪一名之后（倒数顺序里）；英文，≤ 90 字符，必须能被 `sources.md` 里的数据支持。
- `tally.by`：`country` 或 `continent`；用于角落计分板与结尾揭晓。
- `scope_note`（可选，≤ 600 字符，英文）：口径说明（算什么、不算什么、归属规则），进 YouTube 描述框。（v1.1，2026-11-03）
- `image_note`（可选，≤ 48 字符）：无图时占位卡上的一行说明，要写真实原因（版权 / 找不到可用图）。
- `image_risk`（可选，字符串）：图有法律风险（如所在国无商用全景自由）。渲染器**默认不用这张图**、显示占位卡；`--allow-risk-images` 才放进去，输出文件名带 `_with-risk-images`。是否放由人在发布前决定。
- `image_alt` / `image_alt_credit`（可选，v1.4，2026-11-03 follow-up 020）：有 `image_risk` 时，默认母版用这张可商用替代图（须在 `assets.json`、许可可接受）顶替，不出占位卡；`--allow-risk-images` 版仍用 `image`。用户要求每张卡都有高质量图，所以风险图一律配 `image_alt`。
- `layout`（可选，v1.2，2026-11-03 follow-up 004）：`{"card_w": 600, "focus": [0.5, 0.35]}`。`card_w` 卡宽（1080p 像素，480–800，8 的倍数；卡高固定 800），横幅照片多的期（山峰）用 720；`focus` 是本期照片满版裁切的默认焦点 `[x, y]`（0–1），竖幅高楼取 `[0.5, 0.04]` 保住塔尖。
- `image_focus`（可选，v1.2）：单张图的裁切焦点 `[x, y]`，覆盖 `layout.focus`；楼不在画面中间、被国旗或名次挡住时用。
- `mode`（可选，v1.3，2026-11-03 rank_scroll follow-up 004，ep03）：`rank`（默认，倒数到冠军）或 `list`（不排名的列表）。列表模式下 `rank` 就是出场位置，必须等于在 `items` 里的序号（1 = 最先出场、在最左）；不放大前 10 名，不显示名次，结尾停在最后一张卡 4 s（无冠军光晕与 No. 1 面板）；洞察卡不能放在最后一项之后。
- `corner`（可选，v1.3，≤ 12 字符）：卡片右上角的强调色标签（如 `EST. 2015`），有它就不显示名次。
- 公司卡（可选，v1.3）：有 `logo` 或 `person` 时卡片改版式——国旗缩小，名称上方左边是 `logo` 白底圆角牌，右边是 `person` 圆形头像加姓名与身份，国家名小字行去掉。
  - `logo`：PNG 路径，须在 `assets.json` 里且条目 `kind = "logo"`（商标，只作指认，许可字段写商标说明，不走可商用白名单）；`logo_bg`：底牌颜色，白色字标用深色。
  - `person`：`{"name" ≤ 28, "role" ≤ 32, "image", "credit", "focus": [x, y], "image_risk"}`；头像与主图同一套账本与许可规则，`image_risk` 单独标，扣下时显示姓名首字母圆章（bible §4 人物题材：不冒肖像权风险）。
- `thumb`（可选，v1.3，布尔）：封面草图优先取标了 `thumb` 的项（最多 3 个），否则取名次最前的 3 个；列表模式封面不写名次。
- `layout.flags`（可选，默认 true；rank_scroll follow-up 007，2026-11-03）：false 时整期不挂国旗（卡片、无图占位、封面都不画，署名行去掉 flagcdn），`country_iso2` 可为空；`country_name` 仍作卡上强调色小字行（ep05 病毒期写统计窗口）。计分板只能用 `tally.by = continent`，`continent` 字段可放任意分组名（ep05 = 传播途径）。
- `tally.icons`（可选，rank_scroll follow-up 009，2026-11-04）：`{分组名: 图标名}`，计分板揭晓页按它给每组画图标（图标名须在下方列表里），缺省为 globe。ep05 = 传播途径（wind / droplet / bug / bottle / paw / hand-stop）。
- `layout.intro_hold`（可选，秒，0–6，默认 0；rank_scroll follow-up 008，2026-11-03）：片头滑入结束后整排静止这么久再开始滚动，让倒数第一张卡（最后一名）也能读满 3 秒（bible §7-5）；建议 2.5。

## 图标名（Tabler Icons，MIT）

`mountain` `calendar` `building` `stairs` `map-pin` `ruler` `flag` `trophy` `users` `globe` `sparkles` `cpu` `virus` `vaccine` `skull` `droplet` `bug` `wind` `biohazard` `paw` `glass-full` `hand-stop` `bottle` `sparkles` `cpu`（v1.3）

## assets.json（版权账本）

```json
[
  {
    "file": "assets/img/01_mount_everest.jpg",
    "commons_page": "https://commons.wikimedia.org/wiki/File:....jpg",
    "source_url": "https://upload.wikimedia.org/...",
    "author": "Plain-text author name",
    "licence": "CC BY-SA 4.0",
    "licence_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    "attribution_required": true,
    "modified": "resized and cropped",
    "sha256": "...",
    "retrieved_at": "2026-11-03",
    "fop_note": ""
  }
]
```

可接受的许可：Public domain、CC0、CC BY（任意版本）、CC BY-SA（任意版本，只做缩放裁切）、Pexels License、Unsplash License、Pixabay Content License（可商用、免署名；账本里照记作者与来源页，follow-up 007）、`AI-generated (Codex image_gen)`（最后手段，经 `tools/codex_image.py` 生成，上传时勾选合成内容声明，follow-up 020）。GFDL-only、非商用（NC）、禁止演绎（ND）、来源不明的图一律拒绝。
