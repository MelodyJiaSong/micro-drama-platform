# 外部服务请求日志

请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。

## 2026-10-18T01:27:40.621+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "94822e6808bc4e62a83a315ed7cd2e6a",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.png",
  "pid": 44952,
  "request_fingerprint": "1f8fd22d29ced1b38ad6585a7044b99bd2ecdd3bfecb9ea0fc8fcbe1d6bcf277",
  "time": "2026-10-18T01:27:40.621+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一把华丽的细长刺剑。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：剑斜放，剑尖指向画面右上方，整把剑完整入画；剑身长约一米、宽不过两指，笔直收尖，中间一道细细的血槽；护手是几道镀金的弯曲金属条层层盘绕成螺旋笼形，包住握柄前端；握柄约一掌半长，珍珠白色，缠着细金丝；柄尾是一颗圆形的镀金柄头。\n材质与光：剑身是高度抛光的银白钢，表面隐隐透出一层淡金色的光，像钢里面藏着一缕晨光，亮度克制、刃线清晰；镀金护手有使用磨损，凹处发暗；握柄的珍珠白微带温润光泽。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，阔剑，双手巨剑，火焰剑，宝石镶满，霓虹发光剑刃，光剑，夸张金光",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:41.324+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "94822e6808bc4e62a83a315ed7cd2e6a",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.png",
  "pid": 44952,
  "request_fingerprint": "1f8fd22d29ced1b38ad6585a7044b99bd2ecdd3bfecb9ea0fc8fcbe1d6bcf277",
  "time": "2026-10-18T01:27:41.324+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "pending"
  }
}
```

## 2026-10-18T01:27:41.338+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "1bf0a8f2103c47cf81b61a44fe338792",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:41.338+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:41.911+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "1bf0a8f2103c47cf81b61a44fe338792",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:41.911+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "pending"
  }
}
```

## 2026-10-18T01:27:45.948+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "e28b8d4c2bb14f8d9e47d6a3e75fb9e3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:45.948+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:46.654+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "e28b8d4c2bb14f8d9e47d6a3e75fb9e3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:46.654+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:50.660+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "5195f709252541b08e0fcffcff29df35",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:50.660+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:51.301+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "5195f709252541b08e0fcffcff29df35",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:51.301+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:55.326+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "7d4f7e128ff34202b197709a321a07b9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:55.326+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:55.925+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "7d4f7e128ff34202b197709a321a07b9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:55.925+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:59.951+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "29cee98043ac43d18cdb87b0f1c327d9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:27:59.951+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:00.680+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "29cee98043ac43d18cdb87b0f1c327d9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:00.680+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:04.688+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "599f56c65a884f77b0756ac1fd668799",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:04.688+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:05.339+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "599f56c65a884f77b0756ac1fd668799",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:05.339+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:09.366+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "ede0aaa0eec64e3b862598ea9ac535a4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:09.366+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:09.937+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "ede0aaa0eec64e3b862598ea9ac535a4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:09.937+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:13.962+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "93652831d26e44e68e9d85b0ed21bdb7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:13.962+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:14.538+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "93652831d26e44e68e9d85b0ed21bdb7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:14.538+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:18.565+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "95423cd870044db2b48e7e5594afd92e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:18.565+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:19.152+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "95423cd870044db2b48e7e5594afd92e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:19.152+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:23.173+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — request

```json
{
  "request_id": "a78be07ed76c4aa399d45c1c784a590f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:23.173+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lT9OAjgwcSRQn082JqNJ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:23.884+00:00 — elevenlabs / GET /flows/image/lT9OAjgwcSRQn082JqNJ — result

```json
{
  "request_id": "a78be07ed76c4aa399d45c1c784a590f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lT9OAjgwcSRQn082JqNJ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "84cba4ab8a99af910e8aaf30c6580d21ded1d10bfcad28b63c980db3d0fefdb0",
  "time": "2026-10-18T01:28:23.884+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "lT9OAjgwcSRQn082JqNJ",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/nUKIYVVF3D4dNjn5a0IJ/lT9OAjgwcSRQn082JqNJ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012819Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:28:23.913+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "bc7f686bfe6e46b087661d990acccbba",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "132f8a43333542374bbbfa779a95ca792a280c9f86b293d55632c4ee4dc7ef4b",
  "time": "2026-10-18T01:28:23.913+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/nUKIYVVF3D4dNjn5a0IJ/lT9OAjgwcSRQn082JqNJ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012819Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:28:26.079+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "bc7f686bfe6e46b087661d990acccbba",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p10_Divine_Rapier\\p10_Divine_Rapier.part.png",
  "pid": 44952,
  "request_fingerprint": "132f8a43333542374bbbfa779a95ca792a280c9f86b293d55632c4ee4dc7ef4b",
  "time": "2026-10-18T01:28:26.079+00:00",
  "event": "result",
  "elapsed_s": 2.125,
  "response": [
    200,
    {
      "bytes": 4538624,
      "sha256": "49ecdecc516068e9dc08c2dcad9a25758bce1a680d979e29bff125792c411c2c"
    }
  ]
}
```

## 2026-10-18T01:28:26.117+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "69cf20ed4c6e4cec8b5ab2cbc4ce98ba",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.png",
  "pid": 44952,
  "request_fingerprint": "103a27429496b767c839f601166b046b5e08120b804558ca49ad0b388ca0c30d",
  "time": "2026-10-18T01:28:26.117+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一本合着的小开本旧皮面书。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：书平放、略斜，封面朝上，书脊朝向画面左侧；约二十乘十五厘米、厚约五厘米；封面四个角包着三角形的黄铜包角，一条黄铜搭扣从封底绕过来扣住封面；封面上压着一圈简单的回纹框，框内空白，没有任何文字或图案。\n材质与细节：深棕色的旧皮革，表面有细密的皱纹、磨亮的边角和几处褪色擦伤；书脊磨得起毛、露出一点底下的麻布；书页边缘泛黄、略微起伏；黄铜件发暗，凸起处被摸得发亮。整本书不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，封面文字，书名，烫金字，魔法光效，发光符文，翻开的书页，现代精装书，条形码",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:26.887+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "69cf20ed4c6e4cec8b5ab2cbc4ce98ba",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.png",
  "pid": 44952,
  "request_fingerprint": "103a27429496b767c839f601166b046b5e08120b804558ca49ad0b388ca0c30d",
  "time": "2026-10-18T01:28:26.887+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "pending"
  }
}
```

## 2026-10-18T01:28:26.893+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "77d77800a8b040ba850829bf21b7f07d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:26.893+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:27.534+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "77d77800a8b040ba850829bf21b7f07d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:27.534+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:31.563+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "02447edac1d2488ebd6cc2c033642e4b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:31.563+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:32.200+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "02447edac1d2488ebd6cc2c033642e4b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:32.200+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:36.241+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "ea4b73d132824db5913b5335341c6473",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:36.241+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:36.822+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "ea4b73d132824db5913b5335341c6473",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:36.822+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:40.833+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "27fc127e76e54e2a94dd180f7e776177",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:40.833+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:41.499+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "27fc127e76e54e2a94dd180f7e776177",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:41.499+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:45.526+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "ad327c1a8592473288276c88b4097237",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:45.526+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:46.470+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "ad327c1a8592473288276c88b4097237",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:46.470+00:00",
  "event": "result",
  "elapsed_s": 0.937,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:50.497+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "5c5e1e2eeb8649d0b934d8a9f7db6fde",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:50.497+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:51.108+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "5c5e1e2eeb8649d0b934d8a9f7db6fde",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:51.108+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:55.146+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "1d83b40cfe104967ab28e28d100758b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:55.146+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:55.768+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "1d83b40cfe104967ab28e28d100758b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:55.768+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:59.792+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "570b9aa3b6b945d6a5f98a2aa9826790",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:28:59.792+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:00.367+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "570b9aa3b6b945d6a5f98a2aa9826790",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:29:00.367+00:00",
  "event": "result",
  "elapsed_s": 0.579,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:04.373+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "3cef9f5c480440d9b4d48ee091b92020",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:29:04.373+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:05.185+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "3cef9f5c480440d9b4d48ee091b92020",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:29:05.185+00:00",
  "event": "result",
  "elapsed_s": 0.797,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:09.225+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — request

