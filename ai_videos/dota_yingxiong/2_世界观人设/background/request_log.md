# 外部服务请求日志

请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。

## 2026-10-18T01:26:34.310+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "7ab1c731ba524fcbb16effb7d3bf5586",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.png",
  "pid": 48680,
  "request_fingerprint": "1e543b607fab74b1b8cc176d9dcab1b94ecd54e2cad92cddeea0bf666629ec7a",
  "time": "2026-10-18T01:26:34.310+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg1_中路河道交叉口\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n一处开阔的河谷浅滩。一条宽约四十米的清浅河流从画面左上远处斜向右下近处流来，水深只及小腿，水流平缓，河床铺满大小不一的灰褐卵石；近处水面透明，能看见水下的石头与细沙，远处水面映着天光。一条被踩得发硬的土路从画面右侧河岸斜着下到河滩，在画面中央偏下处涉水横过浅滩，再从左侧河岸爬上去；土路在水边留下杂乱的车辙、蹄印和脚印，涉水口两侧是被水冲刷过的碎石滩。两岸是截然不同的两种地貌：右岸是古老的温带阔叶林，树干粗过两人合抱，树皮深灰、挂着苔藓，树冠高大浓密、深绿色，背阴处泛着紫调，林下是成片的蕨类、低矮灌木和长短不齐的绿草，地面铺满褐黄的落叶；左岸地势略高，是一片暗褐色的泥地，泥面上爬满一块块紫黑色的地衣和霉斑一样的腐化纹理，夹着薄薄的白霜，立着稀疏的深色针叶松，松针发黑，树下贴地漂着一层冷雾。远景右侧林缘，一座由活古树长成的防御塔只露出剪影：粗壮扭曲的树干像身躯，两根大枝像举起的臂；远景左侧，冷雾后面一座阶梯式的黑石尖塔，塔顶托着一颗发出冷蓝微光的圆球。\n[细节]\n- 视角: 视点站在河心浅滩偏上游，顺着水流方向望去，高度约一人，平视略俯，24mm 广角感，同时装下两岸\n- 光线: 白天；太阳藏在右上方的薄云后面，从右侧斜照，右岸树冠下落着一块块暖色光斑；左岸被贴地冷雾笼着，光线偏冷灰、阴影发蓝；远处尖塔顶那颗冷蓝光球是左侧唯一的冷色点光；河面反着灰白天光，浅水处有细碎波光\n- 构图: 16:9 横幅；河道从左上远处斜到右下近处，占画面中央偏下；右三分之一是阔叶林岸，左三分之一是紫黑荒地与针叶松岸；土路涉水口在画面中央偏下；前景是近处浅水里的卵石；两座塔远而小，分居左右远景\n- 道具: 水边半埋着几根被冲上岸的枯木；右岸水边一丛芦苇；左岸泥地上几块覆霜的黑色碎石；画面里没有任何文字、旗帜、标记\n- 主色: 主 森林绿与苔绿 / 辅 紫黑与暗褐 / 点缀 暖金色光斑、冷蓝光球 / 高光 河面天光；自然色彩，不过饱和\n- 真实感: 这是在新西兰南岛一处真实温带河谷浅滩实地拍摄的奇幻电影外景剧照，不是渲染图：卵石大小不一、带水渍和青苔；树干有裂纹、断枝和附生苔藓；泥地有积水坑和踩踏痕；霜只薄薄一层，结在背阴处；冷雾有厚有薄，不是均匀的一层平面\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，近处卵石到远景塔影都清晰；大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，平涂紫色地面，过度饱和，荧光色，现代建筑，现代器物，桥梁，路灯，UI 界面",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high"
    },
    "files": [],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:34.972+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "7ab1c731ba524fcbb16effb7d3bf5586",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.png",
  "pid": 48680,
  "request_fingerprint": "1e543b607fab74b1b8cc176d9dcab1b94ecd54e2cad92cddeea0bf666629ec7a",
  "time": "2026-10-18T01:26:34.972+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "pending"
  }
}
```

## 2026-10-18T01:26:34.995+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "f08bc09b11d746089cf9d6553cd7bead",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:34.995+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:35.630+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "f08bc09b11d746089cf9d6553cd7bead",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:35.630+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "pending"
  }
}
```

## 2026-10-18T01:26:39.665+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "bff29d19db8143e9843c99555b6c15c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:39.665+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:40.310+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "bff29d19db8143e9843c99555b6c15c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:40.310+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:26:44.336+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "ff6f149ca4ac4bc4b9e97f37b383b4a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:44.336+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:44.947+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "ff6f149ca4ac4bc4b9e97f37b383b4a0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:44.947+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:26:48.974+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "e2f23c22c0b04446a93b26a77909a14e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:48.974+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:49.603+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "e2f23c22c0b04446a93b26a77909a14e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:49.603+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:26:53.629+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "68e1839c674c41f481a70e55d8263500",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:53.629+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:54.288+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "68e1839c674c41f481a70e55d8263500",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:54.288+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:26:58.313+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "0b611b94364d48a19ec662ed42a0b218",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:58.313+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:26:58.946+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "0b611b94364d48a19ec662ed42a0b218",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:26:58.946+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:02.974+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "b7e83fd345ad41a88c4d4e04c5a2d309",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:02.974+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:03.624+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "b7e83fd345ad41a88c4d4e04c5a2d309",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:03.624+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:07.646+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "2e1d0efd21244a009a830776629a4e29",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:07.646+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:08.240+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "2e1d0efd21244a009a830776629a4e29",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:08.240+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:12.263+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "2159bf7483374d90936954eabb401cf4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:12.263+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:13.592+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "2159bf7483374d90936954eabb401cf4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:13.592+00:00",
  "event": "result",
  "elapsed_s": 1.297,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:17.616+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — request

```json
{
  "request_id": "cf30b905968f4bad89a1beb30d19a392",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:17.616+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/x8w7zHwcTZPcEOvYWl6r",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:18.354+00:00 — elevenlabs / GET /flows/image/x8w7zHwcTZPcEOvYWl6r — result

```json
{
  "request_id": "cf30b905968f4bad89a1beb30d19a392",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/x8w7zHwcTZPcEOvYWl6r",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "2f939d90654b8fc61012ab1c35bf685954a504b84854bd7244d99d6dcd19e446",
  "time": "2026-10-18T01:27:18.354+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "x8w7zHwcTZPcEOvYWl6r",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/JdJ1vUtRKPv5EkbxJUcf/x8w7zHwcTZPcEOvYWl6r/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012715Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:27:18.379+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "3ae363b8b1d74ce3b4598ac80c535bbb",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "e658101731323be45e85581bb32bbfd5a75b8e46ba4790fe2294348023d61148",
  "time": "2026-10-18T01:27:18.379+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/JdJ1vUtRKPv5EkbxJUcf/x8w7zHwcTZPcEOvYWl6r/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012715Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:27:20.652+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "3ae363b8b1d74ce3b4598ac80c535bbb",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg1_中路河道交叉口\\bg1_中路河道交叉口.part.png",
  "pid": 48680,
  "request_fingerprint": "e658101731323be45e85581bb32bbfd5a75b8e46ba4790fe2294348023d61148",
  "time": "2026-10-18T01:27:20.652+00:00",
  "event": "result",
  "elapsed_s": 2.25,
  "response": [
    200,
    {
      "bytes": 5802941,
      "sha256": "4f0ea3bdc1a5e36789a833937b120bcc76b1c7000ce09ce10bacf9c5df84d4a4"
    }
  ]
}
```

## 2026-10-18T01:27:39.931+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "3121adb6f3ed4b288efa312188fdecbd",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.png",
  "pid": 37900,
  "request_fingerprint": "3bd812d912c34a4b28976ca10adc62bc6fcc9efafa4bcd0c0b4e68cfe1ba3697",
  "time": "2026-10-18T01:27:39.931+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg2_近卫基地·世界之树\n参考用法: 参考图只借世界的色板、阔叶林的质感与光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n一片古老巨木林深处的圣地。画面中央偏后立着一棵大到像建筑的古树：树干直径约三十米，深灰褐色的树皮裂成一道道深沟，沟里长着苔藓和蕨，树干底部的板根像几道山脊一样向四周拱出地面，根与根之间形成一个个可以走进去的弧形凹洞；树干向上伸出画面，只看到最低的几根大枝横伸出去，枝下垂着成束的气根和长苔。树皮深沟与气根上星星点点地亮着淡金绿色的微光，像夜光菌和萤火，光很弱，只在背阴处看得出来。树前是一片平整开阔的草坪，草长短不齐，夹着褐黄的落叶和几片花瓣；草坪边缘散着三口齐腰高的圆井，井栏用苔绿色的粗石砌成，石缝长草，井里是清水，水面泛着淡淡的银蓝微光。画面左右两侧是高大的阔叶古树林墙，树冠深绿、背阴处泛紫，林下是蕨和灌木；左后方林间半掩着一株活的古树建筑，树身里长出木构的拱门、阶梯与平台，根脚扎在地里，只露出一部分。\n[细节]\n- 视角: 视点在草坪前缘，高度略低于人眼，微微仰望巨树，28mm 焦距感，巨树底部的板根完整入画、树干顶端出画\n- 光线: 上午；阳光从右上方树冠的缺口斜射下来，形成三四道清晰的光柱，落在草坪上成为暖金色的光斑；空气里有细微的水汽和漂浮的花粉，让光柱可见；树皮缝里的淡金绿微光与井水的银蓝微光只是点缀，不照亮周围；阴影是带一点绿的深色\n- 构图: 16:9 横幅；巨树占画面中央三分之一并贯穿上下；前景下三分之一是空着的平整草坪，留给人物站位；三口石井分别在左前、右中与巨树根前；左右两侧林墙收边；古树建筑在左后方林间半掩\n- 道具: 草坪上几段倒伏的长苔枯枝；井边一只空着的石槽；巨树根旁几簇白色小花；画面里没有任何文字、旗帜、标记\n- 主色: 主 森林绿与苔绿 / 辅 深灰褐树皮 / 点缀 淡金绿微光、银蓝井水 / 高光 光柱里的暖金；自然色彩，不过饱和\n- 真实感: 这是在一片真实的古老温带雨林里实地拍摄、再用电影特效放大巨树的奇幻电影外景剧照，不是渲染图：树皮有剥落、虫蛀孔和湿痕；苔藓厚薄不一；草地有被踩倒的痕迹和裸露的泥土；石井的石块大小不一、带风化缺角\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，童话插画感，霓虹发光树，整棵树通体发光，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:50.690+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "3121adb6f3ed4b288efa312188fdecbd",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.png",
  "pid": 37900,
  "request_fingerprint": "3bd812d912c34a4b28976ca10adc62bc6fcc9efafa4bcd0c0b4e68cfe1ba3697",
  "time": "2026-10-18T01:27:50.690+00:00",
  "event": "result",
  "elapsed_s": 10.766,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "pending"
  }
}
```

## 2026-10-18T01:27:50.694+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "8bd5067214fa47b78d86f391301500d9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:27:50.694+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:51.286+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "8bd5067214fa47b78d86f391301500d9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:27:51.286+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:55.315+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "31b9d0d678794e71b7ca46ea28353cac",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:27:55.315+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:27:55.924+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "31b9d0d678794e71b7ca46ea28353cac",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:27:55.924+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:27:59.953+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "659eafa33c4d4f60bd6c369fe8a8b409",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:27:59.953+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:00.679+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "659eafa33c4d4f60bd6c369fe8a8b409",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:00.679+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:04.688+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "90c780b833634566a1d315cb12e964ee",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:04.688+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:05.307+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "90c780b833634566a1d315cb12e964ee",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:05.307+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:09.342+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "15d6acb4525b4c2ebb53bbf276acdac6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:09.342+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:09.899+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "15d6acb4525b4c2ebb53bbf276acdac6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:09.899+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:13.931+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "9688f852a2f54d758cc3dfbd3d383ec4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:13.931+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:14.489+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "9688f852a2f54d758cc3dfbd3d383ec4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:14.489+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:18.517+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "bfd69fdaacc24c999d3510ad5952f6cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:18.517+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:19.091+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "bfd69fdaacc24c999d3510ad5952f6cd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:19.091+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:23.109+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "3965b29d68244882932b9d868d618f44",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:23.109+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:23.690+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "3965b29d68244882932b9d868d618f44",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:23.690+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:27.715+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "3b5cd5bb8f2f4f7aba8532a385a52062",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:27.715+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:28.280+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "3b5cd5bb8f2f4f7aba8532a385a52062",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:28.280+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:32.303+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "6421fb7d9c964fd1b3966411dbfd7d8c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:32.303+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:32.896+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "6421fb7d9c964fd1b3966411dbfd7d8c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:32.896+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:36.927+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — request

