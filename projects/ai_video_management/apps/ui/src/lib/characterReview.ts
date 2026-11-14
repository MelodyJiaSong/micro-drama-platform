/** 人物审阅页（follow-up 329）：读人物目录里的 `review.json`，按区展示建立视频、三视图、声样、表情等，每项一个编号，
 * 用户按编号说哪一项要修（例：「E05 再自然一点」）。review.json 由 `python tools/character_review.py <人物目录>` 生成。 */
export const CHARACTER_REVIEW_ROUTE = "/character-review";

export type ReviewKind = "image" | "video" | "audio";

export interface ReviewItem {
  id: string;
  label: string;
  path: string;
  kind: ReviewKind;
  desc?: string;
  status?: string;
  note?: string;
}

export interface ReviewSection {
  id: string;
  title: string;
  hint?: string;
  layout?: "wide" | "grid";
  items: ReviewItem[];
}

export interface CharacterReview {
  title: string;
  character: string;
  updated?: string;
  notes?: string[];
  sections: ReviewSection[];
}

/** 可审阅的目录：短剧人物目录，或教学视频的素材目录（如配音选型 `edu_videos/_shared/voice_lab`，follow-up 344）。 */
export const isReviewPath = (path: string): boolean => /^(ai_videos|edu_videos)\/.+/.test(path);

export function characterReviewHref(path: string): string {
  return `${CHARACTER_REVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

const KINDS: ReviewKind[] = ["image", "video", "audio"];

function kindOf(path: string, given: unknown): ReviewKind {
  if (typeof given === "string" && (KINDS as string[]).includes(given)) return given as ReviewKind;
  if (/\.(mp4|mov|webm)$/i.test(path)) return "video";
  if (/\.(mp3|wav|m4a|ogg)$/i.test(path)) return "audio";
  return "image";
}

const str = (v: unknown): string | undefined => (typeof v === "string" && v.trim() ? v : undefined);

/** Validate and normalise review.json; drops malformed entries instead of throwing, reports why. */
export function parseCharacterReview(raw: unknown): { review: CharacterReview | null; problems: string[] } {
  const problems: string[] = [];
  if (!raw || typeof raw !== "object") return { review: null, problems: ["review.json 不是对象"] };
  const r = raw as Record<string, unknown>;
  const sections: ReviewSection[] = [];
  const seen = new Set<string>();
  for (const [si, s] of (Array.isArray(r.sections) ? r.sections : []).entries()) {
    if (!s || typeof s !== "object") { problems.push(`第 ${si + 1} 区不是对象`); continue; }
    const sec = s as Record<string, unknown>;
    const items: ReviewItem[] = [];
    for (const it of Array.isArray(sec.items) ? sec.items : []) {
      const o = (it ?? {}) as Record<string, unknown>;
      const id = str(o.id), path = str(o.path);
      if (!id || !path) { problems.push(`「${str(sec.title) ?? si + 1}」里有一项缺编号或路径`); continue; }
      if (seen.has(id)) problems.push(`编号 ${id} 重复`);
      seen.add(id);
      items.push({ id, path, label: str(o.label) ?? id, kind: kindOf(path, o.kind), desc: str(o.desc), status: str(o.status), note: str(o.note) });
    }
    sections.push({ id: str(sec.id) ?? String(si + 1), title: str(sec.title) ?? `第 ${si + 1} 区`, hint: str(sec.hint),
      layout: sec.layout === "wide" ? "wide" : "grid", items });
  }
  if (!sections.length) problems.push("review.json 没有任何分区");
  const notes = Array.isArray(r.notes) ? r.notes.filter((n): n is string => typeof n === "string") : undefined;
  return { review: { title: str(r.title) ?? "人物审阅", character: str(r.character) ?? "", updated: str(r.updated), notes, sections }, problems };
}

/** 状态的颜色档：通过 / 要修 / 其他（待审）。 */
export function statusTone(status?: string): "ok" | "fix" | "pending" {
  if (!status) return "pending";
  if (/^(通过|已定|OK)/i.test(status)) return "ok";
  if (/(要修|重出|不通过|退回)/.test(status)) return "fix";
  return "pending";
}
