import data from "../../../../../../.agents/references/project/ai_video_glossary.json";

export interface GlossaryCategory { id: string; zh: string; en: string; color: string; }
export interface GlossaryRelationType { id: string; zh: string; en: string; color: string; dash: string; }
export interface GlossaryTerm {
  id: string; zh: string; en: string; category: string; module: string;
  def_zh: string; def_en: string; where: string; x: number; y: number;
  /** Other Chinese names in use. */
  zh_alt?: string;
  /** Distinctions from neighbouring terms and where sources disagree. */
  notes?: string[];
  sources?: string[];
  /** false = listed and linked, but kept off the relationship graph to keep it readable. */
  in_graph?: boolean;
}
export interface GlossaryRelation { from: string; to: string; type: string; card: string; zh: string; }
export type TimelineSpan = [number, number, string];
export interface TimelineRow { term: string; spans: TimelineSpan[]; partial?: string; example?: boolean; }
export interface TimelineMarker { term: string; at: number; zh: string; }
export interface GlossaryTimeline {
  id: string; zh: string; en: string; unit: string; length: number; note: string;
  ticks: number[]; rows: TimelineRow[]; markers: TimelineMarker[];
}
export interface Glossary {
  summary: { zh: string; en: string };
  categories: GlossaryCategory[]; relation_types: GlossaryRelationType[];
  terms: GlossaryTerm[]; relations: GlossaryRelation[]; timelines: GlossaryTimeline[];
}

/** Single source: `.agents/references/project/ai_video_glossary.json` (bundled at build time). */
export const GLOSSARY = data as unknown as Glossary;
export const GLOSSARY_SOURCE = "repo:.agents/references/project/ai_video_glossary.json";

export const termById = (glossary: Glossary, id: string): GlossaryTerm | undefined => glossary.terms.find(term => term.id === id);
export const categoryOf = (glossary: Glossary, term: GlossaryTerm): GlossaryCategory | undefined =>
  glossary.categories.find(category => category.id === term.category);
export const inGraph = (term: GlossaryTerm): boolean => term.in_graph !== false;
export const relationType = (glossary: Glossary, id: string): GlossaryRelationType | undefined =>
  glossary.relation_types.find(type => type.id === id);

/** Relations touching a term, seen from that term (direction kept for wording). */
export function relationsOf(glossary: Glossary, id: string): { relation: GlossaryRelation; other: string; outgoing: boolean }[] {
  return glossary.relations
    .filter(relation => relation.from === id || relation.to === id)
    .map(relation => ({ relation, other: relation.from === id ? relation.to : relation.from, outgoing: relation.from === id }));
}

/** Data problems that would break the diagrams; the test suite keeps this empty. */
export function glossaryProblems(glossary: Glossary): string[] {
  const ids = new Set(glossary.terms.map(term => term.id));
  const categories = new Set(glossary.categories.map(category => category.id));
  const types = new Set(glossary.relation_types.map(type => type.id));
  const problems: string[] = [];
  if (ids.size !== glossary.terms.length) problems.push("duplicate term id");
  for (const term of glossary.terms) {
    if (!categories.has(term.category)) problems.push(`unknown category ${term.category} on ${term.id}`);
    if (![term.zh, term.en, term.def_zh, term.def_en].every(text => text.trim())) problems.push(`missing text on ${term.id}`);
  }
  for (const relation of glossary.relations) {
    if (!ids.has(relation.from) || !ids.has(relation.to)) problems.push(`dangling relation ${relation.from}→${relation.to}`);
    if (!types.has(relation.type)) problems.push(`unknown relation type ${relation.type}`);
  }
  for (const timeline of glossary.timelines) {
    for (const row of timeline.rows) {
      if (!ids.has(row.term)) problems.push(`unknown timeline term ${row.term}`);
      for (const [start, end] of row.spans) if (!(start < end) || start < 0 || end > timeline.length) problems.push(`bad span in ${timeline.id}/${row.term}`);
    }
    for (const marker of timeline.markers) if (!ids.has(marker.term) || marker.at < 0 || marker.at > timeline.length) problems.push(`bad marker in ${timeline.id}`);
  }
  return problems;
}
