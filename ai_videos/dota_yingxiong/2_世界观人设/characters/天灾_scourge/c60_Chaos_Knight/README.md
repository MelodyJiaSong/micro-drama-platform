# 混沌骑士 本轮制作

首轮（follow-up 185，2026-10-24/25）：建立视频 + 四技能 720p，待用户看片 → [审阅包](demo/review_185_20261025/README.md)。

研究：[技能原版参考](ref/skills/refs.md) · [外观原图](ref/model/refs.md)。三视图 `views/`（取自建立视频 0.4 / 4.1 / 5.5 s）。

## Demo（follow-up 185，2026-10-25）

- 定版条：亮相 `7d91193b`（10 s）、混乱之箭第七版 `c38396e4`（12 s）、实相裂隙第六版 `ee565943`（13 s）、致命一击第二版 `cc96914b`（8 s）、幻象第六版 `acfa4832`（20 s）。四条技能合计 53.2 s。
- 成片 v1：[`demo/edit/final/ep01_final_v1.mp4`](demo/edit/final/ep01_final_v1.mp4)（63.833 s，sha `1e18c1332fe9`），剪辑记录 `cut_v1.json`，脚本 `.audit/adhoc_agents/2026-10-25/ck-demo/`。待用户看，未独立冷看、未试听、未锁片。
- 成片 v2：[`demo/edit/final/ep01_final_v2.mp4`](demo/edit/final/ep01_final_v2.mp4)（65.841 s，sha `f100e0a34e69`，`cut_v2.json`）：12 秒亮相 `bbe43389` + k601 第八版 `0cec8b26` + k602 第七版 `3fbd2254` + k603 `cc96914b` + k604 第七版 `1dadc9a7`；三条新片通过自我验证。待用户看，未独立冷看、未试听、未锁片。
- 成片 v3：[`demo/edit/final/ep01_final_v3.mp4`](demo/edit/final/ep01_final_v3.mp4)（65.841 s，sha `6505671bd17e`，`cut_v3.json`）：用户要求混乱之箭、幻象用回上一版——12 秒亮相 `bbe43389` + k601 第七版 `c38396e4` + k602 第七版 `3fbd2254` + k603 `cc96914b` + k604 第六版 `acfa4832`。**定版**（用户「就它了」），未独立冷看、未试听。发布文案 [`demo/publish.md`](demo/publish.md)。
- **follow-up 316（2026-11-01，严格 DotA 1）**：k602 实相裂隙按用户「改回原版」去掉裂隙门、传送特效改回 6.83d 脚本原样（第八版卡，峰值图 `k602_peak_v8`）；`3fbd2254` 与时间轴审阅已过期，待用户重审时间轴后重出。重出后 demo 成片 v3 `demo/edit/final/ep01_final_v3.mp4`（含 k602 `3fbd2254`）需重剪。k601 / k603 / k604 核过，无 Dota 2 来源画面，未改。