```json
{
  "request_id": "b75188c2ffac4f7883e12e19ad2b8cb2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:29:09.225+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/fJY0h8RnNcQw9abY1lak",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:10.599+00:00 — elevenlabs / GET /flows/image/fJY0h8RnNcQw9abY1lak — result

```json
{
  "request_id": "b75188c2ffac4f7883e12e19ad2b8cb2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/fJY0h8RnNcQw9abY1lak",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "80451fef8908ab25096ea7a62398748bc85bff6034a0202436eb20548268f2e6",
  "time": "2026-10-18T01:29:10.599+00:00",
  "event": "result",
  "elapsed_s": 1.344,
  "response": {
    "id": "fJY0h8RnNcQw9abY1lak",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/YJoI1okUbIy6G0gySDsk/fJY0h8RnNcQw9abY1lak/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012906Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:29:10.624+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "160e8ed12c244c919b24b08851916971",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "8c4eb9f3741c51ab9b2f754a0d857b64a376ea7d53522cb263062a5aaf094007",
  "time": "2026-10-18T01:29:10.624+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/YJoI1okUbIy6G0gySDsk/fJY0h8RnNcQw9abY1lak/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012906Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:29:13.778+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "160e8ed12c244c919b24b08851916971",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p11_Item_Tome\\p11_Item_Tome.part.png",
  "pid": 44952,
  "request_fingerprint": "8c4eb9f3741c51ab9b2f754a0d857b64a376ea7d53522cb263062a5aaf094007",
  "time": "2026-10-18T01:29:13.778+00:00",
  "event": "result",
  "elapsed_s": 3.125,
  "response": [
    200,
    {
      "bytes": 7387841,
      "sha256": "5ecad9ca3712b5909b97cba7d20703d7c52c9b331f396300dbe6cd3e58786612"
    }
  ]
}
```

## 2026-10-18T01:29:13.821+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "b4bb4547b8b84963b4b2ad01379e396b",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.png",
  "pid": 44952,
  "request_fingerprint": "e284f37065e9bf02968c0d1ba7ac1cef97f04f0d29a578e81c0ee11be21208be",
  "time": "2026-10-18T01:29:13.821+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一把弯刃短匕。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：匕首斜放，刃尖指向画面右上方；全长约三十厘米，刃身约十八厘米、略向上弯、单刃带一道窄血槽；护手是两片向刃尖方向弯起的弯月形小钢片；握柄缠着深紫色的皮绳，缠法紧密、有几处磨亮；柄尾是一个小小的钢帽，嵌着一颗指甲大的紫晶。\n材质与细节：刃身是暗色碳钢，表面有一层蓝紫色的回火光泽，像油膜一样随角度变色，刃口磨得雪亮；钢件有细小的划痕；紫晶半透明、不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，现代战术刀，折叠刀，霓虹紫光，发光刀刃，宝石镶满，夸张锯齿",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:14.527+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "b4bb4547b8b84963b4b2ad01379e396b",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.png",
  "pid": 44952,
  "request_fingerprint": "e284f37065e9bf02968c0d1ba7ac1cef97f04f0d29a578e81c0ee11be21208be",
  "time": "2026-10-18T01:29:14.527+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "pending"
  }
}
```

## 2026-10-18T01:29:14.566+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "19219c1bb52549b083242bad97784bdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:14.566+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:15.194+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "19219c1bb52549b083242bad97784bdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:15.194+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:19.227+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "6f1b7ef7a7e4428f940f34a501216d59",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:19.227+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:19.932+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "6f1b7ef7a7e4428f940f34a501216d59",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:19.932+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:23.954+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "8b9a279671054b93a60c4b3063c2a683",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:23.954+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:24.534+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "8b9a279671054b93a60c4b3063c2a683",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:24.534+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:28.565+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "70acc0c7cb9f4b789cebbd07cc49cc38",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:28.565+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:29.254+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "70acc0c7cb9f4b789cebbd07cc49cc38",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:29.254+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:33.277+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "ddd86b5c771f474093386d87626d0711",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:33.277+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:33.879+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "ddd86b5c771f474093386d87626d0711",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:33.879+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:37.914+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "a4ea1b08771e47e2a2d6bc4a275a5223",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:37.914+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:38.574+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "a4ea1b08771e47e2a2d6bc4a275a5223",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:38.574+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:42.598+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "b5d0d63cb8ec4af19dd5432b633b8622",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:42.598+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:43.150+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "b5d0d63cb8ec4af19dd5432b633b8622",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:43.150+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:47.186+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "8d9efc4ba10048b393509f6d3423dcb1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:47.186+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:47.766+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "8d9efc4ba10048b393509f6d3423dcb1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:47.766+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:51.801+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "8964833fb23a4f68adcb8fc089af8416",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:51.801+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:52.455+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "8964833fb23a4f68adcb8fc089af8416",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:52.455+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:56.484+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — request

```json
{
  "request_id": "d0535d6bf2a94e9ea47e316ade3ebf4d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:56.484+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x5AbIQ8CAH9XhPzMYTBg",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:57.355+00:00 — elevenlabs / GET /flows/image/x5AbIQ8CAH9XhPzMYTBg — result

```json
{
  "request_id": "d0535d6bf2a94e9ea47e316ade3ebf4d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x5AbIQ8CAH9XhPzMYTBg",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "1ae5f11a9030115842dd281864221e8008e62884684c918f6ec485026374d64c",
  "time": "2026-10-18T01:29:57.355+00:00",
  "event": "result",
  "elapsed_s": 0.844,
  "response": {
    "id": "x5AbIQ8CAH9XhPzMYTBg",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/mk7cXE68HAvQREcKZNFd/x5AbIQ8CAH9XhPzMYTBg/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012953Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:29:57.369+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "ee3dfbcf3be342ad9a36e9bfce2a30c1",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "84fff6b156a7498f93675cb1c37bb7af432342c30efadd1344512800a749ed70",
  "time": "2026-10-18T01:29:57.369+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/mk7cXE68HAvQREcKZNFd/x5AbIQ8CAH9XhPzMYTBg/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012953Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:29:59.761+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "ee3dfbcf3be342ad9a36e9bfce2a30c1",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p12_Kelens_Dagger\\p12_Kelens_Dagger.part.png",
  "pid": 44952,
  "request_fingerprint": "84fff6b156a7498f93675cb1c37bb7af432342c30efadd1344512800a749ed70",
  "time": "2026-10-18T01:29:59.761+00:00",
  "event": "result",
  "elapsed_s": 2.375,
  "response": [
    200,
    {
      "bytes": 5200806,
      "sha256": "05cde5efcb5c6a6ad2e25e5d2caa0dcdd2af80e8bdd931ab5fd96406c064ca17"
    }
  ]
}
```

## 2026-10-18T01:29:59.793+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "949bd954fd434734b9abbd643f445a36",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.png",
  "pid": 44952,
  "request_fingerprint": "1e0ca572a7fb20d2e3c6dbe19d1ab34b874601aaf872736cbd22b911df164696",
  "time": "2026-10-18T01:29:59.793+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一根木质长法杖。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：法杖斜放，杖头在画面右上、杖尾在左下，整根完整入画；全长约一米二，杖身笔直、比拇指略粗，表面被风蚀出一圈圈浅浅的螺旋纹；杖头是三根从杖身分出的弯曲木枝，向上收拢、像被风吹拢一样环抱着一块鸡蛋大的淡青色晶石；杖头下方用细皮绳系着四五根灰白色的长羽毛。\n材质与细节：浅色白蜡木，木纹清晰、被手握处磨得光滑发暗；晶石半透明，内部有絮状的白色纹理，不发光；羽毛有自然的分叉和磨损。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，金属权杖，骷髅杖头，霓虹发光晶石，龙卷风特效，宝石镶满",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:00.482+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "949bd954fd434734b9abbd643f445a36",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.png",
  "pid": 44952,
  "request_fingerprint": "1e0ca572a7fb20d2e3c6dbe19d1ab34b874601aaf872736cbd22b911df164696",
  "time": "2026-10-18T01:30:00.482+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "pending"
  }
}
```

## 2026-10-18T01:30:00.509+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "fa27175ff6c040da9ac5f080f8a95048",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:00.509+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:01.121+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "fa27175ff6c040da9ac5f080f8a95048",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:01.121+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "pending"
  }
}
```

## 2026-10-18T01:30:05.142+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "c5f9be2f6eb84424af6e12eb0b52ba7f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:05.142+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:05.774+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "c5f9be2f6eb84424af6e12eb0b52ba7f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:05.774+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:09.801+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "ebd94d0a21854f46808f7b1402ebb485",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:09.801+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:10.407+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "ebd94d0a21854f46808f7b1402ebb485",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:10.407+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:14.426+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "fa3394d982ef40d29ae5903a780089c6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:14.426+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:15.022+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "fa3394d982ef40d29ae5903a780089c6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:15.022+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:19.044+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "9d6bf291919748b3be89d46b2445b0af",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:19.044+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:19.731+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "9d6bf291919748b3be89d46b2445b0af",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:19.731+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:23.759+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "087246b43f474aa0b311c70b7c2f854d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:23.759+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:24.391+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "087246b43f474aa0b311c70b7c2f854d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:24.391+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:28.415+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "ca6a9a8c1ee04a1387db615cbc8b0832",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:28.415+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:29.046+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "ca6a9a8c1ee04a1387db615cbc8b0832",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:29.046+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:33.069+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "8b717b61443f4317a98570c4d40e3506",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:33.069+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:33.663+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "8b717b61443f4317a98570c4d40e3506",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:33.663+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:37.676+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — request

```json
{
  "request_id": "e0353adf49f643009e00974e057262f2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:37.676+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ZTw4ERhRAsPhPoZ2PsZr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:38.459+00:00 — elevenlabs / GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr — result

```json
{
  "request_id": "e0353adf49f643009e00974e057262f2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ZTw4ERhRAsPhPoZ2PsZr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "6ee4285e6cbea26842e5c670a8c58e7f45bcf4a13e0398ef579f25432d8ebe75",
  "time": "2026-10-18T01:30:38.459+00:00",
  "event": "result",
  "elapsed_s": 0.765,
  "response": {
    "id": "ZTw4ERhRAsPhPoZ2PsZr",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/l0X1hkTpBzBbTYgppQv4/ZTw4ERhRAsPhPoZ2PsZr/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013038Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:30:38.488+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "b612bff2d33e4ef988d86a0eca5daac3",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "f1387f34fd90415fb296778f8db97850e4b440d61d929fa5e7af0180f3a62277",
  "time": "2026-10-18T01:30:38.488+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/l0X1hkTpBzBbTYgppQv4/ZTw4ERhRAsPhPoZ2PsZr/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013038Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:30:40.685+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "b612bff2d33e4ef988d86a0eca5daac3",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p13_Euls_Scepter\\p13_Euls_Scepter.part.png",
  "pid": 44952,
  "request_fingerprint": "f1387f34fd90415fb296778f8db97850e4b440d61d929fa5e7af0180f3a62277",
  "time": "2026-10-18T01:30:40.685+00:00",
  "event": "result",
  "elapsed_s": 2.172,
  "response": [
    200,
    {
      "bytes": 4718701,
      "sha256": "cc781b54fea59a1a00b8e3520c4092b9acc51727e9653bcd6b2f6a37d6e8587f"
    }
  ]
}
```

## 2026-10-18T01:30:40.716+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "f1e0ebb8f1cb4186958a126db1b9bbe8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.png",
  "pid": 44952,
  "request_fingerprint": "3667270585a27b7668fbe0ddb1b394d7bb47aeb42d645f56342a95ca74c64380",
  "time": "2026-10-18T01:30:40.716+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一把月牙形单手弯刃。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：弯刃斜放，柄在左下、刃在右上；刃身长约六十厘米，从柄头向前伸出后向内弯成一道月牙，内侧是刃口、外侧是厚刃背，刃尖锐利；柄长约三十五厘米，硬木制，缠着一圈圈磨旧的深褐皮条，柄尾一个小铁环。\n材质与细节：刃身是暗色钢，表面有锻打的细纹和几处浅浅的锈点，刃口磨得雪亮；刃面沿着弧线蚀刻着一道细细的墨绿色藤蔓纹，颜色像渗进钢里；皮条有汗渍和磨损。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，农用长柄镰刀，死神镰刀，骷髅装饰，霓虹发光，宝石镶满",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:41.430+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "f1e0ebb8f1cb4186958a126db1b9bbe8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.png",
  "pid": 44952,
  "request_fingerprint": "3667270585a27b7668fbe0ddb1b394d7bb47aeb42d645f56342a95ca74c64380",
  "time": "2026-10-18T01:30:41.430+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:30:41.446+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "d047d6c50d1345f28250580041356e24",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:41.446+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:42.122+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "d047d6c50d1345f28250580041356e24",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:42.122+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:30:46.144+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "2138a7c8ec9c4d36b0fa1c06dd486480",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:46.144+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:46.783+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "2138a7c8ec9c4d36b0fa1c06dd486480",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:46.783+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:50.804+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "9cfd1be0f9a349de937c5b8f3c40c10a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:50.804+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:51.378+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "9cfd1be0f9a349de937c5b8f3c40c10a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:51.378+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:55.399+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "4c6c3fbff34f4b6fb0c9f2764cc8e903",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:55.399+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:55.945+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "4c6c3fbff34f4b6fb0c9f2764cc8e903",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:55.945+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:59.964+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "fa2df8a7accf46f3ab5fe38e29ec3940",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:30:59.964+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:00.527+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "fa2df8a7accf46f3ab5fe38e29ec3940",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:00.527+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:04.548+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "324e3981e62848b0a9ba7523c1ab0f03",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:04.548+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:05.168+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "324e3981e62848b0a9ba7523c1ab0f03",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:05.168+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:09.187+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "1796221c849e47e0a865ceb88c058fca",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:09.187+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:09.918+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "1796221c849e47e0a865ceb88c058fca",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:09.918+00:00",
  "event": "result",
  "elapsed_s": 0.718,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:13.935+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "5a3b3db3bedd484b98f8d124e60cfac7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:13.935+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:14.507+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "5a3b3db3bedd484b98f8d124e60cfac7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:14.507+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:18.533+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "7393f8be0f314b5fa84b756f259731c2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:18.533+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:19.079+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "7393f8be0f314b5fa84b756f259731c2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:19.079+00:00",
  "event": "result",
  "elapsed_s": 0.516,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:23.103+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — request

```json
{
  "request_id": "634d2da4bc464ca6a87f603021e3664f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:23.103+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l1EFb2o2r3KeQz685Mc7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:23.881+00:00 — elevenlabs / GET /flows/image/l1EFb2o2r3KeQz685Mc7 — result

```json
{
  "request_id": "634d2da4bc464ca6a87f603021e3664f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l1EFb2o2r3KeQz685Mc7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "48d3d8a9e99458bcb7301a6f2dd58f5df78ade5f12d38e364dad996487687ecc",
  "time": "2026-10-18T01:31:23.881+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "l1EFb2o2r3KeQz685Mc7",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/ctX5yU55n4iQEHOHnzlG/l1EFb2o2r3KeQz685Mc7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013120Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:31:23.900+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "6fd274f4e57d455fad1e553781540d36",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "40f51440cf7f738e451d92020365858c8024459231e1a5a26172c596fbfadae8",
  "time": "2026-10-18T01:31:23.900+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/ctX5yU55n4iQEHOHnzlG/l1EFb2o2r3KeQz685Mc7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013120Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:31:26.320+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "6fd274f4e57d455fad1e553781540d36",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p14_Scythe_of_Vyse\\p14_Scythe_of_Vyse.part.png",
  "pid": 44952,
  "request_fingerprint": "40f51440cf7f738e451d92020365858c8024459231e1a5a26172c596fbfadae8",
  "time": "2026-10-18T01:31:26.320+00:00",
  "event": "result",
  "elapsed_s": 2.407,
  "response": [
    200,
    {
      "bytes": 5776236,
      "sha256": "b835732e100d15d69389ddb29a8fbd39c455e7143e0f9e7bc0c441346e33b1ae"
    }
  ]
}
```

## 2026-10-18T01:31:26.345+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "d48bd0dc3ba546e7b0b2dd7a135a8a63",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.png",
  "pid": 44952,
  "request_fingerprint": "23e66e1e773ad75c6f41456c3f46ad644e2d9de4fa0bbacf14e46f4dbaac6412",
  "time": "2026-10-18T01:31:26.345+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一把双翼形刃的单手战斧。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：斧子斜放，斧头在右上、柄尾在左下；斧柄约六十厘米；斧头只有一面刃，刃口是一道宽阔的弧线，上下两角向后掠起，整片斧刃像一只张开双翼的鳐鱼，薄而锋利；斧刃中央开一个水滴形的减重孔；斧头背面是一个短短的方锤头。斧柄是深色硬木，握处缠着几道细银丝，柄尾一个钢帽。\n材质与细节：斧刃是带冷蓝灰色调的抛光钢，刃口磨亮、表面有细细的锻纹和几道划痕；银丝有磨损发暗处；木柄有手汗浸出的深色。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，双刃大斧，伐木斧，消防斧，霓虹发光，宝石镶满，夸张尖刺",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:27.023+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "d48bd0dc3ba546e7b0b2dd7a135a8a63",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.png",
  "pid": 44952,
  "request_fingerprint": "23e66e1e773ad75c6f41456c3f46ad644e2d9de4fa0bbacf14e46f4dbaac6412",
  "time": "2026-10-18T01:31:27.023+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:31:27.046+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "5e2c1d58aba741a48d1e15cc19539a68",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:27.046+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:27.643+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "5e2c1d58aba741a48d1e15cc19539a68",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:27.643+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:31:31.665+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "873a83d437cc4d14a046643fd1e7dffc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:31.665+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:32.233+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "873a83d437cc4d14a046643fd1e7dffc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:32.233+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:36.248+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "a6285e5aa5be41c19854bab1e017741b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:36.248+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:36.885+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "a6285e5aa5be41c19854bab1e017741b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:36.885+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:40.906+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "2e57de4104c14e6b96355fd7955b5556",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:40.906+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:41.651+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "2e57de4104c14e6b96355fd7955b5556",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:41.651+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:45.675+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "1e3c55f3cfca4cfdad7a1a5a47efa687",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:45.675+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:46.309+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "1e3c55f3cfca4cfdad7a1a5a47efa687",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:46.309+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:50.332+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "1ce42f495fae46af9737a70fc0a0e0c1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:50.332+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:50.961+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "1ce42f495fae46af9737a70fc0a0e0c1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:50.961+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:54.989+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "c7688c3708244e2db5872290519f455f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:54.989+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:55.643+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "c7688c3708244e2db5872290519f455f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:55.643+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:59.668+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "97e29a1be85945678956139840d0dfb6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:31:59.668+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:00.288+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "97e29a1be85945678956139840d0dfb6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:32:00.288+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:04.313+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "770f6e9b567449c8839acbb16fa5fed6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:32:04.313+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:04.976+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "770f6e9b567449c8839acbb16fa5fed6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:32:04.976+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:09.011+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — request

```json
{
  "request_id": "cd398360e764472bb05c6ab2824c8cc1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:32:09.011+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/YAiRw3ZDeYUi6c8pLvQV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:09.877+00:00 — elevenlabs / GET /flows/image/YAiRw3ZDeYUi6c8pLvQV — result

```json
{
  "request_id": "cd398360e764472bb05c6ab2824c8cc1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/YAiRw3ZDeYUi6c8pLvQV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "eb5442171a396d0f5b267b459b6c27dd7b214498d08c1e1b07385a28648f9efd",
  "time": "2026-10-18T01:32:09.877+00:00",
  "event": "result",
  "elapsed_s": 0.859,
  "response": {
    "id": "YAiRw3ZDeYUi6c8pLvQV",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/dBB0b4s2C1rudBpwaoau/YAiRw3ZDeYUi6c8pLvQV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013207Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:32:09.914+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "83bec967ce514bf3bba832fad6b91d46",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "ca40af4946ccf97a98b222daec17e4a15e69f0f516faa476ea7b468a1c99de76",
  "time": "2026-10-18T01:32:09.914+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/dBB0b4s2C1rudBpwaoau/YAiRw3ZDeYUi6c8pLvQV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013207Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:32:13.504+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "83bec967ce514bf3bba832fad6b91d46",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p15_Manta_Style\\p15_Manta_Style.part.png",
  "pid": 44952,
  "request_fingerprint": "ca40af4946ccf97a98b222daec17e4a15e69f0f516faa476ea7b468a1c99de76",
  "time": "2026-10-18T01:32:13.504+00:00",
  "event": "result",
  "elapsed_s": 3.578,
  "response": [
    200,
    {
      "bytes": 5502117,
      "sha256": "ad04328f7728e39d1f39c4a19fd1433374a559039204599aa98bf704c9c47f3e"
    }
  ]
}
```

## 2026-10-18T01:32:13.544+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "e29c7f932ae044fb92a236fa894e4e38",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.png",
  "pid": 44952,
  "request_fingerprint": "73bdd8f4de31367c317621c22e5818baf4eb1b9655773f7c2900282771acd224",
  "time": "2026-10-18T01:32:13.544+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一件结霜的板甲胸甲。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：胸甲立放在一个看不见的支架上，正面朝向画面略偏左；约六十厘米高，前胸一整片弧形板，下接三片可活动的腹甲叠板，两肩各有一个圆弧形的护肩连接扣；胸口正中是一枚手掌大的六角雪花形浮雕，花心镶一颗浅冰蓝色的晶石；甲缘一圈向外翻的卷边上结着一层细小的冰晶。\n材质与细节：钢面带冷白蓝色调，表面像蒙着一层薄霜，霜在凹处更厚、凸处被磨掉露出钢光；铆钉与皮扣是旧皮和铁；晶石半透明、内部有冰裂纹，不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，人台模特，人体，头盔，整套盔甲，霓虹蓝光，冰块雕塑，塑料冰，夸张尖刺",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:14.244+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "e29c7f932ae044fb92a236fa894e4e38",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.png",
  "pid": 44952,
  "request_fingerprint": "73bdd8f4de31367c317621c22e5818baf4eb1b9655773f7c2900282771acd224",
  "time": "2026-10-18T01:32:14.244+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "pending"
  }
}
```

## 2026-10-18T01:32:14.275+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "708037927b324cf7aadba4128bf403c8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:14.275+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:14.917+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "708037927b324cf7aadba4128bf403c8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:14.917+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:18.945+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "39175254c58647c09d9f078764a24ccf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:18.945+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:19.588+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "39175254c58647c09d9f078764a24ccf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:19.588+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:23.631+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "f126097a8c5c42679b12298cfa6e46dc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:23.631+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:24.236+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "f126097a8c5c42679b12298cfa6e46dc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:24.236+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:28.272+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "faaa7af2509b4f0d9353724aa10ddade",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:28.272+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:30.023+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "faaa7af2509b4f0d9353724aa10ddade",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:30.023+00:00",
  "event": "result",
  "elapsed_s": 1.735,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:34.049+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "4df792707eeb4784b8af0905762341c2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:34.049+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:34.772+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "4df792707eeb4784b8af0905762341c2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:34.772+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:38.813+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "d33e508d896e42dc925e5280f2f4158f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:38.813+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:39.482+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "d33e508d896e42dc925e5280f2f4158f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:39.482+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:43.520+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "ce96c26d21974a1e83524e6c70999524",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:43.520+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:44.195+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "ce96c26d21974a1e83524e6c70999524",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:44.195+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:48.227+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "1bbf863914c34db9a1cc733338e1db9c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:48.227+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:48.870+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "1bbf863914c34db9a1cc733338e1db9c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:48.870+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:52.894+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "e42a25ce5d3a4f8e9f2f1ae0e386b923",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:52.894+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:53.515+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "e42a25ce5d3a4f8e9f2f1ae0e386b923",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:53.515+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:57.549+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "96c98d163a31499caea94fe5c5619d02",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:57.549+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:58.181+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "96c98d163a31499caea94fe5c5619d02",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:32:58.181+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:02.220+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — request

```json
{
  "request_id": "0bcb6e64b9c54d46b4e8dd35bcfd95c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:33:02.220+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X8RvmSanJPa0aBFToIYa",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:04.371+00:00 — elevenlabs / GET /flows/image/X8RvmSanJPa0aBFToIYa — result

```json
{
  "request_id": "0bcb6e64b9c54d46b4e8dd35bcfd95c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X8RvmSanJPa0aBFToIYa",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "60a0aed118694e78dc974a13f0dfab057c62964535bcae456ca93046534b6e04",
  "time": "2026-10-18T01:33:04.371+00:00",
  "event": "result",
  "elapsed_s": 2.125,
  "response": {
    "id": "X8RvmSanJPa0aBFToIYa",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/swss3uLI67eSI7hesPkF/X8RvmSanJPa0aBFToIYa/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013259Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:33:04.400+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "604441d9b0d8426fada046e259039a91",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "57c42cd85c91e85f0d2ca72f8992a485c975f52435fc40a484513e747d1b4968",
  "time": "2026-10-18T01:33:04.400+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/swss3uLI67eSI7hesPkF/X8RvmSanJPa0aBFToIYa/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013259Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:33:07.049+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "604441d9b0d8426fada046e259039a91",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p16_Shivas_Guard\\p16_Shivas_Guard.part.png",
  "pid": 44952,
  "request_fingerprint": "57c42cd85c91e85f0d2ca72f8992a485c975f52435fc40a484513e747d1b4968",
  "time": "2026-10-18T01:33:07.049+00:00",
  "event": "result",
  "elapsed_s": 2.609,
  "response": [
    200,
    {
      "bytes": 6817959,
      "sha256": "aa5585ef02ae1f2debfd22b5aa8ae3dcf85210d5cd1422db91f455d5f3e9d098"
    }
  ]
}
```

## 2026-10-18T01:33:07.101+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "f954081b14644c18a74c80de20e9885e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.png",
  "pid": 44952,
  "request_fingerprint": "a145164e81638ef591d6b9754cecabe5a6e901c4a23c989e662504e966902c45",
  "time": "2026-10-18T01:33:07.101+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一只镀金的右手铠甲手套。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：手套手背朝上、手指微微弯曲地平放，略斜，指尖朝向画面右上方；手背由几片弧形的薄甲片从腕口一路叠到指根，每根手指是三四节可活动的小甲片；掌心朝下看不见，只在侧面露出一角圆形金章的边缘；腕口是一圈深红色的皮衬，边缘有一排小铆钉。\n材质与细节：甲片是镀金的薄钢，金色温暖而不刺眼，凸起处磨得发亮、露出一点底下的钢色，凹缝里积着暗色污垢；铆钉是黄铜；皮衬有褶皱和汗渍。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，手，人体，现代手套，拳击手套，霓虹金光，夸张金光，宝石镶满，骷髅",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:08.434+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "f954081b14644c18a74c80de20e9885e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.png",
  "pid": 44952,
  "request_fingerprint": "a145164e81638ef591d6b9754cecabe5a6e901c4a23c989e662504e966902c45",
  "time": "2026-10-18T01:33:08.434+00:00",
  "event": "result",
  "elapsed_s": 1.297,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:33:08.459+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "0d1f77bf3fbf4ed98345662d9f28c725",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:08.459+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:09.101+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "0d1f77bf3fbf4ed98345662d9f28c725",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:09.101+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:33:13.132+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "e14bc5ce8d4d4154af250486f985168c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:13.132+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:13.788+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "e14bc5ce8d4d4154af250486f985168c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:13.788+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:17.812+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "a08b9ccc47814e0e9f88136550dd598d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:17.812+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:18.440+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "a08b9ccc47814e0e9f88136550dd598d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:18.440+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:22.461+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "7c551e247fd54bfe8a47a9c3c5b15977",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:22.461+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:23.131+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "7c551e247fd54bfe8a47a9c3c5b15977",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:23.131+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:27.157+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "a8131071412647ec8ca0689ba10f2612",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:27.157+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:27.784+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "a8131071412647ec8ca0689ba10f2612",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:27.784+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:31.814+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "d25c5ae7f0fe4e609e2d59d56f4f40ce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:31.814+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:32.432+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "d25c5ae7f0fe4e609e2d59d56f4f40ce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:32.432+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:36.462+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "3f5d72275ad74561ba0ae4146f6b7873",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:36.462+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:37.070+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "3f5d72275ad74561ba0ae4146f6b7873",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:37.070+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:41.108+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "875e25cb1b1d4abc8a1cc9e1b70551ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:41.108+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:41.722+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "875e25cb1b1d4abc8a1cc9e1b70551ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:41.722+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:45.744+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "626d844f24b5452a9216d8d390d68050",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:45.744+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:46.403+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "626d844f24b5452a9216d8d390d68050",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:46.403+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:50.432+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — request

```json
{
  "request_id": "e595c56c4265470da92e73db4740006a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:50.432+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TlaooLUZhYNv67WqziW7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:51.179+00:00 — elevenlabs / GET /flows/image/TlaooLUZhYNv67WqziW7 — result

```json
{
  "request_id": "e595c56c4265470da92e73db4740006a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TlaooLUZhYNv67WqziW7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "40a0dc47cdfc34f31962dafc112cccb0608fee828a4a932227ccde5bb82eb593",
  "time": "2026-10-18T01:33:51.179+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "TlaooLUZhYNv67WqziW7",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/FRPT8iZ7l8BW0w3smsu3/TlaooLUZhYNv67WqziW7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013349Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:33:51.217+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "b2c57628da8145938c2df4fb018607d8",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "ef501ec98c8a32d76c0cc4411aabbbb5b7205c3b3068c1e8b2d481d2fa07342d",
  "time": "2026-10-18T01:33:51.217+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/FRPT8iZ7l8BW0w3smsu3/TlaooLUZhYNv67WqziW7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013349Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:33:53.609+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "b2c57628da8145938c2df4fb018607d8",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p17_Hand_of_Midas\\p17_Hand_of_Midas.part.png",
  "pid": 44952,
  "request_fingerprint": "ef501ec98c8a32d76c0cc4411aabbbb5b7205c3b3068c1e8b2d481d2fa07342d",
  "time": "2026-10-18T01:33:53.609+00:00",
  "event": "result",
  "elapsed_s": 2.359,
  "response": [
    200,
    {
      "bytes": 6338513,
      "sha256": "98cad6220c6124ee8c16044175cbe0708f049c0f0c95012fa9eedb5ab13e8f6e"
    }
  ]
}
```

## 2026-10-18T01:33:53.653+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "b40d581ec81f4f5e9b3ca40169ad1528",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.png",
  "pid": 44952,
  "request_fingerprint": "f30195caa6e744f56ded04ac2ec8bae24bdf26d797843ee9672e34d91b468392",
  "time": "2026-10-18T01:33:53.653+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一根黑色短权杖。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：权杖斜放，杖头在右上、杖尾在左下，整根完整入画；全长约七十厘米，杖身是一根略带锥度的乌黑金属棒，表面刻着几道环形凹槽；杖头是一枚拳头大的黑色多面晶石，被四根暗金色的箍条从下往上抱住、在顶端汇成一个小尖；握柄一段缠着黑色皮条；杖尾一个暗金色的圆帽。\n材质与细节：杖身是发乌的黑铁，带细密的锤纹和磨亮的手握处；晶石漆黑、切面反着冷光；暗金箍有旧金的哑光和划痕；皮条有磨损。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，长法杖，骷髅杖头，霓虹发光，夸张金光，宝石镶满，现代警棍",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:54.380+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "b40d581ec81f4f5e9b3ca40169ad1528",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.png",
  "pid": 44952,
  "request_fingerprint": "f30195caa6e744f56ded04ac2ec8bae24bdf26d797843ee9672e34d91b468392",
  "time": "2026-10-18T01:33:54.380+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "pending"
  }
}
```

## 2026-10-18T01:33:54.405+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "9a4241924722477fa6930a05e53e7985",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:33:54.405+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:55.034+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "9a4241924722477fa6930a05e53e7985",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:33:55.034+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:59.074+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "1b4bcb3518ef4ed2a45733072db8c7e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:33:59.074+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:59.702+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "1b4bcb3518ef4ed2a45733072db8c7e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:33:59.702+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:03.733+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "0bf6e9f658a04dbb8c4d4aa9cd4c89cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:03.733+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:04.388+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "0bf6e9f658a04dbb8c4d4aa9cd4c89cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:04.388+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:08.416+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "181ca7fd4f1740c88bb55cfe31851de9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:08.416+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:09.086+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "181ca7fd4f1740c88bb55cfe31851de9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:09.086+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:13.106+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "bb43603221af49de939e5a08385a3afa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:13.106+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:13.695+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "bb43603221af49de939e5a08385a3afa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:13.695+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:17.728+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "df26c360ed3a4202bbe2645e85e06d85",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:17.728+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:18.368+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "df26c360ed3a4202bbe2645e85e06d85",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:18.368+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:22.409+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "2d5b79ec826e4373a20f82949e864542",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:22.409+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:23.020+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "2d5b79ec826e4373a20f82949e864542",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:23.020+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:27.060+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "4fae491c721649338d6f1f79c9ef7bce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:27.060+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:28.164+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "4fae491c721649338d6f1f79c9ef7bce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:28.164+00:00",
  "event": "result",
  "elapsed_s": 1.078,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:32.193+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — request

```json
{
  "request_id": "27daa12d259b45e299ca50a57c17317e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:32.193+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ITznwqe1aBNiWjooUfJp",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:32.993+00:00 — elevenlabs / GET /flows/image/ITznwqe1aBNiWjooUfJp — result

```json
{
  "request_id": "27daa12d259b45e299ca50a57c17317e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ITznwqe1aBNiWjooUfJp",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "6fecc38b07d922b00a6f7eaeeecd67f5977b91edbad26af25bfec1f3c4837e81",
  "time": "2026-10-18T01:34:32.993+00:00",
  "event": "result",
  "elapsed_s": 0.766,
  "response": {
    "id": "ITznwqe1aBNiWjooUfJp",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/zxIQnp8KNqCGFZyFoprB/ITznwqe1aBNiWjooUfJp/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013431Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:34:33.022+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "26ee53e8eb914317a11e7d744b3a378c",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "040aa1ebcbe402d4bfdcfdc55ccdf715ece2839e52655c174e3ed0e4ffd49e99",
  "time": "2026-10-18T01:34:33.022+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/zxIQnp8KNqCGFZyFoprB/ITznwqe1aBNiWjooUfJp/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013431Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:34:35.118+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "26ee53e8eb914317a11e7d744b3a378c",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p18_Black_King_Bar\\p18_Black_King_Bar.part.png",
  "pid": 44952,
  "request_fingerprint": "040aa1ebcbe402d4bfdcfdc55ccdf715ece2839e52655c174e3ed0e4ffd49e99",
  "time": "2026-10-18T01:34:35.118+00:00",
  "event": "result",
  "elapsed_s": 2.079,
  "response": [
    200,
    {
      "bytes": 4786955,
      "sha256": "de6543de629613b948b56bca315e5dc42cc8d8883b87bb43cda5cb03c7ea59e5"
    }
  ]
}
```

## 2026-10-18T01:34:35.170+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "d14c24b7be9e4d0d807496d40f937bbb",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.png",
  "pid": 44952,
  "request_fingerprint": "d50be5fc84a9981199201966bf125028249ab43e780bdab43659e016a98746f0",
  "time": "2026-10-18T01:34:35.170+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一枚嵌火色宝石的金护身符。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：护身符平放、略斜，金链在它上方松松地盘成一个弧；护身符约八厘米宽，外框是镂空的金丝，编成一圈像火舌一样向外卷的纹样，中央托着一颗鸽蛋大的椭圆宝石，用四个小爪扣住；顶端一个粗金环连着链子，链子是手工打的粗链环。\n材质与光：金框是温暖的旧金，有细小的划痕和凹处的暗色；宝石金红色、深处偏暗红，内部有一缕缓缓翻滚的亮橙色光，像封在里面的一小团火，亮度克制，只照亮宝石本身和金框内侧一点点。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，火焰特效，燃烧，霓虹发光，夸张金光，现代首饰，钻石切面闪光，心形",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:35.882+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "d14c24b7be9e4d0d807496d40f937bbb",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.png",
  "pid": 44952,
  "request_fingerprint": "d50be5fc84a9981199201966bf125028249ab43e780bdab43659e016a98746f0",
  "time": "2026-10-18T01:34:35.882+00:00",
  "event": "result",
  "elapsed_s": 0.687,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "pending"
  }
}
```

## 2026-10-18T01:34:35.906+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "90ce6702cea347408d1f780572ee078f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:35.906+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:36.564+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "90ce6702cea347408d1f780572ee078f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:36.564+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:40.585+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "0df342ccc48b4c019dc95aed2743eb65",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:40.585+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:41.230+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "0df342ccc48b4c019dc95aed2743eb65",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:41.230+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:45.279+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "88f1ef9cb6ca4c63864382d1afcc2a14",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:45.279+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:45.922+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "88f1ef9cb6ca4c63864382d1afcc2a14",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:45.922+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:49.966+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "69c598d4a1904a8eb7f8774d2d2a5c65",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:49.966+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:50.590+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "69c598d4a1904a8eb7f8774d2d2a5c65",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:50.590+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:54.624+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "67c8b71a06744797962087a808237802",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:54.624+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:55.251+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "67c8b71a06744797962087a808237802",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:55.251+00:00",
  "event": "result",
  "elapsed_s": 0.579,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:59.285+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "3c5a5f20a5954cb3bbca74917123a72a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:34:59.285+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:00.020+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "3c5a5f20a5954cb3bbca74917123a72a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:00.020+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:04.049+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "c10ed104fcdf4f35982f748d194ceec3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:04.049+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:04.842+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "c10ed104fcdf4f35982f748d194ceec3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:04.842+00:00",
  "event": "result",
  "elapsed_s": 0.765,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:08.879+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "2d217cd966084673afc2bd7dc392e379",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:08.879+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:09.638+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "2d217cd966084673afc2bd7dc392e379",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:09.638+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:13.664+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "a23eb50544004db2b171274ce0ec34cf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:13.664+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:14.365+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "a23eb50544004db2b171274ce0ec34cf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:14.365+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:18.388+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "92ce8c44e89d4041aa09927626e2dcdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:18.388+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:19.016+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "92ce8c44e89d4041aa09927626e2dcdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:19.016+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:23.039+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — request

```json
{
  "request_id": "320950b68ff3478b8bd15f33d51cd959",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:23.039+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1FO127mhlUyU1JmxvbvA",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:23.878+00:00 — elevenlabs / GET /flows/image/1FO127mhlUyU1JmxvbvA — result

```json
{
  "request_id": "320950b68ff3478b8bd15f33d51cd959",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1FO127mhlUyU1JmxvbvA",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "a2832420a5127151e6f32e01a7d5545d417a56616d37b40e1ad05594a80ecd86",
  "time": "2026-10-18T01:35:23.878+00:00",
  "event": "result",
  "elapsed_s": 0.828,
  "response": {
    "id": "1FO127mhlUyU1JmxvbvA",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/l4IUtxx9RYLnZRZdynX4/1FO127mhlUyU1JmxvbvA/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013520Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:35:23.893+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "fd0d9e829b93408b9efdbc531de3cfbf",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "954c2a7fafb8e22ac8c58281ad9d7fea4969566b46b85ae8903801d3de67f0d6",
  "time": "2026-10-18T01:35:23.893+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/l4IUtxx9RYLnZRZdynX4/1FO127mhlUyU1JmxvbvA/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013520Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:35:26.766+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "fd0d9e829b93408b9efdbc531de3cfbf",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p19_Radiance\\p19_Radiance.part.png",
  "pid": 44952,
  "request_fingerprint": "954c2a7fafb8e22ac8c58281ad9d7fea4969566b46b85ae8903801d3de67f0d6",
  "time": "2026-10-18T01:35:26.766+00:00",
  "event": "result",
  "elapsed_s": 2.844,
  "response": [
    200,
    {
      "bytes": 7028236,
      "sha256": "072cf10773050aa4d1cd4f2c0452c4244868cadd75557b243a6af3099e2f34d0"
    }
  ]
}
```

## 2026-10-18T01:35:26.799+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "073272fe5435495fad05dbcaece74f99",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.png",
  "pid": 44952,
  "request_fingerprint": "94a28edb1b8b398a73161998da0aef8647b4b338171d943cd8e1cb419732119a",
  "time": "2026-10-18T01:35:26.799+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一块会发光的红色符石。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一块约三十厘米高的竖立椭圆形黑色符石，像从河里捞起的卵石被凿成一块厚符板，表面打磨得光滑、边缘留着一圈粗凿的原石面；正面刻着一个由螺旋与放射线组成的符纹，刻槽深而利落；背面平整、同样打磨光滑。符石悬在半空、离背景地面约一掌高，下方背景上落着一小圈红色的柔和光晕。\n材质与光：石体是致密的黑色玄武岩，打磨面有细小的气孔与天然纹理；鲜红色的光从刻槽深处和石体内部透出来，中心最亮、向边缘渐暗，亮度克制、刻槽边缘清晰不过曝；光只照亮符石自身和下方那一小圈，不照亮整个背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，橙色，黄色，宝石切面，水晶塑料感，霓虹灯管，平面光效贴图，字母刻字",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:27.478+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "073272fe5435495fad05dbcaece74f99",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.png",
  "pid": 44952,
  "request_fingerprint": "94a28edb1b8b398a73161998da0aef8647b4b338171d943cd8e1cb419732119a",
  "time": "2026-10-18T01:35:27.478+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "pending"
  }
}
```

## 2026-10-18T01:35:27.502+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "21d4fb97ecd448c6a5522d9cf51e2165",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:27.502+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:28.171+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "21d4fb97ecd448c6a5522d9cf51e2165",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:28.171+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "pending"
  }
}
```

## 2026-10-18T01:35:32.186+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "345632e92550401fb56c8e51a0db741a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:32.186+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:32.823+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "345632e92550401fb56c8e51a0db741a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:32.823+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:36.846+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "538fd2dfc6d04033b68e218a430612ed",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:36.846+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:37.480+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "538fd2dfc6d04033b68e218a430612ed",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:37.480+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:41.510+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "0cb992adcad34a5883bc9ce366d5e544",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:41.510+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:42.146+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "0cb992adcad34a5883bc9ce366d5e544",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:42.146+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:46.170+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "566b6d21f6e944b68a55f994443f2399",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:46.170+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:46.815+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "566b6d21f6e944b68a55f994443f2399",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:46.815+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:50.838+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "f30895d0e8e4460daa38cb947f3e5bfa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:50.838+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:51.533+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "f30895d0e8e4460daa38cb947f3e5bfa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:51.533+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:55.551+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "558a7cd5c8dc4ac1bf1505528bbb7b00",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:55.551+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:56.185+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "558a7cd5c8dc4ac1bf1505528bbb7b00",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:35:56.185+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:00.220+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "b99e4d997e4f42019c80acff4ca6f5a5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:00.220+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:00.844+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "b99e4d997e4f42019c80acff4ca6f5a5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:00.844+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:04.873+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "e649735bd6a64331babb62c8c55b3499",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:04.873+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:05.487+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "e649735bd6a64331babb62c8c55b3499",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:05.487+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:09.513+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — request

```json
{
  "request_id": "e81db668753542b9a0b8ee98b07596b1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:09.513+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/l9VM1XLg4qiNWJhTdVQi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:10.420+00:00 — elevenlabs / GET /flows/image/l9VM1XLg4qiNWJhTdVQi — result

```json
{
  "request_id": "e81db668753542b9a0b8ee98b07596b1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/l9VM1XLg4qiNWJhTdVQi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "e0db6c8123a003966bb5c94ce8ffcc22818480039170de340b07b717a84d1be1",
  "time": "2026-10-18T01:36:10.420+00:00",
  "event": "result",
  "elapsed_s": 0.875,
  "response": {
    "id": "l9VM1XLg4qiNWJhTdVQi",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/chvfCwjeQBr5CbToAPXL/l9VM1XLg4qiNWJhTdVQi/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013606Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:36:10.454+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "90c5bae5e8f04f368a19f7fbfde6bf21",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "6e4f27d3adbdd44f4b3c3371f4d70ad4909e1cddc1351f0a9d80e36042c11934",
  "time": "2026-10-18T01:36:10.454+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/chvfCwjeQBr5CbToAPXL/l9VM1XLg4qiNWJhTdVQi/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013606Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:36:12.875+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "90c5bae5e8f04f368a19f7fbfde6bf21",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p1_Haste_Rune\\p1_Haste_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "6e4f27d3adbdd44f4b3c3371f4d70ad4909e1cddc1351f0a9d80e36042c11934",
  "time": "2026-10-18T01:36:12.875+00:00",
  "event": "result",
  "elapsed_s": 2.407,
  "response": [
    200,
    {
      "bytes": 5932485,
      "sha256": "2bcd558e8d30ea457a763c632ef2bee15efe90d558ca9ee77c1fe6a77bf63d70"
    }
  ]
}
```

## 2026-10-18T01:36:12.914+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "6435c405002e41ce912fdce2ebd5db40",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.png",
  "pid": 44952,
  "request_fingerprint": "dfcd65c49d317286bd21fd73e3bee796b93f08c907f46959ea01219d46c9a73f",
  "time": "2026-10-18T01:36:12.914+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一柄双面新月刃的双手战斧。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：战斧斜放，斧头在右上、柄尾在左下，整柄完整入画；长柄约一米三，硬木制；斧头左右各一片新月形的宽刃，对称展开，刃宽约三十厘米，刃口雪亮；两片刃在中央由一圈黑铁箍和六颗大铆钉固定在柄上，箍顶伸出一个短矛尖；柄的中段与末段各缠一段防滑皮条，柄尾一个铁帽。\n材质与细节：斧刃是锻钢，刃面有锻打的波纹、几处缺口和划痕，刃口磨得发亮；黑铁箍发乌、带锈点；皮条被汗浸成深色。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，单刃伐木斧，消防斧，霓虹发光，火焰，宝石镶满，夸张尖刺，骷髅装饰",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:13.679+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "6435c405002e41ce912fdce2ebd5db40",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.png",
  "pid": 44952,
  "request_fingerprint": "dfcd65c49d317286bd21fd73e3bee796b93f08c907f46959ea01219d46c9a73f",
  "time": "2026-10-18T01:36:13.679+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:36:13.702+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "9d20023d55eb4b7d8c68a6b73ee201d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:13.702+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:14.554+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "9d20023d55eb4b7d8c68a6b73ee201d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:14.554+00:00",
  "event": "result",
  "elapsed_s": 0.828,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "pending"
  }
}
```

## 2026-10-18T01:36:18.576+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "0b024790ec0a4d6bb6be385e19c5f884",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:18.576+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:19.191+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "0b024790ec0a4d6bb6be385e19c5f884",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:19.191+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:23.210+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "7b984426571948009f155a01c0171252",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:23.210+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:23.883+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "7b984426571948009f155a01c0171252",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:23.883+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:27.911+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "0a611e5149fb46ca8248ff771b25d354",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:27.911+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:28.493+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "0a611e5149fb46ca8248ff771b25d354",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:28.493+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:32.520+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "ab983771cf344ee29473f6cb7123fac2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:32.520+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:33.155+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "ab983771cf344ee29473f6cb7123fac2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:33.155+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:37.189+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "1fa6704c040447e3b5d35d90a6e5412d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:37.189+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:37.787+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "1fa6704c040447e3b5d35d90a6e5412d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:37.787+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:41.803+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "e585a0974d1d4295a31350d1d8837d57",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:41.803+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:42.381+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "e585a0974d1d4295a31350d1d8837d57",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:42.381+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:46.385+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "a7b5722361e2463e9276968d62cc24ec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:46.385+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:47.040+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "a7b5722361e2463e9276968d62cc24ec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:47.040+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:51.065+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "4f82d735036149bd9d56def410e03fda",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:51.065+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:51.610+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "4f82d735036149bd9d56def410e03fda",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:51.610+00:00",
  "event": "result",
  "elapsed_s": 0.531,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:55.613+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "2c093f32d726475da65d212ea34e3886",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:55.613+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:56.209+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "2c093f32d726475da65d212ea34e3886",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:36:56.209+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:00.232+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — request

```json
{
  "request_id": "2c55d2bfc167400aa15594088b25e5f3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:37:00.232+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/KIYdsUr5cqTJA4gIcyF7",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:00.960+00:00 — elevenlabs / GET /flows/image/KIYdsUr5cqTJA4gIcyF7 — result

```json
{
  "request_id": "2c55d2bfc167400aa15594088b25e5f3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/KIYdsUr5cqTJA4gIcyF7",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "bdf6c60271044258941cf43446c647d625de3baa918b7e7d2bf5bab6696c23b8",
  "time": "2026-10-18T01:37:00.960+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "KIYdsUr5cqTJA4gIcyF7",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/YgBux5Q816rFfut5Toa8/KIYdsUr5cqTJA4gIcyF7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013658Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:37:00.976+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "6f4352f0f98044ad969e9033ddfe7720",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "aed722650f7f6e7a3f42f9ea61229ae1e28b3a1e2a38ab24a33832b817f00e89",
  "time": "2026-10-18T01:37:00.976+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/YgBux5Q816rFfut5Toa8/KIYdsUr5cqTJA4gIcyF7/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013658Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:37:03.205+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "6f4352f0f98044ad969e9033ddfe7720",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p20_Battle_Fury\\p20_Battle_Fury.part.png",
  "pid": 44952,
  "request_fingerprint": "aed722650f7f6e7a3f42f9ea61229ae1e28b3a1e2a38ab24a33832b817f00e89",
  "time": "2026-10-18T01:37:03.205+00:00",
  "event": "result",
  "elapsed_s": 2.218,
  "response": [
    200,
    {
      "bytes": 6956526,
      "sha256": "07349887cd723626e6c291002dbba358934c239274a9b19b4a41f080c14d2951"
    }
  ]
}
```

## 2026-10-18T01:37:03.228+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "67a0b33157f1400abc2a02ef0b9721d5",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.png",
  "pid": 44952,
  "request_fingerprint": "2b41cd0dc198b73446e3424f57e3e7b1007bfa2e743b7578beb8374998d464ff",
  "time": "2026-10-18T01:37:03.228+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一颗放在三爪铜座上的水晶球。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：水晶球直径约九厘米，完美的圆；下面是一只约五厘米高的青铜小座，三只弯爪从座底伸上来轻轻扣住球的下半部；座底是一个圆形小台，边缘一圈细绳纹。\n材质与光：水晶透明无瑕，边缘有清晰的折射和背景的倒影；球内悬着一团青蓝色的雾，雾呈缓慢的螺旋，中心略亮、透出一点柔和的青蓝微光，亮度克制，只让球体本身发亮，不照亮背景；青铜座发暗、凹处有绿锈，爪尖被摸得发亮。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，占卜师水晶球摊，玻璃弹珠，霓虹发光，闪电特效，宝石切面，现代灯具",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:03.911+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "67a0b33157f1400abc2a02ef0b9721d5",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.png",
  "pid": 44952,
  "request_fingerprint": "2b41cd0dc198b73446e3424f57e3e7b1007bfa2e743b7578beb8374998d464ff",
  "time": "2026-10-18T01:37:03.911+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "pending"
  }
}
```

## 2026-10-18T01:37:03.926+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "605a39ed2abc42a0b278118e5009b195",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:03.926+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:04.524+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "605a39ed2abc42a0b278118e5009b195",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:04.524+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "pending"
  }
}
```