```json
{
  "request_id": "937a339221c24f67b6f860d8253ca220",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:36.927+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/DeMXfMlxAQjgOITsCJvb",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:37.639+00:00 — elevenlabs / GET /flows/image/DeMXfMlxAQjgOITsCJvb — result

```json
{
  "request_id": "937a339221c24f67b6f860d8253ca220",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/DeMXfMlxAQjgOITsCJvb",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "b6750bcffabb15e2e20932c7ec0cf8466fe90a6de767c6cd3a40e36e137feaf6",
  "time": "2026-10-18T01:28:37.639+00:00",
  "event": "result",
  "elapsed_s": 0.703,
  "response": {
    "id": "DeMXfMlxAQjgOITsCJvb",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0dgKwtDkk82QOXuQl0YN/DeMXfMlxAQjgOITsCJvb/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012835Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:28:37.670+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "c25413f907bf4aa49142e5288de52042",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "1b0999677a24e7f9910291ff7ae18ea99ae6e75346016945b2f54ddbe222675f",
  "time": "2026-10-18T01:28:37.670+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0dgKwtDkk82QOXuQl0YN/DeMXfMlxAQjgOITsCJvb/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012835Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:28:39.904+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "c25413f907bf4aa49142e5288de52042",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg2_近卫基地·世界之树\\bg2_近卫基地·世界之树.part.png",
  "pid": 37900,
  "request_fingerprint": "1b0999677a24e7f9910291ff7ae18ea99ae6e75346016945b2f54ddbe222675f",
  "time": "2026-10-18T01:28:39.904+00:00",
  "event": "result",
  "elapsed_s": 2.203,
  "response": [
    200,
    {
      "bytes": 5712022,
      "sha256": "7eb26a772d395ad6fd0f91e747dcfcd61770c158b98a6e905fae0c167e29cbcc"
    }
  ]
}
```

## 2026-10-18T01:28:39.943+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "503f9158a7a44e1d9d2819f96876cd7e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.png",
  "pid": 37900,
  "request_fingerprint": "4755faca92632853c1335f63c10927421c582a9cce5e11f92c50803820350ea9",
  "time": "2026-10-18T01:28:39.943+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg3_天灾基地·冰封王座\n参考用法: 参考图只借世界的色板、紫黑荒地与针叶松的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n一片寒冷荒原上的冰峰王座。画面中央偏后立着一座由蓝白冰晶长成的尖峰，高约十五米，冰体半透明，内部有一道道灰白的裂纹和冻住的气泡，棱面锋利，顶端分成几根向上刺出的冰棱；尖峰半腰凿出一张宽大的冰晶王座，靠背高耸、扶手粗重，座面和扶手结着厚厚一层白霜，王座上空无一物；一道由碎冰与黑石垒成的粗糙阶梯从地面盘上王座。王座两侧的远景里立着三座阶梯式的尖塔，由粗凿的黑色玄武岩一层层叠起、越往上越窄，每层边缘挂着冰凌；塔顶由几根弯曲的黑铁与骨白色尖爪托着一颗冷蓝色光球，光球缓缓发光，照亮塔顶周围的霜。前方是一片平坦的冻土空地，暗褐色的泥面上爬满大片紫黑色的地衣和霉斑一样的腐化纹理，夹着冰碴、碎黑岩和薄薄的积雪；四周稀疏立着深色针叶松，松针发黑，枝上挂着白霜；更远处是灰白的冰川和低矮的黑色山脊。\n[细节]\n- 视角: 视点在冻土空地前缘，高度约一人，略仰望冰峰，32mm 焦距感，冰峰顶端完整入画\n- 光线: 阴天正午；天低云厚，冷灰色的漫射天光均匀落下，阴影浅而发蓝；三颗塔顶光球是画面里仅有的点光源，给附近的霜面和冰峰侧面打一层冰蓝补光；冷雾贴地漂着，远处更浓；冰峰内部透出一点冷白的天光\n- 构图: 16:9 横幅；冰峰与王座占画面中央三分之一；左右各有黑石尖塔在远景，高低错落；前景下三分之一是空着的平坦冻土，留给人物站位；针叶松在左右两侧收边；地平线压在画面下三分之一偏上\n- 道具: 冻土上几根折断的黑色枯枝；王座阶梯脚下散着几块碎冰；左前方一截半埋的黑石残柱；画面里没有任何文字、旗帜、标记\n- 主色: 主 紫黑与暗褐 / 辅 骨白与冰蓝 / 点缀 腐绿地衣 / 高光 冰面冷光；自然色彩，不过饱和\n- 真实感: 这是在冰岛一处真实的黑色熔岩荒原与冰川边缘实地拍摄的奇幻电影外景剧照，不是渲染图：冰体有杂质、灰尘和融化后再冻的流痕；玄武岩石块大小不一、有气孔和风化；地衣成片不均，边缘有裸露的冻泥；雪只是薄薄一层，被风吹得有疏有密\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，王座上坐人，骷髅，任何动物，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，水晶塑料感，霓虹发光，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:42.961+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "503f9158a7a44e1d9d2819f96876cd7e",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.png",
  "pid": 37900,
  "request_fingerprint": "4755faca92632853c1335f63c10927421c582a9cce5e11f92c50803820350ea9",
  "time": "2026-10-18T01:28:42.961+00:00",
  "event": "result",
  "elapsed_s": 2.984,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "pending"
  }
}
```

## 2026-10-18T01:28:42.976+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "dd2a86072b8c47babf7c445f19e5573a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:42.976+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:43.578+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "dd2a86072b8c47babf7c445f19e5573a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:43.578+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:47.585+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "1b91c4ec0a074051925bc6478375ff92",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:47.585+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:48.230+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "1b91c4ec0a074051925bc6478375ff92",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:48.230+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:52.259+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "f61cfc69bae44ec1a89d8853b2d66487",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:52.259+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:52.918+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "f61cfc69bae44ec1a89d8853b2d66487",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:52.918+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:28:56.941+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "e861cde563ca49f1834c1d2d1f8d97cf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:56.941+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:28:57.527+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "e861cde563ca49f1834c1d2d1f8d97cf",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:28:57.527+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:01.570+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "a6fb9d0c60964e95b439a8cfd187a83c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:01.570+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:02.154+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "a6fb9d0c60964e95b439a8cfd187a83c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:02.154+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:06.171+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "fa2b2a3c976b43e1b26e7c8f5200e665",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:06.171+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:06.829+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "fa2b2a3c976b43e1b26e7c8f5200e665",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:06.829+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:10.858+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "76d18939a207433988933683f0802349",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:10.858+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:11.482+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "76d18939a207433988933683f0802349",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:11.482+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:15.512+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "df395200fe8e48c4988852bb5c3d40b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:15.512+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:16.138+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "df395200fe8e48c4988852bb5c3d40b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:16.138+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:20.171+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "7befd5d5e98e48c099c2b5ad07f3d996",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:20.171+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:20.837+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "7befd5d5e98e48c099c2b5ad07f3d996",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:20.837+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:24.848+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — request

```json
{
  "request_id": "55e38320117f4343b6578ef6ccf72a94",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:24.848+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/HTecp9tbriHk5BdQhkjQ",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:25.625+00:00 — elevenlabs / GET /flows/image/HTecp9tbriHk5BdQhkjQ — result

```json
{
  "request_id": "55e38320117f4343b6578ef6ccf72a94",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/HTecp9tbriHk5BdQhkjQ",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "c1a41ea3599957d086210874a79a83525df176425236ccb8d0996ca7358ba24b",
  "time": "2026-10-18T01:29:25.625+00:00",
  "event": "result",
  "elapsed_s": 0.766,
  "response": {
    "id": "HTecp9tbriHk5BdQhkjQ",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0FPbUmVnX7jzcrGYzPob/HTecp9tbriHk5BdQhkjQ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012922Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:29:25.658+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "0bf2785443ed4f6eb3b945a3abacdd0e",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "637d424139ca27bce11a915d0391a847425c01fd31cbd81c430d140d3c24c3bd",
  "time": "2026-10-18T01:29:25.658+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/0FPbUmVnX7jzcrGYzPob/HTecp9tbriHk5BdQhkjQ/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T012922Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:29:28.251+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "0bf2785443ed4f6eb3b945a3abacdd0e",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg3_天灾基地·冰封王座\\bg3_天灾基地·冰封王座.part.png",
  "pid": 37900,
  "request_fingerprint": "637d424139ca27bce11a915d0391a847425c01fd31cbd81c430d140d3c24c3bd",
  "time": "2026-10-18T01:29:28.251+00:00",
  "event": "result",
  "elapsed_s": 2.563,
  "response": [
    200,
    {
      "bytes": 4967274,
      "sha256": "bb2d9375f2940262e05db4504bc54fdefedac88be29fada52b4764ea5c5ffc72"
    }
  ]
}
```

## 2026-10-18T01:29:28.311+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "4b58b68610d64d1480afa9545b1e263a",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.png",
  "pid": 37900,
  "request_fingerprint": "004539125a3a9b290a9f5b931a6f24db0081bef67d3262661a09a0d7a8d1f78d",
  "time": "2026-10-18T01:29:28.311+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg4_近卫中路一塔\n参考用法: 参考图只借世界的色板、阔叶林与活古树塔的材质、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n古老阔叶林边缘的一段兵道。一条宽约十米的土路从画面右下近处斜着伸向左上远处，路面是被无数脚步和车轮踩实的土黄色硬土，中间两道浅浅的车辙，路边被踩出碎石和裸土，远端路面下坡，尽头露出一片河谷的亮光和水汽。路的左侧近中景立着一株活的古树，约十二米高：树干粗壮，扭成像有躯干和宽肩的形状，向前微微倾着；两根最粗的枝从肩部伸出，像两条臂膀向路面探去，枝端是更细的分杈和稀疏的深绿叶子；树根在地面上分成几股，像几条粗腿一样踩进土里，根边的土被拱起、裂开；树身半腰有一个天然形成的大树洞，洞里堆着四五块圆滚滚的灰色大石，石面沾着泥。树皮深灰褐、裂成厚厚的鳞片，缝里长着蕨和苔。路的两侧是长着野草的缓坡，坡后是高大的阔叶古树林墙，树冠深绿、背阴处泛紫，林下是灌木和蕨。\n[细节]\n- 视角: 视点在土路右侧路肩上，高度约一人，平视，35mm 焦距感，顺着土路望向远端\n- 光线: 上午；低角度的阳光从画面右后方穿过林冠斜射进来，林间漂着一层薄雾，阳光在雾里显出几道斜光束；古树塔和路边的草在土路上投下长长的斜影；树塔向光的一侧树皮泛暖，背光一侧是带绿的深影\n- 构图: 16:9 横幅；土路从右下斜到左上，占画面中央；古树塔在左侧三分之一、近中景，顶端完整入画；右侧是草坡与林墙；前景是空着的土路，留给人物与兵线；远端河谷的亮光在画面左上\n- 道具: 路边几块半埋的石头；土路上散着几片落叶和一截断枝；塔根旁一小堆滚落的碎石；画面里没有任何文字、旗帜、标记\n- 主色: 主 森林绿 / 辅 深灰褐树皮与土黄路面 / 点缀 苔绿、暖金阳光 / 高光 雾里的光束；自然色彩，不过饱和\n- 真实感: 这是在英格兰一片真实古橡树林林缘实地拍摄、用电影特效塑造活古树的奇幻电影外景剧照，不是渲染图：树皮有裂纹、剥落和湿痕；土路有坑洼、积水的小水洼和深浅不一的踩痕；草长短不齐、夹着杂草；石块有泥和青苔\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，树上的人脸，卡通五官，红色旗帜，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，柏油路，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:33.264+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "4b58b68610d64d1480afa9545b1e263a",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.png",
  "pid": 37900,
  "request_fingerprint": "004539125a3a9b290a9f5b931a6f24db0081bef67d3262661a09a0d7a8d1f78d",
  "time": "2026-10-18T01:29:33.264+00:00",
  "event": "result",
  "elapsed_s": 4.906,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:29:33.286+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "6e33c0e3d9a249989fe263b0444ce95c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:33.286+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:33.879+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "6e33c0e3d9a249989fe263b0444ce95c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:33.879+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "pending"
  }
}
```

## 2026-10-18T01:29:37.914+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "b16eeb703e634dbda84a762773bb698c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:37.914+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:38.584+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "b16eeb703e634dbda84a762773bb698c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:38.584+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:42.610+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "e9ed2dccea8f4b8b8cb48e6140ef5baa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:42.610+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:43.191+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "e9ed2dccea8f4b8b8cb48e6140ef5baa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:43.191+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:47.222+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "1e99ebcc90d0406c8fffca231634855c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:47.222+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:47.796+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "1e99ebcc90d0406c8fffca231634855c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:47.796+00:00",
  "event": "result",
  "elapsed_s": 0.546,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:51.822+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "9cc97ebb83484c15843431872dd2daa4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:51.822+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:52.464+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "9cc97ebb83484c15843431872dd2daa4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:52.464+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:29:56.487+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "24fd8727634c40c5a16223ff1bab3c32",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:56.487+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:29:57.168+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "24fd8727634c40c5a16223ff1bab3c32",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:29:57.168+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:01.190+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "ae3cd6e273e74b2e9094c72b97ecc9bd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:01.190+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:01.808+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "ae3cd6e273e74b2e9094c72b97ecc9bd",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:01.808+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:05.840+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "04702329c89541069b8e18ea14b75733",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:05.840+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:06.435+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "04702329c89541069b8e18ea14b75733",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:06.435+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:10.459+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "23859cf838fd4221b4e514d9d0f1cdf4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:10.459+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:11.157+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "23859cf838fd4221b4e514d9d0f1cdf4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:11.157+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:15.173+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "afd9cf00694f4173a4e608491296347f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:15.173+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:15.777+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "afd9cf00694f4173a4e608491296347f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:15.777+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:19.791+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — request

```json
{
  "request_id": "0f107e1f545c442d91946cd7c089c4be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:19.791+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/8ukORtzhrxLnKd5QGLMV",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:20.581+00:00 — elevenlabs / GET /flows/image/8ukORtzhrxLnKd5QGLMV — result

```json
{
  "request_id": "0f107e1f545c442d91946cd7c089c4be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/8ukORtzhrxLnKd5QGLMV",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "01692588b4140977f39bc391156a3e483d0286183776198a69ef1f32ccf45706",
  "time": "2026-10-18T01:30:20.581+00:00",
  "event": "result",
  "elapsed_s": 0.765,
  "response": {
    "id": "8ukORtzhrxLnKd5QGLMV",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/1KMrTVluctZgMwYtr8Jr/8ukORtzhrxLnKd5QGLMV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013016Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:30:20.612+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "976dfbf6ca5c440d91cdf64e2950b5b4",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "a60262fcc3800c1d763f48bdd5c9c539bc4c80071f68b54195564abcbe617090",
  "time": "2026-10-18T01:30:20.612+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/1KMrTVluctZgMwYtr8Jr/8ukORtzhrxLnKd5QGLMV/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013016Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:30:22.868+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "976dfbf6ca5c440d91cdf64e2950b5b4",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg4_近卫中路一塔\\bg4_近卫中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "a60262fcc3800c1d763f48bdd5c9c539bc4c80071f68b54195564abcbe617090",
  "time": "2026-10-18T01:30:22.868+00:00",
  "event": "result",
  "elapsed_s": 2.235,
  "response": [
    200,
    {
      "bytes": 5995270,
      "sha256": "2dc7d56ef36eb9a599024b8f481b74b26e52c9c8f101bbafba26321d74747e92"
    }
  ]
}
```

## 2026-10-18T01:30:22.918+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "f510722a5d294cf8ab95150da5662003",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.png",
  "pid": 37900,
  "request_fingerprint": "ed8892aff246f2ae31c726500d146086351c80042b96444862ba4a856af738dc",
  "time": "2026-10-18T01:30:22.918+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg5_天灾中路一塔\n参考用法: 参考图只借世界的色板、紫黑荒地与黑石尖塔的材质、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n阴冷荒原上的一段兵道。一条宽约十米的土路从画面左下近处斜着伸向右上远处，路面是被踩烂又冻硬的黑褐色泥，坑洼里积着结了薄冰的污水，两道深车辙里嵌着碎石；远端路面下坡，尽头是灰白雾气笼着的河谷。路的右侧近中景立着一座阶梯式尖塔，约十米高：四层粗凿的黑色玄武岩一层比一层窄地叠起，每层的石块大小不一、接缝粗糙，层沿向外伸出几根骨白色的弯角状装饰，像巨兽的肋骨；塔底一圈台基被泥糊住，边缘挂着冰凌。塔顶由四根向内弯曲的黑铁尖爪托着一颗直径约一米的圆球，球体发出冷蓝色的光，内部像有缓慢翻涌的雾。路的两侧是起伏的荒坡，暗褐色的泥炭地上爬满一片片紫黑色的地衣和霉斑一样的腐化纹理，夹着枯黄的硬草与薄霜；荒坡上稀疏立着深色针叶松，松针发黑，有几棵已经枯死、只剩光秃的枝干，枝上挂着白霜。\n[细节]\n- 视角: 视点在土路左侧路肩上，高度约一人，平视略仰，35mm 焦距感，顺着土路望向远端\n- 光线: 阴天下午；厚云层压得很低，冷灰色的漫射天光均匀落下，阴影浅而发蓝；塔顶光球是画面里唯一的点光源，给塔身上半部、黑铁尖爪和近处泥地的冰面打出冰蓝色的反光；远处雾气偏灰白\n- 构图: 16:9 横幅；土路从左下斜到右上，占画面中央；尖塔在右侧三分之一、近中景，塔顶光球完整入画；左侧是荒坡与针叶松；前景是空着的泥泞土路，留给人物与兵线；远端雾中河谷在画面右上\n- 道具: 路边几块覆霜的黑色碎石；一截倒伏的枯松树干横在左侧坡上；塔基旁散落几块崩落的石块；画面里没有任何文字、旗帜、标记\n- 主色: 主 紫黑与暗褐 / 辅 黑玄武岩与骨白 / 点缀 腐绿地衣 / 高光 冷蓝光球；自然色彩，不过饱和\n- 真实感: 这是在苏格兰高地一处真实泥炭荒原实地拍摄、搭建实景尖塔的奇幻电影外景剧照，不是渲染图：玄武岩有气孔、风化和雨水冲出的白色碱痕；骨白装饰发黄、有裂纹；泥地有脚印、车辙和冻裂的纹路；霜只结在背阴面\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，绿色旗帜，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，金字塔，玛雅神庙，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:28.042+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "f510722a5d294cf8ab95150da5662003",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.png",
  "pid": 37900,
  "request_fingerprint": "ed8892aff246f2ae31c726500d146086351c80042b96444862ba4a856af738dc",
  "time": "2026-10-18T01:30:28.042+00:00",
  "event": "result",
  "elapsed_s": 5.093,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "pending"
  }
}
```

## 2026-10-18T01:30:28.070+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "3dbfe0e03e4243a3adf677abc828fa96",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:28.070+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:28.688+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "3dbfe0e03e4243a3adf677abc828fa96",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:28.688+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:32.714+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "70972a9666d747c4898d5871f2db0314",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:32.714+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:33.278+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "70972a9666d747c4898d5871f2db0314",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:33.278+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:37.285+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "c28154ecfbed4ad181229f097ad5ed5f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:37.285+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:37.906+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "c28154ecfbed4ad181229f097ad5ed5f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:37.906+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:41.931+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "2e5e1f21b0b5411db7f5e41145544429",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:41.931+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:42.634+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "2e5e1f21b0b5411db7f5e41145544429",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:42.634+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:46.659+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "1a2b6b2c56614c5f826962e2af5f8574",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:46.659+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:47.288+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "1a2b6b2c56614c5f826962e2af5f8574",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:47.288+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:51.310+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "4cc2fbd915e34269a8fe7e9148a0aa7b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:51.310+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:51.895+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "4cc2fbd915e34269a8fe7e9148a0aa7b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:51.895+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:30:55.913+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "b4ab5b4eab654933bc173a80e15a7bb7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:55.913+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:30:56.473+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "b4ab5b4eab654933bc173a80e15a7bb7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:30:56.473+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:00.494+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "25719c432c404a648a9933f3bd3cbeec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:00.494+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:01.068+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "25719c432c404a648a9933f3bd3cbeec",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:01.068+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:05.089+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "b3075b8f766344a2b59bb3dcd88184a2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:05.089+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:05.686+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "b3075b8f766344a2b59bb3dcd88184a2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:05.686+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:09.711+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "72b2d44d36704a28919ab8d14ee506cb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:09.711+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:10.296+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "72b2d44d36704a28919ab8d14ee506cb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:10.296+00:00",
  "event": "result",
  "elapsed_s": 0.562,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:14.313+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — request

```json
{
  "request_id": "e81e194a2bff4a708132c13b819e8803",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:14.313+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lVkgRwlqi5iQl61cebFd",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:15.102+00:00 — elevenlabs / GET /flows/image/lVkgRwlqi5iQl61cebFd — result

```json
{
  "request_id": "e81e194a2bff4a708132c13b819e8803",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lVkgRwlqi5iQl61cebFd",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "33fb1a98a9e90562d378506a411f67b17680d7812f268d2839f466c011133b84",
  "time": "2026-10-18T01:31:15.102+00:00",
  "event": "result",
  "elapsed_s": 0.781,
  "response": {
    "id": "lVkgRwlqi5iQl61cebFd",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/F8KmT1jvOfPGVxIvylbV/lVkgRwlqi5iQl61cebFd/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013110Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:31:15.125+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "cfff62deb9ae429db558fb971596f8ef",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "a396416916f3875707820efa1eb131e2d1d0b9fced80b40cd97412bf4d52080a",
  "time": "2026-10-18T01:31:15.125+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/F8KmT1jvOfPGVxIvylbV/lVkgRwlqi5iQl61cebFd/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013110Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:31:17.447+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "cfff62deb9ae429db558fb971596f8ef",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg5_天灾中路一塔\\bg5_天灾中路一塔.part.png",
  "pid": 37900,
  "request_fingerprint": "a396416916f3875707820efa1eb131e2d1d0b9fced80b40cd97412bf4d52080a",
  "time": "2026-10-18T01:31:17.447+00:00",
  "event": "result",
  "elapsed_s": 2.297,
  "response": [
    200,
    {
      "bytes": 5141502,
      "sha256": "29755f31ea6270b31b9aa09c304a209a11faa7bc746b8e3f8e40658809f9ddea"
    }
  ]
}
```

## 2026-10-18T01:31:17.498+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "9ad73cb8833e41f7aa2d476075147495",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.png",
  "pid": 37900,
  "request_fingerprint": "153494aa82e485fe2a2edb260fca03a140cf63025b2dc3da69a4b24e20155ce0",
  "time": "2026-10-18T01:31:17.498+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg6_上河道神符点\n参考用法: 参考图只借世界的色板、河水与阔叶林岸的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的土路与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n林间一处开阔的河湾。河流在这里拐了一个缓弯，水面变宽、几乎静止，水深及膝，水色是透亮的暗青，近处能看见水底的圆石和摇动的水草。河湾中央略偏右，一块灰色的岩台平平地高出水面一掌，直径约三米，近乎圆形，顶面被多年的流水磨得光滑微凹，边缘长着一圈短短的绿苔，岩台上什么也没有。远景正中，阔叶林岸边一道长满青苔的石崖高约八米，一股细细的瀑布从崖顶的树根间垂落下来，落进崖脚的水潭，溅起一层白色的水雾，水潭的涟漪一圈圈荡开到河湾里。两岸都是高大的阔叶古树，树干粗壮、挂着藤蔓和长苔，树冠深绿，有几根大枝斜伸到水面上方；岸边是蕨、芦苇和被水冲上来的枯木；对岸的林缘里零星混着几棵深色的针叶松。\n[细节]\n- 视角: 视点在近岸浅水边，高度约一人，平视，35mm 焦距感，越过平静水面望向河湾中央的岩台与远处瀑布\n- 光线: 下午偏晚；太阳低悬在瀑布石崖的右上方，暖色阳光逆光斜照穿过树冠，水面上铺开一大片金色反光，岩台边缘和瀑布水雾被勾出亮边；近岸的树影把前景压暗；水雾里能看见斜射的光\n- 构图: 16:9 横幅；河湾水面占画面下半部；岩台在中央略偏右、处在三分线上；瀑布石崖在远景正中略偏左；两岸大树从左右两侧收边，伸向水面的大枝在画面上缘形成框；前景是近岸的浅水与几块露出水面的圆石\n- 道具: 近岸水边一截长苔的漂流木；岩台旁漂着几片落叶；对岸一丛高芦苇；画面里没有任何文字、旗帜、标记\n- 主色: 主 森林绿 / 辅 深灰岩石与暗青水色 / 点缀 白色瀑布水花 / 高光 水面暖金反光；自然色彩，不过饱和\n- 真实感: 这是在苏格兰西部一处真实林间河湾实地拍摄的奇幻电影外景剧照，不是渲染图：岩台有水渍分界线和细裂缝；苔藓有干湿深浅；水面有细小的漂浮物和风吹的细纹；瀑布水流粗细不均，不是一条平滑的白线\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，岩台上的发光物，符文刻字，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，桥梁，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:22.119+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "9ad73cb8833e41f7aa2d476075147495",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.png",
  "pid": 37900,
  "request_fingerprint": "153494aa82e485fe2a2edb260fca03a140cf63025b2dc3da69a4b24e20155ce0",
  "time": "2026-10-18T01:31:22.119+00:00",
  "event": "result",
  "elapsed_s": 4.61,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "pending"
  }
}
```

## 2026-10-18T01:31:22.136+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "2eda191fa5404706b27d41380af2f092",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:22.136+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:22.756+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "2eda191fa5404706b27d41380af2f092",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:22.756+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:26.784+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "146f1f7abb8741698655d16542c560c5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:26.784+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:27.388+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "146f1f7abb8741698655d16542c560c5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:27.388+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:31.411+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "566347c4a9114c49957ae1fdaf764f5b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:31.411+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:32.063+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "566347c4a9114c49957ae1fdaf764f5b",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:32.063+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:36.068+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "cae8e03a1491433f9ebc76bdb75a6562",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:36.068+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:36.699+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "cae8e03a1491433f9ebc76bdb75a6562",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:36.699+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:40.726+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "14287c2409024bfd806c16b19a2f99c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:40.726+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:41.480+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "14287c2409024bfd806c16b19a2f99c0",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:41.480+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:45.508+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "66436905b34943d997e1e5ed1df003c8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:45.508+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:46.141+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "66436905b34943d997e1e5ed1df003c8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:46.141+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:50.167+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "ce78ca3c491746c4949552254966cdab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:50.167+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:50.826+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "ce78ca3c491746c4949552254966cdab",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:50.826+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:54.858+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "e591b027a7c548cba9326fa35c469e6c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:54.858+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:31:55.566+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "e591b027a7c548cba9326fa35c469e6c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:55.566+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:31:59.607+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "d5ce1e29dc864096967cabea2d08c7d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:31:59.607+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:00.224+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "d5ce1e29dc864096967cabea2d08c7d7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:32:00.224+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:04.252+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — request

```json
{
  "request_id": "51eac682cb6942fc917c42e2eeb80406",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:32:04.252+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/cDb6v0ew8opAR47JfYBO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:05.059+00:00 — elevenlabs / GET /flows/image/cDb6v0ew8opAR47JfYBO — result

```json
{
  "request_id": "51eac682cb6942fc917c42e2eeb80406",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/cDb6v0ew8opAR47JfYBO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "8a27a4e033607e91d3fd1a88efb1a8cdb6b92aee60123a18134a47773701c92b",
  "time": "2026-10-18T01:32:05.059+00:00",
  "event": "result",
  "elapsed_s": 0.781,
  "response": {
    "id": "cDb6v0ew8opAR47JfYBO",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/XGTBkcjnKBRU67EOgk2E/cDb6v0ew8opAR47JfYBO/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013201Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:32:05.092+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "ef98126290cc4b57bec9690daab8df64",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "0d088d98b538a79c90e90c08719a9609aac0167177c3256ae36124387830afd5",
  "time": "2026-10-18T01:32:05.092+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/XGTBkcjnKBRU67EOgk2E/cDb6v0ew8opAR47JfYBO/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013201Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:32:07.774+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "ef98126290cc4b57bec9690daab8df64",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg6_上河道神符点\\bg6_上河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "0d088d98b538a79c90e90c08719a9609aac0167177c3256ae36124387830afd5",
  "time": "2026-10-18T01:32:07.774+00:00",
  "event": "result",
  "elapsed_s": 2.656,
  "response": [
    200,
    {
      "bytes": 5573614,
      "sha256": "207187c8b4f4bb870969aa6f1ca899cb60082b292718a76edb82a5a0c6b1e3a2"
    }
  ]
}
```

## 2026-10-18T01:32:07.849+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "abeef8a00f89414ca57f7ecc691c3768",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.png",
  "pid": 37900,
  "request_fingerprint": "f25d0064a73c4173f6902aa2077137102bc1ebbfbdf31ac7dbc8acc4e1844037",
  "time": "2026-10-18T01:32:07.849+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg7_下河道神符点\n参考用法: 参考图只借世界的色板、河水与针叶松岸的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的土路与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n岩崖脚下一段湍急的河道。河面在这里收窄到二十多米，水流从画面左后方冲来，在浅滩的乱石间翻起一道道白浪，水色是发灰的暗青。河中央偏左，一块灰色的平顶岩台高出水面一掌，直径约三米，近乎圆形，顶面被水磨得光滑，上游一侧被水流冲出一道弧形的白浪，下游一侧拖着一条平静的回水，岩台上什么也没有。画面右侧，一道黑灰色的岩崖从河岸直直升起，高约二十米，崖面层层叠叠、布满竖向的裂缝，背阴的凹处结着白霜和细小的冰凌，崖顶长着几棵歪斜的针叶松；崖脚靠近水面的地方有一道一人多高的幽暗岩缝，像一条通往山腹深处的通道，里面黑得看不见底。画面左侧是一道陡坡，坡上密密立着深色的针叶松，松针发黑，地面是暗褐色的泥土，夹着几块紫黑色的地衣和薄霜，坡脚的河岸上堆着被冲刷得发白的漂流木。\n[细节]\n- 视角: 视点在左岸坡脚的河边乱石上，高度约一人，平视略俯，32mm 焦距感，斜着望向河中岩台与对面的岩崖\n- 光线: 清晨阴天；天空是一片均匀的冷灰色，天光柔而冷，没有明确的阳光方向，阴影几乎没有边；河面上贴着一层薄薄的晨雾，越往下游越浓；白浪和湿石面反着冷白的天光；岩缝里是全黑的\n- 构图: 16:9 横幅；河道从左后方斜到右前方，占画面中央；岩台在中央偏左；岩崖占右侧三分之一，岩缝在右下；左侧是针叶松陡坡；前景是近岸的湿滑乱石与浅水\n- 道具: 前景乱石上搭着一截发白的漂流木；岩台下游回水里打着转的几根松枝；岩崖脚下几块崩落的碎石；画面里没有任何文字、旗帜、标记\n- 主色: 主 黑灰岩与墨绿针叶 / 辅 暗青灰水色 / 点缀 紫黑地衣、白浪 / 高光 雾里的冷白天光；自然色彩，不过饱和\n- 真实感: 这是在挪威一处真实峡湾支流河段实地拍摄的奇幻电影外景剧照，不是渲染图：岩崖有水流冲出的黑色水痕和白色矿物析出；乱石上有湿滑的青苔；白浪有大有小、有飞溅的水珠；晨雾有浓有淡，不是均匀的一层\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，岩缝里的怪物或眼睛，岩台上的发光物，符文刻字，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，桥梁，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:13.192+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "abeef8a00f89414ca57f7ecc691c3768",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.png",
  "pid": 37900,
  "request_fingerprint": "f25d0064a73c4173f6902aa2077137102bc1ebbfbdf31ac7dbc8acc4e1844037",
  "time": "2026-10-18T01:32:13.192+00:00",
  "event": "result",
  "elapsed_s": 5.313,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "pending"
  }
}
```

## 2026-10-18T01:32:13.232+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "affbb6dc168c48b79328049865e2b0b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:13.232+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:13.881+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "affbb6dc168c48b79328049865e2b0b8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:13.881+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:17.911+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "3c9fc7b9517f4091bfb285e043a8a28e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:17.911+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:18.524+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "3c9fc7b9517f4091bfb285e043a8a28e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:18.524+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:22.553+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "0abefc345dde49b0bb8d83c1b10d8a72",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:22.553+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:23.217+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "0abefc345dde49b0bb8d83c1b10d8a72",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:23.217+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:27.249+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "d9780593b0a64a6b92899447ff131f67",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:27.249+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:29.169+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "d9780593b0a64a6b92899447ff131f67",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:29.169+00:00",
  "event": "result",
  "elapsed_s": 1.89,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:33.189+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "197f761027414820a41f9ef61b0b9556",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:33.189+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:34.156+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "197f761027414820a41f9ef61b0b9556",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:34.156+00:00",
  "event": "result",
  "elapsed_s": 0.922,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:38.184+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "290a8b63de4342998d87ebac0d28b22a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:38.184+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:38.806+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "290a8b63de4342998d87ebac0d28b22a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:38.806+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:42.843+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "7c0b42c1ac0e4533a2270ef03d471152",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:42.843+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:43.488+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "7c0b42c1ac0e4533a2270ef03d471152",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:43.488+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:47.526+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "d0b2ceaef4194235b3afe7215f595b19",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:47.526+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:48.189+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "d0b2ceaef4194235b3afe7215f595b19",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:48.189+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:52.217+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "2e9c011242da41d087475e5325d62bce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:52.217+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:52.869+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "2e9c011242da41d087475e5325d62bce",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:52.869+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "generating"
  }
}
```

## 2026-10-18T01:32:56.897+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — request

```json
{
  "request_id": "46a37ea4fbde4ff794c2ad046672d0de",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:56.897+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/CxvsaerdNtHxdlUzQuqX",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:32:57.683+00:00 — elevenlabs / GET /flows/image/CxvsaerdNtHxdlUzQuqX — result

```json
{
  "request_id": "46a37ea4fbde4ff794c2ad046672d0de",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/CxvsaerdNtHxdlUzQuqX",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "e38d1fcd24ee5b198cd5396756952239a141e0a69de13527aaa44f587e4fca68",
  "time": "2026-10-18T01:32:57.683+00:00",
  "event": "result",
  "elapsed_s": 0.766,
  "response": {
    "id": "CxvsaerdNtHxdlUzQuqX",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/tfRpWGm91HFWw7Mj4cnK/CxvsaerdNtHxdlUzQuqX/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013256Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:32:57.719+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "588813b4edd14bd0ad6e6de45085d773",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "19f6a978ebfe850c5e5cb510978019d6dec305e72c44204fa0abdecd40659f4c",
  "time": "2026-10-18T01:32:57.719+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/tfRpWGm91HFWw7Mj4cnK/CxvsaerdNtHxdlUzQuqX/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013256Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:33:01.391+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "588813b4edd14bd0ad6e6de45085d773",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg7_下河道神符点\\bg7_下河道神符点.part.png",
  "pid": 37900,
  "request_fingerprint": "19f6a978ebfe850c5e5cb510978019d6dec305e72c44204fa0abdecd40659f4c",
  "time": "2026-10-18T01:33:01.391+00:00",
  "event": "result",
  "elapsed_s": 3.64,
  "response": [
    200,
    {
      "bytes": 5599430,
      "sha256": "ba432b2d3356f4924f6dc71f218173b6e906324554c2b9cb91b4a6541a11e0af"
    }
  ]
}
```

## 2026-10-18T01:33:01.461+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "08638a44ca6a4907a30ce20578b3d1f8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.png",
  "pid": 37900,
  "request_fingerprint": "f79f8b6bd874ce9aa07612b6cb5a0a8980e3bf6c18d9c5d8786388606b383b79",
  "time": "2026-10-18T01:33:01.461+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg8_近卫野区空地\n参考用法: 参考图只借世界的色板、阔叶林的质感与光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n古老密林深处的一块空地。空地近乎圆形，直径约二十五米，地面是被踩得发秃的草皮和裸露的黑褐泥土，铺着一层褐黄色的落叶和碎枝，几处长着倔强的野草和小蘑菇。空地四周是一圈密不透风的树墙：老橡和山毛榉的树干一棵挨着一棵，粗的要两人合抱，树皮深灰、长满苔藓和地衣，树干之间塞满齐胸高的冬青灌木和蕨，看不穿后面的林子；只有画面左后方和右侧各有一道窄窄的缝隙，透出后面更暗的林间小径。空地中央偏后有一圈用拳头大的石块围成的火塘，直径一米多，里面是早已熄灭冷透的灰烬和几截烧黑的木头，没有火也没有烟；画面左侧横卧着一截长满青苔的倒木，树皮上被坐出了光滑的凹痕；右前方一块半人高的灰色巨石，石面覆着地衣。头顶是层层叠叠的树冠，深绿色、背阴处泛紫，只在几处露出小块天空。\n[细节]\n- 视角: 视点在空地边缘的树墙前，高度约一人，平视，28mm 焦距感，横穿空地望向对面的树墙\n- 光线: 正午前后；阳光只从树冠的三四个缺口漏下来，在空地上投出几块边缘清晰的明亮光斑，一块落在火塘旁，一块落在倒木上；光斑以外是大片带绿的深影；空气里漂着细小的尘埃和飞虫，在光束里可见；树墙深处几乎全黑\n- 构图: 16:9 横幅；空地占画面中央和下半部；对面的树墙横贯画面上半部；火塘在中央偏后，倒木在左侧，巨石在右前方；树墙的两道窄缝分别在左后与右侧；前景是空地边缘的落叶与几根蕨叶\n- 道具: 火塘旁一小堆劈好的柴，长了青苔；倒木下几个白色小蘑菇；巨石脚下一截锈蚀的断铁片；画面里没有任何文字、旗帜、标记\n- 主色: 主 深森林绿 / 辅 褐黄落叶与裸土 / 点缀 苔绿 / 高光 光斑里的暖白；自然色彩，不过饱和\n- 真实感: 这是在英格兰一片真实古林深处实地拍摄的奇幻电影外景剧照，不是渲染图：落叶有干有湿、有腐烂发黑的；树干有断枝疤和树洞；泥土上有积水的小坑和动物爪印；石块大小不一，长着地衣\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，帐篷，燃烧的火，烟，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:11.806+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "08638a44ca6a4907a30ce20578b3d1f8",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.png",
  "pid": 37900,
  "request_fingerprint": "f79f8b6bd874ce9aa07612b6cb5a0a8980e3bf6c18d9c5d8786388606b383b79",
  "time": "2026-10-18T01:33:11.806+00:00",
  "event": "result",
  "elapsed_s": 10.297,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "pending"
  }
}
```

## 2026-10-18T01:33:11.824+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "3f20a0992f8d4e499806be57ce1e2f8d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:11.824+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:12.459+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "3f20a0992f8d4e499806be57ce1e2f8d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:12.459+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:16.493+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "c1edbfca93644e5cba99e20164f2c462",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:16.493+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:17.142+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "c1edbfca93644e5cba99e20164f2c462",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:17.142+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:21.184+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "2c4d89283fd64612acd03efd06219ba6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:21.184+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:21.823+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "2c4d89283fd64612acd03efd06219ba6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:21.823+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:25.870+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "75c267d7660941e79a8bff5a29395eb1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:25.870+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:26.488+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "75c267d7660941e79a8bff5a29395eb1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:26.488+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:30.516+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "64f396ddecd94e0b895e9ab67f8d55b3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:30.516+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:31.183+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "64f396ddecd94e0b895e9ab67f8d55b3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:31.183+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:35.208+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "b7ae2582b10c427991723e3a0eeae8c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:35.208+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:35.900+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "b7ae2582b10c427991723e3a0eeae8c9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:35.900+00:00",
  "event": "result",
  "elapsed_s": 0.672,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:39.924+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "ee55914590644a468f70ee1b9fe99504",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:39.924+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:40.584+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "ee55914590644a468f70ee1b9fe99504",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:40.584+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:44.617+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "291ff05d36ab49b2bc6835abaa403cc6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:44.617+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:45.244+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "291ff05d36ab49b2bc6835abaa403cc6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:45.244+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:49.268+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "434caebe2f7d4e018c495421ff239485",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:49.268+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:49.909+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "434caebe2f7d4e018c495421ff239485",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:49.909+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:53.931+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "7d8b937f636b4bbdb4ae7b15ab35f1b5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:53.931+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:54.555+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "7d8b937f636b4bbdb4ae7b15ab35f1b5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:54.555+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "generating"
  }
}
```

## 2026-10-18T01:33:58.599+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — request

```json
{
  "request_id": "b7f1b6f17c524545bf6c0f363cdd7210",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:58.599+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/JUKHwO7LKzyWlMEDSlhx",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:33:59.358+00:00 — elevenlabs / GET /flows/image/JUKHwO7LKzyWlMEDSlhx — result

```json
{
  "request_id": "b7f1b6f17c524545bf6c0f363cdd7210",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/JUKHwO7LKzyWlMEDSlhx",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "acb338f09b88bc6d7dbc4184b977b625c9857eebe7c8084940b7a05f3aee7549",
  "time": "2026-10-18T01:33:59.358+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "JUKHwO7LKzyWlMEDSlhx",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/MTJWePQXmJOtfihjFtHd/JUKHwO7LKzyWlMEDSlhx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013357Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:33:59.393+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "233edc08680d43658fbb522e85682690",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "11f008c2c72e014f65d79d9cc9f9e8ae745794948a7b08a2b82ec68605dffe3d",
  "time": "2026-10-18T01:33:59.393+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/MTJWePQXmJOtfihjFtHd/JUKHwO7LKzyWlMEDSlhx/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013357Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:34:02.280+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "233edc08680d43658fbb522e85682690",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg8_近卫野区空地\\bg8_近卫野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "11f008c2c72e014f65d79d9cc9f9e8ae745794948a7b08a2b82ec68605dffe3d",
  "time": "2026-10-18T01:34:02.280+00:00",
  "event": "result",
  "elapsed_s": 2.86,
  "response": [
    200,
    {
      "bytes": 5721327,
      "sha256": "4fb74ddb0c1af5c6dc847b44d4e47e4b62f23c58d4024207cb20d479cb84e2e9"
    }
  ]
}
```

## 2026-10-18T01:34:02.355+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "d7c2fba4a6424855b69507dd109a1a12",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.png",
  "pid": 37900,
  "request_fingerprint": "b530fa35888d25e6c7ae4436b90271154d6e19fcd71fc2f509a7ee687e181e22",
  "time": "2026-10-18T01:34:02.355+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg9_天灾野区空地\n参考用法: 参考图只借世界的色板、紫黑荒地与针叶松的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n阴暗云杉林深处的一块冻土空地。空地呈不规则的椭圆，直径约二十米，地面是暗褐色的冻泥，冻得坑坑洼洼，上面大片大片地爬着紫黑色的地衣和霉斑一样的腐化纹理，夹着碎冰碴、枯黄的硬草和几处没有化尽的灰白残雪。四周是一圈挨得很密的黑色云杉树墙，树干笔直、树皮暗灰，下半截的枯枝向外支棱着，树冠尖而密，针叶发黑，枝头挂着薄霜；树下是一层被压得很暗的低矮灌木，看不穿后面；只有画面右后方有一道窄缝，透出一点更深处的冷雾。空地里和树墙边有三四棵已经死去的云杉，只剩灰白色的枯干和折断的光枝，其中一棵斜倒着靠在别的树上。空地中央偏右堆着一小堆被啃得发白的大型兽骨，肋骨和长骨交错，有的已经发黄裂开；左前方的一块冻土上有几道被巨大利爪刨出的深沟，翻起的泥块边缘结着霜。\n[细节]\n- 视角: 视点在空地边缘的树墙前，高度约一人，平视略俯，28mm 焦距感，横穿空地望向对面的树墙\n- 光线: 阴天傍晚；天光很低，从树冠上方均匀地漏下来，发灰发蓝，没有阳光斑也没有明确的影子方向，阴影柔而均匀；冷雾堆积在树墙脚下和那道窄缝里，越远越浓；霜与残雪是画面里最亮的地方\n- 构图: 16:9 横幅；空地占画面中央和下半部；对面的黑云杉树墙横贯画面上半部；兽骨堆在中央偏右；爪沟冻土在左前方；斜倒的枯干在左后方形成一道斜线；前景是空地边缘覆霜的地衣与硬草\n- 道具: 兽骨堆旁一截断裂的弯角；树墙脚下几块覆霜的黑石；一根折断的枯枝横在前景；画面里没有任何文字、旗帜、标记\n- 主色: 主 紫黑与墨绿 / 辅 暗褐冻泥 / 点缀 骨白、残雪白 / 高光 冷蓝天光；自然色彩，不过饱和\n- 真实感: 这是在芬兰北部一片真实阴暗云杉林里实地拍摄的奇幻电影外景剧照，不是渲染图：冻泥有冻胀裂纹和踩踏的旧痕；地衣成片不均，边缘露出裸泥；兽骨有啃痕、污渍和苔斑；残雪发灰、夹着松针和泥点\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，完整骷髅，人类头骨，血迹，燃烧的火，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:07.206+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "d7c2fba4a6424855b69507dd109a1a12",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.png",
  "pid": 37900,
  "request_fingerprint": "b530fa35888d25e6c7ae4436b90271154d6e19fcd71fc2f509a7ee687e181e22",
  "time": "2026-10-18T01:34:07.206+00:00",
  "event": "result",
  "elapsed_s": 4.828,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "pending"
  }
}
```

## 2026-10-18T01:34:07.224+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "72ff3dbfa8154ba9ad16687d8f0595ed",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:07.224+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:07.798+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "72ff3dbfa8154ba9ad16687d8f0595ed",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:07.798+00:00",
  "event": "result",
  "elapsed_s": 0.546,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "pending"
  }
}
```

## 2026-10-18T01:34:11.804+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "dd835ffa3c484a27bd20fdd3e8726572",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:11.804+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:12.487+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "dd835ffa3c484a27bd20fdd3e8726572",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:12.487+00:00",
  "event": "result",
  "elapsed_s": 0.688,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:16.516+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "9bbef85e34024d4e9fe30ea89030def2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:16.516+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:17.149+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "9bbef85e34024d4e9fe30ea89030def2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:17.149+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:21.183+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "302667b2bdf64d6b8c7e2fa15ef1a2e5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:21.183+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:44.845+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "302667b2bdf64d6b8c7e2fa15ef1a2e5",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:44.845+00:00",
  "event": "result",
  "elapsed_s": 23.625,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:48.886+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "0a01bdd3bac34fb08ea8546bca677292",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:48.886+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:49.537+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "0a01bdd3bac34fb08ea8546bca677292",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:49.537+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:53.572+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "1bf395c56783429b9e54dc3622655012",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:53.572+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:54.219+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "1bf395c56783429b9e54dc3622655012",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:54.219+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "generating"
  }
}
```

