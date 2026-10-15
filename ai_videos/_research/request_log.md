# 外部服务请求日志

请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。

## 2026-10-03T02:11:44.532028+00:00 — openai_builtin / image_gen.imagegen — request

```json
{
  "provider": "openai_builtin",
  "operation": "image_gen.imagegen",
  "target": "ai_videos/_research/service_tests/openai_image/20261003-1790993504068/test.png",
  "request_id": "openai-image-20261003-1790993504068",
  "request": {
    "tool": "image_gen.imagegen",
    "arguments": {
      "prompt": "Generate one square photorealistic image of a single orange tabby cat sitting on a wooden windowsill in soft early morning sunlight. Natural relaxed pose, detailed realistic fur and whiskers, warm cozy light, softly blurred greenery outside the window. Clean coherent anatomy, appealing professional photographic composition. No text, no logos, no watermark.",
      "transparent_background": false
    },
    "purpose": "用户明确要求进行一次 OpenAI/ChatGPT 图像生成能力测试",
    "requested_model": "ChatGPT 最新图像模型",
    "actual_model": "unknown: this built-in interface exposes no model selector or returned model guarantee",
    "official_current_api_models": [
      "gpt-image-2.5-sunburst",
      "gpt-image-2.5-flare"
    ],
    "cost": "unknown",
    "reference_files": [],
    "transport_observability": "one built-in tool invocation; internal HTTP not exposed"
  },
  "time": "2026-10-03T02:11:44.532028+00:00",
  "event": "request",
  "pid": 24380,
  "request_fingerprint": "0ed1880212f65c19f0e3a9cdfea3c0f0f1cb21cd7003e687582bee07fcef97d7"
}
```

## 2026-10-03T02:13:52.263490+00:00 — openai_builtin / image_gen.imagegen — result

```json
{
  "request_id": "openai-image-20261003-1790993504068",
  "provider": "openai_builtin",
  "operation": "image_gen.imagegen",
  "target": "ai_videos/_research/service_tests/openai_image/20261003-1790993504068/test.png",
  "pid": 24380,
  "request_fingerprint": "0ed1880212f65c19f0e3a9cdfea3c0f0f1cb21cd7003e687582bee07fcef97d7",
  "time": "2026-10-03T02:13:52.263490+00:00",
  "event": "result",
  "elapsed_since_request_logged_s": 127.731,
  "response": {
    "event": "result",
    "source_image": "C:\\Users\\light\\.codex\\generated_images\\01a0fd65-4e50-75a3-846b-1f1296c02a3e\\exec-f5db4f2b-2b09-48fa-a4b9-74ace763f58e.png",
    "output_hint": "Generated images are saved to C:\\Users\\light\\.codex\\generated_images\\01a0fd65-4e50-75a3-846b-1f1296c02a3e as C:\\Users\\light\\.codex\\generated_images\\01a0fd65-4e50-75a3-846b-1f1296c02a3e\\exec-f5db4f2b-2b09-48fa-a4b9-74ace763f58e.png by default.\nIf you need to use a generated image at another path, copy it and leave the original in place unless the user explicitly asks you to delete it.\nThe generated image is already displayed to the user. There is no need to render it in the final response as a Markdown image or file link.",
    "actual_model": null,
    "cost": null,
    "image_generation_succeeded": true,
    "image_count": 1,
    "error": null,
    "tool_reported_wall_time_s": 21.4,
    "source_file": {
      "path": "C:\\Users\\light\\.codex\\generated_images\\01a0fd65-4e50-75a3-846b-1f1296c02a3e\\exec-f5db4f2b-2b09-48fa-a4b9-74ace763f58e.png",
      "exists": true,
      "bytes": 2151008,
      "sha256": "e50b9533416a05de3f2294be05cbb191a735e50bd081678bd8484e44dbdcbea4"
    }
  }
}
```

## 2026-10-03T02:13:52.333031+00:00 — openai_builtin / image_gen.imagegen — artifact_saved

```json
{
  "request_id": "openai-image-20261003-1790993504068",
  "provider": "openai_builtin",
  "operation": "image_gen.imagegen",
  "target": "ai_videos/_research/service_tests/openai_image/20261003-1790993504068/test.png",
  "pid": 24380,
  "request_fingerprint": "0ed1880212f65c19f0e3a9cdfea3c0f0f1cb21cd7003e687582bee07fcef97d7",
  "time": "2026-10-03T02:13:52.333031+00:00",
  "event": "artifact_saved",
  "elapsed_since_request_logged_s": 127.731,
  "response": {
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\openai_image\\20261003-1790993504068\\test.png",
      "exists": true,
      "bytes": 2151008,
      "sha256": "e50b9533416a05de3f2294be05cbb191a735e50bd081678bd8484e44dbdcbea4"
    },
    "width": 1254,
    "height": 1254,
    "actual_model": null,
    "cost": null
  }
}
```

## 2026-10-03T02:31:46.962+00:00 — ccconnect / send image — request

```json
{
  "request_id": "80a24e249b634cd380b6eef6bfefed77",
  "provider": "ccconnect",
  "operation": "send image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\openai_image\\20261003-1790993504068\\test.png",
  "pid": 10352,
  "request_fingerprint": "8266fbc9974c41d1d0f8e8c376c05e1a9851fba6aac335150ac6b3f9198e43f0",
  "time": "2026-10-03T02:31:46.962+00:00",
  "event": "request",
  "request": {
    "argv": [
      "C:/Users/light/AppData/Roaming/npm/node_modules/cc-connect/bin/cc-connect.exe",
      "send",
      "--project",
      "my-project-4",
      "--image",
      "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\openai_image\\20261003-1790993504068\\test.png"
    ],
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\openai_image\\20261003-1790993504068\\test.png",
      "exists": true,
      "bytes": 2151008,
      "sha256": "e50b9533416a05de3f2294be05cbb191a735e50bd081678bd8484e44dbdcbea4"
    },
    "destination_project": "my-project-4",
    "destination_platform": "feishu",
    "destination_chat": "oc_bbdc8585203d40cfac52937c3f674dd1",
    "authorization": "[REDACTED]",
    "timeout_s": 120
  }
}
```

## 2026-10-03T02:31:48.993+00:00 — ccconnect / send image — result

```json
{
  "request_id": "80a24e249b634cd380b6eef6bfefed77",
  "provider": "ccconnect",
  "operation": "send image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\openai_image\\20261003-1790993504068\\test.png",
  "pid": 10352,
  "request_fingerprint": "8266fbc9974c41d1d0f8e8c376c05e1a9851fba6aac335150ac6b3f9198e43f0",
  "time": "2026-10-03T02:31:48.993+00:00",
  "event": "result",
  "elapsed_s": 2.015,
  "response": {
    "returncode": 0,
    "stdout": "Message sent successfully.\n",
    "stderr": ""
  }
}
```

## 2026-10-11T07:03:05.834+00:00 — codex_imagegen / image_gen — request

```json
{
  "request_id": "6fd9d7360e0a447ea6d2d078d6fe6ac5",
  "provider": "codex_imagegen",
  "operation": "image_gen",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\codex_image\\20261011_test.png",
  "pid": 38940,
  "request_fingerprint": "20b298f6e3e49d458a317082afbf01653f0cc8498cd586d6d67c272cad9a06c6",
  "time": "2026-10-11T07:03:05.834+00:00",
  "event": "request",
  "request": {
    "service": "Codex CLI 内置 image_gen（ChatGPT 订阅额度）",
    "prompt": "Vertical 9:16 cinematic still: a young swordsman in a dark blue Song-dynasty robe standing on a misty mountain path at dawn, soft rim light, realistic skin texture, shallow depth of field. No text, no watermark.",
    "instruction": "你是出图执行器。只做一件事：调用一次内置 image_gen 工具生成一张图片。\n\n- 图片描述原样使用下方 <prompt> 里的全文，不增删、不改写、不翻译。\n- 不运行任何 shell 命令，不读写文件，不调用其他工具，不搜索网络，不提问。\n- 生成后只回复 DONE；工具失败或被拒时只回复 FAILED: 加原因。\n\n<prompt>\nVertical 9:16 cinematic still: a young swordsman in a dark blue Song-dynasty robe standing on a misty mountain path at dawn, soft rim light, realistic skin texture, shallow depth of field. No text, no watermark.\n</prompt>\n",
    "argv": [
      "C:\\Users\\light\\AppData\\Roaming\\npm\\codex.CMD",
      "exec",
      "--json",
      "--skip-git-repo-check",
      "--sandbox",
      "read-only"
    ],
    "files": [],
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\codex_image\\20261011_test.png",
    "transparent_background": false,
    "codex_model": "用户 config 默认",
    "image_model": "未知（内置工具不暴露）",
    "quality": "未知",
    "size": "未知",
    "cost": "未知",
    "sandbox": "read-only",
    "timeout_s": 580,
    "generated_root": "C:\\Users\\light\\.codex\\generated_images"
  }
}
```

## 2026-10-11T07:05:25.727+00:00 — codex_imagegen / image_gen — result

```json
{
  "request_id": "6fd9d7360e0a447ea6d2d078d6fe6ac5",
  "provider": "codex_imagegen",
  "operation": "image_gen",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\codex_image\\20261011_test.png",
  "pid": 38940,
  "request_fingerprint": "20b298f6e3e49d458a317082afbf01653f0cc8498cd586d6d67c272cad9a06c6",
  "time": "2026-10-11T07:05:25.727+00:00",
  "event": "result",
  "elapsed_s": 139.875,
  "response": {
    "returncode": 0,
    "timed_out": false,
    "stderr_tail": "Reading prompt from stdin...\n2026-10-11T07:03:11.478910Z ERROR codex_models_manager::manager: failed to refresh available models: request timed out\n",
    "thread_id": "01a129c5-b9dd-7b70-a0de-8f6dc250052c",
    "images": [],
    "usage": {
      "input_tokens": 44009,
      "cached_input_tokens": 34176,
      "cache_write_input_tokens": 0,
      "output_tokens": 162,
      "reasoning_output_tokens": 55
    },
    "last_message": "DONE",
    "event_types": {
      "thread.started": 1,
      "turn.started": 1,
      "error": 1,
      "item.completed": 1,
      "turn.completed": 1
    },
    "generated": [
      {
        "path": "C:\\Users\\light\\.codex\\generated_images\\01a129c5-b9dd-7b70-a0de-8f6dc250052c\\exec-2fd57e1f-b822-48c1-b420-a9b85427b96d.png",
        "exists": true,
        "bytes": 2314406,
        "sha256": "6674793d89afd8e21b27f78d76200e0c58a4eb183162700a9d79ac0aa7bf2da6"
      }
    ],
    "saved": [
      {
        "path": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\codex_image\\20261011_test.png",
        "exists": true,
        "bytes": 2314406,
        "sha256": "6674793d89afd8e21b27f78d76200e0c58a4eb183162700a9d79ac0aa7bf2da6"
      }
    ]
  }
}
```

## 2026-10-12T21:47:53.206877+00:00 — cascadeur / inspect_installed_application — request

