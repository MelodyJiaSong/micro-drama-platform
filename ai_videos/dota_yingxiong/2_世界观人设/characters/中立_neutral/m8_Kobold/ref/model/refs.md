# m8 狗头人 · 原版模型参考（WC3 野怪「狗头人」`units\creeps\Kobold\Kobold`，DotA 1 缩放 0.85、偏黄）

> 暴雪娱乐等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。
> **游戏里的红 / 紫纯色块是队伍色**（`KoboldWC3.gif` 里的红、工头身上的红），DotA 1 中立野怪的队伍色是黑 / 暗色，不进画面；毛色「偏黄」是地图染色（d01 §5.2 ✅）。
> 没找到 DotA 1 小野怪营的清楚截图（游戏内远景太小）；DotA 1 直接用这个经典模型，所以以 WC3 经典版为准。重制版只作对照。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_WC3_creep_Kobold.jpg | https://static.wikia.nocookie.net/wowpedia/images/d/d8/Warcraft_III_creep_Kobold.jpg（页面 https://wowpedia.fandom.com/wiki/Kobold_(Warcraft_III)） | e8a1fbe4aeb2 | **经典模型游戏内**：几只狗头人和一只工头。小狗头人：棕黄毛的小矮个，**头顶正中一截白蜡烛、橙色火苗，蜡烛两边各竖一只很大的圆耳朵**，看不到帽子；手里一把长柄、深灰头的镐类工具 |
| wowpedia_WC3_creep_Kobold_Taskmaster.jpg | https://static.wikia.nocookie.net/wowpedia/images/8/80/Warcraft_III_creep_Kobold_Taskmaster.jpg（页面 https://wowpedia.fandom.com/wiki/Kobold_Taskmaster） | fe21e3e97bc6 | **经典模型游戏内 + UI 头像**：头像是灰白鼠脸、红眼、一只粉色内侧的大圆耳、两腮一大蓬白须毛、头顶蜡烛；三只小狗头人都是「蜡烛 + 双大耳 + 棕黄身」，工头更大、拿大斧状工具 |
| wowpedia_BTNKobold.png | https://static.wikia.nocookie.net/wowpedia/images/2/26/BTNKobold.png（同页） | 1ec75d7831a0 | 经典图标：灰白毛鼠脸、一对**红眼**、尖耳缘、**两腮下巴一大蓬白须**、黄门牙 |
| wowpedia_KoboldWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/f/f7/KoboldWC3.gif（同页） | 2bf0157f31b7 | 经典模型小动图（16 帧）：两只大耳朵在头两侧，白色脸毛，手里一把深灰镐头的工具；红色是队伍色 |
| wowpedia_Wc3r_kobold_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/9/97/Wc3r_kobold_portrait.png（同页） | 8be79c06c0d3 | 重制版肖像（对照）：**蜡烛直接粘在头顶，蜡泪淌在头皮上，没有帽子**；大圆耳、大粉鼻、棕色胡须毛 |
| wowpedia_BTNKobold-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/2/2f/BTNKobold-Reforged.png（同页） | 37e427e688df | 重制版图标（对照）：粉紫鼠脸、长须、大门牙，头顶蜡烛与蜡泪，无帽 |
| wowpedia_Wc3r_kobold_taskmaster_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/b/b7/Wc3r_kobold_taskmaster_portrait.png | 193cd8e02f38 | 重制版工头肖像（对照，`m8-1` 用） |

Wowpedia 单位资料：近战（range 100 melee），重甲。

## 结论（据图）

1. **鼠脸**：尖吻、大鼻头、黄大门牙、长白胡须；经典版脸毛灰白、小**红眼**。（旧卡「鼠脸」对，「黑亮小眼」改成暗红小眼。）
2. **白腮须**：两腮和下巴一大蓬白色须毛，是经典图标里最显眼的脸部特征。旧卡没写。
3. **大圆耳**：头顶两侧一对很大的圆耳朵（内侧粉），远景里和蜡烛一起构成头部轮廓。旧卡没写。
4. **蜡烛直接粘在头顶，不戴帽子**：旧卡「破皮帽、帽顶插蜡烛」是凭记忆，帽子把耳朵和头形都盖掉了。
5. **身体**：棕黄毛（DotA 1 偏黄）、小矮个、弓背。
6. **武器**：手持一把深灰头的镐类工具，近战。（旧卡「短柄矿镐」大体对。）
7. 工头 `m8-1`：更大，头顶蜡烛更多，手持大号工具；隧道工 `m8-2` 未找到单独截图。

## 与当前立绘对比（2026-10-21）

当前立绘 `m8_Kobold_v1.png`（2026-10-18，sha `624906a11a3b`）：

- ✅ 鼠脸小怪、长胡须、黄门牙、棕毛、长尾、鼠爪、头顶点燃的蜡烛、矿镐——这些对。
- ❌ 头上一顶大皮帽，蜡烛粘在帽顶；原版蜡烛直接在光脑袋上，没有帽子。
- ❌ 大圆耳：被帽子盖住，完全看不到；原版一对大耳是头部轮廓的主体。
- ❌ 脸：深褐毛、黑眼、没有白腮须；原版灰白脸、白腮须、红眼。
- 帆布马甲、麻绳、护膝是创作，不破坏识别层，保留。

**差异等级：大**（头部最显眼的轮廓——大耳 + 光头顶蜡烛——被帽子换掉，脸色也不对；拿不准时按大处理）→ 已改卡，新立绘待出（出图服务额度不足）。