## 2026-10-18T01:34:58.258+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — request

```json
{
  "request_id": "bc00578b0fad4b81bc56eb8b00be45f6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:58.258+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/lWo5mupFIN7PVPdamZlr",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:34:59.049+00:00 — elevenlabs / GET /flows/image/lWo5mupFIN7PVPdamZlr — result

```json
{
  "request_id": "bc00578b0fad4b81bc56eb8b00be45f6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/lWo5mupFIN7PVPdamZlr",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "fde9f5ad7c92fe48cf0bdf10413757cad1273b90017e1f6499dbb57be9003957",
  "time": "2026-10-18T01:34:59.049+00:00",
  "event": "result",
  "elapsed_s": 0.766,
  "response": {
    "id": "lWo5mupFIN7PVPdamZlr",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/GrJH74DxoJbvnoak6WPy/lWo5mupFIN7PVPdamZlr/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013455Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:34:59.068+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "3c323c9f17d04793bd5d6b005f2d91aa",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "a965505c8d722751a47f598433d5ec230b1cb121cbcdabce7eebf1d3b6bc3f45",
  "time": "2026-10-18T01:34:59.068+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/GrJH74DxoJbvnoak6WPy/lWo5mupFIN7PVPdamZlr/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013455Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:35:01.140+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "3c323c9f17d04793bd5d6b005f2d91aa",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg9_天灾野区空地\\bg9_天灾野区空地.part.png",
  "pid": 37900,
  "request_fingerprint": "a965505c8d722751a47f598433d5ec230b1cb121cbcdabce7eebf1d3b6bc3f45",
  "time": "2026-10-18T01:35:01.140+00:00",
  "event": "result",
  "elapsed_s": 2.047,
  "response": [
    200,
    {
      "bytes": 5687322,
      "sha256": "203895c888870d1b63da17bdad6f046f080f1f8109adb310cf94851fa913eeec"
    }
  ]
}
```

## 2026-10-18T01:35:01.172+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "2b4d6878abe54ab48476006fc494f301",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.png",
  "pid": 37900,
  "request_fingerprint": "b36662967f704d5d03aeb6268336ae685f5c2008b3eba494ae174c6a577e693b",
  "time": "2026-10-18T01:35:01.172+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg10_巨兽巢穴\n参考用法: 参考图只借世界的色板、岩石与河水的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n河岸边一个下沉的巨大岩坑。坑底近乎圆形，直径约三十米，比外面的河岸低三四米，地面铺着灰褐色的碎岩和粗砂砾，散着许多桌面大小的石块，有些被压得粉碎、碾成一摊摊石屑，地上还有几道又宽又深的拖痕，从坑中央一直拖到岩壁脚下，像有极重的东西在这里来回走动。三面是高约二十五米的黑灰色玄武岩壁，岩壁下半部是一根根竖立的多棱石柱，上半部是层层叠叠、粗糙崩裂的岩块，有几处向坑内悬出；岩壁中间隐约夹着一两道细长的暗紫色矿脉，只在湿处才看得出颜色；岩缝里渗着水，挂着一道道湿黑的水痕，缝隙边长着蕨和湿苔。岩坑上方大部分敞开，看得见低低的灰云，坑沿上倒挂着几丛灌木和垂下的根须。画面左侧的岩壁开着一道宽约八米的斜坡豁口，碎石坡从坑底向上通到外面，豁口外露出一截发亮的河面和对岸模糊的针叶林。\n[细节]\n- 视角: 视点在坑底靠后的一侧，贴近地面、约膝盖高度，明显仰视高耸的岩壁，20mm 广角感，坑口的天空入画\n- 光线: 阴天；灰白色的天光从敞开的坑口均匀洒下，坑底中央最亮，越靠近岩壁越暗，岩壁脚下几乎没入阴影；豁口外的河面反着冷白的天光，是画面左侧的第二个亮区；湿岩面泛着冷灰的哑光\n- 构图: 16:9 横幅；坑底占画面下三分之一，中央是空着的碎岩地面，留给人物站位；三面岩壁从左右和后方高高耸起，占据画面上半部；斜坡豁口在左侧三分之一；坑口的一线灰天在画面上缘\n- 道具: 坑底几块被压裂成两半的巨石；拖痕尽头一堆碎成粉末的石屑；豁口坡上几根被冲进来的漂流木；画面里没有任何文字、旗帜、标记\n- 主色: 主 黑灰玄武岩 / 辅 灰褐砂砾 / 点缀 暗紫矿脉、苔绿 / 高光 坑口天光；自然色彩，不过饱和\n- 真实感: 这是在苏格兰斯凯岛一处真实玄武岩海蚀岩谷实地拍摄的奇幻电影外景剧照，不是渲染图：石柱棱角有崩口和风化；碎石大小混杂、有尖有圆；湿处颜色深、干处发灰；苔与蕨只长在有水的缝里\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，水印，logo，任何人物，任何动物，怪物，石头巨人，宝箱，金币堆，紫色发光，水晶洞，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:05.079+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "2b4d6878abe54ab48476006fc494f301",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.png",
  "pid": 37900,
  "request_fingerprint": "b36662967f704d5d03aeb6268336ae685f5c2008b3eba494ae174c6a577e693b",
  "time": "2026-10-18T01:35:05.079+00:00",
  "event": "result",
  "elapsed_s": 3.875,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "pending"
  }
}
```

## 2026-10-18T01:35:05.103+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "4f7f67b2bf494160bb246c2410579822",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:05.103+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:05.753+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "4f7f67b2bf494160bb246c2410579822",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:05.753+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:09.788+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "226815a27b474be6a079ef1505cce1f1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:09.788+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:10.401+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "226815a27b474be6a079ef1505cce1f1",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:10.401+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:14.416+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "6a74625e0d854104aebfc86a79e38747",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:14.416+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:15.050+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "6a74625e0d854104aebfc86a79e38747",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:15.050+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:19.075+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "16d37597349e44a09aee8d49c12b00e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:19.075+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:19.675+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "16d37597349e44a09aee8d49c12b00e2",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:19.675+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:23.713+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "3076e3c8b5d34dde83f2a0c84a75744d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:23.713+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:24.359+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "3076e3c8b5d34dde83f2a0c84a75744d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:24.359+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:28.382+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "5704d7cb94ec423ababe64a7b6b11386",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:28.382+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:28.987+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "5704d7cb94ec423ababe64a7b6b11386",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:28.987+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:33.012+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "30a928d0d66a4d21bb7ef68648830d2f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:33.012+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:33.597+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "30a928d0d66a4d21bb7ef68648830d2f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:33.597+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:37.605+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "2b19482c52e44d9eb9f6cdbff4b26771",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:37.605+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:38.220+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "2b19482c52e44d9eb9f6cdbff4b26771",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:38.220+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:42.245+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "9dcef8a7e820482dbe4715b3c7e2a4e8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:42.245+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:42.889+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "9dcef8a7e820482dbe4715b3c7e2a4e8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:42.889+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "generating"
  }
}
```

## 2026-10-18T01:35:46.916+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — request

```json
{
  "request_id": "61ddffe8dd3a4d0eb70666f784185188",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:46.916+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/nh10VGS8qRe1qCkJBmLM",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:47.680+00:00 — elevenlabs / GET /flows/image/nh10VGS8qRe1qCkJBmLM — result

```json
{
  "request_id": "61ddffe8dd3a4d0eb70666f784185188",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/nh10VGS8qRe1qCkJBmLM",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "64934d9fce9ba75814e5e5cd26eea8d11a082fa717f8e289724bdc6925fa5040",
  "time": "2026-10-18T01:35:47.680+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "nh10VGS8qRe1qCkJBmLM",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/vcaB2F9yk6orsrcALclG/nh10VGS8qRe1qCkJBmLM/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013546Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:35:47.701+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "54aeadf792e041db97b9c0f2046c6f88",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "9d073b8a22e7e84796006351c282e68348ed7bf5ae11a364d200922789da179a",
  "time": "2026-10-18T01:35:47.701+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/vcaB2F9yk6orsrcALclG/nh10VGS8qRe1qCkJBmLM/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013546Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:35:50.162+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "54aeadf792e041db97b9c0f2046c6f88",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\river\\bg10_巨兽巢穴\\bg10_巨兽巢穴.part.png",
  "pid": 37900,
  "request_fingerprint": "9d073b8a22e7e84796006351c282e68348ed7bf5ae11a364d200922789da179a",
  "time": "2026-10-18T01:35:50.162+00:00",
  "event": "result",
  "elapsed_s": 2.437,
  "response": [
    200,
    {
      "bytes": 5363883,
      "sha256": "833fef3d90bed88f25b6de36ade7ad4e7932dc590abb5c5338a87fdcdce21dc7"
    }
  ]
}
```

## 2026-10-18T01:35:50.210+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "0b646658568344b19d041db6443f5057",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.png",
  "pid": 37900,
  "request_fingerprint": "407b10160a67e6db7c4ecdd84c5a469b1551cac74a5dd25ca2f9470fcbdf3968",
  "time": "2026-10-18T01:35:50.210+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg11_秘密商店\n参考用法: 参考图只借世界的色板、阔叶林的质感与光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n老林深处一块隐蔽的凹地里，一个简陋的临时货摊。凹地比周围低一人多，三面被长满青苔的巨石和盘曲裸露的粗大树根围住，只有画面右侧留着一条被踩出来的窄小土径通出去。凹地后部两棵老阔叶树相距约四米，树干之间斜斜地撑起一张浸过油的深褐色帆布篷，篷布有补丁和烧焦的小洞，四角用麻绳拴在树干和一根插进地里的木杆上，边缘垂着水滴。篷下是一张用三块粗木板搭在两只木桶上的柜台，台面磨得发亮、有刀痕和蜡渍；柜台后面堆着几只带铁箍的旧木箱、几个鼓鼓的麻袋、一堆用粗布严严盖住、只看得出长短轮廓的货物，以及一只上着大铁锁的铁皮箱；柜台与货堆之间留着一人宽的空地。木杆顶端挂着一盏铁皮提灯，灯罩是熏黑的玻璃，里面的烛火点着。凹地地面是黑褐泥土和厚厚的落叶，几块踏脚的扁石通往柜台。\n[细节]\n- 视角: 视点在凹地前缘的落叶上，高度约一人，平视略俯，35mm 焦距感，正对柜台稍偏左\n- 光线: 阴天；林冠很密，林下是暗淡的灰绿色漫射光，阴影软而深；提灯里的烛火是画面里唯一的暖色真实光源，只照亮柜台台面、近旁的木箱和篷布内侧一小圈，光圈之外迅速暗下去；画面里没有别的火\n- 构图: 16:9 横幅；帆布篷与柜台占画面中央三分之一；左侧是长苔巨石与树根，右侧是通出去的窄土径；前景是落叶与踏脚扁石；篷顶与两棵老树的树干在画面上半部收边\n- 道具: 柜台上一架小铜秤、一只空木碗；木桶旁靠着一根带铁头的长杆；篷角挂着一串晒干的草药；画面里没有任何文字、招牌、旗帜、标记\n- 主色: 主 深森林绿与暗褐帆布 / 辅 旧木褐、锈铁 / 点缀 提灯暖橙 / 高光 灯下的木面；自然色彩，不过饱和\n- 真实感: 这是在威尔士一处真实老林峡谷里实地拍摄、搭建实景货摊的奇幻电影外景剧照，不是渲染图：帆布有油渍、霉点和磨薄的地方；木箱有裂缝、铁箍生锈；麻袋粗糙起毛；泥地上有脚印和积水\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，招牌字，水印，logo，任何人物，任何动物，陈列的武器展台，发光的宝物，金币堆，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，塑料布，电灯，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:53.528+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "0b646658568344b19d041db6443f5057",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.png",
  "pid": 37900,
  "request_fingerprint": "407b10160a67e6db7c4ecdd84c5a469b1551cac74a5dd25ca2f9470fcbdf3968",
  "time": "2026-10-18T01:35:53.528+00:00",
  "event": "result",
  "elapsed_s": 3.297,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "pending"
  }
}
```

## 2026-10-18T01:35:53.550+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "1bf49bf86ca345d69d6b87e72d811c56",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:35:53.550+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:54.191+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "1bf49bf86ca345d69d6b87e72d811c56",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:35:54.191+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "pending"
  }
}
```

