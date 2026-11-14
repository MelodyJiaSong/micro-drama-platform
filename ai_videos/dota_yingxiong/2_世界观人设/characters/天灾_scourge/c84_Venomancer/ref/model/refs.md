# c84 剧毒术士 · 原版模型参考（WC3 隐藏小动物 Hydralisk `Units\Critters\Hydralisk\Hydralisk`，DotA 原尺寸、染偏蓝 150/200/255）

> 暴雪娱乐 / PlayDotA 版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧（`hq2`/`hq3`＝视频约 50% / 75% 处），没下视频。`*_frame.png` 是本地把 GIF 抽帧拼成的看图用 PNG。
> **队伍色提醒**：WC3 截图里颈下一圈暗红可能是队伍色。**偏蓝染色**（R×0.59、G×0.78、B×1.0）作用在赭橙褐上只会把橙色压暗、偏橄榄，不会变成灰蓝——PlayDotA 录像里看到的仍是赭橙褐色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero106_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/106/character.gif（PlayDotA 剧毒术士页 http://www.playdota.com/heroes/venomancer 的 Wayback 存档） | 90c40360e9d4 | **DotA 1 里的剧毒术士本体**（120 px，30 帧）：赭橙褐色的直立蛇身异形，脑后一片高高竖起、收成尖顶的头冠；前胸一节节骨白横肋环；两条骨白镰刀前肢；下身灰橄榄环节 |
| playdota_hero106_character_frame.png | 上图本地抽帧拼图 | b3721038eec6 | 看图用 |
| wowpedia_HydraliskWC3.png | https://static.wikia.nocookie.net/wowpedia/images/c/c5/HydraliskWC3.png/revision/latest?format=original（页面 https://warcraft.wiki.gg/wiki/Hydralisk） | 220bfd69970d | **经典模型，最重要的一张**：同上，更清楚——赭橙甲片带深褐虎纹、尖顶头冠、骨白肋甲胸、灰橄榄腹环、骨白镰刀前肢、颈下一圈暗红 |
| wowpedia_Hydralisk.jpg | https://static.wikia.nocookie.net/wowpedia/images/4/4d/Hydralisk.jpg/revision/latest?format=original（同页「The Hydralisk from Warcraft III」） | 42b92644f7b4 | 战役里的游戏截图：同一赭褐造型 |
| wowpedia_BTNHydralisk.png | https://static.wikia.nocookie.net/wowpedia/images/5/5a/BTNHydralisk.png/revision/latest?format=original | 794134c54c96 | 经典图标：赭褐虎纹的头冠与口器 |
| wowpedia_BTNHydralisk-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/5/55/BTNHydralisk-Reforged.png/revision/latest?format=original | d8782f941b14 | 重制版图标（对照）：红褐甲、满口尖牙 |
| yt_ByFjqY8OVrU_maxresdefault.jpg | https://i.ytimg.com/vi/ByFjqY8OVrU/maxresdefault.jpg（「DoTa 6.83d - Venomancer, Lesale Deathbringer ★ Gameplay! #1」） | 40926e24ecf5 | DotA 6.83d 界面，左上角头像：赭褐虎纹头冠的虫脸 |
| `yt_uG062Gpuoro_maxresdefault.jpg` | 已删：Dota 2 来源，follow-up 316（原「Dotaology: History of Venomancer」封面，含 Dota 2 形象） | — | — |
| yt_sg-_mdk1Vs8_hq2.jpg | https://i.ytimg.com/vi/sg-_mdk1Vs8/hq2.jpg（「Warcraft 3: Eternity's End - Daughters of the Moon - Hydralisk (Secret Gameplay)」） | 1580106b6ade | WC3 战役游戏画面（远景） |
| yt_sg-_mdk1Vs8_hq3.jpg | 同视频 `hq3.jpg` | b4058e1616d7 | WC3 战役里的刺蛇：褐色直立身、白肋甲 |

## 结论（据图，替换旧卡凭记忆写的外观）

1. **颜色**：**赭橙褐带深褐虎纹**（DotA 偏蓝染色只把它压暗），不是灰蓝。旧卡「灰蓝几丁质」错。
2. **头冠**：脑后**一片高高竖起、收成尖顶**的叠片头冠，不是向两侧张开的眼镜蛇扇形颈褶。
3. **胸腹**：前胸一节节骨白横肋甲环，往下变灰橄榄环节。
4. **前肢**：两条骨白长镰刀。
5. **身体**：粗壮蛇身前倾直立，没有腿。

## 与当前立绘对比（2026-10-21）

旧图 `c84_Venomancer_v1.png`（2026-10-18）：
- ❌ 主色灰蓝 → 原版赭褐虎纹。
- ❌ 向两侧张开的眼镜蛇扇形颈褶 → 原版脑后竖起的尖顶头冠。
- ✅ 直立蛇身、两把镰刀前肢、没有腿、白色腹环。

**差异等级：大**（主色和头部最显眼特征都错）→ 已按图改卡并重出。

新图 `c84_Venomancer.png`（gid `JTs0FI2nv03DOR7yLJB7`）核对：脑后尖顶叠片头冠、赭褐甲片、骨白横肋胸、灰橄榄下腹、两把骨白镰刀前肢带黄绿毒液、无腿，均与结论一致；虎纹偏淡，属小细节。
