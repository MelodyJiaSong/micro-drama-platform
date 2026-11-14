# m182 瘟疫守卫 · 原版模型参考（WC3 兽族「蛇棒 / 毒蛇守卫」`units\orc\SerpentWard\SerpentWard`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1/2/3`＝视频约 25% / 50% / 75% 处），没下视频。GIF 抽帧另存 `*_frame.png`。
> **游戏里的红/蓝等纯色块常是队伍色**（随玩家变），不是角色本色。WC3 原版蛇棒是**红橙色**（暗影猎手的版本）；DotA 1 瘟疫守卫用同一模型，**技能图标与游戏画面都是绿色**——绿色是本卡的颜色，红橙只看造型。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Serpentward.gif | https://static.wikia.nocookie.net/wowpedia/images/8/8b/Serpentward.gif（页面 https://wowpedia.fandom.com/wiki/Serpent_Ward_(Warcraft_III)） | 58c564b4babe | **经典模型动图**（72 px，24 帧）：下面是一根**很矮的木桩**，桩头插着几片灰色刃片和白羽毛，桩脚一团红光；桩顶上方**悬着一个很大的、半透明发光的眼镜蛇头**（张开的蛇颈兜帽，比木桩大得多），蛇头与木桩之间连着一缕烟气 |
| wowpedia_Serpentward_frame.png | 上图 5 帧放大（本地抽帧） | 6fd9a6729595 | 同上 |
| wowpedia_Serpent_Ward_W3.jpg | https://static.wikia.nocookie.net/wowpedia/images/c/c2/Serpent_Ward_W3.jpg | ccfbfea302d8 | 游戏里的蛇棒：短木桩（带刃片、羽饰）插在地上，桩顶上方一团发光的蛇形兜帽 |
| wowpedia_BTNSerpentWard.png | https://static.wikia.nocookie.net/wowpedia/images/e/e8/BTNSerpentWard.png | 7561f860754e | WC3 原版图标：张大嘴、一对毒牙的眼镜蛇头，红橙色 |
| wowpedia_BTNGuardianWard-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/3/37/BTNGuardianWard-Reforged.png | 06688045ebaa | 重制版蛇棒图标（对照）：橙色发光的眼镜蛇头，绿眼，张开的颈兜 |
| playdota_hero106_skill-2.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/106/skill-2.jpg（PlayDotA 剧毒术士页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/venomancer，「瘟疫守卫 Plague Ward」） | de087fe323e0 | **DotA 1 瘟疫守卫图标**：同一个张嘴眼镜蛇头，**整体染成绿色** |
| yt_HOWJjpDrVw8_hq2.jpg | https://i.ytimg.com/vi/HOWJjpDrVw8/hq2.jpg（「Warcraft 3 Reforged: DOTA - Lesale Deathbringer (the Venomancer) Skills」https://www.youtube.com/watch?v=HOWJjpDrVw8） | 8d3fe9330307 | DotA 地图在重制版画面下的瘟疫守卫（HD 模型，只看颜色与轮廓）：**鲜绿色、半透明发光的立起眼镜蛇**，蛇颈 S 形昂起、兜帽张开，比剧毒术士还高一点；喷橙绿色毒 |
| yt_HOWJjpDrVw8_hq3.jpg | https://i.ytimg.com/vi/HOWJjpDrVw8/hq3.jpg（同上视频） | ef6d26c363d7 | 同上近景：几根绿色蛇守卫并排喷毒 |

## 结论（据图）

1. **造型**：主体是**一条昂起的大眼镜蛇（兜帽张开、张嘴露毒牙）**，蛇的上半身在最上面、最大、最显眼；下面是一根**矮木桩**（插着刃片与羽毛）把它「钉」在地上。不是「一根高木桩 + 一条细蛇螺旋缠绕」。
2. **颜色**：DotA 1 瘟疫守卫是**鲜绿 / 毒绿色**，蛇身半透明、自带绿光（原版红橙色是暗影猎手那一版）。
3. **蛇是灵体感**：原模型的蛇头是半透明发光的，和木桩之间连着一缕烟气。
4. **攻击**：张嘴朝目标喷毒（游戏里是一团橙绿色毒弹）。

## 与当前立绘对比（2026-10-21）

对比 `m182_Plague_Ward_v1.png`（旧图，sha `454f6f9d4bbc`）：

- 一致：插在地上不动的木桩 + 一条蛇、蛇头在最上面、嘴挂绿色毒涎、木桩上绑布条骨片。
- 不一致：轮廓是「高木桩 + 细蛇螺旋缠绕」，原版是「矮木桩 + 顶上一条昂起的大眼镜蛇（兜帽张开）」——蛇才是主体。
- 不一致：蛇是暗灰绿的普通蛇鳞、没有兜帽、不发光；原版是鲜绿、半透明带绿光的眼镜蛇。
- 小差异：木桩上的刃片与羽毛（旧卡写布条骨片）。

**差异等级：大**（轮廓与主色都不对）→ 改卡、待出图（出图服务额度不足，follow-up 057 暂停出图）。
