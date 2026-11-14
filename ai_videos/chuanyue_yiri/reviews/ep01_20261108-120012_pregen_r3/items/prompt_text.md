你是独立审稿人，代号 **prompt_text**，只管「Prompt 文本」法则。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-120012_pregen_r3\BRIEF.md`，严格按它的规则和报告格式做。

你的范围：s1。

要查什么：送给生成模型的文字与参考：过期与图文矛盾；物理上做不到的指令（手数、道具来源）；同一 prompt 内前后矛盾或歧义；节拍过满；镜组 prompt 的镜头切换与分界；系列硬规则与负面词是否写全、有无诱发禁区的词；规则源（bible、场景卡、考据）与 prompt 是否一致。最后给「重出前必须改」清单。

怎么查：读 filming.json、prompts.json、各资料包 prompt.txt 与 manifest.json、镜组板与首帧 prompt、人物卡、bible；只在需要验证时看成片。

## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）
- **T1** 图文一致：人物卡、参考图、prompt 文字、bible 互相一致，无过期描述
- **T2** 物理上做不到的指令（手数、道具来源）
- **T3** 同一 prompt 内的矛盾与歧义（景别、参考用法、负面词与正文）
- **T4** 负面词与系列硬规则写全（时代禁用、禁区、相机手机、首饰）
- **T5** 规则源（bible、场景卡、考据）与 prompt 一致
- **T6** 给出「重出前必须改」清单
- **R** 复核上一轮：previous.md 里本代号的重出 / 可剪 / 存疑问题，逐条写是否已改好

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-120012_pregen_r3\reports\prompt_text.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-120012_pregen_r3" prompt_text --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-120012_pregen_r3\reports\prompt_text.md" --by "<你的模型名>/prompt_text"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）