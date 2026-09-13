## Stage-5 spec revision (v1 → v2) — 2026-09-13 11:11:49
Source: validation/{acceptance_criteria,bdd_scenarios,unit_tests,system_tests,security,accessibility,performance}.md + interview/qa.md「Stage-5 decisions」
Summary: 按用户三项裁决（只有 UI 能确认 / v1 只支持现行参考写法 / turntable 走网页视频）和 7 个 level worker 暴露的冲突与缺口，把 spec 修订为 v2。

Auto-updated:
- final_specs/spec.md — 确认闸门改为只接受 UI 身份；新增冻结请求与作业级终态表；调度只在拿到槽位后才准备；指纹改用 output_slot；resolver 按真实数据修订；阈值全部进入 config；身份判定表；下载只走页面控件；长耗时操作改为后台 operation；新增测试注入点。完整清单见 §11 Revision log。
- interview/qa.md — 追加「Stage-5 decisions」。
- validation/strategy.md — 新建；含 v1→v2 取代表与 carve-outs。

No conflicts found in: findings/*
