"""Open YouTube watch pages in headless Chrome (no login, no cookies) and dump
measured metadata + storyboard spec as JSON Lines.

usage: python -I probe.py OUT.jsonl ID [ID ...]
"""
import json
import sys

from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const pr = window.ytInitialPlayerResponse || null;
  const vd = pr && pr.videoDetails || {};
  const mf = pr && pr.microformat && pr.microformat.playerMicroformatRenderer || {};
  const sb = pr && pr.storyboards && pr.storyboards.playerStoryboardSpecRenderer;
  let likes = null;
  try {
    const txt = JSON.stringify(window.ytInitialData);
    const m = txt.match(/"likeCount":"?(\d+)/) || txt.match(/along with (\d[\d,]*) other/);
    if (m) likes = m[1].replace(/,/g, '');
  } catch (e) {}
  const status = pr && pr.playabilityStatus && pr.playabilityStatus.status;
  let vtext = null, dtext = null, ttl = null, owner = null;
  try {
    const cs = window.ytInitialData.contents.twoColumnWatchNextResults.results.results.contents;
    for (const c of cs) {
      const pi = c.videoPrimaryInfoRenderer;
      if (pi) {
        vtext = pi.viewCount.videoViewCountRenderer.viewCount.simpleText;
        dtext = pi.dateText && pi.dateText.simpleText;
        ttl = pi.title.runs.map(r => r.text).join('');
      }
      const si = c.videoSecondaryInfoRenderer;
      if (si) owner = si.owner.videoOwnerRenderer.title.runs[0].text;
    }
  } catch (e) {}
  return {
    id: vd.videoId, title: vd.title, channel: vd.author, channel_id: vd.channelId,
    view_count: vd.viewCount ? Number(vd.viewCount) : null,
    duration: vd.lengthSeconds ? Number(vd.lengthSeconds) : null,
    upload_date: mf.uploadDate || mf.publishDate || null,
    like_count: likes ? Number(likes) : null,
    storyboard_spec: sb ? sb.spec : null,
    playability: status,
    initialdata_views_text: vtext, initialdata_date_text: dtext,
    initialdata_title: ttl, initialdata_channel: owner,
  };
}
"""


def main() -> None:
    out_path, ids = sys.argv[1], sys.argv[2:]
    with sync_playwright() as p, open(out_path, "a", encoding="utf-8") as out:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(locale="en-US", viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        for vid in ids:
            try:
                page.goto(f"https://www.youtube.com/watch?v={vid}&hl=en", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_function("() => !!window.ytInitialPlayerResponse", timeout=30000)
                page.wait_for_timeout(1500)
                rec = page.evaluate(JS)
                rec["requested_id"] = vid
                rec["measured_via"] = "headless chrome watch page (ytInitialPlayerResponse), 2026-11-06"
            except Exception as e:  # noqa: BLE001
                rec = {"requested_id": vid, "error": str(e)[:300]}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            print(vid, rec.get("view_count"), rec.get("duration"), rec.get("playability"), rec.get("error", "")[:80], flush=True)
        browser.close()


if __name__ == "__main__":
    main()
