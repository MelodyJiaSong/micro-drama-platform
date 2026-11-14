"""Rewrite t01 panel prompts with imaginative-but-truthful VFX (follow-up 032)."""
import json
from pathlib import Path

SB = Path(r"C:\workspace\micro-drama-platform\edu_videos\tansuo\t01_inside_a_chip\storyboard")
d = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
BGA = "a small flat square black chip package with smooth edges and no pins or leads on its sides"

V = {
 "P01": ("Cold open in a sunlit study, golden afternoon light with dust motes glittering in the sunbeams. Kai sits leaning in, holding "
         f"{BGA} (about one centimeter, no markings) in fine tweezers close to his eye, squinting. An opened generic smartphone circuit board lies on the desk. "
         "Lin stands beside him with a knowing smile and lifts her left wrist: the watch dial is just beginning to glow, a first thin ring of warm amber light "
         "spreading from it into the air like a ripple on water. Medium close shot, chip in sharp focus in the foreground.",
         "探索表启动：第一道琥珀色刻度涟漪"),
 "P02": ("The signature shrinking effect: from Lin's raised wrist watch, concentric rings of warm amber light expand outward through the air like ripples, "
         "each ring etched with fine evenly spaced ruler tick marks (no numbers). Inside the rings the two characters are mid-shrink, already the height of a grain of rice, "
         "faint light trails streaming off their silhouettes. Around them the desk world rushes up to giant size: wood grain becomes deep canyons, dust motes hang like floating boulders "
         f"lit by a sunbeam, a pencil lies like a fallen log, and {BGA} towers nearby like a low black building. Kai flails, startled, hair lifted; Lin is calm. Low wide-angle macro shot.",
         "标志特效：琥珀刻度涟漪＋缩小光迹"),
 "P03": ("Under the edge of a chip package at a scale where its solder balls are giant: a neat grid of huge mirror-polished silver solder spheres holds up the flat, completely solid, "
         "opaque matte-black package above like the columns of a cathedral. Each sphere reflects the two tiny characters and the light. A shaft of light slants in from the open side, "
         "full of slowly drifting glittering dust particles. Kai points up at the dark package overhead; Lin smiles and gestures inward. The background shows only more solder spheres, "
         "small surface-mount components and the green board fading into haze; no copper wire towers, no glass structures. Low angle, awe-inspiring.",
         "镜面焊球＋光束里的浮尘"),
 "P04": ("Exploded-view effect: the chip package is splitting apart in mid-air into its real layers, each layer floating slightly apart from the next with a glowing thin white edge "
         "along every cut face: from bottom to top — green circuit board, a row of large silver solder balls, the layered package substrate with thin copper traces, a dense row of small "
         "copper bumps, a thin flat slab of grey silicon face-down, and the black mold cap lifting away at the top. Small fragments and sparks of light drift between the separating layers. "
         "The two characters stand on the substrate layer, looking up as the thin silicon slab hovers just above their heads. Dramatic, clean, readable.",
         "爆炸分解：封装按真实层次分开，切面白边"),
 "P05": ("The two characters stand on a vast flat grey silicon chip surface stretching to the horizon under soft even light, no sky. Lin sweeps her hand across the landscape and "
         "large translucent glowing color regions paint themselves across the floor like light spilling over the ground, each region a different soft tint (blue, green, violet, amber) "
         "with crisp edges, revealing the chip's functional areas; the regions follow the subtle underlying textures (a regular tiled grid in one, fine irregular texture in another). "
         "Broad metal power stripes cross the surface like low roads. Kai, wide-eyed, steps back as the light flows past his feet. Wide high-angle shot.",
         "示意色块像光一样铺满地面"),
 "P06": ("The two characters ride downward standing on a small square copper plate sinking through the wiring layers of a microchip, like a glass-free elevator. "
         "Huge thick copper beams with rectangular cross-sections slide upward past them, catching warm light; below, layer after layer of progressively thinner and denser copper lines "
         "spread out, each layer running perpendicular to the one above, receding into a deep glowing abyss. Soft volumetric light pours down from the opening above, "
         "and fine reflections sparkle off the copper. Looking-down perspective, sense of descent and vastness.",
         "下降电梯：体积光从上方倾泻"),
 "P07": ("A vast orderly city of wiring layers inside a microchip: dense parallel copper wires with rectangular cross-sections, alternate layers perpendicular, short square vias connecting them, "
         "clear glassy insulation between. Bright cold blue-white streaks of light race along some of the wires like night traffic on highways (the electrical signal), while inside the wires "
         "a slow haze of tiny warm amber specks drifts lazily (the electrons). Kai stands on a wire, face lit blue, pointing in awe; Lin stands calmly beside him. Characters small in frame.",
         "信号＝蓝白光迹飞驰；电子＝琥珀光点慢漂"),
 "P08": ("Among the copper wires inside a microchip, a single colossal ribbon of light sweeps through the scene like an aurora, a smooth rolling wave with soft rainbow bands; "
         "its wavelength is clearly wider than several copper wires together, so the wires beneath it dissolve into a soft blur as it passes. Kai holds up his smartphone to photograph "
         "the wires but its screen shows only a featureless blur, and he frowns, puzzled; Lin explains with an open palm, her face washed in rainbow light. Gentle humor, breathtaking scale.",
         "光波像极光缎带，宽过好几根导线"),
 "P09": ("The bottom level of a microchip: rows of identical equal-height cells separated by flat metal rails; thin vertical gate lines stand in a perfectly regular fence-like array, "
         "each about as tall as the characters, tiny contacts rising to thin copper lines just overhead, cool blue-grey silicon below. As Lin walks between two gate rows, a soft wave of "
         "warm light ripples along the gates in sequence, each gate briefly glowing at its base where it meets the silicon, like switches flicking on one after another. Kai trails behind, "
         "touching a gate line with curiosity, its glow reflecting on his hand. Strong rhythm and perspective.",
         "栅极依次亮起的开关涟漪（示意）"),
 "P10": ("Close view of a single gate-all-around transistor: three to four thin flat horizontal sheets of blue-grey silicon stacked with even gaps, passing straight through a block of dark "
         "steel-grey gate metal that wraps completely around each sheet with a very thin pale insulating layer; source and drain blocks at either end. A thin glowing channel of warm amber light "
         "is just forming inside the sheets, a stream of tiny amber specks beginning to flow from one end to the other. Kai peers into the gap between sheets, his face lit amber, amazed and puzzled; "
         "Lin points at the wrapping gate. Each character about as tall as the stack.",
         "导电通道刚刚形成：琥珀光点开始流动（下一期伏笔）"),
 "P11": ("Atomic scale: the cut edge of one thin silicon sheet seen as a vast crystal lattice of evenly spaced blue-grey spheres in a diamond-cubic arrangement, atomic layers countable, "
         "extending into the distance like a crystal cathedral. Each atom is wrapped in a faint shimmering translucent electron cloud, and thin glowing bonds link neighbors. "
         "Kai kneels and counts the layers with one finger, astonished, the shimmer reflected in his eyes; Lin crouches beside him, smiling. Cinematic soft light, shallow depth of field.",
         "原子带电子云微光，晶格像水晶大教堂"),
 "P12": ("Kai and Lin sit side by side on the edge of a stack of thin blue-grey silicon sheets, legs dangling over a deep glowing view of the transistor rows below, tiny amber specks "
         "drifting up like fireflies. Kai holds up one hand with fingers spread, guessing a number with a playful confident grin; Lin raises an eyebrow, amused, about to reveal the answer. "
         "Warm, light-hearted, medium shot.",
         "坐在纳米片边缘，下方萤火般的光点"),
 "P13": ("Fast zoom-out through every scale at once: the two characters shoot upward through a tunnel of streaking light where all the levels flash past in sequence — glowing atoms, "
         "rows of gates, copper wire layers, mirror solder spheres — while concentric amber ruler-tick rings rush inward toward them. Bright light opens above. Kai whoops with arms out, hood flapping; "
         "Lin holds her glasses in place, laughing. Dynamic vertical composition, intense speed.",
         "回程隧道：各层尺度闪过＋刻度涟漪收拢"),
 "P14": ("Back at the sunlit desk at normal size, golden light: Kai holds his smartphone and looks at it with new eyes, a thoughtful smile; for a moment a faint warm amber glow shows through "
         "the phone's back where its chip sits, like an echo of the journey. Lin leans on the desk edge, satisfied, arms folded, the last thin amber ring fading from her watch. "
         f"{BGA.capitalize()} rests on the desk in the foreground.",
         "手机背后一闪琥珀余光，表盘最后一圈涟漪消散"),
}
for p in d["panels"]:
    prompt, vfx = V[p["id"]]
    p["prompt"] = prompt
    p["vfx"] = vfx
    if p["id"] == "P03":
        p["style_ref"] = False
