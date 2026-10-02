## Stage-5 spec revision (v1 → v2) — 2026-09-13 11:11:49
Source: validation/{acceptance_criteria,bdd_scenarios,unit_tests,system_tests,security,accessibility,performance}.md + interview/qa.md「Stage-5 decisions」
Summary: 按用户三项裁决（只有 UI 能确认 / v1 只支持现行参考写法 / turntable 走网页视频）和 7 个 level worker 暴露的冲突与缺口，把 spec 修订为 v2。

Auto-updated:
- final_specs/spec.md — 确认闸门改为只接受 UI 身份；新增冻结请求与作业级终态表；调度只在拿到槽位后才准备；指纹改用 output_slot；resolver 按真实数据修订；阈值全部进入 config；身份判定表；下载只走页面控件；长耗时操作改为后台 operation；新增测试注入点。完整清单见 §11 Revision log。
- interview/qa.md — 追加「Stage-5 decisions」。
- validation/strategy.md — 新建；含 v1→v2 取代表与 carve-outs。

No conflicts found in: findings/*

## Stage-6 spec amendment — 2026-09-14 00:32:33
Source: stage-6 U3 service_shell / U6 management_ui integration (autonomous session, parent judgment call)
Summary: HTTP 表补齐 UI 需要的两个端点，并写明作业列表查询参数、裁决请求体和单次解码规则。

Auto-updated:
- final_specs/spec.md §5.10 — 新增 `POST /api/session/browser/open`、`GET /api/history/daily`；写明 `/api/jobs` 查询参数、adjudicate 请求体（含 approve_estimate）、路径只解码一次、UI 合同夹具。
- final_specs/spec.md §11 — 追加一行修订记录。

No conflicts found in: interview/qa.md, findings/*, validation/*

## Follow-up 001 — 2026-09-20 09:30:00
Source: user_input/follow_ups/202609.md - section 001
Summary: 实测证明 dreamina CLI 可直出 Seedance 2.5 的 30s 视频，修正能力矩阵中 seedance2.5 漏掉 cli 后端的错误。

Auto-updated:
- projects/jimeng_web_bridge/config/global.toml — `model_limits.models."seedance2.5".backends` 由 `["web"]` 改为 `["web", "cli"]`，附实测证据注释。
- projects/jimeng_web_bridge/tests/libs/domain/value_objects/test_model_limits__valueobject.py — FR1_ROWS 中 seedance2.5 的期望后端补 `BackendKind.CLI`。
- projects/jimeng_web_bridge/tests/libs/domain/value_objects/test_precheck__valueobject.py — 用例 C15（2.5 + 3 图 + CLI）期望由 `backend_unsupported` 改为无错。

No conflicts found in: final_specs/spec.md, interview/qa.md, findings/*, validation/*

Verification: `uv run pytest tests/ -q` → 2539 passed, 2 skipped.
Unverified: CLI 侧 2.5 的参考图上限（30/10/10）、1080p、`--ratio=9:16` 均未实测。
