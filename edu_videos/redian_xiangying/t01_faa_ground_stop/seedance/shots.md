# t01 Seedance 模拟镜头（v1，2026-11-14）

规则：生成永远人点——用户在对话里同意后才提交；先经 `tools/service_call.py` 写本期 `request_log.md` 再调用 Dreamina CLI。
统一参数：`dreamina text2video --model_version=seedance2.5 --video_resolution=720p --ratio=16:9`；成片里静音使用（只取画面）。
落盘：`seedance/<镜头id>/`（视频 + generation.json + prompt.txt + review.md），媒体不进 git。

| id | 用在哪 | 时长 | prompt |
|---|---|---|---|
| sd1_tarmac | s0 l02–l03（停飞令下达） | 6 秒 | Late afternoon at a large American hub airport, wide aerial drone shot slowly pushing in. Dozens of commercial airliners sit motionless at the gates and in a long queue on the taxiway, engines idling, ground crew standing beside baggage carts, waiting. Nothing takes off. Overcast sky, muted colors, realistic documentary news footage. No text, no captions, no logos, plain white aircraft with no airline livery. |
| sd2_control_room | s1 l11–l13（坏的是一张电信网） | 6 秒 | Inside a dim air route traffic control center: rows of controllers in headsets sit at large dark radar consoles glowing green and amber. One after another the radar screens flicker and freeze. A controller presses his headset, turns to the colleague beside him, then picks up a desk phone. Handheld camera, low light, tense, realistic documentary look. No readable text on screens, no logos, no recognizable real people. |
| sd3_cable_swap | s3 l42–l43（边飞边换） | 6 秒 | A telecommunications equipment room. On the left, an old rack full of tangled copper cables and blinking legacy switches; on the right, a new clean rack with yellow fiber optic cables. A technician's hands carefully unplug one cable from the old rack and plug it into the new rack while status lights keep blinking on both. Close-ups of connectors and LEDs, shallow depth of field, careful and tense mood, realistic. No text, no logos. |
| sd4_trench_cut | s4 l64（同一条沟，一下全断） | 6 秒 | Daytime construction site beside a road. An excavator bucket digs into a narrow trench; inside the trench two black cable conduits run side by side. The bucket bites down and tears through both conduits at once, the severed ends hanging in the dirt. Mid shot then close-up, overcast light, realistic. No text, no logos. |
| sd5_landing | s6 l79（三千五百多架安全落地） | 8 秒 | Night at a large airport, long telephoto lens. A long line of airliner landing lights stretches across the dark sky; planes touch down one after another on a brightly lit runway, calm and orderly. Realistic, cinematic, quiet mood. No text, no logos, no airline livery. |

合计 32 秒。积分以 Dreamina 回执为准（参考：2026-10-03 同入口 seedance2.5 720p 10 秒回执 200 积分）。
