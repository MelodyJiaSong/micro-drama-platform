# ep19 找图子任务（follow-up 023：不用 Codex，Claude 自己用 WebFetch / WebSearch 找候选）

目的：为排行榜视频「Most Visited Countries」每个国家找一张该国**标志性景点**的高质量照片，满版卡（约 9:10，横幅风景照会被居中裁成近方形）。

## 输入
- `image_tasks.json`（本目录）：每项 idx、key、国家、景点 landmark、地点、`hint`（要拍什么、机位、要排除的易混对象）、`content_file`（第一步写好的景点资料，在 ep 目录下）、`codex_candidates`（之前 Codex 找到的直链，**不要重复交**）。

## 怎么找
1. 首选 **Unsplash 站内搜索页**：`WebFetch https://unsplash.com/s/photos/<景点名用-连接>`，让它列出照片页 URL、`images.unsplash.com/photo-XXXX` 图片 ID、摄影师、alt 文本、是否 Unsplash+。**排除 Unsplash+（plus.unsplash.com / premium_photo）**——那不是免费许可。
   - 直链统一写 `https://images.unsplash.com/photo-XXXX?fm=jpg&q=90&w=3000`；licence 写 `Unsplash License`；page_url 写 `https://unsplash.com/photos/<slug>`。
2. 不够再用 Pexels（`https://www.pexels.com/search/<景点>/`，直链 `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg`，licence `Pexels License`）、Pixabay（直链 `https://cdn.pixabay.com/photo/...`，licence `Pixabay Content License`）、Flickr CC（直链 `live.staticflickr.com/..._b.jpg`，licence 照页面原文，如 `CC BY 2.0`；NC / ND 不要）。必要时用 WebSearch 找。
3. **不要**用维基共享资源 / wikipedia 图；不要带水印的图库预览（Getty、Shutterstock、Alamy、Dreamstime）；不要 AI 图、插画、拼贴。
4. 按 alt 文本和照片页描述**确认是 hint 里那个景点**（同名不同地、相似地标要排除），优先：经典机位、景点占满画面、色彩好（蓝天 / 黄金时刻 / 蓝调）、横幅或方形。
5. **每项至少 6 个候选**（加上 codex_candidates 合计 ≥ 8 更好）。每个直链用 Bash `curl -sIL -A "Mozilla/5.0" <url>` 确认返回 200 且 content-type 是 image/*，不是就换。

## 输出
写 `claude_<你的批号>.json`（本目录，UTF-8 合法 JSON），schema：
```json
{"items": [{"key": "00_01_france", "images": [
  {"image_url": "https://images.unsplash.com/photo-...?fm=jpg&q=90&w=3000", "page_url": "https://unsplash.com/photos/...",
   "source": "Unsplash", "author": "摄影师名", "licence": "Unsplash License", "why": "Mont-Saint-Michel from the causeway at sunset, whole island visible"}]}]}
```
key 必须原样照抄 image_tasks.json。只写你自己的那个输出文件，不改其他文件；不调用 Codex 或任何收费服务；不生成图片。
完成后回复 ≤120 字：每项候选数，哪些项不足 6 个、试过哪些来源。
