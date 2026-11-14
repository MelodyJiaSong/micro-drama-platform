# ep03 可商用替代图搜索说明（给 Claude 子代理；follow-up 020 / 023 / 025）

今天是 2026-11-03。英文 YouTube 视频「30 AI Companies」每家一张 720×800 竖版满版卡（照片铺满，底部压文字）+ 一个 156 px 圆形创始人头像。现用的图大多许可未知（新闻照、官网照），所以默认母版需要**可商用许可**的替代图。

只收这些许可（以来源页写明的为准，逐张核对）：Public domain / CC0 / CC BY（任意版本）/ CC BY-SA（任意版本）/ Pexels License / Unsplash License / Pixabay Content License。**NC、ND、All rights reserved、未写许可的一律不要。**

- 不要 Wikimedia Commons / Wikipedia（upload.wikimedia.org、wikipedia.org 一律排除）。
- 好来源：Flickr 上的会议 / 机构账号（Web Summit、TechCrunch、Collision、VivaTech、SXSW、World Economic Forum、各国政府 / 大学账号、Gage Skidmore 等，常为 CC BY / CC BY-SA）；Unsplash / Pexels 上真实拍到该公司办公楼、招牌、产品（机器人等）的照片；公司自己以 CC 许可发布的图。
- Flickr 用 WebFetch 打开照片页确认许可（页面写 "Some rights reserved" 并链接到 creativecommons.org/licenses/by/... 才算），直接图片链接取 live.staticflickr.com 的 `_b.jpg`（1024）或 `_h.jpg`（1600）/ `_k.jpg`（2048）/ `_o.jpg`，越大越好。

每家要两类：

1. `photo`：能代表这家公司的真实照片——总部 / 办公室 / 招牌、产品实拍（机器人、设备）、公司活动现场，或创始人 / CEO 以该公司身份在活动上的照片（可以，作为替代图）。长边 ≥ 1600 px 优先，至少 1024 px。最多 4 张。
2. `person`：指定创始人的清楚正脸照（脸至少 250 px 高），来源页要明确写出此人名字，确认是本人。最多 3 张。

找不到合格的就给空数组，不要凑数，不要用许可不明的图。

输出 JSON（UTF-8），schema 与已有结果相同：
`{"items": [{"key": "<slug>", "images": [{"image_url", "page_url", "source", "author", "licence", "why"}]}]}`
其中 `licence` 照抄来源页（如 "CC BY 2.0"），`why` 写尺寸与内容。`photo` 和 `person` 分两个文件，路径见你的任务。每查完一家就把两个文件整份重写一次（防止断线丢结果）。不要改别的文件，不要下载图片，不要调用 Codex 或任何收费服务。

最后回复：每家 photo / person 各找到几张、许可类型；完全找不到的列出来。
