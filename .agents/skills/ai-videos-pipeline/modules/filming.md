# 影视改编

输入：已确定的故事；剧 README 的全剧 Vision（每场目的与镜头取舍对照它，见[决策记录](decisions.md)「对照 Vision」）。输出：episodes/epNN/filming.json 的 scenes。
每场写 id（s1等稳定编号）、background（bg环境资产key，未选可留空）、location、time、purpose（本场目标与变化）及 shots。
每镜写 id（本场唯一的st1等稳定编号）、duration、cast（出场人物资产键，如 `c1-1`、`c14`）、action、blocking（站位、朝向、视线、移动）、beats（按秒分拍，区间连续）、camera、lighting（光源与性格）、dialogue，可选 props（入画的剧情道具资产键，如 `p475`；道具锚点图进参考行，follow-up 231）；时长为正整数秒，写法见[Prompt 编译与出片](prompts.md)「分镜要给什么」（follow-up 227）。一个shot是一段连续画面；需要切镜时拆成多个shot。
同一background可由不同集/场次复用；当场时空和状态在scene/shot保存。scene/st编号创建后不因重排而改变，列表顺序决定播放顺序。
用可见动作、反应和对白表达故事，设计能拍清它们的摄影：对每个情绪或信息问「观众怎样看见」（见[六个问题](story-questions.md)「用场来想」）。不写「切到」「叠化」，只有承担意义、要两镜配合的转场才写，见[转场](edit-transitions.md)。
指定本镜实际对白，无对白时留空。Seedance保留自然环境声与动作声，禁止背景音乐/配乐；编译模块固定加入声音规则，配乐意图留给后期设计。
按拍摄单位从大到小设计：剧 workflow.json `format` 对应的[片种](filming-formats.md)页（电影的幕 / 连续剧的集）→ [场](filming-scenes.md) → [覆盖](filming-coverage.md) → [镜头](filming-shots.md)。
每场写场级决策记录、每集写集级决策记录，见[决策记录](decisions.md)。
覆盖规划（每场的覆盖档位、每个镜头是主镜头还是某个角度、覆盖哪些拍点或台词）待设计。
先按[场](filming-scenes.md)定每场的目的、环境与镜头覆盖；选择镜头按[镜头](filming-shots.md)：功能、景别、取景、角度与高度、焦点各自回答一个问题；在camera内写清本镜需要的项（裁切范围、同框内容、机位、焦点），一镜一种运镜；不另加字段或自动附加QC。
不新增故事事实或改写动机、结果；需要改故事时向上游提出请求。
确认行为能被镜头看见，动作与对白能放进时间内。保存后由用户确定版本。
