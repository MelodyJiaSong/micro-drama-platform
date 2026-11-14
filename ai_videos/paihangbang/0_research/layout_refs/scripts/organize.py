"""Copy fetched YouTube frames into frames/<NN>_<slug>/ with readable names."""
import shutil, sys
from pathlib import Path
root = Path(sys.argv[1])
VIDEOS = [
 ("01","country_cassette_car_brands","YzRCcFx3XME"),
 ("02","worldtv_population_cubes","wma5fLfVYF0"),
 ("03","worldtv_national_fruits","q6iNqx8nUnI"),
 ("04","dastatistics_phone_brands","OhvO854SS8c"),
 ("05","worlddata3d_oldest_countries","p3E5Y5AyBYg"),
 ("06","realdata_tallest_statues","YEPJDkZRdJU"),
 ("07","mostdata_country_size","BuN8c74BKdM"),
 ("08","globalrank_rice_own_vs_import","3FEoOFsZ-8w"),
 ("09","dataanalyst_rice_export_race","LMEgQRxehlc"),
 ("10","ranktheworld_rice_export_race","tu54enkhyiE"),
 ("11","dataworldplus_bread_by_country","fYv2NP-71HA"),
 ("12","rmrs_top30_fragrances","rYTs0xE6YAY"),
 ("13","bonappetit_12_rice_microscope","ZDYg9SQthas"),
 ("14","foodexplained_every_rice","1X5g92z_OUU"),
 ("15","epicurious_rice_10_countries","pFgndOFYmys"),
 ("16","insider_16_rice_dishes","qb-gcaO_UIg"),
 ("17","insider_29_breads","C8U23AS1irY"),
 ("18","insider_cheese_around_world","2NutfCHAyNM"),
 ("19","bonappetit_every_egg_59","qWAagS_MANg"),
 ("20","epicurious_every_mushroom","wnCCdpt8y6w"),
 ("21","tasty_party_rice_africa","F1ku3Rljj1c"),
 ("22","greatbigstory_7_rice_dishes","ihWdzgsIAIM"),
]
NAMES = {"maxresdefault":"thumb","maxres1":"f25","maxres2":"f50","maxres3":"f75"}
for nn, slug, vid in VIDEOS:
    d = root/"frames"/f"{nn}_{slug}"; d.mkdir(parents=True, exist_ok=True)
    for src, dst in NAMES.items():
        shutil.copyfile(root/"raw"/vid/f"{src}.jpg", d/f"{dst}.jpg")
    q = root/"raw"/"_quads"/f"{vid}.jpg"
    (root/"frames"/"_review_quads").mkdir(exist_ok=True)
    shutil.copyfile(q, root/"frames"/"_review_quads"/f"{nn}_{slug}.jpg")
print("ok", len(VIDEOS))
