# 外部服务请求日志

请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。

## 2026-11-14T05:00:31.421+00:00 — suno-browser / browser_attach — request

```json
{
  "request_id": "7d028b6ee7f44a91a5dd1695804b9973",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T05:00:31.421+00:00",
  "event": "request",
  "request": {
    "cdp": "127.0.0.1:9334",
    "window": "kept open by person"
  }
}
```

## 2026-11-14T05:00:32.087+00:00 — suno-browser / browser_attach — result

```json
{
  "request_id": "7d028b6ee7f44a91a5dd1695804b9973",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T05:00:32.087+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": "<Browser type=<BrowserType name=chromium executable_path=C:\\Users\\light\\AppData\\Local\\ms-playwright\\chromium-1248\\chrome-win64\\chrome.exe> version=156.0.8078.48>"
}
```

## 2026-11-14T05:00:32.199+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "36886f304ff6404abcbbeb2f5a49b24b",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:00:32.199+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:00:40.055+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "36886f304ff6404abcbbeb2f5a49b24b",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:00:40.055+00:00",
  "event": "result",
  "elapsed_s": 7.844,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:00:40.074+00:00 — suno-browser / prepare — request

```json
{
  "request_id": "93bf4b1ee99340eba415262c406fb39b",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "316f31e16f3cb6ebf8f3430152b8d23823d56b97b639c0dd103078433e0d312e",
  "time": "2026-11-14T05:00:40.074+00:00",
  "event": "request",
  "request": {
    "request": {
      "prompt": "Understated documentary news-explainer underscore, calm but quietly tense, minimal electronic pulse, soft muted piano motif, warm analog pad, light ticking percussion, subtle sub bass, steady mid tempo around 90 BPM, no vocals, no big drops, unobtrusive and sits well under a spoken voice, thoughtful and analytical mood",
      "format": "wav",
      "instrumental": true,
      "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
      "mode": "advanced",
      "title": "redian t01 bed",
      "options": {
        "exclude_styles": "vocals, heavy drums, distorted guitar, epic orchestral hits"
      },
      "references": []
    },
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:00:55.595+00:00 — suno-browser / control_missing — request

```json
{
  "request_id": "da75d13765f941729846675a039ecc7c",
  "provider": "suno-browser",
  "operation": "control_missing",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "2271fb0ccd5e771fd4ab2416c17fa8e876cd3821e423c6ea8cca73d0160a4eb5",
  "time": "2026-11-14T05:00:55.595+00:00",
  "event": "request",
  "request": {
    "control": "custom"
  }
}
```

## 2026-11-14T05:00:55.635+00:00 — suno-browser / control_missing — result

```json
{
  "request_id": "da75d13765f941729846675a039ecc7c",
  "provider": "suno-browser",
  "operation": "control_missing",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "2271fb0ccd5e771fd4ab2416c17fa8e876cd3821e423c6ea8cca73d0160a4eb5",
  "time": "2026-11-14T05:00:55.635+00:00",
  "event": "result",
  "elapsed_s": 0.0,
  "response": {
    "candidates_total_visible": [
      [
        0,
        0
      ],
      [
        0,
        0
      ]
    ],
    "url": "https://suno.com/create",
    "modals": []
  }
}
```

## 2026-11-14T05:00:56.111+00:00 — suno-browser / prepare — error

```json
{
  "request_id": "93bf4b1ee99340eba415262c406fb39b",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "316f31e16f3cb6ebf8f3430152b8d23823d56b97b639c0dd103078433e0d312e",
  "time": "2026-11-14T05:00:56.111+00:00",
  "event": "error",
  "elapsed_s": 16.032,
  "error_type": "ServiceError",
  "error": "找不到唯一的 custom 控件；需登录后校准 selectors.json"
}
```

## 2026-11-14T05:01:01.589+00:00 — suno-browser / browser_attach — request

```json
{
  "request_id": "81e83a0bab314525b07c8c41fcf1bd5a",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T05:01:01.589+00:00",
  "event": "request",
  "request": {
    "cdp": "127.0.0.1:9334",
    "window": "kept open by person"
  }
}
```

## 2026-11-14T05:01:02.373+00:00 — suno-browser / browser_attach — result

```json
{
  "request_id": "81e83a0bab314525b07c8c41fcf1bd5a",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T05:01:02.373+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": "<Browser type=<BrowserType name=chromium executable_path=C:\\Users\\light\\AppData\\Local\\ms-playwright\\chromium-1248\\chrome-win64\\chrome.exe> version=156.0.8078.48>"
}
```

## 2026-11-14T05:01:02.509+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "b1f32aa7fa834d328a3da1c553b9bd24",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:01:02.509+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:01:13.689+00:00 — dreamina / user_credit — request

```json
{
  "request_id": "e9fd4d77bf3f4ce69c460d650bfa6490",
  "provider": "dreamina",
  "operation": "user_credit",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 39332,
  "request_fingerprint": "bd7b3f99465a69f987e7ad1cd756e7061dd2b84a49286562b9e0733ed60e98c9",
  "time": "2026-11-14T05:01:13.689+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "user_credit"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:01:31.074+00:00 — dreamina / user_credit — result

```json
{
  "request_id": "e9fd4d77bf3f4ce69c460d650bfa6490",
  "provider": "dreamina",
  "operation": "user_credit",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 39332,
  "request_fingerprint": "bd7b3f99465a69f987e7ad1cd756e7061dd2b84a49286562b9e0733ed60e98c9",
  "time": "2026-11-14T05:01:31.074+00:00",
  "event": "result",
  "elapsed_s": 17.36,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"total_credit\": 100972,\n  \"user_id\": 3054920168911786,\n  \"user_name\": \"\",\n  \"vip_level\": \"ultra\"\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:01:42.925+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "b1f32aa7fa834d328a3da1c553b9bd24",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:01:42.925+00:00",
  "event": "result",
  "elapsed_s": 40.391,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:01:42.972+00:00 — suno-browser / prepare — request

```json
{
  "request_id": "cef5bfe2cb454df59d567cd657210b75",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "316f31e16f3cb6ebf8f3430152b8d23823d56b97b639c0dd103078433e0d312e",
  "time": "2026-11-14T05:01:42.972+00:00",
  "event": "request",
  "request": {
    "request": {
      "prompt": "Understated documentary news-explainer underscore, calm but quietly tense, minimal electronic pulse, soft muted piano motif, warm analog pad, light ticking percussion, subtle sub bass, steady mid tempo around 90 BPM, no vocals, no big drops, unobtrusive and sits well under a spoken voice, thoughtful and analytical mood",
      "format": "wav",
      "instrumental": true,
      "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
      "mode": "advanced",
      "title": "redian t01 bed",
      "options": {
        "exclude_styles": "vocals, heavy drums, distorted guitar, epic orchestral hits"
      },
      "references": []
    },
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:01:55.406+00:00 — suno-browser / prepare — result

```json
{
  "request_id": "cef5bfe2cb454df59d567cd657210b75",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "316f31e16f3cb6ebf8f3430152b8d23823d56b97b639c0dd103078433e0d312e",
  "time": "2026-11-14T05:01:55.406+00:00",
  "event": "result",
  "elapsed_s": 12.421,
  "response": [
    "https://suno.com/song/09516232-f7ee-41b9-836b-5f7dfe1ecf9b",
    "https://suno.com/song/0aabb622-08a2-4038-afd7-287302a1c976",
    "https://suno.com/song/0d5852e5-e5fb-4e52-bfd8-d37192fa3ceb",
    "https://suno.com/song/10ae81b2-3b87-4de7-8f2e-68f6d42fa7e5",
    "https://suno.com/song/173175d4-0fcb-4122-8353-37cd27813504",
    "https://suno.com/song/4b4d868b-ddf4-4352-a908-c7487d743711",
    "https://suno.com/song/58490eaf-9e2b-469e-b5d9-6e35285227ff",
    "https://suno.com/song/6904ff75-7d62-43b1-8fb1-24dce0a4c1b6",
    "https://suno.com/song/6a689bf4-07ae-4dec-992c-245c17819e68",
    "https://suno.com/song/813a380a-3126-4cf2-b165-03f6cb91fdf7",
    "https://suno.com/song/8cc80af1-3c13-47b4-a2f0-0bcc51124e14",
    "https://suno.com/song/a6e8621a-56f7-4d64-82a1-ee0a4796cb95",
    "https://suno.com/song/bf844d85-b6dd-4a34-8c87-5df3ad785609",
    "https://suno.com/song/dbc0e029-77a0-40f8-8f7f-26706f2071d4"
  ]
}
```

## 2026-11-14T05:01:55.459+00:00 — suno-browser / create — request

```json
{
  "request_id": "e8708276a1cd481a9afb979b2359cc6f",
  "provider": "suno-browser",
  "operation": "create",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d628b0b2c8f9f2eae7c74853abbff39d96857154aa0a751e064f4adbd40ece64",
  "time": "2026-11-14T05:01:55.459+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790",
    "attempt": 1
  }
}
```

## 2026-11-14T05:01:58.222+00:00 — suno-browser / create — result

```json
{
  "request_id": "e8708276a1cd481a9afb979b2359cc6f",
  "provider": "suno-browser",
  "operation": "create",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d628b0b2c8f9f2eae7c74853abbff39d96857154aa0a751e064f4adbd40ece64",
  "time": "2026-11-14T05:01:58.222+00:00",
  "event": "result",
  "elapsed_s": 2.75,
  "response": {
    "clicked": true,
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790",
    "cost": "unknown",
    "diagnostic": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\after-submit.json"
  }
}
```

## 2026-11-14T05:01:58.269+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "3bede51e0ad8459990db4e4a48631ddf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:01:58.269+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:01:58.349+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "3bede51e0ad8459990db4e4a48631ddf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:01:58.349+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:03.385+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "a0544e5d08a94039a4f31e0910570dfe",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:03.385+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:03.484+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "a0544e5d08a94039a4f31e0910570dfe",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:03.484+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:08.537+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "1b8979ae1e004fe3a8fe150117dae57a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:08.537+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:08.620+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "1b8979ae1e004fe3a8fe150117dae57a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:08.620+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:13.656+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "edd53b8725bc48659ffb9efae7072b47",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:13.656+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:13.734+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "edd53b8725bc48659ffb9efae7072b47",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:13.734+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:02:18.762+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "87227c6172af4427b725df44c8b8b850",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:18.762+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:18.833+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "87227c6172af4427b725df44c8b8b850",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:18.833+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:23.856+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "16bc38f31a7142f7a8b9ee8712afe302",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:23.856+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:23.936+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "16bc38f31a7142f7a8b9ee8712afe302",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:23.936+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:28.965+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d045612bf3334e2db3b3e5809b53710a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:28.965+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:29.030+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d045612bf3334e2db3b3e5809b53710a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:29.030+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:02:34.065+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b2b22c4baf074fed95a3381b40096394",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:34.065+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:34.156+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b2b22c4baf074fed95a3381b40096394",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:34.156+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:02:39.201+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "135879a3a2004b5da2244d6eaa8094d3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:39.201+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:39.289+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "135879a3a2004b5da2244d6eaa8094d3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:39.289+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:02:44.329+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4a224d837dfc4b8a997e1262a4fc4b70",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:44.329+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:44.434+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4a224d837dfc4b8a997e1262a4fc4b70",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:44.434+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:02:49.479+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "acbde31ea18e40e1bbedd9c281ce28e0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:49.479+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:49.559+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "acbde31ea18e40e1bbedd9c281ce28e0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:49.559+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:02:54.600+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4635aa25b39049c8b1252ba92056b9e2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:54.600+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:54.679+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4635aa25b39049c8b1252ba92056b9e2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:54.679+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:02:59.704+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c7a38e5216ae4e05b9c681bfa0591714",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:59.704+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:02:59.774+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c7a38e5216ae4e05b9c681bfa0591714",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:02:59.774+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:03:04.800+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d860bd60b0fa4f87ba7b3ca890f36e11",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:04.800+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:04.881+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d860bd60b0fa4f87ba7b3ca890f36e11",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:04.881+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:09.902+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "9dacf729e03f42ff9f849614c7db333d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:09.902+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:09.976+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "9dacf729e03f42ff9f849614c7db333d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:09.976+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:03:14.999+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "446bba2d97904beeba83fa17826c503c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:14.999+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:15.077+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "446bba2d97904beeba83fa17826c503c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:15.077+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:20.097+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2a427710b5534f6191051d04414e90ac",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:20.097+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:20.175+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2a427710b5534f6191051d04414e90ac",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:20.175+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:25.187+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7e98dd8f00d749d29a4bca9d911f86dd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:25.187+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:25.242+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7e98dd8f00d749d29a4bca9d911f86dd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:25.242+00:00",
  "event": "result",
  "elapsed_s": 0.032,
  "response": []
}
```

## 2026-11-14T05:03:27.277+00:00 — dreamina / text2video — request

```json
{
  "request_id": "a55487dc54fc43c4847a91b118ce0262",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 41280,
  "request_fingerprint": "c4385d24ccb56413d490dea1d1d08f64d56fc38c16c587d5af42a171f0220f68",
  "time": "2026-11-14T05:03:27.277+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Late afternoon at a large American hub airport, wide aerial drone shot slowly pushing in. Dozens of commercial airliners sit motionless at the gates and in a long queue on the taxiway, engines idling, ground crew standing beside baggage carts, waiting. Nothing takes off. Overcast sky, muted colors, realistic documentary news footage. No text, no captions, no logos, plain white aircraft with no airline livery.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:03:30.269+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "fc08db68a6ad455496130037bd859b60",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:30.269+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:30.346+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "fc08db68a6ad455496130037bd859b60",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:30.346+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:35.361+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "5ab87b18ab2f4beabdefd30f3b1ab043",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:35.361+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:35.441+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "5ab87b18ab2f4beabdefd30f3b1ab043",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:35.441+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:40.470+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b3604de3a2c14a0ca105af481c5521f4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:40.470+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:40.568+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b3604de3a2c14a0ca105af481c5521f4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:40.568+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:03:42.289+00:00 — dreamina / text2video — result

```json
{
  "request_id": "a55487dc54fc43c4847a91b118ce0262",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 41280,
  "request_fingerprint": "c4385d24ccb56413d490dea1d1d08f64d56fc38c16c587d5af42a171f0220f68",
  "time": "2026-11-14T05:03:42.289+00:00",
  "event": "result",
  "elapsed_s": 14.984,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"65e97f85-5e7b-4b0a-ac07-3fba7da1c0a2\",\n  \"logid\": \"2026111413032719801925525351823B2\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 475\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:03:42.561+00:00 — dreamina / text2video — request

```json
{
  "request_id": "6858f080a90f4d909ba696a9633e1fba",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 82164,
  "request_fingerprint": "44cf6736369eb23bfc268118da58de0c09cfd9a6e9442a0e9e10b7e6c584fe32",
  "time": "2026-11-14T05:03:42.561+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Inside a dim air route traffic control center: rows of controllers in headsets sit at large dark radar consoles glowing green and amber. One after another the radar screens flicker and freeze. A controller presses his headset, turns to the colleague beside him, then picks up a desk phone. Handheld camera, low light, tense, realistic documentary look. No readable text on screens, no logos, no recognizable real people.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:03:45.620+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "9b3a0819782d456f9a96e43de9ad04cb",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:45.620+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:45.730+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "9b3a0819782d456f9a96e43de9ad04cb",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:45.730+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:03:50.770+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "6af719ea0cb24e60a04fa8d39a92b1ba",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:50.770+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:50.842+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "6af719ea0cb24e60a04fa8d39a92b1ba",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:50.842+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:03:55.877+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "24bd91fb00104942bfc15c73e357a277",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:55.877+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:03:55.974+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "24bd91fb00104942bfc15c73e357a277",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:03:55.974+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T05:03:58.271+00:00 — dreamina / text2video — result

```json
{
  "request_id": "6858f080a90f4d909ba696a9633e1fba",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 82164,
  "request_fingerprint": "44cf6736369eb23bfc268118da58de0c09cfd9a6e9442a0e9e10b7e6c584fe32",
  "time": "2026-11-14T05:03:58.271+00:00",
  "event": "result",
  "elapsed_s": 15.672,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"64acbd20-b4eb-4c3c-b303-76c8c5b70e34\",\n  \"logid\": \"20261114130342198019255253949FE10\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 453\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:03:58.536+00:00 — dreamina / text2video — request

```json
{
  "request_id": "647a988cb4f74347a369511b04fd391e",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 55204,
  "request_fingerprint": "a0d18cdd8457bd9fd9a58dd451d7d760f86f26a1c0736d583068644964f5b710",
  "time": "2026-11-14T05:03:58.536+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=A telecommunications equipment room. On the left, an old rack full of tangled copper cables and blinking legacy switches; on the right, a new clean rack with yellow fiber optic cables. A technician's hands carefully unplug one cable from the old rack and plug it into the new rack while status lights keep blinking on both. Close-ups of connectors and LEDs, shallow depth of field, careful and tense mood, realistic. No text, no logos.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:04:01.005+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "831729b2df8e4b92b36aa213d7edde64",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:01.005+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:01.081+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "831729b2df8e4b92b36aa213d7edde64",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:01.081+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:06.129+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b4ddfe2cc25a430faa2deb59b1b8340b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:06.129+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:06.208+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b4ddfe2cc25a430faa2deb59b1b8340b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:06.208+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:11.243+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "de44c02531604c34900a684483f43bd3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:11.243+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:11.332+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "de44c02531604c34900a684483f43bd3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:11.332+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:13.204+00:00 — dreamina / text2video — result

```json
{
  "request_id": "647a988cb4f74347a369511b04fd391e",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 55204,
  "request_fingerprint": "a0d18cdd8457bd9fd9a58dd451d7d760f86f26a1c0736d583068644964f5b710",
  "time": "2026-11-14T05:04:13.204+00:00",
  "event": "result",
  "elapsed_s": 14.64,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"56f71d96-beb4-4675-9a88-07108e567b58\",\n  \"logid\": \"20261114130358198019255253926759F\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 420\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:04:13.437+00:00 — dreamina / text2video — request

```json
{
  "request_id": "11fdc825b93c417f85b3874c1b323dbb",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 86768,
  "request_fingerprint": "3decd05c85081a3a98e5b0585f575a95b990537d70167a84cfd161d9bac2e01f",
  "time": "2026-11-14T05:04:13.437+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Daytime construction site beside a road. An excavator bucket digs into a narrow trench; inside the trench two black cable conduits run side by side. The bucket bites down and tears through both conduits at once, the severed ends hanging in the dirt. Mid shot then close-up, overcast light, realistic. No text, no logos.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:04:16.383+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "e91196b42e564da689e3b63327351ce1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:16.383+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:16.486+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "e91196b42e564da689e3b63327351ce1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:16.486+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:04:21.508+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "8bf6395ccc5243ae8bfa1235b0b8723d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:21.508+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:21.602+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "8bf6395ccc5243ae8bfa1235b0b8723d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:21.602+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:26.657+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7d0b600c638c448699060a577f2469f8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:26.657+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:26.740+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7d0b600c638c448699060a577f2469f8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:26.740+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:29.013+00:00 — dreamina / text2video — result

```json
{
  "request_id": "11fdc825b93c417f85b3874c1b323dbb",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 86768,
  "request_fingerprint": "3decd05c85081a3a98e5b0585f575a95b990537d70167a84cfd161d9bac2e01f",
  "time": "2026-11-14T05:04:29.013+00:00",
  "event": "result",
  "elapsed_s": 15.563,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"4e40883e-1a5f-471a-b9ae-1ed28b52af9f\",\n  \"logid\": \"20261114130413198019255253669D550\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 419\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:04:29.329+00:00 — dreamina / text2video — request

```json
{
  "request_id": "d662df5f837f4499a0f7d512fc893a07",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 33992,
  "request_fingerprint": "86d64c94550f134029eb84ac405f39d12cb4ef00251f5ef16a1925ec236fdb47",
  "time": "2026-11-14T05:04:29.329+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Night at a large airport, long telephoto lens. A long line of airliner landing lights stretches across the dark sky; planes touch down one after another on a brightly lit runway, calm and orderly. Realistic, cinematic, quiet mood. No text, no logos, no airline livery.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=8",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:04:31.762+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "20825307a8e74035837a1b11d0ac4f2b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:31.762+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:31.860+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "20825307a8e74035837a1b11d0ac4f2b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:31.860+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:04:36.899+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c16efb0032dd4021b1a8eb5f520bf45e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:36.899+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:36.981+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c16efb0032dd4021b1a8eb5f520bf45e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:36.981+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:42.025+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ce345e13a49342fcb9c4a671214d3e4c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:42.025+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:42.090+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ce345e13a49342fcb9c4a671214d3e4c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:42.090+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:04:45.697+00:00 — dreamina / text2video — result

```json
{
  "request_id": "d662df5f837f4499a0f7d512fc893a07",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 33992,
  "request_fingerprint": "86d64c94550f134029eb84ac405f39d12cb4ef00251f5ef16a1925ec236fdb47",
  "time": "2026-11-14T05:04:45.697+00:00",
  "event": "result",
  "elapsed_s": 16.328,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"dc33ced3-c9bb-4dca-a755-aaba12968ec9\",\n  \"logid\": \"20261114130429198019255253608597F\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 160,\n  \"estimated_remaining_seconds\": 471\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T05:04:47.117+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2f845c7002e34c48b57db82cb29b06b7",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:47.117+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:47.212+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2f845c7002e34c48b57db82cb29b06b7",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:47.212+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:52.254+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "24afdce4533647ffb2752a2fc4c3a544",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:52.254+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:52.348+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "24afdce4533647ffb2752a2fc4c3a544",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:52.348+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:04:57.394+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "569b259925234ff5af97ecf2c5823e19",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:57.394+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:04:57.492+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "569b259925234ff5af97ecf2c5823e19",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:04:57.492+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:02.529+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2c9a502281ee4502b2a896b412226f56",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:02.529+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:02.614+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2c9a502281ee4502b2a896b412226f56",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:02.614+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:07.658+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "415cb0194a0a4208bf4f864a8c55be16",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:07.658+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:07.728+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "415cb0194a0a4208bf4f864a8c55be16",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:07.728+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:05:12.745+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "931c2bdb2c0d43b08c3c098bb447be84",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:12.745+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:12.848+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "931c2bdb2c0d43b08c3c098bb447be84",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:12.848+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:05:17.885+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "53154995d9564532979292a79847ae99",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:17.885+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:17.984+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "53154995d9564532979292a79847ae99",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:17.984+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:05:23.035+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "517bcf5d42014c7c96aa1ba10cc74c4b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:23.035+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:23.114+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "517bcf5d42014c7c96aa1ba10cc74c4b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:23.114+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:28.147+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "19f25454acd64c1d9d70e1ddd2c937da",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:28.147+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:28.249+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "19f25454acd64c1d9d70e1ddd2c937da",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:28.249+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:05:33.295+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "a1584a054dd5411f9638a5ae7ea43c94",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:33.295+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:33.381+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "a1584a054dd5411f9638a5ae7ea43c94",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:33.381+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:38.415+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "23ac8debc61744d885e28d150fca8380",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:38.415+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:38.526+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "23ac8debc61744d885e28d150fca8380",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:38.526+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:05:43.569+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d68932ff6033468183b031a995cdc41f",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:43.569+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:43.649+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d68932ff6033468183b031a995cdc41f",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:43.649+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:48.681+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ce0c6ce3074145ca9e24a6015eb23df1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:48.681+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:48.766+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ce0c6ce3074145ca9e24a6015eb23df1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:48.766+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:05:53.789+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "46bbc0be6e3f48f280c05f9cf1dc06f2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:53.789+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:05:53.901+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "46bbc0be6e3f48f280c05f9cf1dc06f2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:05:53.901+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:05:58.931+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "19e206e3e28c408f850dcd7ccd14f5c0",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:05:58.931+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:06:06.082+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "19e206e3e28c408f850dcd7ccd14f5c0",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:06:06.082+00:00",
  "event": "result",
  "elapsed_s": 7.125,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:06:06.109+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "3c3d2a3d1cf44b95a3681ecec44038f9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:06.109+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:06.168+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "3c3d2a3d1cf44b95a3681ecec44038f9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:06.168+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:06:11.195+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "89c61d758ebc4f9aa29da944e971ed4b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:11.195+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:11.371+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "89c61d758ebc4f9aa29da944e971ed4b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:11.371+00:00",
  "event": "result",
  "elapsed_s": 0.125,
  "response": []
}
```

## 2026-11-14T05:06:16.397+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "a26b094013324e6a9f19f75904dc5933",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:16.397+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:16.487+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "a26b094013324e6a9f19f75904dc5933",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:16.487+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:06:21.499+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "5522ec3715a34f78aaa75fc11e3d0464",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:21.499+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:21.572+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "5522ec3715a34f78aaa75fc11e3d0464",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:21.572+00:00",
  "event": "result",
  "elapsed_s": 0.016,
  "response": []
}
```

## 2026-11-14T05:06:26.590+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "34f4a43285844e6da01c7942f85a24c8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:26.590+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:26.661+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "34f4a43285844e6da01c7942f85a24c8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:26.661+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:06:31.678+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "579075c56e10422ea4e9b20e220fe716",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:31.678+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:31.765+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "579075c56e10422ea4e9b20e220fe716",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:31.765+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:06:36.786+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "3f4250c5a2bb4f3aa35938fbfeb401e1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:36.786+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:36.867+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "3f4250c5a2bb4f3aa35938fbfeb401e1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:36.867+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:06:41.899+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4882b86ce1354db99a55ef896b694ecf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:41.899+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:41.982+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4882b86ce1354db99a55ef896b694ecf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:41.982+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:06:46.994+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "fe1e997afeab4696b89831131d54fdab",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:46.994+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:06:47.059+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "fe1e997afeab4696b89831131d54fdab",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:06:47.059+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:06:52.073+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "1733c2c81d054fa690aa16e8565a286d",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:06:52.073+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:07:05.719+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "1733c2c81d054fa690aa16e8565a286d",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:07:05.719+00:00",
  "event": "result",
  "elapsed_s": 13.609,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:07:05.730+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7e9902bdb2484a29abcd9c09a72dce0f",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:05.730+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:05.787+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7e9902bdb2484a29abcd9c09a72dce0f",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:05.787+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:07:10.804+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "706bdb29e6b74707826ac8c564ede28e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:10.804+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:11.114+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "706bdb29e6b74707826ac8c564ede28e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:11.114+00:00",
  "event": "result",
  "elapsed_s": 0.282,
  "response": []
}
```

## 2026-11-14T05:07:16.147+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ea9b829a280943af87dc2dcbee37a85b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:16.147+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:16.245+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ea9b829a280943af87dc2dcbee37a85b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:16.245+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:21.280+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d041bc84b49745168d82f5b0e028f42e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:21.280+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:21.364+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d041bc84b49745168d82f5b0e028f42e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:21.364+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:26.387+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "36e4bb13dec546178d4624a6efc10c0e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:26.387+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:26.476+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "36e4bb13dec546178d4624a6efc10c0e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:26.476+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:31.510+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "3457f3d4e65546aebfce4d52f894864c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:31.510+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:31.601+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "3457f3d4e65546aebfce4d52f894864c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:31.601+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:36.640+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "e3209ccfaf3940028d3664c9c0ebee3b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:36.640+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:36.721+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "e3209ccfaf3940028d3664c9c0ebee3b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:36.721+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:41.743+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "f6509b2b95ce42e3a6fac653b7c724b4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:41.743+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:41.837+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "f6509b2b95ce42e3a6fac653b7c724b4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:41.837+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:07:46.860+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "cade6fa454a84637a1da861cd4968445",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:46.860+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:46.914+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "cade6fa454a84637a1da861cd4968445",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:46.914+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:07:51.927+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "c3cc505477e145b7a68039dd1cf3f63b",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:07:51.927+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:07:54.191+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "c3cc505477e145b7a68039dd1cf3f63b",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:07:54.191+00:00",
  "event": "result",
  "elapsed_s": 2.235,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:07:54.221+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "de35c265f8054225bcb39fc182446af8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:54.221+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:07:54.910+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "de35c265f8054225bcb39fc182446af8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:54.910+00:00",
  "event": "result",
  "elapsed_s": 0.671,
  "response": []
}
```

## 2026-11-14T05:07:59.945+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "f0fcf90ebf7b4e779847f345c1b87b93",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:07:59.945+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:00.097+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "f0fcf90ebf7b4e779847f345c1b87b93",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:00.097+00:00",
  "event": "result",
  "elapsed_s": 0.125,
  "response": []
}
```

## 2026-11-14T05:08:05.134+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "0219495d3d3447ef9bce2a04aaacffb8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:05.134+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:05.242+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "0219495d3d3447ef9bce2a04aaacffb8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:05.242+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:08:10.268+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "a7dc7a5b31154de18d09a2abb5f27a92",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:10.268+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:10.353+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "a7dc7a5b31154de18d09a2abb5f27a92",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:10.353+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:08:15.378+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "5f35843239d8445d9973d105e28e9df8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:15.378+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:15.461+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "5f35843239d8445d9973d105e28e9df8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:15.461+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:08:20.482+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "45f2bf66f3f549b4874f2614a0389cdf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:20.482+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:20.538+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "45f2bf66f3f549b4874f2614a0389cdf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:20.538+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:08:25.564+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d878cb53711f4ca88a123aa14f0603b4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:25.564+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:25.660+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d878cb53711f4ca88a123aa14f0603b4",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:25.660+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:08:30.693+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "1db702ac884d4934b1b9f055d7a312c9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:30.693+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:30.754+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "1db702ac884d4934b1b9f055d7a312c9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:30.754+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:08:35.781+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d2604e055c54421dbc8e09030d373b0b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:35.781+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:35.876+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d2604e055c54421dbc8e09030d373b0b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:35.876+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:08:40.895+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "2df5025e8d984cd99aea15ef51f06fab",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:08:40.895+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:08:42.337+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "2df5025e8d984cd99aea15ef51f06fab",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:08:42.337+00:00",
  "event": "result",
  "elapsed_s": 1.406,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:08:42.358+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "cd24e22245364bb7992750a3ba8544b9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:42.358+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:42.412+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "cd24e22245364bb7992750a3ba8544b9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:42.412+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:08:47.441+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4c6e875089534860a648851a094890f6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:47.441+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:47.588+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4c6e875089534860a648851a094890f6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:47.588+00:00",
  "event": "result",
  "elapsed_s": 0.109,
  "response": []
}
```

## 2026-11-14T05:08:52.604+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "f4f641dfd60a4f2a88f8c2308070fe26",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:52.604+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:53.030+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "f4f641dfd60a4f2a88f8c2308070fe26",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:53.030+00:00",
  "event": "result",
  "elapsed_s": 0.39,
  "response": []
}
```

## 2026-11-14T05:08:58.074+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ccc1f18cdb5b41f0a1abe3be54ede7bc",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:58.074+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:08:58.184+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ccc1f18cdb5b41f0a1abe3be54ede7bc",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:08:58.184+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T05:09:03.230+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c7f319bc4aaa41ce82bfc057f2603155",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:03.230+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:03.319+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c7f319bc4aaa41ce82bfc057f2603155",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:03.319+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:09:08.364+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "5d2c80eb4c5c46a184669caaf62d41e1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:08.364+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:08.442+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "5d2c80eb4c5c46a184669caaf62d41e1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:08.442+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:09:13.474+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7365212242274b4c9dc166f0a58b4dad",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:13.474+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:13.560+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7365212242274b4c9dc166f0a58b4dad",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:13.560+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:09:18.594+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ab67ff1a6c844d95a8dd8a7e2ac453d6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:18.594+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:18.667+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ab67ff1a6c844d95a8dd8a7e2ac453d6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:18.667+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:09:23.694+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "600f9484940e402e9255723c3d4800b9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:23.694+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:23.799+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "600f9484940e402e9255723c3d4800b9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:23.799+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:09:28.839+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "7cc16e4d28554d7db92859758e7a8e29",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:09:28.839+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:09:31.924+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "7cc16e4d28554d7db92859758e7a8e29",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:09:31.924+00:00",
  "event": "result",
  "elapsed_s": 3.047,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:09:31.944+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2dbcee9aef8a434a902cea2817b7055d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:31.944+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:32.731+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2dbcee9aef8a434a902cea2817b7055d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:32.731+00:00",
  "event": "result",
  "elapsed_s": 0.75,
  "response": []
}
```

## 2026-11-14T05:09:37.778+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4e970de3ad0349918eb2e0965da7353a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:37.778+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:38.019+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4e970de3ad0349918eb2e0965da7353a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:38.019+00:00",
  "event": "result",
  "elapsed_s": 0.203,
  "response": []
}
```

## 2026-11-14T05:09:43.041+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "da58f7652257409192d034826deb2a0c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:43.041+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:43.163+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "da58f7652257409192d034826deb2a0c",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:43.163+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T05:09:48.203+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7d208b9d4b66487da49ac3d797ab92d1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:48.203+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:48.290+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7d208b9d4b66487da49ac3d797ab92d1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:48.290+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:09:53.324+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c660cce124e14216b6d718e4f3122b3b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:53.324+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:53.408+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c660cce124e14216b6d718e4f3122b3b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:53.408+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:09:58.438+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "218049e48e6b4fa79ced7a3e903f999d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:58.438+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:09:58.528+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "218049e48e6b4fa79ced7a3e903f999d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:09:58.528+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:10:03.567+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ceaa88aff33a436a93c1004cd421cf17",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:03.567+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:03.616+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ceaa88aff33a436a93c1004cd421cf17",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:03.616+00:00",
  "event": "result",
  "elapsed_s": 0.032,
  "response": []
}
```

## 2026-11-14T05:10:08.633+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "9b8620c986ec42d4babfd0302518dca0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:08.633+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:08.712+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "9b8620c986ec42d4babfd0302518dca0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:08.712+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:10:13.748+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ca3828e9edb044ba9b220c46be45028b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:13.748+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:13.849+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ca3828e9edb044ba9b220c46be45028b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:13.849+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:10:18.870+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "78b84bd59813480a89c2fb5aed5e8bf2",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:10:18.870+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:10:20.050+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "78b84bd59813480a89c2fb5aed5e8bf2",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:10:20.050+00:00",
  "event": "result",
  "elapsed_s": 1.156,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:10:20.079+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d79b76011cdd46a997221cb1f91366a5",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:20.079+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:20.676+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d79b76011cdd46a997221cb1f91366a5",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:20.676+00:00",
  "event": "result",
  "elapsed_s": 0.578,
  "response": []
}
```

## 2026-11-14T05:10:25.714+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "90ab5e33014643af822f878b054cd5c1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:25.714+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:26.268+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "90ab5e33014643af822f878b054cd5c1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:26.268+00:00",
  "event": "result",
  "elapsed_s": 0.516,
  "response": []
}
```

## 2026-11-14T05:10:31.316+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2638f13c1e14486cab85734cd6fd40fd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:31.316+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:31.423+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2638f13c1e14486cab85734cd6fd40fd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:31.423+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T05:10:36.462+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "573b12845101466caef1ed11d13d2fdf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:36.462+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:36.564+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "573b12845101466caef1ed11d13d2fdf",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:36.564+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:10:41.619+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c4b3003a2f6a44aeb56b1ffe68aeff83",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:41.619+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:41.718+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c4b3003a2f6a44aeb56b1ffe68aeff83",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:41.718+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:10:46.766+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "6ffea154022644fd90279eacb67aad8a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:46.766+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:46.853+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "6ffea154022644fd90279eacb67aad8a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:46.853+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:10:51.873+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "22cded1dc7b64b788427766ce9d28fc3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:51.873+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:51.958+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "22cded1dc7b64b788427766ce9d28fc3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:51.958+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:10:56.989+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4f75361d9c734d378a272d758b3c1de0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:56.989+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:10:57.097+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4f75361d9c734d378a272d758b3c1de0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:10:57.097+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:11:02.134+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "23eadf8ac90940ccb364469af3b2957a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:02.134+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:02.207+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "23eadf8ac90940ccb364469af3b2957a",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:02.207+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:11:07.230+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "35d45bb9f642417baf09a6b5768fe197",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:11:07.230+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:11:09.477+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "35d45bb9f642417baf09a6b5768fe197",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:11:09.477+00:00",
  "event": "result",
  "elapsed_s": 2.203,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:11:09.512+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b85669477685475294dfdb685b6c22aa",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:09.512+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:10.446+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b85669477685475294dfdb685b6c22aa",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:10.446+00:00",
  "event": "result",
  "elapsed_s": 0.907,
  "response": []
}
```

## 2026-11-14T05:11:15.486+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "34d35b039caf4374916898548bd9f973",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:15.486+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:15.739+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "34d35b039caf4374916898548bd9f973",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:15.739+00:00",
  "event": "result",
  "elapsed_s": 0.204,
  "response": []
}
```

## 2026-11-14T05:11:20.781+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "522f2929df624c91865e15d72879b583",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:20.781+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:20.953+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "522f2929df624c91865e15d72879b583",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:20.953+00:00",
  "event": "result",
  "elapsed_s": 0.14,
  "response": []
}
```

