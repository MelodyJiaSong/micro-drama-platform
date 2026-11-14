# -*- coding: utf-8 -*-
"""每个船级的外观辨认要点、易混对象、找图建议（代理据维基 / 船东资料 / 调研整理；写进 _build/content/ 与 image_hint）。"""

NOTES = {
    "pioneering_spirit": dict(
        look="Twin-hull (split-hull) crane vessel, 382 m x 124 m; a 122 m-long slot cut into the bow between the two hulls; eight huge yellow topsides-lift beams at the bow; white/grey superstructure and helideck at the stern; 'ALLSEAS' on the hull.",
        confuse="Not Allseas' pipelayers Solitaire/Audacia; not Heerema's semi-submersible crane vessels Sleipnir or Thialf (red cranes on columns); not the Prelude FLNG.",
        view="Bow three-quarter view at sea or in the Maasvlakte/Rotterdam area, showing the bow slot and yellow lift beams."),
    "icon": dict(
        look="Royal Caribbean cruise ship, 365 m; white hull with blue crown-and-anchor funnel; a giant glass 'AquaDome' at the front of the top decks; colourful water-slide park (Category 6) at the stern.",
        confuse="Not an Oasis-class ship (no glass dome, open-air 'Central Park' slot). Sisters Star of the Seas (2025) and Legend of the Seas (2026) look almost identical.",
        view="Three-quarter bow or broadside view at sea, whole ship visible."),
    "cma_seine": dict(
        look="CMA CGM 24,000 TEU LNG dual-fuel container ship (2025-26), 400 m; dark navy hull with large white 'CMA CGM' letters; deckhouse/bridge placed well forward; stacked containers.",
        confuse="Very similar to the older Jacques Saadé class (2020-21). Members: CMA CGM Seine, Saint Germain, Vendome, Grand Palais, Notre Dame, Pantheon, Orsay.",
        view="At sea or arriving at port (Le Havre, Southampton, Singapore), three-quarter view, fully loaded."),
    "ever_a": dict(
        look="Evergreen 24,000 TEU container ship, 400 m; green hull with white 'EVERGREEN' letters; white/green deckhouse forward of midship; funnel aft.",
        confuse="Not the older Ever G-class (Ever Given, 20,000 TEU). Members include Ever Ace, Ever Act, Ever Aim, Ever Alp, Ever Arm, Ever Art, Ever Alot, Ever Apex, Ever Aria, Ever Atop, Ever Acme, Ever Aeon, Ever Ally.",
        view="Broadside or three-quarter at sea / Rotterdam / Felixstowe, name on bow readable."),
    "cma_saade": dict(
        look="CMA CGM 23,000 TEU, first LNG-powered ultra-large container ships (2020-21), 400 m; navy hull with white 'CMA CGM' letters; bridge forward.",
        confuse="Members: CMA CGM Jacques Saadé, Champs Elysées, Palais Royal, Louvre, Rivoli, Montmartre, Concorde, Trocadéro, Sorbonne. Not the 2025-26 Seine class.",
        view="At sea or in port, three-quarter view."),
    "oasis": dict(
        look="Royal Caribbean cruise ship, 362 m; white hull, blue crown-and-anchor funnels; open 'Central Park'/'Boardwalk' slot splitting the upper decks; Utopia/Wonder have colourful hull art near the bow.",
        confuse="Not the Icon class (glass dome). Six sisters: Oasis, Allure, Harmony, Symphony, Wonder, Utopia of the Seas.",
        view="Three-quarter bow view at sea (Utopia of the Seas or Wonder of the Seas preferred)."),
    "msc_irina": dict(
        look="MSC 24,000 TEU container ship (2023), 400 m; black hull with white 'MSC' letters, yellow funnel with MSC logo; bridge forward.",
        confuse="Members: MSC Irina, Loreto, Michel Cappellini, Mariella, Micol, Türkiye, Tessa, Celestino Maresca, Gemma, Mette, Claude Girardet, Nicola Mastro, China, Raya. Older MSC Gülsün class looks similar.",
        view="Loaded at sea or arriving in port, three-quarter view."),
    "oocl_spain": dict(
        look="OOCL 24,188 TEU container ship (2023-24), 400 m; dark hull with white 'OOCL' letters; red/white funnel; bridge forward.",
        confuse="Not the 2017 OOCL Hong Kong class; not the 2026 OOCL Wisdom methanol class.",
        view="At sea or in port, three-quarter view."),
    "one_innovation": dict(
        look="Ocean Network Express 24,000 TEU container ship (2023), 400 m; bright magenta (pink) hull with white 'ONE' letters; bridge forward.",
        confuse="Not the smaller magenta ONE ships or the 2017 MOL Triumph class (also magenta now). Members: ONE Innovation, Infinity, Integrity, Inspiration, Ingenuity, Intelligence.",
        view="Magenta hull clearly visible, at sea or Felixstowe/Singapore."),
    "oocl_wisdom": dict(
        look="OOCL 24,000 TEU methanol dual-fuel container ship (2026), 400 m; OOCL livery.",
        confuse="Members OOCL Wisdom, OOCL Grace (2026). Do not mix with the 2023 OOCL Spain class.",
        view="Naming ceremony / sea trials / maiden call photos."),
    "msc_gulsun": dict(
        look="MSC 23,700 TEU container ship (2019-21), 400 m; black hull with white 'MSC', yellow funnel; bridge forward.",
        confuse="Members: MSC Gülsün, Samar, Leni, Mia, Febe, Ambra, Mina, Isabella, Arina, Nela, Sixin, Apolline, Amelia, Diletta, Michelle, Allegra.",
        view="At sea or port, three-quarter view."),
    "hmm_algeciras": dict(
        look="HMM 24,000 TEU container ship (2020), 400 m; HMM livery (dark hull with 'HMM' lettering); bridge forward.",
        confuse="Members: HMM Algeciras, Copenhagen, Dublin, Gdansk, Hamburg, Helsinki, Le Havre, Oslo, Rotterdam, Southampton, Stockholm, St Petersburg.",
        view="At sea or port, three-quarter view."),
    "berlin_express": dict(
        look="Hapag-Lloyd 23,660 TEU LNG dual-fuel container ship (2023-25), 400 m; black hull with white 'Hapag-Lloyd' letters; orange Hapag-Lloyd containers.",
        confuse="Not the older Barzan class (also Hapag-Lloyd now). Members include Berlin, Manila, Hanoi, Busan, Singapore, Damietta, Hamburg, Gdansk, Rotterdam, Bangkok, Genova, Wilhelmshaven Express.",
        view="At sea / Hamburg / Rotterdam, three-quarter view."),
    "ever_g": dict(
        look="Evergreen 20,000 TEU container ship (2018-19), 400 m; green hull with white 'EVERGREEN'; the class of Ever Given (Suez Canal blockage 2021).",
        confuse="Not the newer Ever A-class (24,000 TEU). Members: Ever Golden, Goods, Genius, Given, Gifted, Grade, Gentle, Glory, Govern, Globe, Greet.",
        view="Any member at sea; Ever Given itself is fine."),
    "cma_antoine": dict(
        look="CMA CGM 20,600 TEU container ship (2018), 400 m; navy hull with 'CMA CGM'.",
        confuse="Members: CMA CGM Antoine de Saint Exupéry, Jean Mermoz, Louis Blériot.",
        view="At sea or port."),
    "msc_world": dict(
        look="MSC Cruises LNG cruise ship (2022-26), 333 m; white hull with blue wave graphics on the bow; distinctive Y-shaped stern with a dry slide 'The Venom Drop'; very tall superstructure.",
        confuse="Members: MSC World Europa, MSC World America, MSC World Asia. Not Meraviglia-class ships.",
        view="Three-quarter bow view at sea."),
    "cosco_universe": dict(
        look="COSCO Shipping 21,000 TEU container ship (2018-19), 400 m; COSCO Shipping livery (blue/white, 'COSCO SHIPPING' on hull).",
        confuse="Members: COSCO Shipping Universe, Nebula, Galaxy, Solar, Star, Planet.",
        view="At sea or port."),
    "madrid_maersk": dict(
        look="Maersk 20,568 TEU 'Triple-E second generation' (2017-19), 399 m; light-blue Maersk hull, white seven-pointed star on blue funnel; twin-island layout (bridge forward, engine/funnel aft of midship).",
        confuse="Not the first-generation Triple-E (2013-15, 18,000 TEU). Members: Madrid, Munich, Moscow, Milan, Monaco, Marseille, Manchester, Murcia, Manila, Mumbai, Maastricht Maersk.",
        view="At sea or port, three-quarter view."),
    "mol_triumph": dict(
        look="20,000 TEU container ship (2017), 400 m, built for MOL; now ONE magenta livery, renamed ONE Triumph etc.",
        confuse="Members: MOL/ONE Triumph, Trust, Tribute, Tradition, Truth, Treasure.",
        view="At sea or port."),
    "oocl_hk": dict(
        look="OOCL 21,413 TEU container ship (2017-18), 400 m; OOCL livery.",
        confuse="Members: OOCL Hong Kong, Germany, Japan, United Kingdom, Scandinavia, Indonesia.",
        view="At sea or port."),
    "disney_adventure": dict(
        look="Disney Cruise Line ship (delivered Dec 2025), 341 m; navy-blue hull, red-and-black funnels, yellow-gold accents; based in Singapore.",
        confuse="Not Disney Wish/Treasure/Destiny (smaller). Formerly the unfinished Global Dream.",
        view="At sea or arriving Singapore."),
    "valemax": dict(
        look="400,000 dwt very large ore carrier, 362 m x 65 m; low long hull with many hatch covers, accommodation block at stern; often dark/black or red hull.",
        confuse="Not Guaibamax (325,000 dwt, 340 m). Many owners: China Merchants (Pacific …, Ore …), COSCO (Yuan … Hai), Oman Shipping (… Max), Polaris (Sea …), Berge Bulk, Shandong.",
        view="Broadside at sea or loading at Ponta da Madeira / Tubarão / Sohar."),
    "cosco_aries": dict(
        look="COSCO Shipping 20,000 TEU container ship (2018-19), 400 m; COSCO Shipping livery.",
        confuse="Members: COSCO Shipping Aries, Leo, Capricorn, Pisces, Scorpio, Aquarius, Gemini, Taurus, Sagittarius, Libra, Virgo.",
        view="At sea or port."),
    "barzan": dict(
        look="18,800 TEU container ship (2015-16), 400 m, built for UASC; now Hapag-Lloyd livery (orange/black).",
        confuse="Members: Barzan, Al Zubara, Al Muraykh, Al Nefud, Al Dahna Express, Al Jmeliyah, Tihama, Umm Salal.",
        view="At sea or port."),
    "triple_e": dict(
        look="Maersk 18,270 TEU Triple-E (2013-15), 399 m; light-blue hull, twin-island layout.",
        confuse="Members: Mærsk Mc-Kinney Møller, Majestic, Mary, Marie, Madison, Magleby, Maribo, Marstal, Matz, Mayview, Merete, Mette, Marchen, Margrethe, Mogens, Munkebo, Maren, Morten... Not Madrid Maersk class.",
        view="At sea or port."),
    "msc_oscar": dict(
        look="MSC 19,200-19,500 TEU container ship (2014-17), ~395-400 m; black hull with white 'MSC', yellow funnel.",
        confuse="Members: MSC Oscar, Oliver, Zoe, Maya, Sveva, Clara, Jade, Reef, Mirja, Erica, Tina, Diana, Ingy, Eloane, Mirjam, Rifaya, Leanne, Nicole, Anna, Viviana.",
        view="At sea or port."),
    "cscl_globe": dict(
        look="19,100 TEU container ship (2014-15), 400 m; built for China Shipping (CSCL), now COSCO Shipping livery.",
        confuse="Members: CSCL Globe, Pacific Ocean, Indian Ocean, Atlantic Ocean, Arctic Ocean.",
        view="At sea or port."),
    "excel": dict(
        look="Carnival Corp's LNG 'Excellence/Excel' class cruise ship, 337-345 m. Costa Toscana / Smeralda: white hull with Costa yellow-blue 'C' funnel; also P&O Iona/Arvia, AIDAnova/Cosma, Carnival Mardi Gras/Celebration/Jubilee.",
        confuse="Prefer Costa Toscana or Costa Smeralda (Costa yellow funnel); not older Costa ships.",
        view="Three-quarter view at sea or in an Italian / Mediterranean port."),
    "meraviglia_plus": dict(
        look="MSC Cruises ship (2019-23), 331 m; white hull, MSC funnel; MSC Euribia has 'SaveTheSea' hull art.",
        confuse="Members: MSC Grandiosa, MSC Virtuosa, MSC Euribia. Not the shorter Meraviglia class.",
        view="Three-quarter view at sea."),
    "sphere": dict(
        look="Princess Cruises LNG ship (2024-25), 345 m; white hull; large glass 'Dome' on top; Princess sea-witch logo on funnel.",
        confuse="Members Sun Princess (2024), Star Princess (2025). Not older Princess ships.",
        view="Three-quarter view at sea."),
}


