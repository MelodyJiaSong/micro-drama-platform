"""Theme tokens (bible §2.5: a skin may only change these)."""
from __future__ import annotations

from dataclasses import dataclass


def hex_color(h: str, alpha: int = 255) -> int:
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (alpha << 24) | (r << 16) | (g << 8) | b


@dataclass(frozen=True)
class Theme:
    name: str
    bg_top: str
    bg_bottom: str
    header_text: str
    header_muted: str
    card: str
    card_text: str
    card_muted: str
    strip: str
    strip_text: str
    accent: str
    accent_text: str
    value_text: str
    insight_bg: str
    insight_text: str
    divider: str


THEMES: dict[str, Theme] = {
    "default": Theme("default", "#0f1729", "#1d2b4a", "#ffffff", "#9fb0cf", "#ffffff", "#111827", "#6b7280",
                     "#111827", "#ffffff", "#f5a524", "#111827", "#111827", "#f5a524", "#111827", "#e5e7eb"),
    "skyline": Theme("skyline", "#070b18", "#1b2340", "#ffffff", "#a5b1d6", "#ffffff", "#0f172a", "#64748b",
                     "#0f172a", "#ffffff", "#ffb547", "#1a1205", "#0f172a", "#ffb547", "#1a1205", "#e2e8f0"),
    "alpine": Theme("alpine", "#0b2540", "#2a5f86", "#ffffff", "#b9d3ea", "#ffffff", "#0c2236", "#5b7187",
                    "#0c2236", "#ffffff", "#3fb6ff", "#04121f", "#0c2236", "#e9f6ff", "#0c2236", "#dde7f0"),
    # paihangbang ep04 largest land animals: dusk savanna, warm amber accent
    "savanna": Theme("savanna", "#1a1208", "#4a3214", "#ffffff", "#e3cfa8", "#ffffff", "#24180a", "#7a6648",
                     "#24180a", "#ffffff", "#ffb02e", "#1f1404", "#24180a", "#fff4dc", "#24180a", "#efe4cf"),
    # paihangbang ep03 AI companies: deep indigo night, electric cyan accent
    "tech": Theme("tech", "#070817", "#1a1446", "#ffffff", "#a9b4e6", "#ffffff", "#0d0b26", "#646a8f",
                  "#0d0b26", "#ffffff", "#36e2ff", "#03141a", "#0d0b26", "#e8fbff", "#0d0b26", "#e1e5f5"),
    # paihangbang ep06 best-selling manga: ink black to deep crimson, hanko-red accent
    "manga": Theme("manga", "#0c0a0d", "#3a0d16", "#ffffff", "#e3c3c9", "#ffffff", "#140a0d", "#73606a",
                   "#140a0d", "#ffffff", "#ff3b4e", "#ffffff", "#140a0d", "#fff0f2", "#140a0d", "#ece3e5"),
    # paihangbang ep11–ep20 (follow-up 015): one skin per episode, added together so the
    # parallel episode agents never edit this file.
    # ep11 largest ships: deep sea navy, hull-orange accent
    "maritime": Theme("maritime", "#06182a", "#0f3a5c", "#ffffff", "#a6c4dc", "#ffffff", "#071a2b", "#5a7186",
                      "#071a2b", "#ffffff", "#ff6b3d", "#1a0800", "#071a2b", "#eaf4fb", "#071a2b", "#dbe6ef"),
    # ep12 largest countries by area: atlas green, map-gold accent
    "atlas": Theme("atlas", "#0e2116", "#2c5136", "#ffffff", "#bcd3b8", "#ffffff", "#10241a", "#5f7564",
                   "#10241a", "#ffffff", "#e9c46a", "#1c1503", "#10241a", "#f7f1dc", "#10241a", "#e3e9df"),
    # ep13 tallest statues: dark stone, bronze accent
    "monument": Theme("monument", "#14110d", "#3d3326", "#ffffff", "#d8c9ae", "#ffffff", "#1d1810", "#7a6c55",
                      "#1d1810", "#ffffff", "#d4a24c", "#1a1203", "#1d1810", "#f6eedd", "#1d1810", "#ece4d6"),
    # ep14 highest volcanoes: basalt black, lava accent
    "magma": Theme("magma", "#120706", "#3e120b", "#ffffff", "#e6b5a6", "#ffffff", "#1f0b07", "#7d5a52",
                   "#1f0b07", "#ffffff", "#ff5a1f", "#1f0700", "#1f0b07", "#fff0e8", "#1f0b07", "#efe0db"),
    # ep15 deepest lakes: abyssal teal, glacier-cyan accent
    "abyss": Theme("abyss", "#021318", "#06404d", "#ffffff", "#9fcfd6", "#ffffff", "#03181d", "#4f6f74",
                   "#03181d", "#ffffff", "#2fd4c6", "#021412", "#03181d", "#e3faf8", "#03181d", "#d9e9ea"),
    # ep16 largest stadiums: floodlit pitch green, neon-lime accent
    "arena": Theme("arena", "#061509", "#14421f", "#ffffff", "#b7d8bd", "#ffffff", "#0a1d0f", "#5b725f",
                   "#0a1d0f", "#ffffff", "#c6ff3d", "#121a00", "#0a1d0f", "#f3ffe0", "#0a1d0f", "#e0eadf"),
    # ep17 longest rivers: river-delta blue, sky-blue accent
    "delta": Theme("delta", "#081a26", "#1d5066", "#ffffff", "#aacbdb", "#ffffff", "#0a1e2b", "#56707e",
                   "#0a1e2b", "#ffffff", "#4fc3f7", "#03141d", "#0a1e2b", "#e6f6fe", "#0a1e2b", "#dce8ee"),
    # ep18 fastest cars: carbon black, racing-red accent
    "velocity": Theme("velocity", "#0b0b0e", "#2a2a33", "#ffffff", "#c2c2cc", "#ffffff", "#111114", "#66666f",
                      "#111114", "#ffffff", "#ff2d3d", "#ffffff", "#111114", "#fff0f1", "#111114", "#e6e6ea"),
    # ep19 most visited countries: sunset violet, warm coral accent
    "voyage": Theme("voyage", "#1a0f24", "#3f2a5c", "#ffffff", "#cfbde3", "#ffffff", "#1d1229", "#6e5f80",
                    "#1d1229", "#ffffff", "#ff9f68", "#1f0d02", "#1d1229", "#fff1e8", "#1d1229", "#e8e1ef"),
    # ep20 tallest waterfalls: mossy gorge, spray-mint accent
    "cascade": Theme("cascade", "#0a1f1a", "#1e4d40", "#ffffff", "#b0d6c9", "#ffffff", "#0c231d", "#587269",
                     "#0c231d", "#ffffff", "#8ef0d2", "#03170f", "#0c231d", "#e8fcf5", "#0c231d", "#dce9e4"),
    # ep05 deadliest viruses: lab-dark, biohazard-green accent (follow-up 007)
    "virus": Theme("virus", "#05080d", "#10202a", "#ffffff", "#a9c4c9", "#ffffff", "#071014", "#5d7378",
                   "#071014", "#ffffff", "#7cff6b", "#04120a", "#071014", "#ecffe9", "#071014", "#dfe9e6"),
}


def get_theme(name: str) -> tuple[Theme, str | None]:
    if name in THEMES:
        return THEMES[name], None
    return THEMES["default"], f"unknown theme {name!r}; using default"
