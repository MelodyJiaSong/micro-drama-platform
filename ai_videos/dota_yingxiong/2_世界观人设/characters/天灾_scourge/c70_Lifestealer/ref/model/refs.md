# c70 噬魂鬼 · 原版模型参考（WC3 食尸鬼 `units\undead\Ghoul\Ghoul`，缩放 1.5、染暗 100,100,100）

> 暴雪娱乐 / PlayDotA 版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式。YouTube 只取封面与自动截帧，没下视频。warcraft.wiki.gg 本次被拦（返回 HTML 封锁页，已删），经典模型高清正面沿用 `m4_Ghoul/ref/model/wiki_Ghoul_WC3.png`（sha `c55a4085bebf`，同一模型）。
> **队伍色提醒**：上臂、手腕、大腿缠的布是队伍色（PlayDotA 动图里红、m4 参考里紫），随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面）| sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero122_character.gif | https://web.archive.org/web/2014id_/http://media.playdota.com/hero/122/character.gif（PlayDotA 噬魂鬼页 http://web.archive.org/web/2013id_/http://www.playdota.com/heroes/lifestealer；2013 快照取不到，用 2014） | 0036d84e746d | **DotA 1 里的噬魂鬼本体**（120 px，51 帧）：就是食尸鬼模型整体压暗——暗灰褐干皮、近黑条纹；深度佝偻、近乎四肢着地前扑；每只手三根又长又弯的骨爪；肩、上臂、手腕、大腿缠红布（队伍色） |
| playdota_hero122_icon.jpg | 同上 `/hero/122/icon.jpg` | 5b2904316aa6 | DotA 1 头像＝WC3 食尸鬼图标：张大的嘴、整排尖牙，头后一蓬墨绿黑毛，白眼 |
| wowpedia_BTNGhoul.png | https://static.wikia.nocookie.net/wowpedia/images/9/95/BTNGhoul.png（页面 https://wowpedia.fandom.com/wiki/Ghoul_(Warcraft_III)） | 1694ca07ea05 | 同上（与 m4 的 wiki_BTNGhoul.png 同一文件） |
| wowpedia_Ghoul.gif | https://static.wikia.nocookie.net/wowpedia/images/5/5a/Ghoul.gif | ad62c27db947 | 经典食尸鬼小动图（不染色、紫＝队伍色）：前扑、三爪挥击、背上骨刺 |
| yt_om1qboS0MO4_maxres.jpg | https://i.ytimg.com/vi/om1qboS0MO4/maxresdefault.jpg（「The BEEFIEST Ghouls you'll ever see (Level 3 Vampiric Aura) - WC3 - Grubby」；同图也在 m4） | 0c631c4ad54a | 经典食尸鬼游戏内侧面（不染色）：佝偻前探、大下巴整排牙、肩上骨刺与黑毛、长爪垂膝 |
| yt_R90RoCj8p2M_maxres.jpg | https://i.ytimg.com/vi/R90RoCj8p2M/maxresdefault.jpg（「DotA 6.83d - Lifestealer, Nai'x Beyond GODLIKE ! #3」） | 7b405b1ac1d6 | 6.83d 界面：头像为食尸鬼图标，名字 N'aix / Lifestealer |
| yt_R90RoCj8p2M_hq2.jpg | 同上 `hq2.jpg` | 9894a08c0aab | 6.83d 游戏俯视（英雄很小） |
| yt_R90RoCj8p2M_hq3.jpg | 同上 `hq3.jpg` | 15935fd5feb3 | 同上 |
| yt_kajazThRW9E_maxres.jpg | https://i.ytimg.com/vi/kajazThRW9E/maxresdefault.jpg（「DOTA 1 Lifestealer Naix Beyond GODLIKE + RAMPAGE」） | 5b52f4e992c3 | DotA 1 界面（英雄很小） |
| yt_kajazThRW9E_hq2.jpg | 同上 `hq2.jpg` | 74ae02a2f9a8 | 同上 |
| yt_AL0ggFp0lc8_maxres.jpg | https://i.ytimg.com/vi/AL0ggFp0lc8/maxresdefault.jpg（「DOTA LIFESTEALER - NAIX 40 KILLS IN 40 MINUTES」） | b8354ead641d | DotA 1 游戏近景（低角度），被特效挡，可见暗色伏低的身形 |
| yt_AL0ggFp0lc8_hq1.jpg | 同上 `hq1.jpg` | 66359231497c | DotA 1 俯视（英雄很小） |
| compare_classic_crops.png | 本地拼图（PlayDotA 动图 6 帧放大 + m4 的经典正面 + 游戏内侧面） | a1b93f0c2d13 | 出图验收对照用 |

## 结论（据图）

1. **就是食尸鬼**：和兵线食尸鬼 `m4` 同一模型，只是放大到 1.5、整体压暗；识别点照 `m4_Ghoul/ref/model/refs.md`。
2. **姿态**：深度佝偻、近乎四肢着地，头往前探、低到肩的高度；不是直立瘦长的人形。
3. **头**：头骨样的脸，粗眉骨、深眼窝；**下巴巨大前突，上下两排大方牙整排龇出**（第一识别点）；**头顶一蓬后竖的黑毛**，不是光头。
4. **背**：肩胛和脊背几根骨刺。
5. **手**：没有兵器，每只手三根又长又弯的骨爪，几乎前臂长。
6. **颜色**：干黄骨色皮 × 0.4 亮度 → 暗灰褐，条纹近黑，整体「暗的食尸鬼」；不是红皮。
7. **布**：上臂、手腕、大腿缠布（队伍色）→ 画成褪色发黑的脏布条。

## 与当前立绘对比（2026-10-21，旧图 `c70_Lifestealer_v1.png`）

- ❌ 姿态：旧图是两腿直立、手臂垂地的瘦长人形；原版深度佝偻、长臂撑地。
- ❌ 头：旧图是光头、骷髅脸张嘴；原版大下巴前突、两排大方牙整排龇出，头顶一蓬后竖黑毛。
- ❌ 没有肩背骨刺；爪是四五根细黑爪，原版是三根长骨爪。
- ✅ 灰黑暗色、无镣铐、腰间破布、长爪。
- **差异等级：大**（体型轮廓与头部识别点都不对，看起来是另一种怪物，不是放大的食尸鬼）→ 改卡；新立绘待出（follow-up 057，出图服务额度不足）。
