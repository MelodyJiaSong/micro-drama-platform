# 外部服务请求日志

请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。

## 2026-11-14T12:54:56.115+00:00 — elevenlabs / GET /v1/shared-voices — request

```json
{
  "request_id": "367b1b502947493c8e03fd06ddc3d133",
  "provider": "elevenlabs",
  "operation": "GET /v1/shared-voices",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 41584,
  "request_fingerprint": "62fe05c158d6b0a4da0be44fabdb272280137012491b66b2890b67daadb193f6",
  "time": "2026-11-14T12:54:56.115+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/shared-voices?language=zh&gender=male&page_size=30&sort=usage_character_count_1y"
  }
}
```

## 2026-11-14T12:55:10.360+00:00 — elevenlabs / GET /v1/shared-voices — result

```json
{
  "request_id": "367b1b502947493c8e03fd06ddc3d133",
  "provider": "elevenlabs",
  "operation": "GET /v1/shared-voices",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 41584,
  "request_fingerprint": "62fe05c158d6b0a4da0be44fabdb272280137012491b66b2890b67daadb193f6",
  "time": "2026-11-14T12:55:10.360+00:00",
  "event": "result",
  "elapsed_s": 14.25,
  "response": {
    "http_status": 200,
    "body": {
      "voices": [
        {
          "public_owner_id": "60079d355e8d217eb5d21249e688a09ac07a6d483c50a63560d9936211b5b100",
          "voice_id": "4VZIsMPtgggwNg7OXbPY",
          "date_unix": 1735673423,
          "name": "James Gao - Calm, Friendly and Warm",
          "accent": "standard",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A middle-aged Chinese voice in a calm, friendly tone. Perfect for narrative and storytelling. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3",
          "usage_character_count_1y": 103318859,
          "usage_character_count_7d": 1031067,
          "play_api_usage_character_count_1y": 157478595,
          "cloned_by_count": 40170,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/9fLlmDXPhO819IAIRK44.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/ceabbf6c-043c-4f8e-8469-2201c0c1e7c2.mp3"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "el-GR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/a2561d7a-af7d-4d26-b0ab-456b8128411c.mp3"
            },
            {
              "language": "hr",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "hr-HR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/201779a9-fa7b-4897-8ef2-6d3d4ef31486.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/95257599-ce34-4763-98ab-11560652398a.mp3"
            },
            {
              "language": "fil",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "fil-PH",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/c358959d-3e7d-4372-ac04-20cac83a7d92.mp3"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "southern",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/fe95adf7-a51d-44a6-86db-bf89fc1f5ace.mp3"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cs-CZ",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/72c36b4f-8881-4657-b24b-d7a6da6e24a2.mp3"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "ru-RU",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/97056fa7-a2c5-46ca-bd17-9fc5b5829c1e.mp3"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "ko-KR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/0b84285c-f6c7-400d-a043-0ba4bc84a35b.mp3"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "el-GR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/709b0dee-2ef3-4085-a452-cdbd2a25fd80.mp3"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "en-US",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/ba9e4523-fc6e-4ba2-a008-81ebfcb8de69.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "northern",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/qCmCyqVqIbevIuA9FVI25BpgadC2/voices/4VZIsMPtgggwNg7OXbPY/962a18fb-d037-414f-a342-5bb119e39d5d.mp3"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-istrian",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_multilingual_v2",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4VZIsMPtgggwNg7OXbPY/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "29f5388195d2631d13993e7f988c8f402c68c1499a227969fefa53566d228f1c",
          "voice_id": "hZTuv9Zqrq4yHYrEmF1r",
          "date_unix": 1761606535,
          "name": "Adam Li -  Deep, Steady and Calm",
          "accent": "singapore mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": null,
          "description": "Smooth and steady with a touch of depth—like something you’d hear on late-night radio. It doesn’t try too hard, but still pulls you in. Perfect for narration, storytelling, audiobooks, or any calm yet compelling voiceover work.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3",
          "usage_character_count_1y": 88949077,
          "usage_character_count_7d": 740545,
          "play_api_usage_character_count_1y": 123322196,
          "cloned_by_count": 125190,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "singapore mandarin",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/quDcGrthgkcACCa12rwG8Xzyp5Q2/voices/hZTuv9Zqrq4yHYrEmF1r/MReL0fdboS5j8sjxEN0K.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "6293b9dfc6ac413ab58d3844addcf7871b250281ecd7013106d13a2fbe6cfeef",
          "voice_id": "MI36FIkp9wRP7cpWKPTl",
          "date_unix": 1749683297,
          "name": "Evan Zhao - Warm, Calm and Trustworthy",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "gentle",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A calm and trustworthy Mandarin male voice with smooth rhythm and warm tone — perfect for audiobooks, language content, and emotional narration. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3",
          "usage_character_count_1y": 79532432,
          "usage_character_count_7d": 1422605,
          "play_api_usage_character_count_1y": 146310903,
          "cloned_by_count": 34074,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Z4YmgeFNh2To6n9dYoppEePJeMr1/voices/MI36FIkp9wRP7cpWKPTl/ZdfInoVLSM5izvMkRQFp.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "98502da27d31153bf16a3b7acc4708333deb810b421a78e356e09261f54706f0",
          "voice_id": "fQj4gJSexpu8RDE2Ii5m",
          "date_unix": 1736014830,
          "name": "Yu - Youthful, Energetic and Engaging",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "gentle",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Yu is a vibrant, upbeat voice in Traditional Chinese with a youthful Taiwanese accent. It is characterized by its energetic tone and engaging delivery. Perfectly suited for tutorials, podcasts, calls, and classes, this voice ensures clarity and captures attention with a professional yet approachable vibe.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3",
          "usage_character_count_1y": 67673765,
          "usage_character_count_7d": 2395458,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 53548,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8OXM7U7aZFcKI05Whl3sOM2HBaN2/voices/fQj4gJSexpu8RDE2Ii5m/xXnDtL0jvbLE622bVoEA.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "213859b1d1703a17daae1d56066a547571ab298b14e1a86eedd05126a8bf08b8",
          "voice_id": "DowyQ68vDpgFYdWVGjc3",
          "date_unix": 1755829946,
          "name": "Jason Chen - Deep, Magnetic and Calm",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "I am Jason Chen, a deep and magnetic Chinese male voice. My tone is calm, steady, and expressive, carrying a sense of confidence and composure. I am perfect for narrations, audiobooks, podcasts, and any content that needs a mature and captivating voice.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 62181090,
          "usage_character_count_7d": 1755825,
          "play_api_usage_character_count_1y": 125968377,
          "cloned_by_count": 85422,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJmMTdlNzY0YjQ2MzU0OTM0YWViOTFhNDRkNDRiN2ZkMyIsImZpbGVuYW1lIjoiWjh6bnNZaXJXRTV3RVhNM1MxdTIubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_flash_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_multilingual_v2",
              "accent": "da-jutlandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "da",
              "model_id": "eleven_flash_v2_5",
              "accent": "da-jutlandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_turbo_v2_5",
              "accent": "da-jutlandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "uk-kiev",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/DowyQ68vDpgFYdWVGjc3/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "29bd8fd8955e9b728677c3d46738fb974e4f0f6e89a5cdf80181682783dd969e",
          "voice_id": "BrbEfHMQu0fyclQR7lfh",
          "date_unix": 1733003229,
          "name": "Kevin Tu - Natural, Steady and Calm",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "mature",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "An adult Taiwanese Mandarin voice with high-mid voice, good for news, narrative or story.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3",
          "usage_character_count_1y": 57844371,
          "usage_character_count_7d": 1185018,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 25952,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/b5Zp2CfP11gb1M1Z0C1qw5rmVBh1/voices/BrbEfHMQu0fyclQR7lfh/ce3695e5-8510-40c7-925d-96d49a59c266.mp3"
            }
          ],
          "notice_period": 365,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "e9a6840c69b79812b77ea81fa11d55aaf80dcf1938fa0137bf7f514f67f75c99",
          "voice_id": "WuLq5z7nEcrhppO0ZQJw",
          "date_unix": 1715534917,
          "name": "Martin Li - Raspy, Serious and Deep",
          "accent": "standard",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Middle aged Male with a Serious and Intimate voice. Perfect for audiobooks.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3",
          "usage_character_count_1y": 56505872,
          "usage_character_count_7d": 736194,
          "play_api_usage_character_count_1y": 24575571,
          "cloned_by_count": 39276,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/WuLq5z7nEcrhppO0ZQJw/VQoMkMi8aSXSAwz6NHzh.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/dac43adc-4507-4b9e-9d9f-7e442c062def.mp3"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "pl-PL",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/95e74d44-612d-4a8c-b768-93351905138c.mp3"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cs-CZ",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/740568fb-27df-4f9f-9021-a30c8762c22c.mp3"
            },
            {
              "language": "fr",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "fr-FR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/f9a52f18-171d-4c02-ad01-df9cc908147e.mp3"
            },
            {
              "language": "fil",
              "model_id": "eleven_turbo_v2_5",
              "accent": "central",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/d1b96e54-82af-4918-ac4f-e1c308fcf557.mp3"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "tr-TR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/7f25d334-945e-4272-b1ac-b5a2f866c3ee.mp3"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "central",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/09deb146-c5d2-4902-832c-b8d421587755.mp3"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "hu-HU",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/0b3c5a31-a4f6-42d2-a3a6-a91476f1fab5.mp3"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "ro-RO",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/8f6c9d0e-21b9-4c8e-941f-a0820a004db3.mp3"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "pt-BR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/c0dc76c4-998c-4aeb-b84b-4d35b1ec7574.mp3"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cs-CZ",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/cfb1a4b5-03a5-4f68-8a7d-fac2c67eb81f.mp3"
            },
            {
              "language": "sk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "sk-SK",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/d14315af-baa3-476f-9bb2-f3b2222bc165.mp3"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "pl-PL",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/cbbb30ca-a8cc-4bbc-9723-f5243478a082.mp3"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "central",
              "locale": "sv-SE",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/5f871505-2803-4b47-aaad-6e1dd519126c.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/910237bc-8b9a-459d-9301-1a2e7798cc57.mp3"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "es-ES",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/8RYUsFHsalUXjwVG0LjhNwH1j022/voices/WuLq5z7nEcrhppO0ZQJw/6354eaa2-f339-4088-9ce8-cf09e26c1da9.mp3"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/WuLq5z7nEcrhppO0ZQJw/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "37c7a55dd5ac8593c00a130495e595a5d0754ef56973f2acc6c1f1097c10fdfa",
          "voice_id": "W8lBaQb9YIoddhxfQNLP",
          "date_unix": 1761084106,
          "name": "Siqi Liu - Calm, Warm and Gentle",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A calm and warm Chinese male voice with a gentle rhythm and natural articulation. Ideal for audiobooks, podcasts, guided meditations, and emotional storytelling in Mandarin Chinese.\n",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 30070288,
          "usage_character_count_7d": 542889,
          "play_api_usage_character_count_1y": 33992627,
          "cloned_by_count": 17221,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWGJwTUtVRWdESE9OM2F2ZTBQdDJaWVAzVzVBMiIsImZpbGVuYW1lIjoiUDZ3blB1dkRMUkoycldqRXFlc1YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hu",
              "model_id": "eleven_flash_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_multilingual_v2",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ta",
              "model_id": "eleven_flash_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "bg",
              "model_id": "eleven_turbo_v2_5",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_multilingual_v2",
              "accent": "hr-zagreb",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-received-pronunciation",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-received-pronunciation",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/W8lBaQb9YIoddhxfQNLP/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "adc9f3ee76562072a32fad7d72edc6b3e523b1628c749f160e836396cd54ef0e",
          "voice_id": "pU9NaAwkoR3v0Mrg3uKz",
          "date_unix": 1761336200,
          "name": "Haoran - Deep, Calm and Steady",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "advertisement",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A deep and magnetic male voice with a steady tone and expressive delivery. Perfect for voiceovers, documentaries, brand videos, or any project that needs a grounded and engaging presence.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3",
          "usage_character_count_1y": 29385732,
          "usage_character_count_7d": 660159,
          "play_api_usage_character_count_1y": 33099435,
          "cloned_by_count": 49349,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/H79ZdRWHdQYLqHU5CQ9Fcdf6iE63/voices/pU9NaAwkoR3v0Mrg3uKz/OyAgLV46qFj8zWNuBRLa.mp3"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "bg",
              "model_id": "eleven_multilingual_v2",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "bg",
              "model_id": "eleven_flash_v2_5",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_flash_v2_5",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_multilingual_v2",
              "accent": "da-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_flash_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-malaysian",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-malaysian",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/pU9NaAwkoR3v0Mrg3uKz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "b2c9ca34784432b033599d179ceb4b64d8f1ce591924b6b92baae31235f48bfc",
          "voice_id": "agczkAUlHLowaNnL72Cc",
          "date_unix": 1772713944,
          "name": "Adrian - Chinese Mandarin Narration",
          "accent": "standard",
          "gender": "male",
          "age": "young",
          "descriptive": "neutral",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A calm and clear Mandarin Chinese male voice with a modern narration style.  Ideal for documentaries, explainer videos, corporate narration, and educational content. Natural pacing with a professional yet approachable tone.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3",
          "usage_character_count_1y": 25744836,
          "usage_character_count_7d": 1165483,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 13334,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/4e1145b6394747f1a2d2be588f152220/voices/agczkAUlHLowaNnL72Cc/fn0Cwgdgf7oZYQwJDbSB.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "c85885c5be715f04f6838e0c05034903e97f0ab76fa70af63fcbbfb89bba6d74",
          "voice_id": "pTOe8BQRdydOEIgv0wFL",
          "date_unix": 1752818357,
          "name": "LiuPing - Clear, Professional and Calm",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Hi, I’m Liu Ping, a native Mandarin Chinese speaker. My voice is clear, professional, and recorded in standard Chinese (普通话), ideal for audiobooks, AI, learning apps, and narration. If you need a natural, expressive, and high-quality Chinese voice, my model is ready for both personal and commercial use on ElevenLabs.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3",
          "usage_character_count_1y": 17394926,
          "usage_character_count_7d": 386307,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 10772,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fm5UDf7fQEfksunysBwZ2rXkgNf2/voices/pTOe8BQRdydOEIgv0wFL/iKnSGsHhztjTg5231nUR.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "64753ac05e15cb80c266adacebb3ac7b5e32c673f9867dd2bd5ff28ff0660c1f",
          "voice_id": "vZZLclMx4wouUtKBRfZn",
          "date_unix": 1759727668,
          "name": "Jin - Clear, Warm and Casual",
          "accent": "standard",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "casual",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A warm, casual male Chinese voice with a subtle Taiwanese and Singaporean influence, clear and approachable for global audiences. The accent is light, unplaceable, and versatile — making it ideal for natural conversations, Youtube Podcasts, storytelling, and friendly narration.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3",
          "usage_character_count_1y": 16073762,
          "usage_character_count_7d": 635421,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 10273,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/3unCj929XjWjMS71AYlfn2pKKTd2/voices/vZZLclMx4wouUtKBRfZn/2c7992a3-7efd-45b6-99f5-973f9836b04e.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": true,
          "is_bookmarked": false
        },
        {
          "public_owner_id": "9c17de8036c987d57a4f1e304c7d264d051cb3792e4c749165acd1ff35346193",
          "voice_id": "kbrsaic1zriFXx1pgRYN",
          "date_unix": 1755240493,
          "name": "Evan - Warm, Soothing and Soft",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Therapeutic and calming Taiwanese Mandarin, with a laid-back warmth that soothes and reassures.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 15917943,
          "usage_character_count_7d": 572583,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 11222,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/kbrsaic1zriFXx1pgRYN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiMEE2UXBCSUFaQVJJTXEwN3FoQVBWMDU2aWUxMyIsImZpbGVuYW1lIjoiU2FaYkNQdGxlcG1ZWFlHU24ySG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "dd0f5bb9ac12aaca6570a8c8d9c32a6e97f7c05c673d9864fbccc662fb7b03d7",
          "voice_id": "5mZxJZhSmJTjL7GoYfYI",
          "date_unix": 1709644748,
          "name": "Karo Yang - Clear, Lively and Energetic",
          "accent": "standard",
          "gender": "male",
          "age": "young",
          "descriptive": "pleasant",
          "use_case": "social_media",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A youthful Asian male voice with a slightly neutral tone and lively energy is suitable for narrating stories and creating content for social media videos.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3",
          "usage_character_count_1y": 14576048,
          "usage_character_count_7d": 70865,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 10574,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": false,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/5mZxJZhSmJTjL7GoYfYI/AxKwa8mUXQbuKEt3jQTm.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "de3e9737b7354c631b21363fc7fb0df5a3da512da9b6a7c35d04ed19fe29dd23",
          "voice_id": "Z9RJEkFYQw307BCQULDR",
          "date_unix": 1777111120,
          "name": "Kuo Yu - Taiwan ",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "advertisement",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Composed and reserved male voice.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3",
          "usage_character_count_1y": 10909761,
          "usage_character_count_7d": 729585,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 6071,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/8e232e46f36f420e9afd1a1f63df2fe0/voices/Z9RJEkFYQw307BCQULDR/abed432e-3e3c-4915-83fa-b9c370ebb51a.mp3"
            }
          ],
          "notice_period": 180,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "20b44f4877342894cc40f1df17e905bf4082a792ba30b5fa123e8c0789dcc85d",
          "voice_id": "M0TrFmFeBJS9H4xzdk8Z",
          "date_unix": 1745119010,
          "name": "Steven Gor - Low, Calm and Soothing",
          "accent": "standard",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A young-aged Singaporean Chinese voice in a low, calm, soothing tone. Perfect for narrative and storytelling.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 10134082,
          "usage_character_count_7d": 210714,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 6375,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/M0TrFmFeBJS9H4xzdk8Z/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiOXpId1JuQTc1ZVdEQW5BeHNNeVpJY3hwNGZyMSIsImZpbGVuYW1lIjoiMmcwS1NuaGVNb2ZzU2d1SkJKc2YubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "4ef2c624acf6cfe6a51105f9c15c1c64a1ca39bb07bfd7e411be69aabce152ff",
          "voice_id": "BWN0mOtkGHghA3CYFzFK",
          "date_unix": 1761329327,
          "name": "Danyu Zhao - Clear, Calm and Pleasant",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "cute",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A calm and pleasant Chinese male voice with a clear tone and friendly presence. Suitable for lifestyle content, conversational narration, product voiceovers, and character dialogues with a gentle and engaging delivery",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3",
          "usage_character_count_1y": 9290788,
          "usage_character_count_7d": 329360,
          "play_api_usage_character_count_1y": 25574501,
          "cloned_by_count": 8700,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/fu2LfBnTx4bUl3m39eC5X07W76w1/voices/BWN0mOtkGHghA3CYFzFK/zSqqkKsBASRwe6uZSbGR.mp3"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_multilingual_v2",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BWN0mOtkGHghA3CYFzFK/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "8e41fefaeea07b7beaaa6f205ff34ed032e81d698970d9fd0c97ae78c4e11f97",
          "voice_id": "cwzmKSYMCC9Aym1ymCnt",
          "date_unix": 1780415381,
          "name": "Mr. Chen - Trustworthy Chinese Narrator",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A trustworthy and calm Mandarin Chinese male voice. Perfect for financial commentary, documentaries, business presentations, educational content, audiobooks,  narration, and professional AI voice applications.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3",
          "usage_character_count_1y": 8510985,
          "usage_character_count_7d": 390008,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 6823,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/b30a35c622dd4437a67a17967ba4298e/voices/cwzmKSYMCC9Aym1ymCnt/c491886d-2abe-4e6f-89e8-9c8d8cec2d89.mp3"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-dubrovnik",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-dubrovnik",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "bg",
              "model_id": "eleven_multilingual_v2",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "bg",
              "model_id": "eleven_flash_v2_5",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_flash_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-gotland",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "sv",
              "model_id": "eleven_flash_v2_5",
              "accent": "sv-standard",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "sv-standard",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/cwzmKSYMCC9Aym1ymCnt/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": true,
          "is_bookmarked": false
        },
        {
          "public_owner_id": "1f8090e7b6ab3a9d53a4cf0acd183d1ab6d74e79bac9901d959137f168defef2",
          "voice_id": "brChkoggsUHF1stW6omH",
          "date_unix": 1775772319,
          "name": "Ethan Zhang - Deep, Seductive and Smooth",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A deep, smooth, and seductive male voice with a magnetic tone. Perfect for storytelling, romantic content, audiobooks, and cinematic narration. Warm, confident, and emotionally engaging.\n",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 8001716,
          "usage_character_count_7d": 326554,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 15016,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI5YWE4NTU0NjE0NGM0MTgyYTdjYWYxMzhiYTQwOTVlZiIsImZpbGVuYW1lIjoidUQySkIzbGpJVXRUQkJ5ZzBxancubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "bg",
              "model_id": "eleven_turbo_v2_5",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_multilingual_v2",
              "accent": "da-zealandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_multilingual_v2",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ta",
              "model_id": "eleven_flash_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "sv",
              "model_id": "eleven_flash_v2_5",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/brChkoggsUHF1stW6omH/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "fd0ca8b2b02f48e9f96d93a5aa26ff5732c4b8c44d0461cdaf1921487d9b0821",
          "voice_id": "lt7GBaCoAHWbT7JSZ5Xs",
          "date_unix": 1784485984,
          "name": "Xinghe Jiang - Magnetic Conversational",
          "accent": "standard",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "conversational",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "My voice is warm, natural, and magnetic, perfect for relaxed conversations, podcasts, videos, and AI assistants.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 6783619,
          "usage_character_count_7d": 690372,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 4948,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiIyY2M1ZjVmMTFhYzY0M2U3ODJjNmVlY2ViMTNmMzUzZiIsImZpbGVuYW1lIjoiTzIwaVMwTlNkUlEyQnBoWFRYNG8ubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "id",
              "model_id": "eleven_turbo_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_flash_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hu",
              "model_id": "eleven_flash_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-dubrovnik",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-dubrovnik",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-milanese",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-milanese",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-milanese",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/lt7GBaCoAHWbT7JSZ5Xs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "a88ae5146bec8305070e1c0afc7f909caa0f21a1cfd4b0170506789b2e550dc3",
          "voice_id": "R55vTH9XmVSyAcM6YvtV",
          "date_unix": 1760165365,
          "name": "Yao Yuan Wu - Warm, Sweet and Friendly",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A friendly and approachable young male voice with a gentle, charming Taiwanese accent. Its warm mid-bass is perfect for conversational podcasts, engaging YouTube voiceovers, and authentic dialogue. This voice, like listening to a trusted friend, creates a sense of familiarity and a deep connection with your audience.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3",
          "usage_character_count_1y": 5965125,
          "usage_character_count_7d": 236323,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5733,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/Tx9G0iZwRqa73wUCUuWX3kFoJ2I2/voices/R55vTH9XmVSyAcM6YvtV/Gz0n3eMNN70YvMVupsSq.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "551283afef7016ff73ee636df7afb4c8d5518647ee0548bcca026acf6ef38519",
          "voice_id": "OjkyUe8dIihIFvOisuvM",
          "date_unix": 1753569789,
          "name": "Tung Wong - Young, Funny and Friendly",
          "accent": "hong kong cantonese",
          "gender": "male",
          "age": "young",
          "descriptive": "casual",
          "use_case": "social_media",
          "category": "professional",
          "language": "zh",
          "locale": null,
          "description": "A young, conversational and humorous male voice with a subtle Hong Kong accent. Perfect for content creators looking for a friendly and authentic tone with just the right touch of humor and regional charm.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 5223295,
          "usage_character_count_7d": 138066,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 9199,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiQ0lGeGIxTkRQM2RqRG9XMHQ0NVNxVUNOdDEzMyIsImZpbGVuYW1lIjoiQWlCY21GZ2V0NnRJaWdEWUZMMGEubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "id",
              "model_id": "eleven_flash_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_turbo_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-german",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/OjkyUe8dIihIFvOisuvM/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "0e6727b7d53597ce7629413dbe71eba6c1e077ca3309013a30a82e9d5230317b",
          "voice_id": "EttSxNTvxX50EUdRPQQl",
          "date_unix": 1775857861,
          "name": "Jordan Li - Calm, Natural and Grounded",
          "accent": "standard",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "formal",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A calm and natural voice with a grounded tone. Warm, steady, and easy to trust — ideal for everyday narration and clear communication.\n",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3",
          "usage_character_count_1y": 5214465,
          "usage_character_count_7d": 65021,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 2462,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3faea699cc304ae18d4da92099aa0a78/voices/EttSxNTvxX50EUdRPQQl/WMq3COAjAKZMrvalwoBB.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "d8b6fc5995c13b3a1a4fb99dcf9966acbf007e38818bddab7682a1458577d1dd",
          "voice_id": "auoHciLZJwKTwYUoRTYz",
          "date_unix": 1759833388,
          "name": "Neil Chuang - Deep, Trustworthy and Rich",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Originating from Taiwan, my voice carries a rich, low-toned resonance that instantly puts listeners at ease and builds trust. Perfect for product narrations, sales calls, and any setting where a confident and calming voice makes a lasting impression.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D",
          "usage_character_count_1y": 5168658,
          "usage_character_count_7d": 143684,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 9413,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/auoHciLZJwKTwYUoRTYz/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYkJBWXlSWU15YWZQU3Jia3RveXZJYWhQdjZYMiIsImZpbGVuYW1lIjoiNDdiZDVjN2UtZjFkNy00OGFlLTg1NDMtNmM1ZTE4NjEwZTY1Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "438920bc57d417234cc9575862c897f340b76c56c2596e624ae92f9894348bc9",
          "voice_id": "D9bZgM9Er0PhIxuW9Jqa",
          "date_unix": 1748877262,
          "name": "Xin - Low, Slow and Smooth",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "casual",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Chinese Mandarin male voice. Good for conversation.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3",
          "usage_character_count_1y": 5079865,
          "usage_character_count_7d": 111110,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 7986,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/wklEXeIf8AMcUoz2Vg6buhivHvg1/voices/D9bZgM9Er0PhIxuW9Jqa/c04a7b80-ebb3-4ef1-8099-b9c1e1d1537e.mp3"
            }
          ],
          "notice_period": 180,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "2b639961b8881065ef148f39374c2543923ea7598a67f0ad7a5b326eff45a09d",
          "voice_id": "4aW8bNY2tSD8eaHmuXZ0",
          "date_unix": 1771563255,
          "name": "Chen - 23 years old Male",
          "accent": "taiwan mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "crisp",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Refreshing Taiwan Mandarin. Former band Vocal and Professional Voice Trainer.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D",
          "usage_character_count_1y": 4422485,
          "usage_character_count_7d": 165048,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5833,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4aW8bNY2tSD8eaHmuXZ0/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJiNGFiYjJkZTI4NWM0NTczOWRhODFmNmRlZWE1YzcwNSIsImZpbGVuYW1lIjoiNDA3ZTU1ZDctZmRlYi00YzJiLTg0N2QtNjViZGIzN2VkODVlLm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "ad2273ea41c989cb52eba0a9f9eeb40260f159286d4cf6824985dd5fb2c0de11",
          "voice_id": "2I36mEahS1u7ZnTKUoaB",
          "date_unix": 1767785878,
          "name": "Lao Dao - Beijing Anchor",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Standard Mandarin speaker from Beijing, China. Features a professional broadcast-quality tone with clear articulation and neutral pronunciation. Perfect for news narration, corporate presentations, and professional AI assistants.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 4339680,
          "usage_character_count_7d": 272783,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5311,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/2I36mEahS1u7ZnTKUoaB/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoic01iT3QxTHVLT2FyRlM4SDF2aXlRcTVMVFNtMSIsImZpbGVuYW1lIjoiMEkxcVE4Sm0yc29yMWZBVWNpNmQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            }
          ],
          "notice_period": 180,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "943ab2ecbad7fed2d27e7379a408180da0278ac546ae812114f13837dd7810cd",
          "voice_id": "bZtjnyJAFD0Cp3lfNG5g",
          "date_unix": 1781701747,
          "name": "Lan Chen - Relaxed University Lecturer",
          "accent": "beijing mandarin",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "informative_educational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "My voice is a relaxed and conversational university lecturer voice designed for educational content, online courses, and clear academic explanations. It has a calm, natural, and slightly informal tone that makes complex topics easier to understand.\n",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3",
          "usage_character_count_1y": 3965646,
          "usage_character_count_7d": 628851,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 3246,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/3bdf4d928dc8459693ddbd849b692644/voices/bZtjnyJAFD0Cp3lfNG5g/F5W3pw0BBdXHabAjl3i1.mp3"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-cypriot",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-argentine",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-australian",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-australian",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/bZtjnyJAFD0Cp3lfNG5g/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "27bec9f8dcc405464adf698c56a5fdcd44a7acc37f09b1c826d1c492f29a12c4",
          "voice_id": "WkcRFJo38X9XEP8kGExm",
          "date_unix": 1760205677,
          "name": "Vincent - Clear, Brisk and Mature",
          "accent": "standard",
          "gender": "male",
          "age": "middle_aged",
          "descriptive": "professional",
          "use_case": "informative_educational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Hello! I am a professional voice actor. My AI voice was recorded in-studio with a neutral Chinese accent and in a \"no nonsense\" tone. I hope my clear, brisk and mature voice can cater to your multi-purpose needs!",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3",
          "usage_character_count_1y": 3922022,
          "usage_character_count_7d": 153051,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5468,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/R3OxYUSwHubkshChzZpQeOV5MAV2/voices/WkcRFJo38X9XEP8kGExm/UwwDpPyzMkqWsF0KKb0t.mp3"
            }
          ],
          "notice_period": null,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "0c3b338bc63ba734c8ea5c8539d6a918764e3b4fc2d793abf626a1f5415f9348",
          "voice_id": "UFDAUkGzdLAEJlINT3Fx",
          "date_unix": 1777088108,
          "name": "Lin - Warm, Friendly & Conversational ",
          "accent": "standard",
          "gender": "male",
          "age": "young",
          "descriptive": "calm",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A warm, natural Mandarin Chinese male voice built for real-time conversational AI. Clean articulation, balanced pace, and a friendly professional tone that works equally well for customer support agents, sales assistants, and bilingual enterprise use cases. Also speaks English with a light, authentic accent.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3",
          "usage_character_count_1y": 3921510,
          "usage_character_count_7d": 395307,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 3635,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/83345403a39e4067b8e88cba9eef6e2a/voices/UFDAUkGzdLAEJlINT3Fx/cdb4fd52-fbe3-4a50-a492-cfe16add24e6.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        }
      ],
      "has_more": true,
      "total_count": 2043,
      "last_sort_id": null
    }
  }
}
```