## 2026-10-18T01:35:58.213+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "a9fabd4cab7f4907851fa8ac427f1847",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:35:58.213+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:35:58.833+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "a9fabd4cab7f4907851fa8ac427f1847",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:35:58.833+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:02.860+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "58d331d3e8ed4218bbe8d059cf490cfe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:02.860+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:03.465+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "58d331d3e8ed4218bbe8d059cf490cfe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:03.465+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:07.494+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "6ff09d57d93949e48dcab5dcbd34775e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:07.494+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:08.274+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "6ff09d57d93949e48dcab5dcbd34775e",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:08.274+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:12.311+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "e452d6e28c604c63ad39a87d8695de60",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:12.311+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:12.950+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "e452d6e28c604c63ad39a87d8695de60",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:12.950+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:16.970+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "be937c1f263e43fba50d7dbbc2f3c1c3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:16.970+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:17.586+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "be937c1f263e43fba50d7dbbc2f3c1c3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:17.586+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:21.608+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "9631bc3afb2d4989bf06c23d6c74ba9d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:21.608+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:22.242+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "9631bc3afb2d4989bf06c23d6c74ba9d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:22.242+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:26.263+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "efb9f95423334d4ca90f2ad426a968b9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:26.263+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:26.895+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "efb9f95423334d4ca90f2ad426a968b9",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:26.895+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:30.913+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "6c9dc1f4f5284dd4b196f97b1fbaf549",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:30.913+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:31.529+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "6c9dc1f4f5284dd4b196f97b1fbaf549",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:31.529+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:35.553+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "5fbd5505eb334914b5bec9420c5e9445",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:35.553+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:36.447+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "5fbd5505eb334914b5bec9420c5e9445",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:36.447+00:00",
  "event": "result",
  "elapsed_s": 0.891,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:40.464+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — request