## 2026-10-18T01:37:08.553+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "98edfa6b8a4d4b6d9d54ca38955cd1ec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:08.553+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:09.191+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "98edfa6b8a4d4b6d9d54ca38955cd1ec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:09.191+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:13.219+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "99b42d4f07714c738c764dbab47f52a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:13.219+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:13.805+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "99b42d4f07714c738c764dbab47f52a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:13.805+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:17.831+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "faa8e0cd7203482aa5db15fe69bd081c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:17.831+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:18.450+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "faa8e0cd7203482aa5db15fe69bd081c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:18.450+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:22.469+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "cc81a0af0a484059a59a612254d7fb24",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:22.469+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:23.246+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "cc81a0af0a484059a59a612254d7fb24",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:23.246+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:27.268+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "dfeb404211de4d128dabdbc88140e9ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:27.268+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:27.938+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "dfeb404211de4d128dabdbc88140e9ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:27.938+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:31.963+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "ba1bc4513f2441d2add522719e7f4e34",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:31.963+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:32.606+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "ba1bc4513f2441d2add522719e7f4e34",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:32.606+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:36.636+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "52796fedc6d04445bf17dd48dd4fa5bb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:36.636+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:37.296+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "52796fedc6d04445bf17dd48dd4fa5bb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:37.296+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:41.326+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "04589702c80a419c96c8f9e568ff3e50",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:41.326+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:41.968+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "04589702c80a419c96c8f9e568ff3e50",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:41.968+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:45.993+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — request