## 2026-11-14T12:55:11.483+00:00 — elevenlabs / GET /v1/shared-voices — request

```json
{
  "request_id": "7684a7bf074a4482b6214a62cd3974a7",
  "provider": "elevenlabs",
  "operation": "GET /v1/shared-voices",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 41584,
  "request_fingerprint": "01350cd8f786f7ced4275c7902f82951c065af4d8f290b4fe79335dc7c13f66f",
  "time": "2026-11-14T12:55:11.483+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/shared-voices?language=zh&gender=female&page_size=30&sort=usage_character_count_1y"
  }
}
```

## 2026-11-14T12:55:16.375+00:00 — elevenlabs / GET /v1/shared-voices — result

```json
{
  "request_id": "7684a7bf074a4482b6214a62cd3974a7",
  "provider": "elevenlabs",
  "operation": "GET /v1/shared-voices",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 41584,
  "request_fingerprint": "01350cd8f786f7ced4275c7902f82951c065af4d8f290b4fe79335dc7c13f66f",
  "time": "2026-11-14T12:55:16.375+00:00",
  "event": "result",
  "elapsed_s": 4.875,
  "response": {
    "http_status": 200,
    "body": {
      "voices": [
        {
          "public_owner_id": "649d5d7a8d7cda374f337b08fe37fe9066686b8c337c4e357fb5f15ff9b699f9",
          "voice_id": "9lHjugDhwqoxA5MhX0az",
          "date_unix": 1748354146,
          "name": "Anna Su - Casual, Friendly and Bright",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "casual",
          "use_case": "social_media",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A youthful and bright Chinese female voice with a soft, friendly tone — warm, conversational, and effortlessly engaging, like a friend catching up with you over coffee.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3",
          "usage_character_count_1y": 168004076,
          "usage_character_count_7d": 4794335,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 51927,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/55SoO0ERY953JPIuC271.mp3"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "hi-IN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/3c730713-89bb-4038-8cdf-97a293d5c6b3.mp3"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "peninsular",
              "locale": "es-ES",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/a303d78e-b3cc-460b-819d-7a7907965be3.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/700409da-83a2-4fd9-a969-d63aad6a18de.mp3"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "de-DE",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/3e76edd8-97db-4fc1-b1e7-8107684ef1c2.mp3"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "hu-HU",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/dbc2af92-9a96-4136-bfff-6cb8e616ce24.mp3"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "tr-TR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/911e9714-5c0a-4b10-9efb-9c576a7045b1.mp3"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "ko-KR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/a722c3f8-830f-46a0-b6d0-6189be7ae43d.mp3"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "northern",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/504cf969-d089-41ec-ad4d-d9e03e97dc43.mp3"
            },
            {
              "language": "sk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "sk-SK",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/c2087f25-b1a7-4904-89af-23b85f5e1c5b.mp3"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "ro-RO",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/79a97a3d-6aa1-42aa-8e24-8e1f1f92f3ef.mp3"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "hr-HR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/85ae1803-764d-41ff-a6f0-5e2ff2cdc6e2.mp3"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "pt-BR",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/a5a6a62a-c2db-4300-96a6-dfde2106bc12.mp3"
            },
            {
              "language": "sv",
              "model_id": "eleven_turbo_v2_5",
              "accent": "central",
              "locale": "sv-SE",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/14b291f3-bb02-412e-a942-c7a5542f68d1.mp3"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "en-US",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/9fbfa1bf-9e62-48ad-91a5-2c14fd54a6f7.mp3"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "southern",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/b43f6f14-7e80-4fdb-b615-1dee962788f2.mp3"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "es-ES",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/3d90fb0b-37f9-42f0-a486-45cfc2d47f95.mp3"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "it-IT",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/eed17385-1519-4a08-9fad-354ea162902e.mp3"
            },
            {
              "language": "da",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "da-DK",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/iWxuY2XaYrWRf6GQxIUY2M0J0gJ3/voices/9lHjugDhwqoxA5MhX0az/01cb6849-34fd-4305-a6a3-6000458bd8d1.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "3e76152f62e469dfef7259244d6e4a6c4bb9662cae01fd97c52cfde8f915bf32",
          "voice_id": "ByhETIclHirOlWnWKhHc",
          "date_unix": 1713537727,
          "name": "Shan Shan - Young Energetic Female",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "calm",
          "use_case": "social_media",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A youthful Chinese female voice with lively energy. Suitable for narrating stories and creating content for social media videos. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3",
          "usage_character_count_1y": 122640260,
          "usage_character_count_7d": 1421447,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 24148,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/ByhETIclHirOlWnWKhHc/WueuyXkB5LAjxrfqv4nL.mp3"
            },
            {
              "language": "hu",
              "model_id": "eleven_flash_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_multilingual_v2",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_flash_v2_5",
              "accent": "da-copenhagen",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ByhETIclHirOlWnWKhHc/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 90,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "2df33570a4561062869fd105107b8d8409306fbe12788c2e2b11693180596657",
          "voice_id": "hkfHEbBvdQFNX4uWHqRF",
          "date_unix": 1725586281,
          "name": "Stacy - Young, Sweet and Cute",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "pleasant",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Young cute Taiwanese Mandarin female voice. Works well for Narrations & Storytelling.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3",
          "usage_character_count_1y": 53279790,
          "usage_character_count_7d": 949038,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 51387,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/caa5a1882b534d379d7d1037f8cd2248/voices/hkfHEbBvdQFNX4uWHqRF/n5W0eNZRtazdqGAfoBDR.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "2e514ccc44c5906fa3fb4c0fc516255c8cc3eb3a6bebd2311c442b6ac5c98c74",
          "voice_id": "BqljjWyTnrioXPCNkCd4",
          "date_unix": 1763014775,
          "name": "Stella Gu - Cold, Indifferent and Calm",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "serious",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A cold, apathetic female voice with a calm, distant tone. Minimal emotion, clear delivery, and a quietly detached presence.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 27044119,
          "usage_character_count_7d": 586583,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 10527,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiWmhOTkFOUmNqSmZGUmdLckZxRFhyZkVQcVFBMyIsImZpbGVuYW1lIjoiVDZ0dFV3V3k1WG85NmplNlo1ZncubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "hu",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hu-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Imh1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BqljjWyTnrioXPCNkCd4/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "649d5d7a8d7cda374f337b08fe37fe9066686b8c337c4e357fb5f15ff9b699f9",
          "voice_id": "r6qgCCGI7RWKXCagm158",
          "date_unix": 1762140498,
          "name": "Anna Su - Trustworthy, Clear and Natural",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "neutral",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Perfect for YouTube videos, documentaries, and informative projects that require a clear and natural delivery.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 26689469,
          "usage_character_count_7d": 1104842,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 21558,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiaVd4dVkyWGFZcldSZjZHUXhJVVkyTTBKMGdKMyIsImZpbGVuYW1lIjoiajBTcDZUcTBOanAzOEh4Q0ZBbVkubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "id",
              "model_id": "eleven_flash_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_turbo_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-oslo",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-oslo",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-european",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/r6qgCCGI7RWKXCagm158/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "afc66099a72ea525a9d24fba23864a1fa9189915cd563c1dd2eebff3ec474f9d",
          "voice_id": "APSIkVZudNbPAwyPoeVO",
          "date_unix": 1772335005,
          "name": "Sage - Soothing & Gentle",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A warm, soothing female narrative voice. Calm, grounded, and gently intimate. Perfect for psychology, neuroscience, emotional wellness, meditation, self-help, feminist narratives, and romantic storytelling.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D",
          "usage_character_count_1y": 22296468,
          "usage_character_count_7d": 1077689,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 12975,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/APSIkVZudNbPAwyPoeVO/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiJkOGM0ZThmYmZhM2U0ZTFkYTkwZGUwMzFmMmZmYzI0NCIsImZpbGVuYW1lIjoiYTBkM2JiMjMtNDM3My00MWUyLTk1YTctMzJjMzVjOGM3OGM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "01477f5cc1b57546ca379fb0b2c4bbb8bcb3fbbac4fa05b56399bda42087877d",
          "voice_id": "FjfxJryh105iTLL4ktHB",
          "date_unix": 1723317533,
          "name": "Liang - Calm, Natural and Young",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "casual",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A youthful Chinese female voice with a calm tone. Suitable for narrating stories and creating content for social media videos.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3",
          "usage_character_count_1y": 19274853,
          "usage_character_count_7d": 236623,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 4991,
          "rate": 3.0,
          "fiat_rate": 0.25,
          "free_users_allowed": false,
          "live_moderation_enabled": true,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lR7zG0SGCEdZiJWSCYHUCbDntpE3/voices/FjfxJryh105iTLL4ktHB/oFBl7C5OfnlqwKT3XRw9.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "c28f2a2e32fef86df4799f59c881359a47697ae13e78243a2d208211123d0cd7",
          "voice_id": "JZLpE3AGwpKYZI2X65hN",
          "date_unix": 1762978439,
          "name": "Mingyao Ye - Sad and Broken Hearted",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "mature",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A deeply emotional female voice filled with endless sadness & a broken heart. Her tone is gentle, trembling, and beautifully sorrowful — like a whisper from a soul that has loved and lost. Perfect for emotional narration, tragic monologues, or heartfelt storytelling.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 18788113,
          "usage_character_count_7d": 353982,
          "play_api_usage_character_count_1y": 76082039,
          "cloned_by_count": 20158,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/JZLpE3AGwpKYZI2X65hN/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiYUhMd2o5WmtLb1dnUHluMERRbmhmZkF5ZXphMiIsImZpbGVuYW1lIjoiNDJ2ZkFFZmwxUEdoZVFXajBEZkMubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "5cb134719206cde8d28794b08248de419f153cc7bf85537fc46b0d542d947c1c",
          "voice_id": "kGjJqO6wdwRN9iJsoeIC",
          "date_unix": 1750220214,
          "name": "Yui - Delicate, Graceful and Soothing",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "cute",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A delicate, graceful, and soothing voice of a Young Taiwanese Female, perfect for bedtime stories, guided meditations, easing anxiety, promoting sleep, and moments of calm",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3",
          "usage_character_count_1y": 17616155,
          "usage_character_count_7d": 462775,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 15450,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/ldY30W195LNeRXj9WvD2TWSQ5QK2/voices/kGjJqO6wdwRN9iJsoeIC/wCkvneExVQKPTkxvKRGX.mp3"
            }
          ],
          "notice_period": 30,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "2c572ce430114e243fe4f6bc3ad191c2e9dfe3d4986d87b86c65302f9a5f9922",
          "voice_id": "Ca5bKgudqKJzq8YRFoAz",
          "date_unix": 1715248299,
          "name": "Coco Li - Calm, Young and Trustworthy",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "chill",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A young Shanghainese female Chinese voice with a slight rasp in the voice. perfect for story narration and simple advertisement announcement.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3",
          "usage_character_count_1y": 16997781,
          "usage_character_count_7d": 413628,
          "play_api_usage_character_count_1y": 10493,
          "cloned_by_count": 15670,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": true,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/custom/voices/Ca5bKgudqKJzq8YRFoAz/K4ccfm1YkLq6T1VJrk2U.mp3"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-malaysian",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_turbo_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "bg",
              "model_id": "eleven_flash_v2_5",
              "accent": "bg-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImJnIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "sv",
              "model_id": "eleven_multilingual_v2",
              "accent": "sv-stockholm",
              "locale": "sv-SE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InN2IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "uk-kiev",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-kiev",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-american",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_flash_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "en",
              "model_id": "eleven_turbo_v2_5",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Ca5bKgudqKJzq8YRFoAz/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "5444bf6c66fb28ca3e2cd3e0a43208b104ed39f611c05381ee13d556e9544c32",
          "voice_id": "1AKkSX7KMPHIWuz76m0n",
          "date_unix": 1775101939,
          "name": "Tiffy - Taiwanese Bilingual Narrator",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "confident",
          "use_case": "informative_educational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Professional Taiwanese female voice with crystal-clear Mandarin and natural, fluent English. Warm, confident, and highly engaging — perfect for Shorts, educational tutorials, AI automation content, e-learning courses, podcasts, and faceless creator videos. Ideal for bilingual projects and Asian market content.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3",
          "usage_character_count_1y": 16069799,
          "usage_character_count_7d": 1388736,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 11365,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/d3e5c2466cec4438b7e6883f83cd1e67/voices/1AKkSX7KMPHIWuz76m0n/fidyWYIInrx9ciWWNXJg.mp3"
            }
          ],
          "notice_period": 30,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "df4fc9cd53f951eac8a085953ac38dab0b5db5cd13e1bf51164bbfcc5f8e6c1e",
          "voice_id": "tOuLUAIdXShmWH7PEUrU",
          "date_unix": 1734781492,
          "name": "Julia - Young, Smooth and Neutral",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "confident",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Young at heart and thriving in the 30s club, this female voice brings a smooth, neutral accent that's perfect for a wide range of projects in both English and Chinese Whether you're tuning in to a podcast, learning from an online course, diving into an audiobook, or scrolling through social media, this voice delivers clarity, warmth, and just the right touch of charm. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3",
          "usage_character_count_1y": 15204312,
          "usage_character_count_7d": 556938,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 14395,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/lyCyP7PysDfJntM6nncwX4S69pn2/voices/tOuLUAIdXShmWH7PEUrU/cLRFoBrJT4slo9iXmsFk.mp3"
            }
          ],
          "notice_period": 365,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "39d845c0359a1935ac0ba8ab60e695551a453bd4717d51c1a2fc3e088810920a",
          "voice_id": "4NQthjVhIGGVfL3Si000",
          "date_unix": 1772669570,
          "name": "Chen Mandarin Chinese",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "casual",
          "use_case": "social_media",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Native Mandarin Chinese voice with a gentle Taiwanese accent. Clear, warm, and natural delivery — perfect for daily dialogue, storytelling, audiobooks, narration, podcasts, and lifestyle content. My tone is conversational, friendly, and emotionally expressive while maintaining clarity and professionalism.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3",
          "usage_character_count_1y": 13106334,
          "usage_character_count_7d": 436301,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 13801,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2d6ac8c7f1724afc98e7baffe264d777/voices/4NQthjVhIGGVfL3Si000/831ad48d-692b-46bd-b96a-f0504030212d.mp3"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_flash_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-argentine",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-limburgish",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4NQthjVhIGGVfL3Si000/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            }
          ],
          "notice_period": 180,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "8e3c8e4ea2c52fd76e01856e15393b1a5137ae62b1c16d0bbbba6fb421f1cc9a",
          "voice_id": "kAIqZ7fZv234ClKXwzDx",
          "date_unix": 1762827947,
          "name": "Susan - Clear and Calm Storyteller",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "neutral",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Can be used to generate English content. Sounds very clean and natural as well. A native Mandarin voice crafted for clarity, authenticity, and connection. Her tone is warm yet professional—perfect for narrations that need to sound both human and engaging. With balanced pacing and subtle emotional expression, this voice brings out the meaning and rhythm of every sentence, whether it’s a heartfelt story, a brand campaign, or an educational video.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3",
          "usage_character_count_1y": 12645366,
          "usage_character_count_7d": 487467,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 8655,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/utycMEbn19cDZEwvaFQbhHC8cbk2/voices/kAIqZ7fZv234ClKXwzDx/77829702-c646-46ec-9776-222668375af8.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "5ec7715ee5949825dc0959dee2f1f30693d4a5d1ae49c50c078270f5d886caf7",
          "voice_id": "9DMBSOAnMDPiFAsz1ZGK",
          "date_unix": 1771197934,
          "name": "Xiaoxi - Neutral, Young and Friendly  ",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "cute",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Xiaoxi is a Chinese American with a friendly, approachable voice. Perfect for podcasts and voice-overs. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3",
          "usage_character_count_1y": 9769332,
          "usage_character_count_7d": 1088266,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 8273,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/70c524fabc6a45dbab4e22f7c1a5c05d/voices/9DMBSOAnMDPiFAsz1ZGK/H7oKA2Xl2PJm2NVWyk14.mp3"
            }
          ],
          "notice_period": 180,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "4877d28f5fd1f9399f1543777b7be1a4dd595da3c76d62c716be431835368389",
          "voice_id": "Iqi0ix5WGtiSXX9VDZB4",
          "date_unix": 1761270572,
          "name": "Helen Sun - Smooth, Clear and Mature",
          "accent": "standard",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "formal",
          "use_case": "informative_educational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Middle-aged female voice. Great for Informative content.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D",
          "usage_character_count_1y": 9242405,
          "usage_character_count_7d": 918537,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5836,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/Iqi0ix5WGtiSXX9VDZB4/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ1c2VyX2lkIjoiRzhIRnpzMXRJT2hFa3hJM0FqNDRUUzVEVWZyMSIsImZpbGVuYW1lIjoiZDA1ZGE0NWUtZWI0Zi00ZDk1LTlhODUtMWRlNzQzZTk0MzM4Lm1wMyIsInRpbWVzdGFtcCI6MTc5NDY1NzYwMDAwMDAwMH0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "3b0be75e02a108226547718c73784f0a848b7478a1aca10a19a861634cabb8a8",
          "voice_id": "NIqnuIdrAT3LLSSxN05L",
          "date_unix": 1755891912,
          "name": "Chihiro Yoko - Clear, Soothing and Sweet",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "casual",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A soothing and even voice, like the girl next door.\nSweet, clear and professioanl East Asian female voice.\nSmooth and expressive, ideal for storytelling, audiobooks and character voices.\nFriendly, polished and versatile – a voice that adapts easily from formal presentations to casual conversations.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3",
          "usage_character_count_1y": 8427188,
          "usage_character_count_7d": 387814,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 7160,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/HuCnBtMSFaTypirYF938vsnGIBE3/voices/NIqnuIdrAT3LLSSxN05L/W5NCBxuDIPvmx0SCNvHb.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "39994b5a91bfa10b3ed33299692cff7fdb869b4e09d7792d011a521edc595668",
          "voice_id": "n4xdXKggn5lFcXFYE4TA",
          "date_unix": 1760243833,
          "name": "Chloe Chan - Young, Fast and Energetic",
          "accent": "hong kong cantonese",
          "gender": "female",
          "age": "young",
          "descriptive": "casual",
          "use_case": "entertainment_tv",
          "category": "professional",
          "language": "zh",
          "locale": null,
          "description": "A Hong Kong female with a Cantonese mother tongue.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3",
          "usage_character_count_1y": 8129431,
          "usage_character_count_7d": 499621,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 6747,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/WF8D5xsr4UXPEoEAUXBrEYwvG5m1/voices/n4xdXKggn5lFcXFYE4TA/nrqRRy0OoUfGzbhnrSdP.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "ce30ef7cef1c7cb0e78bfb45dfabfb0c52f4c927f3d77274e39d85be35f9d425",
          "voice_id": "YxbjaPemDJV2xlfvkiIG",
          "date_unix": 1764657186,
          "name": "Yun - Elegant, Sweet and Gentle",
          "accent": "standard",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "An elegant Chinese woman, sweet, chill and gentle. ",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3",
          "usage_character_count_1y": 7783476,
          "usage_character_count_7d": 137025,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 7084,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/KID6bP63XXPAUsepL8rvencoBQ43/voices/YxbjaPemDJV2xlfvkiIG/eac85287-2f97-44c8-9c5c-928d15ecf30d.mp3"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-mexican",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "en",
              "model_id": "eleven_multilingual_v2",
              "accent": "en-british",
              "locale": "en-US",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVuIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/YxbjaPemDJV2xlfvkiIG/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "3ee364fd03ba63cb56ba9d103a65902457c1fc835e4093ad6cf8e1bcc807357b",
          "voice_id": "Z8Aisvg1z70p27kGvkZZ",
          "date_unix": 1754253688,
          "name": "Ling - Steady, Calm and Grounded",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "informative_educational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "Ling is a grounded and steady female voice from Taiwan, known for her calm tone, natural pacing, and emotional depth. Her voice carries a quiet strength—warm, reassuring, and full of clarity—making it ideal for educational content, guided narration, personal development, and reflective storytelling. With a gentle but firm delivery, Ling invites listeners to slow down, stay present, and absorb each message with trust and ease.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3",
          "usage_character_count_1y": 7053418,
          "usage_character_count_7d": 565678,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 6867,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/QSwtaUNyT8TthyKKrkMIXL2hGrI2/voices/Z8Aisvg1z70p27kGvkZZ/b7cb87fa-deea-4daf-91a0-abd9e4785744.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "c61cb21f8f8d9a2a2f6cdc8d57fc0c431a2664f4d093d3a193d1e371ba9694c9",
          "voice_id": "gU2KtIu9OZWy3KqiqNj6",
          "date_unix": 1744974337,
          "name": "Lee Ting Ting - Young, Gentle and Sweet",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "chill",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A young woman from Taiwan with a gentle and sweet voice.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3",
          "usage_character_count_1y": 6545796,
          "usage_character_count_7d": 396169,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 10625,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/1Wi7ZTcHCLVjU7jHGVJ7y5jZVIw1/voices/gU2KtIu9OZWy3KqiqNj6/lyK68Sk7deNUMy7K3vC1.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "f50ffe09ca75e10acd23a49e8c34e7a13d4dbf3f806ce7bedcec0380f6eb5fb8",
          "voice_id": "V3z1DARAbkkTVEx5lmEl",
          "date_unix": 1781335422,
          "name": "Jill - Warm, Natural & Trustworthy",
          "accent": "standard",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "pleasant",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Warm and professional Mandarin Chinese female voice with a natural, trustworthy, and engaging delivery. Clear, calm, and easy to listen to, making it ideal for narration, explainers, social media content, documentaries, and professional voiceovers.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3",
          "usage_character_count_1y": 5983068,
          "usage_character_count_7d": 616620,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 4186,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1eee8a7f69dd49dcb4c0c853e14a519e/voices/V3z1DARAbkkTVEx5lmEl/rfDz7crFTvZNlkygW0Du.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "cebf737540219c06da0e56d052ce9a91966916e4f25c0dca242891712ea2a2c7",
          "voice_id": "xDISamJf8LV5rG5A2te1",
          "date_unix": 1771479667,
          "name": "Aki | Deep & Suspenseful",
          "accent": "hong kong cantonese",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "deep",
          "use_case": "characters_animation",
          "category": "professional",
          "language": "zh",
          "locale": null,
          "description": "A unique, deep female voice built for suspense.\nVibe: Mature, dark, slightly snarky/sassy, and highly engaging.\nSpecialty: Masters rhetorical questions and dramatic pauses.\nBest for: True Crime podcasts, thriller audiobooks, and edgy documentary narrations.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3",
          "usage_character_count_1y": 5321361,
          "usage_character_count_7d": 417475,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 3691,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "hong kong cantonese",
              "locale": null,
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/user_4701kgcpep67efwtvjz7k3fnyq27/voices/xDISamJf8LV5rG5A2te1/IPvm3vBnExAEwzBsS5p0.mp3"
            }
          ],
          "notice_period": 365,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "201daba080556fd9c0f46c0287ca5fd78d74bae08ac753b949dc0cf3268f237d",
          "voice_id": "GgmlugwQ4LYXBbEXENWm",
          "date_unix": 1728434572,
          "name": "Maya - Young, Calm and Smooth",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Young female with a calming tone, perfect for creating content and videos.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3",
          "usage_character_count_1y": 5061335,
          "usage_character_count_7d": 176591,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 3864,
          "rate": 3.0,
          "fiat_rate": 0.25,
          "free_users_allowed": false,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/14fd976ef500404fb08f6a9d18786c24/voices/GgmlugwQ4LYXBbEXENWm/AP0YhlW1zVxV5sXFTGF3.mp3"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_flash_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/GgmlugwQ4LYXBbEXENWm/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            }
          ],
          "notice_period": 365,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "0761ca268d5e14a5a888935315f7a6d8b44da84bd142cee2279676a86f7988d8",
          "voice_id": "5qr5FEpvZGzmVOPBS55W",
          "date_unix": 1771668495,
          "name": "Zi Yue - Pro Voice",
          "accent": "standard",
          "gender": "female",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "This is a gentle and delicate Chinese female voice with standard and natural pronunciation, a soft tone yet rich in subtle emotional layers. She excels particularly in narrative and dialogue scenarios, creating a warm, soothing, yet professional listening experience. It is ideal for various scenarios such as audiobooks, emotional radio programs, educational courses, corporate narration, meditation, and bedtime stories. \n\nHer clear enunciation and stable speaking speed prevent listener fatigue even after extended listening sessions, making her an ideal female voice choice that balances companionship and professionalism.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3",
          "usage_character_count_1y": 4871341,
          "usage_character_count_7d": 417835,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 5333,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "standard",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/2abed23fb05842d0a6255a15b78bf0eb/voices/5qr5FEpvZGzmVOPBS55W/811c9f6f-9083-4852-9e5f-378c592a32d5.mp3"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-northern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_turbo_v2_5",
              "accent": "da-jutlandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-standard",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5qr5FEpvZGzmVOPBS55W/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "e25c1104ed395865dbb681412be54dfe1fbb61ef71603296bcde6146a17b039a",
          "voice_id": "0Aj540a9UWvQPWdx9Zq4",
          "date_unix": 1749965702,
          "name": "Jane - Low, Calm and Slow",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "calm",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A woman with very low and calm voice in Taiwanese accent",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3",
          "usage_character_count_1y": 4273959,
          "usage_character_count_7d": 111799,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 7181,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/user/FQO0uAe1zIfirxyxjp4BRUl5ML13/voices/0Aj540a9UWvQPWdx9Zq4/3c665ef9-133e-4807-adc1-0e0ac33eecc4.mp3"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "e907cd3cc58a8522ae43b533dfb971f356bfdd257d43c5245c6e413f37c1dd84",
          "voice_id": "ggacvEjbmpoSuEinfFWs",
          "date_unix": 1777731882,
          "name": "Jackie - Calm Female Reflective Narration",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "calm",
          "use_case": "narrative_story",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "A young calm, reflective female voice. Thoughtful and slightly nostalgic delivery, with a low-toned, restrained quality, perfect for audiobook narration, meditation, documentaries, reflective monologues, and brand storytelling.",
          "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D",
          "usage_character_count_1y": 3965062,
          "usage_character_count_7d": 346738,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 1042,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": false,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/ggacvEjbmpoSuEinfFWs/previews/audio?payload=eyJ2b2ljZV9zb3VyY2UiOiJjdXN0b20iLCJ3b3Jrc3BhY2VfaWQiOiI2M2E4ZWEyZTZhMmQ0NTZlOWYxM2E0YmM0NGQyODJhOCIsImZpbGVuYW1lIjoiZWpwcWdlWmVmSDBYc2ZQQjdQRWQubXAzIiwidGltZXN0YW1wIjoxNzk0NjU3NjAwMDAwMDAwfQ%3D%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "124da371b8bd533d5848b3061cfcfcf69d83208413b10cfb3cf3377ef71314be",
          "voice_id": "4AfodMgwXps9oZFhHzoj",
          "date_unix": 1786355284,
          "name": "Yun - Prime Mandarin Broadcast Anchor",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "professional",
          "use_case": "narrative_story",
          "category": "high_quality",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "Female Mandarin voice. Professionally trained broadcaster, two decades of daily on-air news. Certified Putonghua Proficiency Test Level I Grade A — China's highest Mandarin grade. Standard Putonghua, broadcast diction, natural pacing for news, e-learning, corporate video, audiobooks, documentary narration, short-form video, IVR, and conversational AI.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3",
          "usage_character_count_1y": 3886999,
          "usage_character_count_7d": 379605,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 1546,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": false,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/9ed19418f10a472b8c8786915a78fb0a/voices/4AfodMgwXps9oZFhHzoj/R8xWDYjK88lFNTFqtaZq.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "zh-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InpoIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-rajasthani",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_flash_v2_5",
              "accent": "hi-awadhi",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "hi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "hi-awadhi",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "es-peninsular",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "es-latin-american",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_flash_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "tr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "tr-istanbul",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_flash_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "el",
              "model_id": "eleven_flash_v2_5",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_multilingual_v2",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_flash_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "hr",
              "model_id": "eleven_flash_v2_5",
              "accent": "hr-standard",
              "locale": "hr-HR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_flash_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "vi",
              "model_id": "eleven_turbo_v2_5",
              "accent": "vi-southern",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InZpIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ta",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ta-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/4AfodMgwXps9oZFhHzoj/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "af2e2cefdb699d43191b113f7afe70f104fd32f875cee9a8a2eb2e7618a7739c",
          "voice_id": "5eoK8NqMBsMdqUmImHNs",
          "date_unix": 1792171477,
          "name": "Yating Lin - Relaxed & Spontaneous",
          "accent": "beijing mandarin",
          "gender": "female",
          "age": "middle_aged",
          "descriptive": "chill",
          "use_case": "conversational",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-CN",
          "description": "My voice has a contemporary, conversational style with a smooth and effortless rhythm. I speak with clarity and subtle expression, keeping my delivery relaxed and spontaneous rather than overly polished. My voice works well for social media, lifestyle content, everyday conversations, and modern storytelling.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3",
          "usage_character_count_1y": 3370265,
          "usage_character_count_7d": 1070121,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 2158,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": true,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "test_m2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_multilingual_sts_v2",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "beijing mandarin",
              "locale": "cmn-CN",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/1d88e9de1edf4adcb6f96bd1a2d024d4/voices/5eoK8NqMBsMdqUmImHNs/8EQGFzsv1EJruIvGX7Ys.mp3"
            },
            {
              "language": "es",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "es",
              "model_id": "eleven_flash_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "es",
              "model_id": "eleven_turbo_v2_5",
              "accent": "other",
              "locale": "es-ES",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "id",
              "model_id": "eleven_flash_v2_5",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_multilingual_v2",
              "accent": "ms-malaysian",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ms",
              "model_id": "eleven_flash_v2_5",
              "accent": "ms-malaysian",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ms",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ms-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im1zIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_flash_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "uk",
              "model_id": "eleven_turbo_v2_5",
              "accent": "uk-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_flash_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "nl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_multilingual_v2",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "it",
              "model_id": "eleven_flash_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "it",
              "model_id": "eleven_turbo_v2_5",
              "accent": "it-standard",
              "locale": "it-IT",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Iml0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_flash_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "de",
              "model_id": "eleven_turbo_v2_5",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_multilingual_v2",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ko",
              "model_id": "eleven_flash_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "ko",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ko-seoul",
              "locale": "ko-KR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImtvIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_flash_v2_5",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_multilingual_v2",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pt",
              "model_id": "eleven_flash_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "pt",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pt-brazilian",
              "locale": "pt-BR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InB0IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_flash_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "fr",
              "model_id": "eleven_turbo_v2_5",
              "accent": "fr-standard",
              "locale": "fr-FR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImZyIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_turbo_v2_5",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_multilingual_v2",
              "accent": "no-sørlandsk",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "no",
              "model_id": "eleven_flash_v2_5",
              "accent": "no-oslo",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "no",
              "model_id": "eleven_turbo_v2_5",
              "accent": "no-oslo",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5vIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_flash_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fZmxhc2hfdjJfNSJ9"
            },
            {
              "language": "cs",
              "model_id": "eleven_turbo_v2_5",
              "accent": "cs-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImNzIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "da",
              "model_id": "eleven_turbo_v2_5",
              "accent": "da-zealandic",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRhIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_turbo_v2_5",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/5eoK8NqMBsMdqUmImHNs/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fdHVyYm9fdjJfNSJ9"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        },
        {
          "public_owner_id": "99d01d86686b10916e1b335a8e93aac7a4d7fed480ade722cd2847f0304d6a50",
          "voice_id": "BT0SH7Hb8NRPpT5xbCgg",
          "date_unix": 1784238593,
          "name": "Lulu - Cute Little Witch ",
          "accent": "taiwan mandarin",
          "gender": "female",
          "age": "young",
          "descriptive": "cute",
          "use_case": "characters_animation",
          "category": "professional",
          "language": "zh",
          "locale": "cmn-TW",
          "description": "A cute and playful little witch voice with a bright, energetic, anime-inspired tone. Perfect for anime, games, VTubers, visual novels, fantasy characters, magical girls, and storytelling. Capable of a wide emotional range including cheerful, mischievous, excited, shy, crying, angry, dramatic, and heartwarming performances.",
          "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3",
          "usage_character_count_1y": 3124441,
          "usage_character_count_7d": 322469,
          "play_api_usage_character_count_1y": 0,
          "cloned_by_count": 2778,
          "rate": 1.0,
          "fiat_rate": null,
          "free_users_allowed": false,
          "live_moderation_enabled": false,
          "featured": false,
          "verified_languages": [
            {
              "language": "zh",
              "model_id": "eleven_multilingual_v2",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_turbo_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v2_5_flash",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_flash_v2_5",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_eval",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_hq",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_post_trained",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "zh",
              "model_id": "eleven_v4_turbo_exp",
              "accent": "taiwan mandarin",
              "locale": "cmn-TW",
              "preview_url": "https://storage.googleapis.com/eleven-public-prod/database/workspace/451fb4b0fbd844bbb0c30fe416b6498e/voices/BT0SH7Hb8NRPpT5xbCgg/JMJTJG4vYXdZKcbYxLQv.mp3"
            },
            {
              "language": "id",
              "model_id": "eleven_multilingual_v2",
              "accent": "id-standard",
              "locale": "id-ID",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImlkIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "hi",
              "model_id": "eleven_multilingual_v2",
              "accent": "hi-bhojpuri",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImhpIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "el",
              "model_id": "eleven_multilingual_v2",
              "accent": "el-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImVsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "uk",
              "model_id": "eleven_multilingual_v2",
              "accent": "other",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InVrIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ro",
              "model_id": "eleven_multilingual_v2",
              "accent": "ro-standard",
              "locale": "ro-RO",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJvIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "pl",
              "model_id": "eleven_multilingual_v2",
              "accent": "pl-standard",
              "locale": "pl-PL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InBsIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ar",
              "model_id": "eleven_multilingual_v2",
              "accent": "ar-modern-standard",
              "locale": null,
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImFyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "ru",
              "model_id": "eleven_multilingual_v2",
              "accent": "ru-standard",
              "locale": "ru-RU",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InJ1IiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "tr",
              "model_id": "eleven_multilingual_v2",
              "accent": "tr-standard",
              "locale": "tr-TR",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6InRyIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "nl",
              "model_id": "eleven_multilingual_v2",
              "accent": "nl-standard",
              "locale": "nl-NL",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6Im5sIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            },
            {
              "language": "de",
              "model_id": "eleven_multilingual_v2",
              "accent": "de-standard",
              "locale": "de-DE",
              "preview_url": "https://api.us.elevenlabs.io/v1/voices/BT0SH7Hb8NRPpT5xbCgg/previews/audio?payload=eyJraW5kIjoidmVyaWZpZWRfbGFuZ3VhZ2UiLCJsYW5ndWFnZSI6ImRlIiwibW9kZWxfaWQiOiJlbGV2ZW5fbXVsdGlsaW5ndWFsX3YyIn0%3D"
            }
          ],
          "notice_period": 730,
          "instagram_username": null,
          "twitter_username": null,
          "youtube_username": null,
          "tiktok_username": null,
          "image_url": "",
          "is_added_by_user": false,
          "is_bookmarked": null
        }
      ],
      "has_more": true,
      "total_count": 732,
      "last_sort_id": null
    }
  }
}
```

