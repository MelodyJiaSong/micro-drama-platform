"""从 v12 编译的 ep1_s1_st3 prompt 派生 2×2 四个变体：顺序（现行 / 镜头在前）× 方向（东南西北 / 以镜头为参照）。
只动这两个因素，其余逐字相同。"""
from pathlib import Path

HERE = Path(__file__).parent
base = (HERE / "base_prompt.txt").read_text(encoding="utf-8")
lines = base.split("\n")


def idx(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, prefix
    return hits[0]


DIR = {  # 方向：东南西北 → 镜头参照（一一替换，信息量不变）
    "走位：Riley 由南向北走进门洞，镜头在她身后约两米跟着走；第 4 秒她停步、转身面向镜头。挑夫与骡子在她前方几步继续往北走出画面。工人在门洞西墙边的脚手架上。":
    "走位：Riley 背对镜头、朝画面深处走进门洞，镜头在她身后约两米跟着走；第 4 秒她停步、转身面向镜头。挑夫与骡子在她前方几步，继续朝画面深处走，从门洞远端的亮口走出画面。工人在门洞里画面左侧墙边的脚手架上。",
    "光线：清晨，门洞里是阴凉的阴影，门洞另一头（北）是被晨光照亮的街，形成明亮的出口；自然光。":
    "光线：清晨，门洞里是阴凉的阴影，门洞另一头（画面深处）是被晨光照亮的街，形成明亮的出口；自然光。",
}
BEATS_OLD = "动作：0–3秒 Riley 背对镜头跟着挑夫和骡子走进门洞，骡蹄声在门洞里回响；3–4秒 她抬头看墙边脚手架上递灰浆桶的工人；4–8秒 她停步转身，面对镜头压低声音说那句话，笑着眨眨眼"
BEATS_CAM = ("动作：0–3秒 镜头在她身后约两米平稳向前跟：Riley 背对镜头跟着挑夫和骡子走进门洞，骡蹄声在门洞里回响；"
             "3–4秒 镜头继续跟：她抬头看墙边脚手架上递灰浆桶的工人；"
             "4–8秒 镜头停住，她成腰以上中景：她停步转身，面对镜头压低声音说那句话，笑着眨眨眼")


def variant(order: bool, direction: bool) -> str:
    ls = list(lines)
    if direction:
        for old, new in DIR.items():
            ls[ls.index(old)] = new
    if order:
        ls[ls.index(BEATS_OLD)] = BEATS_CAM
        cam = next(i for i, l in enumerate(ls) if l.startswith("镜头："))
        cam_line = ls.pop(cam)
        pic = next(i for i, l in enumerate(ls) if l.startswith("画面："))
        ls.insert(pic, cam_line)          # 镜头提到「画面」之前（场景之后）
    return "\n".join(ls)


for name, o, d in [("A_v12", False, False), ("O_camfirst", True, False), ("D_camdir", False, True), ("OD_both", True, True)]:
    (HERE / name).mkdir(exist_ok=True)
    (HERE / name / "prompt.txt").write_text(variant(o, d), encoding="utf-8")
    print(name, len(variant(o, d)), "字")
assert variant(False, False) == base
