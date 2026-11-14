import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()))
from tools.service_request import RequestLog
p=Path("ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut")
n=p/'arms/capcut_notes.md'
text=n.read_text(encoding='utf-8')
text=text.split('\n### ?????????')[0]
text='\n'.join(line for line in text.split('\n') if not line.startswith('- ? 1 ') and not line.startswith('- ? 1'))
r=json.loads((p/'check/capcut.json').read_text(encoding='utf-8'))
sent=json.loads((p/'arms/_req/012_req.json').read_text(encoding='utf-8'))
assert sent['query'].endswith('45?55 seconds.')
sent['query']=sent['query'][:-len('45?55 seconds.')]+'45–55 seconds.'
(p/'arms/_req/012_sent_request.json').write_text(json.dumps(sent,ensure_ascii=False,indent=2),encoding='utf-8')
log=RequestLog(p)
from datetime import datetime,timezone
log.append({'event':'audit_correction','time':datetime.now(timezone.utc).isoformat(timespec='milliseconds'),'request_id':'328ed8005e174d4e85530cc4f62a8070','provider':'capcut','operation':'capcut_ailab_start_edit','reason':'本地 PowerShell stdin 编码使原请求日志末句 45–55 记为 45?55；实际原生工具调用发送的是 45–55。保留旧记录，追加当前发现及实际发送参数，非补造调用。','request_actually_sent':sent})
text+='\n\n### 合规机检与停止结论\n\n'
text+='- 第 1 轮上传完成：success=true，VID `v10b9eg5000cdbo9tsnog65ofs8ikkvg`，setPublic.success=true；已 set-vid。私有结果及目录核对范围后移除；未启用第 2、3 轮。\n'
text+='- 指定 check 已完成，退出码 0 仅代表执行完成；报告 `check/capcut.json` 的 `pass=false`。机检不通过。\n'
text+='- 摘要：208 个画面采样，4 个超阈值；global_max=0.0052、block_max=0.0415。195 个有效声音窗口，corr_p05=0.8803、corr_min=0.1569，3 段连续失配。另有 7 条草稿 VID 来源违规。\n'
text+='- 机检问题原文：\n\n'+json.dumps(r['problems'],ensure_ascii=False,indent=2)+'\n\n'
text+='- 修复判断：草稿只有 DRAFT 和七个承载必需剧情的 VIDEO，没有可单独删除的字幕、音乐、特效或转场片段。仅删背景模糊字段不能消除未知来源 VID 与已渲染画面/声音失配；删除这些 VIDEO 会破坏 brief 的必需剧情。替换来源、补登记未经证实的 VID 映射、改阈值、重剪或本地转码均超出“只删除违规元素”范围，未执行。background.blur=30 另作硬规则疑点记录，机检当前未把此字段列为问题。\n'
text+='- 未进行插件后期编辑，未伪造新的渲染结果；没有可执行的合规删除修复，因此未进行第二次下载或机检。本方合规未过，停止于 CHECK_FAILED。成片、草稿均为失败候选，不可进入盲审。\n'
text+='- 成片与草稿保留；报告 SHA256 与当前两文件均吻合。ffprobe 原样结果在 arms/capcut_probe.json。积分未知。009 无回执、结果未知。\n'
text+='- 审计编码问题：核对发现本地 PowerShell 向 python stdin 传代码时，把 012_req.json 末句范围中的 en dash 记成问号，原生 CapCut 调用实际发送的是 45–55。未重写原请求与历史日志；实际发送参数另存 012_sent_request.json，并对同一 request_id 追加 audit_correction。备注中同次 stdin 编码损坏的本次文字已修正，不涉及媒体或草稿改动。\n'
text+='- 全程未打开对照成片、对照检查、pool.json 的 arms、场景 cut_v*.json / s3_final_*.mp4 或集级 edit；未运行 blind / review / reveal；未打开或操作 CapCut 编辑器；未调用图像/视频生成、素材库、模板、字幕或配乐。\n'
text+='- 收尾：`python tools/followup.py check --all` 通过，本会话没有待收尾；其他会话与旧条目提示保留。既有工作区改动未覆盖。\n'
n.write_text(text,encoding='utf-8')
print('notes finalized; request encoding discrepancy recorded transparently')

