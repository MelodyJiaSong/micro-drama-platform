import json
ins = [
 {"after_rank": 41, "text": "Next: South Sudan, the world's newest country. Its 2011 split took a quarter of Sudan."},
 {"after_rank": 32, "text": "Next: Venezuela, just 5,922 km² ahead of Nigeria in UN data. Other atlases flip them."},
 {"after_rank": 21, "text": "Next: Chad and Peru, only 1,216 km² apart. That's barely bigger than Hong Kong."},
 {"after_rank": 14, "text": "Greenland (2.17M km²) is self-governing and listed apart from Denmark; alone it'd be 13th."},
 {"after_rank": 4, "text": "By land alone, China (9.33M km²) beats the US (9.15M km²), and Canada falls to 4th."},
 {"after_rank": 2, "text": "Next: Russia. Often called bigger than Pluto, it isn't: Pluto's surface is ~17.7M km²."},
]
for i in ins: print(len(i["text"]), i["text"])
scope = ("What counts: total area (land plus inland water such as lakes and rivers) of each sovereign country, as reported "
         "in the UN Demographic Yearbook 2024 (Sudan, missing there: World Bank/FAO), cross-checked with the CIA World Factbook. "
         "Not counted: Antarctic claims and territories the UN lists separately (Greenland, French overseas regions, "
         "Western Sahara; with it Morocco would rank 39th). Disputed areas follow each country's UN figure: India's includes "
         "all of Kashmir it claims, Pakistan's excludes the parts it administers, Ukraine is within its recognised borders.")
print(len(scope))
json.dump(ins, open("insights.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(scope, open("scope_note.json", "w", encoding="utf-8"), ensure_ascii=False)