```json
{
  "request_id": "c952c5b1a70e40b88ccb99698c8753bd",
  "provider": "cascadeur",
  "operation": "inspect_installed_application",
  "target": "ai_videos/_research/service_tests/shu_motion_20261013",
  "time": "2026-10-12T21:47:53.206877+00:00",
  "event": "request",
  "request": {
    "interface": "computer-use @oai/sky",
    "executable": "C:/Program Files/Cascadeur/cascadeur.exe",
    "purpose": "核对版本、套餐与本地视频捕捉能力；暂不上传或生成",
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T21:49:02.750924+00:00 — cascadeur / inspect_installed_application — result

```json
{
  "request_id": "c952c5b1a70e40b88ccb99698c8753bd",
  "provider": "cascadeur",
  "operation": "inspect_installed_application",
  "target": "ai_videos/_research/service_tests/shu_motion_20261013",
  "time": "2026-10-12T21:49:02.750924+00:00",
  "event": "result",
  "response": {
    "version": "2026.2.1",
    "plan": "Pro (启动页可见)",
    "window": "Cascadeur 主界面已打开",
    "launch_helper": "初次报未发现窗口；随后找到主窗口"
  }
}
```

## 2026-10-12T21:50:06.594132+00:00 — cascadeur / import_reference — request

```json
{
  "request_id": "064ce522f4704b89a4256cf4eb12d314",
  "provider": "cascadeur",
  "operation": "import_reference",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:50:06.594132+00:00",
  "event": "request",
  "request": {
    "input": "ai_videos/_research/service_tests/shu_motion_20261013/reference_first5.mp4",
    "fps": 30,
    "frames": 150,
    "local_only": true,
    "plan": "Pro",
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T21:51:24.135929+00:00 — cascadeur / import_reference — error

```json
{
  "request_id": "064ce522f4704b89a4256cf4eb12d314",
  "provider": "cascadeur",
  "operation": "import_reference",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:51:24.135929+00:00",
  "event": "error",
  "response": {
    "message": "VIDEO DECODING ERROR: Could not create frames directory",
    "stage": "导入本地视频",
    "charge": 0
  }
}
```

## 2026-10-12T21:51:49.230360+00:00 — cascadeur / import_reference_retry — request

```json
{
  "request_id": "dd212aba005c42cc96f366c03c491a70",
  "provider": "cascadeur",
  "operation": "import_reference_retry",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:51:49.230360+00:00",
  "event": "request",
  "request": {
    "input": "ai_videos/_research/service_tests/shu_motion_20261013/reference_first5.mp4",
    "frames_parent": "ai_videos/_research/service_tests/shu_motion_20261013",
    "directory_selected_by": "UI folder picker",
    "attempt": 2,
    "local_only": true
  }
}
```

## 2026-10-12T21:53:21.871526+00:00 — cascadeur / import_reference_retry — error

```json
{
  "request_id": "dd212aba005c42cc96f366c03c491a70",
  "provider": "cascadeur",
  "operation": "import_reference_retry",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:53:21.871526+00:00",
  "event": "error",
  "response": {
    "message": "解码停在首帧后程序自行退出；未生成动画；未收费"
  }
}
```

## 2026-10-12T21:53:22.180086+00:00 — cascadeur / relaunch_for_compatible_video — request

```json
{
  "request_id": "cdbf3d3546ed476c98b5c4ae3ab9ee12",
  "provider": "cascadeur",
  "operation": "relaunch_for_compatible_video",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:53:22.180086+00:00",
  "event": "request",
  "request": {
    "message": "上次程序自行退出；重新打开已有软件，准备使用H264 baseline/all-I/no B frames编码；Monthly Pro已核实"
  }
}
```

## 2026-10-12T21:54:07.204656+00:00 — cascadeur / relaunch_for_compatible_video — result

```json
{
  "request_id": "cdbf3d3546ed476c98b5c4ae3ab9ee12",
  "provider": "cascadeur",
  "operation": "relaunch_for_compatible_video",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:54:07.204656+00:00",
  "event": "result",
  "response": {
    "message": "Cascadeur重新打开，Cascy样例已载入"
  }
}
```

## 2026-10-12T21:54:07.413379+00:00 — cascadeur / import_reference_compatible — request

```json
{
  "request_id": "935eea8115ed42eaa3e93ad146d88897",
  "provider": "cascadeur",
  "operation": "import_reference_compatible",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:54:07.413379+00:00",
  "event": "request",
  "request": {
    "message": "输入reference_compatible.mp4；H264 baseline，全I帧，无B帧；前5秒；本地导入；第3次试验"
  }
}
```

## 2026-10-12T21:56:15.495387+00:00 — cascadeur / import_reference_compatible — error

```json
{
  "request_id": "935eea8115ed42eaa3e93ad146d88897",
  "provider": "cascadeur",
  "operation": "import_reference_compatible",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:56:15.495387+00:00",
  "event": "error",
  "response": {
    "message": "更保守编码仍在首帧后无响应，WerFault进程出现；停止重复使用原生视频解码；未生成骨骼动画"
  }
}
```

## 2026-10-12T21:57:00.522346+00:00 — cascadeur / image_sequence_session — request

```json
{
  "request_id": "caae762ee7134afebcbb439a73c12565",
  "provider": "cascadeur",
  "operation": "image_sequence_session",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T21:57:00.522346+00:00",
  "event": "request",
  "request": {
    "message": "改用官方支持的图片序列参考：decoded_frames/000000.jpg至000149.jpg；本地FFmpeg已解码150帧；重新打开Cascadeur并载入Cascy、绑定图片序列；不使用原生视频解码"
  }
}
```

## 2026-10-12T22:04:47.982641+00:00 — cascadeur / image_sequence_session — result

```json
{
  "request_id": "caae762ee7134afebcbb439a73c12565",
  "provider": "cascadeur",
  "operation": "image_sequence_session",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:04:47.982641+00:00",
  "event": "result",
  "response": {
    "message": "已用View > Bind images把000000.jpg至000149.jpg绑定到Plane(0)，参考帧已在场景中显示；原生视频解码问题已绕开；未生成骨骼动画"
  }
}
```

## 2026-10-12T22:04:48.185915+00:00 — cascadeur / mocap_local_trial — request

```json
{
  "request_id": "8daf00885cc347eeb462a7c850e49251",
  "provider": "cascadeur",
  "operation": "mocap_local_trial",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:04:48.185915+00:00",
  "event": "request",
  "request": {
    "message": "输入：Plane(0)绑定的150张图片序列，30fps，源shu.mp4前5秒裁掉顶部220像素；目标Cascy；本地Mocap Alpha；Monthly Pro；用户要求试验；如提示下载模型则另记下载请求，不上传视频"
  }
}
```

## 2026-10-12T22:05:41.852473+00:00 — cascadeur / download_mocap_model — request

```json
{
  "request_id": "6edc1f550def47ecad0813f2520fa351",
  "provider": "cascadeur",
  "operation": "download_mocap_model",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:05:41.852473+00:00",
  "event": "request",
  "request": {
    "message": "Cascadeur原生Mocap首次使用提示需下载787MB模型数据；点击Yes下载官方模型；本地已安装软件组件的数据，非新软件；软件内部HTTP不可逐条观察；用户已授权shu.mp4动作试验；不上传视频"
  }
}
```

## 2026-10-12T22:11:14.890+00:00 — cascadeur / GET /animations/files/17/mocap_010725.pt — request

```json
{
  "request_id": "79013108677d475b963eced36b9bd4dc",
  "provider": "cascadeur",
  "operation": "GET /animations/files/17/mocap_010725.pt",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "pid": 49008,
  "request_fingerprint": "f679d511ff6e5e078e220409c0258a550058f1d654a8c3dead76ff7e66af62a3",
  "time": "2026-10-12T22:11:14.890+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "headers": {
      "Range": "bytes=0-1048575"
    },
    "body": null,
    "timeout_s": 25
  }
}
```

## 2026-10-12T22:11:16.327+00:00 — cascadeur / GET /animations/files/17/mocap_010725.pt — result

```json
{
  "request_id": "79013108677d475b963eced36b9bd4dc",
  "provider": "cascadeur",
  "operation": "GET /animations/files/17/mocap_010725.pt",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "pid": 49008,
  "request_fingerprint": "f679d511ff6e5e078e220409c0258a550058f1d654a8c3dead76ff7e66af62a3",
  "time": "2026-10-12T22:11:16.327+00:00",
  "event": "result",
  "elapsed_s": 1.407,
  "response": [
    {
      "bytes": 1048576,
      "sha256": "e3ca4fa1fa86684e6cab010d785a3d95c1a528b6e870d9b4d7f533aef5357ace"
    },
    {
      "Accept-Ranges": "bytes",
      "Content-Type": "text/plain",
      "ETag": "\"eb71f5e0d9aced549b58a8e182a350fd:1751373004.029022\"",
      "Last-Modified": "Tue, 01 Jul 2025 12:27:32 GMT",
      "Server": "AkamaiNetStorage",
      "Date": "Mon, 12 Oct 2026 22:11:15 GMT",
      "Content-Range": "bytes 0-1048575/825323915",
      "Content-Length": "1048576",
      "Connection": "close",
      "Cache-Control": "public, max-age=86400",
      "Access-Control-Max-Age": "86400",
      "Access-Control-Allow-Credentials": "false",
      "Access-Control-Allow-Headers": "*",
      "Access-Control-Allow-Methods": "GET,POST",
      "Access-Control-Allow-Origin": "*"
    },
    206
  ]
}
```

## 2026-10-12T22:12:44.314025+00:00 — cascadeur / download_mocap_model — result

```json
{
  "request_id": "6edc1f550def47ecad0813f2520fa351",
  "provider": "cascadeur",
  "operation": "download_mocap_model",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:12:44.314025+00:00",
  "event": "result",
  "response": {
    "message": "内置下载速度过慢，已点击Cancel；完整模型尚未落盘；改用安装包内记录的同一官方CDN地址，经RequestLog逐段请求"
  }
}
```

## 2026-10-12T22:12:44.496+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "24b587dcd57e4971b3a920c453d1f4bb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "eaac8b2003a9f50d3215736098a58c2bcfb1e53031a7d1449c2836e1d3392cd5",
  "time": "2026-10-12T22:12:44.496+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=0-8388607",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0000.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.498+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a300753ada1c4cf0accd97684f61b79e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "49d225f8d25399fbfbb784115aaf16f7ee6e3d2237102e3ce5208802927a4d03",
  "time": "2026-10-12T22:12:44.498+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=8388608-16777215",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0001.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.505+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "bdb33423c3bf4184baec9f20ea9d5088",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "e6e2ed652f6896f73c9b7c79e7269d54651d57ea0f45c9833cf61b1f17baf284",
  "time": "2026-10-12T22:12:44.505+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=50331648-58720255",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0006.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.501+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "fc6b8a07ab004ff7b3a02aac7b777a7a",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4db8d883436167395f7562d5e1861df980d4948b01979f21cd2f6b9b247264d5",
  "time": "2026-10-12T22:12:44.501+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=25165824-33554431",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0003.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:46.140+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "24b587dcd57e4971b3a920c453d1f4bb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "eaac8b2003a9f50d3215736098a58c2bcfb1e53031a7d1449c2836e1d3392cd5",
  "time": "2026-10-12T22:12:46.140+00:00",
  "event": "result",
  "elapsed_s": 1.609,
  "response": {
    "http_status": 206,
    "content_range": "bytes 0-8388607/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0000.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "55e5a9331e3b666b002b6c31e2c26573e9c48b9cbbafb90d2d8ff79c9a505fdb"
    }
  }
}
```

## 2026-10-12T22:12:46.150+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "7dc814a477c14d9daeb08e014d7b02b9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "226bd88f4b942424933bd5586395e967e5af23c9dc177777f079e9d08bd808e4",
  "time": "2026-10-12T22:12:46.150+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=67108864-75497471",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0008.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.499+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "2fd07a8fbb2546b79e8e8fe9e98ed16e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "3ea5dfd902fb2f265a1768f8cdc42e61dce8d0a8f201dedf64f362923963e1c2",
  "time": "2026-10-12T22:12:44.499+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=16777216-25165823",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0002.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:46.583+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a300753ada1c4cf0accd97684f61b79e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "49d225f8d25399fbfbb784115aaf16f7ee6e3d2237102e3ce5208802927a4d03",
  "time": "2026-10-12T22:12:46.583+00:00",
  "event": "result",
  "elapsed_s": 2.047,
  "response": {
    "http_status": 206,
    "content_range": "bytes 8388608-16777215/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0001.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "86fdb8df94c6783ac5ec4d7a7cf34df5c48ab8ac36e4430f137ebab3c060f1a1"
    }
  }
}
```

## 2026-10-12T22:12:46.593+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b184e96d53bf4b7d90e77693426a14f3",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "d8eac7454806a22f7e3b37e86f51652ba5e18eb49f82e1a367e55cd0ee82dac4",
  "time": "2026-10-12T22:12:46.593+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=75497472-83886079",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0009.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:47.283+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "fc6b8a07ab004ff7b3a02aac7b777a7a",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4db8d883436167395f7562d5e1861df980d4948b01979f21cd2f6b9b247264d5",
  "time": "2026-10-12T22:12:47.283+00:00",
  "event": "result",
  "elapsed_s": 1.719,
  "response": {
    "http_status": 206,
    "content_range": "bytes 25165824-33554431/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0003.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "2146863f659c3fa7ace104ed936d8ad07e15cdf4467988a192fcac05bbe77959"
    }
  }
}
```

## 2026-10-12T22:12:47.304+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "2b4208d15acb4fdf8c6fd08b3f8c46fd",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "5af51d2bf4809e1607458b472cbffec577c97dfbab729f7362550a1be9cdb2ac",
  "time": "2026-10-12T22:12:47.304+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=83886080-92274687",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0010.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:47.362+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "bdb33423c3bf4184baec9f20ea9d5088",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "e6e2ed652f6896f73c9b7c79e7269d54651d57ea0f45c9833cf61b1f17baf284",
  "time": "2026-10-12T22:12:47.362+00:00",
  "event": "result",
  "elapsed_s": 1.813,
  "response": {
    "http_status": 206,
    "content_range": "bytes 50331648-58720255/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0006.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "bd3bdc6ad5f78aae0cbf73ce5e3b04996bb917415d28e9634d80f11e6b429e81"
    }
  }
}
```

## 2026-10-12T22:12:47.393+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "207a989fe42c48779c1e6b4cf9a977ea",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "09042559107141eda69c1a883012846d5b8321c26c83088880f5f11ef3e54f33",
  "time": "2026-10-12T22:12:47.393+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=92274688-100663295",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0011.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.507+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b461858b1a2b42aa9517fbe678464e4d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4a10ec72201489e77461874157e68af5a8c485537891d87ea3a35243db903161",
  "time": "2026-10-12T22:12:44.507+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=58720256-67108863",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0007.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:48.368+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "2fd07a8fbb2546b79e8e8fe9e98ed16e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "3ea5dfd902fb2f265a1768f8cdc42e61dce8d0a8f201dedf64f362923963e1c2",
  "time": "2026-10-12T22:12:48.368+00:00",
  "event": "result",
  "elapsed_s": 1.829,
  "response": {
    "http_status": 206,
    "content_range": "bytes 16777216-25165823/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0002.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "7526cb3bb2c2e1739cc8e542c3ab276594dc37de8bb3a798b66ef62f695990a8"
    }
  }
}
```

## 2026-10-12T22:12:48.400+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "3be4074d005e45b4a629980a4aff057e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "3eec221875f0384f5745eca80bee1289ca352aa0baae8b69b75164fd2fcf5503",
  "time": "2026-10-12T22:12:48.400+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=100663296-109051903",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0012.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.505+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "7446c3a0c3304c1594f23e6f13237283",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "ace5e23dd704911a397ef30c2b44e0397b1442e11af2339c90c40b90f69df855",
  "time": "2026-10-12T22:12:44.505+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=41943040-50331647",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0005.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:48.649+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b184e96d53bf4b7d90e77693426a14f3",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "d8eac7454806a22f7e3b37e86f51652ba5e18eb49f82e1a367e55cd0ee82dac4",
  "time": "2026-10-12T22:12:48.649+00:00",
  "event": "result",
  "elapsed_s": 2.047,
  "response": {
    "http_status": 206,
    "content_range": "bytes 75497472-83886079/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0009.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "23b19fd7b4ec779a71a5804b456b45e964703ebf42cffa9242208a3182830976"
    }
  }
}
```

