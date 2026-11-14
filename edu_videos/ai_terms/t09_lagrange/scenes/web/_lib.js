/* t09 各场景共用的地图构件。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   颜色含义：山（等高带）= 琥珀浅色渐深，围栏 = 墨黑虚线，「最好的点」= 琥珀实心点白边，出圈 = 红，在围栏上 = 绿，圈内 = 灰。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";

/* 在 <svg id=…> 里画等高线地图。scale：每单位多少像素。peak 可换（小地图里山顶在圈内）。 */
function makeMap(sel, { scale = 140, dom = D.domain, peak = D.peak, R = D.R, levels = D.levels, labels = true } = {}) {
  const W = (dom.x[1] - dom.x[0]) * scale, H = (dom.y[1] - dom.y[0]) * scale;
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear(dom.x, [0, W]), y = d3.scaleLinear(dom.y, [H, 0]);
  const clip = "clip" + sel.replace(/[^a-z0-9]/gi, "");
  svg.append("defs").append("clipPath").attr("id", clip).append("rect").attr("width", W).attr("height", H).attr("rx", 28);
  const root = svg.append("g").attr("clip-path", `url(#${clip})`);
  root.append("rect").attr("width", W).attr("height", H).attr("fill", css("--surface2"));
  const hill = root.append("g");
  // 等高带：从外到里，一圈比一圈深（山越高颜色越浓）
  const bands = [0, ...levels].map((lv, i) => hill.append("circle").attr("cx", x(peak[0])).attr("cy", y(peak[1]))
    .attr("r", Math.sqrt(Math.max(D.H - lv, 0.0001)) * scale).attr("fill", css("--accent")).attr("fill-opacity", 0.05 + i * 0.05).node());
  const lines = levels.map(lv => hill.append("circle").attr("cx", x(peak[0])).attr("cy", y(peak[1]))
    .attr("r", Math.sqrt(D.H - lv) * scale).attr("fill", "none").attr("stroke", css("--accent")).attr("stroke-opacity", .55).attr("stroke-width", 2).node());
  const top = root.append("g");
  const summit = top.append("path").attr("d", d3.symbol(d3.symbolTriangle, 520)()).attr("transform", `translate(${x(peak[0])},${y(peak[1])})`)
    .attr("fill", css("--ink")).node();
  const camp = top.append("circle").attr("cx", x(0)).attr("cy", y(0)).attr("r", 9).attr("fill", css("--ink")).node();
  const fence = top.append("circle").attr("cx", x(0)).attr("cy", y(0)).attr("r", R * scale).attr("fill", "none")
    .attr("stroke", css("--ink")).attr("stroke-width", 6).attr("stroke-dasharray", "2 14").attr("stroke-linecap", "round").node();
  const over = svg.append("g");
  const api = {
    svg, x, y, W, H, scale, bands, lines, summit, camp, fence, over,
    /* 「最好的点」：琥珀实心点白边 */
    dot(p) {
      return over.append("circle").attr("cx", x(p[0])).attr("cy", y(p[1])).attr("r", 17).attr("fill", css("--accent"))
        .attr("stroke", css("--surface")).attr("stroke-width", 5).node();
    },
    ring(r, color = "--ink", w = 4, dash = null, cx = 0, cy = 0) {
      const c = over.append("circle").attr("cx", x(cx)).attr("cy", y(cy)).attr("r", r * scale).attr("fill", "none")
        .attr("stroke", css(color)).attr("stroke-width", w).node();
      if (dash) c.setAttribute("stroke-dasharray", dash);
      return c;
    },
    seg(a, b, color, w = 5, dash = null) {
      const l = over.append("line").attr("x1", x(a[0])).attr("y1", y(a[1])).attr("x2", x(b[0])).attr("y2", y(b[1]))
        .attr("stroke", css(color)).attr("stroke-width", w).attr("stroke-linecap", "round").node();
      if (dash) l.setAttribute("stroke-dasharray", dash);
      return l;
    },
    /* 从 p 出发、沿单位向量 u 画一支长 len（像素）的箭头 */
    arrow(p, u, len, color, w = 7) {
      const g = over.append("g").attr("color", css(color));
      const x0 = x(p[0]), y0 = y(p[1]), x1 = x0 + u[0] * len, y1 = y0 - u[1] * len;
      g.append("line").attr("x1", x0).attr("y1", y0).attr("x2", x1).attr("y2", y1).attr("stroke", "currentColor").attr("stroke-width", w).attr("stroke-linecap", "round");
      const a = Math.atan2(y1 - y0, x1 - x0), h = 26;
      g.append("path").attr("d", `M${x1 + Math.cos(a) * 6},${y1 + Math.sin(a) * 6} L${x1 - h * Math.cos(a - .45)},${y1 - h * Math.sin(a - .45)} L${x1 - h * Math.cos(a + .45)},${y1 - h * Math.sin(a + .45)} Z`).attr("fill", "currentColor");
      return g.node();
    },
    /* 地图上某个坐标旁放一段文字（HTML，已按语言取好），返回元素 */
    note(html, at, dx = 0, dy = 0, cls = "caption") {
      const box = document.querySelector(sel).getBoundingClientRect(), stage = document.getElementById("stage").getBoundingClientRect();
      const el = document.createElement("div");
      el.className = cls; el.style.position = "absolute"; el.style.whiteSpace = "nowrap"; el.innerHTML = html;
      el.style.left = (box.left - stage.left + x(at[0]) + dx) + "px";
      el.style.top = (box.top - stage.top + y(at[1]) + dy) + "px";
      document.getElementById("stage").appendChild(el);
      return el;
    },
  };
  return api;
}
/* 让点走到 p（GSAP 改 cx / cy） */
function moveDot(M, el, p, at, d = .7) {
  return EDU.tl.to(el, { attr: { cx: M.x(p[0]), cy: M.y(p[1]) }, duration: d, ease: "power2.inOut" }, at);
}
/* 数字从 from 滚到 to（EDU.count 只能从 0 起）；fmt 缺省去掉末尾的 0（1.50 → 1.5，3.00 → 3） */
const trim2 = v => v.toFixed(2).replace(/\.?0+$/, "");
function countTo(el, at, from, to, d = .8, fmt = trim2) {
  const o = { v: from };
  return EDU.tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v); } }, at);
}
