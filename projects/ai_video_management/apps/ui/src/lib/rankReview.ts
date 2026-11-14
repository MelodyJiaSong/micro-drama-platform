import { ApiError } from "../types";

/** 排行榜审片数据（follow-up 320）：后端 `GET /api/rank-preview?path=`，系列根给总览，一期目录给单期。
 *  路径都是仓库相对路径；文件不在为空串。 */
export const RANK_SERIES_PATH = "ai_videos/paihangbang";

export interface RankVideo {
  name: string; path: string; label: string; risk: boolean;
  /** 无 manifest 又看不出时为 null。 */
  music: boolean | null;
  duration_s: number | null;
  /** 没有 moov（还在渲染）为 false，不能播。 */
  complete: boolean;
  recommended: boolean;
}
export interface RankImageStats { items: number; with_image: number; missing: number; risk: number; alt: number; ai: number }
export interface RankImage { path: string; declared: string; licence: string; author: string; source: string; ai: boolean }
/** 公司卡创始人（契约 v1.3 `person`，follow-up 321）。 */
export interface RankPerson { name: string; role: string; image: RankImage | null; image_risk: string; credit: string }
export interface RankItem {
  /** 列表期（mode=list）是出场序号，不是名次。 */
  rank: number; name: string; subtitle: string; country_iso2: string; country_name: string; flag: string;
  value_display: string; badge: string; image: RankImage | null; image_alt: RankImage | null; image_risk: string;
  /** 契约 v1.3/v1.4 可选字段（follow-up 321）；没写为空串 / null。 */
  corner: string; logo: RankImage | null; logo_bg: string; person: RankPerson | null;
  image_alt_credit: string; secondary_display: string; notes: string;
}
export interface RankDoc { path: string; text: string }
export interface RankEpisodeCard {
  key: string; number: number | null; path: string; title: string; n: number; champion: string;
  duration_s: number | null; thumbnail: string; verdict: string; music: boolean | null; videos: number;
  stats: RankImageStats; error: string;
  /** follow-up 321：列表期没有冠军（champion 为空），给首个 / 末个与排列依据。 */
  mode: "rank" | "list"; first: string; last: string; list_order: string;
}
export interface RankEpisode {
  card: RankEpisodeCard; kicker: string; theme: string; metric_label: string; period_label: string;
  source_line: string; scope_note: string; videos: RankVideo[]; verdict_excerpt: string;
  qc: RankDoc; publish: RankDoc; handoff: RankDoc; items: RankItem[];
  insights: { after_rank: number | null; text: string }[];
}
export interface RankSeries { path: string; focus: number[]; episodes: RankEpisodeCard[] }
export interface RankPreviewData { kind: "series" | "episode"; series: RankSeries | null; episode: RankEpisode | null }

export const isRankSeriesPath = (path: string): boolean => path.replace(/\/+$/, "") === RANK_SERIES_PATH;

export async function loadRankPreview(path: string): Promise<RankPreviewData> {
  const response = await fetch(`/api/rank-preview?path=${encodeURIComponent(path)}`, { cache: "no-store" });
  const data = await response.json();
  if (!response.ok) throw new ApiError(response.status, data.detail?.message || data.detail?.kind || `HTTP ${response.status}`, data.detail);
  return data as RankPreviewData;
}

export function formatDuration(s: number | null): string {
  if (s === null) return "—";
  const total = Math.round(s);
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

/** The tab to open first: the backend's recommended cut, else the first playable one. */
export function defaultVideo(videos: RankVideo[]): RankVideo | null {
  return videos.find(v => v.recommended) ?? videos.find(v => v.complete) ?? videos[0] ?? null;
}

export const musicLabel = (m: boolean | null): string => (m === true ? "有配乐" : m === false ? "无配乐" : "配乐未知");

/** follow-up 321：列表期（mode=list）不排名。 */
export const isListMode = (card: Pick<RankEpisodeCard, "mode">): boolean => card.mode === "list";

/** 「列表期 · 按成立年份，不排名」；排列依据看不出时写「按出场顺序」。 */
export const listModeLabel = (card: Pick<RankEpisodeCard, "list_order">): string =>
  `列表期 · 按${card.list_order || "出场顺序"}，不排名`;

/** 名次 / 序号单元格：排名期 `#3`，列表期 `3`。 */
export const positionLabel = (rank: number, list: boolean): string => (list ? String(rank) : `#${rank}`);

/** 主图风险等级：通讯社图（Getty / Reuters / AP）最高。 */
export const isNewsAgencyRisk = (risk: string): boolean => /news[- ]?agency/i.test(risk);

export const isAiCredit = (credit: string): boolean => /ai-generated/i.test(credit);

/** 姓名首字母圆章（头像缺失时）。 */
export const initials = (name: string): string =>
  name.split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0]?.toUpperCase() ?? "").join("") || "?";
