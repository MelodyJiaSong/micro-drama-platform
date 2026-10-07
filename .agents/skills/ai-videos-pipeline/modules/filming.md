# 影视改编

输入：已确定的故事。输出：episodes/epNN/filming.json 的 scenes。
每场写 id（s1等稳定编号）、background（bg环境资产key，未选可留空）、location、time、purpose（本场目标与变化）及 shots。
每镜只写 id（本场唯一的st1等稳定编号）、duration、action、camera、dialogue；时长为正整数秒。一个shot是一段连续画面；需要切镜时拆成多个shot。
同一background可由不同集/场次复用；当场时空和状态在scene/shot保存。scene/st编号创建后不因重排而改变，列表顺序决定播放顺序。
用可见动作、反应和对白表达故事，设计能拍清它们的摄影。
指定本镜实际对白，无对白时留空。Seedance保留自然环境声与动作声，禁止背景音乐/配乐；编译模块固定加入声音规则，配乐意图留给后期设计，不恢复legacy BGM约束。
选择镜头时按[镜头类型与景别](../../../references/project/ai_video_shot_sizes.md)区分功能与大小，核对取景保留／省略的信息；在camera内明确裁切范围和关键同框内容，不新增字段或自动附加QC。
不新增故事事实或改写动机、结果；需要改故事时向上游提出请求。
确认行为能被镜头看见，动作与对白能放进时间内。保存后由用户确定版本。
