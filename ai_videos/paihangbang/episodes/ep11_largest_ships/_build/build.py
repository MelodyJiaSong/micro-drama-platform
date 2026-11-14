# -*- coding: utf-8 -*-
"""ep11 data.json 生成：classes_computed.json（VesselFinder 全量 + 船级定义）+ DNV 登记 + 人工补充（EXTRA）。

改数据：改 classes_def.py / EXTRA 后依次跑 compute_classes.py → build.py → gen_sources.py。
已有 data.json 里的图片字段（image / image_credit / image_focus / image_risk / image_alt…）按 key 保留。
"""
import json, re, sys
from pathlib import Path

B = Path(__file__).parent
EP = B.parent
sys.path.insert(0, str(B))
from classes_def import CLASSES  # noqa: E402
from visual_notes import NOTES, VN_EXTRA  # noqa: E402

TITANIC_GT = 46328          # RMS Titanic, 46,328 GRT（1912 登记；Encyclopedia Titanica / Wikipedia）
TODAY = "2026-11-03"
ISO_NAME = {"CH": "Switzerland", "US": "United States", "FR": "France", "TW": "Taiwan", "HK": "Hong Kong", "SG": "Singapore",
            "KR": "South Korea", "DE": "Germany", "CN": "China", "DK": "Denmark", "BR": "Brazil", "IT": "Italy"}
CONT = {"CH": "Europe", "US": "North America", "FR": "Europe", "TW": "Asia", "HK": "Asia", "SG": "Asia", "KR": "Asia",
        "DE": "Europe", "CN": "Asia", "DK": "Europe", "BR": "South America", "IT": "Europe"}