## 2026-10-12T22:12:48.689+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "91068c2f2fda419a99fbbbdbb3aac466",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "45bdec524322a30c01af08d660d979d08dc68a890155946201050c219c1d71d3",
  "time": "2026-10-12T22:12:48.689+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=109051904-117440511",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0013.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:48.898+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "7dc814a477c14d9daeb08e014d7b02b9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "226bd88f4b942424933bd5586395e967e5af23c9dc177777f079e9d08bd808e4",
  "time": "2026-10-12T22:12:48.898+00:00",
  "event": "result",
  "elapsed_s": 2.735,
  "response": {
    "http_status": 206,
    "content_range": "bytes 67108864-75497471/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0008.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "98ad24c22346f0a648b439a56dfaa5eb3ea0ef606887abd0d9e2c5482f86a6b3"
    }
  }
}
```

## 2026-10-12T22:12:48.924+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "58899d542b584ab8952c9289c121392c",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "c3d66ef67ee3e8e61f67c2b3c305d2badae3e5878f82550400e8de55d96ca6c7",
  "time": "2026-10-12T22:12:48.924+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=117440512-125829119",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0014.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:49.286+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "2b4208d15acb4fdf8c6fd08b3f8c46fd",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "5af51d2bf4809e1607458b472cbffec577c97dfbab729f7362550a1be9cdb2ac",
  "time": "2026-10-12T22:12:49.286+00:00",
  "event": "result",
  "elapsed_s": 1.984,
  "response": {
    "http_status": 206,
    "content_range": "bytes 83886080-92274687/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0010.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "43e7b65ca6f0d7e4d3cb3028fae3a9e0bb27fe27249d74cc3d517dce61cc278b"
    }
  }
}
```

## 2026-10-12T22:12:49.310+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "2a5f21a632ea4b6990ab9c47884761a6",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "5d0be200ba6e0c813b692e2e37cd0663c9803412f4b49f3bfa7f40ac57e6f500",
  "time": "2026-10-12T22:12:49.310+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=125829120-134217727",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0015.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:49.498+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b461858b1a2b42aa9517fbe678464e4d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4a10ec72201489e77461874157e68af5a8c485537891d87ea3a35243db903161",
  "time": "2026-10-12T22:12:49.498+00:00",
  "event": "result",
  "elapsed_s": 1.954,
  "response": {
    "http_status": 206,
    "content_range": "bytes 58720256-67108863/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0007.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "0332d7073f89891edb2347ab8ddad6b79b054424d0adaa0b645a516b95fc6fad"
    }
  }
}
```

## 2026-10-12T22:12:49.507+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "9cbc50d6a58147108b0d4d3ff29b5f2d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "f5ebb54b0f1d81a390c1eb1a4b91927bc5017ac23f62e4f7764970715f9c14f0",
  "time": "2026-10-12T22:12:49.507+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=134217728-142606335",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0016.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:44.501+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b12db21b6373474db01b94547c46493e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2bbe3aeefcb93becd3b278f3b11e2fbf9a0cc714759d10a3f9e1229cd60099cb",
  "time": "2026-10-12T22:12:44.501+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=33554432-41943039",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0004.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:50.197+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "3be4074d005e45b4a629980a4aff057e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "3eec221875f0384f5745eca80bee1289ca352aa0baae8b69b75164fd2fcf5503",
  "time": "2026-10-12T22:12:50.197+00:00",
  "event": "result",
  "elapsed_s": 1.782,
  "response": {
    "http_status": 206,
    "content_range": "bytes 100663296-109051903/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0012.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "341821befa585f065b9731f2db7407c894f8fe288e7fbf6d2fee312caac5526e"
    }
  }
}
```

## 2026-10-12T22:12:50.225+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b5f739cf1a4240bb857dd2e7f85ff5fe",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "18ecb424f021927aa288db4b2b3fbf4f552130c20cc4b822d7d205883a95b0a2",
  "time": "2026-10-12T22:12:50.225+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=142606336-150994943",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0017.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:49.482+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "207a989fe42c48779c1e6b4cf9a977ea",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "09042559107141eda69c1a883012846d5b8321c26c83088880f5f11ef3e54f33",
  "time": "2026-10-12T22:12:49.482+00:00",
  "event": "result",
  "elapsed_s": 2.063,
  "response": {
    "http_status": 206,
    "content_range": "bytes 92274688-100663295/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0011.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "5966a026ce749493f96221170d23828bde8a4f2b8d694b2a2bf9a0a4063f1d95"
    }
  }
}
```

## 2026-10-12T22:12:50.526+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "4fbdffbec3f44d5c8de405f023ce47ab",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "0f508a19719e53cdbf8f5dbb5a632634af317bbf959ac1bd3c8600c8398b89a6",
  "time": "2026-10-12T22:12:50.526+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=150994944-159383551",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0018.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:50.746+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "7446c3a0c3304c1594f23e6f13237283",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "ace5e23dd704911a397ef30c2b44e0397b1442e11af2339c90c40b90f69df855",
  "time": "2026-10-12T22:12:50.746+00:00",
  "event": "result",
  "elapsed_s": 2.188,
  "response": {
    "http_status": 206,
    "content_range": "bytes 41943040-50331647/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0005.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "bd7b7bb91215697f0b0c62812be932e019b1bbff2553ce72e111359b58d0035c"
    }
  }
}
```

## 2026-10-12T22:12:50.776+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "49919ac3135b4fbda65b5e68166b3d82",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4e9c7df7656612d61c0d6ac321a75ab804de2837683c813d5c5b5b340dd7954a",
  "time": "2026-10-12T22:12:50.776+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=159383552-167772159",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0019.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:51.324+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "58899d542b584ab8952c9289c121392c",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "c3d66ef67ee3e8e61f67c2b3c305d2badae3e5878f82550400e8de55d96ca6c7",
  "time": "2026-10-12T22:12:51.324+00:00",
  "event": "result",
  "elapsed_s": 2.375,
  "response": {
    "http_status": 206,
    "content_range": "bytes 117440512-125829119/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0014.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "3e6620aa8547cd70f63d2ec88e247374507f82a2929ea722a0a1c2fa86497e58"
    }
  }
}
```

## 2026-10-12T22:12:51.353+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "1a8d7fdbd81741578d4bc2bd9d159f96",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "e4d77b27a6dc8f877fea8c90f929c4cc52d82e995a75f7a113f76f0c32f09688",
  "time": "2026-10-12T22:12:51.353+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=167772160-176160767",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0020.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:50.766+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "91068c2f2fda419a99fbbbdbb3aac466",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "45bdec524322a30c01af08d660d979d08dc68a890155946201050c219c1d71d3",
  "time": "2026-10-12T22:12:50.766+00:00",
  "event": "result",
  "elapsed_s": 2.047,
  "response": {
    "http_status": 206,
    "content_range": "bytes 109051904-117440511/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0013.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "b20c0b287a51ba10c665b7b8a3701243ffc75f208b7fa92f8637819614ea0e2c"
    }
  }
}
```

## 2026-10-12T22:12:51.795+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "7a5f114ece824af7824ff5ed21d47839",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "65eabd3c347522882f54ba1c0768187978af9fb09d908bca12dc0e5ba686410e",
  "time": "2026-10-12T22:12:51.795+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=176160768-184549375",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0021.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:52.023+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "9cbc50d6a58147108b0d4d3ff29b5f2d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "f5ebb54b0f1d81a390c1eb1a4b91927bc5017ac23f62e4f7764970715f9c14f0",
  "time": "2026-10-12T22:12:52.023+00:00",
  "event": "result",
  "elapsed_s": 2.5,
  "response": {
    "http_status": 206,
    "content_range": "bytes 134217728-142606335/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0016.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "fe9b0acdc7dbc83c09058502f3f220b265a5f797b25b02498b49ebbb13aa5968"
    }
  }
}
```

## 2026-10-12T22:12:52.061+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0241931e54a74cdc943d5b62c3505016",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2acd17c3b4b7c6d35147e8fbbb6ee5c5619141e63eec12b9644812f10bebbd2e",
  "time": "2026-10-12T22:12:52.061+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=184549376-192937983",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0022.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:52.270+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "2a5f21a632ea4b6990ab9c47884761a6",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "5d0be200ba6e0c813b692e2e37cd0663c9803412f4b49f3bfa7f40ac57e6f500",
  "time": "2026-10-12T22:12:52.270+00:00",
  "event": "result",
  "elapsed_s": 2.938,
  "response": {
    "http_status": 206,
    "content_range": "bytes 125829120-134217727/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0015.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "8eef4dd80fdc678a3c4d125625885bd1adaddb151284ae14cfe22d3f7eb06805"
    }
  }
}
```

## 2026-10-12T22:12:52.305+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "6c9372fe1ab8404cb4ba1ea797d93306",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2f17d82d1884cec5346dd94e5340ff3e52dc697d7ca77c06c4b62063d6bfef8b",
  "time": "2026-10-12T22:12:52.305+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=192937984-201326591",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0023.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:52.430+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b12db21b6373474db01b94547c46493e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2bbe3aeefcb93becd3b278f3b11e2fbf9a0cc714759d10a3f9e1229cd60099cb",
  "time": "2026-10-12T22:12:52.430+00:00",
  "event": "result",
  "elapsed_s": 2.859,
  "response": {
    "http_status": 206,
    "content_range": "bytes 33554432-41943039/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0004.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "e6251ddb48bb2dabb037667422c97095e4fbc7decf1b2398dc411ee44bc5b793"
    }
  }
}
```

## 2026-10-12T22:12:52.471+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "c6a1098115a341e8ad775095e2f490f7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "94c3cd5085cb37d6c8c6daf09ba9609ffc6104240f51b44e864d1292d97a2df0",
  "time": "2026-10-12T22:12:52.471+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=201326592-209715199",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0024.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:12:52.911+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "49919ac3135b4fbda65b5e68166b3d82",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "4e9c7df7656612d61c0d6ac321a75ab804de2837683c813d5c5b5b340dd7954a",
  "time": "2026-10-12T22:12:52.911+00:00",
  "event": "result",
  "elapsed_s": 2.125,
  "response": {
    "http_status": 206,
    "content_range": "bytes 159383552-167772159/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0019.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "77352a66a2a62cb2dd0fc5c77fd1a2af54d8cb0e2d86efbf504e3acc708a3f3d"
    }
  }
}
```

## 2026-10-12T22:12:53.212+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b5f739cf1a4240bb857dd2e7f85ff5fe",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "18ecb424f021927aa288db4b2b3fbf4f552130c20cc4b822d7d205883a95b0a2",
  "time": "2026-10-12T22:12:53.212+00:00",
  "event": "result",
  "elapsed_s": 2.968,
  "response": {
    "http_status": 206,
    "content_range": "bytes 142606336-150994943/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0017.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "5db5305b47f4e71bcd32ba580481db1736a2e4e9565e151dc3fefceacf1fa68a"
    }
  }
}
```

## 2026-10-12T22:12:53.417+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "1a8d7fdbd81741578d4bc2bd9d159f96",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "e4d77b27a6dc8f877fea8c90f929c4cc52d82e995a75f7a113f76f0c32f09688",
  "time": "2026-10-12T22:12:53.417+00:00",
  "event": "result",
  "elapsed_s": 2.046,
  "response": {
    "http_status": 206,
    "content_range": "bytes 167772160-176160767/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0020.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "b5f9d1e6fa17f1f63a3ab6c79496a6818262edab6f8183d63912015580c7f071"
    }
  }
}
```

## 2026-10-12T22:12:53.648+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "4fbdffbec3f44d5c8de405f023ce47ab",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "0f508a19719e53cdbf8f5dbb5a632634af317bbf959ac1bd3c8600c8398b89a6",
  "time": "2026-10-12T22:12:53.648+00:00",
  "event": "result",
  "elapsed_s": 3.11,
  "response": {
    "http_status": 206,
    "content_range": "bytes 150994944-159383551/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0018.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "299ba176f983854d5eb47c62a331078c3e9193ab1cfcff1cf90198d1fb0c525d"
    }
  }
}
```

## 2026-10-12T22:12:54.249+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "7a5f114ece824af7824ff5ed21d47839",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "65eabd3c347522882f54ba1c0768187978af9fb09d908bca12dc0e5ba686410e",
  "time": "2026-10-12T22:12:54.249+00:00",
  "event": "result",
  "elapsed_s": 2.422,
  "response": {
    "http_status": 206,
    "content_range": "bytes 176160768-184549375/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0021.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "fa0d90dcad8dc3aabc74b527cf46b55621373ed14badb1374e9288034ba27d0d"
    }
  }
}
```

## 2026-10-12T22:12:54.434+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0241931e54a74cdc943d5b62c3505016",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2acd17c3b4b7c6d35147e8fbbb6ee5c5619141e63eec12b9644812f10bebbd2e",
  "time": "2026-10-12T22:12:54.434+00:00",
  "event": "result",
  "elapsed_s": 2.344,
  "response": {
    "http_status": 206,
    "content_range": "bytes 184549376-192937983/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0022.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a29045c13952907b281177ef4c82ddd2ab20ed9a9e6c767074dfc7c274e86e27"
    }
  }
}
```

## 2026-10-12T22:12:55.027+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "6c9372fe1ab8404cb4ba1ea797d93306",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "2f17d82d1884cec5346dd94e5340ff3e52dc697d7ca77c06c4b62063d6bfef8b",
  "time": "2026-10-12T22:12:55.027+00:00",
  "event": "result",
  "elapsed_s": 2.703,
  "response": {
    "http_status": 206,
    "content_range": "bytes 192937984-201326591/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0023.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "362583ee0347aa8002c6a54aa13d1516a05b1f69c08178ce3f847517f4cdb6a5"
    }
  }
}
```