```json
{
  "request_id": "a4a15d76196e41f8a2536e82e73e3937",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:45.993+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/3Z1L1wLck9wEb7m3i20h",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:46.819+00:00 — elevenlabs / GET /flows/image/3Z1L1wLck9wEb7m3i20h — result

```json
{
  "request_id": "a4a15d76196e41f8a2536e82e73e3937",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/3Z1L1wLck9wEb7m3i20h",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "27f8b6a6a2573f6a8c9b5627c7f4719a8d2ca5e19494d4419db078d25f6ad4db",
  "time": "2026-10-18T01:37:46.819+00:00",
  "event": "result",
  "elapsed_s": 0.797,
  "response": {
    "id": "3Z1L1wLck9wEb7m3i20h",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/f5iFWc6FlTUFPGmsX5M5/3Z1L1wLck9wEb7m3i20h/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013743Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:37:46.844+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "c9c89ce95aac450eb3d8bf6d1c0a2f6a",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "466f6100348aad72e3a2edfbbca201ab5344e9ec334ee1e3a0f0122110183d67",
  "time": "2026-10-18T01:37:46.844+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/f5iFWc6FlTUFPGmsX5M5/3Z1L1wLck9wEb7m3i20h/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013743Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:37:49.144+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "c9c89ce95aac450eb3d8bf6d1c0a2f6a",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p21_Refresher_Orb\\p21_Refresher_Orb.part.png",
  "pid": 44952,
  "request_fingerprint": "466f6100348aad72e3a2edfbbca201ab5344e9ec334ee1e3a0f0122110183d67",
  "time": "2026-10-18T01:37:49.144+00:00",
  "event": "result",
  "elapsed_s": 2.297,
  "response": [
    200,
    {
      "bytes": 5592338,
      "sha256": "08aaa01f4feeb3a634ba550b8e00c11ccfa9ae0173abeb8ed158ad09fd020b31"
    }
  ]
}
```

## 2026-10-18T01:37:49.185+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "81bd275d6e214ad1b405f0ebccfef52b",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.png",
  "pid": 44952,
  "request_fingerprint": "c4a9d08b94fa73fa19eaa545a274e2d0384590b7367ff7f2160c97f388bad498",
  "time": "2026-10-18T01:37:49.185+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一卷系着蓝丝带的羊皮纸卷轴。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：卷轴横放、略斜；羊皮纸卷成直径约四厘米、长约二十五厘米的圆筒，两端各伸出一截深色木轴，轴头是车削的小圆球；卷轴中段系着一圈深蓝色丝带，打一个扁结，结上压着一枚硬币大的蓝色蜡封，蜡封上压着一个简单的星形印纹（无字）。\n材质与细节：羊皮纸泛黄、边缘起毛有细小撕口和污渍；木轴有手摸出的光泽；丝带有细褶；蜡封边缘不规则、有一道细裂纹。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，摊开的纸面，文字，符咒字，霓虹蓝光，光柱特效，现代纸卷，红色蜡封",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:50.060+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "81bd275d6e214ad1b405f0ebccfef52b",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.png",
  "pid": 44952,
  "request_fingerprint": "c4a9d08b94fa73fa19eaa545a274e2d0384590b7367ff7f2160c97f388bad498",
  "time": "2026-10-18T01:37:50.060+00:00",
  "event": "result",
  "elapsed_s": 0.844,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "pending"
  }
}
```

## 2026-10-18T01:37:50.078+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "820e60c0e2e5405c9c1bbc6aae717756",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:37:50.078+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:50.953+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "820e60c0e2e5405c9c1bbc6aae717756",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:37:50.953+00:00",
  "event": "result",
  "elapsed_s": 0.86,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:54.980+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "1e503b136fb041bda88465899849bca8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:37:54.980+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:55.590+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "1e503b136fb041bda88465899849bca8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:37:55.590+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:59.610+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "feb9fe9b3e304153a8998fd5feeec1a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:37:59.610+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:00.247+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "feb9fe9b3e304153a8998fd5feeec1a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:00.247+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:04.271+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "ec96afcd7f5c4d49b6e8f9f14ff7c15a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:04.271+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:04.865+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "ec96afcd7f5c4d49b6e8f9f14ff7c15a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:04.865+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:08.887+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "557674769a094598b614c0b664b2fccc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:08.887+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:09.485+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "557674769a094598b614c0b664b2fccc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:09.485+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:13.517+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "fa069ea0ac984fccbc22ef55471d7abe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:13.517+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:14.094+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "fa069ea0ac984fccbc22ef55471d7abe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:14.094+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:18.111+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "7e10791f5e0a47a2a5425f22f443ce9a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:18.111+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:18.979+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "7e10791f5e0a47a2a5425f22f443ce9a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:18.979+00:00",
  "event": "result",
  "elapsed_s": 0.859,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:23.007+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "575d2fec1dd54824b95cb72ffe6e6bdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:23.007+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:23.934+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "575d2fec1dd54824b95cb72ffe6e6bdd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:23.934+00:00",
  "event": "result",
  "elapsed_s": 0.906,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:27.970+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — request

```json
{
  "request_id": "43180385a64b40f99704f60d7aca422e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:27.970+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/ELnWGW0JebfV6z9aIJBz",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:29.765+00:00 — elevenlabs / GET /flows/image/ELnWGW0JebfV6z9aIJBz — result

```json
{
  "request_id": "43180385a64b40f99704f60d7aca422e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/ELnWGW0JebfV6z9aIJBz",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "98dafe32eff44394ebec593af687b47c81673aba6f22eab36838cdd3a58310e3",
  "time": "2026-10-18T01:38:29.765+00:00",
  "event": "result",
  "elapsed_s": 1.75,
  "response": {
    "id": "ELnWGW0JebfV6z9aIJBz",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/umy5jjGFcSLOvjEiMsj0/ELnWGW0JebfV6z9aIJBz/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013826Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:38:29.784+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "f71c95fbc245453ebab774a05dd6fe94",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "1b8d01dc1ca7c51eb9de95688db0aeab1f2f8529c108fcf0f778ada5f2dc26e2",
  "time": "2026-10-18T01:38:29.784+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/umy5jjGFcSLOvjEiMsj0/ELnWGW0JebfV6z9aIJBz/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013826Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:38:37.380+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "f71c95fbc245453ebab774a05dd6fe94",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p22_Town_Portal_Scroll\\p22_Town_Portal_Scroll.part.png",
  "pid": 44952,
  "request_fingerprint": "1b8d01dc1ca7c51eb9de95688db0aeab1f2f8529c108fcf0f778ada5f2dc26e2",
  "time": "2026-10-18T01:38:37.380+00:00",
  "event": "result",
  "elapsed_s": 7.578,
  "response": [
    200,
    {
      "bytes": 6009155,
      "sha256": "a0bd65ca8c155db2090e16ed6c1eecfdc7cdafb4226eda4081fb9db18d75465b"
    }
  ]
}
```

## 2026-10-18T01:38:37.391+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "83b4c512de0844f4ab4bd67063ed6079",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.png",
  "pid": 44952,
  "request_fingerprint": "6187e90cf616ec4ca2acfe34ada66dab79bc761172eee76d9be244b543a48094",
  "time": "2026-10-18T01:38:37.391+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一枚圆形青铜机关护符。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：护符正面朝上平放、略斜；直径约十厘米、厚约两厘米；外圈是一圈互相咬合的六只小齿轮，齿轮之间用铆钉固定在底盘上；中间一圈刻着细密的放射纹；正中镶着一块硬币大的圆形翠绿晶片；侧面露出一截背面的旧皮扣。\n材质与细节：青铜发暗，凹处积着绿锈，齿尖和凸起处被摸得发亮；铆钉是铁的、带锈点；晶片半透明，内部有细小的絮状纹，不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，钟表表盘，指针，数字刻度，蒸汽朋克堆砌，霓虹发光，宝石镶满",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:38.121+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "83b4c512de0844f4ab4bd67063ed6079",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.png",
  "pid": 44952,
  "request_fingerprint": "6187e90cf616ec4ca2acfe34ada66dab79bc761172eee76d9be244b543a48094",
  "time": "2026-10-18T01:38:38.121+00:00",
  "event": "result",
  "elapsed_s": 0.704,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "pending"
  }
}
```

## 2026-10-18T01:38:38.157+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "d7b19752739e47418b63f6088077cef7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:38.157+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:39.155+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "d7b19752739e47418b63f6088077cef7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:39.155+00:00",
  "event": "result",
  "elapsed_s": 0.969,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:43.174+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "af1742fbbecc4e72b3129e2350f1bc02",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:43.174+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:43.781+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "af1742fbbecc4e72b3129e2350f1bc02",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:43.781+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:47.808+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "702290ab44bd42469589c4874d14fa61",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:47.808+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:48.540+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "702290ab44bd42469589c4874d14fa61",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:48.540+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:52.563+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "e82010d285464e20bdf79001853c7b6e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:52.563+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:53.218+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "e82010d285464e20bdf79001853c7b6e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:53.218+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:57.252+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "3d741fb0e2f84e1bacb2679ddfabde0b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:57.252+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:57.838+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "3d741fb0e2f84e1bacb2679ddfabde0b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:38:57.838+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:01.873+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "6adedbf374ad409393a137da7f586a6c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:01.873+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:02.563+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "6adedbf374ad409393a137da7f586a6c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:02.563+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:06.585+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "9dc583a53dfa45a0a5b49063afbcd9b5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:06.585+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:07.225+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "9dc583a53dfa45a0a5b49063afbcd9b5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:07.225+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:11.263+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "f69048eba67d4af7b18c724e863206d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:11.263+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:11.894+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "f69048eba67d4af7b18c724e863206d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:11.894+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:15.912+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "26a4d56d470546ce860e50dd32be7d2c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:15.912+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:16.524+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "26a4d56d470546ce860e50dd32be7d2c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:16.524+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:20.558+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — request

```json
{
  "request_id": "ce9bb12f25154d908d83d1ba87f4f64f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:20.558+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/BnrWC9UUsRseOWrCRZmI",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:21.295+00:00 — elevenlabs / GET /flows/image/BnrWC9UUsRseOWrCRZmI — result

```json
{
  "request_id": "ce9bb12f25154d908d83d1ba87f4f64f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/BnrWC9UUsRseOWrCRZmI",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "0e6ce03222730f967e8b27d96e8740b09cdaa60bab34780b6472fb26302bd804",
  "time": "2026-10-18T01:39:21.295+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "BnrWC9UUsRseOWrCRZmI",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0mdNn9uK7RlasUQyBceS/BnrWC9UUsRseOWrCRZmI/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013918Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:39:21.314+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "4b3be95e8d99467ba2d85ea3d3252784",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "2c818f73488c0ca5048219567d26cad7f6add265230f176400e58fd8b7d86b81",
  "time": "2026-10-18T01:39:21.314+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0mdNn9uK7RlasUQyBceS/BnrWC9UUsRseOWrCRZmI/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013918Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:39:23.595+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "4b3be95e8d99467ba2d85ea3d3252784",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p23_Mekansm\\p23_Mekansm.part.png",
  "pid": 44952,
  "request_fingerprint": "2c818f73488c0ca5048219567d26cad7f6add265230f176400e58fd8b7d86b81",
  "time": "2026-10-18T01:39:23.595+00:00",
  "event": "result",
  "elapsed_s": 2.25,
  "response": [
    200,
    {
      "bytes": 7640948,
      "sha256": "ce6ab09d8b49026f019d1c45dd29abe705408f575dded93d5e1a00c73ce84777"
    }
  ]
}
```

## 2026-10-18T01:39:23.636+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "61a766dee6714725b56e07168e773a4f",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.png",
  "pid": 44952,
  "request_fingerprint": "93f4ccc7b92bbad5246f9cd81d8798636937e8cb7e8f83209f56a62acd14aefe",
  "time": "2026-10-18T01:39:23.636+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一根嵌金环的短魔杖。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：魔杖斜放，杖尖在右上、杖尾在左下；全长约四十厘米，杖身是一根微微收锥的深色硬木，从握处到杖尖等距嵌着五道细细的金环；杖尖用三片小金叶托着一颗拇指大的暗红色晶石，晶石呈细长的六棱尖形；杖尾一个小金帽。\n材质与细节：硬木是深红褐色，木纹细密，握处被磨得发亮；金环是旧金，有细划痕；晶石暗红半透明，内部有细小的裂纹，深处隐约一点暗红微光，不照亮周围。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，长法杖，魔法棒卡通星星，数字，霓虹红光，激光，宝石镶满",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:24.348+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "61a766dee6714725b56e07168e773a4f",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.png",
  "pid": 44952,
  "request_fingerprint": "93f4ccc7b92bbad5246f9cd81d8798636937e8cb7e8f83209f56a62acd14aefe",
  "time": "2026-10-18T01:39:24.348+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "pending"
  }
}
```

## 2026-10-18T01:39:24.366+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "873666e144cd4d64a9dcc234eba39d45",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:24.366+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:24.993+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "873666e144cd4d64a9dcc234eba39d45",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:24.993+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "pending"
  }
}
```

## 2026-10-18T01:39:29.027+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "312b2d9bcc87449ab07a874fb397ee23",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:29.027+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:29.652+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "312b2d9bcc87449ab07a874fb397ee23",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:29.652+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:33.674+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "6cc1e8e82ef74f53a7134784b1d3bc78",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:33.674+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:34.859+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "6cc1e8e82ef74f53a7134784b1d3bc78",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:34.859+00:00",
  "event": "result",
  "elapsed_s": 1.156,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:38.891+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "4eecba0472de430892efe7c9f6e00168",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:38.891+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:41.489+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "4eecba0472de430892efe7c9f6e00168",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:41.489+00:00",
  "event": "result",
  "elapsed_s": 2.579,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:45.523+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "a248eb43b42449c6aa5a9aaf7f16321d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:45.523+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:46.179+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "a248eb43b42449c6aa5a9aaf7f16321d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:46.179+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:50.211+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "ebafae7774754c4482ec01248bf2c344",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:50.211+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:50.814+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "ebafae7774754c4482ec01248bf2c344",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:50.814+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:54.819+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "18681ef797344e32b0cb78ab8b354f42",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:54.819+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:55.472+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "18681ef797344e32b0cb78ab8b354f42",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:55.472+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:59.502+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "437a8c3e71af40c98b74ef5a7b08af0e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:39:59.502+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:00.123+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "437a8c3e71af40c98b74ef5a7b08af0e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:40:00.123+00:00",
  "event": "result",
  "elapsed_s": 0.579,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:04.159+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — request

```json
{
  "request_id": "41b1cc75341a4f3b8a9c0a7e04a1fcae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:40:04.159+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/tBGMwQwMoJaJru5gqdFZ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:04.866+00:00 — elevenlabs / GET /flows/image/tBGMwQwMoJaJru5gqdFZ — result

```json
{
  "request_id": "41b1cc75341a4f3b8a9c0a7e04a1fcae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/tBGMwQwMoJaJru5gqdFZ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "8d8f153a009b8e8de76da5a117646001c8d6119df612be664eb67ef545ec44cb",
  "time": "2026-10-18T01:40:04.866+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "tBGMwQwMoJaJru5gqdFZ",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0cyge31wcjtARvDmmegn/tBGMwQwMoJaJru5gqdFZ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014001Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:40:04.900+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "497956d4015f4a81bced194df94c9c34",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "7da872380b3ee2bb5b75e4b9965fd4d73035b8ab13c9b27288b9395f6ed3e41a",
  "time": "2026-10-18T01:40:04.900+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0cyge31wcjtARvDmmegn/tBGMwQwMoJaJru5gqdFZ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014001Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:40:07.375+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "497956d4015f4a81bced194df94c9c34",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p24_Dagon\\p24_Dagon.part.png",
  "pid": 44952,
  "request_fingerprint": "7da872380b3ee2bb5b75e4b9965fd4d73035b8ab13c9b27288b9395f6ed3e41a",
  "time": "2026-10-18T01:40:07.375+00:00",
  "event": "result",
  "elapsed_s": 2.438,
  "response": [
    200,
    {
      "bytes": 5571556,
      "sha256": "6c61e4c41104dca71a412ca7b9ada98b7d2cfa0d2b6cefce3c0f6d559d49db3d"
    }
  ]
}
```

## 2026-10-18T01:40:07.431+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "efb6a4a805634891872a23bd109b77bc",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.png",
  "pid": 44952,
  "request_fingerprint": "fc569de5f0e6e24d947cd4799b5071140898751d93cd713a468b57c60404263e",
  "time": "2026-10-18T01:40:07.431+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一副乌铁半脸面具。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：面具正面朝向画面、略微侧转，像立在一个看不见的支架上；它只覆盖上半张脸，从额头到鼻梁，下缘在鼻梁处收成一个钝尖；两只眼洞向外上方斜挑；眉弓位置刻着两道锯齿状的纹，额心一道竖直的暗红色漆痕；面具两侧各钉着一条深褐色的旧皮带，自然垂下。\n材质与细节：乌铁打成，表面有锤痕、凹坑和磨亮的棱线，内侧边缘有锈；暗红漆痕剥落了一半；皮带有裂纹和汗渍。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，人脸，全脸面具，威尼斯面具，羽毛装饰，骷髅，霓虹红光，现代面罩，口罩",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:08.147+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "efb6a4a805634891872a23bd109b77bc",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.png",
  "pid": 44952,
  "request_fingerprint": "fc569de5f0e6e24d947cd4799b5071140898751d93cd713a468b57c60404263e",
  "time": "2026-10-18T01:40:08.147+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "pending"
  }
}
```

## 2026-10-18T01:40:08.179+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "ed092a250f1440d5ae24a35140c3f131",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:08.179+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:08.835+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "ed092a250f1440d5ae24a35140c3f131",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:08.835+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:12.876+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "41c963f98b3f4fb6a9fd14617770c8d3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:12.876+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:13.509+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "41c963f98b3f4fb6a9fd14617770c8d3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:13.509+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:17.530+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "4d1b3c7cb5214eb4a16b2fd30b9ef402",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:17.530+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:18.191+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "4d1b3c7cb5214eb4a16b2fd30b9ef402",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:18.191+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:22.220+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "00196b46af3345f6a4ea48c8b7c5aafc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:22.220+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:23.385+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "00196b46af3345f6a4ea48c8b7c5aafc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:23.385+00:00",
  "event": "result",
  "elapsed_s": 1.14,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:27.414+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "b8ac5bee4a8841009d6da170d764be42",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:27.414+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:28.018+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "b8ac5bee4a8841009d6da170d764be42",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:28.018+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:32.048+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "189328571bb349139c6b642c6f62a71f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:32.048+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:32.652+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "189328571bb349139c6b642c6f62a71f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:32.652+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:36.694+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "59f81fd2af1f4f06aef0d8e7392bc3cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:36.694+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:37.291+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "59f81fd2af1f4f06aef0d8e7392bc3cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:37.291+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:41.330+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "2b78fae103694d79b3e55a58bdbb4f87",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:41.330+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:42.014+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "2b78fae103694d79b3e55a58bdbb4f87",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:42.014+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:46.042+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "4a174c07160f456ba14302fa4fb4a2be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:46.042+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:46.694+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "4a174c07160f456ba14302fa4fb4a2be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:46.694+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "generating"
  }
}
```

