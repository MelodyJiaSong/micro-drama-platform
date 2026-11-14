你是独立审稿人，代号 **prompt_text**，只管「Prompt 文本」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。

你的范围：s1、s2、s3、s4、s8、s5、s6、s7。

要查什么：送给生成模型的文字与参考：过期与图文矛盾；物理上做不到的指令（手数、道具来源）；同一 prompt 内前后矛盾或歧义；节拍过满；镜组 prompt 的镜头切换与分界；系列硬规则与负面词是否写全、有无诱发禁区的词；规则源（bible、场景卡、考据）与 prompt 是否一致。最后给「重出前必须改」清单。

怎么查：读 filming.json、prompts.json、各资料包 prompt.txt 与 manifest.json、镜组板与首帧 prompt、人物卡、bible；只在需要验证时看成片。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\prompt_text.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" prompt_text --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\prompt_text.md" --by "<你的模型名>/prompt_text"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）