# 人工补充：badge、长度（m, 取代表船 LOA，VesselFinder / DNV）、首制年说明、交叉核对（维基等第二来源）、备注
EXTRA = {
    "pioneering_spirit": dict(badge="", wiki="Pioneering_Spirit", xc=("Wikipedia: Pioneering Spirit (cites Lloyd's Register)", 403342),
        note="Twin-hull platform installation/decommissioning vessel. Hull built by DSME (South Korea), 2014; completed in the Netherlands and in service since 2016. Allseas spec sheet: 382 m (477 m incl. stinger) x 124 m, topsides lift 48,000 t."),
    "icon": dict(badge="LARGEST CRUISE SHIP", wiki="Icon-class_cruise_ship", xc=("Wikipedia: Icon of the Seas", 248663),
        note="Icon of the Seas (2023 delivery, Jan 2024 debut), Star of the Seas (2025), Legend of the Seas (2026) all registered at 248,663 GT (DNV). Royal Caribbean marketing figure 250,800 GT is not the registered tonnage."),
    "cma_seine": dict(badge="NEW 2025", wiki="", xc=("Wikipedia: List of largest container ships (CMA CGM Seine)", 236583),
        note="24,000 TEU LNG dual-fuel series delivered 2025-26: Seine, Saint Germain, Vendome, Grand Palais (Hudong-Zhonghua) and Notre Dame, Pantheon, Orsay (Yangzi Xinfu, French flag). Baird Maritime calls Notre Dame part of the same series as Seine. VesselFinder: Seine-group 237,742 GT; Notre Dame-group 236,463 GT. Wikipedia lists Seine at 236,583 (copied from Saadé class)."),
    "ever_a": dict(badge="", wiki="Ever_Ace", xc=("Wikipedia: Evergreen A-class (Ever Alot 236,228)", 236228),
        note="13 ships 2021-25 (6 Samsung-built Ever Ace group 235,579 GT; Chinese-built Ever Alot group 236,228; Ever Acme 236,673; Ever Aeon & Ever Ally 236,680). Largest GT = Ever Aeon (IMO 9943279), per VesselFinder."),
    "cma_saade": dict(badge="", wiki="CMA_CGM_Jacques_Saadé", xc=("Wikipedia: List of largest ships by gross tonnage", 236583),
        note="9 ships 2020-21, first LNG-powered 23,000 TEU ships; all 236,583 GT."),
    "oasis": dict(badge="", wiki="Oasis-class_cruise_ship", xc=("Wikipedia: Utopia of the Seas infobox", 236860),
        note="6 ships 2009-24. Largest registered = Utopia of the Seas 236,473 GT (DNV). Wikipedia/RCI give 236,860 (marketing). Wonder of the Seas 235,600 (DNV) vs 236,857 (Wikipedia)."),
    "msc_irina": dict(badge="RECORD 24,346 TEU", wiki="", xc=("Wikipedia: List of largest container ships (MSC Irina)", 233328),
        note="MSC 2023 programme of 24,000+ TEU ships split across three Chinese yards: Irina group (Yangzi Xinfu, 24,346 TEU, 236,184 GT), Tessa group (Hudong-Zhonghua / Jiangnan, 24,116 TEU, 235,651-236,078 GT). Largest = MSC Irina 236,184 (DNV). Wikipedia lists 233,328 GT (-1.2%)."),
    "oocl_spain": dict(badge="", wiki="", xc=("Wikipedia: List of largest container ships (OOCL Spain class)", 235341),
        note="24,188 TEU, 2023-24, Nantong & Dalian COSCO KHI; 12 ships, 235,341 GT."),
    "one_innovation": dict(badge="", wiki="", xc=("Wikipedia: List of largest container ships (ONE Innovation)", 235311),
        note="24,136 TEU, 2023, Japan Marine United / Imabari; 6 ships, 235,311 GT (DNV for ONE Innovation). Owned by Japanese lessors, operated by Singapore-based ONE."),
    "oocl_wisdom": dict(badge="NEW 2026", wiki="", xc=("Wikipedia: List of largest container ships (OOCL Wisdom)", 236000),
        note="World's first 24,000 TEU methanol dual-fuel ships, delivered 2026 (OOCL Wisdom, OOCL Grace; Nantong COSCO KHI). OOCL Grace DNV 234,361 GT; Wikipedia gives a rounded 236,000."),
    "msc_gulsun": dict(badge="", wiki="MSC_Gülsün", xc=("Wikipedia: List of largest ships by gross tonnage", 232618),
        note="16 ships 2019-21 from Samsung (232,618 GT) and DSME (228,741-228,786). Largest = MSC Gülsün (DNV)."),
    "hmm_algeciras": dict(badge="", wiki="HMM_Algeciras", xc=("Wikipedia: List of largest ships by gross tonnage (HMM Oslo)", 232311),
        note="12 ships 2020 from DSME (228,283 GT) and Samsung (232,311). Largest = HMM Oslo group."),
    "berlin_express": dict(badge="", wiki="", xc=("Wikipedia: List of largest container ships", 229376),
        note="12 ships 2023-25, 23,660 TEU LNG dual-fuel, Hanwha Ocean; 229,376 GT (DNV)."),
    "ever_g": dict(badge="EVER GIVEN'S CLASS", wiki="Ever_Given", xc=("Wikipedia: List of largest container ships (Ever Glory)", 219775),
        note="11 ships 2018-19 (Imabari and Samsung). Ever Given, which blocked the Suez Canal in March 2021, is 219,079 GT; largest of the class = Ever Glory / Ever Globe 219,775."),
    "cma_antoine": dict(badge="", wiki="CMA_CGM_Antoine_de_Saint_Exupéry", xc=("Wikipedia: List of largest ships by gross tonnage", 219277),
        note="3 ships 2018, 20,954 TEU, built by Hanjin Subic (Philippines)."),
    "msc_world": dict(badge="", wiki="World-class_cruise_ship", xc=("Wikipedia: List of largest ships by gross tonnage (World Europa)", 215863),
        note="LNG cruise ships by Chantiers de l'Atlantique: MSC World Europa (2022, 215,863 GT), MSC World America (2025, 216,638), MSC World Asia (2026, 205,700 per VesselFinder — figure looks provisional)."),
    "cosco_universe": dict(badge="", wiki="", xc=("Wikipedia: List of largest container ships (COSCO Shipping Universe)", 215553),
        note="6 ships 2018-19 (21,237 TEU): Universe/Planet 215,553 GT, Nebula/Galaxy/Solar/Star 216,359 (DNV for COSCO Shipping Solar)."),
    "madrid_maersk": dict(badge="", wiki="Madrid_Maersk", xc=("Wikipedia: List of largest ships by gross tonnage", 214286),
        note="Second-generation Triple-E, 11 ships 2017-19, DSME, 214,286 GT."),
    "mol_triumph": dict(badge="", sub=" · now ONE", wiki="MOL_Triumph", xc=("Wikipedia: List of largest container ships (MOL Triumph)", 210678),
        note="6 ships 2017-18 from Samsung for MOL, now operated by ONE and renamed ONE Triumph etc. VesselFinder: ONE Tribute / ONE Tradition 213,633 GT; Wikipedia lists 210,678 for the class (older figure)."),
    "oocl_hk": dict(badge="", wiki="OOCL_Hong_Kong", xc=("Wikipedia: List of largest container ships", 210890),
        note="6 ships 2017-18, Samsung, 21,413 TEU. VesselFinder: OOCL Hong Kong / Scandinavia / Indonesia 212,035; Germany / Japan / UK 210,890."),
    "disney_adventure": dict(badge="NEW 2025", wiki="Disney_Adventure", xc=("Wikipedia: Disney Adventure (cites DNV)", 208108),
        note="Completed by Meyer Wismar from the unfinished Global Dream hull, delivered 13 Dec 2025, home port Singapore; 208,108 GT (DNV)."),
    "valemax": dict(badge="BIGGEST BULK CARRIER", wiki="Valemax", xc=("Wikipedia: List of largest ships by gross tonnage (Pacific Unity)", 203396),
        note="~400,000 dwt ore carriers built to Vale's specification 2011-20 (68 ships in VesselFinder, many owners: China Merchants, COSCO, Polaris, Oman Shipping, Berge Bulk...). Country = Vale (Brazil), the charterer they are built and operated for. Largest GT = Pacific Unity group 204,014 (DNV)."),
    "cosco_aries": dict(badge="", wiki="", xc=("Wikipedia: List of largest container ships (COSCO Shipping Taurus)", 194864),
        note="11 ships 2018-19 (20,119 TEU) from several Chinese yards: 194,864-197,658 GT; largest = Pisces/Scorpio/Aquarius 197,658."),
    "barzan": dict(badge="", wiki="Barzan_(ship)", xc=("DNV Vessel Register (Barzan, Al Dahna Express)", 195636),
        note="UASC A18 class, 6 ships 2015-16 by Hyundai, 18,800 TEU; UASC merged into Hapag-Lloyd 2017."),
    "triple_e": dict(badge="", wiki="Triple_E-class_container_ship", xc=("Wikipedia: Triple E-class container ship", 194849),
        note="First-generation Triple-E, 20 ships 2013-15, DSME, 18,270 TEU, 194,849 GT."),
    "msc_oscar": dict(badge="", wiki="MSC_Oscar", xc=("Wikipedia: MSC Oscar", 192237),
        note="MSC's 19,200-19,500 TEU programme 2014-17 split across DSME (Oscar group 192,237-192,784; Jade group 194,308), Samsung (Diana group 193,489-194,250) and Hyundai (Anna, Viviana 187,587). All DNV-classed; largest = Jade group 194,308."),
    "cscl_globe": dict(badge="", wiki="CSCL_Globe", xc=("Wikipedia: CSCL Globe", 187541),
        note="5 ships 2014-15, Hyundai, 19,100 TEU; China Shipping merged into COSCO Shipping 2016."),
    "excel": dict(badge="", wiki="Excellence-class_cruise_ship", xc=("Wikipedia: Excellence-class cruise ship (Costa Toscana)", 186364),
        note="Carnival Corporation's LNG class, 9 ships 2018-23 for AIDA, Costa, P&O and Carnival (Meyer Werft / Meyer Turku). Largest GT = Costa Toscana 186,364, so the flag follows its operator Costa Cruises (Genoa, Italy), the same 'operator of the ship that sets the value' rule as every other card."),
    "meraviglia_plus": dict(badge="", wiki="", xc=("Wikipedia: MSC Euribia", 184011),
        note="MSC Grandiosa (2019), MSC Virtuosa (2021) 181,541 GT; MSC Euribia (2023, LNG) 184,011."),
    "beijing_maersk": dict(badge="NEW 2025", wiki="", xc=None,
        note="6 methanol dual-fuel 17,480 TEU ships built by HD Hyundai Heavy Industries, delivered 2025-26; Berlin Maersk named first (18 Jun 2025, gCaptain). Members Berlin, Beijing, Bangkok, Brussels, Brisbane, Barcelona Maersk; 350 m, 180,849 GT per VesselFinder."),
    "cma_franklin": dict(badge="", wiki="", xc=("Wikipedia: CMA CGM Benjamin Franklin (built by Jiangnan Changxing)", None),
        note="3 ships 2015 (CMA CGM Vasco de Gama, Zheng He, Benjamin Franklin), Jiangnan Changxing, ~18,000 TEU, 179,922 GT. Separate order from the Samsung-built Bougainville class."),
    "sphere": dict(badge="", wiki="Sphere-class_cruise_ship", xc=("Wikipedia: Sun Princess (2024) — Princess figure", 175500),
        note="Sun Princess (2024) and Star Princess (2025), Fincantieri, LNG; 177,882 GT per VesselFinder; Princess marketing figure 175,500."),
    "cma_bougainville": dict(badge="", wiki="CMA_CGM_Bougainville", xc=None,
        note="3 ships 2015 by Samsung (CMA CGM Bougainville, Kerguelen, Georg Forster), 17,722 TEU, 177,381 GT."),
    "cma_explorer": dict(badge="", wiki="CMA_CGM_Marco_Polo", xc=None,
        note="CMA CGM Explorer class by DSME, 2012-13: Marco Polo, Alexander von Humboldt (176,546 GT), Jules Verne (176,435); 16,020 TEU."),
    "msc_london": dict(badge="", wiki="", xc=None,
        note="6 ships 2014-16 (MSC London, New York, Amsterdam, Istanbul, Hamburg, Venice), 399 m x 54 m, 176,490 GT per VesselFinder."),
    "yuan_hai_si_lu": dict(badge="NEW 2026", wiki="", xc=("Xinhua photo story 2026-09-02 (hold volume 280,000 m3)", None),
        note="325,000 dwt ore carrier, 340 m x 62 m, completed by COSCO Shipping Heavy Industry (Yangzhou) on 1 Sep 2026 for COSCO Shipping Bulk (Xinhua / Yangtse Evening Post); hold volume 280,000 m3, 40%+ more than conventional ore carriers of the same size, which explains a GT 3.6% above the 340 m Guaibamax ships. VesselFinder: 180,011 GT, under way to Ponta da Madeira (Brazil) in Nov 2026. Counted as its own class (one ship so far)."),
    "winning": dict(badge="NEW 2026", wiki="", xc=None,
        note="325,000 dwt ore carriers delivered 2026 for Winning Shipping (Singapore), 330 m x 60 m: Winning Ambition & Brave 174,863 GT, Creation & Devotion 172,513-172,517 (VesselFinder). Ambition & Brave built by CSSC Qingdao Beihai, Creation & Devotion by Hengli Heavy Industry (Dalian; named 30 Aug 2026, methanol dual-fuel). Same owner, size and delivery year, so counted as one class."),
    "guaibamax": dict(badge="", wiki="", xc=None,
        note="325,000 dwt / 340 m x 62 m ore carriers built to Vale's 'Guaibamax' specification 2019-22 (47 ships, several owners), up to 173,794 GT. VesselFinder also shows YUAN HAI SI LU (IMO 1052397, 340 m x 62 m, 324,700 dwt) at 180,011 GT; Chinese media (Xinhua / Yangtse Evening Post, 1-5 Sep 2026) confirm it was completed at COSCO Shipping Heavy Industry Yangzhou on 1 Sep 2026 for service from Oct 2026, but no source confirms the GT, which is 3.6% above every Guaibamax-size sister, so it is NOT listed (to confirm before publishing)."),
    "ever_e": dict(badge="NEW 2025", wiki="", xc=None,
        note="Evergreen E-class, ~16,556 TEU, built by Samsung Heavy Industries 2025-26; 8 ships, 369 m x 54 m: Ever Eon/Eco 170,795 GT, Ever Echo/Edit/Even/Emit/Eclat/Edify 172,405 (VesselFinder)."),
    "ane_maersk": dict(badge="", wiki="", xc=None,
        note="Maersk's methanol dual-fuel 16,000+ TEU ships 2024-25 (Ane Maersk + 11 sisters incl. A.P. Moller), 351 m, 172,093 GT."),
    "meraviglia": dict(badge="", wiki="", xc=None,
        note="MSC Meraviglia (2017) and MSC Bellissima (2019), Chantiers de l'Atlantique, 171,598 GT."),
    "emma_maersk": dict(badge="OLDEST ON THE LIST", wiki="Emma_Mærsk", xc=None,
        note="Maersk E class, 8 ships 2006-08 by Odense Steel Shipyard (Denmark); world's largest container ships when new; 171,542 GT."),
}