## 2026-11-14T05:11:26.007+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "25fc0f8291434aaa99082b589a083d9b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:26.007+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:26.087+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "25fc0f8291434aaa99082b589a083d9b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:26.087+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:11:31.137+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "33b872ee033d406b8605302e16cd0e05",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:31.137+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:31.230+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "33b872ee033d406b8605302e16cd0e05",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:31.230+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:11:36.276+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "4eae7b2a8d68471e88f2521683983c3d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:36.276+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:36.347+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "4eae7b2a8d68471e88f2521683983c3d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:36.347+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:11:41.380+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2c1a2b6029114dd3b98f3d2a3ef29551",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:41.380+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:41.482+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2c1a2b6029114dd3b98f3d2a3ef29551",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:41.482+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:11:46.530+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "220ce13d5a32477080d808c4af1dfa85",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:46.530+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:46.595+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "220ce13d5a32477080d808c4af1dfa85",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:46.595+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:11:51.624+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d55afb59414c4d80a2c83546e63dbe2d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:51.624+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:51.664+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d55afb59414c4d80a2c83546e63dbe2d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:51.664+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:11:56.687+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "28b66866c0c5454f913040818185f437",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:11:56.687+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:11:58.441+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "28b66866c0c5454f913040818185f437",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:11:58.441+00:00",
  "event": "result",
  "elapsed_s": 1.719,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:11:58.452+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "44997c3c33e142869d20859bee7da510",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:58.452+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:11:58.921+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "44997c3c33e142869d20859bee7da510",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:11:58.921+00:00",
  "event": "result",
  "elapsed_s": 0.469,
  "response": []
}
```

## 2026-11-14T05:12:04.274+00:00 — dreamina / query_result — request

```json
{
  "request_id": "08f797afec4447e3bb956337471e59dd",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 50724,
  "request_fingerprint": "f1921058553f2a0a39f56f324b6688c1cd2a4913108d7bed00f5b060b66fe497",
  "time": "2026-11-14T05:12:04.274+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=65e97f85-5e7b-4b0a-ac07-3fba7da1c0a2",
      "--download_dir=edu_videos/redian_xiangying/t01_faa_ground_stop/seedance/sd1_tarmac"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:12:47.805+00:00 — dreamina / query_result — result

```json
{
  "request_id": "08f797afec4447e3bb956337471e59dd",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 50724,
  "request_fingerprint": "f1921058553f2a0a39f56f324b6688c1cd2a4913108d7bed00f5b060b66fe497",
  "time": "2026-11-14T05:12:47.805+00:00",
  "event": "result",
  "elapsed_s": 43.484,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"65e97f85-5e7b-4b0a-ac07-3fba7da1c0a2\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t01_faa_ground_stop\\\\seedance\\\\sd1_tarmac\\\\65e97f85-5e7b-4b0a-ac07-3fba7da1c0a2_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/30fe4961804336f56194355f29443064/6af7fbd1/video/tos/cn/tos-cn-v-148450/oYsetUvSHdmCEF73JQqgWBy3IaBfSG3RLACLZD/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=14950&bt=14950&cs=0&ds=12&ft=5QYTUxhhe6BMyqcgYheJD12Nzj&mime_type=video_mp4&qs=0&rc=Z2c2PGc4NTczOzdkOjo8NUBpanE6dmlvOmx4ZTczNDM7M0AzLzYuYmMtXjExMDNfMTNgYSM1Y2cxYWFebG9hLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794633147&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=2026111413120419801925525353622C9\n"
  }
}
```

## 2026-11-14T05:12:48.094+00:00 — dreamina / query_result — request

```json
{
  "request_id": "67b003fc333a4631b73c1e77f169a6d4",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 39896,
  "request_fingerprint": "f3c5492f3c8d63cbd1d01361c2e6ac98645627e71251dca1d3e50d95bc038afd",
  "time": "2026-11-14T05:12:48.094+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=64acbd20-b4eb-4c3c-b303-76c8c5b70e34",
      "--download_dir=edu_videos/redian_xiangying/t01_faa_ground_stop/seedance/sd2_control_room"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:13:50.903+00:00 — dreamina / query_result — result

```json
{
  "request_id": "67b003fc333a4631b73c1e77f169a6d4",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 39896,
  "request_fingerprint": "f3c5492f3c8d63cbd1d01361c2e6ac98645627e71251dca1d3e50d95bc038afd",
  "time": "2026-11-14T05:13:50.903+00:00",
  "event": "result",
  "elapsed_s": 62.781,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"64acbd20-b4eb-4c3c-b303-76c8c5b70e34\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t01_faa_ground_stop\\\\seedance\\\\sd2_control_room\\\\64acbd20-b4eb-4c3c-b303-76c8c5b70e34_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v6-artist.vlabvod.com/a0b2873c319abc5b62224c4ea0b49da6/6af7fbfd/video/tos/cn/tos-cn-v-148450/oUT9CIrEaYjYfB7ug7IFSsQzWtmoIqAHVHfBM3/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=11858&bt=11858&cs=0&ds=12&ft=5QYTUxhhe6BMyqY5YheJD12Nzj&mime_type=video_mp4&qs=0&rc=NWc6NjlpZTQ3M2Q2NDs5NkBpanFqbzZvOm94ZTczNDM7M0BjX2JeY2I0XjIxLy81YDUwYSNjai5tYWFmbG9hLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794633191&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=20261114131248198019255253414FC7D\n"
  }
}
```

## 2026-11-14T05:13:51.172+00:00 — dreamina / query_result — request

```json
{
  "request_id": "014e7a94e3c54f5392d2169a01f14094",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 75764,
  "request_fingerprint": "dc0d541507c387f878cb8c7e9f87755a8daeb6703a2b7c3f0326c7558891116d",
  "time": "2026-11-14T05:13:51.172+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=56f71d96-beb4-4675-9a88-07108e567b58",
      "--download_dir=edu_videos/redian_xiangying/t01_faa_ground_stop/seedance/sd3_cable_swap"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:15:51.449+00:00 — dreamina / query_result — result

```json
{
  "request_id": "014e7a94e3c54f5392d2169a01f14094",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 75764,
  "request_fingerprint": "dc0d541507c387f878cb8c7e9f87755a8daeb6703a2b7c3f0326c7558891116d",
  "time": "2026-11-14T05:15:51.449+00:00",
  "event": "result",
  "elapsed_s": 120.235,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"56f71d96-beb4-4675-9a88-07108e567b58\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t01_faa_ground_stop\\\\seedance\\\\sd3_cable_swap\\\\56f71d96-beb4-4675-9a88-07108e567b58_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/b798ae4e0f6ec1cc760ea707f34c5b6d/6af7fc3d/video/tos/cn/tos-cn-v-148450/oIE3aTsdHoB4QEEI7BWqS7TtgXCDHAvH0feHNj/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=9585&bt=9585&cs=0&ds=12&ft=5QYTUxhhe6BMyqY.YheJD12Nzj&mime_type=video_mp4&qs=0&rc=NDw7ZGdlPDw3OzRoNmk6OkBpajczdDZvOnR4ZTczNDM7M0BeYV4vNDI0Xl4xMV82MzJjYSNfbjQ2YWFubG9hLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794633255&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=202611141313511980192552534368B20\n"
  }
}
```

## 2026-11-14T05:15:51.726+00:00 — dreamina / query_result — request

```json
{
  "request_id": "8c4b4422307e4dceb35f30eb14105428",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 30136,
  "request_fingerprint": "d1e5257041b04007d8af5a092bb974318effebb35b4034b5f789b0776fe689bd",
  "time": "2026-11-14T05:15:51.726+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=4e40883e-1a5f-471a-b9ae-1ed28b52af9f",
      "--download_dir=edu_videos/redian_xiangying/t01_faa_ground_stop/seedance/sd4_trench_cut"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:21:35.789+00:00 — dreamina / query_result — result

```json
{
  "request_id": "8c4b4422307e4dceb35f30eb14105428",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 30136,
  "request_fingerprint": "d1e5257041b04007d8af5a092bb974318effebb35b4034b5f789b0776fe689bd",
  "time": "2026-11-14T05:21:35.789+00:00",
  "event": "result",
  "elapsed_s": 344.015,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"4e40883e-1a5f-471a-b9ae-1ed28b52af9f\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t01_faa_ground_stop\\\\seedance\\\\sd4_trench_cut\\\\4e40883e-1a5f-471a-b9ae-1ed28b52af9f_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/a101851d1db356961f11bdb34414e1ea/6af7fcb4/video/tos/cn/tos-cn-v-148450/oMPAkf7ukPjO98EVDucCBCRAItR1gA03efi7jq/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=11778&bt=11778&cs=0&ds=12&ft=5QYTUxhhe6BMyqfGYheJD12Nzj&mime_type=video_mp4&qs=0&rc=OjtpaDdkNTU8OGRmZTw5OEBpanE7eTpvOnd4ZTczNDM7M0AwYWAxLmAvXjMxX2FiNWAtYSNvZDFkYWFubG9hLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794633374&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=20261114131551198019255253998023A\n"
  }
}
```

## 2026-11-14T05:21:36.055+00:00 — dreamina / query_result — request

```json
{
  "request_id": "14dedb86daf6411690010ea092436081",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 80136,
  "request_fingerprint": "b4bce898d4e8785b415aafd8f1edcf5282a5108dbabc781a55a72078eb536481",
  "time": "2026-11-14T05:21:36.055+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=dc33ced3-c9bb-4dca-a755-aaba12968ec9",
      "--download_dir=edu_videos/redian_xiangying/t01_faa_ground_stop/seedance/sd5_landing"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T05:23:01.894+00:00 — dreamina / query_result — result

```json
{
  "request_id": "14dedb86daf6411690010ea092436081",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 80136,
  "request_fingerprint": "b4bce898d4e8785b415aafd8f1edcf5282a5108dbabc781a55a72078eb536481",
  "time": "2026-11-14T05:23:01.894+00:00",
  "event": "result",
  "elapsed_s": 85.813,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"dc33ced3-c9bb-4dca-a755-aaba12968ec9\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t01_faa_ground_stop\\\\seedance\\\\sd5_landing\\\\dc33ced3-c9bb-4dca-a755-aaba12968ec9_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 8.042\n      }\n    ]\n  },\n  \"credit_count\": 160,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v3-artist.vlabvod.com/aeb354c720975db1e62cd7ebd1fd3eda/6af7fe0f/video/tos/cn/tos-cn-v-148450/o4j2f7IJIfNOEk7C83p1RB3DyUkaQZeAHrvVEJ/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=7515&bt=7515&cs=0&ds=12&ft=5QYTUxhhe6BMyqOdYheJD12Nzj&mime_type=video_mp4&qs=0&rc=ZTQ5aDc5N2lpZWRkNzg3OEBpanZ2czZvOjh4ZTczNDM7M0A1YTBhNjJeXjMxMjBfMl9fYSNvZTRjYWEvbW9hLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794633719&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=20261114132136198019255253318049C\n"
  }
}
```

## 2026-11-14T05:27:10.876+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "0593f9e53afb4ec78191e8def5509f2e",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:27:10.876+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:27:14.143+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "0593f9e53afb4ec78191e8def5509f2e",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T05:27:14.143+00:00",
  "event": "result",
  "elapsed_s": 3.25,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T05:27:14.214+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "18b8943b593b40659c69fe34904eabd0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:14.214+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:14.902+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "18b8943b593b40659c69fe34904eabd0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:14.902+00:00",
  "event": "result",
  "elapsed_s": 0.656,
  "response": []
}
```

## 2026-11-14T05:27:19.930+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "6b275aebed29475e99780e5f42587e23",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:19.930+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:21.170+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "6b275aebed29475e99780e5f42587e23",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:21.170+00:00",
  "event": "result",
  "elapsed_s": 1.219,
  "response": []
}
```

