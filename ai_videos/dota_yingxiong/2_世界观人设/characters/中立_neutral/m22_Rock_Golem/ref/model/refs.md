# m22 岩石傀儡 · 原版模型参考（WC3 中立野怪「岩石傀儡」`units\creeps\RockGolem`）

> 暴雪娱乐 / Wowpedia / YouTube 截图等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。
> **肩背石刺的尖端颜色是队伍色**（经典动图里红、DotA 1 视频里蓝紫），随玩家变；石刺本身是灰黑石质。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_WC3_creep_Rock_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/8/8c/Warcraft_III_creep_Rock_Golem.jpg（页面 https://wowpedia.fandom.com/wiki/Rock_golem） | d0b298bbc58d | WC3 经典截图（远景）：灰褐色的驼背石巨人，双臂极粗，旁边一只小号泥傀儡 |
| wowpedia_Rock_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/4/4a/Rock_Golem.jpg | 6ea9714e067b | **经典模型全身（最清楚）**：灰褐色风化石块垒成，肩背极宽、驼背，小头陷在两肩之间；**两肩和背上竖着几根尖锐的黑灰石刺**；两条石臂比腿还粗、拳头是两块大圆石垂到膝；短粗石柱腿 |
| wowpedia_Rock_Golem_face.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/13/Rock_Golem_face.jpg | b8aa240bafed | 经典肖像：小石头脑袋，**眼与嘴连成一圈发黄光的缝**，像一道金黄色的面甲缝 |
| wowpedia_BTNRockGolem.png | https://static.wikia.nocookie.net/wowpedia/images/8/82/BTNRockGolem.png | bbb3d7cb4e55 | 经典图标（DotA 1 头像风格）：灰石头脸，**一只橙黄色发光的眼，嘴是一道发橙光的裂缝** |
| wowpedia_Rockgolem.gif | https://static.wikia.nocookie.net/wowpedia/images/7/77/Rockgolem.gif | caf7adf0c99a | 经典模型小动图（正面）：灰褐石身、发黄的脸缝、肩上几根石刺（红尖＝队伍色） |
| wowpedia_WC3_creep_Granite_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/9/9c/Warcraft_III_creep_Granite_Golem.jpg | aa781209fdef | WC3 同模型的「花岗岩傀儡」（染紫，对照）：同样驼背、巨拳、肩刺 |
| wowpedia_WC3_creep_Mud_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/1d/Warcraft_III_creep_Mud_Golem.jpg | 502fea42a54c | WC3 同模型的小号泥土傀儡（褐，对照；同 `m15`） |
| wowpedia_BTNRockGolem-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/9/96/BTNRockGolem-Reforged.png | 21d9b3714ebf | 重制版图标（对照）：灰石脸，眼与嘴里是熔岩般的橙光——与经典同一设计更清楚的版本 |
| wowpedia_Rock_golem_wcr.jpg | https://static.wikia.nocookie.net/wowpedia/images/f/fe/Rock_golem_wcr.jpg | 56aa596ff101 | 重制版全身（对照，**不照搬**熔岩裂纹）：黑石身、橙光脸、肩背成簇石刺、巨拳 |
| yt_QnlbLZ630-0_maxresdefault.jpg | https://i.ytimg.com/vi/QnlbLZ630-0/maxresdefault.jpg（「Granite Galem vs Black Dragon The Battle of Ancients」https://www.youtube.com/watch?v=QnlbLZ630-0 ，iCCup DotA 6.8x） | 564b2eed8306 | **DotA 1 远古营傀儡（左）**：同一副驼背巨拳的石身，DotA 里染成**赭红褐**；脸是一圈发橙黄光的面甲缝；肩上几根暗色石刺（尖端蓝紫＝队伍色） |
| yt_QnlbLZ630-0_hq3.jpg | https://i.ytimg.com/vi/QnlbLZ630-0/hq3.jpg（同上） | 4f5853b0e7a9 | **DotA 1 游戏内正面近景**：赭红褐石块身、发橙光的脸、肩刺；面板名 **Granite Golem**（见报告） |
| yt_1YNI8Hmrm5M_maxresdefault.jpg | https://i.ytimg.com/vi/1YNI8Hmrm5M/maxresdefault.jpg（「Mega Granite Golem VS Elder Jungle Stalker #Dota #iCCup」） | 97151307b7e4 | DotA 1 封面（左）：赭红石身、橙光脸、肩上红刺（队伍色） |
| yt_1YNI8Hmrm5M_hq1.jpg | https://i.ytimg.com/vi/1YNI8Hmrm5M/hq1.jpg（同上） | 043230795da5 | DotA 1 游戏内俯视：面板名 Granite Golem，赭红石身 |
| compare_classic_crops.png | 本地拼图（经典全身、经典图标、经典肖像、DotA 1 近景） | 9a7d6831fe05 | 出图验收对照用 |

## 结论（据图）

1. **体型轮廓**：驼背的石块巨人，肩背极宽，小头陷在两肩之间；两条石臂比腿粗、拳头是两块大圆石、垂到膝下；短粗石柱腿。（旧卡这一条对。）
2. **头 / 脸（第一识别点）**：小石头脑袋上，**眼与嘴连成一道发橙黄光的缝**，像面甲缝里透出的火光。旧卡写「两个暗洞当眼」「不发光」错。
3. **肩背石刺**：两肩和背上竖着几根尖锐的黑灰石刺，是轮廓上的第二识别点；尖端颜色是队伍色。
4. **石色**：WC3 原版是灰褐 / 赭灰的风化石；DotA 1 远古营里看到的那只（面板名 Granite Golem）染成赭红褐。本卡按原版灰褐。
5. 同模型：泥土傀儡（`m15`）、Roshan（`m7`）都用这副骨架，都带发光脸缝与肩刺（见报告）。

## 与当前立绘对比（2026-10-21）

当前立绘 `m22_Rock_Golem.png`（sha `2b7d4549d6c9`，2026-10-18 出）：

- ✅ 驼背、巨石拳垂膝、小头陷肩、石柱腿——轮廓对。
- ❌ 脸：两个黑洞当眼；原版是一道发橙黄光的眼嘴缝——头部最显眼特征缺失（旧卡负向还写了「发光的眼睛」把它排除了）。
- ❌ 肩背石刺：没有。
- ⚠️ 石色：冷灰花岗岩；原版偏灰褐 / 赭灰（小差异）。
- ⚠️ 缝里的干苔：原版没有，创作，可留可去（新卡去掉）。

**差异等级：大**（头部最显眼的发光脸缝与肩刺两项识别层缺失；拿不准时按大处理）→ 改卡、待出图（follow-up 057）。
