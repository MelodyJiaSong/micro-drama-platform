"""t01 follow-up 057: generate missing storyboard candidates via audited Codex entry."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
SB = Path(__file__).resolve().parent
ns = {}
exec((SB / 'build_preview.py').read_text(encoding='utf-8').split('beats = {}')[0], ns)
VISUALS = ns['VISUALS']
PLAN = ns['SCENE_PLAN']

POSES = {
    'city_reveal': ('An immense aerial view of a rectangular silicon die. Dense rectilinear metal routes and functional blocks resemble a night city, but no real roads, buildings or cars. The die edges are barely visible at the edge of frame, ready for the later reveal. Cold blue signal highlights on a few selected routes, warm copper. Pure structural view.', False),
    'transistor_answer': ('Warm daylight workshop desk, medium two-shot. Lin calmly explains with one open hand; Kai leans toward the tiny loose packaged sample held by tweezers. A separate intact working unbranded smartphone lies beside it. Curious, skeptical expression on Kai. No shrink rings yet.', True),
    'tap_close': ('Extreme closeup of Kai index finger about to touch the intact unbranded phone screen on the wooden desk. Screen has only abstract blurred color shapes, no legible text. Background softly shows the separate loose sample in tweezers on the desk. A tiny cold blue-white signal glint starts at the touch point.', True),
    'watch_rule': ('Medium closeup of Lin lifting her LEFT forearm across her chest and looking at her round black watch, whose face has blank amber radial ticks without numbers. Her right hand is empty and down. Kai stands slightly behind, surprised. Warm workshop desk background. One subtle amber concentric scale ripple starting from the watch.', True),
    'black_package': ('Low wide view from a green motherboard. A matte black rectangular chip package rises like a low broad building, solder balls partly visible underneath. Kai looks up at the black lid; Lin points toward its underside with her right hand, LEFT watch visible on relaxed left arm. Package overwhelmingly larger than both people.', True),
    'solder_detail': ('Macro side cutaway of ONE silver solder ball touching the pad below a thin redistribution layer and the motherboard pad below. Surrounding solder balls fade into depth. Distinct insulating substrate, contact pad and solder interfaces; no decorative columns or flanges. No people.', False),
    'solder_power': ('Top-down oblique underside of a packaged die: orderly silver solder-ball array above a green board. Three separated groups highlighted in restrained white-blue, amber and neutral gray to suggest distinct electrical nets, no labels. Every ball remains silver. No fake glowing circuitry outside actual connections, no people.', False),
    'die_flip': ('Oblique three-quarter exploded packaging demonstration: a thin flat silicon die tilted halfway toward face-up, the patterned active face visible, above the separated thin redistribution layer and silver solder-ball array. Keep thickness small compared with width. Only a single die; no organic thick multilayer slab. No people.', False),
    'die_colors': ('High oblique aerial of a rectangular flat silicon die surface. Subtle translucent false-color functional regions begin fading away, revealing the SAME gray surface beneath. Regions are flat overlays, not physical neon city towers. No people. Leave dark quiet margin for later captions.', False),
    'die_bottom': ('Macro sectional view through a silicon die: many copper interconnect layers above a fine dark gray transistor layer at the bottom, on continuous gray silicon substrate. Camera poised to descend. A clean white cut edge marks removed material. No wiring under the substrate. No people.', False),
    'region_switch_question': ('On a large flat silicon die: Kai asks Lin where the switches are, medium two-shot at surface level. Lin gestures down toward the surface. Very subtle broad false-color regions in distant background; no visible giant transistors on the top surface. Both characters occupy less than one third of image.', True),
    'wiring_layers': ('Clean vertical cutaway through twelve copper wiring layers in clear dielectric: top wires broad and widely spaced; lower wires narrow and dense. Each successive layer physically separate, short square via plugs selectively connect adjacent layers. Substrate and fine transistor layer visible at bottom. Straight engineering geometry, no people.', False),
    'vias_close': ('Extreme macro of two crossing copper routes at DIFFERENT heights. A clear pale dielectric volume fills the gap between the crossing, keeping the wires electrically separate. A second nearby selected intersection has one short square copper via joining the adjacent layers. The non-contact crossing and selected via both clearly visible. No people, no vertical chimney or flanges.', False),
    'electron_drift': ('Macro cutaway inside a straight copper wire: sparse amber electron markers distributed throughout the metal, stationary or with tiny local drift tails. A separate thin cool-blue pulse front near the left end represents the propagating field change. Amber dots remain inside conductor, never race along with pulse. No people.', False),
    'subway_analogy': ('In the interconnect environment, waist-up two-shot: Kai leans his shoulder slightly sideways to mime a small crowded-subway movement, Lin listens with a small amused smile. No train appears physically inside the chip. Copper routes remain stable background, no shove chain or violent movement.', True),
    'wavelength': ('Scientific optical-scale composition, no people. A broad translucent rainbow sinusoidal wave ribbon spans several tiny parallel gray nanostructure ridges below. One full wave period is visibly about ten ridge spacings. The wave is an explanatory overlay, does not bend or deform the ridges. Leave lower dark margin for exact scale overlay.', False),
    'microscope_gray': ('Pure grayscale, electron-microscope-inspired schematic rendered view of nanoridges and thin contacts, oblique macro. It must look like a 3D explanatory model, not a claimed real micrograph; no SEM UI, scale text, stamps or fake machine readings. All material color absent. No people.', False),
    'gray_reaction': ('Closeup of Kai surprised, looking off-camera at a gray rendered chip structure. His skin and navy clothing keep natural color, while the nanostructure behind him is grayscale. Lin is only a soft shoulder at frame edge. This demonstrates false-color removal from structure, not turning the whole world or actors gray.', True),
    'gate_pitch': ('Overhead orthographic-like macro view of six identical parallel gate bars across gray silicon channels. Each bar has a precise central white hairline locator, two adjacent center locators slightly brighter. Bars and gaps are not equal-width. No measurement numerals or arrows, exact 50 nm center spacing will be added later. No people.', False),
    'process_name': ('Kai kneels beside a gray gate-bar array, holding a small blank measuring strip above it, puzzled as he tries to find what a process name measures. Lin stands at the edge, gently explaining. No literal car in the chip, no numeral three anywhere. Make instrument visibly a schematic measuring aid.', True),
    'nanosheet': ('Oblique cutaway of one gate-all-around transistor on gray silicon substrate. Three parallel, continuous thin GRAY SILICON ribbons run horizontally from a left source block through the central gate to a right drain block. Central dark metal gate wraps all four sides of each ribbon, including between ribbons and under lowest ribbon. A narrow front wedge of gate metal is removed solely for viewing, rim marked white. Very thin pale insulating skin separates gate metal from every silicon ribbon. No glass silicon, no empty gate windows, no copper underneath, no people.', False),
    'relay_compare': ('Macro photographed historical electromagnetic relay on a dark tabletop, no people. Copper solenoid coil, hinged metal armature, small clearly separated electrical contact tips. Contact currently OPEN with visible air gap, armature not yet pulled. Practical real device, no invented glowing holograms.', False),
    'static_transistor_reaction': ('Kai crouches near a static gray three-nanosheet transistor, searching for a mechanical handle with a puzzled expression. Lin remains to his side, hands relaxed. Entire transistor stays solid and unmoving; gate cutaway marked white. People about twice total gate height, structures dominate two thirds of image.', True),
    'off_state': ('One N-channel nanosheet transistor cutaway, no people. Continuous three gray silicon ribbons connect left source and right drain; central metal gate wraps each via thin pale insulator. Sparse amber electron markers in source and drain, few in central channel. NO continuous amber path yet. Silicon physically unbroken. Dark gate with no blue activation highlight. White cut edges clearly mark removed gate wedge.', False),
    'channel_material': ('Tight longitudinal view through ONE continuous gray silicon ribbon connecting left and right reservoirs. Thin pale insulating skin above and below, dark gate metal outside it with front cutaway removed. Sparse amber electron markers only, no continuous lit path; emphasize uninterrupted silicon material even though channel is off. No literal road, no people.', False),
    'channel_not_road': ('Tight macro of continuous gray silicon ribbon with a faint dotted ghost-road overlay hovering above it, already dissolving, leaving the solid ribbon unchanged. A few amber carrier markers inside silicon suggest the coming channel, no physical bridge being built. Dark gate cutaway surrounds ribbon through insulating skin. No people.', False),
    'insulator': ('Very close transverse cut section of a rectangular gray silicon nanosheet, wrapped by an extremely thin pale insulating film, surrounded outside by thick dark gray gate metal. The silicon cross section has rounded corners; film follows all four sides continuously. Color and texture distinguish three materials. White cut edge. No carrier crossing the insulator, no people.', False),
    'electrons_gather': ('Longitudinal nanosheet cutaway at BEGINNING of gate voltage increase. Continuous gray ribbon between source and drain, thin insulating skin, outer dark gate metal. Some amber carrier markers are starting to accumulate INSIDE silicon near its boundary, but not yet a complete bright channel. Faint cool-blue field shading crosses insulating film, not amber electrons. No people.', False),
    'electrons_disperse': ('Longitudinal nanosheet cutaway in initially ON state immediately BEFORE voltage removal: a narrow continuous band of amber carrier markers inside gray silicon connects source and drain. Gate and silicon solid, thin pale dielectric continuous. This is starting pose for later dispersion, not an animation montage. No people.', False),
    'channel_cycle': ('Longitudinal cutaway of nanosheet transistor, continuous gray silicon from source to drain. At start of this shot, positive gate bias has just drawn many amber electrons into a barely continuous channel INSIDE silicon. All geometry fixed. Insulating skin unbroken; no amber particles in gate or dielectric. Composition supports later off transition at second line. No people.', False),
    'field_force': ('Medium close two-shot beside enlarged transistor cutaway: Kai points toward the gap of the thin insulating skin, genuinely puzzled; Lin calmly prepares to answer. Gate and gray silicon separated by the pale film. No magnet yet, no physical touching of electrons. Lin watch on LEFT only.', True),
    'field_question': ('Static gate cross-section in foreground with gray silicon, pale insulating film and dark metal. Kai at frame edge studies it, surprised that nothing mechanical moved; Lin listens. Gate remains off, no moving lever, no magnet in this starting frame.', True),
    'magnet_analogy': ('Practical macro tabletop analogy, no people visible except a single neutral right hand moving a small plain bar magnet UNDER a thin wooden tabletop. A small cluster of iron filings sits on TOP directly above it. Side cutaway perspective makes the intervening solid wood obvious. No arrows, no electricity bolts, no levitation. Not inside the chip.', False),
    'switch_realization': ('Close reaction two-shot at transistor scale, Kai half-smiles in sudden understanding, palms relaxed; Lin gives a matter-of-fact small smile. Static nanosheet model in soft background, no levers. Only her LEFT wrist has a black watch. Warm amber fill and cool metal rim.', True),
    'wrap_question': ('Low three-quarter view around one cutaway gate-all-around transistor. Kai leans to inspect the side and underside of central gate, Lin points at the gate surrounding individual gray ribbons. Pale dielectric separates them. Show gate metal between sheets and under lowest, not an empty arch. Characters to frame edge, model dominates.', True),
    'leakage': ('Close gate-all-around cutaway on gray substrate, no people. Gray ribbons, pale insulator and dark wrapping gate. Mostly dark off-state channel with only a few faint amber carrier markers suggesting small residual leakage, not a full bright conducting band. Keep materials solid; no literal holes or dripping fluid.', False),
    'evolution': ('Three separate transistor teaching models arranged left-to-right on a continuous neutral dark plinth, no people: planar silicon channel under flat gate; raised vertical silicon FIN with gate crossing its top and two sides; three stacked horizontal silicon nanosheets wrapped individually by gate on all four sides. Gray silicon, dark gate, pale thin dielectric, white cutaway edges. Models not morphing into one another, no labels, no arrows. Equal presentation scale, schematic not same dimensional scale.', False),
    'tap_arrival': ('Kai turns excitedly toward a thin cold blue-white signal highlight arriving along a TOP metal connection to the gate of the transistor near him. Lin follows his gaze. Distinct source-drain silicon path below; do not show a blue ray passing through insulator as an electron wire. Make signal an overlaid glint on an actual conductor.', True),
    'voltage_01': ('Minimal cinematic explanatory backdrop: dark gray chip plane with TWO separate circuit output nodes presented as metal pads, one softly cold blue-white and one dim neutral. No switch lever, no numerals or text. Generous negative space above and below for exact high/low voltage labels added by code later. No people.', False),
    'inverter': ('Clean dark neutral studio with a faint photoreal copper circuit-board surface, deliberately sparse. Empty central area reserved for an exact CMOS inverter circuit to be drawn later in postproduction; absolutely no invented circuit symbols, text, numbers or extra components. No people. This is a background plate, not the diagram itself.', False),
    'atom_count': ('Medium over-shoulder shot of Kai and Lin viewing a clearly framed large rectangular magnifying display at the side of a gray nanosheet model. The display interior is plain dark neutral EMPTY space reserved for exact silicon lattice compositing, not a physical wall of giant atoms. Kai points at display with RIGHT index finger. Lin stands facing display with BOTH arms relaxed; her LEFT wrist has the only round black watch, right wrist bare. Both people remain transistor-scale; the screen is a graphic magnification window. Realistic faces and fixed clothing. No atomic balls, no text, no diagram on empty display.', True),
    'atom_thickness': ('Macro composition of a thin gray silicon nanosheet cut face, with a large dark clean rectangular inset area to its right reserved for a physically computed 44-layer silicon lattice. Sheet remains continuous, upper and lower pale insulator clearly bounded. No people, no approximate AI atom rows, no text. This is a plate for precise later lattice overlay.', False),
    'scale_answer': ('Close-up on Lin LEFT wrist holding her round black exploration watch in foreground, Kai looking amazed in soft background beside the nanosheet model. Watch face has a single subtle amber radial ring with no digits or letters. Frame leaves generous dark area for later numerical scale calculation. Right wrist bare. No additional watches.', True),
    'reverse_zoom': ('Kai standing on gray transistor-scale substrate gestures outward to the huge grid of devices beyond, eyebrows raised, asking how large the whole chip would become. Lin beside him follows his gesture. Two people each roughly twice the nearby gate height. Horizon begins a dramatic pullback, no actual world city or buildings inside chip.', True),
    'beijing_area': ('Extreme aerial panorama over a dense flat transistor array extending to a hazy distant horizon, rectangular organization, no people. Broad dark negative area in upper third reserved for later area comparison. No literal Beijing city landmarks, no skyline, no giant humans, no invented numbers.', False),
    'pocket_beijing': ('Medium closeup Kai holds his intact unbranded phone in one hand while looking astonished at it, Lin smiles beside him. They are still in the transistor array environment. Keep one side of frame clear and dark for later comparison graphic, no city physically emerging from phone, no text.', True),
    'next_episode': ('Warm daylight workshop desk matching the start. Kai begins to touch his intact phone screen again with an eager questioning smile; Lin smiles, ready for next visit. Loose chip sample on desk. Medium two-shot with empty right third for end-card overlays. No readable logos, text or digits, no shrink ripple yet.', True),
}


def job(key, version):
    out = SB / 'frames' / f'{key}_{version}.png'
    if out.exists():
        return {'key':key,'status':'exists','path':str(out.relative_to(ROOT))}
    pose, cast = POSES[key]
    visual = VISUALS[key]
    refs = []
    if cast:
        refs = [ROOT / f'edu_videos/tansuo/_shared/cast/{c}/turnaround.png' for c in ('lin','kai')]
    prompt = 'Create ONE polished 16:9 landscape cinematic storyboard keyframe, not a grid, not a montage. Photorealistic science documentary mood, precise simple readable composition, material realism, restrained film lighting.\n' + pose
    if cast:
        prompt += '\nReference 1 is Lin, reference 2 is Kai. Preserve their identity, faces, hair and clothing. They are fictional adults. Lin: low black bun, no glasses, light-gray jacket with amber cuff stripes, white tee, charcoal trousers, gray shoes. Her ONLY watch is on her anatomical LEFT wrist. Kai: dark brown wavy hair, navy hoodie, khaki cargo pants, white shoes, sand bag slung from left shoulder to right hip. Do not swap faces or clothes.'
    prompt += '\nThis is a conceptual storyboard composition, not a measured scientific model. Any exact scale bar, numbers, color key and schematic label is added separately later. No text, no letters, no numbers, no logos, no watermark. Do not depict approximate AI atom counts as precise data. Return one single full-bleed landscape image.'
    pf = SB / 'prompts' / 'generation' / f'{key}_{version}.txt'
    pf.parent.mkdir(parents=True,exist_ok=True)
    out.parent.mkdir(exist_ok=True)
    pf.write_text(prompt,encoding='utf-8')
    cmd = [sys.executable,str(ROOT/'tools/codex_image.py'),'--out',str(out),'--prompt-file',str(pf)]
    for ref in refs:
        cmd += ['--ref',str(ref)]
    proc = subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (pf.with_suffix('.log')).write_text(proc.stdout+'\n'+proc.stderr,encoding='utf-8')
    return {'key':key,'status':'candidate' if proc.returncode==0 and out.exists() else 'failed_no_retry','path':str(out.relative_to(ROOT)).replace('\\','/'),'prompt':str(pf.relative_to(ROOT)).replace('\\','/'),'returncode':proc.returncode,'error':proc.stderr[-500:] if proc.returncode else ''}


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('keys',nargs='*')
    ap.add_argument('--version',default='r1')
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--list',action='store_true')
    a=ap.parse_args()
    used={s['visual'] for c in PLAN for s in c['shots']+c.get('en_shots',[])}
    missing=sorted(k for k in used if not VISUALS[k]['image'])
    assert not (set(missing)-set(POSES)-{'scale_guess','array_signal'}), set(missing)-set(POSES)
    if a.list:
        print(json.dumps(missing,ensure_ascii=False,indent=2))
        raise SystemExit()
    keys=a.keys or [k for k in missing if k not in {'atom_count','atom_thickness','inverter','voltage_01'}]
    audit=SB/'frames'/'generation_results.jsonl'
    audit.parent.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        tasks={ex.submit(job,k,a.version):k for k in keys}
        for f in as_completed(tasks):
            result=f.result()
            with audit.open('a',encoding='utf-8') as output:
                output.write(json.dumps(result,ensure_ascii=False)+'\n')
            print(json.dumps(result,ensure_ascii=False),flush=True)