## 2026-11-14T12:55:35.297+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "b728ea6d066a410cb75f85dccc5345d2",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\evan_zhao__eleven_multilingual_v2.mp3",
  "pid": 39212,
  "request_fingerprint": "65db94fb3924d749d96313228122260b977febba31f8f9cfe8dfbbdad806859b",
  "time": "2026-11-14T12:55:35.297+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/MI36FIkp9wRP7cpWKPTl?output_format=mp3_44100_128",
    "voice_id": "MI36FIkp9wRP7cpWKPTl",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_multilingual_v2"
    }
  }
}
```

## 2026-11-14T12:55:39.876+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "b728ea6d066a410cb75f85dccc5345d2",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\evan_zhao__eleven_multilingual_v2.mp3",
  "pid": 39212,
  "request_fingerprint": "65db94fb3924d749d96313228122260b977febba31f8f9cfe8dfbbdad806859b",
  "time": "2026-11-14T12:55:39.876+00:00",
  "event": "error",
  "elapsed_s": 4.563,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"db14fede99da67afd87afe7d875f3588\"}}"
}
```

## 2026-11-14T12:55:40.174+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "d9fda3063cc64fbea61c216e8cfc3ae6",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\mr_chen__eleven_multilingual_v2.mp3",
  "pid": 47636,
  "request_fingerprint": "02a4b30df8deed85d63c252af95dc89c763d351bd06f13ff9d123f6fa0539f0a",
  "time": "2026-11-14T12:55:40.174+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/cwzmKSYMCC9Aym1ymCnt?output_format=mp3_44100_128",
    "voice_id": "cwzmKSYMCC9Aym1ymCnt",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_multilingual_v2"
    }
  }
}
```

## 2026-11-14T12:55:48.713+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "d9fda3063cc64fbea61c216e8cfc3ae6",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\mr_chen__eleven_multilingual_v2.mp3",
  "pid": 47636,
  "request_fingerprint": "02a4b30df8deed85d63c252af95dc89c763d351bd06f13ff9d123f6fa0539f0a",
  "time": "2026-11-14T12:55:48.713+00:00",
  "event": "error",
  "elapsed_s": 8.516,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"dc36e7fe86f160093187d4ee3b2e4a00\"}}"
}
```