## 2026-10-12T22:12:55.282+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "c6a1098115a341e8ad775095e2f490f7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 46976,
  "request_fingerprint": "94c3cd5085cb37d6c8c6daf09ba9609ffc6104240f51b44e864d1292d97a2df0",
  "time": "2026-10-12T22:12:55.282+00:00",
  "event": "result",
  "elapsed_s": 2.781,
  "response": {
    "http_status": 206,
    "content_range": "bytes 201326592-209715199/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0024.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "97aa9846060a9376164fb0fea629f5d6d55e595408c6692779f877cdd1af1bb2"
    }
  }
}
```

## 2026-10-12T22:14:19.278+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "38b5f4230c204516b88fe4812c2fe426",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a170baca3f0b58598975279bd0948908e194664e9c360c08346e1f93d4f46c7a",
  "time": "2026-10-12T22:14:19.278+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=218103808-226492415",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0026.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.281+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "26c2cdbd617844988f1cf0eabcc835ea",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "08d77921b55390075c3d9bec6f932f8d6903d278d775507f269137bc3e4044e9",
  "time": "2026-10-12T22:14:19.281+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=260046848-268435455",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0031.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.279+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "cbd40efdbd4541fb878c476a7c705ed0",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "baad0eb301c937ca6f609460e117b220f1c61ae0c035cd5eb3da031d4afc278f",
  "time": "2026-10-12T22:14:19.279+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=226492416-234881023",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0027.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.280+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "f8e50032dd1f4e59a17a3c34af7c5bd7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9eb63233ab26513374d49292971c14800ff2e6da7a3707421c4caea3c1ba34b6",
  "time": "2026-10-12T22:14:19.280+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=251658240-260046847",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0030.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:20.896+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "26c2cdbd617844988f1cf0eabcc835ea",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "08d77921b55390075c3d9bec6f932f8d6903d278d775507f269137bc3e4044e9",
  "time": "2026-10-12T22:14:20.896+00:00",
  "event": "result",
  "elapsed_s": 1.578,
  "response": {
    "http_status": 206,
    "content_range": "bytes 260046848-268435455/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0031.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "96568c3c1c622003d648473d3d1d7bb4b1ddb0f4e64f20fcfd83612b0279f093"
    }
  }
}
```

## 2026-10-12T22:14:20.909+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "9174b36cf88848ae8723db5b7c7e9907",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b1e804edf8577c2de184fee3bb2c4c3f95138b5bc3255bc5736acea28a54b942",
  "time": "2026-10-12T22:14:20.909+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=276824064-285212671",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0033.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:20.971+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "38b5f4230c204516b88fe4812c2fe426",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a170baca3f0b58598975279bd0948908e194664e9c360c08346e1f93d4f46c7a",
  "time": "2026-10-12T22:14:20.971+00:00",
  "event": "result",
  "elapsed_s": 1.656,
  "response": {
    "http_status": 206,
    "content_range": "bytes 218103808-226492415/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0026.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "04da8e9f9120e241e12a2fe9e36900c7cd01209f8d46f44f898d77cdc8c96297"
    }
  }
}
```

## 2026-10-12T22:14:20.989+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "70392036f051440c8dec993a2be0a46a",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dc1390c8f560eb65a64c0ed0f5daaa7396896d38a676aaa5b08531c4c6b03790",
  "time": "2026-10-12T22:14:20.989+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=285212672-293601279",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0034.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.278+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "36b35befd1c142728a9d589cfd9e2de7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0480fd0ce070fd2841a0ac7534c186def3f76a661e8fef191e226992e0ccc95f",
  "time": "2026-10-12T22:14:19.278+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=209715200-218103807",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0025.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:22.137+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "cbd40efdbd4541fb878c476a7c705ed0",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "baad0eb301c937ca6f609460e117b220f1c61ae0c035cd5eb3da031d4afc278f",
  "time": "2026-10-12T22:14:22.137+00:00",
  "event": "result",
  "elapsed_s": 1.828,
  "response": {
    "http_status": 206,
    "content_range": "bytes 226492416-234881023/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0027.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "8773672aaf3c28143f637473f65e29beb371d17e57c45bd2d5e513d00420176b"
    }
  }
}
```

## 2026-10-12T22:14:22.158+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "5e4ad06d83e94c27ada63805b6743364",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2455754e19e508944fcdce60f7d625239330fff6dee1b33eb63b1e20d541ceed",
  "time": "2026-10-12T22:14:22.158+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=293601280-301989887",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0035.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:22.286+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "f8e50032dd1f4e59a17a3c34af7c5bd7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9eb63233ab26513374d49292971c14800ff2e6da7a3707421c4caea3c1ba34b6",
  "time": "2026-10-12T22:14:22.286+00:00",
  "event": "result",
  "elapsed_s": 1.953,
  "response": {
    "http_status": 206,
    "content_range": "bytes 251658240-260046847/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0030.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "af93c6b6a9107dc41cbf02319a9d6161ec96ff2cfc6e5a741b40722e154f6f51"
    }
  }
}
```

## 2026-10-12T22:14:22.321+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b9ce6cbbb3784a9897a33153456fe75b",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "ecca66ee33769ffeab3e71f8831d330df94745bac39169fd2eada07cfade9652",
  "time": "2026-10-12T22:14:22.321+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=301989888-310378495",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0036.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.282+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "851e9b82f77d4452911662402012da59",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "fdab687038b97b77a8376e6e1afd65c2463c7ebb2767b5dd232b851975c41eb0",
  "time": "2026-10-12T22:14:19.282+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=243269632-251658239",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0029.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:23.292+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "9174b36cf88848ae8723db5b7c7e9907",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b1e804edf8577c2de184fee3bb2c4c3f95138b5bc3255bc5736acea28a54b942",
  "time": "2026-10-12T22:14:23.292+00:00",
  "event": "result",
  "elapsed_s": 2.359,
  "response": {
    "http_status": 206,
    "content_range": "bytes 276824064-285212671/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0033.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "f22ae7504b2e30acc888b759fe21e8acc19b3c962bf3c026d02c0442d5288dbc"
    }
  }
}
```

## 2026-10-12T22:14:23.323+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "cd4476a44d5c48118a1327b4ad1c5df7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e15b971a2a2e12138a56dc739b485bc5abca6a1a2ed6d35ac8841203f3a4bf25",
  "time": "2026-10-12T22:14:23.323+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=310378496-318767103",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0037.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:19.281+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "69fd0674b2ee4412bae361a516e46f23",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "6fd5e3ed8feda01fcd9d29222d9a99263c7ba8a5e8088063190660a937e3408f",
  "time": "2026-10-12T22:14:19.281+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=234881024-243269631",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0028.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:23.285+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "36b35befd1c142728a9d589cfd9e2de7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0480fd0ce070fd2841a0ac7534c186def3f76a661e8fef191e226992e0ccc95f",
  "time": "2026-10-12T22:14:23.285+00:00",
  "event": "result",
  "elapsed_s": 1.937,
  "response": {
    "http_status": 206,
    "content_range": "bytes 209715200-218103807/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0025.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "75f057552ea96712184cf70adf295d0c7dc11f5030b38aa7eff92560070d91fa"
    }
  }
}
```

## 2026-10-12T22:14:19.283+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "87a95aabf5c04b4cb24ee3c0727ba296",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2eccad15aa616b0876fdbd782d71f59792077e4b9dcf0224db0e046f8aa945d8",
  "time": "2026-10-12T22:14:19.283+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=268435456-276824063",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0032.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:24.338+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b247ec0a8f8843b6bde3d62cda19117d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "8cd712f5bfe69b4df36e47fb5bcc7a0a19dc40e6d422e2a8020590c8d3d3ba2b",
  "time": "2026-10-12T22:14:24.338+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=318767104-327155711",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0038.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:24.844+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "5e4ad06d83e94c27ada63805b6743364",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2455754e19e508944fcdce60f7d625239330fff6dee1b33eb63b1e20d541ceed",
  "time": "2026-10-12T22:14:24.844+00:00",
  "event": "result",
  "elapsed_s": 2.672,
  "response": {
    "http_status": 206,
    "content_range": "bytes 293601280-301989887/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0035.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "856ccd186dc6826d32badd2d71471b46e482059ae8e1f6d30cbdd53ff7e79005"
    }
  }
}
```

## 2026-10-12T22:14:24.871+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "ac1b1b658dcd44b59b79e384cb2a1cb6",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9bd1618e2b9acbc33b5f7c82b7b8a1787f279784e2f9f0245fca51ee3560ac47",
  "time": "2026-10-12T22:14:24.871+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=327155712-335544319",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0039.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:24.995+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "851e9b82f77d4452911662402012da59",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "fdab687038b97b77a8376e6e1afd65c2463c7ebb2767b5dd232b851975c41eb0",
  "time": "2026-10-12T22:14:24.995+00:00",
  "event": "result",
  "elapsed_s": 2.61,
  "response": {
    "http_status": 206,
    "content_range": "bytes 243269632-251658239/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0029.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "4900a77e10173f35640c11f5a0727b2200dbbc5c2c11eb6c7ac2401fc95e1ad2"
    }
  }
}
```

## 2026-10-12T22:14:25.013+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "4000b077115b4940861485a37ff8364e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "1c3634e4414d7e34aef43b9d3c4cbf02f6ec6c5da792a586cb60909051ded2c1",
  "time": "2026-10-12T22:14:25.013+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=335544320-343932927",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0040.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:23.290+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "70392036f051440c8dec993a2be0a46a",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dc1390c8f560eb65a64c0ed0f5daaa7396896d38a676aaa5b08531c4c6b03790",
  "time": "2026-10-12T22:14:23.290+00:00",
  "event": "result",
  "elapsed_s": 2.281,
  "response": {
    "http_status": 206,
    "content_range": "bytes 285212672-293601279/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0034.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "d2e2336e800a761a9ab806014491d566ee26ae682c31c60e9a0fd1bb60c05b97"
    }
  }
}
```

## 2026-10-12T22:14:25.341+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a8450f1821734db0b63cb5fb40766b12",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e0ca36b80ebd0ac74135949325653f1229db17ad16eecd7b3eab9dce28434b3b",
  "time": "2026-10-12T22:14:25.341+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=343932928-352321535",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0041.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:24.998+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b9ce6cbbb3784a9897a33153456fe75b",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "ecca66ee33769ffeab3e71f8831d330df94745bac39169fd2eada07cfade9652",
  "time": "2026-10-12T22:14:24.998+00:00",
  "event": "result",
  "elapsed_s": 2.657,
  "response": {
    "http_status": 206,
    "content_range": "bytes 301989888-310378495/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0036.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "11f237d74beb00eeae030b15226dca475002099ffbc3972e5c6a7419ad2d09b8"
    }
  }
}
```

## 2026-10-12T22:14:26.025+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "e6a238128c1e468c8823838bce6372d8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "156d84d62b2b1b5b1e42758faeb07bb01f011af393d72d84ded5d53694337b38",
  "time": "2026-10-12T22:14:26.025+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=352321536-360710143",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0042.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:26.379+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "87a95aabf5c04b4cb24ee3c0727ba296",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2eccad15aa616b0876fdbd782d71f59792077e4b9dcf0224db0e046f8aa945d8",
  "time": "2026-10-12T22:14:26.379+00:00",
  "event": "result",
  "elapsed_s": 2.015,
  "response": {
    "http_status": 206,
    "content_range": "bytes 268435456-276824063/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0032.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "91c07cb3569d58bd917de5a5ca0c71f5312d25c891067bc35220beaa727a067f"
    }
  }
}
```

## 2026-10-12T22:14:26.415+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "c9fdf82ca2ac4963b5e331fec6d26a82",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e20dd57b552fd73d68bade4c93542b9820f443ff9a1a7df932c86ca68c9640f0",
  "time": "2026-10-12T22:14:26.415+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=360710144-369098751",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0043.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:26.772+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "ac1b1b658dcd44b59b79e384cb2a1cb6",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9bd1618e2b9acbc33b5f7c82b7b8a1787f279784e2f9f0245fca51ee3560ac47",
  "time": "2026-10-12T22:14:26.772+00:00",
  "event": "result",
  "elapsed_s": 1.891,
  "response": {
    "http_status": 206,
    "content_range": "bytes 327155712-335544319/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0039.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "84d5b5d8ec607aeaab0dda32c4f5800fc8f31a3a8c4aaf9dbc372186794582ed"
    }
  }
}
```

## 2026-10-12T22:14:26.805+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "7ae602c0d43d4c009aeefbf0d3ffdf84",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "274e03f3f5038141afac017a664ea81d2433597f69c45d6b58320c41c85b870c",
  "time": "2026-10-12T22:14:26.805+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=369098752-377487359",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0044.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:26.937+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "cd4476a44d5c48118a1327b4ad1c5df7",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e15b971a2a2e12138a56dc739b485bc5abca6a1a2ed6d35ac8841203f3a4bf25",
  "time": "2026-10-12T22:14:26.937+00:00",
  "event": "result",
  "elapsed_s": 3.594,
  "response": {
    "http_status": 206,
    "content_range": "bytes 310378496-318767103/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0037.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "f0bb28e474ddeaa1f759fbd8976cd0799fed8c126b8515473e6b210b19c37701"
    }
  }
}
```