REPFIX = {"CC CHAMPS ELYSEES": "CMA CGM CHAMPS ELYSEES", "MAERSKMCKINNEYMOLLER": "MAERSK MC-KINNEY MOLLER",
          "CMACGM VASCO DE GAMA": "CMA CGM VASCO DE GAMA", "CMA CGM ST EXUPERY": "CMA CGM ANTOINE DE SAINT EXUPERY",
          "COSCO NEBULA": "COSCO SHIPPING NEBULA", "COSCO SCORPIO": "COSCO SHIPPING SCORPIO"}
SHORT = {"Container ship": "Container ship", "Cruise ship": "Cruise ship", "Ore carrier": "Ore carrier", "Crane vessel": "Crane vessel"}


def dnv_for(members):
    """首个在 DNV 登记里有 GT 的同级船（优先最大 GT 者）。"""
    for m in members:
        p = B / "dnv" / f"{m[0]}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8")).get("details") or {}
        gt = (d.get("dimensions") or {}).get("grossTon69")
        if gt:
            i = d["identification"]
            return {"imo": m[0], "name": i["vesselName"], "gt": int(gt), "id": i["vesselId"], "status": i.get("operationalStatusString"),
                    "builder": (d.get("yard") or {}).get("contractedBuilder") or (d.get("yard") or {}).get("hullYardName"),
                    "built": ((d.get("yard") or {}).get("dateOfBuild") or "")[:10], "loa": (d.get("dimensions") or {}).get("lengthOverall")}
    return None