## 2026-10-18T01:40:50.730+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — request

```json
{
  "request_id": "f7dadb0ce2b6442eb8df1f54be43adba",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:50.730+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5xLLRKrY2QLM5smrAkQk",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:51.469+00:00 — elevenlabs / GET /flows/image/5xLLRKrY2QLM5smrAkQk — result

```json
{
  "request_id": "f7dadb0ce2b6442eb8df1f54be43adba",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5xLLRKrY2QLM5smrAkQk",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "523320ab3e9e3aa64fa6bc8fe6a884dc1f570527859bd9e8322c4930ecf5cda4",
  "time": "2026-10-18T01:40:51.469+00:00",
  "event": "result",
  "elapsed_s": 0.687,
  "response": {
    "id": "5xLLRKrY2QLM5smrAkQk",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/qyWezufg4jXsA3Edv1qQ/5xLLRKrY2QLM5smrAkQk/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014048Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:40:51.493+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "8b976b6c7c3643ff9332d320b0f7020e",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "964da22ec7a2a8021171873443102d07da223f30e612b09bad960d28e0b199ba",
  "time": "2026-10-18T01:40:51.493+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/qyWezufg4jXsA3Edv1qQ/5xLLRKrY2QLM5smrAkQk/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014048Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:40:54.356+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "8b976b6c7c3643ff9332d320b0f7020e",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p25_Mask_of_Madness\\p25_Mask_of_Madness.part.png",
  "pid": 44952,
  "request_fingerprint": "964da22ec7a2a8021171873443102d07da223f30e612b09bad960d28e0b199ba",
  "time": "2026-10-18T01:40:54.356+00:00",
  "event": "result",
  "elapsed_s": 2.844,
  "response": [
    200,
    {
      "bytes": 5857483,
      "sha256": "cdab485a8235f6667ff957342702bb2954c246c8c538b037e9c81ab6a7424dcb"
    }
  ]
}
```

## 2026-10-18T01:40:54.402+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "85d514bf9fa14aa0894876a67f20e6c2",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.png",
  "pid": 44952,
  "request_fingerprint": "430e38680a20cc2ba0fe29dd85f2be57ed907af341c66f7cd6570a5017687261",
  "time": "2026-10-18T01:40:54.402+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一把烟灰色的单刃长剑。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：剑斜放，剑尖在右上、柄在左下，整把完整入画；剑身约九十厘米、宽约四指，单刃，向刃背一侧微微弯曲，刃尖斜切；护手是一根短而直的黑铁横条，两端略向下弯；握柄约一掌半长，缠着深灰色的鲨皮和一层交叉的黑色细绳；柄尾一个小黑铁帽。\n材质与细节：剑身钢面是烟灰色，表面有一层像流水一样的锻造花纹，刃口一线雪亮，刃背被做旧成发黑的哑光；黑铁件有细小锈点；鲨皮粒面清晰。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，日本武士刀刀镡，双手巨剑，霓虹发光，烟雾特效，宝石镶满，夸张锯齿",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:55.080+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "85d514bf9fa14aa0894876a67f20e6c2",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.png",
  "pid": 44952,
  "request_fingerprint": "430e38680a20cc2ba0fe29dd85f2be57ed907af341c66f7cd6570a5017687261",
  "time": "2026-10-18T01:40:55.080+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "pending"
  }
}
```

## 2026-10-18T01:40:55.109+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "b100938925f8474e8c13ec2c6753e4dd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:40:55.109+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:40:55.714+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "b100938925f8474e8c13ec2c6753e4dd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:40:55.714+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "pending"
  }
}
```

## 2026-10-18T01:40:59.747+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "8f4e8abfb6f044ffa9bc8e0f11738d3e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:40:59.747+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:00.335+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "8f4e8abfb6f044ffa9bc8e0f11738d3e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:00.335+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:04.340+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "8897b26516aa474db3ab79a7c23cf487",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:04.340+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:04.936+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "8897b26516aa474db3ab79a7c23cf487",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:04.936+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:08.962+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "57fe9fb8012042a99a80f56ef37c307e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:08.962+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:09.732+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "57fe9fb8012042a99a80f56ef37c307e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:09.732+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:13.774+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "6dc9839572e04e48b477fd20ecc0d3ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:13.774+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:14.373+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "6dc9839572e04e48b477fd20ecc0d3ae",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:14.373+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:18.409+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "6bf54368ce9040a58b9bc9426b6cddea",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:18.409+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:19.050+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "6bf54368ce9040a58b9bc9426b6cddea",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:19.050+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:23.094+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "2f426b3ee0684b6cbb34c54871bb2a86",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:23.094+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:23.703+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "2f426b3ee0684b6cbb34c54871bb2a86",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:23.703+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:27.708+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "fa390365576a47f1ade1fdae08e6ba19",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:27.708+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:28.326+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "fa390365576a47f1ade1fdae08e6ba19",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:28.326+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:32.371+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "517535500c4e4c9583e7f691642bd209",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:32.371+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:33.003+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "517535500c4e4c9583e7f691642bd209",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:33.003+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:37.044+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — request

```json
{
  "request_id": "348b47f345b64bf8bd0fef56a73584fe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:37.044+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EbvYt0cVTH3aNbED10nl",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:37.771+00:00 — elevenlabs / GET /flows/image/EbvYt0cVTH3aNbED10nl — result

```json
{
  "request_id": "348b47f345b64bf8bd0fef56a73584fe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EbvYt0cVTH3aNbED10nl",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "55dbec259da105be635493ff29fa422f23f76ea7d4c1ca4a7ac6f288a6e54693",
  "time": "2026-10-18T01:41:37.771+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "EbvYt0cVTH3aNbED10nl",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/vH9pLveyElhb3eOi0OZ2/EbvYt0cVTH3aNbED10nl/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014133Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:41:37.797+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "430aaa5175764fa59a49b2fe4f424561",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "79ea42da5f5f02d2b9f2171b77d5389115f9ce80b12ca8e6ac3e94318a6eb16a",
  "time": "2026-10-18T01:41:37.797+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/vH9pLveyElhb3eOi0OZ2/EbvYt0cVTH3aNbED10nl/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014133Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:41:40.551+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "430aaa5175764fa59a49b2fe4f424561",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p26_Lothars_Edge\\p26_Lothars_Edge.part.png",
  "pid": 44952,
  "request_fingerprint": "79ea42da5f5f02d2b9f2171b77d5389115f9ce80b12ca8e6ac3e94318a6eb16a",
  "time": "2026-10-18T01:41:40.551+00:00",
  "event": "result",
  "elapsed_s": 2.734,
  "response": [
    200,
    {
      "bytes": 5962577,
      "sha256": "150ac9604da186b1beff6ff03c0c081cc2b9318b3571e72bdabedae2c39d5162"
    }
  ]
}
```

## 2026-10-18T01:41:40.577+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "033ef573a2764abe98894e4ca8db7eaf",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.png",
  "pid": 44952,
  "request_fingerprint": "00aad937ddf28339c5b0e42d4a8d406c500f37cc022006a669e5ffa6ac54a7ab",
  "time": "2026-10-18T01:41:40.577+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一根顶端雕着眼睛的木桩图腾。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：木桩竖立（像插在看不见的底座上），约一米高、比手腕略粗；下端削成尖锥；上端约一掌长的一段雕成一只睁开的眼睛：上下眼睑是凸起的木棱，中间嵌着一颗核桃大的淡黄绿色玻璃珠作眼珠；眼睛下方的桩身上缠着几圈细麻绳，绳上挂着三四根灰褐色的羽毛和一颗小骨珠。\n材质与细节：木头是风干的灰褐色硬木，表面留着刀削的平面和裂纹；玻璃珠有气泡和划痕，内部一点很淡的黄绿微光；麻绳起毛，羽毛有自然磨损。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，监控摄像头，现代灯柱，霓虹发光，骷髅，卡通眼睛，眼球血丝",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:41.287+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "033ef573a2764abe98894e4ca8db7eaf",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.png",
  "pid": 44952,
  "request_fingerprint": "00aad937ddf28339c5b0e42d4a8d406c500f37cc022006a669e5ffa6ac54a7ab",
  "time": "2026-10-18T01:41:41.287+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "pending"
  }
}
```

## 2026-10-18T01:41:41.327+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "1f52aa8c893e4ea2b9bc5e325bffc127",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:41.327+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:41.961+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "1f52aa8c893e4ea2b9bc5e325bffc127",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:41.961+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "pending"
  }
}
```

