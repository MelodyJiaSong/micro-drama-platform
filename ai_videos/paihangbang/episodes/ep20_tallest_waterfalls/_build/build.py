# -*- coding: utf-8 -*-
"""ep20 data.json 生成：python -I build.py（在 _build/ 下）。
数据来自 raw/wwd_top.json（WWD 抓取）+ items_def.py（入选与主值覆盖）+ 本文件 EXTRA（徽章、标签、出处、交叉核对、认图提示）。
已有 data.json 时保留 image / image_credit / image_focus / image_risk / image_note / image_alt*（找图结果不被重建覆盖）。"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS, VALUE_OVERRIDE  # noqa: E402

TODAY = "2026-11-03"
WIKI_LIST = "https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845"
CONT = {"VE": "South America", "PE": "South America", "ZA": "Africa", "CH": "Europe", "NO": "Europe", "CA": "North America",
        "US": "North America", "NZ": "Oceania", "FR": "Africa"}   # 法国条目均在留尼汪（非洲东侧印度洋）


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("ø", "o").replace("Ø", "O").replace("å", "a").replace("æ", "ae"))
    return re.sub(r"[^a-z0-9]+", "_", s.encode("ascii", "ignore").decode().lower()).strip("_")


def wl(v):  # Wikipedia 列表交叉核对
    return {"name": "Wikipedia: List of waterfalls by height (rev 1379783845)", "url": WIKI_LIST, "value": v}


# 每项补充：badge / tags / cross / notes / hint / source（覆盖默认 WWD 来源）
EXTRA: dict[str, dict] = {
    "Kerepakupai-Meru-1": dict(
        badge="HEIGHT DISPUTED", tags=[("ruler", "807 m main drop"), ("trophy", "Guinness record")],
        source={"name": "Guinness World Records: Tallest waterfall (1949 survey, 979 m)", "url": "https://www.guinnessworldrecords.com/world-records/highest-waterfall"},
        cross={"name": "World Waterfall Database (counts only the 807 m main plunge)", "url": "https://www.worldwaterfalldatabase.com/waterfall/Kerepakupai-Meru-1", "value": 807},
        notes="979 m = 1949 survey of an expedition funded by National Geographic (Ruth Robertson), recognised by Guinness. WWD argues the survey was sighted from the Río Carrao/Caroní ~2 km away and includes ~170 m of river below the falls; it lists only the 807 m main plunge (−17.6%, >10%: kept 979 by our 'published survey/record first' rule — user to confirm). Guinness itself notes that if only 807 m counts, Tugela (948 m) is the tallest. Wikipedia list: 979 m.",
        hint="Angel Falls / Salto Ángel (Kerepakupai Merú), Auyán-tepui, Canaima National Park, Bolívar, Venezuela: ONE ultra-tall white ribbon free-falling from the flat-topped sandstone tepui wall into green jungle, mist at the base; classic full-height view from Mirador Laime / Ratoncito island or from a plane, rainy-season flow. NOT Kaieteur Falls (Guyana, wide river fall), NOT Kukenán or Roraima tepui falls, NOT Iguazú."),
    "Tugela-Falls-2": dict(
        badge="SEASONAL", tags=[("ruler", "Longest drop 411 m"), ("stairs", "5 tiers")],
        source={"name": "World Waterfall Database: Tugela Falls (total height 948 m); same figure in Guinness World Records", "url": "https://www.worldwaterfalldatabase.com/waterfall/Tugela-Falls-2"},
        cross=wl(947),
        notes="WWD flow consistency 4 months (rainy season, Nov–Mar); WWD status 'Unconfirmed' but the 948 m figure is the one Guinness quotes, so it passes our 'independent record' rule. 2016 Czech team (Petr Jan Juračka) measured 983 m, but WWD says from >1 km below the falls; not used. Lower tiers hidden in a gorge; true height not settled.",
        hint="Tugela Falls, the Amphitheatre escarpment, Royal Natal National Park (Maloti-Drakensberg), KwaZulu-Natal, South Africa: thin white multi-tier ribbon leaping off the huge basalt Amphitheatre cliff, summer (green grass, flowing water); full-height view from the Tugela Gorge trail / valley looking up at the Amphitheatre, or from the top near the chain ladders. NOT frozen winter ice shots, NOT Howick Falls, NOT Maletsunyane Falls (Lesotho)."),
    "Mattenbachfälle-27386": dict(
        badge="REMEASURED 2020", tags=[("stairs", "Tiered horsetails"), ("mountain", "Near Stechelberg")],
        cross=wl(840),
        notes="Earlier estimate 840 m (still in Wikipedia list, −9.7%). In 2020 the Vertical Water Canyoning Team abseiled the falls and measured ~930 m (WWD), making it the tallest in Eurasia. Tiny 0.9 km² catchment — can dry out in late-summer drought, so no SEASONAL badge (WWD gives no flow-months figure).",
        hint="Mattenbachfälle (Mattenbach falls), on the EAST wall of the Lauterbrunnen Valley near Stechelberg, Bernese Oberland, Switzerland: a very tall, thin, multi-tier white stream sliding down the sheer limestone valley wall above green meadows; full height of the wall visible, ideally early summer snowmelt. NOT Staubbach Falls (village of Lauterbrunnen, single plunge by the church), NOT Mürrenbach Falls (west wall), NOT Trümmelbach Falls (inside the mountain)."),
    "Yumbilla-Catarata-811": dict(
        tags=[("stairs", "4 tiers"), ("calendar", "IGN survey 2007")],
        source={"name": "Instituto Geográfico Nacional (Peru) laser survey 2007, 895.4 m (reported by MercoPress 2007-12-04; WWD)", "url": "https://en.mercopress.com/2007/12/04/the-world-s-third-highest-waterfall-discovered-in-peru"},
        cross={"name": "World Waterfall Database: Yumbilla (896 m)", "url": "https://www.worldwaterfalldatabase.com/waterfall/Yumbilla-Catarata-811", "value": 896},
        notes="IGN Peru laser survey 2007: 895.4 m (displayed 895 m). WWD 896 m, Wikipedia list 896 m. WWD status Unconfirmed, admitted under our independent-survey rule. Flow regime not documented (best in rainy season); no badge.",
        hint="Yumbilla waterfall (Catarata de Yumbilla), near Cuispes, Bongará province, Amazonas region, northern Peru (Chachapoyas area): a very tall chain of thin white falls down a sheer cliff in dense green cloud forest; full-height view from the Cuispes trail. NOT Gocta waterfall (two big tiers, Cocachimba), NOT Chinata or Pabellón falls."),
    "Skorga-11652": dict(
        badge="SEASONAL", tags=[("calendar", "Flows ~9 months/yr"), ("stairs", "Tiered horsetails")],
        cross=wl(875),
        notes="Height from 1-m contour maps (WWD, visited/catalogued). Only the lower ~600 m is visible from the valley floor. WWD flow consistency 9 months (best April–July).",
        hint="Skorga waterfall (also spelled Skorgafossen / Skorgefossen), Sunndalen valley just east of Sunndalsøra, Sunndal, Møre og Romsdal, Norway: a long white horsetail stream down the steep valley wall beside Vinnufossen; early-summer snowmelt flow; view from the valley floor road (Rv70). NOT Vinnufossen (the broader neighbour), NOT Skorga in Tafjord if different."),
    "Vinnufallet-11651": dict(
        badge="SEASONAL", tags=[("ruler", "Longest drop 575 m"), ("calendar", "Flows ~9 months/yr")],
        cross=wl(845),
        notes="WWD (2026-10-13) says the recognised name is Vinnu (Vinnufallet) and calls Vinnufossen incorrect; kept the widely used name Vinnufossen on screen. Earlier WWD estimate 865 m, revised to 845 m. Glacier-fed; flow consistency 9 months (best May–Sept).",
        hint="Vinnufossen (Vinnufallet), above Sunndalsøra, Sunndal, Møre og Romsdal, Norway: fed by the Vinnu glacier, it shoots out of a crevice at the top of the valley wall then fans out into a wide white veil (150 m broad) down the mountainside; summer view from the Rv70 road / Sunndalsøra. NOT Skorga (neighbouring thinner fall)."),
    "James-Bruce-Falls-1191": dict(
        tags=[("mountain", "Glacier-fed")],
        cross=wl(840),
        notes="WWD: tallest fall it has catalogued in North America; small glacial source likely sustains year-round flow, but volume is low. No flow-months figure; no badge.",
        hint="James Bruce Falls, head of Princess Louisa Inlet (Jervis Inlet), British Columbia, Canada: a very tall, thin white thread high on the granite cliffs above the inlet, partly in a crevice; view from a boat on Princess Louisa Inlet or the Loquilts Creek trail. NOT Chatterbox Falls (the famous wide lower fall at the inlet's head)."),
    "Browne-Falls-18": dict(
        tags=[("stairs", "6 tiers")],
        cross=wl(836),
        notes="WWD: falls drop out of Lake Browne at 836 m straight to Doubtful Sound; Te Ara and older sources give 619 m (2,031 ft) (−26%, >10%: WWD figure kept, it follows the topographic lake level). Year-round flow (WWD high-volume months 12).",
        hint="Browne Falls, above Hall Arm, Doubtful Sound (Patea), Fiordland National Park, New Zealand: steep white tiered cascades zig-zagging down a rainforest-covered fiord wall straight into the dark sea; view from a Doubtful Sound cruise boat. NOT Helena Falls (Deep Cove), NOT Milford Sound's Stirling or Bowen Falls."),
    "Kjerrskredfossen-5552": dict(
        badge="SEASONAL", tags=[("calendar", "Flows ~7 months/yr"), ("stairs", "6+ tiers")],
        cross=None,
        notes="Two side-by-side streams; surveyed by WWD in 2011. Not in the Wikipedia list (no second source). Flow consistency 7 months (best March–June).",
        hint="Kjerrskredfossen, Nærøydalen valley just southwest of Gudvangen, Aurland, Vestland, Norway: two parallel white streams plunging and veiling in many tiers down the sheer 800 m cliffs of the Nærøy valley; spring snowmelt; view from the E16 / valley floor near Gudvangen. NOT Kjelfossen (the famous one right above Gudvangen at the fjord end), NOT Stalheimsfossen or Sivlefossen."),
    "Waihilau-Falls-639": dict(
        tags=[("ruler", "One single drop")],
        cross=wl(792),
        notes="Height = amphitheatre wall per USGS topo (WWD). Flow consistency 12 months.",
        hint="Waihilau Falls, headwall of the remote Waimanu Valley, Kohala coast, Hawaiʻi Island (Big Island), USA: three impossibly tall, slender white threads veiling down a vertical cliff covered in lush green vegetation; helicopter / aerial or valley-floor view. NOT Hiʻilawe Falls (Waipiʻo Valley), NOT Akaka Falls."),
    "Colonial-Creek-Falls-4738": dict(
        tags=[("stairs", "13 steps"), ("mountain", "Colonial Glacier")],
        cross=wl(788),
        notes="WWD triangulated 783 m in Aug 2011 (earlier topo estimate 788 m, still in Wikipedia list; Wikipedia article 783 m). Flows all year (WWD).",
        hint="Colonial Creek Falls, North Cascades National Park, Washington, USA: a long chain of 13 white cascades and plunges from the Colonial Glacier down a dark rock headwall above Diablo Lake's Thunder Arm, among glaciated peaks; view from the Colonial/Pyramid Peak area or aerial. NOT Diablo Lake alone, NOT Gorge Creek Falls or Ladder Creek Falls."),
    "Gocta-Catarata-805": dict(
        tags=[("ruler", "Lower drop 540 m"), ("calendar", "Measured 2006")],
        cross=wl(771),
        notes="Measured 771 m (±13 m) by a survey organised by Stefan Ziemendorff and the Peruvian government, announced 2006; known to locals for centuries but not to the outside world. Perennial (Wikipedia; WWD 12 months).",
        hint="Gocta waterfall (Catarata de Gocta), near Cocachimba / San Pablo, Bongará, Amazonas, Peru (Chachapoyas): two big white plunges, a smaller upper tier and a huge 540 m lower plunge, from a sheer cliff in green cloud-forest mountains; full two-tier view from the Cocachimba trail. NOT Yumbilla (thinner multi-tier), NOT Chinata."),
    "Kjelfossen-45": dict(
        badge="SEASONAL", tags=[("ruler", "Longest drop 198 m"), ("calendar", "Flows ~10 months/yr")],
        cross=wl(755),
        notes="WWD re-evaluated several times; current 765 m is for the centre stream (Vetle Kjelfossen). Wikipedia list 755 m (−1.3%). Flow consistency 10 months (best March–July).",
        hint="Kjelfossen, above the village of Gudvangen at the head of the Nærøyfjord, Aurland, Vestland, Norway: two or three parallel white streams dropping in many tiers down a towering cliff behind Gudvangen; view from Gudvangen village / the fjord. NOT Kjerrskredfossen (southwest in the valley), NOT Stalheimsfossen."),
    "Isella-Falls-4550": dict(
        tags=[("mountain", "Isella Glacier")],
        cross=None,
        notes="WWD estimate from topographic data: top tentatively at 6,650 ft, total ~762 m; could be taller. No second source. Glacier-fed; flow months not documented; no badge.",
        hint="Isella Falls, on the south face of Bonanza Peak above Railroad Creek near Holden Village, Glacier Peak Wilderness, Lake Chelan area, Washington, USA: many braided white meltwater streams sliding down the mountain from the Isella Glacier, merging into one; view from the Railroad Creek Trail. NOT Holden Lake, NOT Rainbow Falls (Stehekin)."),
    "Johannesburg-Falls-3083": dict(
        tags=[("ruler", "Final drop ~244 m"), ("mountain", "Johannesburg Mtn")],
        cross=wl(751),
        notes="WWD from USGS topo: just over 2,400 ft from the glacier, ending in a ~800 ft drop. Flow months not documented; no badge.",
        hint="Johannesburg Falls, on Johannesburg Mountain opposite the Cascade Pass trailhead, North Cascades National Park, Washington, USA: a white glacier-fed stream falling down the steep north face of Johannesburg Mountain, under hanging glaciers; classic view from the Cascade Pass parking lot. NOT Cascade Pass meadows only."),
    "Tjotafossen-415": dict(
        badge="SEASONAL", tags=[("mountain", "Tjøtabreen glacier"), ("calendar", "Flows ~9 months/yr")],
        cross=None,
        notes="WWD: ~750 m from the glacier toe; top shifts as the glacier advances/retreats. Flow consistency 9 months. No second source.",
        hint="Tjøtafossen, Oldedalen valley next to the Briksdal glacier, Stryn, Vestland, Norway: meltwater from Tjøtabreen zig-zags down a smooth granite wall, then spreads into a broad white veil over barren ground; summer view. NOT Briksdalsbreen glacier tongue itself, NOT Volefossen (by the Briksdal road)."),
    "Dontefossen-11": dict(
        tags=[("stairs", "3 sections"), ("map-pin", "Romsdalen")],
        cross=wl(700),
        notes="WWD from 1-m contour maps: 745 m in three sections; Wikipedia list and Norwegian Wikipedia ~700 m (−6%). Lakes above keep a fairly steady flow most of the year (frozen in winter); no flow-months figure, no badge.",
        hint="Døntefossen, Romsdalen valley between Flatmark and Verma, Rauma, Møre og Romsdal, Norway: a tall white fall in three sections (slabs, horsetail, final plunge) down the valley wall, seen from the E136 road across the Rauma river. NOT Vermafossen, NOT Mongefossen (dry), NOT Ølmåfossen."),
    "Yosemite-Falls-9": dict(
        badge="SEASONAL", tags=[("ruler", "Upper fall 436 m"), ("calendar", "Peak flow in spring")],
        cross={"name": "USGS: highest measured waterfall in North America, 2,425 ft (739 m)", "url": "https://www.usgs.gov/media/images/yosemite-falls-all-three-sections", "value": 739},
        notes="2,425 ft from François Matthes' 1913 USGS survey; WWD confirms with 1-m USGS lidar. Usually stops flowing in late summer/fall (WWD flow consistency 8 months).",
        hint="Yosemite Falls (Upper + Lower Yosemite Fall together), Yosemite Valley, Yosemite National Park, California, USA: the classic full view of both falls pouring off the granite wall in spring high flow, from Cook's Meadow / Swinging Bridge / the Merced River. NOT Bridalveil Fall, NOT Vernal or Nevada Fall, NOT Horsetail Fall (El Capitan), NOT lower-fall-only close-ups."),
    "Cloudcap-Falls-4959": dict(
        badge="SEASONAL", tags=[("mountain", "Mount Shuksan"), ("calendar", "Melt season only")],
        cross=wl(732),
        notes="WWD: ~2,400 ft of continuous bedrock cascades, almost all hidden in an incised channel; flows only during the melt season. Wikipedia calls it more seasonal than Seahpo Peak Falls.",
        hint="Cloudcap Falls, below Cloudcap Peak / Jagged Ridge on the east shoulder of Mount Shuksan, Sulphide Creek basin, North Cascades National Park, Washington, USA: a long white cascade down dark glaciated rock among glaciers; aerial view. NOT Seahpo Peak Falls, NOT Sulphide Creek Falls, NOT Mount Shuksan from Picture Lake."),
    "Boulder-Glacier-Falls-10285": dict(
        tags=[("mountain", "Boulder Glacier")],
        cross=None,
        notes="WWD: ~2,350 ft chain of falls and cascades at the head of Bowman Creek's valley; glacier nearly gone, may become seasonal. No second source; no badge.",
        hint="Boulder Glacier Falls, headwall at the upper end of the Bowman Creek valley below Boulder Peak / Boulder Pass, Glacier National Park, Montana, USA: a long chain of white falls and cascades down a huge rock headwall; view from the Boulder Pass trail or Hole-in-the-Wall area. NOT Bowman Lake alone, NOT Grinnell Glacier falls."),
    "Trou-de-Fer-Cascades-de-130": dict(
        tags=[("stairs", "4 tiers")],
        cross=wl(725),
        notes="WWD: initial horsetail ~213 m, then ~183 m, then ~305 m streams into the gorge and an ~24 m final plunge. Flows year-round (WWD 12 months). Réunion is an overseas region of France: flag = France.",
        hint="Trou de Fer, Réunion island (France, Indian Ocean): several white ribbon waterfalls plunging hundreds of metres into a deep, lush green volcanic gorge ('Iron Hole'); the classic helicopter view from above or the Bélouve forest viewpoint. NOT Cascade Niagara, NOT Langevin, NOT Voile de la Mariée (Salazie)."),
    "Yutaje-Salto-19": dict(
        tags=[("mountain", "Cerro Yutajé tepui")],
        cross=wl(671),
        notes="WWD: surveyed 715 m (survey source not named), satellite relief consistent. Wikipedia list 'Salto Yutaj' 671 m (−6.2%). Flows year-round (WWD).",
        hint="Salto Yutajé (Yutajé Falls), Cerro Yutajé tepui, Manapiare, Amazonas state, Venezuela: a tall white plunge off the flat-topped tepui into a deep jungle gorge; aerial or lodge-area view. NOT Angel Falls, NOT Salto Pará."),
    "Kjeragfossen-671": dict(
        badge="SEASONAL", tags=[("ruler", "Free fall 715 m"), ("calendar", "Snowmelt & rain only")],
        cross=wl(715),
        notes="Single near-free-falling plunge, tallest free leap in Europe (WWD). Flows only with snowmelt or heavy rain; about 5 months a year (Wikipedia).",
        hint="Kjeragfossen, from the Kjerag plateau into the Lysefjord, Sandnes, Rogaland, Norway: one long free-falling white plume dropping off a sheer granite cliff straight to the fjord; spring snowmelt; view from a Lysefjord boat / ferry to Lysebotn. NOT Kjeragbolten boulder, NOT Preikestolen."),
    "Tagfossen-6273": dict(
        badge="SEASONAL", tags=[("stairs", "Single horsetail"), ("calendar", "Flows ~8 months/yr")],
        cross=None,
        notes="WWD visited: one delicate horsetail of 710 m from a small lake; usually dry in late summer. Flow consistency 8 months. No second source.",
        hint="Tågfossen, Litldalen valley above lake Dalavatnet, Sunndal, Møre og Romsdal, Norway: a single long delicate white horsetail fall down very high sheer cliffs; view from the Litldalen road. NOT Vinnufossen or Skorga (Sunndalen)."),
    "Ølmåfossen-30753": dict(
        tags=[("mountain", "Trollveggen side")],
        cross=wl(720),
        notes="WWD: ~710 m veiling down the Trollveggen massif cliffs; Wikipedia list 720 m (+1.4%). Glacier and lakes; flow months not documented; no badge.",
        hint="Ølmåfossen, Romsdalen valley near Marstein, Rauma, Møre og Romsdal, Norway: a tall thin white fall veiling down the immense cliffs of the Trollveggen/Trolltindane massif, seen from the E136 / Marstein. NOT Mongefossen (dry, opposite side), NOT Trollveggen climbing shots without the waterfall."),
    "Cabin-Boy-Falls-22806": dict(
        tags=[("mountain", "Below Cloudmaker Lake")],
        cross=None,
        notes="WWD from 1:50,000 topo maps vs imagery: 700–750 m, possibly up to 800 m; listed at 701 m. Topo maps mark only a 124 m drop. No second source.",
        hint="Cabin Boy Falls, on the stream 'The Cabin Boy' below Cloudmaker Lake, Southern Alps, West Coast region, New Zealand (Mount Aspiring area): a long white fall down a steep glaciated valley wall in remote alpine terrain; aerial view."),
    "Balaifossen-633": dict(
        badge="SEASONAL", tags=[("calendar", "Flows ~7 months/yr"), ("map-pin", "Osafjord, Ulvik")],
        cross={"name": "Wikipedia list (as 'Balåifossen', old WWD estimate)", "url": WIKI_LIST, "value": 850},
        notes="Official name Sprænefossen (Norgeskart); formerly listed as Balåifossen 850 m — WWD's 2011 survey cut it to ~700 m (Wikipedia still shows 850, +21%). Low volume, may dry in late summer (WWD 7 months).",
        hint="Sprænefossen (formerly called Balåifossen), Osafjord near Ulvik, Hardanger, Vestland, Norway: a long chain of white falls skipping and veiling down the steep fjord wall onto an alluvial fan by the sea; early-summer snowmelt. NOT Vøringsfossen, NOT Skykkjedalsfossen, NOT Steinsdalsfossen."),
    "Lake-Unknown-Falls-699": dict(
        tags=[("ruler", "Top leap 150 m"), ("mountain", "Dart River valley")],
        cross=wl(680),
        notes="WWD: falls drop out of Lake Unknown in several leaps to the Dart River valley floor; NZ topo shows only the 150 m upper leap. Flow months not documented.",
        hint="Lake Unknown Falls, on the wall of the Dart River valley (Mount Aspiring National Park, near Glenorchy, Otago, New Zealand): a big white fall leaping down a forested valley wall from Lake Unknown, seen from Dart River jet-boat tours. NOT Earnslaw Burn falls, NOT Routeburn falls."),
    "Kukenaam-Salto-21": dict(
        badge="SEASONAL", tags=[("ruler", "Sheer plunge 674 m"), ("mountain", "Kukenán-tepui")],
        cross=wl(674),
        notes="674 m quoted from a Venezuelan National Park document (via WWD). WWD flow consistency 7 months. Often wrongly called one of the five tallest falls.",
        hint="Kukenán Falls (Salto Kukenán / Cuquenán), Kukenán-tepui (Matawi-tepui) beside Roraima, Gran Sabana, Canaima National Park, Bolívar, Venezuela: a long white plunge off the vertical tepui wall, savanna in front; view from the Roraima trek. NOT Angel Falls, NOT Roraima's own falls."),
    "Seahpo-Peak-Falls-4962": dict(
        badge="SEASONAL", tags=[("ruler", "Longest tier ~152 m"), ("mountain", "Mount Shuksan")],
        cross={"name": "Wikipedia: Seahpo Peak Falls (about 2,200 ft / 670 m)", "url": "https://en.wikipedia.org/wiki/Seahpo_Peak_Falls", "value": 670},
        notes="WWD: about 2,200 ft in several narrow tiers; flows well in summer but only while snow melts; Wikipedia calls it intermittent → SEASONAL.",
        hint="Seahpo Peak Falls, east arm of Mount Shuksan above the Sulphide Creek basin, North Cascades National Park, Washington, USA: narrow braided white tiers streaming down dark glaciated cliffs; aerial or Sulphide basin view. NOT Cloudcap Falls, NOT Sulphide Creek Falls."),
    "Sulphide-Creek-Falls-3367": dict(
        tags=[("mountain", "Mount Shuksan")],
        cross=None,
        notes="WWD: almost 2,200 ft below Sulphide Lake outlet, mostly hidden in a narrow flume; year-round (WWD 12 months). Wikipedia article gives similar height (number not retrieved, API rate limit).",
        hint="Sulphide Creek Falls, from Sulphide Lake on the southeast side of Mount Shuksan, North Cascades National Park, Washington, USA: a powerful white fall in a narrow twisting gorge then tall tiers to a broad basin, seen straight-on from across the basin or from the air. NOT Seahpo Peak Falls, NOT Cloudcap Falls."),
    "Äegertenbachfall-27203": dict(
        tags=[("ruler", "Longest drop 329 m"), ("stairs", "2 tiers")],
        cross=None,
        notes="WWD from topographic models: two tiers of ~230 m and ~330 m. No second source; flow months not documented.",
        hint="Ägertenbach falls (Äegertenbachfall / Ägertenbachfall), Lauterbrunnen Valley between Lauterbrunnen and Stechelberg, Bernese Oberland, Switzerland: a tall two-tier white waterfall down the sheer limestone valley wall above green meadows. NOT Staubbach Falls, NOT Mürrenbach Falls, NOT Trümmelbach Falls."),
    "Mardalsfossen-14": dict(
        badge="HYDRO-REGULATED", tags=[("calendar", "Runs Jun 20–Aug 20"), ("ruler", "Longest drop 328 m")],
        cross={"name": "Statistics Norway (SSB) via WWD — head of the hydro scheme, 704 m", "url": "https://www.worldwaterfalldatabase.com/waterfall/Mardalsfossen-14", "value": 704},
        notes="Diverted into the Grytten hydro plant since 1977; licence guarantees a minimum release 20 June–20 August. WWD 645 m from topography; SSB 704 m reflects hydro head (+9%); often cited 655–705 m. WWD tallest drop 328 m (lower tier); upper free fall 262 m (often quoted 297 m).",
        hint="Mardalsfossen, Eikesdalen, Molde, Møre og Romsdal, Norway: a powerful white waterfall in two big plunges (upper free fall into a gorge) down a cliff above green birch forest, summer (June 20–August 20) when it flows; view from the Mardalsfossen trail. NOT Mongefossen."),
    "Blanche-Cascade-60": dict(
        tags=[("ruler", "Top drop ~400 m"), ("stairs", "4 leaps")],
        cross=wl(640),
        notes="WWD from French topo maps: from the ~840 m to ~200 m contour, four leaps, top drop ~400 m; some sources say up to 800 m. Best in the wet season; flow months not documented.",
        hint="Cascade Blanche (Cascade de la Ravine Blanche), on the wall of the Bras de Caverne canyon near Trou de Fer, Réunion island (France): a tall white four-step waterfall contrasting with the deep green jungle cliff; helicopter view. NOT Trou de Fer's main falls, NOT Voile de la Mariée."),
    "Sentinel-Fall-24": dict(
        badge="SEASONAL", tags=[("calendar", "Usually dry by July"), ("ruler", "Longest drop 210 m")],
        cross={"name": "Wikipedia: Sentinel Falls (1,920 ft / 590 m)", "url": "https://en.wikipedia.org/wiki/Sentinel_Fall", "value": 590},
        notes="WWD (visited 2013): 2,070 ft in ~11 steps; Wikipedia 1,920 ft (−6.5%). Usually dries out by July (WWD flow consistency 6 months).",
        hint="Sentinel Fall, south wall of Yosemite Valley beside Sentinel Rock, Yosemite National Park, California, USA: a long series of white cascades down the granite wall next to Sentinel Rock in spring; view from Leidig Meadow / the valley floor. NOT Yosemite Falls (north wall), NOT Bridalveil Fall, NOT Staircase Falls."),
}

INSIGHTS = [
    (30, "SEASONAL = it flows only part of the year, fed by snowmelt or rainy-season runoff."),
    (21, "Zimbabwe's Mutarazi is often listed at 762 m; World Waterfall Database estimates ~479 m."),
    (12, "Norway's Mongefossen (773 m) would rank here, but hydropower has kept it dry since 1977."),
    (4, "Next: a Swiss fall that grew 90 m in 2020, when canyoneers abseiled down and measured it."),
    (2, "Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins."),
]

SCOPE = ("What counts: natural waterfalls ranked by total height, from the top of the highest drop to the base of the lowest, "
         "including cascades between tiers. Heights follow the World Waterfall Database unless a published survey or record "
         "exists (Angel Falls: Guinness, 1949 survey; Tugela: Guinness; Yumbilla: IGN Peru 2007). Listed: named falls the database "
         "surveyed or confirmed with a stated basis, or with an independent survey; unverified estimates (e.g. Hawaii's Olo'upena) and falls dried up by "
         "hydropower (Mongefossen) are left out. SEASONAL = flows only part of the year.")


def m_from(s: str) -> int | None:
    m = re.search(r"([\d,]+) meters", s or "")
    return int(m.group(1).replace(",", "")) if m else None


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    wwd = {r["slug"]: r for r in json.loads((HERE / "raw" / "wwd_top.json").read_text(encoding="utf-8"))}
    old = {}
    if (EP / "data.json").exists():
        for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
            old[it["name"]] = it
    rows = []
    for slug, name, sub, iso, country, wiki in ITEMS:
        r = wwd[slug]
        wm = m_from(r.get("total_height"))
        rows.append((VALUE_OVERRIDE.get(slug, wm), wm, slug, name, sub, iso, country, r))
    rows.sort(key=lambda x: (-x[0], x[3]))
    items = []
    prev_v, prev_rank = None, 0
    for pos, (val, wm, slug, name, sub, iso, country, r) in enumerate(rows, 1):
        rank = prev_rank if val == prev_v else pos
        prev_v, prev_rank = val, rank
        e = EXTRA[slug]
        ft = round(val * 3.28084)
        src = e.get("source") or {"name": f"World Waterfall Database: {r['title'].split(',')[0]} (total height {wm} m)",
                                  "url": f"https://www.worldwaterfalldatabase.com/waterfall/{urllib.parse.quote(slug)}"}
        it = {"rank": rank, "name": name, "subtitle": sub, "country_iso2": iso, "country_name": country,
              "continent": CONT[iso], "value": val, "value_display": f"{round(val):,} m", "secondary_display": f"{ft:,} ft"}
        if e.get("badge"):
            it["badge"] = e["badge"]
        it["tags"] = [{"icon": i, "text": t} for i, t in e.get("tags", [])]
        it["image"] = f"assets/img/{pos:02d}_{slugify(name)}.jpg"
        it["image_credit"] = ""
        it["source"] = {**src, "retrieved_at": TODAY}
        c = e.get("cross")
        if c:
            it["cross_check"] = {**c, "diff_pct": round((c["value"] - val) / val * 100, 1)}
        it["notes"] = e.get("notes", "")
        it["image_hint"] = e["hint"]
        it["wwd"] = {"url": f"https://www.worldwaterfalldatabase.com/waterfall/{urllib.parse.quote(slug)}", "status": r.get("status"),
                     "total_height_m": wm, "tallest_drop": r.get("tallest_drop", ""), "flow_consistency": r.get("flow_consistency", ""),
                     "updated": r.get("updated", "").replace("This page was last updated on ", "").rstrip(":")}
        o = old.get(name)
        if o:
            for k in ("image", "image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit"):
                if k in o:
                    it[k] = o[k]
        items.append(it)
    data = {
        "episode": "ep20_tallest_waterfalls",
        "title": "Tallest Waterfalls in the World",
        "kicker": f"TOP {len(items)}",
        "metric_label": "Total height",
        "unit": "m",
        "period_label": "Data as of Nov 2026",
        "source_line": "Sources: World Waterfall Database, Guinness, IGN Peru, USGS",
        "theme": "cascade",
        "tally": {"by": "country", "title": "Falls by country"},
        "items": items,
        "insights": [{"after_rank": a, "text": t} for a, t in INSIGHTS],
        "scope_note": SCOPE,
        "layout": {"card_w": 600, "focus": [0.5, 0.4],
                   "image_prefer": "the WHOLE waterfall visible from top to bottom (or as much of it as possible), the right named waterfall (check the location), strong flow, the classic recognisable viewpoint, portrait orientation preferred"},
    }
    for t in [x["text"] for x in data["insights"]]:
        assert len(t) <= 90, (len(t), t)
    assert len(SCOPE) <= 600, len(SCOPE)
    for it in items:
        assert len(it.get("badge", "")) <= 22, it["badge"]
        for t in it["tags"]:
            assert len(t["text"]) <= 24, t
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from collections import Counter
    print(len(items), "items;", Counter(i["country_name"] for i in items).most_common())
    for it in items:
        print(it["rank"], it["name"], it["value_display"], it.get("badge", ""), it.get("cross_check", {}).get("diff_pct", ""))


if __name__ == "__main__":
    main()
