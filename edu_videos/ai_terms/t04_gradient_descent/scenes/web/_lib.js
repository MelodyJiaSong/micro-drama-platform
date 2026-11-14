/* t04 各场景共用的构件：旋钮（照 t10 的第 1 季统一画法复制一份，不共用文件）、地形图、下山的路。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   旋钮是第 1 季统一画法（s1_bible「画面」）：圆盘、一根指针、下面标读数。
     - 圆盘：白底（--surface）、细边（--hair）、柔和投影；刻度弧 270°（左下 −135° 到右下 +135°），11 根刻度。
     - 已拧过的那段弧用琥珀（--accent），没拧到的留浅灰（--hair）；指针墨黑（--ink）圆头，圆心琥珀小圆点。
     - 名字在圆盘上方（小号灰字），读数在圆盘下方（大号、等宽数字、可带单位）。
   地形图（与 t11 同一张）：颜色 = 分数，越高越深（琥珀），最低点绿色；走的路：合适 = 琥珀点线，太小 = 灰，太大 = 红，小批量 = 紫（--d-valid）。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const A0 = -135, A1 = 135;             // 刻度弧的起止角（度，0 = 正上方，顺时针为正）

/* 极坐标 → 平面（角度 0 朝上、顺时针） */
const pol = (cx, cy, r, deg) => [cx + r * Math.sin(deg * Math.PI / 180), cy - r * Math.cos(deg * Math.PI / 180)];
function arcPath(cx, cy, r, a, b) {
  if (b - a < 0.01) b = a + 0.01;
  const [x0, y0] = pol(cx, cy, r, a), [x1, y1] = pol(cx, cy, r, b);
  return `M${x0},${y0} A${r},${r} 0 ${b - a > 180 ? 1 : 0} 1 ${x1},${y1}`;
}

/* 在 parent（元素或选择器）里放一个旋钮。
   opt：size（圆盘直径 px）、min / max、value、label（HTML，已按语言取好）、unit（读数后的小字）、fmt（读数格式）、
        left / top（绝对定位，相对 parent）、showLabel / showReading（缺省都显示）、ticks（刻度数，缺省 11）。
   返回 api：el（外层 div）、set(v) 立即设、turn(at, from, to, d) 在时间线上拧、value。 */
