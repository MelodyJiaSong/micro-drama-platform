import { fetchFile } from "../api";

export const IMAGE_STATUS: Record<string, string> = {
  reviewed: "已验收", reviewed_with_notes: "已验收 · 有备注", revision_required: "待修订",
  generated_unreviewed: "有图 · 待验收", failed_or_unknown: "生成失败或结果未知",
  planned: "待生成", in_progress: "生成中",
};
export interface SharedAsset {
  id: string; name: string; aliases: string[]; category: string; version: string; grade: string | null;
  function: string; cost_limit: string; counter_failure: string; visual_signature: string;
  activation: { trigger: string; requirement: string }; parameters: string;
  relations: { target: string; role: string; required: boolean; note: string }[];
  image: { anchor: string; prompt: string; sha256: string | null; status: string; review_notes?: string[] };
  views?: { sheet: string; prompt: string; sha256: string | null; status: string; panels: string[]; review_notes?: string[] };
  name_en?: string; xianxia?: { concept: string; note?: string }; details?: Record<string, string | string[]>;
  adoption?: string; module?: string | null; backlinks?: { source: string; kind: string; role: string }[];
}
export interface SharedAssetGroup { id: string; name: string; children: { id: string; name: string; asset_ids: string[] }[] }
export interface SharedLibrary { title: string; version: string; assets: SharedAsset[]; navigation?: SharedAssetGroup[] }
export const sharedFile = (root: string, relative: string): string => `${root}/${relative}`;
export const sharedFileHref = (root: string, relative: string): string => `/file/${encodeURIComponent(sharedFile(root, relative))}`;
export const acceptedImage = (asset: SharedAsset): boolean => ["reviewed", "reviewed_with_notes"].includes(asset.image.status);

export async function loadSharedLibrary(root: string): Promise<SharedLibrary> {
  const file = await fetchFile(sharedFile(root, "library.json"));
  const data = JSON.parse(file.content) as SharedLibrary;
  if (!Array.isArray(data.assets) || data.assets.some(a => !a.id || !a.name || !a.image)) {
    throw new Error("公共资产目录格式不完整，请检查 library.json。");
  }
  return data;
}

export function filterSharedAssets(assets: SharedAsset[], query: string, category: string, status: string): SharedAsset[] {
  const needle = query.trim().toLocaleLowerCase();
  return assets.filter(a => (!category || a.category === category)
    && (!status || (status === "accepted" ? acceptedImage(a) : a.image.status === status))
    && (!needle || [a.id, a.name, ...(a.aliases ?? []), a.function, a.visual_signature].join(" ").toLocaleLowerCase().includes(needle)));
}
