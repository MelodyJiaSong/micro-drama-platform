/* t12 各场景共用的构件：旋钮、一天的车费图、小折线图、网络图。数据来自 scenes/data.json（data.py 算出）；颜色一律取设计规范变量（tokens.css）。
   旋钮是第 1 季统一画法（s1_bible「画面」，照 t10 的样子各期自画一份）：圆盘、一根指针、下面标读数。
     - 圆盘：白底（--surface）、细边（--hair）、柔和投影；刻度弧 270°；已拧过的那段弧琥珀（--accent），没拧到的浅灰（--hair）；指针墨黑。
   颜色含义：数据点 = 墨黑，直线（两个旋钮的老机器）= 灰，网络的曲线 = 琥珀，「差多少」= 红，学会了 = 绿。 */
const D = EDU.S.data;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const SVGNS = "http://www.w3.org/2000/svg";
const A0 = -135, A1 = 135;
const pol = (cx, cy, r, deg) => [cx + r * Math.sin(deg * Math.PI / 180), cy - r * Math.cos(deg * Math.PI / 180)];
function arcPath(cx, cy, r, a, b) {
  if (b - a < 0.01) b = a + 0.01;
  const [x0, y0] = pol(cx, cy, r, a), [x1, y1] = pol(cx, cy, r, b);
  return `M${x0},${y0} A${r},${r} 0 ${b - a > 180 ? 1 : 0} 1 ${x1},${y1}`;
}

/* 旋钮：在 parent 里放一个。opt：size、min、max、value、label、fmt、left、top、showReading。返回 { el, set(v), turn(at, from, to, d) } */
function knob(parent, opt = {}) {
  const o = Object.assign({ size: 200, min: 0, max: 10, value: 0, label: "", fmt: v => v.toFixed(1), left: 0, top: 0, showReading: true, ticks: 11 }, opt);
  const host = typeof parent === "string" ? document.querySelector(parent) : parent;
  const el = document.createElement("div");
  el.className = "knob";
  Object.assign(el.style, { position: "absolute", left: o.left + "px", top: o.top + "px", width: o.size + "px", display: "flex", flexDirection: "column", alignItems: "center" });
  const S = o.size, c = S / 2, rDisc = S * 0.40, rArc = S * 0.47, w = Math.max(2.5, S * 0.035);
  const lab = document.createElement("div");
  lab.innerHTML = o.label;
  Object.assign(lab.style, { fontSize: Math.max(22, S * 0.13) + "px", fontWeight: 600, color: "var(--sub)", whiteSpace: "nowrap", marginBottom: S * 0.04 + "px", display: o.label ? "block" : "none" });
  const svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("width", S); svg.setAttribute("height", S); svg.style.overflow = "visible";
  const fid = "ks" + Math.round(Math.random() * 1e9);
  svg.innerHTML = `
    <defs><filter id="${fid}" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="${S * 0.03}" stdDeviation="${S * 0.04}" flood-color="#1D1D1F" flood-opacity=".12"/></filter></defs>
    <path d="${arcPath(c, c, rArc, A0, A1)}" fill="none" stroke="${css("--hair")}" stroke-width="${w}" stroke-linecap="round"/>
    <path class="k-fill" fill="none" stroke="${css("--accent")}" stroke-width="${w}" stroke-linecap="round"/>
    <g class="k-ticks"></g>
    <circle cx="${c}" cy="${c}" r="${rDisc}" fill="${css("--surface")}" stroke="${css("--hair")}" stroke-width="${Math.max(1.5, S * 0.008)}" filter="url(#${fid})"/>
    <g class="k-ptr"><line x1="${c}" y1="${c}" x2="${c}" y2="${c - rDisc * 0.78}" stroke="${css("--ink")}" stroke-width="${Math.max(3, S * 0.05)}" stroke-linecap="round"/></g>
    <circle cx="${c}" cy="${c}" r="${Math.max(3, S * 0.05)}" fill="${css("--accent")}"/>`;
  const tg = svg.querySelector(".k-ticks");
  if (S >= 80) for (let i = 0; i < o.ticks; i++) {
    const a = A0 + (A1 - A0) * i / (o.ticks - 1), [x0, y0] = pol(c, c, rDisc * 0.86, a), [x1, y1] = pol(c, c, rDisc * (i % 5 === 0 ? 0.70 : 0.76), a);
    const t = document.createElementNS(SVGNS, "line");
    t.setAttribute("x1", x0); t.setAttribute("y1", y0); t.setAttribute("x2", x1); t.setAttribute("y2", y1);
    t.setAttribute("stroke", css("--faint")); t.setAttribute("stroke-width", Math.max(1.5, S * 0.012)); t.setAttribute("stroke-linecap", "round");
    tg.appendChild(t);
  }
  const ptr = svg.querySelector(".k-ptr"), fill = svg.querySelector(".k-fill");
  const rd = document.createElement("div");
  Object.assign(rd.style, { fontSize: Math.max(22, S * 0.22) + "px", fontWeight: 700, color: "var(--ink)", whiteSpace: "nowrap", marginTop: S * 0.02 + "px",
                            fontVariantNumeric: "tabular-nums", display: o.showReading ? "block" : "none" });
  el.append(lab, svg, rd);
  host.appendChild(el);
  const api = {
    el, value: o.value,
    set(v) {
      api.value = v;
      const k = Math.max(0, Math.min(1, (v - o.min) / (o.max - o.min))), a = A0 + (A1 - A0) * k;
      ptr.setAttribute("transform", `rotate(${a} ${c} ${c})`);
      fill.setAttribute("d", arcPath(c, c, rArc, A0, a));
      fill.style.opacity = k < 0.004 ? 0 : 1;
      rd.textContent = o.fmt(v);
    },
    turn(at, from, to, d = 1.2) {
      const s = { v: from };
      return EDU.tl.fromTo(s, { v: from }, { v: to, duration: d, ease: "power2.inOut", immediateRender: false, onUpdate: () => api.set(s.v) }, at);
    },
  };
  api.set(o.value);
  return api;
}

