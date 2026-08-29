from __future__ import annotations

from libs.application.dtos.compose__dto import ComposeResultCdto
from libs.common.vocab import SUBTITLE_FORBIDDEN_TOKENS
from libs.domain.errors.shot__error import CorruptExtractOutputError, DescriptorDriftError
from libs.domain.value_objects.promptunit__valueobject import PromptUnit, plan_prompt_units
from libs.domain.value_objects.scriptformat__valueobject import render_episode_script
from libs.domain.value_objects.shotprompt__valueobject import (
    DialogueForShot,
    ShotPromptFields,
    build_video_prompt_body,
)
from libs.infrastructure.clients.composer__client import LlmComposer
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter

_RENDER_STYLE = "实拍短剧质感，写实电影感，竖屏构图，皮肤质感自然，浅景深"

_SCRUBBED_FIELDS = ("action", "scene_desc", "blocking", "performance", "lighting", "mood")


def _merge_unit_fields(unit: PromptUnit, sources: list[dict]) -> dict[str, str]:
    """Collapse the covered original-shot analyses into one field set for the prompt
    unit: a merged group narrates the intra-unit cuts; a split segment is labeled."""
    if len(sources) == 1:
        action = sources[0]["action"]
        blocking = sources[0]["blocking"]
        performance = sources[0]["performance"]
    else:
        action = "（镜内跳切）".join(s["action"] for s in sources)
        blocking = "；转：".join(dict.fromkeys(s["blocking"] for s in sources))
        performance = "；".join(dict.fromkeys(s["performance"] for s in sources))
    if unit.segment:
        action += f"（原长镜第{unit.segment[0]}/{unit.segment[1]}段，动作连续推进）"
    return {
        "action": action, "scene_desc": sources[0]["scene_desc"], "blocking": blocking,
        "performance": performance, "lighting": sources[0]["lighting"], "mood": sources[0]["mood"],
    }


def _source_desc(unit: PromptUnit) -> str:
    shots_label = "+".join(f"原镜{i:02d}" for i in unit.source_shot_indexes)
    span = f"时间码 {unit.start_s:.2f}s–{unit.end_s:.2f}s"
    if unit.segment:
        return f"{shots_label} 第{unit.segment[0]}/{unit.segment[1]}段，{span}"
    if len(unit.source_shot_indexes) > 1:
        return f"{shots_label}（镜内跳切合并），{span}"
    return f"{shots_label}，{span}"


def _scrub_subtitle_tokens(analysis: dict) -> tuple[dict[str, str], bool]:
    """Mechanical guarantee for the 台词纯净 contract: VLM descriptions sometimes
    mention on-screen overlay text (角色名牌/字幕浮层 — 2026-07-18 real run), which
    trips SubtitleContaminationError downstream. The understanding prompts now forbid
    it at the source; this scrub keeps compose alive if a token still slips through."""
    texts: dict[str, str] = {}
    hit = False
    for field in _SCRUBBED_FIELDS:
        text = str(analysis[field])
        for token in SUBTITLE_FORBIDDEN_TOKENS:
            if token in text:
                text = text.replace(token, "")
                hit = True
        texts[field] = text
    return texts, hit