## 2026-11-14T12:55:49.121+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "af6d961d49bc47daae8a8b8eb80b9b87",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\lan_chen__eleven_multilingual_v2.mp3",
  "pid": 33932,
  "request_fingerprint": "fcc4896439c5cd2e49474c0c081e37346afce8b95aaad7e4c46a14c7361178da",
  "time": "2026-11-14T12:55:49.121+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/bZtjnyJAFD0Cp3lfNG5g?output_format=mp3_44100_128",
    "voice_id": "bZtjnyJAFD0Cp3lfNG5g",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_multilingual_v2"
    }
  }
}
```

## 2026-11-14T12:55:59.250+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "af6d961d49bc47daae8a8b8eb80b9b87",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\lan_chen__eleven_multilingual_v2.mp3",
  "pid": 33932,
  "request_fingerprint": "fcc4896439c5cd2e49474c0c081e37346afce8b95aaad7e4c46a14c7361178da",
  "time": "2026-11-14T12:55:59.250+00:00",
  "event": "error",
  "elapsed_s": 10.109,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"db61b0a32203ee855b4dc9ebcf61c49d\"}}"
}
```

## 2026-11-14T12:55:59.654+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "b8380fd31dd1416183e7dfff495c42f8",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\yun_anchor__eleven_multilingual_v2.mp3",
  "pid": 35700,
  "request_fingerprint": "b4300907616f807492533b0cdc60f0a2b474787fc45f947f47aca26eaf85f96b",
  "time": "2026-11-14T12:55:59.654+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/4AfodMgwXps9oZFhHzoj?output_format=mp3_44100_128",
    "voice_id": "4AfodMgwXps9oZFhHzoj",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_multilingual_v2"
    }
  }
}
```

## 2026-11-14T12:56:04.881+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "b8380fd31dd1416183e7dfff495c42f8",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\yun_anchor__eleven_multilingual_v2.mp3",
  "pid": 35700,
  "request_fingerprint": "b4300907616f807492533b0cdc60f0a2b474787fc45f947f47aca26eaf85f96b",
  "time": "2026-11-14T12:56:04.881+00:00",
  "event": "error",
  "elapsed_s": 5.203,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"742afbe4bffdd0a15bca64ed17d4de15\"}}"
}
```

