# -*- coding: utf-8 -*-
"""ep20 条目定义（口径见 topic.md / sources.md §1）。
WWD = World Waterfall Database「Overall Height」榜（2026-11-03 抓取，raw/wwd_top.json）。
入选：有名字；WWD 状态 Cataloged（WWD 实地勘测），或 Confirmed 且条目写明高度依据（测量 / 地形图分析 / 官方数值），
或 Unconfirmed 但有独立权威测量 / 记录（Tugela：Guinness；Yumbilla：秘鲁 IGN 2007）；取 ≥ 631 m（第 35 名 Sentinel Fall，下一名 625 m）。
排除：水被水电引走、已基本断流（Mongefossen 773 m、Brufossen 640 m）；Confirmed 但条目只有一个数字、无任何依据
（Helgåfossen 750、Terror Falls 750、Brurasløret 700、Solitary Falls 680、Breiteigsfossen 640、Buskefoss 625）。主值优先用公开测量 / 记录，否则 WWD。
字段：slug（WWD）、name、subtitle、iso2、country、value（m）、value_src（覆盖 WWD 时的来源键）、wiki（en / 其他语种条目名）。"""

ITEMS = [
    # slug, name, subtitle, iso2, country, wiki titles {lang: title}
    ("Kerepakupai-Meru-1", "Angel Falls", "Canaima NP", "VE", "Venezuela", {"en": "Angel Falls"}),
    ("Tugela-Falls-2", "Tugela Falls", "Drakensberg", "ZA", "South Africa", {"en": "Tugela Falls"}),
    ("Mattenbachfälle-27386", "Mattenbach Falls", "Lauterbrunnen", "CH", "Switzerland", {"de": "Mattenbachfall"}),
    ("Yumbilla-Catarata-811", "Yumbilla Falls", "Cuispes, Amazonas", "PE", "Peru", {"en": "Yumbilla Falls"}),
    ("Skorga-11652", "Skorga Falls", "Sunndal", "NO", "Norway", {"en": "Skorga"}),
    ("Vinnufallet-11651", "Vinnufossen", "Sunndal", "NO", "Norway", {"en": "Vinnufossen"}),
    ("James-Bruce-Falls-1191", "James Bruce Falls", "Princess Louisa Inlet", "CA", "Canada", {"en": "James Bruce Falls"}),
    ("Browne-Falls-18", "Browne Falls", "Doubtful Sound, Fiordland", "NZ", "New Zealand", {"en": "Browne Falls"}),
    ("Kjerrskredfossen-5552", "Kjerrskredfossen", "Vestland", "NO", "Norway", {}),
    ("Waihilau-Falls-639", "Waihilau Falls", "Waimanu Valley, Hawaiʻi", "US", "United States", {"en": "Waihilau Falls"}),
    ("Colonial-Creek-Falls-4738", "Colonial Creek Falls", "North Cascades", "US", "United States", {"en": "Colonial Creek Falls"}),
    ("Gocta-Catarata-805", "Gocta Falls", "Cocachimba, Amazonas", "PE", "Peru", {"en": "Gocta Cataracts"}),
    ("Kjelfossen-45", "Kjelfossen", "Gudvangen, Vestland", "NO", "Norway", {"en": "Kjelfossen"}),
    ("Isella-Falls-4550", "Isella Falls", "Washington", "US", "United States", {}),
    ("Johannesburg-Falls-3083", "Johannesburg Falls", "North Cascades", "US", "United States", {"en": "Johannesburg Falls"}),
    ("Tjotafossen-415", "Tjøtafossen", "Vestland", "NO", "Norway", {}),
    ("Dontefossen-11", "Døntefossen", "Møre og Romsdal", "NO", "Norway", {"no": "Døntefossen"}),
    ("Yosemite-Falls-9", "Yosemite Falls", "Yosemite NP", "US", "United States", {"en": "Yosemite Falls"}),
    ("Cloudcap-Falls-4959", "Cloudcap Falls", "Washington", "US", "United States", {"en": "Cloudcap Falls"}),
    ("Boulder-Glacier-Falls-10285", "Boulder Glacier Falls", "Glacier NP", "US", "United States", {}),
    ("Trou-de-Fer-Cascades-de-130", "Trou de Fer Falls", "Réunion", "FR", "France", {"en": "Cascades de Trou de Fer"}),
    ("Yutaje-Salto-19", "Yutajé Falls", "Amazonas state", "VE", "Venezuela", {"en": "Yutajé Falls"}),
    ("Kjeragfossen-671", "Kjeragfossen", "Lysefjord", "NO", "Norway", {"en": "Kjeragfossen"}),
    ("Tagfossen-6273", "Tågfossen", "Møre og Romsdal", "NO", "Norway", {}),
    ("Ølmåfossen-30753", "Ølmåfossen", "Romsdalen", "NO", "Norway", {"no": "Ølmåfossen"}),
    ("Cabin-Boy-Falls-22806", "Cabin Boy Falls", "West Coast", "NZ", "New Zealand", {}),
    ("Balaifossen-633", "Sprænefossen", "Vestland", "NO", "Norway", {}),
    ("Lake-Unknown-Falls-699", "Lake Unknown Falls", "Otago", "NZ", "New Zealand", {"en": "Lake Unknown Falls"}),
    ("Kukenaam-Salto-21", "Kukenán Falls", "Gran Sabana", "VE", "Venezuela", {"en": "Cuquenan Falls"}),
    ("Seahpo-Peak-Falls-4962", "Seahpo Peak Falls", "North Cascades", "US", "United States", {}),
    ("Sulphide-Creek-Falls-3367", "Sulphide Creek Falls", "North Cascades", "US", "United States", {"en": "Sulphide Creek Falls"}),
    ("Äegertenbachfall-27203", "Ägertenbach Falls", "Lauterbrunnen", "CH", "Switzerland", {}),
    ("Mardalsfossen-14", "Mardalsfossen", "Eikesdalen", "NO", "Norway", {"en": "Mardalsfossen"}),
    ("Blanche-Cascade-60", "Cascade Blanche", "Réunion", "FR", "France", {"en": "Cascade Blanche"}),
    ("Sentinel-Fall-24", "Sentinel Fall", "Yosemite NP", "US", "United States", {"en": "Sentinel Falls"}),
]

# 主值覆盖 WWD 的条目（官方 / 权威测量或记录优先）
VALUE_OVERRIDE = {
    "Kerepakupai-Meru-1": 979,     # Guinness World Records（1949 National Geographic 资助的 Ruth Robertson 测量）；WWD 只算主跌落 807 m
    "Yumbilla-Catarata-811": 895.4,  # 秘鲁国家地理研究所 IGN 2007 测量（MercoPress 2007-12-04 等转引）；WWD 896
}
