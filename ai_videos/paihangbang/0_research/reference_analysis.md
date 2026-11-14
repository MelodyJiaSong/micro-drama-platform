# 调研 A0 · 参考片拆解与赛道实测数据

> 2026-11-02。播放量用 `tools/yt_research.py`（yt-dlp）实测，原始数据在 `data/`：
> `country_cassette_uploads_2026-11-02.jsonl`（频道全部 155 条）、`yt_search_2026-11-02.jsonl`（4 个检索词、近一年、79 条）。
> 画面拆解来自浏览器逐帧截图（0:02、2:35、4:56）。

## 1. 参考片

**Top 50 Best Selling Car Brands in the World (2026)**，Country Cassette（@CountryCassette，约 11 万订阅，155 条视频；与 Nerd Cassette 等联合署名）。
时长 5:07（307 s），实测约 48.8 万播放、648 赞。描述框是关键词堆砌加 hashtag，**没有写数据来源**。

### 画面结构（逐帧确认）

- **白底**，画面里同时可见约 2–2.5 列，列之间用细竖线分隔。
- 每列（一张「卡」）从上到下依次是：
  1. 黑底白字的国家名横幅（如 CHINA、UK、CZECH REPUBLIC）。
  2. 主图：抠图的车型侧视图，国旗以「车身贴膜」的方式贴在车门上（这是视觉记忆点）。
  3. 品牌名放在灰色圆角药丸里。
  4. 上升柱状图图标 + 「Units Sold」+ 大号数字（取整到万，如 310,000）。
  5. 分隔线下方是「Rank 50」。
- **排序：从第 50 名到第 1 名倒数**，卡片从右侧进入、向左平移，冠军压轴。
- **节奏：** 第 25 名约在 2:35、第 1 名约在 4:56，即每名约 6 s，匀速。
- **结尾：** 两个片尾画面推荐同系列（摩托车、手机品牌），配一只动画手的点击动作。
- 同系列的封面统一：一排产品图加国旗加「X M UNITS SOLD」。

### 同系列（2026 年「Top 50 Best Selling X Brands」）实测

| 题目 | 播放 | 时长 |
|---|---:|---:|
| Car Brands | 488,282 | 308 s |
| Truck Brands | 385,703 | 305 s |
| Tractor Brands | 259,446 | 299 s |
| Smartphone Brands | 61,166 | 296 s |
| Bus Brands | 30,027 | 304 s |
| Motorcycle Brands | （检索未返回） | 299 s |

判断：同一模板，**冷门工业品（卡车、拖拉机）也能拿到二三十万播放**，说明这个格式本身有自然流量。手机是大众品类，反而偏低，可能因为竞争激烈或题材疲劳（推断）。

### 频道整体

- 149 条有播放数据：中位数 3.6 万，合计 2,916 万。
- 头部是**国家对比**（Qatar vs UAE 350 万、Turkey vs India 220 万、USA vs China 170 万、India vs Pakistan 170 万）和**按国家分类**（Cartoons From Different Countries 110 万）。
- 「How Many Countries Use the Same …」系列多数只有 0.2–7.5 万。

结论：**国家维度 + 对抗 / 归属感**是这个频道的流量引擎；品牌排行是新开的高效子系列。

## 2. 同赛道竞品（近一年检索，按播放排序摘录）

| 播放 | 时长 | 频道 | 标题 |
|---:|---:|---|---|
| 2,373,645 | 1142 s | Global Stats | Richest People in the World (1900-2026) |
| 1,135,282 | 482 s | Global Rank | Top 100 RICHEST People in the World 2026 |
| 710,760 | 581 s | Global Rank | Top 100 Richest People in Asia 2026 |
| 662,165 | 489 s | WatchData | Comparison: Worst To Best Country To Be Born In |
| 256,635 | 601 s | Match Data | Top 100 Richest People in the World 2026 |
| 147,922 | 453 s | Aesthetic Data | TOP 50 Best Selling Buses Brands In The World (2026) |
| 83,378 | 453 s | Aesthetic Data | TOP 50 Best Selling Trucks Brands … 2026 |
| 65,458 | 453 s | Aesthetic Data | TOP 50 Best Selling Cars Brands … (2026) |
| 52,669 | 453 s | Aesthetic Data | TOP 50 Best Selling Bike Brands … (2026) |
| 41,961 | 453 s | Aesthetic Data | TOP 50 Best Selling Cranes Brands … 2026 |
| 39,494 | 456 s | Aesthetic Data | 50 Top Selling Alcohol Brands … (2026) |

观察：

1. **「Top 50 Best Selling X Brands」已被至少两家同题跟拍**（Aesthetic Data 的公交、卡车、汽车、自行车、起重机、酒，每期都是 453 s 同一模板）。直接照抄选题会进入红海，并且正中 YouTube「模板批量」风险。
2. **富豪榜**有百万级需求，但跟风频道极多，而且涉及人物肖像，版权最难。
3. **国家对比、出生国好坏**这类「国家身份」题材，最高可到 66 万以上。
4. 时长集中在 **4–10 分钟**；超长的历史演变（19 分钟、240 万播放）属于另一种「时间轴」格式。