## 2026-11-14T05:27:26.221+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "6b28a92d7e724228a72431c6c52565b3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:26.221+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:26.382+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "6b28a92d7e724228a72431c6c52565b3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:26.382+00:00",
  "event": "result",
  "elapsed_s": 0.14,
  "response": []
}
```

## 2026-11-14T05:27:31.416+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "20a0d5eafa2c4c529dd513e89693d048",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:31.416+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:31.530+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "20a0d5eafa2c4c529dd513e89693d048",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:31.530+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T05:27:36.569+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "dcb650bda35b4d1f993c9b3020c5cd69",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:36.569+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:36.661+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "dcb650bda35b4d1f993c9b3020c5cd69",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:36.661+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T05:27:41.696+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "e4bcdf69b6644dc9882105bbe3348ff2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:41.696+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:41.831+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "e4bcdf69b6644dc9882105bbe3348ff2",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:41.831+00:00",
  "event": "result",
  "elapsed_s": 0.093,
  "response": []
}
```

## 2026-11-14T05:27:46.880+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "93bcbbaa78d24a2fb1ec9f211b25ede7",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:46.880+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:46.953+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "93bcbbaa78d24a2fb1ec9f211b25ede7",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:46.953+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:27:51.999+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "85311d72e80c497bbc8b955b1495ec21",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:51.999+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:52.111+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "85311d72e80c497bbc8b955b1495ec21",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:52.111+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:27:57.149+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "fcc04de805744e649de4df4cce87ca73",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:57.149+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:27:57.228+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "fcc04de805744e649de4df4cce87ca73",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:27:57.228+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T05:28:02.264+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b1867b0cf2c5490cbf2078c7a9f5b439",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:02.264+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:02.355+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b1867b0cf2c5490cbf2078c7a9f5b439",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:02.355+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:07.392+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "af1180fe4aee422db728de95e2cefdf3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:07.392+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:07.493+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "af1180fe4aee422db728de95e2cefdf3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:07.493+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T05:28:12.539+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2cdccb756b674dbfb3146330ca06e96b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:12.539+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:12.630+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2cdccb756b674dbfb3146330ca06e96b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:12.630+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:17.682+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b36e57eff50a4a2380e5f4f4ac71dbf0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:17.682+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:17.762+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b36e57eff50a4a2380e5f4f4ac71dbf0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:17.762+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:22.794+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c25f21fb4e3d49fc9d910c61261db283",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:22.794+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:22.871+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c25f21fb4e3d49fc9d910c61261db283",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:22.871+00:00",
  "event": "result",
  "elapsed_s": 0.032,
  "response": []
}
```

## 2026-11-14T05:28:27.900+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "21ec57aca8014d5bb24caf71ff36cebc",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:27.900+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:27.992+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "21ec57aca8014d5bb24caf71ff36cebc",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:27.992+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:33.035+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b6bad61659154644aa6c8bffbcf38c03",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:33.035+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:33.130+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b6bad61659154644aa6c8bffbcf38c03",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:33.130+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:38.183+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2d917ae1f43f4061bf7d544d9ed6b7c9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:38.183+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:38.289+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2d917ae1f43f4061bf7d544d9ed6b7c9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:38.289+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T05:28:43.332+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "7517383cab164783a6edd5865a8cfb6e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:43.332+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:43.433+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "7517383cab164783a6edd5865a8cfb6e",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:43.433+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T05:28:48.476+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "01fee9b90d0d47b88a317ec73243b755",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:48.476+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T05:28:48.559+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "01fee9b90d0d47b88a317ec73243b755",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T05:28:48.559+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T06:16:08.129+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "79515877dddd433c9ecf075cbf0d2c8f",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T06:16:08.129+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T06:16:10.955+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "79515877dddd433c9ecf075cbf0d2c8f",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T06:16:10.955+00:00",
  "event": "result",
  "elapsed_s": 2.828,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T06:16:10.993+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c100b0ee28e24dacaacf08462e02a5a1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:10.993+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:11.082+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c100b0ee28e24dacaacf08462e02a5a1",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:11.082+00:00",
  "event": "result",
  "elapsed_s": 0.078,
  "response": []
}
```

