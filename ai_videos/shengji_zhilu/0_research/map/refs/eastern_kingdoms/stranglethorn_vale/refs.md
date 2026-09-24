# 参考图 · 荆棘谷（Stranglethorn Vale）

> **用途边界（`divergence #8` / sk2 `#108`，不可商量）：图只进人眼，不进模型。**
> 唯一用途是人逐张看过、把地貌与布局写成**中文锁定串**，锁定串才进 prompt。
> **一张都不上传给生成模型**——① 暴雪美术资产不可再分发；
> ② 实测「喂图出图」会把游戏引擎的光照与材质 1:1 带进画面，正是半写实路线要防的那件事。
> 版权归**暴雪娱乐**；本目录是内部参考，不再分发。

| 文件 | 来源 | 尺寸 | 版本 |
|---|---|---|---|
| `WorldMap-StranglethornVale.jpg` | File:WorldMap-StranglethornVale.jpg | 1002 × 668 | **⚠ 现行零售版（无经典变体）** |

## 怎么用它

1. **人眼核点位**：对着它看我们生成的点位图（`../../../images/zones/stranglethorn_vale.png`）标得对不对。
2. **写锁定串**：把地貌 / 道路 / 水系 / 建筑群的**形制**写成中文，落进场景卡的锁定描述符。
3. **补坐标**：在图上量百分比坐标，回填 `map/g*.yaml` 的 `coords`，生成图就会越来越密。
4. **出 floor plan**：本图是 `ai_video.md` rule 4j 航线俯视图的底图依据之一。

抓取：`python tools/fetch_wow_maps.py --zone stranglethorn_vale`
