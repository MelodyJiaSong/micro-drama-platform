/** Which folder under a drama's `characters/` is a character card: `c{N}_…`
 * (named cast) or `m{N}_…` (monsters and crowd NPCs — they get a turntable too,
 * see the asset rules in .agents/skills/ai-videos-pipeline/resources/assets.md). Single definition for the UI; the backend twin is
 * `libs/common/character_dir.py`. */
const PREFIX = "[cm]\\d+";

/** A character folder name; group 1 is the display name after `cN_` / `mN_`. */
export const CHARACTER_DIR_RE = new RegExp(`^${PREFIX}(?:_(.*))?$`);

/** The same folder as one segment inside a path regex. */
export const CHARACTER_DIR_SEGMENT = `${PREFIX}(?:_[^/]+)?`;