## 2026-10-18T01:41:45.994+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "4692c14bf0084d9d818c06ee681a74e0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:45.994+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:46.629+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "4692c14bf0084d9d818c06ee681a74e0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:46.629+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:50.665+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "a8dcc99287bd4e56ab85cf43801de0d2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:50.665+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:51.299+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "a8dcc99287bd4e56ab85cf43801de0d2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:51.299+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:41:55.330+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "837f42044e9848e88e4ebacd58dc7619",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:55.330+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:41:55.966+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "837f42044e9848e88e4ebacd58dc7619",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:41:55.966+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:00.000+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "0449bdcb8aa3492b97a4102961a19a27",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:00.000+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:00.649+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "0449bdcb8aa3492b97a4102961a19a27",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:00.649+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:04.692+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "1ca3360bb1fb4384bd13c8e23bdbd35b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:04.692+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:06.659+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "1ca3360bb1fb4384bd13c8e23bdbd35b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:06.659+00:00",
  "event": "result",
  "elapsed_s": 1.937,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:10.705+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "307bf1ea6b5e4dd696f5a8c6f1991fab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:10.705+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:11.368+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "307bf1ea6b5e4dd696f5a8c6f1991fab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:11.368+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:15.402+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "5f34a2534d2a45dbacd3ff678da14a60",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:15.402+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:16.013+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "5f34a2534d2a45dbacd3ff678da14a60",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:16.013+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:20.043+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — request

```json
{
  "request_id": "3cea879ec65444ddb330959466e6e24f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:20.043+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/0vqafN2sPX3wVxNc9XGx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:20.853+00:00 — elevenlabs / GET /flows/image/0vqafN2sPX3wVxNc9XGx — result

```json
{
  "request_id": "3cea879ec65444ddb330959466e6e24f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/0vqafN2sPX3wVxNc9XGx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "781fe2911c8e931d105d3c6c1b9e23ff8d1285e7efac347180bf796ba867de73",
  "time": "2026-10-18T01:42:20.853+00:00",
  "event": "result",
  "elapsed_s": 0.781,
  "response": {
    "id": "0vqafN2sPX3wVxNc9XGx",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/kq9OFGmiORwzLd1UC6ta/0vqafN2sPX3wVxNc9XGx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014218Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:42:20.878+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "a10a4e78884b4879ba0367f34cf9eae1",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "941cd792a494637990ec51c9b240cea30e8df9d3385c05718ac83a6928451a03",
  "time": "2026-10-18T01:42:20.878+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/kq9OFGmiORwzLd1UC6ta/0vqafN2sPX3wVxNc9XGx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014218Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:42:23.362+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "a10a4e78884b4879ba0367f34cf9eae1",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p27_Observer_Ward\\p27_Observer_Ward.part.png",
  "pid": 44952,
  "request_fingerprint": "941cd792a494637990ec51c9b240cea30e8df9d3385c05718ac83a6928451a03",
  "time": "2026-10-18T01:42:23.362+00:00",
  "event": "result",
  "elapsed_s": 2.469,
  "response": [
    200,
    {
      "bytes": 5658326,
      "sha256": "f8818c2caa5481afc0f790aa0da34266bb8a020283f2630e3d26075c00e57b0f"
    }
  ]
}
```

## 2026-10-18T01:42:23.409+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "23d27b72d61a416b852a36607591f209",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.png",
  "pid": 44952,
  "request_fingerprint": "64a0121c4d510b2b3cedb943fe0687db4f917a8891858544fe43edd9ad297e4d",
  "time": "2026-10-18T01:42:23.409+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一小束用草绳扎起的厚叶片。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：四片叶子叶柄并拢、叶尖略微散开，平放、略斜；每片叶子约十五厘米长，椭圆形、尖端收尖，厚实饱满，像多肉植物的叶片；叶柄处用三四圈干草绳扎紧，打了一个小结。\n材质与细节：叶面是深绿色，覆着一层蜡质光泽，叶脉是细细的浅金色，从中脉向两侧分开；叶缘有一处小小的缺口和一点干枯的褐边；草绳干燥起毛。不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，花束，盆栽，花朵，卡通叶子，塑料仿真叶，霓虹绿光，芒果，水果",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:24.047+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "23d27b72d61a416b852a36607591f209",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.png",
  "pid": 44952,
  "request_fingerprint": "64a0121c4d510b2b3cedb943fe0687db4f917a8891858544fe43edd9ad297e4d",
  "time": "2026-10-18T01:42:24.047+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "pending"
  }
}
```

## 2026-10-18T01:42:24.080+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "cd87b1c8c6c5499e965c26d33b4d073c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:24.080+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:31.419+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "cd87b1c8c6c5499e965c26d33b4d073c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:31.419+00:00",
  "event": "result",
  "elapsed_s": 7.312,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "pending"
  }
}
```

## 2026-10-18T01:42:35.459+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "9e2cf2f39f564714a116bdd47c9455db",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:35.459+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:36.114+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "9e2cf2f39f564714a116bdd47c9455db",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:36.114+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:40.157+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "f82016b448fc4435a0fe8046faaa832d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:40.157+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:40.787+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "f82016b448fc4435a0fe8046faaa832d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:40.787+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:44.819+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "954f09d143d84cb2bd754af33e7178f1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:44.819+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:45.445+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "954f09d143d84cb2bd754af33e7178f1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:45.445+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:49.475+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "b3580878431c42dca288730c62fe00d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:49.475+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:50.091+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "b3580878431c42dca288730c62fe00d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:50.091+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:54.119+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "f83d79fa111245f9bfde19669e1ef767",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:54.119+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:54.755+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "f83d79fa111245f9bfde19669e1ef767",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:54.755+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:42:58.802+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "00a3a075a77348c496586ec17f883437",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:58.802+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:42:59.478+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "00a3a075a77348c496586ec17f883437",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:42:59.478+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:03.506+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — request

```json
{
  "request_id": "1f77c7fa7a8d427fb96ae1385d6deae1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:43:03.506+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/At5jLsTEk6Q432UdhC84",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:04.380+00:00 — elevenlabs / GET /flows/image/At5jLsTEk6Q432UdhC84 — result

```json
{
  "request_id": "1f77c7fa7a8d427fb96ae1385d6deae1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/At5jLsTEk6Q432UdhC84",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "5de50e5977bffa3d426abf412029f28d28a34442e9a03fde198378a00643c696",
  "time": "2026-10-18T01:43:04.380+00:00",
  "event": "result",
  "elapsed_s": 0.844,
  "response": {
    "id": "At5jLsTEk6Q432UdhC84",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/wkQWl21TFQCMgrLdN6bg/At5jLsTEk6Q432UdhC84/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014301Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:43:04.407+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "09293da370d243ef95026d149ebc7a40",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "45b3cdd70446693874ca86fddee5443dd6ec0b0e0b5dc3ae66f2a2f02eafa2b6",
  "time": "2026-10-18T01:43:04.407+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/wkQWl21TFQCMgrLdN6bg/At5jLsTEk6Q432UdhC84/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014301Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:43:07.184+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "09293da370d243ef95026d149ebc7a40",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p28_Ancient_Tango\\p28_Ancient_Tango.part.png",
  "pid": 44952,
  "request_fingerprint": "45b3cdd70446693874ca86fddee5443dd6ec0b0e0b5dc3ae66f2a2f02eafa2b6",
  "time": "2026-10-18T01:43:07.184+00:00",
  "event": "result",
  "elapsed_s": 2.734,
  "response": [
    200,
    {
      "bytes": 6559692,
      "sha256": "e96a08ec1fff8c6f2887c3ac9a739eafc7265c7bc8678719eca5b8dd0ebc3280"
    }
  ]
}
```

## 2026-10-18T01:43:07.212+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "41ca0edb34cf4ad7800477793857e5d7",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.png",
  "pid": 44952,
  "request_fingerprint": "afff7d47ae0f42b096719461703f8c8ddf55811361d2520efbb3454e4158126c",
  "time": "2026-10-18T01:43:07.212+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一块会发光的绿色符石。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一块约三十厘米高的竖立椭圆形黑色符石，像从河里捞起的卵石被凿成一块厚符板，表面打磨得光滑、边缘留着一圈粗凿的原石面；正面刻着一个由螺旋与放射线组成的符纹，刻槽深而利落；背面平整、同样打磨光滑。符石悬在半空、离背景地面约一掌高，下方背景上落着一小圈绿色的柔和光晕。\n材质与光：石体是致密的黑色玄武岩，打磨面有细小的气孔与天然纹理；翠绿色的光从刻槽深处和石体内部透出来，中心最亮、向边缘渐暗，亮度克制、刻槽边缘清晰不过曝；光只照亮符石自身和下方那一小圈，不照亮整个背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，荧光绿，毒液，宝石切面，水晶塑料感，霓虹灯管，平面光效贴图，字母刻字",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:07.950+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "41ca0edb34cf4ad7800477793857e5d7",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.png",
  "pid": 44952,
  "request_fingerprint": "afff7d47ae0f42b096719461703f8c8ddf55811361d2520efbb3454e4158126c",
  "time": "2026-10-18T01:43:07.950+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "pending"
  }
}
```

## 2026-10-18T01:43:07.991+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "5ff9c7b7c8ca49c7b1bb2bfc65aa0713",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:07.991+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:08.628+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "5ff9c7b7c8ca49c7b1bb2bfc65aa0713",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:08.628+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "pending"
  }
}
```

## 2026-10-18T01:43:12.652+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "5c960805cd92434d983bb88a0d51a1d4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:12.652+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:13.331+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "5c960805cd92434d983bb88a0d51a1d4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:13.331+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:17.368+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "63de3d50d8ea4d37bb97fa47bb5973d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:17.368+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:18.065+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "63de3d50d8ea4d37bb97fa47bb5973d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:18.065+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:22.101+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "19c16f7465214ca58876529d83f62d21",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:22.101+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:22.809+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "19c16f7465214ca58876529d83f62d21",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:22.809+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:26.851+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "c87edb3c6eae4c1981b9b96367105282",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:26.851+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:27.527+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "c87edb3c6eae4c1981b9b96367105282",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:27.527+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:31.548+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "2848a1f7814e4396a5b664cd62126575",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:31.548+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:32.203+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "2848a1f7814e4396a5b664cd62126575",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:32.203+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:36.229+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "78edea244f4b4cfca369ac32a289d3fc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:36.229+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:36.842+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "78edea244f4b4cfca369ac32a289d3fc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:36.842+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:40.886+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "4feddc0b109345d5a90d641c8c9a1904",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:40.886+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:41.663+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "4feddc0b109345d5a90d641c8c9a1904",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:41.663+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:45.706+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — request

