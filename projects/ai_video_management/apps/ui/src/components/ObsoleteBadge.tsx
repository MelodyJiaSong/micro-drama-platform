/** 「已过时」badge: the folder — or, for a drama, its series — holds an
 * `OBSOLETE.md`. Its content was made with, or only serves, the old 0–7 stage
 * pipeline removed in follow-up 233; it stays for reference until it is redone
 * with the six-module workflow. The backend marks the tree node (`obsolete`,
 * `obsolete_note` = the marker's path). */
export function ObsoleteBadge({ note }: { note?: string }): JSX.Element {
  return (
    <small className="obsolete-badge" title={note ? `已过时 — 说明见 ${note}` : "已过时"}>
      已过时
    </small>
  );
}
