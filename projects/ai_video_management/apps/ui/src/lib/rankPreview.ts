/** Ranking-series preview (follow-up 317): one page per paihangbang episode — the finished cuts,
 *  the music, and every card's photo with its credit, licence class and risk note — so a review
 *  needs one link, like the hero preview (follow-up 312). Pure data assembly; the page fetches. */
export const RANK_PREVIEW_ROUTE = "/rank-preview";

export function rankPreviewHref(path: string): string {
  return `${RANK_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

export type LicenceClass = "free" | "attribution" | "risk" | "ai" | "none";

export interface RankItemRaw {
  rank: number; name: string; subtitle?: string; country_name?: string; value_display?: string;
  secondary_display?: string; badge?: string; image?: string | null; image_credit?: string;
  image_risk?: string; image_note?: string;
}
export interface AssetRaw { file: string; licence?: string; author?: string; source_page?: string; commons_page?: string; subject_check?: string }
export interface EpisodeData { episode?: string; title?: string; kicker?: string; items: RankItemRaw[] }
export interface ManifestRaw {
  output?: string; duration_s?: number; render_seconds?: number; renderer?: string;
  inputs?: { music?: { path: string; in_s?: number; out_s?: number }[]; music_bed?: { fit?: string } };
}

export interface RankTile {
  rank: number; name: string; place: string; value: string; badge: string | null;
  image: string | null; credit: string; licence: string; licenceClass: LicenceClass;
  risk: string | null; subjectCheck: string | null; sourcePage: string | null;
}
export interface RankCut { name: string; path: string; label: string; durationS: number | null; music: { path: string; range: string }[] }
export interface RankPreview { title: string; kicker: string; tiles: RankTile[]; counts: Record<LicenceClass, number> }

export function licenceClass(licence: string, risk: string | undefined, hasImage: boolean): LicenceClass {
  if (!hasImage) return "none";
  const low = licence.trim().toLowerCase();
  if (low.startsWith("ai-generated")) return "ai";
  if (risk) return "risk";
  if (/^(public domain|pd\b|cc0|pexels|unsplash|pixabay)/.test(low)) return "free";
  if (/^cc[ -]by/.test(low) && !/\b(nc|nd)\b/.test(low.replace(/-/g, " "))) return "attribution";
  return "risk";
}

/** Episode dir + item-relative path → repo-relative path the media API serves. */
export const join = (dir: string, rel: string): string => `${dir.replace(/\/+$/, "")}/${rel.replace(/^\.?\/+/, "")}`;

export function buildRankPreview(dir: string, data: EpisodeData, assets: AssetRaw[]): RankPreview {
  const byFile = new Map(assets.map(a => [a.file, a]));
  const counts: Record<LicenceClass, number> = { free: 0, attribution: 0, risk: 0, ai: 0, none: 0 };
  const tiles = [...data.items].sort((a, b) => a.rank - b.rank).map(it => {
    const asset = it.image ? byFile.get(it.image) : undefined;
    const licence = asset?.licence ?? "";
    const cls = licenceClass(licence, it.image_risk, Boolean(it.image));
    counts[cls] += 1;
    return {
      rank: it.rank, name: it.name, place: [it.subtitle, it.country_name].filter(Boolean).join(" · "),
      value: [it.value_display, it.secondary_display].filter(Boolean).join(" / "), badge: it.badge ?? null,
      image: it.image ? join(dir, it.image) : null, credit: it.image_credit ?? "", licence,
      licenceClass: cls, risk: it.image_risk ?? null, subjectCheck: asset?.subject_check ?? null,
      sourcePage: asset?.source_page ?? asset?.commons_page ?? null,
    };
  });
  return { title: data.title ?? data.episode ?? dir, kicker: data.kicker ?? "", tiles, counts };
}

/** Absolute paths in manifests → repo-relative (`ai_videos/...`) so the media API can serve them. */
export function repoRelative(p: string): string {
  const norm = p.replace(/\\/g, "/");
  const i = norm.indexOf("ai_videos/");
  return i >= 0 ? norm.slice(i) : norm;
}

/** The rendered cuts: full version (all photos, some awaiting sign-off) first, then the default. */
export function buildCuts(videos: { name: string; path: string }[], manifests: Map<string, ManifestRaw>): RankCut[] {
  const label = (name: string): string =>
    name.includes("_with-risk-images") ? "完整版（含待签字图）" : name.includes("_draft") ? "草稿" : "默认版（风险图扣下）";
  const order = (name: string): number => (name.includes("_with-risk-images") ? 0 : name.includes("_draft") ? 2 : 1);
  return videos.filter(v => v.name.endsWith(".mp4"))
    .sort((a, b) => order(a.name) - order(b.name) || a.name.localeCompare(b.name))
    .map(v => {
      const m = manifests.get(v.name.replace(/\.mp4$/, ".manifest.json"));
      const music = (m?.inputs?.music ?? []).map(t => ({
        path: repoRelative(t.path),
        range: t.in_s !== undefined && t.out_s !== undefined ? `${t.in_s.toFixed(1)}–${t.out_s.toFixed(1)} s` : "整首",
      }));
      return { name: v.name, path: v.path, label: label(v.name), durationS: m?.duration_s ?? null, music };
    });
}

export const LICENCE_LABEL: Record<LicenceClass, string> = {
  free: "可商用", attribution: "CC 需署名", risk: "待签字", ai: "AI 出图", none: "无图",
};