## 2026-10-12T22:14:26.972+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "1a177d24500f4eac946cb7767ecb484b",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "71da2628a98b4d3251d79d86d06a1931a6298464a9eaf50a834744ca3800738b",
  "time": "2026-10-12T22:14:26.972+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=377487360-385875967",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0045.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:27.407+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "4000b077115b4940861485a37ff8364e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "1c3634e4414d7e34aef43b9d3c4cbf02f6ec6c5da792a586cb60909051ded2c1",
  "time": "2026-10-12T22:14:27.407+00:00",
  "event": "result",
  "elapsed_s": 2.375,
  "response": {
    "http_status": 206,
    "content_range": "bytes 335544320-343932927/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0040.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "3bec5188a09076b73d681a43ab9b9fe2b3efbefefe67d67553b02af68a40a5c2"
    }
  }
}
```

## 2026-10-12T22:14:27.438+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "abfe040d6aec44829e95d2847f936eb2",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a8c1f0e5dfc6a264623603ba0623e93b9f75cad77fda6a31efebb0000f6d09bd",
  "time": "2026-10-12T22:14:27.438+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=385875968-394264575",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0046.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:26.786+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "69fd0674b2ee4412bae361a516e46f23",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "6fd5e3ed8feda01fcd9d29222d9a99263c7ba8a5e8088063190660a937e3408f",
  "time": "2026-10-12T22:14:26.786+00:00",
  "event": "result",
  "elapsed_s": 3.406,
  "response": {
    "http_status": 206,
    "content_range": "bytes 234881024-243269631/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0028.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "c51e4329fafbe7cf02d59904a7ed3ef870681cc0549ae873e78ee07a675d2cf4"
    }
  }
}
```

## 2026-10-12T22:14:27.809+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "c108bb05cfa74c2d9acf99d9c7902418",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "741d87da9698d0bc40b6ac3242495df3a166526ddc20bcc37715b4b595b27f79",
  "time": "2026-10-12T22:14:27.809+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=394264576-402653183",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0047.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:28.036+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a8450f1821734db0b63cb5fb40766b12",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e0ca36b80ebd0ac74135949325653f1229db17ad16eecd7b3eab9dce28434b3b",
  "time": "2026-10-12T22:14:28.036+00:00",
  "event": "result",
  "elapsed_s": 2.656,
  "response": {
    "http_status": 206,
    "content_range": "bytes 343932928-352321535/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0041.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "299dbfa560a0bf3cc6cc26be83cd5cb2793f1a1859173fbadf4394890166c3f1"
    }
  }
}
```

## 2026-10-12T22:14:28.055+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "4c46b92560d44063b79e413e42ad09c5",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f10bd9a5cb5d82031890f9b45b0341f973b7549690c67338280eac3086a30db5",
  "time": "2026-10-12T22:14:28.055+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=402653184-411041791",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0048.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:29.017+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "7ae602c0d43d4c009aeefbf0d3ffdf84",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "274e03f3f5038141afac017a664ea81d2433597f69c45d6b58320c41c85b870c",
  "time": "2026-10-12T22:14:29.017+00:00",
  "event": "result",
  "elapsed_s": 2.187,
  "response": {
    "http_status": 206,
    "content_range": "bytes 369098752-377487359/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0044.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "fea155e1faca72ebb34d23e28bc69a83aca54d03ab9e46959a492b544aea1bf7"
    }
  }
}
```

## 2026-10-12T22:14:29.046+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "8bc4923a3b1d40c1a498c074b9cc92c9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "d686d21cd7f2fac24c9bb49f33954cb51066df3d99fe56d98a48c165998b71ec",
  "time": "2026-10-12T22:14:29.046+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=411041792-419430399",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0049.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:28.050+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "e6a238128c1e468c8823838bce6372d8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "156d84d62b2b1b5b1e42758faeb07bb01f011af393d72d84ded5d53694337b38",
  "time": "2026-10-12T22:14:28.050+00:00",
  "event": "result",
  "elapsed_s": 1.984,
  "response": {
    "http_status": 206,
    "content_range": "bytes 352321536-360710143/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0042.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a4d2ea6b6f557e8a8bbf81ec456dfa87b8614d2a5e33bea58f1eb657cd4df39f"
    }
  }
}
```

## 2026-10-12T22:14:29.114+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0f5f89b5f1cd48a7923a1c296cda1419",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "4e03a983872fbd221f438e9c5e719eda0a9119c56a1e8e6c7137e85c428ef991",
  "time": "2026-10-12T22:14:29.114+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=419430400-427819007",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0050.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:29.194+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "c9fdf82ca2ac4963b5e331fec6d26a82",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e20dd57b552fd73d68bade4c93542b9820f443ff9a1a7df932c86ca68c9640f0",
  "time": "2026-10-12T22:14:29.194+00:00",
  "event": "result",
  "elapsed_s": 2.766,
  "response": {
    "http_status": 206,
    "content_range": "bytes 360710144-369098751/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0043.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "69cbfa5b3d492660f0538fc4d14743274cc27181921988b445ee9cdf0657fcca"
    }
  }
}
```

## 2026-10-12T22:14:29.213+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b3645b2bade14cfe9c3db4c210f67b91",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e962a042088008eaac13d016fe3fccfbf657c753fcae2ce3ef96e231c70de042",
  "time": "2026-10-12T22:14:29.213+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=427819008-436207615",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0051.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:29.468+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "1a177d24500f4eac946cb7767ecb484b",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "71da2628a98b4d3251d79d86d06a1931a6298464a9eaf50a834744ca3800738b",
  "time": "2026-10-12T22:14:29.468+00:00",
  "event": "result",
  "elapsed_s": 2.468,
  "response": {
    "http_status": 206,
    "content_range": "bytes 377487360-385875967/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0045.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "787a637080416b62613917f877576ecc2f4ef0832822e7e63bac5f58a0de120e"
    }
  }
}
```

## 2026-10-12T22:14:29.497+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "c74ffe8448fc4e6a89e276260f2d2921",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "5c768a458239300269b403d16186345a67bbbeeddc65872b5261d2fc49519f3b",
  "time": "2026-10-12T22:14:29.497+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=436207616-444596223",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0052.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:29.880+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "abfe040d6aec44829e95d2847f936eb2",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a8c1f0e5dfc6a264623603ba0623e93b9f75cad77fda6a31efebb0000f6d09bd",
  "time": "2026-10-12T22:14:29.880+00:00",
  "event": "result",
  "elapsed_s": 2.437,
  "response": {
    "http_status": 206,
    "content_range": "bytes 385875968-394264575/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0046.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "1fd74ddcbfbfc09e6ac9d5d6b787ed730616203a49dac24866ddce0dd6180981"
    }
  }
}
```

## 2026-10-12T22:14:29.921+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "6ec28086b64e4832a6db0f6060af344c",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bce0d68e930d9ce0d7bae87c7d4d7053233c665e3f981c4f0b3a89f86f055f77",
  "time": "2026-10-12T22:14:29.921+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=444596224-452984831",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0053.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:30.202+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "4c46b92560d44063b79e413e42ad09c5",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f10bd9a5cb5d82031890f9b45b0341f973b7549690c67338280eac3086a30db5",
  "time": "2026-10-12T22:14:30.202+00:00",
  "event": "result",
  "elapsed_s": 2.125,
  "response": {
    "http_status": 206,
    "content_range": "bytes 402653184-411041791/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0048.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "99e7bdd9e1b7c134cdd1f439b94c5717b910d53e9fc0665a5704f175d926ee05"
    }
  }
}
```

## 2026-10-12T22:14:30.229+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "fe5cd59fc90f4e9a91cf752089d3d2c3",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dcfb6c65dc1e8c017bdbfab24c345ce85aab086d5e7bb214064decaecae36466",
  "time": "2026-10-12T22:14:30.229+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=452984832-461373439",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0054.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:30.314+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "c108bb05cfa74c2d9acf99d9c7902418",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "741d87da9698d0bc40b6ac3242495df3a166526ddc20bcc37715b4b595b27f79",
  "time": "2026-10-12T22:14:30.314+00:00",
  "event": "result",
  "elapsed_s": 2.469,
  "response": {
    "http_status": 206,
    "content_range": "bytes 394264576-402653183/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0047.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "e01999e6ee53161144bd827e570b3dd48db872cd7f70044a3d59a7d0607939b7"
    }
  }
}
```

## 2026-10-12T22:14:30.342+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "ea019b5155084ae7adf518de88ce1da8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dae2b8cdeafb6fee3bfbbf42624ed0a93897406bdc0ed1e697c2834640f47792",
  "time": "2026-10-12T22:14:30.342+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=461373440-469762047",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0055.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:31.045+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "8bc4923a3b1d40c1a498c074b9cc92c9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "d686d21cd7f2fac24c9bb49f33954cb51066df3d99fe56d98a48c165998b71ec",
  "time": "2026-10-12T22:14:31.045+00:00",
  "event": "result",
  "elapsed_s": 1.968,
  "response": {
    "http_status": 206,
    "content_range": "bytes 411041792-419430399/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0049.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "67f6cb10765e6b2c0ccf8d020dccdbbbccb413461ba08165a0b34abe0bd8b48e"
    }
  }
}
```

## 2026-10-12T22:14:31.078+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0eebf8e502914aba87d65cba10c9fc57",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0254013373a1d9f684f33ec23fe38055002a8c1c28f4d09384ddc32f0c5805ec",
  "time": "2026-10-12T22:14:31.078+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=469762048-478150655",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0056.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:31.405+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b3645b2bade14cfe9c3db4c210f67b91",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "e962a042088008eaac13d016fe3fccfbf657c753fcae2ce3ef96e231c70de042",
  "time": "2026-10-12T22:14:31.405+00:00",
  "event": "result",
  "elapsed_s": 2.172,
  "response": {
    "http_status": 206,
    "content_range": "bytes 427819008-436207615/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0051.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a16c7ef0b2712c2a100e75b114f6bf97d9f1c69db16ecaf1b21910153e1eaf47"
    }
  }
}
```

## 2026-10-12T22:14:31.430+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "76e0e94e04264276994bc740ebd89970",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b7e9207d86d6feb3e2822c8425cad505f888140fac6548e4f85145d7d3b4246a",
  "time": "2026-10-12T22:14:31.430+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=478150656-486539263",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0057.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:31.529+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0f5f89b5f1cd48a7923a1c296cda1419",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "4e03a983872fbd221f438e9c5e719eda0a9119c56a1e8e6c7137e85c428ef991",
  "time": "2026-10-12T22:14:31.529+00:00",
  "event": "result",
  "elapsed_s": 2.391,
  "response": {
    "http_status": 206,
    "content_range": "bytes 419430400-427819007/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0050.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "99ade238891e848cdeb76a4ddbb9179a8dfb773972bff5c37f7b4430a9a7c1a3"
    }
  }
}
```

## 2026-10-12T22:14:31.562+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "4dc6f7abd03444b3b5409476da22b8dd",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b1c42842e5fbe9172b8f35649866e05017574ab53785048fb14bffa3ee502e07",
  "time": "2026-10-12T22:14:31.562+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=486539264-494927871",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0058.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:31.924+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b247ec0a8f8843b6bde3d62cda19117d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "8cd712f5bfe69b4df36e47fb5bcc7a0a19dc40e6d422e2a8020590c8d3d3ba2b",
  "time": "2026-10-12T22:14:31.924+00:00",
  "event": "result",
  "elapsed_s": 7.531,
  "response": {
    "http_status": 206,
    "content_range": "bytes 318767104-327155711/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0038.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "f90cf19c6f5e5a9b6c81b64c80c328605e5251baf9985f1e478eaf1d4aa06773"
    }
  }
}
```

## 2026-10-12T22:14:31.957+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "71ed2ea52f224c7f9dd9854b9377ac83",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "34ad122566b3af3a78aa8b56119bf69291ab964fd37ba6d91026f5213934dd85",
  "time": "2026-10-12T22:14:31.957+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=494927872-503316479",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0059.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:32.146+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "c74ffe8448fc4e6a89e276260f2d2921",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "5c768a458239300269b403d16186345a67bbbeeddc65872b5261d2fc49519f3b",
  "time": "2026-10-12T22:14:32.146+00:00",
  "event": "result",
  "elapsed_s": 2.625,
  "response": {
    "http_status": 206,
    "content_range": "bytes 436207616-444596223/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0052.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "3c7104b05a8fb83afa2d8fef367426235ea9612bf3279fea10d8db8fb5d8b737"
    }
  }
}
```

## 2026-10-12T22:14:32.172+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b55cd60cdcc9433b92bda63e720f06d9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c03ed66557befd1d58d160fc0d0e7a8882842eb232097d91146bcf1150f23653",
  "time": "2026-10-12T22:14:32.172+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=503316480-511705087",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0060.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:32.585+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "6ec28086b64e4832a6db0f6060af344c",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bce0d68e930d9ce0d7bae87c7d4d7053233c665e3f981c4f0b3a89f86f055f77",
  "time": "2026-10-12T22:14:32.585+00:00",
  "event": "result",
  "elapsed_s": 2.64,
  "response": {
    "http_status": 206,
    "content_range": "bytes 444596224-452984831/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0053.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "7de6e83503673f3ef3181571ea638acb3ac3048dc26845c467d919ace53be685"
    }
  }
}
```