## 2026-11-14T12:56:05.233+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "1543ce483ed943499e7a249fd90971e5",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\evan_zhao__eleven_v3.mp3",
  "pid": 41180,
  "request_fingerprint": "a7db6d3f0bbca9d17116d0cd2907441280667378fc31ec291401054df7e9518a",
  "time": "2026-11-14T12:56:05.233+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/MI36FIkp9wRP7cpWKPTl?output_format=mp3_44100_128",
    "voice_id": "MI36FIkp9wRP7cpWKPTl",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_v3"
    }
  }
}
```

## 2026-11-14T12:56:08.654+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "1543ce483ed943499e7a249fd90971e5",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\evan_zhao__eleven_v3.mp3",
  "pid": 41180,
  "request_fingerprint": "a7db6d3f0bbca9d17116d0cd2907441280667378fc31ec291401054df7e9518a",
  "time": "2026-11-14T12:56:08.654+00:00",
  "event": "error",
  "elapsed_s": 3.406,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"73d15202b16ffe6e57a580b452e2653e\"}}"
}
```

## 2026-11-14T12:56:09.057+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "1d58d5de40dc4219a13725de7b6443db",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\mr_chen__eleven_v3.mp3",
  "pid": 26936,
  "request_fingerprint": "e91e29f7f383e144b439ab3510acbb2b341d80563a0b126851a62c99bf761694",
  "time": "2026-11-14T12:56:09.057+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/cwzmKSYMCC9Aym1ymCnt?output_format=mp3_44100_128",
    "voice_id": "cwzmKSYMCC9Aym1ymCnt",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_v3"
    }
  }
}
```

## 2026-11-14T12:56:11.103+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "1d58d5de40dc4219a13725de7b6443db",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\mr_chen__eleven_v3.mp3",
  "pid": 26936,
  "request_fingerprint": "e91e29f7f383e144b439ab3510acbb2b341d80563a0b126851a62c99bf761694",
  "time": "2026-11-14T12:56:11.103+00:00",
  "event": "error",
  "elapsed_s": 2.016,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"5c6ff8cda1b118a661145aed52678510\"}}"
}
```

