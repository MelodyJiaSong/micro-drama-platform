"""Editor fill with a switchable insertion strategy + real mention picking, and editor snapshot reads (FR-31)."""
from __future__ import annotations

from collections.abc import Sequence

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__steps import guard, is_visible, locate, ms, named, press_keys, require
from libs.infrastructure.daos.jimeng_page__dao import (
    EditorSnapshotDao,
    FillSegmentDao,
    InsertionStrategy,
    NewlineMode,
)

SNAPSHOT_JS: str = """(root, mentionCss) => {
  const out = [];
  const mentions = [];
  const blocks = { P: 1, DIV: 1, LI: 1 };
  const nameOf = (node) => {
    const label = node.getAttribute('data-label') || node.getAttribute('data-id');
    return label !== null ? label : (node.textContent || '').replace(/^@/, '').trim();
  };
  const walk = (parent) => {
    for (const child of parent.childNodes) {
      if (child.nodeType === 3) { out.push(child.data); continue; }
      if (child.nodeType !== 1) continue;
      if (child.matches(mentionCss)) { const name = nameOf(child); out.push(name); mentions.push(name); continue; }
      if (child.getAttribute('contenteditable') === 'false') continue;
      if (child.tagName === 'BR') { if (child.nextSibling) out.push('\\n'); continue; }
      if (blocks[child.tagName] && out.length && !out[out.length - 1].endsWith('\\n')) out.push('\\n');
      walk(child);
    }
  };
  walk(root);
  return { text: out.join(''), mentions: mentions };
}"""
EXEC_INSERT_JS: str = "(text) => document.execCommand('insertText', false, text)"


async def read_editor(session: BrowserSession) -> EditorSnapshotDao:
    editor = await require(session, "editor")
    raw = await editor.evaluate(SNAPSHOT_JS, session.page_map.get("mention_node").css)
    return EditorSnapshotDao(text=str(raw["text"]), mentions=tuple(str(name) for name in raw["mentions"]))


async def clear_editor(session: BrowserSession) -> None:
    editor = await require(session, "editor")
    await editor.click(timeout=ms(session.timeouts.action_s))
    await press_keys(session, "editor_clear")


async def fill_editor(session: BrowserSession, segments: Sequence[FillSegmentDao]) -> None:
    """Clear, then type every segment. Never presses Enter: line breaks follow `timeouts.newline`."""
    await guard(session, "editor")
    await clear_editor(session)
    await session.page.keyboard.press("Control+End")
    for segment in segments:
        if segment.mention is None:
            await _insert_text(session, segment.text)
            await _dismiss_popup(session)
        else:
            await _insert_mention(session, segment.mention)


async def fill_negative(session: BrowserSession, text: str) -> bool:
    field = locate(session, "negative_field")
    if not await is_visible(field):
        return False
    await field.first.fill(text, timeout=ms(session.timeouts.action_s))
    return True


async def _insert_text(session: BrowserSession, text: str) -> None:
    keyboard = session.page.keyboard
    strategy = session.timeouts.insertion
    for index, line in enumerate(text.split("\n")):
        if index > 0:
            if session.timeouts.newline is NewlineMode.SHIFT_ENTER:
                await keyboard.press("Shift+Enter")
            else:
                await keyboard.insert_text("\n")
        if not line:
            continue
        if strategy is InsertionStrategy.INSERT_TEXT:
            await keyboard.insert_text(line)
        elif strategy is InsertionStrategy.EXEC_COMMAND:
            await session.page.evaluate(EXEC_INSERT_JS, line)
        else:
            for part_index, part in enumerate(line.split("\t")):
                if part_index > 0:
                    await keyboard.insert_text("\t")
                if part:
                    await keyboard.type(part)


async def _insert_mention(session: BrowserSession, name: str) -> None:
    keyboard = session.page.keyboard
    await keyboard.insert_text("@")
    await keyboard.insert_text(name)
    popup = locate(session, "mention_popup").first
    timeout = ms(session.timeouts.mention_popup_s)
    try:
        await popup.wait_for(state="visible", timeout=timeout)
        await named(session, "mention_option_by_name", name).first.click(timeout=timeout)
    except PlaywrightTimeoutError:
        await _dismiss_popup(session)


async def _dismiss_popup(session: BrowserSession) -> None:
    if await is_visible(locate(session, "mention_popup")):
        await press_keys(session, "popover_close")