## 2026-10-12T22:14:32.617+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "e1e12c07b3d74c279c2b5bf26651c583",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bd8d54bd1a3b3456ed4cded6acf0a9500789da3bc9788f3dfba0c09c24e6706a",
  "time": "2026-10-12T22:14:32.617+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=511705088-520093695",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0061.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:32.765+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "ea019b5155084ae7adf518de88ce1da8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dae2b8cdeafb6fee3bfbbf42624ed0a93897406bdc0ed1e697c2834640f47792",
  "time": "2026-10-12T22:14:32.765+00:00",
  "event": "result",
  "elapsed_s": 2.406,
  "response": {
    "http_status": 206,
    "content_range": "bytes 461373440-469762047/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0055.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "39c6c8e8243f6ece6d8edc0a2c00595ddbc92d4963b632461b218d5702ab6c7e"
    }
  }
}
```

## 2026-10-12T22:14:32.802+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "2b04fde4dd45486c80500ef3bcc5490f",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "3b4dccf9d9a2f54a9b1b513571438b5d8e469f9673ce6dd9dc3b0aa187624f1a",
  "time": "2026-10-12T22:14:32.802+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=520093696-528482303",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0062.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:33.173+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0eebf8e502914aba87d65cba10c9fc57",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0254013373a1d9f684f33ec23fe38055002a8c1c28f4d09384ddc32f0c5805ec",
  "time": "2026-10-12T22:14:33.173+00:00",
  "event": "result",
  "elapsed_s": 2.062,
  "response": {
    "http_status": 206,
    "content_range": "bytes 469762048-478150655/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0056.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "7d8b6ecbe446953877a4cd057b9627b736c959439d04940e24e75f179e71b378"
    }
  }
}
```

## 2026-10-12T22:14:33.214+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "96f3aeee66ea4ddb97dbe17e00582543",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "af6f5d9b0ed577a7030094697493212cb4ce3fca66635a797f74d8a3b880b636",
  "time": "2026-10-12T22:14:33.214+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=528482304-536870911",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0063.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:33.581+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "fe5cd59fc90f4e9a91cf752089d3d2c3",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dcfb6c65dc1e8c017bdbfab24c345ce85aab086d5e7bb214064decaecae36466",
  "time": "2026-10-12T22:14:33.581+00:00",
  "event": "result",
  "elapsed_s": 3.328,
  "response": {
    "http_status": 206,
    "content_range": "bytes 452984832-461373439/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0054.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "2a0e4fa7ef72916d01c666977c69ffcaf6d419d057bc16e2627e51579db4e669"
    }
  }
}
```

## 2026-10-12T22:14:33.618+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "2a9c27d4021a4579bfc866f9cb0e2d91",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2975db1579133fd542c6e58c254bec58172845151a4e505273751efbeed7a0c5",
  "time": "2026-10-12T22:14:33.618+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=536870912-545259519",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0064.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:33.863+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "4dc6f7abd03444b3b5409476da22b8dd",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b1c42842e5fbe9172b8f35649866e05017574ab53785048fb14bffa3ee502e07",
  "time": "2026-10-12T22:14:33.863+00:00",
  "event": "result",
  "elapsed_s": 2.281,
  "response": {
    "http_status": 206,
    "content_range": "bytes 486539264-494927871/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0058.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "11c89a904a5773ae185109709f27b07fe877fd0ba900e6ddb3862d7d7adb8a5b"
    }
  }
}
```

## 2026-10-12T22:14:33.890+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "962aac49e59848e2844ceaca87fc5e1d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "64c18349d02fb1a8fdb3757e710652187d2c18f7c42e639b986a465df0891337",
  "time": "2026-10-12T22:14:33.890+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=545259520-553648127",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0065.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:33.973+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "76e0e94e04264276994bc740ebd89970",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b7e9207d86d6feb3e2822c8425cad505f888140fac6548e4f85145d7d3b4246a",
  "time": "2026-10-12T22:14:33.973+00:00",
  "event": "result",
  "elapsed_s": 2.531,
  "response": {
    "http_status": 206,
    "content_range": "bytes 478150656-486539263/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0057.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "5ad9f36f2b5f793209370b5a1016f746d83722197115b22c5c29c9709319e573"
    }
  }
}
```

## 2026-10-12T22:14:34.005+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a502b4d45bfc4b96a307ad454a6edcdb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "5254d39707179b25c6b687d9904904277ea75d8e2cab739b082075859cedbc22",
  "time": "2026-10-12T22:14:34.005+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=553648128-562036735",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0066.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:34.178+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "71ed2ea52f224c7f9dd9854b9377ac83",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "34ad122566b3af3a78aa8b56119bf69291ab964fd37ba6d91026f5213934dd85",
  "time": "2026-10-12T22:14:34.178+00:00",
  "event": "result",
  "elapsed_s": 2.203,
  "response": {
    "http_status": 206,
    "content_range": "bytes 494927872-503316479/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0059.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "b2cc73d461fd61bac5a95d98a41c7d762d9aac11debeef80d46265c76d274079"
    }
  }
}
```

## 2026-10-12T22:14:34.214+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "6af9a67af61e41e9a59ce4d8ee0998e4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0687cf46c60323bc2967324afcf1607af776a7731d51852551d3943813e6bf20",
  "time": "2026-10-12T22:14:34.214+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=562036736-570425343",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0067.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:34.659+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b55cd60cdcc9433b92bda63e720f06d9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c03ed66557befd1d58d160fc0d0e7a8882842eb232097d91146bcf1150f23653",
  "time": "2026-10-12T22:14:34.659+00:00",
  "event": "result",
  "elapsed_s": 2.453,
  "response": {
    "http_status": 206,
    "content_range": "bytes 503316480-511705087/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0060.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a19e396ce48fb479f4d503c81eb0c35ec766ae6d23e38e09854a0e54163b8ae1"
    }
  }
}
```

## 2026-10-12T22:14:34.688+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "1c9f7fcd957c4f34be143e8a895a3f81",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bbb311315b096051c430a77460e8917df8dd4a6a2a2bd395b971e03572536338",
  "time": "2026-10-12T22:14:34.688+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=570425344-578813951",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0068.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:35.732+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "e1e12c07b3d74c279c2b5bf26651c583",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bd8d54bd1a3b3456ed4cded6acf0a9500789da3bc9788f3dfba0c09c24e6706a",
  "time": "2026-10-12T22:14:35.732+00:00",
  "event": "result",
  "elapsed_s": 3.094,
  "response": {
    "http_status": 206,
    "content_range": "bytes 511705088-520093695/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0061.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "0b005943a7d7d61c648134c04d72b62023a63bac9efb9059cb97ff8383673246"
    }
  }
}
```

## 2026-10-12T22:14:35.770+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "cd40a88daf0048f49e0c7755fca162bb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c2a538a86c8af136b2851f98be735ae4036e5551dca77baaf8f845dc7d942658",
  "time": "2026-10-12T22:14:35.770+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=578813952-587202559",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0069.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:36.346+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "96f3aeee66ea4ddb97dbe17e00582543",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "af6f5d9b0ed577a7030094697493212cb4ce3fca66635a797f74d8a3b880b636",
  "time": "2026-10-12T22:14:36.346+00:00",
  "event": "result",
  "elapsed_s": 3.109,
  "response": {
    "http_status": 206,
    "content_range": "bytes 528482304-536870911/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0063.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "eea148fddae44d4ab2e7384ecfb87d5ebd5ab3adc6fbf6384fb614da3735f4b6"
    }
  }
}
```

## 2026-10-12T22:14:36.373+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a577e6f634e146e9bc7f5f486ed5013e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f6792b3f239adb368658a8f636d2590416d11c11f273a4ccf543f7ec8d7ad8b5",
  "time": "2026-10-12T22:14:36.373+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=587202560-595591167",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0070.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:36.439+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "2a9c27d4021a4579bfc866f9cb0e2d91",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "2975db1579133fd542c6e58c254bec58172845151a4e505273751efbeed7a0c5",
  "time": "2026-10-12T22:14:36.439+00:00",
  "event": "result",
  "elapsed_s": 2.797,
  "response": {
    "http_status": 206,
    "content_range": "bytes 536870912-545259519/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0064.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a7a297758ba3c997a6581b3ae9ddccfa4877715ccf649218ea73dd19602c6183"
    }
  }
}
```

## 2026-10-12T22:14:36.476+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0752ab4935424ff7a6350ce68a1c793f",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "06678e0f1f25a0b75531e10c92d219f4955a3349d791c849d10cecf9763d72d3",
  "time": "2026-10-12T22:14:36.476+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=595591168-603979775",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0071.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:35.737+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "2b04fde4dd45486c80500ef3bcc5490f",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "3b4dccf9d9a2f54a9b1b513571438b5d8e469f9673ce6dd9dc3b0aa187624f1a",
  "time": "2026-10-12T22:14:35.737+00:00",
  "event": "result",
  "elapsed_s": 2.906,
  "response": {
    "http_status": 206,
    "content_range": "bytes 520093696-528482303/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0062.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "0ae07921bc894ce46a52ca39c95056f156d7b6888c6f4b490bf2ea81665c834f"
    }
  }
}
```

## 2026-10-12T22:14:36.778+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "45279d1f35084cd198537777256e115d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a264fb5a0c72dbe3711dacf6eaaed86dae68636c9c56f96b33363b823d5ef574",
  "time": "2026-10-12T22:14:36.778+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=603979776-612368383",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0072.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:36.859+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "962aac49e59848e2844ceaca87fc5e1d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "64c18349d02fb1a8fdb3757e710652187d2c18f7c42e639b986a465df0891337",
  "time": "2026-10-12T22:14:36.859+00:00",
  "event": "result",
  "elapsed_s": 2.953,
  "response": {
    "http_status": 206,
    "content_range": "bytes 545259520-553648127/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0065.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "00aedb5573efbe0ea4551e9e529e81dede2785d3d0e3c83b5c505684642520ea"
    }
  }
}
```

## 2026-10-12T22:14:36.897+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "00789a1ab08f4c38a8b7f26f8f389aa2",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9fdf2803c3decf8353b45b92fc65fb63efc47f4d1089e611dd61e59b87d2b98a",
  "time": "2026-10-12T22:14:36.897+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=612368384-620756991",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0073.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:37.943+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a502b4d45bfc4b96a307ad454a6edcdb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "5254d39707179b25c6b687d9904904277ea75d8e2cab739b082075859cedbc22",
  "time": "2026-10-12T22:14:37.943+00:00",
  "event": "result",
  "elapsed_s": 3.922,
  "response": {
    "http_status": 206,
    "content_range": "bytes 553648128-562036735/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0066.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a8eac36fed4eaea5a9795f531d22afc836449d1d62619812c24b5b0e12950111"
    }
  }
}
```

## 2026-10-12T22:14:37.981+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "5801287e26824584bf43b4c313a25f52",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "570d8615391d35e29f9a429d70cda410aa6ab8556878af514f62f6c0d729c860",
  "time": "2026-10-12T22:14:37.981+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=620756992-629145599",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0074.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:38.933+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "6af9a67af61e41e9a59ce4d8ee0998e4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "0687cf46c60323bc2967324afcf1607af776a7731d51852551d3943813e6bf20",
  "time": "2026-10-12T22:14:38.933+00:00",
  "event": "result",
  "elapsed_s": 4.703,
  "response": {
    "http_status": 206,
    "content_range": "bytes 562036736-570425343/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0067.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "fe4ac9c070b32066781595f389122b1061c73be5413ed1266ffb99fac5bbab55"
    }
  }
}
```

## 2026-10-12T22:14:38.976+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "cec0b96b976c456cac9868a32e053af8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a91947a7bc7bae2a7ec38091bd425ef506df294a2e4a641835939fd73d281af7",
  "time": "2026-10-12T22:14:38.976+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=629145600-637534207",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0075.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:39.121+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "1c9f7fcd957c4f34be143e8a895a3f81",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "bbb311315b096051c430a77460e8917df8dd4a6a2a2bd395b971e03572536338",
  "time": "2026-10-12T22:14:39.121+00:00",
  "event": "result",
  "elapsed_s": 4.407,
  "response": {
    "http_status": 206,
    "content_range": "bytes 570425344-578813951/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0068.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "2120d752cfd2cbcb04dc23e6169eb98f5b60bc1278a408d7b517b3fe9522dc3b"
    }
  }
}
```

## 2026-10-12T22:14:39.157+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "5d345e3808e74b6c8f615856690842db",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9e634303613c27bf4b3616500eb8ded1c35c1b92b5facb16a50848c7ade9913e",
  "time": "2026-10-12T22:14:39.157+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=637534208-645922815",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0076.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:39.623+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "cd40a88daf0048f49e0c7755fca162bb",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c2a538a86c8af136b2851f98be735ae4036e5551dca77baaf8f845dc7d942658",
  "time": "2026-10-12T22:14:39.623+00:00",
  "event": "result",
  "elapsed_s": 3.829,
  "response": {
    "http_status": 206,
    "content_range": "bytes 578813952-587202559/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0069.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "5031c94cf07e26dab67d5ef0127ce9d37d96f6ad9ab1ce09391bb5bd189e5eed"
    }
  }
}
```

## 2026-10-12T22:14:39.653+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "d3e6e34fb9ea485cad2e4763e33e3fd4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "57bb2e0ffc71c490022b69e49d0f25592ef21bc84839b881419cb05561d8e1cd",
  "time": "2026-10-12T22:14:39.653+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=645922816-654311423",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0077.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:39.947+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0752ab4935424ff7a6350ce68a1c793f",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "06678e0f1f25a0b75531e10c92d219f4955a3349d791c849d10cecf9763d72d3",
  "time": "2026-10-12T22:14:39.947+00:00",
  "event": "result",
  "elapsed_s": 3.453,
  "response": {
    "http_status": 206,
    "content_range": "bytes 595591168-603979775/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0071.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "71dd9dc95e2e3433a3baae743b828fbff8ac5c197f9c73483f02a3e42b50ec65"
    }
  }
}
```

## 2026-10-12T22:14:39.986+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "da8f053b4983484c85f37b4f79a86b00",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c539a19c9c06f40504f9ce910e10b2964001a6515060a251eecf1f4b4c8767a2",
  "time": "2026-10-12T22:14:39.986+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=654311424-662700031",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0078.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:40.333+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a577e6f634e146e9bc7f5f486ed5013e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f6792b3f239adb368658a8f636d2590416d11c11f273a4ccf543f7ec8d7ad8b5",
  "time": "2026-10-12T22:14:40.333+00:00",
  "event": "result",
  "elapsed_s": 3.937,
  "response": {
    "http_status": 206,
    "content_range": "bytes 587202560-595591167/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0070.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "bf4b292777af95b730856a0f1e0d90c4a49a6f697a056e7e01197edfbb45b654"
    }
  }
}
```

