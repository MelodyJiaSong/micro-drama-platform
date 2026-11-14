/* t11 各场景共用的构件。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   颜色含义：数据点 = 墨黑，模型直线 = 琥珀，误差竖线与平方方块 = 红，最低点 = 绿，地形图（分数）= 琥珀浅色渐深（分越高越深）。
   旋钮（全季统一画法，s1_bible）：圆盘、一根指针、下面标读数。 */
const D = EDU.S.data;
(() => {   // 旋钮的版式（各场景共用）
  const st = document.createElement("style");
  st.textContent = `.knob { display: flex; flex-direction: column; align-items: center; gap: 10px; }
    .knob .kv { font-size: var(--fs-h2); font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1; }`;
  document.head.appendChild(st);
})();
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const trim2 = v => v.toFixed(2).replace(/\.?0+$/, "");
/* 旋钮读数：中文 3.5 / 10.2；英文按钱写 $3.50 / $10.20（整数不带小数） */
const money = v => Math.abs(v - Math.round(v)) < 1e-9 ? EDU.tr("", "$") + v.toFixed(0) : EDU.tr(trim2(v), "$" + v.toFixed(2));

/* 数字从 from 滚到 to（EDU.count 只能从 0 起）；fmt 缺省去掉末尾的 0 */
function countTo(el, at, from, to, d = .8, fmt = trim2) {
  const o = { v: from };
  return EDU.tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v); } }, at);
}

/* 旋钮：在容器 el 里画圆盘 + 指针 + 读数。min..max 映射到 −135°..+135°。返回 { set(v, at, d) } */
function knob(el, { label, min, max, value, fmt = money, size = 170 }) {
  const box = typeof el === "string" ? document.querySelector(el) : el;
  box.classList.add("knob");
  box.innerHTML = `<div class="kl eyebrow">${label}</div><svg width="${size}" height="${size}"></svg><div class="kv"></div>`;
  /* 画法照 t10 的全季旋钮：白色圆盘＋细边＋柔和投影；270° 刻度弧（11 根刻度、每 5 根一长）；已拧过的弧段琥珀、未拧到的浅灰；墨黑圆头指针、圆心琥珀小点 */
  const S = size, c = S / 2, rDisc = S * 0.40, rArc = S * 0.47, w = Math.max(3, S * 0.035);
  const svg = d3.select(box.querySelector("svg")).style("overflow", "visible");
  const fid = "ks" + Math.round(Math.random() * 1e9);
  svg.append("defs").append("filter").attr("id", fid).attr("x", "-30%").attr("y", "-30%").attr("width", "160%").attr("height", "160%")
    .append("feDropShadow").attr("dx", 0).attr("dy", S * 0.03).attr("stdDeviation", S * 0.04).attr("flood-color", "#1D1D1F").attr("flood-opacity", .12);
  const arcD = (a0, a1) => d3.arc().innerRadius(rArc).outerRadius(rArc).startAngle(a0 * Math.PI / 180).endAngle(a1 * Math.PI / 180)();
  const g0 = svg.append("g").attr("transform", `translate(${c},${c})`);
  g0.append("path").attr("d", arcD(-135, 135)).attr("fill", "none").attr("stroke", css("--hair")).attr("stroke-width", w).attr("stroke-linecap", "round");
  const fillArc = g0.append("path").attr("fill", "none").attr("stroke", css("--accent")).attr("stroke-width", w).attr("stroke-linecap", "round");
  for (let i = 0; i < 11; i++) {
    const a = (-135 + 27 * i) * Math.PI / 180, r0 = rDisc * 0.86, r1 = rDisc * (i % 5 === 0 ? 0.70 : 0.76);
    g0.append("line").attr("x1", Math.sin(a) * r0).attr("y1", -Math.cos(a) * r0).attr("x2", Math.sin(a) * r1).attr("y2", -Math.cos(a) * r1)
      .attr("stroke", css("--faint")).attr("stroke-width", Math.max(1.5, S * 0.012)).attr("stroke-linecap", "round");
  }
  svg.append("circle").attr("cx", c).attr("cy", c).attr("r", rDisc).attr("fill", css("--surface")).attr("stroke", css("--hair"))
    .attr("stroke-width", Math.max(1.5, S * 0.008)).attr("filter", `url(#${fid})`);
  const ptr = svg.append("g");
  ptr.append("line").attr("x1", c).attr("y1", c).attr("x2", c).attr("y2", c - rDisc * 0.78).attr("stroke", css("--ink")).attr("stroke-width", Math.max(4, S * 0.05)).attr("stroke-linecap", "round");
  svg.append("circle").attr("cx", c).attr("cy", c).attr("r", Math.max(4, S * 0.05)).attr("fill", css("--accent"));
  const kv = box.querySelector(".kv"), ang = v => -135 + 270 * Math.max(0, Math.min(1, (v - min) / (max - min)));
  const st = { v: value };
  const draw = () => { const a = ang(st.v); ptr.attr("transform", `rotate(${a},${c},${c})`); fillArc.attr("d", a > -134.9 ? arcD(-135, a) : null); kv.textContent = fmt(st.v); };
  draw();
  return {
    box,
    set(v, at, d = .9, from = null) {
      const f = from ?? null;
      return EDU.tl.fromTo(st, { v: f ?? st.v }, { v, duration: d, ease: "power2.inOut", immediateRender: false, onUpdate: draw }, at);
    },
    /* 按顺序拧：列表 [[值, 时刻, 时长], …]，起点 from */
    path(from, steps) { let p = from; steps.forEach(([v, at, d]) => { EDU.tl.fromTo(st, { v: p }, { v, duration: d ?? .9, ease: "power2.inOut", immediateRender: false, onUpdate: draw }, at); p = v; }); },
  };
}

