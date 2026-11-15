# 审稿项 physics（世界物理 · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-opus-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-232708_pregen_r2\items\physics__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-232708_pregen_r2\reports\physics__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-232708_pregen_r2" physics --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-232708_pregen_r2\reports\physics__a.md" --by "claude-opus-5-5/physics__a"`

## 评分维度
- **P1** 手数：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手
- **P2** 道具来源与去向：每件道具进场时在哪、出场时在哪；没有凭空出现或消失
- **P3** 交接三段：交接写清从哪拿、交到哪、对方怎么握住或收起；钱、灯、刮板都要
- **P4** 重力与支撑：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对
- **P5** 身体可行：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步
- **P6** 穿模与距离：人、动物、道具之间的距离够，走位路线不穿墙、不撞人
- **P7** 服装与动作相容：衣服允许这个动作（短袖不能卷袖、塞进腰里的下摆不会自己跑出来）
- **P8** 首帧 = 第 0 秒：首帧画的正是第 0 秒的状态，和节拍第一拍接得上
- **P9** 效果有来源：水花、溅泥、扬尘、影子、反光、湿脚印只出现在有来源的地方（踩在干的石头顶面不溅水，没风不扬尘）
- **P10** 真实速度：动作速度像真人：迈一步约 0.5 秒、跨三块垫脚石约 2 秒；分镜给的时长比真实动作长时，是加了别的内容还是把动作拉慢了（拉慢判 ✗）
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`