## 2026-11-14T06:16:16.101+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "306991193084485385dc854ca92a86c3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:16.101+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:17.707+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "306991193084485385dc854ca92a86c3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:17.707+00:00",
  "event": "result",
  "elapsed_s": 1.562,
  "response": []
}
```

## 2026-11-14T06:16:22.717+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "9f0bbfed38e54f4382971a75569483d0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:22.717+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:22.804+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "9f0bbfed38e54f4382971a75569483d0",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:22.804+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T06:16:27.833+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "898f3f0013194eddae210e68818e0635",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:27.833+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:27.908+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "898f3f0013194eddae210e68818e0635",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:27.908+00:00",
  "event": "result",
  "elapsed_s": 0.046,
  "response": []
}
```

## 2026-11-14T06:16:32.933+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "1f3473e89c3446c0bde97c84fd4e9afa",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:32.933+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:33.028+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "1f3473e89c3446c0bde97c84fd4e9afa",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:33.028+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:16:38.044+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "b991a7766ac34347a47b3e4cb17dca81",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:38.044+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:38.111+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "b991a7766ac34347a47b3e4cb17dca81",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:38.111+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:16:43.130+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "c57a79fd077b4dc085256849e6a21b26",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:43.130+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:43.212+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "c57a79fd077b4dc085256849e6a21b26",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:43.212+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T06:16:48.236+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "32865fc0d5684378852dcf035b11a94b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:48.236+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:48.310+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "32865fc0d5684378852dcf035b11a94b",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:48.310+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:16:53.322+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "cd3c1c3f5d6c40898ebcffeebf80769d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:53.322+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:53.398+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "cd3c1c3f5d6c40898ebcffeebf80769d",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:53.398+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:16:58.435+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "94a4ac7c626643b4843159d91f19c5e8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:58.435+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:16:58.517+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "94a4ac7c626643b4843159d91f19c5e8",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:16:58.517+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:03.541+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "6fc4d9c7856c4743b2b2f2fa25ae2be6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:03.541+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:03.592+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "6fc4d9c7856c4743b2b2f2fa25ae2be6",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:03.592+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T06:17:08.613+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "2c4ba9031c664e408d9ab389f04a7f14",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:08.613+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:08.690+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "2c4ba9031c664e408d9ab389f04a7f14",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:08.690+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:13.716+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "d2ed6947bf5446bcaecb145d5e690bee",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:13.716+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:13.802+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "d2ed6947bf5446bcaecb145d5e690bee",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:13.802+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:18.824+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "12cbc5012c0243f99029551e878683ae",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:18.824+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:18.904+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "12cbc5012c0243f99029551e878683ae",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:18.904+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T06:17:23.926+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "ad369aef21da4bd896ddb378931dd0c5",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:23.926+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:23.994+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "ad369aef21da4bd896ddb378931dd0c5",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:23.994+00:00",
  "event": "result",
  "elapsed_s": 0.032,
  "response": []
}
```

## 2026-11-14T06:17:29.016+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "dc3ad677e3e74e458ab84799a0ab8aba",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:29.016+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:29.109+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "dc3ad677e3e74e458ab84799a0ab8aba",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:29.109+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": []
}
```