def main():
    cs = json.loads((B / "classes_computed.json").read_text(encoding="utf-8"))
    old = {}
    if (EP / "data.json").exists():
        for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
            old[it.get("key")] = it
    items = []
    for rank, c in enumerate(cs, 1):
        e = EXTRA[c["key"]]
        rep = c["rep"]
        top = [m for m in c["members"] if int(m[3]) == c["max_gt"]]
        dn = dnv_for(top)
        loa = int(round(float(rep["size"].split("/")[0]))) if rep["size"] else None
        n = c["n"]
        sub = (f"{c['kind']} · {n} ships" if n > 1 else f"{c['kind']} · one of a kind") + e.get("sub", "")
        gt = c["max_gt"]
        it = {
            "key": c["key"], "rank": rank, "name": c["name"], "subtitle": sub,
            "country_iso2": c["iso"], "country_name": ISO_NAME[c["iso"]], "continent": CONT[c["iso"]],
            "value": gt, "value_display": f"{gt:,} GT", "secondary_display": f"{gt / TITANIC_GT:.1f}× Titanic",
            "tags": [{"icon": "ruler", "text": f"{loa} m long"}, {"icon": "calendar", "text": f"Since {2016 if c['key']=='pioneering_spirit' else c['first_year']}"}],
            "operator": c["operator"], "ship_type": c["kind"],
            "representative": {"name": REPFIX.get(rep["name"], rep["name"]), "imo": rep["imo"], "gt": gt, "year": rep["year"]},
            "members_count": n, "first_year": c["first_year"],
        }
        if e.get("badge"):
            it["badge"] = e["badge"]
        if c["key"] in ("icon", "cma_seine", "ever_a"):        # 封面用 #2–#4，不泄露冠军（QC m4）
            it["thumb"] = True
        if dn:
            it["source"] = {"name": f"DNV Vessel Register: {dn['name']} (IMO {dn['imo']}), GT69 {dn['gt']:,}",
                            "url": f"https://vesselregister.dnv.com/vesselregister/details/{dn['id']}", "tier": "primary", "retrieved_at": TODAY}
            vf_x = {"name": f"VesselFinder: {REPFIX.get(rep['name'], rep['name'])} (IMO {rep['imo']})", "url": f"https://www.vesselfinder.com/vessels/details/{rep['imo']}",
                    "value": int(rep["gt"]), "diff_pct": round((int(rep["gt"]) - dn["gt"]) / dn["gt"] * 100, 2)}
            it["cross_check"] = vf_x
            if dn["gt"] != gt:
                it["notes_dnv"] = f"DNV GT {dn['gt']} differs from class max {gt}"
        else:
            it["source"] = {"name": f"VesselFinder (IHS data): {REPFIX.get(rep['name'], rep['name'])} (IMO {rep['imo']}), GT {gt:,}",
                            "url": f"https://www.vesselfinder.com/vessels/details/{rep['imo']}", "tier": "aggregator", "retrieved_at": TODAY}
            if e.get("xc"):
                nm, v = e["xc"]
                it["cross_check"] = {"name": nm, "value": v, "diff_pct": round((v - gt) / gt * 100, 2) if v else None}
        it["notes"] = e["note"]
        vn = NOTES.get(c["key"]) or VN_EXTRA.get(c["key"]) or {}
        it["image_hint"] = (f"photo of {REPFIX.get(rep['name'], rep['name']).title()} (IMO {rep['imo']}) or a named sister of the {c['name']}; "
                            f"{vn.get('look','')} Exclude: {vn.get('confuse','')} View: {vn.get('view','')}")
        if c["key"] in ("pioneering_spirit",):
            it["source"]["name"] = "Lloyd's Register via Wikipedia & VesselFinder: Pioneering Spirit (IMO 9593505), GT 403,342; Allseas spec sheet"
            it["source"]["url"] = "https://www.vesselfinder.com/vessels/details/9593505"
            it["source"]["tier"] = "aggregator"
            it["cross_check"] = {"name": "Wikipedia: Pioneering Spirit (Lloyd's Register ref)", "url": "https://en.wikipedia.org/wiki/Pioneering_Spirit", "value": 403342, "diff_pct": 0.0}
        stem = f"{rank:02d}_{c['key']}"
        o = old.get(c["key"], {})
        it["image"] = o.get("image") or f"assets/img/{stem}.jpg"
        for k in ("image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit"):
            if k in o:
                it[k] = o[k]
        items.append(it)
    data = {
        "episode": "ep11_largest_ships",
        "title": "Biggest Ships in the World",
        "kicker": f"TOP {len(items)}",
        "metric_label": "Gross tonnage",
        "unit": "GT",
        "period_label": "One card per ship class · In service Nov 2026",
        "source_line": "Sources: DNV Vessel Register, VesselFinder · Flag = operator HQ",
        "theme": "maritime",
        "tally": {"by": "country", "title": "Ship classes by operator country"},
        "scope_note": ("What counts: every ship class in service in Nov 2026 bigger than the largest oil tanker still trading "
                       "(170,618 GT), ranked by registered gross tonnage (GT, enclosed volume, not weight). Sister ships share one "
                       "card; the value is the largest ship of the class. Moored units (FPSO, FLNG, storage tankers) and warships "
                       "are excluded. Flags show the operating company's HQ, not the flag of registry: OOCL is listed under Hong Kong, ONE (a Japanese joint venture) under Singapore, Valemax/Guaibamax under Brazil (built for and chartered to Vale)."),
        "layout": {"card_w": 800, "focus": [0.5, 0.5], "intro_hold": 2.5,
                   "image_prefer": "a real photo of this exact ship (or a named sister ship of the same class) at sea or in port, whole hull visible bow to stern, three-quarter bow view preferred"},
        "items": items,
        "insights": json.loads((B / "insights.json").read_text(encoding="utf-8")) if (B / "insights.json").exists() else [],
    }
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(items), "items")


if __name__ == "__main__":
    main()
