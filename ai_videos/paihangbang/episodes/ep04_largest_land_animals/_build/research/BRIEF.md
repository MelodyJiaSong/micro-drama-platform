# ep04 调研任务说明（给调研子代理）

今天是 2026-11-03。系列：YouTube 英文数据视频「排行榜」第 4 期 —— **World's Largest Land Animals, Top 30**。
每张卡：动物野外照片满版 + 国旗 + 大号主数值。主数值 = **成年雄性典型体重（kg）**；小字 = 学名、最大可靠记录体重、野外数量；徽章 = IUCN 受威胁等级。

## 收录口径（已定，照此判断）

- 按**物种**计（以 IUCN Red List 现行分类为准），亚种不单列（如 Kodiak 熊归入棕熊，可写进 notes / fun_fact）。
- 只收**现存野生物种**；家畜 / 家养型（家牛、马、家养牦牛、单峰驼、家水牛、大额牛）不收；野外灭绝或「可能已灭绝」的写清状态（代理会决定是否收）。
- 不收海兽（鳍足类）与鳄类（但鳄类仍要查数据，用于「为什么不在榜上」的洞察卡）。河马、北极熊照常收。

## 每个物种要查清的事实（只收有出处的；查不到写 null，不要猜）

```json
{
  "common_name": "African bush elephant",
  "scientific_name": "Loxodonta africana",
  "class": "mammal|bird|reptile",
  "iucn": {"category": "EN", "assessed_year": 2021, "population_trend": "decreasing|increasing|stable|unknown",
           "url": "https://www.iucnredlist.org/species/..."},
  "male_mass_kg": {"value": 6000, "kind": "mean|typical|range midpoint", "range_low": 5000, "range_high": 7000,
                   "text": "原文怎么说（简短引用或转述）", "source_name": "...", "source_url": "...", "tier": "primary|secondary"},
  "female_mass_kg": {"value": 3000, "source_url": "..."},
  "mass_cross_check": {"value": 6000, "source_name": "...", "source_url": "..."},
  "max_mass_kg": {"value": 10400, "text": "什么记录、哪年、是否可靠", "source_name": "...", "source_url": "..."},
  "shoulder_height_m": {"value": 3.2, "source_url": "..."},
  "wild_population": {"value": 415000, "display": "~415,000", "unit": "individuals|mature individuals", "year": 2016,
                      "source_name": "...", "source_url": "..."},
  "stronghold": {"iso2": "BW", "country": "Botswana", "evidence": "博茨瓦纳约 13 万头，约占全非洲 1/3", "source_url": "...",
                 "confidence": "high|medium|low"},
  "native_continents": ["Africa"],
  "fun_fact": "英文，≤ 90 字符，观众可能不知道", "fun_fact_source": "URL",
  "notes": "口径疑点、来源冲突（差异 > 10% 必写）、分类争议"
}
```

- `male_mass_kg`：成年雄性的平均 / 典型体重。来源只给范围时写范围并取中点（kind = "range midpoint"）。若某种雌性更大，在 notes 写明。
- `stronghold`：**野外个体数最多的国家**（国旗用它）。依据 IUCN 评估、各国普查、保护组织数据；拿不准就给 confidence = low 并列出前两三名候选。
- `max_mass_kg`：可靠记录的最重个体（野外或圈养写清）；传说 / 无出处的不收。

来源优先级：IUCN Red List 评估文本、同行评审论文、ASM《Mammalian Species》物种志、Animal Diversity Web（密歇根大学）、各国政府 / 国家公园 / 保护机构（WWF、IRF 国际犀牛基金会、GCF 长颈鹿保护基金会等）、知名动物园与博物馆 → 权威媒体 → Wikipedia（只作交叉核对，不作唯一出处）。不要用内容农场（a-z-animals、animalfactguide 等只可作线索，不可作出处）。每个 URL 都要是你真的打开或在搜索结果里看到的页面。

## 输出

把结果写成 JSON 文件（UTF-8、缩进 1）：`{"species": [ ... ]}`，路径见你的任务。另外如果你发现名单外还有成年雄性典型体重 ≥ 250 kg 的现存野生陆生物种，在 `"missed": [{"common_name","scientific_name","male_mass_kg","source_url"}]` 里列出。
最后回复里只给：写了哪个文件、每种一行（name / 雄性体重 / 来源类型 / stronghold+confidence / IUCN），以及所有查不到或有冲突的项。