## 2026-11-14T06:17:34.150+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "8f6fcd5d1107435384f4273dbd545ea3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:34.150+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:34.232+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "8f6fcd5d1107435384f4273dbd545ea3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:34.232+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:39.257+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "3546d388b25e4369902e0cf35486def9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:39.257+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:39.350+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "3546d388b25e4369902e0cf35486def9",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:39.350+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:44.377+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "746ca8592349434da864b5b50c08e316",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:44.377+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed · suno-job-817c57f5275a461c8f6459e4229ae790"
  }
}
```

## 2026-11-14T06:17:44.441+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "746ca8592349434da864b5b50c08e316",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "d6545840b45f26dfb318c1f98cec07c3327ff39d458187376471f9af732ccfba",
  "time": "2026-11-14T06:17:44.441+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:17:52.587+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "b0be810d309c41dfaa0d2d5e9c974d58",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T06:17:52.587+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T06:17:54.545+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "b0be810d309c41dfaa0d2d5e9c974d58",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "384982a9249b0e7a5cb06d230b8465d9d3de7b33971afdbccad37464af512dfd",
  "time": "2026-11-14T06:17:54.545+00:00",
  "event": "result",
  "elapsed_s": 1.953,
  "response": {
    "url": "https://suno.com/create"
  }
}
```