## 2026-11-14T12:56:11.505+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "353bd20d7ab94bd7bcdcbd7b4fdedcd3",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\lan_chen__eleven_v3.mp3",
  "pid": 32692,
  "request_fingerprint": "b094d9f9880affe417962de9e137b5fdcdf3f107f3213578f375f14ee71a74bb",
  "time": "2026-11-14T12:56:11.505+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/bZtjnyJAFD0Cp3lfNG5g?output_format=mp3_44100_128",
    "voice_id": "bZtjnyJAFD0Cp3lfNG5g",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_v3"
    }
  }
}
```

## 2026-11-14T12:56:13.604+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "353bd20d7ab94bd7bcdcbd7b4fdedcd3",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\lan_chen__eleven_v3.mp3",
  "pid": 32692,
  "request_fingerprint": "b094d9f9880affe417962de9e137b5fdcdf3f107f3213578f375f14ee71a74bb",
  "time": "2026-11-14T12:56:13.604+00:00",
  "event": "error",
  "elapsed_s": 2.063,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"a306aab386ba22904fc3be92829253ac\"}}"
}
```

## 2026-11-14T12:56:13.946+00:00 — elevenlabs / POST /v1/text-to-speech — request

```json
{
  "request_id": "8d3ad386de184940aa253a378d93bdeb",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\yun_anchor__eleven_v3.mp3",
  "pid": 45948,
  "request_fingerprint": "42b312d91d190dfea51a8d37b1c57befdda13e9fbe8d1e1b3ddb80f361f0ebeb",
  "time": "2026-11-14T12:56:13.946+00:00",
  "event": "request",
  "request": {
    "method": "POST",
    "url": "https://api.elevenlabs.io/v1/text-to-speech/4AfodMgwXps9oZFhHzoj?output_format=mp3_44100_128",
    "voice_id": "4AfodMgwXps9oZFhHzoj",
    "body": {
      "text": "其实就在四天前，他给全体员工写过一封信，里面有这么一句：「我对妻子不忠。」 在我们看来，是中美科技战，把一个 CEO 的私事，变成了国家安全问题。 不过先说清楚，我们不是说他因为国家安全下台。他为什么走，公司没说，到现在也没人知道。 《纽约时报》援引匿名人士说，美国情报界怀疑，一位跟他走得很近的女商人在替中国情报机构做事。 比如胡锡进。据香港〇一转述，他最早说的是，民主党和建制派在搞黄仁勋，进而搞特朗普。 所以等热度过去，这件事留下的道理是：一家公司卖的东西越要紧，它掌门人的私事，就越不是私事。",
      "model_id": "eleven_v3"
    }
  }
}
```