function knob(parent, opt = {}) {
  const o = Object.assign({ size: 220, min: 0, max: 10, value: 0, label: "", unit: "", fmt: v => v.toFixed(1),
                            left: 0, top: 0, showLabel: true, showReading: true, ticks: 11, readingSize: null }, opt);
  const host = typeof parent === "string" ? document.querySelector(parent) : parent;
  const el = document.createElement("div");
  el.className = "knob";
  Object.assign(el.style, { position: "absolute", left: o.left + "px", top: o.top + "px", width: o.size + "px",
                            display: "flex", flexDirection: "column", alignItems: "center" });
  const S = o.size, c = S / 2, rDisc = S * 0.40, rArc = S * 0.47, w = Math.max(3, S * 0.035);
  const lab = document.createElement("div");
  lab.className = "knob-label"; lab.innerHTML = o.label;
  Object.assign(lab.style, { fontSize: Math.max(22, S * 0.13) + "px", fontWeight: 600, color: "var(--sub)", whiteSpace: "nowrap",
                             marginBottom: S * 0.04 + "px", display: o.showLabel && o.label ? "block" : "none" });
  const svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("width", S); svg.setAttribute("height", S);
  svg.style.overflow = "visible";
  svg.innerHTML = `
    <defs><filter id="ks${Math.round(Math.random() * 1e9)}" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="${S * 0.03}" stdDeviation="${S * 0.04}" flood-color="#1D1D1F" flood-opacity=".12"/></filter></defs>
    <path class="k-track" d="${arcPath(c, c, rArc, A0, A1)}" fill="none" stroke="${css("--hair")}" stroke-width="${w}" stroke-linecap="round"/>
    <path class="k-fill" fill="none" stroke="${css("--accent")}" stroke-width="${w}" stroke-linecap="round"/>
    <g class="k-ticks"></g>
    <circle class="k-disc" cx="${c}" cy="${c}" r="${rDisc}" fill="${css("--surface")}" stroke="${css("--hair")}" stroke-width="${Math.max(1.5, S * 0.008)}"/>
    <g class="k-ptr"><line x1="${c}" y1="${c}" x2="${c}" y2="${c - rDisc * 0.78}" stroke="${css("--ink")}" stroke-width="${Math.max(4, S * 0.05)}" stroke-linecap="round"/></g>
    <circle cx="${c}" cy="${c}" r="${Math.max(4, S * 0.05)}" fill="${css("--accent")}"/>`;
  const filt = svg.querySelector("filter");
  svg.querySelector(".k-disc").setAttribute("filter", `url(#${filt.id})`);
  const tg = svg.querySelector(".k-ticks");
  for (let i = 0; i < o.ticks; i++) {
    const a = A0 + (A1 - A0) * i / (o.ticks - 1), [x0, y0] = pol(c, c, rDisc * 0.86, a), [x1, y1] = pol(c, c, rDisc * (i % 5 === 0 ? 0.70 : 0.76), a);
    const t = document.createElementNS(SVGNS, "line");
    t.setAttribute("x1", x0); t.setAttribute("y1", y0); t.setAttribute("x2", x1); t.setAttribute("y2", y1);
    t.setAttribute("stroke", css("--faint")); t.setAttribute("stroke-width", Math.max(1.5, S * 0.012)); t.setAttribute("stroke-linecap", "round");
    tg.appendChild(t);
  }
  const ptr = svg.querySelector(".k-ptr"), fill = svg.querySelector(".k-fill");
  const rd = document.createElement("div");
  rd.className = "knob-reading";
  Object.assign(rd.style, { fontSize: (o.readingSize || Math.max(28, S * 0.22)) + "px", fontWeight: 700, color: "var(--ink)", whiteSpace: "nowrap",
                            marginTop: S * 0.02 + "px", fontVariantNumeric: "tabular-nums", display: o.showReading ? "block" : "none" });
  rd.innerHTML = `<span class="v"></span><span class="u" style="font-size:.5em;font-weight:500;color:var(--sub);margin-left:.18em">${o.unit}</span>`;
  const rv = rd.querySelector(".v");
  el.append(lab, svg, rd);
  host.appendChild(el);
  const api = {
    el, svg, label: lab, reading: rd, value: o.value,
    set(v) {
      api.value = v;
      const k = Math.max(0, Math.min(1, (v - o.min) / (o.max - o.min))), a = A0 + (A1 - A0) * k;
      ptr.setAttribute("transform", `rotate(${a} ${c} ${c})`);
      fill.setAttribute("d", arcPath(c, c, rArc, A0, a));
      fill.style.opacity = k < 0.004 ? 0 : 1;
      rv.textContent = o.fmt(v);
    },
    /* 在时间线上把旋钮从 from 拧到 to（onUpdate 同时调 then(v)，好让图跟着动） */
    turn(at, from, to, d = 1.2, then = null) {
      const s = { v: from };
      return EDU.tl.fromTo(s, { v: from }, { v: to, duration: d, ease: "power2.inOut", immediateRender: false,
        onUpdate: () => { api.set(s.v); if (then) then(s.v); } }, at);
    },
  };
  api.set(o.value);
  return api;
}


/* 地形图：与 t11 损失函数同一张图（2026-11-10 对齐 t11 的 makeLand）：横轴起步价 0–20、纵轴每公里 1–4，
   等高线 2.5 / 5 / 10 / 20 / 40 / 80 / 160 / 320，每一圈琥珀 8.5% 叠上去（越高越深），等高线琥珀 60%、2px；最低点绿环（r30、线宽 7）+ 绿字「最低点」。
   D.land 的网格比 t11 宽（纵向 0–5），按数据坐标投影后裁到图框里，所以看上去和 t11 一样；
   只有第 03 章三张小图传 yDom: [0, 5]（学习率太大时要看得见来回跳）。
   opt：W / H、m（留给坐标轴的边）、yDom、axes、ticks、best、bestR、bestLabel。
   返回 api：x / y 比例尺、over（叠加层）、bestDot、bestLab、dot(p, color)、trail(color)、steps、arrow、note。 */
