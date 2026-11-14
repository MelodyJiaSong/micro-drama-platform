# 审稿项 character_B（人物逻辑 · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s8、s5、s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-sonnet-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\items\character_B__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\character_B__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1" character_B --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\character_B__a.md" --by "claude-sonnet-5-5/character_B__a"`

## b 位 · codex · gpt-6.1-sol
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\items\character_B__b.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\character_B__b.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1" character_B --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\character_B__b.md" --by "gpt-6.1-sol/character_B__b"` `--attest-log <codex exec 运行日志>`（Codex 沙箱跑不了 python，由调用方凭日志代登记）

## 评分维度
- **C1** 知道什么：每个人此刻知道什么、不知道什么，行为不越过他的认知
- **C2** 想要什么：每个人此刻的目的清楚，动作服务于目的
- **C3** 视线：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）
- **C4** 反应拍：配角的反应单独占拍，不被吞掉；反应和身份、性格相符
- **C5** 主持人性格：Riley 的反应符合人设（好奇、敢试、自嘲），对当地人有回应
- **C6** 路人：路人有合理的反应且不雷同，不抢主笑点
- **C7** 动机连贯：跨镜头的情绪与动机连得上，没有突然的转变
- **C8** 听者在干什么：别人说话或画面焦点在别人身上时，其余每个人逐秒在做什么：有手上的活、反应钉在台词的具体词上；没有站成摆件的空白段（分镜里没写动作、出片里静止超过 1.5 秒都扣分）
- **C9** 像真人：把声音关掉看：每个人像活人还是摆件——反应及时（不超过 1.5 秒）、幅度合身份、不僵不夸张；一个梗是否拖成好几拍、同一个梗是否重复用
- **C10** 动机来自人物：每个不寻常的举动（避而不看、不回答、不指方向、突然停住）抛开剧情问「他为什么这么做」：答案只有「情节需要」就 ✗；分镜替他写的心理理由不算数，要看画面上观众能不能读出这个理由
- **C11** 反应合比例：配角的反应是不是过演：大表情（张大嘴、张嘴吸气、瞪大眼、鼓腮、笑出声）、单独一整镜的反应、比事情本身还大的情绪一律 ✗；宁可少一个反应，不要一张傻脸