VN_EXTRA = {
    "beijing_maersk": dict(look="Maersk methanol dual-fuel 17,480 TEU container ship (2025-26, HD Hyundai), 350 m x 56 m; light-blue Maersk hull, white 'MAERSK' letters, blue funnel with white star.", confuse="Members: Beijing, Berlin, Bangkok, Brussels, Brisbane, Barcelona Maersk. Not the 351 m methanol Ane Maersk class.", view="At sea or arriving port, three-quarter view."),
    "cma_franklin": dict(look="CMA CGM ~18,000 TEU container ship (2015), 399 m x 54 m; navy hull, 'CMA CGM'.", confuse="Members: CMA CGM Benjamin Franklin, Vasco de Gama, Zheng He. Not Bougainville class.", view="CMA CGM Benjamin Franklin in US ports (Los Angeles, Oakland, Seattle) or Vasco de Gama at Southampton."),
    "cma_bougainville": dict(look="CMA CGM 17,722 TEU container ship (2015, Samsung), 398 m x 54 m; navy hull.", confuse="Members: CMA CGM Bougainville, Kerguelen, Georg Forster.", view="At Le Havre / Rotterdam / Felixstowe."),
    "cma_explorer": dict(look="CMA CGM 16,020 TEU container ship (2012-13, DSME), 396 m; navy hull, 'CMA CGM'.", confuse="Members: CMA CGM Marco Polo, Alexander von Humboldt, Jules Verne.", view="At sea or port."),
    "msc_london": dict(look="MSC container ship (2014-16), 399 m x 54 m; black hull, white 'MSC', yellow funnel.", confuse="Members: MSC London, New York, Amsterdam, Istanbul, Hamburg, Venice. Not older/smaller 'MSC London Express' etc.", view="At sea or port."),
    "winning": dict(look="325,000 dwt very large ore carrier (2026), 330 m x 60 m, built by CSSC Qingdao Beihai for Winning Shipping (Simandou iron ore, Guinea).", confuse="Members: Winning Ambition, Brave, Creation, Devotion. Not older Winning Capesize ships.", view="Launch / delivery / sea-trial photos."),
    "guaibamax": dict(look="325,000 dwt ore carrier, 340 m x 62 m (Vale 'Guaibamax' spec, 2019-22); long low hull with hatch covers, accommodation aft.", confuse="Many owners: e.g. Sea Guaiba, Sea Shanghai (Polaris), Ore Shantou (China Merchants), BOKM Tubarao (KOSCO), Wooyang Moria, SAO Grace, HL Mercury.", view="At sea or at an ore terminal, broadside."),
    "ever_e": dict(look="Evergreen container ship (2025-26), 369 m x 54 m; green hull, 'EVERGREEN'.", confuse="Members: Ever Eon, Eco, Echo, Edit, Even, Emit, Eclat, Edify. Not old Ever E (2010s small) ships.", view="At sea or port."),
    "ane_maersk": dict(look="Maersk methanol dual-fuel container ship (2024-25), 351 m; light-blue hull; distinctive bridge/accommodation at the very bow and funnel at the stern.", confuse="Members include Ane, Astrid, Axel, Arthur, Albert, Alva, Alexandra, Alette, Antonia, Angelica, Adrian Maersk and A.P. Moller.", view="At sea or port; bow-mounted bridge visible."),
    "meraviglia": dict(look="MSC Cruises ship (2017-19), 316 m; white hull, MSC logo funnel.", confuse="Members: MSC Meraviglia, MSC Bellissima. Not Meraviglia-Plus (Grandiosa) which is longer.", view="Three-quarter view at sea or in port."),
    "emma_maersk": dict(look="Maersk E class (2006-08), 398 m; light-blue hull, white 'MAERSK LINE'; was the world's largest container ship when built.", confuse="Members: Emma, Estelle, Eleonora, Evelyn, Ebba, Elly, Edith, Eugen Maersk.", view="At sea or port."),
    "excel": None,
    "yuan_hai_si_lu": dict(look="325,000 dwt very large ore carrier (2026), 340 m x 62 m, built by COSCO Shipping Heavy Industry (Yangzhou) for COSCO Shipping Bulk; long low hull with hatch covers, accommodation aft.", confuse="Chinese name 远海丝路. Not the smaller 2025-26 'Yuan Hai' Supramax bulkers (Yuan Hai Bai Yu, Yuan Hai Jin Lu...).", view="Naming ceremony / completion photos at Yangzhou, Sep 2026."),
}