/* 一天的车费图：横轴出发时刻 0–24 点，纵轴车费。返回 api：dots、line（两个旋钮的直线）、curve(arr, col) 画一条曲线、gaps（差多少）、mark 文字。 */
function dayChart(sel, { W = 1100, H = 620, fare = [14, 42], ticksY = [20, 30, 40] } = {}) {
  const m = { l: 96, r: 30, t: 40, b: 86 };
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear([0, 24], [m.l, W - m.r]), y = d3.scaleLinear(fare, [H - m.b, m.t]);
  const g = svg.append("g");
  g.append("line").attr("class", "axis-base").attr("x1", m.l).attr("x2", W - m.r).attr("y1", y(fare[0])).attr("y2", y(fare[0]));
  const tick = (t, xx, yy, anchor) => g.append("text").attr("x", xx).attr("y", yy).attr("text-anchor", anchor).attr("font-size", 24).attr("fill", css("--sub")).text(t);
  [0, 6, 12, 18, 24].forEach(k => tick(k, x(k), y(fare[0]) + 36, "middle"));
  ticksY.forEach(f => tick(f, m.l - 18, y(f) + 8, "end"));
  const axX = g.append("text").attr("x", W - m.r).attr("y", y(fare[0]) + 76).attr("text-anchor", "end").attr("font-size", 28).attr("font-weight", 600)
    .attr("fill", css("--ink2")).text(EDU.tr("出发时刻（点）", "Hour")).node();
  const axY = g.append("text").attr("x", m.l - 70).attr("y", m.t - 14).attr("font-size", 28).attr("font-weight", 600)
    .attr("fill", css("--ink2")).text(EDU.tr("车费（元）", "Fare ($)")).node();
  const cid = "clip" + sel.replace(/[^a-z0-9]/gi, "");
  svg.append("defs").append("clipPath").attr("id", cid).append("rect").attr("x", m.l).attr("y", 0).attr("width", W - m.r - m.l).attr("height", y(fare[0]));
  const gapG = svg.append("g").attr("clip-path", `url(#${cid})`), lineG = svg.append("g").attr("clip-path", `url(#${cid})`),
        dotG = svg.append("g"), over = svg.append("g");
  const lineY = h => D.line.b + D.line.k * h;
  const gaps = D.rides.map(r => gapG.append("line").attr("x1", x(r.h)).attr("x2", x(r.h)).attr("y1", y(r.fare)).attr("y2", y(lineY(r.h)))
    .attr("stroke", css("--d-bad")).attr("stroke-width", 4).attr("stroke-linecap", "round").attr("opacity", .75).node());
  const line = lineG.append("line").attr("x1", x(0)).attr("x2", x(24)).attr("y1", y(lineY(0))).attr("y2", y(lineY(24)))
    .attr("stroke", css("--d-neutral")).attr("stroke-width", 7).attr("stroke-linecap", "round").node();
  const dots = D.rides.map(r => dotG.append("circle").attr("cx", x(r.h)).attr("cy", y(r.fare)).attr("r", 9).attr("fill", css("--ink")).node());
  const pathOf = arr => d3.line().x((v, i) => x(D.hh[i])).y(v => y(v))(arr);
  const api = {
    svg, x, y, W, H, g, over, axX, axY, dots, line, gaps, lineG, pathOf,
    curve(arr, col = "--accent", w = 7) {
      return lineG.append("path").attr("d", pathOf(arr)).attr("fill", "none").attr("stroke", css(col)).attr("stroke-width", w)
        .attr("stroke-linejoin", "round").attr("stroke-linecap", "round").node();
    },
    /* 图上某处放一段 HTML 文字（已按语言取好） */
    note(html, h, f, dx = 0, dy = 0, cls = "caption") {
      const box = document.querySelector(sel).getBoundingClientRect(), stage = document.getElementById("stage").getBoundingClientRect();
      const el = document.createElement("div");
      el.className = cls; el.style.position = "absolute"; el.style.whiteSpace = "nowrap"; el.innerHTML = html;
      el.style.left = (box.left - stage.left + x(h) + dx) + "px";
      el.style.top = (box.top - stage.top + y(f) + dy) + "px";
      document.getElementById("stage").appendChild(el);
      return el;
    },
  };
  return api;
}