```json
{
  "request_id": "ea84fda5eaba43adb018b4efd3e30b48",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:40.464+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/EEJ0Ezin7HULb6qHt4Gi",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:41.230+00:00 — elevenlabs / GET /flows/image/EEJ0Ezin7HULb6qHt4Gi — result

```json
{
  "request_id": "ea84fda5eaba43adb018b4efd3e30b48",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/EEJ0Ezin7HULb6qHt4Gi",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8d02a850b04e7d04504570432395c645e136e22032e8d3e6d28cd2210b8b66fb",
  "time": "2026-10-18T01:36:41.230+00:00",
  "event": "result",
  "elapsed_s": 0.734,
  "response": {
    "id": "EEJ0Ezin7HULb6qHt4Gi",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/MQxsErfXBqBWTndJwOqr/EEJ0Ezin7HULb6qHt4Gi/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013638Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:36:41.233+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "fd0de1c0953743d9bb13d7cb736db495",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "0393a830bb5df7d34dd473a04e54fe20b2c031f1acb7bc9bc78045f93c1d860f",
  "time": "2026-10-18T01:36:41.233+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/MQxsErfXBqBWTndJwOqr/EEJ0Ezin7HULb6qHt4Gi/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013638Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:36:43.228+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "fd0de1c0953743d9bb13d7cb736db495",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg11_秘密商店\\bg11_秘密商店.part.png",
  "pid": 37900,
  "request_fingerprint": "0393a830bb5df7d34dd473a04e54fe20b2c031f1acb7bc9bc78045f93c1d860f",
  "time": "2026-10-18T01:36:43.228+00:00",
  "event": "result",
  "elapsed_s": 1.969,
  "response": [
    200,
    {
      "bytes": 5200871,
      "sha256": "961d6600154297a0fd8c623a8e35a9214a9ea90112fbcc540322abaf33d7466d"
    }
  ]
}
```

## 2026-10-18T01:36:43.259+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "4edd756da5b24320addc1ce8a01c4164",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.png",
  "pid": 37900,
  "request_fingerprint": "c2e5e50e68a759037f2ab089c4fb630d59327470d311939632973affcefe43c7",
  "time": "2026-10-18T01:36:43.259+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg12_边路地精商店\n参考用法: 参考图只借世界的色板、阔叶林与土路的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n林边土路旁一处小小的交易点。一条被踩实的土路从画面左前方经过，路边一块平整的空地上立着一间约四米见方、低矮的小铺：墙是用长短不一的旧木板拼钉起来的，有的板子刷过褪色的红漆、有的是原木，接缝处钉着铁皮补片；屋顶是一块块铆接起来的铁皮，钉头成排，边缘卷起，积着落叶；屋顶一角伸出一根歪斜的铁皮烟囱，用铁丝拉着，正冒出一缕细细的灰烟。小铺正面开着一扇向上翻起的木板窗，翻板用两根木棍撑着当遮阳，窗下伸出一块厚木台当柜台，窗上还斜搭着一块打着补丁的土黄色帆布；门边立着一具手摇木吊臂，木轴缠着粗绳，绳头挂着一只空铁钩。铺子右侧是一堆码得歪歪扭扭的货：带铁箍的木箱摞成三四层，几只木桶侧放着用木楔卡住，桶外壁有被火燎过的焦痕，旁边是几卷粗麻绳和一辆盖着油布的两轮推车。小铺背后是一道高大的阔叶林墙，树冠深绿。\n[细节]\n- 视角: 视点在土路对侧的路边，高度约一人，平视，35mm 焦距感，正对小铺偏右，把货堆一起装进来\n- 光线: 晴天正午偏后；阳光从画面左上方照下，铁皮屋顶和铁箍反出亮光，木板墙向光面暖褐、背光面深褐；小铺在右后方地上投下短而清晰的影子；林墙是深绿色的背景，林下偏暗；烟囱的灰烟被风吹得斜向右边；画面里看不见火\n- 构图: 16:9 横幅；小铺占画面中央偏左三分之一；货堆在右侧三分之一；土路从左前方横过画面下缘；林墙横贯画面上半部；柜台前留出一片空地给人物站位\n- 道具: 柜台上一只小铁皮盒和一盏没点的油灯；吊臂下散着几块木屑；推车轮边靠着一把铁锹；画面里没有任何文字、招牌、旗帜、标记\n- 主色: 主 旧木褐与锈铁灰 / 辅 森林绿背景 / 点缀 补丁帆布的土黄与褪色红 / 高光 铁皮反光；自然色彩，不过饱和\n- 真实感: 这是在加拿大不列颠哥伦比亚一处真实老伐木营地遗址实地拍摄、搭建实景小铺的奇幻电影外景剧照，不是渲染图：木板有虫眼、裂纹和雨水留下的黑色水痕；铁皮有锈斑、凹坑和划痕；木桶的铁箍锈蚀；土路有车辙和泥块\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，招牌字，水印，logo，任何人物，任何动物，蒸汽朋克机器人，齿轮堆砌，霓虹，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，塑料桶，电线，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:46.406+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "4edd756da5b24320addc1ce8a01c4164",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.png",
  "pid": 37900,
  "request_fingerprint": "c2e5e50e68a759037f2ab089c4fb630d59327470d311939632973affcefe43c7",
  "time": "2026-10-18T01:36:46.406+00:00",
  "event": "result",
  "elapsed_s": 3.125,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "pending"
  }
}
```

## 2026-10-18T01:36:46.428+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "d9ad570a07884bf98fb7ac3912a04ad3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:46.428+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:47.158+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "d9ad570a07884bf98fb7ac3912a04ad3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:47.158+00:00",
  "event": "result",
  "elapsed_s": 0.718,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:51.182+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "3496fe83b01c4d7488d7acc2b9a9ee14",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:51.182+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:51.736+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "3496fe83b01c4d7488d7acc2b9a9ee14",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:51.736+00:00",
  "event": "result",
  "elapsed_s": 0.547,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:36:55.740+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "4a7b35bbc5eb4137ba722925a3edccb3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:55.740+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:36:56.328+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "4a7b35bbc5eb4137ba722925a3edccb3",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:36:56.328+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:00.332+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "8a938740e76d4963b4ba3612370b248c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:00.332+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:00.932+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "8a938740e76d4963b4ba3612370b248c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:00.932+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:04.948+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "9c2d8a75baf64bf7ad35371c96ab119f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:04.948+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:05.540+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "9c2d8a75baf64bf7ad35371c96ab119f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:05.540+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:09.575+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "4bdf3216a16043b9b83983a711a4afbc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:09.575+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:10.181+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "4bdf3216a16043b9b83983a711a4afbc",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:10.181+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:14.203+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "6835673134764fb0b560f5b5a3e94966",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:14.203+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:14.791+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "6835673134764fb0b560f5b5a3e94966",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:14.791+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:18.817+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "a1d45850f75d46c18ff7245ecc838c99",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:18.817+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:19.458+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "a1d45850f75d46c18ff7245ecc838c99",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:19.458+00:00",
  "event": "result",
  "elapsed_s": 0.609,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:23.476+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "30fd60f72cd4496da67fb4712c8e9109",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:23.476+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:24.208+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "30fd60f72cd4496da67fb4712c8e9109",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:24.208+00:00",
  "event": "result",
  "elapsed_s": 0.718,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:28.228+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — request

```json
{
  "request_id": "9cadd2fd127d4ca3ab07b18ffce87c52",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:28.228+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/5Zk83SZiIOeEAfWGISps",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:28.986+00:00 — elevenlabs / GET /flows/image/5Zk83SZiIOeEAfWGISps — result

```json
{
  "request_id": "9cadd2fd127d4ca3ab07b18ffce87c52",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/5Zk83SZiIOeEAfWGISps",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "86e3360e9fcf2c303bb3277be43ea7a19230a543ae8b1b5745d90e03fb30a70a",
  "time": "2026-10-18T01:37:28.986+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": {
    "id": "5Zk83SZiIOeEAfWGISps",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/Yv0DOhuy7gmtwWXOuBTq/5Zk83SZiIOeEAfWGISps/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013728Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:37:29.009+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "cfe604fb682f4703bf760b13346eabb7",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "5c28947d43140116851db2d3b18ff2782f1d96638edf479f4771f7afd5844ea3",
  "time": "2026-10-18T01:37:29.009+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/Yv0DOhuy7gmtwWXOuBTq/5Zk83SZiIOeEAfWGISps/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013728Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:37:31.070+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "cfe604fb682f4703bf760b13346eabb7",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg12_边路地精商店\\bg12_边路地精商店.part.png",
  "pid": 37900,
  "request_fingerprint": "5c28947d43140116851db2d3b18ff2782f1d96638edf479f4771f7afd5844ea3",
  "time": "2026-10-18T01:37:31.070+00:00",
  "event": "result",
  "elapsed_s": 2.047,
  "response": [
    200,
    {
      "bytes": 5746576,
      "sha256": "e96db1b7222a8c320f196849a86086cd4e490f15004d320cd07c247e9cc1323b"
    }
  ]
}
```

## 2026-10-18T01:37:31.111+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "6412d38fd8364cb4a008c2a51ac1c29d",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.png",
  "pid": 37900,
  "request_fingerprint": "9a2de16ef1cfae61161c0ec1703b7d9714926a460319d0048dfd8e733bcc622d",
  "time": "2026-10-18T01:37:31.111+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg13_近卫泉水与商店\n参考用法: 参考图只借世界的色板、阔叶林与石材的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n森林边缘一片和缓的草坡上，一座古老的泉池和几处店铺。画面中央是一座直径约六米的圆形泉池，池壁是浅灰白色的粗凿石块砌成，齐膝高，石缝里长着青苔和细小的蕨；池中央立着一根刻着藤蔓纹的石柱，托起上下两层浅浅的圆石盘，清水从石盘边缘不断地溢落下来，落进下层石盘再落进池里，溅起细碎的水花和一层薄雾；池水清澈见底，水里透出一层淡淡的青白色微光，像池底长着会发光的苔。泉池前方的草地上，五块直径约两米的圆形石板嵌进地面，排成一道浅浅的弧线，每块石板上刻着一圈细密的环形铭纹，刻槽里积着一线极淡的蓝色微光，白天几乎只看得出刻痕。泉池左后方是一株中空的活古树，树干粗大、树皮皲裂，树干下部张开一个能走进人的大树洞，洞里用树枝搭着木架，挂着成串的小玻璃瓶、草绳捆着的布包和几卷羊皮；右后方是一座缩小比例的白石法师小塔，约九米高，圆形塔身，尖顶覆着深紫灰色的石板瓦，墙上几扇拱窗透出暖光。最后方是高大的阔叶林墙，林间远处一道细瀑布从苔石上垂下。\n[细节]\n- 视角: 视点在泉池前方的草坡下缘，高度约一人，平视略仰，28mm 焦距感，五块石板、泉池、古树店与小塔都完整入画\n- 光线: 清晨；太阳刚升过右后方的林梢，从后方逆光斜照，泉水溢落的水雾被打成一片亮白，石盘边缘与草尖勾出暖色亮边；前景草地在逆光里偏冷绿；泉水的青白微光、石板刻纹的淡蓝微光与小塔拱窗的暖光都只是点缀；草叶上挂着露水\n- 构图: 16:9 横幅；泉池在画面中央；五块石板的弧线在前景下三分之一、空着留给人物站位；古树店在左后三分之一；白石小塔在右后三分之一；林墙与远处瀑布横贯画面上缘\n- 道具: 泉池边一只木水桶和一只长柄木瓢；古树洞口两只叠起的木箱；小塔门前三级石阶；画面里没有任何文字、招牌、旗帜、标记\n- 主色: 主 森林绿与苔绿 / 辅 浅灰白石 / 点缀 青白泉光、淡蓝刻纹、深紫灰瓦 / 高光 逆光水雾；自然色彩，不过饱和\n- 真实感: 这是在新西兰一处真实苔藓蕨林林缘实地拍摄、搭建实景泉池与小塔的奇幻电影外景剧照，不是渲染图：石块有风化缺角和水垢；池壁湿处颜色发深、长着滑腻的绿藻；草坡有踩出的小路和裸土；古树洞口的木架粗糙、绑着草绳\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，招牌字，水印，logo，任何人物，任何动物，霓虹发光圆环，魔法阵光效，喷泉灯光秀，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:37.803+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "6412d38fd8364cb4a008c2a51ac1c29d",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.png",
  "pid": 37900,
  "request_fingerprint": "9a2de16ef1cfae61161c0ec1703b7d9714926a460319d0048dfd8e733bcc622d",
  "time": "2026-10-18T01:37:37.803+00:00",
  "event": "result",
  "elapsed_s": 6.672,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "pending"
  }
}
```

## 2026-10-18T01:37:37.836+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "cdb5e30fc28644f88f0f509423498585",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:37.836+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:38.424+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "cdb5e30fc28644f88f0f509423498585",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:38.424+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "pending"
  }
}
```

## 2026-10-18T01:37:42.464+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "d154c072a88447238183b58c3a28776f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:42.464+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:43.122+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "d154c072a88447238183b58c3a28776f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:43.122+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:47.149+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "6ef4ef1d44aa4bcf9ee81586d9cbafe7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:47.149+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:47.788+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "6ef4ef1d44aa4bcf9ee81586d9cbafe7",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:47.788+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:51.814+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "0e215b98cadb4efab42fd2f3ce9543af",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:51.814+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:52.512+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "0e215b98cadb4efab42fd2f3ce9543af",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:52.512+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:37:56.547+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "b8abfa17cd80428b9f2459a47e38876d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:56.547+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:37:57.165+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "b8abfa17cd80428b9f2459a47e38876d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:37:57.165+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:01.191+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "2879704ad54245bab583921efd53cce4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:01.191+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:01.792+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "2879704ad54245bab583921efd53cce4",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:01.792+00:00",
  "event": "result",
  "elapsed_s": 0.593,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:05.808+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "ee125c1b04f6461ea2c74d7bbc20732a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:05.808+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:06.377+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "ee125c1b04f6461ea2c74d7bbc20732a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:06.377+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:10.398+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "2d4aed6cc8f84999a82a659ed0d05dd6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:10.398+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:11.028+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "2d4aed6cc8f84999a82a659ed0d05dd6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:11.028+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:15.052+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "5014d7d31cbf4f03bd2467d4ae63211d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:15.052+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:15.629+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "5014d7d31cbf4f03bd2467d4ae63211d",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:15.629+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:19.652+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — request

```json
{
  "request_id": "1fe54366e9aa4ed3916760036a2752be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:19.652+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/1TSWcbsUpGaMoRwBJjjO",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:20.674+00:00 — elevenlabs / GET /flows/image/1TSWcbsUpGaMoRwBJjjO — result

```json
{
  "request_id": "1fe54366e9aa4ed3916760036a2752be",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/1TSWcbsUpGaMoRwBJjjO",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "545e9cb29ee48e59a887f3850ad50b97798b0ac8427e6fcd7aa4bd6c73c07b3f",
  "time": "2026-10-18T01:38:20.674+00:00",
  "event": "result",
  "elapsed_s": 1.0,
  "response": {
    "id": "1TSWcbsUpGaMoRwBJjjO",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/2YuS9qXB7paBygTeIvRs/1TSWcbsUpGaMoRwBJjjO/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013819Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:38:20.693+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "5f6f42e28ec14062b79e43d7984d1ea5",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8b281d7b5c2737cec1f6b0144bf898bdbc0169ff12e7abb2a4b1eabed12bec3a",
  "time": "2026-10-18T01:38:20.693+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/2YuS9qXB7paBygTeIvRs/1TSWcbsUpGaMoRwBJjjO/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013819Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:38:24.429+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "5f6f42e28ec14062b79e43d7984d1ea5",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\sentinel\\bg13_近卫泉水与商店\\bg13_近卫泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "8b281d7b5c2737cec1f6b0144bf898bdbc0169ff12e7abb2a4b1eabed12bec3a",
  "time": "2026-10-18T01:38:24.429+00:00",
  "event": "result",
  "elapsed_s": 3.719,
  "response": [
    200,
    {
      "bytes": 5734531,
      "sha256": "775ccc7189ea0a7c2b161e2603f76a192573662b1cef21d536bf2e497be8894f"
    }
  ]
}
```

## 2026-10-18T01:38:24.484+00:00 — elevenlabs / POST /flows/image — request

```json
{
  "request_id": "6b088847f70f4f49bb6dd04a63d42c13",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.png",
  "pid": 37900,
  "request_fingerprint": "116eb2c2fc9b9054e5eacd54dfa26fa1582cc10f4504682566d999a06c7cf7cd",
  "time": "2026-10-18T01:38:24.484+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/flows/image",
    "body": {
      "model_id": "gpt-image-2.5-sunburst",
      "prompt": "bg14_天灾泉水与商店\n参考用法: 参考图只借世界的色板、紫黑荒地与针叶松的质感、光的胶片感；主体、机位与构图全部按下文重建，不照搬参考图的河道与构图。\n【场景锚点底图 · 纯空间背景无人物】\n[主体]\n寒冷荒原的一角，一座被污染的古老泉池和几处阴森的建筑。画面中央是一座直径约六米的圆形泉池，池壁齐膝高，石块原本是灰白色，如今发黑、开裂，表面长满紫黑色的霉斑和地衣，有几块已经崩落在池边；池中央一根刻着藤蔓纹的石柱托着上下两层浅石盘，上层石盘缺了一角，水流细弱、断断续续地从盘沿滴落；池水浑浊发暗，透出一层暗绿偏紫的病态微光，水面漂着一层碎薄冰和灰白的浮沫，池边结着冰凌。泉池前方的冻土上，五块直径约两米的圆形石板嵌进地面，排成一道浅弧，石板上刻着一圈细密的环形铭纹，刻槽里积着一线冷绿色的微光，石板边缘被霜和地衣侵蚀得模糊。泉池左后方是一座半埋进地里的墓穴，黑石砌成的墙只露出一人多高，拱顶由一根根骨白色、弯如肋骨的石梁撑起，梁与梁之间填着黑石，入口是一个幽暗的低矮拱门，两侧挂着两盏生锈的铁灯笼，灯笼没有点亮。右后方是一座约十二米高的瘦高黑石塔，塔身方中带圆，顶上一圈向外刺出的尖刺铁冠，几扇窄窗里透出冷紫色的光。地面是暗褐色的冻泥，大片紫黑色地衣夹着冰碴与薄雪；最后方是一道挂着白霜的黑云杉林墙。\n[细节]\n- 视角: 视点在泉池前方的冻土下缘，高度约一人，平视略仰，28mm 焦距感，五块石板、泉池、墓穴与黑石塔都完整入画\n- 光线: 阴天下午；厚云压得很低，冷灰色的漫射天光均匀落下，阴影浅而发蓝；冷雾贴着地面漂，墓穴入口和林墙脚下最浓；泉水的暗绿紫微光、石板刻纹的冷绿微光、塔窗的冷紫光都只是点缀，只染亮近旁一小圈；霜与薄冰是画面里最亮的地方\n- 构图: 16:9 横幅；泉池在画面中央；五块石板的弧线在前景下三分之一、空着留给人物站位；墓穴在左后三分之一；黑石塔在右后三分之一；黑云杉林墙横贯画面上缘\n- 道具: 泉池边一只破了底的木水桶；墓穴门前几级结霜的石阶；塔脚下一堆崩落的黑石；画面里没有任何文字、招牌、旗帜、标记\n- 主色: 主 紫黑与黑石 / 辅 骨白与暗褐 / 点缀 暗绿紫泉光、冷绿刻纹、冷紫塔窗 / 高光 霜与薄冰；自然色彩，不过饱和\n- 真实感: 这是在冰岛一处真实黑色火山砂荒原边缘实地拍摄、搭建实景泉池与建筑的奇幻电影外景剧照，不是渲染图：石块有裂缝、霉斑和冻融剥落；骨白石梁发黄、有裂纹和污渍；铁件锈蚀流下红褐锈痕；冻泥有冻胀纹和旧脚印\n[风格]\n真实电影剧照，全画幅数字电影机实拍，自然曝光，高光不溢、暗部有细节；低饱和、柔和反差，接近胶片负片色调，细微胶片颗粒；深景深，大气透视，画面不出现任何文字\n负面词: 画面文字，招牌字，水印，logo，任何人物，任何动物，骷髅堆，血池，霓虹发光圆环，魔法阵光效，游戏截图，游戏引擎渲染感，CG 渲染，卡通渲染，低模棱角，微缩模型感，过度饱和，荧光色，现代建筑，现代器物，UI 界面\n参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，不照搬参考图的构图与其中的建筑物件。",
      "aspect_ratio": "16:9",
      "resolution": "2K",
      "quality": "high",
      "images": [
        {
          "type": "inline_base64",
          "mime_type": "image/jpeg",
          "content_base64": {
            "bytes": 597226,
            "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
          }
        }
      ]
    },
    "files": [
      {
        "path": "C:\\Users\\light\\AppData\\Local\\Temp\\dm_refs\\8da37e5b3ebb.jpg",
        "exists": true,
        "bytes": 597226,
        "sha256": "e7aaf587a158256fcd76cf1b4cb791f6b1dd3eaf764931997ebe8526a54734de"
      }
    ],
    "timeout_s": 600,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:38.452+00:00 — elevenlabs / POST /flows/image — result

```json
{
  "request_id": "6b088847f70f4f49bb6dd04a63d42c13",
  "provider": "elevenlabs",
  "operation": "POST /flows/image",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.png",
  "pid": 37900,
  "request_fingerprint": "116eb2c2fc9b9054e5eacd54dfa26fa1582cc10f4504682566d999a06c7cf7cd",
  "time": "2026-10-18T01:38:38.452+00:00",
  "event": "result",
  "elapsed_s": 13.938,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "pending"
  }
}
```

## 2026-10-18T01:38:38.455+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "932042d7cc324e0a964fc9066f8ffa1c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:38.455+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:39.221+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "932042d7cc324e0a964fc9066f8ffa1c",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:39.221+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:43.246+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "cfafb3c0bb0340c29e0a285a07326ddb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:43.246+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:43.867+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "cfafb3c0bb0340c29e0a285a07326ddb",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:43.867+00:00",
  "event": "result",
  "elapsed_s": 0.594,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:47.893+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "c89bf5cdc1e5403cb7dd318dcc703083",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:47.893+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:48.665+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "c89bf5cdc1e5403cb7dd318dcc703083",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:48.665+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:52.688+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "8583ac83ac0749a3a9c731fa69365bfe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:52.688+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:53.344+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "8583ac83ac0749a3a9c731fa69365bfe",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:53.344+00:00",
  "event": "result",
  "elapsed_s": 0.625,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:38:57.369+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "311cfafa98ec45858d6c0bdb36b4d18f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:57.369+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:38:57.944+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "311cfafa98ec45858d6c0bdb36b4d18f",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:38:57.944+00:00",
  "event": "result",
  "elapsed_s": 0.563,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:01.961+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "e81f0d391fa54b6ba4cd4b73e3da74f6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:01.961+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:02.563+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "e81f0d391fa54b6ba4cd4b73e3da74f6",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:02.563+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:06.577+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "4824bd5a16e54280a9d83c62b481903a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:06.577+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:07.226+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "4824bd5a16e54280a9d83c62b481903a",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:07.226+00:00",
  "event": "result",
  "elapsed_s": 0.641,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:11.263+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "c30ec65f0a7841a88d5bc807f24fd3fa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:11.263+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:11.915+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "c30ec65f0a7841a88d5bc807f24fd3fa",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:11.915+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:15.943+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "bfbf659de6ce45a5a10d14805b762237",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:15.943+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:16.566+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "bfbf659de6ce45a5a10d14805b762237",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:16.566+00:00",
  "event": "result",
  "elapsed_s": 0.61,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:20.596+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "58a15be367e9489ba8dba257b88d2d86",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:20.596+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:21.260+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "58a15be367e9489ba8dba257b88d2d86",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:21.260+00:00",
  "event": "result",
  "elapsed_s": 0.64,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "generating"
  }
}
```

