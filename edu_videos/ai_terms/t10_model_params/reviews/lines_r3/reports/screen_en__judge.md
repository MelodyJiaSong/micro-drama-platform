# screen_en__judge（claude-opus-5-5），lines_r3

## 裁决
- P1 2 理由：我按计数规则复核，没有超硬上限：l12 的示意图 + 两张卡共 16–17 词、3 块；l25 有 17 词、4 块，正好卡在上限；最长的标题是 l36「Set by training, not by hand」，6 词。a 判 3 分偏高，因为 l32「Chatting takes far more knobs」和 l19「Whole line goes up」仍是主谓句式。b 判 1 分偏重：s5_l32 截图里这句是压在旋钮阵列上方的 5 词大标题，不是照搬口播的整句；上一轮裁决人也已把它降为建议。所以判 2，有小瑕疵。
- R 1 理由：I3、I4–I6、I13/I14、I19–I21 都已解决，截图里能看到（s2_l12、s5_l37、s4_l29、s5_l35）。有两条没解决，或作者的理由站不住。① I1：到第 3 轮仍没有片尾和章节卡的截图，片尾是严格项，不能按「成片后再核」算通过。② I23：作者「不改」的理由是「收在 GPT-3 的千亿量级」，但 GPT-3 是 175B，而且 l39 口播明说引用新闻原话「over a hundred billion」，回扣的是 l01 的「100B+」，所以理由不成立。b 把 I8、I11、I12 算作「未解决」，不算数：这三条上一轮已由裁决人判不采纳，重新提出改写不等于原问题没解决。
- P6 2 理由：多数问题有可直接替换的改写，但 a 说「none exceeds the original word count」与事实不符：l10 的改写「Fare = base fare + per km × distance」比原文长。b 的 l25「New distance」语义含糊，不如原文。另外，下方补充问题里两人都漏掉的两处（s0_l03/l04 冷开头、l25「$30.50」）都没有改写。
- P4 1 理由：两人都漏了冷开头这个严格项。s0_l03/l04 左卡「LAST TIME / Learns from examples」，动词前没有主语，连着读像是「Last time learns from examples」；右侧眉标「WHAT IT ENDS UP WITH」里的 it，屏上找不到它指什么。冷开头按规则「有一点不对就必改」。a 只在 P2/P3 提了眉标，P4 仍给 2 分，等于没计入；b 完全没提。b 说 l39「100B」与「parameters」间距偏紧，s5_l39 截图看间距是正常的，不成立。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l03–l04（冷开头） | P4 | 必改 | LAST TIME / Learns from examples → WHAT IT ENDS UP WITH / A model | 严格项。「Learns from examples」缺主语，紧贴在眉标「Last time」下面，读起来像「Last time learns…」；箭头右边的「it」在屏上没有指代对象。整条冷开头链条在屏幕上没有主语。 | 左卡「Learning from examples」；右侧眉标「Result」（承接 a 的建议），整体读作「Last time: Learning from examples → Result: A model」 |
| l25 | P2, P4 | 建议 | 8 km → $30.50 | 屏上旋钮正好显示 $10.20 和 $2.54，l11 又教过观众自己算（「10 + 2 × 5 = 20」），一算就是 10.20 + 2.54 × 8 = $30.52，与屏上的 $30.50 对不上。口播说的是「about $30.50」，claims.json 写的也是「≈ 30.5」，屏上把约等号丢了。l35 已经用过「≈ 5,545 years」，加约等号与之一致。 | 8 km → ≈ $30.50 |

## 驳回
- l39（b，P4 间距）：s5_l39 截图中「100B parameters」与「100B knobs」两边的间距是一样的，上一轮裁决人也已判不成立。只保留「+」号缺失这一点（建议级）。
- l32（b，必改级别）：截图里这句是章内第一屏、压在旋钮阵列上方的 5 词标题，不是照搬口播的整句；维持上一轮的建议级。改写可以采用「More knobs for chat」，但不是必改。
- l25（b，「New distance」）：「new」相对于什么不清楚，还丢掉了与「twelve rides」的对应；不如原文，也不如 a 的「Not in our twelve」。
- l19（b，「Whole line ↑」）：只省一个词，换成箭头符号后不好照着读出来；原文 4 个词，和抬线动画同步，不必改。上一轮同一位置的「Upward shift」也已被驳回。
- l10（a，「Fare = base fare + per km × distance」）：改写比原文长，不符合 P6「更短」的要求。旁边旋钮标着「Base fare」，公式里写「base」不会有歧义，原文保留。
