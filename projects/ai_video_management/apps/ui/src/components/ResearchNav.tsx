/** The 选题调研 subtree in the sidebar: 调研结果 › {月份} › {10 大分类}.
 *
 * Driven by the research API rather than the file tree, because the categories
 * are series inside a dataset, not files on disk — materialising them as files
 * would duplicate the dataset and the copies would drift. Datasets are
 * month-keyed (`2026-09.json`), so a new month is a new file and appears here
 * with no code change. */
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { fetchResearchDatasets, type ResearchDatasetSummary } from "../lib/researchApi";

export interface ResearchNavProps {
  /** Depth of the `_research` tree item, so this subtree keeps the tree's indent rhythm. */
  depth: number;
}

const indent = (depth: number): { paddingLeft: string } => ({
  paddingLeft: `${8 + depth * 14}px`,
});

export function ResearchNav({ depth }: ResearchNavProps): JSX.Element | null {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [datasets, setDatasets] = useState<ResearchDatasetSummary[]>([]);
  const [failed, setFailed] = useState(false);
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  useEffect(() => {
    void (async () => {
      try {
        setDatasets((await fetchResearchDatasets()).datasets);
      } catch {
        setFailed(true);
      }
    })();
  }, []);

  const groups = useMemo(() => {
    const byGroup = new Map<string, ResearchDatasetSummary[]>();
    for (const d of datasets) {
      const key = d.group ?? "调研结果";
      byGroup.set(key, [...(byGroup.get(key) ?? []), d]);
    }
    // newest month first — the current month is what the user is working in
    for (const list of byGroup.values()) {
      list.sort((a, b) => (b.month ?? b.dataset).localeCompare(a.month ?? a.dataset));
    }
    return [...byGroup.entries()];
  }, [datasets]);

  if (failed || datasets.length === 0) return null;

  const activeDataset = searchParams.get("dataset");
  const activeSlug = searchParams.get("series");
  const isOpen = (key: string): boolean => collapsed[key] !== true;
  const toggle = (key: string): void => setCollapsed((c) => ({ ...c, [key]: !(c[key] !== true) }));

  return (
    <>
      {groups.map(([group, list]) => (
        <div key={group} className="research-nav-group">
          <div
            className="tree-item tree-branch research-nav-row"
            style={indent(depth + 1)}
            role="treeitem"
            aria-level={depth + 2}
            aria-expanded={isOpen(group)}
            aria-selected={false}
            tabIndex={-1}
            onClick={(e) => {
              e.stopPropagation();
              toggle(group);
            }}
          >
            <button
              type="button"
              className="tree-disclosure"
              aria-label={isOpen(group) ? "折叠" : "展开"}
              onClick={(e) => {
                e.stopPropagation();
                toggle(group);
              }}
            >
              {isOpen(group) ? "▾" : "▸"}
            </button>
            <span className="tree-name">{group}</span>
          </div>

          {isOpen(group)
            ? list.map((d) => {
                const monthKey = `${group}/${d.dataset}`;
                const monthOpen = isOpen(monthKey);
                const monthActive = d.dataset === activeDataset && !activeSlug;
                return (
                  <div key={d.dataset} className="research-nav-month">
                    <div
                      className={
                        monthActive
                          ? "tree-item tree-branch research-nav-row tree-active"
                          : "tree-item tree-branch research-nav-row"
                      }
                      style={indent(depth + 2)}
                      role="treeitem"
                      aria-level={depth + 3}
                      aria-expanded={monthOpen}
                      aria-selected={monthActive}
                      tabIndex={-1}
                      title={`${d.title} · ${d.series_count} 个分类`}
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/research?dataset=${encodeURIComponent(d.dataset)}`);
                      }}
                    >
                      <button
                        type="button"
                        className="tree-disclosure"
                        aria-label={monthOpen ? "折叠" : "展开"}
                        onClick={(e) => {
                          e.stopPropagation();
                          toggle(monthKey);
                        }}
                      >
                        {monthOpen ? "▾" : "▸"}
                      </button>
                      <span className="tree-name">{d.month ?? d.dataset}</span>
                      <span className="research-nav-count">{d.series_count}</span>
                    </div>

                    {monthOpen
                      ? (d.series ?? []).map((s) => {
                          const active = d.dataset === activeDataset && s.slug === activeSlug;
                          return (
                            <div
                              key={s.slug}
                              className={
                                active
                                  ? "tree-item tree-leaf research-nav-row research-nav-series tree-active"
                                  : "tree-item tree-leaf research-nav-row research-nav-series"
                              }
                              style={indent(depth + 3)}
                              role="treeitem"
                              aria-level={depth + 4}
                              aria-selected={active}
                              tabIndex={-1}
                              title={s.name_zh}
                              onClick={(e) => {
                                e.stopPropagation();
                                navigate(
                                  `/research?dataset=${encodeURIComponent(d.dataset)}&series=${encodeURIComponent(s.slug)}`,
                                );
                              }}
                            >
                              <span className="research-nav-rank">#{s.rank}</span>
                              <span className="tree-name research-nav-name">{s.name_zh}</span>
                            </div>
                          );
                        })
                      : null}
                  </div>
                );
              })
            : null}
        </div>
      ))}
    </>
  );
}
