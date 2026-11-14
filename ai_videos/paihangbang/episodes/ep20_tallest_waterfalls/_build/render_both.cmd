@echo off
cd /d C:\workspace\micro-drama-platform\projects\rank_scroll
python -m rank_scroll render ..\..\ai_videos\paihangbang\episodes\ep20_tallest_waterfalls > ..\..\ai_videos\paihangbang\episodes\ep20_tallest_waterfalls\_build\render_default.log 2>&1
python -m rank_scroll render ..\..\ai_videos\paihangbang\episodes\ep20_tallest_waterfalls --allow-risk-images > ..\..\ai_videos\paihangbang\episodes\ep20_tallest_waterfalls\_build\render_risk.log 2>&1
echo done > ..\..\ai_videos\paihangbang\episodes\ep20_tallest_waterfalls\_build\render_done.flag
