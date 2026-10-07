from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import seedance_kit
import indextts_dub
from post import post_common
import build_all_shot_prompts


@pytest.mark.parametrize("reference_prefix", ["References:", "Refs:"])
def test_english_references_bind_original_files_and_entities(tmp_path: Path, reference_prefix: str) -> None:
    (tmp_path / "scene.png").write_bytes(b"image")
    md = tmp_path / "shot01.md"
    md.write_text("""---
duration_s: 10
---
- scene → [`scene`](scene.png)
- c1_Aaron → 在 Seedance 里 @wow_c1_Aaron
## Seedance prompt

```text
References: `scene(scene)=>@` `c1_Aaron(entity)=>@`
No music.
```
""".replace("References:", reference_prefix), encoding="utf-8")
    refs, prompt, _ = seedance_kit.parse(md, {"entity_prefix": "wow"})
    assert [r.label for r in refs] == ["scene", "c1_Aaron"]
    filled = seedance_kit.kit_prompt(prompt, refs)
    assert "=>@图片1" in filled and "=>@wow_c1_Aaron" in filled


def test_english_voice_preserves_windows_identity_and_chinese_review_gloss(tmp_path: Path) -> None:
    md = tmp_path / "shot01.md"
    md.write_text("""---
duration_s: 10
---
## 台词配音 prompt

```text
Speaker: Aaron
Voice ID: en-young-male-01
Emotion: Hesitant.
Kind: in-frame
Text: A little.
Window: 0.4–2.86s
Target: 1.3s
```

中文释义：会一点。
""", encoding="utf-8")
    line = post_common.dialogue(md)[0]
    _, dub = indextts_dub.parse_shot(md)
    assert (line.speaker, line.text, line.zh, line.t0, line.t1) == ("Aaron", "A little.", "会一点。", 0.4, 2.86)
    assert post_common.onscreen(line.kind)
    assert (dub[0].voice_id, dub[0].t0, dub[0].t1, dub[0].text) == ("en-young-male-01", .4, 2.86, "A little.")


def test_snapshot_includes_every_voice_and_uses_english_upload_prompt(tmp_path: Path) -> None:
    d = tmp_path / "shots" / "shot01"
    d.mkdir(parents=True)
    d.joinpath("shot01.md").write_text("""---
duration_s: 10
prompt_format: single_full
prompt_language: zh
---
# ep01 / shot01
## 视频 prompt
```text
旧设计，不应输出。
```
## Seedance prompt
```text
对白语言: 所有人物对白必须使用英语（English only）。
台词: Aaron: A little.
```
## 台词配音 prompt
```text
Text: First.
```
```text
Text: Second.
```
""", encoding="utf-8")
    assert build_all_shot_prompts.build_episode(str(tmp_path)) == (1, 10)
    text = (tmp_path / "all_shot_prompts.md").read_text(encoding="utf-8")
    assert "English only" in text and "旧设计，不应输出" not in text
    assert "Text: First." in text and "Text: Second." in text