/* 小折线图（无刻度）：xs、多条 ys，返回 { svg, path(ys, col, w), x, y } */
function miniPlot(sel, { W = 600, H = 360, xd = [0, 1], yd = [0, 1], base = true } = {}) {
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const x = d3.scaleLinear(xd, [10, W - 10]), y = d3.scaleLinear(yd, [H - 10, 10]);
  if (base) svg.append("line").attr("class", "axis-base").attr("x1", 10).attr("x2", W - 10).attr("y1", y(0)).attr("y2", y(0));
  return {
    svg, x, y,
    path(xs, ys, col = "--accent", w = 6, dash = null) {
      const p = svg.append("path").attr("d", d3.line().x((v, i) => x(xs[i])).y(v => y(v))(ys)).attr("fill", "none")
        .attr("stroke", css(col)).attr("stroke-width", w).attr("stroke-linejoin", "round").attr("stroke-linecap", "round").node();
      if (dash) p.setAttribute("stroke-dasharray", dash);
      return p;
    },
  };
}

/* 网络图：左一个输入、中间 n 个小单元（每个里画一个小折线）、右一个输出；返回各节点与连线 */
function netDiagram(sel, { W = 900, H = 640, n = 12, inLabel = "", outLabel = "" } = {}) {
  const svg = d3.select(sel).attr("width", W).attr("height", H);
  const xi = 110, xh = W / 2, xo = W - 110, top = 40, bot = H - 40, r = Math.min(26, (bot - top) / n / 2.4);
  const hy = i => top + (bot - top) * (i + .5) / n;
  const edges = svg.append("g"), nodes = svg.append("g");
  const e1 = [], e2 = [], units = [];
  for (let i = 0; i < n; i++) {
    e1.push(edges.append("line").attr("x1", xi).attr("y1", H / 2).attr("x2", xh).attr("y2", hy(i)).attr("stroke", css("--hair")).attr("stroke-width", 3).node());
    e2.push(edges.append("line").attr("x1", xh).attr("y1", hy(i)).attr("x2", xo).attr("y2", H / 2).attr("stroke", css("--hair")).attr("stroke-width", 3).node());
  }
  for (let i = 0; i < n; i++) {
    const gu = nodes.append("g").attr("transform", `translate(${xh},${hy(i)})`);
    gu.append("circle").attr("r", r).attr("fill", css("--surface")).attr("stroke", css("--accent")).attr("stroke-width", 3.5);
    const s = r * .55, flip = i % 2 ? -1 : 1;
    gu.append("path").attr("d", `M${-s * flip},${s * .45} L${0},${s * .45} L${s * flip},${-s * .6}`).attr("fill", "none")
      .attr("stroke", css("--accent-text")).attr("stroke-width", 3).attr("stroke-linejoin", "round").attr("stroke-linecap", "round");
    units.push(gu.node());
  }
  const io = (cx, label) => {
    const gg = nodes.append("g").attr("transform", `translate(${cx},${H / 2})`);
    gg.append("circle").attr("r", 44).attr("fill", css("--ink"));
    gg.append("text").attr("y", 82).attr("text-anchor", "middle").attr("font-size", 30).attr("font-weight", 600).attr("fill", css("--ink2")).text(label);
    return gg.node();
  };
  const inp = io(xi, inLabel), out = io(xo, outLabel);
  return { svg, units, e1, e2, inp, out, xi, xh, xo, hy, r };
}