function makeLand(sel, { W = 1040, H = 700, m = { l: 92, r: 24, t: 50, b: 78 }, yDom = [1, 4], axes = true, best = true, ticks = true,
                          bestR = 30, bestLabel = true } = {}) {
  const L = D.land, svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear(L.base, [m.l, W - m.r]), y = d3.scaleLinear(yDom, [H - m.b, m.t]);
  const clip = "clip" + sel.replace(/[^a-z0-9]/gi, "");
  svg.append("defs").append("clipPath").attr("id", clip).append("rect").attr("x", m.l).attr("y", m.t)
    .attr("width", W - m.l - m.r).attr("height", H - m.t - m.b).attr("rx", 24);
  const root = svg.append("g").attr("clip-path", `url(#${clip})`);
  root.append("rect").attr("x", m.l).attr("y", m.t).attr("width", W - m.l - m.r).attr("height", H - m.t - m.b).attr("fill", css("--surface2"));
  const gx = (L.base[1] - L.base[0]) / (L.nx - 1), gy = (L.per_km[1] - L.per_km[0]) / (L.ny - 1);
  // 网格下标 → 数据坐标 → 像素（行 0 是每公里最小，画在最下面）
  const proj = d3.geoTransform({ point(px, py) { this.stream.point(x(L.base[0] + (px - .5) * gx), y(L.per_km[0] + (py - .5) * gy)); } });
  const gpath = d3.geoPath(proj);
  const cs = d3.contours().size([L.nx, L.ny]).thresholds(L.levels)(L.z);
  const land = root.append("g");
  cs.forEach(c => land.append("path").attr("d", gpath(c)).attr("fill", css("--accent")).attr("fill-opacity", .085));
  const lines = cs.map(c => land.append("path").attr("d", gpath(c)).attr("fill", "none").attr("stroke", css("--accent"))
    .attr("stroke-opacity", .6).attr("stroke-width", 2).node());
  const over = svg.append("g").attr("clip-path", `url(#${clip})`), top = svg.append("g");
  let axG = null;
  if (axes) {
    axG = svg.append("g");
    const tk = (t, xx, yy, anchor) => axG.append("text").attr("x", xx).attr("y", yy).attr("text-anchor", anchor).attr("font-size", 26).attr("fill", css("--sub")).text(t);
    if (ticks) {
      [0, 5, 10, 15, 20].forEach(v => tk(v, x(v), H - m.b + 36, "middle"));
      d3.range(Math.ceil(yDom[0]), Math.floor(yDom[1]) + 1).forEach(v => tk(v, m.l - 16, y(v) + 9, "end"));
    }
    axG.append("text").attr("x", W - m.r).attr("y", H - m.b + 70).attr("text-anchor", "end").attr("font-size", 28).attr("font-weight", 600)
      .attr("fill", css("--ink2")).text(EDU.tr("起步价（元）", "Base fare ($)"));
    axG.append("text").attr("x", m.l).attr("y", m.t - 16).attr("font-size", 28).attr("font-weight", 600)
      .attr("fill", css("--ink2")).text(EDU.tr("每公里（元）", "Per km ($)"));
  }
  let bestDot = null, bestLab = null;
  if (best) {
    bestDot = top.append("circle").attr("cx", x(D.best.base)).attr("cy", y(D.best.per_km)).attr("r", bestR).attr("fill", "none")
      .attr("stroke", css("--d-good")).attr("stroke-width", bestR >= 20 ? 7 : 4).node();
    if (bestLabel) bestLab = top.append("text").attr("x", x(D.best.base) + 30).attr("y", y(D.best.per_km) - 24 - (bestR - 30)).attr("font-size", 34)
      .attr("font-weight", 600).attr("fill", css("--d-good")).attr("paint-order", "stroke").attr("stroke", css("--surface2")).attr("stroke-width", 8)
      .attr("stroke-linejoin", "round").text(EDU.tr("最低点", "Lowest point")).node();
  }
  const api = {
    svg, x, y, W, H, m, over, top, land: land.node(), lines, axG: axG && axG.node(), bestDot, bestLab,
    px: p => [x(p[0]), y(p[1])],
    dot(p, color = "--ink", r = 16) {
      return top.append("circle").attr("cx", x(p[0])).attr("cy", y(p[1])).attr("r", r).attr("fill", css(color))
        .attr("stroke", css("--surface")).attr("stroke-width", 5).node();
    },
    /* 一条走过的路（折线），配合 walk() 按进度画出来 */
    trail(color = "--ink", w = 5, dash = null) {
      const pl = over.append("polyline").attr("fill", "none").attr("stroke", css(color)).attr("stroke-width", w)
        .attr("stroke-linejoin", "round").attr("stroke-linecap", "round").node();
      if (dash) pl.setAttribute("stroke-dasharray", dash);
      return pl;
    },
    /* 每一步落脚处的小点（只画前 n 个） */
    steps(path, n, color = "--ink", r = 7) {
      return path.p.slice(0, n).map(q => over.append("circle").attr("cx", x(q[0])).attr("cy", y(q[1])).attr("r", r).attr("fill", css(color)).node());
    },
    /* 从 p 出发、沿屏幕方向 (ux, uy)（像素，向下为正）画一支长 len 的箭头 */
    arrow(p, ux, uy, len, color = "--ink", w = 7) {
      const g = top.append("g").attr("color", css(color)), n = Math.hypot(ux, uy);
      const x0 = x(p[0]), y0 = y(p[1]), x1 = x0 + ux / n * len, y1 = y0 + uy / n * len;
      g.append("line").attr("x1", x0).attr("y1", y0).attr("x2", x1).attr("y2", y1).attr("stroke", "currentColor").attr("stroke-width", w).attr("stroke-linecap", "round");
      const a = Math.atan2(y1 - y0, x1 - x0), h = 24;
      g.append("path").attr("d", `M${x1 + Math.cos(a) * 6},${y1 + Math.sin(a) * 6} L${x1 - h * Math.cos(a - .45)},${y1 - h * Math.sin(a - .45)} L${x1 - h * Math.cos(a + .45)},${y1 - h * Math.sin(a + .45)} Z`).attr("fill", "currentColor");
      return g.node();
    },
    /* 图上某个坐标旁放一段文字（HTML，已按语言取好），返回元素 */
    note(html, p, dx = 0, dy = 0, cls = "caption") {
      const box = document.querySelector(sel).getBoundingClientRect(), stage = document.getElementById("stage").getBoundingClientRect();
      const el = document.createElement("div");
      el.className = cls; el.style.position = "absolute"; el.style.whiteSpace = "nowrap"; el.innerHTML = html;
      el.style.left = (box.left - stage.left + x(p[0]) + dx) + "px";
      el.style.top = (box.top - stage.top + y(p[1]) + dy) + "px";
      document.getElementById("stage").appendChild(el);
      return el;
    },
  };
  return api;
}

