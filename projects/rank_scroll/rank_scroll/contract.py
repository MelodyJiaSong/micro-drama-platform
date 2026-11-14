"""Load and validate an episode directory against ai_videos/paihangbang/data_contract.md (v1.3)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ICONS = {"mountain", "calendar", "building", "stairs", "map-pin", "ruler", "flag", "trophy", "users", "globe", "sparkles", "cpu",
         "virus", "vaccine", "skull", "droplet", "bug", "wind", "biohazard", "paw", "glass-full", "hand-stop", "bottle"}   # follow-up 007 (ep05 viruses)
ACCEPTED_LICENCE_PREFIXES = ("public domain", "pd", "cc0", "cc by", "cc-by",
                             "pexels license", "unsplash license", "pixabay content license",   # 后三者可商用、免署名（paihangbang follow-up 007）
                             "ai-generated")   # Codex image_gen，最后手段；上传时勾选合成内容声明（paihangbang follow-up 020）
REJECTED_LICENCE_MARKERS = ("nc", "nd", "gfdl")
LIMITS = {"badge": 22, "tag": 24, "insight": 90, "source_line": 70, "image_note": 48, "scope_note": 600,
          "corner": 12, "person_name": 28, "person_role": 32}
MODES = {"rank", "list"}   # list (v1.3, rank_scroll follow-up 004): file order left→right, no rank shown, no champion
TALLY_BY = {"country", "continent"}
IMAGE_FITS = {"cover", "contain"}
CARD_STYLES = ("poster", "split", "duo", "polaroid", "spotlight")   # layout.card_style（paihangbang follow-up 055）
CARD_W_DEFAULT, CARD_W_MIN, CARD_W_MAX = 600, 480, 800   # layout.card_w; multiple of 8 keeps the band on even pixels

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FLAG_DIR = REPO_ROOT / "ai_videos" / "paihangbang" / "_assets" / "flags"


@dataclass
class Tag:
    icon: str
    text: str


@dataclass
class Item:
    rank: int
    name: str
    subtitle: str
    country_iso2: str
    country_name: str
    continent: str
    value: float
    value_display: str
    secondary_display: str = ""
    badge: str = ""
    tags: list[Tag] = field(default_factory=list)
    image: Path | None = None
    image_credit: str = ""
    image_note: str = ""          # shown on the placeholder card when there is no photo
    image_withheld: bool = False  # photo exists but was withheld (image_risk) for this render
    image_ai: bool = False        # ledger licence "AI-generated …": card shows an AI IMAGE chip (rank_scroll follow-up 010)
    image_focus: tuple[float, float] = (0.5, 0.35)  # cover-crop focus (x, y in 0..1) of the full-bleed photo
    image_fit: str = "cover"      # "contain"：整图放入、同图虚化填空（rank_scroll follow-up 016 / paihangbang 061）
    # v1.3 company card (optional): top-right label, logo plate, founder headshot circle
    corner: str = ""
    logo: Path | None = None
    logo_bg: str = "#ffffff"
    person_name: str = ""
    person_role: str = ""
    person_image: Path | None = None
    person_credit: str = ""
    person_focus: tuple[float, float] = (0.5, 0.3)
    thumb: bool = False
    inset_image: Path | None = None    # 第二张图（v1.5，paihangbang follow-up 055）：duo 版式的圆形小图，如大米的生米粒特写
    inset_credit: str = ""
    inset_label: str = ""

    @property
    def company_card(self) -> bool:
        return self.logo is not None or bool(self.person_name)


@dataclass
class Insight:
    after_rank: int
    text: str


@dataclass
class Episode:
    root: Path
    episode: str
    title: str
    kicker: str
    metric_label: str
    unit: str
    period_label: str
    source_line: str
    theme: str
    tally_by: str
    tally_title: str
    items: list[Item]
    insights: list[Insight]
    flag_dir: Path = DEFAULT_FLAG_DIR
    scope_note: str = ""
    card_w: int = CARD_W_DEFAULT  # card width in 1080p px (height is fixed); wider suits landscape photos
    mode: str = "rank"
    show_flags: bool = True   # layout.flags=false (follow-up 007): no flags anywhere, country_iso2 may be ""
    tally_icons: dict = field(default_factory=dict)   # tally.icons: group -> icon (rank_scroll follow-up 009)
    lang: str = "en"          # data.{lang}.json 的语言（follow-up 015）
    tally_labels: dict = field(default_factory=dict)   # tally.labels: 计分板分组键 → 显示名；不取条目上的 country_name
    intro_hold: float = 0.0   # layout.intro_hold (s, follow-up 008): band stands still after the slide-in so the first card is readable
    card_style: str = "poster"   # layout.card_style（v1.5，paihangbang follow-up 055）：poster / split / duo / polaroid / spotlight

    @property
    def is_list(self) -> bool:
        return self.mode == "list"

    def flag_path(self, iso2: str) -> Path:
        return self.flag_dir / f"{iso2.lower()}.png"


class ContractError(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = errors


def _licence_ok(lic: str) -> bool:
    low = lic.strip().lower()
    if not low.startswith(ACCEPTED_LICENCE_PREFIXES):
        return False
    tokens = low.replace("-", " ").split()
    return not any(m in tokens for m in REJECTED_LICENCE_MARKERS)


# 大陆版：台湾 / 香港 / 澳门是中国的地区，不得以独立国家的代码、国旗或计分出现（paihangbang follow-up 046）
ZH_FORBIDDEN_ISO = {"TW", "HK", "MO"}


def load_episode(ep_dir: str | Path, flag_dir: Path | None = None, strict_images: bool = False,
                 allow_risk_images: bool = False, lang: str = "en") -> tuple[Episode, list[str]]:
    """Return (episode, warnings). Raise ContractError listing every hard error."""
    root = Path(ep_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    data_path = root / ("data.json" if lang == "en" else f"data.{lang}.json")
    if not data_path.is_file():
        raise ContractError([f"missing {data_path}"])
    try:
        d: dict[str, Any] = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ContractError([f"data.json is not valid JSON: {e}"]) from e

    for key in ("episode", "title", "kicker", "metric_label", "unit", "period_label", "source_line", "items"):
        if key not in d:
            errors.append(f"data.json missing top-level field '{key}'")
    if errors:
        raise ContractError(errors)
    if len(d["source_line"]) > LIMITS["source_line"]:
        errors.append(f"source_line longer than {LIMITS['source_line']} chars")

    mode = d.get("mode", "rank")
    if mode not in MODES:
        errors.append(f"mode must be one of {sorted(MODES)}")
        mode = "rank"
    tally = d.get("tally") or {"by": "country", "title": "Tally"}
    if tally.get("by") not in TALLY_BY:
        errors.append(f"tally.by must be one of {sorted(TALLY_BY)}")

    ledger_files: dict[str, dict] = {}
    ledger_path = root / "assets.json"
    if ledger_path.is_file():
        try:
            for entry in json.loads(ledger_path.read_text(encoding="utf-8")):
                ledger_files[str(entry.get("file", "")).replace("\\", "/")] = entry
        except json.JSONDecodeError as e:
            errors.append(f"assets.json is not valid JSON: {e}")
    else:
        warnings.append("assets.json missing: every image will be rejected")

    fdir = flag_dir or DEFAULT_FLAG_DIR
    show_flags = (d.get("layout") or {}).get("flags", True)
    if not isinstance(show_flags, bool):
        errors.append("layout.flags must be true or false")
        show_flags = True
    intro_hold = (d.get("layout") or {}).get("intro_hold", 0)
    if isinstance(intro_hold, bool) or not isinstance(intro_hold, (int, float)) or not 0 <= intro_hold <= 6:
        errors.append("layout.intro_hold must be a number of seconds 0..6")
        intro_hold = 0
    lf = (d.get("layout") or {}).get("focus", [0.5, 0.35])   # episode default crop focus (towers: keep the top)
    if not (isinstance(lf, list) and len(lf) == 2 and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in lf)):
        errors.append("layout.focus must be [x, y] with 0..1 values")
        lf = [0.5, 0.35]
    default_focus = (float(lf[0]), float(lf[1]))
    items: list[Item] = []
    prev_rank = 0
    for i, raw in enumerate(d["items"]):
        where = f"items[{i}]"
        for key in ("rank", "name", "country_iso2", "country_name", "value", "value_display"):
            if key not in raw:
                errors.append(f"{where} missing '{key}'")
        if any(k not in raw for k in ("rank", "name", "country_iso2", "value", "value_display")):
            continue
        rank = raw["rank"]
        if not isinstance(rank, int) or rank < 1:
            errors.append(f"{where} rank must be a positive int")
            continue
        if mode == "list" and rank != i + 1:
            errors.append(f"{where} rank must equal its position {i + 1} in list mode")
        if rank < prev_rank:
            errors.append(f"{where} rank {rank} out of order (items must be ascending)")
        if rank > prev_rank + 1 and prev_rank and rank != i + 1:
            warnings.append(f"{where} rank jumps from {prev_rank} to {rank}")
        prev_rank = rank
        badge = raw.get("badge") or ""
        if len(badge) > LIMITS["badge"]:
            errors.append(f"{where} badge longer than {LIMITS['badge']}: {badge!r}")
        tags: list[Tag] = []
        for t in raw.get("tags") or []:
            if t.get("icon") not in ICONS:
                errors.append(f"{where} unknown icon {t.get('icon')!r}")
            if len(t.get("text", "")) > LIMITS["tag"]:
                errors.append(f"{where} tag text longer than {LIMITS['tag']}: {t.get('text')!r}")
            tags.append(Tag(t.get("icon", "globe"), t.get("text", "")))
        if len(tags) > 2:
            errors.append(f"{where} has more than 2 tags")
        iso = str(raw["country_iso2"]).lower()
        if iso.upper() in ZH_FORBIDDEN_ISO:        # 中英文版一律（paihangbang follow-up 047）
            errors.append(f"{where} 中文版不得使用 {iso.upper()} 的国家代码 / 旗（台湾、香港、澳门是中国的地区：country_iso2 用 CN，名称写「中国台湾」/「Taiwan, China」等）")
        if show_flags and not (fdir / f"{iso}.png").is_file():
            errors.append(f"{where} flag not found for {iso!r} in {fdir}")
        img: Path | None = None
        rel = raw.get("image")
        withheld = False
        note = str(raw.get("image_note") or "")
        if len(note) > LIMITS["image_note"]:
            errors.append(f"{where} image_note longer than {LIMITS['image_note']}")
        credit = str(raw.get("image_credit") or "")
        image_ai = False
        use_alt = False
        if rel and raw.get("image_risk") and not allow_risk_images:
            if raw.get("image_alt"):
                # image_alt (v1.4, paihangbang follow-up 020): a commercially safe substitute that
                # replaces the withheld risk photo in the default master, so no tile is left empty.
                rel, credit, use_alt = raw["image_alt"], str(raw.get("image_alt_credit") or ""), True
            else:
                warnings.append(f"{where} image withheld (image_risk): {raw.get('name')}")
                rel, withheld = None, True
                note = note or "Photo withheld: architecture copyright"
        if rel:
            rel_norm = str(rel).replace("\\", "/")
            p = (root / rel_norm).resolve()
            if not p.is_file():
                (errors if strict_images else warnings).append(f"{where} image missing: {rel_norm}")
            elif rel_norm not in ledger_files:
                errors.append(f"{where} image {rel_norm} not listed in assets.json")
            # 标了 image_risk 的图只在 --allow-risk-images（人已签字放行）时走到这里，此时许可未知也放行（paihangbang follow-up 009）
            elif (use_alt or not raw.get("image_risk")) and not _licence_ok(str(ledger_files[rel_norm].get("licence", ""))):
                errors.append(f"{where} image licence not accepted: {ledger_files[rel_norm].get('licence')!r}")
            else:
                img = p
                image_ai = str(ledger_files[rel_norm].get("licence", "")).strip().lower().startswith("ai-generated")
        elif not withheld:
            (errors if strict_images else warnings).append(f"{where} has no image ({raw.get('name')})")
        focus = raw.get("image_focus")
        if focus is None:
            focus_t = default_focus
        elif (isinstance(focus, list) and len(focus) == 2
              and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in focus)):
            focus_t = (float(focus[0]), float(focus[1]))
        else:
            errors.append(f"{where} image_focus must be [x, y] with 0..1 values")
            focus_t = (0.5, 0.35)
        fit = str(raw.get("image_fit") or "cover")
        if fit not in IMAGE_FITS:
            errors.append(f"{where} image_fit must be one of {sorted(IMAGE_FITS)}")
            fit = "cover"
        corner = str(raw.get("corner") or "")
        if len(corner) > LIMITS["corner"]:
            errors.append(f"{where} corner longer than {LIMITS['corner']}: {corner!r}")
        logo: Path | None = None
        if raw.get("logo"):
            lrel = str(raw["logo"]).replace("\\", "/")
            lp = (root / lrel).resolve()
            if not lp.is_file():
                errors.append(f"{where} logo missing: {lrel}")
            elif lrel not in ledger_files:
                errors.append(f"{where} logo {lrel} not listed in assets.json")
            elif ledger_files[lrel].get("kind") != "logo":
                errors.append(f"{where} logo {lrel}: assets.json entry needs kind='logo' (trademark, identification only)")
            else:
                logo = lp
        person = raw.get("person") or {}
        pname, prole = str(person.get("name") or ""), str(person.get("role") or "")
        if len(pname) > LIMITS["person_name"]:
            errors.append(f"{where} person.name longer than {LIMITS['person_name']}")
        if len(prole) > LIMITS["person_role"]:
            errors.append(f"{where} person.role longer than {LIMITS['person_role']}")
        pimg: Path | None = None
        pcredit = ""
        if person.get("image"):
            prel = str(person["image"]).replace("\\", "/")
            pp = (root / prel).resolve()
            if person.get("image_risk") and not allow_risk_images:
                warnings.append(f"{where} person photo withheld (image_risk): {pname}")
            elif not pp.is_file():
                (errors if strict_images else warnings).append(f"{where} person image missing: {prel}")
            elif prel not in ledger_files:
                errors.append(f"{where} person image {prel} not listed in assets.json")
            elif not person.get("image_risk") and not _licence_ok(str(ledger_files[prel].get("licence", ""))):
                errors.append(f"{where} person image licence not accepted: {ledger_files[prel].get('licence')!r}")
            else:
                pimg, pcredit = pp, str(person.get("credit") or "")
        pf = person.get("focus", [0.5, 0.3])
        pfocus = (float(pf[0]), float(pf[1])) if isinstance(pf, list) and len(pf) == 2 else (0.5, 0.3)
        inset: Path | None = None
        irel = raw.get("inset_image")
        if irel:
            irel = str(irel).replace("\\", "/")
            ip = (root / irel).resolve()
            if not ip.is_file():
                (errors if strict_images else warnings).append(f"{where} inset image missing: {irel}")
            elif irel not in ledger_files:
                errors.append(f"{where} inset image {irel} not listed in assets.json")
            elif not _licence_ok(str(ledger_files[irel].get("licence", ""))):
                errors.append(f"{where} inset image licence not accepted: {ledger_files[irel].get('licence')!r}")
            else:
                inset = ip
        if len(str(raw.get("inset_label") or "")) > LIMITS["badge"]:
            errors.append(f"{where} inset_label longer than {LIMITS['badge']}")
        items.append(Item(
            rank=rank, name=str(raw["name"]), subtitle=str(raw.get("subtitle") or ""),
            country_iso2=iso, country_name=str(raw.get("country_name", iso.upper())),
            continent=str(raw.get("continent") or ""), value=float(raw["value"]),
            value_display=str(raw["value_display"]), secondary_display=str(raw.get("secondary_display") or ""),
            badge=badge, tags=tags[:2], image=img, image_credit=credit if img else "",
            image_note=note, image_withheld=withheld, image_ai=image_ai and img is not None, image_focus=focus_t, image_fit=fit,
            corner=corner, logo=logo, logo_bg=str(raw.get("logo_bg") or "#ffffff"),
            person_name=pname, person_role=prole, person_image=pimg, person_credit=pcredit, person_focus=pfocus,
            thumb=bool(raw.get("thumb")),
            inset_image=inset, inset_credit=str(raw.get("inset_credit") or "") if inset else "",
            inset_label=str(raw.get("inset_label") or ""),
        ))
    if not items:
        errors.append("no items")
    if tally.get("by") == "continent":
        for it in items:
            if not it.continent:
                errors.append(f"rank {it.rank} has no continent but tally.by=continent")

    insights: list[Insight] = []
    ranks = {it.rank for it in items}
    for j, raw in enumerate(d.get("insights") or []):
        text = str(raw.get("text", ""))
        ar = raw.get("after_rank")
        if len(text) > LIMITS["insight"]:
            errors.append(f"insights[{j}] longer than {LIMITS['insight']} chars")
        if ar not in ranks:
            errors.append(f"insights[{j}] after_rank {ar} is not an item rank")
        elif mode == "rank" and ar == min(ranks):
            errors.append(f"insights[{j}] cannot come after the champion")
        elif mode == "list" and ar == max(ranks):
            errors.append(f"insights[{j}] cannot come after the last item")
        insights.append(Insight(int(ar or 0), text))

    if len(str(d.get("scope_note") or "")) > LIMITS["scope_note"]:
        errors.append(f"scope_note longer than {LIMITS['scope_note']}")
    card_w = (d.get("layout") or {}).get("card_w", CARD_W_DEFAULT)
    if not isinstance(card_w, int) or not CARD_W_MIN <= card_w <= CARD_W_MAX or card_w % 8:
        errors.append(f"layout.card_w must be an int {CARD_W_MIN}..{CARD_W_MAX}, multiple of 8")
        card_w = CARD_W_DEFAULT
    card_style = (d.get("layout") or {}).get("card_style", "poster")
    if card_style not in CARD_STYLES:
        errors.append(f"layout.card_style must be one of {CARD_STYLES}")
        card_style = "poster"
    if errors:
        raise ContractError(errors)
    tally_icons = tally.get("icons") or {}
    if not isinstance(tally_icons, dict) or any(v not in ICONS for v in tally_icons.values()):
        errors.append("tally.icons must map group names to known icon names")
        tally_icons = {}
    if errors:
        raise ContractError(errors)
    ep = Episode(
        root=root, episode=str(d["episode"]), title=str(d["title"]), kicker=str(d["kicker"]),
        metric_label=str(d["metric_label"]), unit=str(d["unit"]), period_label=str(d["period_label"]),
        source_line=str(d["source_line"]), theme=str(d.get("theme") or "default"),
        tally_by=str(tally.get("by")), tally_title=str(tally.get("title") or "Tally"),
        items=items, insights=insights, flag_dir=fdir, scope_note=str(d.get("scope_note") or ""),
        card_w=card_w, mode=mode, show_flags=show_flags, intro_hold=float(intro_hold), tally_icons=tally_icons,
        lang=lang, tally_labels=dict(tally.get("labels") or {}), card_style=card_style,
    )
    return ep, warnings