## 2026-10-12T22:14:40.368+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "525cf26b513646ba9de76a28f4a90b85",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "51e4ac6d9ccbce03204a3a885714005ba50875ab03768d21ce2cac04d875e2bc",
  "time": "2026-10-12T22:14:40.368+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=662700032-671088639",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0079.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:41.840+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "00789a1ab08f4c38a8b7f26f8f389aa2",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9fdf2803c3decf8353b45b92fc65fb63efc47f4d1089e611dd61e59b87d2b98a",
  "time": "2026-10-12T22:14:41.840+00:00",
  "event": "result",
  "elapsed_s": 4.922,
  "response": {
    "http_status": 206,
    "content_range": "bytes 612368384-620756991/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0073.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "6b0331561621d088a93c619797254d010360a5f8fef777ce40c208a1cba9a254"
    }
  }
}
```

## 2026-10-12T22:14:41.874+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "3c6520a9364a4ae3a9915b86d5f39144",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a082677d194bff11b4e16912060af1196716e2c67547ca88aed1d15a5440c3eb",
  "time": "2026-10-12T22:14:41.874+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=671088640-679477247",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0080.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:42.293+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "45279d1f35084cd198537777256e115d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a264fb5a0c72dbe3711dacf6eaaed86dae68636c9c56f96b33363b823d5ef574",
  "time": "2026-10-12T22:14:42.293+00:00",
  "event": "result",
  "elapsed_s": 5.484,
  "response": {
    "http_status": 206,
    "content_range": "bytes 603979776-612368383/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0072.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "8b2b4a88c6695d9020bae55ab71ee274d16df930acc6704b4ee4076eafa9df4f"
    }
  }
}
```

## 2026-10-12T22:14:42.334+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "62dad48886294a6997a66e35de601fc4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "500736f1f70c61ce8f19e4c1e193d8143a67d6b3f65861b1083f0d5024f0cd77",
  "time": "2026-10-12T22:14:42.334+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=679477248-687865855",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0081.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:43.232+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "cec0b96b976c456cac9868a32e053af8",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a91947a7bc7bae2a7ec38091bd425ef506df294a2e4a641835939fd73d281af7",
  "time": "2026-10-12T22:14:43.232+00:00",
  "event": "result",
  "elapsed_s": 4.234,
  "response": {
    "http_status": 206,
    "content_range": "bytes 629145600-637534207/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0075.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a10107f6714a8295c31c377b410ffe9357c81b83e12ec19678d7b59c4070150f"
    }
  }
}
```

## 2026-10-12T22:14:43.268+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "8001672668ad451abfa0c98680415eb1",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c296d274ec155f0dcfecb8e5a1e2dae5882d1032ffbd47d7f537fbfe045c2bbb",
  "time": "2026-10-12T22:14:43.268+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=687865856-696254463",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0082.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:43.332+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "5801287e26824584bf43b4c313a25f52",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "570d8615391d35e29f9a429d70cda410aa6ab8556878af514f62f6c0d729c860",
  "time": "2026-10-12T22:14:43.332+00:00",
  "event": "result",
  "elapsed_s": 5.328,
  "response": {
    "http_status": 206,
    "content_range": "bytes 620756992-629145599/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0074.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "6d65e8c72f033c4b0b8162883120b24710cc5a4ebe52d02db646d30bbbf91f2e"
    }
  }
}
```

## 2026-10-12T22:14:43.358+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "56a9d358bce44cc1b4c511dcaed53446",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f0b4ecbaa28d861c33e296fb26af16d843caf19e87980d5c12ec42ecc2956778",
  "time": "2026-10-12T22:14:43.358+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=696254464-704643071",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0083.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:43.675+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "5d345e3808e74b6c8f615856690842db",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "9e634303613c27bf4b3616500eb8ded1c35c1b92b5facb16a50848c7ade9913e",
  "time": "2026-10-12T22:14:43.675+00:00",
  "event": "result",
  "elapsed_s": 4.484,
  "response": {
    "http_status": 206,
    "content_range": "bytes 637534208-645922815/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0076.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "2171dc53d6af177606204be7ff9d2701282e74efd7a6aa72bd3f71a688adfed9"
    }
  }
}
```

## 2026-10-12T22:14:43.712+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0ccf2e1c65d84f319105720bdc54b5aa",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "ea2017dbbcef9121e27f4be33cdc30a82f1d7691bf18b4be7a12e80a569657a1",
  "time": "2026-10-12T22:14:43.712+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=704643072-713031679",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0084.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:44.464+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "d3e6e34fb9ea485cad2e4763e33e3fd4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "57bb2e0ffc71c490022b69e49d0f25592ef21bc84839b881419cb05561d8e1cd",
  "time": "2026-10-12T22:14:44.464+00:00",
  "event": "result",
  "elapsed_s": 4.797,
  "response": {
    "http_status": 206,
    "content_range": "bytes 645922816-654311423/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0077.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "bf7839b741672aa50dc57cea672522b84583397b0725332994d8fda5120d2af7"
    }
  }
}
```

## 2026-10-12T22:14:44.491+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "5fd0af45025141dbb06751d9169c3e65",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "151861677cd51bd348dcd894bc4fc9209216c131b14e092a32746f87dec626db",
  "time": "2026-10-12T22:14:44.491+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=713031680-721420287",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0085.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:45.374+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "525cf26b513646ba9de76a28f4a90b85",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "51e4ac6d9ccbce03204a3a885714005ba50875ab03768d21ce2cac04d875e2bc",
  "time": "2026-10-12T22:14:45.374+00:00",
  "event": "result",
  "elapsed_s": 4.985,
  "response": {
    "http_status": 206,
    "content_range": "bytes 662700032-671088639/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0079.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "da1653782791a86f60fd771aceddc305e9d632cb4c488cde3712813034a5ce6c"
    }
  }
}
```

## 2026-10-12T22:14:45.412+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "bc210a8cfe7f4acd93b80fcc25ff63c9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a7397646bf508d6af98f95466dbc988f4e4afbd389c9a7196bbc5dc83972995e",
  "time": "2026-10-12T22:14:45.412+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=721420288-729808895",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0086.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:45.486+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "da8f053b4983484c85f37b4f79a86b00",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c539a19c9c06f40504f9ce910e10b2964001a6515060a251eecf1f4b4c8767a2",
  "time": "2026-10-12T22:14:45.486+00:00",
  "event": "result",
  "elapsed_s": 5.469,
  "response": {
    "http_status": 206,
    "content_range": "bytes 654311424-662700031/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0078.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "613487f7a40d68fa7996b95b14cbc2167f4b375e0f938c7b1df3960a785d1d36"
    }
  }
}
```

## 2026-10-12T22:14:45.506+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "9ac54478be6e456182a06c8086ee814d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dce61bc8563c2f94c6ab9587e58bc6c21a9e0655400d100f6262080b5c537fd9",
  "time": "2026-10-12T22:14:45.506+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=729808896-738197503",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0087.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:46.061+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "3c6520a9364a4ae3a9915b86d5f39144",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a082677d194bff11b4e16912060af1196716e2c67547ca88aed1d15a5440c3eb",
  "time": "2026-10-12T22:14:46.061+00:00",
  "event": "result",
  "elapsed_s": 4.156,
  "response": {
    "http_status": 206,
    "content_range": "bytes 671088640-679477247/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0080.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "ee138f9e6bbc72e1c87d7112e3f9d06516f9666e699469d2373f8d54fcd0bdb4"
    }
  }
}
```

## 2026-10-12T22:14:46.086+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "00af5f7e9ba44b17a74d17ca69ab1114",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "6a3ae4003cb8da4b267809f6d9f3d1da23be8d976fb8c316bb7552b44d07b5a3",
  "time": "2026-10-12T22:14:46.086+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=738197504-746586111",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0088.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:46.726+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "62dad48886294a6997a66e35de601fc4",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "500736f1f70c61ce8f19e4c1e193d8143a67d6b3f65861b1083f0d5024f0cd77",
  "time": "2026-10-12T22:14:46.726+00:00",
  "event": "result",
  "elapsed_s": 4.375,
  "response": {
    "http_status": 206,
    "content_range": "bytes 679477248-687865855/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0081.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "a222f93891c7f04ea60b76bc278a50bcf465b39bb27042794bd85bbc4042d1a3"
    }
  }
}
```

## 2026-10-12T22:14:46.762+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "19be3bdb08e44c98b1cbcd49b55d6236",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "373a9296d79e71df8d1525c8d47026aecc8f746176959047c8d3346a455d4f03",
  "time": "2026-10-12T22:14:46.762+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=746586112-754974719",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0089.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:47.440+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "8001672668ad451abfa0c98680415eb1",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "c296d274ec155f0dcfecb8e5a1e2dae5882d1032ffbd47d7f537fbfe045c2bbb",
  "time": "2026-10-12T22:14:47.440+00:00",
  "event": "result",
  "elapsed_s": 4.141,
  "response": {
    "http_status": 206,
    "content_range": "bytes 687865856-696254463/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0082.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "051da0c8bfdb5fa01bcd578cd586ebf8c1655c7b8c2884314b2484fca4aa2a01"
    }
  }
}
```

## 2026-10-12T22:14:47.467+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "8ce7c6ed902e4a5886fcf6d845da6095",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a4c73f2f1d05d4d86f480d65e49703de30478b49fa41884d56ac5dba57c6c4a4",
  "time": "2026-10-12T22:14:47.467+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=754974720-763363327",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0090.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:47.832+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "56a9d358bce44cc1b4c511dcaed53446",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f0b4ecbaa28d861c33e296fb26af16d843caf19e87980d5c12ec42ecc2956778",
  "time": "2026-10-12T22:14:47.832+00:00",
  "event": "result",
  "elapsed_s": 4.468,
  "response": {
    "http_status": 206,
    "content_range": "bytes 696254464-704643071/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0083.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "34e9e852383b9b0768c72f63da49c2260c1f5ce7702aef911703826b2ffda116"
    }
  }
}
```

## 2026-10-12T22:14:47.857+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a5c25e2bf58841348edd1bbe91c034bf",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "153970787602d1392550676dd7623e3dbdad6f9812e24507e73fda73bf4b30b8",
  "time": "2026-10-12T22:14:47.857+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=763363328-771751935",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0091.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:48.299+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0ccf2e1c65d84f319105720bdc54b5aa",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "ea2017dbbcef9121e27f4be33cdc30a82f1d7691bf18b4be7a12e80a569657a1",
  "time": "2026-10-12T22:14:48.299+00:00",
  "event": "result",
  "elapsed_s": 4.562,
  "response": {
    "http_status": 206,
    "content_range": "bytes 704643072-713031679/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0084.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "619fc9986b34fd6f79f82fbe869cd9c9b6ddcffabb6e30423ccc17d52dd92f45"
    }
  }
}
```

## 2026-10-12T22:14:48.337+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "a0f72342cda7494394e6130f2b9ea5d0",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f2e0d19608e184e7c62b0b41497f4aa8356cb1d9945e13945ca3711173d2495e",
  "time": "2026-10-12T22:14:48.337+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=771751936-780140543",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0092.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:49.294+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "bc210a8cfe7f4acd93b80fcc25ff63c9",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a7397646bf508d6af98f95466dbc988f4e4afbd389c9a7196bbc5dc83972995e",
  "time": "2026-10-12T22:14:49.294+00:00",
  "event": "result",
  "elapsed_s": 3.843,
  "response": {
    "http_status": 206,
    "content_range": "bytes 721420288-729808895/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0086.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "9eb441ff0f1612ad7f4c0933d2652b65db35014bf39e80a13ac6f29650db28a7"
    }
  }
}
```

## 2026-10-12T22:14:49.320+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "7af021ae5ef74d0b94606f9c3e292b49",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "950342f6571cf060e9cdafc22e60dae521d6132bc6d59006ac18d5c1d2a88929",
  "time": "2026-10-12T22:14:49.320+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=780140544-788529151",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0093.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:49.705+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "5fd0af45025141dbb06751d9169c3e65",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "151861677cd51bd348dcd894bc4fc9209216c131b14e092a32746f87dec626db",
  "time": "2026-10-12T22:14:49.705+00:00",
  "event": "result",
  "elapsed_s": 5.188,
  "response": {
    "http_status": 206,
    "content_range": "bytes 713031680-721420287/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0085.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "c3bec165fd907150867035e05f33aeab85f0b32beb63c8817ef432c785969cd1"
    }
  }
}
```

## 2026-10-12T22:14:49.742+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "0c69bbbbbba7407299d1eb8f92fd4f23",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a1be090c09287e271dc29c79628dd0af61ad21a8aeefd1c084d276a7e0ab5ac3",
  "time": "2026-10-12T22:14:49.742+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=788529152-796917759",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0094.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:50.017+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "9ac54478be6e456182a06c8086ee814d",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "dce61bc8563c2f94c6ab9587e58bc6c21a9e0655400d100f6262080b5c537fd9",
  "time": "2026-10-12T22:14:50.017+00:00",
  "event": "result",
  "elapsed_s": 4.484,
  "response": {
    "http_status": 206,
    "content_range": "bytes 729808896-738197503/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0087.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "f1f800d6a40096e5704c2e2aa223986a653bb3e48724bccbc1f3cac7bc1099bb"
    }
  }
}
```