## 2026-11-14T12:56:16.033+00:00 — elevenlabs / POST /v1/text-to-speech — error

```json
{
  "request_id": "8d3ad386de184940aa253a378d93bdeb",
  "provider": "elevenlabs",
  "operation": "POST /v1/text-to-speech",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven\\yun_anchor__eleven_v3.mp3",
  "pid": 45948,
  "request_fingerprint": "42b312d91d190dfea51a8d37b1c57befdda13e9fbe8d1e1b3ddb80f361f0ebeb",
  "time": "2026-11-14T12:56:16.033+00:00",
  "event": "error",
  "elapsed_s": 2.062,
  "error_type": "SystemExit",
  "error": "ElevenLabs HTTP 401：{\"detail\":{\"type\":\"invalid_request\",\"code\":\"quota_exceeded\",\"message\":\"This request exceeds your quota of 600358. You have 0 credits remaining, while 121 credits are required for this request.\",\"status\":\"quota_exceeded\",\"request_id\":\"b2cd8531aa067904918dde7eb419654e\"}}"
}
```

## 2026-11-14T12:56:23.538+00:00 — elevenlabs / GET /v1/user/subscription — request

```json
{
  "request_id": "257cd996f0c34665a0bab12f87951c04",
  "provider": "elevenlabs",
  "operation": "GET /v1/user/subscription",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 38576,
  "request_fingerprint": "aeebbacccaf65524d2b307f7680c0197ced9f66d49cd395d4670f326e2e6c72c",
  "time": "2026-11-14T12:56:23.538+00:00",
  "event": "request",
  "request": {
    "method": "GET",
    "url": "https://api.elevenlabs.io/v1/user/subscription"
  }
}
```

