# -*- coding: utf-8 -*-
"""t00 实验：教电脑认手写数字（scikit-learn 自带 digits，即 UCI Optical Recognition of Handwritten Digits 的 8×8 版，1797 张）。
系统 Python 跑（要 scikit-learn），结果写 scenes/data.json 给网页场景用；讲稿里的数字由文末断言守住，数据变了先改讲稿。

    python edu_videos/ai_terms/t00_what_is_ai/scenes/data.py

设定：固定种子 0 分出 300 张「考试题」（模型从没见过），其余 1497 张里依次取前 N 张当「练习题」，
逻辑回归（不讲内部，只说「看例子调整自己」）训练后在考试题上算准确率；每个 N 重复 20 次（换练习题的抽法），取中位数。
「把握」示例取考试题里第一张 3（讲稿 s5「这张图，它说：96% 是三」）。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression

OUT = Path(__file__).resolve().parent / "data.json"
SIZES = (10, 30, 100, 300, 1000, 1497)
REPEATS = 20


def main() -> None:
    d = load_digits()
    X, y = d.data / 16.0, d.target
    rng = np.random.default_rng(0)
    order = rng.permutation(len(y))
    test, pool = order[:300], order[300:]

    acc, cover10, draws10 = {}, [], []
    for n in SIZES:
        runs = []
        for r in range(REPEATS if n < len(pool) else 1):
            pick = np.random.default_rng(100 + r).permutation(pool)[:n]
            if n == 10:
                cover10.append(len(set(y[pick].tolist())))      # 随机抽 10 张覆盖了几种数字（讲稿 l29）
                draws10.append([int(v) for v in y[pick]])
            m = LogisticRegression(max_iter=2000)
            m.fit(X[pick], y[pick])
            runs.append(float((m.predict(X[test]) == y[test]).mean()))
        acc[n] = float(np.median(runs))

    m = LogisticRegression(max_iter=2000).fit(X[pool], y[pool])
    pred = m.predict(X[test])
    wrong = [int(i) for i in test[pred != y[test]]]
    probe = int(next(i for i in test if y[i] == 3))

    # 屏幕上展示的样例：每个数字取练习池里前 3 张（看出同一个数字写法各不相同）
    samples = {k: [X[i].reshape(8, 8).round(3).tolist() for i in pool if y[i] == k][:3] for k in range(10)}
    # 「没见过的东西」：人画的笑脸和字母 A（不是数字），看模型照样给出一个数字和把握（讲稿 s7 第一条提醒）
    OOD = {"smile": ["..####..", ".#....#.", "#.#..#.#", "#......#", "#.#..#.#", "#..##..#", ".#....#.", "..####.."],
           "A": ["...##...", "..#..#..", "..#..#..", ".#....#.", ".######.", ".#....#.", ".#....#.", ".#....#."]}
    ood = {}
    for k, rows in OOD.items():
        img = np.array([[1.0 if c == "#" else 0.0 for c in r] for r in rows]).reshape(1, 64)
        pr = m.predict_proba(img)[0]
        ood[k] = {"img": img.reshape(8, 8).tolist(), "pred": int(pr.argmax()), "conf": float(pr.max().round(4)), "proba": pr.round(4).tolist()}
    # 讲稿 s1「这些全是真人写的三」：练习池里模型有六成以上把握认作 3 的（人也认得出），按离「平均的 3」由近到远排，
    # 等距取 12 张：第一张最端正（l10 单独放大），后面越来越胖、瘦、歪
    cand = [i for i in pool if y[i] == 3 and m.predict_proba(X[i:i + 1])[0][3] > 0.6]
    mean3 = X[cand].mean(axis=0)
    cand.sort(key=lambda i: float(np.linalg.norm(X[i] - mean3)))
    threes = [cand[int(round(k))] for k in np.linspace(0, 0.9 * (len(cand) - 1), 12)]   # 最怪的一成不用，免得看着像 7
    out = {
        "source": "scikit-learn load_digits = UCI Optical Recognition of Handwritten Digits (Alpaydin & Kaynak, 1998), 8x8",
        "n_total": int(len(y)), "n_test": int(len(test)), "n_pool": int(len(pool)),
        "sizes": list(SIZES), "accuracy": [acc[n] for n in SIZES], "repeats": REPEATS, "cover10": cover10, "draw10": next(d for d in draws10 if len(set(d)) == 6),   # 画面展示一次「只覆盖六种」的抽法（中位数附近）
       
        "full_wrong": len(wrong), "wrong_examples": [{"img": X[i].reshape(8, 8).round(3).tolist(), "true": int(y[i]),
                                                       "pred": int(m.predict(X[i:i + 1])[0]),
                                                       "conf": float(m.predict_proba(X[i:i + 1]).max().round(4))} for i in wrong[:4]],
        "samples": samples,
        "threes": [X[i].reshape(8, 8).round(3).tolist() for i in threes],
        "ood": ood,
        "probe": {"img": X[probe].reshape(8, 8).round(3).tolist(), "true": int(y[probe]),
                  "proba": m.predict_proba(X[probe:probe + 1])[0].round(4).tolist()},
    }
    check(out)
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print({n: round(acc[n], 3) for n in SIZES}, "wrong", len(wrong), "probe", out["probe"]["true"], max(out["probe"]["proba"]), out["ood"], [(w["true"], w["pred"], w["conf"]) for w in out["wrong_examples"]])


def check(o: dict) -> None:
    """讲稿 v2 与 claims.json 的说法（C01–C06）。"""
    pct = lambda v: round(100 * v)
    acc = dict(zip(o["sizes"], o["accuracy"]))
    assert o["n_total"] == 1797 and o["n_test"] == 300 and o["n_pool"] == 1497, "l26/l27 张数"
    assert (pct(acc[10]), pct(acc[100]), pct(acc[1497])) == (37, 88, 97), "l29–l31 准确率"
    assert 5 <= min(o["cover10"]) and max(o["cover10"]) <= 9, "l29「随便抽十个，往往有几个数字一张都没见过」"
    assert o["full_wrong"] == 10, "l33「错了十道」"
    assert o["probe"]["true"] == 3 and pct(max(o["probe"]["proba"])) == 96, "l35「96% 是三」"
    assert (o["ood"]["A"]["pred"], pct(o["ood"]["A"]["conf"])) == (4, 92), "l50「字母 A，92% 是四」"
    assert abs(sum(o["ood"]["A"]["proba"]) - 1) < 1e-3, "l51「把握只是十个数字间比较」：十类概率和为 1"
    w2 = next(w for w in o["wrong_examples"] if w["true"] == 2)
    assert (w2["pred"], pct(w2["conf"])) == (1, 81), "l33/l52「这张二，81% 说是一」"


if __name__ == "__main__":
    main()