## 2026-10-18T01:39:25.283+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — request

```json
{
  "request_id": "1dcc35f14bdb42efab42adcca8baa5f8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:25.283+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/flows/image/S1hEIhDAW7FTjxqvx29M",
    "body": null,
    "files": [],
    "timeout_s": 120,
    "attempt": 1
  }
}
```

## 2026-10-18T01:39:26.272+00:00 — elevenlabs / GET /flows/image/S1hEIhDAW7FTjxqvx29M — result

```json
{
  "request_id": "1dcc35f14bdb42efab42adcca8baa5f8",
  "provider": "elevenlabs",
  "operation": "GET /flows/image/S1hEIhDAW7FTjxqvx29M",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "3a9dd1d4b21db5fc4be1695bf228ec47c201e2bb24f2bb89757dd89eb290b39b",
  "time": "2026-10-18T01:39:26.272+00:00",
  "event": "result",
  "elapsed_s": 0.969,
  "response": {
    "id": "S1hEIhDAW7FTjxqvx29M",
    "status": "completed",
    "content_url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/wazvWGNvTsozXkINV1XF/S1hEIhDAW7FTjxqvx29M/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013923Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "content_mime_type": "image/png"
  }
}
```

## 2026-10-18T01:39:26.289+00:00 — elevenlabs / GET artifact — request

