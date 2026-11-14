/** Scene storyboard (follow-up 336): every shot's panel cut from its group's board, left to right, each with its text and
 *  time range — for review only, never uploaded. Written by `tools/scene_board.py` into `scenes/sN/board/`. */
export const SCENE_PREVIEW_ROUTE = "/scene-preview";

export interface ScenePanel {
  shot: string; group: string | null; start: number; end: number; image: string; text: string; action: string;
  dialogue: string; board: string | null; cell: number;
}
export interface SceneBoard { scene: string; location: string; time: string; total: number; panels: ScenePanel[] }

const SCENE_PATH_RE = /^(.*\/episodes\/ep\d+)\/scenes\/(s\d+)$/;

export function scenePreviewHref(path: string): string {
  return `${SCENE_PREVIEW_ROUTE}?${new URLSearchParams({ path })}`;
}

export function parseScenePath(path: string): { episodePath: string; scene: string } | null {
  const m = SCENE_PATH_RE.exec(path.replace(/\/+$/, ""));
  return m ? { episodePath: m[1], scene: m[2] } : null;
}

export const boardIndexPath = (scenePath: string): string => `${scenePath.replace(/\/+$/, "")}/board/scene_board.json`;
export const boardStripPath = (scenePath: string): string => `${scenePath.replace(/\/+$/, "")}/board/scene_board.png`;

/** Consecutive panels of one group, so the page can draw one bracket per group. */
export function groupRuns(panels: ScenePanel[]): { group: string | null; panels: ScenePanel[] }[] {
  const runs: { group: string | null; panels: ScenePanel[] }[] = [];
  for (const p of panels) {
    const last = runs[runs.length - 1];
    if (last && p.group !== null && last.group === p.group) last.panels.push(p);
    else runs.push({ group: p.group, panels: [p] });
  }
  return runs;
}
