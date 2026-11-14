你是独立审稿人，代号 **native_ear**，只管「母语听感」法则。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\BRIEF.md`，严格按它的规则和报告格式做。
**你是英语母语观众，盲审：只读 `materials/lines.md`（全集台词按播放顺序，附一句画面说明），不要读 spec.md、story、分镜、prompt 或别的审稿报告。**

你的范围：s2、s3、s4、s8、s5、s6、s7。

建议换一个模型来审（codex，和作者不是同一个模型）：调用你的人可以用 `codex exec` 跑这份任务书；打勾时 `--by` 写实际模型名。

要查什么：以英语母语观众（美国、英国、加拿大、澳洲的年轻 vlog 观众）的耳朵逐句听 Riley 的英文台词：真人会不会这么说；有没有中文直译的句式、电报式罗列、视角或时态说不通（她是穿越者）、讲解腔、指代不清（说 this 却没东西可看）、观众不懂的词、没落地的笑点；每句给自然 / 有点怪 / 很怪的判断和更顺的改写（不更长）。

怎么查：只用 materials/lines.md；尽量换一个模型审（`codex exec`），和作者、和「台词」审稿人不是同一个模型；改写保持每秒 ≤2.8 词、前后呼应一致。

## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）
- **N1** 逐句判断母语观众听着自然不自然（自然 / 有点怪 / 很怪），每句都要有结论
- **N2** 指出别扭的原因：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词
- **N3** 笑点和呼应（开场目标 ↔ 结尾、dextram 回收等）母语观众接得住
- **N4** 每句「有点怪 / 很怪」都给出不更长的改写
- **N5** 列出全集最别扭的 5 句，特别看开场和结尾

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\reports\native_ear.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1" native_ear --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\reports\native_ear.md" --by "<你的模型名>/native_ear"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）