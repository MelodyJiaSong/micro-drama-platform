import json,sys,urllib.request,urllib.parse
B="http://127.0.0.1:8766/api/episode-workflow"; EP="ai_videos/chuanyue_yiri/episodes/ep01"
H={"Content-Type":"application/json","Origin":"http://127.0.0.1:8766"}
def get():
    return json.load(urllib.request.urlopen(B+"?episode_path="+urllib.parse.quote(EP),timeout=60))
def mods(): return {m["id"]:m for m in get()["modules"]}
def post(body):
    r=urllib.request.Request(B,data=json.dumps(body).encode(),headers=H,method="POST")
    try: return json.load(urllib.request.urlopen(r,timeout=600))
    except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode()[:500]); raise