class ComposeCommand:
    """FR-5: script (逐字忠实) -> novel (文学化) -> per-shot shotNN.md (repo ai_video
    contract). Generation-time gates: prompt budget, subtitle purity, and non-empty
    byte-identical 锁定描述符 (DescriptorDriftError if the understand stage failed to
    author one)."""

    def __init__(self, composer: LlmComposer, reader: ArtifactReader, writer: ArtifactWriter) -> None:
        self._composer = composer
        self._reader = reader
        self._writer = writer

    def run(self, drama_id: str, episode_rel_dir: str, force: bool = False) -> ComposeResultCdto:
        manifest_rel = f"{episode_rel_dir}/compose_manifest.json"
        script_rel = f"{episode_rel_dir}/script.md"
        if self._reader.exists(manifest_rel) and not force:
            existing = self._reader.read_json(manifest_rel)
            return ComposeResultCdto(episode_rel_dir=episode_rel_dir, shot_files=existing["shot_files"],
                                     script_rel_path=script_rel, novel_rel_path=existing["novel_rel_path"],
                                     degradations=existing["degradations"], skipped=True)

        understanding = self._reader.read_json(f"{episode_rel_dir}/understanding.json")
        dialogue = self._reader.read_json(f"{episode_rel_dir}/dialogue.json")
        shots = self._reader.read_json(f"{episode_rel_dir}/shots.json")
        library = self._reader.read_json(f"{drama_id}/characters/library.json")
        descriptors = {c["name"]: c["descriptor"] for c in library["characters"]}
        analyses = {a["index"]: a for a in understanding["shots"]}

        lines_by_shot, clamped = self._assign_lines_to_shots(dialogue["lines"], shots)
        episode_index = int(episode_rel_dir.rsplit("ep", 1)[-1])
        script_md = render_episode_script(episode_index, understanding["narrative"], shots, analyses, lines_by_shot)
        self._writer.write_text(script_rel, script_md)
        self._writer.write_text(f"{episode_rel_dir}/dialogue.md", self._render_dialogue_table(shots, lines_by_shot))

        degradations: list[str] = []
        if clamped:
            degradations.append(f"lines_clamped_to_nearest_shot:{clamped}")
        novel_rel = f"{episode_rel_dir}/novel.md"
        if self._composer.available:
            self._writer.write_text(novel_rel, self._composer.compose_novel(script_md, understanding["narrative"]))
        else:
            degradations.append("novel_llm_unavailable_skeleton_only")
            self._writer.write_text(novel_rel, f"# 小说（骨架版·待 LLM 后端润色）\n\n{understanding['narrative']}\n")

        # 分镜级 prompt 层 (follow-up 005): the episode-level script above keeps the
        # original detected shots; prompt units re-plan those spans under the Seedance
        # 4–15s bounds (>15s split into 承接 segments, <4s merged into a neighbor)
        units = plan_prompt_units(shots)
        unit_spans = [{"index": u.unit_index, "start_s": u.start_s, "end_s": u.end_s} for u in units]
        lines_by_unit, _ = self._assign_lines_to_shots(dialogue["lines"], unit_spans)
        links = self._unit_links(units, analyses)

        shot_files: list[str] = []
        all_parts: list[str] = []
        for pos, unit in enumerate(units):
            sources = [analyses[i] for i in unit.source_shot_indexes]
            names = list(dict.fromkeys(n for s in sources for n in s["characters"]))
            for name in names:
                if not (descriptors.get(name) or "").strip():
                    raise DescriptorDriftError(
                        f"character '{name}' has no locked descriptor — understand stage must author it first"
                    )
            texts, scrubbed = _scrub_subtitle_tokens(_merge_unit_fields(unit, sources))
            if scrubbed:
                degradations.append(f"shot{unit.unit_index:02d}_subtitle_token_scrubbed")
            if unit.floor_clamped:
                degradations.append(f"shot{unit.unit_index:02d}_duration_floor_clamped_to_4s")
            tail_locked = pos + 1 < len(units) and links[pos + 1] == "承接"
            fields = ShotPromptFields(
                index=unit.unit_index,
                reference_line=self._reference_line(links[pos], unit.unit_index,
                                                    units[pos - 1].unit_index if pos else None, names),
                characters={n: descriptors[n] for n in names},
                plot=texts["action"],
                scene=texts["scene_desc"],
                shot_size=sources[0]["shot_size"], camera_angle=sources[0]["camera_angle"],
                camera_move=sources[0]["camera_move"], blocking=texts["blocking"],
                action=f"表演：{texts['performance']}",
                dialogue=tuple(
                    DialogueForShot(l["speaker"], l["text"], l.get("dialogue_type", "对白"))
                    for l in lines_by_unit.get(unit.unit_index, [])
                ),
                lighting=texts["lighting"], pacing=texts["mood"],
                render_style=_RENDER_STYLE, duration_s=unit.duration_s,
                link=links[pos], tail_locked=tail_locked,
            )
            body, dropped = build_video_prompt_body(fields)
            if dropped:
                degradations.append(f"shot{unit.unit_index:02d}_budget_dropped:{'+'.join(dropped)}")
            shot_rel = f"{episode_rel_dir}/shots/shot{unit.unit_index:02d}/shot{unit.unit_index:02d}.md"
            self._writer.write_text(
                shot_rel, self._render_shot_md(drama_id, episode_rel_dir, fields, body, _source_desc(unit)))
            shot_files.append(shot_rel)
            all_parts.append(f"## shot{unit.unit_index:02d}\n\n```text\n{body}\n```\n")

        self._writer.write_text(f"{episode_rel_dir}/all_shot_prompts.md",
                                f"# 全镜 prompt 汇总 — {episode_rel_dir}\n\n" + "\n".join(all_parts))
        self._writer.write_json(manifest_rel, {
            "shot_files": shot_files, "novel_rel_path": novel_rel, "degradations": degradations,
        })
        return ComposeResultCdto(episode_rel_dir=episode_rel_dir, shot_files=shot_files,
                                 script_rel_path=script_rel, novel_rel_path=novel_rel, degradations=degradations)

    @staticmethod
    def _unit_links(units: list[PromptUnit], analyses: dict[int, dict]) -> list[str]:
        links: list[str] = []
        for pos, unit in enumerate(units):
            if pos == 0:
                links.append("硬切")
            elif unit.segment and unit.segment[0] > 1:
                links.append("承接")  # split segments chain by construction
            else:
                links.append("承接" if analyses[unit.source_shot_indexes[0]]["continuous_with_prev"] else "硬切")
        return links

    @staticmethod
    def _assign_lines_to_shots(lines: list[dict], shots: list[dict]) -> tuple[dict[int, list[dict]], int]:
        """Every line is assigned (FR-5.1 逐字忠实): midpoint containment first, else
        clamped to the nearest shot; the clamp count is surfaced as a degradation."""
        if lines and not shots:
            raise CorruptExtractOutputError("episode has dialogue lines but zero shots")
        result: dict[int, list[dict]] = {}
        clamped = 0
        for line in lines:
            mid = (line["start_s"] + line["end_s"]) / 2
            target = next((s for s in shots if s["start_s"] <= mid < s["end_s"]), None)
            if target is None:
                target = min(shots, key=lambda s: min(abs(mid - s["start_s"]), abs(mid - s["end_s"])))
                clamped += 1
            result.setdefault(target["index"], []).append(line)
        assert sum(len(v) for v in result.values()) == len(lines)
        return result, clamped

    @staticmethod
    def _reference_line(link: str, index: int, prev_index: int | None, characters: list[str]) -> str:
        handles = "、".join(f"@{n}参考图" for n in characters) if characters else "（无人物参考）"
        if link == "承接" and prev_index is not None:
            return f"参考: 本镜首帧(上一镜末帧)=>shot{prev_index:02d}_lastframe.png；{handles}"
        return f"参考: 首帧图=>shot{index:02d}_firstframe.png；{handles}"

    @staticmethod
    def _render_dialogue_table(shots: list[dict], lines_by_shot: dict[int, list[dict]]) -> str:
        dlg = ["# 台词表\n"]
        for shot in shots:
            for line in lines_by_shot.get(shot["index"], []):
                mark = f"（{line['dialogue_type']}）" if line.get("dialogue_type") in ("内心独白", "旁白") else ""
                dlg.append(f"- [镜{shot['index']:02d}] {line['speaker']}{mark}：「{line['text']}」")
        return "\n".join(dlg)

    def _render_shot_md(self, drama_id: str, episode_rel_dir: str, f: ShotPromptFields, body: str,
                        source_desc: str) -> str:
        """武神觉醒 shotNN.md 五层结构 (follow-up 008): YAML → ## 原片对应段 → H1 →
        ## Shot context 要点列表 → ## 视频 prompt → ## 台词配音 prompt (```text 块)."""
        ep_label = episode_rel_dir.rsplit("/", 1)[-1]
        title = (f.pacing.split("，")[0].split("、")[0].strip() or "正片") if f.pacing else "正片"
        link_line = (f"承接 shot{f.index - 1:02d} 末帧（首帧＝上一镜末帧）" if f.link == "承接" else "硬切（独立首帧）")
        summary = f.plot if len(f.plot) <= 120 else f.plot[:120] + "…"
        scene = f.scene.rstrip("。")
        char_items = ("；".join(f"{n}（{d}）" for n, d in f.characters.items())
                      if f.characters else "（无具名角色）")
        refs: list[str] = []
        if f.link == "承接":
            refs.append(f"shot{f.index - 1:02d}_lastframe.png（上一镜渲染末帧＝本镜首帧，用户上传）")
        refs += [f"{n} 参考图" for n in f.characters]
        context = [
            f"- **Summary**：{summary}",
            f"- **Characters**：{char_items}。",
            f"- **Scene**：{scene}。",
            f"- **Duration**：{f.duration_s:.0f}s。",
            f"- **衔接**：{link_line}。",
        ]
        if f.tail_locked:
            context.append(f"- **尾帧锁定**：本镜末帧为下一镜承接首帧（交接源）——重生成时须以已存 "
                           f"shot{f.index:02d}_lastframe.png 经模型尾帧槽钉住末帧。")
        context.append("- **Reference uploads**：" + ("、".join(refs) if refs else "（无）") + "。")
        if f.duration_s > 10:
            context.append(f"- **Kling 拆段**：Kling 档位仅 5s/10s——本镜 {f.duration_s:.0f}s > 10s，"
                           f"Kling 侧需按承接帧拆段渲染。")
        voice_stanzas = "\n\n".join(
            f"角色: {d.speaker}\n"
            f"音色: voice_{d.speaker}(锁定，voice_id 待选定后全剧复用)\n"
            f"情绪: {f.pacing}\n"
            f"语速: 正常\n"
            f"类型: {d.dialogue_type}\n"
            f"台词: {d.text}\n"
            f"时长目标: {f.duration_s:.0f}秒内"
            for d in f.dialogue
        )
        voice_block = f"```text\n{voice_stanzas}\n```" if voice_stanzas else "（本镜无台词，无需配音）"
        return (
            f"---\ndrama: {drama_id}\nepisode: {episode_rel_dir}\nshot: {f.index}\n"
            f"duration_s: {f.duration_s:.0f}\nlink: {f.link}\ntail_locked: {str(f.tail_locked).lower()}\n---\n\n"
            f"## 原片对应段\n\n{source_desc}（{f.duration_s:.0f}s）。"
            f"场景：{scene}。动作：{f.plot}\n\n"
            f"# {ep_label} / shot{f.index:02d} · {title}\n\n"
            f"## Shot context\n" + "\n".join(context) + "\n\n"
            f"## 视频 prompt\n\n```text\n{body}\n```\n\n"
            f"## 台词配音 prompt\n\n{voice_block}\n"
        )