## 2026-10-12T22:14:50.048+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "61afe8a10b3f4ed487124b4395b86aad",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "db604423550a5b5fc11c786cb2fe50ecac21a14288afbcd22161ef15fcc6d0ea",
  "time": "2026-10-12T22:14:50.048+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=796917760-805306367",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0095.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:50.053+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "00af5f7e9ba44b17a74d17ca69ab1114",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "6a3ae4003cb8da4b267809f6d9f3d1da23be8d976fb8c316bb7552b44d07b5a3",
  "time": "2026-10-12T22:14:50.053+00:00",
  "event": "result",
  "elapsed_s": 3.953,
  "response": {
    "http_status": 206,
    "content_range": "bytes 738197504-746586111/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0088.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "c8b24dd36213df30f1dbec04b7b30eed42b339b0f6cf9fb225c8aabc22560388"
    }
  }
}
```

## 2026-10-12T22:14:50.113+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "b9263e74ac8a4eedaa4611f29a92c51e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "d87fcb0d89bedd1b208c0132985268b4f11d2817e4bbd159571f7920088beb32",
  "time": "2026-10-12T22:14:50.113+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=805306368-813694975",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0096.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:51.147+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "19be3bdb08e44c98b1cbcd49b55d6236",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "373a9296d79e71df8d1525c8d47026aecc8f746176959047c8d3346a455d4f03",
  "time": "2026-10-12T22:14:51.147+00:00",
  "event": "result",
  "elapsed_s": 4.36,
  "response": {
    "http_status": 206,
    "content_range": "bytes 746586112-754974719/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0089.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "fcca86f29ec84826568f6fa153019ee7e1671c0403007ab0d165dd8dfff40986"
    }
  }
}
```

## 2026-10-12T22:14:51.185+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "8d2fd990fa0249eb8ec3ea0b07c6d8cf",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b32bc502cb88a1e5e3e1ee52ecfad71712af4816fe8b8ff810602a8fef8bf979",
  "time": "2026-10-12T22:14:51.185+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=813694976-822083583",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0097.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:51.948+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "8ce7c6ed902e4a5886fcf6d845da6095",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a4c73f2f1d05d4d86f480d65e49703de30478b49fa41884d56ac5dba57c6c4a4",
  "time": "2026-10-12T22:14:51.948+00:00",
  "event": "result",
  "elapsed_s": 4.453,
  "response": {
    "http_status": 206,
    "content_range": "bytes 754974720-763363327/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0090.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "aca6fe61eb0b258a6bf04d536f2014440a27b56f7692f580cc18821b7e8230b7"
    }
  }
}
```

## 2026-10-12T22:14:51.984+00:00 — cascadeur / download_mocap_model_range — request

```json
{
  "request_id": "e92491e76d5b43ab8c6e5b26d265d638",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f37539a83873e8b9d4c316ff89065df063f8944b44eef221126ad5bab2dd14f1",
  "time": "2026-10-12T22:14:51.984+00:00",
  "event": "request",
  "request": {
    "url": "https://cdn.cascadeur.com/animations/files/17/mocap_010725.pt",
    "range": "bytes=822083584-825323914",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0098.bin",
    "timeout_s": 30,
    "attempt": 1,
    "authorization": "[REDACTED]"
  }
}
```

## 2026-10-12T22:14:52.172+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a5c25e2bf58841348edd1bbe91c034bf",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "153970787602d1392550676dd7623e3dbdad6f9812e24507e73fda73bf4b30b8",
  "time": "2026-10-12T22:14:52.172+00:00",
  "event": "result",
  "elapsed_s": 4.296,
  "response": {
    "http_status": 206,
    "content_range": "bytes 763363328-771751935/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0091.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "d30ed75df3f44c6eaf070d66efa6d658303f55122f5102a3b140ef050b41b9b7"
    }
  }
}
```

## 2026-10-12T22:14:52.648+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "a0f72342cda7494394e6130f2b9ea5d0",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f2e0d19608e184e7c62b0b41497f4aa8356cb1d9945e13945ca3711173d2495e",
  "time": "2026-10-12T22:14:52.648+00:00",
  "event": "result",
  "elapsed_s": 4.297,
  "response": {
    "http_status": 206,
    "content_range": "bytes 771751936-780140543/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0092.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "8aedb4e466f5d2f7314f7aa98ded1bc72d3f9b7c37e3bb0675bbfb53c7334a8d"
    }
  }
}
```

## 2026-10-12T22:14:53.810+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "0c69bbbbbba7407299d1eb8f92fd4f23",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "a1be090c09287e271dc29c79628dd0af61ad21a8aeefd1c084d276a7e0ab5ac3",
  "time": "2026-10-12T22:14:53.810+00:00",
  "event": "result",
  "elapsed_s": 4.047,
  "response": {
    "http_status": 206,
    "content_range": "bytes 788529152-796917759/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0094.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "d04b8c46a256e243c37d57feb1d49394475996bd607cec6c6e4542a5b8b0e660"
    }
  }
}
```

## 2026-10-12T22:14:54.684+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "61afe8a10b3f4ed487124b4395b86aad",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "db604423550a5b5fc11c786cb2fe50ecac21a14288afbcd22161ef15fcc6d0ea",
  "time": "2026-10-12T22:14:54.684+00:00",
  "event": "result",
  "elapsed_s": 4.609,
  "response": {
    "http_status": 206,
    "content_range": "bytes 796917760-805306367/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0095.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "3c16d00eec42f077fa6f50608c6bca9dc2a0505b888468a1ba85330ec7757f36"
    }
  }
}
```

## 2026-10-12T22:14:54.868+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "b9263e74ac8a4eedaa4611f29a92c51e",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "d87fcb0d89bedd1b208c0132985268b4f11d2817e4bbd159571f7920088beb32",
  "time": "2026-10-12T22:14:54.868+00:00",
  "event": "result",
  "elapsed_s": 4.735,
  "response": {
    "http_status": 206,
    "content_range": "bytes 805306368-813694975/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0096.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "b7e13aee885e027affae34323a3e8e2ee795d72925fe0b34240a0771d8f8d778"
    }
  }
}
```

## 2026-10-12T22:14:55.070+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "7af021ae5ef74d0b94606f9c3e292b49",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "950342f6571cf060e9cdafc22e60dae521d6132bc6d59006ac18d5c1d2a88929",
  "time": "2026-10-12T22:14:55.070+00:00",
  "event": "result",
  "elapsed_s": 5.735,
  "response": {
    "http_status": 206,
    "content_range": "bytes 780140544-788529151/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0093.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "f20d7db7a79d86431941794f4ff0ea71baed66d0827c395d04ca2ff443cc3b5f"
    }
  }
}
```

## 2026-10-12T22:14:55.626+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "e92491e76d5b43ab8c6e5b26d265d638",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "f37539a83873e8b9d4c316ff89065df063f8944b44eef221126ad5bab2dd14f1",
  "time": "2026-10-12T22:14:55.626+00:00",
  "event": "result",
  "elapsed_s": 3.61,
  "response": {
    "http_status": 206,
    "content_range": "bytes 822083584-825323914/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0098.bin",
      "exists": true,
      "bytes": 3240331,
      "sha256": "61c5126ae533e5546166501df20577e1adf0d3160988c915037a7e4ff931a253"
    }
  }
}
```

## 2026-10-12T22:14:56.027+00:00 — cascadeur / download_mocap_model_range — result

```json
{
  "request_id": "8d2fd990fa0249eb8ec3ea0b07c6d8cf",
  "provider": "cascadeur",
  "operation": "download_mocap_model_range",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013\\mocap_010725.pt",
  "pid": 53068,
  "request_fingerprint": "b32bc502cb88a1e5e3e1ee52ecfad71712af4816fe8b8ff810602a8fef8bf979",
  "time": "2026-10-12T22:14:56.027+00:00",
  "event": "result",
  "elapsed_s": 4.813,
  "response": {
    "http_status": 206,
    "content_range": "bytes 813694976-822083583/825323915",
    "file": {
      "path": "C:\\workspace\\micro-drama-platform\\.audit\\adhoc_agents\\2026-10-13\\shu-motion-test\\model_parts\\0097.bin",
      "exists": true,
      "bytes": 8388608,
      "sha256": "72155d5b106e18dee470378ef721e652f909e5045f3046439fdf669970129a2a"
    }
  }
}
```

## 2026-10-12T22:18:17.773787+00:00 — cascadeur / mocap_local_trial — result

```json
{
  "request_id": "8daf00885cc347eeb462a7c850e49251",
  "provider": "cascadeur",
  "operation": "mocap_local_trial",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:18:17.773787+00:00",
  "event": "result",
  "response": {
    "message": "首次原生Mocap调用仅触发模型缺失下载提示，未生成动画；模型现已完整安装825323915字节，复制后SHA256一致"
  }
}
```

## 2026-10-12T22:18:17.946714+00:00 — cascadeur / mocap_sequence_capture — request

```json
{
  "request_id": "5531c0e60545469795deac584585254e",
  "provider": "cascadeur",
  "operation": "mocap_sequence_capture",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:18:17.946714+00:00",
  "event": "request",
  "request": {
    "message": "官方模型已安装；Plane(0)连续图片参考，30fps；准备选择0至149帧，对Cascy执行本地Mocap；不上传源视频，不计积分"
  }
}
```

## 2026-10-12T22:32:35.693451+00:00 — cascadeur / mocap_sequence_capture — result

```json
{
  "request_id": "5531c0e60545469795deac584585254e",
  "provider": "cascadeur",
  "operation": "mocap_sequence_capture",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:32:35.693451+00:00",
  "event": "result",
  "response": {
    "message": "连续区间选择未可靠完成，未执行批量捕捉；先改为当前帧姿势识别验证"
  }
}
```

## 2026-10-12T22:32:35.868537+00:00 — cascadeur / mocap_pose_probe — request

```json
{
  "request_id": "439e3c981cb34c69b58316fb85e20aef",
  "provider": "cascadeur",
  "operation": "mocap_pose_probe",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:32:35.868537+00:00",
  "event": "request",
  "request": {
    "message": "当前时间指示99帧，选择边界显示100；参考Plane(0)，目标场景只有Cascy一个角色；官方mocap_010725.pt已完整安装；本地单帧捕捉验证"
  }
}
```

## 2026-10-12T22:35:49.655947+00:00 — cascadeur / mocap_pose_probe — observation

```json
{
  "request_id": "439e3c981cb34c69b58316fb85e20aef",
  "provider": "cascadeur",
  "operation": "mocap_pose_probe",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-12T22:35:49.655947+00:00",
  "event": "observation",
  "observation": {
    "processing_window": "Mocap Cascy.casc",
    "confirmation_window": "Mocap",
    "buttons": [
      "Yes",
      "No"
    ],
    "prompt_text": "桌面工具不可读，等待用户提供",
    "animation_completion": "未知，未交付",
    "unexpected_prior_control": "曾点击Motion Generation按钮，因不足2关键帧被软件拒绝；未提交任务"
  }
}
```

## 2026-10-13T01:10:33.788783+00:00 — cascadeur / mocap_pose_probe — error

```json
{
  "request_id": "439e3c981cb34c69b58316fb85e20aef",
  "provider": "cascadeur",
  "operation": "mocap_pose_probe",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-13T01:10:33.788783+00:00",
  "event": "error",
  "response": {
    "message": "用户报告已确认Yes并进入Mocaping；日志09:05:47 start mocap，09:08:53起多次AutoPosing: wrong input count，09:09:06 ERROR；09:10当前进程和窗口均未发现，尚未取得可验证动画。"
  }
}
```

## 2026-10-13T01:10:33.955857+00:00 — cascadeur / recovery_inspection — request

```json
{
  "request_id": "038d885ff2ee46238cb471632ca488dc",
  "provider": "cascadeur",
  "operation": "recovery_inspection",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-13T01:10:33.955857+00:00",
  "event": "request",
  "request": {
    "message": "重新打开已安装Cascadeur检查是否存在本次试验自动恢复工程；仅检查恢复资料并另存，不重试同一Mocap。"
  }
}
```

## 2026-10-13T01:14:36.516383+00:00 — cascadeur / recovery_inspection — result

```json
{
  "request_id": "038d885ff2ee46238cb471632ca488dc",
  "provider": "cascadeur",
  "operation": "recovery_inspection",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-13T01:14:36.516383+00:00",
  "event": "result",
  "response": {
    "message": "重开成功；恢复autosave2-Cascy仅有站立角色和参考平面，未发现可验证捕捉动画；最新捕捉前autosave0已复制reference_setup_recovered.casc，5438820字节，SHA256 ed46ee15ec77f8a9bd732786f1d62b4cc2fe8e2004b1f1354d777ee8f5f49795，副本尚未单独重新打开验证。"
  }
}
```

## 2026-10-13T12:42:48.306302+00:00 — cascadeur / autoposing_diagnostic — request

```json
{
  "request_id": "453e786428ab4e958a1d1ce9fde370d5",
  "provider": "cascadeur",
  "operation": "autoposing_diagnostic",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\_research\\service_tests\\shu_motion_20261013",
  "interface": "computer-use @oai/sky",
  "time": "2026-10-13T12:42:48.306302+00:00",
  "event": "request",
  "request": {
    "message": "用户询问进展后继续排查既有崩溃；检查当前参考工程及全新官方角色的AutoPosing配置，暂不发起新Mocap、不覆盖样例。"
  }
}
```