```json
{
  "request_id": "09a8a30174094fbbb9034c650703a3bb",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "ad1c85df263969d87f06ecc5bde433c950ddf566f984bd6efe05fd233d98d680",
  "time": "2026-10-18T01:39:26.289+00:00",
  "event": "request",
  "request": {
    "url": "https://storage.googleapis.com/xi-backend/database/workspace/53598e2b94d8473cb1eb1c6edb67ac4d/content_generation/wazvWGNvTsozXkINV1XF/S1hEIhDAW7FTjxqvx29M/content.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=%5BREDACTED%5D&X-Goog-Date=20261018T013923Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature=%5BREDACTED%5D",
    "output": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
    "timeout_s": 300
  }
}
```

## 2026-10-18T01:39:28.703+00:00 — elevenlabs / GET artifact — result

```json
{
  "request_id": "09a8a30174094fbbb9034c650703a3bb",
  "provider": "elevenlabs",
  "operation": "GET artifact",
  "target": "C:\\workspace\\micro-drama-platform\\ai_videos\\dota_yingxiong\\2_世界观人设\\background\\dota_map\\scourge\\bg14_天灾泉水与商店\\bg14_天灾泉水与商店.part.png",
  "pid": 37900,
  "request_fingerprint": "ad1c85df263969d87f06ecc5bde433c950ddf566f984bd6efe05fd233d98d680",
  "time": "2026-10-18T01:39:28.703+00:00",
  "event": "result",
  "elapsed_s": 2.391,
  "response": [
    200,
    {
      "bytes": 5649318,
      "sha256": "a8b257bc319609624056abc6a7b48edb952d0fcf51c33540067451f6155eec61"
    }
  ]
}
```