/* 沿一条算好的路走：path = D.good 之类（k 步号、p 落点、loss 分数），从第 a 个点走到第 b 个点（下标，不是步号）。
   dot：移动的点；pl：折线（画出走过的路）；on(q, loss, k)：每帧回调（拧旋钮、改读数）；ease 缺省匀速。 */
function walk(M, path, a, b, at, d, { dot = null, pl = null, on = null, ease = "none" } = {}) {
  const o = { i: a }, P = path.p;
  const pts = P.map(q => `${M.x(q[0]).toFixed(1)},${M.y(q[1]).toFixed(1)}`);
  return EDU.tl.fromTo(o, { i: a }, { i: b, duration: d, ease, immediateRender: false, onUpdate: () => {
    const j = Math.floor(o.i), f = o.i - j, q0 = P[j], q1 = P[Math.min(j + 1, P.length - 1)];
    const q = [q0[0] + (q1[0] - q0[0]) * f, q0[1] + (q1[1] - q0[1]) * f];
    const l0 = path.loss[j], l1 = path.loss[Math.min(j + 1, P.length - 1)], k0 = path.k[j], k1 = path.k[Math.min(j + 1, P.length - 1)];
    if (dot) { dot.setAttribute("cx", M.x(q[0])); dot.setAttribute("cy", M.y(q[1])); }
    if (pl) pl.setAttribute("points", pts.slice(0, j + 1).concat(`${M.x(q[0]).toFixed(1)},${M.y(q[1]).toFixed(1)}`).join(" "));
    if (on) on(q, l0 + (l1 - l0) * f, Math.round(k0 + (k1 - k0) * f));
  } }, at);
}

/* 数字从 from 滚到 to（EDU.count 只能从 0 起） */
function countTo(el, at, from, to, d = .8, fmt = v => v.toFixed(1)) {
  const o = { v: from };
  return EDU.tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v); } }, at);
}
const money = v => EDU.tr(v.toFixed(1), "$" + v.toFixed(2));
const money2 = v => EDU.tr(v.toFixed(2), "$" + v.toFixed(2));

/* 蒙眼：整张图盖一层底色，只在 p 处留一个半径 r（像素）的小圆看得见。返回 { g, hole }，hole 的 r 可以动画。 */
function fog(M, p, r = 70, opacity = .93) {
  const id = "fog" + Math.round(Math.random() * 1e9);
  const mask = M.svg.select("defs").append("mask").attr("id", id);
  mask.append("rect").attr("width", M.W).attr("height", M.H).attr("fill", "#fff");
  const hole = mask.append("circle").attr("cx", M.x(p[0])).attr("cy", M.y(p[1])).attr("r", r).attr("fill", "#000").node();
  const g = M.svg.append("g").attr("mask", `url(#${id})`).node();
  d3.select(g).append("rect").attr("x", M.m.l).attr("y", M.m.t).attr("width", M.W - M.m.l - M.m.r).attr("height", M.H - M.m.t - M.m.b)
    .attr("rx", 18).attr("fill", css("--bg")).attr("fill-opacity", opacity);
  return { g, hole };
}
