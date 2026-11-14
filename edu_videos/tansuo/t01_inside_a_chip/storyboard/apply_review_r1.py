"""按独立审稿 r1（reviews/r1.md）改 panels.json 与 gen_panels.py：结构锁定短语、去掉画风参考图、逐格修正。"""
import json
from pathlib import Path

SB = Path(__file__).resolve().parent
d = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
P = {p["id"]: p for p in d["panels"]}


def rep(pid, old, new):
    assert old in P[pid]["prompt"], (pid, old[:40])
    P[pid]["prompt"] = P[pid]["prompt"].replace(old, new)


def add(pid, text):
    P[pid]["prompt"] += " " + text


# P03 焊球
rep("P03", "like the columns of a cathedral", "like a low covered hall")
rep("P03", "more solder spheres, small surface-mount components and the green board fading into haze",
    "more solder spheres and the green board fading into haze")
add("P03", "Each solder ball is a solid opaque silver metal sphere slightly flattened top and bottom, firmly joined to the board pad below and to the underside "
    "of the black package above; no rims, no necks, no flared bases, not glass; the package underside is a low ceiling resting directly on top of the balls, "
    "gap height equals ball height; no components under the package footprint.")
# P04 封装分解
rep("P04", "Small fragments and sparks of light drift between the separating layers.", "Only faint glints along the cut edges.")
add("P04", "The small copper bumps sit only directly beneath the silicon die footprint, matching its outline; the rest of the substrate top is flat. "
    "The cut face of the substrate shows a few thin horizontal copper layers stacked in resin with small vertical vias, no circuit-board trace patterns. "
    "No orbiting light trails, no shattered glass shards. Matte dark grey silicon with a faint metallic sheen, clearly opaque.")
# P05 硅片表面
rep("P05", "large translucent glowing color regions paint themselves across the floor like light spilling over the ground, each region a different soft tint (blue, green, violet, amber) "
    "with crisp edges, revealing the chip's functional areas; the regions follow the subtle underlying textures (a regular tiled grid in one, fine irregular texture in another). "
    "Broad metal power stripes cross the surface like low roads.",
    "translucent color light washes across the floor like light spilling over the ground, in soft blue, green and violet zones with crisp edges (no amber), "
    "revealing the chip's functional areas; only a faint flat regular grid is visible under the blue zone.")
add("P05", "A perfectly flat featureless matte grey silicon plain: no copper beams, no pillars, no raised blocks or city structures.")
# P06 下降
add("P06", "The copper wires passing them are horizontal rectangular bars seen sliding upward edge-on, layer by layer, each layer perpendicular to the one above; "
    "no vertical copper columns, no round pipes; no amber dots on the wires.")
# P07 导线城市
add("P07", "Every wire stays flat within its own layer, straight with only right-angle turns; changes between layers happen only through vias. "
    "Kai points up at the wires in awe, his face lit blue; Lin stands calmly beside him with her hands relaxed.")
# P08 拍不到
add("P08", "Over-the-shoulder view of Kai's phone: we see its screen facing Kai, showing only a featureless soft blur; the camera lenses are on the back facing the wires, "
    "not visible; generic phone with a simple vertical dual-lens camera, no brand-like design.")
# P09 栅极
rep("P09", "thin vertical gate lines stand in a perfectly regular fence-like array, each about as tall as the characters,",
    "gates are long thin parallel walls running across the floor at equal spacing, each wall crossing over low horizontal silicon channels that run perpendicular beneath them, "
    "gate height only about one to two times the gap between gates (about as tall as the characters), no isolated square posts, no pedestals,")
rep("P09", "each gate briefly glowing at its base where it meets the silicon", "each gate glowing only at its base where it meets the silicon channel")
# P10 晶体管
rep("P10", "three to four thin flat horizontal sheets of blue-grey silicon stacked with even gaps, passing straight through a block of dark steel-grey gate metal that wraps completely "
    "around each sheet with a very thin pale insulating layer; source and drain blocks at either end.",
    "three separate flat silicon nanosheets, stacked with even gaps, each running straight from the source block on the left through the middle of the gate to the drain block "
    "on the right; the dark steel-grey gate metal fills the gaps and wraps all four sides of each sheet in the middle section, with a very thin pale insulating layer around each "
    "sheet; no U-turns, no folded ribbon.")
rep("P10", "A thin glowing channel of warm amber light is just forming inside the sheets, a stream of tiny amber specks beginning to flow from one end to the other.",
    "A thin glowing channel of warm amber light is just forming inside the silicon sheets themselves (not in the gaps), tiny amber specks beginning to flow from source to drain.")
# P11 晶格
add("P11", "Silicon diamond-cubic lattice viewed along the [110] direction: atoms in paired zigzag rows, each atom with four bonds to its neighbors; "
    "the full thickness of the sheet is visible from top surface to bottom surface so its forty-odd atomic layers can be counted.")
# P12 坐在晶体管上
P["P12"]["prompt"] = ("Kai and Lin sit side by side on top of a single nanosheet transistor whose stack of three to four thin grey silicon sheets wrapped in dark gate metal "
                      "is about as tall as a standing person, legs dangling over its edge. Below the stack there is only the plain grey silicon substrate; no copper, no wiring "
                      "and no other transistors below. Tiny amber specks drift up like fireflies. Kai holds up one hand with fingers spread, guessing a number with a playful "
                      "confident grin; Lin raises an eyebrow, amused, about to reveal the answer. Warm, light-hearted, medium shot.")
P["P12"]["scale"] = "50 nm"
# P13 只改 prompt（图不重出）
rep("P13", "Lin holds her glasses in place, laughing", "Lin holds a loose strand of hair from her face with her left hand, laughing")

FIX = ["P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12"]
for pid in FIX:
    P[pid]["style_ref"] = False
    P[pid]["retries"] = P[pid].get("retries", 0) + 1
d["review"] = "r1 → 10 格重出（第 1 次），P13 只改 prompt，P01/P02/P14 不动"
(SB / "panels.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

g = (SB / "gen_panels.py").read_text(encoding="utf-8")
old = '"clear glassy insulating material with subtle refraction, contacts and gate metal dark steel grey.")'
assert old in g
g = g.replace(old, '"clear glassy insulating material with subtle refraction, contacts and gate metal dark steel grey. '
              'Vias are short square plugs no wider than the wires, connecting only adjacent layers; no tall round copper columns, no flanges, no glass rings around vias; '
              'clear glassy insulation fills the space between wires.")')
old2 = '"Kai: young man of mixed'
g = g.replace(old2, '"Lin wears her single round black watch on her LEFT wrist only, nothing on her right wrist, and never wears glasses. "\n         ' + old2)
# 不挂画风参考图时也要带上材料与结构短语（芯片内部格）
old3 = '    if p.get("style_ref"):\n        parts.append(MAT)\n        refs.append(ROOT / spec["style_ref"])'
assert old3 in g
g = g.replace(old3, '    if p.get("style_ref"):\n        refs.append(ROOT / spec["style_ref"])\n    if p["id"] not in ("P01", "P02", "P14"):\n        parts.append(MAT)')
(SB / "gen_panels.py").write_text(g, encoding="utf-8")
print("ok", FIX)