d["version"] = "v3"
(SB / "panels.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

g = (SB / "gen_panels.py").read_text(encoding="utf-8")
old = ('"shallow depth of field, anamorphic film look, natural color grade. Not cartoon, not 3D animation style, not neon, not sci-fi, no glowing circuits, no holograms.")')
assert old in g
g = g.replace(old, '"shallow depth of field, anamorphic film look. Spectacular, imaginative visual effects like a big-budget science documentary feature: volumetric light, particles, light trails, bloom; '
              'the effects depict real phenomena (light, electric signals, electrons, change of scale, structures splitting apart). Not cartoon, not 3D animation style. '
              'Structures stay physically plausible: no decorative fake circuit patterns, no floating UI, no holographic text.")')
(SB / "gen_panels.py").write_text(g, encoding="utf-8")

b = (SB / "build_review.py").read_text(encoding="utf-8")
old = 'desc = f"拍 {p[\'beat\']} · 比例尺 {p[\'scale\']} · {p[\'source\']}\\n" + "\\n".join(p["lines"])'
assert old in b
b = b.replace(old, 'desc = f"拍 {p[\'beat\']} · 比例尺 {p[\'scale\']} · {p[\'source\']}\\n特效：{p.get(\'vfx\', \'—\')}\\n" + "\\n".join(p["lines"])')
(SB / "build_review.py").write_text(b, encoding="utf-8")
print("ok")