/* 散点图：十二趟打车 + 模型直线 + 误差竖线 + 平方方块。state {b, m} 由 GSAP 补间，render() 按当前旋钮重画。 */
function makeChart(sel, { W = 980, H = 640, xMax = 14, yMax = 50, pad = { l: 90, b: 70, t: 20, r: 30 } } = {}) {
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear([0, xMax], [pad.l, W - pad.r]), y = d3.scaleLinear([0, yMax], [H - pad.b, pad.t]);
  const ky = y(0) - y(1);                       // 每元多少像素（方块边长用）
  const g = svg.append("g");
  const axes = g.append("g");
  axes.append("line").attr("class", "axis-base").attr("x1", pad.l).attr("x2", W - pad.r).attr("y1", y(0)).attr("y2", y(0));
  axes.append("line").attr("class", "axis-base").attr("x1", pad.l).attr("x2", pad.l).attr("y1", y(0)).attr("y2", pad.t);
  [0, 5, 10].forEach(v => axes.append("text").attr("x", x(v)).attr("y", y(0) + 38).attr("text-anchor", "middle").attr("font-size", 26).attr("fill", css("--sub")).text(v));
  [0, 20, 40].forEach(v => axes.append("text").attr("x", pad.l - 18).attr("y", y(v) + 9).attr("text-anchor", "end").attr("font-size", 26).attr("fill", css("--sub")).text(v));
  const xt = axes.append("text").attr("x", W - pad.r).attr("y", y(0) + 38).attr("text-anchor", "end").attr("font-size", 28).attr("fill", css("--ink2")).text(EDU.tr("公里", "km")).node();
  const yt = axes.append("text").attr("x", pad.l + 16).attr("y", pad.t + 22).attr("font-size", 28).attr("fill", css("--ink2")).text(EDU.tr("车费（元）", "Fare ($)")).node();
  const sqG = g.append("g"), errG = g.append("g");
  const line = g.append("line").attr("stroke", css("--accent")).attr("stroke-width", 7).attr("stroke-linecap", "round").node();
  const ptG = g.append("g");
  const pts = D.rides.map(r => ptG.append("circle").attr("cx", x(r.km)).attr("cy", y(r.fare)).attr("r", 11).attr("fill", css("--ink")).node());
  const errs = D.rides.map(() => errG.append("line").attr("stroke", css("--d-bad")).attr("stroke-width", 5).attr("stroke-linecap", "round").node());
  const sqs = D.rides.map(() => sqG.append("path").attr("fill", css("--d-bad")).attr("fill-opacity", .16).attr("stroke", css("--d-bad")).attr("stroke-opacity", .55).attr("stroke-width", 2).node());
  const st = { b: 0, m: 0 };
  const render = () => {
    const f = v => st.b + st.m * v;
    line.setAttribute("x1", x(0)); line.setAttribute("y1", y(f(0)));
    line.setAttribute("x2", x(xMax)); line.setAttribute("y2", y(f(xMax)));
    D.rides.forEach((r, i) => {
      const p = f(r.km), e = p - r.fare, s = Math.abs(e) * ky;
      errs[i].setAttribute("x1", x(r.km)); errs[i].setAttribute("x2", x(r.km));
      errs[i].setAttribute("y1", y(r.fare)); errs[i].setAttribute("y2", y(p));
      // 方块往左长：右边那条边就是误差竖线
      sqs[i].setAttribute("d", `M${x(r.km) - s},${Math.min(y(r.fare), y(p))}h${s}v${s}h${-s}Z`);
    });
  };
  const api = {
    svg, x, y, W, H, ky, g, line, pts, errs, sqs, xt, yt, axes, st,
    set(b, m) { st.b = b; st.m = m; render(); },
    /* 旋钮补间：从 (b0, m0) 拧到 (b1, m1) */
    turn(b0, m0, b1, m1, at, d = .9) {
      return EDU.tl.fromTo(st, { b: b0, m: m0 }, { b: b1, m: m1, duration: d, ease: "power2.inOut", immediateRender: false, onUpdate: render }, at);
    },
    /* 图上某个数据坐标旁放一段文字（SVG text），返回节点 */
    text(t, at, dx = 0, dy = 0, { size = 30, col = "--ink", weight = 600, anchor = "start", halo = true } = {}) {
      const n = g.append("text").attr("x", x(at[0]) + dx).attr("y", y(at[1]) + dy).attr("font-size", size).attr("font-weight", weight)
        .attr("text-anchor", anchor).attr("fill", css(col)).text(t);
      if (halo) n.attr("paint-order", "stroke").attr("stroke", css("--bg")).attr("stroke-width", 8).attr("stroke-linejoin", "round");
      return n.node();
    },
  };
  return api;
}