```json
{
  "request_id": "cb95ea229b3b4aec99e3ef9c9299c8c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:45.706+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VWe8Xc4VexH9u96wgO38",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:46.543+00:00 — elevenlabs / GET /flows/image/VWe8Xc4VexH9u96wgO38 — result

```json
{
  "request_id": "cb95ea229b3b4aec99e3ef9c9299c8c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VWe8Xc4VexH9u96wgO38",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0fecb965249349afb938af633b4355945d3f690280e16ecad66cbb42e1231e91",
  "time": "2026-10-18T01:43:46.543+00:00",
  "event": "result",
  "elapsed_s": 0.796,
  "response": {
    "id": "VWe8Xc4VexH9u96wgO38",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/Q60iiPvPaWd18lbfQQqG/VWe8Xc4VexH9u96wgO38/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014345Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:43:46.568+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "9ca43afc769248ee85c8d719c595da59",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "ba2595e5f8e23074fd3fc64a09b9dc9dc374cbb4ab7b6383c4d04604e8d639c0",
  "time": "2026-10-18T01:43:46.568+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/Q60iiPvPaWd18lbfQQqG/VWe8Xc4VexH9u96wgO38/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014345Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:43:48.720+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "9ca43afc769248ee85c8d719c595da59",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p2_Regeneration_Rune\\p2_Regeneration_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "ba2595e5f8e23074fd3fc64a09b9dc9dc374cbb4ab7b6383c4d04604e8d639c0",
  "time": "2026-10-18T01:43:48.720+00:00",
  "event": "result",
  "elapsed_s": 2.125,
  "response": [
    200,
    {
      "bytes": 6186357,
      "sha256": "a40746e30bce1f77bf5c37ff1e8a316740085c9619d54691cc9f330d719ac934"
    }
  ]
}
```

## 2026-10-18T01:43:48.770+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "f6e1222764a94f6ba80d2c45fec85202",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.png",
  "pid": 44952,
  "request_fingerprint": "5fe268abd372612c1ba04384c1fa46be49538e2d983e0b4dd47049643670e95f",
  "time": "2026-10-18T01:43:48.770+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一块会发光的蓝色符石。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一块约三十厘米高的竖立椭圆形黑色符石，像从河里捞起的卵石被凿成一块厚符板，表面打磨得光滑、边缘留着一圈粗凿的原石面；正面刻着一个由螺旋与放射线组成的符纹，刻槽深而利落；背面平整、同样打磨光滑。符石悬在半空、离背景地面约一掌高，下方背景上落着一小圈蓝色的柔和光晕。\n材质与光：石体是致密的黑色玄武岩，打磨面有细小的气孔与天然纹理；宝蓝色的光从刻槽深处和石体内部透出来，中心最亮、向边缘渐暗，亮度克制、刻槽边缘清晰不过曝；光只照亮符石自身和下方那一小圈，不照亮整个背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，紫色，青色，宝石切面，水晶塑料感，霓虹灯管，平面光效贴图，字母刻字",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:49.466+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "f6e1222764a94f6ba80d2c45fec85202",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.png",
  "pid": 44952,
  "request_fingerprint": "5fe268abd372612c1ba04384c1fa46be49538e2d983e0b4dd47049643670e95f",
  "time": "2026-10-18T01:43:49.466+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "pending"
  }
}
```

## 2026-10-18T01:43:49.494+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "a4034b0075f04e0c862c238c10efc0c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:49.494+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:50.130+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "a4034b0075f04e0c862c238c10efc0c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:50.130+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:54.155+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "bf39818483b44cb5ad5f50c6d9d2b958",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:54.155+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:54.776+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "bf39818483b44cb5ad5f50c6d9d2b958",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:54.776+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:43:58.803+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "92b9e78b380e43e5a48f4e874180dd3b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:58.803+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:43:59.430+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "92b9e78b380e43e5a48f4e874180dd3b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:43:59.430+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:03.468+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "41807eef032d44efaa193d86c0bed01c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:03.468+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:04.100+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "41807eef032d44efaa193d86c0bed01c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:04.100+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:08.129+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "02961979843543b4b4b8f915899795b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:08.129+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:08.796+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "02961979843543b4b4b8f915899795b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:08.796+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:12.826+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "c564e54c9f8c4aae999aeb0297a95f39",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:12.826+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:13.449+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "c564e54c9f8c4aae999aeb0297a95f39",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:13.449+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:17.489+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "20b4d5ca42f746578f047076db962369",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:17.489+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:18.182+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "20b4d5ca42f746578f047076db962369",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:18.182+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:22.211+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "a804bcc0d4684376899acfc4fec0cba3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:22.211+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:22.967+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "a804bcc0d4684376899acfc4fec0cba3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:22.967+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:26.993+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — request

```json
{
  "request_id": "fc4a2ebb9ea240baaaff1f1444c5d764",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:26.993+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/hLwBec52pXlHrxfv05cx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:27.759+00:00 — elevenlabs / GET /flows/image/hLwBec52pXlHrxfv05cx — result

```json
{
  "request_id": "fc4a2ebb9ea240baaaff1f1444c5d764",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/hLwBec52pXlHrxfv05cx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2041235d117949927314225b887d67cd0f183efbc6b2b1bc54f5e9f4ab7d586e",
  "time": "2026-10-18T01:44:27.759+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "hLwBec52pXlHrxfv05cx",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/I052F9lKRaE76eexWuAw/hLwBec52pXlHrxfv05cx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014425Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:44:27.787+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "eff69d5c547b4cb5945ca30af5474650",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "ee9f221994ab0deda359fe8715cda180dfd65bbf77292888ea72fe15be7cefc7",
  "time": "2026-10-18T01:44:27.787+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/I052F9lKRaE76eexWuAw/hLwBec52pXlHrxfv05cx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014425Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:44:30.018+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "eff69d5c547b4cb5945ca30af5474650",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p3_Double_Damage_Rune\\p3_Double_Damage_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "ee9f221994ab0deda359fe8715cda180dfd65bbf77292888ea72fe15be7cefc7",
  "time": "2026-10-18T01:44:30.018+00:00",
  "event": "result",
  "elapsed_s": 2.219,
  "response": [
    200,
    {
      "bytes": 5816424,
      "sha256": "dbd72b0da70faec142025e01ad9dc71772a5ce844582afe76b3f376b0aee9649"
    }
  ]
}
```

## 2026-10-18T01:44:30.049+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "8bed0de922b84f89befb5fe164f6032e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.png",
  "pid": 44952,
  "request_fingerprint": "ed207124ccd08e6c83b85d7557f05fab06f077c2f7e12805be8e5c60faace121",
  "time": "2026-10-18T01:44:30.049+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一块会发光的金黄色符石。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一块约三十厘米高的竖立椭圆形黑色符石，像从河里捞起的卵石被凿成一块厚符板，表面打磨得光滑、边缘留着一圈粗凿的原石面；正面刻着一个由螺旋与放射线组成的符纹，刻槽深而利落；背面平整、同样打磨光滑。符石悬在半空、离背景地面约一掌高，下方背景上落着一小圈金黄色的柔和光晕。\n材质与光：石体是致密的黑色玄武岩，打磨面有细小的气孔与天然纹理；橄榄金黄色的光从刻槽深处和石体内部透出来，中心最亮、向边缘渐暗，亮度克制、刻槽边缘清晰不过曝；光只照亮符石自身和下方那一小圈，不照亮整个背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，橙红，纯白，宝石切面，水晶塑料感，霓虹灯管，平面光效贴图，字母刻字",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:30.742+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "8bed0de922b84f89befb5fe164f6032e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.png",
  "pid": 44952,
  "request_fingerprint": "ed207124ccd08e6c83b85d7557f05fab06f077c2f7e12805be8e5c60faace121",
  "time": "2026-10-18T01:44:30.742+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "pending"
  }
}
```

## 2026-10-18T01:44:30.772+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "4bd9ce8b77e8456ea7b09fa8a87948aa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:30.772+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:32.023+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "4bd9ce8b77e8456ea7b09fa8a87948aa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:32.023+00:00",
  "event": "result",
  "elapsed_s": 1.235,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:36.044+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "e78334fe6c444d558a39349b2c330712",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:36.044+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:36.662+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "e78334fe6c444d558a39349b2c330712",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:36.662+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:40.692+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "403b4d1691b9401caff5f3a49e86119e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:40.692+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:41.390+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "403b4d1691b9401caff5f3a49e86119e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:41.390+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:45.417+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "98d9c1a34cf24a3eb127a763d192a8d6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:45.417+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:46.008+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "98d9c1a34cf24a3eb127a763d192a8d6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:46.008+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:50.031+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "b83c2d0f09b246789fa42f54e3495f64",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:50.031+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:50.936+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "b83c2d0f09b246789fa42f54e3495f64",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:50.936+00:00",
  "event": "result",
  "elapsed_s": 0.875,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:54.972+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "259532fe4e2a4e098e02865e409e7f3c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:54.972+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:44:55.580+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "259532fe4e2a4e098e02865e409e7f3c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:55.580+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:44:59.601+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "04bd66586eaf4a3099020ceb99d66a74",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:44:59.601+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:00.358+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "04bd66586eaf4a3099020ceb99d66a74",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:45:00.358+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:04.382+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "72d61d294b2e4fcc9de36d24d7dcf58a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:45:04.382+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:05.118+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "72d61d294b2e4fcc9de36d24d7dcf58a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:45:05.118+00:00",
  "event": "result",
  "elapsed_s": 0.704,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:09.144+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — request

```json
{
  "request_id": "bb9c12d825664d069b71a9720501649e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:45:09.144+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/qTumie74YdaHsfiyRWV2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:10.066+00:00 — elevenlabs / GET /flows/image/qTumie74YdaHsfiyRWV2 — result

```json
{
  "request_id": "bb9c12d825664d069b71a9720501649e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/qTumie74YdaHsfiyRWV2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "d58ea72f5ccada08c25c88854d81e3611b1cbbcef87da212023f415bc6d47745",
  "time": "2026-10-18T01:45:10.066+00:00",
  "event": "result",
  "elapsed_s": 0.907,
  "response": {
    "id": "qTumie74YdaHsfiyRWV2",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/QAw5Nqn1cJB4DvgEKbGo/qTumie74YdaHsfiyRWV2/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014508Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:45:10.104+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "823c289a9a2f43fe83bef3b69b9da31d",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0e7b6d0b3d597c509c63bf9935d6fb6cc7405d6b42369d9b0f4fec4d79aa61ed",
  "time": "2026-10-18T01:45:10.104+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/QAw5Nqn1cJB4DvgEKbGo/qTumie74YdaHsfiyRWV2/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014508Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:45:12.539+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "823c289a9a2f43fe83bef3b69b9da31d",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p4_Illusion_Rune\\p4_Illusion_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0e7b6d0b3d597c509c63bf9935d6fb6cc7405d6b42369d9b0f4fec4d79aa61ed",
  "time": "2026-10-18T01:45:12.539+00:00",
  "event": "result",
  "elapsed_s": 2.421,
  "response": [
    200,
    {
      "bytes": 6207261,
      "sha256": "1211157ef8732ed2a966de4bd6bba3a8379a3cfddad79eb85c652010f25bd055"
    }
  ]
}
```

## 2026-10-18T01:45:12.561+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "4d44bef1bb464bdab12529a285fb3ed4",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.png",
  "pid": 44952,
  "request_fingerprint": "1be3de272a537563fa1ffaf128ef851a0a3e2cadc67a9184d0dfb19b8d112efe",
  "time": "2026-10-18T01:45:12.561+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一块会发光的蓝紫色符石。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一块约三十厘米高的竖立椭圆形黑色符石，像从河里捞起的卵石被凿成一块厚符板，表面打磨得光滑、边缘留着一圈粗凿的原石面；正面刻着一个由螺旋与放射线组成的符纹，刻槽深而利落；背面平整、同样打磨光滑。符石悬在半空、离背景地面约一掌高，下方背景上落着一小圈蓝紫色的柔和光晕。\n材质与光：石体是致密的黑色玄武岩，打磨面有细小的气孔与天然纹理；蓝紫色的光从刻槽深处和石体内部透出来，中心最亮、向边缘渐暗，亮度克制、刻槽边缘清晰不过曝；光只照亮符石自身和下方那一小圈，不照亮整个背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，粉红，品红，宝石切面，水晶塑料感，霓虹灯管，平面光效贴图，字母刻字",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:13.252+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "4d44bef1bb464bdab12529a285fb3ed4",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.png",
  "pid": 44952,
  "request_fingerprint": "1be3de272a537563fa1ffaf128ef851a0a3e2cadc67a9184d0dfb19b8d112efe",
  "time": "2026-10-18T01:45:13.252+00:00",
  "event": "result",
  "elapsed_s": 0.687,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "pending"
  }
}
```

## 2026-10-18T01:45:13.273+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "a88e9262465641b191a41a47f8015bd7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:13.273+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:13.919+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "a88e9262465641b191a41a47f8015bd7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:13.919+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "pending"
  }
}
```

## 2026-10-18T01:45:17.945+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "d18c65ea36bb4f5f8180342729e655d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:17.945+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:18.610+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "d18c65ea36bb4f5f8180342729e655d1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:18.610+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:22.633+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "c79871629bf84ffcb330782da047c010",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:22.633+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:23.307+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "c79871629bf84ffcb330782da047c010",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:23.307+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:27.337+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "8f3bc0ab74f24ebc8c6f62cc59374b63",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:27.337+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:27.984+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "8f3bc0ab74f24ebc8c6f62cc59374b63",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:27.984+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:32.018+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "830750cdaa1c446d96263a72a07894bc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:32.018+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:32.646+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "830750cdaa1c446d96263a72a07894bc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:32.646+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:36.681+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "e454dcc38e19401e85799907ccedf872",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:36.681+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:37.303+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "e454dcc38e19401e85799907ccedf872",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:37.303+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:41.333+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "546f198e31564804ad8c1fcdccfc929f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:41.333+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:41.968+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "546f198e31564804ad8c1fcdccfc929f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:41.968+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:46.001+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "2b9d6d193d3e45a9b9313a955c344cd3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:46.001+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:46.632+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "2b9d6d193d3e45a9b9313a955c344cd3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:46.632+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:50.649+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "bc5e04e096ec4055af3a10ad0417fa00",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:50.649+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:51.395+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "bc5e04e096ec4055af3a10ad0417fa00",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:51.395+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "generating"
  }
}
```

## 2026-10-18T01:45:55.417+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — request

