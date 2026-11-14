"""QC: 按 y 坐标把 DYB Table 3 每行拼起来，打印含指定国名的行（独立于 parse_dyb.py）。"""
import sys, pymupdf
doc = pymupdf.open(sys.argv[1]); names = sys.argv[2:]
for pno, page in enumerate(doc, 1):
    words = page.get_text('words')
    rows = {}
    for w in words:
        rows.setdefault(round(w[1] / 3), []).append(w)
    for k in sorted(rows):
        line = ' '.join(x[4] for x in sorted(rows[k], key=lambda w: w[0]))
        for n in names:
            if line.startswith(n):
                # 也打印下一行（名称跨两行时数值常在第二行）
                nxt = rows.get(k + 3) or rows.get(k + 4) or []
                print(f'p{pno} | {line[:200]}  || next: {" ".join(x[4] for x in sorted(nxt, key=lambda w: w[0]))[:160]}')
