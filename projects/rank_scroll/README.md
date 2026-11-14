# rank_scroll

把 `ai_videos/paihangbang/episodes/epNN_*/` 渲染成横向滚动的 Top-N 排行视频（1920×1080，60 fps）。
规格见 `specs/development/rank_scroll/final_specs/spec.md`；输入契约见 `ai_videos/paihangbang/data_contract.md`；画面规范见 `ai_videos/paihangbang/bible.md` §2。

## 安装

```bash
python -m pip install -r projects/rank_scroll/requirements.txt   # skia-python 144.1、numpy、pytest
# 另需 ffmpeg 在 PATH 中
# 非拉丁字符（如 Commons 作者名）回退字体，17 MB，不进 git；缺失时改用 Windows 自带的 NotoSansSC-VF.ttf
curl -L -o projects/rank_scroll/assets/fonts/NotoSansSC-Variable.ttf "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
```

## 用法（在 `projects/rank_scroll/` 下运行）

```bash
python -m rank_scroll validate <ep_dir> [--strict]        # 校验数据、图片账本、国旗、图标、长度上限
python -m rank_scroll timeline <ep_dir>                   # 打印各段时长
python -m rank_scroll preview  <ep_dir> --t 3 40 300      # 单帧 PNG → <ep_dir>/render/preview/
python -m rank_scroll thumb    <ep_dir>                   # 1280×720 封面草图
python -m rank_scroll render   <ep_dir> --draft           # 960×540 30fps 草稿（libx264 veryfast）
python -m rank_scroll render   <ep_dir> --music a.mp3 b.mp3   # 正片；多首按顺序 4 s 交叉淡化，不足循环，响度 -16 LUFS
python -m rank_scroll render   <ep_dir> --music a.mp3@:180 b.mp3 --music-fit end   # a 截到 180 s；b 跳过开头、结尾对齐片尾；两遍线性 loudnorm
python -m rank_scroll render   <ep_dir> --from 60 --to 90     # 只渲一段
```

正片输出 `<ep_dir>/render/<episode>_master.mp4`，旁边写 `.manifest.json`（输入文件 sha256、模板版本、时间线、ffmpeg 命令）。

## 画面

- 片头 5 s → 滚动（第 N 名在左，卡片向左平移，匀速 2 px/帧；卡宽 600 时每名 ≈ 5.3 s，`layout.card_w` 可按期加宽；前 10 名卡片放大 1.06×）→ 冠军停留 6 s（光晕＋No. 1 标注）→ 计分板揭晓 7 s → 来源与署名 4 s → 片尾 18 s（留 YouTube 片尾元素位置）。
- 卡片 v0.2（满版照片海报）：照片铺满整卡（裁切焦点 `layout.focus` / `image_focus`），左上大国旗（原比例），右上名次，底部渐变上是国家、名称、大号数值，地点和标签并成一行小字，最底一行署名。
- 列表模式（契约 v1.3，follow-up 004，ep03）：`data.json` 写 `"mode": "list"`，按文件顺序从左到右出场，不显示名次、不放大前 10 名，结尾停在最后一张卡 4 s；公司卡（`logo` 白底牌、`person` 圆形头像，扣下时显示首字母、右上 `corner` 标签如 EST. 2015）。
- 洞察卡按 `insights[].after_rank` 插入滚动带，宽度为照片卡的 72%。
- 角落计分板按 `tally.by`（country / continent）累计已完整进入画面的卡片。
- 主题 token 在 `rank_scroll/theme.py`（default / skyline / alpine）。

## 素材许可

- 字体 Inter（SIL OFL 1.1，`assets/fonts/Inter-LICENSE.txt`）。
- 图标 Tabler Icons 3.24.0（MIT，`assets/icons/LICENSE.txt`）。
- 国旗 flagcdn（公有领域），在 `ai_videos/paihangbang/_assets/flags/`。

## 已知限制（v0.2）

- 本机 NVIDIA 驱动 596.58 低于 NVENC 所需的 610，草稿改用 libx264 veryfast（实测 960×540 约 390 fps；1080p60 正片约 129 fps，6 分钟片约 3 分钟渲完）。
- 名称只排一行，超长时缩小字号到下限后加省略号。
- 竖版 Shorts、柱状图竞赛、4K 尚未实现（spec Out of scope）。

## 测试

```bash
cd projects/rank_scroll && python -m pytest -q
```