## 2026-11-14T06:17:54.566+00:00 — suno-browser / prepare — request

```json
{
  "request_id": "b7faa7e5708e489daec6800cab4b7c5e",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "cb78601654616af39792f1dd7e4b73bd9f9a564fe23a9cda9b2755028081c5be",
  "time": "2026-11-14T06:17:54.566+00:00",
  "event": "request",
  "request": {
    "request": {
      "prompt": "Understated documentary news-explainer underscore, calm but quietly tense, minimal electronic pulse, soft muted piano motif, warm analog pad, light ticking percussion, subtle sub bass, steady mid tempo around 90 BPM, no vocals, no big drops, unobtrusive and sits well under a spoken voice, thoughtful and analytical mood",
      "format": "wav",
      "instrumental": true,
      "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
      "mode": "advanced",
      "title": "redian t01 bed v2",
      "options": {
        "exclude_styles": "vocals, heavy drums, distorted guitar, epic orchestral hits"
      },
      "references": []
    },
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:02.904+00:00 — suno-browser / prepare — result

```json
{
  "request_id": "b7faa7e5708e489daec6800cab4b7c5e",
  "provider": "suno-browser",
  "operation": "prepare",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "cb78601654616af39792f1dd7e4b73bd9f9a564fe23a9cda9b2755028081c5be",
  "time": "2026-11-14T06:18:02.904+00:00",
  "event": "result",
  "elapsed_s": 8.328,
  "response": [
    "https://suno.com/song/09516232-f7ee-41b9-836b-5f7dfe1ecf9b",
    "https://suno.com/song/0aabb622-08a2-4038-afd7-287302a1c976",
    "https://suno.com/song/0d5852e5-e5fb-4e52-bfd8-d37192fa3ceb",
    "https://suno.com/song/10ae81b2-3b87-4de7-8f2e-68f6d42fa7e5",
    "https://suno.com/song/173175d4-0fcb-4122-8353-37cd27813504",
    "https://suno.com/song/4b4d868b-ddf4-4352-a908-c7487d743711",
    "https://suno.com/song/58490eaf-9e2b-469e-b5d9-6e35285227ff",
    "https://suno.com/song/6904ff75-7d62-43b1-8fb1-24dce0a4c1b6",
    "https://suno.com/song/6a689bf4-07ae-4dec-992c-245c17819e68",
    "https://suno.com/song/813a380a-3126-4cf2-b165-03f6cb91fdf7",
    "https://suno.com/song/8cc80af1-3c13-47b4-a2f0-0bcc51124e14",
    "https://suno.com/song/a6e8621a-56f7-4d64-82a1-ee0a4796cb95",
    "https://suno.com/song/bf844d85-b6dd-4a34-8c87-5df3ad785609",
    "https://suno.com/song/dbc0e029-77a0-40f8-8f7f-26706f2071d4"
  ]
}
```

## 2026-11-14T06:18:02.931+00:00 — suno-browser / create — request

```json
{
  "request_id": "df059e4613c44902b7462152d2e710d6",
  "provider": "suno-browser",
  "operation": "create",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "579d3fd8a68b701e407ba6f3e1f8472f5de5d3e648540e44e9ff55afa6f28e62",
  "time": "2026-11-14T06:18:02.931+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54",
    "attempt": 1
  }
}
```

## 2026-11-14T06:18:13.987+00:00 — suno-browser / create — result

```json
{
  "request_id": "df059e4613c44902b7462152d2e710d6",
  "provider": "suno-browser",
  "operation": "create",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "579d3fd8a68b701e407ba6f3e1f8472f5de5d3e648540e44e9ff55afa6f28e62",
  "time": "2026-11-14T06:18:13.987+00:00",
  "event": "result",
  "elapsed_s": 11.047,
  "response": {
    "clicked": true,
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54",
    "cost": "unknown",
    "diagnostic": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\after-submit.json"
  }
}
```

## 2026-11-14T06:18:14.016+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "0fc951b247f74fc49cbc1f9a9eededfe",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:14.016+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:14.068+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "0fc951b247f74fc49cbc1f9a9eededfe",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:14.068+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:18:19.084+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "182fcf46269a431fb2e80d14a43819fd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:19.084+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:19.169+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "182fcf46269a431fb2e80d14a43819fd",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:19.169+00:00",
  "event": "result",
  "elapsed_s": 0.047,
  "response": []
}
```

## 2026-11-14T06:18:24.193+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "716b4a7e946c48e692813452ffcd48c3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:24.193+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:24.266+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "716b4a7e946c48e692813452ffcd48c3",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:24.266+00:00",
  "event": "result",
  "elapsed_s": 0.031,
  "response": []
}
```

## 2026-11-14T06:18:29.283+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "9a3e03c572884bc89ff461fb81dbc880",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:29.283+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:29.424+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "9a3e03c572884bc89ff461fb81dbc880",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:29.424+00:00",
  "event": "result",
  "elapsed_s": 0.109,
  "response": []
}
```

