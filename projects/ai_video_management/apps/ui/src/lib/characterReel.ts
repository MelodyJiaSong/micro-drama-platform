import { ApiError } from "../types";
import { CHARACTER_DIR_SEGMENT, CHARACTER_GROUP_SEGMENT } from "./characterDir";

/** 人物卡的「样片与正片」（follow-up 286）：后端 `GET /api/character-reel`。 */
export interface ReelClip {
  id: string;
  video: string;
  stage: "turntable" | "draft" | "final";
  submit_id: string;
  credits: number | null;
  generated_at: string;
  duration: number | null;
  resolution: string;
  review_status: string;
}
export interface SkillReel {
  key: string; title: string; path: string; card: string; icon: string; peak: string;
  final: ReelClip | null; finals: ReelClip[]; drafts: ReelClip[];
}
export interface ReelCut {
  version: number; stage: "draft" | "final"; episode: string; path: string; video: string;
  duration: number | null; note: string; status: string; phase: string; error: string;
  /** 在人物目录 `demo/` 下（follow-up 288，没有分集的剧），后端已排在各集剪辑前。 */
  own: boolean;
}
export interface CharacterReel {
  name: string; path: string; turntable: ReelClip | null; skills: SkillReel[];
  cuts: Record<"draft" | "final", ReelCut[]>; watch: string[];
}

/** 人物卡正文 `…/characters/[{分组}/]{卡}/{卡}.md` → 人物目录；别的文件返回 null。 */
const CARD_MD_RE = new RegExp(`^(ai_videos/(?:[^/]+/)*characters/${CHARACTER_GROUP_SEGMENT}(${CHARACTER_DIR_SEGMENT}))/([^/]+)\.md$`);
export function characterCardDir(path: string): string | null {
  const match = CARD_MD_RE.exec(path);
  return match && match[2] === match[3] ? match[1] : null;
}

/** 有技能视频（草稿或正式条）才有东西可审。 */
export function hasSkillVideos(reel: CharacterReel): boolean {
  return reel.skills.some(skill => skill.drafts.length > 0 || skill.finals.length > 0);
}

export async function loadCharacterReel(dir: string): Promise<CharacterReel> {
  const response = await fetch(`/api/character-reel?path=${encodeURIComponent(dir)}`, { cache: "no-store" });
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || `HTTP ${response.status}`, data.detail);
  return data as CharacterReel;
}