## 2026-11-14T12:56:28.984+00:00 — elevenlabs / GET /v1/user/subscription — result

```json
{
  "request_id": "257cd996f0c34665a0bab12f87951c04",
  "provider": "elevenlabs",
  "operation": "GET /v1/user/subscription",
  "target": "C:\\workspace\\micro-drama-platform\\edu_videos\\redian_xiangying\\_shared\\voice_lab_eleven",
  "pid": 38576,
  "request_fingerprint": "aeebbacccaf65524d2b307f7680c0197ced9f66d49cd395d4670f326e2e6c72c",
  "time": "2026-11-14T12:56:28.984+00:00",
  "event": "result",
  "elapsed_s": 5.422,
  "response": {
    "http_status": 200,
    "body": {
      "tier": "pro",
      "character_count": 600358,
      "character_limit": 600358,
      "max_character_limit_extension": 0,
      "max_credit_limit_extension": 0,
      "can_extend_character_limit": false,
      "allowed_to_extend_character_limit": false,
      "next_character_count_reset_unix": 1794898865,
      "voice_slots_used": 2,
      "professional_voice_slots_used": 1,
      "professional_voice_slots_used_in_workspace": 1,
      "voice_limit": 160,
      "max_voice_add_edits": 290,
      "voice_add_edit_counter": 1,
      "professional_voice_limit": 1,
      "can_extend_voice_limit": false,
      "can_use_instant_voice_cloning": true,
      "can_use_professional_voice_cloning": true,
      "currency": "usd",
      "current_overage": {
        "amount": "0",
        "currency": "usd"
      },
      "status": "active",
      "billing_period": "annual_period",
      "character_refresh_period": "monthly_period",
      "next_invoice": {
        "amount_due_cents": 0,
        "subtotal_cents": 0,
        "tax_cents": null,
        "discount_percent_off": null,
        "discount_amount_off": null,
        "discounts": [],
        "next_payment_attempt_unix": 1821164860,
        "payment_intent_status": null,
        "payment_intent_statusses": []
      },
      "open_invoices": [],
      "has_open_invoices": false,
      "cancels_immediately": false,
      "pending_change": {
        "kind": "cancellation",
        "timestamp_seconds": 1821161260
      },
      "has_used_starter_coupon_on_account": false,
      "has_used_creator_coupon_on_account": false,
      "is_eligible_for_starter_promo": false,
      "creator_arm_price": null,
      "is_annual_four_months_subscriber": false,
      "bfcm_2026_offer": null
    }
  }
}
```