## 2026-11-14T06:18:34.450+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "0e9cdaa630ce46d9ac320235f5e7af96",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:34.450+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:34.558+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "0e9cdaa630ce46d9ac320235f5e7af96",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:34.558+00:00",
  "event": "result",
  "elapsed_s": 0.062,
  "response": []
}
```

## 2026-11-14T06:18:39.593+00:00 — suno-browser / poll_generation — request

```json
{
  "request_id": "5d2896b79e86414cb31193f4a2f13786",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:39.593+00:00",
  "event": "request",
  "request": {
    "title": "redian t01 bed v2 · suno-job-163bf01492874bde91d917836816ac54"
  }
}
```

## 2026-11-14T06:18:39.695+00:00 — suno-browser / poll_generation — result

```json
{
  "request_id": "5d2896b79e86414cb31193f4a2f13786",
  "provider": "suno-browser",
  "operation": "poll_generation",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "ec8e07c1b8de60d5335ef3bceeb8fb4433c2b92a580919b059278806aac23e8e",
  "time": "2026-11-14T06:18:39.695+00:00",
  "event": "result",
  "elapsed_s": 0.063,
  "response": [
    "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec",
    "https://suno.com/song/24ce1bfa-f31c-4f08-b9dd-a640e4dd9964"
  ]
}
```

## 2026-11-14T06:18:39.714+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "4275fdb93d064821b3eaf6c6d0b3c297",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:18:39.714+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:18:41.166+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "4275fdb93d064821b3eaf6c6d0b3c297",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:18:41.166+00:00",
  "event": "result",
  "elapsed_s": 1.437,
  "response": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:18:41.182+00:00 — suno-browser / download_official — request

```json
{
  "request_id": "1b800199e7c548d7944bd86bfa0b0470",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:18:41.182+00:00",
  "event": "request",
  "request": {
    "song_url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec",
    "format": "wav",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\outputs\\163bf01492874bde91d917836816ac54\\0c929b9c-3ad5-40d5-b21f-b509c6c76eec.wav"
  }
}
```

## 2026-11-14T06:19:05.859+00:00 — suno-browser / download_official — error

```json
{
  "request_id": "1b800199e7c548d7944bd86bfa0b0470",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:19:05.859+00:00",
  "event": "error",
  "elapsed_s": 24.672,
  "error_type": "ServiceError",
  "error": "more 匹配多个可见控件；需校准 selectors.json"
}
```

## 2026-11-14T06:19:12.986+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "d93258a387da4e679eb8246080707c07",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:19:12.986+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:19:14.406+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "d93258a387da4e679eb8246080707c07",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:19:14.406+00:00",
  "event": "result",
  "elapsed_s": 1.421,
  "response": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:19:14.420+00:00 — suno-browser / download_official — request

```json
{
  "request_id": "edb22043db914904a185c45677625849",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:19:14.420+00:00",
  "event": "request",
  "request": {
    "song_url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec",
    "format": "wav",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\outputs\\163bf01492874bde91d917836816ac54\\0c929b9c-3ad5-40d5-b21f-b509c6c76eec.wav"
  }
}
```

## 2026-11-14T06:19:16.152+00:00 — suno-browser / download_official — error

```json
{
  "request_id": "edb22043db914904a185c45677625849",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:19:16.152+00:00",
  "event": "error",
  "elapsed_s": 1.734,
  "error_type": "ServiceError",
  "error": "more 匹配多个可见控件；需校准 selectors.json"
}
```

## 2026-11-14T06:34:36.540+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "26fe0f598a114bbaa5b4e711b3d1b63f",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:34:36.540+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:34:38.329+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "26fe0f598a114bbaa5b4e711b3d1b63f",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:34:38.329+00:00",
  "event": "result",
  "elapsed_s": 1.797,
  "response": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:34:38.342+00:00 — suno-browser / download_official — request

```json
{
  "request_id": "fca23e1a597b4971b6aa17b1c9c6c13b",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:34:38.342+00:00",
  "event": "request",
  "request": {
    "song_url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec",
    "format": "wav",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\outputs\\163bf01492874bde91d917836816ac54\\0c929b9c-3ad5-40d5-b21f-b509c6c76eec.wav"
  }
}
```

## 2026-11-14T06:34:39.105+00:00 — suno-browser / download_official — error

```json
{
  "request_id": "fca23e1a597b4971b6aa17b1c9c6c13b",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 98200,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:34:39.105+00:00",
  "event": "error",
  "elapsed_s": 0.75,
  "error_type": "ServiceError",
  "error": "more 匹配多个可见控件；需校准 selectors.json"
}
```

## 2026-11-14T06:41:24.916+00:00 — suno-browser / browser_attach — request

```json
{
  "request_id": "150aea365147489dae69b954a091d6f4",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T06:41:24.916+00:00",
  "event": "request",
  "request": {
    "cdp": "127.0.0.1:9334",
    "window": "kept open by person"
  }
}
```

## 2026-11-14T06:41:25.640+00:00 — suno-browser / browser_attach — result

```json
{
  "request_id": "150aea365147489dae69b954a091d6f4",
  "provider": "suno-browser",
  "operation": "browser_attach",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "00563f9647a2fc3f5551043ae6116fb894e2154002ac26761512f51b2c37b409",
  "time": "2026-11-14T06:41:25.640+00:00",
  "event": "result",
  "elapsed_s": 0.719,
  "response": "<Browser type=<BrowserType name=chromium executable_path=C:\\Users\\light\\AppData\\Local\\ms-playwright\\chromium-1248\\chrome-win64\\chrome.exe> version=156.0.8078.48>"
}
```

## 2026-11-14T06:41:25.809+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "4ed2580e17404849b630b6d7235cf124",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:41:25.809+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:41:28.234+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "4ed2580e17404849b630b6d7235cf124",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "56258f420da4bc90412db14e6e72ebd5ae23e3eb71af594e568616c13564488c",
  "time": "2026-11-14T06:41:28.234+00:00",
  "event": "result",
  "elapsed_s": 2.391,
  "response": {
    "url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:41:28.256+00:00 — suno-browser / download_official — request

```json
{
  "request_id": "7405311f9d8f4296ae5accab2b02fa34",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:41:28.256+00:00",
  "event": "request",
  "request": {
    "song_url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec",
    "format": "wav",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\outputs\\163bf01492874bde91d917836816ac54\\0c929b9c-3ad5-40d5-b21f-b509c6c76eec.wav"
  }
}
```

## 2026-11-14T06:41:58.468+00:00 — suno-browser / download_official — result

```json
{
  "request_id": "7405311f9d8f4296ae5accab2b02fa34",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "1de7011e36d4324df8c42876c087830663bee70c1dddb4e61b8d9290b1c27f89",
  "time": "2026-11-14T06:41:58.468+00:00",
  "event": "result",
  "elapsed_s": 30.203,
  "response": {
    "name": "0c929b9c-3ad5-40d5-b21f-b509c6c76eec.wav",
    "bytes": 17117178,
    "sha256": "43ebfee830d5c0771c47bb6dd37f7f9a105eef9ebf751cfab436fb2e8e942297",
    "song_url": "https://suno.com/song/0c929b9c-3ad5-40d5-b21f-b509c6c76eec"
  }
}
```

## 2026-11-14T06:41:58.512+00:00 — suno-browser / navigate — request

```json
{
  "request_id": "0c52e41061254eb1a243db3d04a19ff4",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "def778b6697e4be817e5c320f1b3c3c0ca89da70f9b6d3929aa2991b61f354e4",
  "time": "2026-11-14T06:41:58.512+00:00",
  "event": "request",
  "request": {
    "url": "https://suno.com/song/24ce1bfa-f31c-4f08-b9dd-a640e4dd9964"
  }
}
```

## 2026-11-14T06:42:00.108+00:00 — suno-browser / navigate — result

```json
{
  "request_id": "0c52e41061254eb1a243db3d04a19ff4",
  "provider": "suno-browser",
  "operation": "navigate",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "def778b6697e4be817e5c320f1b3c3c0ca89da70f9b6d3929aa2991b61f354e4",
  "time": "2026-11-14T06:42:00.108+00:00",
  "event": "result",
  "elapsed_s": 1.579,
  "response": {
    "url": "https://suno.com/song/24ce1bfa-f31c-4f08-b9dd-a640e4dd9964"
  }
}
```

## 2026-11-14T06:42:00.136+00:00 — suno-browser / download_official — request

```json
{
  "request_id": "d57be87f50424d2ea3f7e57d866e5175",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "dd4cc8830b7e82bacc041a2079b9bb26ddcfdd8216fc4e8c3d37dfe059c7eede",
  "time": "2026-11-14T06:42:00.136+00:00",
  "event": "request",
  "request": {
    "song_url": "https://suno.com/song/24ce1bfa-f31c-4f08-b9dd-a640e4dd9964",
    "format": "wav",
    "output": "C:\\workspace\\micro-drama-platform\\.audit\\service_requests\\suno_browser_service\\outputs\\163bf01492874bde91d917836816ac54\\24ce1bfa-f31c-4f08-b9dd-a640e4dd9964.wav"
  }
}
```

## 2026-11-14T06:42:25.715+00:00 — suno-browser / download_official — result

```json
{
  "request_id": "d57be87f50424d2ea3f7e57d866e5175",
  "provider": "suno-browser",
  "operation": "download_official",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t01_faa_ground_stop",
  "pid": 69548,
  "request_fingerprint": "dd4cc8830b7e82bacc041a2079b9bb26ddcfdd8216fc4e8c3d37dfe059c7eede",
  "time": "2026-11-14T06:42:25.715+00:00",
  "event": "result",
  "elapsed_s": 25.547,
  "response": {
    "name": "24ce1bfa-f31c-4f08-b9dd-a640e4dd9964.wav",
    "bytes": 14828538,
    "sha256": "48e49feaf373b3989390b2f110d63bc071903724852f6f56ddd1fc83c0053bd4",
    "song_url": "https://suno.com/song/24ce1bfa-f31c-4f08-b9dd-a640e4dd9964"
  }
}
```

## 2026-11-14T12:30:55.429+00:00 — dreamina / text2video — request

```json
{
  "request_id": "37ec9a4ee30443e2851b8ac83f4c851a",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 13408,
  "request_fingerprint": "f16c079a2e2ce338eb1dfb7cf80cc0e4e786e766e0e08345bde9fb7fbf1e5889",
  "time": "2026-11-14T12:30:55.429+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=A large empty keynote stage in a dark arena after the show. A single spotlight shines on an empty spot at center stage, a giant blank screen behind it glowing faintly. The spotlight slowly dims and goes out. Rows of empty seats in the foreground, slow push-in, quiet, melancholic, realistic documentary look. No people, no text, no logos.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:31:07.991+00:00 — dreamina / text2video — result

```json
{
  "request_id": "37ec9a4ee30443e2851b8ac83f4c851a",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 13408,
  "request_fingerprint": "f16c079a2e2ce338eb1dfb7cf80cc0e4e786e766e0e08345bde9fb7fbf1e5889",
  "time": "2026-11-14T12:31:07.991+00:00",
  "event": "result",
  "elapsed_s": 12.547,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"2112846e-db87-47e7-afba-c4b9bdaac506\",\n  \"logid\": \"20261114203055198019255253881A712\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 499\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T12:31:08.279+00:00 — dreamina / text2video — request

```json
{
  "request_id": "a039231c862e4575ba8eeb287e5b81ac",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 38940,
  "request_fingerprint": "1ff843e752f039132af2da07c06945dfca6fb5977edff0a5acb3e9c7b4717983",
  "time": "2026-11-14T12:31:08.279+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Inside a vast modern AI data center: long aisles of black server racks with dense blinking status lights and thick bundles of cables, cool blue light, faint haze. Slow dolly forward down the aisle. Realistic, cinematic, no people, no readable text, no logos or brand markings.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:31:21.081+00:00 — dreamina / text2video — result

```json
{
  "request_id": "a039231c862e4575ba8eeb287e5b81ac",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 38940,
  "request_fingerprint": "1ff843e752f039132af2da07c06945dfca6fb5977edff0a5acb3e9c7b4717983",
  "time": "2026-11-14T12:31:21.081+00:00",
  "event": "result",
  "elapsed_s": 12.781,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"ca8bdd32-5d5a-4da4-aec7-11c72a1f4ef7\",\n  \"logid\": \"202611142031081980192552539452848\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 509\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T12:31:21.392+00:00 — dreamina / text2video — request

```json
{
  "request_id": "76744336da1c440b98cfe920a1ad4fa9",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 9244,
  "request_fingerprint": "d0fecfdf358e68406b298d966e13bf060ce3c7ec1d535d17505d98471a77a723",
  "time": "2026-11-14T12:31:21.392+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=Dusk at a busy Southeast Asian container port. A crane lowers a shipping container onto a cargo ship; in the foreground, a forklift carries wooden-crated server boxes wrapped in plastic toward a container. Humid air, orange sky, wide shot slowly panning. Realistic documentary footage, workers small and unrecognizable in the distance. No readable text, no logos.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:31:32.425+00:00 — dreamina / text2video — result

```json
{
  "request_id": "76744336da1c440b98cfe920a1ad4fa9",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 9244,
  "request_fingerprint": "d0fecfdf358e68406b298d966e13bf060ce3c7ec1d535d17505d98471a77a723",
  "time": "2026-11-14T12:31:32.425+00:00",
  "event": "result",
  "elapsed_s": 11.0,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"69d4f1de-f1d8-4e58-bdee-000038369815\",\n  \"logid\": \"202611142031211980192552537601A07\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 548\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T12:31:32.956+00:00 — dreamina / text2video — request

```json
{
  "request_id": "66c45c65572b48aab36aca36239da338",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 6360,
  "request_fingerprint": "f5ddae17d845437fa42d3f8801d459e6ef58b5274bb04e384431dfef3b2dd860",
  "time": "2026-11-14T12:31:32.956+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "text2video",
      "--prompt=An empty congressional hearing room: a raised curved dais with rows of leather chairs and microphones, a single empty witness table with one microphone facing it. Soft overhead light, dust in the air, slow push-in toward the empty witness chair. Realistic, quiet, tense. No people, no flags with readable text, no nameplates, no logos.",
      "--model_version=seedance2.5",
      "--video_resolution=720p",
      "--ratio=16:9",
      "--duration=6",
      "--poll=0"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:31:45.460+00:00 — dreamina / text2video — result

```json
{
  "request_id": "66c45c65572b48aab36aca36239da338",
  "provider": "dreamina",
  "operation": "text2video",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 6360,
  "request_fingerprint": "f5ddae17d845437fa42d3f8801d459e6ef58b5274bb04e384431dfef3b2dd860",
  "time": "2026-11-14T12:31:45.460+00:00",
  "event": "result",
  "elapsed_s": 12.469,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"eaacbbb4-3d67-4560-833f-7dfe03e24af8\",\n  \"logid\": \"202611142031331980192552535503E1C\",\n  \"gen_status\": \"querying\",\n  \"credit_count\": 120,\n  \"estimated_remaining_seconds\": 547\n}\n",
    "stderr": ""
  }
}
```

## 2026-11-14T12:39:38.259+00:00 — dreamina / query_result — request

```json
{
  "request_id": "aea65ef88db9498f91b2575ec2371793",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 17792,
  "request_fingerprint": "e2b7abb510c06323fc03cc6509dfeb20a27d6a2b181093951e1f3c457e533539",
  "time": "2026-11-14T12:39:38.259+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=2112846e-db87-47e7-afba-c4b9bdaac506",
      "--download_dir=edu_videos/redian_xiangying/t02_jensen_huang_resigns/seedance/sd1_empty_stage"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:39:54.269+00:00 — dreamina / query_result — result

```json
{
  "request_id": "aea65ef88db9498f91b2575ec2371793",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 17792,
  "request_fingerprint": "e2b7abb510c06323fc03cc6509dfeb20a27d6a2b181093951e1f3c457e533539",
  "time": "2026-11-14T12:39:54.269+00:00",
  "event": "result",
  "elapsed_s": 15.969,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"2112846e-db87-47e7-afba-c4b9bdaac506\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t02_jensen_huang_resigns\\\\seedance\\\\sd1_empty_stage\\\\2112846e-db87-47e7-afba-c4b9bdaac506_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v3-artist.vlabvod.com/23db1be3ca2d91820740fe31115832f0/6af864c3/video/tos/cn/tos-cn-v-148450/osnQCIq0gSqfAsaqBtIUCqaBLKf4M7H8vwX5gw/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=7248&bt=7248&cs=0&ds=12&ft=5QYTUxhhe6BMyqj~dleJD12Nzj&mime_type=video_mp4&qs=0&rc=aTQ4NDUzODQ8aGU1O2hlNEBpM29pNWdvOnY4ZTczNDM7M0A2L15gNi5gX18xLjBfNDQwYSMwcGVfYWFmXnBhLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794660013&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=20261114203938198019255253832D8B2\n"
  }
}
```

## 2026-11-14T12:39:54.715+00:00 — dreamina / query_result — request

```json
{
  "request_id": "b4994687fa854af8964af132c745ddd9",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 47500,
  "request_fingerprint": "ef23ada2a0703d1b0208066152a4d54c292fd2401b6e1027bc43311ba8ad4a61",
  "time": "2026-11-14T12:39:54.715+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=ca8bdd32-5d5a-4da4-aec7-11c72a1f4ef7",
      "--download_dir=edu_videos/redian_xiangying/t02_jensen_huang_resigns/seedance/sd2_datacenter"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:40:28.677+00:00 — dreamina / query_result — result

```json
{
  "request_id": "b4994687fa854af8964af132c745ddd9",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 47500,
  "request_fingerprint": "ef23ada2a0703d1b0208066152a4d54c292fd2401b6e1027bc43311ba8ad4a61",
  "time": "2026-11-14T12:40:28.677+00:00",
  "event": "result",
  "elapsed_s": 33.938,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"ca8bdd32-5d5a-4da4-aec7-11c72a1f4ef7\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t02_jensen_huang_resigns\\\\seedance\\\\sd2_datacenter\\\\ca8bdd32-5d5a-4da4-aec7-11c72a1f4ef7_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/3b9c817fd7fbb55d3a21abb3ddb5d136/6af864d8/video/tos/cn/tos-cn-v-148450/o4IV0DDDOUaeD4o7IVtVeQeYBkcSIACDFKgEkk/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=19495&bt=19495&cs=0&ds=12&ft=5QYTUxhhe6BMyqq9dleJD12Nzj&mime_type=video_mp4&qs=0&rc=Nzk0N2Q7ZzppPDRkaTpkNUBpMzg5NTRvOnk4ZTczNDM7M0BgYDFeNC4wNmIxLTViLzUzYSM2MDVtYWEvXnBhLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794660034&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=202611142039551980192552532382530\n"
  }
}
```

## 2026-11-14T12:40:29.111+00:00 — dreamina / query_result — request

```json
{
  "request_id": "e42aa60f6c3e4ed9adfc3ea54ddb9760",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 38768,
  "request_fingerprint": "cbda7d66a5b35aa06aa78482c347630d4a732069805d3b20fd2ed56b0e7c019d",
  "time": "2026-11-14T12:40:29.111+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=69d4f1de-f1d8-4e58-bdee-000038369815",
      "--download_dir=edu_videos/redian_xiangying/t02_jensen_huang_resigns/seedance/sd3_port"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:40:51.191+00:00 — dreamina / query_result — result

```json
{
  "request_id": "e42aa60f6c3e4ed9adfc3ea54ddb9760",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 38768,
  "request_fingerprint": "cbda7d66a5b35aa06aa78482c347630d4a732069805d3b20fd2ed56b0e7c019d",
  "time": "2026-11-14T12:40:51.191+00:00",
  "event": "result",
  "elapsed_s": 22.046,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"69d4f1de-f1d8-4e58-bdee-000038369815\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t02_jensen_huang_resigns\\\\seedance\\\\sd3_port\\\\69d4f1de-f1d8-4e58-bdee-000038369815_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/88c39e9e7e59850a62908c2b06977632/6af864f8/video/tos/cn/tos-cn-v-148450/o0RIhIThUMVgxav1EaGQlwKQXQ4VdWvsEdtZZ/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=16510&bt=16510&cs=0&ds=12&ft=5QYTUxhhe6BMyqN9dleJD12Nzj&mime_type=video_mp4&qs=0&rc=Omk0aTRnaDQ7NWkzZGc1aEBpanR3Z2lvOjg4ZTczNDM7M0BjLjJiYjQuX18xLmMtNS1eYSNsbl4yYWFeX3BhLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794660066&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=202611142040291980192552537498B11\n"
  }
}
```

## 2026-11-14T12:40:51.538+00:00 — dreamina / query_result — request

```json
{
  "request_id": "bc9c5800d6ee4e618bf7708efedf7880",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 31612,
  "request_fingerprint": "dbb4edca90f37f47fb091a4683a0e15497c8089a13cbdbc984bd371151686aac",
  "time": "2026-11-14T12:40:51.538+00:00",
  "event": "request",
  "request": {
    "argv": [
      "dreamina",
      "query_result",
      "--submit_id=eaacbbb4-3d67-4560-833f-7dfe03e24af8",
      "--download_dir=edu_videos/redian_xiangying/t02_jensen_huang_resigns/seedance/sd4_hearing_room"
    ],
    "files": [],
    "timeout_s": null,
    "attempt": 1,
    "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"
  }
}
```

## 2026-11-14T12:41:10.851+00:00 — dreamina / query_result — result

```json
{
  "request_id": "bc9c5800d6ee4e618bf7708efedf7880",
  "provider": "dreamina",
  "operation": "query_result",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\t02_jensen_huang_resigns",
  "pid": 31612,
  "request_fingerprint": "dbb4edca90f37f47fb091a4683a0e15497c8089a13cbdbc984bd371151686aac",
  "time": "2026-11-14T12:41:10.851+00:00",
  "event": "result",
  "elapsed_s": 19.297,
  "response": {
    "returncode": 0,
    "stdout": "{\n  \"submit_id\": \"eaacbbb4-3d67-4560-833f-7dfe03e24af8\",\n  \"gen_status\": \"success\",\n  \"result_json\": {\n    \"images\": [],\n    \"videos\": [\n      {\n        \"path\": \"edu_videos\\\\redian_xiangying\\\\t02_jensen_huang_resigns\\\\seedance\\\\sd4_hearing_room\\\\eaacbbb4-3d67-4560-833f-7dfe03e24af8_video_1.mp4\",\n        \"fps\": 24,\n        \"width\": 1280,\n        \"height\": 720,\n        \"format\": \"mp4\",\n        \"duration\": 6.042\n      }\n    ]\n  },\n  \"credit_count\": 120,\n  \"queue_info\": {\n    \"queue_idx\": 0,\n    \"priority\": 7,\n    \"queue_status\": \"Finish\",\n    \"queue_length\": 0,\n    \"debug_info\": \"{\\\"have_no_dreamina_queue_name\\\":false,\\\"dreamina_matrix_queue_name\\\":\\\"dreamina_fusion_video45_pro\\\",\\\"dreamina_matrix_req_key\\\":\\\"DreaminaFusion:Video45_base\\\",\\\"dreamina_matrix_second_req_key\\\":\\\"\\\",\\\"have_no_queue_name\\\":true,\\\"queue_name\\\":\\\"\\\",\\\"matrix_req_key\\\":\\\"\\\",\\\"matrix_second_req_key\\\":\\\"\\\"}\"\n  }\n}\n",
    "stderr": "download video 1 URL: https://v9-artist.vlabvod.com/56807c9236d2c646682310bc9ccccff1/6af8650c/video/tos/cn/tos-cn-v-148450/oQdVPTpWIWviV3ahIQkIXqEnvbEtQhg4bjwCE/?a=4066&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&br=11352&bt=11352&cs=0&ds=12&ft=5QYTUxhhe6BMyqa9dleJD12Nzj&mime_type=video_mp4&qs=0&rc=Zjs0Z2VkaTQ2aWc0ZTg7ZEBpMzpoamlvOnE4ZTczNDM7M0A2YTNfXmFjNTQxXjNiMTZiYSNmMmhoYWEvXnBhLS1kNC9zcw%3D%3D&btag=80000e00008000&dy_q=1794660086&feature_id=04b16e464b574158bb99cac30ccb1f5e&l=202611142040511980192552538990F64\n"
  }
}
```