/* 分数地形图（t04 梯度下降接着用同样画法）：横轴 起步价，纵轴 每公里；颜色 = 分数，越高越深；等高线 D.land.levels。 */
function makeLand(sel, { W = 940, H = 640, pad = { l: 100, b: 76, t: 16, r: 24 } } = {}) {
  const L = D.land, svg = d3.select(sel).attr("width", W).attr("height", H);
  const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
  const x = d3.scaleLinear(L.base, [pad.l, pad.l + iw]), y = d3.scaleLinear(L.per_km, [pad.t + ih, pad.t]);
  const clip = "clip" + sel.replace(/[^a-z0-9]/gi, "");
  svg.append("defs").append("clipPath").attr("id", clip).append("rect").attr("x", pad.l).attr("y", pad.t).attr("width", iw).attr("height", ih).attr("rx", 24);
  const root = svg.append("g").attr("clip-path", `url(#${clip})`);
  root.append("rect").attr("x", pad.l).attr("y", pad.t).attr("width", iw).attr("height", ih).attr("fill", css("--surface2"));
  const sx = iw / (L.nx - 1), sy = ih / (L.ny - 1);
  const proj = d3.geoTransform({ point(px, py) { this.stream.point(pad.l + (px - .5) * sx, pad.t + ih - (py - .5) * sy); } });
  const path = d3.geoPath(proj);
  const cs = d3.contours().size([L.nx, L.ny]).thresholds(L.levels)(L.z);
  const bands = cs.map(c => root.append("path").attr("d", path(c)).attr("fill", css("--accent")).attr("fill-opacity", .085).node());
  const lines = cs.map(c => root.append("path").attr("d", path(c)).attr("fill", "none").attr("stroke", css("--accent")).attr("stroke-opacity", .6).attr("stroke-width", 2).node());
  const axes = svg.append("g");
  [0, 5, 10, 15, 20].forEach(v => axes.append("text").attr("x", x(v)).attr("y", pad.t + ih + 36).attr("text-anchor", "middle").attr("font-size", 26).attr("fill", css("--sub")).text(v));
  [1, 2, 3, 4].forEach(v => axes.append("text").attr("x", pad.l - 16).attr("y", y(v) + 9).attr("text-anchor", "end").attr("font-size", 26).attr("fill", css("--sub")).text(v));
  const xt = axes.append("text").attr("x", pad.l + iw).attr("y", pad.t + ih + 70).attr("text-anchor", "end").attr("font-size", 28).attr("fill", css("--ink2")).text(EDU.tr("起步价 →", "Starting fare →")).node();
  const yt = axes.append("text").attr("transform", `translate(${pad.l - 62},${pad.t}) rotate(-90)`).attr("text-anchor", "end").attr("font-size", 28).attr("fill", css("--ink2")).text(EDU.tr("每公里 →", "Per km →")).node();
  const over = svg.append("g");
  return {
    svg, x, y, W, H, bands, lines, xt, yt, axes, over,
    /* 一组拧法的点：墨黑圆点 + 白边 */
    dot(b, m, col = "--ink", r = 15) {
      return over.append("circle").attr("cx", x(b)).attr("cy", y(m)).attr("r", r).attr("fill", css(col)).attr("stroke", css("--surface")).attr("stroke-width", 5).node();
    },
    text(t, b, m, dx = 0, dy = 0, { size = 30, col = "--ink", weight = 600, anchor = "start" } = {}) {
      return over.append("text").attr("x", x(b) + dx).attr("y", y(m) + dy).attr("font-size", size).attr("font-weight", weight).attr("text-anchor", anchor)
        .attr("fill", css(col)).attr("paint-order", "stroke").attr("stroke", css("--surface2")).attr("stroke-width", 8).attr("stroke-linejoin", "round").text(t).node();
    },
  };
}