```json
{
  "request_id": "4a819597c9dd447081036fd038119b67",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:55.417+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cNXXBKjKGC3CoRiJ8CZ2",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:56.208+00:00 — elevenlabs / GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2 — result

```json
{
  "request_id": "4a819597c9dd447081036fd038119b67",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cNXXBKjKGC3CoRiJ8CZ2",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "0f9a92b89132b243b5374dd916cdce8e9684e2863b5810c67f06070bad66bc10",
  "time": "2026-10-18T01:45:56.208+00:00",
  "event": "result",
  "elapsed_s": 0.765,
  "response": {
    "id": "cNXXBKjKGC3CoRiJ8CZ2",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/NdQDAxBAE9T2W1WM3nm4/cNXXBKjKGC3CoRiJ8CZ2/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014553Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:45:56.225+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "12c7e65d9cb448fe9035479a89836919",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "4bcef88397fcd126c3aa3e347ead67173e1e8862de5f9b5818e082129fbf38cc",
  "time": "2026-10-18T01:45:56.225+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/NdQDAxBAE9T2W1WM3nm4/cNXXBKjKGC3CoRiJ8CZ2/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014553Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:45:58.630+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "12c7e65d9cb448fe9035479a89836919",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p5_Invisibility_Rune\\p5_Invisibility_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "4bcef88397fcd126c3aa3e347ead67173e1e8862de5f9b5818e082129fbf38cc",
  "time": "2026-10-18T01:45:58.630+00:00",
  "event": "result",
  "elapsed_s": 2.39,
  "response": [
    200,
    {
      "bytes": 6187277,
      "sha256": "0ded09531c3418aa38b4b484a6aff44f08b1d79e18e1ac041e6c62d4eda02fd3"
    }
  ]
}
```

## 2026-10-18T01:45:58.667+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "b7d62141194a439bb6742f466e313c44",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.png",
  "pid": 44952,
  "request_fingerprint": "db1c3c922ff48e3d00c6fc2040450507dd9d3c60f27d2517bc8663b66db88ee6",
  "time": "2026-10-18T01:45:58.667+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一只装满金币的铸铁小罐。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一只约三十厘米高的鼓肚小罐，三只短而粗的脚，罐口略收、外翻一圈厚唇，两侧各一只铁环耳；罐里堆满金币，高出罐口一截，几枚金币从罐沿滑落、斜靠在罐脚边。\n材质与细节：罐身是铸铁，黑色中透着暗褐，表面有铸造砂眼、细小锈斑和被手摸亮的地方；金币是厚实的手打旧金币，大小略有不同，边缘不圆整，压着模糊的花纹（无字），金色温暖、有磨损和细划痕，反射柔和的高光。整件东西不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，发光，魔法光效，彩虹，卡通金币，硬币上的文字或数字，现代硬币，陶瓷罐，宝箱",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:59.354+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "b7d62141194a439bb6742f466e313c44",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.png",
  "pid": 44952,
  "request_fingerprint": "db1c3c922ff48e3d00c6fc2040450507dd9d3c60f27d2517bc8663b66db88ee6",
  "time": "2026-10-18T01:45:59.354+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "pending"
  }
}
```

## 2026-10-18T01:45:59.372+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "e28aba0a3c6f4fa0a8365833c01c4641",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:45:59.372+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:45:59.991+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "e28aba0a3c6f4fa0a8365833c01c4641",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:45:59.991+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:04.011+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "d71ef202972440fd8face1e80dcf639e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:04.011+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:04.685+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "d71ef202972440fd8face1e80dcf639e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:04.685+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:08.722+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "619cd5c3292e4790acca851c45f4ceab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:08.722+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:09.371+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "619cd5c3292e4790acca851c45f4ceab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:09.371+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:13.398+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "2fd8f517f695483bb37bec0503bfa377",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:13.398+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:15.776+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "2fd8f517f695483bb37bec0503bfa377",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:15.776+00:00",
  "event": "result",
  "elapsed_s": 2.344,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:19.798+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "f2bd77ef29a1446fb17ee721a4b00916",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:19.798+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:20.411+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "f2bd77ef29a1446fb17ee721a4b00916",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:20.411+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:24.428+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "cd15b076505d46139290d87d512039e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:24.428+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:25.092+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "cd15b076505d46139290d87d512039e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:25.092+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:29.125+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "92156459dafb438e9aa6bcf9c271b203",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:29.125+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:29.748+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "92156459dafb438e9aa6bcf9c271b203",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:29.748+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:33.782+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "980663959e39479fa639d41ddf0f9626",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:33.782+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:34.421+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "980663959e39479fa639d41ddf0f9626",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:34.421+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:38.455+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — request

```json
{
  "request_id": "829d4e838663443c830f747504a4d93b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:38.455+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/VgdokhViwlJKVOqrp2Jh",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:39.391+00:00 — elevenlabs / GET /flows/image/VgdokhViwlJKVOqrp2Jh — result

```json
{
  "request_id": "829d4e838663443c830f747504a4d93b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/VgdokhViwlJKVOqrp2Jh",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "2f0c75fd84030d333cca8ec85ab08be69c7840c5d13bbcd8a8a34ce2c0d0ff51",
  "time": "2026-10-18T01:46:39.391+00:00",
  "event": "result",
  "elapsed_s": 0.922,
  "response": {
    "id": "VgdokhViwlJKVOqrp2Jh",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/n6gby0WWlWWXRI99uivq/VgdokhViwlJKVOqrp2Jh/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014638Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:46:39.405+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "cac910404a6c4b909813b3979e0af3ed",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "58324ade34acab767ca11bb0410e09fcaee8cfe8756318f2efd834147818f2cd",
  "time": "2026-10-18T01:46:39.405+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/n6gby0WWlWWXRI99uivq/VgdokhViwlJKVOqrp2Jh/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014638Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:46:41.878+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "cac910404a6c4b909813b3979e0af3ed",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p6_Bounty_Rune\\p6_Bounty_Rune.part.png",
  "pid": 44952,
  "request_fingerprint": "58324ade34acab767ca11bb0410e09fcaee8cfe8756318f2efd834147818f2cd",
  "time": "2026-10-18T01:46:41.878+00:00",
  "event": "result",
  "elapsed_s": 2.469,
  "response": [
    200,
    {
      "bytes": 6483472,
      "sha256": "83d54ad99b45fd836eee8fc6977b0dc45bcf37d36db6fca478565fd7d71e0661"
    }
  ]
}
```

## 2026-10-18T01:46:41.902+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "33396cc372424518b4dfc306e71a9be0",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.png",
  "pid": 44952,
  "request_fingerprint": "d3c06bd19510ee16a596f12930b03e0579e008544592b6111ca1e9bba110ca10",
  "time": "2026-10-18T01:46:41.902+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一面圆形护心小盾。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：一面直径约四十五厘米的圆形小盾，盾面向中心微微隆起；正中凸起一个圆台，上面镶着一枚鸽蛋大的乳白色晶石；盾缘向内一掌宽处压着一圈简洁的叶脉浮雕，叶片首尾相接绕满一圈；盾的背面露出一截深褐色的旧皮臂带和两颗铆钉。没有翅膀、没有尖刺、没有兽首。\n材质与细节：盾体是带蓝灰色调的冷钢（像淬过火的奥金金属），表面有细密的锤痕、几道浅划痕和边缘磨亮处；晶石半透明，内部隐约有一点乳白微光，光很弱，不照亮盾面。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，翅膀，羽翼装饰，金色奖杯，鸢形盾，尖刺盾，兽首浮雕，霓虹发光，宝石切面闪光",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:42.619+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "33396cc372424518b4dfc306e71a9be0",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.png",
  "pid": 44952,
  "request_fingerprint": "d3c06bd19510ee16a596f12930b03e0579e008544592b6111ca1e9bba110ca10",
  "time": "2026-10-18T01:46:42.619+00:00",
  "event": "result",
  "elapsed_s": 0.704,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "pending"
  }
}
```

## 2026-10-18T01:46:42.638+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "61165a8fd9e14a4184688374e9f06009",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:42.638+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:43.235+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "61165a8fd9e14a4184688374e9f06009",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:43.235+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "pending"
  }
}
```

## 2026-10-18T01:46:47.247+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "33a36131092f42e7aef9c217bbeb24f8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:47.247+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:47.807+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "33a36131092f42e7aef9c217bbeb24f8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:47.807+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:51.821+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "63b91b49de69446e9fb23fc11e481e1e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:51.821+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:52.446+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "63b91b49de69446e9fb23fc11e481e1e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:52.446+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:46:56.472+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "462838a4a8714065af7a16c58332f152",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:56.472+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:46:57.072+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "462838a4a8714065af7a16c58332f152",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:46:57.072+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:01.110+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "09c4687b14e44dc995819ac84ef57e35",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:01.110+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:01.743+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "09c4687b14e44dc995819ac84ef57e35",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:01.743+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:05.767+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "c1d4e3f379a94e91af49012cb8566b46",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:05.767+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:06.714+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "c1d4e3f379a94e91af49012cb8566b46",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:06.714+00:00",
  "event": "result",
  "elapsed_s": 0.922,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:10.741+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "93c3e53e825c4c7b8ff9473a5a517cb8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:10.741+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:11.358+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "93c3e53e825c4c7b8ff9473a5a517cb8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:11.358+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:15.387+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "9788b3e6235f42bf8d8e355d9389675f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:15.387+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:16.005+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "9788b3e6235f42bf8d8e355d9389675f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:16.005+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:20.030+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "940f3b637fd24993a1659a8d48520077",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:20.030+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:20.678+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "940f3b637fd24993a1659a8d48520077",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:20.678+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:24.702+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — request

```json
{
  "request_id": "9aa8df9507f44d4b975de97b5edbf7bb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:24.702+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/yQz5XSWk982RAuZTqS8P",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:25.803+00:00 — elevenlabs / GET /flows/image/yQz5XSWk982RAuZTqS8P — result

```json
{
  "request_id": "9aa8df9507f44d4b975de97b5edbf7bb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/yQz5XSWk982RAuZTqS8P",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "c5d90dd1f2544299117349cf6ac6538b52873c7d52f5881266ae2447d9d0f85a",
  "time": "2026-10-18T01:47:25.803+00:00",
  "event": "result",
  "elapsed_s": 1.062,
  "response": {
    "id": "yQz5XSWk982RAuZTqS8P",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/tdmaY0mbZh1woDgakyzn/yQz5XSWk982RAuZTqS8P/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014724Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:47:25.827+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "3e496ac929b941b490751f42bbd0f297",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "6678016ed9d569cf875daa3f3c660b80777ffb5ffbc92a318f882a58a5edb757",
  "time": "2026-10-18T01:47:25.827+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/tdmaY0mbZh1woDgakyzn/yQz5XSWk982RAuZTqS8P/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014724Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:47:28.608+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "3e496ac929b941b490751f42bbd0f297",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p7_Aegis_of_the_Immortal\\p7_Aegis_of_the_Immortal.part.png",
  "pid": 44952,
  "request_fingerprint": "6678016ed9d569cf875daa3f3c660b80777ffb5ffbc92a318f882a58a5edb757",
  "time": "2026-10-18T01:47:28.608+00:00",
  "event": "result",
  "elapsed_s": 2.766,
  "response": [
    200,
    {
      "bytes": 8351427,
      "sha256": "9db4b414dc1d9c3b2d71bea22de2bc991316f18cd7ef8201dedb48406f5e55cc"
    }
  ]
}
```

## 2026-10-18T01:47:28.652+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "91cb0a529878429cadb11d1fe0789552",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.png",
  "pid": 44952,
  "request_fingerprint": "37e971a1709ffcb06360f57ae84be25c6db6debad09031e69af2df17a8666166",
  "time": "2026-10-18T01:47:28.652+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一大块楔形陈年硬奶酪。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：从一整轮奶酪上切下的一大块楔形，长约二十五厘米、厚约十厘米，尖头朝向画面左前方；两个切面朝上和朝前，布满大小不一的圆孔，有的孔大如指头、有的只是针眼；弧形的外皮一侧残留着几片剥落一半的红色蜡封。\n材质与细节：奶酪是淡金黄色，切面微微出油、有细小的结晶白点和刀切的细纹；外皮更深、蜡黄发硬，带布纹印痕。整块东西不发光。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，卡通奶酪，亮黄色塑料，发光，切片包装，盘子，刀，砧板",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:29.333+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "91cb0a529878429cadb11d1fe0789552",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.png",
  "pid": 44952,
  "request_fingerprint": "37e971a1709ffcb06360f57ae84be25c6db6debad09031e69af2df17a8666166",
  "time": "2026-10-18T01:47:29.333+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "pending"
  }
}
```

## 2026-10-18T01:47:29.370+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "dafd7bbee90744c6b2f010d0967ed1f0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:29.370+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:29.983+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "dafd7bbee90744c6b2f010d0967ed1f0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:29.983+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "pending"
  }
}
```

## 2026-10-18T01:47:34.006+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "cb4f7ec5156f48cd82938f21e6921570",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:34.006+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:34.632+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "cb4f7ec5156f48cd82938f21e6921570",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:34.632+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:38.667+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "da79a4e002b142adaf07c2c1ccf1c42d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:38.667+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:39.278+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "da79a4e002b142adaf07c2c1ccf1c42d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:39.278+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:43.304+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "880c4c79f7ec4ad79e05f4f9859baf57",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:43.304+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:43.918+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "880c4c79f7ec4ad79e05f4f9859baf57",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:43.918+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:47.958+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "32b3aea9d4ce4a50add0221a51429faf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:47.958+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:48.544+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "32b3aea9d4ce4a50add0221a51429faf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:48.544+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:52.569+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "2399e4b5af6044fca98f9015f88cf012",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:52.569+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:53.335+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "2399e4b5af6044fca98f9015f88cf012",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:53.335+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:47:57.377+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "845891bb9579448099ef20b54a9a2381",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:57.377+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:47:58.073+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "845891bb9579448099ef20b54a9a2381",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:47:58.073+00:00",
  "event": "result",
  "elapsed_s": 0.657,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:02.099+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "4dff7483f1e44b6781f571682848f134",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:02.099+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:02.750+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "4dff7483f1e44b6781f571682848f134",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:02.750+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:06.783+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "b34cc3d5e0f149fd8c8baa2384f394e7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:06.783+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:07.422+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "b34cc3d5e0f149fd8c8baa2384f394e7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:07.422+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:11.461+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — request

```json
{
  "request_id": "40938525262142a1b4447336f4186492",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:11.461+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/TGvL60wJFhyyDcyfounM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:12.277+00:00 — elevenlabs / GET /flows/image/TGvL60wJFhyyDcyfounM — result

```json
{
  "request_id": "40938525262142a1b4447336f4186492",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/TGvL60wJFhyyDcyfounM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "4487862f23a40f9e98b2a808dcd783e066282d467a5260550495b83c077bb3fd",
  "time": "2026-10-18T01:48:12.277+00:00",
  "event": "result",
  "elapsed_s": 0.766,
  "response": {
    "id": "TGvL60wJFhyyDcyfounM",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/taU5a0dg5ebGTlBBgKbE/TGvL60wJFhyyDcyfounM/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014812Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:48:12.312+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "db65a61d3a8a40e5b40a6a14ef40a970",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "ef5cc8f869976798855ccd8a85830bdfd90cd268d6da48dcec611d4d14c3aac3",
  "time": "2026-10-18T01:48:12.312+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/taU5a0dg5ebGTlBBgKbE/TGvL60wJFhyyDcyfounM/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014812Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:48:15.089+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "db65a61d3a8a40e5b40a6a14ef40a970",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p8_Cheese\\p8_Cheese.part.png",
  "pid": 44952,
  "request_fingerprint": "ef5cc8f869976798855ccd8a85830bdfd90cd268d6da48dcec611d4d14c3aac3",
  "time": "2026-10-18T01:48:15.089+00:00",
  "event": "result",
  "elapsed_s": 2.75,
  "response": [
    200,
    {
      "bytes": 6166877,
      "sha256": "51394ccf6e7841e48924086df2b863ae86bd04bb957180fd96c98a6a3c37394c"
    }
  ]
}
```

## 2026-10-18T01:48:15.127+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "10c1986e85c947dd993916c5f1c537b8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.png",
  "pid": 44952,
  "request_fingerprint": "e077b56c1c713be70a54d43c0ded41bbb3a891cab82d39e70c42c4ed33f2db8f",
  "time": "2026-10-18T01:48:15.127+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2",
      "prompt": "单件道具锚点图：一只圆腹细颈的旧玻璃瓶。单件道具放在中性浅灰色无缝摄影棚背景前，居中、完整入画不裁切，四分之三俯视约二十度，均匀柔和的散射光，物体下方只有很淡的接触阴影。\n形制：瓶身是一个圆鼓鼓的球腹，上接一段细长的瓶颈，总高约二十二厘米；瓶口塞着一只略高出瓶口的软木塞；瓶颈上紧紧缠着几圈深褐色皮绳，绳头系着一只小铜扣；瓶里装着大半瓶清水，水面平静。\n材质与光：厚实的手工吹制玻璃，厚薄不均、带细小气泡，微泛灰绿色，表面有几道细划痕和手指摸过的雾痕；瓶里的水清澈，透出一层淡淡的银蓝色微光，光很克制，只让水体本身显得通透，不照亮背景。\n摄影与风格：实拍道具产品照，真实制作的电影道具实物，100mm 微距定焦，影视级实拍质感，35mm 胶片颗粒，真实的金属、木头、皮革、石头与玻璃纹理和使用磨损；背景无缝干净；画面不出现任何文字。\n负面词: 画面文字，字幕，水印，logo，物品图标，UI 界面，游戏截图质感，游戏引擎渲染感，低模棱角，卡通渲染，三维动画感，Q版，塑料感材质，现代器物，人物，手，环境背景，地面场景，多个物件同框，比例参照物，标尺，现代玻璃瓶，塑料瓶，药瓶标签，酒标，螺纹瓶盖，霓虹发光液体，荧光色",
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "quality": "medium"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:15.864+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "10c1986e85c947dd993916c5f1c537b8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.png",
  "pid": 44952,
  "request_fingerprint": "e077b56c1c713be70a54d43c0ded41bbb3a891cab82d39e70c42c4ed33f2db8f",
  "time": "2026-10-18T01:48:15.864+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:48:15.897+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "67971d83653a4669879dcae645e970ce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:15.897+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:16.524+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "67971d83653a4669879dcae645e970ce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:16.524+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:48:20.551+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "dc86379be68649c2995b43936e4876e5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:20.551+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:21.228+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "dc86379be68649c2995b43936e4876e5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:21.228+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:25.267+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "76495a8ff64c4d48bc287ec1b5cd0b8d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:25.267+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:25.952+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "76495a8ff64c4d48bc287ec1b5cd0b8d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:25.952+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:29.990+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "025ff943dafb4c3b8e27898bae923fbc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:29.990+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:30.631+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "025ff943dafb4c3b8e27898bae923fbc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:30.631+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:34.667+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "cdc60a1e19074f368072054ec400a341",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:34.667+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:35.283+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "cdc60a1e19074f368072054ec400a341",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:35.283+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:39.320+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "35ae2b854d14425b8470fb3778abe723",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:39.320+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:39.946+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "35ae2b854d14425b8470fb3778abe723",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:39.946+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:43.992+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "5f7c8707c880466c956d6b4ba149cfdc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:43.992+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:44.601+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "5f7c8707c880466c956d6b4ba149cfdc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:44.601+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:48.634+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "884cb4516255497593c25334351f0828",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:48.634+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:49.332+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "884cb4516255497593c25334351f0828",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:49.332+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:48:53.368+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — request

```json
{
  "request_id": "fa6fd79505234bde86ff5f420f674504",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:53.368+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/X4dR7CccQC2U3DhmR9ZV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:48:54.133+00:00 — elevenlabs / GET /flows/image/X4dR7CccQC2U3DhmR9ZV — result

```json
{
  "request_id": "fa6fd79505234bde86ff5f420f674504",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/X4dR7CccQC2U3DhmR9ZV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "41c3011e1f09c908b6118759c1821fe68650c76e8040ca3f62debb4a9c7724dc",
  "time": "2026-10-18T01:48:54.133+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "X4dR7CccQC2U3DhmR9ZV",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/oYwnKsPAhxAHSEfZrPVG/X4dR7CccQC2U3DhmR9ZV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014853Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:48:54.157+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "baee10b3fd7f4017a4e8afb40f350fe0",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "65679925370cdcad596585d437baa6429dd7e40e51a023c9025afa271c8b28a3",
  "time": "2026-10-18T01:48:54.157+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/oYwnKsPAhxAHSEfZrPVG/X4dR7CccQC2U3DhmR9ZV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T014853Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:48:56.301+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "baee10b3fd7f4017a4e8afb40f350fe0",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\props\\p9_Empty_Bottle\\p9_Empty_Bottle.part.png",
  "pid": 44952,
  "request_fingerprint": "65679925370cdcad596585d437baa6429dd7e40e51a023c9025afa271c8b28a3",
  "time": "2026-10-18T01:48:56.301+00:00",
  "event": "result",
  "elapsed_s": 2.109,
  "response": [
    200,
    {
      "bytes": 6572889,
      "sha256": "63f1301d769927a22fa4143c4f55cfae9ca8e4315cb47db33553b3648c73aa53"
    }
  ]
}
```
