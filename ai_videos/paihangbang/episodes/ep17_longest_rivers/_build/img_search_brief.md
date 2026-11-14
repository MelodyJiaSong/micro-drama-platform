# 找图子任务说明（ep17 世界最长河流）

目标：为分给你的每条河找 **≥6 张候选真实照片**（至少要有 3 张许可可商用、且确认拍的就是这条河），写成一个 JSON 文件。只找链接，不下载、不生成图、不写别的文件。

## 规则
- **只用 WebFetch**（不要用 WebSearch：本会话搜索额度已用尽）。**不要调用 codex / Codex CLI / 任何收费服务。**
- 不用维基共享资源 / Wikipedia 的图（upload.wikimedia.org 一律不要）。
- 许可只收：Unsplash License（非 Unsplash+ / premium / plus）、Pexels License、Pixabay Content License、CC0、Public domain、CC BY、CC BY-SA。NC / ND / 保留所有权利 / 不明 的不要。
- **认准对象**：只收描述、标题、地点或标签里明确指向这条河（或河边的具体城市 / 地标 / 峡谷）的照片。同名不同物、只是「一条河」而说不清是哪条的，一律不收。宁缺毋滥。
- 偏好：横幅风景、河本身是主体、清晰、色彩好、长边 ≥ 2000 px；不要地图、卫星假彩色、水印、文字。

## 主要工具：Unsplash 站内搜索 JSON（经 WebFetch）
`https://unsplash.com/napi/search/photos?query=<关键词>&per_page=30`
WebFetch prompt 示例：`Output ONLY a JSON array (no prose) of the results where premium is false and plus is false, each as {"id":id,"u":urls.raw,"p":links.html,"a":user.name,"d":(description or alt_description) truncated to 100 chars,"w":width,"h":height}. Include every qualifying result.`
- 关键词换着试：河名的英文 / 当地语言 / 俄文（如 Енисей、Лена、Вилюй、Алдан、Оленёк、Нижняя Тунгуска、Урал река、Ишим）/ 葡语西语 / 沿河城市名 + river / 地标名。
- 描述不够判断时，看单张详情：`https://unsplash.com/napi/photos/<id>`（字段 location.name / location.city / location.country、tags[].title、description）。
- 直链：`image_url` = urls.raw 后面加 `&fm=jpg&q=85&w=3000`；`page_url` = links.html；`licence` = "Unsplash License"；`source` = "Unsplash"。
- 也可试 Pexels / Pixabay 页面（如 `https://www.pexels.com/search/<关键词>/`、`https://pixabay.com/images/search/<关键词>/`），能取到直链（images.pexels.com/photos/... 或 cdn.pixabay.com/photo/...）和作者就收；取不到就算了。

## 输出
写到给定路径，UTF-8 JSON，schema 严格如下（key 原样照抄我给的）：
```json
{"items":[{"key":"NN_<stem>","images":[{"image_url":"...","page_url":"...","source":"Unsplash","author":"...","licence":"Unsplash License","why":"为什么认定是这条河 + 画面描述（地点、角度、色彩）"}]}]}
```
每项 images 按你认为的好坏排序，最好的放前面。找不到 3 张确认可用的项，照样写上已有的，并在最终回复里列出「不足项 + 试过的关键词」。

## 最终回复（≤150 字）
每项找到几张（确认可用几张），哪些项不足、试过什么关键词。