/* 一台带两个旋钮的机器（简笔）：圆角机身、两个小旋钮、顶上一块分数屏。返回各部件节点 */
function machine(sel, { w = 520, h = 360 } = {}) {
  const svg = d3.select(sel).attr("width", w + 40).attr("height", h + 150);
  const g = svg.append("g").attr("transform", "translate(20,130)");
  const body = g.append("rect").attr("width", w).attr("height", h).attr("rx", 44).attr("fill", css("--surface")).attr("stroke", css("--hair")).attr("stroke-width", 4).node();
  const screen = g.append("g").attr("transform", `translate(${w / 2 - 130},-110)`);
  screen.append("rect").attr("width", 260).attr("height", 96).attr("rx", 22).attr("fill", css("--ink"));
  const scoreT = screen.append("text").attr("x", 130).attr("y", 66).attr("text-anchor", "middle").attr("font-size", 54).attr("font-weight", 700).attr("fill", css("--surface")).text("—").node();
  const knobs = [w * .3, w * .7].map(cx => {
    const k = g.append("g").attr("transform", `translate(${cx},${h * .55})`);
    k.append("circle").attr("r", 78).attr("fill", css("--surface2")).attr("stroke", css("--hair")).attr("stroke-width", 3);
    const p = k.append("g");
    p.append("line").attr("x1", 0).attr("y1", 0).attr("x2", 0).attr("y2", -58).attr("stroke", css("--ink")).attr("stroke-width", 10).attr("stroke-linecap", "round");
    k.append("circle").attr("r", 13).attr("fill", css("--accent"));
    return p.node();
  });
  const turn = (i, a0, a1, at, d = .7) => {
    const o = { a: a0 };
    return EDU.tl.fromTo(o, { a: a0 }, { a: a1, duration: d, ease: "power2.inOut", immediateRender: false, onUpdate: () => knobs[i].setAttribute("transform", `rotate(${o.a})`) }, at);
  };
  knobs[0].setAttribute("transform", "rotate(-40)"); knobs[1].setAttribute("transform", "rotate(30)");
  return { svg, body, screen: screen.node(), scoreT, knobs, turn };
}
